from django.test import Client, TestCase

from experiment.models import Participant

class ParticipantCreationTest(TestCase):

    def setUp(self):
        self.client = Client(
            HTTP_USER_AGENT='Agent 007'
        )

    def test_access_info(self):
        self.client.get('/experiment/participant/')
        participant = Participant.objects.first()
        assert participant.access_info == 'Agent 007'

    def test_country_code(self):
        session = self.client.session
        session['country_code'] = 'BLA'
        session.save()
        self.client.get('/experiment/participant/')
        participant = Participant.objects.last()
        assert participant.country_code == 'BLA'


