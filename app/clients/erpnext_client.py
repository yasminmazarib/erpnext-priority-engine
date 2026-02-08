import os
import json
import requests
from datetime import datetime, date
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import HTTPException

from app.models.priority_models import Invoice


# Load environment variables from .env
load_dotenv()


class ERPNextClient:
    def __init__(self):
        self.base_url = os.getenv("ERPNEXT_BASE_URL")
        self.api_key = os.getenv("ERPNEXT_API_KEY")
        self.api_secret = os.getenv("ERPNEXT_API_SECRET")

        # Debug – חייב לראות ערכים אמיתיים
        print("========== ERPNextClient INIT ==========")
        print("BASE URL:", self.base_url)
        print("API KEY:", self.api_key)
        print("API SECRET:", self.api_secret)
        print("=======================================")

        if not self.base_url:
            print("[WARN] ERPNEXT_BASE_URL is missing – using MOCK mode")

    # --------------------------------------------------
    # Helper
    # --------------------------------------------------
    def _calculate_days_overdue(self, due_date_str: Optional[str]) -> int:
        if not due_date_str:
            return 0
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            return max((date.today() - due_date).days, 0)
        except Exception:
            return 0

    # --------------------------------------------------
    # Get overdue Sales Invoices
    # --------------------------------------------------
    def get_overdue_invoices(self) -> List[Invoice]:

        # 🟡 MOCK MODE (אם אין ERPNext)
        if not self.base_url:
            return [
                Invoice("INV-001", "Test Corp", 100000, 45, date.today()),
                Invoice("INV-002", "Demo Ltd", 50000, 30, date.today()),
                Invoice("INV-003", "Sample Inc", 75000, 60, date.today()),
            ]

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
            "limit_page_length": 200,
        }

        try:
            response = requests.get(
                url,
                params=params,
                auth=(self.api_key, self.api_secret),   # ⭐ זה הפתרון הקריטי
                headers={
                    "Accept": "application/json"
                },
                timeout=10,
            )

            # Debug
            print("[DEBUG] ERPNext URL:", response.url)
            print("[DEBUG] Status:", response.status_code)
            print("[DEBUG] Raw response (first 200 chars):")
            print(response.text[:200])

            response.raise_for_status()

            data = response.json().get("data", [])
            invoices: List[Invoice] = []

            for inv in data:
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

        except requests.exceptions.Timeout:
            raise HTTPException(
                status_code=504,
                detail="ERPNext request timed out",
            )

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else 502
            body = e.response.text[:200] if e.response else "No response body"
            print("[ERROR] ERPNext HTTP Error:", status, body)

            raise HTTPException(
                status_code=502,
                detail=f"ERPNext HTTP error {status}",
            )

        except Exception as e:
            print("[ERROR] ERPNext connection error:", str(e))
            raise HTTPException(
                status_code=502,
                detail=f"ERPNext connection error: {str(e)}",
            )

    # --------------------------------------------------
    # Get Inventory Bins
    # --------------------------------------------------
    def get_bins(self):
        if not self.base_url:
            return []

        url = f"{self.base_url}/api/resource/Bin"

        params = {
            "fields": json.dumps([
                "item_code",
                "warehouse",
                "actual_qty",
                "reserved_qty",
                "projected_qty",
                "ordered_qty",
                "indented_qty",
            ]),
            "limit_page_length": 500,
        }

        try:
            response = requests.get(
                url,
                params=params,
                auth=(self.api_key, self.api_secret),
                headers={
                    "Accept": "application/json"
                },
                timeout=10,
            )

            response.raise_for_status()
            return response.json().get("data", [])

        except Exception as e:
            print("[ERROR] Failed to fetch bins:", e)
            return []