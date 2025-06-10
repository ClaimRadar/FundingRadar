from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from utils.keyboards import (
    start_menu_keyboard,
    main_menu_keyboard,
    customize_filters_keyboard
)
from models.user_data_store import get_or_create_user

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    await query.answer()

    user = get_or_create_user(user_id)

    if data == "main_menu":
        await query.edit_message_text(
            "📊 Main Menu:",
            reply_markup=main_menu_keyboard()
        )

    elif data == "premium_menu":
        await query.edit_message_text(
            "💎 Premium Features:\n\n"
            "• Real-time alerts\n"
            "• Custom thresholds\n"
            "• Exchange & token filters\n"
            "• Funding countdowns\n\n"
            "Coming soon...",
            parse_mode="Markdown"
        )

    elif data == "global_alerts":
        await query.edit_message_text(
            "📢 Global alerts will be sent hourly.\nUse /alert anytime for instant check."
        )

    elif data == "customize_filters":
        if not user.is_premium:
            await query.edit_message_text("🔒 This feature is available for Premium users only.")
            return
        await query.edit_message_text(
            "🛠 Customize your tracking filters:",
            reply_markup=customize_filters_keyboard()
        )

    elif data == "select_coins":
        await query.edit_message_text("📝 Enter coins you want to track (comma-separated): e.g. BTC,ETH")
        context.user_data["awaiting_coin_input"] = True

    elif data == "select_exchanges":
        await query.edit_message_text("📝 Enter exchanges to follow (comma-separated): e.g. Binance,Bybit")
        context.user_data["awaiting_exchange_input"] = True

    elif data == "set_threshold":
        await query.edit_message_text("🔢 Enter your custom threshold (e.g. 0.25 for 0.25%)")
        context.user_data["awaiting_threshold_input"] = True

    elif data == "my_filters":
        coins = ", ".join(user.coins) if user.coins else "All"
        exchanges = ", ".join(user.exchanges) if user.exchanges else "All"
        threshold = f"{user.threshold:.2f}%"
        countdown = "Enabled ✅" if user.countdown_enabled else "Disabled ❌"

        msg = (
            "🔍 *Your Current Filters:*\n\n"
            f"• Coins: `{coins}`\n"
            f"• Exchanges: `{exchanges}`\n"
            f"• Threshold: `{threshold}`\n"
            f"• Countdown: `{countdown}`"
        )

        await query.edit_message_text(msg, parse_mode="Markdown")

callback_query_handler = CallbackQueryHandler(handle_callback)
