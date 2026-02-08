import unittest
from unittest.mock import patch

from app.models.priority_models import Invoice
from app.services.priority_service import PriorityService


class TestPriorityService(unittest.TestCase):

    # ---------- calculate_priority ----------

    def test_high_priority_invoice(self):
        invoice = Invoice(
            invoice_id="INV-001",
            customer="Grant Plastics Ltd.",
            amount=67000,
            days_overdue=45
        )

        issue = PriorityService.calculate_priority(invoice)

        self.assertEqual(issue.priority, "HIGH")
        self.assertEqual(issue.reason, "High amount or long overdue")

    def test_medium_priority_invoice(self):
        invoice = Invoice(
            invoice_id="INV-002",
            customer="Alpha Tech",
            amount=10000,
            days_overdue=20
        )

        issue = PriorityService.calculate_priority(invoice)

        # amount >= 10000 → HIGH
        self.assertEqual(issue.priority, "HIGH")
        self.assertEqual(issue.reason, "High amount or long overdue")

    def test_low_priority_invoice(self):
        invoice = Invoice(
            invoice_id="INV-003",
            customer="West View Software",
            amount=5000,
            days_overdue=5
        )

        issue = PriorityService.calculate_priority(invoice)

        # days >= 3 OR amount >= 3000 → MEDIUM
        self.assertEqual(issue.priority, "MEDIUM")
        self.assertEqual(issue.reason, "Medium amount or moderate overdue")

    def test_calculate_priority_with_none_invoice(self):
        issue = PriorityService.calculate_priority(None)
        self.assertIsNone(issue)

    # ---------- get_top_issues ----------

    def test_get_top_issues_sorted(self):
        invoices = [
            Invoice("INV-001", "A", 1500, 2),     # LOW
            Invoice("INV-002", "B", 80000, 40),   # HIGH
            Invoice("INV-003", "C", 5000, 5),     # MEDIUM
            Invoice("INV-004", "D", 60000, 35),   # HIGH
            Invoice("INV-005", "E", 1000, 1),     # LOW
        ]

        results = PriorityService.get_top_issues(invoices)

        self.assertEqual(results[0].priority, "HIGH")
        self.assertEqual(results[1].priority, "HIGH")
        self.assertGreaterEqual(results[0].amount, results[1].amount)

        self.assertEqual(results[2].priority, "MEDIUM")
        self.assertEqual(results[3].priority, "LOW")
        self.assertEqual(results[4].priority, "LOW")

    def test_get_top_issues_with_empty_list(self):
        results = PriorityService.get_top_issues([])
        self.assertEqual(results, [])

    # ---------- get_priority_issues (mock ERPNext) ----------

    def test_get_priority_issues_limit_validation(self):
        with self.assertRaises(ValueError):
            PriorityService.get_priority_issues(limit=0)

    @patch("app.services.priority_service.ERPNextClient")
    def test_get_priority_issues_empty_result(self, mock_client):
        mock_client.return_value.get_overdue_invoices.return_value = []

        issues = PriorityService.get_priority_issues()
        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
