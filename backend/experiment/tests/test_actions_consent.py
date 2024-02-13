from django.test import TestCase

from experiment.actions.consent import Consent


class ConsentTest(TestCase):

    def test_markdown_rendering(self):
        consent = Consent('#test', render_format='MARKDOWN')
        self.assertEqual(consent.text, '<h1>test</h1>')

    def test_no_markdown_rendering(self):
        consent = Consent('#test')
        self.assertEqual(consent.text, '#test')