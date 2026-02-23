'use client';

import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

interface SEOGaugeProps {
  score: number;
  label: string;
}

export default function SEOGauge({ score, label }: SEOGaugeProps) {
  const data = [
    { value: score },
    { value: 100 - score }
  ];

  const getColor = (value: number) => {
    if (value >= 90) return '#10b981'; // Green
    if (value >= 70) return '#f59e0b'; // Amber
    return '#ef4444'; // Red
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex flex-col items-center">
      <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">{label}</h4>
      <div className="h-40 w-full relative">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={70}
              startAngle={180}
              endAngle={0}
              paddingAngle={0}
              dataKey="value"
            >
              <Cell fill={getColor(score)} />
              <Cell fill="#e5e7eb" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex items-center justify-center pt-8">
          <span className="text-3xl font-bold" style={{ color: getColor(score) }}>{score}</span>
        </div>
      </div>
    </div>
  );
}
