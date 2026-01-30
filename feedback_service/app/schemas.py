from pydantic import BaseModel
from typing import Optional

class FeedbackInput(BaseModel):
    app_name: str
    action: str
    severity: str
    success: bool
    manual_override: Optional[bool] = False
    user_rating: Optional[int] = None  # 1–5

class FeedbackResult(BaseModel):
    app_name: str
    reward: float
    policy_updated: bool
