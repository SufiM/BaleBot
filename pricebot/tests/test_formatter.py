from pricebot.services.formatter import format_prices


def test_format_prices():

    prices = {
        "gold": 100,
        "usd": 200,
        "eur": 300,
        "coin": 400,
    }

    text = format_prices(prices)

    assert "طلا" in text
    assert "دلار" in text
    assert "یورو" in text
    assert "سکه" in text
    assert "100" in text
    assert "200" in text
    assert "300" in text
    assert "400" in text


def test_format_prices_none_values():

    prices = {"gold": None, "usd": 200, "eur": None, "coin": 400}

    text = format_prices(prices)

    assert "N/A" in text
    assert "200" in text
