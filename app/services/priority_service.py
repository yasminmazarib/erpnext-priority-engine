from app.clients.erpnext_client import ERPNextClient
from app.models.priority_models import PriorityIssue


class PriorityService:

    @staticmethod
    def calculate_priority(invoice):
        if invoice.days_overdue > 30 and invoice.amount > 50000:
            return PriorityIssue(
                invoice.invoice_id,
                invoice.customer,
                invoice.amount,
                invoice.days_overdue,
                "HIGH",
                "Overdue more than 30 days and high amount"
            )
        elif invoice.days_overdue > 14:
            return PriorityIssue(
                invoice.invoice_id,
                invoice.customer,
                invoice.amount,
                invoice.days_overdue,
                "MEDIUM",
                "Overdue more than 14 days"
            )
        else:
            return PriorityIssue(
                invoice.invoice_id,
                invoice.customer,
                invoice.amount,
                invoice.days_overdue,
                "LOW",
                "Recently overdue"
            )

    @staticmethod
    def get_top_issues(invoices):
        issues = [PriorityService.calculate_priority(inv) for inv in invoices]

        priority_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
        issues.sort(key=lambda x: (priority_order[x.priority], -x.amount))

        return issues

    @staticmethod
    def get_priority_issues(limit=5, min_days=1, min_amount=0):
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        client = ERPNextClient()
        invoices = client.fetch_overdue_invoices()

        filtered = [
            inv for inv in invoices
            if inv.days_overdue >= min_days and inv.amount >= min_amount
        ]

        issues = PriorityService.get_top_issues(filtered)
        return issues[:limit]
