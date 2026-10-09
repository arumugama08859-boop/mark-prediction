import React from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceDot,
  ReferenceLine
} from 'recharts';
import { LineChart as ChartIcon, Sparkles } from 'lucide-react';

export default function RegressionChart({ chartData, currentPrediction }) {
  if (!chartData) {
    return (
      <div className="glass-panel rounded-3xl p-6 border border-slate-800 shadow-xl flex items-center justify-center h-80">
        <span className="text-xs text-slate-400">Loading regression visualizer...</span>
      </div>
    );
  }

  const { scatter_points = [], regression_line = [] } = chartData;

  // Filter training vs testing scatter points
  const trainPoints = scatter_points.filter((p) => p.split === 'train');
  const testPoints = scatter_points.filter((p) => p.split === 'test');

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-900/95 border border-slate-700 p-3 rounded-xl shadow-xl text-xs backdrop-blur-md">
          <div className="font-bold text-white mb-1">
            Study Hours: <span className="text-indigo-400">{data.hours} hrs</span>
          </div>
          {data.marks !== undefined && (
            <div className="text-slate-300">
              Exam Mark:{' '}
              <span className="font-semibold text-emerald-400">{data.marks}%</span>
              <span className="text-slate-500 text-[10px] ml-1">({data.split} set)</span>
            </div>
          )}
          {data.predicted_marks !== undefined && (
            <div className="text-slate-300">
              Line Prediction:{' '}
              <span className="font-semibold text-purple-400">{data.predicted_marks}%</span>
            </div>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-panel rounded-3xl p-6 md:p-7 border border-slate-800 shadow-xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
            <ChartIcon className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Linear Regression Relationship</h2>
            <p className="text-xs text-slate-400">Actual student samples vs OLS fitted regression line</p>
          </div>
        </div>

        {currentPrediction && (
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-xs text-indigo-300 self-start sm:self-auto">
            <Sparkles className="w-3.5 h-3.5 text-yellow-400" />
            <span>
              Your Input: <strong>{currentPrediction.study_hours}h → {currentPrediction.predicted_marks}%</strong>
            </span>
          </div>
        )}
      </div>

      {/* Recharts Composed Container */}
      <div className="w-full h-80 md:h-96">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart
            margin={{ top: 20, right: 20, bottom: 20, left: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
            <XAxis
              type="number"
              dataKey="hours"
              name="Hours"
              unit="h"
              domain={[0, 14]}
              tick={{ fill: '#94a3b8', fontSize: 11 }}
              tickLine={{ stroke: '#475569' }}
              axisLine={{ stroke: '#475569' }}
              label={{
                value: 'Daily Study Hours',
                position: 'insideBottom',
                offset: -10,
                fill: '#94a3b8',
                fontSize: 12,
              }}
            />
            <YAxis
              type="number"
              dataKey="marks"
              name="Marks"
              unit="%"
              domain={[0, 105]}
              tick={{ fill: '#94a3b8', fontSize: 11 }}
              tickLine={{ stroke: '#475569' }}
              axisLine={{ stroke: '#475569' }}
              label={{
                value: 'Marks (%)',
                angle: -90,
                position: 'insideLeft',
                offset: 15,
                fill: '#94a3b8',
                fontSize: 12,
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              verticalAlign="top"
              align="right"
              wrapperStyle={{ paddingBottom: '12px', fontSize: '12px' }}
            />

            {/* Regression Line */}
            <Line
              data={regression_line}
              dataKey="predicted_marks"
              name="Fitted OLS Line"
              stroke="#818cf8"
              strokeWidth={3}
              dot={false}
              isAnimationActive={false}
            />

            {/* Training Samples Scatter */}
            <Scatter
              data={trainPoints}
              dataKey="marks"
              name="Training Data (80%)"
              fill="#3b82f6"
              stroke="#1e40af"
              strokeWidth={1}
            />

            {/* Testing Samples Scatter */}
            <Scatter
              data={testPoints}
              dataKey="marks"
              name="Testing Data (20%)"
              fill="#c084fc"
              stroke="#7e22ce"
              strokeWidth={1}
            />

            {/* Active User Prediction Marker */}
            {currentPrediction && (
              <>
                <ReferenceLine
                  x={currentPrediction.study_hours}
                  stroke="#fbbf24"
                  strokeDasharray="3 3"
                  opacity={0.7}
                />
                <ReferenceLine
                  y={currentPrediction.predicted_marks}
                  stroke="#fbbf24"
                  strokeDasharray="3 3"
                  opacity={0.7}
                />
                <ReferenceDot
                  x={currentPrediction.study_hours}
                  y={currentPrediction.predicted_marks}
                  r={8}
                  fill="#f59e0b"
                  stroke="#ffffff"
                  strokeWidth={2}
                  name="Your Prediction"
                />
              </>
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
