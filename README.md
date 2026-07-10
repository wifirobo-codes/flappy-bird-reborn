# Flappy Bird Reborn

A modern, lightweight Flappy Bird-style game built with **Python + Pygame**.

## What is Flappy Bird Reborn?

Flappy Bird Reborn keeps the original one-button, pipe-dodging gameplay, but adds small twists to make runs feel more dynamic and rewarding.

---

## What’s Different from Classic Flappy Bird?

### 1) **Speed Orb Power-Up**
- Some pipe gaps contain a **Speed Orb**.
- If you collect it:
  - You get a short **boost mode** for about 2 seconds.
  - Your movement speed increases.
  - Your score gained from passing pipes becomes **x2** during the boost.
  - Your bird gets a small upward assist.

### 2) **High Score Saving**
- Your best score is saved locally in:
  - `Flappy Bird Reborn/Python/highscore.txt`
- The game shows your current score and your best score ("best ...") on screen.

### 3) **Simple Restart Flow**
- After game over, press:
  - **Space** (or Up / W) to restart instantly
  - **R** to restart

### 4) **Clean, Extendable Codebase**
- Easy to customize assets, tweak physics, or add features.

---

## Controls (User Manual)

## In-Game Controls
- **Space** / **Up Arrow** / **W** → Flap (jump)
- **R** → Restart (when dead)
- **Close Window** → Quit game

## Game States
1. **Ready State**
   - Message shows: `press space`
   - Press Space/Up/W to begin.

2. **Play State**
   - Gravity pulls bird down continuously.
   - Pass pipe sets to earn points.
   - Avoid:
     - Hitting pipes
     - Flying too high (top boundary)
     - Falling to the ground

3. **Dead State**
   - “game over” panel appears.
   - Press Space/Up/W or R to restart.

---

## Scoring System

- Normal pipe pass: **+1**
- Pipe pass during boost mode: **+2**
- High score updates automatically when beaten.

---

## Power-Up Guide: Speed Orb

- Spawn chance is low (appears occasionally in a pipe gap).
- Collecting an orb:
  - Activates temporary boost (`x2` indicator shown near bird)
  - Increases horizontal game speed
  - Doubles pipe score gain while active

### Strategy Tip
Sometimes it’s worth taking a slightly risky line through the gap to collect an orb if you can safely chain several pipes during boost.

---

## Installation & Running

## Requirements
- Python 3.8+
- `pygame`

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/wifirobo-codes/flappy-bird-reborn.git
   cd flappy-bird-reborn
   ```

2. Install dependency:
   ```bash
   pip install pygame
   ```

3. Run the game:
   ```bash
   python "Flappy Bird Reborn/Python/main.py"
   ```

---

## Project Structure

```text
flappy-bird-reborn/
├─ Flappy Bird Reborn/
│  ├─ Assets/                  # Sprites, sounds, background, pipes, orb
│  └─ Python/
│     ├─ main.py               # Main game loop and logic
│     └─ highscore.txt         # Saved best score
├─ .gitignore
└─ README.md
```

---

## Customization Ideas

- Change gravity/flap force for difficulty tuning
- Add multiple bird skins
- Add day/night themes
- Add pause button and settings menu
- Add sound/music toggles

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`**
  - Install pygame: `pip install pygame`

- **Game launches but no sound**
  - Mixer/audio device might not be available; game still runs without sound.

- **Assets not loading**
  - Ensure you run from repository with original folder structure intact.

---

## License

Add your preferred license here (MIT recommended for open-source projects).
