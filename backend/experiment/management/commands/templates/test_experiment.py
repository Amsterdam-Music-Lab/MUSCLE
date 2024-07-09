from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class NewBlockRulesetTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.participant = Participant.objects.create()
        self.playlist = Playlist.objects.create(name='NewBlockRuleset')
        self.block = Block.objects.create(name='NewBlockRuleset', rounds=5)
        self.session = Session.objects.create(
            block=self.block,
            participant=self.participant,
            playlist=self.playlist
        )

    def test_initializes_correctly(self):
        assert self.block.name == 'NewBlockRuleset'
