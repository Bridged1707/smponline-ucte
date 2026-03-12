import asyncio


async def run_periodic(task, interval):

    while True:

        try:
            await task()

        except Exception as e:
            print(f"[UCTE] Task error: {e}")

        await asyncio.sleep(interval)