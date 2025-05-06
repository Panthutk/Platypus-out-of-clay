# === stat_logger.py ===
import csv
import os
from datetime import datetime

CSV_FILE = "gamedata.csv"
FIELDNAMES = [
    "Timestamp", "SessionID", "DistanceTraveled", "ShotsFired", "ShotsHit",
    "PowerUpsUsed", "SurvivalTime", "EnemiesDefeated", "Score",
    "PowerUpEffectiveness", "EnemiesDefeatedPerMinute", "AccuracyPerMinute"
]

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def log_stats(session_id, distance, shots_fired, shots_hit, powerups_used,
              survival_time, enemies_defeated, score,
              powerup_effectiveness=0, edpm=0, accuracy_per_min=0):
    init_csv()
    row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "SessionID": session_id,
        "DistanceTraveled": distance,
        "ShotsFired": shots_fired,
        "ShotsHit": shots_hit,
        "PowerUpsUsed": powerups_used,
        "SurvivalTime": survival_time,
        "EnemiesDefeated": enemies_defeated,
        "Score": score,
        "PowerUpEffectiveness": powerup_effectiveness,
        "EnemiesDefeatedPerMinute": edpm,
        "AccuracyPerMinute": accuracy_per_min
    }

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)
