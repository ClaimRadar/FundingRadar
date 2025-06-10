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
# Gerekirse: from handlers.profile import profile_handler

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

    print("✅ Stripe Webhook received:", event['type'])

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

# Saatlik görev (her 1 saatte bir funding alarm)
async def hourly_alert_task(app):
    while True:
        await asyncio.sleep(3600)
        user_ids = get_all_user_ids()
        for user_id in user_ids:
            try:
                await app.bot.send_message(
                    chat_id=user_id,
                    text="⏰ Hourly funding check:\nUse /alert to see the latest rates."
                )
            except Exception as e:
                print(f"❌ Error sending to {user_id}: {e}")

# Komut menüsünü ayarla
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

# Flask'ı ayrı bir thread'de çalıştır
def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Telegram handlers
    app.add_handler(start_handler)
    app.add_handler(callback_query_handler)
    app.add_handler(global_alerts_handler)
    app.add_handler(message_input_handler)
    # Gerekirse: app.add_handler(profile_handler)

    # Keep alive
    keep_alive.keep_alive()

    # Saatlik funding kontrolü başlat
    app.job_queue.run_once(lambda ctx: asyncio.create_task(hourly_alert_task(app)), when=0)

    # Slash komutları ve menu button'u Telegram'a yükle
    app.post_init = setup_bot_menu

    # Flask webhook başlat
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    print("✅ FundingRadar Bot is live with Stripe, commands, menu and alerts.")
    app.run_polling()

if __name__ == "__main__":
    main()
