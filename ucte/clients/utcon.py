import requests
from ucte.config import UTCON_URL


def post_transaction(event):

    url = f"{UTCON_URL}/v1/raw/transactions/record"

    try:
        r = requests.post(url, json=event, timeout=10)

        if r.status_code != 200:
            print(f"[UCTE] UTCON transaction error {r.status_code}")

    except Exception as e:
        print(f"[UCTE] UTCON connection error: {e}")


def post_shops(shops):

    url = f"{UTCON_URL}/v1/raw/shop/record"

    try:
        r = requests.post(url, json={"shops": shops}, timeout=30)

        if r.status_code != 200:
            print(f"[UCTE] UTCON shop error {r.status_code}")

    except Exception as e:
        print(f"[UCTE] UTCON shop error: {e}")