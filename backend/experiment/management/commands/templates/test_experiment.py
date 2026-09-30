from django.test import TestCase

from experiment.models import Block, Phase
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class NewBlockRulesetTest(TestCase):
    fixtures = ["experiment_testing"]

    @classmethod
    def setUpTestData(self):
        self.participant = Participant.objects.create()
        self.playlist = Playlist.objects.create(name="NewBlockPlaylist")
        self.block = Block.objects.create(
            identifier="new_block", phase=Phase.objects.get(pk=4242), rounds=5
        )
        self.session = Session.objects.create(
            block=self.block,
            participant=self.participant,
            playlist=self.playlist
        )

    def test_initializes_correctly(self):
        assert self.block.identifier == "new_block"
