import React from 'react';
import ScatterChart from './ScatterChart';
import HistogramChart from './HistogramChart';
import BoxPlotChart from './BoxPlotChart';
import type { ChartsGridSummary } from '../types/dataset';
import HeatmapChart from './CorrelationHeatmap';

interface AdvancedChartsGridProps {
  summary: ChartsGridSummary | null;
}

const AdvancedChartsGrid: React.FC<AdvancedChartsGridProps> = ({ summary }) => {
  if (!summary) {
    return (
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-72 animate-pulse rounded-xl border border-slate-200 bg-white" />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <ScatterChart summary={summary} />
      <HistogramChart summary={summary} />
      <BoxPlotChart data={[
    { label: 'Flowrate', min: 12, q1: 20, median: 28, q3: 35, max: 42 },
    { label: 'Pressure', min: 1.2, q1: 2.1, median: 2.8, q3: 3.4, max: 4.1 },
    { label: 'Temperature', min: 22, q1: 30, median: 38, q3: 45, max: 52 },
  ]} />
      <HeatmapChart
        labels={['A', 'B', 'C', 'D', 'E']}
        matrix={[
          [1, 0.4, 0.2, -0.6, -0.3],
          [0.4, 1, -0.2, 0.3, 0.1],
          [0.2, -0.2, 1, 0.7, 0.4],
          [-0.6, 0.3, 0.7, 1, 0.5],
          [-0.3, 0.1, 0.4, 0.5, 1],
        ]}
      />
    </div>
  );
};

export default AdvancedChartsGrid;
