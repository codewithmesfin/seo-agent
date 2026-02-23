'use client';

import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/Layout';
import ScanForm from '@/components/ScanForm';
import ProgressIndicator from '@/components/ProgressIndicator';
import Suggestions from '@/components/Suggestions';
import api from '@/lib/api';

export default function ScanPage() {
  const [status, setStatus] = useState<'idle' | 'running' | 'completed' | 'failed'>('idle');
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<any>(null);
  const [scanId, setScanId] = useState<string | null>(null);

  const startScan = async (url: string) => {
    setStatus('running');
    setProgress(5);
    try {
      const { data } = await api.post('/scans', { url });
      setScanId(data._id);
    } catch (err) {
      setStatus('failed');
    }
  };

  useEffect(() => {
    let interval: any;
    if (status === 'running' && scanId) {
      interval = setInterval(async () => {
        try {
          const { data } = await api.get(`/scans/${scanId}`);
          const scan = data.scan;
          if (scan.status === 'completed') {
            setStatus('completed');
            setProgress(100);
            setResults(data);
            clearInterval(interval);
          } else if (scan.status === 'failed') {
            setStatus('failed');
            clearInterval(interval);
          } else {
            // Simulated progress while waiting for worker
            setProgress((prev) => Math.min(prev + 10, 95));
          }
        } catch (err) {
          console.error("Polling error", err);
        }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [status, scanId]);

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
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-6">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
               <h3 className="text-xl font-bold mb-4">Audit Summary</h3>
               <div className="flex gap-8">
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Overall Score</p>
                    <p className="text-4xl font-bold text-primary-600">{Math.round(results.scan.overall_score)}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Pages Crawled</p>
                    <p className="text-4xl font-bold">{results.scan.pages_count}</p>
                  </div>
               </div>
            </div>
            {/* Show suggestions from the first page for simplicity */}
            {results.pages && results.pages.length > 0 && (
              <Suggestions suggestions={[]} />
            )}
            <p className="text-center text-sm text-gray-400 italic">Full suggestions per page available in detailed reports.</p>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
