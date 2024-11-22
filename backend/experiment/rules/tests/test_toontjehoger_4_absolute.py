from unittest.mock import patch

from django.test import TestCase

from section.models import Playlist as PlaylistModel

from experiment.rules.toontjehoger_4_absolute import ToontjeHoger4Absolute


class TestToontjeHoger4Absolute(TestCase):

    def setUp(self):
        # Mock the file_exists_validator function from section.models
        # instead of section.validators as it is imported in the Playlist class
        # which is in the section.models module
        patcher = patch('section.models.file_exists_validator')
        self.mock_file_exists_validator = patcher.start()
        self.mock_file_exists_validator.return_value = None
        self.addCleanup(patcher.stop)

    def test_initializes_correctly(self):
        toontje_hoger_4_absolute = ToontjeHoger4Absolute()
        assert toontje_hoger_4_absolute.ID == 'TOONTJE_HOGER_4_ABSOLUTE'

    def test_validate_valid_playlist(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-1.mp3,a,1\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-2.mp3,c,2\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-10.mp3,b,10\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-3.mp3,a,3\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-8.mp3,b,8\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-4.mp3,b,4\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-5.mp3,c,5\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-9.mp3,b,9\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-6.mp3,b,6\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-7.mp3,b,7\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-11.mp3,b,11\n"
        )
        playlist = PlaylistModel.objects.create(name='TestToontjeHoger4Absolute')
        playlist.csv = csv_data
        playlist._update_sections()

        toontje_hoger_4_absolute = ToontjeHoger4Absolute()
        self.assertEqual(
            toontje_hoger_4_absolute.validate_playlist(playlist), []
        )

    def test_validate_invalid_integer_groups(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-1.mp3,a,a\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-2.mp3,c,2\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-3.mp3,a,4\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-4.mp3,b,4\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-5.mp3,c,11\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-6.mp3,b,7\n"
        )
        playlist = PlaylistModel.objects.create(name='TestToontjeHoger4Absolute')
        playlist.csv = csv_data
        playlist._update_sections()

        toontje_hoger_4_absolute = ToontjeHoger4Absolute()

        self.assertEqual(
            toontje_hoger_4_absolute.validate_playlist(playlist),
            ["Groups in playlist sections should be numbers. This playlist has groups: ['11', '2', '4', '7', 'a']"]
        )

    def test_validate_invalid_sequential_groups(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-1.mp3,a,8\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-2.mp3,c,3\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-3.mp3,a,3\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-4.mp3,b,4\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-5.mp3,c,11\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-6.mp3,b,1\n"
        )
        playlist = PlaylistModel.objects.create(name='TestToontjeHoger4Absolute')
        playlist.csv = csv_data
        playlist._update_sections()

        toontje_hoger_4_absolute = ToontjeHoger4Absolute()

        self.assertEqual(
            toontje_hoger_4_absolute.validate_playlist(playlist),
            ['Groups in playlist sections should be sequential numbers starting from 1 to the number of items in the playlist (13). E.g. "1, 2, 3, ... 13"']
        )

    def test_validate_invalid_tags(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-1.mp3,a,1\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-2.mp3,c,2\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-3.mp3,a,3\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-4.mp3,b,4\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-5.mp3,c,5\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-6.mp3,d,6\n"
        )
        playlist = PlaylistModel.objects.create(name='TestToontjeHoger4AbsoluteInvalidTags')
        playlist.csv = csv_data
        playlist._update_sections()

        toontje_hoger_4_absolute = ToontjeHoger4Absolute()
        self.assertEqual(
            toontje_hoger_4_absolute.validate_playlist(playlist),
            ['Tags in playlist sections should be \'a\', \'b\' or \'c\'. This playlist has tags: [\'a\', \'b\', \'c\', \'d\']']
        )
