from os.path import join

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from experiment.rules.views import Final

def combine_actions(*argv):
    """Combine actions, make them next_round of each predecessor"""
    last = None
    for action in reversed(argv):
        # Skip empty actions
        if not action:
            continue
        if last:
            action['next_round'] = last
        last = action

    # Action stored in last is actually the first action
    return last

def final_action_with_optional_button(session, final_text, request_session):
    """ given a session, a score message and an optional session dictionary from an experiment series,
    return a Final.action, which has a button to continue to the next experiment if series is defined
    """
    if request_session:
        from experiment.models import Session
        series_data = request_session.get('experiment_series')
        series_slug = series_data.get('slug')
        series_session = Session.objects.get(pk=series_data.get('session_id'))
        series_session.final_score += 1
        series_session.save()
        return Final(
            title=_('End'),
            session=session,
            final_text=final_text,
            button={
                'text': _('Continue'),
                'link': '{}/{}'.format(settings.CORS_ORIGIN_WHITELIST[0], series_slug)
            }
        ).action()
    else:
        return Final(
            title=_('End'),
            session=session,
            final_text=final_text,
        ).action()

def render_feedback_trivia(feedback, trivia):
    ''' Given two texts of feedback and trivia,
    render them in the final/feedback_trivia.html template.'''
    context = {'feedback': feedback, 'trivia': trivia}
    return render_to_string(join('final',
        'feedback_trivia.html'), context)
