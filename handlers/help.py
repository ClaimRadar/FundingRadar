from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "❓ *How to Use FundingRadar Bot*\n\n"
        "• `/start` - Launch the bot\n"
        "• `/alert` - Trigger a funding alert now\n"
        "• `/profile` - View your plan and filters\n"
        "• `/settings` - Change filters and preferences\n"
        "• `/premium` - Upgrade for real-time alerts\n"
        "\nNeed help? Just type /help anytime."
    )

    await update.message.reply_text(msg, parse_mode="Markdown")

help_handler = CommandHandler("help", help_command)
