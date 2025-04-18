import copy
from os.path import join
from typing import Any, List, Optional

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, get_language
from django.contrib.postgres.fields import ArrayField
from django.db.models.query import QuerySet
from experiment.standards.iso_languages import ISO_LANGUAGES
from theme.models import ThemeConfig
from image.models import Image
from session.models import Session

from .validators import markdown_html_validator, block_slug_validator, experiment_slug_validator

language_choices = [(key, ISO_LANGUAGES[key]) for key in ISO_LANGUAGES.keys()]


class Experiment(models.Model):
    """A model to allow nesting multiple phases with blocks into a 'parent' experiment

    Attributes:
        slug (str): Slug
        translated_content (Queryset[ExperimentTranslatedContent]): Translated content
        theme_config (theme.ThemeConfig): ThemeConfig instance
        active (bool): Set experiment active
        social_media_config (SocialMediaConfig): SocialMediaConfig instance
        phases (Queryset[Phase]): Queryset of Phase instances
    """

    slug = models.SlugField(
        db_index=True, max_length=64, unique=True, null=True, validators=[experiment_slug_validator]
    )
    translated_content = models.QuerySet["ExperimentTranslatedContent"]
    theme_config = models.ForeignKey("theme.ThemeConfig", blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    social_media_config: Optional["SocialMediaConfig"]
    phases: models.QuerySet["Phase"]

    def __str__(self):
        translated_content = self.get_fallback_content()
        return translated_content.name if translated_content else self.slug

    @property
    def name(self):
        content = self.get_fallback_content()
        return content.name if content and content.name else ""

    class Meta:
        verbose_name_plural = "Experiments"

    def associated_blocks(self) -> list["Block"]:
        """Return a list of all associated blocks for this experiment

        Returns:
            Associated blocks
        """

        phases = self.phases.all()
        return [block for phase in phases for block in list(phase.blocks.all())]

    def export_sessions(self) -> QuerySet[Session]:
        """export sessions for this experiment

        Returns:
            Associated sessions
        """

        all_sessions = Session.objects.none()
        for block in self.associated_blocks():
            all_sessions |= Session.objects.filter(block=block).order_by("-started_at")
        return all_sessions

    def current_participants(self) -> list["Participant"]:
        """Get distinct list of participants

        Returns:
            (participant.models.Participant): Associated participants
        """

        participants = {}
        for session in self.export_sessions():
            participants[session.participant.id] = session.participant
        return participants.values()

    def export_feedback(self) -> QuerySet[Session]:
        """export feedback for the blocks in this experiment

        Returns:
            Associated block feedback
        """

        all_feedback = Feedback.objects.none()
        for block in self.associated_blocks():
            all_feedback |= Feedback.objects.filter(block=block)
        return all_feedback

    def get_fallback_content(self) -> "ExperimentTranslatedContent":
        """Get fallback content for the experiment

        Returns:
            Translated content
        """

        return self.translated_content.order_by("index").first()

    def get_translated_content(self, language: str, fallback: bool = True) -> "ExperimentTranslatedContent":
        """Get content for a specific language

        Args:
            language: Language code
            fallback: Return fallback language if language isn't available

        Returns:
            Translated content
        """

        content = self.translated_content.filter(language=language).first()

        if not content and fallback:
            fallback_content = self.get_fallback_content()

            if not fallback_content:
                raise ValueError("No fallback content found for experiment")

            return fallback_content

        if not content:
            raise ValueError(f"No content found for language {language}")

        return content

    def get_current_content(self, fallback: bool = True) -> "ExperimentTranslatedContent":
        """Get content for the 'current' language

        Args:
            fallback: Return fallback language if language isn't available

        Returns:
            Translated content
        """

        language = get_language()
        return self.get_translated_content(language, fallback)


def consent_upload_path(instance: Experiment, filename: str) -> str:
    """Generate path to save consent file based on experiment.slug and language

    Args:
        instance (Experiment): Experiment instance to determine folder name
        filename (str): Name of the consent file to be uploaded

    Returns:
        upload_to (str): Path for uploading the consent file

    Note:
        Used by the Block model for uploading consent file
    """
    experiment = instance.experiment
    folder_name = experiment.slug
    language = instance.language

    return join("consent", folder_name, f"{language}-{filename}")


class Phase(models.Model):
    """Root entity for configuring experiment phases

    Attributes:
        experiment (Experiment): Instance of an Experiment
        index (int): Index of the phase
        dashboard (bool): Should the dashbopard be displayed for this phase?
        randomize (bool): Should the blocks of this phase be randomized?
    """

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="phases")
    index = models.IntegerField(default=0, help_text="Index of the phase in the series. Lower numbers come first.")
    dashboard = models.BooleanField(default=False)
    randomize = models.BooleanField(default=False, help_text="Randomize the order of the blocks in this phase.")

    def __str__(self):
        default_content = self.experiment.get_fallback_content()
        experiment_name = default_content.name if default_content else None
        compound_name = experiment_name or self.experiment.slug or "Unnamed experiment"
        return f"{compound_name} ({self.index})"

    class Meta:
        ordering = ["index"]


class Block(models.Model):
    """Root entity for configuring experiment blocks

    Attributes:
        phase (Phase): The phase this block belongs to
        index (int): Index of this phase
        playlists (list(section.models.Playlist)): The playlist(s) used in this block
        image (image.models.Image): Image that will be showed on the dashboard
        slug (str): Slug for this block
        active (bool): Is this block active?
        rounds (int): Number of rounds
        bonus_points (int): Bonus points
        rules (str): The rules used for this block
        translated_content (BlockTranslatedContent): Translated content
        theme_config (theme.models.ThemeConfig): Theme settings
    """

    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name="blocks", blank=True, null=True)
    index = models.IntegerField(default=0, help_text="Index of the block in the phase. Lower numbers come first.")
    playlists = models.ManyToManyField("section.Playlist", blank=True)

    image = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(db_index=True, max_length=64, unique=True, validators=[block_slug_validator])

    rounds = models.PositiveIntegerField(default=10)
    bonus_points = models.PositiveIntegerField(default=0)
    rules = models.CharField(default="", max_length=64)

    theme_config = models.ForeignKey(ThemeConfig, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        # If this block is unsaved or being deleted (has no PK),
        # avoid calling get_fallback_content() (which does a DB query).
        if not self.pk:
            # Provide a fallback label or just return self.slug if present.
            return self.slug or "Deleted/Unsaved Block"

        content = self.get_fallback_content()
        return content.name if content and content.name else self.slug

    @property
    def name(self):
        """Name of the block, which will be used for dashboards"""
        content = self.get_fallback_content()
        return content.name if content and content.name else ""

    @property
    def description(self):
        content = self.get_fallback_content()
        return content.description if content and content.description else ""

    def session_count(self) -> int:
        """Number of sessions

        Returns:
            Number of sessions
        """

        return self.session_set.count()

    session_count.short_description = "Sessions"

    def playlist_count(self) -> int:
        """Number of playlists

        Returns:
            Number of playlists
        """

        return self.playlists.count()

    playlist_count.short_description = "Playlists"

    def current_participants(self) -> List["participant.models.Participant"]:
        """Get distinct list of participants

        Returns:
            Associated participants
        """

        participants = {}
        for session in self.session_set.all():
            participants[session.participant.id] = session.participant
        return participants.values()

    def _export_admin(self) -> dict:
        """Export data for admin

        Returns:
            Export data for admin

        """
        return {
            "exportedAt": timezone.now().isoformat(),
            "block": {
                "id": self.id,
                "name": self.name,
                "sessions": [session._export_admin() for session in self.session_set.all()],
                "participants": [participant._export_admin() for participant in self.current_participants()],
            },
        }

    def export_sessions(self):
        # export session objects
        return self.session_set.all()

    def get_rules(self) -> "experiment.rules.base.Base":
        """Get instance of rules class to be used for this session

        Returns:
            Rules
        """

        from experiment.rules import BLOCK_RULES

        if self.rules not in BLOCK_RULES:
            raise ValueError(f"Rules do not exist (anymore): {self.rules} for block {self.name} ({self.slug})")

        cl = BLOCK_RULES[self.rules]
        return cl()

    def max_score(self) -> int:
        """Get max score from all sessions with a positive score

        Returns:
            max score from all sessions with a positive score
        """

        score = self.session_set.filter(final_score__gte=0).aggregate(models.Max("final_score"))
        if "final_score__max" in score:
            return score["final_score__max"]

        return 0

    def add_default_question_series(self):
        """Add default question_series to block"""

        from experiment.rules import BLOCK_RULES
        from question.models import Question, QuestionSeries, QuestionInSeries

        question_series = getattr(BLOCK_RULES[self.rules](), "question_series", None)
        if question_series:
            for i, question_series in enumerate(question_series):
                qs = QuestionSeries.objects.create(
                    name=question_series["name"], block=self, index=i + 1, randomize=question_series["randomize"]
                )
                for i, question in enumerate(question_series["keys"]):
                    QuestionInSeries.objects.create(
                        question_series=qs, question=Question.objects.get(pk=question), index=i + 1
                    )

    def get_fallback_content(self) -> "BlockTranslatedContent | None":
        """Get fallback content for the block

        Returns:
            Fallback content
        """
        experiment = self.phase.experiment
        experiment_fallback_content = experiment.get_fallback_content()

        if not experiment_fallback_content or not experiment_fallback_content.language:
            return None

        experiment_fallback_language = experiment_fallback_content.language

        fallback_content = self.translated_contents.filter(language=experiment_fallback_language).first()

        return fallback_content

    def get_translated_content(self, language: str, fallback: bool = True) -> "BlockTranslatedContent":
        """Get content for a specific language

        Returns:
            Translated content
        """

        content = self.translated_contents.filter(language=language).first()

        if not content and fallback:
            fallback_content = self.get_fallback_content()

            if not fallback_content:
                raise ValueError("No fallback content found for block")

            return fallback_content

        if not content:
            raise ValueError(f"No content found for language {language}")

        return content

    def get_current_content(self, fallback: bool = True) -> "BlockTranslatedContent":
        """Get content for the 'current' language

        Returns:
            Translated content

        """
        language = get_language()
        return self.get_translated_content(language, fallback)


class TranslatedContent(models.Model):
    language = models.CharField(default="en", blank=True, choices=language_choices, max_length=2)

    class Meta:
        abstract = True


class ExperimentTranslatedContent(TranslatedContent):
    """Translated content for an Experiment

    Attributes:
        experiment (Experiment): Associated experiment
        index (int): Index
        language (str): Language code
        description (str): Description
        consent (FileField): Consent text markdown or html
        about_content (str): About text
        social_media_message (str): Message to post with on social media. Can contain {points} and {experiment_name} placeholders
        disclaimer (str): Disclaimer text
        privacy (str): Privacy statement text
    """

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="translated_content")
    index = models.IntegerField(default=0)
    name = models.CharField(max_length=64, default="")
    description = models.TextField(blank=True, default="")
    consent = models.FileField(
        upload_to=consent_upload_path, blank=True, default="", validators=[markdown_html_validator()]
    )
    about_content = models.TextField(blank=True, default="")
    social_media_message = models.TextField(
        blank=True,
        help_text=_("Content for social media sharing. Use {points} and {experiment_name} as placeholders."),
        default="I scored {points} points in {experiment_name}!",
    )
    disclaimer = models.TextField(blank=True, default="")
    privacy = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ["experiment", "language"]
        ordering = ["index"]


class BlockTranslatedContent(TranslatedContent):
    """Translated content for a Block

    Attributes:
        block (Block): Associated block
        language (str): Language code
        name (str): Block name
        description (str): Description

    """

    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name="translated_contents")
    name = models.CharField(max_length=64, default="")
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Block text: {ISO_LANGUAGES.get(self.language)}"

    class Meta:
        # Assures that there is only one translation per language
        unique_together = ["block", "language"]


class Feedback(models.Model):
    """A model for adding feedback to an experiment block

    Attributes:
        text (str): Text
        block (Block): Associated block
    """

    text = models.TextField()
    block = models.ForeignKey(Block, on_delete=models.CASCADE)


class SocialMediaConfig(models.Model):
    """Social media config for an experiment

    Attributes:
        experiment (Experiment): Experiment instance
        tags (list[str]): Tags
        url (str): Url to be shared
        channels (list[str]): Social media channel
    """

    experiment = models.OneToOneField(Experiment, on_delete=models.CASCADE, related_name="social_media_config")

    tags = ArrayField(
        models.CharField(max_length=100), blank=True, default=list, help_text=_("List of tags for social media sharing")
    )

    url = models.URLField(
        blank=True, help_text=_("URL to be shared on social media. If empty, the experiment URL will be used.")
    )

    SOCIAL_MEDIA_CHANNELS = [
        ("facebook", _("Facebook")),
        ("whatsapp", _("WhatsApp")),
        ("twitter", _("Twitter")),
        ("weibo", _("Weibo")),
        ("share", _("Share")),
        ("clipboard", _("Clipboard")),
    ]
    channels = ArrayField(
        models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHANNELS),
        blank=True,
        default=list,
        help_text=_("Selected social media channels for sharing"),
    )

    def get_content(self, score: float) -> str:
        """Get social media share content

        Args:
            score: Score
            experiment_name: Experiment name

        Returns:
            Social media shared text

        Raises:
            ValueError: If required parameters are missing when needed
        """
        translated_content = self.experiment.get_current_content()
        social_message = translated_content.social_media_message
        experiment_name = translated_content.name

        if social_message:
            has_placeholders = "{points}" in social_message and "{experiment_name}" in social_message

            if not has_placeholders:
                return social_message

            if has_placeholders and (score is None or experiment_name is None):
                raise ValueError("score and experiment_name are required for placeholder substitution")

            return social_message.format(points=score, experiment_name=experiment_name)

        if score is None or experiment_name is None:
            raise ValueError("score and name are required when no social media message is provided")

        return _("I scored %(score)d points in %(experiment_name)s") % {
            "score": score,
            "experiment_name": experiment_name,
        }

    def __str__(self):
        fallback_content = self.experiment.get_fallback_content()
        if fallback_content:
            return f"Social Media for {fallback_content.name}"

        return f"Social Media for {self.experiment.slug}"
