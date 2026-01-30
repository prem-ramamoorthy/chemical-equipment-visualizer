import type { CorrelationInsightsProps } from "../components/CorrelationInsights";
import type { StatisticalSummaryProps } from "../components/StatisticalSummary";

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

  DistributionAnalysis: {
    title: string;
    unit: string;
    stats: {
      min: number;
      q1: number;
      median: number;
      q3: number;
      max: number;
      outliers: number[];
    };
  };

  CorrelationInsights: CorrelationInsightsProps

  ConditionalAnalysis: {
    conditionLabel: string;
    totalRecords: number;
    stats: {
      flowrate: number;
      pressure: number;
      temperature: number;
    };
  };

  EquipmentPerformanceRanking: {
    [equipmentName: string]: {
      flowrate: number;
      pressure: number;
      temperature: number;
    };
  };

  StatisticalSummary: StatisticalSummaryProps

  GroupedEquipmentAnalytics: {
    [equipmentType: string]: {
      flowrate: {
        mean: number;
        std: number;
        min: number;
        max: number;
      };
      pressure: {
        mean: number;
        std: number;
        min: number;
        max: number;
      };
      temperature: {
        mean: number;
        std: number;
        min: number;
        max: number;
      };
    };
  };

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
