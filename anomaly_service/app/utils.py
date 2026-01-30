# anomaly_service/app/utils.py

from typing import List, Dict
from app.prometheus_client import fetch_metrics
from app.monitoring_profiles import WEB_APPS, DATABASES, CACHE
from app.redis_client import get_app_state

def get_metrics_for_app(app_type: str) -> List[str]:
    if app_type in WEB_APPS:
        return WEB_APPS[app_type]
    if app_type in DATABASES:
        return DATABASES[app_type]
    if app_type in CACHE:
        return CACHE[app_type]
    return []


def get_live_metrics(
    prometheus_url: str,
    app_name: str,
    app_type: str
) -> Dict[str, float]:

    metric_list = get_metrics_for_app(app_type)
    if not metric_list:
        return {}

    return fetch_metrics(
        prometheus_url=prometheus_url,
        app_name=app_name,
        metric_list=metric_list
    )


def get_app_state_from_redis(app_name: str):
    return get_app_state(app_name)
