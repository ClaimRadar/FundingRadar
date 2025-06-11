import requests

MAXG_API_URL = "https://maxg-api.pages.dev/data/funding.json"

def get_live_funding_data():
    try:
        response = requests.get(MAXG_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Failed to fetch funding data: {e}")
        return []

    formatted = []

    for item in data:
        try:
            coin = item["symbol"]
            exchange = item["exchange"]
            rate = float(item["fundingRate"]) * 100  # Oranı yüzdeye çeviriyoruz
            time_remaining = int(item.get("nextFundingInMins", 0))

            formatted.append({
                "coin": coin,
                "exchange": exchange,
                "rate": rate,
                "funding_in": time_remaining
            })
        except Exception as e:
            continue

    return formatted
