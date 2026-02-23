'use client';

import React from 'react';

interface ProgressIndicatorProps {
  status: 'idle' | 'running' | 'completed' | 'failed';
  progress: number;
}

export default function ProgressIndicator({ status, progress }: ProgressIndicatorProps) {
  if (status === 'idle') return null;

  const statusColors = {
    running: 'bg-primary-600',
    completed: 'bg-green-600',
    failed: 'bg-red-600',
    idle: 'bg-gray-400'
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 mt-6">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
          {status === 'running' ? 'Scanning in progress...' : `Status: ${status}`}
        </span>
        <span className="text-sm font-bold text-primary-600">{progress}%</span>
      </div>
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 overflow-hidden">
        <div
          className={`h-full transition-all duration-500 ${statusColors[status]}`}
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      {status === 'running' && (
        <p className="mt-4 text-xs text-gray-500 animate-pulse">
          Our crawlers are analyzing your page structure, performance, and SEO tags. This usually takes 30-60 seconds.
        </p>
      )}
    </div>
  );
}
