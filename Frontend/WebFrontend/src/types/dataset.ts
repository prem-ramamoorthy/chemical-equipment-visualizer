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

export interface ChartsGridSummary {
  id: number;

  total_count: number;
  avg_flowrate: number;
  avg_pressure: number;
  avg_temperature: number;

  type_distribution: Record<string, number>;

  scatter_points: {
    x: number;
    y: number;
    t: number;
  }[];

  histogram: {
    labels: string[];
    flowrate: number[];
    temperature: number[];
  };

  boxplot: {
    labels: string[];
    values: number[][];
  };

  correlation: {
    x: string;
    y: string;
    v: number;
  }[];

  data: Record<string, unknown>[];
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
