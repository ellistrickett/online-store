import unittest
from app import app


class AuthTestCase(unittest.TestCase):
    # Ensure login page loads
    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        self.assertEqual(response.status_code, 200)

    # Ensure login form posts and redirects to welcome page
    def test_login_post_redirect(self):
        tester = app.test_client(self)
        customer_name = "Ellis"
        response = tester.post(
            "/login",
            data=dict(name=customer_name),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"Welcome {customer_name} to the Online Store!".encode(), response.data)


if __name__ == "__main__":
    unittest.main()