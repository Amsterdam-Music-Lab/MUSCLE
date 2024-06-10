from unittest.mock import patch

from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from result.models import Result
from section.models import Playlist as PlaylistModel
from session.models import Session

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

    @classmethod
    def setUpTestData(self):
        self.section_csv = (
            "Dave,m1_contour_practice,0.0,20.0,samediff/melody_1_contour.wav,practice,1\n"
            "Dave,m2_same_practice,0.0,20.0,samediff/melody_1_same.wav,practice,1\n"
            "Dave,m1_same,0.0,20.0,samediff/melody_1_same.wav,A,1\n"
            "Dave,m1_scale,0.0,20.0,samediff/melody_1_scale.wav,B,1\n"
            "Dave,m1_contour,0.0,20.0,samediff/melody_1_contour.wav,C,1\n"
            "Dave,m1_interval,0.0,20.0,samediff/melody_1_interval.wav,D,1\n"
            "Dave,m1_same,0.0,20.0,samediff/melody_1_same.wav,A,2\n"
            "Dave,m1_scale,0.0,20.0,samediff/melody_1_scale.wav,B,2\n"
            "Dave,m1_contour,0.0,20.0,samediff/melody_1_contour.wav,C,2\n"
            "Dave,m1_interval,0.0,20.0,samediff/melody_1_interval.wav,D,2\n"
        )
        self.playlist = PlaylistModel.objects.create(name='ToontjeHoger4Absolute')
        self.playlist.csv = self.section_csv
        self.playlist.update_sections()
        self.participant = Participant.objects.create()
        self.experiment = Experiment.objects.create(
            name='ToontjeHoger4Absolute',
            slug='toontjehoger_4_absolute',
            rounds=4,
        )
        self.session = Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            playlist=self.playlist
        )

    def test_initializes_correctly(self):
        toontje_hoger_4_absolute = ToontjeHoger4Absolute()
        assert toontje_hoger_4_absolute.ID == 'TOONTJE_HOGER_4_ABSOLUTE'

    def test_validate_valid_groups(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-1.mp3,1,1\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-2.mp3,2,2\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-3.mp3,3,3\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-4.mp3,4,4\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-5.mp3,5,5\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-6.mp3,6,6\n"
        )
        playlist = PlaylistModel.objects.create(name='TestToontjeHoger5Tempo')
        playlist.csv = csv_data
        playlist.update_sections()

        toontje_hoger_4_absolute = ToontjeHoger4Absolute()
        self.assertEqual(
            toontje_hoger_4_absolute.validate_playlist(playlist), []
        )

    def test_validate_invalid_groups(self):
        csv_data = (
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-1.mp3,1,a\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-2.mp3,2,2\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-3.mp3,3,4\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-4.mp3,4,4\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-5.mp3,5,5\n"
            "Albania 2018 - Eugent Bushpepa,Mall,7.046,45.0,ToontjeHoger4Absolute/audio-6.mp3,6,7\n"
        )
        playlist = PlaylistModel.objects.create(name='TestToontjeHoger5Tempo')
        playlist.csv = csv_data
        playlist.update_sections()

        toontje_hoger_4_absolute = ToontjeHoger4Absolute()
        self.assertEqual(
            toontje_hoger_4_absolute.validate_playlist(playlist),
            [
                'Groups in playlist sections should be sequential and unique from 1 to 6. E.g. [1, 2, 3, 4, 5, 6]'
            ]
        )
