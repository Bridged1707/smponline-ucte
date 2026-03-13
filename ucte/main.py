import asyncio

from ucte.collectors.websocket import run as websocket_run
from ucte.collectors.shop_snapshot import run as shop_snapshot_run


async def main():

    queue = asyncio.Queue()

    print("[UCTE] Connecting to economy websocket")

    await shop_snapshot_run()

    await websocket_run(queue)


if __name__ == "__main__":
    asyncio.run(main())