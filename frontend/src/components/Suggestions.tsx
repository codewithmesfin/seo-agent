'use client';

import React from 'react';
import { Lightbulb, CheckCircle2, AlertCircle } from 'lucide-react';

interface Suggestion {
  category: string;
  issue: string;
  suggestion: string;
}

interface SuggestionsProps {
  suggestions: Suggestion[];
}

export default function Suggestions({ suggestions }: SuggestionsProps) {
  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
      <div className="flex items-center gap-2 mb-6">
        <Lightbulb className="text-yellow-500" size={24} />
        <h3 className="text-xl font-bold text-gray-900 dark:text-white">Optimization Suggestions</h3>
      </div>
      <div className="space-y-4">
        {suggestions.length === 0 ? (
          <div className="flex items-center gap-3 p-4 bg-green-50 rounded-lg">
            <CheckCircle2 className="text-green-600" size={20} />
            <p className="text-green-800 font-medium">Your page is perfectly optimized!</p>
          </div>
        ) : (
          suggestions.map((item, index) => (
            <div key={index} className="flex gap-4 p-4 border border-gray-100 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <div className="mt-1">
                <AlertCircle className="text-primary-500" size={20} />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-bold uppercase tracking-wider px-2 py-0.5 bg-primary-100 text-primary-700 rounded">
                    {item.category}
                  </span>
                  <h4 className="font-semibold text-gray-900 dark:text-white">{item.issue}</h4>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{item.suggestion}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
