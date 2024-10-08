from random import shuffle

from django_markup.markup import formatter

from experiment.actions.consent import Consent
from image.serializers import serialize_image
from participant.models import Participant
from session.models import Session
from theme.serializers import serialize_theme
from .models import Block, Experiment, Phase, SocialMediaConfig


def serialize_actions(actions):
    """Serialize an array of actions"""
    if isinstance(actions, list):
        return [a.action() for a in actions]
    return actions.action()


def serialize_experiment(experiment: Experiment, language: str = "en") -> dict:
    """Serialize experiment

    Args:
        experiment: Experiment instance

    Returns:
        Basic info about an experiment
    """

    translated_content = experiment.get_translated_content(language)

    if not translated_content:
        raise ValueError("No translated content found for experiment")

    serialized = {
        "slug": experiment.slug,
        "name": translated_content.name,
        "description": formatter(translated_content.description, filter_name="markdown"),
    }

    if translated_content.consent:
        serialized["consent"] = Consent(translated_content.consent).action()
    elif experiment.get_fallback_content() and experiment.get_fallback_content().consent:
        serialized["consent"] = Consent(experiment.get_fallback_content().consent).action()

    if experiment.theme_config:
        serialized["theme"] = serialize_theme(experiment.theme_config)

    if translated_content.about_content:
        serialized["aboutContent"] = formatter(translated_content.about_content, filter_name="markdown")

    if hasattr(experiment, "social_media_config") and experiment.social_media_config:
        serialized["socialMedia"] = serialize_social_media_config(experiment.social_media_config)

    return serialized


def serialize_social_media_config(social_media_config: SocialMediaConfig) -> dict:
    """Serialize social media config

    Args:
        social_media_config: SocialMediaConfig instance

    returns:
        Basic social media info
    """

    return {
        "tags": social_media_config.tags,
        "url": social_media_config.url,
        "content": social_media_config.get_content(),
        "channels": social_media_config.channels,
    }


def serialize_phase(phase: Phase, participant: Participant) -> dict:
    """Serialize phase

    Args:
        phase: Phase instance
        participant: Participant instance

    Returns:
        Dashboard info for a participant
    """

    blocks = list(Block.objects.filter(phase=phase.id).order_by("index"))

    if phase.randomize:
        shuffle(blocks)

    next_block = get_upcoming_block(blocks, participant, phase.dashboard)

    total_score = get_total_score(blocks, participant)

    if not next_block:
        return None

    return {
        "dashboard": [serialize_block(block, participant) for block in blocks] if phase.dashboard else [],
        "nextBlock": next_block,
        "totalScore": total_score,
    }


def serialize_block(block_object: Block, language: str = "en") -> dict:
    """Serialize block

    Args:
        block_object: Block instance
        language: Language code

    Returns:
        Block info for a participant
    """

    return {
        "slug": block_object.slug,
        "name": block_object.name,
        "description": block_object.description,
        "image": serialize_image(block_object.image) if block_object.image else None,
    }


def get_upcoming_block(block_list: list[Block], participant: Participant, repeat_allowed: bool = True):
    """return next block with minimum finished sessions for this participant
    if repeated blocks are not allowed (dashboard=False) and there are only finished sessions, return None

    Args:
        block_list: List of Block instances
        participant: Participant instance
        repeat_allowed: Allow repeating a block
    """

    finished_session_counts = [get_finished_session_count(block, participant) for block in block_list]
    minimum_session_count = min(finished_session_counts)
    if not repeat_allowed and minimum_session_count != 0:
        return None
    return serialize_block(block_list[finished_session_counts.index(minimum_session_count)], participant)


def get_started_session_count(block: Block, participant: Participant) -> int:
    """Get the number of started sessions for this block and participant

    Args:
        block: Block instance
        participant: Participant instance

    Returns:
        Number of started sessions for this block and participant
    """

    count = Session.objects.filter(block=block, participant=participant).count()
    return count


def get_finished_session_count(block: Block, participant: Participant) -> int:
    """Get the number of finished sessions for this block and participant

    Args:
        block: Block instance
        participant: Participant instance

    Returns:
        Number of finished sessions for this block and participant
    """

    count = Session.objects.filter(block=block, participant=participant, finished_at__isnull=False).count()
    return count


def get_total_score(blocks: list, participant: dict) -> int:
    """Calculate total score of all blocks on the dashboard

    Args:
        blocks: All blocks on the dashboard
        participant: The participant we want the total score from

    Returns:
        Total score of given the blocks for this participant
    """

    total_score = 0
    for block in blocks:
        sessions = Session.objects.filter(block=block, participant=participant)

        for session in sessions:
            total_score += session.final_score
    return total_score
