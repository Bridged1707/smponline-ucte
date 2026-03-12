import time
import requests

from ucte.core.config import SHOP_ENDPOINT
from ucte.services.utdb_client import send_raw_event


async def sync_shops():

    print("[UCTE] Syncing shop snapshot")

    try:

        response = requests.get(SHOP_ENDPOINT, timeout=20)

        if response.status_code != 200:
            print("[UCTE] Shop API error")
            return

        shops = response.json()

        timestamp = int(time.time() * 1000)

        send_raw_event(
            "shop_snapshot",
            shops,
            timestamp
        )

        print(f"[UCTE] Stored snapshot ({len(shops)} shops)")

    except Exception as e:
        print(f"[UCTE] Shop sync failed: {e}")