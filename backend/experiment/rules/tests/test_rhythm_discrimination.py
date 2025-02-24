from django.test import TestCase

from experiment.models import Block, ExperimentTranslatedContent
from participant.models import Participant
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

    def test_get_next_trial(self):
        rules = self.block.get_rules()
        rules.plan_stimuli(self.session)
        self.session.save_json_data({"practice_done": True})
        trial = rules.get_next_trial(self.session)
        assert trial

    def test_block_flow(self):
        # Initial setup
        participant = self._setup_participant()
        block_json = self._get_block_info("rhdis")
        session_id = block_json["session_id"]

        # Test practice rounds (first 4 rounds)
        self._validate_practice_round(session_id, 1, participant, actions=["EXPLAINER", "EXPLAINER", "TRIAL_VIEW"])
        self._validate_practice_round(session_id, 2, participant)
        self._validate_practice_round(session_id, 3, participant)
        self._validate_practice_round(session_id, 4, participant)
        self._validate_practice_round(
            session_id, 5, participant, actions=["EXPLAINER", "EXPLAINER"]
        )

        # Test real rounds (should be 36 rounds)
        for i in range(36):
            real_round_number = i + 5  # Real rounds start from 5th round
            self._validate_real_round(session_id, real_round_number, participant)

        # Debriefing (one single 'FINAL' view)
        next_round = self._get_next_round(session_id)
        self.assertEqual(len(next_round), 1)
        self.assertEqual(next_round[0]["view"], "FINAL")

    def _setup_participant(self):
        """Setup participant and session data"""
        participant_response = self.client.get("/participant/")
        participant = self.load_json_or_fail(participant_response)

        self.assertTrue("id" in participant)
        self.assertTrue(participant["id"])

        session = self.client.session
        session.update({"participant_id": participant["id"]})
        session.save()

        return participant

    def _validate_practice_round(self, session_id, round_number, participant, actions=["EXPLAINER", "TRIAL_VIEW"]):
        next_round = self._get_next_round(session_id)

        # Check practice round structure
        for i, action in enumerate(actions):
            self.assertEqual(next_round[i]["view"], action, f"Round {round_number} action {i} is not {action}")

        # Trial view index
        try:
            trial_view_index = actions.index("TRIAL_VIEW")
            trial_view = next_round[trial_view_index]
        except:
            # no trial view, return
            return next_round

        # Check title requirements for practice round - should contain "practice" or "oefenen"
        trial_title = trial_view["title"].lower()
        self.assertTrue(
            "practice" in trial_title or "oefenen" in trial_title, f"Round {round_number} title is not practice"
        )

        # Submit score for practice round
        self._submit_score(
            session_id=session_id,
            result_id=trial_view["feedback_form"]["form"][0]["result_id"],
            expected_response=trial_view["feedback_form"]["form"][0]["expected_response"],
            csrf_token=participant["csrf_token"],
        )

        return next_round

    def _validate_real_round(self, session_id, round_number, participant, actions=["TRIAL_VIEW"]):
        next_round = self._get_next_round(session_id)

        # Check real round structure
        for i, action in enumerate(actions):
            self.assertEqual(next_round[i]["view"], action, f"Round {round_number} action {i} is not {action}")

        # Check title requirements for real round
        trial_view_index = actions.index("TRIAL_VIEW")
        trial_view = next_round[trial_view_index]
        trial_title = trial_view["title"].lower()
        title_round_number = round_number - 4  # Real rounds start from 5th round
        self.assertNotIn("practice", trial_title, f"Round {round_number} title contains practice")
        self.assertNotIn("oefenen", trial_title, f"Round {round_number} title contains oefenen")
        self.assertTrue(
            f"{title_round_number} van " in trial_title or f"{title_round_number} of " in trial_title,
            f"Round {round_number} title is not {title_round_number} van",
        )

        # Submit score for real round
        self._submit_score(
            session_id=session_id,
            result_id=trial_view["feedback_form"]["form"][0]["result_id"],
            expected_response=trial_view["feedback_form"]["form"][0]["expected_response"],
            csrf_token=participant["csrf_token"],
        )

        return next_round

    def _get_block_info(self, block_slug):
        """Get block information"""
        block_response = self.client.get(f"/experiment/block/{block_slug}/")
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

        return block_json

    def _get_next_round(self, session_id):
        """Get next round data"""
        next_round_response = self.client.post(f"/session/{session_id}/next_round/")
        return self.load_json_or_fail(next_round_response).get("next_round")

    def _submit_score(self, session_id, result_id, expected_response, csrf_token):
        """Submit score for a round"""
        score_response = self.client.post(
            "/result/score/",
            {
                "session_id": session_id,
                "json_data": '{"decision_time":2,"form":[{"key":"same","value":"%s","result_id":%s}]}'
                % (expected_response, result_id),
                "csrfmiddlewaretoken": csrf_token,
            },
        )
        self.load_json_or_fail(score_response)

    def load_json_or_fail(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

        return response.json()
