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
        Section.objects.bulk_create(
            [
                Section(
                    filename=f"section_{i}",
                    song=Song.objects.create(artist=f"artist_{i}", name=f"name_{i}"),
                    playlist=cls.playlist,
                )
                for i in range(5)
            ]
        )
        cls.block = Block.objects.create(
            identifier="test-block", rules="LIKERT", phase=cls.phase
        )
        Question.objects.bulk_create(
            [Question("test_profile_" + str(i)) for i in range(5)]
        )
        question_list = QuestionList.objects.create(block=cls.block)
        question_list.questions.add(*Question.objects.all())
        for playlist in cls.block.playlists.all():
            playlist._update_sections()
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
                    section=Section.objects.get(filename="section_" + str(i)),
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
                    question_identifier="test_profile_" + str(i),
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
                rows[0].split(","),
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

    def test_experiment_csv_export(self):
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
                )
                for i in range(5)
            ]
        )
        csv_output = experiment_export_csv_results("test-experiment")
        self.assertIsNotNone(csv_output)

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
            self.assertEqual(len(these_profiles), 5)

            these_results = json.loads(test_zip.read("results.json").decode("utf-8"))
            self.assertEqual(len(these_results), 5)

            these_sections = json.loads(test_zip.read("sections.json").decode("utf-8"))
            self.assertEqual(len(these_sections), 1000)

            these_sessions = json.loads(test_zip.read("sessions.json").decode("utf-8"))

            self.assertEqual(len(these_sessions), 1)
            self.assertEqual(these_sessions[0]["fields"]["block"], 4)

            these_songs = json.loads(test_zip.read("songs.json").decode("utf-8"))
            self.assertEqual(len(these_songs), 100)

            this_feedback = json.loads(test_zip.read("feedback.json").decode("utf-8"))
            self.assertEqual(len(this_feedback), 2)

    def test_block_json_export_admin(self):
        response = get_block_json_export_as_response(self.block.identifier)
        # test response from forced download
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response["content-type"], "application/x-zip-compressed")
