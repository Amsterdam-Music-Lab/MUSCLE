from unittest.mock import patch

from django.test import TestCase

from section.models import Playlist

from experiment.rules.toontjehogerkids_5_tempo import ToontjeHogerKids5Tempo


class ToontjeHogerKids5TempoTest(TestCase):

    def setUp(self):
        # Mock the file_exists_validator function from section.models
        # instead of section.validators as it is imported in the Playlist class
        # which is in the section.models module
        patcher = patch('section.models.file_exists_validator')
        self.mock_file_exists_validator = patcher.start()
        self.mock_file_exists_validator.return_value = None
        self.addCleanup(patcher.stop)

    # Toontje Hoger Kids 5 Tempo does not have the strict tag validation
    # that Toontje Hoger 5 Tempo has. Therefore, we must ensure that
    # the validate_playlist method does not raise any errors for tags
    # that would be considered invalid in Toontje Hoger 5 Tempo.
    def test_validate_playlist_valid(self):
        csv_data = (
            "song-01,artist-01,7.046,45.0,ToontjeHoger5Tempo/song-01.mp3,C3_P2_OR,ch\n"
            "song-02,artist-02,7.046,45.0,ToontjeHoger5Tempo/song-02.mp3,C2_P1_OR,ch\n"
            "song-03,artist-03,7.046,45.0,ToontjeHoger5Tempo/song-03.mp3,C4_P2_OR,ch\n"
            "song-04,artist-04,7.046,45.0,ToontjeHoger5Tempo/song-04.mp3,C4_P2_OR,ch\n"
            "song-05,artist-05,7.046,45.0,ToontjeHoger5Tempo/song-05.mp3,C5_P2_OR,ch\n"
            "song-06,artist-06,7.046,45.0,ToontjeHoger5Tempo/song-06.mp3,C5_P2_CH,ch\n"
            "song-07,artist-07,7.046,45.0,ToontjeHoger5Tempo/song-07.mp3,C4_P1_OR,ch\n"
            "song-08,artist-08,7.046,45.0,ToontjeHoger5Tempo/song-08.mp3,C2_P1_CH,or\n"
            "song-09,artist-09,7.046,45.0,ToontjeHoger5Tempo/song-09.mp3,C3_P1_OR,or\n"
            "song-10,artist-10,7.046,45.0,ToontjeHoger5Tempo/song-10.mp3,C2_P2_OR,or\n"
            "song-11,artist-11,7.046,45.0,ToontjeHoger5Tempo/song-11.mp3,F4_P2_OR,or\n"
            "song-12,artist-12,7.046,45.0,ToontjeHoger5Tempo/song-12.mp3,C4_P9_OR,or\n"
            "song-13,artist-13,7.046,45.0,ToontjeHoger5Tempo/song-13.mp3,C4_P2_ZR,or\n"
            "song-14,artist-14,7.046,45.0,ToontjeHoger5Tempo/song-14.mp3,C6_P1_OR,or\n"
            "song-15,artist-15,7.046,45.0,ToontjeHoger5Tempo/song-15.mp3,C1_P3_OR,or\n"
            "song-16,artist-16,7.046,45.0,ToontjeHoger5Tempo/song-16.mp3,C1_P1_OZ,or\n"
        )
        playlist = Playlist.objects.create(name='TestToontjeHoger5Tempo')
        playlist.csv = csv_data
        playlist._update_sections()

        toontje_hoger_5_tempo_rules = ToontjeHogerKids5Tempo()
        self.assertEqual(
            toontje_hoger_5_tempo_rules.validate_playlist(playlist), []
        )
