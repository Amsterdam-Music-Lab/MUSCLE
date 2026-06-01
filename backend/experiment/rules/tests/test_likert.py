from django.test import TestCase

from experiment.models import Block, Experiment, Phase
from participant.models import Participant
from section.models import Playlist
from session.models import Session

class TestLikertExperiment(TestCase):
    fixtures = ["playlist"]

    @classmethod
    def setUpTestData(cls):
        exp = Experiment.objects.create(slug="likert_test")
        phase = Phase.objects.create(experiment=exp)
        playlist = Playlist.objects.get(name="MusicalPreferences")
        playlist._update_sections()
        block = Block.objects.create(slug="likert_test", phase=phase, rules="LIKERT_EXPERIMENT")
        cls.session = Session.objects.create(participant=Participant.objects.create(), block=block, playlist=playlist)
    
    def test_get_trial(self):
        rules = self.session.block_rules()
        n_rounds = self.session.playlist.session_set.count()
        trial = rules.get_trial(self.session, n_rounds)
        self.assertIsNotNone(trial)
