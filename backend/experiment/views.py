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
    ''' this view goes through all experiment in an ExperimentSeries in this order:
    first_experiments (fixed order)
    random_experiments (random order)
    last_experiments (fixed order)
    it will return the next experiment from one of these fields which has an unfinished session
    except if ExperimentSeries.dashboard = True,
    then all random_experiments will be returned as an array (also those with finished session)
    '''
    try:
        collection = ExperimentSeries.objects.get(slug=slug)
    except:
        return Http404
    request.session[COLLECTION_KEY] = slug
    participant = get_participant(request)
    if collection.first_experiments:
        experiments = get_associated_experiments(collection.first_experiments)
        upcoming_experiment = get_upcoming_experiment(experiments, participant)
        if upcoming_experiment:
            return JsonResponse(
                serialize_experiment_series(
                    collection,
                    redirect_to=upcoming_experiment
                )
            )
    if collection.random_experiments:
        experiments = get_associated_experiments(collection.random_experiments)
        shuffle(experiments)
        if collection.dashboard:
            serialized = [
                serialize_experiment(
                    experiment,
                    get_finished_session_count(experiment, participant)
                ) for experiment in experiments]
            return JsonResponse(
                serialize_experiment_series(
                    collection,
                    dashboard=serialized
                )
            )
        else:
            upcoming_experiment = get_upcoming_experiment(
                experiments, participant)
            if upcoming_experiment:
                return JsonResponse(
                    serialize_experiment_series(
                        collection,
                        redirect_to=upcoming_experiment
                    )
                )
    if collection.last_experiments:
        experiments = get_associated_experiments(collection.last_experiments)
        upcoming_experiment = get_upcoming_experiment(experiments, participant)
        if upcoming_experiment:
            return JsonResponse(
                serialize_experiment_series(
                    collection,
                    redirect_to=upcoming_experiment
                )
            )
    return JsonResponse()


def serialize_experiment_series_group(group: ExperimentSeriesGroup):
    grouped_experiments = GroupedExperiment.objects.filter(group_id=group.id).order_by('order')

    if group.randomize:
        grouped_experiments = list(grouped_experiments)
        shuffle(grouped_experiments)

    return {
        'name': group.name,
        'dashboard': group.dashboard,
        'experiments': [serialize_experiment(experiment.experiment) for experiment in grouped_experiments]
    }


def serialize_experiment_series(
    experiment_series: ExperimentSeries,
    dashboard: list = [],
    redirect_to: Experiment = None
):
    groups = ExperimentSeriesGroup.objects.filter(series_id=experiment_series.id)
    serialized_groups = [serialize_experiment_series_group(group) for group in groups]

    return {
        'slug': experiment_series.slug,
        'name': experiment_series.name,
        'description': experiment_series.description,
        'dashboard': dashboard,
        'redirect_to': redirect_to,
        'groups': serialized_groups,
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


def get_upcoming_experiment(experiment_list, participant):
    ''' get next experiment for which there is no finished session for this participant '''
    upcoming = next((experiment for experiment in experiment_list if
                     get_finished_session_count(experiment, participant) == 0), None)
    if upcoming:
        return serialize_experiment(upcoming)


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
