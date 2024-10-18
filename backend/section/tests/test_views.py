from django.conf import settings
from django.http import FileResponse
from django.test import override_settings, TestCase

from section.models import Playlist, Section


@override_settings(TESTING=True)
class SectionViewTest(TestCase):

    def setUp(self) -> None:
        self.playlist = Playlist.objects.create(name="TestPlaylist")

    @override_settings(DEBUG=True)
    def test_get_section_development(self):
        section = Section.objects.create(playlist=self.playlist, filename="example.mp3")
        response = self.client.get(f"/section/{section.id}/")
        # need to fetch the updated Section object in order to get the updated play_count
        self.assertEqual(Section.objects.get(pk=section.id).play_count, 1)
        self.assertEqual(type(response), FileResponse)

    @override_settings(DEBUG=True)
    def test_get_section_remote(self):
        section = Section.objects.create(
            playlist=self.playlist,
            filename="http://some/imaginary/audio.mp3",
        )
        response = self.client.get(f"/section/{section.id}/")
        self.assertEqual(response.status_code, 302)
        assert response.url.startswith("http://some/")

    @override_settings(DEBUG=True)
    def test_get_section_with_url_prefix(self):
        playlist = Playlist.objects.create(
            name="AnotherTestPlaylist", url_prefix="https://another/path/"
        )
        section = Section.objects.create(
            playlist=playlist,
            filename="audio.mp3",
        )
        response = self.client.get(f"/section/{section.id}/")
        self.assertEqual(response.status_code, 302)
        assert response.url.startswith("https://another")

    def test_get_section_production(self):
        section = Section.objects.create(playlist=self.playlist, filename="example.mp3")
        response = self.client.get(f"/section/{section.id}/")
        self.assertEqual(response.status_code, 302)
        assert response.url.startswith(settings.MEDIA_URL)

    def test_get_unknown_section(self):
        response = self.client.get("/section/12345/12345/")
        self.assertEqual(response.status_code, 404)
