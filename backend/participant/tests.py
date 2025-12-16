import json
from django.utils import timezone

from django.test import Client, TestCase
from experiment.models import Block
from participant.models import Participant
from participant.utils import get_participant, PARTICIPANT_KEY
from question.models import QuestionList
from question.banks import get_question_bank
from result.models import Result
from session.models import Session


class ParticipantTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.create(rules='RHYTHM_BATTERY_INTRO', slug='test')
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

    def test_profile_results(self):
        self.assertEqual(self.participant.profile_results().count(), 1)

    def test_profile(self):
        po = self.participant.profile()
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
        self.block.create_question_list(
            {
                "name": "test_msi1",
                "question_keys": get_question_bank("MSI_F1_ACTIVE_ENGAGEMENT"),
            }
        )
        self.block.create_question_list(
            {
                "name": "test_msi2",
                "question_keys": get_question_bank("MSI_F2_PERCEPTUAL_ABILITIES"),
            }
        )
        score_sum = self.participant.score_sum(
            QuestionList.objects.get(block=self.block, name="test_msi1")
        )
        assert score_sum == 8
        score_sum = self.participant.score_sum(
            QuestionList.objects.get(block=self.block, name="test_msi2")
        )
        assert score_sum is None

    def test_session_count(self):
        new_participant = Participant.objects.create(unique_hash=4242)
        Session.objects.bulk_create(
            [
                Session(block=self.block, participant=new_participant),
                Session(block=self.block, participant=new_participant),
                Session(block=self.block, participant=new_participant),
            ]
        )
        self.assertEqual(new_participant.session_count(), 3)

    def test_result_count(self):
        this_session = Session.objects.create(
            block=self.block, participant=self.participant
        )
        that_session = Session.objects.create(
            block=self.block, participant=self.participant
        )
        Result.objects.bulk_create(
            [
                Result(session=this_session),
                Result(session=this_session),
                Result(session=this_session),
            ]
        )
        self.assertEqual(self.participant.result_count(), 3)
        Result.objects.bulk_create(
            [
                Result(session=that_session),
                Result(session=that_session),
                Result(session=that_session),
            ]
        )
        self.assertEqual(self.participant.result_count(), 6)

    def test_profile_results(self):
        Result.objects.bulk_create(
            [
                Result(participant=self.participant,
                       question_key='msi_01_music_activities',
                       given_response="response"),
                Result(participant=self.participant,
                       question_key='msi_24_music_addiction',
                       given_response="response"),
                Result(participant=self.participant,
                       question_key='msi_08_intrigued_styles',
                       given_response="response"),
            ]
        )
        this_profile = self.participant.profile_results()
        self.assertEqual(this_profile.count(), 4)

    def test_is_dutch(self):
        new_participant = Participant.objects.create(unique_hash="84",
                                                     country_code="nl",
                                                     access_info="Mozilla/5.0 (X11; Linux x86_64)",
                                                     participant_id_url = "this_participant",
                                                     )
        self.assertEqual(new_participant.is_dutch(), True)

    def test_scores_per_experiment(self):
        Session.objects.create(
            block=self.block,
            participant=self.participant,
            finished_at=timezone.now(),
            final_score=30.0,
        )
        these_scores = self.participant.scores_per_experiment()
        self.assertEqual(len(these_scores), 1)
        self.assertEqual(these_scores[0]['block_slug'], "test")
        self.assertEqual(these_scores[0]['rank'], {'text': 'silver', 'class': 'silver'})
        self.assertEqual(these_scores[0]['score'], 30.0)
        self.assertEqual(these_scores[0]['date'], "today")
