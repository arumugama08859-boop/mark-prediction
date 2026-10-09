import React from 'react';
import { Sparkles, Award, Cpu, BookOpen } from 'lucide-react';

export default function WelcomeBanner({ metrics, datasetSummary }) {
  const r2Score = metrics ? `${metrics.r2_percentage}%` : '98.9%';
  const totalRecords = datasetSummary ? `${datasetSummary.total_records}` : '40';
  const correlation = datasetSummary ? `${datasetSummary.correlation}` : '0.99';

  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blue-900/80 via-indigo-900/80 to-purple-900/80 border border-indigo-500/30 p-6 md:p-8 shadow-2xl shadow-indigo-950/50 mb-8">
      {/* Decorative background glow circles */}
      <div className="absolute -top-16 -right-16 w-64 h-64 bg-purple-500/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-16 -left-16 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-xs font-semibold text-indigo-200 mb-3">
            <Sparkles className="w-3.5 h-3.5 text-yellow-300" />
            <span>MACHINE LEARNING DEMONSTRATOR</span>
          </div>

          <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight mb-2">
            Student Marks Predictor
          </h1>

          <p className="text-sm md:text-base text-slate-300 leading-relaxed">
            Estimate student examination marks based on daily study hours using a trained
            Ordinary Least Squares (OLS) Linear Regression model built with Python, FastAPI, and React.
          </p>
        </div>

        {/* Quick Highlights Grid */}
        <div className="grid grid-cols-2 gap-3 sm:flex sm:items-center">
          <div className="bg-slate-900/60 backdrop-blur-md border border-slate-700/60 rounded-2xl p-3.5 text-center min-w-[105px]">
            <div className="flex items-center justify-center text-indigo-400 mb-1">
              <Award className="w-4 h-4" />
            </div>
            <div className="text-xl font-bold text-white">{r2Score}</div>
            <div className="text-[11px] font-medium text-slate-400">R² Accuracy</div>
          </div>

          <div className="bg-slate-900/60 backdrop-blur-md border border-slate-700/60 rounded-2xl p-3.5 text-center min-w-[105px]">
            <div className="flex items-center justify-center text-purple-400 mb-1">
              <BookOpen className="w-4 h-4" />
            </div>
            <div className="text-xl font-bold text-white">{totalRecords}</div>
            <div className="text-[11px] font-medium text-slate-400">Students</div>
          </div>

          <div className="bg-slate-900/60 backdrop-blur-md border border-slate-700/60 rounded-2xl p-3.5 text-center min-w-[105px] col-span-2 sm:col-span-1">
            <div className="flex items-center justify-center text-blue-400 mb-1">
              <Cpu className="w-4 h-4" />
            </div>
            <div className="text-xl font-bold text-white">{correlation}</div>
            <div className="text-[11px] font-medium text-slate-400">Pearson r</div>
          </div>
        </div>
      </div>
    </div>
  );
}
