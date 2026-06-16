from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard():

    keyboard = [
        [InlineKeyboardButton("طلا", callback_data="price_gold"),
         InlineKeyboardButton("دلار", callback_data="price_usd")],
        [InlineKeyboardButton("یورو", callback_data="price_eur"),
         InlineKeyboardButton("سکه", callback_data="price_coin")],
        [InlineKeyboardButton(" به‌روزرسانی کلی", callback_data="refresh_all")]
    ]
    return InlineKeyboardMarkup(keyboard)

def single_asset_keyboard(asset):

    keyboard = [
        [InlineKeyboardButton(f" به‌روزرسانی", callback_data=f"refresh_{asset}")],
        [InlineKeyboardButton(" بازگشت به لیست", callback_data="main_list")]
    ]
    return InlineKeyboardMarkup(keyboard)