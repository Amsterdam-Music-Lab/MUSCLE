from django.test import TestCase

from experiment.models import Block
from experiment.rules.toontjehoger_1_mozart import ToontjeHoger1Mozart
from experiment.rules.toontjehogerkids_1_mozart import ToontjeHogerKids1Mozart
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestToontjeHoger1Mozart(TestCase):

    def test_initializes(self):
        rules = ToontjeHoger1Mozart()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_1_MOZART")

    def test_can_play_through(self):
        playlist = Playlist.objects.create(
            name="thPreverbalTest",
            csv=(
                'Tomaso Albinoni,"Adagio in G mineur, uitgevoerd door het Prague Baroque Orchestra, onder leiding van Trevor Pinnock",0.0,26.0,/toontjehoger/mozart/fragment_a.mp3,0,1\n'
                'Wolfgang Amadeus Mozart,"Sonate voor twee pianos in D groot, KV 448 (uitgevoerd door Lucas en Arthur Jussen)",0.0,28.0,/toontjehoger/mozart/fragment_b.mp3,0,2\n'
            ),
        )
        playlist._update_sections()
        block = Block.objects.create(slug="th-1-test", rules="TOONTJE_HOGER_1_MOZART", rounds=2)
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            actions = rules.next_round(session)
            last_result = session.result_set.last()
            last_result.score = rules.SCORE_CORRECT
            last_result.save()
            self.assertIsNotNone(actions)


class TestToontjeHogerKids1Mozart(TestCase):

    def test_initializes(self):
        rules = ToontjeHogerKids1Mozart()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_KIDS_1_MOZART")

    def test_can_play_through(self):
        playlist = Playlist.objects.create(name="thk1KidsMozart", csv=(
            'componist Albinoni (gespeeld door het Praags Barokorkest met dirigent Trevor Pinnock),Adagio in G mineur,0.0,12.0,toontjehoger_kids/mozart/fragment_a.mp3,0,1\n'
            'componist Mozart (gespeeld door Lucas en Arthur Jussen),Sonate voor twee pianos in D groot,0.0,14.0,toontjehoger_kids/mozart/fragment_b.mp3,0,2\n'
        ))
        playlist._update_sections()
        block = Block.objects.create(slug="thk-1-test", rules="TOONTJE_HOGER_KIDS_1_MOZART", rounds=2)
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))
