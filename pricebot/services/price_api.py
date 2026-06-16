import requests
from decouple import config

PRICE_API_URL = config("PRICE_API_URL")

TARGET_KEYS = {
    "gold": 137120,
    "usd": 137202,
    "eur": 137204,
    "coin": 137137,
}


class PriceAPIError(Exception):
    pass


def fetch_prices():
    try:
        response = requests.get(PRICE_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        raise PriceAPIError(f"Failed to fetch prices: {exc}")

    items = data.get("result", [])
    if not isinstance(items, list):
        raise PriceAPIError("Invalid API format: 'result' is not a list")

    found = {}
    for item in items:
        key = item.get("key")
        if key in TARGET_KEYS.values():
            found[key] = item

    def get_by_key(target_key):
        item = found.get(target_key)
        if not item:
            return None
        return item.get("price")

    return {name: get_by_key(key) for name, key in TARGET_KEYS.items()}
