from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.keyboards import settings_menu_keyboard

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚙️ Settings Menu:",
        reply_markup=settings_menu_keyboard()
    )

settings_handler = CommandHandler("settings", settings)
