import React from 'react';
import { Tooltip, Legend } from 'chart.js';
import { MatrixController, MatrixElement } from 'chartjs-chart-matrix';
import { Chart as ChartJS } from 'chart.js';
import { Grid } from 'lucide-react';
import SafeChart from './SafeChart';
import type { ChartsGridSummary } from '../types/dataset';

ChartJS.register(MatrixController, MatrixElement, Tooltip, Legend);

interface CorrelationHeatmapProps {
  summary: ChartsGridSummary | null;
}

const CorrelationHeatmap: React.FC<CorrelationHeatmapProps> = ({ summary }) => {
  if (!summary) return null;

  // Generate labels and data from summary if available, else fallback to defaults
  const variables = summary?.variables ?? ["Flowrate", "Pressure", "Temperature"];
  const matrix = summary?.correlationMatrix ?? [
    [1.0, 0.62, 0.48],
    [0.62, 1.0, 0.71],
    [0.48, 0.71, 1.0],
  ];

  const data = {
    datasets: [
      {
        label: 'Correlation',
        data: variables.flatMap((rowVar, i) =>
          variables.map((colVar, j) => ({
            x: colVar,
            y: rowVar,
            v: matrix[i][j],
          }))
        ),
        backgroundColor: (ctx: import('chart.js').ScriptableContext<'matrix'>) => {
          const v = Math.abs((ctx.raw as { v: number }).v);
          return `rgba(59,130,246,${v})`;
        },
        width: () => 40,
        height: () => 40,
        xAxisID: 'x',
        yAxisID: 'y',
      },
    ],
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
      <div className="mb-4 flex items-center gap-2">
        <Grid className="h-5 w-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-slate-900">Correlation Matrix</h3>
      </div>
      <div className="h-64">
        <SafeChart
          type="matrix"
          data={data}
          options={{
            responsive: true,
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  title: (items) => `${items[0].raw.x} vs ${items[0].raw.y}`,
                  label: (item) => `Correlation: ${(item.raw as any).v.toFixed(2)}`,
                },
              },
            },
            scales: {
              x: {
                type: 'category',
                labels: variables,
                offset: true,
                grid: { display: false },
                position: 'top',
              },
              y: {
                type: 'category',
                labels: variables,
                offset: true,
                grid: { display: false },
                reverse: true,
              },
            },
          }}
          chartKey="correlation-chart"
        />
      </div>
    </div>
  );
};

export default CorrelationHeatmap;
