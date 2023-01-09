import json

from django.test import TestCase

from experiment.models import Experiment, Participant, Session
from ..rules.base import Base

class SessionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.experiment = Experiment.objects.create(rules='LISTENING_CONDITIONS', slug='test')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
        )
    
    def test_handle_results_with_form(self):
        data = {
            'form': [
                {'key': 'silly_walk', 'value': 'very silly indeed'},
                {'key': 'tea', 'value': 'Ms Two Lumps'}],
            'config': {'something': 'registered as config'},
            'decision_time': 42
        }
        Base.handle_results(self.session, data)
        assert self.session.result_count() == 2
        json_data = json.loads(self.session.result_set.first().json_data)
        assert json_data.get('config') != None
        assert json_data.get('decision_time') == 42


