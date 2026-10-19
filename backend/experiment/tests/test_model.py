from django.test import TestCase

from image.models import Image
from theme.models import ThemeConfig
from experiment.models import (
    Block,
    Experiment,
    Phase,
)
from participant.models import Participant
from session.models import Session

class BlockModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        logo_image = Image.objects.create(file="logoimage.svg")
        background_image = Image.objects.create(file="backgroundimage.tif")
        ThemeConfig.objects.create(
            name="Default",
            description="Default theme configuration",
            heading_font_url="https://example.com/heading_font",
            body_font_url="https://example.com/body_font",
            logo_image=logo_image,
            background_image=background_image,
        )
        experiment = Experiment.objects.create(
            identifier="test-experiment", name="Experiment name"
        )
        cls.phase = Phase.objects.create(experiment=experiment)
        cls.block = Block.objects.create(
            phase=cls.phase,
            identifier="test-block",
            rounds=5,
            bonus_points=10,
            rules="QUESTIONNAIRE",
            theme_config=ThemeConfig.objects.get(name="Default"),
            name="Test Block",
            description="Test block description",
        )
        Session.objects.create(
            block=cls.block, participant=Participant.objects.create()
        )

    def test_block_str(self):
        self.assertEqual(str(self.block), "Test Block")

    def test_block_str_without_content(self):
        block_no_content = Block.objects.create(
            phase=self.phase, identifier="test-block-no-content", rules="QUESTIONNAIRE"
        )
        self.assertEqual(str(block_no_content), "test-block-no-content")

    def test_block_session_count(self):
        self.assertEqual(self.block.session_count(), 1)

    def test_block_playlist_count(self):
        self.assertEqual(self.block.playlist_count(), 0)

    def test_block_get_rules(self):
        rules = self.block.get_rules()
        self.assertIsNotNone(rules)


class ExperimentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(
            identifier="test-series",
            name="Test Experiment",
            name_pt="Experimento de Prueba",
            description="Descripción de la experimento de prueba en español.",
        )

    def test_experiment_str(self):
        self.assertEqual(str(self.experiment), "Test Experiment")

        experiment_no_content = Experiment.objects.create(
            identifier="test-series-no-content",
        )
        self.assertEqual(str(experiment_no_content), "test-series-no-content")
