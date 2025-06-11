from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from models.user_data_store import get_or_create_user
from services.funding_data import get_live_funding_data
from services.alert_logger import log_alert  # ✅ Log fonksiyonu

def format_minutes(mins):
    h = mins // 60
    m = mins % 60
    return f"{h}h {m}m" if h else f"{m}m"

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_or_create_user(user_id)

    data = get_live_funding_data()
    filtered = []

    for item in data:
        coin, exch, rate, mins = item.values()

        # coin filtresi (Premium)
        if user.coins and coin not in user.coins:
            continue

        # exchange filtresi (Premium)
        if user.exchanges and exch not in user.exchanges:
            continue

        # threshold filtresi
        if abs(rate) < user.threshold:
            continue

        # emoji
        if rate > 0:
            emoji = "🟢"
        elif rate < 0:
            emoji = "🔴"
        else:
            emoji = "⚪️"

        heat = "🔥" * (1 + int(abs(rate) * 10))  # 0.1 → 2x 🔥

        msg = f"{emoji} *{coin}* on *{exch}* → `{rate:.3f}%` {heat}"

        if user.countdown_enabled:
            msg += f" ⏳ in {format_minutes(mins)}"

        filtered.append(msg)

        # ✅ Log dosyasına yaz
        log_alert(user_id, coin, exch, rate, mins)

    if not filtered:
        await update.message.reply_text("📭 No alerts above your threshold.")
    else:
        await update.message.reply_text(
            "*Funding Rate Alerts:*\n\n" + "\n".join(filtered),
            parse_mode="Markdown"
        )

alert_handler = CommandHandler("alert", alert)
