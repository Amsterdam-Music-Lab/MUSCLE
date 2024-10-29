import logging
from decimal import Decimal, ROUND_HALF_UP

from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.actions import Trial, Explainer, Step
from experiment.actions.form import ChoiceQuestion, Form
from experiment.actions.playback import Autoplay
from experiment.rules.util.practice import get_practice_views, get_trial_condition
from experiment.actions.utils import final_action_with_optional_button, render_feedback_trivia
from experiment.actions.utils import get_average_difference_level_based
from experiment.rules.util.staircasing import register_turnpoint
from result.utils import prepare_result
from section.models import Playlist, Section
from session.models import Session

logger = logging.getLogger(__name__)

MAX_TURNPOINTS = 6


class HBat(Base):
    """ section.group (and possibly section.tag) must be convertable to int"""

    ID = 'H_BAT'
    start_diff = 20

    def next_round(self, session: Session):
        if session.final_score == 0:
            # we are practicing
            actions = get_practice_views(
                session,
                self.get_intro_explainer(),
                staircasing,
                self.next_trial_action,
                self.response_explainer,
                get_previous_condition,
                1
            )
            return actions
        # actual experiment
        previous_results = session.result_set.order_by('-created_at')
        trial_condition = get_trial_condition(2)
        if not previous_results.count():
            # first trial
            action = self.next_trial_action(session, trial_condition, 1)
            if not action:
                # participant answered first trial incorrectly (outlier)
                action = self.finalize_block(session)
        else:
            action = staircasing(session, self.next_trial_action)
            if not action:
                # action is None if the audio file doesn't exist
                action = self.finalize_block(session)
            if session.final_score == MAX_TURNPOINTS+1:
                # delete result created before this check
                session.result_set.order_by('-created_at').first().delete()
                action = self.finalize_block(session)
            return action

    def next_trial_action(self, session, trial_condition, level=1, *kwargs):
        """
        Get the next actions for the block
        trial_condition is either 1 or 0
        level can be 1 (20 ms) or higher (10, 5, 2.5 ms...)
        """
        try:
            section = session.playlist.section_set.filter(
                group=str(level)).get(tag=str(trial_condition))
        except Section.DoesNotExist:
            return None
        expected_response = 'SLOWER' if trial_condition else 'FASTER'
        key = 'longer_or_equal'
        question = ChoiceQuestion(
            key=key,
            question=_(
                "Is the rhythm going SLOWER or FASTER?"),
            choices={
                'SLOWER': _('SLOWER'),
                'FASTER': _('FASTER')
            },
            result_id=prepare_result(
                key,
                session,
                section=section,
                expected_response=expected_response,
                scoring_rule='CORRECTNESS'
            ),
            view='BUTTON_ARRAY',
            submits=True
        )
        playback = Autoplay([section])
        form = Form([question])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('Beat acceleration'),
            config={
                'response_time': section.duration + .1
            }
        )
        return view

    def get_intro_explainer(self):
        return Explainer(
            instruction=_(
                'In this test you will hear a series of tones for each trial.'),
            steps=[
                Step(_(
                    "It's your job to decide if the rhythm goes SLOWER of FASTER.")),
                Step(_(
                    'During the experiment it will become more difficult to hear the difference.')),
                Step(_(
                    "Try to answer as accurately as possible, even if you're uncertain.")),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(_(
                    "In this test, you can answer as soon as you feel you know the answer, but please wait until you are sure or the sound has stopped.")),
                Step(_(
                    'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'))
            ],
            step_numbers=True,
            button_label='Ok'
        )

    def response_explainer(self, correct, slower, button_label=_('Next fragment')):
        if correct:
            if slower:
                instruction = _(
                    'The rhythm went SLOWER. Your response was CORRECT.')
            else:
                instruction = _(
                    'The rhythm went FASTER. Your response was CORRECT.')
        else:
            if slower:
                instruction = _(
                    'The rhythm went SLOWER. Your response was INCORRECT.')
            else:
                instruction = _(
                    'The rhythm went FASTER. Your response was INCORRECT.')
        return Explainer(
            instruction=instruction,
            steps=[],
            button_label=button_label
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
    trial_condition = get_trial_condition(2)
    previous_results = session.result_set.order_by('-created_at')
    last_result = previous_results.first()
    if not last_result:
        # first trial
        action = trial_action_callback(
            session, trial_condition, 1)
    elif last_result.score == 0:
        # the previous response was incorrect
        json_data = session.json_data
        direction = json_data.get('direction')
        last_result.comment = 'decrease difficulty'
        last_result.save()
        if direction == 'increase':
            register_turnpoint(session, last_result)
        # register decreasing difficulty
        session.save_json_data({'direction': 'decrease'})
        session.save()
        level = get_previous_level(last_result) - 1  # decrease difficulty
        action = trial_action_callback(
            session, trial_condition, level)
    else:
        if previous_results.count() == 1:
            # this is the second trial, so the level is still 1
            action = trial_action_callback(
                session, trial_condition, 1)
        elif previous_results.all()[1].score == 1 and not previous_results.all()[1].comment:
            # the previous two responses were correct
            json_data = session.json_data
            direction = json_data.get('direction')
            last_result.comment = 'increase difficulty'
            last_result.save()
            if direction == 'decrease':
                # mark the turnpoint
                register_turnpoint(session, last_result)
            # register increasing difficulty
            session.save_json_data({'direction': 'increase'})
            session.save()
            level = get_previous_level(last_result) + 1  # increase difficulty
            action = trial_action_callback(
                session, trial_condition, level)
        else:
            # previous answer was correct
            # but we didn't yet get two correct in a row
            level = get_previous_level(last_result)
            action = trial_action_callback(
                session, trial_condition, level)
    if not action:
        # action is None if the audio file doesn't exist
        return None
    return action
