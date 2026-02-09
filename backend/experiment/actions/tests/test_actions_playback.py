from django.test import TestCase

from experiment.actions.playback import Autoplay, get_play_method, PLAY_BUFFER, PLAY_EXTERNAL, PLAY_HTML, PLAY_NOAUDIO, PlaybackSection, PlayButtons, TYPE_AUTOPLAY, TYPE_BUTTON
from section.models import Playlist, Section

class PlaybackActionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.playlist = Playlist.objects.create(name='TestPlaylist')
        cls.section = Section.objects.create(
            filename="testing.mp3", playlist=cls.playlist)
    
    def test_autoplay(self):
        autoplay = Autoplay(sections=[PlaybackSection(self.section)]).action()
        self.assertEqual(autoplay.get('sections')[0].get('link'), self.section.absolute_url())
        self.assertEqual(autoplay.get('view'), TYPE_AUTOPLAY)
    
    def test_play_buttons(self):
        play_buttons = PlayButtons(sections=[PlaybackSection(self.section)]).action()
        self.assertEqual(play_buttons.get('sections')[0].get('link'), self.section.absolute_url())
        self.assertEqual(play_buttons.get('view'), TYPE_BUTTON)

    def test_get_play_method(self):
        section = Section.objects.create(
            filename='some/audio/file.mp3', playlist=self.playlist)
        assert get_play_method(section) == PLAY_BUFFER
        section.duration = 50
        assert get_play_method(section) == PLAY_HTML
        section = Section.objects.create(
            filename='http://example.com/some/audio/file.mp3', playlist=self.playlist)
        assert get_play_method(section) == PLAY_EXTERNAL
        section = Section.objects.create(
            filename='some/other/file.jpg', playlist=self.playlist)
        assert get_play_method(section) == PLAY_NOAUDIO
