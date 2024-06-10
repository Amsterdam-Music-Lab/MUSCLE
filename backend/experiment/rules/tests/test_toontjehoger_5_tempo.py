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
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C5_P2_OR,or\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C5_P2_CH,or\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P1_OR,or\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C2_P1_CH,or\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C3_P1_OR,or\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C2_P2_OR,or\n"
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
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C6_P1_OR,or\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C1_P3_OR,or\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C1_P1_OZ,or\n"
        )
        playlist = Playlist.objects.create(name='TestToontjeHoger5Tempo')
        playlist.csv = csv_data
        playlist.update_sections()

        toontje_hoger_5_tempo_rules = ToontjeHoger5Tempo()
        self.assertEqual(
            toontje_hoger_5_tempo_rules.validate_playlist(playlist),
            [
                "Tags should start with either 'C', 'J' or 'R', followed by a number between "
                "1 and 5, followed by '_P', followed by either 1 or 2, followed by either "
                "'_OR' or '_CH'. Invalid tags: C1_P1_OZ, C1_P3_OR, C4_P2_ZR, C4_P9_OR, "
                'C6_P1_OR, F4_P2_OR'
            ]
        )

    def test_validate_playlist_invalid_groups(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C3_P2_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C2_P1_OR,ch\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,Eurovision/Set2/Karaoke/2018-11-00-07-046-k.mp3,C4_P2_OR,ch\n"
        )
        playlist = Playlist.objects.create(name='TestToontjeHoger5Tempo')
        playlist.csv = csv_data
        playlist.update_sections()

        toontje_hoger_5_tempo_rules = ToontjeHoger5Tempo()
        self.assertEqual(
            toontje_hoger_5_tempo_rules.validate_playlist(playlist),
            [
                "The playlist must contain two groups: 'or' and 'ch'. Found: ['ch']"
            ]
        )
