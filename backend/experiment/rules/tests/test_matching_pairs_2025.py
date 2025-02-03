from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from section.models import Playlist, Section
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
        cls.block = Block.objects.create(rules="MATCHING_PAIRS_2025", slug="mpairs-2025", rounds=42)
        cls.session = Session.objects.create(block=cls.block, participant=cls.participant, playlist=cls.playlist)
        cls.rules = cls.session.block_rules()

    @staticmethod
    def create_section_csv():
        corpora = [
            {"name": "CH", "condition_stimuli_amount": 8},
        ]
        conditions_types = {
            "O": {"name": "original", "conditions": ["1"]},
            "T": {"name": "temporal", "conditions": ["1", "2", "3", "4", "5"]},
            "F": {"name": "frequency", "conditions": ["1", "2", "3", "4", "5"]},
        }

        section_csv = ""

        for corpus in corpora:
            for condition_type, condition in conditions_types.items():
                for condition_number in condition["conditions"]:
                    for i in range(corpus["condition_stimuli_amount"]):
                        stimuli_number = i + 1
                        section_csv += f"default,{corpus['name']}_{condition_type}_{condition_number}_{stimuli_number},0.0,10.0,MatchingPairs2/{condition['name']}/{corpus['name']}_{condition_type}_{condition_number}_{stimuli_number}.mp3,{condition['name']},{condition_number}\n"

        return section_csv

    def test_select_least_played_session_condition_types_participant_specific(self):
        # Clear existing json_data for the base session
        self.session.json_data = {"conditions": [["original", "1"]]}
        self.session.save(update_fields=["json_data"])

        # Create two additional sessions for the same participant
        session2 = Session.objects.create(block=self.block, participant=self.participant, playlist=self.playlist)
        session2.json_data = {"conditions": [["temporal", "2"], ["frequency", "3"]]}
        session2.save(update_fields=["json_data"])

        session3 = Session.objects.create(block=self.block, participant=self.participant, playlist=self.playlist)
        session3.json_data = {"conditions": [["original", "1"], ["temporal", "4"]]}
        session3.save(update_fields=["json_data"])

        # For participant_specific=True, only sessions from self.participant are considered.
        # Counts: "original": 1 (self.session) + 1 (session3) = 2,
        #         "temporal": 1 (session2) + 1 (session3) = 2,
        #         "frequency": 1 (session2) = 1.
        least_types = self.rules._select_least_played_session_condition_types(self.session, participant_specific=True)
        # Expect the condition type with lowest count ("frequency")
        self.assertEqual(least_types, ["frequency"])

    def test_select_least_played_session_condition_types_overall(self):
        # Set base session's json_data
        self.session.json_data = {"conditions": [["temporal", "2"]]}
        self.session.save(update_fields=["json_data"])

        # Create sessions for different participants, they will be included overall.
        participant_b = Participant.objects.create()
        session_b = Session.objects.create(block=self.block, participant=participant_b, playlist=self.playlist)
        session_b.json_data = {"conditions": [["original", "1"], ["temporal", "3"]]}
        session_b.save(update_fields=["json_data"])

        participant_c = Participant.objects.create()
        session_c = Session.objects.create(block=self.block, participant=participant_c, playlist=self.playlist)
        session_c.json_data = {"conditions": [["original", "1"], ["frequency", "4"]]}
        session_c.save(update_fields=["json_data"])

        # Overall counts (all sessions in the playlist):
        # From self.session: "temporal": 1.
        # From session_b: "original": 1, "temporal": 1.
        # From session_c: "original": 1, "frequency": 1.
        # Totals: "original": 2, "temporal": 2, "frequency": 1.
        least_types = self.rules._select_least_played_session_condition_types(self.session, participant_specific=False)

        self.assertEqual(least_types, ["frequency"])

    def test_select_least_played_session_conditions_participant_specific(self):
        # Create a custom playlist with controlled sections
        custom_playlist = Playlist.objects.create(name="TestConditionsParticipantSpecific")
        # Manually create two sections for tag "temporal" with two different groups
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="1")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="2")

        # Create two sessions for the same participant using the custom playlist
        session_custom = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_custom.json_data = {"conditions": [["temporal", "1"]]}
        session_custom.save(update_fields=["json_data"])

        session_custom2 = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_custom2.json_data = {"conditions": [["temporal", "1"], ["temporal", "2"]]}
        session_custom2.save(update_fields=["json_data"])

        # For participant_specific=True, only sessions from self.participant are considered.
        # Count for group "1": 1 (from session_custom) + 1 (from session_custom2) = 2,
        # Count for group "2": 0 (in session_custom) + 1 (from session_custom2) = 1.
        # So the least played condition group is "2".
        least = self.rules._select_least_played_session_conditions(
            session_custom, "temporal", participant_specific=True
        )
        self.assertEqual(least, ["2"])

    def test_select_least_played_session_conditions_participant_specific_multiple(self):
        # Create a custom playlist with controlled sections
        custom_playlist = Playlist.objects.create(name="TestConditionsParticipantSpecificMultiple")
        # Manually create sections for tag "temporal" with two different groups
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="1")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="2")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="3")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="4")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="5")

        # Create two sessions for the same participant using the custom playlist
        session_custom = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_custom.json_data = {"conditions": [["original", "1"], ["frequency", "2"], ["temporal", "3"]]}
        session_custom.save(update_fields=["json_data"])

        session_custom2 = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_custom2.json_data = {"conditions": [["frequency", "1"], ["temporal", "2"]]}
        session_custom2.save(update_fields=["json_data"])

        # For participant_specific=True, only sessions from self.participant are considered.
        # Count for group "1": 1 (from session_custom) + 1 (from session_custom2) = 2,
        # Count for group "2": 0 (in session_custom) + 1 (from session_custom2) = 1.
        # So the least played condition group is "2".
        least = self.rules._select_least_played_session_conditions(
            session_custom, "temporal", participant_specific=True
        )
        self.assertEqual(least, ["1", "4", "5"])

    def test_select_least_played_session_conditions_overall(self):
        # Create a custom playlist with controlled sections
        custom_playlist = Playlist.objects.create(name="TestConditionsOverall")
        # Manually create two sections for tag "temporal"
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="1")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="2")

        # Create a session for self.participant with json_data playing both groups once
        session_primary = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_primary.json_data = {"conditions": [["temporal", "1"], ["temporal", "2"]]}
        session_primary.save(update_fields=["json_data"])

        # Create a session for a different participant
        participant_b = Participant.objects.create()
        session_b = Session.objects.create(block=self.block, participant=participant_b, playlist=custom_playlist)
        # This session only plays group "2"
        session_b.json_data = {"conditions": [["temporal", "2"]]}
        session_b.save(update_fields=["json_data"])

        # Overall, playlist.session_set.all() includes both sessions.
        # Count for group "1": 1 (from session_primary).
        # Count for group "2": 1 (from session_primary) + 1 (from session_b) = 2.
        # So the least played condition group overall is "1".
        least = self.rules._select_least_played_session_conditions(
            session_primary, "temporal", participant_specific=False
        )
        self.assertEqual(least, ["1"])

    def test_select_least_played_session_conditions_overall_multiple(self):
        # Create a custom playlist with controlled sections
        custom_playlist = Playlist.objects.create(name="TestConditionsOverallMultiple")
        # Manually create sections for tag "temporal" with two different groups
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="1")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="2")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="3")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="4")
        Section.objects.create(playlist=custom_playlist, tag="temporal", group="5")

        # Create a session for self.participant with json_data playing all groups once
        session_primary = Session.objects.create(
            block=self.block, participant=self.participant, playlist=custom_playlist
        )
        session_primary.json_data = {
            "conditions": [
                ["temporal", "1"],
                ["temporal", "2"],
                ["temporal", "5"],
            ]
        }
        session_primary.save(update_fields=["json_data"])

        # Create a session for a different participant
        participant_b = Participant.objects.create()
        session_b = Session.objects.create(block=self.block, participant=participant_b, playlist=custom_playlist)
        # This session only plays group "2"
        session_b.json_data = {"conditions": [["temporal", "2"], ["temporal", "5"]]}
        # Overall, playlist.session_set.all() includes both sessions.
        # Count for group "1": 1 (from session_primary).
        # Count for group "2": 1 (from session_primary) + 1 (from session_b) = 2.
        # So the least played condition group overall is "1".
        least = self.rules._select_least_played_session_conditions(
            session_primary, "temporal", participant_specific=False
        )
        self.assertEqual(least, ["3", "4"])

    def test_select_least_played_condition_type_condition_pair(self):
        """The methods to select a condition type and a condition are made so that the participant
        will never play the same condition type condition combination before playing all other condition type condition combinations.
        E.g., assuming we have the following combos: [O1, T1, T2, T3, T4, T5, F1, F2, F3, F4, F5],
        the participant will play all of them (in least played overall / random order) before playing any of them again.
        We thus want to test if there are no repetitions in the selected sections if a participant plays 11 blocks.
        """

        # Use the playlist from the setup
        playlist = self.playlist

        # Create a session for the participant
        session = Session.objects.create(block=self.block, participant=self.participant, playlist=playlist)

        # Create a list to store the selected sections
        selected_condition_type_condition_pairs = []

        condition_pairs_amount = playlist.section_set.values("tag", "group").distinct().count()

        # Let's simulate the participant playing all conditions 5 times
        for i in range(condition_pairs_amount * 5):
            # Select sections for the session
            condition_type, condition = self.rules._select_least_played_condition_type_condition_pair(session)

            # Add the selected section to the list
            selected_condition_type_condition_pairs.append(f"{condition_type}{condition}")

            # Append the selected section to the session's json_data
            if "conditions" not in session.json_data:
                session.json_data["conditions"] = []

            session.json_data["conditions"].append([condition_type, condition])

            # Save the session
            session.save(update_fields=["json_data"])

            # If this was the 3rd block in the session, create a new session
            if (i + 1) % 3 == 0:
                session = Session.objects.create(block=self.block, participant=self.participant, playlist=playlist)

        # The first three blocks should always have different condition_types
        first_three_blocks = selected_condition_type_condition_pairs[:3]

        # Compare the first character of each condition_type
        self.assertEqual(len(set([x[0] for x in first_three_blocks])), 3)

        # Check if there are no repetitions in the first 11 blocks
        first_repetition_set = selected_condition_type_condition_pairs[:condition_pairs_amount]
        self.assertEqual(len(first_repetition_set), len(set(first_repetition_set)))

        # Check if every pair is represented 5 times in selected_condition_type_condition_pairs (the participant played 5 times * 11 blocks)
        for pair in selected_condition_type_condition_pairs:
            self.assertEqual(selected_condition_type_condition_pairs.count(pair), 5)
