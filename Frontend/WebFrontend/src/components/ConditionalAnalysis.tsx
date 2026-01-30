import React from 'react';
import { Filter, TrendingUp, Wind, Gauge, Thermometer } from 'lucide-react';

interface ConditionalStats {
  flowrate: number;
  pressure: number;
  temperature: number;
}

interface ConditionalAnalysisProps {
  conditionLabel: string;
  totalRecords: number;
  stats: ConditionalStats;
}

const MetricRow = ({
  icon: Icon,
  label,
  value,
  unit,
}: {
  icon: React.ElementType;
  label: string;
  value: number;
  unit: string;
}) => (
  <div className="flex items-center justify-between rounded-lg bg-slate-50 px-4 py-3">
    <div className="flex items-center gap-3">
      <Icon className="h-4 w-4 text-blue-600" />
      <span className="text-sm font-medium text-slate-700">{label}</span>
    </div>
    <span className="text-sm font-semibold text-slate-900">
      {value.toFixed(2)}
      {unit}
    </span>
  </div>
);

const ConditionalAnalysis: React.FC<ConditionalAnalysisProps> = ({
  conditionLabel,
  totalRecords,
  stats,
}) => {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6 flex items-center gap-3">
        <div className="rounded-lg bg-emerald-50 p-2">
          <Filter className="h-5 w-5 text-emerald-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-slate-900">
            Conditional Analysis
          </h3>
          <p className="text-sm text-slate-500">{conditionLabel}</p>
        </div>
      </div>

      <div className="mb-5 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3">
          <p className="text-xs uppercase tracking-wide text-emerald-700">
            Records Matching Condition
          </p>
          <div className="mt-2 flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-emerald-600" />
            <span className="text-xl font-semibold text-emerald-700">
              {totalRecords}
            </span>
          </div>
        </div>

        <div className="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
          <p className="text-xs uppercase tracking-wide text-slate-500">
            Condition Summary
          </p>
          <p className="mt-2 text-sm font-medium text-slate-700">
            Pressure above dataset mean
          </p>
        </div>
      </div>

      <div>
        <h4 className="mb-3 text-sm font-semibold text-slate-700">
          Average Parameters Under Condition
        </h4>

        <div className="space-y-3">
          <MetricRow
            icon={Wind}
            label="Flowrate"
            value={stats.flowrate}
            unit=" m³/h"
          />
          <MetricRow
            icon={Gauge}
            label="Pressure"
            value={stats.pressure}
            unit=" bar"
          />
          <MetricRow
            icon={Thermometer}
            label="Temperature"
            value={stats.temperature}
            unit=" °C"
          />
        </div>
      </div>
    </div>
  );
};

export default ConditionalAnalysis;
