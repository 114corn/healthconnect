import json
import unittest
from my_api import app, db
from flask_testing import TestCase
from dotenv import load_dotenv
import os

load_dotenv()

class TestAPI(TestCase):
    
    def create_app(self):
        app.config['TESTing'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("TEST_DATABASE_URI")
        app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def post_request(self, endpoint, data):
        return self.client.post(endpoint, data=json.dumps(data), content_type='application/json')
    
    def get_request(self, endpoint, token=None):
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        return self.client.get(endpoint, headers=headers)
    
    def patch_request(self, endpoint, data, token=None):
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return self.client.patch(endpoint, data=json.dumps(data), content_type='application/json', headers=headers)

    def decode_response(self, response):
        return json.loads(response.data)

    def test_health_data_creation(self):
        response = self.post_request('/health-data', {
            'patient_id': 1,
            'data_type': 'blood_pressure',
            'value': '120/80',
            'timestamp': '2023-01-01T12:00:00'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('data_id', self.decode_response(response))

    def test_health_data_privacy(self):
        response = self.get_request('/health-data/2', 'some_invalid_token')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.decode_response(response)['message'], 'Unauthorized access.')

    def test_appointment_scheduling(self):
        response = self.post_request('/appointments', {
            'patient_id': 3,
            'doctor_id': 1,
            'scheduled_date': '2023-03-05T09:00:00'
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn('appointment_id', self.decode_response(response))

    def test_appointment_modification(self):
        response = self.patch_request('/appointments/1', {
            'scheduled_date': '2023-03-07T10:00:00'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('new_date', self.decode_response(response))

    def test_secure_endpoints(self):
        response = self.get_request('/secure-endpoint')
        self.assertEqual(response.status_code, 401)

    def test_health_data_analytics(self):
        valid_token = "Bearer valid_token_example"
        response = self.get_request('/analytics/health-dashboards', valid_token)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('analytics_data', self.decode_response(response))
        
if __name__ == '__main__':
    unittest.main()