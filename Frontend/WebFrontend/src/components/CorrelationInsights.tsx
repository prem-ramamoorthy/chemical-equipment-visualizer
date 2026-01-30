import React from 'react';
import { Link2, TrendingUp, Minus, TrendingDown } from 'lucide-react';

interface CorrelationMatrix {
  [row: string]: {
    [col: string]: number;
  };
}

export interface CorrelationInsightsProps {
  matrix: CorrelationMatrix;
}

const getStrength = (value: number) => {
  const abs = Math.abs(value);
  if (abs >= 0.7) return { label: 'Strong', icon: TrendingUp, color: 'text-emerald-600' };
  if (abs >= 0.4) return { label: 'Moderate', icon: Minus, color: 'text-amber-600' };
  return { label: 'Weak', icon: TrendingDown, color: 'text-slate-500' };
};

const CorrelationInsights: React.FC<CorrelationInsightsProps> = ({ matrix }) => {
  const variables = Object.keys(matrix);

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      {/* Header */}
      <div className="mb-6 flex items-center gap-3">
        <div className="rounded-lg bg-indigo-50 p-2">
          <Link2 className="h-5 w-5 text-indigo-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-slate-900">
            Correlation Insights
          </h3>
          <p className="text-sm text-slate-500">
            Relationship strength between operational parameters
          </p>
        </div>
      </div>

      {/* Matrix */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr>
              <th className="border-b border-slate-200 px-4 py-2 text-left text-slate-500" />
              {variables.map(v => (
                <th
                  key={v}
                  className="border-b border-slate-200 px-4 py-2 text-left font-medium text-slate-700"
                >
                  {v}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {variables.map(row => (
              <tr key={row}>
                <td className="border-b border-slate-100 px-4 py-2 font-medium text-slate-700">
                  {row}
                </td>

                {variables.map(col => {
                  const value = matrix[row][col];
                  const { label, icon: Icon, color } = getStrength(value);

                  return (
                    <td
                      key={col}
                      className="border-b border-slate-100 px-4 py-3"
                    >
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-slate-900">
                          {value.toFixed(2)}
                        </span>
                        {row !== col && (
                          <span
                            className={`flex items-center gap-1 text-xs font-medium ${color}`}
                          >
                            <Icon className="h-3.5 w-3.5" />
                            {label}
                          </span>
                        )}
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Interpretation */}
      <div className="mt-6 rounded-lg bg-slate-50 p-4">
        <h4 className="mb-2 text-sm font-semibold text-slate-700">
          Interpretation Summary
        </h4>

        <ul className="space-y-2 text-sm text-slate-600">
          <li>
            <strong>Flowrate & Pressure:</strong> Moderate positive correlation
            (≈ 0.50), indicating pressure generally increases with flowrate.
          </li>
          <li>
            <strong>Flowrate & Temperature:</strong> Strong positive correlation
            (≈ 0.70), suggesting higher flowrates are associated with higher
            temperatures.
          </li>
          <li>
            <strong>Pressure & Temperature:</strong> Weak correlation
            (≈ 0.16), implying largely independent behavior.
          </li>
        </ul>
      </div>
    </div>
  );
};

export default CorrelationInsights;
