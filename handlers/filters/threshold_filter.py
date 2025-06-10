from telegram import Update
from telegram.ext import CallbackQueryHandler, MessageHandler, ContextTypes, filters
from models.user_data_store import get_or_create_user

# Inline buttonla başlatılır
async def threshold_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    context.user_data["awaiting_threshold_input"] = True

    await query.edit_message_text(
        "🔢 Please enter your custom threshold (example: 0.25 for 0.25%)"
    )

# Kullanıcının gönderdiği mesaj işlenir
async def threshold_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_or_create_user(user_id)

    if context.user_data.get("awaiting_threshold_input"):
        try:
            value = float(update.message.text.strip())
            user.threshold = value
            context.user_data["awaiting_threshold_input"] = False

            await update.message.reply_text(
                f"✅ Your threshold has been set to `{value:.2f}%`",
                parse_mode="Markdown"
            )
        except ValueError:
            await update.message.reply_text("❌ Invalid number. Please try again (e.g., 0.25)")

threshold_entry_handler = CallbackQueryHandler(threshold_entry, pattern="^set_threshold$")
threshold_input_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), threshold_input)
