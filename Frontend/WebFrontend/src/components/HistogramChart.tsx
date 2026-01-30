import React from 'react';
import { CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js';
import { Chart as ChartJS } from 'chart.js';
import { BarChart3 } from 'lucide-react';
import SafeChart from './SafeChart';
import type { ChartsGridSummary } from '../types/dataset';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

interface HistogramChartProps {
  summary: ChartsGridSummary | null;
}

const HistogramChart: React.FC<HistogramChartProps> = ({ summary }) => {
  if (!summary) return null;

  // Assume summary.histogram contains: { flowrate: number[], temperature: number[] }
  // We'll combine both datasets into a single histogram using "stacked" bars with transparency.

  // Calculate bins (assuming both arrays are same length and bins)
  const bins = summary.histogram.labels;
  const flowrateData = summary.histogram.flowrate;
  const temperatureData = summary.histogram.temperature;

  const data = {
    labels: bins,
    datasets: [
      {
        label: 'Flowrate',
        data: flowrateData,
        backgroundColor: 'rgba(37, 99, 235, 0.6)', // blue, alpha=0.6
        borderWidth: 1,
        barPercentage: 1.0,
        categoryPercentage: 1.0,
      },
      {
        label: 'Temperature',
        data: temperatureData,
        backgroundColor: 'rgba(220, 38, 38, 0.6)', // red, alpha=0.6
        borderWidth: 1,
        barPercentage: 1.0,
        categoryPercentage: 1.0,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true, position: 'top' as const },
      title: {
        display: true,
        text: 'Flowrate vs Temperature Distribution',
        font: { size: 18 },
      },
      tooltip: { mode: 'index', intersect: false },
    },
    scales: {
      x: {
        title: { display: true, text: 'Value' },
        grid: { display: true },
        stacked: false,
      },
      y: {
        title: { display: true, text: 'Frequency' },
        grid: { display: true },
        stacked: false,
      },
    },
    elements: {
      bar: {
        borderRadius: 2,
      },
    },
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
      <div className="mb-4 flex items-center gap-2">
        <BarChart3 className="h-5 w-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-slate-900">Parameter Distribution</h3>
      </div>
      <div className="h-full w-full">
        <SafeChart type="bar" data={data} options={options} chartKey="histogram-chart" />
      </div>
    </div>
  );
};

export default HistogramChart;
