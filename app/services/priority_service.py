from app.clients.erpnext_client import ERPNextClient
from app.models.priority_models import PriorityIssue


class PriorityService:

    @staticmethod
    def get_priority_issues(limit=5, min_days=1, min_amount=0):
        # ✅ בדיקת קלט – שייכת לפונקציה
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        client = ERPNextClient()
        invoices = client.fetch_overdue_invoices()

        issues = []

        for inv in invoices:
            if inv.days_overdue < min_days or inv.amount < min_amount:
                continue

            if inv.days_overdue > 30 and inv.amount > 50000:
                priority = "HIGH"
                reason = "Overdue more than 30 days and high amount"
            elif inv.days_overdue > 14:
                priority = "MEDIUM"
                reason = "Overdue more than 14 days"
            else:
                priority = "LOW"
                reason = "Recently overdue"

            issues.append(
                PriorityIssue(
                    invoice_id=inv.invoice_id,
                    customer=inv.customer,
                    amount=inv.amount,
                    days_overdue=inv.days_overdue,
                    priority=priority,
                    reason=reason
                )
            )

        priority_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
        issues.sort(key=lambda x: (priority_order[x.priority], -x.amount))

        return issues[:limit]
