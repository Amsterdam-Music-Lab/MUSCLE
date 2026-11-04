import operator as op
import re

from django.db import models
from django.utils.translation import gettext_lazy as _

from experiment.actions.explainer import (
    Explainer as ExplainerAction,
    Step as StepAction,
)
from session.models import Session

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

    def get_feedback_text(self, session: Session):
        return " ".join(
            [
                feedback.feedback_text.get_feedback_text(session)
                for feedback in self.feedbacks.all()
            ]
        )


OPERATOR_CHOICES = [
    ("eq", _("equals")),
    ("ne", _("different from")),
    ("gt", _("greater than")),
    ("ge", _("greater than or equal")),
    ("lt", _("lower than")),
    ("le", _("lower than or equal")),
]


class FeedbackCondition(models.Model):
    metric = models.CharField(
        help_text=_(
            "The metric to check: make sure this key is present in the json_data"
        )
    )
    operator = models.CharField(
        max_length=2,
        choices=OPERATOR_CHOICES,
        help_text=_("Choose the operator to check whether the condition is met"),
    )
    value = models.CharField(
        help_text=_("The value against which to compare. Can be string or integer.")
    )

    def __str__(self):
        return f"{self.metric} {self.get_operator_display()} {self.value}"

    def is_met(self, json_data: dict) -> bool:
        """check if the actual value of the metric saved on the session meets the condition"""
        actual_value = json_data.get(self.metric)
        if not actual_value:
            return False
        operator = getattr(op, self.operator)
        try:
            return operator(int(actual_value), int(self.value))
        except:
            return operator(actual_value, self.value)


class FeedbackText(models.Model):
    """A model to present feedback to the participant.
    This feedback can be different depending on a given value in the json_data of the session,
    and / or it may contain values from the json_data of the session.
    """

    index = models.PositiveSmallIntegerField(
        default=0,
        help_text=_(
            "Set the index to control the order of Feedbacks, in case you have multiple"
        ),
    )
    condition = models.ForeignKey(
        FeedbackCondition, null=True, blank=True, on_delete=models.SET_NULL
    )
    text = models.TextField(
        help_text=_(
            "This text will be shown when the condition is met, or if no condition is defined"
        )
    )
    alternative_text = models.TextField(
        blank=True,
        default="",
        help_text=_(
            "Optional: This text will be shown when the condition is not met. Use curly braces around values in json_data to render them."
        ),
    )

    class Meta:
        ordering = ["index"]

    def get_feedback_text(self, session: Session) -> str:
        json_data = session.json_data
        if self.condition:
            if self.condition.is_met(json_data):
                feedback_text = str(self.text)
            else:
                feedback_text = str(self.alternative_text)
        else:
            feedback_text = str(self.text)
        replacements = re.findall(r"\{\w+\}", feedback_text)
        for rep in replacements:
            feedback_text = feedback_text.replace(
                rep, str(json_data.get(rep.strip("{}"), ""))
            )
        return feedback_text


class FinalFeedback(models.Model):
    feedback_text = models.OneToOneField(FeedbackText, on_delete=models.CASCADE)
    final = models.ForeignKey(Final, related_name="feedbacks", on_delete=models.CASCADE)
