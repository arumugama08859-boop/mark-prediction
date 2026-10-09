/**
 * api.js - Centralized API service for communicating with the FastAPI backend.
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Predict student marks based on daily study hours.
 * @param {number} studyHours
 * @returns {Promise<Object>}
 */
export async function predictMarks(studyHours) {
  try {
    const response = await client.post('/api/predict', {
      study_hours: parseFloat(studyHours),
    });
    return { data: response.data, error: null };
  } catch (err) {
    const message =
      err.response?.data?.detail ||
      (err.code === 'ECONNABORTED'
        ? 'Request timed out. Please check if the backend server is running.'
        : err.message || 'Failed to connect to prediction server.');
    return { data: null, error: message };
  }
}

/**
 * Fetch model evaluation metrics (MAE, RMSE, R2, learned equation, test comparisons).
 * @returns {Promise<Object>}
 */
export async function getMetrics() {
  try {
    const response = await client.get('/api/metrics');
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: err.response?.data?.detail || err.message };
  }
}

/**
 * Fetch dataset records and summary statistics.
 * @returns {Promise<Object>}
 */
export async function getDataset() {
  try {
    const response = await client.get('/api/dataset');
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: err.response?.data?.detail || err.message };
  }
}

/**
 * Fetch scatter data points and regression line for Recharts visualization.
 * @returns {Promise<Object>}
 */
export async function getChartData() {
  try {
    const response = await client.get('/api/chart-data');
    return { data: response.data, error: null };
  } catch (err) {
    return { data: null, error: err.response?.data?.detail || err.message };
  }
}

/**
 * Check backend connection status.
 */
export async function checkServerHealth() {
  try {
    const response = await client.get('/');
    return { online: response.status === 200, data: response.data };
  } catch {
    return { online: false, data: null };
  }
}
