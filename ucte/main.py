import asyncio

from ucte.collectors.websocket import run as websocket_run
from ucte.collectors.shop_snapshot import run as shop_snapshot_run

from ucte.workers.transaction_worker import run as transaction_worker
from ucte.workers.shop_worker import run as shop_worker


async def main():

    transaction_queue = asyncio.Queue(maxsize=10000)
    shop_queue = asyncio.Queue(maxsize=10000)

    await asyncio.gather(

        websocket_run(transaction_queue),
        shop_snapshot_run(shop_queue),

        transaction_worker(transaction_queue),
        shop_worker(shop_queue)

    )


if __name__ == "__main__":

    asyncio.run(main())