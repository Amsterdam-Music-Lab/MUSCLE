from django.test import TestCase

from experiment.actions.form import Form
from experiment.actions.question import NumberQuestion

class FormTest(TestCase):
    def setUp(self):
        self.questions = [NumberQuestion(key='test_key', min_value=1, max_value=10)]
        self.form = Form(form=self.questions, submit_label='Submit', skip_label='Skip', is_skippable=True)

    def test_initialization(self):
        self.assertEqual(len(self.form.form), 1)
        self.assertEqual(self.form.submit_label, 'Submit')
        self.assertEqual(self.form.skip_label, 'Skip')
        self.assertTrue(self.form.is_skippable)

    def test_action_method(self):
        action_result = self.form.action()
        self.assertIn('form', action_result)
        self.assertEqual(len(action_result['form']), 1)
        self.assertIn('submit_label', action_result)
        self.assertIn('skip_label', action_result)
        self.assertIn('is_skippable', action_result)
