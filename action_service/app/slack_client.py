import os
import requests

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(message: str):
    if not SLACK_WEBHOOK_URL:
        return False

    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=3)
    return True
