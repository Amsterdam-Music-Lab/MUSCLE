from django.test import TestCase

from experiment.models import Block, Phase
from experiment.rules.toontjehoger_6_relative import ToontjeHoger6Relative
from experiment.rules.toontjehogerkids_6_relative import ToontjeHogerKids6Relative
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestToontjeHoger6Relative(TestCase):
    fixtures = ["toontjehoger", "toontjehoger_kids"]

    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.get(name="Toontje Hoger 6 - Relative")
        cls.playlist._update_sections()

    def test_th_6_initializes(self):
        rules = ToontjeHoger6Relative()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_6_RELATIVE")

    def test_can_play_through_th_6(self):

        block = Block.objects.get(identifier="th_relative")
        session = Session.objects.create(
            block=block,
            participant=Participant.objects.create(),
            playlist=self.playlist,
        )
        rules = session.block_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))

    def test_thk_6_initializes(self):
        rules = ToontjeHogerKids6Relative()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_KIDS_6_RELATIVE")

    def test_can_play_through_thk_6(self):
        block = Block.objects.get(identifier="thk_relative")
        session = Session.objects.create(
            block=block,
            participant=Participant.objects.create(),
            playlist=self.playlist,
        )
        rules = session.block_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))
