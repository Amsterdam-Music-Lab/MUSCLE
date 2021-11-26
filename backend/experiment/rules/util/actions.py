from django.conf import settings
from django.utils.translation import gettext_lazy as _

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

def final_action_with_optional_button(session, score_message, request_session):
    """ given a session, a score message and an optional session dictionary from an experiment series,
    return a Final.action, which has a button to continue to the next experiment if series is defined
    """
    if request_session:
        series_slug = request_session.get('experiment_series').get('slug')
        this_slug = session.experiment.slug
        request_session.update({'completed': {this_slug: True}})
        return Final.action(
            title=_('End'),
            session=session,
            score_message=score_message,
            button={
                'text': _('Continue'),
                'link': '{}/{}'.format(settings.CORS_ORIGIN_WHITELIST[0], series_slug)
            }
        )
    else:
        return Final.action(
            title=_('End'),
            session=session,
            score_message=score_message
        )
