import asyncio

from ucte.collectors.websocket import run as websocket_run
from ucte.collectors.shop_snapshot import run as shop_snapshot_run
from ucte.workers.transaction_worker import run as transaction_worker_run


async def main():
    queue = asyncio.Queue()

    print("[UCTE] Starting shop snapshot")
    await shop_snapshot_run()

    print("[UCTE] Starting websocket + transaction worker")
    await asyncio.gather(
        websocket_run(queue),
        transaction_worker_run(queue),
    )


if __name__ == "__main__":
    asyncio.run(main())