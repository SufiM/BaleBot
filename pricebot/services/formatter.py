def format_prices(prices):
    def clean(value):
        return value if value is not None else "N/A"

    return (
        "**  قیمت های لحظه ای  **\n\n"
        "  قیمت ها به تومان می باشد  \n\n"
        f" طلا:  {clean(prices['gold'])}\n"
        f" دلار:  {clean(prices['usd'])}\n"
        f" یورو:  {clean(prices['eur'])}\n"
        f" سکه:  {clean(prices['coin'])}\n"
    )
