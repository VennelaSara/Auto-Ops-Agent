from fastapi import FastAPI
from app.schemas import ActionInput, ActionResult
from app.action_router import execute_actions
import os
import requests

app = FastAPI(
    title="Action Service",
    version="1.1.0",
    description="Executes alerts, tickets and remediation for AIOps"
)

FEEDBACK_SERVICE_URL = os.getenv(
    "FEEDBACK_SERVICE_URL",
    "http://feedback-service:8004/feedback"
)

TIMEOUT_SECONDS = 3


@app.post("/act", response_model=ActionResult)
def perform_action(input_data: ActionInput):

    # 1️⃣ Execute actions
    actions_taken = execute_actions(input_data)

    # 2️⃣ Send feedback (fire-and-forget)
    try:
        requests.post(
            FEEDBACK_SERVICE_URL,
            json={
                "app_name": input_data.app_name,
                "severity": input_data.severity,
                "actions_taken": actions_taken,
                "status": "success",
                "confidence": input_data.confidence if hasattr(input_data, "confidence") else None
            },
            timeout=TIMEOUT_SECONDS
        )
    except Exception:
        # Feedback must NEVER break action execution
        pass

    # 3️⃣ Respond immediately
    return ActionResult(
        app_name=input_data.app_name,
        status="executed",
        actions_taken=actions_taken
    )
