import React from "react";
import { History, FileSpreadsheet, Clock, ChevronRight } from "lucide-react";
import type { UploadHistory, DatasetSummary } from "../types/dataset";

interface HistoryListProps {
  history: UploadHistory[];
  datasets: Map<number, DatasetSummary>;
  onSelect: (datasetId: number) => void;
  currentDatasetId: number | null;
}

const HistoryList: React.FC<HistoryListProps> = ({
  history,
  datasets,
  onSelect,
  currentDatasetId,
}) => {
  const formatTime = (date: Date): string =>
    new Intl.DateTimeFormat("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    }).format(date);

  const formatDate = (date: Date): string => {
    const today = new Date();
    const isToday =
      date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear();

    if (isToday) {
      return `Today, ${formatTime(date)}`;
    }

    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center gap-2">
        <History className="h-5 w-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-slate-900">
          Upload History
        </h3>
      </div>

      {history.length === 0 ? (
        <div className="py-10 text-center text-slate-500">
          <Clock className="mx-auto mb-3 h-10 w-10 opacity-40" />
          <p className="text-sm">No uploads yet</p>
        </div>
      ) : (
        <div className="space-y-2">
          {history.map((item) => {
            const dataset = datasets.get(item.datasetId);
            const isActive = currentDatasetId === item.datasetId;

            return (
              <button
                key={item.id}
                onClick={() => onSelect(item.datasetId)}
                className={`flex w-full items-center gap-3 rounded-lg border p-3 text-left transition ${
                  isActive
                    ? "border-blue-300 bg-blue-50"
                    : "border-transparent bg-slate-50 hover:border-slate-200 hover:bg-slate-100"
                }`}
              >
                <div
                  className={`flex h-9 w-9 items-center justify-center rounded-lg ${
                    isActive ? "bg-blue-600" : "bg-slate-200"
                  }`}
                >
                  <FileSpreadsheet
                    className={`h-4 w-4 ${
                      isActive ? "text-white" : "text-slate-600"
                    }`}
                  />
                </div>

                <div className="min-w-0 flex-1">
                  <p
                    className={`truncate text-sm font-medium ${
                      isActive ? "text-blue-700" : "text-slate-900"
                    }`}
                  >
                    {item.filename}
                  </p>
                  <div className="mt-0.5 flex items-center gap-2 text-xs text-slate-500">
                    <Clock className="h-3 w-3" />
                    <span>{formatDate(item.uploadedAt)}</span>
                    {dataset && (
                      <span>• {dataset.total_count} items</span>
                    )}
                  </div>
                </div>

                <ChevronRight
                  className={`h-4 w-4 shrink-0 ${
                    isActive ? "text-blue-600" : "text-slate-400"
                  }`}
                />
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default HistoryList;
