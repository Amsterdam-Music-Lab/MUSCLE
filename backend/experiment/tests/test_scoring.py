from django.test import Client, TestCase

from experiment.models import Result, Session

class ScoringTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.session = Session.objects.create()
    
    def test_likert_score(self):
        session_id = self.session.pk
        client_request = {
            
        }
        

