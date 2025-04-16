# Platypus Out of Clay

A 2D side-scrolling shooter inspired by the classic game *Platypus*, featuring pixel graphics, unique enemy patterns, power-ups, and animated effects.

## 📌 Project Checkpoint: v0.5

This is the 50% checkpoint submission for **Computer Programming II (01219116/01219117)**  
**Semester:** 2024/2  
**Section:** 450

---

## 🔧 Installation Instructions

### 🐍 Create Virtual Environment (Recommended)

#### PowerShell (Windows)

```bash
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python main.py

```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## 🕹 Current Features (v0.5)

* Player movement and autocannon shooting

* Three enemy types: Fighter, Torpedo, Battlecruiser with AI and shooting patterns
* Background animations

* Score and health system

* Power-up drops on enemy death:

  * SG: Shotgun (5-way spread)
  * IF: Increased Fire Rate
  * MS: Missile (FSM)

* Display of active power-ups with blinking expiration warning

* Game over screen with "Continue" and "Exit" options
