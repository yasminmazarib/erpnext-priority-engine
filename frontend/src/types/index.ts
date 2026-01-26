export interface PriorityIssue {
  invoice_id: string;
  customer: string;
  amount: number;
  days_overdue: number;
  priority?: string;
  reason?: string;
}

export interface APIResponse {
  top_issues: PriorityIssue[];
  message?: string;
}

export interface FilterParams {
  limit: number;
  min_days: number;
  min_amount: number;
}
