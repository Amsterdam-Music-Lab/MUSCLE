from django.test import TestCase

from experiment.models import Experiment, ExperimentCollection, Phase, GroupedExperiment
from experiment.actions.utils import COLLECTION_KEY
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
            slug='testviews',
            rules='RHYTHM_BATTERY_INTRO'
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

    def test_next_round(self):
        session = Session.objects.create(
            experiment=self.experiment, participant=self.participant)
        response = self.client.get(
            f'/session/{session.id}/next_round/')
        assert response

    def test_next_round_with_collection(self):
        slug = 'mycollection'
        collection = ExperimentCollection.objects.create(slug=slug)
        request_session = self.client.session
        request_session[COLLECTION_KEY] = slug
        request_session.save()
        session = Session.objects.create(
            experiment=self.experiment, participant=self.participant)
        response = self.client.get(
            f'/session/{session.id}/next_round/')
        assert response
        changed_session = Session.objects.get(pk=session.pk)
        assert changed_session.load_json_data().get(COLLECTION_KEY) is None
        phase = Phase.objects.create(series=collection)
        GroupedExperiment.objects.create(
            phase=phase, experiment=self.experiment)
        response = self.client.get(
            f'/session/{session.id}/next_round/')
        changed_session = Session.objects.get(pk=session.pk)
        assert changed_session.load_json_data().get(COLLECTION_KEY) == slug
