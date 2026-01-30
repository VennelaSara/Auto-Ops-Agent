import redis
import json
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)


def save_monitoring_strategy(app_name: str, data: dict):
    redis_client.set(
        f"monitoring:{app_name}",
        json.dumps(data)
    )


def get_monitoring_strategy(app_name: str):
    value = redis_client.get(f"monitoring:{app_name}")
    return json.loads(value) if value else None
