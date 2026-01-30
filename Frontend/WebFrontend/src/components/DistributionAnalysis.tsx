import React from 'react';
import {
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Activity,
} from 'lucide-react';

interface DistributionStats {
  min: number;
  q1: number;
  median: number;
  q3: number;
  max: number;
  outliers?: number[];
}

interface DistributionAnalysisProps {
  title: string;
  unit?: string;
  stats: DistributionStats;
}

const DistributionAnalysis: React.FC<DistributionAnalysisProps> = ({
  title,
  unit,
  stats,
}) => {
  const iqr = stats.q3 - stats.q1;
  const range = stats.max - stats.min;
  const skew =
    stats.median - stats.q1 > stats.q3 - stats.median
      ? 'Right Skewed'
      : 'Left Skewed';

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
      <div className="mb-6 flex items-center gap-3">
        <Activity className="h-6 w-6 text-blue-600" />
        <div>
          <h3 className="text-lg font-semibold text-slate-900">
            {title} – Distribution Analysis
          </h3>
          <p className="text-sm text-slate-500">
            Statistical summary based on quartile distribution
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Median" value={stats.median} unit={unit} />
        <StatCard label="IQR" value={iqr} unit={unit} />
        <StatCard label="Range" value={range} unit={unit} />
        <SkewCard skew={skew} />
      </div>

      <div className="mt-6 rounded-lg bg-slate-50 p-4">
        <h4 className="mb-2 text-sm font-semibold text-slate-700">
          Interpretation
        </h4>
        <p className="text-sm text-slate-600 leading-relaxed">
          The median value of <strong>{stats.median}{unit}</strong> indicates
          the central tendency of the dataset. The interquartile range (IQR)
          of <strong>{iqr}{unit}</strong> reflects moderate variability,
          while the total range suggests the overall spread.
          The distribution is <strong>{skew}</strong>, indicating unequal
          dispersion around the median.
        </p>

        {stats.outliers && stats.outliers.length > 0 && (
          <div className="mt-3 flex items-start gap-2 text-sm text-amber-600">
            <AlertTriangle className="h-4 w-4 mt-0.5" />
            <span>
              {stats.outliers.length} potential outlier(s) detected which may
              require further inspection.
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

const StatCard = ({
  label,
  value,
  unit,
}: {
  label: string;
  value: number;
  unit?: string;
}) => (
  <div className="rounded-lg border border-slate-200 bg-white p-4">
    <p className="text-xs uppercase tracking-wide text-slate-500">{label}</p>
    <p className="mt-1 text-xl font-semibold text-slate-900">
      {value}
      {unit}
    </p>
  </div>
);

const SkewCard = ({ skew }: { skew: string }) => {
  const isRight = skew === 'Right Skewed';

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <p className="text-xs uppercase tracking-wide text-slate-500">
        Distribution
      </p>
      <div className="mt-2 flex items-center gap-2">
        {isRight ? (
          <TrendingUp className="h-5 w-5 text-emerald-600" />
        ) : (
          <TrendingDown className="h-5 w-5 text-indigo-600" />
        )}
        <span className="text-sm font-medium text-slate-800">{skew}</span>
      </div>
    </div>
  );
};

export default DistributionAnalysis;
