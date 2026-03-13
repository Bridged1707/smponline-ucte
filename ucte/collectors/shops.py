import time
import requests

from ucte.core.config import SHOP_ENDPOINT
from ucte.services.utcon_client import post_shops


async def sync_shops():

    print("[UCTE] Syncing shop snapshot")

    try:

        response = requests.get(SHOP_ENDPOINT, timeout=20)

        if response.status_code != 200:
            print("[UCTE] Shop API error")
            return

        shops = response.json()

        post_shops(shops)

        print(f"[UCTE] Synced {len(shops)} shops")

    except Exception as e:
        print(f"[UCTE] Shop sync failed: {e}")