import requests
from ucte.config import SHOP_API


def get_all_shops():

    r = requests.get(SHOP_API, timeout=30)

    if r.status_code != 200:
        raise Exception("Shop API error")

    return r.json()