import json

from django.test import Client, TestCase

from .models import Participant
from experiment.models import Experiment
from session.models import Session
from result.models import Result

class ParticipantTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.experiment = Experiment.objects.create(rules='LISTENING_CONDITIONS', slug='test')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
        )
        cls.result1 = Result.objects.create(
            participant=cls.participant,
            question_key='test1',
            given_response='2 1/2',
            score=2.5
        )
        cls.result2 = Result.objects.create(
            participant=cls.participant,
            question_key='test2'
        )

    def setUp(self):
        self.client = Client(
            HTTP_USER_AGENT='Agent 007'
        )
        self.session = self.client.session
        self.session['country_code'] = 'BLA'
        self.session.save()
    
    def set_participant(self):
        self.session['participant_id'] = self.participant.id
        self.session.save()
    
    def test_current_view(self):
        self.set_participant()
        response = json.loads(self.client.get('/participant/').content)
        assert response.get('id') == self.participant.id
        assert int(response.get('hash')) == self.participant.unique_hash
        assert response.get('csrf_token') != None

    def test_profile(self):
        assert len(self.participant.profile()) == 1
    
    def test_profile_object(self):
        po = self.participant.profile_object()
        assert len(po.keys()) == 2
        assert po.get('test1_score') == 2.5

    def test_access_info(self):
        # this will create a new participant
        self.client.get('/participant/')
        participant = Participant.objects.last()
        assert participant.access_info == 'Agent 007'

    def test_country_code(self):
        self.client.get('/participant/')
        participant = Participant.objects.last()
        assert participant.country_code == 'BLA'
    

