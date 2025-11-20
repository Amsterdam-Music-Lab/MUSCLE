from django.test import TestCase

from experiment.actions.button import Button

class ButtonTest(TestCase):

    def test_button_init_with_named_args(self):
        button = Button('some label', link="/relative/link")
        self.assertTrue(button)
        action = button.action()
        self.assertEqual(action.get('color'), 'colorPrimary')