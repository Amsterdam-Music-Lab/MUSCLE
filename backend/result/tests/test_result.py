from django.test import Client, TestCase

from experiment.models import Experiment
from participant.models import Participant
from result.models import Result
from session.models import Session


class ResultTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.experiment = Experiment.objects.create(
            rules='MUSICAL_PREFERENCES', slug='test')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
        )

    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()
        self.result = Result.objects.create(
            question_key="speed_swallow",
            participant=self.participant
        )

    def test_json_data(self):
        
        self.result.save_json_data({'test': 'tested'})
        self.assertEqual(self.result.load_json_data(), {'test': 'tested'})
        self.result.save_json_data({'test_len': 'tested_len'})
        self.assertEqual(len(self.result.json_data), 2)

    def test_json_data_direct(self):        
        self.result.json_data.update({'test_direct': 'tested_direct'})
        self.result.save()
        self.assertEqual(self.result.json_data['test_direct'], 'tested_direct') 
        self.result.save_json_data({'test_direct_len': 'tested_direct_len'})
        self.result.save()
        self.assertEqual(len(self.result.json_data), 2)
        self.result.json_data.pop('test_direct_len')
        self.assertEqual(len(self.result.json_data), 1)
        self.assertEqual(self.result.json_data.get('test_direct_len', 'temp_value'), 'temp_value')
