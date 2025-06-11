from telegram.ext import CommandHandler, ContextTypes
from telegram import Update

async def ask_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_coin_input"] = True
    await update.message.reply_text("🪙 Please enter coins to track (comma-separated):\ne.g. `BTC, ETH, PEPE`", parse_mode="Markdown")

async def ask_exchanges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_exchange_input"] = True
    await update.message.reply_text("💱 Please enter exchanges to filter:\ne.g. `Binance, OKX, Bybit`", parse_mode="Markdown")

async def ask_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_threshold_input"] = True
    await update.message.reply_text("📊 Enter your minimum threshold (e.g. `0.5` for 0.5%)")

ask_coins_handler = CommandHandler("setcoins", ask_coins)
ask_exchanges_handler = CommandHandler("setexchanges", ask_exchanges)
ask_threshold_handler = CommandHandler("setthreshold", ask_threshold)
