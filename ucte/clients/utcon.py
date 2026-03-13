import requests
from ucte.config import UTCON_URL


def post_transactions(transactions):

    url = f"{UTCON_URL}/v1/raw/transactions/record"

    r = requests.post(url, json=transactions, timeout=30)

    if r.status_code != 200:
        print("[UCTE] transaction error", r.status_code)
        print(r.text)


def post_shops(shops):

    url = f"{UTCON_URL}/v1/raw/shop/record"

    r = requests.post(url, json=shops, timeout=120)

    if r.status_code != 200:
        print("[UCTE] shop error", r.status_code)
        print(r.text)