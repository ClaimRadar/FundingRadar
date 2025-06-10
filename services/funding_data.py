import random
import time

def get_mock_funding_data():
    return [
        {"coin": "BTC", "exchange": "Binance", "rate": 0.018, "funding_in": 180},
        {"coin": "ETH", "exchange": "Bybit", "rate": 0.027, "funding_in": 45},
        {"coin": "PEPE", "exchange": "OKX", "rate": -0.042, "funding_in": 10},
        {"coin": "XRP", "exchange": "MEXC", "rate": 0.095, "funding_in": 190},
    ]

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
