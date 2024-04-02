import json
import logging
from random import shuffle

from django.http import Http404, JsonResponse
from django.conf import settings
from django.utils.translation import activate, gettext_lazy as _
from django_markup.markup import formatter

from .models import Experiment, ExperimentSeries, ExperimentSeriesGroup, Feedback, GroupedExperiment
from .utils import serialize
from participant.utils import get_participant
from participant.models import Participant
from session.models import Session
from experiment.rules import EXPERIMENT_RULES
from experiment.actions.utils import COLLECTION_KEY

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
        'theme': experiment.theme_config.__to_json__() if experiment.theme_config else None,
        'class_name': class_name,  # can be used to override style
        'rounds': experiment.rounds,
        'playlists': [
            {'id': playlist.id, 'name': playlist.name}
            for playlist in experiment.playlists.all()
        ],
        'feedback_info': experiment.get_rules().feedback_info(),
        'next_round': serialize(experiment.get_rules().first_round(experiment)),
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


def get_experiment_collection(request, slug):
    ''' 
    check which `ExperimentSeriesGroup` objects are related to the `ExperimentSeries` with the given slug
    retrieve the group with the lowest order (= current_group)
    return the next experiment from the current_group without a finished session
    except if ExperimentSeriesGroup.dashboard = True,
    then all experiments of the current_group will be returned as an array (also those with finished session)
    '''
    try:
        collection = ExperimentSeries.objects.get(slug=slug)
    except:
        return Http404
    request.session[COLLECTION_KEY] = slug
    participant = get_participant(request)
    active_groups = ExperimentSeriesGroup.objects.filter(
        series=collection.id, finished=False).order_by('order')
    if not active_groups:
        return JsonResponse({})
    current_group = active_groups.first()
    serialized_group = serialize_experiment_series_group(
        current_group, participant)
    if not serialized_group:
        # if the current group is not a dashboard and has no unfinished experiments, it will return None
        return get_experiment_collection(request, slug)
    return JsonResponse({
        **serialize_experiment_series(collection),
        **serialized_group
    })


def serialize_experiment_series_group(group: ExperimentSeriesGroup, participant: Participant) -> dict:
    grouped_experiments = list(GroupedExperiment.objects.filter(
        group_id=group.id).order_by('order'))

    if group.randomize:
        shuffle(grouped_experiments)

    next_experiment = get_upcoming_experiment(
        grouped_experiments, participant, group.dashboard)

    if not next_experiment:
        group.finished = True
        group.save()
        return None

    return {
        'dashboard': [serialize_experiment(experiment.experiment) for experiment in grouped_experiments] if group.dashboard else None,
        'next_experiment': next_experiment
    }


def serialize_experiment_series(
    experiment_series: ExperimentSeries
):
    about_content = experiment_series.about_content

    if about_content:
        about_content = formatter(about_content, filter_name='markdown')

    return {
        'slug': experiment_series.slug,
        'name': experiment_series.name,
        'description': experiment_series.description,
        'about_content': about_content,
    }


def serialize_experiment(experiment_object: Experiment, finished=0):
    return {
        'slug': experiment_object.slug,
        'name': experiment_object.name,
        'finished_session_count': finished,
        'description': experiment_object.description,
        'image': experiment_object.image.file.url if experiment_object.image else '',
    }


def get_finished_session_count(experiment, participant):
    ''' Get the number of finished sessions for this experiment and participant '''
    count = Session.objects.filter(
        experiment=experiment, participant=participant, finished_at__isnull=False).count()
    return count


def get_associated_experiments(pk_list):
    ''' get all the experiment objects registered in an ExperimentSeries field'''
    return [Experiment.objects.get(pk=pk) for pk in pk_list]


def get_upcoming_experiment(experiment_list, participant, repeat_allowed=True):
    ''' return next experiment with minimum finished sessions for this participant
     if repeated experiments are not allowed (dashboard=False) and there are only finished sessions, return None '''
    finished_session_counts = [get_finished_session_count(
        experiment.experiment, participant) for experiment in experiment_list]
    minimum_session_count = min(finished_session_counts)
    if not repeat_allowed and minimum_session_count != 0:
        return None
    return serialize_experiment(experiment_list[finished_session_counts.index(minimum_session_count)].experiment)


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
