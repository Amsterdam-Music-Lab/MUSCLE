import math
import logging
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.models import Section
from .views import Trial, Consent, Final, Explainer, StartSession, Step, Playlist
from .views.form import ChoiceQuestion, Form
from .views.playback import Playback
from .util.actions import combine_actions, final_action_with_optional_button, render_feedback_trivia
from .util.score import get_average_difference
from .util.practice import get_trial_condition_block, get_practice_views, practice_explainer
from .util.staircasing import register_turnpoint

logger = logging.getLogger(__name__)

class DurationDiscrimination(Base):
    """
    These rules make use of the session's final_score to register turnpoints
    """
    ID = 'DURATION_DISCRIMINATION'
    condition = _('interval')
    start_diff = 400000
    max_turnpoints = 8
    catch_condition = 'EQUAL'
    block_size = 5
    increase_difficulty_multiplier = .5
    decrease_difficulty_multiplier = 1.5

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds"""
        explainer = cls.intro_explanation().action(True)

        # 2. Consent with default text
        consent = Consent.action()

        explainer2 = practice_explainer().action()

        start_session = StartSession.action()

        return combine_actions(
            explainer,
            consent,
            explainer2,
            start_session
        )

    @classmethod
    def next_round(cls, session, request_session=None):
        if session.final_score == 0:
            cls.register_difficulty(session)
            # we are practicing
            actions = get_practice_views(
                session,
                cls.intro_explanation(),
                cls.staircasing_blocks,
                cls.next_trial_action,
                cls.get_response_explainer,
                cls.get_previous_condition,
                cls.get_difficulty(session))
            return actions

        else:
            ##### Actual trials ####
            action = cls.staircasing_blocks(session, cls.next_trial_action, request_session)
            return action

    @staticmethod
    def calculate_score(result, form_element, data):
        # a result's score is used to keep track of how many correct results were in a row
        # for catch trial, set score to 2 -> not counted for calculating turnpoints
        try:
            expected_response = result.expected_response
        except Exception as e:
            logger.log(e)
            expected_response = None
        if expected_response and expected_response == form_element['value']:
            if expected_response == 'LONGER':
                return 1
            else:
                return 2
        else:
            return 0

    @classmethod
    def register_difficulty(cls, session):
        session.merge_json_data({'difficulty': cls.start_diff})
        session.save()

    @classmethod
    def get_previous_condition(cls, last_result):
        return last_result.expected_response

    @classmethod
    def get_response_explainer(cls, correct, correct_response, button_label=_('Next fragment')):
        preposition = _('than') if correct_response=='LONGER' else _('as')
        correct_response = _('LONGER') if correct_response=='LONGER' else _('EQUAL')
        if correct:
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

    @classmethod
    def next_trial_action(cls, session, trial_condition, difficulty):
        """
        Provide the next trial action
        Arguments:
        - session: the session
        - trial_condition: 1 for catch trial, 0 for normal trial
        - difficulty: difficulty of the trial (translates to file name)
        """
        if trial_condition == 1:
            # catch trial
            difference = 0
        else:
            difference = difficulty
        try:
            section = session.playlist.section_set.get(name=difference)
        except Section.DoesNotExist:
            return None
        expected_result = 'EQUAL' if difference == 0 else 'LONGER'
        # create Result object and save expected result to database
        result_pk = Base.prepare_result(session, section, expected_result)
        question_text = cls.get_question_text()
        question = ChoiceQuestion(
            question=question_text,
            key='longer_or_equal',
            choices={
                'EQUAL': _('EQUALLY LONG'),
                'LONGER': _('LONGER')
            },
            view='BUTTON_ARRAY',
            result_id=result_pk,
            submits=True
        )
        playback = Playback([section])
        form = Form([question])
        view = Trial(
            playback=playback,
            feedback_form=form,
            title=_('%(title)s duration discrimination') % {'title': cls.condition},
            config={
                'listen_first': True,
                'decision_time': section.duration + .5
            }
        )
        return view.action()

    @classmethod
    def get_question_text(cls):
        return _("Is the second interval EQUALLY LONG as the first interval or LONGER?")

    @classmethod
    def intro_explanation(cls):
        return Explainer(
            instruction=cls.get_introduction(),
            steps=[
                Step(cls.get_task_explanation()),
                Step(_(
                        'During the experiment it will become more difficult to hear the difference.')),
                Step(_(
                        "Try to answer as accurately as possible, even if you're uncertain.")),
                Step(_("Remember: try not to move or tap along with the sounds")),
                Step(_(
                        'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'))
            ],
            button_label='Ok'
        )

    @classmethod
    def get_task_explanation(cls):
        return _("It's your job to decide if the second interval is EQUALLY LONG as the first interval, or LONGER.")

    @classmethod
    def get_introduction(cls):
        return _('In this test you will hear two time durations for each trial, which are marked by two tones.')

    @classmethod
    def finalize_experiment(cls, session, request_session):
        ''' After 8 turnpoints, finalize experiment
        Give participant feedback
        '''
        difference = get_average_difference(session, 4, cls.start_diff)
        final_text = cls.get_final_text(difference)
        session.finish()
        session.save()
        return final_action_with_optional_button(session, final_text, request_session)

    @classmethod
    def get_final_text(cls, difference):
        percentage = round(difference / 6000, 2)
        feedback = _(
            "Well done! You heard the difference between two intervals that \
            differed only {} percent in duration.").format(percentage)
        trivia = _("When we research timing in \
            humans, we often find that people's accuracy in this task scales: \
            for shorter durations, people can hear even smaller differences than for longer durations.")
        return render_feedback_trivia(feedback, trivia)

    @classmethod
    def staircasing_blocks(cls, session, trial_action_callback, request_session=None):
        """ Calculate staircasing procedure in blocks of 5 trials with one catch trial
        Arguments:
        - session: the session
        - trial_action_callback: function to build a trial action
        - optional: condition: if the explainers from duration_discrimination are reused, set condition
        """
        previous_results = session.result_set.order_by('-created_at')
        trial_condition = get_trial_condition_block(session, cls.block_size)
        if not previous_results.count():
            # first trial
            difficulty = cls.get_difficulty(session)
            return trial_action_callback(session, trial_condition, difficulty)
        previous_condition = previous_results.first().expected_response
        if previous_condition == cls.catch_condition:
            # last trial was catch trial, don't calculate turnpoints
            # don't manipulate duration
            difficulty = cls.get_difficulty(session)
            action = trial_action_callback(
                session,
                trial_condition,
                difficulty)
        else:
            if previous_results.first().score == 0:
                # the previous response was incorrect
                json_data = session.load_json_data()
                direction = json_data.get('direction')
                last_result = previous_results.first()
                last_result.comment = 'decrease difficulty'
                last_result.save()
                if direction == 'increase':
                    # register turnpoint
                    register_turnpoint(session, last_result)
                if session.final_score == cls.max_turnpoints + 1:
                    # experiment is finished, None will be replaced by final view
                    action = None
                else:
                    # register decreasing difficulty
                    session.merge_json_data({'direction': 'decrease'})
                    session.save()
                    # decrease difficulty
                    difficulty = cls.get_difficulty(session, cls.decrease_difficulty_multiplier)
                    action = trial_action_callback(
                        session,
                        trial_condition,
                        difficulty)
            else:
                # the previous response was correct - check if previous non-catch trial was 1
                if previous_results.count() > 1 and cls.last_non_catch_correct(previous_results.all()):
                    # the previous two responses were correct
                    json_data = session.load_json_data()
                    direction = json_data.get('direction')
                    last_correct_result = previous_results.first()
                    last_correct_result.comment = 'increase difficulty'
                    last_correct_result.save()
                    if direction == 'decrease':
                        # register turnpoint
                        register_turnpoint(session, last_correct_result)
                    if session.final_score == cls.max_turnpoints + 1:
                        # experiment is finished, None will be replaced by final view
                        action = None
                    else:
                        # register increasing difficulty
                        session.merge_json_data({'direction': 'increase'})
                        session.save()
                        # increase difficulty
                        difficulty = cls.get_difficulty(session, cls.increase_difficulty_multiplier)
                        action = trial_action_callback(
                            session,
                            trial_condition,
                            difficulty)
                else:
                    difficulty = cls.get_difficulty(session)
                    action = trial_action_callback(
                        session,
                        trial_condition,
                        difficulty)
        if not action:
            # action is None if the audio file doesn't exist
            return cls.finalize_experiment(session, request_session)
        return action

    @classmethod
    def get_difficulty(cls, session, multiplier=1.0):
        '''
         - multiplier:
            1.5 multiplier for difference *increase*
            1 if difference should stay the same
            0.5 for difference *decrease*
        '''
        json_data = session.load_json_data()
        difficulty = json_data.get('difficulty')
        current_difficulty = difficulty * multiplier
        session.merge_json_data({'difficulty': current_difficulty})
        session.save()
        # return rounded difficulty
        # this uses the decimal module, since round() does not work entirely as expected
        return int(Decimal(str(current_difficulty)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

    @classmethod
    def last_non_catch_correct(cls, previous_results):
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
            elif result.expected_response == cls.catch_condition:
                continue
            else:
                break
        return answer
