from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from models.user_data_store import get_or_create_user

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_or_create_user(user_id)

    coins = ", ".join(user.coins) if user.coins else "All"
    exchanges = ", ".join(user.exchanges) if user.exchanges else "All"
    threshold = f"{user.threshold:.2f}%"
    countdown = "Enabled ✅" if user.countdown_enabled else "Disabled ❌"
    premium = "💎 Yes (Premium)" if user.is_premium else "🆓 No (Free)"

    msg = (
        f"👤 *Your Profile*\n\n"
        f"• User ID: `{user_id}`\n"
        f"• Plan: {premium}\n"
        f"• Coins: `{coins}`\n"
        f"• Exchanges: `{exchanges}`\n"
        f"• Threshold: `{threshold}`\n"
        f"• Countdown: {countdown}"
    )

    await update.message.reply_text(msg, parse_mode="Markdown")

profile_handler = CommandHandler("profile", profile)
