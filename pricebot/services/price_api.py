import requests
from decouple import config

PRICE_API_URL = config("PRICE_API_URL")

TARGET_SYMBOLS = {
    "usd": "USD",
    "eur": "EUR",
    "coin": "EMAMI1",
    "gold": "GOL18",
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

    if not isinstance(data, list):
        raise PriceAPIError("Invalid API format: expected list")

    price_map = {item.get("symbol"): item for item in data if "symbol" in item}

    def get_price(symbol):
        item = price_map.get(symbol)
        if not item:
            return None
        return item.get("sell")

    return {name: get_price(symbol) for name, symbol in TARGET_SYMBOLS.items()}
