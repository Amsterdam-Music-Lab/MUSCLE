from django.db import models
from django.utils.translation import gettext_lazy as _

from experiment.actions.explainer import (
    Explainer as ExplainerAction,
    Step as StepAction,
)

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


STATISTIC_VISUALIZATION_CHOICES = [
    (None, "----"),
    ("error_bar", "Error bar"),
    ("progress_bar", "Progress bar"),
]


class Final(models.Model):
    identifier = models.SlugField(max_length=64, primary_key=True)
    title = models.CharField(
        max_length=128,
        blank=True,
        default="End",
        help_text=_("This text will be displayed in the title bar"),
    )
    score_label = models.CharField(
        max_length=16,
        blank=True,
        default="points",
        help_text=_("This short label will be displayed along with the score"),
    )
    visualization_type = models.CharField(
        choices=STATISTIC_VISUALIZATION_CHOICES,
        null=True,
        default=None,
        help_text=_("Select a visualization of the relative score."),
    )
    # Potential TODO: allow setting a button
