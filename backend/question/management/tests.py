from django.test import TestCase
from question.questions import create_default_questions


class CreateQuestionsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_questions()

    def test_createquestions(self):
        from question.models import Question, QuestionGroup
        self.assertEqual(
            len(Question.objects.all()), 176
        )  # Only built-in questions in test database
        self.assertEqual(len(QuestionGroup.objects.all()), 18) # Only built-in question groups in test database
        self.assertEqual(len(Question.objects.filter(key='dgf_country_of_origin')), 1)
        self.assertEqual(len(QuestionGroup.objects.filter(key='DEMOGRAPHICS')), 1)
