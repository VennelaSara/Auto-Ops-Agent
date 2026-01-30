# anomaly_service/app/prometheus_client.py

import requests
from typing import Dict, List

def fetch_metrics(
    prometheus_url: str,
    app_name: str,
    metric_list: List[str]
) -> Dict[str, float]:

    metrics = {}

    for metric in metric_list:
        # Example PromQL
        query = f'{metric}{{job="{app_name}"}}'

        try:
            resp = requests.get(
                f"{prometheus_url}/api/v1/query",
                params={"query": query},
                timeout=3
            )
            data = resp.json()

            if data["status"] == "success" and data["data"]["result"]:
                value = float(data["data"]["result"][0]["value"][1])
                metrics[metric] = value
            else:
                metrics[metric] = 0.0

        except Exception:
            metrics[metric] = 0.0

    return metrics
