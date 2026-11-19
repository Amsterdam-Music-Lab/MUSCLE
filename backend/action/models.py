import operator as op
import re

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_markup.markup import formatter

from experiment.actions.explainer import Explainer as ExplainerView, Step as StepView
from session.models import Session
from theme.models import COLOR_CHOICES

class Explainer(models.Model):
    identifier = models.SlugField(max_length=64, unique=True)
    instruction = models.CharField(max_length=256, blank=True, default="")
    timer = models.IntegerField(blank=True, null=True)
    number_steps = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.identifier

    def convert_to_action(self):
        return ExplainerView(
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
        return StepView(description=self.description)


STATISTIC_VISUALIZATION_CHOICES = [
    (None, "----"),
    ("error_bar", "Error bar"),
    ("progress_bar", "Progress bar"),
]


class Button(models.Model):
    label = models.CharField(
        max_length=16, help_text=_("Set the text displayed on the button")
    )
    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        blank=True,
        null=True,
        help_text=_(
            "Set the color of the button, based on the theme. If not set, defaults to primary color."
        ),
    )
    link = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_(
            "If clicking on a button should link to a specific url, set it here. Otherwise, the button will link back to the experiment's entrypoint."
        ),
    )

    def to_dict(self):
        return {
            "label": self.label,
            "color": self.color or "colorPrimary",
            "link": self.link,
        }


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
    button = models.OneToOneField(
        Button, blank=True, null=True, on_delete=models.CASCADE
    )

    def convert_to_view(self, session: Session) -> dict:
        scores = session.json_data.get("scores")
        active_experiment = self.block.experiment
        timeline = (
            active_experiment.timeline
            if hasattr(active_experiment, "timeline")
            else None
        )
        active_rank = (
            self.block.ranking.get_active_rank(session.json_data)
            if hasattr(self.block, "ranking")
            else None
        )

        button = self.button or Button(label=_("Play again"))
        setattr(
            button,
            "link",
            button.link or session.get_current_experiment_link(),
        )
        return {
            "view": "FINAL",
            "title": self.title or _("End"),
            "visualization": self.visualization_type,
            "rank": active_rank.to_dict() if active_rank else None,
            "scores": scores,
            "finalFeedbackText": formatter(
                self.get_feedback_text(session.json_data), filter_name="markdown"
            ),
            "timeline": timeline.to_dict() if timeline else None,
            "button": (
                button.to_dict()
                if not active_experiment.is_finished(session.participant)
                else None
            ),
        }

    def get_feedback_text(self, json_data: dict):
        return " ".join(
            [
                feedback.feedback_text.get_feedback_text(json_data)
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


class Condition(models.Model):
    identifier = models.CharField(max_length=100, primary_key=True, blank=True)
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

    def save(self, **kwargs):
        if not self.pk:
            self.pk = f"{str(self.metric)}-{str(self.operator)}-{str(self.value)}"
        super().save(**kwargs)

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
        Condition, null=True, blank=True, on_delete=models.SET_NULL
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

    def get_feedback_text(self, json_data: dict) -> str:
        """get the feedback text, optionally based on conditions
        replace {statistic_name} with json_data[statistic_name]
        Return empty string if any statistic is missing in json_data
        """

        if self.condition:
            if self.condition.is_met(json_data):
                feedback_text = str(self.text)
            else:
                feedback_text = str(self.alternative_text)
        else:
            feedback_text = str(self.text)
        if not feedback_text:
            return ""
        replacements = list(set(re.findall(r"\{\w+\}", feedback_text)))
        for rep in replacements:
            statistic = json_data.get(rep.strip("{}"))
            if not statistic:
                return ""
            feedback_text = feedback_text.replace(rep, str(statistic))
        return feedback_text


class FinalFeedback(models.Model):
    feedback_text = models.OneToOneField(FeedbackText, on_delete=models.CASCADE)
    final = models.ForeignKey(Final, related_name="feedbacks", on_delete=models.CASCADE)
