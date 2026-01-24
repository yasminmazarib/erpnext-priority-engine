# ERPNext Priority Engine

## Problem
ERP systems contain many operational issues such as overdue invoices and blocked cash flow.
Managers and accountants often don’t know **what to fix first**.

## Solution
ERPNext Priority Engine analyzes overdue invoices and returns
a prioritized list based on business impact and clear priority rules.

## Business Value
- Focus on high-impact issues first
- Reduce cash-flow risks
- Improve operational decision-making
- Save time for finance and management teams

## Priority Rules
- **HIGH**: overdue > 30 days AND amount > 50,000
- **MEDIUM**: overdue > 14 days
- **LOW**: overdue ≤ 14 days

## API Endpoints
**GET /priority/issues**  
Returns a prioritized list of overdue invoices.

## Example Response
```json
{
  "top_issues": [
    {
      "invoice_id": "INV-001",
      "customer": "Grant Plastics Ltd.",
      "amount": 67000,
      "days_overdue": 45,
      "priority": "HIGH",
      "reason": "Overdue more than 30 days and high amount"
    }
  ]
}
