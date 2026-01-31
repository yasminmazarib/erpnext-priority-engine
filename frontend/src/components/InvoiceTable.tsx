'use client';

import { PriorityIssue } from '@/types';
import { formatCurrency } from '@/lib/formatters';

interface InvoiceTableProps {
  data: PriorityIssue[];
}

const priorityColors: Record<string, string> = {
  HIGH: 'bg-red-100 text-red-700',
  MEDIUM: 'bg-orange-100 text-orange-700',
  LOW: 'bg-green-100 text-green-700',
};

export default function InvoiceTable({ data }: InvoiceTableProps) {
  if (data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No invoices found matching the filters.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto shadow-md rounded-lg">
      <table
        className="w-full border-collapse bg-white"
        data-testid="invoice-table"
      >
        <thead>
          <tr className="bg-gray-100 border-b-2 border-gray-300">
            <th className="px-6 py-4 text-left font-semibold text-gray-700">
              Invoice ID
            </th>
            <th className="px-6 py-4 text-left font-semibold text-gray-700">
              Customer
            </th>
            <th className="px-6 py-4 text-right font-semibold text-gray-700">
              Amount
            </th>
            <th className="px-6 py-4 text-right font-semibold text-gray-700">
              Days Overdue
            </th>
            <th className="px-6 py-4 text-center font-semibold text-gray-700">
              Priority
            </th>
          </tr>
        </thead>

        <tbody>
          {data.map((issue, index) => (
            <tr
              key={issue.invoice_id}
              className={`border-b transition-colors ${
                index % 2 === 0 ? 'bg-gray-50' : 'bg-white'
              } hover:bg-blue-50`}
            >
              <td className="px-6 py-4 font-medium text-gray-900">
                {issue.invoice_id}
              </td>

              <td className="px-6 py-4 text-gray-700">
                {issue.customer}
              </td>

              <td className="px-6 py-4 text-right text-gray-700">
                {formatCurrency(issue.amount)}
              </td>

              <td className="px-6 py-4 text-right">
                <span className="px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800">
                  {issue.days_overdue} days
                </span>
              </td>

              <td className="px-6 py-4 text-center">
                <span
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    priorityColors[issue.priority] ?? 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {issue.priority}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
