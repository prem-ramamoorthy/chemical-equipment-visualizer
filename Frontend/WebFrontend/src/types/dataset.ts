export interface Equipment {
  name: string;
  type: string;
  flowrate: number;
  pressure: number;
  temperature: number;
}

export interface DatasetSummary {
  id: number;
  total_count: number;
  avg_flowrate: number;
  avg_pressure: number;
  avg_temperature: number;
  type_distribution: Record<string, number>;
  data: Equipment[];
}

export interface User {
  username: string;
  isAuthenticated: boolean;
}

export interface UploadHistory {
  id: number;
  filename: string;
  uploadedAt: Date;
  datasetId: number;
}
