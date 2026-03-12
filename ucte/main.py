import asyncio

from ucte.collectors.economy_ws import run_economy_ws
from ucte.collectors.shops import sync_shops
from ucte.core.scheduler import run_periodic
from ucte.core.config import SHOP_SYNC_INTERVAL


async def main():

    print("[UCTE] Starting UCTE")

    await asyncio.gather(

        run_economy_ws(),

        run_periodic(
            sync_shops,
            SHOP_SYNC_INTERVAL
        )

    )


if __name__ == "__main__":
    asyncio.run(main())