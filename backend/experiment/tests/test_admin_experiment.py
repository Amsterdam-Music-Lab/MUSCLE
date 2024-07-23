from zipfile import ZipFile
from io import BytesIO
import json
from django.test import Client, TestCase, RequestFactory
from django.forms.models import model_to_dict
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.utils.html import format_html
from experiment.admin import BlockAdmin, ExperimentAdmin, PhaseAdmin
from experiment.models import Block, Experiment, Phase, GroupedBlock
from participant.models import Participant
from result.models import Result
from session.models import Session


# Expected field count per model
EXPECTED_BLOCK_FIELDS = 15
EXPECTED_SESSION_FIELDS = 9
EXPECTED_RESULT_FIELDS = 12
EXPECTED_PARTICIPANT_FIELDS = 5


class MockRequest:
    pass


request = MockRequest()


class TestAdminBlock(TestCase):

    @classmethod
    def setUpTestData(cls):
        Block.objects.create(
                    name='test',
                    slug='TEST'
                )
        Participant.objects.create()
        Session.objects.create(
            block=Block.objects.first(),
            participant=Participant.objects.first()
        )
        Result.objects.create(
            session=Session.objects.first()
        )

    def setUp(self):
        self.admin = BlockAdmin(
            model=Block,
            admin_site=AdminSite,
            )

    def test_block_model_fields(self):
        block = model_to_dict(Block.objects.first())
        block_fields = [key for key in block]
        self.assertEqual(len(block_fields), EXPECTED_BLOCK_FIELDS)

    def test_session_model_fields(self):
        session = model_to_dict(Session.objects.first())
        session_fields = [key for key in session]
        self.assertEqual(len(session_fields), EXPECTED_SESSION_FIELDS)

    def test_result_model_fields(self):
        result = model_to_dict(Result.objects.first())
        result_fields = [key for key in result]
        self.assertEqual(len(result_fields), EXPECTED_RESULT_FIELDS)

    def test_participant_model(self):
        participant = model_to_dict(Participant.objects.first())
        participant_fields = [key for key in participant]
        self.assertEqual(len(participant_fields), EXPECTED_PARTICIPANT_FIELDS)

    def test_block_link(self):
        block = Block.objects.create(name="Test Block")
        site = AdminSite()
        admin = BlockAdmin(block, site)
        link = admin.block_name_link(block)
        expected_url = reverse(
            "admin:experiment_block_change", args=[block.pk])
        expected_name = "Test Block"
        expected_link = format_html(
            '<a href="{}">{}</a>', expected_url, expected_name)
        self.assertEqual(link, expected_link)

    def test_block_slug_link(self):
        block = Block.objects.create(name="Test Block", slug="test-block")
        site = AdminSite()
        admin = BlockAdmin(block, site)
        link = admin.block_slug_link(block)

        expected_link = '<a href="/block/test-block" target="_blank" rel="noopener noreferrer" title="Open test-block block in new tab" >test-block&nbsp;<small>&#8599;</small></a>'
        self.assertEqual(link, expected_link)


class TestAdminBlockExport(TestCase):

    fixtures = ['playlist', 'experiment']

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.get(name='Hooked-China')
        for playlist in cls.block.playlists.all():
            playlist.update_sections()
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
        )
        for i in range(5):
            Result.objects.create(
                session=Session.objects.first(),
                expected_response = i,
                given_response = i,
                question_key = 'test_question_' + str(i),
            )
            Result.objects.create(
                participant=cls.participant,
                question_key= i,
                given_response = i,
            )

    def setUp(self):
        self.client = Client()
        self.admin = BlockAdmin(
            model=Block,
            admin_site=AdminSite
            )

    def test_admin_export(self):
        response = self.admin.export(request, self.block)
        zip_buffer = BytesIO(response.content)
        with ZipFile(zip_buffer, 'r') as test_zip:
            # Test files inside zip
            self.assertIn('participants.json', test_zip.namelist())
            self.assertIn('profiles.json', test_zip.namelist())
            self.assertIn('results.json', test_zip.namelist())
            self.assertIn('sections.json', test_zip.namelist())
            self.assertIn('sessions.json', test_zip.namelist())
            self.assertIn('songs.json', test_zip.namelist())
            self.assertEqual(len(test_zip.namelist()), 6)

            # test content of the json files in the zip
            these_participants = json.loads(test_zip.read('participants.json').decode("utf-8"))
            self.assertEqual(len(these_participants), 1)
            self.assertEqual(Participant.objects.first().unique_hash, '42')

            these_profiles = json.loads(test_zip.read('profiles.json').decode("utf-8"))
            self.assertEqual(len(these_profiles), 5)

            these_results = json.loads(test_zip.read('results.json').decode("utf-8"))
            self.assertEqual(len(these_results), 5)

            these_sections = json.loads(test_zip.read('sections.json').decode("utf-8"))
            self.assertEqual(len(these_sections), 1000)

            these_sessions = json.loads(test_zip.read('sessions.json').decode("utf-8"))

            self.assertEqual(len(these_sessions), 1)
            self.assertEqual(these_sessions[0]['fields']['block'], 14)

            these_songs = json.loads(test_zip.read('songs.json').decode("utf-8"))
            self.assertEqual(len(these_songs), 100)

        # test response from forced download
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/x-zip-compressed')

    def test_export_table_includes_question_key(self):
        session_keys = ['session_start', 'session_end']
        result_keys = ['question_key']
        export_options = ['convert_result_json']  # Adjust based on your needs

        # Call the method under test
        rows, fieldnames = self.block.export_table(session_keys, result_keys, export_options)

        # Assert that 'question_key' is in the fieldnames and check its value in rows
        self.assertIn('question_key', fieldnames)
        for i in range(len(rows)):
            row = rows[i]
            self.assertIn('question_key', row)
            self.assertEqual(row['question_key'], 'test_question_' + str(i))


class TestExperimentAdmin(TestCase):

    @classmethod
    def setUpTestData(self):
        self.experiment_series = Experiment.objects.create(
            name='test',
            description='test description very long like the tea of oolong and the song of the bird in the morning',
            slug='TEST',
        )

    def setUp(self):
        self.admin = ExperimentAdmin(model=Experiment,
                                               admin_site=AdminSite
                                               )

    def test_experiment_series_admin_list_display(self):
        self.assertEqual(
            ExperimentAdmin.list_display,
            (
                'name',
                'slug_link',
                'description_excerpt',
                'dashboard',
                'phases',
                'active',
            )
        )

    def test_experiment_series_admin_description_excerpt(self):
        self.assertEqual(
            self.admin.description_excerpt(self.experiment_series),
            'test description very long like the tea of oolong ...'
        )
        self.assertEqual(
            self.admin.description_excerpt(
                Experiment.objects.create(description='')),
            ''
        )

    def test_experiment_admin_research_dashboard(self):
        request = RequestFactory().request()
        response = self.admin.dashboard(request, self.experiment_series)
        self.assertEqual(response.status_code, 200)


class PhaseAdminTest(TestCase):

    def setUp(self):
        self.admin = PhaseAdmin(model=Phase,
                                admin_site=AdminSite
                                )

    def test_related_series_with_series(self):
        series = Experiment.objects.create(name='Test Series')
        phase = Phase.objects.create(
            name='Test Group', index=1, randomize=False, series=series, dashboard=True)
        related_series = self.admin.related_series(phase)
        expected_url = reverse(
            "admin:experiment_experiment_change", args=[series.pk])
        expected_related_series = format_html('<a href="{}">{}</a>', expected_url, series.name)
        self.assertEqual(related_series, expected_related_series)

    def test_blocks_with_no_blocks(self):
        series = Experiment.objects.create(name='Test Series')
        phase = Phase.objects.create(
            name='Test Group', index=1, randomize=False, dashboard=True, series=series)
        blocks = self.admin.blocks(phase)
        self.assertEqual(blocks, "No blocks")

    def test_blocks_with_blocks(self):
        series = Experiment.objects.create(name='Test Series')
        phase = Phase.objects.create(
            name='Test Group', index=1, randomize=False, dashboard=True, series=series)
        block1 = Block.objects.create(name='Block 1', slug='block-1')
        block2 = Block.objects.create(name='Block 2', slug='block-2')
        grouped_block1 = GroupedBlock.objects.create(phase=phase, block=block1)
        grouped_block2 = GroupedBlock.objects.create(phase=phase, block=block2)

        blocks = self.admin.blocks(phase)
        expected_blocks = format_html(
            ', '.join([
                f'<a href="/admin/experiment/groupedblock/{block.id}/change/">{block.block.name}</a>'
                for block in [grouped_block1, grouped_block2]
            ])
        )
        self.assertEqual(blocks, expected_blocks)
