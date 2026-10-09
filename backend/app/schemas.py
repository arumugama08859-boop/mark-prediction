"""
schemas.py - Pydantic schemas for request and response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class PredictionRequest(BaseModel):
    study_hours: float = Field(
        ...,
        ge=0.0,
        le=24.0,
        description="Number of daily study hours between 0.0 and 24.0"
    )


class PredictionResponse(BaseModel):
    study_hours: float
    predicted_marks: float
    raw_prediction: float
    is_clamped: bool
    category: str
    badge_color: str
    tip: str
    clamping_note: Optional[str] = None


class TestComparisonItem(BaseModel):
    study_hours: float
    actual_marks: float
    predicted_marks: float
    absolute_error: float


class MetricsResponse(BaseModel):
    mae: float
    rmse: float
    r2: float
    r2_percentage: float
    slope: float
    intercept: float
    equation: str
    train_samples: int
    test_samples: int
    test_comparison: List[TestComparisonItem]


class StudentDataPoint(BaseModel):
    hours_studied: float
    marks_percentage: float


class DatasetSummary(BaseModel):
    total_records: int
    hours_mean: float
    hours_min: float
    hours_max: float
    marks_mean: float
    marks_min: float
    marks_max: float
    correlation: float


class DatasetResponse(BaseModel):
    summary: DatasetSummary
    data: List[StudentDataPoint]


class ChartScatterPoint(BaseModel):
    hours: float
    marks: float
    split: str  # 'train' or 'test'


class ChartLinePoint(BaseModel):
    hours: float
    predicted_marks: float


class ChartDataResponse(BaseModel):
    scatter_points: List[ChartScatterPoint]
    regression_line: List[ChartLinePoint]
