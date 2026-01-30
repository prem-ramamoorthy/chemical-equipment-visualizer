import React from 'react';
import { BarChart2, Gauge, Thermometer } from 'lucide-react';

interface StatColumn {
  count: number;
  mean: number;
  std: number;
  min: number;
  q1: number;
  median: number;
  q3: number;
  max: number;
}

export interface StatisticalSummaryProps {
  data: {
    flowrate: StatColumn;
    pressure: StatColumn;
    temperature: StatColumn;
  };
}

const MetricCard = ({
  title,
  icon: Icon,
  stats,
  unit,
}: {
  title: string;
  icon: React.ElementType;
  stats: StatColumn;
  unit: string;
}) => {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center gap-3">
        <div className="rounded-lg bg-blue-50 p-2">
          <Icon className="h-5 w-5 text-blue-600" />
        </div>
        <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Stat label="Count" value={stats.count} />
        <Stat label="Mean" value={`${stats.mean}${unit}`} />
        <Stat label="Std Dev" value={stats.std} />
        <Stat label="Min" value={`${stats.min}${unit}`} />
        <Stat label="Q1 (25%)" value={`${stats.q1}${unit}`} />
        <Stat label="Median" value={`${stats.median}${unit}`} />
        <Stat label="Q3 (75%)" value={`${stats.q3}${unit}`} />
        <Stat label="Max" value={`${stats.max}${unit}`} />
      </div>
    </div>
  );
};

const Stat = ({ label, value }: { label: string; value: number | string }) => (
  <div className="rounded-lg bg-slate-50 px-4 py-3">
    <p className="text-xs uppercase tracking-wide text-slate-500">{label}</p>
    <p className="mt-1 text-sm font-semibold text-slate-900">{value}</p>
  </div>
);

const StatisticalSummary: React.FC<StatisticalSummaryProps> = ({ data }) => {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-slate-900">
          Statistical Summary
        </h2>
        <p className="text-sm text-slate-500">
          Descriptive statistics across operational parameters
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <MetricCard
          title="Flowrate"
          icon={BarChart2}
          unit=" m³/h"
          stats={data.flowrate}
        />

        <MetricCard
          title="Pressure"
          icon={Gauge}
          unit=" bar"
          stats={data.pressure}
        />

        <MetricCard
          title="Temperature"
          icon={Thermometer}
          unit=" °C"
          stats={data.temperature}
        />
      </div>
    </div>
  );
};

export default StatisticalSummary;