from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
import keep_alive
from handlers.start import start_handler
from handlers.callback import callback_query_handler

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(start_handler)
    app.add_handler(callback_query_handler)

    # Keep alive (for Replit)
    keep_alive.keep_alive()

    print("✅ FundingRadar Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
