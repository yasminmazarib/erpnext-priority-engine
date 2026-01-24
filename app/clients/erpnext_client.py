from datetime import date
from app.models.priority_models import Invoice


class ERPNextClient:
    def fetch_overdue_invoices(self) -> list[Invoice]:
        """
        Mock ERPNext response.
        In real life – this will call ERPNext REST API.
        """
        return [
            Invoice(
                invoice_id="INV-001",
                customer="Grant Plastics Ltd.",
                amount=67000,
                days_overdue=45,
                due_date=date(2025, 12, 10)
            ),
            Invoice(
                invoice_id="INV-002",
                customer="West View Software",
                amount=15000,
                days_overdue=20,
                due_date=date(2026, 1, 1)
            ),
            Invoice(
                invoice_id="INV-003",
                customer="Alpha Tech",
                amount=3000,
                days_overdue=5,
                due_date=date(2026, 1, 15)
            )
        ]
