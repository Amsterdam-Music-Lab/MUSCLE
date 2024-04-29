from django.test import TestCase
from experiment.models import Experiment, ExperimentCollection, ExperimentCollectionGroup, GroupedExperiment


class TestModelExperiment(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(rules='THATS_MY_SONG', slug='hooked', rounds=42)

    def test_separate_rules_instance(self):
        rules1 = self.experiment.get_rules()
        rules2 = self.experiment.get_rules()
        keys1 = [q.key for q in rules1.questions]
        keys2 = [q.key for q in rules2.questions]
        assert keys1 != keys2


class TestModelExperimentCollection(TestCase):

    def test_verbose_name_plural(self):
        # Get the ExperimentCollection Meta class
        meta = ExperimentCollection._meta
        # Check if verbose_name_plural is correctly set
        self.assertEqual(meta.verbose_name_plural, "Experiment Collections")

    def test_associated_experiments(self):
        collection = ExperimentCollection.objects.create(name='collection')
        group1 = ExperimentCollectionGroup.objects.create(
            name='first_phase', series=collection)
        group2 = ExperimentCollectionGroup.objects.create(
            name='second_phase', series=collection)
        experiment = Experiment.objects.create(
            rules='THATS_MY_SONG', slug='hooked', rounds=42)
        experiment2 = Experiment.objects.create(
            rules='THATS_MY_SONG', slug='unhinged', rounds=42)
        experiment3 = Experiment.objects.create(
            rules='THATS_MY_SONG', slug='derailed', rounds=42)
        GroupedExperiment.objects.create(
            experiment=experiment, group=group1)
        GroupedExperiment.objects.create(
            experiment=experiment2, group=group2)
        GroupedExperiment.objects.create(
            experiment=experiment3, group=group2)
        self.assertEqual(collection.associated_experiments(), [
                         experiment, experiment2, experiment3])
