from os.path import dirname, join
from shutil import rmtree

from django.test import override_settings, TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from image.models import Image
from experiment.serializers import serialize_phase
from experiment.models import (
    Block,
    Experiment,
    Feedback,
    Phase,
    SocialMediaConfig,
)
from experiment.rules.rhythm_battery_intro import RhythmBatteryIntro
from participant.models import Participant
from participant.utils import PARTICIPANT_KEY
from session.models import Session
from theme.models import ThemeConfig, FooterConfig, HeaderConfig

here = dirname(__file__)

class TestExperimentViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create()
        theme_config = create_theme_config()
        experiment = Experiment.objects.create(
            slug="test_series",
            theme_config=theme_config,
            name="Test Series",
            description="Test Description",
            social_media_message="Please play this Test experiment!",
        )
        experiment.social_media_config = create_social_media_config(experiment)
        cls.introductory_phase = Phase.objects.create(experiment=experiment, index=1)
        cls.block1 = Block.objects.create(slug="block1", phase=cls.introductory_phase)
        cls.intermediate_phase = Phase.objects.create(experiment=experiment, index=2)
        cls.block2 = Block.objects.create(slug="block2", theme_config=theme_config, phase=cls.intermediate_phase)
        cls.block3 = Block.objects.create(slug="block3", phase=cls.intermediate_phase)
        cls.final_phase = Phase.objects.create(experiment=experiment, index=3)
        cls.block4 = Block.objects.create(slug="block4", phase=cls.final_phase)

    @classmethod
    def tearDownClass(cls):
        rmtree(join(here, 'consent'))
        return super().tearDownClass()

    def setUp(self):
        session = self.client.session
        session["participant_id"] = self.participant.id
        session.save()

    def test_get_experiment(self):
        # check that the correct block is returned correctly
        response = self.client.get("/experiment/test_series/")
        self.assertEqual(response.json().get("nextBlock").get("slug"), "block1")
        # create session
        Session.objects.create(block=self.block1, participant=self.participant, finished_at=timezone.now())
        response = self.client.get("/experiment/test_series/")
        self.assertIn(response.json().get("nextBlock").get("slug"), ("block2", "block3"))
        self.assertEqual(response.json().get("dashboard"), [])
        Session.objects.create(block=self.block2, participant=self.participant, finished_at=timezone.now())
        Session.objects.create(block=self.block3, participant=self.participant, finished_at=timezone.now())
        response = self.client.get("/experiment/test_series/")
        response_json = response.json()
        self.assertEqual(response_json.get("nextBlock").get("slug"), "block4")
        self.assertEqual(response_json.get("dashboard"), [])
        self.assertEqual(response_json.get("theme").get("name"), "test_theme")
        self.assertEqual(len(response_json["theme"]["header"]["score"]), 3)
        self.assertEqual(response_json.get("socialMedia").get("url"), "https://www.example.com")
        self.assertEqual(response_json.get("socialMedia").get("content"), "Please play this Test experiment!")
        self.assertEqual(response_json.get("socialMedia").get("tags"), ["aml", "toontjehoger"])
        self.assertEqual(response_json.get("socialMedia").get("channels"), ["facebook", "twitter", "weibo"])
        Session.objects.create(
            block=self.block4, participant=self.participant, finished_at=timezone.now()
        )
        # starting second round of experiment
        response = self.client.get("/experiment/test_series/")
        response_json = response.json()
        self.assertIsNotNone(response_json)
        self.assertEqual(response_json.get("nextBlock").get("slug"), "block1")
        Session.objects.create(
            block=self.block1, participant=self.participant, finished_at=timezone.now()
        )
        response = self.client.get("/experiment/test_series/")
        response_json = response.json()
        self.assertIsNotNone(response_json)
        self.assertIn(response_json.get("nextBlock").get("slug"), ("block2", "block3"))

    def test_get_experiment_returning_participant(self):
        Session.objects.bulk_create(
            self._get_session_objects(
                [
                    self.block1,
                    self.block2,
                    self.block3,
                    self.block4,
                    self.block1,
                    self.block2,
                    self.block3,
                    self.block4,
                ]
            )
        )
        response = self.client.get("/experiment/test_series/")
        self.assertEqual(response.json().get("nextBlock").get("slug"), "block1")

    def _get_session_objects(self, block_list: list[Block]) -> list[Session]:
        return [
            Session(
                block=block, participant=self.participant, finished_at=timezone.now()
            )
            for block in block_list
        ]

    def test_experiment_not_found(self):
        # if Experiment does not exist, return 404
        response = self.client.get("/experiment/not_found/")
        self.assertEqual(response.status_code, 404)

    def test_experiment_inactive(self):
        # if Experiment is inactive, return 404
        experiment = Experiment.objects.get(slug="test_series")
        experiment.active = False
        experiment.save()
        response = self.client.get("/experiment/test_series/")
        self.assertEqual(response.status_code, 404)

    def test_experiment_has_no_phases(self):
        Experiment.objects.create(slug="invalid_experiment")
        response = self.client.get("/experiment/invalid_experiment/")
        self.assertEqual(response.status_code, 500)

    def test_experiment_without_social_media(self):
        experiment = Experiment.objects.create(
            slug="no_social_media",
            theme_config=create_theme_config(name="no_social_media"),
            name="Test Experiment",
            description="Test Description",
        )
        self.intermediate_phase.experiment = experiment
        self.intermediate_phase.save()
        response = self.client.get("/experiment/no_social_media/")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("socialMedia", response.json())

    def test_experiment_with_dashboard(self):
        # if Experiment has dashboard set True, return list of random blocks
        Session.objects.create(block=self.block1, participant=self.participant, finished_at=timezone.now())
        self.intermediate_phase.dashboard = True
        self.intermediate_phase.save()
        # check that the dashboard is returned correctly
        response = self.client.get("/experiment/test_series/")
        self.assertEqual(type(response.json().get("dashboard")), list)

    def test_experiment_total_score(self):
        """Test calculation of total score for grouped block on dashboard"""
        Session.objects.create(
            block=self.block2, participant=self.participant, finished_at=timezone.now(), final_score=8
        )
        self.intermediate_phase.dashboard = True
        self.intermediate_phase.save()
        serialized_coll_1 = serialize_phase(
            self.intermediate_phase, self.participant, 0
        )
        total_score_1 = serialized_coll_1["accumulatedScore"]
        self.assertEqual(total_score_1, 8)
        Session.objects.create(
            block=self.block3, participant=self.participant, finished_at=timezone.now(), final_score=8
        )
        serialized_coll_2 = serialize_phase(
            self.intermediate_phase, self.participant, 0
        )
        total_score_2 = serialized_coll_2["accumulatedScore"]
        self.assertEqual(total_score_2, 16)

    def test_experiment_translation(self):
        """Test translations of experiment texts"""

        experiment = Experiment.objects.create(
            slug="test_experiment_translated_content",
            name_en="Test Experiment Translation",
            description_en="Test experiment description in English.",
            name_nl="Probeersel",
            description_nl="Eens kijken of vertaling werkt.",
        )
        self.intermediate_phase.experiment = experiment
        self.intermediate_phase.save()

        session = self.client.session
        session["participant_id"] = self.participant.id
        session.save()

        # request experiment with language set to English (British)
        response = self.client.get(
            "/experiment/test_experiment_translated_content/",
            headers={"Accept-Language": "en-Gb"},
        )
        # since English translation is available, the English content should be returned
        self.assertEqual(response.json().get("name"), "Test Experiment Translation")

        # request experiment with language set to Spanish
        response = self.client.get(
            "/experiment/test_experiment_translated_content/",
            headers={"Accept-Language": "nl"},
        )

        # since Spanish translation is available, the Spanish content should be returned
        self.assertEqual(response.json().get("name"), "Probeersel")

        # request experiment with language set to Dutch
        response = self.client.get("/experiment/test_experiment_translated_content/", headers={"Accept-Language": "nl"})

        # since no Dutch translation is available, the fallback content should be returned
        self.assertEqual(
            response.json().get("description"), "Eens kijken of vertaling werkt."
        )

    @override_settings(MEDIA_ROOT=here)
    def test_get_block(self):
        # Create a block
        experiment = Experiment.objects.create(
            slug="test-experiment",
            name="Test Experiment",
            description="Test Description",
            consent=SimpleUploadedFile("test-consent.md", b"test consent"),
        )
        phase = Phase.objects.create(experiment=experiment)
        block = Block.objects.create(
            slug="test-block",
            image=Image.objects.create(file="test-image.jpg"),
            rules=RhythmBatteryIntro.ID,
            theme_config=create_theme_config("new-theme"),
            rounds=3,
            bonus_points=42,
            phase=phase,
            name="Test Block",
            description="This is a test block",
        )
        participant = Participant.objects.create()
        participant.save()

        # Request session (not to be confused with experiment block session)
        request_session = self.client.session
        request_session.update({PARTICIPANT_KEY: participant.id})
        request_session.save()

        # Experiment block session
        Session.objects.bulk_create(
            [Session(block=block, participant=participant, finished_at=timezone.now()) for index in range(3)]
        )

        response = self.client.get("/experiment/block/test-block/")

        self.assertEqual(response.json()["slug"], "test-block")
        self.assertEqual(response.json()["name"], "Test Block")
        self.assertEqual(response.json()["theme"]["name"], "new-theme")
        self.assertEqual(len(response.json()["theme"]["header"]["score"]), 3)
        self.assertEqual(response.json()["rounds"], 3)
        self.assertEqual(response.json()["bonus_points"], 42)

    def test_post_feedback(self):
        request = {"feedback": "I have a lot of feedback here"}
        self.client.post("/experiment/block/block1/feedback/", request)
        self.assertEqual(Feedback.objects.count(), 1)
        response = self.client.post(
            "/experiment/block/nonexisting-slug/feedback/", request
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Feedback.objects.count(), 1)
        request = {"feedback": ""}
        response = self.client.post("/experiment/block/block1/feedback/", request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Feedback.objects.count(), 1)


def create_theme_config(name="test_theme") -> ThemeConfig:
    theme_config = ThemeConfig.objects.create(
        name=name,
        description="Test Theme",
        heading_font_url="https://fonts.googleapis.com/css2?family=Architects+Daughter&family=Micro+5&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap",
        body_font_url="https://fonts.googleapis.com/css2?family=Architects+Daughter&family=Micro+5&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap",
        logo_image=Image.objects.create(file="test-logo.jpg"),
        background_image=Image.objects.create(file="test-background.jpg"),
    )
    HeaderConfig.objects.create(theme=theme_config, show_score=True)
    footer_config = FooterConfig.objects.create(
        theme=theme_config,
    )
    footer_config.logos.add(Image.objects.create(file="test-logo-b.jpg"), through_defaults={"index": 1})
    footer_config.logos.add(Image.objects.create(file="test-logo-a.jpg"), through_defaults={"index": 0})

    return theme_config


def create_social_media_config(experiment: Experiment) -> SocialMediaConfig:
    return SocialMediaConfig.objects.create(
        experiment=experiment,
        url="https://www.example.com",
        channels=["facebook", "twitter", "weibo"],
        tags=["aml", "toontjehoger"],
    )
