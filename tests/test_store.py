import unittest
from unittest.mock import MagicMock, patch
from app import app


class StoreTestCase(unittest.TestCase):
    # Ensure store home page loads
    def test_home_route(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.status_code, 200)

    # Ensure database status endpoint returns connection info
    @patch("routes.db_routes.get_connection")
    def test_db_status_route(self, mock_get_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("store_db", "store_user")
        mock_cursor.__enter__.return_value = mock_cursor
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_get_conn.return_value = mock_conn

        tester = app.test_client(self)
        response = tester.get("/sys-status/db")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"store_db", response.data)


if __name__ == "__main__":
    unittest.main()