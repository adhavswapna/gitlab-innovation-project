# test_app.py
import unittest
from app import app

class TestApp(unittest.TestCase):
    def test_home_route(self):
        client = app.test_client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
