from django.test import TestCase
from django.utils import timezone

from experiment.models import Block, Experiment, Phase, Rank, Ranking, Timeline
from participant.models import Participant
from session.models import Session

class TestModelBlock(TestCase):
    fixtures = [
        "choice_lists",
        "demographics",
        "goldsmiths_msi",
        "musicgens",
        "vanderbilt",
        "hooked",
        "conditions",
        "rankings",
        "thats_my_song",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.block = Block.objects.get(identifier="thats_my_song")


class TestModelExperiment(TestCase):
    fixtures = ["conditions", "rankings", "toontjehoger"]

    def test_verbose_name_plural(self):
        # Get the Experiment Meta class
        meta = Experiment._meta
        # Check if verbose_name_plural is correctly set
        self.assertEqual(meta.verbose_name_plural, "Experiments")

    def test_associated_blocks(self):
        experiment = Experiment.objects.create(name="test_experiment")
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

    def test_is_replayable(self):
        experiment = Experiment.objects.first()
        participant = Participant.objects.create()
        self.assertFalse(experiment.is_finished(participant))
        blocks = experiment.associated_blocks()
        Session.objects.bulk_create(
            [
                Session(
                    block=block, participant=participant, finished_at=timezone.now()
                )
                for block in blocks
            ]
        )
        self.assertFalse(experiment.is_finished(participant))
        experiment.replayable = False
        experiment.save()
        self.assertTrue(experiment.is_finished(participant))

    def test_get_played_sessions_count(self):
        participant = Participant.objects.create()
        Session.objects.bulk_create(
            [
                Session(
                    block=block,
                    participant=participant,
                    finished_at=timezone.now(),
                )
                for block in Block.objects.all()
            ]
            * 2
        )
        experiment = Experiment.objects.first()
        played_sessions = experiment.get_played_sessions_count(participant)
        self.assertEqual(played_sessions, Block.objects.count() * 2)

    def test_get_played_sessions_count_no_duplicates(self):
        participant = Participant.objects.create()
        Session.objects.bulk_create(
            [
                Session(
                    block=block,
                    participant=participant,
                    finished_at=timezone.now(),
                )
                for block in Block.objects.all()
            ]
            * 2
        )
        experiment = Experiment.objects.first()
        played_sessions = experiment.get_played_sessions_count(
            participant, remove_duplicates=True
        )
        self.assertEqual(played_sessions, Block.objects.count())


class RankingModelTest(TestCase):
    fixtures = ["conditions", "rankings", "hooked", "eurovision_2020"]

    def test_get_active_rank(self):
        ranking = Ranking.objects.get(identifier="hooked-ranking")
        self.assertEqual(ranking.get_active_rank({"percentile": 98.0}).label, "diamond")
        self.assertEqual(
            ranking.get_active_rank({"percentile": 90.0}).label, "platinum"
        )
        self.assertEqual(ranking.get_active_rank({"percentile": 80.0}).label, "gold")
        self.assertEqual(ranking.get_active_rank({"percentile": 40.0}).label, "silver")
        self.assertEqual(ranking.get_active_rank({"percentile": 20.0}).label, "bronze")
        self.assertEqual(ranking.get_active_rank({}).label, "plastic")


class TimelineModelTest(TestCase):
    fixtures = [
        "choice_lists",
        "demographics",
        "conditions",
        "rankings",
        "matching_pairs_2025",
    ]

    def test_to_dict(self):
        timeline = Timeline.objects.first()
        steps = timeline.to_dict().get('steps')
        self.assertEqual(len(steps), 12)
        self.assertEqual([s["image"] for s in steps[:3]], ["", "", "star"])
        self.assertEqual([s["image"] for s in steps[9:12]], ["", "", "cup"])
