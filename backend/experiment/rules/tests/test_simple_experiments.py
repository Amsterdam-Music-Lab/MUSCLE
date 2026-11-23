from django.test import TestCase

from experiment.models import Block, Experiment, Phase
from participant.models import Participant
from section.models import Playlist
from session.models import Session

class TestSimpleBlockExperiment(TestCase):
    fixtures = [
        "choice_lists",
        "demographics",
        "questions_china",
        "goldsmiths_msi",
        "musical_preferences",
        "simple_experiments",
    ]

    @classmethod
    def setUpTestData(cls):
        playlist = Playlist.objects.get(name="MusicalPreferences")
        playlist._update_sections()
        block = Block.objects.get(identifier="simple_block")
        cls.session = Session.objects.create(participant=Participant.objects.create(), block=block, playlist=playlist)

    def test_get_trial(self):
        rules = self.session.block_rules()
        n_rounds = self.session.playlist.session_set.count()
        trial = rules.get_trial(self.session, n_rounds)
        self.assertIsNotNone(trial)
