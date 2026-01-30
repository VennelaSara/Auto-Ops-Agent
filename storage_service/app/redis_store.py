import redis
import os
import json
import uuid
from datetime import datetime

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def store_event(event):
    event_id = str(uuid.uuid4())
    timestamp = event.timestamp or datetime.utcnow()

    key = f"event:{event.app_name}:{event.event_type}:{event_id}"

    payload = {
        "event_id": event_id,
        "app_name": event.app_name,
        "event_type": event.event_type,
        "severity": event.severity,
        "timestamp": timestamp.isoformat(),
        "data": event.data
    }

    redis_client.set(key, json.dumps(payload))
    redis_client.lpush(f"events:{event.app_name}", key)

    return event_id

def fetch_events(app_name: str, limit: int = 50):
    keys = redis_client.lrange(f"events:{app_name}", 0, limit - 1)
    return [json.loads(redis_client.get(k)) for k in keys if redis_client.get(k)]
