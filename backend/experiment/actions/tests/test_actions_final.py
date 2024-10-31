from django.test import TestCase

from experiment.models import (
    Block,
    BlockTranslatedContent,
    Experiment,
    ExperimentTranslatedContent,
    Phase,
    SocialMediaConfig,
)
from participant.models import Participant
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
            social_media_message="Ik heb {points} punten gescoord op {experiment_name}"
            language="nl",
            index=0,
        )
        phase = Phase.objects.create(experiment=cls.experiment)
        block = Block.objects.create(phase=phase, rules="HOOKED", rounds=6)
        BlockTranslatedContent.objects.create(
            block=block, name="Test block", language="en"
        )
        participant = Participant.objecs.create()
        cls.session = Session.objects.create(block=block, participant=participant)

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
        self.assertEqual(social_info.get("content"), "")
