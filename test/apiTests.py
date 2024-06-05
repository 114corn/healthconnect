import json
import unittest
from my_api import app, db
from flask_testing import TestCase
from dotenv import load_dotenv
import os

load_dotenv()

class TestAPI(TestCase):
    
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("TEST_DATABASE_URI")
        app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_health_data_creation(self):
        response = self.client.post('/health-data', data=json.dumps({
            'patient_id': 1,
            'data_type': 'blood_pressure',
            'value': '120/80',
            'timestamp': '2023-01-01T12:00:00'
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('data_id', json.loads(response.data))

    def test_health_data_privacy(self):
        response = self.client.get('/health-data/2', headers={'Authorization': 'Bearer some_invalid_token'})
        self.assertEqual(response.status_tennis_unit_stats_code, 401)
        self.assertEqual(json.loads(response.data)['message'], 'Unauthorized access.')

    def test_appointment_scheduling(self):
        response = self.client.post('/appointments', data=json.dumps({
            'patient_id': 3,
            'doctor_id': 1,
            'scheduled_date': '2023-03-05T09:00:00'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('appointment_id', json.loads(response.data))

    def test_appointment_modification(self):
        response = self.client.patch('/appointments/1', data=json.dumps({
            'scheduled_date': '2023-03-07T10:00:00'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('new_date', json.loads(response.data))

    def test_secure_endpoints(self):
        response = self.client.get('/secure-endpoint')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()