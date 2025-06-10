from flask import Flask, request
from threading import Thread
import stripe
import os
from dotenv import load_dotenv
from models.user_data_store import get_or_create_user

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = Flask('')

@app.route('/')
def home():
    return "FundingRadar Bot is running"

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return f"Webhook Error: {e}", 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = int(session['metadata']['user_id'])
        user = get_or_create_user(user_id)
        user.is_premium = True
        print(f"✅ User {user_id} upgraded to Premium")

    return '', 200

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
