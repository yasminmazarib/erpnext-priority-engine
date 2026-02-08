import {
  FilterParams,
  InventoryFilterParams,
  APIResponse,
  InventoryAPIResponse,
} from '@/types';

// ✅ שם משתנה תואם ל־.env.local
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

// 🛟 הגנה + דיבוג
if (!API_BASE_URL) {
  console.error(
    '❌ NEXT_PUBLIC_API_BASE_URL is not defined. Check .env.local and restart dev server.'
  );
}

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

  console.log(
    '📡 Fetching priority issues from:',
    `${API_BASE_URL}/priority/issues?${queryParams.toString()}`
  );

  const response = await fetch(
    `${API_BASE_URL}/priority/issues?${queryParams.toString()}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch priority issues (status ${response.status})`
    );
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

  console.log(
    '📡 Fetching inventory issues from:',
    `${API_BASE_URL}/inventory/issues?${queryParams.toString()}`
  );

  const response = await fetch(
    `${API_BASE_URL}/inventory/issues?${queryParams.toString()}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch inventory issues (status ${response.status})`
    );
  }

  return response.json();
}