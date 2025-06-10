import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

DOMAIN = os.getenv("BOT_DOMAIN")  # örnek: https://fundingradar.replit.app

def create_checkout_session(user_id):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': os.getenv("STRIPE_PRICE_ID"),  # Stripe Dashboard’dan aldığın
                'quantity': 1
            }],
            success_url=f"{DOMAIN}/success?user_id={user_id}",
            cancel_url=f"{DOMAIN}/cancel",
            metadata={"user_id": user_id}
        )
        return session.url
    except Exception as e:
        print(f"Stripe Checkout error: {e}")
        return None
