# CollectorBlocks

A 2D side-scrolling mining and crafting game built with Python and Pygame.

You explore a procedurally generated world, mine resources, craft items, research upgrades, trade with NPC cities, and deploy autonomous mining machines to dig deeper.

## Features

- Procedurally generated terrain with biomes, caves, rock deposits, and wildflowers
- Mining with tiered pickaxe power — deeper layers require researched upgrades
- Crafting system for tools, building blocks, and automation equipment
- Research tree unlocked with materials and money
- NPC cities with merchants and quests
- Automations: deploy coal/iron/diamond miners that dig tunnels and deposit loot
- Farming: plant and harvest a wide variety of crops
- Save/load via SQLite database

## Requirements

- Python 3.10+
- Pygame

Install dependencies:

```bash
pip install pygame
```

## Running

```bash
python main.py
```

The game launches in fullscreen by default. Press **F11** to toggle windowed mode.

## Controls

| Key | Action |
|-----|--------|
| A / D | Move left / right |
| Space | Jump |
| Left click | Mine block / interact |
| Right click | Place block |
| 1–8 | Select hotbar slot |
| Scroll wheel | Cycle hotbar |
| E | Open inventory |
| R | Open research tree |
| T | Open automations panel |
| Esc | Close panel / pause |
| F11 | Toggle fullscreen |
