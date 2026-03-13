import asyncio

from ucte.clients.utcon import post_transactions
from ucte.config import TRANSACTION_BATCH_SIZE


async def run(queue):

    batch = []

    while True:

        tx = await queue.get()

        batch.append(tx)

        if len(batch) >= TRANSACTION_BATCH_SIZE:

            post_transactions(batch)

            batch.clear()