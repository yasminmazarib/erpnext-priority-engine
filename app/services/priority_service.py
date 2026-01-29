from app.clients.erpnext_client import ERPNextClient
from app.models.priority_models import PriorityIssue, Invoice


class PriorityService:
    """
    Business rules for invoice prioritization:
    -----------------------------------------
    HIGH   -> days_overdue >= 7 OR amount >= 10000
    MEDIUM -> days_overdue >= 3 OR amount >= 3000
    LOW    -> otherwise
    """

    PRIORITY_ORDER = {
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    @staticmethod
    def calculate_priority(invoice: Invoice) -> PriorityIssue:
        if invoice.days_overdue >= 7 or invoice.amount >= 10000:
            return PriorityIssue(
                invoice.invoice_id,
                invoice.customer,
                invoice.amount,
                invoice.days_overdue,
                "HIGH",
                "High amount or long overdue"
            )

        if invoice.days_overdue >= 3 or invoice.amount >= 3000:
            return PriorityIssue(
                invoice.invoice_id,
                invoice.customer,
                invoice.amount,
                invoice.days_overdue,
                "MEDIUM",
                "Medium amount or moderate overdue"
            )

        return PriorityIssue(
            invoice.invoice_id,
            invoice.customer,
            invoice.amount,
            invoice.days_overdue,
            "LOW",
            "Recently overdue with low amount"
        )

    @staticmethod
    def get_top_issues(invoices: list) -> list:
        """
        Convert raw invoices to PriorityIssues and sort by priority + amount.
        This is the single source of truth for priority sorting.
        """
        issues = [
            PriorityService.calculate_priority(inv)
            for inv in invoices
        ]

        # Sort by priority order, then by amount (descending)
        issues.sort(
            key=lambda x: (
                PriorityService.PRIORITY_ORDER[x.priority],
                -x.amount
            )
        )

        return issues

    @staticmethod
    def get_priority_issues(limit=10, min_days=1, min_amount=0):
        """Fetch and filter invoices, then calculate priorities."""
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        client = ERPNextClient()
        invoices = client.get_overdue_invoices()

        # Filter by min_days and min_amount
        filtered = [
            inv for inv in invoices
            if inv.days_overdue >= min_days and inv.amount >= min_amount
        ]

        # Use get_top_issues to calculate and sort
        issues = PriorityService.get_top_issues(filtered)

        return issues[:limit]
