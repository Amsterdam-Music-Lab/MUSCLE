from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from question.admin import duplicate_question, QuestionAdmin
from question.models import Question
from question.questions import create_default_questions

class AdminTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_questions()

    def test_duplicate_question(self):
        question_admin = QuestionAdmin(model=Question, admin_site=AdminSite())
        request = RequestFactory().request()
        questions_to_duplicate = Question.objects.filter(key__startswith='dgf_country_of_origin')
        duplicate_question(question_admin, request, questions_to_duplicate)
        duplicates = Question.objects.filter(
            key__startswith='dgf_country_of_origin', key__endswith='1'
        )
        self.assertEqual(duplicates.count(), 2)
        country_open = duplicates.get(key__contains='open')
        self.assertEqual(country_open.choice_set.count(), 0)
        country_choices = duplicates.exclude(key__contains='open').first()
        self.assertEqual(country_choices.choice_set.count(), 249)
