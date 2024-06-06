import json
import logging

from django.http import Http404, HttpRequest, JsonResponse
from django.conf import settings
from django.utils.translation import activate, gettext_lazy as _
from django_markup.markup import formatter

from .models import Experiment, ExperimentCollection, ExperimentCollectionGroup, Feedback
from section.models import Playlist
from experiment.serializers import serialize_actions, serialize_experiment_collection, serialize_experiment_collection_group
from experiment.rules import EXPERIMENT_RULES
from experiment.actions.utils import COLLECTION_KEY
from participant.utils import get_participant
from theme.serializers import serialize_theme

logger = logging.getLogger(__name__)


def get_experiment(request, slug):
    """Get experiment data from active experiment with given :slug
    DO NOT modify session data here, it will break participant_id system
       (/participant and /experiment/<slug> are called at the same time by the frontend)"""
    experiment = experiment_or_404(slug)
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
        'theme': serialize_theme(experiment.theme_config) if experiment.theme_config else None,
        'description': experiment.description,
        'image': experiment.image.file.url if experiment.image else '',
        'class_name': class_name,  # can be used to override style
        'rounds': experiment.rounds,
        'playlists': [
            {'id': playlist.id, 'name': playlist.name}
            for playlist in experiment.playlists.all()
        ],
        'feedback_info': experiment.get_rules().feedback_info(),
        'next_round': serialize_actions(experiment.get_rules().first_round(experiment)),
        'loading_text': _('Loading')
    }

    response = JsonResponse(experiment_data, json_dumps_params={'indent': 4})
    if experiment.language:
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, experiment.language)
    else:
        # avoid carrying over language cookie from other experiments
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, None)
    return response


def post_feedback(request, slug):
    text = request.POST.get('feedback')
    experiment = experiment_or_404(slug)
    feedback = Feedback(text=text, experiment=experiment)
    feedback.save()
    return JsonResponse({'status': 'ok'})


def experiment_or_404(slug):
    # get experiment
    try:
        return Experiment.objects.get(slug=slug, active=True)
    except Experiment.DoesNotExist:
        raise Http404("Experiment does not exist")


def default_questions(request, rules):
    return JsonResponse({'default_questions': [q.key for q in EXPERIMENT_RULES[rules]().questions]})


def get_experiment_collection(request: HttpRequest, slug: str, group_index: int = 0) -> JsonResponse:
    '''
    check which `ExperimentCollectionGroup` objects are related to the `ExperimentCollection` with the given slug
    retrieve the group with the lowest order (= current_group)
    return the next experiment from the current_group without a finished session
    except if ExperimentCollectionGroup.dashboard = True,
    then all experiments of the current_group will be returned as an array (also those with finished session)
    '''
    try:
        collection = ExperimentCollection.objects.get(slug=slug)
    except:
        return Http404
    request.session[COLLECTION_KEY] = slug
    participant = get_participant(request)
    groups = list(ExperimentCollectionGroup.objects.filter(
        series=collection.id).order_by('order'))
    try:
        current_group = groups[group_index]
        serialized_group = serialize_experiment_collection_group(
            current_group, participant)
        if not serialized_group:
            # if the current group is not a dashboard and has no unfinished experiments, it will return None
            # set it to finished and continue to next group
            group_index += 1
            return get_experiment_collection(request, slug, group_index=group_index)
    except IndexError:
        serialized_group = {
            'dashboard': [],
            'next_experiment': None
        }
    return JsonResponse({
        **serialize_experiment_collection(collection),
        **serialized_group
    })


def get_associated_experiments(pk_list):
    ''' get all the experiment objects registered in an ExperimentCollection field'''
    return [Experiment.objects.get(pk=pk) for pk in pk_list]


def render_markdown(request):

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

    if not request.body:
        return JsonResponse({'status': 'error', 'message': 'No body found in request'})

    if request.content_type != 'application/json':
        return JsonResponse({'status': 'error', 'message': 'Only application/json content type is allowed'})

    data = json.loads(request.body)
    markdown = data['markdown']

    if markdown:
        return JsonResponse({'html': formatter(markdown, filter_name='markdown')})

    return JsonResponse({'html': ''})


def validate_experiment_playlist(
        request: HttpRequest,
        rules_id: str
        ) -> JsonResponse:
    """
    Validate the playlist of an experiment based on the used rules
    """

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

    if not request.body:
        return JsonResponse({'status': 'error', 'message': 'No body found in request'})

    if request.content_type != 'application/json':
        return JsonResponse({'status': 'error', 'message': 'Only application/json content type is allowed'})

    json_body = json.loads(request.body)
    playlist_ids = json_body.get('playlists', [])
    playlists = Playlist.objects.filter(id__in=playlist_ids)

    if not playlists:
        return JsonResponse({'status': 'error', 'message': 'The experiment must have a playlist.'})

    rules = EXPERIMENT_RULES[rules_id]()

    if not rules.validate_playlist:
        return JsonResponse({'status': 'warn', 'message': 'This rulesset does not have a playlist validation.'})

    playlist_errors = []

    for playlist in playlists:
        errors = rules.validate_playlist(playlist)
        if errors:
            playlist_errors.append({
                'playlist': playlist.name,
                'errors': errors
                })

    if playlist_errors:
        return JsonResponse({'status': 'error', 'message': 'There are errors in the playlist.', 'errors': playlist_errors})

    return JsonResponse({'status': 'ok', 'message': 'The playlist is valid.'})
