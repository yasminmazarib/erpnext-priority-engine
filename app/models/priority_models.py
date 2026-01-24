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
    priority: str = ""


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
