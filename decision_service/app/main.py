from fastapi import FastAPI, HTTPException
from app.schemas import DecisionInput, DecisionResult
from app.prompt_builder import build_decision_prompt
from app.ollama_client import run_decision_llm
from app.severity import apply_guardrails

import os
import requests
from typing import Dict, Any

# --------------------------------------------------
# App Init
# --------------------------------------------------

app = FastAPI(
    title="Decision Service",
    version="1.1.0",
    description="LLM-powered decision making for AIOps"
)

# --------------------------------------------------
# Service Config
# --------------------------------------------------

ACTION_SERVICE_URL = os.getenv(
    "ACTION_SERVICE_URL",
    "http://action-service:8003/act"
)

TIMEOUT_SECONDS = 5


# --------------------------------------------------
# Decision Endpoint
# --------------------------------------------------

@app.post("/decide", response_model=DecisionResult)
def make_decision(input_data: DecisionInput):
    """
    Takes anomaly scores + metrics
    → Uses LLM for reasoning
    → Applies safety guardrails
    → Triggers Action Service
    """

    # 1️⃣ Build prompt for LLM
    prompt = build_decision_prompt(input_data.dict())

    # 2️⃣ Run LLM with safe fallback
    try:
        llm_result: Dict[str, Any] = run_decision_llm(prompt)
    except Exception:
        llm_result = {
            "severity": "UNKNOWN",
            "root_cause": "LLM unavailable or failed",
            "recommendation": "Fallback to rule-based monitoring",
            "notify": False,
            "create_ticket": False,
            "confidence": 0.2
        }

    # 3️⃣ Apply deterministic guardrails
    final_decision = apply_guardrails(
        llm_result=llm_result,
        anomaly_scores=input_data.scores
    )

    # 4️⃣ Call Action Service (non-blocking-safe)
    try:
        requests.post(
            ACTION_SERVICE_URL,
            json={
                "app_name": input_data.app_name,
                "severity": final_decision["severity"],
                "root_cause": final_decision["root_cause"],
                "recommendation": final_decision["recommendation"],
                "notify": final_decision["notify"],
                "create_ticket": final_decision["create_ticket"]
            },
            timeout=TIMEOUT_SECONDS
        )
    except Exception:
        # Action failure should NOT break decision service
        pass

    # 5️⃣ Return final decision
    return DecisionResult(
        app_name=input_data.app_name,
        severity=final_decision["severity"],
        root_cause=final_decision["root_cause"],
        recommendation=final_decision["recommendation"],
        notify=final_decision["notify"],
        create_ticket=final_decision["create_ticket"],
        confidence=float(final_decision["confidence"])
    )
