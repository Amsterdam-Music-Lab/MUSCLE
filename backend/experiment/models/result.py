import json
from django.db import models
from django.utils import timezone
from . import Session, Section


class Result(models.Model):
    """Score for each step in a session"""

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    expected_response = models.CharField(max_length=100, blank=True)
    given_response = models.CharField(max_length=100, blank=True)
    score = models.FloatField(null=True, blank=True)

    # Contains data in json_format
    json_data = models.TextField(blank=True)

    def save_json_data(self, data):
        """Store data (object) to json_data string"""
        self.json_data = json.dumps(data, indent=4) if data else ""

    def load_json_data(self):
        """Get json_data as object"""
        return json.loads(self.json_data) if self.json_data else None

    def export_admin(self):
        """Export data for admin"""
        return {
            'created_at': self.created_at.isoformat(),
            'section': self.section.name,
            'score': self.score,
            'expected_response': self.expected_response,
            'given_response': self.given_response,
            'details': self.load_json_data(),
        }
