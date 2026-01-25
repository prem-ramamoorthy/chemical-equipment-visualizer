import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import { PieChart, BarChart3 } from 'lucide-react';
import type { DatasetSummary } from '../types/dataset';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface ChartsProps {
  summary: DatasetSummary | null;
}

const Charts: React.FC<ChartsProps> = ({ summary }) => {
  if (!summary) {
    return (
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {[1, 2].map((i) => (
          <div
            key={i}
            className="rounded-xl border border-slate-200 bg-white p-6 shadow-md"
          >
            <div className="mb-4 h-4 w-32 rounded bg-slate-200" />
            <div className="h-64 rounded bg-slate-200 animate-pulse" />
          </div>
        ))}
      </div>
    );
  }

  const pieData = {
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        data: Object.values(summary.type_distribution),
        backgroundColor: [
          'hsl(210, 60%, 45%)',
          'hsl(185, 55%, 45%)',
          'hsl(35, 90%, 55%)',
          'hsl(280, 55%, 55%)',
          'hsl(145, 55%, 42%)',
        ],
        borderWidth: 0,
      },
    ],
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          usePointStyle: true,
          padding: 20,
          font: { size: 12 },
        },
      },
      tooltip: {
        backgroundColor: 'hsl(215, 25%, 15%)',
        titleFont: { size: 13 },
        bodyFont: { size: 12 },
        padding: 12,
        cornerRadius: 8,
      },
    },
  };

  const barData = {
    labels: ['Flowrate (m³/h)', 'Pressure (bar)', 'Temperature (°C)'],
    datasets: [
      {
        label: 'Average Values',
        data: [
          summary.avg_flowrate,
          summary.avg_pressure,
          summary.avg_temperature,
        ],
        backgroundColor: [
          'hsl(200, 80%, 50%)',
          'hsl(35, 90%, 55%)',
          'hsl(0, 72%, 51%)',
        ],
        borderRadius: 6,
        borderSkipped: false,
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'hsl(215, 25%, 15%)',
        titleFont: { size: 13 },
        bodyFont: { size: 12 },
        padding: 12,
        cornerRadius: 8,
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { size: 11 } },
      },
      y: {
        grid: { color: 'hsl(214, 20%, 88%)' },
        ticks: { font: { size: 11 } },
      },
    },
  };

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
        <div className="mb-4 flex items-center gap-2">
          <PieChart className="h-5 w-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-slate-900">
            Equipment Type Distribution
          </h3>
        </div>
        <div className="h-64">
          <Pie data={pieData} options={pieOptions} />
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
        <div className="mb-4 flex items-center gap-2">
          <BarChart3 className="h-5 w-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-slate-900">
            Average Parameters
          </h3>
        </div>
        <div className="h-64">
          <Bar data={barData} options={barOptions} />
        </div>
      </div>
    </div>
  );
};

export default Charts;