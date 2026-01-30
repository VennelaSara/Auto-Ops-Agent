import yaml
import os
import requests
from typing import List, Dict

PROM_CONFIG_PATH = "/etc/prometheus/prometheus.yml"
PROM_RELOAD_URL = "http://localhost:9090/-/reload"

# For local dev (Docker / non-root)
if not os.path.exists(PROM_CONFIG_PATH):
    PROM_CONFIG_PATH = "./prometheus.yml"


# ---------------- LOAD / SAVE ---------------- #

def load_config() -> Dict:
    with open(PROM_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def save_config(config: Dict):
    with open(PROM_CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


def reload_prometheus():
    try:
        r = requests.post(PROM_RELOAD_URL, timeout=2)
        if r.status_code != 200:
            raise RuntimeError("Prometheus reload failed")
    except Exception as e:
        print("⚠️ Prometheus reload error:", e)


# ---------------- HELPERS ---------------- #

def job_exists(config: Dict, job_name: str) -> bool:
    return any(j["job_name"] == job_name for j in config.get("scrape_configs", []))


def sanitize_job_name(url: str) -> str:
    return url.replace("http://", "").replace("https://", "").replace("/", "_")


# ---------------- CORE API ---------------- #

def configure_prometheus_scrape(
    url: str,
    metrics: List[str],
    auth: bool = False,
    bearer_token: str | None = None,
    basic_auth: Dict | None = None,
    scrape_interval: str = "15s"
) -> Dict:
    """
    Dynamically adds a scrape config for an app.
    """

    config = load_config()
    config.setdefault("scrape_configs", [])

    job_name = f"auto-{sanitize_job_name(url)}"

    if job_exists(config, job_name):
        return {"status": "exists", "job": job_name}

    scrape_config = {
        "job_name": job_name,
        "scrape_interval": scrape_interval,
        "metrics_path": "/metrics",
        "static_configs": [
            {
                "targets": [url.replace("http://", "").replace("https://", "")]
            }
        ]
    }

    # ---- AUTH SUPPORT ----
    if auth:
        if bearer_token:
            scrape_config["authorization"] = {
                "credentials": bearer_token
            }
        elif basic_auth:
            scrape_config["basic_auth"] = basic_auth

    # ---- METRIC FILTERING ----
    if metrics:
        scrape_config["metric_relabel_configs"] = [
            {
                "source_labels": ["__name__"],
                "regex": "|".join(metrics),
                "action": "keep"
            }
        ]

    config["scrape_configs"].append(scrape_config)

    save_config(config)
    reload_prometheus()

    return {
        "status": "created",
        "job": job_name,
        "metrics_count": len(metrics)
    }


# ---------------- KUBERNETES AUTO ---------------- #

def configure_kubernetes_scrape() -> Dict:
    config = load_config()
    config.setdefault("scrape_configs", [])

    job_name = "kubernetes-auto"

    if job_exists(config, job_name):
        return {"status": "exists", "job": job_name}

    scrape_config = {
        "job_name": job_name,
        "kubernetes_sd_configs": [{"role": "pod"}],
        "relabel_configs": [
            {
                "source_labels": ["__meta_kubernetes_pod_annotation_prometheus_io_scrape"],
                "action": "keep",
                "regex": "true"
            },
            {
                "source_labels": ["__meta_kubernetes_pod_annotation_prometheus_io_path"],
                "action": "replace",
                "target_label": "__metrics_path__",
                "regex": "(.+)"
            },
            {
                "source_labels": [
                    "__address__",
                    "__meta_kubernetes_pod_annotation_prometheus_io_port"
                ],
                "action": "replace",
                "regex": "([^:]+)(?::\\d+)?;(\\d+)",
                "replacement": "$1:$2",
                "target_label": "__address__"
            }
        ]
    }

    config["scrape_configs"].append(scrape_config)
    save_config(config)
    reload_prometheus()

    return {"status": "created", "job": job_name}


# ---------------- BLACKBOX ---------------- #

def configure_blackbox_scrape(target_url: str) -> Dict:
    config = load_config()
    config.setdefault("scrape_configs", [])

    job_name = f"blackbox-{sanitize_job_name(target_url)}"

    if job_exists(config, job_name):
        return {"status": "exists", "job": job_name}

    scrape_config = {
        "job_name": job_name,
        "metrics_path": "/probe",
        "params": {"module": ["http_2xx"]},
        "static_configs": [{"targets": [target_url]}],
        "relabel_configs": [
            {
                "source_labels": ["__address__"],
                "target_label": "__param_target"
            },
            {
                "target_label": "__address__",
                "replacement": "blackbox-exporter:9115"
            }
        ]
    }

    config["scrape_configs"].append(scrape_config)
    save_config(config)
    reload_prometheus()

    return {"status": "created", "job": job_name}
