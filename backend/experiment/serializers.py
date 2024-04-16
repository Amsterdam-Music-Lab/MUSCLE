from random import shuffle

from django_markup.markup import formatter

from participant.models import Participant
from session.models import Session
from .models import Experiment, ExperimentCollection, ExperimentCollectionGroup, GroupedExperiment


def serialize_actions(actions):
    ''' Serialize an array of actions '''
    if isinstance(actions, list):
        return [a.action() for a in actions]
    return actions.action()


def serialize_experiment_collection(
    experiment_series: ExperimentCollection
) -> dict:
    about_content = experiment_series.about_content

    if about_content:
        about_content = formatter(about_content, filter_name='markdown')

    return {
        'slug': experiment_series.slug,
        'name': experiment_series.name,
        'description': experiment_series.description,
        'about_content': about_content,
    }


def serialize_experiment_collection_group(group: ExperimentCollectionGroup, participant: Participant) -> dict:
    grouped_experiments = list(GroupedExperiment.objects.filter(
        group_id=group.id).order_by('order'))

    if group.randomize:
        shuffle(grouped_experiments)

    next_experiment = get_upcoming_experiment(
        grouped_experiments, participant, group.dashboard)

    if not next_experiment:
        return None

    return {
        'dashboard': [serialize_experiment(experiment.experiment, participant) for experiment in grouped_experiments] if group.dashboard else [],
        'next_experiment': next_experiment
    }


def serialize_experiment(experiment_object: Experiment, participant: Participant):
    return {
        'slug': experiment_object.slug,
        'name': experiment_object.name,
        'started_session_count': get_started_session_count(experiment_object, participant),
        'finished_session_count': get_finished_session_count(experiment_object, participant),
        'description': experiment_object.description,
        'image': experiment_object.image.file.url if experiment_object.image else '',
    }


def get_upcoming_experiment(experiment_list, participant, repeat_allowed=True):
    ''' return next experiment with minimum finished sessions for this participant
     if repeated experiments are not allowed (dashboard=False) and there are only finished sessions, return None '''
    finished_session_counts = [get_finished_session_count(
        experiment.experiment, participant) for experiment in experiment_list]
    minimum_session_count = min(finished_session_counts)
    if not repeat_allowed and minimum_session_count != 0:
        return None
    return serialize_experiment(experiment_list[finished_session_counts.index(minimum_session_count)].experiment, participant)


def get_started_session_count(experiment, participant):
    ''' Get the number of started sessions for this experiment and participant '''
    count = Session.objects.filter(
        experiment=experiment, participant=participant).count()
    return count


def get_finished_session_count(experiment, participant):
    ''' Get the number of finished sessions for this experiment and participant '''
    count = Session.objects.filter(
        experiment=experiment, participant=participant, finished_at__isnull=False).count()
    return count
