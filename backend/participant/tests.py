import json

from django.test import TestCase

from models import Participant

class ParticipantTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
    
    def test_current_view(self):
        request = {
            'participant_id': 1
        }
        response = json.loads(self.client.get('/participant/', request))
        assert response.get('id') == 1
        assert response.get('hash') == 42
        assert response.get('csrf_token') != None