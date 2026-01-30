import React from 'react';
import { Box } from 'lucide-react';
import { ResponsiveContainer, ComposedChart, Bar, Line, XAxis, YAxis, Tooltip } from 'recharts';
import type { ChartsGridSummary } from '../types/dataset';

interface BoxPlotChartProps {
  summary: ChartsGridSummary | null;
}

const BoxPlotChart: React.FC<BoxPlotChartProps> = ({ summary }) => {
  if (!summary) return null;

  // Prepare data for Recharts
  const chartData = summary.boxplot.labels.map((label, i) => ({
    name: label,
    min: summary.boxplot.values[i][0],
    q1: summary.boxplot.values[i][1],
    median: summary.boxplot.values[i][2],
    q3: summary.boxplot.values[i][3],
    max: summary.boxplot.values[i][4],
  }));

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
      <div className="mb-4 flex items-center gap-2">
        <Box className="h-5 w-5 text-orange-600" />
        <h3 className="text-lg font-semibold text-slate-900">Pressure Distribution</h3>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 20, left: 20, bottom: 10 }}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar
              dataKey="q3"
              stackId="a"
              fill="hsl(35, 90%, 55%)"
              shape={(props) => {
                const { x, y, width, height } = props;
                return (
                  <rect x={x} y={y} width={width} height={height} fill="hsl(35, 90%, 55%)" />
                );
              }}
            />
            <Line
              type="monotone"
              dataKey="median"
              stroke="hsl(35, 90%, 40%)"
              strokeWidth={2}
              dot={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default BoxPlotChart;
