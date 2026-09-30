from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from session.models import Session


n_results = 10


class SessionUtilsTest(TestCase):
    fixtures = ["testing"]

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.get(identifier='test-block')
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
        )
        # create results with various question_identifiers, and scores from 0 to 9
        identifiers = ['a', 'a', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'd']
        Result.objects.bulk_create(
            [
                Result(session=cls.session, question_identifier=identifiers[i], score=i)
                for i in range(n_results)
            ]
        )

    def test_previous_score(self):
        result = self.session.last_result(["c", "d"])
        assert result.score == 9
