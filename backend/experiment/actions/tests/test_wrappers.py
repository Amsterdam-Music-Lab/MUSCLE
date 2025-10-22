from django.test import TestCase
from unittest import mock

from experiment.actions.trial import Trial
from experiment.actions.wrappers import song_sync
from experiment.models import Block
from participant.models import Participant
from section.models import Playlist, Section
from session.models import Session


class ActionWrappersTest(TestCase):

    def setUp(self):
        self.playlist = Playlist.objects.create(name='TestPlaylist')
        self.participant = Participant.objects.create()
        self.section = Section.objects.create(
            filename='some/audio/file.mp3', playlist=self.playlist)
        self.block = Block.objects.create(slug="test-block")
        self.session = Session.objects.create(
            block=self.block, participant=self.participant, playlist=self.playlist)

    def test_song_sync(self):
        actions = song_sync(self.session, self.section, 'HookedTest')
        assert len(actions) == 3
        for action in actions:
            assert isinstance(action, Trial)

    @mock.patch("random.choice")
    def test_song_sync_no_jitter(self, mock_random_choice):
        mock_random_choice.return_value = True
        song_sync(self.session, self.section, 'HookedTest')
        inspect_session = Session.objects.first()
        saved_jitter = inspect_session.last_result().json_data.get(
            "continuation_offset"
        )
        assert saved_jitter == 0

    @mock.patch("random.choice")
    def test_song_sync_with_jitter(self, mock_random_choice):
        mock_random_choice.return_value = False
        song_sync(self.session, self.section, 'HookedTest')
        inspect_session = Session.objects.first()
        saved_jitter = inspect_session.last_result().json_data.get(
            "continuation_offset"
        )
        assert saved_jitter != 0
