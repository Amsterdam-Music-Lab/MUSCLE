from random import shuffle

from django_markup.markup import formatter

from experiment.actions.consent import Consent
from image.serializers import serialize_image
from participant.models import Participant
from session.models import Session
from theme.serializers import serialize_theme
from .models import Block, ExperimentCollection, Phase, GroupedBlock, SocialMediaConfig


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
        'description': formatter(
            experiment_collection.description,
            filter_name='markdown'
        ),
    }

    if experiment_collection.consent:
        serialized['consent'] = Consent(experiment_collection.consent).action()

    if experiment_collection.theme_config:
        serialized['theme'] = serialize_theme(
            experiment_collection.theme_config
        )

    if experiment_collection.about_content:
        serialized['aboutContent'] = formatter(
            experiment_collection.about_content,
            filter_name='markdown'
        )

    if experiment_collection.social_media_config:
        serialized['socialMedia'] = serialize_social_media_config(
            experiment_collection.social_media_config
        )

    return serialized


def serialize_social_media_config(
        social_media_config: SocialMediaConfig
        ) -> dict:
    return {
        'tags': social_media_config.tags,
        'url': social_media_config.url,
        'content': social_media_config.content,
        'channels': social_media_config.channels,
    }


def serialize_phase(
        phase: Phase,
        participant: Participant
        ) -> dict:
    grouped_blocks = list(GroupedBlock.objects.filter(
        phase_id=phase.id).order_by('index'))

    if phase.randomize:
        shuffle(grouped_blocks)

    next_block = get_upcoming_block(
        grouped_blocks, participant, phase.dashboard)

    total_score = get_total_score(grouped_blocks, participant)

    if not next_block:
        return None

    return {
        'dashboard': [serialize_block(block.block, participant) for block in grouped_blocks] if phase.dashboard else [],
        'nextBlock': next_block,
        'totalScore': total_score
    }


def serialize_block(block_object: Block, participant: Participant):
    return {
        'slug': block_object.slug,
        'name': block_object.name,
        'description': block_object.description,
        'image': serialize_image(block_object.image) if block_object.image else None,
    }


def get_upcoming_block(block_list, participant, repeat_allowed=True):
    ''' return next block with minimum finished sessions for this participant
     if repeated blocks are not allowed (dashboard=False) and there are only finished sessions, return None '''
    finished_session_counts = [get_finished_session_count(
        block.block, participant) for block in block_list]
    minimum_session_count = min(finished_session_counts)
    if not repeat_allowed and minimum_session_count != 0:
        return None
    return serialize_block(block_list[finished_session_counts.index(minimum_session_count)].block, participant)


def get_started_session_count(block, participant):
    ''' Get the number of started sessions for this block and participant '''
    count = Session.objects.filter(
        block=block, participant=participant).count()
    return count


def get_finished_session_count(block, participant):
    ''' Get the number of finished sessions for this block and participant '''
    count = Session.objects.filter(
        block=block, participant=participant, finished_at__isnull=False).count()
    return count


def get_total_score(grouped_blocks, participant):
    '''Calculate total score of all blocks on the dashboard'''
    total_score = 0
    for grouped_block in grouped_blocks:
        sessions = Session.objects.filter(block=grouped_block.block, participant=participant)
        for session in sessions:
            total_score += session.final_score
    return total_score
