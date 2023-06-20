import json

from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from section.models import Playlist
from result.models import Result
from session.models import Session

class SessionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.experiment = Experiment.objects.create(rules='LISTENING_CONDITIONS', slug='test')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
        )
        cls.playlist = Playlist.objects.create(
            name='Test playlist'
        )
    
    def test_create(self):
        data = {
            'experiment_id': self.experiment.pk,
            'playlist_id': self.playlist.pk,
            'participant_id': self.participant.pk
        } 
        response = self.client.post('/session/create', data)
        assert response.status_code != 500

    def test_finalize(self):
        response = self.client.get('/participant/')
        response_data = json.loads(response.content)
        csrf_token = response_data.get('csrf_token')
        participant = Participant.objects.get(pk=response_data.get('id'))
        session = Session.objects.create(
            experiment=self.experiment,
            participant=participant)
        data = {
            'csrfmiddlewaretoken:': csrf_token
        }
        response = self.client.post('/session/{}/finalize/'.format(session.pk), data)
        assert response.status_code == 200
        assert Session.objects.filter(finished_at__isnull=False).count() == 1

    def test_total_questions(self):   
        assert self.session.total_questions() == 0
        Result.objects.create(
            session=self.session
        )
        assert self.session.total_questions() == 1
    
    def test_skipped_answered_questions(self):
        Result.objects.create(
            session=self.session,
            given_response=''
        )
        assert self.session.answered_questions() == 0
        Result.objects.create(
            session=self.session,
            given_response='Something really elaborate'
        )
        assert self.session.skipped_questions() == 1
        assert self.session.answered_questions() == 1
        Result.objects.create(
            session=self.session,
            given_response=''
        )
        assert self.session.skipped_questions() == 2
