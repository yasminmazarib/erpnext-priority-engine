import os
import json
import requests
from datetime import datetime, date
from dotenv import load_dotenv
from typing import List
from app.models.priority_models import Invoice

load_dotenv()


class ERPNextClient:
    def __init__(self):
        self.base_url = os.getenv("ERPNEXT_BASE_URL")
        self.api_key = os.getenv("ERPNEXT_API_KEY")
        self.api_secret = os.getenv("ERPNEXT_API_SECRET")

        self.headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json"
        }

    def fetch_overdue_invoices(self) -> List[Invoice]:
        """
        Fetch overdue invoices.
        If ERPNext is not configured (CI / tests), return mock data.
        """
        # 🧪 CI / tests
        if not self.base_url:
            return [
                Invoice("INV-001", "Test Corp", 100000, 45),
                Invoice("INV-002", "Demo Ltd", 50000, 30),
                Invoice("INV-003", "Sample Inc", 75000, 60),
            ]

        # 🌐 Real ERPNext call
        url = f"{self.base_url}/api/resource/Sales Invoice"
        today = date.today().isoformat()

        params = {
            "filters": json.dumps([
                ["docstatus", "=", 1],
                ["outstanding_amount", ">", 0],
                ["due_date", "<", today]
            ]),
            "fields": json.dumps([
                "name",
                "customer",
                "due_date",
                "outstanding_amount"
            ]),
            "limit_page_length": 500
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        invoices = []
        for inv in response.json().get("data", []):
            invoices.append(
                Invoice(
                    invoice_id=inv["name"],
                    customer=inv["customer"],
                    amount=inv.get("outstanding_amount", 0),
                    days_overdue=self._calculate_days_overdue(inv.get("due_date"))
                )
            )

        return invoices

    def _calculate_days_overdue(self, due_date: str) -> int:
        if not due_date:
            return 0
        try:
            due = datetime.strptime(due_date, "%Y-%m-%d").date()
            return max((date.today() - due).days, 0)
        except Exception:
            return 0
