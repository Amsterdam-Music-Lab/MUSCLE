from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from experiment.models import Experiment
from experiment.actions.consent import Consent


class ConsentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Experiment.objects.create(
            slug="MARKDOWN",
            consent=SimpleUploadedFile(
                "consent.md", b"#test", content_type="text/html"
            ),
        )
        Experiment.objects.create(
            slug="HTML",
            consent=SimpleUploadedFile(
                "consent.html", b"<h1>test</h1>", content_type="text/html"
            ),
        )
        Experiment.objects.create(
            slug="TEMPLATE",
            consent=SimpleUploadedFile(
                "template.html",
                b"{% load i18n %}{% blocktranslate %}<p>test</p>{% endblocktranslate %}",
                content_type="text/html",
            ),
        )

    def test_markdown_rendering(self):
        consent = Consent("", url="dev/consent_mock.md")
        self.assertEqual(consent.text, "<h1>test</h1>")

    def test_html_rendering(self):
        consent = Consent("", url="dev/consent_mock.html")
        self.assertEqual(consent.text, "<h1>test</h1>")

    def test_uploaded_markdown_rendering(self):
        experiment = Experiment.objects.get(slug="MARKDOWN")
        consent = Consent(experiment.consent)
        breakpoint()
        self.assertEqual(consent.text, "<h1>test</h1>")

    def test_uploaded_html_rendering(self):
        experiment = Experiment.objects.get(slug="HTML")
        consent = Consent(experiment.consent)
        self.assertEqual(consent.text, "<h1>test</h1>")

    def test_template_language_rendering(self):
        experiment = Experiment.objects.get(slug="TEMPLATE")
        consent = Consent(experiment.consent)
        self.assertEqual(consent.text, "<p>test</p>")
