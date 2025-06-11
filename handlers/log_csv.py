from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import ADMIN_USER_ID
from telegram.constants import ChatAction
import os

LOG_CSV = "logs/alert_log.csv"

async def send_log_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    if not os.path.exists(LOG_CSV):
        await update.message.reply_text("📭 CSV file not found.")
        return

    await update.message.chat.send_action(action=ChatAction.UPLOAD_DOCUMENT)
    await update.message.reply_document(document=open(LOG_CSV, "rb"), filename="alert_log.csv")

log_csv_handler = CommandHandler("logcsv", send_log_csv)
