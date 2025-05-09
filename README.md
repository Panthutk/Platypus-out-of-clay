# Platypus Out of Clay

A 2D side-scrolling shooter inspired by the classic game *Platypus*, featuring pixel graphics, unique enemy patterns, power-ups, and animated effects.

## 📌 Project Version: v1.0

Final submission for **Computer Programming II (01219116/01219117)**  
**Semester:** 2024/2  
**Section:** 450

---

## 🔧 Installation Instructions

### 🐍 Create Virtual Environment (Recommended)

### PowerShell (Windows)

#### Create Virtual Environment

```bash
python -m venv venv
```

#### Activate Virtual Environment

```bash
.\venv\Scripts\Activate
```

#### Install all requirements

```bash
pip install -r requirements.txt
```

#### Run main game

```bash
python main.py
```

#### Run visualizations (statistics graph)

```bash
python visualizations.py
```

### macOS / Linux

#### Create Virtual Environment

```bash
python3 -m venv venv
```

#### Activate Virtual Environment

```bash
source venv/bin/activate
```

#### Install all requirements

```bash
pip install -r requirements.txt
```

#### Run main game

```bash
python3 main.py
```

#### Run visualizations (statistics graph)

```bash
python3 visualizations.py
```

## 🕹 Current Features (v1.0)

🎮 Core Gameplay

* Smooth player movement with engine effects

* Autocannon fire with animation

* Health-based sprite states

* Shield effect upon taking damage

👾 Enemy System

* Three unique enemy types:

  * Fighter: Direct shooter with vertical patrol

  * Torpedo: Sine-wave mover dropping bombs

  * Battlecruiser: Slow but durable with tracking projectiles

* Animated destruction on enemy death

💥 Weapons & Power-Ups

* SG: Shotgun (5-way bullet spread)

* IF: Increased fire rate

* MS: Missile launcher (tracks enemies with FSM logic)

* Power-up display with blinking warnings before expiry

📈 Difficulty Scaling

* Enemies grow stronger, faster, and spawn more frequently over time

* Notification when difficulty increases

🧾 Logging & Analytics

* gamedata.csv logs every session:

  * Distance traveled, shots fired/hit

  * Power-ups used, score, survival time

  * Enemies defeated, accuracy, and effectiveness

* `visualizations.py` generates 6 gameplay analytics graphs using matplotlib

💀 Game Over Flow

* Options: E to continue, Q to quit and save data by using `stats_logger.py`
