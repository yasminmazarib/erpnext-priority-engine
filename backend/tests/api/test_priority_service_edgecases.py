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
    assert issue.reason == "High amount or long overdue"


def test_medium_priority_invoice():
    invoice = Invoice(
        invoice_id="INV-002",
        customer="Alpha Tech",
        amount=10000,
        days_overdue=20
    )

    issue = PriorityService.calculate_priority(invoice)

    # amount=10000 >= 10000 triggers HIGH, not MEDIUM
    assert issue.priority == "HIGH"
    assert issue.reason == "High amount or long overdue"


def test_low_priority_invoice():
    invoice = Invoice(
        invoice_id="INV-003",
        customer="West View Software",
        amount=5000,
        days_overdue=5
    )

    issue = PriorityService.calculate_priority(invoice)

    # amount=5000 >= 3000 AND days=5 >= 3 triggers MEDIUM, not LOW
    assert issue.priority == "MEDIUM"
    assert issue.reason == "Medium amount or moderate overdue"


def test_get_top_issues_sorted():
    """Test that get_top_issues sorts by priority and amount correctly."""
    invoices = [
        Invoice("INV-001", "A", 1500, 2),      # LOW (amount < 3000, days < 3)
        Invoice("INV-002", "B", 80000, 40),    # HIGH (amount >= 10000)
        Invoice("INV-003", "C", 5000, 5),      # MEDIUM (days >= 3 AND amount >= 3000)
        Invoice("INV-004", "D", 60000, 35),    # HIGH (amount >= 10000)
        Invoice("INV-005", "E", 1000, 1),      # LOW (amount < 3000, days < 3)
    ]

    results = PriorityService.get_top_issues(invoices)

    # First two should be HIGH, sorted by amount descending
    assert results[0].priority == "HIGH"
    assert results[1].priority == "HIGH"
    assert results[0].amount >= results[1].amount  # 80000 >= 60000
    
    # Third should be MEDIUM
    assert results[2].priority == "MEDIUM"
    
    # Rest should be LOW
    assert results[3].priority == "LOW"
    assert results[4].priority == "LOW"
