import logging

from django.http import Http404, JsonResponse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate

from experiment.models import Experiment

logger = logging.getLogger(__name__)

# Experiment


def get(request, slug):
    """Get experiment data from active experiment with given :slug"""
    # get experiment

    try:
        experiment = Experiment.objects.get(slug=slug, active=True)
    except Experiment.DoesNotExist:
        raise Http404("Experiment does not exist")

    class_name = ''
    if request.LANGUAGE_CODE.startswith('zh'):
        class_name = 'chinese'

    if experiment.language:
        activate(experiment.language)

    from django.urls import get_resolver
    print(get_resolver().url_patterns)
    
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
