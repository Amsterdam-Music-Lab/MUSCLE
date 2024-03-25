from django.test import TestCase
from django.utils import timezone

from image.models import Image
from experiment.views import (
    serialize_experiment,
    serialize_experiment_series,
    serialize_experiment_series_group
)
from experiment.models import (
    Experiment,
    ExperimentSeries,
    ExperimentSeriesGroup,
    GroupedExperiment,
)
from participant.models import Participant
from session.models import Session


class TestExperimentCollectionViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()

    def test_get_experiment_collection(self):
        # save participant data to request session
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()

        experiment1 = Experiment.objects.create(
            name='experiment1', slug='experiment1')
        experiment2 = Experiment.objects.create(
            name='experiment2', slug='experiment2')
        experiment3 = Experiment.objects.create(
            name='experiment3', slug='experiment3')
        experiment4 = Experiment.objects.create(
            name='experiment4', slug='experiment4')
        collection = ExperimentSeries.objects.create(
            slug='series_test',
            first_experiments=[experiment1.pk],
            random_experiments=[experiment2.pk, experiment3.pk],
            last_experiments=[experiment4.pk]
        )
        # check that first_experiments is returned correctly
        response = self.client.get('/experiment/collection/series_test/')
        assert response.json().get('redirect_to').get('slug') == 'experiment1'
        # create session
        Session.objects.create(
            experiment=experiment1,
            participant=self.participant,
            finished_at=timezone.now()
        )
        response = self.client.get('/experiment/collection/series_test/')
        assert response.json().get('redirect_to').get('slug') in ('experiment2', 'experiment3')
        Session.objects.create(
            experiment=experiment2,
            participant=self.participant,
            finished_at=timezone.now()
        )
        Session.objects.create(
            experiment=experiment3,
            participant=self.participant,
            finished_at=timezone.now()
        )
        response = self.client.get('/experiment/collection/series_test/')
        assert response.json().get('redirect_to').get('slug') == 'experiment4'
        # if ExperimentSeries has dashboard set True, return list of random experiments
        collection.dashboard = True
        collection.save()
        response = self.client.get('/experiment/collection/series_test/')
        assert type(response.json().get('dashboard')) == list


class ExperimentViewsTest(TestCase):

    def test_serialize_experiment(self):
        # Create an experiment
        experiment = Experiment.objects.create(
            slug='test-experiment',
            name='Test Experiment',
            description='This is a test experiment',
            image=Image.objects.create(
                file='test-image.jpg'
            )
        )

        # Call the serialize_experiment function
        serialized_experiment = serialize_experiment(experiment, 3)

        # Assert the serialized data
        self.assertEqual(
            serialized_experiment['slug'], 'test-experiment'
        )
        self.assertEqual(
            serialized_experiment['name'], 'Test Experiment'
        )
        self.assertEqual(
            serialized_experiment['description'], 'This is a test experiment'
        )
        self.assertEqual(
            serialized_experiment['image'], '/upload/test-image.jpg'
        )
        self.assertEqual(
            serialized_experiment['finished_session_count'], 3
        )

    def test_serialize_experiment_series(self):
        # Create an experiment series
        experiment_series = ExperimentSeries.objects.create(
            slug='test-series',
            name='Test Series',
            description='This is a test series'
        )

        # Create some experiment series groups
        ExperimentSeriesGroup.objects.create(
            series=experiment_series,
            name='Group 1',
            order=0,
            dashboard=True,
            randomize=False
        )
        ExperimentSeriesGroup.objects.create(
            series=experiment_series,
            name='Group 2',
            order=1,
            dashboard=False,
            randomize=True
        )

        # Call the serialize_experiment_series function
        serialized_experiment_series = serialize_experiment_series(
            experiment_series
        )

        # Assert the serialized data
        self.assertEqual(
            serialized_experiment_series['slug'], 'test-series'
        )
        self.assertEqual(
            serialized_experiment_series['name'], 'Test Series'
        )
        self.assertEqual(
            serialized_experiment_series['description'], 'This is a test series'
        )
        self.assertEqual(
            serialized_experiment_series['dashboard'], []
        )
        self.assertIsNone(
            serialized_experiment_series['redirect_to']
        )
        self.assertEqual(
            len(serialized_experiment_series['groups']), 2
        )
        self.assertEqual(
            serialized_experiment_series['groups'][0]['name'], 'Group 1'
        )
        self.assertEqual(
            serialized_experiment_series['groups'][1]['name'], 'Group 2'
        )

    def test_serialize_experiment_series_group(self):
        # Create an experiment series
        experiment_series = ExperimentSeries.objects.create(
            slug='test-series',
            name='Test Series',
            description='This is a test series'
        )

        # Create an experiment series group
        experiment_series_group = ExperimentSeriesGroup.objects.create(
            series=experiment_series,
            name='Test Group',
            dashboard=True,
            randomize=False,
            order=0
        )

        # Create some experiments
        experiment1 = Experiment.objects.create(
            slug='test-experiment-1',
            name='Test Experiment 1',
        )
        experiment2 = Experiment.objects.create(
            slug='test-experiment-2',
            name='Test Experiment 2',
        )

        # Create some grouped experiments
        GroupedExperiment.objects.create(
            group=experiment_series_group,
            experiment=experiment1,
            order=0
        )
        GroupedExperiment.objects.create(
            group=experiment_series_group,
            experiment=experiment2,
            order=1
        )

        # Call the serialize_experiment_series_group function
        serialized_experiment_series_group = serialize_experiment_series_group(
            experiment_series_group
        )

        # Assert the serialized data
        self.assertEqual(
            serialized_experiment_series_group['name'], 'Test Group'
        )
        self.assertTrue(
            serialized_experiment_series_group['dashboard']
        )
        self.assertEqual(
            len(serialized_experiment_series_group['experiments']), 2
        )
        self.assertEqual(
            serialized_experiment_series_group['experiments'][0]['slug'],
            'test-experiment-1'
        )
        self.assertEqual(
            serialized_experiment_series_group['experiments'][1]['slug'],
            'test-experiment-2'
        )
