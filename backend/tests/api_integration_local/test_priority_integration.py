import os
import unittest
from fastapi.testclient import TestClient
from app.main import app


@unittest.skipUnless(
    os.getenv("ERPNEXT_BASE_URL") and os.getenv("ERPNEXT_API_KEY"),
    "ERPNext not configured – skipping integration tests"
)
class TestPriorityIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_priority_issues_returns_200(self):
        response = self.client.get("/priority/issues")
        self.assertEqual(response.status_code, 200)

    def test_priority_issues_with_limit(self):
        response = self.client.get("/priority/issues?limit=1")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
