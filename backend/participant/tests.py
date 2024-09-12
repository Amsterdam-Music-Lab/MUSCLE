import json

from django.test import Client, TestCase
from .models import Participant
from .utils import get_participant, PARTICIPANT_KEY
from experiment.models import Block
from session.models import Session
from result.models import Result
from question.questions import create_default_questions


class ParticipantTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_questions()
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.create(
            rules='RHYTHM_BATTERY_INTRO', slug='test')
        cls.session = Session.objects.create(
            block=cls.block,
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

        cls.result3 = Result.objects.create(
            participant=cls.participant,
            question_key='msi_01_music_activities',
            score=1
        )

        cls.result4 = Result.objects.create(
            participant=cls.participant,
            question_key='msi_08_intrigued_styles',
            score=2
        )

        cls.result5 = Result.objects.create(
            participant=cls.participant,
            question_key='msi_24_music_addiction',
            score=5
        )


    def setUp(self):
        self.client = Client(
            HTTP_USER_AGENT='Agent 007'
        )
        self.session = self.client.session
        self.session['country_code'] = 'BLA'
        self.session.save()

    def test_get_participant(self):
        participant = Participant.objects.create()
        participant.save()

        session = self.client.session
        session.update({PARTICIPANT_KEY: participant.id})
        session.save()

        request = self.client.request().wsgi_request
        request.session = session

        self.assertEqual(get_participant(request), participant)

    def test_get_participant_no_participant_in_session(self):
        request = self.client.request().wsgi_request
        request.session = self.client.session

        with self.assertRaisesMessage(
            Participant.DoesNotExist,
            'No participant in session'
        ):
            get_participant(request)

    def test_get_participant_no_participant(self):
        session = self.client.session
        session.update({PARTICIPANT_KEY: 1234567890})
        session.save()

        request = self.client.request().wsgi_request
        request.session = session

        with self.assertRaisesMessage(
            Participant.DoesNotExist,
            'Participant matching query does not exist.'
        ):
            get_participant(request)

    def set_participant(self):
        self.session['participant_id'] = self.participant.id
        self.session.save()

    def test_current_view(self):
        self.set_participant()
        response = json.loads(self.client.get('/participant/').content)
        assert response.get('id') == self.participant.id
        assert int(response.get('hash')) == self.participant.unique_hash
        assert response.get('csrf_token') is not None

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

    def test_score_sum(self):
        score_sum = self.participant.score_sum("MSI_F1_ACTIVE_ENGAGEMENT")
        assert score_sum == 8
        score_sum = self.participant.score_sum("MSI_F2_PERCEPTUAL_ABILITIES")
        assert score_sum is None
