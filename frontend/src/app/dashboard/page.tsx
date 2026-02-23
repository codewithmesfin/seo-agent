'use client';

import { useQuery } from '@tanstack/react-query';
import DashboardLayout from '@/components/Layout';
import SEOGauge from '@/components/charts/SEOGauge';
import CompetitorChart from '@/components/charts/CompetitorChart';
import { useAuth } from '@/lib/auth-context';
import api from '@/lib/api';
import { Loader2 } from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuth();

  const { data: scans, isLoading } = useQuery({
    queryKey: ['scans'],
    queryFn: async () => {
      const { data } = await api.get('/scans');
      return data;
    },
  });

  const avgScore = scans?.length
    ? Math.round(scans.reduce((acc: number, s: any) => acc + s.overall_score, 0) / scans.length)
    : 0;

  const mockStats = [
    { label: 'Avg SEO Score', score: avgScore },
    { label: 'Scans Done', score: scans?.length || 0 },
    { label: 'Health Index', score: scans?.length ? 85 : 0 },
  ];

  const competitorData = [
    { name: 'Your Average', score: avgScore },
    { name: 'Competitor A', score: 91 },
    { name: 'Competitor B', score: 78 },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Analytics Overview</h1>
          <p className="text-gray-500">Track your SEO and performance progress over time.</p>
        </div>

        {isLoading ? (
          <div className="flex justify-center p-12"><Loader2 className="animate-spin text-primary-600" size={40} /></div>
        ) : (
          <>
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
                  {!scans || scans.length === 0 ? (
                    <p className="text-center text-gray-500 py-8">No scans found. Start your first audit!</p>
                  ) : (
                    scans.slice(0, 5).map((scan: any) => (
                      <div key={scan._id} className="flex justify-between items-center p-3 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg transition-colors cursor-pointer">
                        <div>
                          <p className="font-medium text-gray-900 dark:text-white truncate max-w-xs">{scan.domain}</p>
                          <p className="text-xs text-gray-500">{new Date(scan.created_at).toLocaleDateString()}</p>
                        </div>
                        <div className="flex items-center gap-2">
                           <span className={`px-2 py-1 text-xs font-bold rounded ${
                             scan.status === 'completed' ? 'bg-green-100 text-green-700' :
                             scan.status === 'failed' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
                           }`}>
                             {scan.status === 'completed' ? Math.round(scan.overall_score) : scan.status}
                           </span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
