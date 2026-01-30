from fastapi import FastAPI
from app.schemas import FeedbackInput, FeedbackResult
from app.reward_engine import compute_reward
from app.trainer import train_policy
import os
import requests

app = FastAPI(
    title="Feedback Service",
    version="1.1.0",
    description="Learning feedback loop for AIOps actions"
)
STORAGE_SERVICE_URL = os.getenv(
    "STORAGE_SERVICE_URL",
    "http://storage-service:8005/store"
)

requests.post(
    STORAGE_SERVICE_URL,
    json={
        "event_type": "feedback",
        "app_name": feedback.app_name,
        "reward": reward,
        "policy_updated": updated
    },
    timeout=TIMEOUT_SECONDS
)


TIMEOUT_SECONDS = 3


@app.post("/feedback", response_model=FeedbackResult)
def submit_feedback(feedback: FeedbackInput):

    # 1️⃣ Compute reward
    reward = compute_reward(feedback)

    # 2️⃣ Train policy / update learning state
    updated = train_policy(
        app_name=feedback.app_name,
        reward=reward
    )

    # 3️⃣ Notify Monitoring Service (fire-and-forget)
    try:
        requests.post(
    STORAGE_SERVICE_URL,
    json={
        "event_type": "feedback",
        "app_name": feedback.app_name,
        "reward": reward,
        "policy_updated": updated
    },
    timeout=TIMEOUT_SECONDS
)
    except Exception:
        # Monitoring update should NEVER break feedback loop
        pass

    # 4️⃣ Return feedback result
    return FeedbackResult(
        app_name=feedback.app_name,
        reward=reward,
        policy_updated=updated
    )
