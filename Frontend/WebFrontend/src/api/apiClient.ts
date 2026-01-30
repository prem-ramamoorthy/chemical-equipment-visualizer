import type { Equipment, DatasetSummary } from '../types/dataset';

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

export const mockDatasets: DatasetSummary[] = [
  calculateSummary(1, mockEquipment1),
  calculateSummary(2, mockEquipment2),
];

export const mockLogin = async (username: string, password: string): Promise<boolean> => {
  await new Promise((resolve) => setTimeout(resolve, 800));

  if (username.length > 0 && password.length > 0) {
    return true;
  }
  return false;
};

export const mockUploadCSV = async (file: File, url: string): Promise<DatasetSummary> => {
  const serverData = await uploadCSVToServer(file, url);

  if (Array.isArray(serverData) && serverData.length > 0 && serverData[0].name && serverData[0].type) {
    const equipmentData: Equipment[] = serverData.map((item: any) => ({
      name: item.name,
      type: item.type,
      flowrate: parseFloat(item.flowrate),
      pressure: parseFloat(item.pressure),
      temperature: parseFloat(item.temperature),
    }));
    return {
      ...calculateSummary(Date.now(), equipmentData),
      id: Date.now(),
    };
  }

  const randomIndex = Math.floor(Math.random() * mockDatasets.length);
  const dataset = mockDatasets[randomIndex];
  return {
    ...dataset,
    id: Date.now(),
  };
};

export const uploadCSVToServer = async (file: File, url: string): Promise<any> => {
  const text = await file.text();
  const rows = text.trim().split('\n');
  const headers = rows[0].split(',');
  const data = rows.slice(1).map(row => {
    const values = row.split(',');
    return headers.reduce((obj, header, idx) => {
      obj[header.trim()] = values[idx]?.trim();
      return obj;
    }, {} as Record<string, string>);
  });

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to upload CSV');
  }

  return response.json();
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