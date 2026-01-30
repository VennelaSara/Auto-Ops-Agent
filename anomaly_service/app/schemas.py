from pydantic import BaseModel
from typing import Dict, List, Optional

class MetricsInput(BaseModel):
    app_name: str
    app_type: str
    metrics: Dict[str, float]  # metric_name -> value

class AnomalyResult(BaseModel):
    app_name: str
    anomalies: Dict[str, bool]  # metric_name -> True/False
    scores: Dict[str, float]    # reconstruction error per metric
