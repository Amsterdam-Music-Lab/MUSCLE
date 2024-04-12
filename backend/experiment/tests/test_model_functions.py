from django.test import TestCase
from experiment.models import Experiment, ExperimentSeries


class TestModelExperiment(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(rules='THATS_MY_SONG', slug='hooked', rounds=42)

    def test_separate_rules_instance(self):
        rules1 = self.experiment.get_rules()
        rules2 = self.experiment.get_rules()
        keys1 = rules1.question_series[0]['keys'] + rules1.question_series[1]['keys']
        keys2 = rules2.question_series[0]['keys'] + rules2.question_series[1]['keys']
        assert keys1 == keys2


class TestModelExperimentSeries(TestCase):

    def test_verbose_name_plural(self):
        # Get the ExperimentSeries Meta class
        meta = ExperimentSeries._meta
        # Check if verbose_name_plural is correctly set
        self.assertEqual(meta.verbose_name_plural, "Experiment Series")
