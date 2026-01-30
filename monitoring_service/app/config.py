import os

# ---------- APP ----------
APP_NAME = os.getenv("APP_NAME", "auto-monitoring-orchestrator")
ENV = os.getenv("ENV", "dev")

# ---------- REDIS ----------
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# ---------- PROMETHEUS ----------
PROMETHEUS_CONFIG_PATH = os.getenv(
    "PROMETHEUS_CONFIG_PATH",
    "./prometheus/prometheus.yml"
)
PROMETHEUS_RELOAD_URL = os.getenv(
    "PROMETHEUS_RELOAD_URL",
    "http://localhost:9090/-/reload"
)

# ---------- LOKI ----------
LOKI_URL = os.getenv("LOKI_URL", "http://localhost:3100")

# ---------- TEMPO ----------
TEMPO_URL = os.getenv("TEMPO_URL", "http://localhost:3200")

# ---------- TIMEOUTS ----------
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", 3))
