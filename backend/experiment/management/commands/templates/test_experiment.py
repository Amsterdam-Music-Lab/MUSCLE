from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class NewExperimentRulesetTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.participant = Participant.objects.create()
        self.playlist = Playlist.objects.create(name='NewExperimentRuleset')
        self.experiment = Experiment.objects.create(name='NewExperimentRuleset', rounds=5)
        self.session = Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            playlist=self.playlist
        )

    def test_initializes_correctly(self):
        assert self.experiment.name == 'NewExperimentRuleset'