from django.test import TestCase

from experiment.models import Block
from experiment.rules.toontjehoger_6_relative import ToontjeHoger6Relative
from experiment.rules.toontjehogerkids_6_relative import ToontjeHogerKids6Relative
from participant.models import Participant
from section.models import Playlist
from session.models import Session

def get_playlist():
    playlist = Playlist.objects.create(name="test-th-6", csv=(
        "AML,Fragment A,0.0,1.0,/toontjehoger/relative/relative_a.mp3,a,0\n"
        "AML,Fragment B,0.0,1.0,/toontjehoger/relative/relative_b.mp3,b,0\n"
        "AML,Fragment C,0.0,1.0,/toontjehoger/relative/relative_c.mp3,c,0\n"
    ))
    playlist._update_sections()
    return playlist

class TestToontjeHoger6Relative(TestCase):
    
    def test_th_6_initializes(self):
        rules = ToontjeHoger6Relative()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_6_RELATIVE")

    def test_can_play_through_th_6(self):
        block = Block.objects.create(slug="test-th-6", rules="TOONTJE_HOGER_6_RELATIVE", rounds=2)
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=get_playlist())
        rules = session.block_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))
    
    def test_thk_6_initializes(self):
        rules = ToontjeHogerKids6Relative()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_KIDS_6_RELATIVE")

    def test_can_play_through_thk_6(self):
        block = Block.objects.create(slug="test-thk-6", rules="TOONTJE_HOGER_KIDS_6_RELATIVE", rounds=2)
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=get_playlist())
        rules = session.block_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))