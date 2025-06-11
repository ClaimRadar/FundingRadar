from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import ADMIN_USER_ID
from telegram.constants import ChatAction
from analytics.graph import generate_weekly_graph

async def send_graph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    await update.message.chat.send_action(action=ChatAction.UPLOAD_PHOTO)

    path = generate_weekly_graph()
    if path:
        await update.message.reply_photo(photo=open(path, 'rb'))
    else:
        await update.message.reply_text("📭 No data available to generate graph.")

graph_handler = CommandHandler("graph", send_graph)
