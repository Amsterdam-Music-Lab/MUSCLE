from django.test import TestCase

from experiment.actions import Trial
from experiment.models import Block
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestMatchingPairsVariants(TestCase):

    def setUp(self):
        section_csv = (
            "default,Crown_1_E1,0.0,10.0,MatchingPairs/Original/Crown_1_E1.mp3,Original,6\n"
            "default,Crown_1_E1,0.0,10.0,MatchingPairs/1stDegradation/Crown_1_E1.mp3,1stDegradation,6\n"
            "default,ER_2_E1,0.0,10.0,MatchingPairs/Original/ER_2_E1.mp3,Original,21\n"
            "default,ER_2_E1,0.0,10.0,MatchingPairs/1stDegradation/ER_2_E1.mp3,1stDegradation,21\n"
            "default,GameOfThrones_1_E1,0.0,10.0,MatchingPairs/Original/GameOfThrones_1_E1.mp3,Original,26\n"
            "default,GameOfThrones_1_E1,0.0,10.0,MatchingPairs/1stDegradation/GameOfThrones_1_E1.mp3,1stDegradation,26\n"
            "default,RickandMorty_12_E1,0.0,10.0,MatchingPairs/Original/RickandMorty_12_E1.mp3,Original,44\n"
            "default,RickandMorty_12_E1,0.0,10.0,MatchingPairs/1stDegradation/RickandMorty_12_E1.mp3,1stDegradation,44\n"
            "default,TwinPeaks_0_E1,0.0,10.0,MatchingPairs/1stDegradation/TwinPeaks_0_E1.mp3,1stDegradation,86\n"
            "default,TwinPeaks_1_E1,0.0,10.0,MatchingPairs/Original/TwinPeaks_1_E1.mp3,Original,86\n"
        )
        self.playlist = Playlist.objects.create(name='TestMatchingPairs')
        self.playlist.csv = section_csv
        self.playlist._update_sections()
        self.participant = Participant.objects.create()

    def test_lite_version(self):
        block = Block.objects.create(
            rules='MATCHING_PAIRS_LITE', slug='mpairs_lite'
        )
        session = Session.objects.create(
            block=block,
            participant=self.participant,
            playlist=self.playlist
        )
        first_trial = session.block_rules().get_matching_pairs_trial(session)
        another_session = Session.objects.create(
            block=block,
            participant=self.participant,
            playlist=self.playlist
        )
        second_trial = another_session.block_rules(
        ).get_matching_pairs_trial(another_session)
        assert isinstance(first_trial, Trial)
        assert isinstance(second_trial, Trial)
        assert first_trial.playback.sections != second_trial.playback.sections

    def test_fixed_order_sections(self):
        block = Block.objects.create(
            rules='MATCHING_PAIRS_FIXED', slug='mpairs_fixed')
        session = Session.objects.create(
            block=block,
            participant=self.participant,
            playlist=self.playlist
        )
        first_trial = session.block_rules().get_matching_pairs_trial(session)
        another_session = Session.objects.create(
            block=block,
            participant=self.participant,
            playlist=self.playlist
        )
        second_trial = another_session.block_rules(
        ).get_matching_pairs_trial(another_session)
        assert isinstance(first_trial, Trial)
        assert isinstance(second_trial, Trial)
        assert first_trial.playback.sections == second_trial.playback.sections

    def test_visual_matching_pairs(self):
        section_csv = (
            "owner,George,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTUyNjE0NzAzMl5BMl5BanBnXkFtZTYwMjQzMzU3._V1_FMjpg_UX1000_.jpg,vmp,3\n"
            "owner,George,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTUyNjE0NzAzMl5BMl5BanBnXkFtZTYwMjQzMzU3._V1_FMjpg_UX1000_.jpg,vmp,3\n"
            "owner,John,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTYwMDE4MzgzMF5BMl5BanBnXkFtZTYwMDQzMzU3._V1_FMjpg_UX1000_.jpg,vmp,1\n"
            "owner,John,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTYwMDE4MzgzMF5BMl5BanBnXkFtZTYwMDQzMzU3._V1_FMjpg_UX1000_.jpg,vmp,1\n"
            "owner,Paul,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTkyNTY0MzUxOV5BMl5BanBnXkFtZTYwNTQzMzU3._V1_.jpg,vmp,2\n"
            "owner,Paul,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTkyNTY0MzUxOV5BMl5BanBnXkFtZTYwNTQzMzU3._V1_.jpg,vmp,2\n"
            "owner,Ringo,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTU1NjY5NTY4N15BMl5BanBnXkFtZTYwNzQzMzU3._V1_.jpg,vmp,4\n"
            "owner,Ringo,0.0,1.0,https://m.media-amazon.com/images/M/MV5BMTU1NjY5NTY4N15BMl5BanBnXkFtZTYwNzQzMzU3._V1_.jpg,vmp,4\n"
        )
        playlist = Playlist.objects.create(name='TestVisualMatchingPairs')
        playlist.csv = section_csv
        playlist._update_sections()

        block = Block.objects.create(rules='MATCHING_PAIRS_LITE', slug='vmpairs', rounds=3)

        session = Session.objects.create(
            block=block,
            participant=self.participant,
            playlist=playlist
        )

        rules = session.block_rules()
        trial = rules.get_matching_pairs_trial(session)
        self.assertIsInstance(trial, Trial)
        self.assertEqual(trial.playback.play_method, 'NOAUDIO')
