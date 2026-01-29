from fastapi import APIRouter, Query
from app.clients.erpnext_client import ERPNextClient
from app.services.priority_service import PriorityService

router = APIRouter()
erpnext_client = ERPNextClient()


# --------------------------------------------------
# Overdue invoices (RAW data – WITHOUT priority logic)
# --------------------------------------------------
@router.get("/priority/invoices")
def get_overdue_invoices(
    limit: int = Query(10, gt=0, description="Max number of invoices to return")
):
    """
    Return overdue invoices as raw data.
    Priority is NOT calculated here.
    """
    invoices = erpnext_client.get_overdue_invoices()

    if not invoices:
        return {
            "invoices": [],
            "count": 0,
            "message": "No overdue invoices found"
        }

    invoices = invoices[:limit]

    return {
        "invoices": [
            {
                "invoice_id": inv.invoice_id,
                "customer": inv.customer,
                "amount": inv.amount,
                "days_overdue": inv.days_overdue,
                "due_date": inv.due_date.isoformat() if inv.due_date else None
            }
            for inv in invoices
        ],
        "count": len(invoices)
    }


# --------------------------------------------------
# Priority issues (BUSINESS LOGIC via PriorityService)
# --------------------------------------------------
@router.get("/priority/issues")
def get_priority_issues(
    limit: int = Query(5, gt=0, description="Max number of issues to return"),
    min_days: int = Query(1, ge=0, description="Minimum days overdue"),
    min_amount: float = Query(0, ge=0, description="Minimum invoice amount"),
):
    """
    Fetch top priority issues using service-based logic.
    """
    issues = PriorityService.get_priority_issues(
        limit=limit,
        min_days=min_days,
        min_amount=min_amount,
    )

    if not issues:
        return {
            "top_issues": [],
            "message": "No priority issues found for given filters",
        }

    return {
        "top_issues": [issue.to_dict() for issue in issues]
    }
