from dataclasses import dataclass
from typing import Optional


# 🔹 מייצג שורה אחת מ־Bin ב־ERPNext
@dataclass
class InventoryBin:
    item_code: str
    warehouse: str
    actual_qty: float
    reserved_qty: float = 0.0
    stock_value: Optional[float] = None

# 🔹 מייצג בעיית מלאי (מה שה־Skill מחזיר)
@dataclass
class InventoryIssue:
    item_code: str
    warehouse: str
    actual_qty: float
    reserved_qty: float
    priority: str          # HIGH / MEDIUM / LOW
    reason: str

    def to_dict(self):
        return {
            "item_code": self.item_code,
            "warehouse": self.warehouse,
            "actual_qty": self.actual_qty,
            "reserved_qty": self.reserved_qty,
            "priority": self.priority,
            "reason": self.reason,
        }
