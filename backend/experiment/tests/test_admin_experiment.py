from zipfile import ZipFile
from io import BytesIO
import json
from django.test import Client, TestCase
from django.forms.models import model_to_dict
from django.contrib.admin.sites import AdminSite
from experiment.admin import ExperimentAdmin
from experiment.models import Experiment
from participant.models import Participant
from result.models import Result
from session.models import Session

# Expected field count per model
EXPECTED_EXPERIMENT_FIELDS = 15
EXPECTED_SESSION_FIELDS = 9
EXPECTED_RESULT_FIELDS = 12
EXPECTED_PARTICIPANT_FIELDS = 5


class MockRequest:
    pass


request = MockRequest()

this_experiment_admin = ExperimentAdmin(
    model=Experiment, admin_site=AdminSite)


class TestAdminExperiment(TestCase):    

    @classmethod
    def setUpTestData(cls):
        Experiment.objects.create(
                    name='test',
                    slug='TEST'
                )
        Participant.objects.create()
        Session.objects.create(
            experiment=Experiment.objects.first(),
            participant=Participant.objects.first()
        )
        Result.objects.create(
            session=Session.objects.first()
        )

    def test_experiment_model_fields(self):
        experiment = model_to_dict(Experiment.objects.first())
        experiment_fields = [key for key in experiment]
        self.assertEqual(len(experiment_fields), EXPECTED_EXPERIMENT_FIELDS)

    def test_session_model_fields(self):
        session = model_to_dict(Session.objects.first())
        session_fields = [key for key in session]
        self.assertEqual(len(session_fields), EXPECTED_SESSION_FIELDS)

    def test_result_model_fields(self):
        result = model_to_dict(Result.objects.first())
        result_fields = [key for key in result]
        self.assertEqual(len(result_fields), EXPECTED_RESULT_FIELDS)

    def test_participant_model(self):
        participant = model_to_dict(Participant.objects.first())
        participant_fields = [key for key in participant]
        self.assertEqual(len(participant_fields), EXPECTED_PARTICIPANT_FIELDS)


class TestAdminExperimentExport(TestCase):

    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.experiment = Experiment.objects.get(name='Hooked-China')
        for playlist in cls.experiment.playlists.all():
            playlist.update_sections()
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
        )
        for i in range(5):
            Result.objects.create(
                session=Session.objects.first(),
                expected_response = i,
                given_response = i,
                question_key = 'test_question_' + str(i),
            )
            Result.objects.create(
                participant=cls.participant,
                question_key= i,
                given_response = i,
            )

    def setUp(self):
        self.client = Client()

    def test_admin_export(self):
        response = this_experiment_admin.export(request, self.experiment)
        zip_buffer = BytesIO(response.content)
        with ZipFile(zip_buffer, 'r') as test_zip:
            # Test files inside zip
            self.assertIn('participants.json', test_zip.namelist())
            self.assertIn('profiles.json', test_zip.namelist())
            self.assertIn('results.json', test_zip.namelist())
            self.assertIn('sections.json', test_zip.namelist())
            self.assertIn('sessions.json', test_zip.namelist())
            self.assertIn('songs.json', test_zip.namelist())
            self.assertEqual(len(test_zip.namelist()), 6)

            # test content of the json files in the zip
            these_participants = json.loads(test_zip.read('participants.json').decode("utf-8"))
            self.assertEqual(len(these_participants), 1)
            self.assertEqual(Participant.objects.first().unique_hash, '42')

            these_profiles = json.loads(test_zip.read('profiles.json').decode("utf-8"))
            self.assertEqual(len(these_profiles), 5)

            these_results = json.loads(test_zip.read('results.json').decode("utf-8"))
            self.assertEqual(len(these_results), 5)

            these_sections = json.loads(test_zip.read('sections.json').decode("utf-8"))
            self.assertEqual(len(these_sections), 1000)

            these_sessions = json.loads(test_zip.read('sessions.json').decode("utf-8"))

            self.assertEqual(len(these_sessions), 1)
            self.assertEqual(these_sessions[0]['fields']['experiment'], 14)

            these_songs = json.loads(test_zip.read('songs.json').decode("utf-8"))
            self.assertEqual(len(these_songs), 100)

        # test response from forced download
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/x-zip-compressed')

    def test_export_table_includes_question_key(self):
        session_keys = ['session_start', 'session_end']
        result_keys = ['question_key']
        export_options = ['convert_result_json']  # Adjust based on your needs

        # Call the method under test
        rows, fieldnames = self.experiment.export_table(session_keys, result_keys, export_options)

        # Assert that 'question_key' is in the fieldnames and check its value in rows
        self.assertIn('question_key', fieldnames)
        for i in range(len(rows)):
            row = rows[i]
            self.assertIn('question_key', row)
            self.assertEqual(row['question_key'], 'test_question_' + str(i))