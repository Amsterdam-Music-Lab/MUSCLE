import json
import logging

from django.test import Client, TestCase

from experiment.models import Block
from participant.models import Participant
from result.models import Result
from session.models import Session

from result.utils import handle_results
from result.views import verify_session

class ResultTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = Participant.objects.create(unique_hash=42)
        cls.block = Block.objects.create(
            rules='MUSICAL_PREFERENCES', slug='test')
        cls.session = Session.objects.create(
            block=cls.block,
            participant=cls.participant,
        )

    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['participant_id'] = self.participant.id
        session.save()
        logging.disable(logging.CRITICAL)

    def test_get(self):
        response = self.client.get('/result/speed_swallow/')
        assert response.status_code == 204

    def test_create(self):
        result = Result.objects.create(
            question_key="speed_swallow",
            participant=self.participant
        )
        view = { "form": [
            {"key": "speed_swallow",
            "result_id": result.id,
            "view": "TEXT",
            "scale_steps": 7,
            "value": 'An African or a European swallow?'
            }
        ]}
        request = {
            "session_id": self.session.id,
            "json_data": json.dumps(view)
        }
        response = self.client.post('/result/score/', request)
        assert response.status_code == 200
        assert Result.objects.count() == 1
        response = self.client.get('/result/speed_swallow/')
        assert json.loads(response.content).get('answer') is not None
        response = self.client.post('/result/score/', request)
        assert Result.objects.count() == 1

    def test_handle_results_with_form(self):
        result1 = Result.objects.create(
            session=self.session
        )
        result2 = Result.objects.create(
            session=self.session
        )
        data = {
            'form': [
                {'key': 'silly_walk', 'value': 'very silly indeed', 'result_id': result1.pk},
                {'key': 'tea', 'value': 'Ms Two Lumps', 'result_id': result2.pk}],
            'config': {'something': 'registered as config'},
            'decision_time': 42
        }
        handle_results(data, self.session)
        assert self.session.result_count() == 2
        json_data = self.session.result_set.first().json_data
        assert json_data.get('config') is not None
        assert json_data.get('decision_time') == 42

    def test_score_view(self):
        request = {"session_id": self.session.id}
        response = self.client.post('/result/score/', request)
        self.assertEqual(response.status_code, 400)
        request.update({"json_data": json.dumps({"irrelevant": "data"})})
        response = self.client.post('/result/score/', request)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content.decode(), 'Invalid data')

    def test_intermediate_score(self):
        request = {"session_id": 424242}
        response = self.client.post('/result/intermediate_score/', request)
        self.assertEqual(response.status_code, 404)
        request = {"session_id": self.session.id}
        response = self.client.post('/result/intermediate_score/', request)
        self.assertEqual(response.status_code, 400)
        request.update({"json_data": json.dumps({"some": "json"})})
        response = self.client.post('/result/intermediate_score/', request)
        self.assertEqual(response.status_code, 200)

    def test_current_profile(self):
        response = self.client.get('/result/current_profile/', {})
        self.assertEqual(response.status_code, 200)
        new_client = Client()
        session = new_client.session
        session['participant_id'] = '-2'
        session.save()
        with self.assertRaises(Participant.DoesNotExist):
            response = new_client.get('/result/current_profile/', {})

    def test_verify_session(self):
        request_factory = self.client.post('/result/score/', {})
        response = verify_session(request_factory.wsgi_request)
        self.assertEqual(response.status_code, 400)
        request_factory = self.client.post('/result/score', {'session_id': 424242})
        response = verify_session(request_factory.wsgi_request)
        self.assertEqual(response.status_code, 404)
        request_factory = self.client.post(
            '/result/score', {'session_id': self.session.id}
        )
        response = verify_session(request_factory.wsgi_request)
        self.assertIsInstance(response, Session)
        self.session.finish()
        self.session.save()
        response = verify_session(request_factory.wsgi_request)
        self.assertEqual(response.status_code, 500)
