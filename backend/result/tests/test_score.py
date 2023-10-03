from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from result.models import Result
from result.score import get_previous_result
from session.models import Session

class ResultScoreTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        participant = Participant.objects.create(unique_hash=42)
        experiment = Experiment.objects.create(
            rules='MUSICAL_PREFERENCES', slug='test')
        cls.session = Session.objects.create(
            experiment=experiment,
            participant=participant,
        )
        result1 = Result.objects.create(
            session=cls.session,
            question_key='question1',
            expected_response='yes',
            given_response='no'
        )
        result2 = Result.objects.create(
            session=cls.session,
            question_key='question2',
            expected_response='yes',
            given_response='yes'
        )
        result3 = Result.objects.create(
            session=cls.session,
            question_key='question3',
            expected_response=None,
            given_response='42'
        )
        result4 = Result.objects.create(
            session=cls.session,
            question_key='question4',
            expected_response='no',
            given_response='no'
        )
        cls.results = [result1, result2, result3, result4]
    
    def test_get_previous_results(self):
        result = get_previous_result(self.session, {'given_response': 'no'})
        assert result != None
        result = get_previous_result(self.session, {'section': 42})
        assert result == None