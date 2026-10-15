from django.test import TestCase

from experiment.models import Block, Experiment, Phase, Progress, Ranking
from participant.models import Participant


class TestModelBlock(TestCase):
    fixtures = [
        "choice_lists",
        "demographics",
        "goldsmiths_msi",
        "musicgens",
        "vanderbilt",
        "thats_my_song",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.block = Block.objects.get(identifier="thats_my_song")


class TestModelExperiment(TestCase):
    fixtures = ["ranking_toontjehoger", "toontjehoger"]

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
                Block(
                    rules="THATS_MY_SONG",
                    identifier="hooked",
                    rounds=42,
                    phase=phase1,
                    experiment=experiment,
                ),
                Block(
                    rules="THATS_MY_SONG",
                    identifier="unhinged",
                    rounds=42,
                    phase=phase2,
                    experiment=experiment,
                ),
                Block(
                    rules="THATS_MY_SONG",
                    identifier="derailed",
                    rounds=42,
                    phase=phase2,
                    experiment=experiment,
                ),
            ]
        )
        self.assertEqual(experiment.associated_blocks().count(), 3)

    def test_get_active_rank(self):
        experiment = Experiment.objects.get(identifier="toontjehoger")
        scores = {"accumulative_score": 400}
        self.assertEqual(experiment.get_active_rank(scores).label, "gold")


class RankingModelTest(TestCase):
    fixtures = ["eurovision_2020", "ranking_hooked"]

    def test_get_active_rank(self):
        ranking = Ranking.objects.get(identifier="hooked-ranking")
        self.assertEqual(ranking.get_active_rank(98.0).label, "diamond")
        self.assertEqual(ranking.get_active_rank(90.0).label, "platinum")
        self.assertEqual(ranking.get_active_rank(80.0).label, "gold")
        self.assertEqual(ranking.get_active_rank(40.0).label, "silver")
        self.assertEqual(ranking.get_active_rank(20.0).label, "bronze")
        self.assertEqual(ranking.get_active_rank(-1.0).label, "plastic")

