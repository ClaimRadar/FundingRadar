from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from services.stripe_checkout import create_checkout_session

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    url = create_checkout_session(user_id)

    if url:
        msg = f"💳 Click to upgrade your plan:\n{url}"
    else:
        msg = "❌ Error creating Stripe checkout session."

    await update.message.reply_text(msg)

premium_handler = CommandHandler("premium", premium)
