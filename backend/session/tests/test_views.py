from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class SessionViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.playlist1 = Playlist.objects.create(name='First Playlist')
        cls.playlist2 = Playlist.objects.create(name='Second Playlist')
        cls.experiment = Experiment.objects.create(
            name='TestViews',
            slug='testviews'
        )
        cls.experiment.playlists.add(
            cls.playlist1, cls.playlist2
        )

    def setUp(self):
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()

    def test_create_with_playlist(self):
        request = {
            "experiment_id": self.experiment.id,
            "playlist_id": self.playlist2.id
        }
        self.client.post('/session/create/', request)
        new_session = Session.objects.get(
            experiment=self.experiment, participant=self.participant)
        assert new_session
        assert new_session.playlist == self.playlist2

    def test_create_without_playlist(self):
        request = {
            "experiment_id": self.experiment.id
        }
        self.client.post('/session/create/', request)
        new_session = Session.objects.get(
            experiment=self.experiment, participant=self.participant)
        assert new_session
        assert new_session.playlist == self.playlist1
