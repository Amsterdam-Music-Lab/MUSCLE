from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from experiment.models import (
    Block,
    BlockTranslatedContent,
    Experiment,
    ExperimentTranslatedContent,
    Phase,
)
from experiment.serializers import get_upcoming_block, serialize_block, serialize_phase
from experiment.tests.test_views import create_theme_config
from image.models import Image
from participant.models import Participant
from session.models import Session


class SerializerTest(TestCase):
    fixtures = ["playlist", "experiment"]

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        cls.experiment = Experiment.objects.get(slug="rhythm_battery")
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
        phase = serialize_phase(self.phase1, self.participant, 0)
        self.assertIsNotNone(phase)
        next_block_slug = phase.get("nextBlock").get("slug")
        self.assertEqual(phase.get("dashboard"), [])
        self.assertEqual(next_block_slug, "rhythm_intro")
        self.assertEqual(phase.get("totalScore"), 0)
        Session.objects.create(
            participant=self.participant,
            block=Block.objects.get(slug=next_block_slug),
            finished_at=timezone.now(),
        )
        phase = serialize_phase(self.phase1, self.participant, 0)
        self.assertIsNone(phase)

    def test_upcoming_block(self):
        block = get_upcoming_block(self.phase1, self.participant, 0)
        self.assertEqual(block.get("slug"), "rhythm_intro")
        Session.objects.create(
            block=Block.objects.get(slug=block.get("slug")),
            participant=self.participant,
            finished_at=timezone.now(),
        )
        block = get_upcoming_block(self.phase1, self.participant, 0)
        self.assertIsNone(block)
        for i in range(3):
            block = get_upcoming_block(self.phase2, self.participant, 0)
            self.assertIsNotNone(block)
            self.assertIn(block.get("slug"), ["ddi", "hbat_bit", "rhdis"])
            Session.objects.create(
                block=Block.objects.get(slug=block.get("slug")),
                participant=self.participant,
                finished_at=timezone.now(),
            )
        block = get_upcoming_block(self.phase2, self.participant, 0)
        self.assertIsNone(block)
        block = get_upcoming_block(self.phase1, self.participant, 1)
        self.assertIsNotNone(block)

    def test_serialize_block(self):
        # Create a block
        block = Block.objects.create(
            slug="test-block",
            image=Image.objects.create(
                title="Test",
                description="",
                file="test-image.jpg",
                alt="Test",
                href="https://www.example.com",
                rel="",
                target="_self",
            ),
            theme_config=create_theme_config(),
            phase=self.phase1,
        )
        BlockTranslatedContent.objects.create(
            block=block,
            language="en",
            name="Test Block",
            description="This is a test block",
        )
        participant = Participant.objects.create()
        Session.objects.bulk_create(
            [
                Session(
                    block=block, participant=participant, finished_at=timezone.now()
                )
                for index in range(3)
            ]
        )

        # Call the serialize_block function
        serialized_block = serialize_block(block, participant)

        # Assert the serialized data
        self.assertEqual(serialized_block["slug"], "test-block")
        self.assertEqual(serialized_block["name"], "Test Block")
        self.assertEqual(serialized_block["description"], "This is a test block")
        self.assertEqual(
            serialized_block["image"],
            {
                "title": "Test",
                "description": "",
                "file": f"{settings.BASE_URL}/upload/test-image.jpg",
                "href": "https://www.example.com",
                "alt": "Test",
                "rel": "",
                "target": "_self",
                "tags": [],
            },
        )
