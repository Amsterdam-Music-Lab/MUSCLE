from django.test import TestCase

from experiment.models import Block
from experiment.rules.toontjehoger_2_preverbal import ToontjeHoger2Preverbal
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestToontjeHoger2Preverbal(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.create(
            name="thPreverbalTest",
            csv=(
                "AML,Duitse baby,0.0,1.0,/toontjehoger/preverbal/4_duitse_baby.mp3,b,2\n"
                "AML,Franse baby,0.0,1.0,/toontjehoger/preverbal/5_franse_baby.mp3,a,2\n"
                "AML,Mens,0.0,1.0,/toontjehoger/preverbal/1_mens.mp3,c,1\n"
                "AML,Trompet,0.0,1.0,/toontjehoger/preverbal/3_trompet.mp3,a,1\n"
                "AML,Walvis,0.0,1.0,/toontjehoger/preverbal/2_walvis.mp3,b,1\n"
            ),
        )
        cls.playlist._update_sections()

    def test_initializes_correctly(self):
        toontje_hoger_2_preverbal = ToontjeHoger2Preverbal()
        assert toontje_hoger_2_preverbal.ID == 'TOONTJE_HOGER_2_PREVERBAL'

    def test_can_play_through_th(self):
        block_th = Block.objects.create(
            slug="test_th_2", rules='TOONTJE_HOGER_2_PREVERBAL', rounds=2
        )
        session = Session.objects.create(
            block=block_th,
            playlist=self.playlist,
            participant=Participant.objects.create(),
        )
        rules = block_th.get_rules()
        for round in range(block_th.rounds):
            self.assertIsNotNone(rules.next_round(session))

    def test_playthough_th_kids(self):
        block_th = Block.objects.create(
            slug="test_th_2", rules='TOONTJE_HOGER_KIDS_2_PREVERBAL', rounds=2
        )
        session = Session.objects.create(
            block=block_th,
            playlist=self.playlist,
            participant=Participant.objects.create(),
        )
        rules = block_th.get_rules()
        for round in range(block_th.rounds):
            self.assertIsNotNone(rules.next_round(session))
