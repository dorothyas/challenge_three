import unittest
from api.views import app
import json
from unittest import TestCase
from api.database import Connection 


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app= app
        self.client = self.app.test_client()
        self.sample_menu= {"foodname": "beef", "prices":12000}
        self.sample_signup={"user_id":1, "user_name":"Dorothy", "email":"dorothy@gmail.com", "user_password":"dorothy"}
        self.sample_login = {"username":"dorothy", "user_password":"dorothy"}
        self.db = Connection()    

    def test_can_add_menu(self):
        menu = self.client.post('/menu', json=self.sample_menu, content_type='application/json')
        self.assertEqual(menu.status_code, 200)

    def test_signup(self):
        response = self.client.post('/auth/signup', json=self.sample_signup, content_type='application/json')
        self.assertEqual(response.status_code, 201)











if __name__ == '__main__':
    unittest.main()
