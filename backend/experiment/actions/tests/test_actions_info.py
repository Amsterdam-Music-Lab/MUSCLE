import unittest

from experiment.actions.button import Button
from experiment.actions.info import Info


class TestInfo(unittest.TestCase):

    def test_initialization_all_parameters(self):
        info = Info(
            body="<p>Test Body</p>",
            heading="Test Heading",
            button=Button("Test Label", link="http://example.com"),
        )
        self.assertEqual(info.body, "<p>Test Body</p>")
        self.assertEqual(info.heading, "Test Heading")
        self.assertEqual(info.button.label, "Test Label")
        self.assertEqual(info.button.link, "http://example.com")

    def test_initialization_only_body(self):
        info = Info(body="<p>Only Body</p>")
        self.assertEqual(info.body, "<p>Only Body</p>")
        self.assertEqual(info.heading, "")
        self.assertIsNone(info.button)

    def test_initialization_default_values(self):
        info = Info(body="<p>Body</p>", heading="Heading")
        self.assertEqual(info.body, "<p>Body</p>")
        self.assertEqual(info.heading, "Heading")
        self.assertIsNone(info.button)
