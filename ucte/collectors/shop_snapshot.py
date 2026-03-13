import asyncio

from ucte.clients.smp_api import get_all_shops
from ucte.clients.utcon import post_shops
from ucte.config import SHOP_SYNC_INTERVAL


async def run():

    while True:

        try:

            print("[UCTE] Fetching shop snapshot")

            shops = get_all_shops()

            post_shops(shops)

            print(f"[UCTE] Synced {len(shops)} shops")

        except Exception as e:

            print(f"[UCTE] Shop sync failed: {e}")

        await asyncio.sleep(SHOP_SYNC_INTERVAL)