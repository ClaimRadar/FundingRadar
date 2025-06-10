from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def start_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Get Started", callback_data="main_menu")],
        [InlineKeyboardButton("💸 Premium Plans", callback_data="premium_menu")]
    ])

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1️⃣ Global Alerts", callback_data="global_alerts")],
        [InlineKeyboardButton("2️⃣ Customize Filters", callback_data="customize_filters")],
        [InlineKeyboardButton("3️⃣ My Filters", callback_data="my_filters")],
        [InlineKeyboardButton("4️⃣ Settings", callback_data="settings")]
    ])

def customize_filters_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📌 Select Coins", callback_data="select_coins")],
        [InlineKeyboardButton("💱 Select Exchanges", callback_data="select_exchanges")],
        [InlineKeyboardButton("📊 Set Threshold", callback_data="set_threshold")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])

def settings_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Change Language", callback_data="change_language")],
        [InlineKeyboardButton("♻️ Reset Filters", callback_data="reset_filters")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])

def premium_purchase_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Buy Premium", callback_data="buy_premium")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])
