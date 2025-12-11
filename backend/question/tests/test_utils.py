from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from question.models import Question, QuestionInList, QuestionList
from question.utils import get_unanswered_questions


class UtilsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        block = Block.objects.create(rules='RHYTHM_BATTERY_INTRO', slug='test')
        cls.result = Result.objects.create(
            participant=cls.participant,
            question_key='dgf_gender_identity',
            given_response='non_answer'
        )
        questions = Question.objects.filter(
            key__in=['dgf_country_of_origin', 'dgf_generation', 'dgf_gender_identity']
        )
        cls.question_list = QuestionList.objects.create(
            name='TEST_QUESTION_LIST', block=block, index=0
        )
        QuestionInList.objects.bulk_create(
            [
                QuestionInList(
                    questionlist=cls.question_list, question=question, index=index
                )
                for index, question in enumerate(questions)
            ]
        )

    def test_unanswered_question(self):
        question_iterator = get_unanswered_questions(
            self.participant, self.question_list.questions.all()
        )
        question = next(question_iterator)
        self.assertEqual(question.key, 'dgf_country_of_origin')
        question = next(question_iterator)
        self.assertEqual(question.key, 'dgf_generation')
        with self.assertRaises(StopIteration):
            question = next(question_iterator)
