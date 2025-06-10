from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def start_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🚀 Get Started", callback_data="main_menu")],
        [InlineKeyboardButton("💸 Premium Plans", callback_data="premium_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
