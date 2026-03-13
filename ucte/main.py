import asyncio

from ucte.collectors.economy_ws import run_economy_ws
from ucte.collectors.shops import sync_shops
from ucte.core.config import SHOP_SYNC_INTERVAL


async def shop_loop():

    while True:

        await sync_shops()

        await asyncio.sleep(SHOP_SYNC_INTERVAL)


async def main():

    await asyncio.gather(
        run_economy_ws(),
        shop_loop()
    )


if __name__ == "__main__":

    asyncio.run(main())