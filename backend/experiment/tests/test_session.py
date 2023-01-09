from django.test import TestCase

from experiment.models import Experiment, Participant, Result, Session

class SessionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.experiment = Experiment.objects.create(rules='LISTENING_CONDITIONS', slug='test')
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            participant=cls.participant,
        )
    
    def test_total_questions(self):   
        assert self.session.total_questions() == 0
        Result.objects.create(
            session=self.session
        )
        assert self.session.total_questions() == 1
    
    def test_skipped_answered_questions(self):
        Result.objects.create(
            session=self.session,
            given_response=''
        )
        assert self.session.answered_questions() == 0
        Result.objects.create(
            session=self.session,
            given_response='Something really elaborate'
        )
        assert self.session.skipped_questions() == 1
        assert self.session.answered_questions() == 1
        Result.objects.create(
            session=self.session,
            given_response=''
        )
        assert self.session.skipped_questions() == 2