import asyncio
import json
import websockets

from ucte.config import ECONOMY_WS, USER_AGENT, WS_RECONNECT_DELAY
from ucte.clients.utcon import post_transaction


async def run():

    while True:

        try:

            print("[UCTE] Connecting to economy websocket")

            async with websockets.connect(
                ECONOMY_WS,
                extra_headers={"User-Agent": USER_AGENT}
            ) as ws:

                print("[UCTE] Websocket connected")

                async for message in ws:

                    data = json.loads(message)

                    if "event" not in data:
                        continue

                    post_transaction(data)

        except Exception as e:

            print(f"[UCTE] Websocket disconnected: {e}")
            await asyncio.sleep(WS_RECONNECT_DELAY)