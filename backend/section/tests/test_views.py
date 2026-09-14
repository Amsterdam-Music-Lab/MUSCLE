import json

from django.conf import settings
from django.http import FileResponse, HttpResponseBadRequest
from django.test import override_settings, TestCase

from experiment.models import Block
from participant.models import Participant
from section.models import Playlist, Section
from session.models import Session


@override_settings(TESTING=True)
class GetSectionViewTest(TestCase):

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


class SetPlaylistViewTest(TestCase):
    fixtures = ["testing"]

    @classmethod
    def setUpTestData(cls):
        Playlist.objects.bulk_create(
            [Playlist(name=f"TestPlaylist-{n}") for n in range(3)]
        )
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.get(identifier='test-block')
        cls.playlist = Playlist.objects.first()
        cls.session = Session.objects.create(
            block=cls.block, participant=cls.participant
        )

    def test_set_playlist(self):
        request = {"session_id": self.session.id, "playlist_id": self.playlist.id}
        response = self.client.post("/section/set_playlist/", request)
        self.assertEqual(response.status_code, 200)

    def test_set_nonexisting_playlist(self):
        fake_playlist_id = sum(Playlist.objects.all().values_list("id", flat=True))
        request = {"session_id": self.session.id, "playlist_id": fake_playlist_id}
        response = self.client.post("/section/set_playlist/", request)
        self.assertEqual(response.status_code, 404)

    def test_set_playlist_to_nonexistent_session(self):
        request = {"session_id": self.session.id + 1, "playlist_id": self.playlist.id}
        response = self.client.post("/section/set_playlist/", request)
        self.assertEqual(response.status_code, 404)

    def test_set_playlist_incomplete_params(self):
        request = {"session_id": self.session.id + 1}
        response = self.client.post("/section/set_playlist/", request)
        self.assertIsInstance(response, HttpResponseBadRequest)
