import asyncio
import httpx

from ucte.config import SMP_API_BASE, UTCON_URL, SHOP_BATCH_SIZE


async def run():
    print("[UCTE] Fetching shop snapshot")

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.get(f"{SMP_API_BASE}/quickshop/v1/getAllShops")
        resp.raise_for_status()
        shops = resp.json()

    print(f"[UCTE] Queued {len(shops)} shops")

    await push_shops(shops)


async def push_shops(shops):
    async with httpx.AsyncClient(timeout=120) as client:

        total = len(shops)

        for i in range(0, total, SHOP_BATCH_SIZE):

            batch = shops[i:i + SHOP_BATCH_SIZE]

            try:
                resp = await client.post(
                    f"{UTCON_URL}/v1/raw/shops/record",
                    json={"body": batch}
                )

                if resp.status_code != 200:
                    print("[UCTE] shop error", resp.status_code)
                    print(resp.text)

            except Exception as exc:
                print("[UCTE] shop push failed:", exc)

            await asyncio.sleep(0.05)