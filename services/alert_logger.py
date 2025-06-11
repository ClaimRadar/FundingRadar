import json
import os
from datetime import datetime
import csv

LOG_JSON = "logs/alert_log.json"
LOG_CSV = "logs/alert_log.csv"

def log_alert(user_id, coin, exchange, rate, funding_in):
    timestamp = datetime.utcnow().isoformat()

    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "coin": coin,
        "exchange": exchange,
        "rate": rate,
        "funding_in": funding_in
    }

    # JSON'e ekle
    logs = []
    if os.path.exists(LOG_JSON):
        with open(LOG_JSON, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(log_entry)
    with open(LOG_JSON, "w") as f:
        json.dump(logs, f, indent=2)

    # ✅ CSV'ye yaz
    write_header = not os.path.exists(LOG_CSV)
    with open(LOG_CSV, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=log_entry.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(log_entry)
