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
    name = models.CharField(max_length=64, default="")
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

    name = models.CharField(max_length=64, default="")
    description = models.TextField(blank=True, default="")

    playlists = models.ManyToManyField("section.Playlist", blank=True)

    image = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)

    rounds = models.PositiveIntegerField(default=10)
    bonus_points = models.PositiveIntegerField(default=0)
    rules = models.CharField(default="", max_length=64)

    theme_config = models.ForeignKey(ThemeConfig, on_delete=models.SET_NULL, blank=True, null=True)

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

    def export_table(
        self, session_keys: list[str], result_keys: list[str], export_options: dict[str, Any]
    ) -> tuple[list[dict[str, Any]], list[str]]:
        """Export filtered tabular data for admin

        Args:
            session_keys: session fieldnames to be included
            result_keys: result fieldnames to be included
            export_options: export options (see admin/forms.py)

        Returns:
            csv rows, field names
        """

        rows = []  # a list of dictionaries
        fieldnames = set()  # keep track of all potential fieldnames
        result_prefix = ""
        for session in self.session_set.all():
            profile = session.participant._export_admin()
            session_finished = session.finished_at.isoformat() if session.finished_at else None
            # Get data for all potential session fields
            full_row = {
                "block_id": self.id,
                "block_name": self.name,
                "participant_id": profile["id"],
                "participant_country": profile["country_code"],
                "participant_access_info": profile["access_info"],
                "session_start": session.started_at.isoformat(),
                "session_end": session_finished,
                "final_score": session.final_score,
            }
            row = {}
            # Add the selected sessions fields
            for session_key in session_keys:
                row[session_key] = full_row[session_key]
            # Add profile data if selected
            if "export_profile" in export_options:
                row.update(profile["profile"])
            # Add session data
            if session.json_data != "":
                if "session_data" in export_options:
                    # Convert json session data to csv columns if selected
                    if "convert_session_json" in export_options:
                        row.update(session.json_data)
                    else:
                        row["session_data"] = session.json_data
            fieldnames.update(row.keys())
            if session.result_set.count() == 0:
                # some sessions may have only profile questions
                rows.append(row)
            else:
                result_counter = 1
                # Create new row for each result
                if "wide_format" in export_options:
                    this_row = copy.deepcopy(row)
                for result in session.result_set.all():
                    # Add all results to one row
                    if "wide_format" not in export_options:
                        this_row = copy.deepcopy(row)
                    # Get data for al potential result fields
                    full_result_data = {
                        "section_name": result.section.song.name if result.section else None,
                        "result_created_at": result.created_at.isoformat(),
                        "result_score": result.score,
                        "result_comment": result.comment,
                        "expected_response": result.expected_response,
                        "given_response": result.given_response,
                        "question_key": result.question_key,
                    }

                    result_data = {}
                    # Add counter for single row / wide format
                    if "wide_format" in export_options:
                        result_prefix = str(result_counter).zfill(3) + "-"
                        # add the selected result fields
                        for result_key in result_keys:
                            result_data[(result_prefix + result_key)] = full_result_data[result_key]
                    else:
                        # add the selected result fields
                        for result_key in result_keys:
                            result_data[result_key] = full_result_data[result_key]
                    # Add result data
                    if result.json_data != "":
                        # convert result json data to csv columns if selected
                        if "convert_result_json" in export_options:
                            if "decision_time" in export_options:
                                result_data[result_prefix + "decision_time"] = result.json_data.get("decision_time", "")
                            if "result_config" in export_options:
                                result_data[result_prefix + "result_config"] = result.json_data.get("config", "")
                        else:
                            if "result_config" in export_options:
                                result_data[result_prefix + "result_data"] = result.json_data
                    this_row.update(result_data)
                    fieldnames.update(result_data.keys())
                    result_counter += 1
                    # Append row for long format
                    if "wide_format" not in export_options:
                        rows.append(this_row)
                # Append row for wide format
                if "wide_format" in export_options:
                    rows.append(this_row)
        return rows, list(fieldnames)

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
