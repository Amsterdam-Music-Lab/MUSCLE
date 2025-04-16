from django.test import TestCase

from experiment.models import Block, Experiment, Phase
from participant.models import Participant
from result.models import Result
from section.models import Playlist, Section, Song
from session.models import Session
from question.questions import create_default_questions


class MatchingPairs2025Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_default_questions()
        section_csv = cls.create_section_csv()
        cls.playlist = Playlist.objects.create(name="TestMatchingPairs2025")
        cls.playlist.csv = section_csv
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

    def test_select_least_played_session_condition_types_participant_specific(self):
        # Instead of 'original', store as 'O','1'
        self.session.save_json_data({"conditions": [["O", "1"]]})

        # Create two additional sessions for the same participant
        session2 = Session.objects.create(block=self.block, participant=self.participant, playlist=self.playlist)
        session2.save_json_data({"conditions": [["TD", "2"], ["SD", "3"]]})

        session3 = Session.objects.create(block=self.block, participant=self.participant, playlist=self.playlist)
        session3.save_json_data({"conditions": [["O", "1"], ["TD", "4"]]})

        # For participant_specific=True, only sessions from self.participant are considered.
        # Counts: "O": 1 (self.session) + 1 (session3) = 2,
        #         "TD": 1 (session2) + 1 (session3) = 2,
        #         "SD": 1 (session2) = 1.
        least_types = self.rules._select_least_played_session_condition_types(self.session, participant_specific=True)
        # Expect the condition type with lowest count ("SD")
        self.assertEqual(least_types, ["SD"])

    def test_select_least_played_session_condition_types_overall(self):
        # Set base session's json_data
        self.session.save_json_data({"conditions": [["TD", "2"]]})

        # Create sessions for different participants, they will be included overall.
        participant_b = Participant.objects.create()
        session_b = Session.objects.create(block=self.block, participant=participant_b, playlist=self.playlist)
        session_b.save_json_data({"conditions": [["O", "1"], ["TD", "3"]]})

        participant_c = Participant.objects.create()
        session_c = Session.objects.create(block=self.block, participant=participant_c, playlist=self.playlist)
        session_c.save_json_data({"conditions": [["O", "1"], ["SD", "4"]]})

        # Overall counts (all sessions in the playlist):
        # From self.session: "temporal": 1.
        # From session_b: "original": 1, "temporal": 1.
        # From session_c: "original": 1, "frequency": 1.
        # Totals: "original": 2, "temporal": 2, "frequency": 1.
        least_types = self.rules._select_least_played_session_condition_types(self.session, participant_specific=False)

        self.assertEqual(least_types, ["SD"])

    def test_select_least_played_session_conditions_participant_specific(self):
        # Create a custom playlist with controlled sections
        custom_playlist = Playlist.objects.create(name="TestConditionsParticipantSpecific")
        # Manually create two sections for tag "temporal" with two different groups
        Section.objects.create(playlist=custom_playlist, group="TD", tag="1")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="2")

        # Create two sessions for the same participant using the custom playlist
        session_custom = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_custom.save_json_data({"conditions": [["TD", "1"]]})

        session_custom2 = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_custom2.save_json_data({"conditions": [["TD", "1"], ["TD", "2"]]})

        # For participant_specific=True, only sessions from self.participant are considered.
        # Count for group "1": 1 (from session_custom) + 1 (from session_custom2) = 2,
        # Count for group "2": 0 (in session_custom) + 1 (from session_custom2) = 1.
        # So the least played condition group is "2".
        least = self.rules._select_least_played_session_difficulty(
            session_custom, "TD", participant_specific=True
        )
        self.assertEqual(least, ["2"])

    def test_select_least_played_session_conditions_participant_specific_multiple(self):
        # Create a custom playlist with controlled sections
        custom_playlist = Playlist.objects.create(name="TestConditionsParticipantSpecificMultiple")
        # Manually create sections for tag "temporal" with two different groups
        Section.objects.create(playlist=custom_playlist, group="TD", tag="1")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="2")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="3")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="4")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="5")

        # Create two sessions for the same participant using the custom playlist
        session_custom = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_custom.save_json_data(
            {"conditions": [["O", "1"], ["SD", "2"], ["TD", "3"]]}
        )

        session_custom2 = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_custom2.save_json_data({"conditions": [["SD", "1"], ["TD", "2"]]})

        # For participant_specific=True, only sessions from self.participant are considered.
        # Count for group "1": 1 (from session_custom) + 1 (from session_custom2) = 2,
        # Count for group "2": 0 (in session_custom) + 1 (from session_custom2) = 1.
        # So the least played condition group is "2".
        least = self.rules._select_least_played_session_difficulty(
            session_custom, "TD", participant_specific=True
        )

        self.assertEqual(len(least), 3)
        self.assertIn("1", least)
        self.assertIn("4", least)
        self.assertIn("5", least)

    def test_select_least_played_session_conditions_overall(self):
        # Create a custom playlist with controlled sections
        custom_playlist = Playlist.objects.create(name="TestConditionsOverall")
        # Manually create two sections for tag "temporal"
        Section.objects.create(playlist=custom_playlist, group="TD", tag="1")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="2")

        # Create a session for self.participant with json_data playing both groups once
        session_primary = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_primary.save_json_data({"conditions": [["TD", "1"], ["TD", "2"]]})

        # Create a session for a different participant
        participant_b = Participant.objects.create()
        session_b = Session.objects.create(block=self.block, participant=participant_b, playlist=custom_playlist)
        # This session only plays group "2"
        session_b.save_json_data({"conditions": [["TD", "2"]]})

        # Overall, playlist.session_set.all() includes both sessions.
        # Count for group "1": 1 (from session_primary).
        # Count for group "2": 1 (from session_primary) + 1 (from session_b) = 2.
        # So the least played condition group overall is "1".
        least = self.rules._select_least_played_session_difficulty(
            session_primary, "TD", participant_specific=False
        )
        self.assertEqual(least, ["1"])

    def test_select_least_played_session_conditions_overall_multiple(self):
        # Create a custom playlist with controlled sections
        custom_playlist = Playlist.objects.create(name="TestConditionsOverallMultiple")
        # Manually create sections for tag "temporal" with two different groups
        Section.objects.create(playlist=custom_playlist, group="TD", tag="1")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="2")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="3")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="4")
        Section.objects.create(playlist=custom_playlist, group="TD", tag="5")

        # Create a session for self.participant with json_data playing all groups once
        session_primary = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_primary.save_json_data(
            {
                "conditions": [
                    ["TD", "1"],
                    ["TD", "2"],
                    ["TD", "5"],
                ]
            }
        )

        # Create a session for a different participant
        participant_b = Participant.objects.create()
        session_b = Session.objects.create(block=self.block, participant=participant_b, playlist=custom_playlist)
        # This session only plays group "2"
        session_b.save_json_data({"conditions": [["TD", "2"], ["TD", "5"]]})
        # Overall, playlist.session_set.all() includes both sessions.
        # Count for group "1": 1 (from session_primary).
        # Count for group "2": 1 (from session_primary) + 1 (from session_b) = 2.
        # So the least played condition group overall is "1".
        least = self.rules._select_least_played_session_difficulty(
            session_primary, "TD", participant_specific=False
        )
        self.assertEqual(len(least), 2)
        self.assertIn("3", least)
        self.assertIn("4", least)

    def test_select_least_played_condition_type_difficulty_pair(self):
        """The methods to select a condition type and a condition are made so that the participant
        will never play the same condition type condition combination before playing all other condition type condition combinations.
        E.g., assuming we have the following combos: [O0, TD1, TD2, TD3, T4, T5, F1, F2, F3, F4, F5],
        the participant will play all of them (in least played overall / random order) before playing any of them again.
        We thus want to test if there are no repetitions in the selected sections if a participant plays 11 blocks.
        """

        # Use the playlist from the setup
        playlist = self.playlist

        # Create a session for the participant
        session = Session.objects.create(block=self.block, participant=self.participant, playlist=playlist)

        # Create a list to store the selected sections
        selected_condition_type_difficulty_pairs = []

        condition_pairs_amount = (
            playlist.section_set.values_list("group", "tag").distinct().count()
        )

        # Let's simulate the participant playing all conditions 5 times
        for i in range(condition_pairs_amount * 5):
            # Select sections for the session
            condition_type, difficulty = (
                self.rules._select_least_played_condition_type_difficulty_pair(session)
            )

            # Add the selected section to the list
            selected_condition_type_difficulty_pairs.append(
                f"{condition_type}{difficulty}"
            )

            condition_data = session.json_data.get('conditions', [])
            condition_data.append([condition_type, difficulty])
            session.save_json_data({'conditions': condition_data})

            # If this was the 3rd block in the session, create a new session
            if (i + 1) % 3 == 0:
                session = Session.objects.create(block=self.block, participant=self.participant, playlist=playlist)

        # The first three blocks should always have different condition_types
        first_three_blocks = selected_condition_type_difficulty_pairs[:3]

        # Assertain that we have unique condition type / difficulty for each block
        self.assertEqual(len(set(first_three_blocks)), 3)

        # Check if there are no repetitions in the first 11 blocks
        first_repetition_set = selected_condition_type_difficulty_pairs[
            :condition_pairs_amount
        ]
        self.assertEqual(len(first_repetition_set), len(set(first_repetition_set)))

        # Check if every pair is represented 5 times in selected_condition_type_condition_pairs (the participant played 5 times * 11 blocks)
        for pair in selected_condition_type_difficulty_pairs:
            self.assertEqual(selected_condition_type_difficulty_pairs.count(pair), 5)

    def create_fake_results(self, session, n_results=5, score=1) -> list[int]:
        songs = Song.objects.all().values_list('id', flat=True)[:n_results]
        for song in songs:
            result, _created = Result.objects.get_or_create(
                participant=session.participant,
                question_key=f"song_{song}",
            )
            result.score = score
            result.save()
        return songs

    def test_select_sections_original_condition(self):
        """Test that _select_sections returns correct number of sections for original condition"""
        session = Session.objects.create(block=self.block, participant=self.participant, playlist=self.playlist)

        # Mock the condition selection to force "original" condition
        self.rules._select_least_played_condition_difficulty_pair = lambda x: (
            'O',
            '0',
        )

        sections = self.rules._select_sections(session)

        # Should return num_pairs * 2 sections (pairs are duplicated for original condition)
        self.assertEqual(len(sections), self.rules.num_pairs * 2)
        # All sections should have group "O" and tag "0"
        self.assertTrue(
            all(section.group == "O" and section.tag == '0' for section in sections)
        )

    def test_select_sections_temporal_condition(self):
        """Test that _select_sections returns correct sections for temporal condition with original pairs"""
        session = Session.objects.create(block=self.block, participant=self.participant, playlist=self.playlist)

        # Mock the condition selection to force "temporal" condition
        self.rules._select_least_played_condition_difficulty_pair = lambda x: (
            "TD",
            "1",
        )

        sections = self.rules._select_sections(session)

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
        session = Session.objects.create(block=self.block, participant=self.participant, playlist=self.playlist)

        # Mock the condition selection to force "frequency" condition
        self.rules._select_least_played_condition_difficulty_pair = lambda x: (
            "SD",
            "1",
        )

        sections = self.rules._select_sections(session)

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
        song_ids = self.create_fake_results(session, 2, 1)
        sections = self.rules._select_sections(session)
        for section in sections:
            self.assertNotIn(section.song.id, song_ids)

    def test_select_sections_least_played(self):
        """Test that we get preferably the least played sections"""
        session = Session.objects.create(
            block=self.block, participant=self.participant, playlist=self.playlist
        )
        # fake that all songs have been played
        faked_plays = self.create_fake_results(session, 10, 1)
        # fake that 5 songs have been played twice
        multiple_plays = self.create_fake_results(session, 5, 2)
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
