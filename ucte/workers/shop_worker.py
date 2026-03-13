import asyncio

from ucte.clients.utcon import post_shops
from ucte.config import SHOP_BATCH_SIZE


async def run(queue):

    batch = []

    while True:

        shop = await queue.get()

        batch.append(shop)

        if len(batch) >= SHOP_BATCH_SIZE:

            post_shops(batch)

            batch.clear()