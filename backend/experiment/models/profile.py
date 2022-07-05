from django.db import models
from django.utils import timezone
from . import Participant


class Profile(models.Model):
    """Question and answer for a participant profile"""

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    # Key of the question e.g.: AGE
    question = models.CharField(max_length=64)
    answer = models.CharField(max_length=512, default="")

    session_id = models.PositiveIntegerField(default=0)

    score = models.FloatField(null=True, blank=True)

    class Meta:
        # Add index on participant/session_id and answer, as these
        # will be queried often together
        indexes = [
            models.Index(fields=['participant', 'answer']),
            models.Index(fields=['session_id', 'answer']),
        ]

    def export_admin(self):
        """Export data for admin"""
        return {
            'created_at': self.created_at.isoformat(),
            'question': self.question,
            'answer': self.answer,
            'session_id': self.session_id
        }
