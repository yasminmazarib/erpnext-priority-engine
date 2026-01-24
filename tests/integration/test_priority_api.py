from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_priority_issues_success():
    response = client.get("/priority/issues")

    assert response.status_code == 200

    data = response.json()
    assert "top_issues" in data
    assert len(data["top_issues"]) > 0

    first_issue = data["top_issues"][0]
    assert "priority" in first_issue
    assert first_issue["priority"] in ["HIGH", "MEDIUM", "LOW"]


def test_priority_issues_with_limit():
    response = client.get("/priority/issues?limit=1")

    assert response.status_code == 200

    data = response.json()
    assert len(data["top_issues"]) == 1


def test_priority_issues_with_min_days():
    response = client.get("/priority/issues?min_days=30")

    assert response.status_code == 200

    data = response.json()
    for issue in data["top_issues"]:
        assert issue["days_overdue"] >= 30


def test_priority_issues_with_min_amount():
    response = client.get("/priority/issues?min_amount=50000")

    assert response.status_code == 200

    data = response.json()
    for issue in data["top_issues"]:
        assert issue["amount"] >= 50000

def test_no_results_response():
    response = client.get("/priority/issues?min_days=1000")

    assert response.status_code == 200

    data = response.json()
    assert data["top_issues"] == []
    assert "message" in data


def test_invalid_limit():
    response = client.get("/priority/issues?limit=0")

    assert response.status_code == 422
def test_priority_issues_with_limit():
    response = client.get("/priority/issues?limit=2")
    assert response.status_code == 200

    data = response.json()
    assert len(data["top_issues"]) == 2


def test_priority_issues_with_min_days():
    response = client.get("/priority/issues?min_days=30")
    assert response.status_code == 200

    data = response.json()
    for issue in data["top_issues"]:
        assert issue["days_overdue"] >= 30


def test_priority_issues_with_min_amount():
    response = client.get("/priority/issues?min_amount=50000")
    assert response.status_code == 200

    data = response.json()
    for issue in data["top_issues"]:
        assert issue["amount"] >= 50000

