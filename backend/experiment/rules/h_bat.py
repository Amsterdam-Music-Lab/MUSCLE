import logging
from decimal import Decimal, ROUND_HALF_UP
import random

from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from .practice import PracticeMixin
from experiment.actions.button import Button
from experiment.actions.explainer import Explainer, Step
from experiment.actions.form import Form
from experiment.actions.playback import Autoplay, PlaybackSection
from experiment.actions.question import ButtonArrayQuestion
from experiment.actions.trial import Trial
from experiment.actions.utils import (
    get_average_difference_level_based,
    render_feedback_trivia,
)
from experiment.actions.wrappers import final_action_with_optional_button
from experiment.rules.util.staircasing import register_turnpoint
from result.utils import prepare_result
from section.models import Playlist, Section
from session.models import Session

logger = logging.getLogger(__name__)

MAX_TURNPOINTS = 6


class HBat(BaseRules, PracticeMixin):
    """Harvard Beat Assessment Test (H-BAT)
    Fujii & Schlaug, 2013
    """

    ID = 'H_BAT'
    start_diff = 20
    n_practice_rounds_second_condition = 2
    first_condition = "slower"
    first_condition_i18n = _("SLOWER")
    second_condition = "faster"
    second_condition_i18n = _("FASTER")

    def next_round(self, session: Session) -> list:
        practice_finished = session.json_data.get("practice_done")
        if not practice_finished:
            return self.next_practice_round(session)
        else:
            # actual experiment
            action = staircasing(session, self.get_next_trial)
            if not action:
                # action is None if the audio file doesn't exist
                action = self.finalize_block(session)
            if session.final_score == MAX_TURNPOINTS + 1:
                # delete result created before this check
                session.result_set.order_by("-created_at").first().delete()
                action = self.finalize_block(session)
            return action

    def get_condition(self, session) -> int:
        """get the condition of the trial, which depends either on json data (practice),
        or is random choice between faster / slower
        """
        if not session.json_data.get("practice_done"):
            return super().get_condition(session)
        else:
            return random.choice([self.first_condition, self.second_condition])

    def get_difficulty(self, session: Session) -> int:
        last_result = session.last_result()
        if not last_result:
            return 1
        else:
            current_difficulty = int(last_result.section.group)
            if last_result.json_data.get("difficulty") == "decrease":
                return current_difficulty - 1
            elif last_result.json_data.get("difficulty") == "increase":
                return current_difficulty + 1
            return current_difficulty

    def get_next_trial(self, session: Session, *kwargs) -> Trial:
        """
        Get the next actions for the block
        trial_condition is either 1 or 0
        level can be 1 (20 ms) or higher (10, 5, 2.5 ms...)
        """
        level = self.get_difficulty(session)
        trial_condition = self.get_condition(session)
        trial_tag = "1" if trial_condition == self.first_condition else "0"
        try:
            section = session.playlist.get_section(
                {"group": str(level), "tag": trial_tag}
            )
        except Section.DoesNotExist:
            # we are out of valid sections, end experiment
            return None

        key = "slower_or_faster"
        question = ButtonArrayQuestion(
            key=key,
            text=self.get_trial_question(),
            choices={
                self.first_condition: self.first_condition_i18n,
                self.second_condition: self.second_condition_i18n,
            },
            result_id=prepare_result(
                key,
                session,
                section=section,
                expected_response=trial_condition,
                scoring_rule="CORRECTNESS",
            ),
        )
        playback = Autoplay(sections=[PlaybackSection(section)], show_animation=False)
        form = Form([question], submit_button=None)
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=self.get_trial_title(),
            response_time=section.duration + 0.1,
        )
        return view

    def get_trial_question(self):
        return _("Is the rhythm going SLOWER or FASTER?")

    def get_trial_title(self):
        return _("Beat acceleration")

    def get_intro_explainer(self):
        return Explainer(
            instruction=_(
                'In this test you will hear a series of tones for each trial.'
            ),
            steps=[
                Step(_("It's your job to decide if the rhythm goes SLOWER of FASTER.")),
                Step(
                    _(
                        'During the experiment it will become more difficult to hear the difference.'
                    )
                ),
                Step(
                    _(
                        "Try to answer as accurately as possible, even if you're uncertain."
                    )
                ),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(
                    _(
                        "In this test, you can answer as soon as you feel you know the answer, but please wait until you are sure or the sound has stopped."
                    )
                ),
                Step(
                    _(
                        'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'
                    )
                ),
            ],
            step_numbers=True,
            button=Button('Ok'),
        )

    def get_feedback_explainer(self, session: Session):
        correct_response, is_correct = self.get_condition_and_correctness(session)
        if is_correct:
            instruction = _(
                "The rhythm went %(correct_response)s. Your response was CORRECT."
            ) % {"correct_response": correct_response}
        else:
            instruction = _(
                "The rhythm went %(correct_response)s. Your response was INCORRECT."
            ) % {"correct_response": correct_response}
        return Explainer(
            instruction=instruction, steps=[], button=Button(_("Next fragment"))
        )

    def finalize_block(self, session):
        """ if either the max_turnpoints have been reached,
        or if the section couldn't be found (outlier), stop the experiment
        """
        average_diff = get_average_difference_level_based(
            session, 6, self.start_diff)
        percentage = float(Decimal(str(average_diff / 5)
                                   ).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        feedback = _("Well done! You heard the difference when the rhythm was \
                    speeding up or slowing down with only {} percent!").format(percentage)
        trivia = self.get_trivia()
        final_text = render_feedback_trivia(feedback, trivia)
        session.finish()
        session.save()
        return final_action_with_optional_button(session, final_text)

    def get_trivia(self):
        return _("When people listen to music, they often perceive an underlying regular pulse, like the woodblock \
            in this task. This allows us to clap along with the music at a concert and dance together in synchrony.")

    def practice_successful(self, session: Session) -> bool:
        previous_results = session.last_n_results(n_results=2)
        return all(r.score > 0 for r in previous_results)

    def validate_playlist(self, playlist: Playlist):
        errors = []
        errors += super().validate_playlist(playlist)
        sections = playlist.section_set.all()
        if sections.count() != 32:
            errors.append("This block should have a playlist with 32 sections")
        groups, tags = zip(*[(s.group, s.tag) for s in sections])
        try:
            group_numbers = sorted(list(set([int(g) for g in groups])))
            if group_numbers != [*range(1, 17)]:
                errors.append("Groups should be ascending integers from 1 to 16")
        except:
            errors.append("The groups should be integers")
        try:
            tag_numbers = sorted(list(set([int(t) for t in tags])))
            if tag_numbers != [0, 1]:
                errors.append("Tags should be 0 and 1")
        except:
            errors.append("Tags should be integers")

        return errors


def get_previous_condition(previous_result):
    """ check if previous section was slower / in 2 (1) or faster / in 3 (0) """
    return int(previous_result.section.tag)


def get_previous_level(previous_result):
    return int(previous_result.section.group)


def staircasing(session, trial_action_callback):
    previous_results = session.result_set.order_by('-created_at')
    last_result = previous_results.first()
    if not last_result:
        # first trial
        action = trial_action_callback(session)
    elif last_result.score == 0:
        # the previous response was incorrect
        direction = session.json_data.get('direction')
        last_result.save_json_data({"difficulty": "decrease"})
        last_result.save()
        if direction == 'increase':
            register_turnpoint(session, last_result)
        # register decreasing difficulty
        session.save_json_data({"direction": "decrease"})
        action = trial_action_callback(session)
    else:
        if previous_results.count() == 1:
            # this is the second trial, so the level is still 1
            action = trial_action_callback(session)
        elif previous_results.all()[1].score == 1 and not previous_results.all()[1].comment:
            # the previous two responses were correct
            direction = session.json_data.get("direction")
            last_result.save_json_data({"difficulty": "increase"})
            if direction == 'decrease':
                # mark the turnpoint
                register_turnpoint(session, last_result)
            # register increasing difficulty
            session.save_json_data({"direction": "increase"})
            action = trial_action_callback(session)
        else:
            # previous answer was correct
            # but we didn't yet get two correct in a row
            action = trial_action_callback(session)
    if not action:
        # action is None if the audio file doesn't exist
        return None
    return action
