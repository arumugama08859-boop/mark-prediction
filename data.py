"""
data.py - Dataset generation, loading, and validation module.

This module is responsible for:
1. Creating a reproducible synthetic dataset of student study hours vs marks.
2. Loading and validating dataset integrity.
3. Calculating dataset descriptive statistics.
"""

import os
import numpy as np
import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DEFAULT_CSV_PATH = os.path.join(DATA_DIR, "student_marks.csv")


def generate_sample_dataset(csv_path: str = DEFAULT_CSV_PATH, n_samples: int = 40, random_state: int = 42) -> pd.DataFrame:
    """
    Generates a realistic, reproducible synthetic dataset for student marks prediction.
    
    Parameters:
        csv_path (str): Filepath where the CSV will be saved.
        n_samples (int): Number of student records to generate.
        random_state (int): Fixed seed to ensure exact reproducibility.
        
    Returns:
        pd.DataFrame: Generated dataset containing 'Hours_Studied' and 'Marks_Percentage'.
    """
    np.random.seed(random_state)
    
    # Generate study hours between 1.0 and 9.5 hours
    # Using a combination of uniform distribution and realistic spacing
    hours = np.round(np.random.uniform(1.2, 9.6, size=n_samples), 1)
    hours = np.sort(hours)
    
    # Linear relationship: Base marks + (Rate per hour * Hours) + Natural Random Variance
    # Base marks: ~16 marks minimum baseline knowledge
    # Slope: ~8.6 marks per hour of focused study
    # Noise: Normal distribution with standard deviation of ~3.2 marks
    noise = np.random.normal(loc=0.0, scale=3.2, size=n_samples)
    raw_marks = 16.0 + (8.5 * hours) + noise
    
    # Ensure marks stay within realistic exam boundaries [10.0, 98.0]
    marks = np.clip(raw_marks, 10.0, 99.0)
    marks = np.round(marks, 1)
    
    df = pd.DataFrame({
        "Hours_Studied": hours,
        "Marks_Percentage": marks
    })
    
    # Ensure target directory exists
    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    
    # Save to CSV
    df.to_csv(csv_path, index=False)
    return df


def load_dataset(csv_path: str = DEFAULT_CSV_PATH) -> pd.DataFrame:
    """
    Loads and validates the student marks dataset.
    If the file does not exist, it automatically generates a reproducible dataset.
    
    Parameters:
        csv_path (str): Filepath to load.
        
    Returns:
        pd.DataFrame: Cleaned and validated dataset.
        
    Raises:
        ValueError: If required columns are missing or data is malformed.
    """
    if not os.path.exists(csv_path):
        # Auto-create reproducible dataset if missing
        return generate_sample_dataset(csv_path=csv_path)
    
    df = pd.read_csv(csv_path)
    
    # Validate columns
    required_cols = ["Hours_Studied", "Marks_Percentage"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")
    
    # Handle missing / null values
    if df[required_cols].isnull().any().any():
        df = df.dropna(subset=required_cols)
        
    # Ensure numeric types
    df["Hours_Studied"] = pd.to_numeric(df["Hours_Studied"], errors="coerce")
    df["Marks_Percentage"] = pd.to_numeric(df["Marks_Percentage"], errors="coerce")
    df = df.dropna(subset=required_cols)
    
    # Sort for cleaner presentation
    df = df.sort_values(by="Hours_Studied").reset_index(drop=True)
    return df


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


if __name__ == "__main__":
    data = generate_sample_dataset()
    print(f"Sample dataset generated successfully with {len(data)} records.")
    print(data.head())
    print("Summary:", get_dataset_summary(data))
