from django.test import TestCase

from experiment.actions.utils import get_current_experiment_url, randomize_playhead
from experiment.models import Block, Experiment, Phase
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestActions(TestCase):

    def setUp(self) -> None:
        self.playlist = Playlist.objects.create(name='TestPlaylist')
        self.participant = Participant.objects.create()
        self.experiment = Experiment.objects.create(slug="utils_test")
        phase = Phase.objects.create(experiment=self.experiment)
        self.block = Block.objects.create(phase=phase, slug="TestBlock")
        self.session = Session.objects.create(
            block=self.block, participant=self.participant, playlist=self.playlist)

    def test_get_current_experiment_url(self):
        self.assertEqual(get_current_experiment_url(self.session), "/utils_test")
        self.participant.participant_id_url = 'participant42'
        self.assertEqual(
            get_current_experiment_url(self.session),
            "/utils_test?participant_id=participant42",
        )

    def test_get_current_experiment_url_replayable(self):
        new_session = Session.objects.create(
            block=self.block, participant=Participant.objects.create()
        )
        new_session.finish()
        self.assertIsNone(get_current_experiment_url(self.session))
        self.experiment.replayable = True
        self.experiment.save()
        self.assertEqual(get_current_experiment_url(new_session), "/utils_test")

    def test_randomize_playhead(self):
        min_jitter = 5
        max_jitter = 10
        unjittered_playhead = randomize_playhead(min_jitter, max_jitter, True)
        assert unjittered_playhead == 0
        jittered_playhead = randomize_playhead(min_jitter, max_jitter, False)
        assert jittered_playhead >= min_jitter
