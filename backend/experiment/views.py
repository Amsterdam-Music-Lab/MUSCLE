import logging
from random import shuffle

from django.http import Http404, JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate

from .models import Experiment, ExperimentSeries, Feedback
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
            return JsonResponse(upcoming_experiment)
    if collection.random_experiments:
        experiments = get_associated_experiments(collection.random_experiments)
        shuffle(experiments)
        if collection.dashboard:
            serialized = [serialize_experiment(experiment, check_finished_session(
                experiment, participant)) for experiment in experiments]
            return JsonResponse({'dashboard': serialized})
        else:
            upcoming_experiment = get_upcoming_experiment(
                experiments, participant)
            if upcoming_experiment:
                return JsonResponse(upcoming_experiment)
    if collection.last_experiments:
        experiments = get_associated_experiments(collection.last_experiments)
        upcoming_experiment = get_upcoming_experiment(experiments, participant)
        if upcoming_experiment:
            return JsonResponse(upcoming_experiment)
    return JsonResponse()


def serialize_experiment(experiment_object, finished=False):
    return {
        'slug': experiment_object.slug,
        'name': experiment_object.name,
        'finished': finished
    }


def check_finished_session(experiment, participant):
    ''' Check if there is a finished session for this experiment and participant '''
    try:
        Session.objects.get(
            experiment=experiment, participant=participant, finished_at__isnull=False)
        return True
    except:
        return False


def get_associated_experiments(pk_list):
    ''' get all the experiment objects registered in an ExperimentSeries field'''
    return [Experiment.objects.get(pk=pk) for pk in pk_list]


def get_upcoming_experiment(experiment_list, participant):
    ''' get next experiment for which there is no finished session for this participant '''
    upcoming = next((experiment for experiment in experiment_list if
                     check_finished_session(experiment, participant) is False), None)
    if upcoming:
        return serialize_experiment(upcoming)
