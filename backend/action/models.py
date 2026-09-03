from django.db import models
from django.utils.translation import gettext_lazy as _

from experiment.actions.explainer import (
    Explainer as ExplainerAction,
    Step as StepAction,
)
from experiment.actions.final import Final as FinalAction

STATISTIC_VISUALIZATION_CHOICES = [
    (None, "----"),
    ("error_bar", "Error bar"),
    ("progress_bar", "Progress bar"),
]


class Explainer(models.Model):
    identifier = models.SlugField(max_length=64, unique=True)
    instruction = models.CharField(max_length=256, blank=True, default="")
    timer = models.IntegerField(blank=True, null=True)
    number_steps = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.identifier

    def convert_to_action(self):
        return ExplainerAction(
            instruction=self.instruction,
            steps=[step.convert_to_action() for step in list(self.steps.all())],
            step_numbers=self.number_steps,
            timer=self.timer,
        )


class Step(models.Model):
    explainer = models.ForeignKey(
        Explainer, on_delete=models.CASCADE, related_name="steps"
    )
    description = models.CharField(max_length=256, blank=True, default="")
    index = models.IntegerField(blank=True, default=1)

    class Meta:
        ordering = ["index"]

    def convert_to_action(self):
        return StepAction(description=self.description)


class Final(models.Model):
    identifier = models.SlugField(max_length=64, primary_key=True)
    title = models.CharField(
        max_length=128,
        blank=True,
        default="End",
        help_text=_("This text will be displayed in the title bar"),
    )
    score_text = models.CharField(
        max_length=16,
        blank=True,
        default="points",
        help_text=_("This short text will be displayed along with the score"),
    )
    visualization_type = models.CharField(
        choices=STATISTIC_VISUALIZATION_CHOICES,
        null=True,
        default=None,
        help_text=_("Select a visualization of the relative score."),
    )
    # Potential TODO: allow setting a button

    def set_score(self, score: float):
        self.score = score

    def set_relative_score(self, relative_score: float):
        self.relative_score = relative_score

    def convert_to_action(self) -> FinalAction:
        if not self.hasattr("relative_score"):
            self.relative_score = 100
        self.active_feedback = (
            self.feedbacks.filter(cutoff__lte=self.relative_score)
            .order_by(models.Max("cutoff"))
            .first()
        )
        self.active_rank = (
            self.ranks.filter(cutoff__lte=self.relative_score)
            .order_by(models.Max("cutoff"))
            .first()
        )
        return {
            "title": self.title,
            "score": self.final_score.convert_to_action(),
            "relative_score": self.relative_score,
            "rank": self.active_rank.convert_to_action(),
            "feedback": self.active_feedback.render_text(),
            "visualization": self.visualization_type,
            "progress": self.progress.covert_to_action(),
        }


class Rank(models.Model):
    final = models.ForeignKey(Final, on_delete=models.CASCADE, related_name="ranks")
    text = models.CharField(max_length=10, blank=True, default="")
    css_class = models.CharField(max_length=10, blank=True, default="")
    cutoff = models.FloatField(
        help_text=_("The minimal relative score for which this rank is displayed"),
        default=0.0,
        blank=True,
    )

    def convert_to_action(self):
        return {
            "text": self.text,
            "css_class": self.css_class,
        }


class FinalFeedback(models.Model):
    final = models.ForeignKey(
        Final,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="feedbacks",
    )
    text = models.TextField(default="You outperformed {relative}% of the players!")
    cutoff = models.FloatField(
        help_text=_(
            "The minimal relative score for which this feedback text is displayed"
        ),
        default=0.0,
        blank=True,
    )

    def render_text(self) -> str:
        if "{relative}" in self.text:
            self.text = self.text.replace("{relative}", self.final.relative_score)
        return self.text


class Progress(models.Model):
    final = models.OneToOneField(Final, on_delete=models.CASCADE)
    total_sessions = models.IntegerField(
        help_text=_("Set the total number of sessions the participant should play")
    )
    reward_every = models.IntegerField(
        blank=True,
        default=0,
        help_text=_("Optional: display a reward for every nth dot on the progress bar"),
    )
    # TO DO? Allow setting a custom image on the progress bar

    def convert_to_action(self):
        {
            "total_sessions": self.total_sessions,
            "reward_every": self.reward_every,
        }
