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

# User Data
from models.user_data_store import get_all_user_ids

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
    except ValueError as e:
        print("❌ Invalid payload")
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        print("❌ Invalid signature")
        return 'Invalid signature', 400

    print("✅ Stripe Webhook geldi:", event['type'])

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("🟢 Ödeme tamamlandı:", session)

        # Burada kullanıcıya Telegram'dan mesaj gönderebilirsin

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

# Flask'ı ayrı thread'de başlat
def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

def main():
    # Telegram botu
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(start_handler)
    app.add_handler(callback_query_handler)
    app.add_handler(global_alerts_handler)
    app.add_handler(message_input_handler)

    keep_alive.keep_alive()

    app.job_queue.run_once(lambda ctx: asyncio.create_task(hourly_alert_task(app)), when=0)

    # Flask başlat
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    print("✅ FundingRadar Bot is running with webhook support...")
    app.run_polling()

if __name__ == "__main__":
    main()
