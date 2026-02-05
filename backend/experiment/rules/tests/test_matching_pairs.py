import json

from django.test import TestCase

from experiment.actions.playback import PlaybackSection
from experiment.models import Block
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session


class MatchingPairsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        section_csv = (
            "default,Crown_1_E1,0.0,10.0,MatchingPairs/Original/Crown_1_E1.mp3,Original,6\n"
            "default,Crown_1_E1,0.0,10.0,MatchingPairs/1stDegradation/Crown_1_E1.mp3,1stDegradation,6\n"
            "default,Crown_1_E1,0.0,10.0,MatchingPairs/2ndDegradation/Crown_1_E1.mp3,2ndDegradation,6\n"
            "default,ER_2_E1,0.0,10.0,MatchingPairs/Original/ER_2_E1.mp3,Original,21\n"
            "default,ER_2_E1,0.0,10.0,MatchingPairs/1stDegradation/ER_2_E1.mp3,1stDegradation,21\n"
            "default,ER_2_E1,0.0,10.0,MatchingPairs/2ndDegradation/ER_2_E1.mp3,2ndDegradation,21\n"
            "default,GameOfThrones_1_E1,0.0,10.0,MatchingPairs/Original/GameOfThrones_1_E1.mp3,Original,26\n"
            "default,GameOfThrones_1_E1,0.0,10.0,MatchingPairs/1stDegradation/GameOfThrones_1_E1.mp3,1stDegradation,26\n"
            "default,GameOfThrones_1_E1,0.0,10.0,MatchingPairs/2ndDegradation/GameOfThrones_1_E1.mp3,2ndDegradation,26\n"
            "default,RickandMorty_12_E1,0.0,10.0,MatchingPairs/Original/RickandMorty_12_E1.mp3,Original,44\n"
            "default,RickandMorty_12_E1,0.0,10.0,MatchingPairs/1stDegradation/RickandMorty_12_E1.mp3,1stDegradation,44\n"
            "default,RickandMorty_12_E1,0.0,10.0,MatchingPairs/2ndDegradation/RickandMorty_12_E1.mp3,2ndDegradation,44\n"
            "default,TwinPeaks_0_E1,0.0,10.0,MatchingPairs/1stDegradation/TwinPeaks_0_E1.mp3,1stDegradation,86\n"
            "default,TwinPeaks_0_E1,0.0,10.0,MatchingPairs/2ndDegradation/TwinPeaks_0_E1.mp3,2ndDegradation,86\n"
            "default,TwinPeaks_1_E1,0.0,10.0,MatchingPairs/Original/TwinPeaks_1_E1.mp3,Original,86\n"
        )
        cls.playlist = Playlist.objects.create(name="TestMatchingPairs")
        cls.playlist.csv = section_csv
        cls.playlist._update_sections()
        cls.participant = Participant.objects.create()
        cls.block = Block.objects.create(rules="MATCHING_PAIRS", slug="mpairs", rounds=42)
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
            assert trial
            data = self.session.json_data
            pairs = data.get("pairs")
            degradations = data.get("degradations")
            # degradations cycle through list of two, list of one, empty list
            if i % 2 == 0:
                # there are 5 pairs available in total from the playlist;
                # two are selected for this round, three saved for next
                assert len(pairs) == 3
            elif i % 3 == 0:
                assert len(degradations) == 2
            elif i % 3 == 1:
                assert len(degradations) == 1
            else:
                # two more pairs are selected for this round, one saved for next
                assert len(pairs) == 1
                assert len(degradations) == 0

    def intermediate_score_request(self, data):
        request_data = {"json_data": json.dumps(data), **self.csrf_token, **self.session_data}
        self.client.post("/result/intermediate_score/", request_data)
        result = Result.objects.filter(question_key="move").last()
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
