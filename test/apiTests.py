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

    def post_request(self, endpoint, data, token=None):
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        return self.client.post(endpoint, data=json.dumps(data), content_type='application/json', headers=headers)
    
    def get_request(self, endpoint, token=None):
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        return self.client.get(endpoint, headers=headers)
    
    def patch_request(self, endpoint, data, token=None):
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        return self.client.patch(endpoint, data=json.dumps(data), content_url='application/json', headers=headers)

    def decode_response(self, response):
        return json.loads(response.data)
    
    def test_create_user_profile(self):
        response = self.post_request('/user-profile', {
            'user_id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'birthdate': '1985-02-25',
            'role': 'patient'
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn('profile_id', self.decode:{
            'name': 'John D. Doe',
            'email': 'john.d.doe@example.com'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('updated', self.decode_response(response))
    
    def test_get_user_profile(self):
        response = self.get_request('/user-profile/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_id', self.decode_response(response))
    
if __name__ == '__main__':
    unittest.main()