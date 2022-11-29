
from django.test import TestCase
from experiment.models import Experiment, Playlist, Session
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

        playlist = Playlist.objects.create(csv=csv)
        playlist.update_sections()
        experiment = Experiment.objects.create(rules='BEAT_ALIGNMENT', slug='ba') #rules is BeatAlignment.ID in beat_alignment.py
        experiment.playlists.add(playlist)


    def load_json(self, response):
        '''Asserts response status 200 OK, asserts content type json, loads and returns response.content json in a dictionary'''
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        return json.loads(response.content)

    def test_experiment(self):

        response = self.client.get('/experiment/id/ba/')
        response_json = self.load_json(response)
        self.assertTrue( {'id','slug','name','class_name','rounds','playlists','next_round','loading_text'} <= response_json.keys() )
        # 3 practice rounds (number hardcoded in BeatAlignment.first_round)
        views_exp = ['EXPLAINER','CONSENT'] + ['TRIAL_VIEW']*3 + ['EXPLAINER','START_SESSION']
        self.assertEquals(len(response_json['next_round']), len(views_exp))
        for i in range(len(views_exp)):
            self.assertEquals(response_json['next_round'][i]['view'], views_exp[i])

        response = self.client.get('/experiment/participant/')
        response_json = self.load_json(response)
        self.assertTrue( {'id','hash','csrf_token','country'} <= response_json.keys() )
        csrf_token = response_json['csrf_token']

        response = self.client.get('/experiment/profile/consent_ba/')
        self.assertEqual(response.status_code, 404) # By design, returns 404 if no consent has been given so far :/

        data = {"json_data": "{\"form\":[{\"key\":\"consent_ba\",\"value\":true}]}", "csrfmiddlewaretoken": csrf_token}
        response = self.client.post('/experiment/profile/create/', data)
        response_json = self.load_json(response)
        self.assertTrue(response_json['status'],'ok')

        # Can throw an error if some of the tags in playlist not zero, cannot find a section to play
        data =  {"experiment_id": "1", "playlist_id":"","json_data":"", "csrfmiddlewaretoken":csrf_token}
        response = self.client.post('/experiment/session/create/', data)
        response_json = self.load_json(response)
        self.assertTrue( {'session','next_round'} <= response_json.keys() )
        self.assertEqual( len(response_json['next_round']), 1 )
        self.assertEqual( response_json['next_round'][0]['view'],'TRIAL_VIEW')
        session_id = response_json['session']['id']
        result_id = response_json['next_round'][0]['feedback_form']['form'][0]['result_id']

        rounds_n = Experiment.objects.get(pk=1).rounds # Default 10
        views_exp = ['TRIAL_VIEW']*(rounds_n-1) + ['FINAL'] 
        for i in range(len(views_exp)):
            data = {
                "session_id": session_id,
                "csrfmiddlewaretoken": csrf_token,
                "json_data": json.dumps({
                    "decision_time":2.5,
                    "form":
                        [{  
                            "key": "aligned",
                            "view": "BUTTON_ARRAY",
                            "explainer": "",
                            "question":
                                ["Are the beeps ALIGNED TO THE BEAT or NOT ALIGNED TO THE BEAT?"],
                            "result_id": result_id,
                            "is_skippable": False,
                            "submits": True,
                            "scoring_rule": "CORRECTNESS",
                            "choices": {
                                "ON": "ALIGNED TO THE BEAT",
                                "OFF": "NOT ALIGNED TO THE BEAT"
                            },
                            "value": "ON"
                        }],
                    })
            }
            response = self.client.post('/experiment/session/result/', data)
            response_json = self.load_json(response)
            self.assertEqual(response_json['view'], views_exp[i])
            if i < len(views_exp)-1: # Last view 'FINAL' does not have result_id or feedback form
                result_id = response_json['feedback_form']['form'][0]['result_id']

        # Number of Results
        results = Session.objects.get(id=session_id).result_set.all()
        self.assertEqual(len(results), rounds_n)
