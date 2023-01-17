import json
from importlib import import_module

from django.test import Client, TestCase
from django.test.client import RequestFactory

from .models import Participant
from .utils import get_or_create_participant
from experiment.models import Experiment
from session.models import Session
from result.models import Result

class ParticipantTest(TestCase):

    def setUp(self):
        self.client = Client(
            HTTP_USER_AGENT='Agent 007'
        )
        self.factory = RequestFactory()

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
    
    def test_current_view(self):
        # set participant_id to test session 
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()
        response = json.loads(self.client.get('/participant/').content)
        assert response.get('id') == 1
        assert int(response.get('hash')) == 42
        assert response.get('csrf_token') != None

    def test_profile(self):
        assert len(self.participant.profile()) == 2
    
    def test_profile_object(self):
        po = self.participant.profile_object()
        assert len(po.keys()) == 3
        assert po.get('test2') == None
        assert po.get('test1_score') == 2.5
    
    def test_profile_question(self):
        result = self.participant.profile_question('test1')
        assert result.given_response == '2 1/2'

    def test_profile_questions(self):
        results = self.participant.profile_questions()
        assert len(results) == 2
        assert results.first() == 'test1'
        Result.objects.all().delete()
        results = self.participant.profile_questions()
        assert len(results) == 0
    
    def test_empty_profile_question(self):
        empty_result = self.participant.random_empty_profile_question()
        assert empty_result.question_key == 'test2'

    def test_access_info(self):
        self.client.get('/participant/')
        participant = Participant.objects.last()
        assert participant.access_info == 'Agent 007'

    def test_country_code(self):
        session = self.client.session
        session['country_code'] = 'BLA'
        session.save()
        self.client.get('/participant/')
        participant = Participant.objects.last()
        assert participant.country_code == 'BLA'
    
    def test_get_or_create_participant(self):
        request = self.factory.get('/experiment/slug')
        participant = get_or_create_participant(request)
        assert participant != None
