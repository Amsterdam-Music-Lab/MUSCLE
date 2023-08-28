from django.test import TestCase
from experiment.models import Experiment

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
