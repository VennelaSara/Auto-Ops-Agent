from fastapi import FastAPI
from app.schemas import StorageEvent, StorageAck
from app.redis_store import store_event, fetch_events

app = FastAPI(
    title="Storage Service",
    version="1.0.0",
    description="Persistent storage for AIOps events"
)

@app.post("/store", response_model=StorageAck)
def store(event: StorageEvent):
    event_id = store_event(event)
    return StorageAck(status="stored", event_id=event_id)

@app.get("/events/{app_name}")
def get_events(app_name: str, limit: int = 50):
    return fetch_events(app_name, limit)
