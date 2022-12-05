from django.db import models

class Score(models.Model):
    rule = models.CharField(default="", max_length=64)
    value = models.FloatField(null=True, blank=True)