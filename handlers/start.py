from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.keyboards import start_menu_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=(
            "👋 Welcome to *Funding Radar Bot*!\n\n"
            "This bot monitors funding rates across major exchanges like *Binance, Bybit, OKX,* and *MEXC*.\n\n"
            "Use the menu below to get started 👇"
        ),
        reply_markup=start_menu_keyboard(),
        parse_mode="Markdown"
    )

start_handler = CommandHandler("start", start)
