from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestMatchingPairsFixed(TestCase):

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
        self.playlist.update_sections()
        self.participant = Participant.objects.create()
        self.experiment = Experiment.objects.create(
            rules='MATCHING_PAIRS_FIXED', slug='mpairs_fixed')

    def test_fixed_order_sections(self):
        session = Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            playlist=self.playlist
        )
        first_run_sections = session.experiment_rules().select_sections(session)
        another_session = Session.objects.create(
            experiment=self.experiment,
            participant=self.participant,
            playlist=self.playlist
        )
        second_run_sections = another_session.experiment_rules().select_sections(another_session)
        assert first_run_sections == second_run_sections
