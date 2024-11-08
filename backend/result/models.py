import json

from django.db import models
from django.utils import timezone

from django.core.exceptions import ValidationError


# Create your models here.
class Result(models.Model):
    """Score for each step in a session"""
    session = models.ForeignKey('session.Session', on_delete=models.CASCADE, blank=True, null=True)
    participant = models.ForeignKey('participant.Participant', on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(
        'section.Section', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    # Key of the question e.g.: AGE
    question_key = models.CharField(max_length=64, default='')
    expected_response = models.CharField(max_length=100, blank=True, default="")
    given_response = models.CharField(max_length=100, blank=True, default="")
    comment = models.CharField(max_length=100, default='')
    score = models.FloatField(default=0, blank=True)
    scoring_rule = models.CharField(default="", max_length=64)

    # Contains data in json_format
    json_data = models.JSONField(default=dict, blank=True)

    def clean(self):
        # Don't save if both session and participant field are null
        if self.session is None and self.participant is None:
            raise ValidationError('Session or participant needed for valid result')

    class Meta:
        ordering = ['created_at']

    def load_json_data(self):
        """Get json_data as object"""
        return self.json_data if self.json_data else {}

    def save_json_data(self, data):
        """Merge data with json_data, overwriting duplicate keys."""
        new_data = self.json_data
        new_data.update(data)
        self.json_data = new_data
        self.save()

    def _export_admin(self):
        """Export data for admin"""
        return {
            "created_at": self.created_at.isoformat(),
            "section_id": self.section.id if self.section else None,
            "section_name": (
                self.section.song.name if self.section and self.section.song else None
            ),
            "score": self.score,
            "expected_response": self.expected_response,
            "given_response": self.given_response,
            "comment": self.comment,
            "details": self.json_data,
        }
