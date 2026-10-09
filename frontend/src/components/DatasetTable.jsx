import React, { useState } from 'react';
import { Database, Download, Search, Users, Clock, Award, TrendingUp } from 'lucide-react';

export default function DatasetTable({ dataset }) {
  const [searchTerm, setSearchTerm] = useState('');

  if (!dataset) {
    return (
      <div className="glass-panel rounded-3xl p-8 border border-slate-800 shadow-xl text-center">
        <p className="text-sm text-slate-400">Loading dataset...</p>
      </div>
    );
  }

  const { summary, data = [] } = dataset;

  // Filter records based on search
  const filteredData = data.filter((row) => {
    const term = searchTerm.toLowerCase();
    return (
      row.hours_studied.toString().includes(term) ||
      row.marks_percentage.toString().includes(term)
    );
  });

  // Handle CSV Download
  const handleDownloadCSV = () => {
    const header = 'Hours_Studied,Marks_Percentage\n';
    const rows = data.map((d) => `${d.hours_studied},${d.marks_percentage}`).join('\n');
    const blob = new Blob([header + rows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'student_marks_dataset.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl md:text-2xl font-bold text-white tracking-tight">
            Student Dataset Explorer
          </h2>
          <p className="text-xs md:text-sm text-slate-400 mt-1">
            Reproducible dataset with realistic Gaussian noise used to train and evaluate the model.
          </p>
        </div>

        <button
          onClick={handleDownloadCSV}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold border border-slate-700 transition-all shadow-md self-start sm:self-auto"
        >
          <Download className="w-4 h-4 text-indigo-400" />
          <span>Export CSV</span>
        </button>
      </div>

      {/* Dataset Summary Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="glass-panel rounded-2xl p-4 border border-slate-800">
          <div className="flex items-center gap-2 text-indigo-400 text-xs font-semibold mb-1">
            <Users className="w-4 h-4" />
            <span>Total Records</span>
          </div>
          <div className="text-2xl font-bold text-white">{summary.total_records}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Student sample size</div>
        </div>

        <div className="glass-panel rounded-2xl p-4 border border-slate-800">
          <div className="flex items-center gap-2 text-blue-400 text-xs font-semibold mb-1">
            <Clock className="w-4 h-4" />
            <span>Avg Study Hours</span>
          </div>
          <div className="text-2xl font-bold text-white">{summary.hours_mean} hrs</div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            Range: {summary.hours_min} – {summary.hours_max} hrs
          </div>
        </div>

        <div className="glass-panel rounded-2xl p-4 border border-slate-800">
          <div className="flex items-center gap-2 text-purple-400 text-xs font-semibold mb-1">
            <Award className="w-4 h-4" />
            <span>Avg Exam Marks</span>
          </div>
          <div className="text-2xl font-bold text-white">{summary.marks_mean}%</div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            Range: {summary.marks_min}% – {summary.marks_max}%
          </div>
        </div>

        <div className="glass-panel rounded-2xl p-4 border border-slate-800">
          <div className="flex items-center gap-2 text-emerald-400 text-xs font-semibold mb-1">
            <TrendingUp className="w-4 h-4" />
            <span>Pearson Correlation</span>
          </div>
          <div className="text-2xl font-bold text-white">r = {summary.correlation}</div>
          <div className="text-[11px] text-emerald-400/80 mt-0.5 font-medium">
            Very strong direct relation
          </div>
        </div>
      </div>

      {/* Dataset Table with Search */}
      <div className="glass-panel rounded-2xl p-5 border border-slate-800 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-indigo-400" />
            <h3 className="text-sm font-bold text-white">
              Dataset Records ({filteredData.length} shown)
            </h3>
          </div>

          {/* Search Input */}
          <div className="relative w-full sm:w-64">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search hours or marks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <div className="overflow-x-auto max-h-96 overflow-y-auto">
          <table className="w-full text-left text-xs">
            <thead className="sticky top-0 bg-slate-900 text-slate-300 font-semibold border-b border-slate-700 z-10">
              <tr>
                <th className="py-2.5 px-4"># Student</th>
                <th className="py-2.5 px-4">Hours Studied</th>
                <th className="py-2.5 px-4">Marks Percentage</th>
                <th className="py-2.5 px-4">Visual Scale</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {filteredData.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-2.5 px-4 font-mono text-slate-500">
                    Student #{idx + 1}
                  </td>
                  <td className="py-2.5 px-4 font-semibold text-white">
                    {row.hours_studied} hrs
                  </td>
                  <td className="py-2.5 px-4 font-bold text-indigo-300">
                    {row.marks_percentage}%
                  </td>
                  <td className="py-2.5 px-4 w-44">
                    <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden border border-slate-700/50">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-full rounded-full"
                        style={{ width: `${row.marks_percentage}%` }}
                      />
                    </div>
                  </td>
                </tr>
              ))}
              {filteredData.length === 0 && (
                <tr>
                  <td colSpan={4} className="text-center py-8 text-slate-500">
                    No student records matching "{searchTerm}".
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
