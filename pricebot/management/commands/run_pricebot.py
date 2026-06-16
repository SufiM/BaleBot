from django.core.management.base import BaseCommand
from decouple import config
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from pricebot.services.bot_handlers import start, price, button


class Command(BaseCommand):
    help = "Run the Bale Price Bot"

    def handle(self, *args, **kwargs):

        token = config("PRICEBOT_TOKEN").strip()

        app = (
            Application.builder()
            .token(token)
            .base_url("https://tapi.bale.ai/bot")
            .build()
        )

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("price", price))
        app.add_handler(CallbackQueryHandler(button))

        self.stdout.write(self.style.SUCCESS("PriceBot is running on Bale..."))
        app.run_polling()
