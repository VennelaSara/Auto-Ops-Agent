from app.redis_store import fetch_events

def get_app_history(app_name: str, limit: int = 50):
    return fetch_events(app_name, limit)
