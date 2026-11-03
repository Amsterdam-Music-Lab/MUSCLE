from os.path import join
import re
from typing import Optional

from django.db import models
from django.utils.translation import gettext_lazy as _, get_language
from django.contrib.postgres.fields import ArrayField

from experiment.standards.iso_languages import ISO_LANGUAGES
from image.models import Image
from session.models import Session

from .validators import (
    markdown_html_validator,
    identifier_validator,
)

language_choices = [(key, ISO_LANGUAGES[key]) for key in ISO_LANGUAGES.keys()]


def consent_upload_path(instance, filename) -> str:
    """Generate path to save consent file based on experiment.identifier and language
    Returns:
        upload_to (str): Path for uploading the consent file
    """
    folder_name = instance.identifier
    language = get_language()
    return join("consent", folder_name, f"consent_{language}", filename)


class Experiment(models.Model):
    """A model to allow nesting multiple phases with blocks into a 'parent' experiment

    Attributes:
        identifier (str): Identifier of the experiment
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

    identifier = models.SlugField(
        db_index=True,
        max_length=64,
        unique=True,
        null=True,
        validators=[identifier_validator],
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
    replayable = models.BooleanField(
        blank=True,
        default=False,
        help_text=(
            "If True, the experiment will restart from the first block after the last block has been finished."
        ),
    )
    theme_config = models.ForeignKey(
        "theme.ThemeConfig", blank=True, null=True, on_delete=models.SET_NULL
    )
    ranking = models.ForeignKey(
        "experiment.Ranking",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="experiments",
    )
    active = models.BooleanField(default=True)
    social_media_config: Optional["SocialMediaConfig"]
    phases: models.QuerySet["Phase"]

    def __str__(self):
        return self.name or self.identifier

    class Meta:
        verbose_name_plural = "Experiments"

    def associated_blocks(self) -> list["Block"]:
        """Return a list of all associated blocks for this experiment

        Returns:
            Associated blocks
        """

        return Block.objects.filter(phase__experiment=self)

    def get_active_rank(self, scores: dict):
        if not self.ranking:
            return None
        else:
            return self.ranking.get_active_rank(scores.get('accumulative_score'))

    def get_played_sessions(self, participant) -> int:
        return Session.objects.filter(
            block__in=self.associated_blocks(),
            participant=participant,
            finished_at__isnull=False,
        ).count()


class Timeline(models.Model):
    experiment = models.OneToOneField(Experiment, on_delete=models.CASCADE)
    total_sessions = models.PositiveIntegerField(
        help_text=_(
            "Optional: set the total number of sessions the participant should play to complete this experiment. If greater than 1, the Final view displays a timeline after very session."
        ),
        default=1,
        blank=True,
    )
    # TO DO? Allow setting a custom image on the timeline bar for non-reward sessions

    def to_dict(self):
        return {
            "steps": [
                self.serialize_step(step_number)
                for step_number in range(1, self.total_sessions + 1)
            ]
        }

    def serialize_step(self, step_number: int) -> str:
        eligible_rewards = self.rewards.filter(session_number=step_number)
        if eligible_rewards:
            return eligible_rewards.first().image
        else:
            return ""


REWARD_IMAGE_CHOICES = [
    ("cup", _("Cup")),
    ("star", _("Star")),
]


class Reward(models.Model):
    timeline = models.ForeignKey(
        Timeline, on_delete=models.CASCADE, related_name="rewards"
    )
    session_number = models.PositiveIntegerField(
        help_text=_("Show this reward after this many sessions"), default=1
    )
    image = models.CharField(max_length=8, choices=REWARD_IMAGE_CHOICES, default="cup")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["timeline", "session_number"],
                name="unique_reward_step_per_timeline",
            )
        ]


class Phase(models.Model):
    """Root entity for configuring experiment phases

    Attributes:
        experiment (Experiment): Instance of an Experiment
        index (int): Index of the phase
        dashboard (bool): Should the dashbopard be displayed for this phase?
        randomize (bool): Should the blocks of this phase be randomized?
    """

    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="phases"
    )
    index = models.IntegerField(
        default=0,
        help_text="Index of the phase in the experiment. Lower numbers come first.",
    )
    dashboard = models.BooleanField(default=False)
    randomize = models.BooleanField(
        default=False, help_text="Randomize the order of the blocks in this phase."
    )

    def __str__(self):
        compound_name = self.experiment.name or self.experiment.identifier
        return f"{compound_name} ({self.index})"

    class Meta:
        ordering = ["index"]


class Block(models.Model):
    """Root entity for configuring experiment blocks

    Attributes:
        phase (Phase): The phase this block belongs to
        index (int): Index of this block in the phase
        identifier (str): Identifier for this block
        name (str): Block name
        description (str): Description
        playlists (list(section.models.Playlist)): The playlist(s) used in this block
        image (image.models.Image): Image that will be showed on the dashboard
        active (bool): Is this block active?
        rounds (int): Number of rounds
        bonus_points (int): Bonus points
        rules (str): The rules used for this block
        theme_config (theme.ThemeConfig): Theme settings
        rules_config (dict): a dictionary containing extra settings for the rules coupled to the block
    """

    experiment = models.ForeignKey(
        Experiment,
        on_delete=models.CASCADE,
        related_name="blocks",
    )
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name="blocks")
    identifier = models.SlugField(
        db_index=True, max_length=64, validators=[identifier_validator]
    )
    index = models.IntegerField(
        default=0,
        help_text="Index of the block in the phase. Lower numbers come first.",
    )

    name = models.CharField(max_length=64, blank=True, default="")
    description = models.TextField(blank=True, default="")

    playlists = models.ManyToManyField("section.Playlist", blank=True)

    image = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)

    rounds = models.PositiveIntegerField(default=10)
    bonus_points = models.PositiveIntegerField(default=0)
    rules = models.CharField(default="", max_length=64)

    theme_config = models.ForeignKey(
        "theme.ThemeConfig", on_delete=models.SET_NULL, blank=True, null=True
    )

    ranking = models.ForeignKey(
        "experiment.Ranking",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="blocks",
    )

    rules_config = models.JSONField(
        default=dict,
        help_text=_("Extra settings to control the behaviour of the block's rules"),
        blank=True,
    )

    class Meta:
        ordering = ["index"]
        constraints = [
            models.UniqueConstraint(
                fields=["experiment", "identifier"],
                name="unique_block_identifier_per_experiment",
            )
        ]

    def save(self, *args, **kwargs):
        self.experiment = self.phase.experiment
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else self.identifier

    def session_count(self) -> int:
        """Number of sessions

        Returns:
            Number of sessions
        """

        return self.sessions.count()

    session_count.short_description = "Sessions"

    def playlist_count(self) -> int:
        """Number of playlists

        Returns:
            Number of playlists
        """

        return self.playlists.count()

    playlist_count.short_description = "Playlists"

    def get_rules(self) -> "experiment.rules.base.Base":
        """Get instance of rules class to be used for this session

        Returns:
            Rules
        """

        from experiment.rules import BLOCK_RULES

        if self.rules not in BLOCK_RULES:
            raise ValueError(
                f"Rules do not exist (anymore): {self.rules} for block {self.name} ({self.identifier})"
            )

        cl = BLOCK_RULES[self.rules]
        return cl()


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

    experiment = models.OneToOneField(
        Experiment, on_delete=models.CASCADE, related_name="social_media_config"
    )

    tags = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text=_("List of tags for social media sharing"),
    )

    url = models.URLField(
        blank=True,
        help_text=_(
            "URL to be shared on social media. If empty, the experiment URL will be used."
        ),
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

        Returns:
            Social media shared text

        Raises:
            ValueError: If required parameters are missing when needed
        """
        social_message = self.experiment.social_media_message
        experiment_name = self.experiment.name

        if social_message:
            has_placeholders = (
                "{points}" in social_message and "{experiment_name}" in social_message
            )

            if not has_placeholders:
                return social_message

            if has_placeholders and (score is None or experiment_name is None):
                raise ValueError(
                    "score and experiment_name are required for placeholder substitution"
                )

            return social_message.format(points=score, experiment_name=experiment_name)

        if score is None or experiment_name is None:
            raise ValueError(
                "score and name are required when no social media message is provided"
            )

        return _("I scored %(score)d points in %(experiment_name)s") % {
            "score": score,
            "experiment_name": experiment_name,
        }

    def __str__(self):
        social_media_description = self.experiment.name or self.experiment.identifier
        return f"Social Media for {social_media_description}"


class Ranking(models.Model):
    identifier = models.SlugField(primary_key=True, max_length=128)

    def get_active_rank(
        self, score: Optional[float], has_feedback: bool = False
    ) -> Optional["experiment.Rank"]:
        if not score:
            score = -1
        try:
            if has_feedback:
                return (
                    self.ranks.exclude(feedback__exact="")
                    .filter(cutoff__lte=score)
                    .order_by("-cutoff")
                    .first()
                )
            return self.ranks.filter(cutoff__lte=score).order_by("-cutoff").first()
        except:
            None


RANK_CHOICES = [
    (None, "----"),
    ("plastic", _("Plastic")),
    ("bronze", _("Bronze")),
    ("silver", _("Silver")),
    ("gold", _("Gold")),
    ("platinum", _("Platinum")),
    ("diamond", _("Diamond")),
]


class Rank(models.Model):
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE, related_name="ranks")
    label = models.CharField(
        max_length=8, choices=RANK_CHOICES, null=True, default=None
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text=_("(Optional) Enter a description of the rank here"),
    )
    feedback = models.TextField(
        blank=True,
        default="",
        help_text=_("(Optional) enter feedback to your participant here"),
    )
    cutoff = models.FloatField(
        help_text=_("The minimal relative score for which this rank is displayed"),
        default=0.0,
        blank=True,
    )

    def get_trophy_data(self):
        return {
            "label": self.get_label_display(),  # Django inbuilt: returns translatable text
            "description": self.description,
            "className": self.label,
        }

    def get_feedback_text(self, session: Session) -> str:
        score_data = session.json_data.get("scores")
        feedback_text = str(self.feedback)
        replacements = re.findall(r"\{\w+\}", feedback_text)
        for rep in replacements:
            feedback_text = feedback_text.replace(
                rep, str(score_data.get(rep.strip("{}"), ""))
            )
        return feedback_text
