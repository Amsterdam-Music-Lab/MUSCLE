from django.test import TestCase
from session.models import Session
from participant.models import Participant
from experiment.models import Block, Experiment, Phase


class TestModelBlock(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.block = Block.objects.create(
            rules="THATS_MY_SONG", slug="hooked", rounds=42
        )

    def test_separate_rules_instance(self):
        rules1 = self.block.get_rules()
        rules2 = self.block.get_rules()
        keys1 = rules1.question_series[0]["keys"] + rules1.question_series[1]["keys"]
        keys2 = rules2.question_series[0]["keys"] + rules2.question_series[1]["keys"]
        assert keys1 == keys2


class TestModelExperiment(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(name="test_experiment")
        cls.participant1 = Participant.objects.create(participant_id_url="001")
        cls.participant2 = Participant.objects.create(participant_id_url="002")
        cls.participant3 = Participant.objects.create(participant_id_url="003")

    def test_verbose_name_plural(self):
        # Get the Experiment Meta class
        meta = Experiment._meta
        # Check if verbose_name_plural is correctly set
        self.assertEqual(meta.verbose_name_plural, "Experiments")

    def test_associated_blocks(self):
        experiment = self.experiment
        phase1 = Phase.objects.create(experiment=experiment)
        phase2 = Phase.objects.create(experiment=experiment)
        Block.objects.bulk_create(
            [
                Block(rules="THATS_MY_SONG", slug="hooked", rounds=42, phase=phase1),
                Block(rules="THATS_MY_SONG", slug="unhinged", rounds=42, phase=phase2),
                Block(rules="THATS_MY_SONG", slug="derailed", rounds=42, phase=phase2),
            ]
        )
        self.assertEqual(experiment.associated_blocks().count(), 3)

    def test_associated_sessions(self):
        experiment = self.experiment
        phase = Phase.objects.create(experiment=experiment)
        block = Block.objects.create(
            rules="THATS_MY_SONG", slug="hooked", rounds=42, phase=phase
        )
        Session.objects.bulk_create(
            [
                Session(block=block, participant=self.participant1),
                Session(block=block, participant=self.participant2),
                Session(block=block, participant=self.participant3),
            ]
        )
        sessions = experiment.associated_sessions()
        self.assertEqual(len(sessions), 3)
