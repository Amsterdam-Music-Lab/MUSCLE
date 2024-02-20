from django.test import TestCase

from experiment.models import Experiment
from experiment.rules import VisualMatchingPairsGame
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class VisualMatchingPairsTest(TestCase):

    @classmethod
    def setUpTestData(self):
        section_csv = (
            "owner,George,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTUyNjE0NzAzMl5BMl5BanBnXkFtZTYwMjQzMzU3._V1_FMjpg_UX1000_.jpg,	vmp,	3\n"
            "owner,George,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTUyNjE0NzAzMl5BMl5BanBnXkFtZTYwMjQzMzU3._V1_FMjpg_UX1000_.jpg,	vmp,	3\n"
            "owner,John,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTYwMDE4MzgzMF5BMl5BanBnXkFtZTYwMDQzMzU3._V1_FMjpg_UX1000_.jpg,	vmp,	1\n"
            "owner,John,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTYwMDE4MzgzMF5BMl5BanBnXkFtZTYwMDQzMzU3._V1_FMjpg_UX1000_.jpg,	vmp,	1\n"
            "owner,Paul,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTkyNTY0MzUxOV5BMl5BanBnXkFtZTYwNTQzMzU3._V1_.jpg,	vmp,	2\n"
            "owner,Paul,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTkyNTY0MzUxOV5BMl5BanBnXkFtZTYwNTQzMzU3._V1_.jpg,	vmp,	2\n"
            "owner,Ringo,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTU1NjY5NTY4N15BMl5BanBnXkFtZTYwNzQzMzU3._V1_.jpg,	vmp,	4\n"
            "owner,Ringo,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTU1NjY5NTY4N15BMl5BanBnXkFtZTYwNzQzMzU3._V1_.jpg,	vmp,	4\n"
        )
        self.playlist = Playlist.objects.create(name='TestVisualMatchingPairs')
        self.playlist.csv = section_csv
        self.playlist.update_sections()

        self.sections = list(self.playlist.section_set.filter(tag__contains='vmp'))

        self.participant = Participant.objects.create()
        self.experiment = Experiment.objects.create(rules='VISUAL_MATCHING_PAIRS', slug='vmpairs', rounds=3)

        self.session = Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            playlist=self.playlist
        )
        self.rules = VisualMatchingPairsGame()

    def test_visual_matching_pairs_trial(self):
        trial = self.rules.get_matching_pairs_trial(self.session)
        self.assertIsNotNone(trial)
        self.assertEqual(trial.title, 'Visual Tune twins')
        self.assertIsNotNone(trial.playback)
        self.assertEqual(trial.playback.ID, 'VISUALMATCHINGPAIRS')

    def test_next_round_logic(self):
        self.session.increment_round()
        next_round = self.rules.next_round(self.session)
        self.assertEqual(len(next_round), 1)
        self.assertEqual(next_round[0].title, 'Visual Tune twins')