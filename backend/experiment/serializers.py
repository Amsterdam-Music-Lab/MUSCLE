from random import shuffle
from typing import Optional, TypedDict, Literal

from django_markup.markup import formatter
from django.utils.translation import activate, get_language
from rest_framework import serializers

from experiment.actions.consent import Consent
from image.serializers import serialize_image
from participant.models import Participant
from result.models import Result
from session.models import Session
from theme.serializers import serialize_theme
from .models import Block, Experiment, Phase, SocialMediaConfig, ExperimentTranslatedContent


class ExperimentTranslatedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentTranslatedContent
        fields = ["id", "index", "language", "name", "description", "about_content", "social_media_message"]


class BlockSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Block
        fields = [
            "id",
            "index",
            "slug",
            "rounds",
            "bonus_points",
            "rules",
        ]
        extra_kwargs = {
            "slug": {"validators": []},
        }


class PhaseSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True, required=False)

    class Meta:
        model = Phase
        fields = ["id", "index", "dashboard", "randomize", "blocks"]


class ExperimentSerializer(serializers.ModelSerializer):
    translated_content = ExperimentTranslatedContentSerializer(many=True, required=False)
    phases = PhaseSerializer(many=True, required=False)

    class Meta:
        model = Experiment
        fields = ["id", "slug", "active", "translated_content", "phases"]

    def create(self, validated_data):
        translated_content_data = validated_data.pop("translated_content", [])
        phases_data = validated_data.pop("phases", [])
        experiment = Experiment.objects.create(**validated_data)

        for content_data in translated_content_data:
            ExperimentTranslatedContent.objects.create(experiment=experiment, **content_data)

        for phase_data in phases_data:
            blocks_data = phase_data.pop("blocks", [])
            phase = Phase.objects.create(experiment=experiment, **phase_data)

            for block_data in blocks_data:
                Block.objects.create(phase=phase, **block_data)

        return experiment

    def update(self, instance, validated_data):
        translated_content_data = validated_data.pop("translated_content", [])
        phases_data = validated_data.pop("phases", [])

        # Update experiment fields
        instance.slug = validated_data.get("slug", instance.slug)
        instance.active = validated_data.get("active", instance.active)
        instance.save()

        # Update translated content
        if translated_content_data is not None:
            existing_content_ids = set()

            # Update or create translated content
            for content_data in translated_content_data:
                content_id = content_data.get("id")
                if content_id:
                    content, _ = ExperimentTranslatedContent.objects.update_or_create(
                        id=content_id, experiment=instance, defaults=content_data
                    )
                else:
                    content = ExperimentTranslatedContent.objects.create(experiment=instance, **content_data)
                existing_content_ids.add(content.id)

            # Delete removed content
            instance.translated_content.exclude(id__in=existing_content_ids).delete()

        # Update phases
        if phases_data is not None:
            existing_phase_ids = set()

            # Update or create phases
            for phase_data in phases_data:
                blocks_data = phase_data.pop("blocks", [])
                phase_id = phase_data.get("id")

                if phase_id:
                    phase, _ = Phase.objects.update_or_create(id=phase_id, experiment=instance, defaults=phase_data)
                else:
                    phase = Phase.objects.create(experiment=instance, **phase_data)
                existing_phase_ids.add(phase.id)

                # Handle blocks for this phase
                existing_block_ids = set()

                for block_data in blocks_data:
                    block_id = block_data.get("id")

                    print("MEKKA", block_data, block_id)

                    if block_id:
                        block_instance = Block.objects.get(pk=block_id)
                        block_serializer = BlockSerializer(block_instance, data=block_data, partial=True)
                    else:
                        block_serializer = BlockSerializer(data=block_data, partial=True)
                    block_serializer.is_valid(raise_exception=True)
                    block = block_serializer.save(phase=phase)
                    existing_block_ids.add(block.id)

                # Delete removed blocks
                phase.blocks.exclude(id__in=existing_block_ids).delete()

            # Delete removed phases
            instance.phases.exclude(id__in=existing_phase_ids).delete()

        return instance


def serialize_actions(actions):
    """Serialize an array of actions"""
    if isinstance(actions, list):
        return [a.action() for a in actions]
    return actions.action()


def get_experiment_translated_content(experiment):
    language_code = get_language()[0:2]

    translated_content = experiment.get_translated_content(language_code)

    if not translated_content:
        raise ValueError("No translated content found for this experiment")

    # set language cookie to the first available translation for this experiment
    activate(translated_content.language)
    return translated_content


def serialize_experiment(experiment: Experiment) -> dict:
    """Serialize experiment

    Args:
        experiment: Experiment instance

    Returns:
        Basic info about an experiment
    """

    translated_content = get_experiment_translated_content(experiment)

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
        A dictionary of the dashboard (if applicable), the next block, and the total score of the phase
    """
    blocks = list(phase.blocks.order_by("index").all())

    next_block = get_upcoming_block(phase, participant, times_played)
    if not next_block:
        return None

    total_score = get_total_score(blocks, participant)
    if phase.randomize:
        shuffle(blocks)

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


def get_upcoming_block(phase: Phase, participant: Participant, times_played: int) -> dict:
    """return next block with minimum finished sessions for this participant
    if all blocks have been played an equal number of times, return None

    Args:
        phase: Phase for which next block needs to be picked
        participant: Participant for which next block needs to be picked
    """
    blocks = list(phase.blocks.all())

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


def get_total_score(blocks: list, participant: Participant) -> int:
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
