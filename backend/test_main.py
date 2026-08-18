import json
import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

import database
import openrouter
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

    def test_ai_connectivity_requires_authentication(self):
        self.assertEqual(self.client.post("/api/ai/test").status_code, 401)

    def test_ai_connectivity_uses_openrouter(self):
        self.login()
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "4"}}]
        }

        with (
            patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}),
            patch("openrouter.httpx.post", return_value=mock_response) as post,
        ):
            response = self.client.post("/api/ai/test")

        self.assertEqual(response.json(), {"response": "4"})
        self.assertEqual(post.call_args.kwargs["headers"]["Authorization"], "Bearer test-key")

    def test_ai_chat_requires_authentication(self):
        response = self.client.post(
            "/api/ai/chat", json={"message": "Summarize the board.", "history": []}
        )

        self.assertEqual(response.status_code, 401)

    def test_ai_chat_returns_a_response_without_changing_the_board(self):
        self.login()
        board = self.client.get("/api/board").json()

        with patch(
            "openrouter.ask_structured",
            return_value={"response": "The board has five columns.", "boardUpdate": None},
        ) as ask:
            response = self.client.post(
                "/api/ai/chat",
                json={
                    "message": "How many columns are there?",
                    "history": [{"role": "user", "content": "Hello"}],
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["boardUpdate"], None)
        self.assertEqual(ask.call_args.args[0], board)
        self.assertEqual(
            ask.call_args.args[1], [{"role": "user", "content": "Hello"}]
        )
        self.assertEqual(self.client.get("/api/board").json(), board)

    def test_ai_chat_persists_a_valid_board_update(self):
        self.login()
        updated_board = self.client.get("/api/board").json()
        updated_board["columns"][0]["title"] = "Planned"

        with patch(
            "openrouter.ask_structured",
            return_value={
                "response": "I renamed the first column.",
                "boardUpdate": updated_board,
            },
        ):
            response = self.client.post(
                "/api/ai/chat", json={"message": "Rename Backlog to Planned"}
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.client.get("/api/board").json()["columns"][0]["title"], "Planned"
        )

    def test_ai_chat_rejects_an_invalid_board_update(self):
        self.login()
        original_board = self.client.get("/api/board").json()

        with patch(
            "openrouter.ask_structured",
            return_value={
                "response": "I made a change.",
                "boardUpdate": {"columns": []},
            },
        ):
            response = self.client.post(
                "/api/ai/chat", json={"message": "Make a change"}
            )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(self.client.get("/api/board").json(), original_board)

    def test_structured_openrouter_call_uses_json_schema(self):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {"response": "No changes.", "boardUpdate": None}
                        )
                    }
                }
            ]
        }

        with (
            patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}),
            patch("openrouter.httpx.post", return_value=mock_response) as post,
        ):
            result = openrouter.ask_structured(
                {"columns": [], "cards": {}},
                [],
                "Summarize the board.",
                {"type": "object"},
            )

        self.assertEqual(result, {"response": "No changes.", "boardUpdate": None})
        response_format = post.call_args.kwargs["json"]["response_format"]
        self.assertEqual(response_format["type"], "json_schema")
        self.assertTrue(response_format["json_schema"]["strict"])


if __name__ == "__main__":
    unittest.main()
