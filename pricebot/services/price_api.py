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
        response = requests.get(PRICE_API_URL, timeout=30)
        print(response)
        response.raise_for_status()
        data = response.json()
        print(data)
    
    except requests.exceptions.RequestException as exc:
        print("HTTP error:", exc)
        if hasattr(exc, "response") and exc.response is not None:
            print("Response body:", exc.response.text)
        raise PriceAPIError(f"Failed to fetch prices: {exc}")

    except ValueError as exc:
        print("JSON decode error:", exc)
        raise PriceAPIError(f"Invalid JSON response: {exc}")

    if not isinstance(data, list):
        print("Unexpected API response:", data)
        raise PriceAPIError("Invalid API format: expected list")

    price_map = {item.get("symbol"): item for item in data if "symbol" in item}

    def get_price(symbol):
        item = price_map.get(symbol)
        if not item:
            return None

        price = item.get("sell")
        if price is None:
            return None

        return int(float(price))

    return {name: get_price(symbol) for name, symbol in TARGET_SYMBOLS.items()}
