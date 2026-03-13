import asyncio

from ucte.clients.smp_api import get_all_shops
from ucte.processors.normalize_shops import normalize_shop
from ucte.config import SHOP_SYNC_INTERVAL


async def run(queue):

    while True:

        try:

            print("[UCTE] Fetching shop snapshot")

            shops = get_all_shops()

            for shop in shops:
                await queue.put(normalize_shop(shop))

            print(f"[UCTE] Queued {len(shops)} shops")

        except Exception as e:

            print("[UCTE] Shop sync failed:", e)

        await asyncio.sleep(SHOP_SYNC_INTERVAL)