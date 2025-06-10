from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from config import BOT_TOKEN
import keep_alive
import asyncio

# Handlers
from handlers.start import start_handler
from handlers.callback import callback_query_handler
from handlers.global_alerts import global_alerts_handler, send_global_alert
from handlers.message_input import message_input_handler

# User Data
from models.user_data_store import get_all_user_ids

# Saatlik görev
async def hourly_alert_task(app):
    while True:
        await asyncio.sleep(3600)  # Her 1 saatte bir
        user_ids = get_all_user_ids()
        for user_id in user_ids:
            try:
                await app.bot.send_message(
                    chat_id=user_id,
                    text="⏰ Hourly funding check:\nUse /alert to see the latest rates."
                )
            except Exception as e:
                print(f"❌ Error sending to {user_id}: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Bot komutları ve mesajlar
    app.add_handler(start_handler)
    app.add_handler(callback_query_handler)
    app.add_handler(global_alerts_handler)
    app.add_handler(message_input_handler)

    # Replit keep-alive
    keep_alive.keep_alive()

    # Saatlik loop başlat
    app.job_queue.run_once(lambda ctx: asyncio.create_task(hourly_alert_task(app)), when=0)

    print("✅ FundingRadar Bot is running with all features active...")
    app.run_polling()

if __name__ == "__main__":
    main()
