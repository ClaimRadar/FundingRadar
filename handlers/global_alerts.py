from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from services.funding_data import get_dummy_funding_rates

async def send_global_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    funding_data = get_dummy_funding_rates()

    threshold = 0.01  # Free kullanıcılar için %1
    matched = []

    for item in funding_data:
        rate = item["funding_rate"]
        if abs(rate) >= threshold:
            matched.append(item)

    if not matched:
        await update.message.reply_text("📉 No significant funding rates above threshold at the moment.")
        return

    message = "📊 *Funding Rate Alerts*\n\n"
    for item in matched:
        symbol = item["symbol"]
        exchange = item["exchange"]
        rate = item["funding_rate"]
        rate_percent = rate * 100
        emoji = get_rate_emoji(rate_percent)
        color = "🟢" if rate > 0 else "🔴"

        message += f"{color} *{symbol}* on _{exchange}_ → {rate_percent:.2f}% {emoji}\n"

    await update.message.reply_text(message, parse_mode="Markdown")

def get_rate_emoji(rate_percent: float) -> str:
    """
    Converts rate % to emojis
    """
    if abs(rate_percent) >= 3.0:
        return "🔥🔥🔥"
    elif abs(rate_percent) >= 2.0:
        return "🔥🔥"
    elif abs(rate_percent) >= 1.0:
        return "🔥"
    else:
        return ""

global_alerts_handler = CommandHandler("alert", send_global_alert)
