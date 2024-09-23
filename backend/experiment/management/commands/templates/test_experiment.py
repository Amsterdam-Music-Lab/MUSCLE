from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class NewBlockRulesetTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.participant = Participant.objects.create()
        self.playlist = Playlist.objects.create(name="NewBlockPlaylist")
        self.block = Block.objects.create(slug="new_block", rounds=5)
        self.session = Session.objects.create(
            block=self.block,
            participant=self.participant,
            playlist=self.playlist
        )

    def test_initializes_correctly(self):
        assert self.block.slug == "new_block"
