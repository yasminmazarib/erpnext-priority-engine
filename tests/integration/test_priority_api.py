from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from app.models.priority_models import Invoice
import pytest


@pytest.fixture
def client():
    return TestClient(app)


def test_get_priority_issues_success(client):
    """Test that the API returns priority issues with expected fields."""
    response = client.get("/priority/issues")

    assert response.status_code == 200

    data = response.json()
    assert "top_issues" in data
    assert isinstance(data["top_issues"], list)

    if len(data["top_issues"]) > 0:
        first_issue = data["top_issues"][0]
        assert "priority" in first_issue
        assert first_issue["priority"] in ["HIGH", "MEDIUM", "LOW"]
        assert "invoice_id" in first_issue
        assert "customer" in first_issue
        assert "amount" in first_issue
        assert "days_overdue" in first_issue
        assert "reason" in first_issue


def test_priority_issues_with_limit(client):
    """Test that limit parameter restricts results correctly."""
    response = client.get("/priority/issues?limit=1")

    assert response.status_code == 200

    data = response.json()
    assert len(data["top_issues"]) <= 1


def test_priority_issues_with_min_days(client):
    """Test that min_days filter works correctly."""
    response = client.get("/priority/issues?min_days=30")

    assert response.status_code == 200

    data = response.json()
    for issue in data["top_issues"]:
        assert issue["days_overdue"] >= 30


def test_priority_issues_with_min_amount(client):
    """Test that min_amount filter works correctly."""
    response = client.get("/priority/issues?min_amount=50000")

    assert response.status_code == 200

    data = response.json()
    for issue in data["top_issues"]:
        assert issue["amount"] >= 50000


def test_priority_issues_combined_filters(client):
    """Test multiple filters combined."""
    response = client.get("/priority/issues?limit=5&min_days=10&min_amount=20000")

    assert response.status_code == 200

    data = response.json()
    assert len(data["top_issues"]) <= 5
    for issue in data["top_issues"]:
        assert issue["days_overdue"] >= 10
        assert issue["amount"] >= 20000


def test_no_results_response(client):
    """Test response when no invoices match filters."""
    response = client.get("/priority/issues?min_days=1000")

    assert response.status_code == 200

    data = response.json()
    assert data["top_issues"] == []
    assert "message" in data


def test_invalid_limit(client):
    """Test that invalid limit returns 422 (validation error)."""
    response = client.get("/priority/issues?limit=0")

    assert response.status_code == 422


def test_priority_sorting_order(client):
    """Test that HIGH priorities come before MEDIUM and MEDIUM before LOW."""
    response = client.get("/priority/issues?limit=100")

    assert response.status_code == 200

    data = response.json()
    issues = data["top_issues"]

    if len(issues) > 1:
        priority_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
        for i in range(len(issues) - 1):
            current_priority = priority_order[issues[i]["priority"]]
            next_priority = priority_order[issues[i + 1]["priority"]]
            if current_priority == next_priority:
                # If same priority, should be sorted by amount descending
                assert issues[i]["amount"] >= issues[i + 1]["amount"]
            else:
                assert current_priority <= next_priority


def test_priority_issues_with_mocked_high_priority(client):
    """Test that HIGH priority invoices are correctly identified."""
    invoices = [
        Invoice(
            invoice_id="INV-001",
            customer="Big Customer",
            amount=15000,
            days_overdue=2
        )
    ]

    with patch(
        "app.clients.erpnext_client.ERPNextClient.get_overdue_invoices",
        return_value=invoices
    ):
        response = client.get("/priority/issues")

        assert response.status_code == 200
        data = response.json()
        assert len(data["top_issues"]) == 1
        assert data["top_issues"][0]["priority"] == "HIGH"


def test_priority_issues_with_mocked_medium_priority(client):
    """Test that MEDIUM priority invoices are correctly identified."""
    invoices = [
        Invoice(
            invoice_id="INV-002",
            customer="Medium Customer",
            amount=3500,
            days_overdue=1
        )
    ]

    with patch(
        "app.clients.erpnext_client.ERPNextClient.get_overdue_invoices",
        return_value=invoices
    ):
        response = client.get("/priority/issues")

        assert response.status_code == 200
        data = response.json()
        assert len(data["top_issues"]) == 1
        assert data["top_issues"][0]["priority"] == "MEDIUM"


def test_priority_issues_with_mocked_low_priority(client):
    """Test that LOW priority invoices are correctly identified."""
    invoices = [
        Invoice(
            invoice_id="INV-003",
            customer="Low Customer",
            amount=1000,
            days_overdue=1
        )
    ]

    with patch(
        "app.clients.erpnext_client.ERPNextClient.get_overdue_invoices",
        return_value=invoices
    ):
        response = client.get("/priority/issues")

        assert response.status_code == 200
        data = response.json()
        assert len(data["top_issues"]) == 1
        assert data["top_issues"][0]["priority"] == "LOW"


def test_priority_issues_with_mocked_high_days_overdue(client):
    """Test that invoices overdue >= 7 days trigger HIGH priority."""
    invoices = [
        Invoice(
            invoice_id="INV-004",
            customer="Old Invoice",
            amount=1000,
            days_overdue=10
        )
    ]

    with patch(
        "app.clients.erpnext_client.ERPNextClient.get_overdue_invoices",
        return_value=invoices
    ):
        response = client.get("/priority/issues")

        assert response.status_code == 200
        data = response.json()
        assert len(data["top_issues"]) == 1
        assert data["top_issues"][0]["priority"] == "HIGH"


def test_priority_issues_with_mocked_high_amount(client):
    """Test that high amount invoices (>= 10000) trigger HIGH priority."""
    invoices = [
        Invoice(
            invoice_id="INV-005",
            customer="Expensive Invoice",
            amount=50000,
            days_overdue=1
        )
    ]

    with patch(
        "app.clients.erpnext_client.ERPNextClient.get_overdue_invoices",
        return_value=invoices
    ):
        response = client.get("/priority/issues")

        assert response.status_code == 200
        data = response.json()
        assert len(data["top_issues"]) == 1
        assert data["top_issues"][0]["priority"] == "HIGH"
