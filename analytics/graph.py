import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

LOG_CSV = "logs/alert_log.csv"

def generate_weekly_graph(output_path="logs/weekly_graph.png"):
    if not os.path.exists(LOG_CSV):
        return None

    df = pd.read_csv(LOG_CSV)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sadece son 7 gün
    last_week = datetime.utcnow() - timedelta(days=7)
    df = df[df['timestamp'] >= last_week]

    # Coin + Exchange bazlı ortalama funding
    grouped = df.groupby(['coin', 'exchange'])['rate'].mean().reset_index()
    grouped = grouped.sort_values(by='rate', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    bars = plt.barh(
        [f"{c} @ {e}" for c, e in zip(grouped['coin'], grouped['exchange'])],
        grouped['rate'],
        color=["green" if r > 0 else "red" for r in grouped['rate']]
    )

    plt.xlabel("Average Funding Rate (%)")
    plt.title("Top 10 Weekly Funding Rates")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path
