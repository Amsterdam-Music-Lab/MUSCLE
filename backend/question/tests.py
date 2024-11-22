from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from session.models import Session
from .demographics import DEMOGRAPHICS
from .utils import unanswered_questions, total_unanswered_questions
from question.questions import create_default_questions


class UtilsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_questions()
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.create(
            rules='RHYTHM_BATTERY_INTRO', slug='test')
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
        )
        cls.result = Result.objects.create(
            participant=cls.participant,
            question_key='dgf_gender_identity',
            given_response='non_answer'
        )
        cls.questions = DEMOGRAPHICS[:3]

    def test_unanswered_questions(self):
        questions = unanswered_questions(self.participant, self.questions)
        question = next(questions)
        assert question.key == 'dgf_generation'
        question = next(questions)
        assert question.key == 'dgf_country_of_origin'

    def test_total_unanswered_questions(self):
        number = total_unanswered_questions(self.participant, self.questions)
        assert number == 2
