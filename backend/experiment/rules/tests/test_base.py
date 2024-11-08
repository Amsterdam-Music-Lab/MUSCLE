from django.test import TestCase
from django.conf import settings
from experiment.models import Experiment, Phase, Block, ExperimentTranslatedContent, SocialMediaConfig
from session.models import Session
from participant.models import Participant
from section.models import Playlist
from ..base import Base


class BaseTest(TestCase):

    def test_get_play_again_url(self):
        block = Block.objects.create(
            slug="music-lab",
        )
        session = Session.objects.create(
            block=block,
            participant=Participant.objects.create(),
        )
        base = Base()
        play_again_url = base.get_play_again_url(session)
        self.assertEqual(play_again_url, "/music-lab")

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
        base = Base()
        play_again_url = base.get_play_again_url(session)
        self.assertEqual(play_again_url, "/music-lab?participant_id=42")

    def test_validate_playlist(self):
        base = Base()
        playlist = None
        errors = base.validate_playlist(playlist)
        self.assertEqual(errors, ["The block must have a playlist."])

        playlist = Playlist.objects.create()
        errors = base.validate_playlist(playlist)
        self.assertEqual(errors, ["The block must have at least one section."])
