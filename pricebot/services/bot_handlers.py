import logging

from django.utils import timezone
from asgiref.sync import sync_to_async

from core.models import PlatformUser, BotInteraction, CommandStat
from pricebot.services.price_api import fetch_prices, PriceAPIError
from pricebot.services.formatter import format_prices
from pricebot.services.keyboards import main_keyboard, single_asset_keyboard

from decouple import config


logger = logging.getLogger(__name__)

BOT_NAME = config("BOT_NAME")


async def register_user(tg_user):
    user, created = await sync_to_async(PlatformUser.objects.get_or_create)(
        bale_user_id=tg_user.id,
        defaults={
            "username": tg_user.username,
            "first_seen": timezone.now(),
            "last_seen": timezone.now(),
        },
    )

    if not created:
        user.username = tg_user.username
        user.last_seen = timezone.now()
        await sync_to_async(user.save)(update_fields=["username", "last_seen"])

    return user


async def log_command(user, command):
    await sync_to_async(BotInteraction.objects.create)(
        bot_name=BOT_NAME,
        user=user,
        command=command,
    )
    await sync_to_async(CommandStat.increment)(BOT_NAME, command)


async def send_prices(update, context, is_edit=False):
    try:
        prices = await sync_to_async(fetch_prices)()
        text = format_prices(prices)
    except PriceAPIError:
        logger.warning("Failed to fetch prices for user %s", update.effective_user.id)
        text = "مشکلی پیش آمده است .لطفا دوباره تلاش کنید."

    if is_edit:
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=main_keyboard(),
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=main_keyboard(),
            parse_mode="Markdown",
        )


async def start(update, context):
    user = await register_user(update.effective_user)
    await log_command(user, "/start")

    help_text = (
        "سلام! به ربات قیمت‌های طلا و ارز خوش آمدید. \n\n"
        "شما می‌توانید با استفاده از دکمه‌های زیر قیمت‌ها را مشاهده کنید.\n"
        "برای مشاهده لیست کامل از /price استفاده کنید."
    )
    await update.message.reply_text(
        help_text,
        reply_markup=main_keyboard(),
    )


async def price(update, context):
    user = await register_user(update.effective_user)
    await log_command(user, "/price")

    await send_prices(update, context)


async def send_single_price(update, context, asset, is_edit=True):
    try:
        prices = await sync_to_async(fetch_prices)()
    except PriceAPIError:
        logger.warning("Failed to fetch price for asset %s", asset)
        text = "مشکلی پیش آمده است .لطفا دوباره تلاش کنید."
    else:
        price_value = prices.get(asset, "نامشخص")
        text = f"قیمت فعلی {asset}: {price_value}"

    if is_edit:
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=single_asset_keyboard(asset),
            parse_mode="Markdown",
        )


async def button(update, context):
    query = update.callback_query
    await query.answer()

    user = await register_user(update.effective_user)
    data = query.data
    await log_command(user, f"callback:{data}")

    if data == "refresh_all" or data == "main_list":
        await send_prices(update, context, is_edit=True)

    elif data.startswith(("price_", "refresh_")):
        asset = data.split("_", 1)[1]
        await send_single_price(update, context, asset, is_edit=True)

    else:
        logger.warning("Unknown callback data: %s", data)
