'use client';

import { useState, useEffect } from 'react';
import FilterPanel from '@/components/FilterPanel';
import InvoiceTable from '@/components/InvoiceTable';
import AmountChart from '@/components/AmountChart';
import { PriorityIssue, FilterParams } from '@/types';
import { formatCurrency } from '@/lib/formatters';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function DashboardPage() {
  const [issues, setIssues] = useState<PriorityIssue[]>([]);
  const [filters, setFilters] = useState<FilterParams>({
    limit: 5,
    min_days: 1,
    min_amount: 0,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasInitialized, setHasInitialized] = useState(false);

  useEffect(() => {
    if (!hasInitialized) {
      loadData();
      setHasInitialized(true);
    }
  }, [hasInitialized]);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const queryParams = new URLSearchParams({
        limit: filters.limit.toString(),
      });

      const response = await fetch(
        `${API_BASE_URL}/priority/invoices?${queryParams.toString()}`,
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

      const data = await response.json();
      setIssues(data.invoices || []);
    } catch (err) {
      console.error('Fetch error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch data. Please try again.';
      setError(errorMessage);
      setIssues([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleApplyFilters = () => {
    loadData();
  };

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            ERPNext Priority Engine
          </h1>
          <p className="text-gray-600">
            Monitor and track overdue invoices
          </p>
        </div>

        <div className="space-y-6">
          <FilterPanel
            filters={filters}
            onFiltersChange={setFilters}
            onApply={handleApplyFilters}
            isLoading={isLoading}
          />

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
              <p className="font-medium">Error</p>
              <p>{error}</p>
            </div>
          )}

          {isLoading && (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          )}

          {!isLoading && !error && (
            <>
              <div className="space-y-2">
                <h2 className="text-xl font-semibold text-gray-900">
                  Summary
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
                    <p className="text-gray-600 text-sm">Total Invoices</p>
                    <p className="text-3xl font-bold text-gray-900">
                      {issues.length}
                    </p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
                    <p className="text-gray-600 text-sm">Total Amount</p>
                    <p className="text-3xl font-bold text-gray-900">
                      {formatCurrency(
                        issues.reduce((sum, issue) => sum + issue.amount, 0)
                      )}
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <h2 className="text-xl font-semibold text-gray-900">
                  Invoice Amounts by Customer
                </h2>
                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                  <AmountChart data={issues} />
                </div>
              </div>

              <div className="space-y-2">
                <h2 className="text-xl font-semibold text-gray-900">
                  Overdue Invoices
                </h2>
                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                  <InvoiceTable data={issues} />
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </main>
  );
}

