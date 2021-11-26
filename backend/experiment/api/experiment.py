import logging

from django.http import Http404, JsonResponse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate

from experiment.models import Experiment, Session

logger = logging.getLogger(__name__)

# Experiment


def get(request, slug):
    """Get experiment data from active experiment with given :slug"""
    # get experiment
    try:
        experiment = Experiment.objects.get(slug=slug, active=True)
    except Experiment.DoesNotExist:
        raise Http404("Experiment does not exist")
    
    if experiment.nested_experiments:
        # we are in the middle of a test battery
        series_data = request.session.get('experiment_series')
        try:
            session = Session.objects.get(pk=series_data.get('session_id'))
        except Session.DoesNotExist:
            raise Http404("Session does not exist")
        # TODO: if participant did not complete any experiment in nested_experiments but not in experiment json_data, add these to the top of the stack
        data = {
            'session': {
                'id': session.id,
                'playlist': session.playlist.id,
                'json_data': session.load_json_data(),
            },
            'next_round': session.experiment_rules().next_round(session)
        }
        return JsonResponse(data, json_dumps_params={'indent': 4})

    class_name = ''
    if request.LANGUAGE_CODE.startswith('zh'):
        class_name = 'chinese'

    if experiment.language:
        activate(experiment.language)
    
    # create data
    experiment_data = {
        'id': experiment.id,
        'slug': experiment.slug,
        'name': experiment.name,
        'class_name': class_name,  # can be used to override style
        'rounds': experiment.rounds,
        'playlists': [
            {'id': playlist.id, 'name': playlist.name}
            for playlist in experiment.playlists.all()
        ],
        'first_round': experiment.get_rules().first_round(experiment),
        'loading_text': _('Loading')
    }

    response = JsonResponse(experiment_data, json_dumps_params={'indent': 4})
    if experiment.language:
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, experiment.language)
    else:
        # avoid carrying over language cookie from other experiments
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, None)
    return response