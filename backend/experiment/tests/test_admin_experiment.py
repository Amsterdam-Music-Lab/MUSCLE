from zipfile import ZipFile
from io import BytesIO
import json
from django.test import Client, TestCase, RequestFactory
from django.forms.models import model_to_dict
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.utils.html import format_html
from experiment.admin import BlockAdmin, ExperimentAdmin, PhaseAdmin
from experiment.models import Block, Experiment, Phase, ExperimentTranslatedContent, BlockTranslatedContent
from participant.models import Participant
from result.models import Result
from session.models import Session
from section.models import Playlist
from theme.models import ThemeConfig
from question.models import QuestionSeries, QuestionInSeries, Question
from question.questions import create_default_questions

# Expected field count per model
EXPECTED_BLOCK_FIELDS = 10
EXPECTED_SESSION_FIELDS = 8
EXPECTED_RESULT_FIELDS = 12
EXPECTED_PARTICIPANT_FIELDS = 5


class MockRequest:
    pass


request = MockRequest()


class TestAdminBlock(TestCase):
    @classmethod
    def setUpTestData(cls):
        Block.objects.create(slug="test")
        Participant.objects.create()
        Session.objects.create(block=Block.objects.first(), participant=Participant.objects.first())
        Result.objects.create(session=Session.objects.first())

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

    def test_block_slug_link(self):
        block = Block.objects.create(slug="test-block")
        site = AdminSite()
        admin = BlockAdmin(block, site)
        link = admin.block_slug_link(block)

        expected_link = '<a href="/block/test-block" target="_blank" rel="noopener noreferrer" title="Open test-block block in new tab" >test-block&nbsp;<small>&#8599;</small></a>'
        self.assertEqual(link, expected_link)


class TestAdminBlockExport(TestCase):
    fixtures = ["playlist", "experiment"]

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.get(slug="huang_2022")
        for playlist in cls.block.playlists.all():
            playlist._update_sections()
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
        )
        for i in range(5):
            Result.objects.create(
                session=Session.objects.first(),
                expected_response=i,
                given_response=i,
                question_key="test_question_" + str(i),
            )
            Result.objects.create(
                participant=cls.participant,
                question_key=i,
                given_response=i,
            )

    def setUp(self):
        self.client = Client()
        self.admin = BlockAdmin(model=Block, admin_site=AdminSite)

    def test_admin_export(self):
        response = self.admin.export(request, self.block)
        zip_buffer = BytesIO(response.content)
        with ZipFile(zip_buffer, "r") as test_zip:
            # Test files inside zip
            self.assertIn("participants.json", test_zip.namelist())
            self.assertIn("profiles.json", test_zip.namelist())
            self.assertIn("results.json", test_zip.namelist())
            self.assertIn("sections.json", test_zip.namelist())
            self.assertIn("sessions.json", test_zip.namelist())
            self.assertIn("songs.json", test_zip.namelist())
            self.assertEqual(len(test_zip.namelist()), 6)

            # test content of the json files in the zip
            these_participants = json.loads(test_zip.read("participants.json").decode("utf-8"))
            self.assertEqual(len(these_participants), 1)
            self.assertEqual(Participant.objects.first().unique_hash, "42")

            these_profiles = json.loads(test_zip.read("profiles.json").decode("utf-8"))
            self.assertEqual(len(these_profiles), 5)

            these_results = json.loads(test_zip.read("results.json").decode("utf-8"))
            self.assertEqual(len(these_results), 5)

            these_sections = json.loads(test_zip.read("sections.json").decode("utf-8"))
            self.assertEqual(len(these_sections), 1000)

            these_sessions = json.loads(test_zip.read("sessions.json").decode("utf-8"))

            self.assertEqual(len(these_sessions), 1)
            self.assertEqual(these_sessions[0]["fields"]["block"], 14)

            these_songs = json.loads(test_zip.read("songs.json").decode("utf-8"))
            self.assertEqual(len(these_songs), 100)

        # test response from forced download
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/x-zip-compressed")

    def test_export_table_includes_question_key(self):
        session_keys = ["session_start", "session_end"]
        result_keys = ["question_key"]
        export_options = ["convert_result_json"]  # Adjust based on your needs

        # Call the method under test
        rows, fieldnames = self.block.export_table(session_keys, result_keys, export_options)

        # Assert that 'question_key' is in the fieldnames and check its value in rows
        self.assertIn("question_key", fieldnames)
        for i in range(len(rows)):
            row = rows[i]
            self.assertIn("question_key", row)
            self.assertEqual(row["question_key"], "test_question_" + str(i))


class TestExperimentAdmin(TestCase):
    @classmethod
    def setUpTestData(self):
        self.experiment = Experiment.objects.create(
            slug="TEST",
        )
        ExperimentTranslatedContent.objects.create(
            experiment=self.experiment,
            language="en",
            name="test",
            description="test description very long like the tea of oolong and the song of the bird in the morning",
        )

    def setUp(self):
        self.admin = ExperimentAdmin(model=Experiment, admin_site=AdminSite)

    def test_experiment_admin_list_display(self):
        self.assertEqual(
            ExperimentAdmin.list_display,
            (
                "name",
                "slug_link",
                "remarks",
                "active",
            ),
        )

    def test_experiment_admin_research_dashboard(self):
        request = RequestFactory().request()
        response = self.admin.experimenter_dashboard(request, self.experiment)
        self.assertEqual(response.status_code, 200)


class PhaseAdminTest(TestCase):
    def setUp(self):
        self.admin = PhaseAdmin(model=Phase, admin_site=AdminSite)

    def test_phase_admin_related_experiment_method(self):
        experiment = Experiment.objects.create(slug="test-experiment")
        ExperimentTranslatedContent.objects.create(experiment=experiment, language="en", name="Test Experiment")
        phase = Phase.objects.create(
            index=1, randomize=False, experiment=experiment, dashboard=True
        )
        related_experiment = self.admin.related_experiment(phase)
        expected_url = reverse("admin:experiment_experiment_change", args=[experiment.pk])
        expected_related_experiment = format_html(
            '<a href="{}">{}</a>', expected_url, experiment.get_fallback_content().name
        )
        self.assertEqual(related_experiment, expected_related_experiment)

    def test_experiment_with_no_blocks(self):
        experiment = Experiment.objects.create(slug="no-blocks")
        ExperimentTranslatedContent.objects.create(
            experiment=experiment,
            language="en",
            name="No Blocks",
        )
        phase = Phase.objects.create(
            index=1, randomize=False, dashboard=True, experiment=experiment
        )
        blocks = self.admin.blocks(phase)
        self.assertEqual(blocks, "No blocks")

    def test_experiment_with_blocks(self):
        experiment = Experiment.objects.create(slug="with-blocks")
        ExperimentTranslatedContent.objects.create(
            experiment=experiment,
            language="en",
            name="With Blocks",
        )
        phase = Phase.objects.create(
            index=1, randomize=False, dashboard=True, experiment=experiment
        )
        block1 = Block.objects.create(slug="block-1", phase=phase)
        block2 = Block.objects.create(slug="block-2", phase=phase)

        blocks = self.admin.blocks(phase)
        expected_blocks = format_html(
            ", ".join([f"{block.slug}" for block in [block1, block2]])
        )
        self.assertEqual(blocks, expected_blocks)


class TestDuplicateExperiment(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(slug="original")
        ExperimentTranslatedContent.objects.create(
            experiment=cls.experiment,
            language="en",
            name="original experiment",
        )
        ExperimentTranslatedContent.objects.create(
            experiment=cls.experiment,
            language="nl",
            name="origineel experiment",
        )
        cls.first_phase = Phase.objects.create(
            index=1, randomize=False, dashboard=True, experiment=cls.experiment
        )
        cls.second_phase = Phase.objects.create(
            index=2, randomize=False, dashboard=True, experiment=cls.experiment
        )
        cls.playlist1 = Playlist.objects.create(name="first")
        cls.playlist2 = Playlist.objects.create(name="second")
        cls.theme = ThemeConfig.objects.create(name='test_theme')

        cls.block1 = Block.objects.create(slug="block1", phase=cls.first_phase, theme_config=cls.theme)
        cls.block2 = Block.objects.create(slug="block2", phase=cls.first_phase, theme_config=cls.theme)
        cls.block3 = Block.objects.create(slug="block3", phase=cls.second_phase, theme_config=cls.theme)
        cls.block4 = Block.objects.create(slug="block4", phase=cls.second_phase, theme_config=cls.theme)

        cls.block1.playlists.add(cls.playlist1)
        cls.block1.playlists.add(cls.playlist2)
        cls.block1.save()
        create_default_questions()
        cls.question_series = QuestionSeries.objects.create(block=cls.block2, index=0)
        cls.questions = Question.objects.all()
        index = 0
        for question in cls.questions:
            QuestionInSeries.objects.create(question_series = cls.question_series,
                                            question=question,
                                            index=index)
            index += 1

        cls.questions_in_series = QuestionInSeries.objects.all()

        BlockTranslatedContent.objects.create(
            block=cls.block1,
            language="en",
            name="First block",
            description="Block1 description"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block1,
            language="nl",
            name="Eerste blok",
            description="Block1 omschrijving"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block2,
            language="en",
            name="Second block",
            description="Block2 description"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block2,
            language="nl",
            name="Tweede blok",
            description="Block2 omschrijving"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block3,
            language="en",
            name="Third block",
            description="Block3 description"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block3,
            language="nl",
            name="Derde blok",
            description="Block3 omschrijving"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block4,
            language="en",
            name="Fourth block",
            description="Block4 description"
        )
        BlockTranslatedContent.objects.create(
            block=cls.block4,
            language="nl",
            name="Vierde blok",
            description="Block4 omschrijving"
        )

    def setUp(self):
        self.admin = ExperimentAdmin(model=Experiment, admin_site=AdminSite)

    def test_duplicate_experiment(self):
        request = MockRequest()
        request.POST = {"_duplicate": "",
                        "slug-extension": "duplitest"}
        response = self.admin.duplicate(request, self.experiment)

        new_exp = Experiment.objects.last()
        all_experiments = Experiment.objects.all()
        all_exp_content = ExperimentTranslatedContent.objects.all()

        all_phases = Phase.objects.all()

        all_blocks = Block.objects.all()
        last_block = Block.objects.last()
        all_block_content = BlockTranslatedContent.objects.all()
        new_block1 = Block.objects.get(slug="block1-duplitest")

        all_question_series = QuestionSeries.objects.all()
        all_questions = Question.objects.all()

        self.assertEqual(all_experiments.count(), 2)
        self.assertEqual(all_exp_content.count(), 4)
        self.assertEqual(new_exp.slug, 'original-duplitest')

        self.assertEqual(all_phases.count(), 4)

        self.assertEqual(all_blocks.count(), 8)
        self.assertEqual(all_block_content.count(), 16)
        self.assertEqual(last_block.slug, 'block4-duplitest')
        self.assertEqual(last_block.theme_config.name, 'test_theme')

        self.assertEqual(new_block1.playlists.all().count(), 2)

        self.assertEqual(all_question_series.count(), 2)
        self.assertEqual(self.questions.count(), (all_questions.count()))

        self.assertEqual(response.status_code, 302)
