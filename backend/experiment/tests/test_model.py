from django.test import TestCase
from theme.models import ThemeConfig
from experiment.models import Experiment, ExperimentCollection
from participant.models import Participant
from session.models import Session
from result.models import Result


class ExperimentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ThemeConfig.objects.create(
            name='Default',
            description='Default theme configuration',
            heading_font_url='https://example.com/heading_font',
            body_font_url='https://example.com/body_font',
            logo_url='https://example.com/logo',
            background_url='https://example.com/background',
        )
        Experiment.objects.create(
            name='Test Experiment',
            description='Test experiment description',
            slug='test-experiment',
            url='https://example.com/experiment',
            hashtag='test',
            rounds=5,
            bonus_points=10,
            rules='GOLD_MSI',
            language='en',
            theme_config=ThemeConfig.objects.get(name='Default'),
        )

    def test_experiment_str(self):
        experiment = Experiment.objects.get(name='Test Experiment')
        self.assertEqual(str(experiment), 'Test Experiment')

    def test_experiment_session_count(self):
        experiment = Experiment.objects.get(name='Test Experiment')
        self.assertEqual(experiment.session_count(), 0)

    def test_experiment_playlist_count(self):
        experiment = Experiment.objects.get(name='Test Experiment')
        self.assertEqual(experiment.playlist_count(), 0)

    def test_experiment_current_participants(self):
        experiment = Experiment.objects.get(name='Test Experiment')
        participants = experiment.current_participants()
        self.assertEqual(len(participants), 0)

    def test_experiment_export_admin(self):
        experiment = Experiment.objects.get(name='Test Experiment')
        exported_data = experiment.export_admin()
        self.assertEqual(exported_data['experiment']['name'], 'Test Experiment')

    def test_experiment_export_sessions(self):
        experiment = Experiment.objects.get(name='Test Experiment')
        sessions = experiment.export_sessions()
        self.assertEqual(len(sessions), 0)

    def test_experiment_export_table(self):
        experiment = Experiment.objects.get(name='Test Experiment')
        amount_of_sessions = 3

        for i in range(amount_of_sessions):
            session = Session.objects.create(
                experiment=experiment,
                participant=Participant.objects.create()
            )
            Result.objects.create(
                session=session,
                expected_response=1,
                given_response=1,
                question_key='test_question_1',
            )

        session_keys = ['experiment_id', 'experiment_name']
        result_keys = ['section_name', 'result_created_at']
        export_options = {'wide_format': True}
        rows, fieldnames = experiment.export_table(
            session_keys,
            result_keys,
            export_options
        )

        self.assertEqual(len(rows), amount_of_sessions)
        self.assertEqual(len(fieldnames), len(session_keys) + len(result_keys))

    def test_experiment_get_rules(self):
        experiment = Experiment.objects.get(name='Test Experiment')
        rules = experiment.get_rules()
        self.assertIsNotNone(rules)

    def test_experiment_max_score(self):
        experiment = Experiment.objects.get(name='Test Experiment')

        amount_of_results = 3
        question_score = 1

        session = Session.objects.create(
            experiment=experiment,
            participant=Participant.objects.create()
        )
        for j in range(amount_of_results):
            Result.objects.create(
                session=session,
                expected_response=1,
                given_response=1,
                score=question_score,
                question_key=f'test_question_{j + 1}',
            )
        session.finish()
        session.save()

        question_scores = amount_of_results * question_score
        bonus_points = experiment.bonus_points
        max_score = experiment.max_score()
        self.assertEqual(max_score, question_scores + bonus_points)
        self.assertEqual(max_score, 13.0)


class ExperimentCollectionModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.experiment_series = ExperimentCollection.objects.create(
            slug='test-series',
            name='Test Series',
            description='Test series description with a very long description. From here to the moon and from the moon to the stars.',
        )

    def test_experiment_series_str(self):
        experiment_series_no_name = ExperimentCollection.objects.create(
            slug='test-series-no-name',
        )

        self.assertEqual(str(self.experiment_series), 'Test Series')
        self.assertEqual(str(experiment_series_no_name), 'test-series-no-name')
