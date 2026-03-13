import asyncio

from ucte.collectors.economy_ws import run as ws_collector
from ucte.collectors.shop_snapshot import run as shop_collector


async def main():

    await asyncio.gather(
        ws_collector(),
        shop_collector()
    )


if __name__ == "__main__":

    asyncio.run(main())