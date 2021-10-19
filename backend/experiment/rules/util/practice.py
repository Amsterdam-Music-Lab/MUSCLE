import numpy as np

from django.utils.translation import gettext as _

from ..views import Explainer
from .actions import combine_actions


def get_practice_views(
    session, 
    intro_explainer,
    first_trial_condition,
    trial_callback,
    response_callback,
    check_previous_condition,
    start_diff=400000
):
    ''' Present practice views, in blocks of 2
    Give feedback on the correctness of the response,
    and repeat practice if necessary.
    - session: session
    - intro_explainer: introduction explainer for the experiment
    - first_trial_condition: condition for the first trial after practice
    - trial_callback: function to return the data for a trial
    - response_callback: function to generate explainer about correctness of response
    - check_previous_condition: function to determine the condition of previous practice trial
    - start_diff: if applicable, "easiest" difference between stimuli
    '''
    results_count = session.result_set.count()
    trial_condition = get_trial_condition_block(results_count, session.id, 2)
    previous_results = session.result_set.order_by('-created_at')
    if not previous_results.count():
        # first practice trial
        return trial_callback(session, trial_condition, 1.0, start_diff)
    last_result = previous_results.first()
    if previous_results.count() < 4:
        # practice trial
        correct = last_result.score > 0
        previous_condition = check_previous_condition(last_result)
        response_explainer = response_callback(correct, previous_condition)
        trial = trial_callback(
            session, trial_condition, 1.0, start_diff)
        return combine_actions(response_explainer, trial)
    else:
        # after last practice trial 
        if last_result.score > 0 and previous_results.all()[1].score > 0:
            # Practice went successfully, start experiment
            previous_condition = check_previous_condition(last_result)
            response_explainer = response_callback(
                True, previous_condition)
            session.final_score = 1
            session.result_set.all().delete()
            session.save()
            start_explainer = start_experiment_explainer()
            trial = trial_callback(
                session, first_trial_condition, 1.0, start_diff)
            return combine_actions(response_explainer, start_explainer, trial)
        else:
            # need more practice, start over
            response_explainer = response_callback(False, check_previous_condition(last_result))
            next_trial = trial_callback(
                session, trial_condition, 1.0, start_diff)
            return combine_actions(
                response_explainer,
                practice_again_explainer(),
                intro_explainer,
                practice_explainer(),
                next_trial
            )


def practice_explainer():
    return Explainer.action(
        instruction=_('We will now practice first.'),
        steps=[
            Explainer.step(
                description=_('First you will hear 4 practice trials.'),
            )
        ],
        button_label=_('Begin experiment')
    )

def practice_again_explainer():
    return Explainer.action(
        instruction=_(
            "You have answered 1 or more practice trials incorrectly."),
        steps=[Explainer.step(
            description=_("We will therefore practice again."),
            number=1
        ),
            Explainer.step(
            description=_(
                'But first, you can read the instructions again.'),
            number=2
        ),
        ],
        button_label=_('Continue')
    )

def start_experiment_explainer():
    return Explainer.action(
        instruction=_(
            'Now we will start the real experiment.'),
        steps=[
            Explainer.step(
                description=_(
                    'Pay attention! During the experiment it will become more difficult to hear the difference between the tones.'),
                number=1
            ),
            Explainer.step(
                description=_(
                    "Try to answer as accurately as possible, even if you're uncertain."),
                number=2
            ),
            Explainer.step(
                description=_(
                    "Remember that you don't move along or tap during the test."),
                number=3
            ),
        ],
        button_label=_('Start')
    )


def get_trial_condition_block(results_count, session_id, n_trials_per_block):
    """
    for each block of trials, initialize an array with one catch trial
    shuffle the array, based on a seed that changes every n_trials_per_block
    return the condition of the current trial
    """
    seed = int(results_count / n_trials_per_block) + session_id
    np.random.seed(seed)
    trial_block = np.zeros(n_trials_per_block)
    trial_block[0] = 1
    np.random.shuffle(trial_block)
    trial_number = results_count % n_trials_per_block
    return trial_block[trial_number]

def get_trial_condition(n_choices):
    """ get randomized trial condition 
    return an integer between 0 and n_choices-2
    """
    options = np.arange(n_choices)
    return np.random.choice(options)
    