import json

from django.test import TestCase

from result.models import Result

class ResultTest(TestCase):
    
    def test_get(self):
        response = self.client.get('/result/speed_swallow/')
        assert response.status_code == 404
        
    def test_create(self):
        view = { "form": [
            {"key": "speed_swallow",
            "result_id": None,
            "view": "TEXT",
            "scale_steps": 7,
            "value": 'An African or an European swallow?'
            }
        ]}
        request = {
            "session_id": -1,
            "json_data": json.dumps(view)
        }
        response = self.client.post('/result/create/', request)
        assert Result.objects.count() == 1
        assert json.loads(response.content).get('status') == 'ok'
        response = self.client.get('/result/speed_swallow/')
        assert json.loads(response.content).get('answer') != None
        response = self.client.post('/result/create/', request)
        assert Result.objects.count() == 1