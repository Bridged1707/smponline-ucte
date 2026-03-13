# ucte/collectors/shop_snapshot.py
import asyncio
import httpx
import sys
from typing import List

from ucte.config import SMP_API_BASE, UTCON_URL, SHOP_BATCH_SIZE


async def run():
    """Entry point called by ucte main to fetch the QuickShop snapshot and push it to UTCON."""
    print("[UCTE] Fetching shop snapshot")

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.get(f"{SMP_API_BASE}/quickshop/v1/getAllShops")
        resp.raise_for_status()
        shops = resp.json()

    print(f"[UCTE] Queued {len(shops)} shops")

    # Try to push everything in one request (best).
    pushed = await push_all_once(shops)

    # If that didn't succeed, fall back to batch-mode.
    if not pushed:
        await push_in_batches(shops)


async def push_all_once(shops: List[dict]) -> bool:
    """
    Try to push the entire snapshot in one request.
    Returns True on success, False on failure (so caller can fall back to batching).
    """
    print("[UCTE] Attempting single bulk upload of shops to UTCON")

    async with httpx.AsyncClient(timeout=120) as client:
        try:
            resp = await client.post(
                f"{UTCON_URL}/v1/raw/shops/record",
                json={"body": shops},
                headers={"Content-Type": "application/json"},
                timeout=120
            )

            if resp.status_code == 200:
                print("[UCTE] Snapshot pushed (single request)")
                return True

            # Not 200 — print details and signal failure
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
    """Send shops to UTCON in batches (safe fallback)."""
    print("[UCTE] Falling back to batched upload (size=%s)" % SHOP_BATCH_SIZE)
    total = len(shops)
    async with httpx.AsyncClient(timeout=120) as client:

        for i in range(0, total, SHOP_BATCH_SIZE):
            batch = shops[i : i + SHOP_BATCH_SIZE]

            try:
                resp = await client.post(
                    f"{UTCON_URL}/v1/raw/shops/record",
                    json={"body": batch},
                    headers={"Content-Type": "application/json"},
                    timeout=120
                )

                if resp.status_code != 200:
                    # log full response for debugging
                    print("[UCTE] shop error", resp.status_code)
                    try:
                        print(resp.json())
                    except Exception:
                        print(resp.text)

                else:
                    # small progress log per batch
                    print(f"[UCTE] batch {i}-{i+len(batch)-1} pushed ({len(batch)} items)")

            except Exception as exc:
                # this prints the name 'shop' is not defined errors as well
                print("[UCTE] shop push failed:", exc)

            # small delay to avoid hammering UTCON — adjust if needed
            await asyncio.sleep(0.02)


# for local debugging / quick manual run
if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        sys.exit(0)