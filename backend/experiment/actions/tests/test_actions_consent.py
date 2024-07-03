from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from experiment.models import Block
from experiment.actions.consent import Consent


class ConsentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Block.objects.create(
            name='test_md',
            slug='MARKDOWN',
            consent=SimpleUploadedFile('consent.md', b'#test', content_type='text/html')
        )
        Block.objects.create(
            name='test_html',
            slug='HTML',
            consent=SimpleUploadedFile('consent.html', b'<h1>test</h1>', content_type='text/html')
        )
        Block.objects.create(
            name='test_template',
            slug='TEMPLATE',
            consent=SimpleUploadedFile('template.html', b'{% load i18n %}{% blocktranslate %}<p>test</p>{% endblocktranslate %}', content_type='text/html')
        )

    def test_markdown_rendering(self):
        consent = Consent('', url='dev/consent_mock.md')
        self.assertEqual(consent.text, '<h1>test</h1>')

    def test_html_rendering(self):
        consent = Consent('', url='dev/consent_mock.html')
        self.assertEqual(consent.text, '<h1>test</h1>')

    def test_uploaded_markdown_rendering(self):
        block = Block.objects.get(slug='MARKDOWN')
        consent = Consent(block.consent)
        self.assertEqual(consent.text, '<h1>test</h1>')

    def test_uploaded_html_rendering(self):
        block = Block.objects.get(slug='HTML')
        consent = Consent(block.consent)
        self.assertEqual(consent.text, '<h1>test</h1>')

    def test_template_language_rendering(self):
        block = Block.objects.get(slug='TEMPLATE')
        consent = Consent(block.consent)
        self.assertEqual(consent.text, '<p>test</p>')
