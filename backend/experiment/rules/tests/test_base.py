from django.test import TestCase
from django.conf import settings
from experiment.models import Experiment, Phase, Block, SocialMediaConfig
from session.models import Session
from participant.models import Participant
from section.models import Playlist
from ..base import Base


class BaseTest(TestCase):
    def test_social_media_info(self):
        reload_participant_target = settings.RELOAD_PARTICIPANT_TARGET
        slug = "music-lab"
        experiment = Experiment.objects.create(
            slug=slug,
        )
        SocialMediaConfig.objects.create(
            experiment=experiment,
            url="https://app.amsterdammusiclab.nl/music-lab",
            tags=["music-lab"],
        )
        phase = Phase.objects.create(
            experiment=experiment,
        )
        block = Block.objects.create(
            name="Music Lab",
            slug=slug,
            phase=phase,
        )
        base = Base()
        social_media_info = base.social_media_info(
            block=block,
            score=100,
        )

        expected_url = f"{reload_participant_target}/{slug}"

        self.assertEqual(social_media_info["apps"], ["facebook", "twitter"])
        self.assertEqual(
            social_media_info["message"], "I scored 100 points on https://app.amsterdammusiclab.nl/music-lab"
        )
        self.assertEqual(social_media_info["url"], expected_url)
        # Check for double slashes
        self.assertNotIn(social_media_info["url"], "//")
        self.assertEqual(social_media_info["hashtags"], ["music-lab", "amsterdammusiclab", "citizenscience"])

    def test_get_play_again_url(self):
        block = Block.objects.create(
            name="Music Lab",
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
            name="Music Lab",
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
