from django.test import TestCase

from experiment.models import Block
from experiment.rules.rhythm_discrimination import next_trial_actions, plan_stimuli
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session


class RhythmDiscriminationTest(TestCase):
    fixtures = ["playlist", "experiment"]

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name="RhythmDiscrimination")
        cls.playlist._update_sections()
        cls.block = Block.objects.get(slug="rhdis")
        cls.session = Session.objects.create(block=cls.block, participant=cls.participant, playlist=cls.playlist)

    def test_next_trial_actions(self):
        plan_stimuli(self.session)
        self.session.final_score = 1
        self.session.save()
        trial = next_trial_actions(self.session, 6)
        assert trial

    def test_block_flow(self):
        participant_response = self.client.get("/participant/")
        participant = self.load_json_or_fail(participant_response)
        self.assertTrue("id" in participant)
        self.assertTrue(participant["id"])
        csrf_token = participant["csrf_token"]

        session = self.client.session
        session.update({"participant_id": participant["id"]})
        session.save()

        block_response = self.client.get("/experiment/block/rhdis/")

        block_json = self.load_json_or_fail(block_response)
        self.assertTrue(
            {
                "slug",
                "class_name",
                "rounds",
                "playlists",
                "loading_text",
                "session_id",
            }
            <= block_json.keys()
        )

        session_id = block_json["session_id"]

        # go to the next round (1st round | practice)
        next_round_response = self.client.post(f"/session/{session_id}/next_round/")
        next_round = self.load_json_or_fail(next_round_response).get("next_round")

        # first two actions should be 'EXPLAINER', then one 'TRIAL_VIEW'
        self.assertEqual(next_round[0]["view"], "EXPLAINER")
        self.assertEqual(next_round[1]["view"], "EXPLAINER")
        self.assertEqual(next_round[2]["view"], "TRIAL_VIEW")

        feedback_form_result_id = next_round[2]["feedback_form"]["form"][0]["result_id"]
        expected_response = next_round[2]["feedback_form"]["form"][0]["expected_response"]

        # post score
        score_response = self.client.post(
            "/result/score/",
            {
                "session_id": session_id,
                "json_data": '{"decision_time":2,"form":[{"key":"same","value":"%s","result_id":%s}]}'
                % (expected_response, feedback_form_result_id),
                "csrfmiddlewaretoken": csrf_token,
            },
        )
        self.load_json_or_fail(score_response)

        # go to the next round (2nd round | practice)
        next_round_response = self.client.post(f"/session/{session_id}/next_round/")
        next_round = self.load_json_or_fail(next_round_response).get("next_round")

        # check that 1st action is 'EXPLAINER' and 2nd is 'TRIAL_VIEW'
        self.assertEqual(next_round[0]["view"], "EXPLAINER")
        self.assertEqual(next_round[1]["view"], "TRIAL_VIEW")

        # post score
        feedback_form_result_id = next_round[1]["feedback_form"]["form"][0]["result_id"]
        expected_response = next_round[1]["feedback_form"]["form"][0]["expected_response"]
        score_response = self.client.post(
            "/result/score/",
            {
                "session_id": session_id,
                "json_data": '{"decision_time":2,"form":[{"key":"same","value":"%s","result_id":%s}]}'
                % (expected_response, feedback_form_result_id),
                "csrfmiddlewaretoken": csrf_token,
            },
        )

        self.load_json_or_fail(score_response)

        # go to the next round (3rd round | practice)
        next_round_response = self.client.post(f"/session/{session_id}/next_round/")
        next_round = self.load_json_or_fail(next_round_response).get("next_round")

        # check that 1st action is 'EXPLAINER' and 2nd is 'TRIAL_VIEW'
        self.assertEqual(next_round[0]["view"], "EXPLAINER")
        self.assertEqual(next_round[1]["view"], "TRIAL_VIEW")

        # post score
        feedback_form_result_id = next_round[1]["feedback_form"]["form"][0]["result_id"]
        expected_response = next_round[1]["feedback_form"]["form"][0]["expected_response"]
        score_response = self.client.post(
            "/result/score/",
            {
                "session_id": session_id,
                "json_data": '{"decision_time":2,"form":[{"key":"same","value":"%s","result_id":%s}]}'
                % (expected_response, feedback_form_result_id),
                "csrfmiddlewaretoken": csrf_token,
            },
        )

        self.load_json_or_fail(score_response)

        # go to the next round (4th round | practice)
        next_round_response = self.client.post(f"/session/{session_id}/next_round/")
        next_round = self.load_json_or_fail(next_round_response).get("next_round")

        # check that 1st action is 'EXPLAINER' and 2nd is 'TRIAL_VIEW'
        self.assertEqual(next_round[0]["view"], "EXPLAINER")
        self.assertEqual(next_round[1]["view"], "TRIAL_VIEW")

        # post score
        feedback_form_result_id = next_round[1]["feedback_form"]["form"][0]["result_id"]
        expected_response = next_round[1]["feedback_form"]["form"][0]["expected_response"]
        score_response = self.client.post(
            "/result/score/",
            {
                "session_id": session_id,
                "json_data": '{"decision_time":2,"form":[{"key":"same","value":"%s","result_id":%s}]}'
                % (expected_response, feedback_form_result_id),
                "csrfmiddlewaretoken": csrf_token,
            },
        )

        self.load_json_or_fail(score_response)

        # go to the next round (5th round | real)
        next_round_response = self.client.post(f"/session/{session_id}/next_round/")
        next_round = self.load_json_or_fail(next_round_response).get("next_round")

        # check that 1st & 2nd action is 'EXPLAINER' and 3nd is 'TRIAL_VIEW'
        self.assertEqual(next_round[0]["view"], "EXPLAINER")
        self.assertEqual(next_round[1]["view"], "EXPLAINER")
        self.assertEqual(next_round[2]["view"], "TRIAL_VIEW")

        # check that the title of the TRIAL_VIEW does not contain 'practice' or 'oefenen'
        self.assertNotIn("practice", next_round[2]["title"].lower())
        self.assertNotIn("oefenen", next_round[2]["title"].lower())

    def load_json_or_fail(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
        return response.json()
