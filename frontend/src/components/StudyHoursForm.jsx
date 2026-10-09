import React from 'react';
import { Clock, Calculator, Loader2, AlertCircle } from 'lucide-react';

export default function StudyHoursForm({
  studyHours,
  setStudyHours,
  onPredict,
  isLoading,
  error,
}) {
  const presets = [2, 5, 8, 11];

  const handleSliderChange = (e) => {
    setStudyHours(parseFloat(e.target.value));
  };

  const handleInputChange = (e) => {
    const val = e.target.value;
    if (val === '') {
      setStudyHours(0);
      return;
    }
    const parsed = parseFloat(val);
    if (!isNaN(parsed)) {
      setStudyHours(parsed);
    }
  };

  const handlePresetClick = (hours) => {
    setStudyHours(hours);
  };

  return (
    <div className="glass-panel rounded-3xl p-6 md:p-7 border border-slate-800 shadow-xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
          <Clock className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-white">Daily Study Commitment</h2>
          <p className="text-xs text-slate-400">Adjust the slider or pick a preset to forecast marks</p>
        </div>
      </div>

      {/* Main Slider & Number Input */}
      <div className="space-y-6">
        <div>
          <div className="flex justify-between items-center mb-3">
            <label className="text-sm font-semibold text-slate-300">
              Hours Studied per Day:
            </label>
            <div className="flex items-center gap-2">
              <input
                type="number"
                min="0"
                max="24"
                step="0.25"
                value={studyHours}
                onChange={handleInputChange}
                className="w-20 px-3 py-1.5 bg-slate-800/80 border border-slate-700 rounded-lg text-right font-bold text-indigo-300 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <span className="text-xs text-slate-400 font-medium">hrs</span>
            </div>
          </div>

          {/* Range Slider */}
          <input
            type="range"
            min="0"
            max="14"
            step="0.25"
            value={studyHours}
            onChange={handleSliderChange}
            className="w-full h-2.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500 hover:accent-indigo-400 transition-all"
          />

          <div className="flex justify-between text-[11px] text-slate-400 mt-1.5 px-0.5">
            <span>0 hrs</span>
            <span>3.5 hrs</span>
            <span>7 hrs</span>
            <span>10.5 hrs</span>
            <span>14 hrs</span>
          </div>
        </div>

        {/* Quick Presets */}
        <div>
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2.5">
            Quick-Select Presets
          </span>
          <div className="grid grid-cols-4 gap-2.5">
            {presets.map((hours) => {
              const isSelected = studyHours === hours;
              return (
                <button
                  key={hours}
                  type="button"
                  onClick={() => handlePresetClick(hours)}
                  className={`py-2 px-3 rounded-xl text-xs font-bold transition-all duration-200 border ${
                    isSelected
                      ? 'bg-gradient-to-r from-blue-600 to-indigo-600 border-indigo-400 text-white shadow-md shadow-indigo-600/30'
                      : 'bg-slate-800/60 border-slate-700/60 text-slate-300 hover:bg-slate-800 hover:text-white hover:border-slate-600'
                  }`}
                >
                  {hours} hrs
                </button>
              );
            })}
          </div>
        </div>

        {/* Error message */}
        {error && (
          <div className="flex items-start gap-2.5 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Predict Marks Button */}
        <button
          type="button"
          onClick={onPredict}
          disabled={isLoading}
          className="w-full py-3.5 px-6 rounded-2xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:via-indigo-500 hover:to-purple-500 text-white font-bold text-sm tracking-wide shadow-lg shadow-indigo-600/30 hover:shadow-indigo-600/50 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-150 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Analyzing with Model...</span>
            </>
          ) : (
            <>
              <Calculator className="w-4 h-4" />
              <span>Predict Marks</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
