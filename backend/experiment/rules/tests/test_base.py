from django.test import TestCase
from experiment.models import Block
from session.models import Session
from participant.models import Participant
from section.models import Playlist
from ..base import BaseRules


class BaseRulesTest(TestCase):

    def test_validate_playlist(self):
        base = BaseRules()
        playlist = None
        errors = base.validate_playlist(playlist)
        self.assertEqual(errors, ["The block must have a playlist."])

        playlist = Playlist.objects.create()
        errors = base.validate_playlist(playlist)
        self.assertEqual(errors, ["The block must have at least one section."])
