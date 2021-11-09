import logging

from django.utils.translation import gettext as _

from .base import Base
from experiment.models import Section
from .views import CompositeView, Explainer, Consent, StartSession, Playlist
from .views.form import ChoiceQuestion, Form

from .util.practice import get_practice_views, practice_explainer, get_trial_condition, get_trial_condition_block
from .util.actions import combine_actions
from .util.score import get_average_difference_level_based

logger = logging.getLogger(__name__)

MAX_TURNPOINTS = 6

class HBat(Base):
    ID = 'H_BAT'

    @classmethod
    def next_round(cls, session):
        if session.final_score == MAX_TURNPOINTS+1:
            return cls.finalize_experiment(session)
        elif session.final_score == 0:
            # we are practicing
            actions = get_practice_views(
                session,
                cls.intro_explainer(),
                staircasing,
                cls.next_trial_action,
                cls.response_explainer,
                get_previous_condition,
                1
            )
            return actions
        # actual experiment
        previous_results = session.result_set.order_by('-created_at')
        trial_condition = get_trial_condition(2)
        if not previous_results.count():
            # first trial
            return cls.next_trial_action(session, trial_condition, 1)

        else:
            action = staircasing(session, cls.next_trial_action)
            if not action:
                # action is None if the audio file doesn't exist
                return cls.finalize_experiment(session)
            else:
                return action
        
    @classmethod
    def first_round(cls, experiment):
        explainer = cls.intro_explainer()
        consent = Consent.action()
        explainer2 = practice_explainer()
        playlist = Playlist.action(experiment.playlists.all())
        start_session = StartSession.action()
        return combine_actions(
            explainer,
            consent,
            explainer2,
            playlist,
            start_session
        )
    
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
            return 1
        else:
            return 0
    
    @staticmethod
    def handle_result(session, section, data):
        return Base.handle_results(session, section, data)

    @classmethod
    def next_trial_action(cls, session, trial_condition, level=1, *kwargs):
        """
        Get the next actions for the experiment
        trial_condition is either 1 or 0
        level can be 1 (20 ms) or higher (10, 5, 2.5 ms...)
        """
        try:
            section = session.playlist.section_set.filter(group_id=level).get(tag_id=trial_condition)
        except Section.DoesNotExist:
            return None
        expected_result = 'SLOWER' if trial_condition else 'FASTER'
        # create Result object and save expected result to database
        result_pk = Base.prepare_result(session, section, expected_result)
        instructions = {
            'preload': '',
            'during_presentation': ''
        }
        question = ChoiceQuestion(
            key='longer_or_equal',
            question=_(
                "Is the rhythm going SLOWER or FASTER?"),
            choices={
                'SLOWER': _('SLOWER'),
                'FASTER': _('FASTER')
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
            title=_('Beat acceleration')
        )
        config = {
            'listen_first': True,
            'decision_time': section.duration + .5
        }
        return view.action(config)

    @classmethod
    def intro_explainer(cls):
        return Explainer.action(
            instruction=_(
                'In this test you will hear a series of tones for each trial.'),
            steps=[
                Explainer.step(
                    description=_(
                        "It's your job to decide if the rhythm goes SLOWER of FASTER."),
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

    @classmethod
    def response_explainer(cls, correct, slower, button_label=_('Next fragment')):
            if correct:
                if slower:
                    instruction = _(
                        'The rhythm went SLOWER. Your response was correct.')
                else:
                    instruction = _(
                        'The rhythm went FASTER. Your response was correct.')
            else:
                if slower:
                    instruction = _(
                        'The rhythm went FASTER. Your response was incorrect.')
                else:
                    instruction = _(
                        'The rhythm went SLOWER. Your response was incorrect.')
            return Explainer.action(
                instruction=instruction,
                steps=[],
                button_label=button_label
            )
        
    @classmethod
    def finalize_experiment(cls, session):
        """ if either the max_turnpoints have been reached,
        or if the section couldn't be found (outlier), stop the experiment
        """
        percentage = (get_average_difference_level_based(session, 4) / 500) * 100
        score_message = _("Well done! You heard the difference when the rhythm was \
            speeding up or slowing down with only {} percent!").format(percentage)
        session.finish()
        session.save()
        return Final.action(
            title=_('End'),
            session=session,
            score_message=score_message
        )


def get_previous_condition(previous_result):
    """ check if previous section was slower / in 2 (1) or faster / in 3 (0) """
    return previous_result.section.tag_id

def get_previous_level(previous_result):
    return previous_result.section.group_id

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
        # set previous score to 4, to mark the turnpoint
        last_result.score = 4
        last_result.save()
        # register turnpoint and increase difference
        session.final_score += 1
        session.save()
        level = get_previous_level(last_result) - 1 # decrease difficulty
        action = trial_action_callback(
            session, trial_condition, level)
    else:
        if previous_results.count() == 1:
            # this is the second trial, so the level is still 1
            action = trial_action_callback(
                session, trial_condition, 1)
        # previous response was correct
        elif previous_results.all()[1].score == 1:
            # set previous score to 4, to mark the turnpoint
            # the previous two responses were correct
            last_result = previous_results.first()
            last_result.score = 4
            last_result.save()
            # register turnpoint and decrease difference
            session.final_score += 1
            session.save()
            level = get_previous_level(last_result) + 1 # increase difficulty
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
        return finalize_experiment(session)
    return action