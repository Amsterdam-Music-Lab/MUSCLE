from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class RhythmDiscriminationTest(TestCase):
    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.playlist = Playlist.objects.get(name='RhythmDiscrimination')
        cls.playlist._update_sections()
        cls.block = Block.objects.get(slug="rhdis")
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
            playlist=cls.playlist
        )

    def test_next_trial_actions(self):
        rules = self.block.get_rules()
        rules.plan_stimuli(self.session)
        self.session.save_json_data({"practice_done": True})
        trial = rules.get_next_trial(self.session)
        assert trial
