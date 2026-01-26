from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Invoice:
    invoice_id: str
    customer: str
    amount: float
    days_overdue: int
    due_date: Optional[date] = None

    @property
    def priority(self) -> str:
        """
        Calculate priority level based on days overdue and amount.
        """
        if self.days_overdue >= 7 or self.amount >= 10000:
            return "HIGH"
        elif self.days_overdue >= 3 or self.amount >= 3000:
            return "MEDIUM"
        else:
            return "LOW"


@dataclass
class PriorityIssue:
    invoice_id: str
    customer: str
    amount: float
    days_overdue: int
    priority: str
    reason: Optional[str] = None

    def to_dict(self):
        return {
            "invoice_id": self.invoice_id,
            "customer": self.customer,
            "amount": self.amount,
            "days_overdue": self.days_overdue,
            "priority": self.priority,
            "reason": self.reason
        }
