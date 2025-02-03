from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from section.models import Playlist
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
            "O": {"name": "original", "conditions": [1]},
            "T": {"name": "temporal", "conditions": [1, 2, 3, 4, 5]},
            "F": {"name": "frequency", "conditions": [1, 2, 3, 4, 5]},
        }

        section_csv = ""

        for corpus in corpora:
            for condition_type, condition in conditions_types.items():
                for condition_number in condition["conditions"]:
                    for i in range(corpus["condition_stimuli_amount"]):
                        stimuli_number = i + 1
                        section_csv += f"default,{corpus['name']}_{condition_type}_{condition_number}_{stimuli_number},0.0,10.0,MatchingPairs2/{condition['name']}/{corpus['name']}_{condition_type}_{condition_number}_{stimuli_number}.mp3,{condition['name']},{condition_number}\n"

        return section_csv

    def test_select_least_played_participant_condition_types(self):
        # We play multiple sections of all condition types (tag) and make sure that "frequency" and "original" are the least played condition types per condition (group)
        for section in self.session.playlist.section_set.filter(tag="temporal", group=4):
            for _ in range(25):
                Result.objects.create(
                    participant=self.participant,
                    section=section,
                    session=self.session,
                    score=10,
                    given_response="match",
                )

        for section in self.session.playlist.section_set.filter(tag="original", group=1):
            for _ in range(4):
                Result.objects.create(
                    participant=self.participant,
                    section=section,
                    session=self.session,
                    score=10,
                    given_response="match",
                )

        for section in self.session.playlist.section_set.filter(tag="frequency", group=4):
            for _ in range(20):
                Result.objects.create(
                    participant=self.participant,
                    section=section,
                    session=self.session,
                    score=10,
                    given_response="match",
                )

        condition_type = self.rules._select_least_played_participant_condition_types(self.session)
        self.assertNotEqual(condition_type, "temporal")
        self.assertEqual(condition_type, ["frequency", "original"])

        # We play a bit more of the "frequency" condition type to make "original" the least played condition type
        for section in self.session.playlist.section_set.filter(tag="frequency", group=1):
            for _ in range(1):
                Result.objects.create(
                    participant=self.participant,
                    section=section,
                    session=self.session,
                    score=10,
                    given_response="match",
                )

        condition_type = self.rules._select_least_played_participant_condition_types(self.session)
        self.assertEqual(condition_type, ["original"])

    def test_select_least_played_overall_condition_types(self):
        # We play multiple sections of all condition types (tag) and make sure that "frequency" and "original" are the least played condition types per condition (group)
        for section in self.session.playlist.section_set.filter(tag="temporal", group=4):
            for _ in range(25):
                participant = Participant.objects.create()
                Result.objects.create(
                    participant=participant,
                    section=section,
                    session=self.session,
                    score=10,
                    given_response="match",
                )

        for section in self.session.playlist.section_set.filter(tag="original", group=1):
            for _ in range(4):
                participant = Participant.objects.create()
                Result.objects.create(
                    participant=participant,
                    section=section,
                    session=self.session,
                    score=10,
                    given_response="match",
                )

        for section in self.session.playlist.section_set.filter(tag="frequency", group=4):
            for _ in range(20):
                participant = Participant.objects.create()
                Result.objects.create(
                    participant=participant,
                    section=section,
                    session=self.session,
                    score=10,
                    given_response="match",
                )

        condition_type = self.rules._select_least_played_overall_condition_types(self.session)
        self.assertNotEqual(condition_type, "temporal")
        self.assertEqual(condition_type, ["frequency", "original"])

        # We play a bit more of the "frequency" condition type to make "original" the least played condition type
        for section in self.session.playlist.section_set.filter(tag="frequency", group=1):
            for _ in range(1):
                participant = Participant.objects.create()
                Result.objects.create(
                    participant=participant,
                    section=section,
                    session=self.session,
                    score=10,
                    given_response="match",
                )

        condition_type = self.rules._select_least_played_overall_condition_types(self.session)
        self.assertEqual(condition_type, ["original"])
