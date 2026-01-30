import { useState, useCallback } from "react";
import Navbar from "../components/Navbar";
import FileUpload from "../components/FileUpload";
import SummaryCards from "../components/SummaryCards";
import AdvancedChartsGrid from "../components/AdvancedChartsGrid";
import DataTable from "../components/DataTable";
import HistoryList from "../components/HistoryList";
import type { DatasetSummary, UploadHistory, ChartsGridSummary } from "../types/dataset";
import { mockUploadCSV } from "../api/apiClient";

const mockDatasetSummary: ChartsGridSummary = {
  id: 1,

  total_count: 500,
  avg_flowrate: 52.4,
  avg_pressure: 6.8,
  avg_temperature: 74.1,

  type_distribution: {
    Pump: 180,
    Valve: 140,
    Compressor: 100,
    "Heat Exchanger": 80,
  },

  scatter_points: Array.from({ length: 200 }, () => ({
    x: +(30 + Math.random() * 50).toFixed(2),
    y: +(4 + Math.random() * 5).toFixed(2), 
    t: +(60 + Math.random() * 30).toFixed(2)
  })),

  histogram: {
    labels: ["0–20", "20–40", "40–60", "60–80", "80–100"],
    flowrate: [12, 84, 210, 150, 44],
    temperature: [6, 70, 190, 180, 54],
  },

  boxplot: {
    labels: ["Pump", "Valve", "Compressor", "Heat Exchanger"],
    values: [
      [5.1, 5.6, 6.2, 6.5, 6.9, 5.8], 
      [4.4, 4.9, 5.2, 5.6, 5.8],
      [6.8, 7.1, 7.4, 7.7, 8.0],
      [5.9, 6.2, 6.5, 6.8, 7.0],
    ],
  },

  correlation: [
    { x: "Flowrate", y: "Flowrate", v: 1.0 },
    { x: "Flowrate", y: "Pressure", v: 0.62 },
    { x: "Flowrate", y: "Temperature", v: 0.48 },

    { x: "Pressure", y: "Flowrate", v: 0.62 },
    { x: "Pressure", y: "Pressure", v: 1.0 },
    { x: "Pressure", y: "Temperature", v: 0.71 },

    { x: "Temperature", y: "Flowrate", v: 0.48 },
    { x: "Temperature", y: "Pressure", v: 0.71 },
    { x: "Temperature", y: "Temperature", v: 1.0 },
  ],

  data: Array.from({ length: 20 }, (_, i) => ({
    id: i + 1,
    type: ["Pump", "Valve", "Compressor", "Heat Exchanger"][i % 4],
    flowrate: +(30 + Math.random() * 50).toFixed(2),
    pressure: +(4 + Math.random() * 5).toFixed(2),
    temperature: +(60 + Math.random() * 30).toFixed(2),
  })),
};

const Dashboard = () => {
  const username = localStorage.getItem("username") || "Guest";

  const [currentDataset, setCurrentDataset] =
    useState<DatasetSummary | null>(null);

  const [datasets, setDatasets] = useState<Map<number, DatasetSummary>>(
    new Map()
  );

  const [uploadHistory, setUploadHistory] = useState<UploadHistory[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const onLogout = async () => {
    try {
      await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/logout/`, {
        method: "POST",
        credentials: "include",
      });
    } catch (error) {
      console.error("Logout failed:", error);
    } finally {
      localStorage.removeItem("username");
      localStorage.removeItem("isAuthenticated");
      window.location.reload();
    }
  };

  const handleUpload = useCallback(async (filename: string) => {
    setIsUploading(true);

    try {
      const dataset = await mockUploadCSV(filename);

      setDatasets((prev) => {
        const next = new Map(prev);
        next.set(dataset.id, dataset);
        return next;
      });

      const historyItem: UploadHistory = {
        id: Date.now(),
        filename,
        uploadedAt: new Date(),
        datasetId: dataset.id,
      };

      setUploadHistory((prev) => [historyItem, ...prev].slice(0, 2));
      setCurrentDataset(dataset);
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      setIsUploading(false);
    }
  }, []);

  const handleSelectDataset = useCallback(
    (datasetId: number) => {
      const dataset = datasets.get(datasetId);
      if (dataset) setCurrentDataset(dataset);
    },
    [datasets]
  );

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar username={username} onLogout={onLogout} />

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-4">
          <aside className="space-y-6 lg:col-span-1">
            <FileUpload onUpload={handleUpload} isLoading={isUploading} />

            <HistoryList
              history={uploadHistory}
              datasets={datasets}
              onSelect={handleSelectDataset}
              currentDatasetId={currentDataset?.id ?? null}
            />
          </aside>

          <section className="space-y-6 lg:col-span-3">
            <SummaryCards summary={currentDataset} />

            <AdvancedChartsGrid summary={mockDatasetSummary} />

            <DataTable data={currentDataset?.data ?? []} />
          </section>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
