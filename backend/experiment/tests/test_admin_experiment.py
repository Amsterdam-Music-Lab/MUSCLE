from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.test import TestCase, RequestFactory
from django.urls import reverse

from experiment.admin import BlockAdmin, ExperimentAdmin
from experiment.models import Block, Experiment, Phase
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

class TestExperimentAdmin(TestCase):
    @classmethod
    def setUpTestData(self):
        self.experiment = Experiment.objects.create(
            slug="TEST",
            name="test",
            description="test description very long like the tea of oolong and the song of the bird in the morning",
        )

    def setUp(self):
        self.admin = ExperimentAdmin(model=Experiment, admin_site=AdminSite)

    def test_experiment_admin_list_display(self):
        self.assertEqual(
            ExperimentAdmin.list_display,
            (
                "experiment_name",
                "slug_link",
                "remarks",
                "active",
            ),
        )

    def test_experiment_admin_research_dashboard(self):
        request = RequestFactory().request()
        response = self.admin.experimenter_dashboard(request, self.experiment)
        self.assertEqual(response.status_code, 200)


class PhaseInlineTemplateTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = ExperimentAdmin(model=Experiment, admin_site=self.site)
        self.user = get_user_model().objects.create_superuser(
            username='admin', password='pass', email='admin@example.com'
        )
        self.client.login(username='admin', password='pass')

    def test_phase_inline_template_renders_blocks(self):
        experiment = Experiment.objects.create(slug="inline-test", name="Inline Test")
        phase = Phase.objects.create(
            index=1, randomize=False, dashboard=True, experiment=experiment
        )
        block = Block.objects.create(slug="block-inline", phase=phase)

        url = reverse("admin:experiment_experiment_change", args=[experiment.pk])
        response = self.client.get(url)
        self.assertContains(response, "Blocks")
        self.assertContains(response, block.slug)
        self.assertContains(response, 'add/?phase_id=%s' % phase.pk)


class TestDuplicateExperiment(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experiment = Experiment.objects.create(
            slug="original",
            name_en="original experiment",
            name_nl="origineel experiment",
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

        cls.block1 = Block.objects.create(
            slug="block1",
            phase=cls.first_phase,
            name_en="First block",
            description_en="Block1 description",
            name_nl="Eerste blok",
            description_nl="Block1 omschrijving",
            theme_config=cls.theme,
        )
        cls.block2 = Block.objects.create(
            slug="block2",
            phase=cls.first_phase,
            name_en="Second block",
            description_en="Block2 description",
            name_nl="Tweede blok",
            description_nl="Block2 omschrijving",
            theme_config=cls.theme,
        )
        cls.block3 = Block.objects.create(
            slug="block3",
            phase=cls.second_phase,
            name_en="Third block",
            description_en="Block3 description",
            name_nl="Derde blok",
            description_nl="Block3 omschrijving",
            theme_config=cls.theme,
        )
        cls.block4 = Block.objects.create(
            slug="block4",
            phase=cls.second_phase,
            name_en="Fourth block",
            description_en="Block4 description",
            name_nl="Vierde blok",
            description_nl="Block4 omschrijving",
            theme_config=cls.theme,
        )

        cls.block1.playlists.add(cls.playlist1)
        cls.block1.playlists.add(cls.playlist2)
        cls.block1.save()
        create_default_questions()
        cls.question_series = QuestionSeries.objects.create(block=cls.block2, index=0)
        cls.questions = Question.objects.all()
        index = 0
        for question in cls.questions:
            QuestionInSeries.objects.create(
                question_series=cls.question_series, question=question, index=index
            )
            index += 1

        cls.questions_in_series = QuestionInSeries.objects.all()

    def setUp(self):
        self.admin = ExperimentAdmin(model=Experiment, admin_site=AdminSite)

    def test_duplicate_experiment(self):
        request = MockRequest()
        request.POST = {"_duplicate": "",
                        "slug-extension": "duplitest"}
        response = self.admin.duplicate(request, self.experiment)

        new_exp = Experiment.objects.last()
        all_experiments = Experiment.objects.all()

        all_phases = Phase.objects.all()

        all_blocks = Block.objects.all()
        last_block = Block.objects.last()
        new_block1 = Block.objects.get(slug="block1-duplitest")

        all_question_series = QuestionSeries.objects.all()
        all_questions = Question.objects.all()

        self.assertEqual(all_experiments.count(), 2)
        self.assertEqual(new_exp.slug, 'original-duplitest')

        self.assertEqual(all_phases.count(), 4)

        self.assertEqual(all_blocks.count(), 8)
        self.assertEqual(last_block.slug, 'block4-duplitest')
        self.assertEqual(last_block.theme_config.name, 'test_theme')

        self.assertEqual(new_block1.playlists.all().count(), 2)

        self.assertEqual(all_question_series.count(), 2)
        self.assertEqual(self.questions.count(), (all_questions.count()))

        self.assertEqual(response.status_code, 302)
