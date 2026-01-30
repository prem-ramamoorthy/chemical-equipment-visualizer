import { useState, useCallback } from "react";
import Navbar from "../components/Navbar";
import FileUpload from "../components/FileUpload";
import AdvancedChartsGrid from "../components/AdvancedChartsGrid";
import DataTable from "../components/DataTable";
import HistoryList from "../components/HistoryList";
import type { DatasetSummary, UploadHistory, ChartsGridSummary } from "../types/dataset";
import { mockUploadCSV } from "../api/apiClient";
import DistributionAnalysis from "../components/DistributionAnalysis";
import StatisticalSummary from "../components/StatisticalSummary";
import GroupedEquipmentAnalytics from "../components/GroupedEquipmentAnalytics";
import CorrelationInsights from "../components/CorrelationInsights";
import ConditionalAnalysis from "../components/ConditionalAnalysis";
import EquipmentPerformanceRanking from "../components/EquipmentPerformanceRanking";

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
    labels: ['A', 'B', 'C', 'D'],
    values: [
      [10, 25, 40, 55, 80],
      [15, 30, 45, 60, 85],
      [20, 35, 50, 65, 90],
      [25, 45, 60, 75, 100],
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

  StatisticalSummary: {
    data: {
      flowrate: {
        count: 500,
        mean: 126.0074,
        std: 37.472654,
        min: 51.3,
        q1: 99.4,
        median: 137.25,
        q3: 157.5,
        max: 174.8,
      },
      pressure: {
        count: 500,
        mean: 6.4444,
        std: 1.431519,
        min: 3.5,
        q1: 5.5,
        median: 6.8,
        q3: 7.4,
        max: 8.8,
      },
      temperature: {
        count: 500,
        mean: 120.9308,
        std: 16.418311,
        min: 90.2,
        q1: 106.75,
        median: 122.35,
        q3: 134.175,
        max: 150.0,
      },
    }
  },

  GroupedEquipmentAnalytics: {
    Compressor: {
      flowrate: { mean: 97.61, std: 6.71, min: 85.2, max: 109.7 },
      pressure: { mean: 8.33, std: 0.29, min: 7.8, max: 8.8 },
      temperature: { mean: 96.8, std: 4.67, min: 90.2, max: 104.8 },
    },
    Condenser: {
      flowrate: { mean: 164.72, std: 5.53, min: 155.5, max: 174.8 },
      pressure: { mean: 7.0, std: 0.29, min: 6.5, max: 7.5 },
      temperature: { mean: 128.08, std: 4.37, min: 120.0, max: 134.8 },
    },
    HeatExchanger: {
      flowrate: { mean: 154.42, std: 8.07, min: 140.2, max: 169.8 },
      pressure: { mean: 6.4, std: 0.36, min: 5.8, max: 7.0 },
      temperature: { mean: 132.96, std: 7.57, min: 120.1, max: 144.4 },
    },
    Pump: {
      flowrate: { mean: 126.26, std: 8.36, min: 110.1, max: 139.9 },
      pressure: { mean: 5.46, std: 0.4, min: 4.8, max: 6.2 },
      temperature: { mean: 113.9, std: 5.68, min: 105.1, max: 124.8 },
    },
    Reactor: {
      flowrate: { mean: 143.12, std: 7.1, min: 130.0, max: 154.8 },
      pressure: { mean: 7.38, std: 0.34, min: 6.8, max: 8.0 },
      temperature: { mean: 143.03, std: 4.39, min: 135.2, max: 150.0 },
    },
    Valve: {
      flowrate: { mean: 59.77, std: 5.54, min: 51.3, max: 69.9 },
      pressure: { mean: 3.96, std: 0.27, min: 3.5, max: 4.5 },
      temperature: { mean: 107.33, std: 4.35, min: 100.3, max: 115.0 },
    },
  },

  DistributionAnalysis: {
    title: "Flowrate",
    unit: " m³/h",
    stats: {
      min: 12,
      q1: 20,
      median: 28,
      q3: 35,
      max: 42,
      outliers: [45],
    }
  },

  CorrelationInsights: {
    matrix: {
      Flowrate: {
        Flowrate: 1.0,
        Pressure: 0.4957,
        Temperature: 0.6998,
      },
      Pressure: {
        Flowrate: 0.4957,
        Pressure: 1.0,
        Temperature: 0.1627,
      },
      Temperature: {
        Flowrate: 0.6998,
        Pressure: 0.1627,
        Temperature: 1.0,
      },
    }
  },

  ConditionalAnalysis: {
    conditionLabel: "Records with ABOVE average pressure",
    totalRecords: 301,
    stats: {
      flowrate: 140.330233,
      pressure: 7.42093,
      temperature: 124.555482,
    }
  },

  EquipmentPerformanceRanking:
  {
    Compressor: {
      flowrate: 97.61,
      pressure: 8.33,
      temperature: 96.8,
    },
    Reactor: {
      flowrate: 143.12,
      pressure: 7.38,
      temperature: 143.03,
    },
    Condenser: {
      flowrate: 164.72,
      pressure: 7.0,
      temperature: 128.08,
    },
    HeatExchanger: {
      flowrate: 154.42,
      pressure: 6.4,
      temperature: 132.96,
    },
    Pump: {
      flowrate: 126.26,
      pressure: 5.46,
      temperature: 113.9,
    },
    Valve: {
      flowrate: 59.77,
      pressure: 3.96,
      temperature: 107.33,
    },
  }

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

  const handleUpload = useCallback(async (file: File, filename: string) => {
    setIsUploading(true);

    try {
      const dataset = await mockUploadCSV(file, `${import.meta.env.VITE_API_BASE_URL}/datasets/upload/`);

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

            <StatisticalSummary
              data={mockDatasetSummary.StatisticalSummary.data}
            />

            <AdvancedChartsGrid summary={mockDatasetSummary} />

            <CorrelationInsights
              matrix={mockDatasetSummary.CorrelationInsights.matrix}
            />

            <ConditionalAnalysis
              conditionLabel={mockDatasetSummary.ConditionalAnalysis.conditionLabel}
              totalRecords={mockDatasetSummary.ConditionalAnalysis.totalRecords}
              stats={mockDatasetSummary.ConditionalAnalysis.stats}
            />

            <DistributionAnalysis
              title={mockDatasetSummary.DistributionAnalysis.title}
              unit={mockDatasetSummary.DistributionAnalysis.unit}
              stats={mockDatasetSummary.DistributionAnalysis.stats}
            />

            <EquipmentPerformanceRanking
              data={mockDatasetSummary.EquipmentPerformanceRanking}
            />

            <GroupedEquipmentAnalytics
              data={mockDatasetSummary.GroupedEquipmentAnalytics}
            />

            <DataTable data={currentDataset?.data ?? []} />
          </section>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
