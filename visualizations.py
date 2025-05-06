import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("gamedata.csv", parse_dates=["Timestamp"])
df = df.sort_values("Timestamp")

plt.style.use("ggplot")

# Set the figure size and title
fig, axs = plt.subplots(3, 2, figsize=(18, 12))
fig.suptitle("Gameplay Statistics Visualization", fontsize=20, fontweight="bold")

# === Graph 1: Distance Traveled Over Time ===
axs[0, 0].plot(df["Timestamp"], df["DistanceTraveled"], marker='o', color='tab:blue')
axs[0, 0].set_title("Player Movement Distance")
axs[0, 0].set_xlabel("Time")
axs[0, 0].set_ylabel("Distance")
axs[0, 0].set_ylim(0, df["DistanceTraveled"].max() + 500)
axs[0, 0].tick_params(axis='x', rotation=30)

# === Graph 2: Power-ups Used Per Session ===
axs[0, 1].bar(df["Timestamp"], df["PowerUpsUsed"], color='tab:green')
axs[0, 1].set_title("Power-up Usage per Session")
axs[0, 1].set_xlabel("Time")
axs[0, 1].set_ylabel("Times Collected")
axs[0, 1].tick_params(axis='x', rotation=30)

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

# === Graph 5: Enemies Defeated Per Minute Over Time ===
axs[2, 0].plot(df["Timestamp"], df["EnemiesDefeatedPerMinute"], marker='o', color='tab:purple')
axs[2, 0].set_title("Enemies Defeated Per Minute Over Time")
axs[2, 0].set_xlabel("Time")
axs[2, 0].set_ylabel("Enemies/Min")
axs[2, 0].set_ylim(0, df["EnemiesDefeatedPerMinute"].max() + 2)
axs[2, 0].tick_params(axis='x', rotation=30)

# === Graph 6: Accuracy Over Time ===
axs[2, 1].plot(df["Timestamp"], df["AccuracyPerMinute"], marker='o', color='tab:brown')
axs[2, 1].set_title("Accuracy Over Time")
axs[2, 1].set_xlabel("Time")
axs[2, 1].set_ylabel("Accuracy (%)")
axs[2, 1].set_ylim(0, 100)
axs[2, 1].tick_params(axis='x', rotation=30)


plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.subplots_adjust(hspace=0.5)
plt.show()
