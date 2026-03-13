import asyncio
import httpx

from ucte.config import QUICKSHOP_API_URL, UTCON_URL

BATCH_SIZE = 500


async def run():
    print("[UCTE] Fetching shop snapshot")

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.get(f"{QUICKSHOP_API_URL}/quickshop/v1/getAllShops")
        r.raise_for_status()

        shops = r.json()

    print(f"[UCTE] Queued {len(shops)} shops")

    await send_to_utcon(shops)


async def send_to_utcon(shops):

    async with httpx.AsyncClient(timeout=120) as client:

        for i in range(0, len(shops), BATCH_SIZE):
            batch = shops[i:i + BATCH_SIZE]

            try:
                r = await client.post(
                    f"{UTCON_URL}/v1/raw/shop/record",
                    json=batch
                )

                if r.status_code != 200:
                    print("[UCTE] shop error", r.status_code)
                    print(r.text)

            except Exception as e:
                print("[UCTE] shop push failed:", e)

            await asyncio.sleep(0.05)