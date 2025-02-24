from random import shuffle
from typing import Optional, TypedDict, Literal

from django_markup.markup import formatter
from django.utils.translation import activate, get_language
from rest_framework import serializers

from experiment.actions.consent import Consent
from image.serializers import serialize_image
from participant.models import Participant
from session.models import Session
from theme.serializers import serialize_theme
from .models import Block, Experiment, Phase, SocialMediaConfig, ExperimentTranslatedContent, BlockTranslatedContent
from section.models import Playlist
from question.models import QuestionSeries, QuestionInSeries, Question


class ExperimentTranslatedContentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ExperimentTranslatedContent
        fields = ["id", "index", "language", "name", "description", "about_content", "social_media_message"]


class BlockTranslatedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockTranslatedContent
        fields = ["language", "name", "description"]


class PlaylistSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Playlist
        fields = ["id", "name"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "key",
            "question",
            "type",
            "is_skippable",
            "explainer",
            "scale_steps",
            "profile_scoring_rule",
            "min_value",
            "max_value",
            "max_length",
            "min_values",
            "view",
        ]


class QuestionInSeriesSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=False)
    question_key = serializers.SlugRelatedField(
        source="question", queryset=Question.objects.all(), write_only=True, slug_field="key"
    )

    class Meta:
        model = QuestionInSeries
        fields = ["id", "question", "question_key", "index"]

    def to_internal_value(self, data):
        if isinstance(data, str):
            # Handle the case where only a question key is provided
            return {"question_key": data}
        return super().to_internal_value(data)


class QuestionSeriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    questions = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(), allow_empty=False), write_only=True, required=False
    )

    class Meta:
        model = QuestionSeries
        fields = [
            "id",
            "name",
            "index",
            "randomize",
            "questions",
        ]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        question_series = QuestionSeries.objects.create(**validated_data)
        self._handle_questions(question_series, questions_data)
        return question_series

    def update(self, instance, validated_data):
        questions_data = validated_data.pop("questions", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Clear existing questions and create new ones
        self._handle_questions(instance, questions_data)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["questions"] = [
            {"key": q.question.key, "index": q.index} for q in instance.questioninseries_set.all()
        ]
        return representation

    def _handle_questions(self, question_series, questions_data):
        # Get existing questions
        existing_questions = {qs.question.key: qs for qs in question_series.questioninseries_set.all()}

        # Create set of new question keys
        new_question_keys = set()

        for question_data in questions_data:
            question_key = question_data["key"]
            question_index = question_data.get("index", 0)
            new_question_keys.add(question_key)

            if question_key not in existing_questions:
                # Only create new questions that don't exist
                question = Question.objects.get(key=question_key)
                QuestionInSeries.objects.create(
                    question_series=question_series, question=question, index=question_index
                )
            else:
                # Update index of existing question
                existing_questions[question_key].index = question_index
                existing_questions[question_key].save()

        # Remove questions that are not in the new set
        question_series.questioninseries_set.filter(
            question__key__in=set(existing_questions.keys()) - new_question_keys
        ).delete()


class BlockSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    translated_contents = BlockTranslatedContentSerializer(many=True, required=False, read_only=False)
    playlists = PlaylistSerializer(many=True, required=False)
    questionseries_set = QuestionSeriesSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Block
        fields = [
            "id",
            "index",
            "slug",
            "rounds",
            "bonus_points",
            "rules",
            "translated_contents",
            "playlists",
            "questionseries_set",
        ]
        extra_kwargs = {
            "slug": {"validators": []},
        }

    def create(self, validated_data):
        translated_contents_data = validated_data.pop("translated_contents", [])
        playlists_data = validated_data.pop("playlists", [])
        question_series_data = validated_data.pop("questionseries_set", [])
        block = Block.objects.create(**validated_data)

        for content_data in translated_contents_data:
            BlockTranslatedContent.objects.create(block=block, **content_data)

        for playlist_data in playlists_data:
            playlist = Playlist.objects.get(pk=playlist_data["id"])
            block.playlists.add(playlist)

        for series_data in question_series_data:
            series_serializer = QuestionSeriesSerializer(data=series_data)
            series_serializer.is_valid(raise_exception=True)
            series_serializer.save(block=block)

        return block

    def update(self, instance, validated_data):
        translated_contents_data = validated_data.pop("translated_contents", [])
        playlists_data = validated_data.pop("playlists", [])
        question_series_data = validated_data.pop("questionseries_set", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        BlockTranslatedContent.objects.filter(block=instance).delete()
        for content_data in translated_contents_data:
            BlockTranslatedContent.objects.create(block=instance, **content_data)

        existing_playlist_ids = set()
        for playlist_data in playlists_data:
            playlist_id = playlist_data.get("id")
            if playlist_id:
                playlist = Playlist.objects.get(pk=playlist_id)
                instance.playlists.add(playlist)
                existing_playlist_ids.add(playlist.id)

        # Delete removed playlists
        instance.playlists.exclude(id__in=existing_playlist_ids).delete()

        # Handle question series
        if question_series_data is not None:
            existing_series_ids = set()

            for series_data in question_series_data:
                series_id = series_data.get("id")
                if series_id:
                    series = QuestionSeries.objects.get(id=series_id)
                    series_serializer = QuestionSeriesSerializer(series, data=series_data)
                else:
                    series_serializer = QuestionSeriesSerializer(data=series_data)

                if series_serializer.is_valid(raise_exception=True):
                    series = series_serializer.save(block=instance)
                    existing_series_ids.add(series.id)

            # Delete removed series
            instance.questionseries_set.exclude(id__in=existing_series_ids).delete()

        instance.save()

        return instance


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


from django.utils.translation import gettext_lazy as _


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
        serialized["backButtonText"] = _("Back")

    if translated_content.disclaimer:
        serialized["disclaimer"] = formatter(translated_content.disclaimer, filter_name="markdown")

    if translated_content.privacy:
        serialized["privacy"] = formatter(translated_content.privacy, filter_name="markdown")

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
