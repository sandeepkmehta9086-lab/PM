import unittest

from fastapi.testclient import TestClient

from main import active_sessions, app


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        active_sessions.clear()
        self.client = TestClient(app)

    def test_login_creates_a_session_and_logout_clears_it(self):
        login = self.client.post(
            "/api/login", json={"username": "user", "password": "password"}
        )

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


if __name__ == "__main__":
    unittest.main()
