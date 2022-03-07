import logging

from django.utils.translation import gettext_lazy as _

from .base import Base
from experiment.models import Section
from .views import CompositeView, Consent, Explainer, Step, Playlist, StartSession
from .views.form import ChoiceQuestion, Form

from .util.practice import get_practice_views, practice_explainer, get_trial_condition, get_trial_condition_block
from .util.actions import combine_actions, final_action_with_optional_button
from .util.score import get_average_difference_level_based
from .util.staircasing import register_turnpoint

logger = logging.getLogger(__name__)

MAX_TURNPOINTS = 6

class HBat(Base):
    ID = 'H_BAT'
    start_diff = 20

    @classmethod
    def next_round(cls, session, request_session=None):
        if session.final_score == 0:
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
            action = cls.next_trial_action(session, trial_condition, 1)
            if not action:
                # participant answered first trial incorrectly (outlier)
                action = cls.finalize_experiment(session, request_session)
        else:
            action = staircasing(session, cls.next_trial_action)
            if not action:
                # action is None if the audio file doesn't exist
                action = cls.finalize_experiment(session, request_session)
            if session.final_score == MAX_TURNPOINTS+1:
                # delete result created before this check
                session.result_set.order_by('-created_at').first().delete()
                action = cls.finalize_experiment(session, request_session)
            return action
        
    @classmethod
    def first_round(cls, experiment):
        explainer = cls.intro_explainer().action(True)
        consent = Consent.action()
        explainer2 = practice_explainer().action()
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
            'decision_time': section.duration + .5
        }
        return view.action(config)

    @classmethod
    def intro_explainer(cls):
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
                Step(_(
                        "In this test, you can answer as soon as you feel you know the answer.")),
                Step(_(
                        "NOTE: Please wait with answering until you are either sure, or the sound has stopped.")),
                Step(_(
                        'This test will take around 4 minutes to complete. Try to stay focused for the entire test!'))
                ],
            button_label='Ok'
        )

    @classmethod
    def response_explainer(cls, correct, slower, button_label=_('Next fragment')):
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
                        'The rhythm went FASTER. Your response was INCORRECT.')
                else:
                    instruction = _(
                        'The rhythm went SLOWER. Your response was INCORRECT.')
            return Explainer(
                instruction=instruction,
                steps=[],
                button_label=button_label
            )
        
    @classmethod
    def finalize_experiment(cls, session, request_session):
        """ if either the max_turnpoints have been reached,
        or if the section couldn't be found (outlier), stop the experiment
        """
        percentage = round(get_average_difference_level_based(session, 6, cls.start_diff) / 5, 2)
        score_message = _("Well done! You heard the difference when the rhythm was \
            speeding up or slowing down with only %(percent)d percent!\n\n %(trivia)s") % {'percent': percentage, 'trivia': cls.get_trivia()}
        session.finish()
        session.save()
        return final_action_with_optional_button(session, score_message, request_session)
    
    @classmethod
    def get_trivia(cls):
        return _("When people listen to music, they often perceive an underlying regular pulse, like the woodblock \
            in this task. This allows us to clap along with the music at a concert and dance together in synchrony.")


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
        json_data = session.load_json_data()
        direction = json_data.get('direction')
        last_result.comment = 'decrease difficulty'
        last_result.save()
        if direction == 'increase':
            register_turnpoint(session, last_result)
        # register decreasing difficulty
        session.merge_json_data({'direction': 'decrease'})
        session.save()
        level = get_previous_level(last_result) - 1 # decrease difficulty
        action = trial_action_callback(
            session, trial_condition, level)
    else:
        if previous_results.count() == 1:
            # this is the second trial, so the level is still 1
            action = trial_action_callback(
                session, trial_condition, 1)
        elif previous_results.all()[1].score == 1 and not previous_results.all()[1].comment:
            # the previous two responses were correct
            json_data = session.load_json_data()
            direction = json_data.get('direction')
            last_result.comment = 'increase difficulty'
            last_result.save()
            if direction == 'decrease':
                # mark the turnpoint
                register_turnpoint(session, last_result)
            # register increasing difficulty
            session.merge_json_data({'direction': 'increase'})
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
        return None
    return action