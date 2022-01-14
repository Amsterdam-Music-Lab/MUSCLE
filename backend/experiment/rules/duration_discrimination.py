import math
import logging

import numpy as np
from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.models import Section
from .views import CompositeView, Consent, Final, Explainer, StartSession, Playlist
from .views.form import ChoiceQuestion, Form
from .util.actions import combine_actions, final_action_with_optional_button
from .util.score import get_average_difference
from .util.practice import get_trial_condition_block, get_practice_views, practice_explainer

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
        explainer = cls.intro_explanation()

        # 2. Consent with default text
        consent = Consent.action()

        explainer2 = practice_explainer()

        start_session = StartSession.action()

        return combine_actions(
            explainer,
            consent,
            explainer2,
            start_session
        )

    @classmethod
    def next_round(cls, session, request_session=None):
        if session.final_score == cls.max_turnpoints+1:
            return cls.finalize_experiment(session, request_session)

        elif session.final_score == 0:
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
    def calculate_score(result, form_element):
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
    
    @staticmethod
    def handle_result(session, section, data):
        return Base.handle_results(session, section, data)

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
        return Explainer.action(
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
        instructions = {
            'preload': '',
            'during_presentation': ''
        }
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
        form = Form([question])
        view = CompositeView(
            section=section,
            feedback_form=form.action(),
            instructions=instructions,
            title=_('%(title)s duration discrimination') % {'title': cls.condition}
        )
        config = {
            'listen_first': True,
            'decision_time': section.duration + .1
        }
        action = view.action(config)
        return action
    
    @classmethod
    def get_question_text(cls):
        return _("Is the second interval EQUALLY LONG as the first interval or LONGER?")

    @classmethod
    def intro_explanation(cls):
        task_explanation = cls.get_task_explanation()
        return Explainer.action(
            instruction=_(
                'In this test you will hear two time durations for each trial, which are marked by two tones.'),
            steps=[
                Explainer.step(
                    description=task_explanation,
                    number=1
                ),
                Explainer.step(
                    description=_(
                        'During the experiment it will become more difficult to hear the difference.'),
                    number=2
                ),
                Explainer.step(
                    description=_(
                        "Try to answer as accurately as possible, even if you're uncertain."),
                    number=3
                ),
                Explainer.step(
                    description=_(
                        'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'),
                    number=4
                )],
            button_label='Ok'
        )
    
    @classmethod
    def get_task_explanation(cls):
        return _("It's your job to decide if the second interval is EQUALLY LONG as the first interval, or LONGER.")

    @classmethod
    def finalize_experiment(cls, session, request_session):
        ''' After 8 turnpoints, finalize experiment
        Give participant feedback
        '''
        milliseconds = round(get_average_difference(session, 4) / 1000)
        score_message = cls.get_score_message(milliseconds)
        session.finish()
        session.save()
        return final_action_with_optional_button(session, score_message, request_session)
    
    @classmethod
    def get_score_message(cls, milliseconds):
        percentage = round((milliseconds / 600) * 100, 1)
        return _(
            "Well done! You heard the difference between two intervals that \
            differed only {} percent in duration.\n\nWhen we research timing in \
            humans, we often find that people's accuracy in this task scales: \
            for shorter durations, people can hear even smaller differences than for longer durations.").format(percentage)

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
                # set previous score to 4, to mark the turnpoint
                json_data = session.load_json_data()
                direction = json_data.get('direction')
                if not direction or direction == 'increase':
                    # register turnpoint
                    last_result = previous_results.first()
                    last_result.score = 4
                    last_result.save()
                    session.final_score += 1
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
                    # set previous score to 4, to mark the turnpoint
                    json_data = session.load_json_data()
                    direction = json_data.get('direction')
                    if not direction or direction == 'decrease':
                        # register turnpoint
                        last_correct_result = previous_results.first()
                        last_correct_result.score = 4
                        last_correct_result.save()
                        session.final_score += 1
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
        current_difficulty = int(difficulty * multiplier)
        session.merge_json_data({'difficulty': current_difficulty})
        session.save()
        return current_difficulty
    
    @classmethod
    def last_non_catch_correct(cls, previous_results):
        """ check if previous responses (before the current one, which is correct)
        have been catch or non-catch, and if non-catch, if they were correct
        """
        n_results = len(previous_results)
        if previous_results[1].score == 1:
            return True
        elif previous_results[1].expected_response == cls.catch_condition:
            if n_results < 3:
                # we didn't have more than 2 trials yet, so cannot check previous response
                return False
            elif previous_results[2].score == 1:
                return True
        elif previous_results[2].expected_response == cls.catch_condition and previous_results[3].score == 1:
            return True
        else:
            return False