from django.test import TestCase

from experiment.models import Block, Phase
from experiment.rules.toontjehoger_1_mozart import ToontjeHoger1Mozart
from experiment.rules.toontjehogerkids_1_mozart import ToontjeHogerKids1Mozart
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestToontjeHoger1Mozart(TestCase):
    fixtures = ["toontjehoger"]

    def test_initializes(self):
        rules = ToontjeHoger1Mozart()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_1_MOZART")

    def test_can_play_through(self):
        playlist = Playlist.objects.get(name="Toontje Hoger 1 - Mozart")
        playlist._update_sections()
        block = Block.objects.get(identifier="th_mozart")
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            actions = rules.next_round(session)
            last_result = session.result_set.last()
            last_result.score = rules.SCORE_CORRECT
            last_result.save()
            self.assertIsNotNone(actions)


class TestToontjeHogerKids1Mozart(TestCase):
    fixtures = ["toontjehoger_kids"]

    def test_initializes(self):
        rules = ToontjeHogerKids1Mozart()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_KIDS_1_MOZART")

    def test_can_play_through(self):
        playlist = Playlist.objects.get(name="THK_Mozart")
        playlist._update_sections()
        block = Block.objects.get(identifier="thk_mozart")
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            actions = rules.next_round(session)
            last_result = session.result_set.last()
            last_result.score = rules.SCORE_CORRECT
            last_result.save()
            self.assertIsNotNone(actions)
