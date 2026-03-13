import requests
from ucte.config import SMP_API_BASE


def get_all_shops():

    url = f"{SMP_API_BASE}/quickshop/v1/getAllShops"

    r = requests.get(url, timeout=120)

    r.raise_for_status()

    return r.json()