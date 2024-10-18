from django.test import TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from session.models import Session


n_results = 10


class SessionUtilsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.create(
            rules='MUSICAL_PREFERENCES', slug='test')
        cls.session = Session.objects.create(
            block=cls.block,
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

    def test_previous_score(self):
        result = self.session.last_result(["c", "d"])
        assert result.score == 9
