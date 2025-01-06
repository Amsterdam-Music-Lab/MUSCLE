from os.path import join
import random

from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.actions import Final
from session.models import Session

EXPERIMENT_KEY = 'experiment'


def get_current_experiment_url(session: Session) -> str:
    experiment_slug = session.json_data.get(EXPERIMENT_KEY)
    if not experiment_slug:
        return None

    if session.participant.participant_id_url:
        participant_id_url = session.participant.participant_id_url
        return f'/{experiment_slug}?participant_id={participant_id_url}'
    else:
        return f'/{experiment_slug}'


def final_action_with_optional_button(session, final_text='', title=_('End'), button_text=_('Continue')):
    """ given a session, a score message and an optional session dictionary from an experiment,
    return a Final.action, which has a button to continue to the next block if series is defined
    """
    redirect_url = get_current_experiment_url(session)

    if redirect_url:
        return Final(
            title=title,
            session=session,
            final_text=final_text,
            button={
                'text': button_text,
                'link': redirect_url
            }
        )
    else:
        return Final(
            title=title,
            session=session,
            final_text=final_text,
        )


def render_feedback_trivia(feedback, trivia):
    ''' Given two texts of feedback and trivia,
    render them in the final/feedback_trivia.html template.'''
    context = {'feedback': feedback, 'trivia': trivia}
    return render_to_string(join('final',
        'feedback_trivia.html'), context)


def get_average_difference(session, num_turnpoints, initial_value):
    """
    return the average difference in milliseconds participants could hear
    """
    last_turnpoints = get_last_n_turnpoints(session, num_turnpoints)
    if last_turnpoints.count() == 0:
        last_result = get_fallback_result(session)
        if last_result:
            return float(last_result.section.song.name)
        else:
            # this cannot happen in DurationDiscrimination style blocks
            # for future compatibility, still catch the condition that there may be no results
            return initial_value
    return (sum([int(result.section.song.name) for result in last_turnpoints]) / last_turnpoints.count())


def get_average_difference_level_based(session, num_turnpoints, initial_value):
    """ calculate the difference based on exponential decay,
    starting from an initial_value """
    last_turnpoints = get_last_n_turnpoints(session, num_turnpoints)
    if last_turnpoints.count() == 0:
        # outliers
        last_result = get_fallback_result(session)
        if last_result:
            return initial_value / (2 ** (int(last_result.section.song.name.split('_')[-1]) - 1))
        else:
            # participant didn't pay attention,
            # no results right after the practice rounds
            return initial_value
    # Difference by level starts at initial value (which is level 1, so 20/(2^0)) and then halves for every next level
    return sum([initial_value / (2 ** (int(result.section.song.name.split('_')[-1]) - 1)) for result in last_turnpoints]) / last_turnpoints.count()


def get_fallback_result(session):
    """ if there were no turnpoints (outliers):
    return the last result, or if there are no results, return None
    """
    if session.result_set.count() == 0:
        # stopping right after practice rounds
        return None
    return session.result_set.order_by('-created_at')[0]


def get_last_n_turnpoints(session, num_turnpoints):
    """
    select all results associated with turnpoints in the result set
    return the last num_turnpoints results, or all turnpoint results if fewer than num_turnpoints
    """
    all_results = session.result_set.filter(comment__iendswith='turnpoint').order_by('-created_at').all()
    cutoff = min(all_results.count(), num_turnpoints)
    return all_results[:cutoff]


def randomize_playhead(min_jitter, max_jitter, continuation_correctness):
    return random.uniform(min_jitter, max_jitter) if not continuation_correctness else 0
