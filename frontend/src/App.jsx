import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import WelcomeBanner from './components/WelcomeBanner';
import StudyHoursForm from './components/StudyHoursForm';
import PredictionCard from './components/PredictionCard';
import RegressionChart from './components/RegressionChart';
import MetricsSection from './components/MetricsSection';
import DatasetTable from './components/DatasetTable';
import AlgorithmGuide from './components/AlgorithmGuide';
import { 
  predictMarks, 
  getMetrics, 
  getDataset, 
  getChartData, 
  checkServerHealth 
} from './services/api';
import { Menu, Sparkles, BarChart3, Database, BrainCircuit } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('predict');
  const [studyHours, setStudyHours] = useState(6.0);
  const [prediction, setPrediction] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isServerOnline, setIsServerOnline] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Load initial backend data
  const loadInitialData = async () => {
    const health = await checkServerHealth();
    setIsServerOnline(health.online);

    if (health.online) {
      // Parallel fetches
      const [metricsRes, datasetRes, chartRes, initialPred] = await Promise.all([
        getMetrics(),
        getDataset(),
        getChartData(),
        predictMarks(studyHours),
      ]);

      if (metricsRes.data) setMetrics(metricsRes.data);
      if (datasetRes.data) setDataset(datasetRes.data);
      if (chartRes.data) setChartData(chartRes.data);
      if (initialPred.data) setPrediction(initialPred.data);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  // Handle Predict button click
  const handlePredict = async () => {
    setIsLoading(true);
    setError(null);

    const { data, error: apiError } = await predictMarks(studyHours);
    setIsLoading(false);

    if (apiError) {
      setError(apiError);
    } else {
      setPrediction(data);
    }
  };

  const navItems = [
    { id: 'predict', label: 'Predictor', icon: Sparkles },
    { id: 'metrics', label: 'Metrics', icon: BarChart3 },
    { id: 'dataset', label: 'Dataset', icon: Database },
    { id: 'guide', label: 'Guide', icon: BrainCircuit },
  ];

  return (
    <div className="flex flex-col lg:flex-row min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500 selection:text-white">
      {/* Sidebar for Desktop */}
      <div className="hidden lg:flex">
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          isServerOnline={isServerOnline}
          onCheckHealth={loadInitialData}
        />
      </div>

      {/* Mobile Top Header */}
      <div className="lg:hidden flex items-center justify-between p-4 bg-slate-900 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center font-bold text-white text-sm">
            M
          </div>
          <span className="font-bold text-sm tracking-tight text-white">
            MarksPredict
          </span>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-[11px]">
            <span
              className={`w-2 h-2 rounded-full ${
                isServerOnline ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'
              }`}
            />
            <span className="text-slate-300 font-medium">
              {isServerOnline ? 'Online' : 'Offline'}
            </span>
          </div>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white"
          >
            <Menu className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden p-4 bg-slate-900 border-b border-slate-800 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  setMobileMenuOpen(false);
                }}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold ${
                  isActive
                    ? 'bg-indigo-600 text-white'
                    : 'text-slate-300 hover:bg-slate-800'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      )}

      {/* Main Content Area */}
      <main className="flex-1 p-4 md:p-8 lg:p-10 max-w-7xl mx-auto w-full overflow-x-hidden">
        {/* Welcome Header */}
        <WelcomeBanner
          metrics={metrics}
          datasetSummary={dataset ? dataset.summary : null}
        />

        {/* Dynamic Views based on activeTab */}
        {activeTab === 'predict' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8 items-start">
              <StudyHoursForm
                studyHours={studyHours}
                setStudyHours={setStudyHours}
                onPredict={handlePredict}
                isLoading={isLoading}
                error={error}
              />
              <PredictionCard
                prediction={prediction}
                isLoading={isLoading}
              />
            </div>

            {/* Regression Fit & Interactive Scatter Chart */}
            <RegressionChart
              chartData={chartData}
              currentPrediction={prediction}
            />
          </div>
        )}

        {activeTab === 'metrics' && (
          <MetricsSection metrics={metrics} />
        )}

        {activeTab === 'dataset' && (
          <DatasetTable dataset={dataset} />
        )}

        {activeTab === 'guide' && (
          <AlgorithmGuide />
        )}

        {/* Global Footer */}
        <footer className="mt-16 pt-6 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-2">
          <span>Student Marks Predictor • Machine Learning Mini-Project</span>
          <span>FastAPI (Python) + React (Vite & Tailwind CSS)</span>
        </footer>
      </main>
    </div>
  );
}
