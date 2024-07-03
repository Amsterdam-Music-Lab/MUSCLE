from django.test import TestCase

from experiment.models import Block
from experiment.rules.rhythm_discrimination import next_trial_actions, plan_stimuli
from participant.models import Participant
from result.models import Result
from section.models import Playlist
from session.models import Session


class RhythmDiscriminationTest(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name='RhythmDiscrimination')
        cls.playlist.update_sections()
        cls.block = Block.objects.get(name='RhythmDiscrimination')
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=cls.playlist
        )

    def test_next_trial_actions(self):
        plan_stimuli(self.session)
        self.session.final_score = 1
        self.session.save()
        trial = next_trial_actions(self.session, 6)
        assert trial
