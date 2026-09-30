from django.test import TestCase

from experiment.models import Block, Phase
from experiment.rules.toontjehoger_2_preverbal import ToontjeHoger2Preverbal
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestToontjeHoger2Preverbal(TestCase):
    fixtures = ["toontjehoger", "toontjehoger_kids"]

    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.get(name="Toontje Hoger 2 - Preverbal")
        cls.playlist._update_sections()

    def test_initializes_correctly(self):
        toontje_hoger_2_preverbal = ToontjeHoger2Preverbal()
        assert toontje_hoger_2_preverbal.ID == 'TOONTJE_HOGER_2_PREVERBAL'

    def test_can_play_through(self):
        block_th = Block.objects.get(identifier="th_preverbal")
        session = Session.objects.create(
            block=block_th,
            playlist=self.playlist,
            participant=Participant.objects.create(),
        )
        rules = block_th.get_rules()
        for round in range(block_th.rounds):
            self.assertIsNotNone(rules.next_round(session))

    def test_playthough_th_kids(self):
        block_th = Block.objects.get(identifier="thk_preverbal")
        session = Session.objects.create(
            block=block_th,
            playlist=self.playlist,
            participant=Participant.objects.create(),
        )
        rules = block_th.get_rules()
        for round in range(block_th.rounds):
            self.assertIsNotNone(rules.next_round(session))
