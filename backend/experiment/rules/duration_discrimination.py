import logging
from decimal import Decimal, ROUND_HALF_UP
import random

from django.utils.translation import gettext_lazy as _

from .base import BaseRules
from .practice import PracticeMixin
from section.models import Section
from experiment.actions.playback import Autoplay
from experiment.actions.explainer import Explainer, Step
from experiment.actions.form import Form
from experiment.actions.question import ButtonArrayQuestion
from experiment.actions.trial import Trial
from experiment.actions.utils import (
    final_action_with_optional_button,
    get_average_difference,
    render_feedback_trivia,
)
from experiment.rules.util.staircasing import register_turnpoint
from result.models import Result
from result.utils import prepare_result
from section.models import Playlist
from session.models import Session

logger = logging.getLogger(__name__)


class DurationDiscrimination(BaseRules, PracticeMixin):
    """
    These rules make use of the session's final_score to register turnpoints
    """
    ID = 'DURATION_DISCRIMINATION'
    task_description = _("Duration discrimination")
    subtask = _("Interval")
    start_diff = 400000
    max_turnpoints = 8
    first_condition = "longer"
    first_condition_i18n = _("LONGER")
    second_condition = "equal"  # second condition is 'catch' condition
    second_condition_i18n = _("EQUAL")
    n_practice_rounds_second_condition = 2
    block_size = 5
    section_count = 247
    increase_difficulty_multiplier = .5
    decrease_difficulty_multiplier = 1.5

    def next_round(self, session: Session) -> list:
        practice_finished = session.json_data.get("practice_done")
        if not practice_finished:
            # we are practicing
            return self.next_practice_round(session)

        else:
            # Actual trials
            return self.staircasing_blocks(session)

    def calculate_score(self, result: Result, data: dict) -> int:
        # a result's score is used to keep track of how many correct results were in a row
        # for catch condition, set score to 2 -> not counted for calculating turnpoints
        try:
            expected_response = result.expected_response
        except Exception as e:
            logger.log(e)
            expected_response = None
        if expected_response and expected_response == result.given_response:
            if expected_response == self.first_condition:
                return 1
            else:
                return 2
        else:
            return 0

    def get_feedback_explainer(self, session):
        button_label = _("Next fragment")
        correct_response, is_correct = self.get_condition_and_correctness(session)
        preposition = _("than") if is_correct else _("as")
        if is_correct:
            instruction = _(
                'The second interval was %(correct_response)s %(preposition)s the first interval. Your answer was CORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        else:
            instruction = _(
                'The second interval was %(correct_response)s %(preposition)s the first interval. Your answer was INCORRECT.') % {'correct_response': correct_response, 'preposition': preposition}
        return Explainer(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )

    def get_next_trial(self, session: Session) -> Trial:
        """
        Provide the next trial action

        Args:
            session: the session
            trial_condition: string defined by second_condition for catch trial, first_condition for normal trial
            difficulty: difficulty of the trial (translates to file name)
        """
        trial_condition = self.get_condition(session)
        difficulty = self.get_difficulty(session)
        if trial_condition == self.second_condition:
            # catch trial
            difference = 0
        else:
            difference = difficulty
        try:
            section = session.playlist.section_set.get(song__name=difference)
        except Section.DoesNotExist:
            return None
        question_text = self.get_question_text()
        key = self.task_description.replace(" ", "_")
        question = ButtonArrayQuestion(
            text=question_text,
            key=key,
            choices={
                self.first_condition: self.first_condition_i18n,
                self.second_condition: self.second_condition_i18n,
            },
            result_id=prepare_result(
                key, session, section=section, expected_response=trial_condition
            ),
        )

        playback = Autoplay([section])
        form = Form([question], submit_label="")
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_("%(title)s %(task)s")
            % {"title": self.subtask, "task": self.task_description},
            config={"listen_first": True, "response_time": section.duration + 0.1},
        )
        return view

    def get_question_text(self):
        return _("Is the second interval EQUALLY LONG as the first interval or LONGER?")

    def get_intro_explainer(self):
        return Explainer(
            instruction=self.get_introduction(),
            steps=[
                Step(self.get_task_explanation()),
                Step(_(
                    'During the experiment it will become more difficult to hear the difference.')),
                Step(_(
                    "Try to answer as accurately as possible, even if you're uncertain.")),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(_(
                    'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'))
            ],
            button_label='Ok',
            step_numbers=True
        )

    def get_task_explanation(self):
        return _("It's your job to decide if the second interval is EQUALLY LONG as the first interval, or LONGER.")

    def get_introduction(self):
        return _('In this test you will hear two time durations for each trial, which are marked by two tones.')

    def finalize_block(self, session):
        ''' After 8 turnpoints, finalize experiment
        Give participant feedback
        '''
        difference = get_average_difference(session, 4, self.start_diff)
        final_text = self.get_final_text(difference)
        session.finish()
        session.save()
        return final_action_with_optional_button(session, final_text)

    def get_final_text(self, difference):
        percentage = round(difference / 6000, 2)
        feedback = _(
            "Well done! You heard the difference between two intervals that \
            differed only {} percent in duration.").format(percentage)
        trivia = _("When we research timing in \
            humans, we often find that people's accuracy in this task scales: \
            for shorter durations, people can hear even smaller differences than for longer durations.")
        return render_feedback_trivia(feedback, trivia)

    def staircasing_blocks(self, session):
        """Calculate staircasing procedure in blocks of 5 trials with one catch trial

        Args:
            session: the session

        Returns:
            a Trial object
        """
        previous_results = session.result_set.order_by("-created_at")
        if not previous_results.count():
            # first trial
            return self.get_next_trial(session)
        previous_condition = previous_results.first().expected_response
        if previous_condition == self.second_condition:
            # last trial was catch trial, don't calculate turnpoints
            # don't manipulate duration
            action = self.get_next_trial(session)
        else:
            if previous_results.first().score == 0:
                # the previous response was incorrect
                direction = session.json_data.get("direction")
                last_result = previous_results.first()
                last_result.save_json_data(
                    {"multiplier": self.decrease_difficulty_multiplier}
                )
                if direction == 'increase':
                    # register turnpoint
                    register_turnpoint(session, last_result)
                if session.final_score == self.max_turnpoints + 1:
                    # experiment is finished, None will be replaced by final view
                    return None
                else:
                    # register decreasing difficulty
                    session.save_json_data({"direction": "decrease"})
                    # decrease difficulty
                    action = self.get_next_trial(session)
            else:
                # the previous response was correct - check if previous non-catch trial was 1
                if previous_results.count() > 1 and self.last_non_catch_correct(previous_results.all()):
                    # the previous two responses were correct
                    direction = session.json_data.get("direction")
                    last_correct_result = previous_results.first()
                    last_correct_result.save_json_data(
                        {"multiplier": self.increase_difficulty_multiplier}
                    )
                    if direction == 'decrease':
                        # register turnpoint
                        register_turnpoint(session, last_correct_result)
                    if session.final_score == self.max_turnpoints + 1:
                        # experiment is finished, None will be replaced by final view
                        action = None
                    else:
                        # register increasing difficulty
                        session.save_json_data({"direction": "increase"})
                        # increase difficulty
                        action = self.get_next_trial(session)
                else:
                    action = self.get_next_trial(session)
        if not action:
            # action is None if the audio file doesn't exist
            return self.finalize_block(session)
        return action

    def get_difficulty(self, session: Session) -> int:
        """
        Args:
            session: the session
            multiplier: float with three different possible values:
                1.5 multiplier for difference *increase*
                1 if difference should stay the same
                0.5 for difference *decrease*

        Returns:
            an integer indicating the inter-onset-interval in milliseconds
        """
        difficulty = session.json_data.get("difficulty")
        if not difficulty:
            difficulty = self.start_diff
            session.save_json_data({"difficulty": self.start_diff})
            return difficulty
        if not session.json_data.get("practice_done"):
            return difficulty
        last_result = session.last_result()
        if not last_result:
            return difficulty
        multiplier = last_result.json_data.get("multiplier", 1.0)
        current_difficulty = difficulty * multiplier
        session.save_json_data({"difficulty": current_difficulty})
        # return rounded difficulty
        # this uses the decimal module, since round() does not work entirely as expected
        return int(Decimal(str(current_difficulty)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

    def last_non_catch_correct(self, previous_results: list[Result]) -> bool:
        """ check if previous responses (before the current one, which is correct)
        have been catch or non-catch, and if non-catch, if they were correct
        """
        n_results = len(previous_results)
        # get the previous scores and conditions, from most to least recent
        results = [previous_results[r] for r in range(1, n_results)]
        answer = False
        while results:
            result = results.pop(0)
            if result.score == 1:
                if result.comment:
                    # a comment on the second-to-last result indicates that difficulty changed there;
                    # we need to wait for another correct response before changing again
                    break
                else:
                    answer = True
                    break
            elif result.expected_response == self.second_condition:
                continue
            else:
                break
        return answer

    def practice_successful(self, session: Session) -> bool:
        previous_results = session.last_n_results(n_results=2)
        return all(r.score > 0 for r in previous_results)

    def get_condition(self, session: Session) -> str:
        if not session.json_data.get("practice_done"):
            return super().get_condition(session)
        else:
            return self.get_trial_condition(session)

    def get_trial_condition(self, session: Session) -> str:
        """make a list of the {block_size} conditions, of which one is a catch condition
        store updates in the session.json_data field
        """
        current_trials = session.json_data.get("current_trials")
        if not current_trials:
            current_trials = [self.first_condition] * (self.block_size - 1) + [
                self.second_condition
            ]
            random.shuffle(current_trials)
        condition = current_trials.pop()
        session.save_json_data({"current_trials": current_trials})
        session.save()
        return condition

    def validate_playlist(self, playlist: Playlist):
        errors = []
        errors += super().validate_playlist(playlist)
        sections = playlist.section_set.all()
        if sections.count() is not self.section_count:
            errors.append("The playlist should contain 247 sections")
        try:
            numerical_song_names = [int(section.song_name()) for section in sections]
            if self.start_diff not in numerical_song_names:
                errors.append(
                    f"The file for the starting difference of {self.start_diff} is missing"
                )
        except:
            errors.append(
                "The sections should have an associated song with an integer name"
            )

        return errors
