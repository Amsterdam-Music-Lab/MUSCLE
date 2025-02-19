from django.test import TestCase
from django.utils.translation import activate

from experiment.models import (
    Block,
    BlockTranslatedContent,
    Experiment,
    ExperimentTranslatedContent,
    Phase,
    SocialMediaConfig,
)
from participant.models import Participant
from result.models import Result
from session.models import Session

from experiment.actions import Final


class FinalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(
            slug="final_countdown",
        )
        ExperimentTranslatedContent.objects.create(
            experiment=cls.experiment, name="Final Countdown", language="en", index=1
        )
        ExperimentTranslatedContent.objects.create(
            experiment=cls.experiment,
            name="Laatste Telaf",
            social_media_message="Ik heb {points} punten gescoord op {experiment_name}. Kan jij het beter?",
            language="nl",
            index=0,
        )
        phase = Phase.objects.create(experiment=cls.experiment)
        block = Block.objects.create(phase=phase, rules="HOOKED", rounds=6)
        BlockTranslatedContent.objects.create(block=block, name="Test block", language="en")
        participant = Participant.objects.create()
        cls.session = Session.objects.create(block=block, participant=participant)
        Result.objects.create(session=cls.session, score=28)
        Result.objects.create(session=cls.session, score=14)

    def test_final_action_without_social(self):
        final = Final(self.session)
        serialized = final.action()
        self.assertEqual(serialized.get("title"), "Final score")
        self.assertIsNone(serialized.get("social"))

    def test_final_action_with_social(self):
        SocialMediaConfig.objects.create(
            experiment=self.experiment,
            channels=["Facebook"],
            tags=["amazing"],
            url="example.com",
        )
        final = Final(self.session)
        serialized = final.action()
        social_info = serialized.get("social")
        self.assertIsNotNone(social_info)
        self.assertEqual(social_info.get("channels"), ["Facebook"])
        self.assertEqual(social_info.get("url"), "example.com")
        self.assertEqual(social_info.get("tags"), ["amazing"])
        self.assertEqual(
            social_info.get("content"),
            "Ik heb 42.0 punten gescoord op Laatste Telaf. Kan jij het beter?",
        )
        activate("en")
        final = Final(self.session)
        serialized = final.action()
        social_info = serialized.get("social")
        self.assertEqual(social_info.get("content"), "I scored 42.0 points in Final Countdown!")

    def test_final_action_with_percentile_disabled(self):
        final = Final(self.session)
        final.percentile = 85.0
        serialized = final.action()
        self.assertEqual(serialized.get("percentile"), 85.0)

    def test_final_action_with_percentile_ranges(self):
        test_cases = [95.0, 85.0, 65.0, 45.0, 25.0, 5.0]
        for percentile in test_cases:
            with self.subTest(percentile=percentile):
                final = Final(self.session)
                final.percentile = percentile
                serialized = final.action()
                self.assertIn("percentile", serialized)
                self.assertEqual(serialized["percentile"], percentile)

    def test_final_action_with_percentile(self):
        final = Final(self.session)
        final.percentile = 85.0
        serialized = final.action()
        self.assertIn("percentile", serialized)
        self.assertIn("rank", serialized)

    def test_wrap_final_text(self):
        final = Final(self.session)
        final.final_text = 'plain text'
        serialized = final.action()
        self.assertEqual(serialized.get('final_text'), '<center>plain text</center>')
        final.final_text = '<p>wrapped text</p>'
        serialized = final.action()
        self.assertEqual(serialized.get('final_text'), final.final_text)
