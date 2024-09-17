from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from experiment.actions import Explainer
from experiment.models import Experiment, ExperimentTranslatedContent, Block
from experiment.rules.rhythm_battery_final import RhythmBatteryFinal
from participant.models import Participant
from section.models import Playlist
from session.models import Session


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
        block = Block.objects.create(slug="test_md", rules=RhythmBatteryFinal.ID)
        block.add_default_question_series()
        Session.objects.create(
            block=block, playlist=Playlist.objects.create(name="test"), participant=Participant.objects.create()
        )

    def test_init(self):
        rhythm_final = RhythmBatteryFinal()
        self.assertEqual(rhythm_final.ID, "RHYTHM_BATTERY_FINAL")

    def test_next_round(self):
        session = Session.objects.first()
        goldMSI = RhythmBatteryFinal()
        actions = goldMSI.next_round(session)

        self.assertIsInstance(actions[0], Explainer)
