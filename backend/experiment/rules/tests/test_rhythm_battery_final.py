from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from experiment.actions import Explainer
from experiment.models import Block
from experiment.rules.rhythm_battery_final import RhythmBatteryFinal


class TestRhythmBatteryFinal(TestCase):
    @classmethod
    def setUpTestData(cls):
        Block.objects.create(
            name='test_md',
            slug='MARKDOWN',
            consent=SimpleUploadedFile(
                'consent.md', b'# test', content_type='text/html')
        )

    def test_init(self):
        rhythm_final = RhythmBatteryFinal()
        self.assertEqual(rhythm_final.ID, 'RHYTHM_BATTERY_FINAL')

    def test_first_round(self):
        block = Block.objects.first()
        goldMSI = RhythmBatteryFinal()
        actions = goldMSI.first_round(block)

        self.assertIsInstance(actions[0], Explainer)
