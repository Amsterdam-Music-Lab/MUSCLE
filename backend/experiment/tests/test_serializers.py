from django.test import TestCase
from django.utils import timezone

from experiment.models import Block, Experiment, Phase
from experiment.serializers import serialize_phase
from participant.models import Participant
from session.models import Session


class SerializerTest(TestCase):
    fixtures = ["playlist", "experiment"]

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.experiment = Experiment.objects.get(slug="RhythmTestSeries")
        cls.phase1 = Phase.objects.create(experiment=cls.experiment)
        block = Block.objects.get(slug="rhythm_intro")
        block.phase = cls.phase1
        block.save()
        cls.phase2 = Phase.objects.create(
            experiment=cls.experiment, index=1, randomize=True
        )
        block = Block.objects.get(slug="ddi")
        block.phase = cls.phase2
        block.save()
        block = Block.objects.get(slug="hbat_bit")
        block.phase = cls.phase2
        block.save()
        block = Block.objects.get(slug="rhdis")
        block.phase = cls.phase2
        block.save()
        cls.phase3 = Phase.objects.create(experiment=cls.experiment, index=2)
        block = Block.objects.get(slug="rhythm_outro")
        block.phase = cls.phase3
        block.save()

    def test_serialize_phase(self):
        for i in range(3):
            phase = serialize_phase(self.phase2, self.participant)
            next_block = phase.get("nextBlock")
            self.assertIsNotNone(next_block)
            self.assertIn(next_block.get("slug"), ["ddi", "hbat_bit", "rhdis"])
            block_obj = Block.objects.get(slug=next_block.get("slug"))
            Session.objects.create(
                block=block_obj,
                participant=self.participant,
                finished_at=timezone.now(),
            )
        phase = serialize_phase(self.phase2, self.participant)
        self.assertIsNone(phase)
        # if we enter the phase once more, we're going to get next_block again
        phase = serialize_phase(self.phase2, self.participant)
        self.assertIsNotNone(phase)
        next_block = phase.get("nextBlock")
        self.assertIsNotNone(next_block)
        self.assertIn(next_block.get("slug"), ["ddi", "hbat_bit", "rhdis"])
