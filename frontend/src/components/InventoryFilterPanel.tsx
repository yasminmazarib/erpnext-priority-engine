'use client';

import { InventoryFilterParams } from '@/types';

interface InventoryFilterPanelProps {
  filters: InventoryFilterParams;
  onFiltersChange: (filters: InventoryFilterParams) => void;
  onApply: () => void;
  isLoading: boolean;
}

export default function InventoryFilterPanel({
  filters,
  onFiltersChange,
  onApply,
  isLoading,
}: InventoryFilterPanelProps) {
  const handleChange = (key: keyof InventoryFilterParams, value: number) => {
    onFiltersChange({
      ...filters,
      [key]: value,
    });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Filters</h2>

      <div className="grid grid-cols-1 md:grid-cols-1 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Limit
          </label>
          <input
            type="number"
            min={1}
            max={100}
            value={filters.limit}
            onChange={(e) => handleChange('limit', parseInt(e.target.value, 10))}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      <button
        onClick={onApply}
        disabled={isLoading}
        className="w-full md:w-auto px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {isLoading ? 'Loading...' : 'Apply Filters'}
      </button>
    </div>
  );
}
