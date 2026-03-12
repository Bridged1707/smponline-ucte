import requests
import time

from ucte.core.config import UTDB_API_URL


def send_raw_event(event_type: str, payload: dict, timestamp: int):

    url = f"{UTDB_API_URL}/events/raw"

    data = {
        "event_type": event_type,
        "event_timestamp": timestamp,
        "payload": payload
    }

    try:

        response = requests.post(url, json=data, timeout=10)

        if response.status_code != 200:
            print(f"[UCTE] UTDB error: {response.text}")

    except Exception as e:
        print(f"[UCTE] Failed sending event: {e}")