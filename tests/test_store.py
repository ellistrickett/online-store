import unittest
from app import app

class StoreTestCase(unittest.TestCase):
    # Ensure that Flask was set up correctly
    def test_login_route(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type="html/text")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()