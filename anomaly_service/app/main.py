# anomaly_service/app/main.py

from fastapi import FastAPI, HTTPException
from app.schemas import MetricsInput, AnomalyResult
from app.anomaly_detector import MetricAutoencoder, detect_anomalies
from app.utils import get_live_metrics
import os
import torch
import requests
from typing import Dict

app = FastAPI(
    title="Anomaly Detection Service",
    version="1.2.0"
)

# ===================== ENV =====================

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://prometheus:9090")
DECISION_SERVICE_URL = os.getenv(
    "DECISION_SERVICE_URL",
    "http://decision-service:8002"
)

MODEL_STORE: Dict[str, MetricAutoencoder] = {}

# ===================== MODEL =====================

def load_model(input_size: int):
    model = MetricAutoencoder(input_size=input_size)
    try:
        model.load_state_dict(torch.load("autoencoder.pth"))
        model.eval()
    except FileNotFoundError:
        # First-time training / cold start
        pass
    return model

# ===================== API =====================

@app.post("/detect", response_model=AnomalyResult)
def detect_anomaly(input_data: MetricsInput):

    # 1️⃣ Fetch live metrics from Prometheus
    metrics = get_live_metrics(
        prometheus_url=PROMETHEUS_URL,
        app_name=input_data.app_name,
        app_type=input_data.app_type
    )

    if not metrics:
        raise HTTPException(status_code=400, detail="No metrics found")

    metric_list = list(metrics.keys())
    model_key = f"{input_data.app_type}_{len(metric_list)}"

    # 2️⃣ Load / reuse model
    if model_key not in MODEL_STORE:
        MODEL_STORE[model_key] = load_model(len(metric_list))

    # 3️⃣ Detect anomalies
    anomalies, scores = detect_anomalies(
        metrics=metrics,
        metric_list=metric_list,
        model=MODEL_STORE[model_key]
    )

    anomaly_result = {
        "app_name": input_data.app_name,
        "app_type": input_data.app_type,
        "anomalies": anomalies,
        "scores": scores
    }

    # 4️⃣ CALL DECISION SERVICE  🔥 (NEW)
    try:
        decision_resp = requests.post(
            f"{DECISION_SERVICE_URL}/decide",
            json=anomaly_result,
            timeout=3
        )
        decision_data = decision_resp.json()
    except Exception as e:
        decision_data = {
            "decision": "UNKNOWN",
            "reason": f"Decision service unreachable: {str(e)}"
        }

    # 5️⃣ Return anomaly + decision
    return AnomalyResult(
        app_name=input_data.app_name,
        anomalies=anomalies,
        scores=scores,
        decision=decision_data
    )
