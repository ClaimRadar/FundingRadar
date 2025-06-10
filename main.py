from handlers.filters.coin_filter import coin_filter_entry_handler, coin_filter_toggle_handler
from handlers.filters.exchange_filter import exchange_filter_entry_handler, exchange_filter_toggle_handler

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram import BotCommand, MenuButtonCommands
from config import BOT_TOKEN
import keep_alive
import asyncio
import threading

# Stripe Webhook için Flask
from flask import Flask, request
import stripe
import os

# Handlers
from handlers.start import start_handler
from handlers.callback import callback_query_handler
from handlers.global_alerts import global_alerts_handler, send_global_alert
from handlers.message_input import message_input_handler

# ✅ Yeni Slash Command handler'ları
from handlers.profile import profile_handler
from handlers.settings import settings_handler
from handlers.help import help_handler
from handlers.premium import premium_handler
from handlers.alert import alert_handler

# User Data
from models.user_data_store import get_all_user_ids, get_or_create_user

# .env'den Stripe secret alınır
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

# Flask App (Webhook listener)
flask_app = Flask(__name__)

@flask_app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError:
        print("❌ Invalid payload")
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        print("❌ Invalid signature")
        return 'Invalid signature', 400

    print("✅ Stripe Webhook geldi:", event['type'])

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get("metadata", {})
        user_id = metadata.get("user_id")

        if user_id:
            user = get_or_create_user(int(user_id))
            user.is_premium = True
            print(f"💎 User {user_id} upgraded to Premium via Stripe!")
        else:
            print("⚠️ user_id not found in session metadata")

    return '', 200

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

# Komut menüsünü Telegram'a tanımla
async def setup_bot_menu(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("alert", "View funding alerts"),
        BotCommand("profile", "View your profile and plan"),
        BotCommand("settings", "Adjust preferences"),
        BotCommand("help", "How to use this bot"),
        BotCommand("premium", "Upgrade to premium"),
    ])
    await app.bot.set_chat_menu_button(menu_button=MenuButtonCommands())

# Flask'ı ayrı thread'de başlat
def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

def main():
    # Telegram botu
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Komut ve callback handler'lar
    app.add_handler(start_handler)
    app.add_handler(callback_query_handler)
    app.add_handler(global_alerts_handler)
    app.add_handler(message_input_handler)

    # ✅ Slash komut handler'ları
    app.add_handler(profile_handler)
    app.add_handler(settings_handler)
    app.add_handler(help_handler)
    app.add_handler(premium_handler)
    app.add_handler(alert_handler)
    app.add_handler(coin_filter_entry_handler)
    app.add_handler(coin_filter_toggle_handler)
    app.add_handler(exchange_filter_entry_handler)
    app.add_handler(exchange_filter_toggle_handler)
    app.add_handler(threshold_entry_handler)
    app.add_handler(threshold_input_handler)


    # Replit keep-alive
    keep_alive.keep_alive()

    # Saatlik funding kontrolü başlat
    app.job_queue.run_once(lambda ctx: asyncio.create_task(hourly_alert_task(app)), when=0)

    # Slash komutları ve menu butonu yükle
    app.post_init = setup_bot_menu

    # Flask webhook başlat
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    print("✅ FundingRadar Bot is running with menu, webhook, and alert support...")
    app.run_polling()

if __name__ == "__main__":
    main()
