'use client';

import { useState } from 'react';
import DashboardLayout from '@/components/Layout';
import ScanForm from '@/components/ScanForm';
import ProgressIndicator from '@/components/ProgressIndicator';
import Suggestions from '@/components/Suggestions';
import api from '@/lib/api';

export default function ScanPage() {
  const [status, setStatus] = useState<'idle' | 'running' | 'completed' | 'failed'>('idle');
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<any>(null);

  const startScan = async (url: string) => {
    setStatus('running');
    setProgress(10);

    try {
      // In a real app, you'd poll an endpoint for progress
      // For this demo, we simulate the async process
      const { data } = await api.post('/scans', { url });

      let currentProgress = 10;
      const interval = setInterval(() => {
        currentProgress += 15;
        if (currentProgress >= 95) {
          clearInterval(interval);
        } else {
          setProgress(currentProgress);
        }
      }, 2000);

      // Simulate waiting for Celery
      setTimeout(() => {
        clearInterval(interval);
        setProgress(100);
        setStatus('completed');
        setResults({
          suggestions: [
            { category: 'Title', issue: 'Title too short', suggestion: 'Increase title to 50-60 chars' },
            { category: 'Meta', issue: 'Missing meta description', suggestion: 'Add a description for better CTR' }
          ]
        });
      }, 10000);

    } catch (err) {
      setStatus('failed');
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">New SEO Audit</h1>
          <p className="text-gray-500">Analyze any website in seconds.</p>
        </div>

        <ScanForm onScan={startScan} isSubmitting={status === 'running'} />

        <ProgressIndicator status={status} progress={progress} />

        {status === 'completed' && results && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <Suggestions suggestions={results.suggestions} />
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
