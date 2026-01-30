import redis
import json
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def store_anomaly(app_name, result):
    r.hset("anomalies", app_name, json.dumps(result))
