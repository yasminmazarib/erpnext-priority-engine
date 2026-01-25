from fastapi import APIRouter, Query
from app.services.priority_service import PriorityService
from app.clients.erpnext_client import ERPNextClient

router = APIRouter()
erpnext_client = ERPNextClient()


@router.get("/priority/invoices")
def get_overdue_invoices():
    """Fetch overdue invoices from ERPNext."""
    invoices = erpnext_client.get_overdue_invoices()
    
    if not invoices:
        return {
            "invoices": [],
            "count": 0,
            "message": "No overdue invoices found"
        }
    
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


@router.get("/priority/issues")
def get_priority_issues(
    limit: int = Query(5, gt=0, description="Max number of issues to return"),
    min_days: int = Query(1, ge=0, description="Minimum days overdue"),
    min_amount: float = Query(0, ge=0, description="Minimum invoice amount"),
):
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
        "top_issues": [i.to_dict() for i in issues]
    }

