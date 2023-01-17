from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from result.models import Result
from session.models import Session
from experiment.util.questions import DEMOGRAPHICS, next_question, unasked_question

class UtilsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.experiment = Experiment.objects.create(rules='LISTENING_CONDITIONS', slug='test')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
        )
        cls.gender_result = Result.objects.create(
            participant=cls.participant,
            question_key='dgf_gender_identity',
            given_response='non_answer'
        )
        cls.result2 = Result.objects.create(
            participant=cls.participant,
            question_key='dgf_generation',
            given_response='boomer'
        )
        cls.questions = DEMOGRAPHICS[:3]
    
    def test_unasked_question(self):
        question = unasked_question(self.session, self.questions)
        assert question.key == 'dgf_country_of_origin'
    
    def test_next_question(self):
        Result.objects.create(
            participant=self.participant,
            question_key='dgf_country_of_origin',
            given_response='Luilekkerland'
        )
        question = next_question(self.session, self.questions)
        assert question == None
        # test that next_question creates empty result
        questions = DEMOGRAPHICS[:4]
        question = next_question(self.session, questions)
        assert Result.objects.count() == 4
        question = next_question(self.session, questions, continue_with_random=True)
        assert question != None
