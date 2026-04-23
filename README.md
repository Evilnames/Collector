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
- Somewhere elusive snow leopards and mountain lions roam.

## Collectables
- This game is focused very much on collecting natural wonders. It currently has:
 - Birds - They fly around, if you stay still as they're nesting you can collect them into your encycolopedia. You can also build bird nests and bird feeders to get them to stop by.
 - Fish - Find a lake or river and start fishing for one of 50 unique types of fish.
 - Wildflowers - Scattered around 15 different biomes is different wildflowers to collect.
 - Mushrooms - Mushrooms live underground and in some forests.
 - Rocks - Hundreds of unique rocks to collect, polish and trade with other collectors in game.
 - Gems - Unique gems require cleaning.
 - Fossils - Deep underground undercover the animals that were before you.

 ## Breeding
- Taming animals gives you the ability to breed different features, from size to color.
- Animals have history that you can see to see how you got there.

## Construction Equipment and Automation
- Mine deep underground with construction equipment that requires oil.
- Use automations to quickly build out tunnels or tend to your crops.

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
