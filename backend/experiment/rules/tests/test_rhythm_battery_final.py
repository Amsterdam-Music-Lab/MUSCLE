from django.test import TestCase
from experiment.actions import Explainer
from experiment.models import Experiment, ExperimentTranslatedContent, Block
from experiment.rules.rhythm_battery_final import RhythmBatteryFinal
from django.core.files.uploadedfile import SimpleUploadedFile


class TestRhythmBatteryFinal(TestCase):
    @classmethod
    def setUpTestData(cls):
        Experiment.objects.create(
            slug="MARKDOWN_EXPERIMENT",
        )
        ExperimentTranslatedContent.objects.create(
            experiment=Experiment.objects.get(slug="MARKDOWN_EXPERIMENT"),
            language="en",
            consent=SimpleUploadedFile("consent.md", b"# test", content_type="text/html"),
        )
        Block.objects.create(
            name="test_md",
            slug="MARKDOWN",
        )

    def test_init(self):
        rhythm_final = RhythmBatteryFinal()
        self.assertEqual(rhythm_final.ID, "RHYTHM_BATTERY_FINAL")

    def test_first_round(self):
        block = Block.objects.first()
        goldMSI = RhythmBatteryFinal()
        actions = goldMSI.first_round(block)

        self.assertIsInstance(actions[0], Explainer)
