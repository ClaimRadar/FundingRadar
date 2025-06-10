from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from models.user_data_store import get_or_create_user

EXCHANGE_LIST = ["Binance", "Bybit", "OKX", "MEXC"]

def build_exchange_keyboard(selected):
    keyboard = []
    for exch in EXCHANGE_LIST:
        label = f"✅ {exch}" if exch in selected else exch
        keyboard.append([InlineKeyboardButton(label, callback_data=f"toggle_exchange:{exch}")])
    keyboard.append([InlineKeyboardButton("✅ Confirm", callback_data="confirm_exchanges")])
    return InlineKeyboardMarkup(keyboard)

async def exchange_filter_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)

    await query.edit_message_text(
        "🏦 Select the exchanges you want to follow:",
        reply_markup=build_exchange_keyboard(user.exchanges)
    )

async def exchange_filter_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)
    data = query.data

    if data.startswith("toggle_exchange:"):
        exch = data.split(":")[1]
        if exch in user.exchanges:
            user.exchanges.remove(exch)
        else:
            user.exchanges.append(exch)

        await query.edit_message_reply_markup(
            reply_markup=build_exchange_keyboard(user.exchanges)
        )

    elif data == "confirm_exchanges":
        await query.edit_message_text(
            f"✅ Exchange filters updated:\n`{', '.join(user.exchanges) or 'All'}`",
            parse_mode="Markdown"
        )

exchange_filter_entry_handler = CallbackQueryHandler(exchange_filter_entry, pattern="^select_exchanges$")
exchange_filter_toggle_handler = CallbackQueryHandler(exchange_filter_callback, pattern="^(toggle_exchange:|confirm_exchanges)")
