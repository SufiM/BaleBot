import pytest
from unittest.mock import patch

from pricebot.services.price_api import fetch_prices, PriceAPIError


MOCK_API_RESPONSE = {
    "result": [
        {"key": 137120, "price": 100},
        {"key": 137202, "price": 200},
        {"key": 137204, "price": 300},
        {"key": 137137, "price": 400},
    ]
}


@patch("pricebot.services.price_api.requests.get")
def test_fetch_prices_success(mock_get):

    mock_get.return_value.json.return_value = MOCK_API_RESPONSE
    mock_get.return_value.raise_for_status.return_value = None

    prices = fetch_prices()

    assert prices["gold"] == 100
    assert prices["usd"] == 200
    assert prices["eur"] == 300
    assert prices["coin"] == 400

@patch("pricebot.services.price_api.requests.get")
def test_fetch_prices_failure(mock_get):

    mock_get.side_effect = Exception("API down")

    with pytest.raises(PriceAPIError):
        fetch_prices()