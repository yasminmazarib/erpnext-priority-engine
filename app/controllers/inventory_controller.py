# app/controllers/inventory_controller.py
from fastapi import APIRouter, Query
from app.clients.erpnext_client import ERPNextClient
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])

PRIORITY_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}


@router.get("/issues")
def get_inventory_issues(
    limit: int = Query(20, ge=1, description="Max number of inventory issues to return")
):
    client = ERPNextClient()

    # 🔹 שלב 1: משיכת Bin מ-ERPNext
    bins = client.get_bins()

    if not bins:
        return {
            "issues": [],
            "count": 0,
            "message": "No inventory data received from ERPNext"
        }

    # 🔹 שלב 2: חישוב בעיות מלאי
    issues = InventoryService.get_inventory_issues(bins)

    # 🔹 שלב 3: מיון לפי עדיפות (HIGH → LOW)
    issues.sort(
        key=lambda issue: PRIORITY_ORDER.get(issue.priority, 0),
        reverse=True
    )

    # 🔹 שלב 4: החלת limit
    issues = issues[:limit]

    if not issues:
        return {
            "issues": [],
            "count": 0,
            "message": "No inventory issues found"
        }

    return {
        "issues": [issue.to_dict() for issue in issues],
        "count": len(issues)
    }
