import pytest
from types import SimpleNamespace
from asgiref.sync import sync_to_async
from unittest.mock import AsyncMock, patch

from core.models import PlatformUser, BotInteraction, CommandStat
from pricebot.services.bot_handlers import (
    register_user,
    log_command,
    price,
    button,
    send_single_price,
)
from pricebot.services.price_api import PriceAPIError


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_register_user():
    tg_user = SimpleNamespace(
        id=1,
        username="tester",
    )

    user = await register_user(tg_user)

    assert user.bale_user_id == 1
    assert user.username == "tester"

    user_count = await sync_to_async(PlatformUser.objects.count)()

    assert user_count == 1


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_register_user_updates_existing_user():
    tg_user = SimpleNamespace(
        id=1,
        username="old_username",
    )

    user = await register_user(tg_user)

    assert user.username == "old_username"

    updated_tg_user = SimpleNamespace(
        id=1,
        username="new_username",
    )

    updated_user = await register_user(updated_tg_user)

    assert updated_user.id == user.id
    assert updated_user.username == "new_username"

    user_count = await sync_to_async(PlatformUser.objects.count)()

    assert user_count == 1


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_log_command(user):

    await log_command(user, "/start")

    interaction_count = await sync_to_async(BotInteraction.objects.count)()
    stat = await sync_to_async(CommandStat.objects.get)(command="/start")

    assert interaction_count == 1
    assert stat.count == 1


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_log_command_increments_existing_stat(user):

    await sync_to_async(BotInteraction.objects.all().delete)()
    await sync_to_async(CommandStat.objects.all().delete)()

    await log_command(user, "/price")
    await log_command(user, "/price")

    interaction_count = await sync_to_async(BotInteraction.objects.count)()
    stat = await sync_to_async(CommandStat.objects.get)(command="/price")

    assert interaction_count == 2
    assert stat.count == 2


@pytest.mark.django_db
@pytest.mark.asyncio
@patch("pricebot.services.bot_handlers.fetch_prices")
async def test_price_handler(mock_fetch_prices):
    mock_fetch_prices.return_value = {
        "gold": 100,
        "usd": 200,
        "eur": 300,
        "coin": 400,
    }

    message = AsyncMock()

    update = SimpleNamespace(
        effective_user=SimpleNamespace(
            id=1,
            username="tester",
        ),
        message=message,
    )

    context = SimpleNamespace()

    await price(update, context)

    message.reply_text.assert_called_once()

    call_kwargs = message.reply_text.call_args.kwargs

    assert "طلا" in call_kwargs["text"]
    assert "100" in call_kwargs["text"]
    assert "200" in call_kwargs["text"]
    assert call_kwargs["parse_mode"] == "Markdown"


@pytest.mark.django_db
@pytest.mark.asyncio
@patch("pricebot.services.bot_handlers.fetch_prices")
async def test_button_refresh_all(mock_fetch_prices):
    mock_fetch_prices.return_value = {
        "gold": 100,
        "usd": 200,
        "eur": 300,
        "coin": 400,
    }

    query = AsyncMock()
    query.data = "refresh_all"

    update = SimpleNamespace(
        effective_user=SimpleNamespace(
            id=1,
            username="tester",
        ),
        callback_query=query,
    )

    context = SimpleNamespace()

    await button(update, context)

    query.answer.assert_called_once()
    query.edit_message_text.assert_called_once()

    call_kwargs = query.edit_message_text.call_args.kwargs

    assert "طلا" in call_kwargs["text"]
    assert call_kwargs["parse_mode"] == "Markdown"


@pytest.mark.django_db
@pytest.mark.asyncio
@patch("pricebot.services.bot_handlers.fetch_prices")
async def test_button_single_asset_price(mock_fetch_prices):
    mock_fetch_prices.return_value = {
        "gold": 100,
        "usd": 200,
        "eur": 300,
        "coin": 400,
    }

    query = AsyncMock()
    query.data = "price_gold"

    update = SimpleNamespace(
        effective_user=SimpleNamespace(
            id=1,
            username="tester",
        ),
        callback_query=query,
    )

    context = SimpleNamespace()

    await button(update, context)

    query.answer.assert_called_once()
    query.edit_message_text.assert_called_once()

    call_kwargs = query.edit_message_text.call_args.kwargs

    assert "gold: 100" in call_kwargs["text"]
    assert call_kwargs["parse_mode"] == "Markdown"


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_button_unknown_callback():
    query = AsyncMock()
    query.data = "unknown_action"

    update = SimpleNamespace(
        effective_user=SimpleNamespace(id=1, username="tester"),
        callback_query=query,
    )

    await button(update, SimpleNamespace())

    query.answer.assert_called_once()
    query.edit_message_text.assert_not_called()


@pytest.mark.django_db
@pytest.mark.asyncio
@patch("pricebot.services.bot_handlers.fetch_prices", side_effect=PriceAPIError("down"))
async def test_send_single_price_api_failure(mock_fetch_prices):
    query = AsyncMock()
    update = SimpleNamespace(
        effective_user=SimpleNamespace(id=1, username="tester"),
        callback_query=query,
    )

    await send_single_price(update, SimpleNamespace(), "gold")

    call_kwargs = query.edit_message_text.call_args.kwargs
    assert "مشکلی" in call_kwargs["text"]
