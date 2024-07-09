from django.test import TestCase

from image.models import Image
from theme.models import ThemeConfig
from experiment.models import Block, ExperimentCollection
from participant.models import Participant
from session.models import Session
from result.models import Result


class BlockModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        logo_image = Image.objects.create(
            file='logoimage.svg'
        )
        background_image = Image.objects.create(
            file='backgroundimage.tif'
        )
        ThemeConfig.objects.create(
            name='Default',
            description='Default theme configuration',
            heading_font_url='https://example.com/heading_font',
            body_font_url='https://example.com/body_font',
            logo_image=logo_image,
            background_image=background_image,
        )
        Block.objects.create(
            name='Test Block',
            description='Test block description',
            slug='test-block',
            url='https://example.com/block',
            hashtag='test',
            rounds=5,
            bonus_points=10,
            rules='RHYTHM_BATTERY_FINAL',
            language='en',
            theme_config=ThemeConfig.objects.get(name='Default'),
        )

    def test_block_str(self):
        block = Block.objects.get(name='Test Block')
        self.assertEqual(str(block), 'Test Block')

    def test_block_session_count(self):
        block = Block.objects.get(name='Test Block')
        self.assertEqual(block.session_count(), 0)

    def test_block_playlist_count(self):
        block = Block.objects.get(name='Test Block')
        self.assertEqual(block.playlist_count(), 0)

    def test_block_current_participants(self):
        block = Block.objects.get(name='Test Block')
        participants = block.current_participants()
        self.assertEqual(len(participants), 0)

    def test_block_export_admin(self):
        block = Block.objects.get(name='Test Block')
        exported_data = block.export_admin()
        self.assertEqual(exported_data['block']['name'], 'Test Block')

    def test_block_export_sessions(self):
        block = Block.objects.get(name='Test Block')
        sessions = block.export_sessions()
        self.assertEqual(len(sessions), 0)

    def test_block_export_table(self):
        block = Block.objects.get(name='Test Block')
        amount_of_sessions = 3

        for i in range(amount_of_sessions):
            session = Session.objects.create(
                block=block,
                participant=Participant.objects.create()
            )
            Result.objects.create(
                session=session,
                expected_response=1,
                given_response=1,
                question_key='test_question_1',
            )

        session_keys = ['block_id', 'block_name']
        result_keys = ['section_name', 'result_created_at']
        export_options = {'wide_format': True}
        rows, fieldnames = block.export_table(
            session_keys,
            result_keys,
            export_options
        )

        self.assertEqual(len(rows), amount_of_sessions)
        self.assertEqual(len(fieldnames), len(session_keys) + len(result_keys))

    def test_block_get_rules(self):
        block = Block.objects.get(name='Test Block')
        rules = block.get_rules()
        self.assertIsNotNone(rules)

    def test_block_max_score(self):
        block = Block.objects.get(name='Test Block')

        amount_of_results = 3
        question_score = 1

        session = Session.objects.create(
            block=block,
            participant=Participant.objects.create()
        )
        for j in range(amount_of_results):
            Result.objects.create(
                session=session,
                expected_response=1,
                given_response=1,
                score=question_score,
                question_key=f'test_question_{j + 1}',
            )
        session.finish()
        session.save()

        question_scores = amount_of_results * question_score
        bonus_points = block.bonus_points
        max_score = block.max_score()
        self.assertEqual(max_score, question_scores + bonus_points)
        self.assertEqual(max_score, 13.0)


class ExperimentCollectionModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.experiment_series = ExperimentCollection.objects.create(
            slug='test-series',
            name='Test Series',
            description='Test series description with a very long description. From here to the moon and from the moon to the stars.',
        )

    def test_experiment_series_str(self):
        experiment_series_no_name = ExperimentCollection.objects.create(
            slug='test-series-no-name',
        )

        self.assertEqual(str(self.experiment_series), 'Test Series')
        self.assertEqual(str(experiment_series_no_name), 'test-series-no-name')
