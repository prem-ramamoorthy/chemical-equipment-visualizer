import React, { useState } from 'react';
import { Table2, ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-react';
import type { EquipmentRecord } from '../types/dataset';

export interface DataTableProps {
  data: EquipmentRecord[];
}

type SortField = 'Equipment Name' | 'Type' | 'Flowrate' | 'Pressure' | 'Temperature';
type SortOrder = 'asc' | 'desc' | null;

const DataTable: React.FC<Partial<DataTableProps>> = ({ data }) => {
  if (!data) data = [];

  const [sortField, setSortField] = useState<SortField | null>(null);
  const [sortOrder, setSortOrder] = useState<SortOrder>(null);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      if (sortOrder === 'asc') setSortOrder('desc');
      else if (sortOrder === 'desc') {
        setSortOrder(null);
        setSortField(null);
      } else setSortOrder('asc');
    } else {
      setSortField(field);
      setSortOrder('asc');
    }
  };

  const getSortIcon = (field: SortField) => {
    if (sortField !== field) {
      return <ChevronsUpDown className="h-4 w-4 text-slate-400" />;
    }
    if (sortOrder === 'asc') {
      return <ChevronUp className="h-4 w-4 text-blue-600" />;
    }
    return <ChevronDown className="h-4 w-4 text-blue-600" />;
  };

  const sortedData = React.useMemo(() => {
    if (!sortField || !sortOrder) return data;

    return [...data].sort((a, b) => {
      const aVal: string | number | undefined = a[sortField];
      const bVal: string | number | undefined = b[sortField];

      if (['Flowrate', 'Pressure', 'Temperature'].includes(sortField)) {
        const aNum = typeof aVal === 'number' ? aVal : parseFloat(aVal as string);
        const bNum = typeof bVal === 'number' ? bVal : parseFloat(bVal as string);
        const safeANum = isNaN(aNum) ? 0 : aNum;
        const safeBNum = isNaN(bNum) ? 0 : bNum;
        return sortOrder === 'asc' ? safeANum - safeBNum : safeBNum - safeANum;
      }

      if (typeof aVal === 'string' && typeof bVal === 'string') {
        return sortOrder === 'asc'
          ? aVal.localeCompare(bVal)
          : bVal.localeCompare(aVal);
      }

      return 0;
    });
  }, [data, sortField, sortOrder]);

  const typeBadge = (type: string) => {
    if (type === 'Pump')
      return 'bg-blue-100 text-blue-700';
    if (type === 'Reactor')
      return 'bg-teal-100 text-teal-700';
    if (type === 'Heat Exchanger')
      return 'bg-orange-100 text-orange-700';
    return 'bg-slate-100 text-slate-700';
  };

  if (data.length === 0) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-md">
        <div className="mb-4 flex items-center gap-2">
          <Table2 className="h-5 w-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-slate-900">Equipment Data</h3>
        </div>
        <div className="py-12 text-center text-slate-500">
          No data available. Upload a dataset to view equipment details.
        </div>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-md" style={{ height: 400, display: 'flex', flexDirection: 'column' }}>
      <div className="flex items-center gap-2 border-b border-slate-200 px-6 py-4">
        <Table2 className="h-5 w-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-slate-900">Equipment Data</h3>
        <span className="ml-2 inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-700">
          {data.length} items
        </span>
      </div>

      <div className="overflow-x-auto flex-1" style={{ overflowY: 'auto' }}>
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-slate-100 text-xs font-semibold uppercase tracking-wide text-slate-500">
              {([
                { field: 'Equipment Name' as SortField, label: 'Equipment Name' },
                { field: 'Type' as SortField, label: 'Type' },
                { field: 'Flowrate' as SortField, label: 'Flowrate (m³/h)' },
                { field: 'Pressure' as SortField, label: 'Pressure (bar)' },
                { field: 'Temperature' as SortField, label: 'Temp (°C)' },
              ]).map((col) => (
                <th
                  key={col.field}
                  onClick={() => handleSort(col.field)}
                  className="cursor-pointer px-6 py-4 text-left transition hover:bg-slate-200"
                >
                  <div className="flex items-center gap-2">
                    <span>{col.label}</span>
                    {getSortIcon(col.field)}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedData.map((equipment, index) => (
              <tr
                key={`${equipment['Equipment Name']}-${index}`}
                className="border-b border-slate-200 transition hover:bg-slate-50"
              >
                <td className="px-6 py-4 font-medium text-slate-900">
                  {equipment['Equipment Name']}
                </td>
                <td className="px-6 py-4">
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${typeBadge(
                      equipment.Type
                    )}`}
                  >
                    {equipment.Type}
                  </span>
                </td>
                <td className="px-6 py-4 font-mono text-sm text-slate-600">
                  {parseFloat(equipment.Flowrate).toFixed(1)}
                </td>
                <td className="px-6 py-4 font-mono text-sm text-slate-600">
                  {parseFloat(equipment.Pressure).toFixed(1)}
                </td>
                <td className="px-6 py-4 font-mono text-sm text-slate-600">
                  {parseFloat(equipment.Temperature).toFixed(1)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;
