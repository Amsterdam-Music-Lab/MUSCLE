from django.core.management import call_command
from django.test import TestCase


class CreateQuestionsTest(TestCase):

    def test_createquestions(self):
        from question.models import Question, QuestionGroup
        call_command('bootstrap')
        self.assertEqual(len(Question.objects.all()), 161) # Only built-in questions in test database
        self.assertEqual(len(QuestionGroup.objects.all()), 18) # Only built-in question groups in test database
        self.assertEqual(len(Question.objects.filter(key='dgf_country_of_origin')), 1)
        self.assertEqual(len(QuestionGroup.objects.filter(key='DEMOGRAPHICS')), 1)


