from django.test import TestCase
from session.models import Session
from participant.models import Participant
from experiment.models import Block, Experiment, Phase, GroupedBlock


class TestModelBlock(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.block = Block.objects.create(rules='THATS_MY_SONG', slug='hooked', rounds=42)

    def test_separate_rules_instance(self):
        rules1 = self.block.get_rules()
        rules2 = self.block.get_rules()
        keys1 = rules1.question_series[0]['keys'] + rules1.question_series[1]['keys']
        keys2 = rules2.question_series[0]['keys'] + rules2.question_series[1]['keys']
        assert keys1 == keys2


class TestModelExperiment(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(name='experiment')
        cls.participant1 = Participant.objects.create(participant_id_url='001')
        cls.participant2 = Participant.objects.create(participant_id_url='002')
        cls.participant3 = Participant.objects.create(participant_id_url='003')

    def test_verbose_name_plural(self):
        # Get the Experiment Meta class
        meta = Experiment._meta
        # Check if verbose_name_plural is correctly set
        self.assertEqual(meta.verbose_name_plural, "Experiments")

    def test_associated_blocks(self):
        experiment = self.experiment
        phase1 = Phase.objects.create(
            name='first_phase', series=experiment)
        phase2 = Phase.objects.create(
            name='second_phase', series=experiment)
        block = Block.objects.create(
            rules='THATS_MY_SONG', slug='hooked', rounds=42)
        block2 = Block.objects.create(
            rules='THATS_MY_SONG', slug='unhinged', rounds=42)
        block3 = Block.objects.create(
            rules='THATS_MY_SONG', slug='derailed', rounds=42)
        GroupedBlock.objects.create(
            block=block, phase=phase1)
        GroupedBlock.objects.create(
            block=block2, phase=phase2)
        GroupedBlock.objects.create(
            block=block3, phase=phase2)
        self.assertEqual(experiment.associated_blocks(), [
                         block, block2, block3])

    def test_export_sessions(self):
        experiment = self.experiment
        phase = Phase.objects.create(
            name='test', series=experiment)
        block = Block.objects.create(
            rules='THATS_MY_SONG', slug='hooked', rounds=42)
        GroupedBlock.objects.create(
            block=block, phase=phase)
        Session.objects.bulk_create(
            [Session(block=block, participant=self.participant1),
             Session(block=block, participant=self.participant2),
             Session(block=block, participant=self.participant3)]
             )
        sessions = experiment.export_sessions()
        self.assertEqual(len(sessions), 3)

    def test_current_participants(self):
        experiment = self.experiment
        phase = Phase.objects.create(
            name='test', series=experiment)
        block = Block.objects.create(
            rules='THATS_MY_SONG', slug='hooked', rounds=42)
        GroupedBlock.objects.create(
            block=block, phase=phase)
        Session.objects.bulk_create(
            [Session(block=block, participant=self.participant1),
             Session(block=block, participant=self.participant2),
             Session(block=block, participant=self.participant3)]
             )
        participants = experiment.current_participants()
        self.assertEqual(len(participants), 3)
