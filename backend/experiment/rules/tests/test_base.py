from datetime import datetime

from django.test import TestCase

from experiment.models import Block
from session.models import Session
from participant.models import Participant
from section.models import Playlist
from ..base import BaseRules


class BaseRulesTest(TestCase):
    def test_get_play_again_url(self):
        block = Block.objects.create(
            slug="music-lab",
        )
        session = Session.objects.create(
            block=block,
            participant=Participant.objects.create(),
        )
        base = BaseRules()
        play_again_url = base.get_play_again_url(session)
        self.assertEqual(play_again_url, "/block/music-lab")

    def test_get_play_again_url_with_participant_id(self):
        block = Block.objects.create(
            slug="music-lab",
        )
        participant = Participant.objects.create(
            participant_id_url="42",
        )
        session = Session.objects.create(
            block=block,
            participant=participant,
        )
        base = BaseRules()
        play_again_url = base.get_play_again_url(session)
        self.assertEqual(play_again_url, "/block/music-lab?participant_id=42")

    def test_validate_playlist(self):
        base = BaseRules()
        playlist = None
        errors = base.validate_playlist(playlist)
        self.assertEqual(errors, ["The block must have a playlist."])

        playlist = Playlist.objects.create()
        errors = base.validate_playlist(playlist)
        self.assertEqual(errors, ["The block must have at least one section."])

    def test_has_played_before(self):
        base = BaseRules()
        block = Block.objects.create(slug="music-lab")
        participant = Participant.objects.create()
        session = Session.objects.create(block=block, participant=participant)
        self.assertFalse(base.has_played_before(session))
        session.finished_at = datetime.now()
        session.save()
        self.assertTrue(base.has_played_before(session))
