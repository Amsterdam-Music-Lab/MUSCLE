import csv
import json
from zipfile import ZipFile

from django.test import TestCase, Client

from experiment.utils import (
    block_export_csv_results,
    block_export_json_results,
    experiment_export_csv_results,
    format_label,
    get_block_csv_export_as_response,
    get_block_json_export_as_response,
)

from experiment.models import Experiment, Phase, Block, Feedback
from participant.models import Participant
from question.models import Question, QuestionList
from result.models import Result
from section.models import Playlist, Section, Song
from session.models import Session

class TestExperimentUtils(TestCase):

    def test_format_label(self):
        label = format_label(2, 'alphabetic')
        self.assertEqual(label, 'C')
        label = format_label(3, 'roman')
        self.assertEqual(label, 'IV')


class TestExport(TestCase):

    @classmethod
    def setUpTestData(cls):
        experiment = Experiment.objects.create(
            identifier="test-experiment", name="Test Experiment"
        )
        cls.phase = Phase.objects.create(experiment=experiment)
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.playlist = Playlist.objects.create(name="TestPlaylist")
        cls.block = Block.objects.create(
            identifier="test-block", rules="LIKERT", phase=cls.phase
        )
        cls.block.playlists.add(cls.playlist)
        song = Song.objects.create(artist="artist", name="name")
        Section.objects.bulk_create(
            [
                Section(
                    filename=f"section_{i}",
                    song=song,
                    playlist=cls.playlist,
                )
                for i in range(5)
            ]
        )
        Question.objects.bulk_create(
            [Question("test_profile_" + str(i)) for i in range(5)]
        )
        question_list = QuestionList.objects.create(block=cls.block)
        question_list.questions.add(*Question.objects.all())
        cls.session = Session.objects.create(
            block=cls.block, participant=cls.participant, playlist=cls.playlist
        )
        # create session results
        Result.objects.bulk_create(
            [
                Result(
                    session=cls.session,
                    expected_response=i,
                    given_response=i,
                    score=i,
                    section=Section.objects.get(filename=f"section_{i}"),
                    question_identifier="test_question",
                )
                for i in range(5)
            ]
        )
        # create profile results
        Result.objects.bulk_create(
            [
                Result(
                    participant=cls.participant,
                    question_identifier=f"test_profile_{i}",
                    given_response=i,
                )
                for i in range(5)
            ]
        )
        Feedback.objects.create(
            block=cls.block,
            text="Lorem",
        )
        Feedback.objects.create(
            block=cls.block,
            text="Ipsum",
        )

    def setUp(self):
        self.client = Client()

    def test_block_csv_export(self):
        csv_output = block_export_csv_results(self.block.identifier)
        reader = csv.DictReader(csv_output.split("\n"))
        rows = [r for r in reader]
        session_results_count = Result.objects.filter(session__isnull=False).count()
        self.assertEqual(len(rows), session_results_count)
        self.assertIn("test_profile_1.score", rows[0])
        profile_results_count = Result.objects.filter(participant__isnull=False).count()
        self.assertGreater(
            len(
                rows[0].keys(),
            ),
            profile_results_count * 2,
        )

    def test_block_csv_export_without_profile_results(self):
        Result.objects.exclude(participant__isnull=True).delete()
        csv_output = block_export_csv_results(self.block.identifier)
        reader = csv.DictReader(csv_output.split("\n"))
        rows = [r for r in reader]
        self.assertIsNone(rows[0].get("test_profile_0.score"))

    def test_block_csv_export_without_session_results(self):
        Result.objects.exclude(session__isnull=True).delete()
        csv_output = block_export_csv_results(self.block.identifier)
        reader = csv.DictReader(csv_output.split("\n"))
        rows = [r for r in reader]
        self.assertEqual(len(rows), 1)

    def test_block_csv_export_admin(self):
        response = get_block_csv_export_as_response(self.block.identifier)
        # test response from forced download
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response["content-type"], "text/csv")

    def test_experiment_csv_export_same_session(self):
        self.create_same_session_results()
        rows = self.get_rows_from_csv()
        response_keys = [key for key in rows[0].keys() if ".given_response" in key]
        self.assertEqual(len(response_keys), self.get_expected_results_count())
        self.assertEqual(len(rows), Section.objects.count())

    def create_same_session_results(self):
        Result.objects.bulk_create(
            [
                Result(
                    session=self.session,
                    section=Section.objects.get(filename="section_" + str(i)),
                    question_identifier="test_question2",
                    given_response=i + 10,
                    score=i + 10,
                )
                for i in range(5)
            ]
        )

    def test_experiment_csv_export_another_session(self):
        self.create_another_session_results()
        rows = self.get_rows_from_csv()
        response_keys = [key for key in rows[0].keys() if ".given_response" in key]
        self.assertEqual(len(response_keys), self.get_expected_results_count())
        self.assertEqual(len(rows), Section.objects.count())
        # test that the value from the first session by this participant is used
        self.assertEqual(int(rows[1].get("test_question.given_response")), 1)

    def create_another_session_results(self):
        # create another set of results with same identifier on another session on self.block
        same_block_session = Session.objects.create(
            block=self.block, participant=self.participant
        )
        Result.objects.bulk_create(
            [
                Result(
                    session=same_block_session,
                    section=Section.objects.get(filename="section_" + str(i)),
                    question_identifier="test_question",
                    given_response=i + 30,
                    score=i + 30,
                )
                for i in range(5)
            ]
        )

    def test_experiment_csv_export_another_block(self):
        self.create_another_block_results()
        rows = self.get_rows_from_csv()
        response_keys = [key for key in rows[0].keys() if ".given_response" in key]
        self.assertEqual(len(response_keys), self.get_expected_results_count())
        self.assertEqual(len(rows), Section.objects.count())

    def create_another_block_results(self):
        # create extra results for the test sections on another block & session
        block = Block.objects.create(
            identifier="test-block-2", rules="LIKERT", phase=self.phase
        )
        session = Session.objects.create(block=block, participant=self.participant)
        Result.objects.bulk_create(
            [
                Result(
                    session=session,
                    section=Section.objects.get(filename="section_" + str(i)),
                    question_identifier="test_question2",
                    given_response=i + 10,
                    score=i + 10,
                )
                for i in range(5)
            ]
        )

    def test_experiment_csv_export_another_participant(self):
        new_participant = Participant.objects.create()
        self.create_another_participant_results(new_participant)
        rows = self.get_rows_from_csv()
        response_keys = [key for key in rows[0].keys() if ".given_response" in key]
        self.assertEqual(len(response_keys), self.get_expected_results_count())
        self.assertEqual(len(rows), Section.objects.count() * 2)

    def create_another_participant_results(self, participant: Participant):
        # create another set of results for another participant
        new_session = Session.objects.create(block=self.block, participant=participant)
        Result.objects.bulk_create(
            [
                Result(
                    session=new_session,
                    section=Section.objects.get(filename="section_" + str(i)),
                    question_identifier="test_question",
                    given_response=i + 40,
                    score=i + 40,
                )
                for i in range(5)
            ]
        )

    def create_another_participant_profile_results(self, participant: Participant):
        Result.objects.bulk_create(
            [
                Result(
                    participant=participant,
                    question_identifier=f"test_profile_{i}",
                    given_response=i + 10,
                    score=i + 10,
                )
                for i in range(5)
            ]
        )

    def test_experiment_csv_export_with_all_scenarios(self):
        self.create_same_session_results()
        self.create_another_session_results()
        self.create_another_block_results()
        new_participant = Participant.objects.create()
        self.create_another_participant_results(new_participant)
        self.create_another_participant_profile_results(new_participant)
        rows = self.get_rows_from_csv()
        response_keys = [key for key in rows[0].keys() if ".given_response" in key]
        self.assertEqual(len(response_keys), self.get_expected_results_count())
        self.assertEqual(len(rows), Section.objects.count() * 2)

    def get_expected_results_count(self):
        return (
            Result.objects.filter(question_identifier__startswith="test_profile")
            .order_by("question_identifier")
            .distinct("question_identifier")
            .count()
            + Result.objects.filter(question_identifier__startswith="test_question")
            .order_by("question_identifier")
            .distinct("question_identifier")
            .count()
        )

    def get_rows_from_csv(self):
        csv_output = experiment_export_csv_results("test-experiment")
        reader = csv.DictReader(csv_output.split("\n"))
        return [r for r in reader]

    def test_block_json_export(self):
        zip_buffer = block_export_json_results(self.block.identifier)
        with ZipFile(zip_buffer, "r") as test_zip:
            # Test files inside zip
            self.assertIn("participants.json", test_zip.namelist())
            self.assertIn("profiles.json", test_zip.namelist())
            self.assertIn("results.json", test_zip.namelist())
            self.assertIn("sections.json", test_zip.namelist())
            self.assertIn("sessions.json", test_zip.namelist())
            self.assertIn("songs.json", test_zip.namelist())
            self.assertIn("feedback.json", test_zip.namelist())
            self.assertEqual(len(test_zip.namelist()), 7)

            # test content of the json files in the zip
            these_participants = json.loads(test_zip.read("participants.json").decode("utf-8"))
            self.assertEqual(len(these_participants), 1)
            self.assertEqual(Participant.objects.first().unique_hash, "42")

            these_profiles = json.loads(test_zip.read("profiles.json").decode("utf-8"))
            self.assertEqual(
                len(these_profiles),
                Result.objects.filter(participant__isnull=False).count(),
            )

            these_results = json.loads(test_zip.read("results.json").decode("utf-8"))
            self.assertEqual(
                len(these_results),
                Result.objects.filter(participant__isnull=False).count(),
            )

            these_sections = json.loads(test_zip.read("sections.json").decode("utf-8"))
            self.assertEqual(len(these_sections), Section.objects.count())

            these_sessions = json.loads(test_zip.read("sessions.json").decode("utf-8"))
            self.assertEqual(len(these_sessions), 1)
            self.assertEqual(these_sessions[0]["fields"]["block"], self.block.id)

            these_songs = json.loads(test_zip.read("songs.json").decode("utf-8"))
            self.assertEqual(len(these_songs), Song.objects.count())

            this_feedback = json.loads(test_zip.read("feedback.json").decode("utf-8"))
            self.assertEqual(len(this_feedback), Feedback.objects.count())

    def test_block_json_export_admin(self):
        response = get_block_json_export_as_response(self.block.identifier)
        # test response from forced download
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response["content-type"], "application/x-zip-compressed")
