'use client';

import React from 'react';
import { FilterParams } from '@/types';

interface FilterPanelProps {
  filters: FilterParams;
  onFiltersChange: (filters: FilterParams) => void;
  onApply: () => void;
  isLoading: boolean;
}

const FilterPanel: React.FC<FilterPanelProps> = ({
  filters,
  onFiltersChange,
  onApply,
  isLoading,
}) => {
  const handleChange = (key: keyof FilterParams, value: number) => {
    onFiltersChange({
      ...filters,
      [key]: value,
    });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Filters</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Limit
          </label>
          <input
            type="number"
            min={1}
            max={100}
            value={filters.limit}
            onChange={(e) =>
              handleChange('limit', parseInt(e.target.value, 10))
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-lg"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Minimum Days Overdue
          </label>
          <input
            type="number"
            min={0}
            value={filters.min_days}
            onChange={(e) =>
              handleChange('min_days', parseInt(e.target.value, 10))
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-lg"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Minimum Amount ($)
          </label>
          <input
            type="number"
            min={0}
            step={100}
            value={filters.min_amount}
            onChange={(e) =>
              handleChange('min_amount', parseFloat(e.target.value))
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-lg"
          />
        </div>
      </div>

      <button
        onClick={onApply}
        disabled={isLoading}
        data-testid="apply-filters"
        className="px-6 py-2 bg-blue-600 text-white rounded-lg disabled:bg-gray-400"
      >
        {isLoading ? 'Loading...' : 'Apply Filters'}
      </button>
    </div>
  );
};

export default FilterPanel;
