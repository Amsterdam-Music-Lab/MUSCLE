from os.path import dirname, join
from shutil import rmtree

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from experiment.models import Experiment
from experiment.actions.consent import Consent

here = dirname(__file__)

class ConsentTest(TestCase):

    @classmethod
    def tearDownClass(cls):
        rmtree(join(here, 'consent'))
        return super().tearDownClass()

    def test_markdown_rendering(self):
        consent = Consent("", url="dev/consent_mock.md")
        self.assertEqual(consent.text, "<h1>test</h1>")

    def test_html_rendering(self):
        consent = Consent("", url="dev/consent_mock.html")
        self.assertEqual(consent.text, "<h1>test</h1>")

    @override_settings(MEDIA_ROOT=here)
    def test_uploaded_markdown_rendering(self):
        experiment = Experiment.objects.create(
            slug="MARKDOWN",
            consent=SimpleUploadedFile(
                "consent.md", b"#test", content_type="text/html"
            ),
        )
        consent = Consent(experiment.consent)
        self.assertEqual(consent.text, "<h1>test</h1>")

    @override_settings(MEDIA_ROOT=here)
    def test_uploaded_html_rendering(self):
        experiment = Experiment.objects.create(
            slug="HTML",
            consent=SimpleUploadedFile(
                "consent.html", b"<h1>test</h1>", content_type="text/html"
            ),
        )
        consent = Consent(experiment.consent)
        self.assertEqual(consent.text, "<h1>test</h1>")

    @override_settings(MEDIA_ROOT=here)
    def test_template_language_rendering(self):
        experiment = Experiment.objects.create(
            slug="TEMPLATE",
            consent=SimpleUploadedFile(
                "template.html",
                b"{% load i18n %}{% blocktranslate %}<p>test</p>{% endblocktranslate %}",
                content_type="text/html",
            ),
        )
        consent = Consent(experiment.consent)
        self.assertEqual(consent.text, "<p>test</p>")
