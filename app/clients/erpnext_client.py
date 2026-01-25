import os
import json
import requests
from datetime import datetime, date
from dotenv import load_dotenv
from typing import List, Dict, Any
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

    def get_sales_invoices(self) -> List[Invoice]:
        """Fetch all sales invoices from ERPNext."""
        url = f"{self.base_url}/api/resource/Sales Invoice"
        
        params = {
            "fields": json.dumps([
                "name",
                "customer",
                "due_date",
                "outstanding_amount",
                "docstatus"
            ]),
            "limit_page_length": 500
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        invoices = []
        for inv in response.json()["data"]:
            invoices.append(
                Invoice(
                    invoice_id=inv["name"],
                    customer=inv["customer"],
                    amount=inv.get("outstanding_amount", 0),
                    days_overdue=self._calculate_days_overdue(inv.get("due_date")),
                    due_date=datetime.strptime(inv.get("due_date", ""), "%Y-%m-%d").date() if inv.get("due_date") else None
                )
            )
        return invoices

    def get_overdue_invoices(self) -> List[Invoice]:
        """Fetch overdue invoices from ERPNext."""
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
        for inv in response.json()["data"]:
            invoices.append(
                Invoice(
                    invoice_id=inv["name"],
                    customer=inv["customer"],
                    amount=inv.get("outstanding_amount", 0),
                    days_overdue=self._calculate_days_overdue(inv.get("due_date")),
                    due_date=datetime.strptime(inv.get("due_date", ""), "%Y-%m-%d").date() if inv.get("due_date") else None
                )
            )
        return invoices

    def _calculate_days_overdue(self, due_date: str) -> int:
        """Calculate days overdue from due date."""
        if not due_date:
            return 0
        try:
            due = datetime.strptime(due_date, "%Y-%m-%d").date()
            today = date.today()
            return max((today - due).days, 0)
        except (ValueError, TypeError):
            return 0
