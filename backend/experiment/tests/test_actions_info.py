import unittest

from experiment.actions.info import Info


class TestInfo(unittest.TestCase):

    def test_initialization_all_parameters(self):
        info = Info(
            body="<p>Test Body</p>",
            heading="Test Heading",
            button_label="Test Label",
            button_link="http://example.com"
        )
        self.assertEqual(info.body, "<p>Test Body</p>")
        self.assertEqual(info.heading, "Test Heading")
        self.assertEqual(info.button_label, "Test Label")
        self.assertEqual(info.button_link, "http://example.com")

    def test_initialization_only_body(self):
        info = Info(body="<p>Only Body</p>")
        self.assertEqual(info.body, "<p>Only Body</p>")
        self.assertEqual(info.heading, "")
        self.assertIsNone(info.button_label)
        self.assertIsNone(info.button_link)

    def test_initialization_default_values(self):
        info = Info(body="<p>Body</p>", heading="Heading")
        self.assertEqual(info.body, "<p>Body</p>")
        self.assertEqual(info.heading, "Heading")
        self.assertIsNone(info.button_label)
        self.assertIsNone(info.button_link)


if __name__ == '__main__':
    unittest.main()
