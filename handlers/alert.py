from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# örnek: funding alert datası buradan çağrılır
async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Bu kısımda gerçek funding verileri gösterilecek
    msg = (
        "📢 *Funding Alert*\n\n"
        "• BTC: +0.035% 🔥\n"
        "• ETH: -0.010% 🧊\n"
        "• SOL: +0.250% 🔥🔥🔥"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

alert_handler = CommandHandler("alert", alert)
