from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import ADMIN_USER_ID
import json
import os

LOG_PATH = "logs/alert_log.json"

async def show_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to view the logs.")
        return

    if not os.path.exists(LOG_PATH):
        await update.message.reply_text("📭 No log file found.")
        return

    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    if not logs:
        await update.message.reply_text("📭 No alerts have been logged yet.")
        return

    # En son 5 logu al (çok büyükse Telegram engeller)
    latest = logs[-5:]
    messages = []

    for entry in latest:
        messages.append(
            f"📌 [{entry['timestamp'][:19]} UTC] {entry['coin']} on {entry['exchange']} → {entry['rate']:.2f}% (in {entry['funding_in']}m)\nUser: `{entry['user_id']}`"
        )

    await update.message.reply_text(
        "*Last 5 Funding Alerts:*\n\n" + "\n\n".join(messages),
        parse_mode="Markdown"
    )

log_handler = CommandHandler("log", show_logs)
