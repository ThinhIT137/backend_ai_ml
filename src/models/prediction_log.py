from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class PredictionLogRecord(BaseModel):
    session_id: Optional[str] = None
    cccd: Optional[str] = None
    evaluation_type: str = "admission_chance"
    target_major_code: Optional[str] = None
    target_major_name: Optional[str] = None
    admission_method: str = "PT1"
    academic_scores: Dict[str, float] = {}
    priority_region: Optional[str] = None
    priority_group: Optional[str] = None
    optimal_combination: Optional[str] = None
    calculated_score: Optional[float] = None
    predicted_benchmark: Optional[float] = None
    admission_probability: Optional[float] = None
    risk_level: Optional[str] = None
    strategic_advice: Optional[List[str]] = None
    created_at: Optional[datetime] = None
