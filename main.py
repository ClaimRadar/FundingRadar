from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
import keep_alive

# Komutları getiriyoruz
from handlers.start import start_handler
from handlers.callback import callback_query_handler
from handlers.global_alerts import global_alerts_handler  # ✅ BURAYA EKLE

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Komutları tanıt
    app.add_handler(start_handler)
    app.add_handler(callback_query_handler)
    app.add_handler(global_alerts_handler)  # ✅ BURAYA DA EKLE

    # Replit'te 7/24 çalıştırma
    keep_alive.keep_alive()

    print("✅ FundingRadar Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
