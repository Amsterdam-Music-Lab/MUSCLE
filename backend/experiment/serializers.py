from random import shuffle

from django_markup.markup import formatter

from experiment.actions.consent import Consent
from image.serializers import serialize_image
from participant.models import Participant
from session.models import Session
from theme.serializers import serialize_theme
from .models import Experiment, ExperimentCollection, ExperimentCollectionGroup, GroupedExperiment


def serialize_actions(actions):
    ''' Serialize an array of actions '''
    if isinstance(actions, list):
        return [a.action() for a in actions]
    return actions.action()


def serialize_experiment_collection(
    experiment_collection: ExperimentCollection
) -> dict:

    serialized = {
        'slug': experiment_collection.slug,
        'name': experiment_collection.name,
        'description': experiment_collection.description,
    }

    if experiment_collection.consent:
        serialized['consent'] = Consent(experiment_collection.consent).action()

    if experiment_collection.theme_config:
        serialized['theme'] = serialize_theme(
            experiment_collection.theme_config)

    if experiment_collection.about_content:
        serialized['aboutContent'] = formatter(
            experiment_collection.about_content, filter_name='markdown')

    return serialized


def serialize_experiment_collection_group(group: ExperimentCollectionGroup, participant: Participant) -> dict:
    grouped_experiments = list(GroupedExperiment.objects.filter(
        group_id=group.id).order_by('order'))

    if group.randomize:
        shuffle(grouped_experiments)

    next_experiment = get_upcoming_experiment(
        grouped_experiments, participant, group.dashboard)

    total_score = get_total_score(grouped_experiments, participant)

    if not next_experiment:
        return None

    return {
        'dashboard': [serialize_experiment(experiment.experiment, participant) for experiment in grouped_experiments] if group.dashboard else [],
        'nextExperiment': next_experiment,
        'totalScore': total_score
    }


def serialize_experiment(experiment_object: Experiment, participant: Participant):
    return {
        'slug': experiment_object.slug,
        'name': experiment_object.name,
        'description': experiment_object.description,
        'image': serialize_image(experiment_object.image) if experiment_object.image else None,
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


def get_total_score(grouped_experiments, participant):
    '''Calculate total score of all experiments on the dashboard'''
    total_score = 0
    for grouped_experiment in grouped_experiments:
        sessions = Session.objects.filter(experiment=grouped_experiment.experiment, participant=participant)
        for session in sessions:
            total_score += session.final_score
    return total_score
