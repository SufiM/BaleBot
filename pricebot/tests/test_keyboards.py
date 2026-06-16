from pricebot.services.keyboards import main_keyboard, single_asset_keyboard


def test_main_keyboard():

    keyboard = main_keyboard()

    assert keyboard.inline_keyboard[0][0].callback_data == "price_gold"
    assert keyboard.inline_keyboard[2][0].callback_data == "refresh_all"


def test_single_asset_keyboard():

    keyboard = single_asset_keyboard("usd")

    assert keyboard.inline_keyboard[0][0].callback_data == "refresh_usd"
    assert keyboard.inline_keyboard[1][0].callback_data == "main_list"