from django.db import models

SCORING_CHOICES = [
    'CORRECTNESS',
    'REACTION_TIME',
    'LIKERT',
    'LIKERT_REVERSED'
]

class Question(models.Model):
    key = models.CharField(max_length=128, unique=True)
    is_profile = models.BooleanField(default=False)
    scoring_rule = models.CharField(choices=SCORING_CHOICES, default='CORRECTNESS')