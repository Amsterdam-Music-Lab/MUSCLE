import json

from django.test import Client, TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from section.models import Playlist, Section, Song
from session.models import Session

from result.utils import handle_results


class ResultTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.create(
            rules='MUSICAL_PREFERENCES', slug='test')
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
        )

    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()

    def test_get(self):
        response = self.client.get('/result/speed_swallow/')
        assert response.status_code == 204

    def test_create(self):
        result = Result.objects.create(
            question_key="speed_swallow",
            participant=self.participant
        )
        view = { "form": [
            {"key": "speed_swallow",
            "result_id": result.id,
            "view": "TEXT",
            "scale_steps": 7,
            "value": 'An African or a European swallow?'
            }
        ]}
        request = {
            "session_id": self.session.id,
            "json_data": json.dumps(view)
        }
        response = self.client.post('/result/score/', request)
        assert response.status_code == 200
        assert Result.objects.count() == 1
        response = self.client.get('/result/speed_swallow/')
        assert json.loads(response.content).get('answer') is not None
        response = self.client.post('/result/score/', request)
        assert Result.objects.count() == 1

    def test_handle_results_with_form(self):
        result1 = Result.objects.create(
            session=self.session
        )
        result2 = Result.objects.create(
            session=self.session
        )
        data = {
            'form': [
                {'key': 'silly_walk', 'value': 'very silly indeed', 'result_id': result1.pk},
                {'key': 'tea', 'value': 'Ms Two Lumps', 'result_id': result2.pk}],
            'config': {'something': 'registered as config'},
            'decision_time': 42
        }
        handle_results(data, self.session)
        assert self.session.result_count() == 2
        json_data = self.session.result_set.first().json_data
        assert json_data.get('config') is not None
        assert json_data.get('decision_time') == 42


class ScoringTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        playlist = Playlist.objects.create(name='score_test')
        song = Song.objects.create(
            artist="Cheese Shop",
            name="Gouda"
        )
        cls.section = Section.objects.create(
            playlist=playlist,
            song=song,
            filename="not/to_be_found.mp3",
            tag=0
        )
        cls.block = Block.objects.create(
            rules='RHYTHM_BATTERY_INTRO',
            slug='test')
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=playlist
        )

    def likert_request(self, rule, value, profile=False):
        result = Result.objects.create(
            question_key="test",
            session=self.session,
            section=self.section,
            scoring_rule=rule
        )
        action = {
            "form": [{
                "key": "likert_test",
                "result_id": result.pk,
                "view": "TEXT_RANGE",
                "scale_steps": 7,
                "value": value
            }]
        }
        return self.make_request(action)

    def choice_request(self):
        result = Result.objects.create(
            session=self.session,
            section=self.section,
            scoring_rule='CATEGORIES_TO_LIKERT',
            question_key='test'
        )
        view = {
            "form": [
                {
                    "key": "likert_test",
                    "result_id": result.pk,
                    "view": "RADIOS",
                    "choices": {
                        "first": "Spam",
                        "second": "Eggs and Spam",
                        "third": "Eggs, Fried Beans and Spam",
                        "fourth": "Spam, Fried Beans and Spam",
                        "fifth": "Spam, Spam, Spam, Spam, Eggs and Spam"
                    },
                    "value": "second"
                }
            ],
        }
        return self.make_request(view)

    def correctness_request(self, value):
        result = Result.objects.create(
            session = self.session,
            section = self.section,
            expected_response = 'spam',
            scoring_rule='CORRECTNESS',
            question_key=''
        )
        view = { "form": [
            {"key": "correctness_test",
            "result_id": result.pk,
            "view": "BUTTON_ARRAY",
            "value": value
            }
        ]}
        return self.make_request(view)

    def song_sync_recognize_request(self, result_type):
        result = Result.objects.create(
            question_key='recognize',
            session=self.session,
            section=self.section,
            scoring_rule='SONG_SYNC_RECOGNITION'
        )
        view = {
            "decision_time": 10,
            "config": {
                "response_time": 15
            },
            "form": [
                {"key": "recognize", "result_id": result.pk, "value": result_type}
            ]
        }
        return self.make_request(view)

    def song_sync_continue_request(self, result_type):
        result = Result.objects.create(
            question_key='correct_place',
            session=self.session,
            section=self.section,
            scoring_rule='SONG_SYNC_CONTINUATION',
            expected_response='yes'
        )
        view = {
            "decision_time": 10,
            "config": {
                "response_time": 15
            },
            "form": [
                {"key": "recognize", "result_id": result.pk, "value": result_type}
            ]
        }
        return self.make_request(view)

    def make_request(self, view):
        """ set up the Django session data,
        return a request wrapping the view and id of the custom Session object """
        session = self.client.session
        session['participant_id'] = self.participant.pk
        session.save()
        session_id = self.session.pk
        return {
            "session_id": session_id,
            "json_data": json.dumps(view)
        }

    def test_likert_score(self):
        client_request = self.likert_request('LIKERT', 2)
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.count() == 1
        assert self.session.result_set.last().score == 2

    def test_likert_reversed(self):
        client_request = self.likert_request('REVERSE_LIKERT', 2)
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.count() == 1
        assert self.session.result_set.last().score == 6

    def test_likert_profile(self):
        client_request = self.likert_request('LIKERT', 6, True)
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.count() == 1
        assert self.session.result_set.last().score == 6

    def test_categories_to_likert(self):
        client_request = self.choice_request()
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 2

    def test_correctness(self):
        client_request = self.correctness_request('spam')
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 1
        client_request = self.correctness_request('eggs')
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.count() == 2
        assert self.session.result_set.last().score == 0

    def test_song_sync(self):
        client_request = self.song_sync_recognize_request("TIMEOUT")
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 0
        client_request = self.song_sync_recognize_request('no')
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 0
        client_request = self.song_sync_recognize_request('yes')
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 5
        client_request = self.song_sync_continue_request('no')
        response = self.client.post('/result/score/', client_request)
        assert response.status_code == 200
        assert self.session.last_result(["recognize"]).score == -5
