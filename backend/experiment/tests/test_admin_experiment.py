from django.test import Client, TestCase
from django.forms.models import model_to_dict
from django.contrib.admin.sites import AdminSite
from experiment.admin.experiment import ExperimentAdmin
from experiment.models import Experiment, Session, Result, Participant

# Expected field count per model
EXPERIMENT_FIELDS = 10
SESSION_FIELDS = 8
RESULT_FIELDS = 9
PARTICIPANT_FIELDS = 4


class MockRequest:
    pass


request = MockRequest()

this_experiment_admin = ExperimentAdmin(
    model=Experiment, admin_site=AdminSite)


class TestAdminExperiment(TestCase):

    def setUp(self):

        self.client = Client(
            HTTP_USER_AGENT='Agent 007'
        )

        Experiment.objects.create(
            name='test',
            slug='TEST'
        )

        self.client.get('/experiment/participant/')

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
        self.assertEqual(len(experiment_fields), EXPERIMENT_FIELDS)

    def test_session_model_fields(self):
        session = model_to_dict(Session.objects.first())
        session_fields = [key for key in session]
        self.assertEqual(len(session_fields), SESSION_FIELDS)

    def test_result_model_fields(self):
        result = model_to_dict(Result.objects.first())
        result_fields = [key for key in result]
        self.assertEqual(len(result_fields), RESULT_FIELDS)

    def test_participant_model(self):
        participant = model_to_dict(Participant.objects.first())
        participant_fields = [key for key in participant]
        self.assertEqual(len(participant_fields), PARTICIPANT_FIELDS)

    def test_admin_export(self):
        experiment = Experiment.objects.first()
        response = this_experiment_admin.export(request, experiment)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
