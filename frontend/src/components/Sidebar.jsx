import React from 'react';
import { 
  GraduationCap, 
  Sparkles, 
  BarChart3, 
  Database, 
  BrainCircuit, 
  CheckCircle2, 
  XCircle,
  RefreshCw
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, isServerOnline, onCheckHealth }) {
  const navItems = [
    { id: 'predict', label: 'Predict & Dashboard', icon: Sparkles },
    { id: 'metrics', label: 'Model Evaluation', icon: BarChart3 },
    { id: 'dataset', label: 'Dataset Explorer', icon: Database },
    { id: 'guide', label: 'Algorithm Guide', icon: BrainCircuit },
  ];

  return (
    <aside className="w-full lg:w-64 bg-slate-900/90 border-r border-slate-800 flex flex-col justify-between shrink-0">
      <div>
        {/* Brand Logo & Title */}
        <div className="p-6 border-b border-slate-800/80">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/20">
              <GraduationCap className="w-6 h-6" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-white tracking-tight leading-none">
                MarksPredict
              </h1>
              <span className="text-xs text-indigo-400 font-medium">
                React + FastAPI ML
              </span>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-4 space-y-1.5">
          <div className="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Menu
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md shadow-indigo-600/25 font-semibold'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Backend Server Status Pill */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-950/40 m-3 rounded-2xl">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-slate-400">FastAPI Backend</span>
          <button 
            onClick={onCheckHealth}
            title="Check server connection"
            className="text-slate-400 hover:text-white transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
        <div className="flex items-center gap-2">
          {isServerOnline ? (
            <>
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <span className="text-xs font-semibold text-emerald-400">Connected (:8000)</span>
            </>
          ) : (
            <>
              <span className="relative flex h-2.5 w-2.5">
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500"></span>
              </span>
              <span className="text-xs font-semibold text-rose-400">Offline</span>
            </>
          )}
        </div>
        <div className="mt-2 text-[11px] text-slate-500 leading-tight">
          Supervised Linear Regression • scikit-learn
        </div>
      </div>
    </aside>
  );
}
