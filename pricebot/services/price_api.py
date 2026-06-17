import requests
from decouple import config

PRICE_API_URL = config("PRICE_API_URL")
PRICE_API_KEY = config("PRICE_API_KEY")


class PriceAPIError(Exception):
    pass


def _to_int(value):
    if value is None:
        return None
    return int(value)


def fetch_prices():
    headers = {
        "Authorization": f"Bearer {PRICE_API_KEY}",
        "Accept": "application/json",
    }

    try:
        response = requests.get(
            PRICE_API_URL,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()

    except Exception as exc:
        raise PriceAPIError(f"Failed to fetch prices: {exc}")

    try:
        data = payload["data"]

        prices = {
            "gold": _to_int(data["gold"]["GOLD18K"]["current"]),
            "coin": _to_int(data["gold"]["SEKE_EMAMI"]["current"]),
            "usd": _to_int(data["currency"]["USD"]["current"]),
            "eur": _to_int(data["currency"]["EUR"]["current"]),
        }

        return prices

    except KeyError as exc:
        raise PriceAPIError(
            f"Unexpected API format, missing field: {exc}. "
        )
