from django.test import TestCase

from experiment.models import Block, Experiment, Phase
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class SessionViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        experiment = Experiment.objects.create(slug='myexperiment')
        phase = Phase.objects.create(experiment=experiment)
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.playlist1 = Playlist.objects.create(name="First Playlist")
        cls.playlist2 = Playlist.objects.create(name="Second Playlist")
        cls.block = Block.objects.create(
            phase=phase, slug="testviews", rules="RHYTHM_BATTERY_INTRO"
        )
        cls.block.playlists.add(cls.playlist1, cls.playlist2)

    def setUp(self):
        session = self.client.session
        session["participant_id"] = self.participant.id
        session.save()

    def test_next_round(self):
        session = Session.objects.create(block=self.block, participant=self.participant)
        response = self.client.get(f"/session/{session.id}/next_round/")
        assert response

    def test_next_round_with_experiment(self):
        session = Session.objects.create(block=self.block, participant=self.participant)
        response = self.client.get(f"/session/{session.id}/next_round/")
        self.assertIsNotNone(response)
