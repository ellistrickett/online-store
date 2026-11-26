import unittest
from unittest.mock import MagicMock, patch
from app import app


class UsersTestCase(unittest.TestCase):
    # Ensure registration form renders on GET
    def test_register_form_page(self):
        tester = app.test_client(self)
        response = tester.get("/users/html-register")
        self.assertEqual(response.status_code, 200)

    # Ensure missing registration fields return 400
    def test_register_missing_fields(self):
        tester = app.test_client(self)
        response = tester.post(
            "/users/html-register",
            data=dict(email="shopper@example.com"),
        )
        self.assertEqual(response.status_code, 400)

    # Ensure getting a missing user returns 404
    @patch("routes.user_routes.get_connection")
    def test_get_user_not_found(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.__enter__.return_value = mock_cursor
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_get_conn.return_value = mock_conn

        tester = app.test_client(self)
        missing_user_id = 999
        response = tester.get(f"/users/{missing_user_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"No user found", response.data)

    # Ensure getting an existing user returns 200 and user data
    @patch("routes.user_routes.get_connection")
    def test_get_user_by_id(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            1,
            "ellis@example.com",
            "hashed_pw",
            "Ellis",
            "Trickett",
            "2026-01-01",
        )
        mock_cursor.__enter__.return_value = mock_cursor
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_get_conn.return_value = mock_conn

        tester = app.test_client(self)
        target_user_id = 1
        response = tester.get(f"/users/{target_user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ellis@example.com", response.data)


if __name__ == "__main__":
    unittest.main()