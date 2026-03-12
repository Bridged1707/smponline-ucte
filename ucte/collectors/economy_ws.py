import asyncio
import json
import websockets

from ucte.core.config import ECONOMY_WS, USER_AGENT, ECONOMY_WS_RECONNECT_DELAY
from ucte.services.utdb_client import send_raw_event


async def run_economy_ws():

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

                    event_type = data["event"]
                    timestamp = data.get("timestamp")

                    send_raw_event(
                        event_type,
                        data,
                        timestamp
                    )

        except Exception as e:

            print(f"[UCTE] Websocket disconnected: {e}")
            print(f"[UCTE] Reconnecting in {ECONOMY_WS_RECONNECT_DELAY}s")

            await asyncio.sleep(ECONOMY_WS_RECONNECT_DELAY)