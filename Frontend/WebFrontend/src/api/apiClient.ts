import type { Equipment, DatasetSummary } from '../types/dataset';

// Mock equipment data for Dataset 1
const mockEquipment1: Equipment[] = [
  { name: 'P-101', type: 'Pump', flowrate: 125.5, pressure: 3.2, temperature: 45.0 },
  { name: 'R-201', type: 'Reactor', flowrate: 450.0, pressure: 8.5, temperature: 180.0 },
  { name: 'E-301', type: 'Heat Exchanger', flowrate: 320.0, pressure: 2.8, temperature: 95.0 },
  { name: 'P-102', type: 'Pump', flowrate: 98.0, pressure: 4.1, temperature: 38.0 },
  { name: 'R-202', type: 'Reactor', flowrate: 380.0, pressure: 12.0, temperature: 220.0 },
  { name: 'E-302', type: 'Heat Exchanger', flowrate: 275.0, pressure: 3.5, temperature: 110.0 },
  { name: 'P-103', type: 'Pump', flowrate: 150.0, pressure: 2.9, temperature: 42.0 },
  { name: 'E-303', type: 'Heat Exchanger', flowrate: 190.0, pressure: 2.2, temperature: 75.0 },
];

// Mock equipment data for Dataset 2
const mockEquipment2: Equipment[] = [
  { name: 'P-401', type: 'Pump', flowrate: 88.0, pressure: 5.0, temperature: 52.0 },
  { name: 'R-501', type: 'Reactor', flowrate: 520.0, pressure: 15.0, temperature: 250.0 },
  { name: 'E-601', type: 'Heat Exchanger', flowrate: 410.0, pressure: 4.2, temperature: 130.0 },
  { name: 'P-402', type: 'Pump', flowrate: 112.0, pressure: 3.8, temperature: 40.0 },
  { name: 'R-502', type: 'Reactor', flowrate: 480.0, pressure: 10.5, temperature: 195.0 },
  { name: 'E-602', type: 'Heat Exchanger', flowrate: 350.0, pressure: 3.0, temperature: 88.0 },
];

const calculateSummary = (id: number, data: Equipment[]): DatasetSummary => {
  const total_count = data.length;
  const avg_flowrate = parseFloat((data.reduce((sum, eq) => sum + eq.flowrate, 0) / total_count).toFixed(2));
  const avg_pressure = parseFloat((data.reduce((sum, eq) => sum + eq.pressure, 0) / total_count).toFixed(2));
  const avg_temperature = parseFloat((data.reduce((sum, eq) => sum + eq.temperature, 0) / total_count).toFixed(2));

  const type_distribution: Record<string, number> = {};
  data.forEach((eq) => {
    type_distribution[eq.type] = (type_distribution[eq.type] || 0) + 1;
  });

  return {
    id,
    total_count,
    avg_flowrate,
    avg_pressure,
    avg_temperature,
    type_distribution,
    data,
  };
};

// Pre-calculated mock datasets
export const mockDatasets: DatasetSummary[] = [
  calculateSummary(1, mockEquipment1),
  calculateSummary(2, mockEquipment2),
];

// Simulated API functions
export const mockLogin = async (username: string, password: string): Promise<boolean> => {
  // Simulate network delay
  await new Promise((resolve) => setTimeout(resolve, 800));

  // Accept any non-empty credentials for demo
  if (username.length > 0 && password.length > 0) {
    return true;
  }
  return false;
};

export const mockUploadCSV = async (filename : string): Promise<DatasetSummary> => {
  // Simulate network delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Randomly return one of the mock datasets
  const randomIndex = Math.floor(Math.random() * mockDatasets.length);
  const dataset = mockDatasets[randomIndex];

  // Return a copy with a new ID based on timestamp
  return {
    ...dataset,
    id: Date.now(),
  };
};

export const getDatasetById = (id: number): DatasetSummary | undefined => {
  return mockDatasets.find((ds) => ds.id === id);
};

export interface SignupResponse {
  success: boolean;
  username?: string;
}

export const mockSignup = async (
  username: string,
  email: string,
  password: string
): Promise<SignupResponse> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("Signup called with:", { username, email, password });
      resolve({ success: true, username });
    }, 1000); // simulate network delay
  })
};