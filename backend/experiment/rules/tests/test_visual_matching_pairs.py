from django.test import TestCase

from experiment.models import Experiment
from experiment.rules import VisualMatchingPairs
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class VisualMatchingPairsTest(TestCase):

    @classmethod
    def setUpTestData(self):
        section_csv = (
            "owner,George,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTUyNjE0NzAzMl5BMl5BanBnXkFtZTYwMjQzMzU3._V1_FMjpg_UX1000_.jpg,0,	vmp,	3\n"
            "owner,George,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTUyNjE0NzAzMl5BMl5BanBnXkFtZTYwMjQzMzU3._V1_FMjpg_UX1000_.jpg,0,	vmp,	3\n"
            "owner,John,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTYwMDE4MzgzMF5BMl5BanBnXkFtZTYwMDQzMzU3._V1_FMjpg_UX1000_.jpg,0,	vmp,	1\n"
            "owner,John,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTYwMDE4MzgzMF5BMl5BanBnXkFtZTYwMDQzMzU3._V1_FMjpg_UX1000_.jpg,0,	vmp,	1\n"
            "owner,Paul,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTkyNTY0MzUxOV5BMl5BanBnXkFtZTYwNTQzMzU3._V1_.jpg,0,	vmp,	2\n"
            "owner,Paul,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTkyNTY0MzUxOV5BMl5BanBnXkFtZTYwNTQzMzU3._V1_.jpg,0,	vmp,	2\n"
            "owner,Ringo,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTU1NjY5NTY4N15BMl5BanBnXkFtZTYwNzQzMzU3._V1_.jpg,0,	vmp,	4\n"
            "owner,Ringo,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTU1NjY5NTY4N15BMl5BanBnXkFtZTYwNzQzMzU3._V1_.jpg,0,	vmp,	4\n"
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
        self.rules = VisualMatchingPairs()

    def test_visual_matching_pairs_trial(self):
        trial = self.rules.get_visual_matching_pairs_trial(self.session)
        self.assertIsNotNone(trial)
        self.assertEqual(trial.title, 'Visual Tune twins')
        self.assertIsNotNone(trial.playback)
        self.assertEqual(trial.playback.ID, 'VISUALMATCHINGPAIRS')

    def test_calculate_score(self):
        result = None
        data = {
            'result': {
                'moves': [
                    { "selectedSection": self.sections[1].id, "cardIndex": 1, "score": 0, "timestamp": 1 },
                    { "selectedSection": self.sections[6].id, "cardIndex": 6, "score": 0, "timestamp": 2 },
                    { "selectedSection": self.sections[7].id, "cardIndex": 5, "score": 0, "timestamp": 3 },
                    { "selectedSection": self.sections[6].id, "cardIndex": 6, "score": 20, "timestamp": 4 },
                    { "selectedSection": self.sections[2].id, "cardIndex": 2, "score": 0, "timestamp": 5 },
                    { "selectedSection": self.sections[5].id, "cardIndex": 7, "score": 0, "timestamp": 6 },
                    { "selectedSection": self.sections[3].id, "cardIndex": 3, "score": 0, "timestamp": 7 },
                    { "selectedSection": self.sections[4].id, "cardIndex": 2, "score": 20, "timestamp": 8 },
                    { "selectedSection": self.sections[5].id, "cardIndex": 7, "score": 0, "timestamp": 9 },
                    { "selectedSection": self.sections[0].id, "cardIndex": 4, "score": 0, "timestamp": 10 },
                    { "selectedSection": self.sections[0].id, "cardIndex": 4, "score": 0, "timestamp": 11 },
                    { "selectedSection": self.sections[1].id, "cardIndex": 1, "score": 20, "timestamp": 12 },
                    { "selectedSection": self.sections[5].id, "cardIndex": 7, "score": 0, "timestamp": 13 },
                    { "selectedSection": self.sections[4].id, "cardIndex": 0, "score": 10, "timestamp": 14 }
                ],
                'score': 10
            }
        }

        score = self.rules.calculate_score(result, data)
        self.assertEqual(score, 10)

    def test_next_round_logic(self):
        self.session.increment_round()
        next_round = self.rules.next_round(self.session)
        self.assertEqual(len(next_round), 1)
        self.assertEqual(next_round[0].title, 'Visual Tune twins')