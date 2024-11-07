import random
import logging

from django.utils.translation import gettext_lazy as _

from experiment.actions.utils import final_action_with_optional_button, render_feedback_trivia
from experiment.rules.util.practice import get_practice_explainer, practice_again_explainer, start_experiment_explainer
from experiment.actions import Trial, Explainer, Step
from experiment.actions.playback import Autoplay
from experiment.actions.form import ChoiceQuestion, Form

from result.utils import prepare_result
from section.models import Playlist

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

    def next_round(self, session):
        next_round_number = session.get_rounds_passed()

        if next_round_number == 0:
            plan_stimuli(session)
            return [get_intro_explainer(), get_practice_explainer(), *next_trial_actions(session, next_round_number)]

        return next_trial_actions(
            session, next_round_number)

    def validate_playlist(self, playlist: Playlist):
        errors = []
        errors += super().validate_playlist(playlist)
        sections = playlist.section_set.all()
        if not sections.count():
            return errors
        if sections.count() != 720:
            errors.append("The block needs a playlist with 720 sections")
        tags, groups = zip(*[(s.tag, s.group) for s in sections])
        try:
            tag_numbers = sorted(list(set([int(t) for t in tags])))
            if tag_numbers != [150, 160, 170, 180, 190, 200]:
                errors.append("Tags should have values 150, 160, 170, 180, 190, 200")
        except:
            errors.append("The sections should have integer tags")
        try:
            group_numbers = sorted(list(set([int(g) for g in groups])))
            if group_numbers != [0, 1]:
                errors.append("Groups should have values 0, 1")
        except:
            errors.append("The sections should have integer groups")

        def pattern_error(pattern: str) -> str:
            return f"There should be 12 sections with pattern {pattern}"

        metric_standard = STIMULI["metric"]["standard"]
        for m in metric_standard:
            if sections.filter(song__name__startswith=m).count() != 12:
                errors.append(pattern_error(m))
        metric_deviant = STIMULI["metric"]["deviant"]
        for m in metric_deviant:
            if sections.filter(song__name__startswith=m).count() != 12:
                errors.append(pattern_error(m))
        nonmetric_standard = STIMULI["nonmetric"]["standard"]
        for n in nonmetric_standard:
            if sections.filter(song__name__startswith=n).count() != 12:
                errors.append(pattern_error(n))
        nonmetric_deviant = STIMULI["nonmetric"]["deviant"]
        for n in nonmetric_deviant:
            if sections.filter(song__name__startswith=n).count() != 12:
                errors.append(pattern_error(n))

        return errors


def next_trial_actions(session, round_number):
    """
    Get the next trial action, depending on the round number
    """
    actions = []
    try:
        plan = session.json_data["plan"]
    except KeyError as error:
        print('Missing plan key: %s' % str(error))
        return actions

    if len(plan) == round_number:
        return [finalize_block(session)]

    condition = plan[round_number]

    if session.final_score == 0:
        # practice: add feedback on previous result
        previous_results = session.result_set.order_by('-created_at')
        if previous_results.count():
            same = previous_results.first().expected_response == 'SAME'
            actions.append(
                response_explainer(previous_results.first().score, same)
            )
        if round_number == 4:
            total_score = sum(
                [res.score for res in previous_results.all()[:4]])
            if total_score < 2:
                # start practice over
                actions.append(practice_again_explainer())
                actions.append(get_intro_explainer())
                session.result_set.all().delete()
                session.save()
            else:
                # experiment starts
                session.final_score = 1
                session.save()
                explainer = start_experiment_explainer()
                explainer.steps.pop(0)
                actions.append(explainer)

    try:
        section = session.playlist.section_set.filter(
            song__name__startswith=condition['rhythm']).filter(
            tag=condition['tag']).get(
            group=condition['group']
        )
    except:
        return actions

    expected_response = 'SAME' if condition['group'] == '1' else 'DIFFERENT'
    key = 'same'
    question = ChoiceQuestion(
        key=key,
        question=_(
            "Is the third rhythm the SAME or DIFFERENT?"),
        choices={
            'SAME': _('SAME'),
            'DIFFERENT': _('DIFFERENT')
        },
        view='BUTTON_ARRAY',
        result_id=prepare_result(key, session, expected_response=expected_response, scoring_rule='CORRECTNESS'),
        submits=True
    )
    form = Form([question])
    playback = Autoplay([section])
    if round_number < 4:
        title = _('practice')
    else:
        title = _('trial %(index)d of %(total)d') % (
            {'index': round_number - 3, 'total': len(plan) - 4})
    view = Trial(
        playback=playback,
        feedback_form=form,
        title=_('Rhythm discrimination: %s' % (title)),
        config={
            'listen_first': True,
            'response_time': section.duration + .5
        }
    )

    actions.append(view)
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
    block = metric_deviants + metric_standard + \
        nonmetric_deviants + nonmetric_standard
    random.shuffle(block)
    plan = practice + block
    session.save_json_data({'plan': plan})
    session.save()


def get_intro_explainer():
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
        step_numbers=True,
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
    )


def finalize_block(session):
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
    return final_action_with_optional_button(session, final_text)
