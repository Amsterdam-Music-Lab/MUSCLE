from os.path import join
from typing import Optional

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


def consent_upload_path(instance, filename) -> str:
    """Generate path to save consent file based on experiment.slug and language
    Returns:
        upload_to (str): Path for uploading the consent file
    """
    folder_name = instance.slug
    language = get_language()
    return join("consent", folder_name, f"consent_{language}", filename)


class Experiment(models.Model):
    """A model to allow nesting multiple phases with blocks into a 'parent' experiment

    Attributes:
        slug (str): Slug
        name (str): Name of the experiment
        description (str): Description
        consent (FileField): Consent text markdown or html
        about_content (str): About text
        social_media_message (str): Message to post with on social media. Can contain {points} and {experiment_name} placeholders
        disclaimer (str): Disclaimer text
        privacy (str): Privacy statement text
        theme_config (theme.ThemeConfig): ThemeConfig instance
        active (bool): Set experiment active
        social_media_config (SocialMediaConfig): SocialMediaConfig instance
        phases (Queryset[Phase]): Queryset of Phase instances
    """

    slug = models.SlugField(
        db_index=True,
        max_length=64,
        unique=True,
        null=True,
        validators=[experiment_slug_validator],
    )
    name = models.CharField(max_length=64, blank=True, default="")
    description = models.TextField(blank=True, default="")
    consent = models.FileField(
        upload_to=consent_upload_path,
        blank=True,
        default="",
        validators=[markdown_html_validator()],
    )
    about_content = models.TextField(blank=True, default="")
    social_media_message = models.TextField(
        blank=True,
        help_text=_(
            "Content for social media sharing. Use {points} and {experiment_name} as placeholders."
        ),
        default="I scored {points} points in {experiment_name}!",
    )
    disclaimer = models.TextField(blank=True, default="")
    privacy = models.TextField(blank=True, default="")
    theme_config = models.ForeignKey("theme.ThemeConfig", blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    social_media_config: Optional["SocialMediaConfig"]
    phases: models.QuerySet["Phase"]

    def __str__(self):
        return self.name or self.slug

    class Meta:
        verbose_name_plural = "Experiments"

    def associated_blocks(self) -> list["Block"]:
        """Return a list of all associated blocks for this experiment

        Returns:
            Associated blocks
        """

        return Block.objects.filter(phase__experiment=self)

    def associated_sessions(self) -> QuerySet[Session]:
        """export sessions for this experiment

        Returns:
            Associated sessions
        """

        return Session.objects.filter(block__phase__experiment=self).order_by(
            "-started_at"
        )

    def associated_feedback(self) -> QuerySet[Session]:
        """return feedback for the blocks in this experiment

        Returns:
            Associated block feedback
        """

        return Feedback.objects.filter(block__in=self.associated_blocks())


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
        compound_name = (
            self.experiment.name or self.experiment.slug or "Unnamed experiment"
        )
        return f"{compound_name} ({self.index})"

    class Meta:
        ordering = ["index"]


class BlockManager(models.Manager):

    def with_stats(self):
        return self.annotate(
            n_sessions=models.Count("session_set"),
            n_sessions_finished=models.Count(
                "session_set", filter=models.Q(finished_at__isnull=False)
            ),
            n_participants=models.Count("session__participant", unique=True),
        )


class Block(models.Model):
    """Root entity for configuring experiment blocks

    Attributes:
        phase (Phase): The phase this block belongs to
        index (int): Index of this block in the phase
        slug (str): Slug for this block
        name (str): Block name
        description (str): Description
        playlists (list(section.models.Playlist)): The playlist(s) used in this block
        image (image.models.Image): Image that will be showed on the dashboard
        active (bool): Is this block active?
        rounds (int): Number of rounds
        bonus_points (int): Bonus points
        rules (str): The rules used for this block
        theme_config (theme.models.ThemeConfig): Theme settings
    """

    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name="blocks", blank=True, null=True)
    slug = models.SlugField(
        db_index=True, max_length=64, unique=True, validators=[block_slug_validator]
    )
    index = models.IntegerField(default=0, help_text="Index of the block in the phase. Lower numbers come first.")

    name = models.CharField(max_length=64, blank=True, default="")
    description = models.TextField(blank=True, default="")

    playlists = models.ManyToManyField("section.Playlist", blank=True)

    image = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)

    rounds = models.PositiveIntegerField(default=10)
    bonus_points = models.PositiveIntegerField(default=0)
    rules = models.CharField(default="", max_length=64)

    theme_config = models.ForeignKey(ThemeConfig, on_delete=models.SET_NULL, blank=True, null=True)
    objects = BlockManager()

    def __str__(self):
        return self.name if self.name else self.slug

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

    def associated_sessions(self) -> QuerySet[Session]:
        """export sessions for this experiment

        Returns:
            Associated sessions
        """

        return self.associated_sessions().order_by("-started_at")

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
                "sessions": [
                    session._export_admin() for session in self.session_set.all()
                ],
                "participants": self.associated_participants().values(
                    "id",
                    "unique_hash",
                    "country_code",
                    "access_info",
                    "participant_id_url",
                    "profile",
                ),
            },
        }

    def associated_sessions(self):
        """return all sessions associated with this block"""
        return self.session_set.all()

    def associated_participants(self):
        from participant.models import Participant

        return Participant.objects.filter(session__in=self.associated_sessions())

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
        social_message = self.experiment.social_media_message
        experiment_name = self.experiment.name

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
        social_media_description = self.experiment.name or self.experiment.slug
        return f"Social Media for {social_media_description}"
