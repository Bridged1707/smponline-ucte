import asyncio

from ucte.collectors.websocket import run as websocket_run
from ucte.collectors.shop_snapshot import run_forever as shop_snapshot_run_forever
from ucte.workers.transaction_worker import run as transaction_worker_run

import os

async def main():
    queue = asyncio.Queue()

    print("[UCTE] Starting websocket + transaction worker + shop snapshot loop")
    await asyncio.gather(
        websocket_run(queue),
        transaction_worker_run(queue),
        shop_snapshot_run_forever(),
    )


if __name__ == "__main__":
    asyncio.run(main())
