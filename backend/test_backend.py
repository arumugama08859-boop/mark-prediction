"""
backend/test_backend.py - Automated test suite for FastAPI backend endpoints.
"""

import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add app directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from main import app


class TestBackendAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Using TestClient with lifespan context
        cls.client = TestClient(app)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client.__exit__(None, None, None)

    def test_01_root_health(self):
        """Test root endpoint returns healthy status."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    def test_02_predict_valid_inputs(self):
        """Test predictions for various study hours."""
        for hours in [2.0, 5.0, 8.0, 11.0]:
            response = self.client.post("/api/predict", json={"study_hours": hours})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["study_hours"], hours)
            self.assertGreaterEqual(data["predicted_marks"], 0.0)
            self.assertLessEqual(data["predicted_marks"], 100.0)
            self.assertIn("category", data)
            self.assertIn("tip", data)

    def test_03_predict_clamping_upper(self):
        """Test that excessive hours are clamped to 100 with explanation note."""
        response = self.client.post("/api/predict", json={"study_hours": 16.0})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["predicted_marks"], 100.0)
        self.assertTrue(data["is_clamped"])
        self.assertIsNotNone(data["clamping_note"])

    def test_04_predict_invalid_inputs(self):
        """Test negative hours and excessive hours validation."""
        # Negative hours
        resp_neg = self.client.post("/api/predict", json={"study_hours": -5.0})
        self.assertIn(resp_neg.status_code, [400, 422])

        # Exceeding 24 hours
        resp_excess = self.client.post("/api/predict", json={"study_hours": 26.0})
        self.assertIn(resp_excess.status_code, [400, 422])

    def test_05_metrics_endpoint(self):
        """Test evaluation metrics endpoint returns MAE, RMSE, and R2."""
        response = self.client.get("/api/metrics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("mae", data)
        self.assertIn("rmse", data)
        self.assertIn("r2", data)
        self.assertGreater(data["r2"], 0.7)
        self.assertIn("equation", data)
        self.assertGreater(len(data["test_comparison"]), 0)

    def test_06_dataset_endpoint(self):
        """Test dataset endpoint returns summary and records."""
        response = self.client.get("/api/dataset")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("summary", data)
        self.assertIn("data", data)
        self.assertGreater(len(data["data"]), 20)
        self.assertGreater(data["summary"]["correlation"], 0.8)

    def test_07_chart_data_endpoint(self):
        """Test chart data endpoint returns scatter points and regression line."""
        response = self.client.get("/api/chart-data")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("scatter_points", data)
        self.assertIn("regression_line", data)
        self.assertGreater(len(data["scatter_points"]), 20)
        self.assertGreater(len(data["regression_line"]), 10)


if __name__ == "__main__":
    unittest.main()
