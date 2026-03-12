from django.test import TestCase

from experiment.models import Block
from experiment.rules.toontjehoger_2_preverbal import ToontjeHoger2Preverbal
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestToontjeHoger2Preverbal(TestCase):
    def setUp(self):
        playlist = Playlist.objects.create(
            name="thPreverbalTest",
            csv=(
                "AML,Duitse baby,0.0,1.0,/toontjehoger/preverbal/4_duitse_baby.mp3,b,2\n"
                "AML,Franse baby,0.0,1.0,/toontjehoger/preverbal/5_franse_baby.mp3,a,2\n"
                "AML,Mens,0.0,1.0,/toontjehoger/preverbal/1_mens.mp3,c,1\n"
                "AML,Trompet,0.0,1.0,/toontjehoger/preverbal/3_trompet.mp3,a,1\n"
                "AML,Walvis,0.0,1.0,/toontjehoger/preverbal/2_walvis.mp3,b,1\n"
            )
        )
        playlist._update_sections()
        self.block = Block.objects.create(slug="test_th_2", rules='TOONTJE_HOGER_2_PREVERBAL', rounds=2)
        self.session = Session.objects.create(block=self.block, playlist=playlist, participant=Participant.objects.create())

    def test_initializes_correctly(self):
        toontje_hoger_2_preverbal = ToontjeHoger2Preverbal()
        assert toontje_hoger_2_preverbal.ID == 'TOONTJE_HOGER_2_PREVERBAL'

    def test_can_play_through(self):
        rules = self.block.get_rules()
        for round in range(self.block.rounds):
            self.assertIsNotNone(rules.next_round(self.session))