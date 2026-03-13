import asyncio
import json
import websockets

from ucte.config import SMP_WS_URL
from ucte.processors.normalize_transactions import (
    normalize_auction,
    normalize_shop_transaction
)


async def run(queue):
    while True:
        try:
            print("[UCTE] Connecting to economy websocket")

            async with websockets.connect(
                SMP_WS_URL,
                extra_headers={"User-Agent": "UCTE/1.0"}
            ) as ws:
                print("[UCTE] Websocket connected")

                async for message in ws:
                    print("[UCTE] raw ws message:", message)

                    data = json.loads(message)

                    if "event" not in data:
                        continue

                    if data["event"] == "auctionComplete":
                        tx = normalize_auction(data)
                        print("[UCTE] queued auction tx:", tx)
                        await queue.put(tx)

                    elif data["event"] == "shopTransaction":
                        tx = normalize_shop_transaction(data)
                        print("[UCTE] queued shop tx:", tx)
                        await queue.put(tx)

        except Exception as e:
            print("[UCTE] Websocket disconnected:", e)
            await asyncio.sleep(5)