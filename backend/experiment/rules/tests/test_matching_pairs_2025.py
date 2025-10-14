import random
from unittest import skip

from django.db.models import Avg
from django.test import TestCase

from experiment.models import Block, Experiment, Phase
from experiment.actions.final import Final
from participant.models import Participant
from result.models import Result
from section.models import Playlist, Song
from session.models import Session
from question.questions import create_default_questions


class MatchingPairs2025Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_default_questions()
        cls.playlist = Playlist.objects.create(name="TestMatchingPairs2025")
        cls.playlist.csv = cls.create_section_csv()
        cls.playlist._update_sections()
        cls.playlist.save()
        cls.participant = Participant.objects.create()
        cls.exp = Experiment.objects.create(slug="matching_pairs_2025")
        cls.phase = Phase.objects.create(experiment=cls.exp)
        cls.block = Block.objects.create(rules="MATCHING_PAIRS_2025", slug="mpairs-2025", rounds=42, phase=cls.phase)
        cls.session = Session.objects.create(block=cls.block, participant=cls.participant, playlist=cls.playlist)
        cls.rules = cls.session.block_rules()

    @staticmethod
    def create_section_csv():
        corpora = [{"name": "CH"}]
        stimuli = [
            {'artist': 'A', 'name': 'F1'},
            {'artist': 'A', 'name': 'F2'},
            {'artist': 'H', 'name': 'F11'},
            {'artist': 'H', 'name': 'F12'},
            {'artist': 'H', 'name': 'F13'},
            {'artist': 'H', 'name': 'F14'},
            {'artist': 'H', 'name': 'F18'},
            {'artist': 'H', 'name': 'F19'},
            {'artist': 'H', 'name': 'F1'},
            {'artist': 'H', 'name': 'F20'},
        ]
        conditions = [
            {"type": "O", "difficulties": ["0"]},
            {"type": "TD", "difficulties": ["1", "2", "3", "4", "5"]},
            {"type": "SD", "difficulties": ["1", "2", "3", "4", "5"]},
        ]

        section_csv = ""

        for corpus in corpora:
            for condition in conditions:
                for difficulty in condition["difficulties"]:
                    for stimulus in stimuli:
                        section_csv += (
                            f"{stimulus['artist']},{stimulus['name']},0.0,10.0,"
                            f"MatchingPairs2/{corpus['name']}/{condition['type']}/{stimulus['artist']}_{stimulus['name']}.mp3,"
                            f"{difficulty},{condition['type']}\n"
                        )
        return section_csv

    def create_fake_condition_results(
        self, n_results: int = 5, score: int = 1
    ) -> tuple[str, str]:
        conditions = random.sample(
            self.rules._get_possible_conditions(self.session), n_results
        )
        for cond in conditions:
            result, _created = Result.objects.get_or_create(
                participant=self.session.participant,
                question_key="condition",
                given_response=f"{cond[0]}_{cond[1]}",
            )
            result.score = score
            result.save()
        return conditions

    def test_select_condition_first_play(self):
        """Test that selecting a condition / difficulty pair works on first play"""
        condition, difficulty = (
            self.rules._select_least_played_condition_difficulty_pair(self.session)
        )
        self.assertIn(
            (condition, difficulty), self.rules._get_possible_conditions(self.session)
        )

    def test_select_condition_repeated_play(self):
        """Test that selecting a condition / difficulty pair works with repeated play"""
        played_conditions = self.create_fake_condition_results(10)
        condition, difficulty = condition, difficulty = (
            self.rules._select_least_played_condition_difficulty_pair(self.session)
        )
        self.assertNotIn((condition, difficulty), played_conditions)

    def test_select_condition_all_conditions_played(self):
        """Test that selecting a condition / difficulty pair works when all conditions have been played at least once"""
        self.create_fake_condition_results(11, 1)
        played_multiple = self.create_fake_condition_results(5, 2)
        condition, difficulty = condition, difficulty = (
            self.rules._select_least_played_condition_difficulty_pair(self.session)
        )
        self.assertNotIn((condition, difficulty), played_multiple)

    def create_fake_song_results(
        self, n_results: int = 5, score: float = 1
    ) -> list[int]:
        songs = Song.objects.all().values_list('id', flat=True)[:n_results]
        for song in songs:
            result, _created = Result.objects.get_or_create(
                participant=self.session.participant,
                question_key="song",
                given_response=song,
            )
            result.score = score
            result.save()
        return songs

    def test_select_sections_original_condition(self):
        """Test that _select_sections returns correct number of sections for original condition"""
        # Mock the condition selection to force "original" condition
        self.rules._select_least_played_condition_difficulty_pair = lambda x: (
            'O',
            '0',
        )

        sections = self.rules._select_sections(self.session)

        # Should return num_pairs * 2 sections (pairs are duplicated for original condition)
        self.assertEqual(len(sections), self.rules.num_pairs * 2)
        # All sections should have group "O" and tag "0"
        self.assertTrue(
            all(section.group == "O" and section.tag == '0' for section in sections)
        )

    def test_select_sections_temporal_condition(self):
        """Test that _select_sections returns correct sections for temporal condition with original pairs"""
        # Mock the condition selection to force "temporal" condition
        self.rules._select_least_played_condition_difficulty_pair = lambda x: (
            "TD",
            "1",
        )

        sections = self.rules._select_sections(self.session)

        # Should return num_pairs * 2 sections (temporal + matching original sections)
        self.assertEqual(len(sections), self.rules.num_pairs * 2)

        # Half should be temporal sections
        temporal_sections = [s for s in sections if s.group == "TD" and s.tag == "1"]
        self.assertEqual(len(temporal_sections), self.rules.num_pairs)

        # Half should be original sections
        original_sections = [s for s in sections if s.group == "O" and s.tag == "0"]
        self.assertEqual(len(original_sections), self.rules.num_pairs)

        # Temporal and original sections should have matching songs
        temporal_groups = {s.song for s in temporal_sections}
        original_groups = {s.song for s in original_sections}
        self.assertEqual(temporal_groups, original_groups)

    def test_select_sections_frequency_condition(self):
        """Test that _select_sections returns correct sections for frequency condition with original pairs"""
        # Mock the condition selection to force "frequency" condition
        self.rules._select_least_played_condition_difficulty_pair = lambda x: (
            "SD",
            "1",
        )

        sections = self.rules._select_sections(self.session)

        # Should return num_pairs * 2 sections (frequency + matching original sections)
        self.assertEqual(len(sections), self.rules.num_pairs * 2)

        # Half should be frequency sections
        frequency_sections = [s for s in sections if s.group == "SD" and s.tag == "1"]
        self.assertEqual(len(frequency_sections), self.rules.num_pairs)

        # Half should be original sections
        original_sections = [s for s in sections if s.group == "O" and s.tag == "0"]
        self.assertEqual(len(original_sections), self.rules.num_pairs)

        # Frequency and original sections should have matching group numbers
        frequency_groups = {s.song for s in frequency_sections}
        original_groups = {s.song for s in original_sections}
        self.assertEqual(frequency_groups, original_groups)

    def test_select_sections_unplayed(self):
        """test that we get preferably unplayed songs"""
        session = Session.objects.create(
            block=self.block, participant=self.participant, playlist=self.playlist
        )
        song_ids = self.create_fake_song_results(2, 1)
        sections = self.rules._select_sections(session)
        for section in sections:
            self.assertNotIn(section.song.id, song_ids)

    def test_select_sections_least_played(self):
        """Test that we get preferably the least played sections"""
        session = Session.objects.create(
            block=self.block, participant=self.participant, playlist=self.playlist
        )
        # fake that all songs have been played
        faked_plays = self.create_fake_song_results(10, 1)
        # fake that 5 songs have been played twice
        multiple_plays = self.create_fake_song_results(5, 2)
        single_plays = [p for p in faked_plays if p not in multiple_plays]
        song_ids = list(
            set([section.song.id for section in self.rules._select_sections(session)])
        )
        for m in single_plays:
            self.assertIn(m, song_ids)
        self.assertEqual(
            len(list(set(song_ids).intersection(set(multiple_plays)))),
            self.rules.num_pairs - len(single_plays),
        )

    def create_session(self, final_score, json_data):
        participant = Participant.objects.create()
        session = Session.objects.create(
            block=self.block,
            participant=participant,
            playlist=self.playlist,
            final_score=final_score,
            json_data=json_data,
        )
        return session

    def test_get_percentile_rank(self):
        json_data = {'condition': 'TD', 'difficulty': '4'}
        self.create_session(80, json_data)
        self.create_session(90, json_data)
        self.create_session(90, json_data)
        self.create_session(100, json_data)
        self.create_session(110, json_data)
        self.create_session(120, json_data)
        session = self.create_session(100, json_data)
        percentile = self.rules._get_percentile_rank(session)
        expected = (5 - 0.5 * 2) / 7 * 100  # 5 lower or equal, 2 equal, 7 total
        self.assertAlmostEqual(percentile, expected)

    def test_other_conditions_do_not_affect_percentile_rank(self):
        target_data = {'condition': 'TD', 'difficulty': '4'}
        self.create_session(80, target_data)
        self.create_session(100, target_data)
        self.create_session(120, target_data)
        session = self.create_session(110, target_data)
        self.create_session(20, {'condition': 'SD', 'difficulty': '2'})
        self.create_session(20, {'condition': 'SD', 'difficulty': '2'})
        percentile = self.rules._get_percentile_rank(session)
        expected = (3 - 0.5 * 1) / 4 * 100  #  3 lower or equal, 1 equal, 4 total
        self.assertEqual(percentile, expected)

    def test_has_played_before_returns_false(self):
        """Test that _has_played_before returns False when there are no previous results."""
        experiment = Experiment.objects.create(slug="dummy_experiment")
        phase = Phase.objects.create(experiment=experiment)

        session = Session.objects.create(block=self.block, participant=self.participant, playlist=self.playlist)
        session.block.phase = phase
        session.save()

        self.assertFalse(self.rules._has_played_before(session))

    def test_has_played_before_returns_true(self):
        """Test that _has_played_before returns True when a previous session has a result."""

        previous_session = Session.objects.create(
            block=self.block, participant=self.participant, playlist=self.playlist
        )
        Result.objects.create(session=previous_session)

        session = Session.objects.create(block=self.block, participant=self.participant, playlist=self.playlist)

        self.assertTrue(self.rules._has_played_before(session))

    def test_get_final_actions(self):
        mp_block = Block.objects.create(phase=self.phase, rules="MATCHING_PAIRS_2025", slug="mpairs-2025-2")
        session = Session.objects.create(participant=self.participant, block=mp_block, final_score=100)
        final_action = self.rules._get_final_actions(session)[0]
        self.assertIsInstance(final_action, Final)
        self.assertEqual(final_action.total_score, 100)

    def test_get_possible_conditions(self):
        possible_conditions = self.rules._get_possible_conditions(self.session)
        self.assertEqual(len(possible_conditions), 11)


@skip("This test simulates repeated playthroughs, comment this line out to run")
class PlaythroughSimulationTest(TestCase):
    fixtures = ['playlist']

    @classmethod
    def setUpTestData(cls):
        cls.exp = Experiment.objects.create(slug="matching_pairs_2025")
        cls.phase = Phase.objects.create(experiment=cls.exp)
        cls.ch_playlist = Playlist.objects.get(name="MP2.0 - CH")
        cls.ch_playlist._update_sections()
        cls.rc_playlist = Playlist.objects.get(name="MP2.0 - RC")
        cls.rc_playlist._update_sections()
        cls.tv_playlist = Playlist.objects.get(name="MP2.0 - TV")
        cls.tv_playlist._update_sections()
        cls.block = Block.objects.create(
            rules="MATCHING_PAIRS_2025", slug="mpairs-2025", rounds=1, phase=cls.phase
        )
        cls.participant = Participant.objects.create()
        cls.rules = cls.block.get_rules()

    def test_simulate_repeated_playthrough(self):
        n_games = 500
        for corpus in ['ch', 'rc', 'tv']:
            playlist = getattr(self, f'{corpus}_playlist')
            for game in range(n_games):
                session = Session.objects.create(
                    participant=self.participant,
                    block=self.block,
                    playlist=playlist,
                )
                actions = self.rules.next_round(session)
                self.assertNotEqual(len(actions), 0)
            song_results = Result.objects.filter(
                participant=self.participant, question_key='song'
            )
            average_plays = song_results.aggregate(Avg('score'))['score__avg']
            # check that all songs have been played equally frequently, give or take 1
            for song_result in song_results:
                self.assertAlmostEqual(song_result.score, average_plays, delta=1)
            song_results.delete()
            condition_results = Result.objects.filter(
                participant=self.participant, question_key='condition'
            )
            average_conditions = condition_results.aggregate(Avg('score'))['score__avg']
            # check that all conditions have been played equally frequently, give or take 1
            for condition_result in condition_results:
                self.assertAlmostEqual(
                    condition_result.score, average_conditions, delta=1
                )
            condition_results.delete()
