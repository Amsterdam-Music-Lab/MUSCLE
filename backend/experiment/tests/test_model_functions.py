from django.test import TestCase

from experiment.models import Block, Experiment, Phase
from participant.models import Participant
from question.models import QuestionInList, QuestionList
from session.models import Session


class TestModelBlock(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.block = Block.objects.create(
            rules="THATS_MY_SONG", slug="hooked", rounds=42
        )

    def test_separate_rules_instance(self):
        rules1 = self.block.get_rules()
        rules2 = self.block.get_rules()
        keys1 = (
            rules1.question_lists[0]["question_keys"]
            + rules1.question_lists[1]["question_keys"]
        )
        keys2 = (
            rules2.question_lists[0]["question_keys"]
            + rules2.question_lists[1]["question_keys"]
        )
        assert keys1 == keys2

    def test_add_default_question_lists(self):
        block = Block(
            name='test question list',
            slug='test_question_list',
            rules='RHYTHM_BATTERY_FINAL',
        )
        block.save()  # triggers `add_default_question_lists` method
        created_lists = QuestionList.objects.filter(block=block)
        n_lists = created_lists.count()
        expected_n = len(block.get_rules().question_lists)
        self.assertEqual(
            n_lists,
            expected_n,
        )
        self.assertNotEqual(
            QuestionInList.objects.filter(questionlist=created_lists.first()).count(),
            0,
        )
        # test that question series aren't created more than once
        block.save()
        created_series = QuestionList.objects.filter(block=block)
        self.assertEqual(created_series.count(), n_lists)


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
