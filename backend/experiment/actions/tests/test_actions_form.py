from django.test import TestCase

from experiment.actions.form import Form
from experiment.actions.question import (
    AutoCompleteQuestion,
    ButtonArrayQuestion,
    CheckBoxQuestion,
    DropdownQuestion,
    IconRangeQuestion,
    RangeQuestion,
    RadiosQuestion,
    NumberQuestion,
    TextRangeQuestion,
    TextQuestion,
)
from question.models import ChoiceSet

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


class NumberQuestionTest(TestCase):
    def setUp(self):
        self.number_question = NumberQuestion(
            key='test_key',
            min_value=1,
            max_value=10,
        )

    def test_initialization(self):
        self.assertEqual(self.number_question.key, 'test_key')
        self.assertEqual(self.number_question.min_value, 1)
        self.assertEqual(self.number_question.max_value, 10)

    def test_action_method(self):
        action_result = self.number_question.action()
        self.assertIn('key', action_result)
        self.assertIn('min_value', action_result)
        self.assertIn('max_value', action_result)
        self.assertEqual(action_result['min_value'], 1)
        self.assertEqual(action_result['max_value'], 10)


class TextQuestionTest(TestCase):
    def setUp(self):
        self.text_question = TextQuestion(
            key='test_key',
            max_length=100,
        )

    def test_initialization(self):
        self.assertEqual(self.text_question.key, 'test_key')
        self.assertEqual(self.text_question.max_length, 100)

    def test_action_method(self):
        action_result = self.text_question.action()
        self.assertIn('key', action_result)
        self.assertIn('max_length', action_result)
        self.assertEqual(action_result['max_length'], 100)

class MultipleChoiceQuestionTest(TestCase):
    def setUp(self):
        self.choice_question = CheckBoxQuestion(
            key='test_key', choices={'no': 'No', 'yes': 'Yes'}, min_values=1
        )

    def test_initialization(self):
        self.assertEqual(self.choice_question.key, 'test_key')
        self.assertEqual(self.choice_question.choices, {'no': 'No', 'yes': 'Yes'})
        self.assertEqual(self.choice_question.min_values, 1)

    def test_action_method(self):
        action_result = self.choice_question.action()
        self.assertIn('key', action_result)
        self.assertIn('choices', action_result)
        self.assertEqual(action_result['choices'], {'no': 'No', 'yes': 'Yes'})
        self.assertIn('min_values', action_result)
        self.assertEqual(action_result['min_values'], 1)


class DropdownQuestionTest(TestCase):
    def setUp(self):
        self.dropdown_question = DropdownQuestion(
            key='test_key',
            choices={
                'no': 'No',
                'yes': 'Yes'
            },
        )

    def test_initialization(self):
        self.assertEqual(self.dropdown_question.key, 'test_key')
        self.assertEqual(self.dropdown_question.choices, {'no': 'No', 'yes': 'Yes'})

    def test_action_method(self):
        action_result = self.dropdown_question.action()
        self.assertIn('key', action_result)
        self.assertIn('choices', action_result)
        self.assertEqual(action_result['choices'], {'no': 'No', 'yes': 'Yes'})


class AutoCompleteQuestionTest(TestCase):
    def setUp(self):
        self.autocomplete_question = AutoCompleteQuestion(
            key='test_key',
            choices={
                'no': 'No',
                'yes': 'Yes'
            },
        )

    def test_initialization(self):
        self.assertEqual(self.autocomplete_question.key, 'test_key')
        self.assertEqual(self.autocomplete_question.choices, {'no': 'No', 'yes': 'Yes'})

    def test_action_method(self):
        action_result = self.autocomplete_question.action()
        self.assertIn('key', action_result)
        self.assertIn('choices', action_result)
        self.assertEqual(action_result['choices'], {'no': 'No', 'yes': 'Yes'})


class RadiosQuestionTest(TestCase):
    def setUp(self):
        self.radios_question = RadiosQuestion(
            key='test_key',
            choices={
                'no': 'No',
                'yes': 'Yes'
            },
        )

    def test_initialization(self):
        self.assertEqual(self.radios_question.key, 'test_key')
        self.assertEqual(self.radios_question.choices, {'no': 'No', 'yes': 'Yes'})

    def test_action_method(self):
        action_result = self.radios_question.action()
        self.assertIn('key', action_result)
        self.assertIn('choices', action_result)
        self.assertEqual(action_result['choices'], {'no': 'No', 'yes': 'Yes'})


class ButtonArrayQuestionTest(TestCase):
    def setUp(self):
        self.buttonarray_question = ButtonArrayQuestion(
            key='test_key',
            choices={
                'no': 'No',
                'yes': 'Yes'
            },
        )

    def test_initialization(self):
        self.assertEqual(self.buttonarray_question.key, 'test_key')
        self.assertEqual(self.buttonarray_question.choices, {'no': 'No', 'yes': 'Yes'})

    def test_action_method(self):
        action_result = self.buttonarray_question.action()
        self.assertIn('key', action_result)
        self.assertIn('choices', action_result)
        self.assertEqual(action_result['choices'], {'no': 'No', 'yes': 'Yes'})


class RangeQuestionTest(TestCase):
    def setUp(self):
        self.range_question = RangeQuestion(
            key='test_key',
            min_value=1,
            max_value=10,
        )

    def test_initialization(self):
        self.assertEqual(self.range_question.key, 'test_key')
        self.assertEqual(self.range_question.min_value, 1)
        self.assertEqual(self.range_question.max_value, 10)

    def test_action_method(self):
        action_result = self.range_question.action()
        self.assertIn('key', action_result)
        self.assertIn('min_value', action_result)
        self.assertIn('max_value', action_result)
        self.assertEqual(action_result['min_value'], 1)
        self.assertEqual(action_result['max_value'], 10)


class TextRangeQuestionTest(TestCase):

    def setUp(self):
        self.likert_question = TextRangeQuestion(
            key='test_key',
            choices=ChoiceSet.objects.get(pk="LIKERT_AGREE_7").to_dict(),
        )

    def test_initialization(self):
        self.assertEqual(self.likert_question.key, 'test_key')
        self.assertEqual(
            self.likert_question.choices,
            {
                '1': "Completely Disagree",
                '2': "Strongly Disagree",
                '3': "Disagree",
                '4': "Neither Agree nor Disagree",
                '5': "Agree",
                '6': "Strongly Agree",
                '7': "Completely Agree",
            },
        )

    def test_action_method(self):
        action_result = self.likert_question.action()
        self.assertIn('key', action_result)
        self.assertIn('choices', action_result)
        self.assertEqual(
            action_result['choices'],
            {
                '1': "Completely Disagree",
                '2': "Strongly Disagree",
                '3': "Disagree",
                '4': "Neither Agree nor Disagree",
                '5': "Agree",
                '6': "Strongly Agree",
                '7': "Completely Agree",
            },
        )


class IconRangeTest(TestCase):

    def setUp(self):
        self.likert_question_icon = IconRangeQuestion(
            key='test_key', choices=ChoiceSet.objects.get(pk='LIKERT_ICONS_7').to_dict()
        )

    def test_initialization(self):
        self.assertEqual(self.likert_question_icon.key, 'test_key')
        self.assertEqual(self.likert_question_icon.view, 'ICON_RANGE')
        self.assertEqual(
            self.likert_question_icon.choices,
            {
                '1': 'fa-face-grin-hearts',
                '2': 'fa-face-grin',
                '3': 'fa-face-smile',
                '4': 'fa-face-meh',
                '5': 'fa-face-frown',
                '6': 'fa-face-frown-open',
                '7': 'fa-face-angry',
            },
        )

    def test_action_method(self):
        action_result = self.likert_question_icon.action()
        self.assertIn('key', action_result)
        self.assertIn('view', action_result)
        self.assertEqual(action_result['view'], 'ICON_RANGE')
        self.assertIn('choices', action_result)
        self.assertEqual(
            action_result['choices'],
            {
                '1': 'fa-face-grin-hearts',
                '2': 'fa-face-grin',
                '3': 'fa-face-smile',
                '4': 'fa-face-meh',
                '5': 'fa-face-frown',
                '6': 'fa-face-frown-open',
                '7': 'fa-face-angry',
            },
        )
