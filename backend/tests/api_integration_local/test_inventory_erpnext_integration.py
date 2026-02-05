import os
import unittest
from fastapi.testclient import TestClient
from app.main import app


@unittest.skipUnless(
    os.getenv("ERPNEXT_BASE_URL") and os.getenv("ERPNEXT_API_KEY"),
    "ERPNext not configured – skipping integration tests"
)
class TestInventoryIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_inventory_issues_integration(self):
        response = self.client.get("/inventory/issues?limit=5")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("issues", data)
        self.assertIn("count", data)

        self.assertIsInstance(data["issues"], list)
        self.assertIsInstance(data["count"], int)

        if len(data["issues"]) > 0:
            issue = data["issues"][0]
            self.assertIn("item_code", issue)
            self.assertIn("warehouse", issue)
            self.assertIn("actual_qty", issue)
            self.assertIn("reserved_qty", issue)
            self.assertIn("priority", issue)
            self.assertIn("reason", issue)


if __name__ == "__main__":
    unittest.main()
