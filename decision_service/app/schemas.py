from pydantic import BaseModel
from typing import Dict, Any, Optional

class DecisionInput(BaseModel):
    app_name: str
    app_type: str
    anomalies: Dict[str, bool]
    scores: Dict[str, float]
    metrics: Dict[str, float]

class DecisionResult(BaseModel):
    app_name: str
    severity: str
    root_cause: str
    recommendation: str
    notify: bool
    create_ticket: bool
    confidence: float
