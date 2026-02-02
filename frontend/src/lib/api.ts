import {
  FilterParams,
  InventoryFilterParams,
  APIResponse,
  InventoryAPIResponse,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

/* =========================
   PRIORITY (Invoices)
========================= */
export async function fetchPriorityIssues(
  params: FilterParams
): Promise<APIResponse> {
  const queryParams = new URLSearchParams({
    limit: params.limit.toString(),
    min_days: params.min_days.toString(),
    min_amount: params.min_amount.toString(),
  });

  const response = await fetch(
    `${API_BASE_URL}/priority/issues?${queryParams.toString()}`
  );

  if (!response.ok) {
    throw new Error('Failed to fetch priority issues');
  }

  return response.json();
}

/* =========================
   INVENTORY
========================= */
export async function fetchInventoryIssues(
  params: InventoryFilterParams
): Promise<InventoryAPIResponse> {
  const queryParams = new URLSearchParams({
    limit: params.limit.toString(),
  });

  const response = await fetch(
    `${API_BASE_URL}/inventory/issues?${queryParams.toString()}`
  );

  if (!response.ok) {
    throw new Error('Failed to fetch inventory issues');
  }

  return response.json();
}
