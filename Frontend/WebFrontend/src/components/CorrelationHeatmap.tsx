import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js';
import { MatrixController, MatrixElement } from 'chartjs-chart-matrix';
import SafeChart from './SafeChart';

ChartJS.register(
  CategoryScale,
  LinearScale,
  MatrixController,
  MatrixElement,
  Tooltip,
  Legend
);

interface CorrelationHeatmapProps {
  labels: string[];
  matrix: number[][];
}

const HeatmapChart: React.FC<CorrelationHeatmapProps> = ({ labels, matrix }) => {
  const data = {
    datasets: [
      {
        label: 'Correlation',
        data: matrix.flatMap((row, i) =>
          row.map((value, j) => ({
            x: labels[j],
            y: labels[i],
            v: value,
          }))
        ),
        backgroundColor: (ctx: any) => {
          const value = ctx.raw.v;
          const alpha = Math.abs(value);
          return value > 0
            ? `rgba(33, 150, 243, ${alpha})`
            : `rgba(244, 67, 54, ${alpha})`;
        },
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.8)',
        width: ({ chart }: any) =>
          (chart.chartArea || {}).width / labels.length - 2,
        height: ({ chart }: any) =>
          (chart.chartArea || {}).height / labels.length - 2,
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
        callbacks: {
          label: (ctx: any) => `Correlation: ${ctx.raw.v.toFixed(2)}`,
        },
      },
    },
    scales: {
      x: {
        type: 'category' as const,
        labels,
        grid: { display: false },
        ticks: { font: { size: 11 } },
      },
      y: {
        type: 'category' as const,
        labels,
        grid: { display: false },
        ticks: { font: { size: 11 } },
      },
    },
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
      <h3 className="mb-4 text-lg font-semibold text-slate-900">
        Correlation Heatmap
      </h3>
      <div className="h-80">
        <SafeChart
          type="matrix"
          data={data}
          options={options}
          chartKey="correlation-heatmap"
        />
      </div>
    </div>
  );
};

export default HeatmapChart;
