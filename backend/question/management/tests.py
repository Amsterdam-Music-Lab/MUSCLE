from django.core.management import call_command
from django.test import TestCase

from question.models import Choice, ChoiceList, Question


class CreateQuestionsTest(TestCase):
    fixtures = ['choice_lists', 'goldsmiths_msi', 'choices_goldsmiths_msi']

    def test_updatequestions(self):
        """at the beginning of this test,
        all question models from fixtures
        have been imported due to migration
        """
        n_choices = Choice.objects.count()
        n_choice_lists = ChoiceList.objects.count()
        n_questions = Question.objects.count()
        Choice.objects.all().delete()
        ChoiceList.objects.all().delete()
        Question.objects.all().delete()
        self.assertEqual(Choice.objects.count(), 0)
        self.assertEqual(ChoiceList.objects.count(), 0)
        self.assertEqual(Question.objects.count(), 0)
        call_command('updatequestions')
        self.assertGreater(Choice.objects.count(), n_choices)
        self.assertEqual(ChoiceList.objects.count(), n_choice_lists)
        self.assertGreater(Question.objects.count(), n_questions)
