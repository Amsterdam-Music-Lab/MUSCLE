import json

from django.test import TestCase
from django.utils import timezone

from experiment.models import Experiment
from participant.models import Participant
from section.models import Playlist, Section, Song
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
    
    def test_percentile_rank(self):
        # create one session with relatively low score
        Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            final_score=24,
            finished_at=timezone.now()
        )
        # create one unfinished session with relatively high score
        Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            final_score=180
        )
        finished_session = Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            final_score=42,
            finished_at=timezone.now()
        )
        rank = finished_session.percentile_rank(exclude_unfinished=True)
        assert rank == 75.0
        rank = finished_session.percentile_rank(exclude_unfinished=False)
        assert rank == 62.5

    def test_last_song(self):
        song = Song.objects.create(artist='Beavis', name='Butthead')
        section = Section.objects.create(playlist=self.playlist, song=song)
        Result.objects.create(
            session=self.session,
            section=section,
            question_key='preference',
            score=0
        )
        previous_section = self.session.previous_section()
        assert previous_section
        last_song = self.session.last_song()
        assert last_song == 'Beavis - Butthead'

    def test_json_data(self):
        self.session.save_json_data({'test': 'tested'})
        self.assertEqual(self.session.load_json_data(), {'test': 'tested'})
        self.session.save_json_data({'test_len': 'tested_len'})
        self.assertEqual(len(self.session.json_data), 2)

    def test_json_data_direct(self):        
        self.session.json_data.update({'test_direct': 'tested_direct'})
        self.session.save()
        self.assertEqual(self.session.json_data['test_direct'], 'tested_direct') 
        self.session.save_json_data({'test_direct_len': 'tested_direct_len'})
        self.session.save()
        self.assertEqual(len(self.session.json_data), 2)
        self.session.json_data.pop('test_direct_len')
        self.assertEqual(len(self.session.json_data), 1)
        self.assertEqual(self.session.json_data.get('test_direct_len', 'temp_value'), 'temp_value')
