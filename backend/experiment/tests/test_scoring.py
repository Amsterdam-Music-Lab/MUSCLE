import json

from django.test import TestCase
from experiment.models.participant import Participant

from experiment.models import Experiment, Participant, Playlist, Result, Section, Session

class ScoringTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.experiment = Experiment.objects.create(rules='LISTENING_CONDITIONS', slug='test')
        playlist = Playlist.objects.create(name='test')
        cls.section = Section.objects.create(
            playlist=playlist,
            artist="Cheese Shop",
            name="Gouda",
            filename="not/to_be_found.mp3",
            tag=0
        )
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
            playlist=playlist
        )
    
    def likert_request(self, rule, value):
        view = { "form": [
            {"key": "test",
            "result_id": None,
            "view": "TEXT_RANGE",
            "scale_steps": 7,
            "scoring_rule": rule,
            "value": value
            }
        ]}
        return self.make_request(view)
    
    def choice_request(self):
        view = {
            "form": [
                {
                    "key": "test",
                    "result_id": None,
                    "view": "RADIOS",
                    "choices": {
                        "first": "Spam",
                        "second": "Eggs and Spam",
                        "third": "Eggs, Fried Beans and Spam",
                        "fourth": "Spam, Fried Beans and Spam",
                        "fifth": "Spam, Spam, Spam, Spam, Eggs and Spam"
                    },
                    "value": "second",
                    "scoring_rule": "CATEGORIES_TO_LIKERT"
                }
            ],
        }
        return self.make_request(view)
    
    def correctness_request(self, value):   
        result = Result.objects.create(
            session = self.session,
            section = self.section,
            expected_response = 'spam'
        )
        view = { "form": [
            {"key": "test",
            "result_id": result.pk,
            "view": "BUTTON_ARRAY",
            "scoring_rule": 'CORRECTNESS',
            "value": value
            }
        ]}
        return self.make_request(view)

    def song_sync_request(self, result_type, continuation_correctness):
        result = Result.objects.create(
            session = self.session,
            section = self.section,
        )
        view = {
            "result_id": result.pk,
            "view": "SONG_SYNC",
            "result": {
                "type": result_type,
                "continuation_correctness": continuation_correctness,
                "recognition_time": 10
            },
            "config": {
                "recognition_time": 15,
                "continuation_correctness": True,
                "scoring_rule": "SONG_SYNC"
            }
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
        response = self.client.post('/experiment/session/result/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.count() == 1
        assert self.session.result_set.last().score == 2
    
    def test_likert_reversed(self):
        client_request = self.likert_request('REVERSE_LIKERT', 2)
        response = self.client.post('/experiment/session/result/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.count() == 1
        assert self.session.result_set.last().score == 6
    
    def test_likert_profile(self):
        client_request = self.likert_request('LIKERT', 6)
        response = self.client.post('/experiment/profile/create/', client_request)
        assert response.status_code == 200
        assert self.participant.profile_set.count() == 1
        assert self.participant.profile_set.last().score == 6
    
    def test_categories_to_likert(self):
        client_request = self.choice_request()
        response = self.client.post('/experiment/session/result/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 2
    
    def test_correctness(self):
        client_request = self.correctness_request('spam')
        response = self.client.post('/experiment/session/result/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 1
        client_request = self.correctness_request('eggs')
        response = self.client.post('/experiment/session/result/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.count() == 2
        assert self.session.result_set.last().score == 0
    
    def test_song_sync(self):
        client_request = self.song_sync_request('time_passed', False)
        response = self.client.post('/experiment/session/result/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 0
        client_request = self.song_sync_request('not_recognized', False)
        response = self.client.post('/experiment/session/result/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 0
        client_request = self.song_sync_request('recognized', False)
        response = self.client.post('/experiment/session/result/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == -5
        client_request = self.song_sync_request('recognized', True)
        response = self.client.post('/experiment/session/result/', client_request)
        assert response.status_code == 200
        assert self.session.result_set.last().score == 5
