'use client';

import { useState, useEffect } from 'react';
import FilterPanel from '@/components/FilterPanel';
import InvoiceTable from '@/components/InvoiceTable';
import AmountChart from '@/components/AmountChart';
import { PriorityIssue, FilterParams } from '@/types';
import { formatCurrency } from '@/lib/formatters';
import { fetchPriorityIssues } from '@/lib/api';

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
      const data = await fetchPriorityIssues(filters);

      // ✅ תמיכה גם ב-issues וגם ב-top_issues (מה-Backend שלך)
      const safeIssues: PriorityIssue[] = Array.isArray((data as any)?.issues)
        ? (data as any).issues
        : Array.isArray((data as any)?.top_issues)
        ? (data as any).top_issues
        : [];

      setIssues(safeIssues);
    } catch (err) {
      console.error('Fetch error:', err);
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to fetch data. Please try again.'
      );
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
              {/* ===== Summary ===== */}
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
                        issues.reduce(
                          (sum, issue) => sum + issue.amount,
                          0
                        )
                      )}
                    </p>
                  </div>
                </div>
              </div>

              {/* ===== Chart ===== */}
              <div className="space-y-2">
                <h2 className="text-xl font-semibold text-gray-900">
                  Invoice Amounts by Customer
                </h2>
                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                  <AmountChart data={issues} />
                </div>
              </div>

              {/* ===== Table ===== */}
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
