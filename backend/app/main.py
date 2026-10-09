"""
backend/app/main.py - FastAPI application for Student Marks Predictor.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys

# Ensure backend package can import its local modules
sys.path.insert(0, os.path.dirname(__file__))

from data import load_dataset, get_dataset_summary
from model import train_linear_regression, predict_score, get_chart_dataset
from schemas import (
    PredictionRequest,
    PredictionResponse,
    MetricsResponse,
    DatasetResponse,
    ChartDataResponse
)

# Global state for cached model and dataset
state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load dataset and fit ML model
    print("[FastAPI] Initializing dataset and training Machine Learning model...")
    df = load_dataset()
    results = train_linear_regression(df)
    summary = get_dataset_summary(df)
    chart_data = get_chart_dataset(results)
    
    state["df"] = df
    state["model_results"] = results
    state["summary"] = summary
    state["chart_data"] = chart_data
    print(f"[FastAPI] Model successfully trained with R²={results['metrics']['r2']:.4f}")
    yield
    # Shutdown
    state.clear()


app = FastAPI(
    title="Student Marks Predictor API",
    description="Machine Learning REST API for predicting student exam marks using Linear Regression.",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for local React development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    """Root health and status endpoint."""
    return {
        "status": "healthy",
        "app": "Student Marks Predictor API",
        "version": "2.0.0",
        "endpoints": [
            "/api/predict",
            "/api/metrics",
            "/api/dataset",
            "/api/chart-data"
        ]
    }


@app.post("/api/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    """
    Predicts student marks for given daily study hours.
    Validates range [0, 24] and clamps predicted marks between [0, 100].
    """
    if "model_results" not in state:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Machine learning model is not ready."
        )
    
    try:
        prediction_result = predict_score(
            state["model_results"]["model"],
            payload.study_hours
        )
        return PredictionResponse(**prediction_result)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while computing prediction: {str(e)}"
        )


@app.get("/api/metrics", response_model=MetricsResponse)
def get_metrics():
    """Returns evaluation metrics, coefficients, and unseen test set comparison."""
    if "model_results" not in state:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Machine learning model is not ready."
        )
        
    res = state["model_results"]
    return MetricsResponse(
        mae=res["metrics"]["mae"],
        rmse=res["metrics"]["rmse"],
        r2=res["metrics"]["r2"],
        r2_percentage=res["metrics"]["r2_percentage"],
        slope=res["slope"],
        intercept=res["intercept"],
        equation=res["equation"],
        train_samples=res["train_samples"],
        test_samples=res["test_samples"],
        test_comparison=res["test_comparison"]
    )


@app.get("/api/dataset", response_model=DatasetResponse)
def get_dataset():
    """Returns descriptive dataset statistics and sample records."""
    if "df" not in state or "summary" not in state:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Dataset is not loaded."
        )
        
    df = state["df"]
    data_list = [
        {
            "hours_studied": round(float(row["Hours_Studied"]), 1),
            "marks_percentage": round(float(row["Marks_Percentage"]), 1)
        }
        for _, row in df.iterrows()
    ]
    
    return DatasetResponse(
        summary=state["summary"],
        data=data_list
    )


@app.get("/api/chart-data", response_model=ChartDataResponse)
def get_chart_data():
    """Returns data points for scatter visualization and the fitted regression line."""
    if "chart_data" not in state:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chart data is not ready."
        )
    return ChartDataResponse(**state["chart_data"])
