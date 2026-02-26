from random import shuffle
from typing import Optional, TypedDict, Literal

from django.db.models import Sum
from django_markup.markup import formatter
from django.utils.translation import gettext_lazy as _

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


def serialize_experiment(experiment: Experiment) -> dict:
    """Serialize experiment

    Args:
        experiment: Experiment instance

    Returns:
        Basic info about an experiment
    """

    serialized = {
        "slug": experiment.slug,
        "name": experiment.name,
        "description": formatter(experiment.description, filter_name="markdown"),
    }

    if experiment.consent:
        serialized["consent"] = Consent(experiment.consent).action()

    if experiment.theme_config:
        serialized["theme"] = serialize_theme(experiment.theme_config)

    if experiment.about_content:
        serialized["aboutContent"] = formatter(
            experiment.about_content, filter_name="markdown"
        )
        serialized["backButtonText"] = _("Back")

    if experiment.disclaimer:
        serialized["disclaimer"] = formatter(
            experiment.disclaimer, filter_name="markdown"
        )

    if experiment.privacy:
        serialized["privacy"] = formatter(experiment.privacy, filter_name="markdown")

    if hasattr(experiment, "social_media_config") and experiment.social_media_config:
        serialized["socialMedia"] = serialize_social_media_config(experiment.social_media_config)

    return serialized


class SocialMediaConfigConfiguration(TypedDict):
    channels: list[Literal["facebook", "whatsapp", "twitter", "weibo", "share", "clipboard"]] | list[str]
    url: str
    content: str
    tags: list[str]


def serialize_social_media_config(
    social_media_config: SocialMediaConfig,
    score: Optional[float] = 0,
) -> SocialMediaConfigConfiguration:
    return {
        "tags": social_media_config.tags or ["amsterdammusiclab", "citizenscience"],
        "url": social_media_config.url,
        "content": social_media_config.get_content(score),
        "channels": social_media_config.channels or ["facebook", "twitter"],
    }


def serialize_phase(phase: Phase, participant: Participant, times_played: int) -> dict:
    """Serialize phase

    Args:
        phase: Phase instance
        participant: Participant instance

    Returns:
        a dictionary of the dashboard (if applicable),
        the next block,
        number of sessions played
        accumlated score of the phase
    """
    blocks = list(phase.blocks.order_by("index").all())

    next_block = get_upcoming_block(phase, participant, times_played)
    if not next_block:
        return None

    session_info = get_session_info(blocks, participant)

    if phase.randomize:
        shuffle(blocks)

    return {
        "dashboard": [serialize_block(block, participant) for block in blocks] if phase.dashboard else [],
        "nextBlock": next_block,
        **session_info
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


def get_upcoming_block(phase: Phase, participant: Participant, times_played: int) -> dict:
    """return next block with minimum finished sessions for this participant
    if all blocks have been played an equal number of times, return None

    Args:
        phase: Phase for which next block needs to be picked
        participant: Participant for which next block needs to be picked
    """
    blocks = list(phase.blocks.all())

    if phase.randomize:
        shuffle(blocks)
    finished_session_counts = [get_finished_session_count(block, participant) for block in blocks]

    min_session_count = min(finished_session_counts)
    if not phase.dashboard:
        if times_played != min_session_count:
            return None
    next_block_index = finished_session_counts.index(min_session_count)
    return serialize_block(blocks[next_block_index])


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

    return Session.objects.filter(block=block, participant=participant, finished_at__isnull=False).count()


def get_session_info(blocks: list[Block], participant: Participant) -> dict:
    """Return information of the sessions played by this participant in the blocks of this phase

    Args:
        blocks: All blocks from the current phase
        participant: The participant currently playing

    Returns:
        dict with session count and accumulated score
    """
    participant_sessions = participant.sessions.filter(
        block__in=blocks
    )
    accumulated_score = participant_sessions.aggregate(
        total_score=Sum("final_score")
    )["total_score"] or 0

    return {
        "playedSessions": participant_sessions.count(),
        "accumulatedScore": accumulated_score
    }
