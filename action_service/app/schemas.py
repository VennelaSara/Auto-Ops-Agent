from pydantic import BaseModel
from typing import List

class ActionInput(BaseModel):
    app_name: str
    severity: str
    root_cause: str
    recommendation: str
    notify: bool
    create_ticket: bool


class ActionResult(BaseModel):
    app_name: str
    status: str
    actions_taken: List[str]
