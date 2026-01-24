from app.models.priority_models import Invoice
from app.services.priority_service import PriorityService
from unittest.mock import patch


def test_high_priority_invoice():
    invoice = Invoice(
        invoice_id="INV-001",
        customer="Grant Plastics Ltd.",
        amount=67000,
        days_overdue=45
    )

    issue = PriorityService.calculate_priority(invoice)

    assert issue.priority == "HIGH"
    assert issue.reason == "Overdue more than 30 days and high amount"


def test_medium_priority_invoice():
    invoice = Invoice(
        invoice_id="INV-002",
        customer="Alpha Tech",
        amount=10000,
        days_overdue=20
    )

    issue = PriorityService.calculate_priority(invoice)

    assert issue.priority == "MEDIUM"


def test_low_priority_invoice():
    invoice = Invoice(
        invoice_id="INV-003",
        customer="West View Software",
        amount=5000,
        days_overdue=5
    )

    issue = PriorityService.calculate_priority(invoice)

    assert issue.priority == "LOW"


def test_get_top_issues_sorted():
    invoices = [
        Invoice("INV-001", "A", 10000, 10),
        Invoice("INV-002", "B", 80000, 40),   # HIGH
        Invoice("INV-003", "C", 20000, 20),   # MEDIUM
        Invoice("INV-004", "D", 60000, 35),   # HIGH
        Invoice("INV-005", "E", 3000, 3),
    ]

    results = PriorityService.get_top_issues(invoices)

    assert results[0].priority == "HIGH"
    assert results[1].priority == "HIGH"
    assert results[0].amount >= results[1].amount

def test_priority_issues_with_mocked_client():
    mocked_invoices = [
        {
            "invoice_id": "INV-100",
            "customer": "Mock Corp",
            "amount": 90000,
            "days_overdue": 60,
        }
    ]

    # אנחנו מחזירים Invoice-ים דרך ה-client
    from app.models.priority_models import Invoice
    invoices = [
        Invoice(
            invoice_id="INV-100",
            customer="Mock Corp",
            amount=90000,
            days_overdue=60
        )
    ]

    with patch("app.clients.erpnext_client.ERPNextClient.fetch_overdue_invoices", return_value=invoices):
        response = client.get("/priority/issues")

        assert response.status_code == 200
        data = response.json()
        assert len(data["top_issues"]) == 1
        assert data["top_issues"][0]["priority"] == "HIGH"
