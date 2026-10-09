import React from 'react';
import { 
  Award, 
  BarChart2, 
  Activity, 
  Percent, 
  Sliders, 
  CheckCircle2, 
  Code2 
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  Cell
} from 'recharts';

export default function MetricsSection({ metrics }) {
  if (!metrics) {
    return (
      <div className="glass-panel rounded-3xl p-8 border border-slate-800 shadow-xl text-center">
        <p className="text-sm text-slate-400">Loading model evaluation metrics...</p>
      </div>
    );
  }

  const {
    mae,
    rmse,
    r2,
    r2_percentage,
    slope,
    intercept,
    equation,
    train_samples,
    test_samples,
    test_comparison = [],
  } = metrics;

  // Prepare residual errors for BarChart
  const residualData = test_comparison.map((item, idx) => ({
    name: `#${idx + 1}`,
    hours: item.study_hours,
    actual: item.actual_marks,
    predicted: item.predicted_marks,
    residual: parseFloat((item.actual_marks - item.predicted_marks).toFixed(2)),
  }));

  return (
    <div className="space-y-6">
      {/* Metrics Header */}
      <div>
        <h2 className="text-xl md:text-2xl font-bold text-white tracking-tight">
          Model Evaluation & Performance Metrics
        </h2>
        <p className="text-xs md:text-sm text-slate-400 mt-1">
          Strictly calculated on the <strong>{test_samples} unseen test records (20%)</strong> to avoid data leakage.
        </p>
      </div>

      {/* Top 4 Metrics Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* R2 Card */}
        <div className="glass-panel glass-panel-hover rounded-2xl p-5 border border-slate-800">
          <div className="flex items-center justify-between text-indigo-400 mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              R² Score (Accuracy)
            </span>
            <Award className="w-5 h-5" />
          </div>
          <div className="text-3xl font-extrabold text-white mb-1">
            {r2}
          </div>
          <div className="text-xs text-indigo-300 font-medium">
            {r2_percentage}% variance explained
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Measures how well study hours account for variations in marks.
          </p>
        </div>

        {/* MAE Card */}
        <div className="glass-panel glass-panel-hover rounded-2xl p-5 border border-slate-800">
          <div className="flex items-center justify-between text-blue-400 mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Mean Abs Error (MAE)
            </span>
            <Activity className="w-5 h-5" />
          </div>
          <div className="text-3xl font-extrabold text-white mb-1">
            ±{mae}%
          </div>
          <div className="text-xs text-blue-300 font-medium">
            Average test deviation
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Average absolute gap between truth and prediction.
          </p>
        </div>

        {/* RMSE Card */}
        <div className="glass-panel glass-panel-hover rounded-2xl p-5 border border-slate-800">
          <div className="flex items-center justify-between text-purple-400 mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Root MSE (RMSE)
            </span>
            <BarChart2 className="w-5 h-5" />
          </div>
          <div className="text-3xl font-extrabold text-white mb-1">
            {rmse}%
          </div>
          <div className="text-xs text-purple-300 font-medium">
            Standard deviation of residuals
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Penalizes larger outliers more heavily than MAE.
          </p>
        </div>

        {/* Coefficients Card */}
        <div className="glass-panel glass-panel-hover rounded-2xl p-5 border border-slate-800">
          <div className="flex items-center justify-between text-emerald-400 mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Slope (m) & Bias (c)
            </span>
            <Sliders className="w-5 h-5" />
          </div>
          <div className="text-2xl font-extrabold text-white mb-1">
            m = +{slope}
          </div>
          <div className="text-xs text-emerald-300 font-medium">
            Intercept c = {intercept}%
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Each added study hour gains ~{slope}% in exam marks.
          </p>
        </div>
      </div>

      {/* Learned Mathematical Equation Box */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/60 to-slate-900 border border-indigo-500/30 rounded-2xl p-5 shadow-lg">
        <div className="flex items-center gap-2 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-2">
          <Code2 className="w-4 h-4" />
          <span>Learned OLS Regression Formula</span>
        </div>
        <div className="font-mono text-lg md:text-xl font-bold text-white bg-slate-950/80 px-4 py-3 rounded-xl border border-slate-800 inline-block">
          {equation}
        </div>
        <p className="text-xs text-slate-400 mt-2">
          Trained on <strong>{train_samples} student records (80%)</strong>. No artificial or hardcoded formulas.
        </p>
      </div>

      {/* Grid: Test Comparison Table & Residual Bar Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Test Set Comparison Table */}
        <div className="glass-panel rounded-2xl p-5 border border-slate-800 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white">
              Unseen Test Set Validation (N={test_samples})
            </h3>
            <span className="text-[11px] text-emerald-400 font-semibold flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> Zero Data Leakage
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-800/80 text-slate-300 font-semibold border-b border-slate-700">
                <tr>
                  <th className="py-2.5 px-3 rounded-l-lg">Hours</th>
                  <th className="py-2.5 px-3">Actual Marks</th>
                  <th className="py-2.5 px-3">Predicted</th>
                  <th className="py-2.5 px-3 rounded-r-lg text-right">Error</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {test_comparison.map((row, i) => (
                  <tr key={i} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-2.5 px-3 font-semibold text-white">
                      {row.study_hours} hrs
                    </td>
                    <td className="py-2.5 px-3 text-emerald-400 font-medium">
                      {row.actual_marks}%
                    </td>
                    <td className="py-2.5 px-3 text-purple-400 font-medium">
                      {row.predicted_marks}%
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-slate-400">
                      ±{row.absolute_error}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Residuals Bar Chart */}
        <div className="glass-panel rounded-2xl p-5 border border-slate-800 shadow-xl">
          <h3 className="text-sm font-bold text-white mb-1">
            Residual Errors (Actual − Predicted)
          </h3>
          <p className="text-[11px] text-slate-400 mb-4">
            Positive error (green) means student scored higher than line; negative (rose) means lower.
          </p>

          <div className="w-full h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={residualData} margin={{ top: 10, right: 10, bottom: 20, left: -10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
                <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 10 }} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} unit="%" />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const d = payload[0].payload;
                      return (
                        <div className="bg-slate-900 border border-slate-700 p-2.5 rounded-lg text-xs shadow-xl">
                          <div className="font-bold text-white">Student {d.name} ({d.hours} hrs)</div>
                          <div className="text-slate-300">Actual: {d.actual}%</div>
                          <div className="text-slate-300">Predicted: {d.predicted}%</div>
                          <div className="text-indigo-400 font-semibold">Residual: {d.residual}%</div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <ReferenceLine y={0} stroke="#64748b" strokeWidth={1} />
                <Bar dataKey="residual" radius={[4, 4, 0, 0]}>
                  {residualData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.residual >= 0 ? '#10b981' : '#f43f5e'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
