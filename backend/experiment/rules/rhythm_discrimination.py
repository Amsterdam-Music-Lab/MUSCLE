import random
import logging

from django.utils.translation import gettext_lazy as _

from .util.actions import combine_actions, final_action_with_optional_button, render_feedback_trivia
from .util.practice import practice_explainer, practice_again_explainer, start_experiment_explainer
from .views import Trial, Consent, Explainer, StartSession, Step
from .views.playback import Playback
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
    def first_round(cls, experiment, participant):
        """Create data for the first experiment rounds"""
        explainer = intro_explainer().action(True)

        # 2. Consent with default text
        consent = Consent.action()

        explainer2 = practice_explainer().action()

        start_session = StartSession.action()

        return [
            explainer,
            consent,
            explainer2,
            start_session
        ]

    @classmethod
    def next_round(cls, session, request_session=None):
        next_round_number = session.get_next_round()

        if next_round_number == 1:
            plan_stimuli(session)

        actions = next_trial_actions(
            session, next_round_number, request_session)
        if isinstance(actions, dict):
            return actions
        return combine_actions(*actions)


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

    if len(plan) == round_number-1:
        return finalize_experiment(session, request_session)

    condition = plan[round_number-1]

    if session.final_score == 0:
        # practice: add feedback on previous result
        previous_results = session.result_set.order_by('-created_at')
        if previous_results.count():
            same = previous_results.first().expected_response == 'SAME'
            actions.append(
                response_explainer(previous_results.first().score, same)
            )
        if round_number == 5:
            total_score = sum(
                [res.score for res in previous_results.all()[:4]])
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
            tag=condition['tag']).get(
            group=condition['group']
        )
    except:
        return actions

    expected_result = 'SAME' if condition['group'] == '1' else 'DIFFERENT'
    # create Result object and save expected result to database
    result_pk = RhythmDiscrimination.prepare_result(
        session, section, expected_result)
    question = ChoiceQuestion(
        key='same',
        question=_(
            "Is the third rhythm the SAME or DIFFERENT?"),
        choices={
            'SAME': _('SAME'),
            'DIFFERENT': _('DIFFERENT')
        },
        view='BUTTON_ARRAY',
        scoring_rule='CORRECTNESS',
        result_id=result_pk,
        submits=True
    )
    form = Form([question])
    playback = Playback([section])
    if round_number < 5:
        title = _('practice')
    else:
        title = _('trial %(index)d of %(total)d') % (
            {'index': round_number - 4, 'total': len(plan) - 4})
    view = Trial(
        playback=playback,
        feedback_form=form,
        title=_('Rhythm discrimination: %s' % (title)),
        config={
            'listen_first': True,
            'decision_time': section.duration + .1
        }
    )

    actions.append(view.action())
    return actions


def plan_stimuli(session):
    """ select 60 stimuli, of which 30 are standard, 30 deviant.
    rhythm refers to the type of rhythm,
    tag refers to the tempo,
    group refers to the condition (0 is deviant, 1 is standard)
    """
    metric = STIMULI['metric']
    nonmetric = STIMULI['nonmetric']
    tempi = [150, 160, 170, 180, 190, 200]
    tempi = [str(t) for t in tempi]
    metric_deviants = [{'rhythm': m, 'tag': random.choice(
        tempi), 'group': '0'} for m in metric['deviant']]
    metric_standard = [{'rhythm': m, 'tag': random.choice(
        tempi), 'group': '1'} for m in metric['standard']]
    nonmetric_deviants = [{'rhythm': m, 'tag': random.choice(
        tempi), 'group': '0'} for m in nonmetric['deviant']]
    nonmetric_standard = [{'rhythm': m, 'tag': random.choice(
        tempi), 'group': '1'} for m in nonmetric['standard']]
    practice = [
        {'rhythm': STIMULI['practice']['metric']['standard'],
            'tag': random.choice(tempi), 'group': '1'},
        {'rhythm': STIMULI['practice']['metric']['deviant'],
            'tag': random.choice(tempi), 'group': '0'},
        {'rhythm': STIMULI['practice']['nonmetric']['standard'],
            'tag': random.choice(tempi), 'group': '1'},
        {'rhythm': STIMULI['practice']['nonmetric']['deviant'],
            'tag': random.choice(tempi), 'group': '0'},
    ]
    experiment = metric_deviants + metric_standard + \
        nonmetric_deviants + nonmetric_standard
    random.shuffle(experiment)
    plan = practice + experiment
    session.merge_json_data({'plan': plan})
    session.save()


def intro_explainer():
    return Explainer(
        instruction=_(
            'In this test you will hear the same rhythm twice. After that, you will hear a third rhythm.'),
        steps=[
            Step(_(
                "Your task is to decide whether this third rhythm is the SAME as the first two rhythms or DIFFERENT.")),
            Step(_("Remember: try not to move or tap along with the sounds")),
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
    percentage = (sum([res.score for res in session.result_set.all()]
                      ) / session.result_set.count()) * 100
    session.finish()
    session.save()
    feedback = _("Well done! You've answered {} percent correctly!").format(
        percentage)
    trivia = _("One reason for the \
        weird beep-tones in this test (instead of some nice drum-sound) is that it is used very often\
        in brain scanners, which make a lot of noise. The beep-sound helps people in the scanner \
        to hear the rhythm really well.")
    final_text = render_feedback_trivia(feedback, trivia)
    return final_action_with_optional_button(session, final_text, request_session)
