import { useState, useCallback } from "react";
import Navbar from "../components/Navbar";
import FileUpload from "../components/FileUpload";
import SummaryCards from "../components/SummaryCards";
import Charts from "../components/Charts";
import DataTable from "../components/DataTable";
import HistoryList from "../components/HistoryList";
import type { DatasetSummary, UploadHistory } from "../types/dataset";
import { mockUploadCSV } from "../api/apiClient";

const Dashboard = () => {
  const username = localStorage.getItem('username') || 'Guest';
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
      localStorage.removeItem('username');
      localStorage.removeItem('isAuthenticated');
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
      if (dataset) {
        setCurrentDataset(dataset);
      }
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

            <Charts summary={currentDataset} />

            <DataTable data={currentDataset?.data ?? []} />
          </section>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
