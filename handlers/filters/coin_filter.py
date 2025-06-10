from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from models.user_data_store import get_or_create_user

COIN_LIST = ["BTC", "ETH", "SOL", "PEPE", "XRP", "DOGE"]

def build_coin_keyboard(selected):
    keyboard = []
    for coin in COIN_LIST:
        if coin in selected:
            label = f"✅ {coin}"
        else:
            label = coin
        keyboard.append([InlineKeyboardButton(label, callback_data=f"toggle_coin:{coin}")])
    keyboard.append([InlineKeyboardButton("✅ Confirm", callback_data="confirm_coins")])
    return InlineKeyboardMarkup(keyboard)

async def coin_filter_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)

    await query.edit_message_text(
        "🪙 Select which coins to receive alerts for:",
        reply_markup=build_coin_keyboard(user.coins)
    )

async def coin_filter_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)

    data = query.data

    if data.startswith("toggle_coin:"):
        coin = data.split(":")[1]
        if coin in user.coins:
            user.coins.remove(coin)
        else:
            user.coins.append(coin)

        await query.edit_message_reply_markup(
            reply_markup=build_coin_keyboard(user.coins)
        )

    elif data == "confirm_coins":
        await query.edit_message_text(
            f"✅ Coin filters updated:\n`{', '.join(user.coins) or 'All'}`",
            parse_mode="Markdown"
        )

coin_filter_entry_handler = CallbackQueryHandler(coin_filter_entry, pattern="^select_coins$")
coin_filter_toggle_handler = CallbackQueryHandler(coin_filter_callback, pattern="^(toggle_coin:|confirm_coins)")
