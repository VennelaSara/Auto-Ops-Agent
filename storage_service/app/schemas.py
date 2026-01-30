from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class StorageEvent(BaseModel):
    app_name: str
    event_type: str  # anomaly | decision | action | feedback
    severity: Optional[str] = None
    data: Dict
    timestamp: Optional[datetime] = None

class StorageAck(BaseModel):
    status: str
    event_id: str
