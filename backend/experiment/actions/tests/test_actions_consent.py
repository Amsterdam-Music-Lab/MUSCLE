from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from experiment.models import Experiment, ExperimentTranslatedContent
from experiment.actions.consent import Consent


class ConsentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Experiment.objects.create(
            slug="MARKDOWN",
        )
        ExperimentTranslatedContent.objects.create(
            experiment=Experiment.objects.get(slug="MARKDOWN"),
            language="en",
            consent=SimpleUploadedFile("consent.md", b"#test", content_type="text/html"),
        )
        Experiment.objects.create(
            slug="HTML",
        )
        ExperimentTranslatedContent.objects.create(
            experiment=Experiment.objects.get(slug="HTML"),
            language="en",
            consent=SimpleUploadedFile("consent.html", b"<h1>test</h1>", content_type="text/html"),
        )
        Experiment.objects.create(
            slug="TEMPLATE",
        )
        ExperimentTranslatedContent.objects.create(
            experiment=Experiment.objects.get(slug="TEMPLATE"),
            language="en",
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
        content = experiment.get_fallback_content()
        consent = Consent(content.consent)
        self.assertEqual(consent.text, "<h1>test</h1>")

    def test_uploaded_html_rendering(self):
        experiment = Experiment.objects.get(slug="HTML")
        content = experiment.get_fallback_content()
        consent = Consent(content.consent)
        self.assertEqual(consent.text, "<h1>test</h1>")

    def test_template_language_rendering(self):
        experiment = Experiment.objects.get(slug="TEMPLATE")
        content = experiment.get_fallback_content()
        consent = Consent(content.consent)
        self.assertEqual(consent.text, "<p>test</p>")
