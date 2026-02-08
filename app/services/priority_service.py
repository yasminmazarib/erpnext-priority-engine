from typing import List, Optional

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
    def calculate_priority(
        invoice: Optional[Invoice]
    ) -> Optional[PriorityIssue]:
        # ✅ guard clause – חשוב ל-QA ו-coverage
        if invoice is None:
            return None

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
    def get_top_issues(invoices: List[Invoice]) -> List[PriorityIssue]:
        """
        Convert raw invoices to PriorityIssues and sort by priority + amount.
        This is the single source of truth for priority sorting.
        """
        if not invoices:
            return []

        issues = []
        for inv in invoices:
            issue = PriorityService.calculate_priority(inv)
            if issue:
                issues.append(issue)

        # Sort by priority order, then by amount (descending)
        issues.sort(
            key=lambda x: (
                PriorityService.PRIORITY_ORDER.get(x.priority, 99),
                -x.amount
            )
        )

        return issues

    @staticmethod
    def get_priority_issues(
        limit: int = 10,
        min_days: int = 1,
        min_amount: float = 0
    ) -> List[PriorityIssue]:
        """Fetch and filter invoices, then calculate priorities."""
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        client = ERPNextClient()
        invoices = client.get_overdue_invoices() or []

        # Filter by min_days and min_amount
        filtered = [
            inv for inv in invoices
            if inv.days_overdue >= min_days and inv.amount >= min_amount
        ]

        # Use get_top_issues to calculate and sort
        issues = PriorityService.get_top_issues(filtered)

        return issues[:limit]
