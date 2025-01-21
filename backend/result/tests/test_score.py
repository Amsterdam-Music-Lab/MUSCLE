import json

from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from result.score import boolean_score, reaction_time_score
from section.models import Playlist, Section, Song
from session.models import Session


class ScoreTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        playlist = Playlist.objects.create(name='score_test')
        song = Song.objects.create(artist="Cheese Shop", name="Gouda")
        cls.section = Section.objects.create(
            playlist=playlist, song=song, filename="not/to_be_found.mp3", tag=0
        )
        cls.block = Block.objects.create(rules='RHYTHM_BATTERY_INTRO', slug='test')
        cls.session = Session.objects.create(
            block=cls.block, participant=cls.participant, playlist=playlist
        )

    def likert_request(self, rule, value, profile=False):
        result = Result.objects.create(
            question_key="test",
            session=self.session,
            section=self.section,
            scoring_rule=rule,
        )
        action = {
            "form": [
                {
                    "key": "likert_test",
                    "result_id": result.pk,
                    "view": "TEXT_RANGE",
                    "scale_steps": 7,
                    "value": value,
                }
            ]
        }
        return self.make_request(action)

    def choice_request(self):
        result = Result.objects.create(
            session=self.session,
            section=self.section,
            scoring_rule='CATEGORIES_TO_LIKERT',
            question_key='test',
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
                        "fifth": "Spam, Spam, Spam, Spam, Eggs and Spam",
                    },
                    "value": "second",
                }
            ],
        }
        return self.make_request(view)

    def correctness_request(self, value):
        result = Result.objects.create(
            session=self.session,
            section=self.section,
            expected_response='spam',
            scoring_rule='CORRECTNESS',
            question_key='',
        )
        view = {
            "form": [
                {
                    "key": "correctness_test",
                    "result_id": result.pk,
                    "view": "BUTTON_ARRAY",
                    "value": value,
                }
            ]
        }
        return self.make_request(view)

    def song_sync_recognize_request(self, result_type):
        result = Result.objects.create(
            question_key='recognize',
            session=self.session,
            section=self.section,
            scoring_rule='SONG_SYNC_RECOGNITION',
        )
        view = {
            "decision_time": 10,
            "config": {"response_time": 15},
            "form": [
                {"key": "recognize", "result_id": result.pk, "value": result_type}
            ],
        }
        return self.make_request(view)

    def song_sync_continue_request(self, result_type):
        result = Result.objects.create(
            question_key='correct_place',
            session=self.session,
            section=self.section,
            scoring_rule='SONG_SYNC_CONTINUATION',
            expected_response='yes',
        )
        view = {
            "decision_time": 10,
            "config": {"response_time": 15},
            "form": [
                {"key": "recognize", "result_id": result.pk, "value": result_type}
            ],
        }
        return self.make_request(view)

    def make_request(self, view):
        """set up the Django session data,
        return a request wrapping the view and id of the custom Session object"""
        session = self.client.session
        session['participant_id'] = self.participant.pk
        session.save()
        session_id = self.session.pk
        return {"session_id": session_id, "json_data": json.dumps(view)}

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

    def test_boolean_score(self):
        result = Result.objects.create(
            session=self.session, question_key='boolean_test', given_response='no'
        )
        score = boolean_score(result, {})
        self.assertEqual(score, 0)
        result = Result.objects.create(
            session=self.session, question_key='boolean_test', given_response='yes'
        )
        score = boolean_score(result, {})
        self.assertEqual(score, 1)

    def test_reaction_time_score(self):
        result = Result.objects.create(
            session=self.session,
            question_key='reaction_test',
            expected_response='yes',
            json_data={'decision_time': 5, 'config': {'response_time': 10}},
        )
        score = reaction_time_score(result, {'value': 'yes'})
        self.assertEqual(score, 5)
        score = reaction_time_score(result, {'value': 'no'})
        self.assertEqual(score, -5)
