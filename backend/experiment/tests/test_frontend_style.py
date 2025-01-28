import unittest

from experiment.actions.styles import (
    ColorScheme,
    ConflictingStylesException,
    FrontendStyle,
    TextStyle,
)


class TestFrontendStyle(unittest.TestCase):

    def test_init_with_valid_style(self):
        style = FrontendStyle([ColorScheme.NEUTRAL, TextStyle.INVISIBLE])
        self.assertEqual(style.styles, ['neutral', 'invisible-text'])

    def test_apply_invalid_style(self):
        with self.assertRaises(ValueError):
            FrontendStyle(['fantasy-style'])

    def test_apply_conflicting_styles(self):
        with self.assertRaises(ConflictingStylesException):
            FrontendStyle(["neutral", "boolean"])

    def test_to_dict(self):
        style = FrontendStyle([ColorScheme.NEUTRAL])
        expected_dict = {'neutral': True}
        self.assertEqual(style.to_dict(), expected_dict)
