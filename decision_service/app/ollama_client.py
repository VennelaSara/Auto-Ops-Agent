import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def run_decision_llm(prompt: str) -> dict:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )

    raw = response.json()["response"]

    try:
        return json.loads(raw)
    except Exception:
        return {
            "severity": "MEDIUM",
            "root_cause": "Unclear",
            "recommendation": "Manual inspection required",
            "notify": True,
            "create_ticket": False,
            "confidence": 0.5
        }
