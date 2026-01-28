'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { PriorityIssue } from '@/types';
import { formatCurrency } from '@/lib/formatters';

interface AmountChartProps {
  data: PriorityIssue[];
}

export default function AmountChart({ data }: AmountChartProps) {
  if (data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No data available for chart.
      </div>
    );
  }

  const chartData = data.map((issue) => ({
    customer: issue.customer.substring(0, 15),
    amount: issue.amount,
    days_overdue: issue.days_overdue,
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="customer"
          angle={-45}
          textAnchor="end"
          height={80}
        />
        <YAxis
          label={{ value: 'Amount (₪)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip
          formatter={(value) => formatCurrency(value as number)}
          labelFormatter={(label) => `Customer: ${label}`}
        />
        <Legend />
        <Bar dataKey="amount" fill="#3b82f6" name="Invoice Amount" />
      </BarChart>
    </ResponsiveContainer>
  );
}
