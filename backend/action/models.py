from django.db import models

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
    explainer = models.ForeignKey(Explainer, on_delete=models.CASCADE, related_name="steps")
    description = models.CharField(max_length=256, blank=True, default="")
    index = models.IntegerField(blank=True, default=1)

    class Meta:
        ordering = ["index"]

    def convert_to_action(self):
        return StepAction(description=self.description)
