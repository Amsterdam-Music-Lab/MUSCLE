import json

from django.db import models
from django.utils import timezone

from session.models import Session
from section.models import Section

# Create your models here.
class Result(models.Model):
    """Score for each step in a session"""

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    # Key of the question e.g.: AGE
    question_key = models.CharField(max_length=64)
    is_profile = models.BooleanField(default=False)

    expected_response = models.CharField(max_length=100, blank=True, null=True)
    given_response = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=100, default='')
    score = models.FloatField(null=True, blank=True)
    scoring_rule = models.CharField(default="", max_length=64)

    # Contains data in json_format
    json_data = models.TextField(blank=True)

    class Meta:
        ordering = ['created_at']

    def save_json_data(self, data):
        """Store data (object) to json_data string"""
        self.json_data = json.dumps(data, indent=4) if data else ""

    def load_json_data(self):
        """Get json_data as object"""
        return json.loads(self.json_data) if self.json_data else None
    
    def merge_json_data(self, data):
        """Convert json data object to string and merge with json_data, overwriting duplicate keys.

        Only valid for JSON objects/Python dicts.
        """
        if data:
            self.json_data = json.dumps(
                {**self.load_json_data(), **data}, indent=4)


    def export_admin(self):
        """Export data for admin"""
        return {
            'created_at': self.created_at.isoformat(),
            'section': self.section.name if self.section else None,
            'score': self.score,
            'expected_response': self.expected_response,
            'given_response': self.given_response,
            'comment': self.comment,
            'details': self.load_json_data(),
        }
