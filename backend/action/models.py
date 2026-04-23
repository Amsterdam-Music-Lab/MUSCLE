from django.db import models

class Explainer(models.Model):
    instruction = models.CharField(max_length=256, blank=True, default="")
    timer = models.IntegerField(blank=True, default=0)
    number_steps = models.BooleanField(blank=True, default=False)

class Step(models.Model):
    explainer = models.ForeignKey(Explainer, on_delete=models.CASCADE, related_name="steps")
    description = models.CharField(max_length=256, blank=True, default="")
    index = models.IntegerField(blank=True, default=1)
