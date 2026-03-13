import asyncio

from ucte.clients.utcon import post_transactions
from ucte.config import TRANSACTION_BATCH_SIZE


async def run(queue):
    batch = []

    while True:
        try:
            tx = await asyncio.wait_for(queue.get(), timeout=5)
            batch.append(tx)
            print(f"[UCTE] transaction queued for batch, size now {len(batch)}")

            if len(batch) >= TRANSACTION_BATCH_SIZE:
                print(f"[UCTE] posting transaction batch of {len(batch)}")
                post_transactions(batch)
                batch.clear()

        except asyncio.TimeoutError:
            if batch:
                print(f"[UCTE] flushing partial transaction batch of {len(batch)}")
                post_transactions(batch)
                batch.clear()