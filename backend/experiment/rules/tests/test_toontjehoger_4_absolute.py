from unittest.mock import patch

from django.test import TestCase

from experiment.models import Block, Phase
from participant.models import Participant
from section.models import Playlist
from session.models import Session

from experiment.rules.toontjehoger_4_absolute import ToontjeHoger4Absolute


class TestToontjeHoger4Absolute(TestCase):
    fixtures = ["toontjehoger"]

    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.get(name="Toontje Hoger 4 - Absolute")
        cls.playlist._update_sections()

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
        toontje_hoger_4_absolute = ToontjeHoger4Absolute()
        self.assertEqual(toontje_hoger_4_absolute.validate_playlist(self.playlist), [])

    def test_validate_insufficient_groups(self):
        csv_data = (
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-1.mp3,a,1\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-2.mp3,b,1\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-3.mp3,c,1\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-4.mp3,a,2\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-5.mp3,b,2\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-6.mp3,c,2\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-7.mp3,a,3\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-8.mp3,b,3\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-9.mp3,c,3\n"
        )
        playlist = Playlist.objects.create(name='TestToontjeHoger4Absolute')
        playlist.csv = csv_data
        playlist._update_sections()

        toontje_hoger_4_absolute = ToontjeHoger4Absolute()

        self.assertEqual(
            toontje_hoger_4_absolute.validate_playlist(playlist),
            [
                "There should be at least 5 distinct groups in the playlist. This playlist has only 3 groups"
            ],
        )

    def test_validate_invalid_tags(self):
        csv_data = (
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-1.mp3,a,1\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-2.mp3,d,1\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-3.mp3,c,1\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-4.mp3,a,2\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-5.mp3,e,2\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-6.mp3,c,2\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-7.mp3,a,3\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-8.mp3,b,3\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-9.mp3,c,3\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-10.mp3,a,4\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-11.mp3,b,4\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-10.mp3,c,4\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-11.mp3,a,5\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-10.mp3,b,5\n"
            "Test,Test,7.046,45.0,ToontjeHoger4Absolute/audio-11.mp3,c,5\n"
        )
        playlist = Playlist.objects.create(name='TestToontjeHoger4Absolute')
        playlist.csv = csv_data
        playlist._update_sections()

        toontje_hoger_4_absolute = ToontjeHoger4Absolute()

        self.assertEqual(
            toontje_hoger_4_absolute.validate_playlist(playlist),
            [
                "Tags for each group should be 'a', 'b' or 'c'. Group 1 has tags: ['a', 'c', 'd']",
                "Tags for each group should be 'a', 'b' or 'c'. Group 2 has tags: ['a', 'c', 'e']",
            ],
        )

    def test_can_play_through(self):
        block = Block.objects.get(identifier="th_absolute")
        session = Session.objects.create(
            block=block,
            participant=Participant.objects.create(),
            playlist=self.playlist,
        )
        rules = block.get_rules()
        for round in range(block.rounds):
            self.assertIsNotNone(rules.next_round(session))
