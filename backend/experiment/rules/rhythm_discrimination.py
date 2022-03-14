import random
import logging

from django.utils.translation import gettext_lazy as _

from .util.actions import combine_actions, final_action_with_optional_button, render_feedback_trivia
from .util.practice import practice_explainer, practice_again_explainer, start_experiment_explainer
from .views import CompositeView, Consent, Final, Explainer, Step, StartSession, Playlist
from .views.form import ChoiceQuestion, Form
from .base import Base

logger = logging.getLogger(__name__)

STIMULI = {
    'practice': {
        'metric': {
            'standard': '4 1 1 1 1 3 1',
            'deviant': '1 1 2 4 2 2', 
        },
        'nonmetric': {
            'standard': '4.5  1 1  3.5  3.5',
            'deviant': '4.5 1 1.4  1.4 1 1.4'
        }
    },
    'nonmetric':  {
        'standard': [
            '1 1  3.5  4.5  3.5',
            '1 3.5  1.4  4.5  1.4',
            '1 3.5  1.4  3.5  1.4 1',
            '3.5  1.4  3.5  1.4  1 1',
            '4.5  1.4 1 3.5  1 1',
            '1 3.5 1 4.5  1 1 1',
            '1.4  3.5  3.5  1 1  1 1',
            '1.4 1 4.5 1 1.4  1 1',
            '3.5  1 1  4.5  1 1 1'
        ],
        'deviant': [
            '1.4  3.5  1.4  4.5 1',
            '3.5  3.5 1 4.5 1',
            '1 1.4  1.4 1 4.5  1.4',
            '1 1.4  4.5  1 1  3.5',
            '1 1.4 1 1.4  3.5  3.5',
            '1.4  1.4 1 1.4  4.5 1',
            '1 1  3.5  1.4 1 3.5 1',
            '1 4.5  1 1  3.5  1 1',
            '1.4 1 1.4  3.5  1.4  1 1'
        ]
    },
    'metric': {
        'standard': [
            '3 1 4 2 2',
            '4 3 1 2 2',
            '2 1 1 2 2 4',
            '2 2 2 1 1 4',
            '4 2 2 1 1 2',
            '1 1 2 2 1 1 4',
            '1 1 2 3 1 2 2',
            '2 2 1 1 1 1 4',
            '3 1 4 1 1 1 1'
        ],
        'deviant': [
            '2 2 4 1 3',
            '3 1 4 1 3',
            '1 1 2 3 1 4',
            '2 1 1 1 3 4',
            '2 2 3 1 1 3',
            '3 1 1 3 2 2',
            '1 1 2 3 1 1 3',
            '2 1 1 3 1 1 3',
            '4 2 2 1 1 1 1'
        ]
    }
}

class RhythmDiscrimination(Base):
    ID = 'RHYTHM_DISCRIMINATION'

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds"""
        explainer = intro_explainer().action(True)

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
        next_round_number = session.get_next_round()

        if next_round_number == 1:
            plan_stimuli(session)
        
        actions = next_trial_actions(session, next_round_number, request_session)
        if isinstance(actions, dict):
            return actions
        return combine_actions(*actions)
    
    @staticmethod
    def calculate_score(result, form_element):
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


def next_trial_actions(session, round_number, request_session):
    """
    Get the next trial action, depending on the round number
    """
    actions = []
    try:
        plan = session.load_json_data()['plan']
    except KeyError as error:
        print('Missing plan key: %s' % str(error))
        return actions
    
    if len(plan)==round_number-1:
        return finalize_experiment(session, request_session)
    
    condition = plan[round_number-1]

    if session.final_score == 0:
        # practice: add feedback on previous result
        previous_results = session.result_set.order_by('-created_at')
        if previous_results.count():
            actions.append(
                response_explainer(previous_results.first().score, plan[round_number-2]['group_id'])
            )
        if round_number == 5:
            total_score = sum([res.score for res in previous_results.all()[:4]])
            if total_score < 2:
                # start practice over
                actions.append(practice_again_explainer())
                actions.append(intro_explainer())
                session.result_set.all().delete()
                session.save()
            else:
                # experiment starts
                session.final_score = 1
                session.save()
                explainer = start_experiment_explainer()
                explainer.steps.pop(0)
                actions.append(explainer.action(True))
    
    try:
        section = session.playlist.section_set.filter(
            name__startswith=condition['rhythm']).filter(
            tag_id=condition['tag_id']).get(
            group_id=condition['group_id']
        )
    except Section.DoesNotExist:
        return actions

    expected_result = 'SAME' if condition['group_id'] == 1 else 'DIFFERENT'
    # create Result object and save expected result to database
    result_pk = Base.prepare_result(session, section, expected_result)
    instructions = {
        'preload': '',
        'during_presentation': ''
    }
    question = ChoiceQuestion(
        key='same',
        question=_(
            "Is the third rhythm the SAME or DIFFERENT?"),
        choices={
            'SAME': _('SAME'),
            'DIFFERENT': _('DIFFERENT')
        },
        view='BUTTON_ARRAY',
        result_id=result_pk,
        submits=True
    )
    form = Form([question])
    if round_number < 5:
        title = _('practice')
    else:
        title = _('trial %(index)d of %(total)d') % ({'index': round_number - 4, 'total': len(plan) - 4})
    view = CompositeView(
        section=section,
        feedback_form=form.action(),
        instructions=instructions,
        title=_('Ryhthm discrimination: %s' %(title))
    )
    config = {
            'listen_first': True,
            'decision_time': section.duration + .5
    }
    actions.append(view.action(config))
    return actions

def plan_stimuli(session):
    """ select 60 stimuli, of which 30 are standard, 30 deviant.
    rhythm refers to the type of rhythm,
    tag_id refers to the tempo,
    group_id refers to the condition (0 is deviant, 1 is standard)
    """
    metric = STIMULI['metric']
    nonmetric = STIMULI['nonmetric']
    tempi = [150, 160, 170, 180, 190, 200]
    metric_deviants = [{'rhythm': m, 'tag_id': random.choice(tempi), 'group_id': 0} for m in metric['standard']]
    metric_standard = [{'rhythm': m, 'tag_id': random.choice(tempi), 'group_id': 1} for m in metric['deviant']]
    nonmetric_deviants = [{'rhythm': m, 'tag_id': random.choice(tempi), 'group_id': 0} for m in nonmetric['standard']]
    nonmetric_standard = [{'rhythm': m, 'tag_id': random.choice(tempi), 'group_id': 1} for m in nonmetric['deviant']]
    practice = [
        {'rhythm': STIMULI['practice']['metric']['standard'], 'tag_id': random.choice(tempi), 'group_id': 1},
        {'rhythm': STIMULI['practice']['metric']['deviant'], 'tag_id': random.choice(tempi), 'group_id': 0},
        {'rhythm': STIMULI['practice']['nonmetric']['standard'], 'tag_id': random.choice(tempi), 'group_id': 1},
        {'rhythm': STIMULI['practice']['nonmetric']['deviant'], 'tag_id': random.choice(tempi), 'group_id': 0},
    ]
    experiment = metric_deviants + metric_standard + nonmetric_deviants + nonmetric_standard
    random.shuffle(experiment)
    plan =  practice + experiment
    session.merge_json_data({'plan': plan})
    session.save()

def intro_explainer():
    return Explainer(
        instruction=_(
            'In this test you will hear the same rhythm twice. After that, you will hear a third rhythm.'),
        steps=[
            Step(_(
                    "Your task is to decide whether this third rhythm is the SAME as the first two rhythms or DIFFERENT.")),
            Step(_(
                    'This test will take around 6 minutes to complete. Try to stay focused for the entire test!'))
        ],
        button_label='Ok'
    )
    
def response_explainer(correct, same, button_label=_('Next fragment')):
    if correct:
        if same:
            instruction = _(
                'The third rhythm is the SAME. Your response was CORRECT.')
        else:
            instruction = _(
                'The third rhythm is DIFFERENT. Your response was CORRECT.')
    else:
        if same:
            instruction = _(
                'The third rhythm is the SAME. Your response was INCORRECT.')
        else:
            instruction = _(
                'The third rhythm is DIFFERENT. Your response was INCORRECT.')
    return Explainer(
        instruction=instruction,
        steps=[],
        button_label=button_label
    ).action()

def finalize_experiment(session, request_session):
    # we had 4 practice trials and 60 experiment trials
    percentage = (sum([res.score for res in session.result_set.all()]) / session.experiment.rounds) * 100
    session.finish()
    session.save()
    feedback = _("Well done! You've answered {} percent correctly!").format(percentage)
    trivia = _("One reason for the \
        weird beep-tones in this test (instead of some nice drum-sound) is that it is used very often\
        in brain scanners, which make a lot of noise. The beep-sound helps people in the scanner \
        to hear the rhythm really well.")
    final_text = render_feedback_trivia(feedback, trivia)
    return final_action_with_optional_button(session, final_text, request_session)

