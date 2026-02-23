'use client';

import { useState } from 'react';
import { Search } from 'lucide-react';

interface ScanFormProps {
  onScan: (url: string) => void;
  isSubmitting: boolean;
}

export default function ScanForm({ onScan, isSubmitting }: ScanFormProps) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url) onScan(url);
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Run a New SEO Audit</h3>
      <form onSubmit={handleSubmit} className="flex gap-4">
        <div className="flex-1 relative">
          <input
            type="url"
            placeholder="https://example.com"
            required
            className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <Search className="absolute left-3 top-3.5 text-gray-400" size={20} />
        </div>
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2"
        >
          {isSubmitting ? 'Starting Scan...' : 'Start Audit'}
        </button>
      </form>
      <p className="mt-4 text-sm text-gray-500">
        Enter a full URL including https:// for the best results.
      </p>
    </div>
  );
}
