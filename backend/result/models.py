from django.db import models
from django.utils import timezone

from django.core.exceptions import ValidationError


class Result(models.Model):
    """A model to register participant responses to the database.

    Note:
        a Result can be either tied to a Session, which is the common way to log responses to tasks during an experiment,
        or to a Participant, which can be a consent form or a demographic question.

    Attributes:
        session (Optional[Session]): session for which this result will be registered
        participant (Optional[Participant]): participant for which this result will be registered
        section (Optional[Section]): a section tied to the result, usually applicable for Trials with Playback
        created_at (datetime): a timestamp, set automatically at creation time
        question_key (str): a description by which to identify the result during analysis
        expected_response (str): if there is a correct response for a given Trial, it can be logged here
        given_response (str): set as a result of the participant's response
        comment (str): optional comment to help analysis
        score (float): numerical value to reflect the participant's success
        scoring_rule (str): a key by which scores can be induced from expected and given response from [scoring_rules](result_score.md)
        json_data (dict): a field to log additional information to help analysis

    """
    session = models.ForeignKey(
        'session.Session', on_delete=models.CASCADE, blank=True, null=True
    )
    participant = models.ForeignKey(
        'participant.Participant', on_delete=models.CASCADE, blank=True, null=True
    )
    section = models.ForeignKey(
        'section.Section', on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(default=timezone.now)
    # Key of the question e.g.: AGE
    question_key = models.CharField(max_length=64, default='')
    expected_response = models.CharField(max_length=100, blank=True, null=True)
    given_response = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=100, default='')
    score = models.FloatField(null=True, blank=True)
    scoring_rule = models.CharField(default="", max_length=64)

    # Contains data in json_format
    json_data = models.JSONField(default=dict, blank=True, null=True)

    def clean(self):
        # Don't save if both session and participant field are null
        if self.session is None and self.participant is None:
            raise ValidationError('Session or participant needed for valid result')

    class Meta:
        ordering = ['created_at']

    def save_json_data(self, data: dict):
        """Merge data with json_data, overwriting duplicate keys.

        Args:
            data: dictionary of data to merge into the `json_data` field
        """
        self.json_data.update(data)
        self.save()

    def _export_admin(self) -> dict:
        """Export data for admin"""
        return {
            "created_at": self.created_at.isoformat(),
            "section_id": self.section.id if self.section else None,
            "section_name": (self.section.song_name() if self.section else None),
            "score": self.score,
            "expected_response": self.expected_response,
            "given_response": self.given_response,
            "comment": self.comment,
            "details": self.json_data,
        }
