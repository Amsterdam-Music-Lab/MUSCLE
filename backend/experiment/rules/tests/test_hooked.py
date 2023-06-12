from django.test import TestCase

from experiment.models import Experiment
from experiment.rules import Eurovision2020, Huang2022, ThatsMySong
from participant.models import Participant
from section.models import Playlist
from session.models import Session

class HookedTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ''' set up data for Hooked base class '''
        cls.participant = Participant.objects.create()
        section_csv = (
            "Brenda Lee,I'm Sorry,70.501,45,ThatsMySong/1960 - Brenda Lee - I'm Sorry - Verse - 3.mp3,0,Verse,1960s\n"
            "Jimmy Dean,Big Bad John,96.239,45,ThatsMySong/1961 - Jimmy Dean - Big Bad John - Verse - 4.mp3,0,Verse,1960s\n"
            "Marvin Gaye,Let's Get It On,49.199,45,ThatsMySong/1973 - Marvin Gaye - Let's Get It On - Chorus.mp3,0,Chorus,1970s\n"
            "The Bee Gees,Stayin' Alive,0,45,ThatsMySong/1977 - The Bee Gees - Stayin' Alive - Verse - 3.mp3,0,Verse,1970s\n"
            "Queen,Another One Bites the Dust,39.642,45,ThatsMySong/1980 - Queen - Another One Bites the Dust - Chorus - 2.mp3,0,Chorus,1980s\n"
            "The Steve Miller Band,Abracadabra,263.082,45,ThatsMySong/1981 - The Steve Miller Band - Abracadabra - Verse - 6.mp3,0,Verse,1980s\n"
            "Boyz II Men,End of the Road,57.915,45,ThatsMySong/1992 - Boyz II Men - End of the Road - Chorus - 2.mp3,0,Chorus,1990s\n"
            "Whitney Houston,I Will Always Love You,188.059,45,ThatsMySong/1992 - Whitney Houston - I Will Always Love You - Verse - 2.mp3,0,Verse,1990s\n"
            "Mariah Carey,We Belong Together,131.301,45,ThatsMySong/2005 - Mariah Carey - We Belong Together - Verse - 2.mp3,0,Verse,2000s\n"
            "The Black Eyed Peas,I Gotta Feeling,119.977,45,ThatsMySong/2009 - The Black Eyed Peas - I Gotta Feeling - Other - 1.mp3,0,Other,2000s\n"
        )
        cls.playlist = Playlist.objects.create(name='TestHooked')
        cls.playlist.csv = section_csv
        cls.playlist.update_sections()

    def test_eurovision(self):
        section_csv = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,euro2/Karaoke/2018-11-00-07-046-k.mp3,0,3,201811007\n"
            "Lithuania 2018 - Ieva Zasimauskaitė,When We're Old,2.743,45.0,euro2/V1/2018-12-00-02-743-v1.mp3,0,1,201812003\n"
            "Italy 2019 - Mahmood,Soldi,65.37,45.0,euro2/V2/2019-02-01-05-370-v2.mp3,0,2,201902065\n"
            "Iceland 2019 - Hatari,Hatrið mun sigra,136.666,45.0,euro/2019-10-02-16-666-c2.mp3,0,0,201910137\n"
            "Netherlands 2016 - Douwe Bob,Slow Down,3.501,45.0,euro/2016-11-00-03-501-v1.mp3,0,0,201611004\n"
            "Serbia 2018 - Sanja Ilić & Balkanika,Nova Deca,0.0,45.0,euro/2018-19-00-00-000-v1.mp3,0,0,201819000\n"
            "United Kingdom 2017 - Lucie Jones,Never Give Up on You,94.575,45.0,euro/2017-15-01-34-575-c2.mp3,0,0,201715095\n"
        )
        playlist = Playlist.objects.create(name='TestEurovision')
        playlist.csv = section_csv
        playlist.update_sections()
        assert playlist.section_set.count() == 7
        assert playlist.section_set.filter(tag=0).count() == 4
        assert len(list(playlist.song_ids({'tag__lt': 3}))) == 6
        assert len(list(playlist.song_ids({'tag__gt': 0}))) == 3
        
        experiment = Experiment.objects.create(rules='EUROVISION_2020', slug='eu', rounds=6)
        session = Session.objects.create(
            experiment=experiment,
            participant=self.participant,
            playlist=playlist
        )
        Eurovision2020.plan_sections(session)
        assert session.load_json_data().get('plan') != None
        action = Eurovision2020.next_song_sync_action(session)
        assert action != None
        action = Eurovision2020.next_heard_before_action(session)
        assert action != None
    
    def test_thats_my_song(self):
        experiment = Experiment.objects.create(rules='THATS_MY_SONG', slug='tms', rounds=6)
        session = Session.objects.create(
            experiment=experiment,
            participant=self.participant,
            playlist=self.playlist
        )
        assert ThatsMySong.feedback_info() == None
        ThatsMySong.plan_sections(session)
        assert session.load_json_data().get('plan') != None
        assert ThatsMySong.next_song_sync_action(session) != None
        [session.increment_round() for i in range(4)]
        assert ThatsMySong.next_heard_before_action(session) != None
    
    def test_hooked_china(self):
        assert Huang2022.feedback_info() != None
