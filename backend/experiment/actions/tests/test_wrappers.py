from django.test import TestCase
from unittest import mock

from experiment.actions import Trial
from experiment.actions.wrappers import song_sync
from experiment.models import Experiment
from participant.models import Participant
from section.models import Playlist, Section
from session.models import Session


class ActionWrappersTest(TestCase):
    def setUp(self):
        self.playlist = Playlist.objects.create(name='TestPlaylist')
        self.participant = Participant.objects.create()
        self.section = Section.objects.create(
            filename='some/audio/file.mp3', playlist=self.playlist)
        self.experiment = Experiment.objects.create(name='TestExperiment')
        self.session = Session.objects.create(
            experiment=self.experiment, participant=self.participant, playlist=self.playlist)

    def test_song_sync(self):
        actions = song_sync(self.session, self.section, 'HookedTest')
        assert len(actions) == 3
        for action in actions:
            assert isinstance(action, Trial)

    @mock.patch("random.randint")
    def test_song_sync_no_jitter(self, mock_randint):
        mock_randint.return_value = 1
        song_sync(self.session, self.section, 'HookedTest')
        inspect_session = Session.objects.first()
        saved_jitter = inspect_session.load_json_data().get('continuation_offset')
        assert saved_jitter == 0

    @mock.patch("random.randint")
    def test_song_sync_with_jitter(self, mock_randint):
        mock_randint.return_value = 0
        song_sync(self.session, self.section, 'HookedTest')
        inspect_session = Session.objects.first()
        saved_jitter = inspect_session.load_json_data().get('continuation_offset')
        assert saved_jitter != 0
