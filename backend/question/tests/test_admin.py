from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from question.admin import (
    ChoiceListAdmin,
    duplicate_choice_list,
    duplicate_question,
    QuestionAdmin,
)
from question.models import Choice, ChoiceList, Question


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


class ChoiceListAdminTestCase(TestCase):

    def test_duplicate_choice_list(self):
        cs_admin = ChoiceListAdmin(model=ChoiceList, admin_site=AdminSite())
        request = RequestFactory().request()
        choicelists_to_duplicate = ChoiceList.objects.filter(key__startswith='LIKERT')
        duplicate_choice_list(cs_admin, request, choicelists_to_duplicate)
        new_choicelists = ChoiceList.objects.filter(
            key__startswith='LIKERT', key__endswith='1'
        )
        self.assertEqual(choicelists_to_duplicate.count(), new_choicelists.count())
        self.assertNotEqual(
            Choice.objects.filter(choicelist=new_choicelists.first()).count(), 0
        )
