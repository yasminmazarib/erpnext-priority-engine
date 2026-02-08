'use client';

import { InventoryIssue } from '@/types';

interface InventoryTableProps {
  data: InventoryIssue[];
}

function getPriorityColor(priority: 'HIGH' | 'MEDIUM' | 'LOW') {
  switch (priority) {
    case 'HIGH':
      return 'bg-red-100 text-red-800';
    case 'MEDIUM':
      return 'bg-yellow-100 text-yellow-800';
    case 'LOW':
      return 'bg-green-100 text-green-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
}

export default function InventoryTable({ data }: InventoryTableProps) {
  if (data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No inventory issues found.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto shadow-md rounded-lg">
      <table className="w-full border-collapse bg-white">
        <thead>
          <tr className="bg-gray-100 border-b-2 border-gray-300">
            <th className="px-6 py-4 text-left font-semibold text-gray-700">
              Item Code
            </th>
            <th className="px-6 py-4 text-left font-semibold text-gray-700">
              Warehouse
            </th>
            <th className="px-6 py-4 text-right font-semibold text-gray-700">
              Actual Qty
            </th>
            <th className="px-6 py-4 text-right font-semibold text-gray-700">
              Reserved Qty
            </th>
            <th className="px-6 py-4 text-center font-semibold text-gray-700">
              Priority
            </th>
            <th className="px-6 py-4 text-left font-semibold text-gray-700">
              Reason
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((issue, index) => (
            <tr
              key={`${issue.item_code}-${issue.warehouse}`}
              className={`border-b transition-colors ${
                index % 2 === 0 ? 'bg-gray-50' : 'bg-white'
              } hover:bg-blue-50`}
            >
              <td className="px-6 py-4 font-medium text-gray-900">
                {issue.item_code}
              </td>
              <td className="px-6 py-4 text-gray-700">{issue.warehouse}</td>
              <td className="px-6 py-4 text-right text-gray-700">
                {issue.actual_qty}
              </td>
              <td className="px-6 py-4 text-right text-gray-700">
                {issue.reserved_qty}
              </td>
              <td className="px-6 py-4 text-center">
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${getPriorityColor(
                    issue.priority
                  )}`}
                >
                  {issue.priority}
                </span>
              </td>
              <td className="px-6 py-4 text-gray-700 text-sm">
                {issue.reason}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
