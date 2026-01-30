import React from 'react';
import ScatterChart from './ScatterChart';
import HistogramChart from './HistogramChart';
import BoxPlotChart from './BoxPlotChart';
import CorrelationHeatmap from './CorrelationHeatmap';
import type { ChartsGridSummary } from '../types/dataset';

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
      <BoxPlotChart summary={summary} />
      <CorrelationHeatmap summary={summary} />
    </div>
  );
};

export default AdvancedChartsGrid;
