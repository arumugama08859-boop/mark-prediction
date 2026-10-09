"""
backend/app/data.py - Dataset generation, loading, and validation module.
"""

import os
import numpy as np
import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DEFAULT_CSV_PATH = os.path.join(DATA_DIR, "student_marks.csv")


def generate_sample_dataset(csv_path: str = DEFAULT_CSV_PATH, n_samples: int = 40, random_state: int = 42) -> pd.DataFrame:
    """
    Generates a reproducible dataset for student marks prediction.
    """
    np.random.seed(random_state)
    
    hours = np.round(np.random.uniform(1.2, 9.6, size=n_samples), 1)
    hours = np.sort(hours)
    
    noise = np.random.normal(loc=0.0, scale=3.2, size=n_samples)
    raw_marks = 16.0 + (8.5 * hours) + noise
    
    marks = np.clip(raw_marks, 10.0, 99.0)
    marks = np.round(marks, 1)
    
    df = pd.DataFrame({
        "Hours_Studied": hours,
        "Marks_Percentage": marks
    })
    
    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    df.to_csv(csv_path, index=False)
    return df


def load_dataset(csv_path: str = DEFAULT_CSV_PATH) -> pd.DataFrame:
    """
    Loads and validates the student marks dataset.
    """
    if not os.path.exists(csv_path):
        # Also check root data directory if present
        root_csv = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "student_marks.csv")
        if os.path.exists(root_csv):
            df = pd.read_csv(root_csv)
            os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
            df.to_csv(csv_path, index=False)
            return df
        return generate_sample_dataset(csv_path=csv_path)
    
    df = pd.read_csv(csv_path)
    
    required_cols = ["Hours_Studied", "Marks_Percentage"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")
    
    df["Hours_Studied"] = pd.to_numeric(df["Hours_Studied"], errors="coerce")
    df["Marks_Percentage"] = pd.to_numeric(df["Marks_Percentage"], errors="coerce")
    df = df.dropna(subset=required_cols)
    
    return df.sort_values(by="Hours_Studied").reset_index(drop=True)


def get_dataset_summary(df: pd.DataFrame) -> dict:
    """
    Calculates summary statistics and correlation for the dataset.
    """
    correlation = float(df["Hours_Studied"].corr(df["Marks_Percentage"]))
    return {
        "total_records": len(df),
        "hours_mean": round(float(df["Hours_Studied"].mean()), 2),
        "hours_min": round(float(df["Hours_Studied"].min()), 2),
        "hours_max": round(float(df["Hours_Studied"].max()), 2),
        "marks_mean": round(float(df["Marks_Percentage"].mean()), 2),
        "marks_min": round(float(df["Marks_Percentage"].min()), 2),
        "marks_max": round(float(df["Marks_Percentage"].max()), 2),
        "correlation": round(correlation, 4)
    }
