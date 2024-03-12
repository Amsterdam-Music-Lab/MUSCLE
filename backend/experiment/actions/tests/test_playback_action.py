from django.test import TestCase

from experiment.actions.playback import determine_play_method, PLAY_BUFFER, PLAY_EXTERNAL,  PLAY_HTML, PLAY_NOAUDIO
from section.models import Playlist, Section


class PlaybackActionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.create(name='TestPlaylist')

    def test_determine_play_method(self):
        section = Section.objects.create(
            filename='some/audio/file.mp3', playlist=self.playlist)
        assert determine_play_method(section) == PLAY_BUFFER
        section.duration = 50
        assert determine_play_method(section) == PLAY_HTML
        section = Section.objects.create(
            filename='http://example.com/some/audio/file.mp3', playlist=self.playlist)
        assert determine_play_method(section) == PLAY_EXTERNAL
        section = Section.objects.create(
            filename='some/other/file.jpg', playlist=self.playlist)
        assert determine_play_method(section) == PLAY_NOAUDIO
