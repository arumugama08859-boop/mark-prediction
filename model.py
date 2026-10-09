"""
model.py - Machine Learning Model training, evaluation, and prediction.

This module implements the core Machine Learning workflow using scikit-learn:
1. Feature extraction and train-test splitting (avoiding data leakage).
2. Model training using Ordinary Least Squares Linear Regression.
3. Model evaluation using MAE, MSE, RMSE, and R² score.
4. Safe mark prediction with physical range clamping [0, 100].
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
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'Hours_Studied' and 'Marks_Percentage'.
        test_size (float): Fraction of data reserved for testing (default: 0.2, i.e., 20%).
        random_state (int): Seed for reproducible train/test split.
        
    Returns:
        dict: Complete dictionary containing trained model, evaluation metrics,
              coefficients, and test comparison data.
    """
    # 1. Feature matrix (X: 2D) and Target vector (y: 1D)
    X = df[["Hours_Studied"]].values
    y = df["Marks_Percentage"].values
    
    # 2. Train-Test Split (Strictly avoids data leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # 3. Model Initialization and Training
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 4. Predictions on unseen Test Data
    y_pred = model.predict(X_test)
    
    # 5. Model Evaluation Metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # 6. Model Parameters
    slope = float(model.coef_[0])
    intercept = float(model.intercept_)
    equation_str = f"Marks = ({slope:.2f} × Hours) + {intercept:.2f}"
    
    # 7. Test Set Comparison Table
    test_comparison = pd.DataFrame({
        "Study Hours": X_test.flatten(),
        "Actual Marks (%)": np.round(y_test, 1),
        "Predicted Marks (%)": np.round(y_pred, 1),
        "Absolute Error": np.round(np.abs(y_test - y_pred), 2)
    }).sort_values(by="Study Hours").reset_index(drop=True)
    
    return {
        "model": model,
        "metrics": {
            "MAE": round(float(mae), 3),
            "MSE": round(float(mse), 3),
            "RMSE": round(float(rmse), 3),
            "R2": round(float(r2), 4),
            "R2_Percentage": round(float(r2) * 100, 2)
        },
        "slope": round(slope, 4),
        "intercept": round(intercept, 4),
        "equation": equation_str,
        "train_data": {
            "X": X_train.flatten(),
            "y": y_train
        },
        "test_data": {
            "X": X_test.flatten(),
            "y": y_test,
            "y_pred": y_pred
        },
        "test_comparison": test_comparison,
        "total_train_samples": len(X_train),
        "total_test_samples": len(X_test)
    }


def predict_score(model: LinearRegression, hours: float) -> Dict[str, Any]:
    """
    Predicts student marks for given study hours, enforcing range constraints [0, 100].
    
    Parameters:
        model (LinearRegression): Trained scikit-learn model.
        hours (float): Number of daily study hours.
        
    Returns:
        dict: Detailed prediction results with categorization and guidance.
        
    Raises:
        ValueError: If hours input is invalid (negative or > 24 hours/day).
    """
    if hours is None:
        raise ValueError("Please enter a valid number for study hours.")
    
    if not isinstance(hours, (int, float)):
        try:
            hours = float(hours)
        except (ValueError, TypeError):
            raise ValueError("Study hours must be a valid numeric value.")
            
    if hours < 0:
        raise ValueError("Study hours cannot be negative. Please enter 0 or more hours.")
        
    if hours > 24:
        raise ValueError("A day has only 24 hours! Daily study hours cannot exceed 24.")
    
    # Model inference
    raw_pred = float(model.predict([[hours]])[0])
    
    # Real-world constraint: Marks must lie in [0, 100]
    bounded_pred = min(max(raw_pred, 0.0), 100.0)
    is_clamped = (raw_pred < 0.0) or (raw_pred > 100.0)
    
    # Categorization and pedagogical advice
    if bounded_pred >= 85:
        category = "Distinction / Outstanding"
        badge_color = "#10B981"  # Emerald green
        tip = "🌟 Excellent study routine! Maintain this consistent dedication while ensuring adequate rest and breaks."
    elif bounded_pred >= 70:
        category = "First Class"
        badge_color = "#3B82F6"  # Blue
        tip = "🎯 Strong performance! Adding 30-45 minutes of revision or practice problem-solving could boost you into Distinction."
    elif bounded_pred >= 50:
        category = "Second Class"
        badge_color = "#8B5CF6"  # Purple
        tip = "📚 Decent progress, but there is significant room for improvement. Increasing focused study time by 1-2 hours will make a big difference."
    elif bounded_pred >= 35:
        category = "Pass Class"
        badge_color = "#F59E0B"  # Amber
        tip = "⚠️ You are on the borderline. Dedicating more daily study hours and seeking concept clarification from teachers is strongly recommended."
    else:
        category = "Needs Immediate Improvement"
        badge_color = "#EF4444"  # Red
        tip = "🚨 Low predicted score. More daily study hours, consistent revision, and active practice are critical to passing comfortably."
        
    return {
        "hours": round(hours, 2),
        "predicted_marks": round(bounded_pred, 2),
        "raw_prediction": round(raw_pred, 2),
        "is_clamped": is_clamped,
        "category": category,
        "badge_color": badge_color,
        "tip": tip
    }


if __name__ == "__main__":
    from data import load_dataset
    df = load_dataset()
    results = train_linear_regression(df)
    print("Equation:", results["equation"])
    print("Metrics:", results["metrics"])
    pred = predict_score(results["model"], 6.5)
    print("Prediction for 6.5 hours:", pred)
