import React from 'react';
import { Target, Lightbulb, AlertTriangle, CheckCircle, Info } from 'lucide-react';

export default function PredictionCard({ prediction, isLoading }) {
  if (isLoading) {
    return (
      <div className="glass-panel rounded-3xl p-6 md:p-7 border border-slate-800 shadow-xl flex flex-col items-center justify-center min-h-[320px] text-center">
        <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4 animate-pulse">
          <Target className="w-6 h-6 animate-spin" />
        </div>
        <h3 className="text-base font-semibold text-white mb-1">Calculating Estimation</h3>
        <p className="text-xs text-slate-400 max-w-xs">
          Computing Ordinary Least Squares linear regression inference...
        </p>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="glass-panel rounded-3xl p-6 md:p-7 border border-slate-800 shadow-xl flex flex-col items-center justify-center min-h-[320px] text-center">
        <div className="w-12 h-12 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-400 mb-4">
          <Target className="w-6 h-6" />
        </div>
        <h3 className="text-base font-semibold text-white mb-1">Ready to Predict</h3>
        <p className="text-xs text-slate-400 max-w-xs">
          Adjust the daily study hours on the left and click "Predict Marks" to calculate your estimated score.
        </p>
      </div>
    );
  }

  const {
    study_hours,
    predicted_marks,
    raw_prediction,
    is_clamped,
    category,
    tip,
    clamping_note,
  } = prediction;

  // Badge color mapping
  const badgeColors = {
    emerald: 'bg-emerald-500/15 border-emerald-500/30 text-emerald-300',
    blue: 'bg-blue-500/15 border-blue-500/30 text-blue-300',
    purple: 'bg-purple-500/15 border-purple-500/30 text-purple-300',
    amber: 'bg-amber-500/15 border-amber-500/30 text-amber-300',
    rose: 'bg-rose-500/15 border-rose-500/30 text-rose-300',
  };

  const currentBadgeClass = badgeColors[prediction.badge_color] || badgeColors.blue;

  return (
    <div className="glass-panel rounded-3xl p-6 md:p-7 border border-indigo-500/30 shadow-2xl shadow-indigo-950/40 relative overflow-hidden">
      {/* Background soft glow */}
      <div className="absolute -top-12 -right-12 w-48 h-48 bg-indigo-600/15 rounded-full blur-2xl pointer-events-none" />

      {/* Header with Title and Category Badge */}
      <div className="flex items-center justify-between gap-4 mb-4">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
          Estimated Performance
        </span>
        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${currentBadgeClass}`}>
          {category}
        </span>
      </div>

      {/* Large Score Display */}
      <div className="my-4">
        <div className="flex items-baseline gap-2">
          <span className="text-5xl md:text-6xl font-black bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent tracking-tight">
            {predicted_marks}%
          </span>
          <span className="text-base font-semibold text-slate-400">/ 100%</span>
        </div>
        <p className="text-xs text-slate-400 mt-1">
          Predicted score for <strong className="text-slate-200">{study_hours} daily study hours</strong>
        </p>
      </div>

      {/* Visual Progress Bar */}
      <div className="w-full bg-slate-800/80 rounded-full h-3 mb-5 overflow-hidden p-0.5 border border-slate-700/50">
        <div
          className="h-full rounded-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-all duration-500 ease-out"
          style={{ width: `${Math.min(Math.max(predicted_marks, 0), 100)}%` }}
        />
      </div>

      {/* Academic Recommendation Tip */}
      <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-3.5 mb-4 flex items-start gap-3">
        <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
        <p className="text-xs text-slate-300 leading-relaxed font-normal">
          {tip}
        </p>
      </div>

      {/* Clamping & Extrapolation Notice (if applicable) */}
      {is_clamped && (
        <div className="bg-amber-500/10 border border-amber-500/25 rounded-2xl p-3 mb-3 flex items-start gap-2.5">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <div className="text-[11px] text-amber-200/90 leading-normal">
            <span className="font-semibold block mb-0.5">Physical Boundary Enforcement:</span>
            Raw linear equation output was <strong>{raw_prediction}%</strong>. {clamping_note}
          </div>
        </div>
      )}

      {/* Real Model Integrity Badge */}
      <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-500">
        <span className="flex items-center gap-1.5">
          <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
          Real scikit-learn OLS calculation
        </span>
        <span>Equation: y = mx + c</span>
      </div>
    </div>
  );
}
