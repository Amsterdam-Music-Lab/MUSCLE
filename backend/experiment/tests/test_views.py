from django.test import TestCase

from experiment.models import Experiment, ExperimentSeries


class TestExperimentViews(TestCase):

    def test_get_experiment_collection(self):
        experiment1 = Experiment.objects.create(
            name='experiment1', slug='experiment1')
        experiment2 = Experiment.objects.create(
            name='experiment2', slug='experiment2')
        experiment3 = Experiment.objects.create(
            name='experiment1', slug='experiment3')
        experiment4 = Experiment.objects.create(
            name='experiment2', slug='experiment4')
        collection = ExperimentSeries.objects.create(
            slug='series_test',
            first_experiments=[experiment1.pk],
            random_experiments=[experiment2.pk, experiment3.pk],
            last_experiments=[experiment4.pk]
        )
