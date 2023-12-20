from django.test import TestCase
from django.db.models import Avg

from experiment.rules.musical_preferences import MusicalPreferences

from experiment.models import Experiment
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session

class MusicalPreferencesTest(TestCase):
    fixtures = ['playlist', 'experiment']
    
    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.create(name='MusicalPrefences')
        csv = ("SuperArtist,SuperSong,0.0,10.0,bat/artist1.mp3,0,0,0\n"
               "SuperArtist,MehSong,0.0,10.0,bat/artist2.mp3,0,0,0\n"
               "MehArtist,MehSong,0.0,10.0,bat/artist3.mp3,0,0,0\n"
               "AwfulArtist,MehSong,0.0,10.0,bat/artist4.mp3,0,0,0\n"
               "AwfulArtist,AwfulSong,0.0,10.0,bat/artist5.mp3,0,0,0\n")
        cls.playlist.csv = csv
        cls.playlist.update_sections()
        cls.experiment = Experiment.objects.create(name='MusicalPreferences', rounds=5)
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
            playlist=cls.playlist
        )

    def test_preferred_songs(self):
        for index, section in enumerate(list(self.playlist.section_set.all())):
            Result.objects.create(
                question_key='like_song',
                score=5-index,
                section=section,
                session=self.session
            )
        mp = MusicalPreferences()
        preferred_sections = mp.get_preferred_songs(self.session.result_set, 3)
        assert preferred_sections[0]['artist'] == 'SuperArtist'
        assert preferred_sections[1]['name'] == 'MehSong'
        assert preferred_sections[2]['artist'] == 'MehArtist'
        assert 'AwfulArtist' not in [p['artist'] for p in preferred_sections]