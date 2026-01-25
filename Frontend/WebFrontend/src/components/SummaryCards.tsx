import React from "react";
import { Gauge, Thermometer, Droplets, Box } from "lucide-react";
import type { DatasetSummary } from "../types/dataset";

interface SummaryCardsProps {
  summary: DatasetSummary | null;
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  unit?: string;
  bgClass: string;
}

const StatCard: React.FC<StatCardProps> = ({
  icon,
  label,
  value,
  unit,
  bgClass,
}) => (
  <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md">
    <div className="flex items-start justify-between">
      <div>
        <p className="text-sm font-medium text-slate-500">{label}</p>
        <div className="mt-2 flex items-baseline gap-1">
          <span className="text-2xl font-bold text-slate-900">{value}</span>
          {unit && (
            <span className="text-sm text-slate-500">{unit}</span>
          )}
        </div>
      </div>
      <div className={`rounded-lg p-3 ${bgClass}`}>{icon}</div>
    </div>
  </div>
);

const SummaryCards: React.FC<SummaryCardsProps> = ({ summary }) => {
  if (!summary) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className="animate-pulse rounded-xl border border-slate-200 bg-white p-6"
          >
            <div className="mb-3 h-4 w-24 rounded bg-slate-200"></div>
            <div className="h-8 w-16 rounded bg-slate-200"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <StatCard
        icon={<Box className="h-6 w-6 text-blue-600" />}
        label="Total Equipment"
        value={summary.total_count}
        bgClass="bg-blue-100"
      />

      <StatCard
        icon={<Droplets className="h-6 w-6 text-cyan-600" />}
        label="Avg Flowrate"
        value={summary.avg_flowrate}
        unit="m³/h"
        bgClass="bg-cyan-100"
      />

      <StatCard
        icon={<Gauge className="h-6 w-6 text-orange-600" />}
        label="Avg Pressure"
        value={summary.avg_pressure}
        unit="bar"
        bgClass="bg-orange-100"
      />

      <StatCard
        icon={<Thermometer className="h-6 w-6 text-red-600" />}
        label="Avg Temperature"
        value={summary.avg_temperature}
        unit="°C"
        bgClass="bg-red-100"
      />
    </div>
  );
};

export default SummaryCards;
