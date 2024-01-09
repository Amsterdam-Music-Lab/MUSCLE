from django.test import TestCase

from experiment.actions.html import HTML

class HTMLTest(TestCase):

    def test_initialization(self):
        test_html_body = "<div>Test HTML Content</div>"
        html_action = HTML(body=test_html_body)
        self.assertEqual(html_action.body, test_html_body)
