from django.test import TestCase

from experiment.models import Block, Experiment, Phase
from experiment.rules.toontjehoger_3_plink import ToontjeHoger3Plink
from experiment.rules.toontjehogerkids_3_plink import ToontjeHogerKids3Plink
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestToontjeHoger3Plink(TestCase):
    fixtures = ["toontjehoger"]

    def test_initializes(self):
        rules = ToontjeHoger3Plink()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_3_PLINK")

    def test_can_play_through(self):
        playlist = Playlist.objects.get(name="Toontje Hoger 3 - Plink")
        playlist._update_sections()
        block = Block.objects.get(identifier="th_plink")
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            actions = rules.next_round(session)
            last_result = session.result_set.filter(question_identifier='plink').last()
            last_result.score = rules.SCORE_MAIN_CORRECT
            last_result.save()
            self.assertIsNotNone(actions)


class TestToontjeHogerKids3Plink(TestCase):
    fixtures = ["toontjehoger_kids"]

    def test_initializes(self):
        rules = ToontjeHogerKids3Plink()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_KIDS_3_PLINK")

    def test_can_play_through(self):
        playlist = Playlist.objects.get(name="THK_Plink")
        playlist._update_sections()
        block = Block.objects.get(identifier="thk_plink")
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))
