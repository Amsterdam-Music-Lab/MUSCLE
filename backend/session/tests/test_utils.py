
from django.test import TestCase

from experiment.models import Experiment
from participant.models import Participant
from result.models import Result
from session.models import Session


n_results = 10


class SessionUtilsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.experiment = Experiment.objects.create(
            rules='MUSICAL_PREFERENCES', slug='test')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
        )
        # create results with various question_keys, and scores from 0 to 9
        for i in range(n_results):
            keys = ['a', 'a', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'd']
            Result.objects.create(
                session=cls.session,
                question_key=keys[i],
                score=i
            )
    
    def test_relevant_results_without_filter(self):
        results = self.session.get_relevant_results()
        assert results.count() == n_results
    
    def test_relevant_results_with_filter(self):
        results = self.session.get_relevant_results(['a', 'b'])
        assert results.count() == 6
        assert 'd' not in results.values_list('question_key')
    
    def test_previous_score(self):
        result = self.session.get_previous_result(['c', 'd'])
        assert result.score == 9
        
