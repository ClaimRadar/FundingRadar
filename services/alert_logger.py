import json
import os
from datetime import datetime

LOG_PATH = "logs/alert_log.json"

def log_alert(user_id, coin, exchange, rate, funding_in):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "coin": coin,
        "exchange": exchange,
        "rate": rate,
        "funding_in": funding_in
    }

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)

    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    logs.append(log_entry)

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
