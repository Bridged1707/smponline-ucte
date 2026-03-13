import requests

from ucte.core.config import UTCON_API_URL


def post_transaction(event: dict):

    url = f"{UTCON_API_URL}/v1/raw/transactions/record"

    try:

        r = requests.post(url, json=event, timeout=10)

        if r.status_code != 200:
            print(f"[UCTE] UTCON transaction error: {r.text}")

    except Exception as e:
        print(f"[UCTE] Failed sending transaction: {e}")


def post_shops(shops: list):

    url = f"{UTCON_API_URL}/v1/raw/shop/record"

    try:

        r = requests.post(url, json={"shops": shops}, timeout=30)

        if r.status_code != 200:
            print(f"[UCTE] UTCON shop error: {r.text}")

    except Exception as e:
        print(f"[UCTE] Failed sending shop snapshot: {e}")