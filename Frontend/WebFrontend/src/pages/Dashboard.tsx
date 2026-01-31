import { useState, useCallback } from "react";
import Navbar from "../components/Navbar";
import FileUpload from "../components/FileUpload";
import AdvancedChartsGrid from "../components/AdvancedChartsGrid";
import DataTable from "../components/DataTable";
import HistoryList from "../components/HistoryList";
import type { DatasetSummary, UploadHistory, ChartsGridSummary, EquipmentRecord } from "../types/dataset";
import { mockUploadCSV } from "../api/apiClient";
import DistributionAnalysis from "../components/DistributionAnalysis";
import StatisticalSummary from "../components/StatisticalSummary";
import GroupedEquipmentAnalytics from "../components/GroupedEquipmentAnalytics";
import CorrelationInsights from "../components/CorrelationInsights";
import ConditionalAnalysis from "../components/ConditionalAnalysis";
import EquipmentPerformanceRanking from "../components/EquipmentPerformanceRanking";

const Dashboard = () => {
  const username = localStorage.getItem("username") || "Guest";
  const [data, setData] = useState<EquipmentRecord[]>([]);

  const [currentDataset, setCurrentDataset] =
    useState<ChartsGridSummary | null>(null);

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
      const { serverdata: dataset, data } = await mockUploadCSV(file, `${import.meta.env.VITE_API_BASE_URL}/datasets/upload/`);
      setData(data);
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

            <StatisticalSummary data={currentDataset?.StatisticalSummary.data} />

            <AdvancedChartsGrid summary={currentDataset} />

            <CorrelationInsights
              matrix={currentDataset?.CorrelationInsights.matrix}
            />

            <ConditionalAnalysis
              conditionLabel={currentDataset?.ConditionalAnalysis.conditionLabel}
              totalRecords={currentDataset?.ConditionalAnalysis.totalRecords}
              stats={currentDataset?.ConditionalAnalysis.stats}
            />

            <DistributionAnalysis
              title={currentDataset?.DistributionAnalysis.title}
              unit={currentDataset?.DistributionAnalysis.unit}
              stats={currentDataset?.DistributionAnalysis.stats}
            />

            <EquipmentPerformanceRanking
              data={currentDataset?.EquipmentPerformanceRanking}
            />

            <GroupedEquipmentAnalytics
              data={currentDataset?.GroupedEquipmentAnalytics}
            />

            <DataTable data={data as EquipmentRecord[] ?? []} />
          </section>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
