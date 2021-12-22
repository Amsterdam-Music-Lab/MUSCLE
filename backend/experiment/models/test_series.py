from django.db import models

class TestSeries(models.Model):
    name = models.CharField(max_length=64, default='')
    # first experiments in a test series, in fixed order
    first_experiments = models.JSONField(blank=True, null=True, default=dict)
    random_experiments = models.JSONField(blank=True, null=True, default=dict)
    # last experiments in a test series, in fixed order
    last_experiments = models.JSONField(blank=True, null=True, default=dict)