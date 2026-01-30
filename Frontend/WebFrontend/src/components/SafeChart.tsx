import React, { useRef, useEffect } from 'react';
import { Chart } from 'react-chartjs-2';

interface SafeChartProps {
  type: any;
  data: any;
  options?: any;
  chartKey: string;
}

const SafeChart: React.FC<SafeChartProps> = ({ type, data, options, chartKey }) => {
  const chartRef = useRef<any>(null);

  useEffect(() => {
    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, [chartKey]);

  return <Chart ref={chartRef} type={type} data={data} options={options} key={chartKey} />;
};

export default SafeChart;
