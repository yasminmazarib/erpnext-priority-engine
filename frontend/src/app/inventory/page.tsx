'use client';

import { useState, useEffect } from 'react';
import InventoryFilterPanel from '@/components/InventoryFilterPanel';
import InventoryTable from '@/components/InventoryTable';
import { fetchInventoryIssues } from '@/lib/api';
import { InventoryIssue, InventoryFilterParams } from '@/types';

export default function InventoryPage() {
  const [issues, setIssues] = useState<InventoryIssue[]>([]);
  const [filters, setFilters] = useState<InventoryFilterParams>({
    limit: 20,
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
      const data = await fetchInventoryIssues(filters);
      setIssues(data.issues || []);
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
            Inventory Management
          </h1>
          <p className="text-gray-600">
            Monitor and track inventory issues across warehouses
          </p>
        </div>

        <div className="space-y-6">
          <InventoryFilterPanel
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
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
                    <p className="text-gray-600 text-sm">Total Issues</p>
                    <p className="text-3xl font-bold text-gray-900">
                      {issues.length}
                    </p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
                    <p className="text-gray-600 text-sm">High Priority</p>
                    <p className="text-3xl font-bold text-red-600">
                      {issues.filter((i) => i.priority === 'HIGH').length}
                    </p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
                    <p className="text-gray-600 text-sm">Medium Priority</p>
                    <p className="text-3xl font-bold text-yellow-600">
                      {issues.filter((i) => i.priority === 'MEDIUM').length}
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <h2 className="text-xl font-semibold text-gray-900">
                  Inventory Issues
                </h2>
                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                  <InventoryTable data={issues} />
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </main>
  );
}
