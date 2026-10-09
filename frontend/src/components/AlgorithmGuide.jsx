import React from 'react';
import { BrainCircuit, Split, ShieldCheck, Scale, HelpCircle } from 'lucide-react';

export default function AlgorithmGuide() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl md:text-2xl font-bold text-white tracking-tight">
          How Machine Learning Predicts Student Marks
        </h2>
        <p className="text-xs md:text-sm text-slate-400 mt-1">
          A clear, beginner-friendly guide to Linear Regression, model evaluation, and best practices.
        </p>
      </div>

      {/* Grid of conceptual cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Card 1: Linear Regression Basics */}
        <div className="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl space-y-3">
          <div className="flex items-center gap-2.5 text-blue-400 font-bold text-sm">
            <BrainCircuit className="w-5 h-5" />
            <span>1. What is Simple Linear Regression?</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Simple Linear Regression is a supervised learning algorithm that finds the mathematical
            straight line best modeling the relationship between an independent input feature (<strong>Study Hours</strong>)
            and a continuous target outcome (<strong>Exam Marks</strong>).
          </p>
          <div className="bg-slate-900 border border-slate-700/80 rounded-xl p-3 font-mono text-center text-indigo-300 text-sm font-bold">
            y = (m × x) + c
          </div>
          <ul className="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
            <li><strong>y (Dependent Target):</strong> Predicted exam mark.</li>
            <li><strong>x (Independent Feature):</strong> Daily study hours.</li>
            <li><strong>m (Slope / Weight):</strong> Marks gained per additional study hour.</li>
            <li><strong>c (Y-Intercept / Bias):</strong> Baseline score with 0 hours studied.</li>
          </ul>
        </div>

        {/* Card 2: Ordinary Least Squares (OLS) */}
        <div className="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl space-y-3">
          <div className="flex items-center gap-2.5 text-purple-400 font-bold text-sm">
            <Scale className="w-5 h-5" />
            <span>2. How OLS Finds the Best Line</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            The scikit-learn model calculates the slope and intercept by minimizing the
            <strong> Residual Sum of Squares (RSS)</strong>—the sum of squared vertical gaps
            between the actual student scores and the fitted line:
          </p>
          <div className="bg-slate-900 border border-slate-700/80 rounded-xl p-3 font-mono text-center text-purple-300 text-sm font-bold">
            Minimize: ∑ (Actual - Predicted)²
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Squaring the errors guarantees positive distances and strongly penalizes larger prediction deviations.
          </p>
        </div>

        {/* Card 3: Avoiding Data Leakage */}
        <div className="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl space-y-3">
          <div className="flex items-center gap-2.5 text-emerald-400 font-bold text-sm">
            <Split className="w-5 h-5" />
            <span>3. Zero Data Leakage (80/20 Split)</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            In machine learning, testing a model on the exact data used for training gives false confidence (data leakage).
            Our system strictly partitions data into:
          </p>
          <div className="grid grid-cols-2 gap-2 text-center text-xs">
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-2.5">
              <span className="font-bold text-blue-300 block">Training Set (80%)</span>
              <span className="text-[11px] text-slate-400">Used solely to fit weights</span>
            </div>
            <div className="bg-purple-500/10 border border-purple-500/20 rounded-xl p-2.5">
              <span className="font-bold text-purple-300 block">Testing Set (20%)</span>
              <span className="text-[11px] text-slate-400">Hidden until evaluation</span>
            </div>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            All metrics (MAE, RMSE, R²) are calculated exclusively against the 20% unseen test records.
          </p>
        </div>

        {/* Card 4: Clamping [0, 100] & Physical Limits */}
        <div className="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl space-y-3">
          <div className="flex items-center gap-2.5 text-amber-400 font-bold text-sm">
            <ShieldCheck className="w-5 h-5" />
            <span>4. Boundary Clamping [0, 100%]</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Pure mathematical lines extend to infinity in both directions. For instance, entering 16 hours might mathematically
            output 150 marks!
          </p>
          <div className="bg-slate-900 border border-slate-700/80 rounded-xl p-3 font-mono text-center text-amber-300 text-xs font-bold">
            final_pred = min(max(raw_pred, 0.0), 100.0)
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Our API clamps values into [0, 100] and flags when clipping occurred. Note that clamping enforces physical feasibility,
            though linear extrapolation at extremes is not guaranteed accurate.
          </p>
        </div>
      </div>

      {/* Viva Voce Questions Section */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800 shadow-xl">
        <div className="flex items-center gap-2 text-indigo-400 font-bold text-sm mb-4">
          <HelpCircle className="w-5 h-5" />
          <span>Frequently Asked Viva Voce & Evaluation Questions</span>
        </div>

        <div className="space-y-4 text-xs">
          <div className="p-3.5 bg-slate-900/60 rounded-xl border border-slate-800">
            <strong className="text-white block mb-1">
              Q: What is the difference between MAE and RMSE?
            </strong>
            <span className="text-slate-300 leading-relaxed block">
              A: MAE (Mean Absolute Error) treats all errors linearly. RMSE (Root Mean Squared Error) squares the errors before averaging, penalizing large outlier errors much more heavily.
            </span>
          </div>

          <div className="p-3.5 bg-slate-900/60 rounded-xl border border-slate-800">
            <strong className="text-white block mb-1">
              Q: What does an R² score of 0.98 mean?
            </strong>
            <span className="text-slate-300 leading-relaxed block">
              A: It indicates that 98% of the total variance in student examination marks is predictable from the hours they spent studying.
            </span>
          </div>

          <div className="p-3.5 bg-slate-900/60 rounded-xl border border-slate-800">
            <strong className="text-white block mb-1">
              Q: Why is Linear Regression suitable for this problem?
            </strong>
            <span className="text-slate-300 leading-relaxed block">
              A: Because exam marks are a continuous numerical variable (regression task) that exhibits a strong direct positive relationship with disciplined daily study hours.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
