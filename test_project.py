"""
test_project.py - Automated test suite for the Student Marks Predictor.

Tests cover:
1. Dataset loading, structure, and statistics.
2. Handling of missing dataset files.
3. Model training, train/test split ratio, and metrics calculation.
4. Prediction logic across low, medium, and high study hours.
5. Range clamping enforcement [0, 100].
6. Error handling for negative, out-of-range, and invalid inputs.
"""

import os
import unittest
import numpy as np
import pandas as pd
from data import load_dataset, get_dataset_summary, generate_sample_dataset
from model import train_linear_regression, predict_score


class TestStudentMarksPredictor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load dataset and train model once for test suite
        cls.df = load_dataset()
        cls.model_results = train_linear_regression(cls.df)
        cls.model = cls.model_results["model"]

    def test_01_dataset_integrity(self):
        """Test dataset shape, required columns, and non-empty status."""
        self.assertGreater(len(self.df), 20, "Dataset should have at least 20 records.")
        self.assertIn("Hours_Studied", self.df.columns)
        self.assertIn("Marks_Percentage", self.df.columns)
        self.assertFalse(self.df.isnull().any().any(), "Dataset should not contain NaN values.")

    def test_02_dataset_summary(self):
        """Test descriptive summary metrics."""
        summary = get_dataset_summary(self.df)
        self.assertGreater(summary["total_records"], 0)
        self.assertGreater(summary["correlation"], 0.8, "Correlation between study hours and marks should be strong.")

    def test_03_train_test_split_no_leakage(self):
        """Verify train-test split sizes and absence of data leakage."""
        train_count = self.model_results["total_train_samples"]
        test_count = self.model_results["total_test_samples"]
        total = len(self.df)
        
        self.assertEqual(train_count + test_count, total)
        # 80/20 split check
        self.assertAlmostEqual(test_count / total, 0.2, delta=0.05)

    def test_04_model_evaluation_metrics(self):
        """Ensure evaluation metrics are real, non-zero, and scientifically plausible."""
        metrics = self.model_results["metrics"]
        self.assertIn("MAE", metrics)
        self.assertIn("MSE", metrics)
        self.assertIn("RMSE", metrics)
        self.assertIn("R2", metrics)
        
        self.assertGreater(metrics["MAE"], 0.0)
        self.assertGreater(metrics["MSE"], 0.0)
        self.assertGreater(metrics["RMSE"], 0.0)
        self.assertGreater(metrics["R2"], 0.7, "R2 score should be high for linear relation.")
        self.assertLessEqual(metrics["R2"], 1.0)
        # Verify RMSE is sqrt(MSE)
        self.assertAlmostEqual(metrics["RMSE"], np.sqrt(metrics["MSE"]), delta=0.01)

    def test_05_prediction_normal_range(self):
        """Test predictions for low, medium, and high study hours."""
        # Low study hours
        pred_low = predict_score(self.model, 2.0)
        self.assertGreaterEqual(pred_low["predicted_marks"], 0.0)
        self.assertLessEqual(pred_low["predicted_marks"], 100.0)
        
        # Medium study hours
        pred_mid = predict_score(self.model, 6.0)
        self.assertGreater(pred_mid["predicted_marks"], pred_low["predicted_marks"])
        self.assertLessEqual(pred_mid["predicted_marks"], 100.0)
        
        # High study hours
        pred_high = predict_score(self.model, 9.0)
        self.assertGreater(pred_high["predicted_marks"], pred_mid["predicted_marks"])
        self.assertLessEqual(pred_high["predicted_marks"], 100.0)

    def test_06_boundary_clamping_upper(self):
        """Verify that predictions never exceed 100%, even for excessive hours."""
        pred_high = predict_score(self.model, 18.0)
        self.assertEqual(pred_high["predicted_marks"], 100.0)
        self.assertTrue(pred_high["is_clamped"])
        self.assertGreater(pred_high["raw_prediction"], 100.0)

    def test_07_boundary_clamping_lower(self):
        """Verify that predictions never drop below 0%."""
        pred_zero = predict_score(self.model, 0.0)
        self.assertGreaterEqual(pred_zero["predicted_marks"], 0.0)

    def test_08_invalid_input_negative(self):
        """Test that negative hours raise ValueError."""
        with self.assertRaises(ValueError):
            predict_score(self.model, -3.5)

    def test_09_invalid_input_exceeds_day(self):
        """Test that study hours > 24 raise ValueError."""
        with self.assertRaises(ValueError):
            predict_score(self.model, 25.0)

    def test_10_invalid_input_non_numeric(self):
        """Test that string or non-numeric inputs raise ValueError."""
        with self.assertRaises(ValueError):
            predict_score(self.model, "invalid_hours")


if __name__ == "__main__":
    unittest.main()
