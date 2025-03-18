from django.test import TestCase

from image.models import Image
from theme.models import ThemeConfig
from experiment.models import (
    Block,
    BlockText,
    Experiment,
    ExperimentText,
    Phase,
)
from participant.models import Participant
from session.models import Session
from result.models import Result


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
        experiment = Experiment.objects.create(slug="test-experiment")
        ExperimentText.objects.create(experiment=experiment, name="Experiment name")
        cls.phase = Phase.objects.create(experiment=experiment)
        block = Block.objects.create(
            phase=cls.phase,
            slug="test-block",
            rounds=5,
            bonus_points=10,
            rules="RHYTHM_BATTERY_FINAL",
            theme_config=ThemeConfig.objects.get(name="Default"),
        )
        BlockText.objects.create(
            block=block,
            name="Test Block",
            description="Test block description",
        )

    def test_block_str(self):
        block = Block.objects.get(slug="test-block")
        self.assertEqual(str(block), "Test Block")

    def test_block_str_without_content(self):
        block_no_content = Block.objects.create(
            phase=self.phase, slug="test-block-no-content"
        )
        self.assertEqual(str(block_no_content), "test-block-no-content")

    def test_block_str_without_pk(self):
        block_no_pk = Block.objects.create(phase=self.phase)
        BlockText.objects.create(
            block=block_no_pk,
            name="Not yet deleted test block",
            description="Deleted test block description",
        )
        self.assertEqual(str(block_no_pk), "Not yet deleted test block")
        block_no_pk.delete()
        self.assertEqual(str(block_no_pk), "Deleted/Unsaved Block")

    def test_block_session_count(self):
        block = Block.objects.get(slug="test-block")
        self.assertEqual(block.session_count(), 0)

    def test_block_playlist_count(self):
        block = Block.objects.get(slug="test-block")
        self.assertEqual(block.playlist_count(), 0)

    def test_block_current_participants(self):
        block = Block.objects.get(slug="test-block")
        participants = block.current_participants()
        self.assertEqual(len(participants), 0)

    def test_block_export_admin(self):
        block = Block.objects.get(slug="test-block")
        exported_data = block._export_admin()
        self.assertEqual(exported_data["block"]["name"], "Test Block")

    def test_block_export_sessions(self):
        block = Block.objects.get(slug="test-block")
        sessions = block.export_sessions()
        self.assertEqual(len(sessions), 0)

    def test_block_export_table(self):
        block = Block.objects.get(slug="test-block")
        amount_of_sessions = 3

        for i in range(amount_of_sessions):
            session = Session.objects.create(
                block=block, participant=Participant.objects.create()
            )
            Result.objects.create(
                session=session,
                expected_response=1,
                given_response=1,
                question_key="test_question_1",
            )

        session_keys = ["block_id", "block_name"]
        result_keys = ["section_name", "result_created_at"]
        export_options = {"wide_format": True}
        rows, fieldnames = block.export_table(session_keys, result_keys, export_options)

        self.assertEqual(len(rows), amount_of_sessions)
        self.assertEqual(len(fieldnames), len(session_keys) + len(result_keys))

    def test_block_get_rules(self):
        block = Block.objects.get(slug="test-block")
        rules = block.get_rules()
        self.assertIsNotNone(rules)

    def test_block_max_score(self):
        block = Block.objects.get(slug="test-block")

        amount_of_results = 3
        question_score = 1

        session = Session.objects.create(
            block=block, participant=Participant.objects.create()
        )
        for j in range(amount_of_results):
            Result.objects.create(
                session=session,
                expected_response=1,
                given_response=1,
                score=question_score,
                question_key=f"test_question_{j + 1}",
            )
        session.finish()
        session.save()

        question_scores = amount_of_results * question_score
        bonus_points = block.bonus_points
        max_score = block.max_score()
        self.assertEqual(max_score, question_scores + bonus_points)
        self.assertEqual(max_score, 13.0)


class ExperimentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(
            slug="test-series",
        )
        ExperimentText.objects.create(
            experiment=cls.experiment,
            name="Experimento de Prueba",
            description="Descripción de la experimento de prueba en español.",
        )

    def test_experiment_str(self):
        self.assertEqual(str(self.experiment), "Test Experiment")

        experiment_no_content = Experiment.objects.create(
            slug="test-series-no-content",
        )
        self.assertEqual(str(experiment_no_content), "test-series-no-content")
