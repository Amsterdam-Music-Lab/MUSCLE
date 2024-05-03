from django.test import TestCase
from django.conf import settings
from experiment.models import Experiment
from section.models import Playlist
from ..base import Base


class BaseTest(TestCase):

    def test_social_media_info(self):
        reload_participant_target = settings.RELOAD_PARTICIPANT_TARGET
        slug = 'music-lab'
        experiment = Experiment.objects.create(
            name='Music Lab',
            slug=slug,
        )
        base = Base()
        social_media_info = base.social_media_info(
            experiment=experiment,
            score=100,
        )

        expected_url = f"{reload_participant_target}/{slug}"

        self.assertEqual(social_media_info['apps'], ['facebook', 'twitter'])
        self.assertEqual(social_media_info['message'], 'I scored 100 points on https://app.amsterdammusiclab.nl/music-lab')
        self.assertEqual(social_media_info['url'], expected_url)
        # Check for double slashes
        self.assertNotIn(social_media_info['url'], '//')
        self.assertEqual(social_media_info['hashtags'], ['music-lab', 'amsterdammusiclab', 'citizenscience'])

    def test_validate_playlist(self):
        base = Base()
        playlist = None
        errors = base.validate_playlist(playlist)
        self.assertEqual(errors, ['The experiment must have a playlist.'])

        playlist = Playlist()
        errors = base.validate_playlist(playlist)
        self.assertEqual(errors, ['The experiment must have at least one section.'])