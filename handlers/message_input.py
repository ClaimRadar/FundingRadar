from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from models.user_data_store import get_or_create_user

async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_or_create_user(user_id)
    text = update.message.text.strip()

    # COIN INPUT
    if context.user_data.get("awaiting_coin_input"):
        coins = [coin.strip().upper() for coin in text.split(",") if coin.strip()]
        user.coins = coins
        context.user_data["awaiting_coin_input"] = False
        await update.message.reply_text(f"✅ Coins updated: {', '.join(coins)}")

    # EXCHANGE INPUT
    elif context.user_data.get("awaiting_exchange_input"):
        exchanges = [ex.strip().capitalize() for ex in text.split(",") if ex.strip()]
        user.exchanges = exchanges
        context.user_data["awaiting_exchange_input"] = False
        await update.message.reply_text(f"✅ Exchanges updated: {', '.join(exchanges)}")

    # THRESHOLD INPUT
    elif context.user_data.get("awaiting_threshold_input"):
        try:
            threshold = float(text)
            user.threshold = threshold
            context.user_data["awaiting_threshold_input"] = False
            await update.message.reply_text(f"✅ Threshold updated to {threshold:.2f}%")
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number like 0.25")

message_input_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input)
