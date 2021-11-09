import logging
from django.utils.translation import gettext as _

from experiment.models import Section
from .views import CompositeView, Final, Explainer, Consent, StartSession, Playlist
from .views.form import ChoiceQuestion, Form
from .base import Base
from .duration_discrimination import staircasing_blocks

from .util.practice import get_practice_views, get_trial_condition_block, practice_explainer
from .util.actions import combine_actions
from .util.score import get_average_difference

logger = logging.getLogger(__name__)

class Anisochrony(Base):
    ID = 'ANISOCHRONY'
    start_diff = 270000
    max_turnpoints = 8
    
    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds"""
        explainer = intro_explanation()

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
        if session.final_score == cls.max_turnpoints+1:
            return finalize_experiment(session)

        elif session.final_score == 0:
            # we are practicing
            actions = get_practice_views(
                session,
                intro_explanation(),
                staircasing_blocks,
                trial_action_callback,
                get_response_explainer,
                get_previous_condition,
                difficulty
            )
            return actions

        ##### Actual trials ####    
        action = staircasing_blocks(session, next_trial_action)
        return action
    

    @staticmethod
    def handle_result(session, section, data):
        return Base.handle_results(session, section, data)
    
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
            if expected_response == 'IRREGULAR':
                return 1
            else:
                return 2
        else:
            return 0


def get_response_explainer(correct, irregular, button_label=_('Next fragment')):
    if correct:
        if irregular:
            instruction = _(
                'The tones were IRREGULAR. Your answer was correct.')
        else:
            instruction = _(
                'The tones were REGULAR. Your answer was correct.')
    else:
        if irregular:
            instruction = _(
                'The tones were IRREGULAR. Your answer was incorrect.')
        else:
            instruction = _(
                'The tones were REGULAR. Your answer was incorrect.')
    return Explainer.action(
        instruction=instruction,
        steps=[],
        button_label=button_label
    )

def finalize_experiment(session):
    # we had 8 turnpoints (we start adding to 1), so finish session
    milliseconds = int(get_average_difference(session, 4)/1000)
    session.finish()
    session.save()
    # Return a score and final score action
    return Final.action(
        title=_('End'),
        session=session,
        score_message=_(
            "Well done! You managed to hear the difference between tones \
            that differed only {} milliseconds in length. Humans are really \
            good at hearing these small differences in durations, which is \
            very handy if we want to be able to process rhythm in music.").format(milliseconds)
    )

def intro_explanation():
    return Explainer.action(
        instruction=_(
            'In this test you will hear a series of tones for each trial.'),
        steps=[
            Explainer.step(
                description=_(
                    "It's your job to decide of the tones sounds REGULAR or IRREGULAR"),
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

def next_trial_action(session, trial_condition, difficulty):
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
    - question: question type with choices
    - title: title of trial page
    - available_choices: e.g., 'LONGER', 'EQUALLY LONG'
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
    expected_result = 'REGULAR' if difference == 0 else 'IRREGULAR'
    # create Result object and save expected result to database
    result_pk = Base.prepare_result(session, section, expected_result)
    instructions = {
        'preload': '',
        'during_presentation': ''
    }
    question = question = ChoiceQuestion(
        key='if_regular',
        question=_(
                "Were the tones REGULAR or IRREGULAR?"),
        choices={
            'REGULAR': _('REGULAR'),
            'IRREGULAR': _('IRREGULAR')
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
        title=_('Anisochrony')
    )
    config = {
        'listen_first': True,
        'decision_time': section.duration + .5
    }
    action = view.action(config)
    return action

def get_previous_condition(last_result):
    return last_result.expected_response == 'IRREGULAR'