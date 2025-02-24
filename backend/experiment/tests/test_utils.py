from zipfile import ZipFile
from io import BytesIO
import json

from django.test import TestCase, Client

from experiment.utils import create_player_labels, export_json_results

from experiment.models import Experiment, ExperimentTranslatedContent, Phase, Block, Feedback
from participant.models import Participant
from session.models import Session
from result.models import Result


class TestExperimentUtils(TestCase):

    def test_create_player_labels(self):
        labels = create_player_labels(3, 'alphabetic')
        assert labels == ['A', 'B', 'C']
        labels = create_player_labels(4, 'roman')
        assert labels == ['I', 'II', 'III', 'IV']
        labels = create_player_labels(2)
        assert labels == ['1', '2']

class TestBlockExport(TestCase):
    fixtures = ["playlist", "experiment"]

    @classmethod
    def setUpTestData(cls):
        experiment = Experiment.objects.create(slug="test-experiment")
        ExperimentTranslatedContent.objects.create(
            experiment=experiment, language="en", name="Test Experiment"
        )
        phase = Phase.objects.create(experiment=experiment)
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.get(slug="huang_2022")
        cls.block.phase = phase
        for playlist in cls.block.playlists.all():
            playlist._update_sections()
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
        )

        for i in range(5):
            Result.objects.create(
                session=Session.objects.first(),
                expected_response=i,
                given_response=i,
                question_key="test_question_" + str(i),
            )
            Result.objects.create(
                participant=cls.participant,
                question_key=i,
                given_response=i,
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

    def test_admin_export(self):
        response = export_json_results(self.block.id)
        zip_buffer = BytesIO(response.content)
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

        # test response from forced download
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/x-zip-compressed")

    def test_export_table_includes_question_key(self):
        session_keys = ["session_start", "session_end"]
        result_keys = ["question_key"]
        export_options = ["convert_result_json"]  # Adjust based on your needs

        # Call the method under test
        rows, fieldnames = self.block.export_table(session_keys, result_keys, export_options)

        # Assert that 'question_key' is in the fieldnames and check its value in rows
        self.assertIn("question_key", fieldnames)
        for i in range(len(rows)):
            row = rows[i]
            self.assertIn("question_key", row)
            self.assertEqual(row["question_key"], "test_question_" + str(i))
