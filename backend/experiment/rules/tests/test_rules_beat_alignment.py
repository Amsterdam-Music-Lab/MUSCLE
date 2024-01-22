
from django.test import TestCase
from experiment.models import Experiment
from result.models import Result
from section.models import Playlist
from session.models import Session
import json


class BeatAlignmentRuleTest(TestCase):

    @classmethod
    def setUpTestData(cls):        
        # ex* are practice rounds. No actual mp3 files are present or tested
        csv = ("Artist 1,Name 1,0.0,10.0,bat/artist1.mp3,0,0,0\n"
               "Artist 2,Name 2,0.0,10.0,bat/artist2.mp3,0,0,0\n"
               "Artist 3,Name 3,0.0,10.0,bat/artist3.mp3,0,0,0\n"
               "Artist 4,Name 4,0.0,10.0,bat/artist4.mp3,0,0,0\n"
               "Artist 5,Name 5,0.0,10.0,bat/artist5.mp3,0,0,0\n"
               "Artist 6,Name 6,0.0,10.0,bat/artist6.mp3,0,0,0\n"
               "Artist 7,Name 7,0.0,10.0,bat/artist7.mp3,0,0,0\n"
               "Artist 8,Name 8,0.0,10.0,bat/artist8.mp3,0,0,0\n"
               "Artist 9,Name 9,0.0,10.0,bat/artist9.mp3,0,0,0\n"
               "Artist 10,Name 10,0.0,10.0,bat/artist10.mp3,0,0,0\n"
               "Artist 11,Name 10,0.0,10.0,bat/artist11.mp3,0,0,0\n"
               "Artist 12,Name 10,0.0,10.0,bat/artist12.mp3,0,0,0\n"
               "Artist 1,ex1 Name 1,0.0,10.0,bat/exartist1.mp3,0,0,0\n"
               "Artist 2,ex2 Name 2,0.0,10.0,bat/exartist2.mp3,0,0,0\n"
               "Artist 3,ex3_Name 3,0.0,10.0,bat/exartist3.mp3,0,0,0\n")

        playlist = Playlist.objects.create(name='TestBAT')
        playlist.csv = csv
        playlist.update_sections()
        cls.experiment = Experiment.objects.create(rules='BEAT_ALIGNMENT', slug='ba', rounds=13) #rules is BeatAlignment.ID in beat_alignment.py
        cls.experiment.playlists.add(playlist)

    def load_json(self, response):
        '''Asserts response status 200 OK, asserts content type json, loads and returns response.content json in a dictionary'''
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        return json.loads(response.content)

    def test_experiment(self):
        response = self.client.get('/experiment/ba/')
        response_json = self.load_json(response)
        self.assertTrue( {'id','slug','name','class_name','rounds','playlists','next_round','loading_text'} <= response_json.keys() )
        # 3 practice rounds (number hardcoded in BeatAlignment.first_round)
        views_exp = ['EXPLAINER', 'CONSENT']
        self.assertEquals(len(response_json['next_round']), len(views_exp))
        for i in range(len(views_exp)):
            self.assertEquals(response_json['next_round'][i]['view'], views_exp[i])
        header = {'HTTP_USER_AGENT':"Test device with test browser"}
        response = self.client.get('/participant/', **header)
        response_json = self.load_json(response)
        self.assertTrue( {'id','hash','csrf_token','country'} <= response_json.keys() )
        csrf_token = response_json['csrf_token']

        response = self.client.get('/result/consent_ba/')
        self.assertEqual(response.status_code, 204) # returns 204 if no consent has been given so far

        data = {"json_data": "{\"key\":\"consent_ba\",\"value\":true}", "csrfmiddlewaretoken": csrf_token}
        response = self.client.post('/result/consent/', data)
        response_json = self.load_json(response)
        self.assertTrue(response_json['status'],'ok')

        # Can throw an error if some of the tags in playlist not zero, cannot find a section to play
        data =  {"experiment_id": self.experiment.id, "playlist_id":"","json_data":"", "csrfmiddlewaretoken":csrf_token}
        response = self.client.post('/session/create/', data)
        response_json = self.load_json(response)
        session_id = response_json['session']['id']
        session = Session.objects.get(pk=session_id)
        
        # practice rounds
        response = self.client.post('/session/{}/next_round/'.format(session_id))
        response_json = self.load_json(response)
        rounds = response_json.get('next_round')
        assert len(rounds) == 4
        assert rounds[0].get('title') == 'Example 1'
        rounds_n = self.experiment.rounds # Default 10
        views_exp = ['TRIAL_VIEW']*(rounds_n)
        for i in range(len(views_exp)):
            response = self.client.post('/session/{}/next_round/'.format(session_id))
            response_json = self.load_json(response)
            result_id = response_json.get(
                'next_round')[0]['feedback_form']['form'][0]['result_id']
            result = Result.objects.get(pk=result_id)
            result.score = 1
            result.save()
            self.assertEqual(response_json['next_round'][0]['view'], views_exp[i]) 
        # final view
        response = self.client.post('/session/{}/next_round/'.format(session_id))
        response_json = self.load_json(response)
        assert response_json.get('next_round')[0]['view'] == 'FINAL'

        # Number of Results
        results = Session.objects.get(id=session_id).result_set.all()
        self.assertEqual(len(results), rounds_n)
