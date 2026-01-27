import { APIResponse, FilterParams, InventoryAPIResponse, InventoryFilterParams } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export async function fetchPriorityIssues(params: FilterParams): Promise<APIResponse> {
  const queryParams = new URLSearchParams({
    limit: params.limit.toString(),
    min_days: params.min_days.toString(),
    min_amount: params.min_amount.toString(),
  });

  const response = await fetch(
    `${API_BASE_URL}/priority/issues?${queryParams.toString()}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}

export async function fetchInventoryIssues(params: InventoryFilterParams): Promise<InventoryAPIResponse> {
  const queryParams = new URLSearchParams({
    limit: params.limit.toString(),
  });

  const response = await fetch(
    `${API_BASE_URL}/inventory/issues?${queryParams.toString()}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors',
      credentials: 'omit',
    }
  );

  if (!response.ok) {
    const errorData = await response.text();
    throw new Error(`API Error ${response.status}: ${errorData || response.statusText}`);
  }

  return response.json();
}
