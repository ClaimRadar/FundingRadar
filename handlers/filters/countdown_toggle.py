from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from models.user_data_store import get_or_create_user

def countdown_toggle_keyboard(enabled):
    if enabled:
        btn = InlineKeyboardButton("❌ Disable Countdown", callback_data="disable_countdown")
    else:
        btn = InlineKeyboardButton("✅ Enable Countdown", callback_data="enable_countdown")
    return InlineKeyboardMarkup([[btn], [InlineKeyboardButton("🔙 Back", callback_data="settings")]])

async def countdown_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)

    await query.edit_message_text(
        "⏳ Countdown setting:",
        reply_markup=countdown_toggle_keyboard(user.countdown_enabled)
    )

async def toggle_countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = get_or_create_user(user_id)

    if query.data == "enable_countdown":
        user.countdown_enabled = True
        msg = "✅ Funding countdown is now *enabled*."
    elif query.data == "disable_countdown":
        user.countdown_enabled = False
        msg = "❌ Funding countdown is now *disabled*."
    else:
        msg = "⚠️ Unknown option."

    await query.edit_message_text(
        msg,
        parse_mode="Markdown",
        reply_markup=countdown_toggle_keyboard(user.countdown_enabled)
    )

countdown_menu_handler = CallbackQueryHandler(countdown_menu, pattern="^toggle_countdown_menu$")
toggle_countdown_handler = CallbackQueryHandler(toggle_countdown, pattern="^(enable_countdown|disable_countdown)$")
