from django.test import TestCase
from experiment.models import Block
from result.models import Result
from participant.models import Participant
from participant.utils import PARTICIPANT_KEY
from section.models import Playlist
from session.models import Session
import json


class BeatAlignmentRuleTest(TestCase):
    fixtures = ["choice_lists", "goldsmiths_msi", "demographics", "rhythm_tests"]

    @classmethod
    def setUpTestData(cls):
        playlist = Playlist.objects.get(name="BAT")
        playlist._update_sections()
        cls.block = Block.objects.get(identifier="bat")

    def load_json(self, response):
        '''Asserts response status 200 OK, asserts content type json, loads and returns response.content json in a dictionary'''
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        return json.loads(response.content)

    def test_block(self):
        participant = Participant.objects.create()
        participant.save()

        session = self.client.session
        session.update({PARTICIPANT_KEY: participant.id})
        session.save()

        block_response = self.client.get('/experiment/rhythm_battery/block/bat/')

        block_json = self.load_json(block_response)
        self.assertTrue(
            {
                "identifier",
                "class_name",
                "rounds",
                "playlists",
                "loading_text",
                "session_id",
            }
            <= block_json.keys()
        )
        session_id = block_json['session_id']
        response = self.client.post(
                f'/session/{session_id}/next_round/')
        rounds = self.load_json(response).get('next_round')

        # check that we get the intro explainer, 3 practice rounds and another explainer
        self.assertEqual(len(rounds), 5)
        self.assertEqual(
            rounds[0]['view'], 'EXPLAINER')
        # check practice rounds
        self.assertEqual(rounds[1].get('title'), 'Example 1')
        self.assertEqual(rounds[3].get('title'), 'Example 3')
        self.assertEqual(
            rounds[4]['view'], 'EXPLAINER')

        header = {'HTTP_USER_AGENT': "Test device with test browser"}
        participant_response = self.client.get('/participant/', **header)
        participant_json = self.load_json(participant_response)
        self.assertTrue(
            {'id', 'hash', 'csrf_token', 'country'} <= participant_json.keys()
        )
        csrf_token = participant_json['csrf_token']

        consent_response = self.client.get('/result/consent_ba/')
        # returns 204 if no consent has been given so far
        self.assertEqual(consent_response.status_code, 204)
        data = {
            "json_data": "{\"identifier\":\"consent_ba\",\"value\":true}",
            "csrfmiddlewaretoken": csrf_token,
        }
        consent_response = self.client.post('/result/consent/', data)
        consent_json = self.load_json(consent_response)
        self.assertTrue(consent_json['status'], 'ok')

        # test remaining rounds with request to `/session/{session_id}/next_round/`
        rounds_n = self.block.rounds  # Default 10
        views_exp = ['TRIAL_VIEW']*(rounds_n)
        for i in range(len(views_exp)):
            response = self.client.post(
                f'/session/{session_id}/next_round/')
            response_json = self.load_json(response)
            result_id = response_json.get('next_round')[0]['feedbackForm']['form'][0][
                'resultId'
            ]
            result = Result.objects.get(pk=result_id)
            result.score = 1
            result.save()
            self.assertEqual(
                response_json['next_round'][0]['view'], views_exp[i])
        # final view
        response = self.client.post(
            '/session/{}/next_round/'.format(session_id))
        response_json = self.load_json(response)
        assert response_json.get('next_round')[0]['view'] == 'FINAL'

        # Number of Results
        results = Session.objects.get(id=session_id).result_set.all()
        self.assertEqual(len(results), rounds_n)
