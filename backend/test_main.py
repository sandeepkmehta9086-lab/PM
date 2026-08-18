import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from fastapi.testclient import TestClient

import database
from main import active_sessions, app


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        database.DATABASE_PATH = Path(self.temp_directory.name) / "test.db"
        active_sessions.clear()
        self.client_context = TestClient(app)
        self.client = self.client_context.__enter__()

    def tearDown(self):
        self.client_context.__exit__(None, None, None)
        self.temp_directory.cleanup()

    def login(self):
        return self.client.post(
            "/api/login", json={"username": "user", "password": "password"}
        )

    def test_login_creates_a_session_and_logout_clears_it(self):
        login = self.login()

        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.json(), {"username": "user"})
        self.assertEqual(self.client.get("/api/session").json()["authenticated"], True)

        self.assertEqual(self.client.post("/api/logout").status_code, 200)
        self.assertEqual(self.client.get("/api/session").json()["authenticated"], False)

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            "/api/login", json={"username": "user", "password": "wrong"}
        )

        self.assertEqual(response.status_code, 401)

    def test_board_is_created_for_the_authenticated_user(self):
        self.login()

        response = self.client.get("/api/board")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["columns"]), 5)
        with closing(sqlite3.connect(database.DATABASE_PATH)) as connection:
            self.assertEqual(
                connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
                ).fetchall(),
                [("boards",), ("users",)],
            )

    def test_board_updates_persist(self):
        self.login()
        board = self.client.get("/api/board").json()
        board["columns"][0]["title"] = "Prioritized"

        update = self.client.put("/api/board", json=board)

        self.assertEqual(update.status_code, 200)
        self.client_context.__exit__(None, None, None)
        active_sessions.clear()
        self.client_context = TestClient(app)
        self.client = self.client_context.__enter__()
        self.login()

        self.assertEqual(
            self.client.get("/api/board").json()["columns"][0]["title"], "Prioritized"
        )

    def test_board_requires_authentication(self):
        self.assertEqual(self.client.get("/api/board").status_code, 401)


if __name__ == "__main__":
    unittest.main()
