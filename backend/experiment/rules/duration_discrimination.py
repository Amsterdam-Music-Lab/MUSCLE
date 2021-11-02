import math
import logging

import numpy as np
from django.utils.translation import gettext as _

from .base import Base
from experiment.models import Section
from .views import CompositeView, Consent, Final, Explainer, StartSession, Playlist
from .views.form import ChoiceQuestion, Form
from .util.actions import combine_actions
from .util.score import get_average_difference
from .util.practice import get_trial_condition_block, get_practice_views, practice_explainer

logger = logging.getLogger(__name__)

START_DIFF = 400000
MAX_TURNPOINTS = 8


class DurationDiscrimination(Base):
    """ 
    These rules make use of the session's final_score to register turnpoints
    """
    ID = 'DURATION_DISCRIMINATION'
    condition = _('interval')

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds"""
        explainer = intro_explanation(cls.condition)

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
    def next_round(cls, session):
        if session.final_score == MAX_TURNPOINTS+1:
            return finalize_experiment(session, cls.condition)

        elif session.final_score == 0:
            # we are practicing
            actions = get_practice_views(session, intro_explanation(_('interval')), get_trial_condition_block(0, session.id, 2), cls.next_trial_action, cls.get_response_explainer, get_previous_condition)
            return actions

        else:
            ##### Actual trials ####
            action = staircasing_blocks(session, cls.next_trial_action, cls.condition)
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
    
    @staticmethod
    def handle_result(session, section, data):
        return Base.handle_results(session, section, data)

    @classmethod
    def get_response_explainer(cls, correct, longer, button_label=_('Next fragment')):
        if correct:
            if longer:
                instruction = _(
                    'The second %(type)s was LONGER than the first %(type)s. Your answer was correct.') % {'type': cls.condition}
            else:
                instruction = _(
                    'The second %(type)s was EQUALLY LONG as the first %(type)s. Your answer was correct.') % {'type': cls.condition}
        else:
            if longer:
                instruction = _(
                    'The second %(type)s was LONGER than the first %(type)s. Your answer was incorrect.') % {'type': cls.condition}
            else:
                instruction = _(
                    'The second %(type)s was EQUALLY LONG as the first %(type)s. Your answer was incorrect.') % {'type': cls.condition}
        return Explainer.action(
            instruction=instruction,
            steps=[],
            button_label=button_label
        )
    
    @classmethod
    def next_trial_action(cls, session, trial_condition, multiplier, previous_difference):
        """
        Provide the next trial action
        Arguments:
        - session: the session
        - trial_condition: 1 for catch trial, 0 for normal trial
        - multiplier: 
            1.5 multiplier for difference *increase*
            1 if difference should stay the same
            0.5 for difference *decrease*
        - previous difference: difference of previous trial
        """
        if trial_condition == 1:
            # catch trial
            difference = 0
        else:
            difference = int(previous_difference * multiplier)
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
        question = question = ChoiceQuestion(
            question=_("Is the second %(type)s LONGER than the first %(type)s or EQUALLY LONG?") % {'type': cls.condition},
            key='longer_or_equal',
            choices={
                'LONGER': _('LONGER'),
                'EQUAL': _('EQUALLY LONG')
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
            title=_('%(title)s duration discrimination') % {'title': cls.condition.title()}
        )
        config = {
            'listen_first': True,
            'decision_time': section.duration + .5
        }
        action = view.action(config)
        return action

def finalize_experiment(session, condition):
    ''' After 8 turnpoints, finalize experiment
    Give participant feedback
    '''
    milliseconds = get_average_difference(session, 4)
    if condition=='interval':
        percentage = (milliseconds / 600) * 100
        score_message = _(
            'Well done! You heard the difference between two intervals that \
            differed only {} percent in duration. When we research timing in \
            humans, we often find that for shorter durations, people can hear \
            even smaller differences than for longer durations.').format(percentage)
    else:
        score_message = _(
            'Well done! You managed to hear the difference between tones that \
            differed only {} milliseconds in length. Humans are really good at \
            hearing these small differences in durations, which is very handy \
            if we want to be able to process rhythm in music.').format(milliseconds)
    session.finish()
    session.save()
    
    # Return a score and final score action
    return Final.action(
        title=_('End of this experiment'),
        session=session,
        score_message=score_message
    )

def intro_explanation(condition):
    return Explainer.action(
        instruction=_(
            'In this test you will hear two time durations for each trial, which are marked by two tones.'),
        steps=[
            Explainer.step(
                description=_(
                    "It's your job to decide if the second %(type)s is LONGER than the first %(type)s, or EQUALLY LONG.") % {'type': condition},
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
            )],
        button_label='Ok'
    )

def get_previous_condition(last_result):
    return last_result.expected_response == 'LONGER'

def staircasing_blocks(session, trial_action_callback, condition='interval'):
    """ Calculate staircasing procedure in blocks of 5 trials with one catch trial 
    Arguments:
    - session: the session
    - trial_action_callback: function to build a trial action
    """
    previous_results = session.result_set.order_by('-created_at')
    trial_condition = get_trial_condition_block(
        previous_results.count(), session.id, 5)
    if not previous_results.count():
        # first trial
        return trial_action_callback(session, trial_condition, 1.0, START_DIFF)
    previous_difference = int(previous_results.first().section.name)
    if previous_difference == 0:
        # last trial was catch trial, don't calculate turnpoints
        # find pre-catch difference and don't manipulate duration
        if previous_results.count() == 1:
            # this is the second trial, so the difference is still at initial value
            previous_difference = START_DIFF
        else:
            counter = 0
            while(previous_difference == 0):
                # search for last non-catch difference
                # this could be as far as 2 trials back (one block ends, another one starts with catch trial)
                counter += 1
                previous_difference = int(previous_results.all()[
                                          counter].section.name)
        action = trial_action_callback(
            session,
            trial_condition,
            1.0,
            previous_difference)
    if previous_results.first().score == 0:
        # the previous response was incorrect
        # set previous score to 4, to mark the turnpoint
        last_result = previous_results.first()
        last_result.score = 4
        last_result.save()
        # register turnpoint and increase difference
        session.final_score += 1
        session.save()
        action = trial_action_callback(
            session,
            trial_condition,
            1.5,
            previous_difference)
    else:
        # the previous response was correct
        if previous_results.count() > 1 and previous_results.all()[1].score == 1:
            # the previous two responses were correct
            # set previous score to 4, to mark the turnpoint
            last_correct_result = previous_results.first()
            last_correct_result.score = 4
            last_correct_result.save()
            # register turnpoint and decrease difference
            session.final_score += 1
            session.save()
            action = trial_action_callback(
                session,
                trial_condition,
                0.5,
                previous_difference)
        else:
            action = trial_action_callback(
                session,
                trial_condition,
                1.0,
                previous_difference)
    if not action:
        # action is None if the audio file doesn't exist
        return finalize_experiment(session, condition)
    return action