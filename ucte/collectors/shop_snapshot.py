import asyncio
import httpx
import sys
from typing import List

from ucte.config import SMP_API_BASE, UTCON_URL, SHOP_BATCH_SIZE, SHOP_SYNC_INTERVAL
from ucte.processors.normalize_shops import normalize_shop


SNAPSHOT_TIMEOUT = 120
RETRY_MIN_SECONDS = 15
RETRY_MAX_SECONDS = 300


async def fetch_snapshot() -> List[dict]:
    print("[UCTE] Fetching shop snapshot")

    async with httpx.AsyncClient(timeout=SNAPSHOT_TIMEOUT) as client:
        resp = await client.get(f"{SMP_API_BASE}/quickshop/v1/getAllShops")
        resp.raise_for_status()
        shops = resp.json()

    normalized = [normalize_shop(shop) for shop in shops]
    print(f"[UCTE] Queued {len(normalized)} shops")
    return normalized


async def run_once() -> bool:
    """
    Attempt one full snapshot cycle.
    Returns True on success, False on failure.
    """
    try:
        shops = await fetch_snapshot()
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        body = ""
        try:
            body = exc.response.text if exc.response is not None else ""
        except Exception:
            body = ""
        print(f"[UCTE] shop snapshot HTTP error {status}")
        if body:
            print(body[:1000])
        return False
    except Exception as exc:
        print(f"[UCTE] shop snapshot failed: {exc}")
        return False

    pushed = await push_all_once(shops)
    if not pushed:
        await push_in_batches(shops)

    return True


async def run_forever():
    """
    Keep snapshots running forever.
    Snapshot failures should not kill UCTE.
    """
    retry_delay = RETRY_MIN_SECONDS

    # Try one immediately on startup
    while True:
        ok = await run_once()

        if ok:
            retry_delay = RETRY_MIN_SECONDS
            print(f"[UCTE] Next shop snapshot in {SHOP_SYNC_INTERVAL}s")
            await asyncio.sleep(SHOP_SYNC_INTERVAL)
        else:
            print(f"[UCTE] Retrying shop snapshot in {retry_delay}s")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, RETRY_MAX_SECONDS)


async def push_all_once(shops: List[dict]) -> bool:
    print("[UCTE] Attempting single bulk upload of shops to UTCON")

    async with httpx.AsyncClient(timeout=SNAPSHOT_TIMEOUT) as client:
        try:
            resp = await client.post(
                f"{UTCON_URL}/v1/raw/shops/record",
                json=shops,
                headers={"Content-Type": "application/json"},
                timeout=SNAPSHOT_TIMEOUT,
            )

            if resp.status_code == 200:
                print("[UCTE] Snapshot pushed (single request)")
                return True

            print("[UCTE] shop error", resp.status_code)
            try:
                print(resp.json())
            except Exception:
                print(resp.text)
            return False

        except Exception as exc:
            print("[UCTE] shop push failed (single):", exc)
            return False


async def push_in_batches(shops: List[dict]):
    print(f"[UCTE] Falling back to batched upload (size={SHOP_BATCH_SIZE})")
    total = len(shops)

    async with httpx.AsyncClient(timeout=SNAPSHOT_TIMEOUT) as client:
        for i in range(0, total, SHOP_BATCH_SIZE):
            batch = shops[i:i + SHOP_BATCH_SIZE]

            try:
                resp = await client.post(
                    f"{UTCON_URL}/v1/raw/shops/record",
                    json=batch,
                    headers={"Content-Type": "application/json"},
                    timeout=SNAPSHOT_TIMEOUT,
                )

                if resp.status_code != 200:
                    print("[UCTE] shop error", resp.status_code)
                    try:
                        print(resp.json())
                    except Exception:
                        print(resp.text)
                else:
                    print(f"[UCTE] batch {i}-{i + len(batch) - 1} pushed ({len(batch)} items)")

            except Exception as exc:
                print("[UCTE] shop push failed:", exc)

            await asyncio.sleep(0.02)


# Backward-compatible old entry name if anything imports run directly
async def run():
    return await run_once()


if __name__ == "__main__":
    try:
        asyncio.run(run_forever())
    except KeyboardInterrupt:
        sys.exit(0)