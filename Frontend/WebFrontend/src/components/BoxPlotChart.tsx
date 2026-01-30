import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Title,
} from 'chart.js';
import {
  BoxPlotController,
  BoxAndWiskers,
} from '@sgratzl/chartjs-chart-boxplot';
import { Activity } from 'lucide-react';
import SafeChart from './SafeChart';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BoxPlotController,
  BoxAndWiskers,
  Tooltip,
  Legend,
  Title
);

interface BoxPlotProps {
  data: {
    label: string;
    min: number;
    q1: number;
    median: number;
    q3: number;
    max: number;
  }[];
}

const BoxPlotChart: React.FC<BoxPlotProps> = ({ data }) => {
  const chartData = {
    labels: data.map(d => d.label),
    datasets: [
      {
        label: 'Statistical Distribution',
        data: data.map(d => ({
          min: d.min,
          q1: d.q1,
          median: d.median,
          q3: d.q3,
          max: d.max,
        })),
        backgroundColor: 'hsl(210, 85%, 55%)',
        borderColor: 'hsl(215, 25%, 25%)',
        borderWidth: 1.5,
        outlierColor: 'hsl(0, 72%, 51%)',
        padding: 8,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'hsl(215, 25%, 15%)',
        cornerRadius: 8,
        titleFont: { size: 13 },
        bodyFont: { size: 12 },
      },
      title: {
        display: false,
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: {
          font: { size: 11 },
          color: 'hsl(215, 15%, 35%)',
        },
      },
      y: {
        grid: { color: 'hsl(214, 20%, 88%)' },
        ticks: {
          font: { size: 11 },
          color: 'hsl(215, 15%, 35%)',
        },
      },
    },
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
      <div className="mb-4 flex items-center gap-2">
        <Activity className="h-5 w-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-slate-900">
          Distribution Analysis (Box Plot)
        </h3>
      </div>

      <div className="h-72">
        <SafeChart
          type="boxplot"
          data={chartData}
          options={options}
          chartKey="boxplot-summary"
        />
      </div>
    </div>
  );
};

export default BoxPlotChart;
