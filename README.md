# joncoop-pygame-platformer

A 2D platformer game built with Python and Pygame featuring multiple levels, enemies, collectibles, and interactive elements.

## Features

- **Multiple Levels**: Progress through 3 different worlds, each with unique layouts
- **Character Control**: Smooth player movement with walking, jumping, and interactions
- **Enemies**: Various enemy types including clouds, spikeballs, and spikemen
- **Collectibles**:
  - Gems for scoring points
  - Hearts to restore health
  - Keys to unlock doors
- **Interactive Elements**: Doors and locked doors that can be opened with keys
- **Goal System**: Reach the flag to complete each level
- **Health System**: Start with 3 hearts; lose a heart when hit by enemies or falling off the map
- **Score System**: Collect gems to increase your score
- **Smooth Camera**: Camera that follows the player with configurable lag
- **UI Overlays**: Title screen, pause menu, win/lose screens, and HUD
- **Audio**: Background music and sound effects for actions

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Steps

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd pygame-platformer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Simply run the main script:

```bash
python main.py
```

## Controls

| Action | Key |
|--------|-----|
| Move Left | ← (Left Arrow) |
| Move Right | → (Right Arrow) |
| Jump | Space |
| Interact | ↑ (Up Arrow) |
| Uninteract | ↓ (Down Arrow) |
| Pause | P |
| Toggle Grid (Debug) | G |
| Toggle Camera View (Debug) | C |
| Restart (Win/Lose Screen) | R |
| Start Game | Space (Title Screen) |

## Game Structure

The game is organized into several scenes:
- **START**: Title screen
- **PLAYING**: Main gameplay
- **PAUSE**: Paused game state
- **LEVEL_COMPLETE**: Transition between levels
- **WIN**: Victory screen (shown after completing all levels)
- **LOSE**: Game over screen (shown when hearts reach 0)

## Project Structure

```
pygame-platformer/
├── main.py                 # Entry point of the game
├── settings.py             # Game configuration and constants
├── requirements.txt        # Python dependencies
├── assets/                 # Game assets
│   ├── fonts/             # Custom fonts
│   ├── images/            # Sprites and textures
│   │   ├── backgrounds/   # Background images
│   │   ├── characters/    # Player and enemy sprites
│   │   ├── items/         # Collectible item sprites
│   │   └── tiles/         # Level tile sprites
│   ├── levels/            # Level data (JSON format)
│   ├── music/             # Background music files
│   └── sounds/            # Sound effect files
├── src/                   # Source code
│   └── platformer/
│       ├── game.py        # Main game class
│       ├── camera/        # Camera system
│       ├── entities/      # Game entities (hero, enemies, items, etc.)
│       └── overlays/      # UI overlays (HUD, menus, etc.)
└── map_maker/             # Tools for creating levels
```

## Configuration

Most game settings can be customized in `settings.py`, including:
- Screen dimensions
- Player speed and jump power
- Enemy speeds
- Gravity and physics constants
- Control key mappings
- Number of hearts
- Level files

## Level Format

Levels are stored as JSON files in `assets/levels/`. Each level defines:
- World dimensions
- Player starting position
- Platform locations (grass and blocks)
- Enemy positions (clouds, spikeballs, spikemen)
- Item locations (gems, hearts, keys)
- Door positions with optional key codes
- Goal flag position

## License

See LICENSE.txt for details.
