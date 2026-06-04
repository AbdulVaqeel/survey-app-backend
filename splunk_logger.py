import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SPLUNK_HEC_URL = os.getenv(
    "SPLUNK_HEC_URL",
    "https://grimacing-reenact-shudder.ngrok-free.dev/services/collector/event"
)
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN")

def send_to_splunk(action: str, username: str, ip: str, reason: str = None):
    if not SPLUNK_HEC_URL or not SPLUNK_TOKEN:
        print("Splunk HEC not configured — skipping", flush=True)
        return

    payload = {
        "time": datetime.datetime.utcnow().timestamp(),
        "index": "survey_auth_logs",
        "sourcetype": "survey_auth",
        "event": {
            "action": action,
            "username": username,
            "ip": ip,
            "reason": reason or "",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "environment": os.getenv("ENVIRONMENT", "production")
        }
    }
    headers = {
        "Authorization": f"Splunk {SPLUNK_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            SPLUNK_HEC_URL,
            json=payload,
            headers=headers,
            verify=False,
            timeout=5
        )
        print(f"[Splunk HEC] {response.status_code} — {response.text}", flush=True)
    except Exception as e:
        print(f"[Splunk HEC Error] {e}", flush=True)