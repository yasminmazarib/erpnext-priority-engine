export interface PriorityIssue {
  invoice_id: string;
  customer: string;
  amount: number;
  days_overdue: number;
  priority?: string;
  reason?: string;
}

export interface InventoryIssue {
  item_code: string;
  warehouse: string;
  actual_qty: number;
  reserved_qty: number;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  reason: string;
}

export interface APIResponse {
  top_issues: PriorityIssue[];
  message?: string;
}

export interface InventoryAPIResponse {
  issues: InventoryIssue[];
  count: number;
}

export interface FilterParams {
  limit: number;
  min_days: number;
  min_amount: number;
}

export interface InventoryFilterParams {
  limit: number;
}
