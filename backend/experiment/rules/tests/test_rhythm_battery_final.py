from django.test import TestCase

from experiment.actions.explainer import Explainer
from experiment.models import Experiment, Block
from experiment.rules.rhythm_battery_final import RhythmBatteryFinal
from participant.models import Participant
from section.models import Playlist
from session.models import Session


class TestRhythmBatteryFinal(TestCase):
    fixtures = ["choice_lists", "demographics", "goldsmiths_msi"]

    @classmethod
    def setUpTestData(cls):
        Experiment.objects.create(
            slug="MARKDOWN_EXPERIMENT",
        )
        block = Block.objects.create(slug="test_md", rules=RhythmBatteryFinal.ID)
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
