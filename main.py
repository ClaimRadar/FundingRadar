from telegram.ext import ApplicationBuilder, ContextTypes
from config import BOT_TOKEN
import keep_alive

# Handlers
from handlers.start import start_handler
from handlers.callback import callback_query_handler
from handlers.global_alerts import global_alerts_handler, send_global_alert  # ✅

import asyncio

async def hourly_alert_task(app):
    while True:
        await asyncio.sleep(3600)  # 1 saat bekle
        for user_id in get_all_free_user_ids():  # Tüm kullanıcı ID'lerini çek (dummy)
            try:
                await app.bot.send_message(chat_id=user_id, text="⏰ Hourly funding check:\n(use /alert to see latest rates)")
            except Exception as e:
                print(f"Error sending to {user_id}: {e}")

def get_all_free_user_ids():
    # Şimdilik sabit değer (test amaçlı)
    return [123456789]  # Kendi Telegram user_id'n ile test et

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command Handlers
    app.add_handler(start_handler)
    app.add_handler(callback_query_handler)
    app.add_handler(global_alerts_handler)

    # Replit Keep Alive
    keep_alive.keep_alive()

    # Job başlat
    app.job_queue.run_once(lambda ctx: asyncio.create_task(hourly_alert_task(app)), when=0)

    print("✅ FundingRadar Bot is running with hourly alert loop...")
    app.run_polling()

if __name__ == "__main__":
    main()
