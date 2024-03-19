from django.test import TestCase
from django.utils import timezone

from experiment.models import Experiment, ExperimentSeries
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
