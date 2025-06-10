class UserSettings:
    def __init__(self, user_id):
        self.user_id = user_id
        self.is_premium = False
        self.coins = []  # örnek: ["BTC", "ETH"]
        self.exchanges = []  # örnek: ["Binance", "Bybit"]
        self.threshold = 1.0  # varsayılan threshold (freeler için %1)
        self.countdown_enabled = False

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "is_premium": self.is_premium,
            "coins": self.coins,
            "exchanges": self.exchanges,
            "threshold": self.threshold,
            "countdown_enabled": self.countdown_enabled
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(data.get("user_id"))
        instance.is_premium = data.get("is_premium", False)
        instance.coins = data.get("coins", [])
        instance.exchanges = data.get("exchanges", [])
        instance.threshold = data.get("threshold", 1.0)
        instance.countdown_enabled = data.get("countdown_enabled", False)
        return instance
