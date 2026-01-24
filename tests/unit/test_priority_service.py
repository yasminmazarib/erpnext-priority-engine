from app.models.priority_models import Invoice
from app.services.priority_service import PriorityService


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
