from django.test import TestCase

from experiment.models import Block
from experiment.rules.toontjehoger_3_plink import ToontjeHoger3Plink
from experiment.rules.toontjehogerkids_3_plink import ToontjeHogerKids3Plink
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestToontjeHoger3Plink(TestCase):
    
    def test_initializes(self):
        rules = ToontjeHoger3Plink()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_3_PLINK")

    def test_can_play_through(self):
        playlist = Playlist.objects.create(name="test-th-plink", csv=(
            "Billy Joel,Piano Man,0.0,1.0,toontjehoger/plink/2021-005.mp3,70s,vrolijk\n"
            "Boudewijn de Groot,Avond,0.0,1.0,toontjehoger/plink/2021-010.mp3,90s,tederheid\n"
            "Bruce Springsteen,The River,0.0,1.0,toontjehoger/plink/2021-016.mp3,80s,droevig\n"
            "Coldplay,Fix You,0.0,1.0,toontjehoger/plink/2021-011.mp3,00s,tederheid\n"
            "Danny Vera,Roller Coaster,0.0,1.0,toontjehoger/plink/2021-002.mp3,10s,tederheid\n"
            "David Bowie,Heroes,0.0,1.0,toontjehoger/plink/2021-024.mp3,70s,vrolijk\n"
            "Deep Purple,Child In Time,0.0,1.0,toontjehoger/plink/2021-015.mp3,70s,boosheid\n"
            "Di-rect,Soldier On,0.0,1.0,toontjehoger/plink/2021-014.mp3,20s,tederheid\n"
            "Dire Straits,Brothers In Arms,0.0,1.0,toontjehoger/plink/2021-018.mp3,80s,angst\n"
            "Dire Straits,Sultans Of Swing,0.0,1.0,toontjehoger/plink/2021-025.mp3,70s,vrolijk\n"
            "Disturbed,The Sound Of Silence,0.0,1.0,toontjehoger/plink/2021-019.mp3,10s,droevig\n"
            "Eagles,Hotel California,0.0,1.0,toontjehoger/plink/2021-004.mp3,70s,droevig\n"
            "Golden Earring,Radar Love,0.0,1.0,toontjehoger/plink/2021-006.mp3,70s,vrolijk\n"
        ))
        playlist._update_sections()
        block = Block.objects.create(slug="test-th-plink", rules="TOONTJE_HOGER_3_PLINK", rounds=10)
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))


class TestToontjeHogerKids3Plink(TestCase):
    
    def test_initializes(self):
        rules = ToontjeHogerKids3Plink()
        self.assertEqual(rules.ID, "TOONTJE_HOGER_KIDS_3_PLINK")

    def test_can_play_through(self):
        playlist = Playlist.objects.create(name="test-thk-plink", csv=(
            "Adele,Hello,0.0,1.0,toontjehoger_kids/plink/2024-003.mp3,0,60s;droevig\n"
            "Flemming,Alles Op Gevoel,0.0,1.0,toontjehoger_kids/plink/2024-006.mp3,0,70s;vrolijk\n"
            "Frozen,Laat Het Los,0.0,1.0,toontjehoger_kids/plink/2024-011.mp3,0,00s;tederheid\n"
            "Joost Klein,Europapa,0.0,1.0,toontjehoger_kids/plink/2024-007.mp3,0,70s;tederheid\n"
            "K3,De 3 Biggetjes,0.0,1.0,toontjehoger_kids/plink/2024-001.mp3,0,70s;droevig\n"
            "Kinderen Voor Kinderen,Daba Die Daba Daa,0.0,1.0,toontjehoger_kids/plink/2024-002.mp3,0,10s;tederheid\n"
            "Mariah Carey,All I Want For Christmas,0.0,1.0,toontjehoger_kids/plink/2024-010.mp3,0,90s;tederheid\n"
            "Meau,Stukje Van Mij,0.0,1.0,toontjehoger_kids/plink/2024-005.mp3,0,70s;vrolijk\n"
            "Pinkfong,Baby Shark,0.0,1.0,toontjehoger_kids/plink/2024-008.mp3,0,90s;droevig\n"
            "S10,De Diepte,0.0,1.0,toontjehoger_kids/plink/2024-004.mp3,0,70s;droevig\n"
            "Snelle,Schuur,0.0,1.0,toontjehoger_kids/plink/2024-014.mp3,0,20s;tederheid\n"
            "Snollebollekes,Links Rechts,0.0,1.0,toontjehoger_kids/plink/2024-009.mp3,0,90s;droevig\n"
            "Super Mario Bros.,de intro,0.0,1.0,toontjehoger_kids/plink/2024-013.mp3,0,70s;droevig\n"
            "The Tokens,The Lion Sleeps Tonight (Wimoweh),0.0,1.0,toontjehoger_kids/plink/2024-012.mp3,0,70s;tederheid\n"
        ))
        playlist._update_sections()
        block = Block.objects.create(slug="test-thk-plink", rules="TOONTJE_HOGER_KIDS_3_PLINK", rounds=10)
        session = Session.objects.create(block=block, participant=Participant.objects.create(), playlist=playlist)
        rules = block.get_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))