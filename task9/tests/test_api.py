"""Endpoint tests that do not depend on external network access."""

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_post_returns_greeting_for_required_header(self) -> None:
        response = self.client.post("/", headers={"Test": "Hello"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello, World!")

    def test_post_returns_403_without_header(self) -> None:
        response = self.client.post("/")

        self.assertEqual(response.status_code, 403)

    def test_post_returns_403_for_wrong_header_value(self) -> None:
        response = self.client.post("/", headers={"Test": "Wrong"})

        self.assertEqual(response.status_code, 403)

    @patch("app.main.ping_target", return_value=True)
    def test_health_returns_ok_when_ping_succeeds(self, _ping_mock) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "OK")

    @patch("app.main.ping_target", return_value=False)
    def test_health_returns_503_when_ping_fails(self, _ping_mock) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.text, "Service Unavailable")


if __name__ == "__main__":
    unittest.main()
