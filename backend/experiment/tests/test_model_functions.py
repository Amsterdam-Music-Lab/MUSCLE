from django.test import TestCase
from experiment.models import Experiment, ExperimentCollection, ExperimentCollectionGroup, GroupedExperiment
from session.models import Session
from participant.models import Participant


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


class TestModelExperimentCollection(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.collection = ExperimentCollection.objects.create(name='collection')
        cls.participant1 = Participant.objects.create(participant_id_url='001')
        cls.participant2 = Participant.objects.create(participant_id_url='002')
        cls.participant3 = Participant.objects.create(participant_id_url='003')

    def test_verbose_name_plural(self):
        # Get the ExperimentCollection Meta class
        meta = ExperimentCollection._meta
        # Check if verbose_name_plural is correctly set
        self.assertEqual(meta.verbose_name_plural, "Experiment Collections")

    def test_associated_experiments(self):
        collection = self.collection
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

    def test_export_sessions(self):
        collection = self.collection
        group = ExperimentCollectionGroup.objects.create(
            name='test', series=collection)
        experiment = Experiment.objects.create(
            rules='THATS_MY_SONG', slug='hooked', rounds=42)
        GroupedExperiment.objects.create(
            experiment=experiment, group=group)
        Session.objects.bulk_create(
            [Session(experiment=experiment, participant=self.participant1),
             Session(experiment=experiment, participant=self.participant2),
             Session(experiment=experiment, participant=self.participant3)]
             )
        sessions = collection.export_sessions()
        self.assertEqual(len(sessions), 3)

    def test_current_participants(self):
        collection = self.collection
        group = ExperimentCollectionGroup.objects.create(
            name='test', series=collection)
        experiment = Experiment.objects.create(
            rules='THATS_MY_SONG', slug='hooked', rounds=42)
        GroupedExperiment.objects.create(
            experiment=experiment, group=group)
        Session.objects.bulk_create(
            [Session(experiment=experiment, participant=self.participant1),
             Session(experiment=experiment, participant=self.participant2),
             Session(experiment=experiment, participant=self.participant3)]
             )
        participants = collection.current_participants()
        self.assertEqual(len(participants), 3)
