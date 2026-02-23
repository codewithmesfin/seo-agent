'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth-context';
import {
  LayoutDashboard,
  Search,
  BarChart3,
  Users,
  Settings,
  LogOut,
  Menu,
  X
} from 'lucide-react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(true);

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'New Scan', href: '/dashboard/scan', icon: Search },
    { name: 'Reports', href: '/dashboard/reports', icon: BarChart3 },
    { name: 'Competitors', href: '/dashboard/competitors', icon: Users },
    { name: 'Settings', href: '/dashboard/settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex">
      {/* Sidebar */}
      <aside className={`${isSidebarOpen ? 'w-64' : 'w-20'} bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transition-all duration-300 flex flex-col`}>
        <div className="h-16 flex items-center justify-between px-6 border-b border-gray-200 dark:border-gray-700">
          <span className={`font-bold text-xl text-primary-600 ${!isSidebarOpen && 'hidden'}`}>SEO Platform</span>
          <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
        <nav className="flex-1 mt-6 px-4 space-y-2">
          {navigation.map((item) => (
            <Link key={item.name} href={item.href} className="flex items-center space-x-3 p-3 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-primary-50 hover:text-primary-600 dark:hover:bg-gray-700 transition-colors">
              <item.icon size={20} />
              <span className={!isSidebarOpen ? 'hidden' : ''}>{item.name}</span>
            </Link>
          ))}
        </nav>
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <button onClick={logout} className="flex items-center space-x-3 p-3 w-full rounded-lg text-red-600 hover:bg-red-50 transition-colors">
            <LogOut size={20} />
            <span className={!isSidebarOpen ? 'hidden' : ''}>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-8">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Welcome back, {user?.email}</h2>
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-bold">
              U
            </div>
          </div>
        </header>
        <div className="flex-1 overflow-auto p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
