import redis
import os
import json

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def update_policy(app_name: str, reward: float):
    key = f"policy:{app_name}"
    redis_client.incrbyfloat(key, reward)

def get_policy(app_name: str):
    return float(redis_client.get(f"policy:{app_name}") or 0.0)
