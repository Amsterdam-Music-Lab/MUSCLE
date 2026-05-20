from django.test import TestCase

from experiment.actions.form import Form
from experiment.actions.question import NumberQuestion

mock_choices = [{"value": "no", "label": "No"}, {"value": "yes", "label": "Yes"}]

class FormTest(TestCase):
    def setUp(self):
        self.questions = [NumberQuestion(key='test_key', max_value=10)]
        self.form = Form(form=self.questions)

    def test_initialization(self):
        self.assertEqual(len(self.form.form), 1)
        self.assertEqual(self.form.submit_button.label, 'Submit')
        self.assertEqual(self.form.skip_button.label, 'Skip')

    def test_action_method(self):
        action_result = self.form.action()
        self.assertIn('form', action_result)
        self.assertEqual(len(action_result['form']), 1)
        self.assertIsNone(action_result.get("skipButton"))
