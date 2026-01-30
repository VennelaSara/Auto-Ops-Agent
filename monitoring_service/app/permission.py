import requests
import socket
from typing import Dict, List
from urllib.parse import urlparse

from app.prometheus_dynamic import configure_prometheus_scrape
from app.monitoring_profiles import (
    WEB_APPS,
    FRONTEND_APPS,
    WORKERS,
    MESSAGING,
    DATABASES,
    CACHE,
    KUBERNETES,
    CLOUD,
    AI_SYSTEMS,
    BLACKBOX,
    SECURITY,
    BASE_METRICS,
    GOLDEN_SIGNALS
)

# ---------------- CONFIG ---------------- #

PROM_TIMEOUT = 3
OTEL_TIMEOUT = 2
STATSD_PORT = 8125
LOKI_TIMEOUT = 3
TEMPO_TIMEOUT = 3


# ---------------- LOW LEVEL CHECKS ---------------- #

def check_prometheus_metrics(base_url: str) -> bool:
    try:
        r = requests.get(f"{base_url}/metrics", timeout=PROM_TIMEOUT)
        return r.status_code == 200 and "HELP" in r.text
    except Exception:
        return False


def check_prometheus_auth(base_url: str) -> bool:
    try:
        r = requests.get(f"{base_url}/metrics", timeout=PROM_TIMEOUT)
        return r.status_code in (401, 403)
    except Exception:
        return False


def check_otlp_http(base_url: str) -> bool:
    for path in ("/v1/metrics", "/v1/traces"):
        try:
            r = requests.post(f"{base_url}{path}", timeout=OTEL_TIMEOUT)
            if r.status_code in (200, 404, 415):
                return True
        except Exception:
            pass
    return False


def check_otlp_grpc(host: str, port: int = 4317) -> bool:
    try:
        with socket.create_connection((host, port), timeout=OTEL_TIMEOUT):
            return True
    except Exception:
        return False


def check_statsd(host: str) -> bool:
    try:
        with socket.create_connection((host, STATSD_PORT), timeout=2):
            return True
    except Exception:
        return False


def check_blackbox_http(url: str) -> bool:
    try:
        r = requests.get(url, timeout=5)
        return r.status_code < 500
    except Exception:
        return False


def detect_kubernetes(headers: Dict) -> bool:
    return "kubernetes" in str(headers).lower()


def detect_cloud(headers: Dict) -> str | None:
    h = str(headers).lower()
    if "x-amzn" in h:
        return "aws"
    if "x-goog" in h:
        return "gcp"
    if "x-ms" in h:
        return "azure"
    return None


def check_loki(url: str) -> bool:
    try:
        r = requests.get(f"{url}/loki/api/v1/labels", timeout=LOKI_TIMEOUT)
        return r.status_code == 200
    except Exception:
        return False


def check_tempo(url: str) -> bool:
    try:
        r = requests.get(f"{url}/tempo/api/traces", timeout=TEMPO_TIMEOUT)
        return r.status_code in (200, 404)
    except Exception:
        return False


# ---------------- METRIC RESOLVER ---------------- #

def resolve_metrics(app_type: str, framework: str) -> List[str]:
    metrics = BASE_METRICS.copy()

    metrics += GOLDEN_SIGNALS["latency"]
    metrics += GOLDEN_SIGNALS["traffic"]
    metrics += GOLDEN_SIGNALS["errors"]
    metrics += GOLDEN_SIGNALS["saturation"]

    sources = [
        WEB_APPS,
        FRONTEND_APPS,
        WORKERS,
        MESSAGING,
        DATABASES,
        CACHE,
        AI_SYSTEMS
    ]

    for src in sources:
        if framework in src:
            metrics += src[framework]

    if app_type == "kubernetes":
        metrics += KUBERNETES

    return list(set(metrics))


# ---------------- STRATEGY DECISION ---------------- #

def detect_monitoring_strategy(app: Dict) -> Dict:
    url = app["url"]
    app_type = app.get("type", "web")
    framework = app.get("framework", "")
    parsed = urlparse(url)
    host = parsed.hostname

    try:
        headers = requests.get(url, timeout=2).headers
    except Exception:
        headers = {}

    decision = {
        "monitorable": False,
        "strategies": [],
        "metrics": [],
        "logs": False,
        "traces": False,
        "state": False,
        "confidence": "low"
    }

    # ---- METRICS ----
    if check_prometheus_metrics(url):
        decision["strategies"].append("prometheus")
        decision["monitorable"] = True
        decision["confidence"] = "high"

    elif check_prometheus_auth(url):
        decision["strategies"].append("prometheus-auth")
        decision["monitorable"] = True

    elif check_otlp_http(url):
        decision["strategies"].append("otel-http")
        decision["monitorable"] = True

    elif check_otlp_grpc(host):
        decision["strategies"].append("otel-grpc")
        decision["monitorable"] = True

    elif check_statsd(host):
        decision["strategies"].append("statsd")
        decision["monitorable"] = True

    elif detect_kubernetes(headers):
        decision["strategies"].append("kubernetes-auto")
        decision["monitorable"] = True

    else:
        cloud = detect_cloud(headers)
        if cloud:
            decision["strategies"].append(f"{cloud}-cloud-metrics")
            decision["monitorable"] = True

    # ---- BLACKBOX FALLBACK ----
    if not decision["monitorable"] and check_blackbox_http(url):
        decision["strategies"].append("blackbox")
        decision["monitorable"] = True

    # ---- LOGS / TRACES ----
    if check_loki(url):
        decision["logs"] = True

    if check_tempo(url):
        decision["traces"] = True

    # ---- STATE ----
    if app_type in ("cache", "database", "queue"):
        decision["state"] = True

    if decision["monitorable"]:
        decision["metrics"] = resolve_metrics(app_type, framework)

    return decision


# ---------------- APPLY STRATEGY ---------------- #

def apply_monitoring(app: Dict, decision: Dict) -> Dict:
    url = app["url"]
    framework = app.get("framework", "")
    hostname = urlparse(url).hostname

    applied = {}

    if "prometheus" in decision["strategies"]:
        applied["prometheus"] = configure_prometheus_scrape(
            url=url,
            metrics=decision["metrics"]
        )

    if "prometheus-auth" in decision["strategies"]:
        applied["prometheus"] = configure_prometheus_scrape(
            url=url,
            auth=True,
            metrics=decision["metrics"]
        )

    if "otel-http" in decision["strategies"]:
        applied["otel"] = {
            "protocol": "http",
            "endpoint": url
        }

    if "otel-grpc" in decision["strategies"]:
        applied["otel"] = {
            "protocol": "grpc",
            "endpoint": f"{hostname}:4317"
        }

    if "blackbox" in decision["strategies"]:
        applied["blackbox"] = BLACKBOX

    if decision["logs"]:
        applied["loki"] = True

    if decision["traces"]:
        applied["tempo"] = True

    if decision["state"]:
        applied["redis"] = True

    return applied
