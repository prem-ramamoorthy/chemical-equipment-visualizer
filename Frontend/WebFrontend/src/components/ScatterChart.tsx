import React from 'react';
import { LinearScale, PointElement, Tooltip, Legend, ScatterController } from 'chart.js';
import { Activity } from 'lucide-react';
import SafeChart from './SafeChart';
import type { ChartsGridSummary } from '../types/dataset';

import { Chart as ChartJS } from 'chart.js';
ChartJS.register(LinearScale, PointElement, Tooltip, Legend, ScatterController);

interface ScatterChartProps {
  summary: ChartsGridSummary | null;
}

const ScatterChart: React.FC<ScatterChartProps> = ({ summary }) => {
  if (!summary) return null;

  const data = {
    datasets: [
      {
        label: 'Flowrate vs Pressure',
        data: summary.scatter_points,
        backgroundColor: 'hsl(200, 80%, 50%)',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: { title: { display: true, text: 'Flowrate' } },
      y: { title: { display: true, text: 'Pressure' } },
    },
    plugins: { tooltip: { backgroundColor: 'hsl(215, 25%, 15%)', cornerRadius: 8 } },
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
      <div className="mb-4 flex items-center gap-2">
        <Activity className="h-5 w-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-slate-900">Flowrate vs Pressure</h3>
      </div>
      <div className="h-64">
        <SafeChart type="scatter" data={data} options={options} chartKey="scatter-chart" />
      </div>
    </div>
  );
};

export default ScatterChart;
