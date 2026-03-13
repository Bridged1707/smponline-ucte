import asyncio
import httpx

from ucte.config import SMP_API_BASE, UTCON_URL, SHOP_BATCH_SIZE

async def run():
    print("[UCTE] Fetching shop snapshot")

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.get(f"{SMP_API_BASE}/quickshop/v1/getAllShops")
        r.raise_for_status()

        shops = r.json()

    print(f"[UCTE] Queued {len(shops)} shops")

    await send_to_utcon(shops)


async def send_to_utcon(shops):

    async with httpx.AsyncClient(timeout=120) as client:

        for i in range(0, len(shops), SHOP_BATCH_SIZE):
            batch = shops[i:i + SHOP_BATCH_SIZE]

            try:
                await client.post(
                f"{UTCON_URL}/v1/raw/shops/record",
                json={"body": shop}
            )

                if r.status_code != 200:
                    print("[UCTE] shop error", r.status_code)
                    print(r.text)

            except Exception as e:
                print("[UCTE] shop push failed:", e)

            await asyncio.sleep(0.05)