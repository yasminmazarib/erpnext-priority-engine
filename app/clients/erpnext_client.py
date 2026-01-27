import os
import json
import requests
from datetime import datetime, date
from dotenv import load_dotenv
from typing import List, Optional

from app.models.priority_models import Invoice

# טוען משתני סביבה מקובץ .env
load_dotenv()


class ERPNextClient:
    def __init__(self):
        self.base_url = os.getenv("ERPNEXT_BASE_URL")
        self.api_key = os.getenv("ERPNEXT_API_KEY")
        self.api_secret = os.getenv("ERPNEXT_API_SECRET")

        self.headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json",
        }

        # לוג בסיסי – עוזר להבין אם env נטען
        print("ERPNext BASE URL:", self.base_url)

    # --------------------------------------------------
    # Helper: calculate days overdue
    # --------------------------------------------------
    def _calculate_days_overdue(self, due_date_str: Optional[str]) -> int:
        if not due_date_str:
            return 0
        try:
            due = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            return max((date.today() - due).days, 0)
        except Exception:
            return 0

    # --------------------------------------------------
    # Get ALL sales invoices
    # --------------------------------------------------
    def get_sales_invoices(self) -> List[Invoice]:
        if not self.base_url:
            return []

        url = f"{self.base_url}/api/resource/Sales%20Invoice"
        params = {
            "fields": json.dumps([
                "name",
                "customer",
                "due_date",
                "outstanding_amount",
            ]),
            "limit_page_length": 500,
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()

            invoices: List[Invoice] = []

            for inv in response.json().get("data", []):
                due_date_str = inv.get("due_date")

                invoices.append(
                    Invoice(
                        invoice_id=inv.get("name"),
                        customer=inv.get("customer"),
                        amount=inv.get("outstanding_amount", 0),
                        days_overdue=self._calculate_days_overdue(due_date_str),
                        due_date=datetime.strptime(due_date_str, "%Y-%m-%d").date()
                        if due_date_str else None,
                    )
                )

            return invoices

        except Exception as e:
            print(f"❌ Error fetching sales invoices: {e}")
            return []

    # --------------------------------------------------
    # Get OVERDUE invoices – sorted by PRIORITY then AMOUNT
    # --------------------------------------------------
    def get_overdue_invoices(self) -> List[Invoice]:
        PRIORITY_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}

        if not self.base_url:
            invoices = [
                Invoice("INV-001", "Test Corp", 100000, 45, date.today()),
                Invoice("INV-002", "Demo Ltd", 50000, 30, date.today()),
                Invoice("INV-003", "Sample Inc", 75000, 60, date.today()),
            ]

            invoices.sort(
                key=lambda x: (PRIORITY_ORDER[x.priority], x.amount),
                reverse=True,
            )
            return invoices

        url = f"{self.base_url}/api/resource/Sales%20Invoice"
        today = date.today().isoformat()

        params = {
            "filters": json.dumps([
                ["docstatus", "=", 1],
                ["outstanding_amount", ">", 0],
                ["due_date", "<", today],
            ]),
            "fields": json.dumps([
                "name",
                "customer",
                "due_date",
                "outstanding_amount",
            ]),
            "limit_page_length": 500,
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()

            invoices: List[Invoice] = []

            for inv in response.json().get("data", []):
                due_date_str = inv.get("due_date")

                invoices.append(
                    Invoice(
                        invoice_id=inv.get("name"),
                        customer=inv.get("customer"),
                        amount=inv.get("outstanding_amount", 0),
                        days_overdue=self._calculate_days_overdue(due_date_str),
                        due_date=datetime.strptime(due_date_str, "%Y-%m-%d").date()
                        if due_date_str else None,
                    )
                )

            invoices.sort(
                key=lambda x: (PRIORITY_ORDER[x.priority], x.amount),
                reverse=True,
            )

            return invoices

        except Exception as e:
            print(f"❌ Error fetching overdue invoices: {e}")
            return []

    # --------------------------------------------------
    # Get Inventory Bins (Stock Snapshot) ✅ מתוקן סופית
    # --------------------------------------------------
    def get_bins(self):
        if not self.base_url:
            return []

        url = f"{self.base_url}/api/resource/Bin"

        params = {
            # 🔥 כל השדות ש-InventoryService עלול להשתמש בהם
            "fields": json.dumps([
                "item_code",
                "warehouse",
                "actual_qty",
                "reserved_qty",
                "projected_qty",
                "ordered_qty",
                "indented_qty"
            ]),
            "limit_page_length": 500
        }

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )

            print("ERPNext bins URL:", response.url)
            print("status:", response.status_code)

            response.raise_for_status()
            return response.json().get("data", [])

        except Exception as e:
            print(f"❌ Error fetching inventory bins: {e}")
            return []