import React from 'react';
import { Trophy, Wind, Gauge, Thermometer } from 'lucide-react';

interface PerformanceMetrics {
    flowrate: number;
    pressure: number;
    temperature: number;
}

interface EquipmentRankingProps {
    data: Record<string, PerformanceMetrics>;
}

const Metric = ({
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
    <div className="flex items-center justify-between rounded-lg bg-slate-50 px-4 py-2">
        <div className="flex items-center gap-2 text-slate-600">
            <Icon className="h-4 w-4" />
            <span className="text-xs">{label}</span>
        </div>
        <span className="text-sm font-semibold text-slate-900">
            {value.toFixed(2)}
            {unit}
        </span>
    </div>
);

const RankBadge = ({ rank }: { rank: number }) => {
    const styles = [
        'bg-yellow-100 text-yellow-700 border-yellow-300',
        'bg-slate-100 text-slate-700 border-slate-300',
        'bg-amber-100 text-amber-700 border-amber-300',
    ];

    return (
        <div
            className={`flex h-9 w-9 items-center justify-center rounded-full border text-sm font-bold ${styles[rank - 1] ?? 'bg-slate-50 text-slate-600 border-slate-200'
                }`}
        >
            #{rank}
        </div>
    );
};

const EquipmentCard = ({
    name,
    rank,
    metrics,
}: {
    name: string;
    rank: number;
    metrics: PerformanceMetrics;
}) => (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
                <RankBadge rank={rank} />
                <h3 className="text-lg font-semibold text-slate-900">{name}</h3>
            </div>
            {rank === 1 && (
                <div className="flex items-center gap-1 text-xs font-medium text-yellow-600 whitespace-nowrap">
                    <Trophy className="h-4 w-4" />
                    Top Performer
                </div>
            )}
        </div>

        <div className="space-y-2">
            <Metric icon={Wind} label="Flowrate" value={metrics.flowrate} unit=" m³/h" />
            <Metric icon={Gauge} label="Pressure" value={metrics.pressure} unit=" bar" />
            <Metric
                icon={Thermometer}
                label="Temperature"
                value={metrics.temperature}
                unit=" °C"
            />
        </div>
    </div>
);

const EquipmentPerformanceRanking: React.FC<EquipmentRankingProps> = ({ data }) => {
    const ranked = Object.entries(data).sort(
        (a, b) => b[1].flowrate - a[1].flowrate
    );

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-xl font-semibold text-slate-900">
                    Equipment Performance Ranking
                </h2>
                <p className="text-sm text-slate-500">
                    Ranked by operational performance metrics
                </p>
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
                {ranked.map(([name, metrics], index) => (
                    <EquipmentCard
                        key={name}
                        name={name}
                        rank={index + 1}
                        metrics={metrics}
                    />
                ))}
            </div>
        </div>
    );
};

export default EquipmentPerformanceRanking;