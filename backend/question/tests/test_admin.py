from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from question.admin import (
    ChoiceSetAdmin,
    duplicate_choice_set,
    duplicate_question,
    QuestionAdmin,
)
from question.models import Choice, ChoiceSet, Question


class QuestionAdminTestCase(TestCase):

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
        self.assertIsNone(country_open.choices)
        country_closed = duplicates.exclude(key__contains='open').first()
        self.assertEqual(country_closed.choices.choices.count(), 249)


class ChoiceSetAdminTestCase(TestCase):

    def test_duplicate_choice_set(self):
        cs_admin = ChoiceSetAdmin(model=ChoiceSet, admin_site=AdminSite())
        request = RequestFactory().request()
        choicesets_to_duplicate = ChoiceSet.objects.filter(key__startswith='LIKERT')
        duplicate_choice_set(cs_admin, request, choicesets_to_duplicate)
        new_choicesets = ChoiceSet.objects.filter(
            key__startswith='LIKERT', key__endswith='1'
        )
        self.assertEqual(choicesets_to_duplicate.count(), new_choicesets.count())
        self.assertNotEqual(
            Choice.objects.filter(set=new_choicesets.first()).count(), 0
        )
