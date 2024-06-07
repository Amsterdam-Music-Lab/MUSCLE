from unittest.mock import patch

from django.test import TestCase

from section.models import Playlist

from experiment.rules.toontjehoger_5_tempo import ToontjeHoger5Tempo


class ToontjeHoger5TempoTest(TestCase):

    def setUp(self):
        # Mock the file_exists_validator function from section.models
        # instead of section.validators as it is imported in the Playlist class
        # which is in the section.models module
        patcher = patch('section.models.file_exists_validator')
        self.mock_file_exists_validator = patcher.start()
        self.mock_file_exists_validator.return_value = None
        self.addCleanup(patcher.stop)

    def test_validate_playlist_valid(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C3_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C2_P1_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C5_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C5_P2_CH,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P1_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C2_P1_CH,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C3_P1_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C2_P2_OR,ch\n"
        )
        playlist = Playlist.objects.create(name='TestToontjeHoger5Tempo')
        playlist.csv = csv_data
        playlist.update_sections()

        toontje_hoger_5_tempo_rules = ToontjeHoger5Tempo()
        self.assertEqual(
            toontje_hoger_5_tempo_rules.validate_playlist(playlist), []
        )

    def test_validate_playlist_invalid_tags(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,F4_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P9_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P2_ZR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C6_P1_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C1_P3_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C1_P1_OZ,ch\n"
        )
        playlist = Playlist.objects.create(name='TestToontjeHoger5Tempo')
        playlist.csv = csv_data
        playlist.update_sections()

        toontje_hoger_5_tempo_rules = ToontjeHoger5Tempo()
        self.assertEqual(
            toontje_hoger_5_tempo_rules.validate_playlist(playlist),
            [
                'Invalid tag: C1_P1_OZ',
                'Invalid tag: C1_P3_OR',
                'Invalid tag: C4_P2_ZR',
                'Invalid tag: C4_P9_OR',
                'Invalid tag: C6_P1_OR',
                'Invalid tag: F4_P2_OR',
            ]
        )
