from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from app.schemas import AppOnboardRequest, MonitoringDecision
from app.permission import detect_monitoring_strategy, apply_monitoring
from app.redis_client import save_monitoring_strategy, get_monitoring_strategy
from app.monitoring_profiles import WEB_APPS
from app.config import APP_NAME
from typing import Dict, Any, List
import requests
import os

# -------------------- Service URLs --------------------

ANOMALY_SERVICE_URL = os.getenv(
    "ANOMALY_SERVICE_URL",
    "http://anomaly-service:8001"
)

# -------------------- FastAPI App --------------------

app = FastAPI(
    title="Auto Monitoring Orchestrator",
    version="1.0.0",
    description="Automatic monitoring detection, strategy resolution & execution"
)

# -------------------- Anomaly Trigger --------------------

def trigger_anomaly_detection(app_name: str, app_type: str):
    """
    Fire-and-forget call to anomaly detection service
    """
    try:
        requests.post(
    f"{ANOMALY_SERVICE_URL}/detect",
    json={
        "app_name": app_name,
        "app_type": app_type
    },
    timeout=2
)

    except Exception as e:
        # Do NOT break onboarding if anomaly service is unavailable
        print(f"[WARN] Anomaly service unreachable: {e}")

# -------------------- API Endpoints --------------------

@app.post("/onboard", response_model=MonitoringDecision)
def onboard_app(app_req: AppOnboardRequest):

    # Step 1: Detect monitoring strategy
    strategy_info = detect_monitoring_strategy({
        **app_req.dict(),
        "url": str(app_req.url)
    })

    if not strategy_info.get("monitorable", False):
        return MonitoringDecision(
            monitorable=False,
            strategy=strategy_info.get("strategy") or strategy_info.get("strategies"),
            confidence=str(strategy_info.get("confidence", "")),
            details=str(strategy_info.get("details", "")),
            metrics=None,
            logs=None,
            traces=None,
            state=None
        )

    # Step 2: Get metrics profile
    metrics: List[str] = []
    if app_req.app_type and app_req.app_type in WEB_APPS:
        metrics = WEB_APPS[app_req.app_type]

    # Step 3: Apply monitoring strategy (Prometheus / OTEL / etc.)
    applied_config: Dict[str, Any] = apply_monitoring({
        **app_req.dict(),
        "url": str(app_req.url)
    }, strategy_info)

    # Step 4: Persist state in Redis
    final_state = jsonable_encoder({
        "app": {
            **app_req.dict(),
            "url": str(app_req.url)
        },
        "strategy": strategy_info,
        "metrics": metrics,
        "applied_config": applied_config
    })

    save_monitoring_strategy(app_req.name, final_state)

    # 🔥 Step 4.5: Trigger anomaly detection
    trigger_anomaly_detection(
        app_name=app_req.name,
        app_type=app_req.app_type
    )

    # Step 5: Ensure logs and traces are dictionaries or None
    logs = applied_config.get("loki")
    if not isinstance(logs, dict):
        logs = None

    traces = applied_config.get("tempo")
    if not isinstance(traces, dict):
        traces = None

    # Step 6: Return monitoring decision
    return MonitoringDecision(
        monitorable=True,
        strategy=strategy_info.get("strategy") or strategy_info.get("strategies"),
        confidence=str(strategy_info.get("confidence", "")),
        details=strategy_info.get("details", {}),
        metrics=metrics,
        logs=logs,
        traces=traces,
        state={"stored_in": "redis"}
    )


@app.get("/state/{app_name}")
def get_state(app_name: str):
    state = get_monitoring_strategy(app_name)
    if not state:
        raise HTTPException(status_code=404, detail="App not found")
    return state
