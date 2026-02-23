'use client';

import DashboardLayout from '@/components/Layout';
import SEOGauge from '@/components/charts/SEOGauge';
import CompetitorChart from '@/components/charts/CompetitorChart';
import { useAuth } from '@/lib/auth-context';

export default function DashboardPage() {
  const { user } = useAuth();

  const mockStats = [
    { label: 'Avg SEO Score', score: 82 },
    { label: 'Avg Performance', score: 74 },
    { label: 'Pages Scanned', score: 145 },
  ];

  const competitorData = [
    { name: 'Your Site', score: 82 },
    { name: 'Competitor A', score: 91 },
    { name: 'Competitor B', score: 78 },
    { name: 'Competitor C', score: 85 },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Analytics Overview</h1>
          <p className="text-gray-500">Track your SEO and performance progress over time.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {mockStats.map((stat) => (
            <SEOGauge key={stat.label} score={stat.score} label={stat.label} />
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <CompetitorChart data={competitorData} />
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
            <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Recent Scans</h4>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex justify-between items-center p-3 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg transition-colors cursor-pointer">
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">https://example.com/blog/post-{i}</p>
                    <p className="text-xs text-gray-500">2 hours ago</p>
                  </div>
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded">92</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
