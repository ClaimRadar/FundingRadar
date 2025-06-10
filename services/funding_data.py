import random
import time

def get_dummy_funding_rates():
    """
    Returns fake funding rate data for testing.
    You can later replace this with real API data.
    """

    return [
        {
            "symbol": "BTC",
            "exchange": "Binance",
            "funding_rate": round(random.uniform(-0.02, 0.035), 4),
            "next_funding_time": time.time() + 3600
        },
        {
            "symbol": "ETH",
            "exchange": "Bybit",
            "funding_rate": round(random.uniform(-0.01, 0.02), 4),
            "next_funding_time": time.time() + 1800
        },
        {
            "symbol": "PEPE",
            "exchange": "OKX",
            "funding_rate": round(random.uniform(-0.03, 0.04), 4),
            "next_funding_time": time.time() + 5400
        }
    ]
