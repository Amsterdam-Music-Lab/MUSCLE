from django.core.management import call_command
from django.test import TestCase

from question.models import Choice, ChoiceSet, Question

class CreateQuestionsTest(TestCase):

    def test_updatequestions(self):
        """at the beginning of this test,
        all question models from fixtures
        have been imported due to migration
        """
        n_choices = Choice.objects.count()
        n_choice_sets = ChoiceSet.objects.count()
        n_questions = Question.objects.count()
        Choice.objects.all().delete()
        ChoiceSet.objects.all().delete()
        Question.objects.all().delete()
        self.assertEqual(Choice.objects.count(), 0)
        self.assertEqual(ChoiceSet.objects.count(), 0)
        self.assertEqual(Question.objects.count(), 0)
        call_command('updatequestions')
        self.assertEqual(Choice.objects.count(), n_choices)
        self.assertEqual(ChoiceSet.objects.count(), n_choice_sets)
        self.assertEqual(Question.objects.count(), n_questions)

    def test_translatequestions(self):
        msi_24 = Question.objects.get(pk='msi_24_music_addiction')
        self.assertIsNone(msi_24.text_nl)
        with self.settings(TESTING=True):
            call_command('translatequestions')
        msi_24 = Question.objects.get(pk='msi_24_music_addiction')
        self.assertIn('verslaving', msi_24.text_nl)
