from django.test import TestCase
from django.utils import timezone

from image.models import Image
from experiment.serializers import (
    serialize_experiment,
)
from experiment.models import (
    Experiment,
    ExperimentCollection,
    ExperimentCollectionGroup,
    GroupedExperiment,
)
from participant.models import Participant
from session.models import Session


class TestExperimentCollectionViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        collection = ExperimentCollection.objects.create(
            name='Test Series',
            slug='test_series'
        )
        introductory_group = ExperimentCollectionGroup.objects.create(
            name='introduction',
            series=collection,
            order=1
        )
        cls.experiment1 = Experiment.objects.create(
            name='experiment1', slug='experiment1')
        GroupedExperiment.objects.create(
            experiment=cls.experiment1,
            group=introductory_group
        )
        intermediate_group = ExperimentCollectionGroup.objects.create(
            name='intermediate',
            series=collection,
            order=2
        )
        cls.experiment2 = Experiment.objects.create(
            name='experiment2', slug='experiment2')
        cls.experiment3 = Experiment.objects.create(
            name='experiment3', slug='experiment3')
        GroupedExperiment.objects.create(
            experiment=cls.experiment2,
            group=intermediate_group
        )
        GroupedExperiment.objects.create(
            experiment=cls.experiment3,
            group=intermediate_group
        )
        final_group = ExperimentCollectionGroup.objects.create(
            name='final',
            series=collection,
            order=3
        )
        cls.experiment4 = Experiment.objects.create(
            name='experiment4', slug='experiment4')
        GroupedExperiment.objects.create(
            experiment=cls.experiment4,
            group=final_group
        )

    def test_get_experiment_collection(self):
        # save participant data to request session
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()
        # check that first_experiments is returned correctly
        response = self.client.get('/experiment/collection/test_series/')
        self.assertEqual(response.json().get(
            'next_experiment').get('slug'), 'experiment1')
        # create session
        Session.objects.create(
            experiment=self.experiment1,
            participant=self.participant,
            finished_at=timezone.now()
        )
        response = self.client.get('/experiment/collection/test_series/')
        self.assertIn(response.json().get('next_experiment').get(
            'slug'), ('experiment2', 'experiment3'))
        self.assertEqual(response.json().get('dashboard'), [])
        Session.objects.create(
            experiment=self.experiment2,
            participant=self.participant,
            finished_at=timezone.now()
        )
        Session.objects.create(
            experiment=self.experiment3,
            participant=self.participant,
            finished_at=timezone.now()
        )
        response = self.client.get('/experiment/collection/test_series/')
        self.assertEqual(response.json().get(
            'next_experiment').get('slug'), 'experiment4')

    def test_experiment_collection_with_dashboard(self):
        # if ExperimentCollection has dashboard set True, return list of random experiments
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()
        Session.objects.create(
            experiment=self.experiment1,
            participant=self.participant,
            finished_at=timezone.now()
        )
        intermediate_group = ExperimentCollectionGroup.objects.get(
            name='intermediate'
        )
        intermediate_group.dashboard = True
        intermediate_group.save()
        # check that first_experiments is returned correctly
        response = self.client.get('/experiment/collection/test_series/')
        self.assertEqual(type(response.json().get('dashboard')), list)


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
