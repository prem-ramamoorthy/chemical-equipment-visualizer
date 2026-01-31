import React from 'react';
import {
  Settings,
  Wind,
  Gauge,
  Thermometer,
} from 'lucide-react';

interface MetricStats {
  mean: number;
  std: number;
  min: number;
  max: number;
}

interface EquipmentAnalytics {
  flowrate: MetricStats;
  pressure: MetricStats;
  temperature: MetricStats;
}

interface GroupedAnalyticsProps {
  data: Record<string, EquipmentAnalytics>;
}

const round2 = (value: number) => Number(value).toFixed(2);

const MetricBlock = ({
  title,
  icon: Icon,
  unit,
  stats,
}: {
  title: string;
  icon: React.ElementType;
  unit: string;
  stats: MetricStats;
}) => (
  <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
    <div className="mb-3 flex items-center gap-2">
      <Icon className="h-4 w-4 text-blue-600" />
      <p className="text-sm font-semibold text-slate-800">{title}</p>
    </div>

    <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
      <Stat label="Mean" value={`${round2(stats.mean)}${unit}`} />
      <Stat label="Std" value={round2(stats.std)} />
      <Stat label="Min" value={`${round2(stats.min)}${unit}`} />
      <Stat label="Max" value={`${round2(stats.max)}${unit}`} />
    </div>
  </div>
);

const Stat = ({ label, value }: { label: string; value: number | string }) => (
  <div>
    <p className="text-xs text-slate-500">{label}</p>
    <p className="font-medium text-slate-900">{value}</p>
  </div>
);

const EquipmentCard = ({
  name,
  analytics,
}: {
  name: string;
  analytics: EquipmentAnalytics;
}) => (
  <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
    <div className="mb-5 flex items-center gap-3">
      <div className="rounded-lg bg-blue-50 p-2">
        <Settings className="h-5 w-5 text-blue-600" />
      </div>
      <h3 className="text-lg font-semibold text-slate-900">{name}</h3>
    </div>

    <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
      <MetricBlock
        title="Flowrate"
        icon={Wind}
        unit=" m³/h"
        stats={analytics.flowrate}
      />

      <MetricBlock
        title="Pressure"
        icon={Gauge}
        unit=" bar"
        stats={analytics.pressure}
      />

      <MetricBlock
        title="Temperature"
        icon={Thermometer}
        unit=" °C"
        stats={analytics.temperature}
      />
    </div>
  </div>
);

const GroupedEquipmentAnalytics: React.FC<Partial<GroupedAnalyticsProps>> = ({ data }) => {

  if (!data) {
    return (
      <div className="space-y-6">
        <div>
          <div className="h-6 w-64 bg-slate-200 rounded mb-2 animate-pulse" />
          <div className="h-4 w-40 bg-slate-100 rounded animate-pulse" />
        </div>

        <div className="space-y-6">
          {[1, 2].map((i) => (
            <div
              key={i}
              className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm animate-pulse"
            >
              <div className="mb-5 flex items-center gap-3">
                <div className="h-8 w-8 rounded-lg bg-slate-200 animate-pulse" />
                <div className="h-5 w-32 bg-slate-200 rounded animate-pulse" />
              </div>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                {[1, 2, 3].map((j) => (
                  <div
                    key={j}
                    className="rounded-lg border border-slate-200 bg-slate-50 p-4"
                  >
                    <div className="mb-3 flex items-center gap-2">
                      <div className="h-4 w-4 bg-slate-200 rounded animate-pulse" />
                      <div className="h-4 w-24 bg-slate-200 rounded animate-pulse" />
                    </div>
                    <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                      {[1, 2, 3, 4].map((k) => (
                        <div key={k} className="h-4 w-16 bg-slate-200 rounded animate-pulse" />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-slate-900">
          Grouped Analytics by Equipment Type
        </h2>
        <p className="text-sm text-slate-500">
          Mean, variability, and operating ranges across equipment categories
        </p>
      </div>

      <div className="space-y-6">
        {Object.entries(data).map(([equipment, analytics]) => (
          <EquipmentCard
            key={equipment}
            name={equipment}
            analytics={analytics}
          />
        ))}
      </div>
    </div>
  );
};

export default GroupedEquipmentAnalytics;
