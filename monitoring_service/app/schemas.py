from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any, List, Union


class AppOnboardRequest(BaseModel):
    name: str = Field(..., example="payments-service")
    url: HttpUrl = Field(..., example="http://localhost:8000")
    app_type: Optional[str] = Field(None, example="fastapi")
    logs_enabled: bool = False
    traces_enabled: bool = False


class MonitoringDecision(BaseModel):
    monitorable: bool
    strategy: Optional[Union[str, List[str]]] = None  # accept string or list
    confidence: Optional[Union[str, float]] = None    # accept string or float
    details: Optional[Union[str, Dict[str, Any]]] = None  # accept string or dict
    metrics: Optional[List[str]] = None
    logs: Optional[Dict[str, Any]] = None
    traces: Optional[Dict[str, Any]] = None
    state: Optional[Dict[str, Any]] = None
