from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from result.utils import apply_scoring_rule, get_result, prepare_result
from session.models import Session


class ResultUtilsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.create(rules='MUSICAL_PREFERENCES', slug='test')
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
        )

    def test_prepare_result_raises(self):
        result_id = prepare_result('labadi', self.session, scoring_rule='CORRECTNESS')
        self.assertIsNotNone(result_id)
        with self.assertRaises(ValueError):
            prepare_result('labada', self.session, scoring_rule='GIBBERISH')

    def test_result_invalid(self):
        result = Result.objects.create(
            participant=self.participant, question_key='some_key'
        )
        data = {'result_id': result.id}
        result = get_result(self.session, data)
        self.assertIsNotNone(result)
        new_participant = Participant.objects.create()
        result = Result.objects.create(
            participant=new_participant, question_key='another_key'
        )
        data = {'result_id': result.id}
        with self.assertRaises(Result.DoesNotExist):
            get_result(self.session, data)

    def test_apply_scoring_rule(self):
        result = Result.objects.create(
            session=self.session,
            question_key='test_result',
            scoring_rule='CORRECTNESS',
            expected_response='42',
            given_response='42',
        )
        data = {'result_id': result.id, 'value': '42'}
        score = apply_scoring_rule(result, data)
        self.assertEqual(score, 1)
