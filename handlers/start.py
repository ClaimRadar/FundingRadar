from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.keyboards import start_menu_keyboard
from models.user_data_store import get_or_create_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_or_create_user(user_id)  # Kullanıcıyı belleğe al

    await update.message.reply_text(
        text=(
            "👋 Welcome to *Funding Radar Bot*!\n\n"
            "This bot monitors funding rates across major exchanges like *Binance, Bybit, OKX,* and *MEXC*.\n\n"
            "Use the menu below to get started 👇"
        ),
        reply_markup=start_menu_keyboard(),  # ✅ BUTONLAR BURADA
        parse_mode="Markdown"
    )

start_handler = CommandHandler("start", start)
