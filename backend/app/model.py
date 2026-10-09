"""
backend/app/model.py - Machine Learning Model training, evaluation, and inference.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict, Any


def train_linear_regression(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> Dict[str, Any]:
    """
    Trains a Linear Regression model on student study hours vs marks.
    Enforces strict train-test split to prevent data leakage.
    """
    X = df[["Hours_Studied"]].values
    y = df["Marks_Percentage"].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    slope = float(model.coef_[0])
    intercept = float(model.intercept_)
    equation_str = f"Marks = ({slope:.2f} × Hours) + {intercept:.2f}"
    
    test_comparison = [
        {
            "study_hours": round(float(x[0]), 1),
            "actual_marks": round(float(act), 1),
            "predicted_marks": round(float(prd), 1),
            "absolute_error": round(float(abs(act - prd)), 2)
        }
        for x, act, prd in sorted(zip(X_test, y_test, y_pred), key=lambda item: item[0][0])
    ]
    
    return {
        "model": model,
        "metrics": {
            "mae": round(float(mae), 3),
            "rmse": round(float(rmse), 3),
            "r2": round(float(r2), 4),
            "r2_percentage": round(float(r2) * 100, 2)
        },
        "slope": round(slope, 4),
        "intercept": round(intercept, 4),
        "equation": equation_str,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "test_comparison": test_comparison,
        "X_train": X_train.flatten(),
        "y_train": y_train,
        "X_test": X_test.flatten(),
        "y_test": y_test
    }


def predict_score(model: LinearRegression, hours: float) -> Dict[str, Any]:
    """
    Predicts student marks for given daily study hours.
    Clamps output between 0 and 100 while explaining the implication of extrapolation.
    """
    if hours is None:
        raise ValueError("Please provide a valid study hours value.")
        
    try:
        hours = float(hours)
    except (ValueError, TypeError):
        raise ValueError("Study hours must be a valid numeric value.")
        
    if hours < 0:
        raise ValueError("Study hours cannot be negative. Please enter a value >= 0.")
    if hours > 24:
        raise ValueError("A single day has only 24 hours. Daily study hours cannot exceed 24.")
        
    raw_pred = float(model.predict([[hours]])[0])
    bounded_pred = min(max(raw_pred, 0.0), 100.0)
    is_clamped = (raw_pred < 0.0) or (raw_pred > 100.0)
    
    clamping_note = None
    if is_clamped:
        clamping_note = (
            "Note: The raw linear regression model extrapolated outside realistic exam boundaries (0–100%). "
            "While the predicted value has been clamped to the valid scale for display, "
            "clipping mathematically does not guarantee real-world model accuracy at extreme values."
        )
        
    # Performance categorization
    if bounded_pred >= 85:
        category = "Distinction / Outstanding"
        badge_color = "emerald"
        tip = "Outstanding dedication! Maintain this regular discipline while ensuring sufficient sleep and mental relaxation."
    elif bounded_pred >= 70:
        category = "First Class"
        badge_color = "blue"
        tip = "Solid academic routine! Adding 30 to 45 minutes of problem-solving review can propel you into Distinction territory."
    elif bounded_pred >= 50:
        category = "Second Class"
        badge_color = "purple"
        tip = "Moderate performance. Increasing your daily study focus by 1–2 hours will yield noticeable score gains."
    elif bounded_pred >= 35:
        category = "Pass Class"
        badge_color = "amber"
        tip = "Borderline result. Prioritize core conceptual understanding and dedicated revision to avoid slipping below passing thresholds."
    else:
        category = "Needs Immediate Improvement"
        badge_color = "rose"
        tip = "Low predicted performance. Substantial increase in daily study commitment and concept guidance is strongly advised."
        
    return {
        "study_hours": round(hours, 2),
        "predicted_marks": round(bounded_pred, 2),
        "raw_prediction": round(raw_pred, 2),
        "is_clamped": is_clamped,
        "category": category,
        "badge_color": badge_color,
        "tip": tip,
        "clamping_note": clamping_note
    }


def get_chart_dataset(model_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constructs formatted data points for frontend visualization (Recharts).
    """
    scatter_points = []
    
    # Train samples
    for x, y in zip(model_results["X_train"], model_results["y_train"]):
        scatter_points.append({
            "hours": round(float(x), 2),
            "marks": round(float(y), 2),
            "split": "train"
        })
        
    # Test samples
    for x, y in zip(model_results["X_test"], model_results["y_test"]):
        scatter_points.append({
            "hours": round(float(x), 2),
            "marks": round(float(y), 2),
            "split": "test"
        })
        
    scatter_points = sorted(scatter_points, key=lambda p: p["hours"])
    
    # Regression line points (smooth span across 0 to 12 hours)
    regression_line = []
    x_steps = np.linspace(0, 12, 25)
    for x in x_steps:
        y_val = model_results["slope"] * x + model_results["intercept"]
        y_clamped = min(max(y_val, 0.0), 100.0)
        regression_line.append({
            "hours": round(float(x), 2),
            "predicted_marks": round(float(y_clamped), 2)
        })
        
    return {
        "scatter_points": scatter_points,
        "regression_line": regression_line
    }
