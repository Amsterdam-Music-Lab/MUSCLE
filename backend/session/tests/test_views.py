from django.test import TestCase

from experiment.models import Block, Experiment, Phase
from experiment.actions.utils import EXPERIMENT_KEY
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class SessionViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.playlist1 = Playlist.objects.create(name="First Playlist")
        cls.playlist2 = Playlist.objects.create(name="Second Playlist")
        cls.block = Block.objects.create(slug="testviews", rules="RHYTHM_BATTERY_INTRO")
        cls.block.playlists.add(cls.playlist1, cls.playlist2)

    def setUp(self):
        session = self.client.session
        session["participant_id"] = self.participant.id
        session.save()

    def test_create_with_invalid_block(self):
        request = {}
        response = self.client.post("/session/create/", request)
        self.assertEqual(response.status_code, 400)
        request = {"block_id": self.block.id + 1}
        response = self.client.post("/session/create/", request)
        self.assertEqual(response.status_code, 404)

    def test_create_with_playlist(self):
        request = {"block_id": self.block.id, "playlist_id": self.playlist2.id + 1}
        response = self.client.post("/session/create/", request)
        self.assertEqual(response.status_code, 404)
        request = {"block_id": self.block.id, "playlist_id": self.playlist2.id}
        self.client.post("/session/create/", request)
        new_session = Session.objects.get(block=self.block, participant=self.participant)
        self.assertTrue(new_session)
        self.assertEqual(new_session.playlist, self.playlist2)

    def test_create_without_playlist(self):
        request = {"block_id": self.block.id}
        self.client.post("/session/create/", request)
        new_session = Session.objects.get(block=self.block, participant=self.participant)
        assert new_session
        assert new_session.playlist == self.playlist1

    def test_next_round(self):
        session = Session.objects.create(block=self.block, participant=self.participant)
        response = self.client.get(f"/session/{session.id}/next_round/")
        assert response

    def test_next_round_with_experiment(self):
        slug = "myexperiment"
        experiment = Experiment.objects.create(slug=slug)
        request_session = self.client.session
        request_session[EXPERIMENT_KEY] = slug
        request_session.save()
        session = Session.objects.create(block=self.block, participant=self.participant)
        response = self.client.get(f"/session/{session.id}/next_round/")
        assert response
        changed_session = Session.objects.get(pk=session.pk)
        assert changed_session.json_data.get(EXPERIMENT_KEY) is None
        phase = Phase.objects.create(experiment=experiment)
        self.block.phase = phase
        self.block.save()
        response = self.client.get(f"/session/{session.id}/next_round/")
        changed_session = Session.objects.get(pk=session.pk)
        assert changed_session.json_data.get(EXPERIMENT_KEY) == slug
