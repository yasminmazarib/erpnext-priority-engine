"""
Integration test: Inventory Issues API ↔ ERPNext

This test verifies that the skill API successfully integrates
with the ERPNext system and returns inventory issues data.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_inventory_issues_integration():
    """
    GIVEN ERPNext is running and accessible
    WHEN calling the inventory issues endpoint
    THEN the API should return a valid response structure
    """

    response = client.get("/inventory/issues?limit=5")

    # Basic HTTP validation
    assert response.status_code == 200

    data = response.json()

    # Response structure validation
    assert "issues" in data
    assert "count" in data

    assert isinstance(data["issues"], list)
    assert isinstance(data["count"], int)

    # Optional but useful: if there are issues, validate fields
    if len(data["issues"]) > 0:
        issue = data["issues"][0]

        assert "item_code" in issue
        assert "warehouse" in issue
        assert "actual_qty" in issue
        assert "reserved_qty" in issue
        assert "priority" in issue
        assert "reason" in issue
