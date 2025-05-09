# === visualizations.py ===
import pandas as pd
import matplotlib.pyplot as plt

# Load and sort
df = pd.read_csv("gamedata.csv", parse_dates=["Timestamp"])
df = df.sort_values("Timestamp").reset_index(drop=True)

# use session number instead of timestamp
df["Session"] = range(1, len(df) + 1)

plt.style.use("ggplot")
fig, axs = plt.subplots(3, 2, figsize=(18, 12))
fig.suptitle("Gameplay Statistics Visualization", fontsize=20, fontweight="bold")

# === Graph 1: Player Movement Distance ===
axs[0, 0].plot(df["Session"], df["DistanceTraveled"], marker='o', color='tab:blue')
axs[0, 0].set_title("Player Movement Distance")
axs[0, 0].set_xlabel("Session")
axs[0, 0].set_ylabel("Distance")
axs[0, 0].set_ylim(0, df["DistanceTraveled"].max() + 500)

# === Graph 2: Power-up Usage ===
axs[0, 1].bar(df["Session"], df["PowerUpsUsed"], color='tab:green')
axs[0, 1].set_title("Power-up Usage per Session")
axs[0, 1].set_xlabel("Session")
axs[0, 1].set_ylabel("Times Collected")

# === Graph 3: Enemies Defeated Histogram ===
axs[1, 0].hist(df["EnemiesDefeated"], bins=8, color='tab:orange', edgecolor='black')
axs[1, 0].set_title("Enemies Defeated per Session")
axs[1, 0].set_xlabel("Enemies Defeated")
axs[1, 0].set_ylabel("Session Count")

# === Graph 4: Power-up Effectiveness Histogram ===
axs[1, 1].hist(df["PowerUpEffectiveness"], bins=10, color='tab:red', edgecolor='black')
axs[1, 1].set_title("Power-up Effectiveness per Session")
axs[1, 1].set_xlabel("Effectiveness (Score / Uses)")
axs[1, 1].set_ylabel("Session Count")

# === Graph 5: Enemies Defeated Per Minute ===
axs[2, 0].plot(df["Session"], df["EnemiesDefeatedPerMinute"], marker='o', color='tab:purple')
axs[2, 0].set_title("Enemies Defeated Per Minute Over Time")
axs[2, 0].set_xlabel("Session")
axs[2, 0].set_ylabel("Enemies/Min")
axs[2, 0].set_ylim(0, df["EnemiesDefeatedPerMinute"].max() + 2)

# === Graph 6: Accuracy Over Time ===
axs[2, 1].plot(df["Session"], df["AccuracyPerMinute"], marker='o', color='tab:brown')
axs[2, 1].set_title("Accuracy Over Time")
axs[2, 1].set_xlabel("Session")
axs[2, 1].set_ylabel("Accuracy (%)")
axs[2, 1].set_ylim(0, 100)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.subplots_adjust(hspace=0.5)
plt.show()
