from typing import Any, Dict, List, Optional, Union

from app.models.inventory_models import InventoryBin, InventoryIssue


class InventoryService:
    PRIORITY_ORDER = {
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }

    @staticmethod
    def _to_inventory_bin(raw: Union[InventoryBin, Dict[str, Any]]) -> Optional[InventoryBin]:
        """
        ERPNext מחזיר dict.
        הפונקציה הזו ממירה dict -> InventoryBin.
        אם זה כבר InventoryBin, מחזירה אותו כמו שהוא.
        אם חסרים שדות קריטיים, מחזירה None.
        """
        if isinstance(raw, InventoryBin):
            return raw

        if not isinstance(raw, dict):
            return None

        item_code = raw.get("item_code")
        warehouse = raw.get("warehouse")

        if not item_code or not warehouse:
            return None

        # ברירת מחדל 0 כדי לא לקרוס
        actual_qty = float(raw.get("actual_qty") or 0)
        reserved_qty = float(raw.get("reserved_qty") or 0)

        # אם המודל שלך כולל שדות נוספים (projected/ordered/indented)
        # אפשר להעביר אותם כאן גם, אבל לא חובה ללוגיקה הנוכחית
        return InventoryBin(
            item_code=item_code,
            warehouse=warehouse,
            actual_qty=actual_qty,
            reserved_qty=reserved_qty,
        )

    @staticmethod
    def calculate_priority(bin_obj: InventoryBin) -> Optional[InventoryIssue]:
        qty = float(bin_obj.actual_qty or 0)

        if qty >= 200:
            priority = "HIGH"
            reason = "High quantity stock"
        elif qty >= 100:
            priority = "MEDIUM"
            reason = "Medium quantity stock"
        elif qty >= 20:
            priority = "LOW"
            reason = "Low quantity stock"
        else:
            return None

        return InventoryIssue(
            item_code=bin_obj.item_code,
            warehouse=bin_obj.warehouse,
            actual_qty=bin_obj.actual_qty,
            reserved_qty=bin_obj.reserved_qty,
            priority=priority,
            reason=reason,
        )

    @staticmethod
    def get_inventory_issues(
        bins: List[Union[InventoryBin, Dict[str, Any]]],
        limit: int = 20
    ) -> List[InventoryIssue]:

        issues: List[InventoryIssue] = []

        for raw in bins:
            bin_obj = InventoryService._to_inventory_bin(raw)
            if not bin_obj:
                continue

            issue = InventoryService.calculate_priority(bin_obj)
            if issue:
                issues.append(issue)

        # מיון עסקי נכון ודטרמיניסטי
        issues.sort(
            key=lambda x: (
                InventoryService.PRIORITY_ORDER.get(x.priority, 0),
                float(x.actual_qty or 0),
            ),
            reverse=True
        )

        return issues[:limit]
