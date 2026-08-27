import json

from django.test import TestCase

from experiment.actions.playback import PlaybackSection
from experiment.models import Block, Phase
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session


class MatchingPairsTest(TestCase):
    fixtures = ["choice_lists", "demographics", "matching_pairs"]

    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.get(name="TuneTwins")
        cls.playlist._update_sections()
        cls.participant = Participant.objects.create()
        cls.block = Block.objects.get(
            identifier="mpairs",
        )
        cls.session = Session.objects.create(block=cls.block, participant=cls.participant, playlist=cls.playlist)
        cls.rules = cls.session.block_rules()

    def test_next_round(self):
        actions = self.rules.next_round(self.session)
        # expect five extra question rounds and one extra explainer
        self.assertEqual(len(actions), 9)

    def test_matching_pairs_trial(self):
        self.rules.num_pairs = 2
        for i in range(6):
            trial = self.rules.get_matching_pairs_trial(self.session)
            self.assertIsNotNone(trial)
            data = self.session.json_data
            pairs = data.get("pairs")
            degradations = data.get("degradations")
            # there are three conditions (degradations) per audio segment, so 3 times as many sections as pairs
            self.assertEqual(
                len(pairs), (self.playlist._section_count() / 3) - (i + 1) * 2
            )
            # check that degradations cycle through list of two, list of one, empty list
            self.assertEqual(len(degradations), 2 - i % 3)

    def intermediate_score_request(self, data):
        request_data = {"json_data": json.dumps(data), **self.csrf_token, **self.session_data}
        self.client.post("/result/intermediate_score/", request_data)
        result = Result.objects.filter(question_identifier="move").last()
        return result

    def test_intermediate_score(self):
        participant_info = json.loads(self.client.get("/participant/").content)
        self.csrf_token = {"csrfmiddlewaretoken": participant_info.get("csrf_token")}
        self.session.participant = Participant.objects.get(pk=int(participant_info.get("id")))
        self.session.save()
        self.session_data = {"session_id": self.session.id}
        sections = [
            PlaybackSection(section) for section in self.playlist.section_set.all()
        ]
        data = {
            "first_card": {"link": sections[0].link},
            "second_card": {"link": sections[1].link},
        }
        result = self.intermediate_score_request(data)
        assert result.score == 10
        assert result.given_response == "lucky match"
        data["second_card"].update({"seen": True})
        result = self.intermediate_score_request(data)
        assert result.score == 20
        assert result.given_response == "match"
        data["second_card"] = {"link": sections[3].link, "seen": True}
        result = self.intermediate_score_request(data)
        assert result.score == -10
        assert result.given_response == "misremembered"
        data["first_card"].update({"seen": True})
        data["second_card"].pop("seen")
        result = self.intermediate_score_request(data)
        assert result.score == 0
        assert result.given_response == "no match"
