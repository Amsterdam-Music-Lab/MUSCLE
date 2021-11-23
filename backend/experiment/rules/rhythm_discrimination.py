import random
import logging

from django.utils.translation import gettext_lazy as _

from .util.actions import combine_actions
from .util.practice import practice_explainer, practice_again_explainer, start_experiment_explainer
from .views import CompositeView, Consent, Final, Explainer, StartSession, Playlist
from .views.form import ChoiceQuestion, Form
from .base import Base

logger = logging.getLogger(__name__)

STIMULI = {
    'nonmetric': [
        '1 1  3.5  4.5  3.5', '1 3.5  1.4  4.5  1.4', '1.4  3.5  1.4  4.5 1', '3.5  3.5 1 4.5 1', '4.5  1 1  3.5  3.5', '4.5 1 1.4  3.5  1.4', '1 1.4 1 1.4  3.5  3.5', '1 1.4  1.4 1 4.5  1.4', '1 1.4  4.5  1 1  3.5', '1 3.5  1.4  3.5  1.4 1', '1.4 1 4.5  1.4  1.4 1', '1.4 1 4.5  3.5  1 1', '1.4  1.4 1 1.4  4.5 1', '1.4  3.5  1 1  1.4  3.5', '3.5  1.4 1 4.5  1 1', '3.5  1.4  3.5  1.4  1 1', '4.5 1 1.4  1.4 1 1.4', '4.5  1.4 1 3.5  1 1', '1 1 1 1.4  4.5 1 1.4', '1 1  3.5  1.4 1 3.5 1', '1 1  3.5  1.4  1.4 1 1.4', '1 3.5 1 4.5  1 1 1', '1 4.5  1 1  3.5  1 1', '1.4 1 1.4  3.5  1.4  1 1', '1.4 1 4.5 1 1.4  1 1', '1.4  3.5  3.5  1 1  1 1', '3.5  1 1  3.5 1 1.4 1', '3.5  1 1  4.5  1 1 1', '3.5  1.4  1.4  1 1 1 1.4', '4.5  1 1 1 1.4  1.4 1'
    ],
    'metric': [
        '2 2 4 1 3', '3 1 4 1 3', '3 1 4 2 2', '4 1 3 3 1', '4 3 1 1 3', '4 3 1 2 2', '1 1 2 3 1 4', '1 1 2 4 2 2', '2 1 1 1 3 4', '2 1 1 2 2 4', '2 1 1 4 1 3', '2 2 1 3 3 1', '2 2 2 1 1 4', '2 2 3 1 1 3', '3 1 1 3 2 2', '3 1 2 2 1 3', '4 1 1 2 3 1', '4 2 2 1 1 2', '1 1 1 1 4 3 1', '1 1 2 2 1 1 4', '1 1 2 3 1 1 3', '1 1 2 3 1 2 2', '2 1 1 2 2 3 1', '2 1 1 3 1 1 3', '2 2 1 1 1 1 4', '3 1 2 1 1 1 3', '3 1 2 2 1 1 2', '3 1 4 1 1 1 1', '4 1 1 1 1 3 1', '4 2 2 1 1 1 1'
    ]
}

class RhythmDiscrimination(Base):
    ID = 'RHYTHM_DISCRIMINATION'

    @classmethod
    def first_round(cls, experiment):
        """Create data for the first experiment rounds"""
        explainer = intro_explainer()

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
    def next_round(cls, session, series=None):
        if session.rounds_complete():
            return finalize_experiment(session, series)
        
        next_round_number = session.get_next_round()

        if next_round_number == 1:
            plan_stimuli(session)
        
        return combine_actions(*next_trial_actions(session, next_round_number))
    
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


def next_trial_actions(session, round_number):
    """
    Get the next trial action, depending on the round number
    """
    actions = []
    try:
        plan = session.load_json_data()['plan']
    except KeyError as error:
        print('Missing plan key: %s' % str(error))
        return actions
    
    condition = plan[round_number]

    if session.final_score == 0:
        # practice: add feedback on previous result
        previous_results = session.result_set.order_by('-created_at')
        if previous_results.count():
            actions.append(
                response_explainer(previous_results.first().score, plan[round_number-1]['group_id'])
            )
        if round_number == 5:
            total_score = sum([res.score for res in previous_results.all()[:4]])
            if total_score < 3:
                # start practice over
                actions.append(practice_again_explainer())
                actions.append(intro_explainer())
                session.result_set.all().delete()
                session.save()
            else:
                # experiment starts
                session.final_score = 1
                session.save()
                actions.append(start_experiment_explainer())
    
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
    view = CompositeView(
        section=section,
        feedback_form=form.action(),
        instructions=instructions,
        title=_('Ryhthm discrimination')
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
    random.shuffle(metric)
    random.shuffle(nonmetric)
    tempi = [150, 160, 170, 180, 190, 200]
    metric_deviants = [{'rhythm': m, 'tag_id': random.choice(tempi), 'group_id': 0} for m in metric[:15]]
    metric_standard = [{'rhythm': m, 'tag_id': random.choice(tempi), 'group_id': 1} for m in metric[15:]]
    nonmetric_deviants = [{'rhythm': m, 'tag_id': random.choice(tempi), 'group_id': 0} for m in nonmetric[:15]]
    nonmetric_standard = [{'rhythm': m, 'tag_id': random.choice(tempi), 'group_id': 1} for m in nonmetric[15:]]
    practice = [
        random.choice(metric_deviants),
        random.choice(metric_standard),
        random.choice(nonmetric_deviants),
        random.choice(nonmetric_standard)
    ]
    experiment = metric_deviants + metric_standard + nonmetric_deviants + nonmetric_standard
    random.shuffle(experiment)
    plan =  practice + experiment
    session.merge_json_data({'plan': plan})
    session.save()

def intro_explainer():
    return Explainer.action(
        instruction=_(
            'In this test you will hear the same rhythm twice. After that, you will hear a third rhythm.'),
        steps=[
            Explainer.step(
                description=_(
                    "Your task is to decide whether this third rhythm is the SAME as the first two rhythms or DIFFERENT."),
            )],
        button_label='Ok'
    )
    
def response_explainer(correct, same, button_label=_('Next fragment')):
    if correct:
        if same:
            instruction = _(
                'The third rhythm is the SAME. Your response was correct.')
        else:
            instruction = _(
                'The third rhythm is DIFFERENT. Your response was correct.')
    else:
        if same:
            instruction = _(
                'The third rhythm is the SAME. Your response was incorrect.')
        else:
            instruction = _(
                'The third rhythm is DIFFERENT. Your response was incorrect.')
    return Explainer.action(
        instruction=instruction,
        steps=[],
        button_label=button_label
    )

def finalize_experiment(session, series):
    # we had 4 practice trials and 60 experiment trials
    percentage = (sum([res.score for res in session.result_set.all()]) / session.experiment.rounds) * 100
    session.finish()
    session.save()
    # Return a score and final score action
    return Final.action(
        title=_('End'),
        session=session,
        score_message=_(
            "Well done! You've answered {} percent correctly!").format(percentage)
    )