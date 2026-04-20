# CollectorBlocks — Game Design Document

## Concept

A 2D side-scrolling digger game built in Pygame. The player starts on the surface of a procedurally generated world and digs downward (or in any direction) to mine blocks, collect resources, and discover rare materials deeper underground.

---

## Core Loop

1. **Dig** — mine blocks in any direction (up, down, left, right)
2. **Collect** — gather the resources that drop from mined blocks
3. **Upgrade** — spend resources to improve your pick, expand storage, or unlock new abilities
4. **Descend** — go deeper to find harder but more valuable blocks

---

## World

- The world is a 2D grid of blocks, scrolling in all directions
- The surface is a thin layer of grass/dirt; underground is layered by depth
- World is procedurally generated using noise (e.g. Perlin/simplex) for natural-looking cave pockets and ore veins
- World height: ~200 blocks deep; width: ~500 blocks wide (wraps horizontally)

### Depth Zones

| Zone        | Depth (blocks) | Theme          |
|-------------|----------------|----------------|
| Surface     | 0–5            | Grass, soil    |
| Shallow     | 5–40           | Stone, common ores |
| Mid         | 40–100         | Dense rock, rare ores |
| Deep        | 100–160        | Hardened rock, gems |
| Core        | 160–200        | Obsidian, legendary materials |

---

## Block Types

Each block has:
- **Hardness** (1–10): how many hits to mine
- **Drop**: what resource it yields when mined
- **Rarity**: how frequently it appears at a given depth

| Block       | Hardness | Drop           | Found At      |
|-------------|----------|----------------|---------------|
| Dirt        | 1        | Dirt clump     | Surface       |
| Stone       | 2        | Stone chip     | Shallow+      |
| Coal Ore    | 3        | Coal           | Shallow+      |
| Iron Ore    | 4        | Iron chunk     | Shallow–Mid   |
| Gold Ore    | 5        | Gold nugget    | Mid+          |
| Crystal Ore | 6        | Crystal shard  | Deep+         |
| Ruby Ore    | 7        | Ruby           | Deep+         |
| Obsidian    | 9        | Obsidian slab  | Core          |
| Bedrock     | ∞        | Nothing        | Bottom edge   |

---

## Player

- Spawns at the surface center
- Has a **health bar** (damage from falling, cave-ins, hazards)
- Has an **inventory** with a fixed number of slots (expandable via upgrades)
- Has a **pickaxe** with a `power` stat that determines how quickly blocks are mined

### Mining

- Player faces a block and holds the mine key
- A progress bar fills based on `hardness / pick_power`
- When full, the block is destroyed and the drop is added to inventory

### Movement

- Walk left/right on solid ground
- Jump (limited height)
- Gravity pulls the player downward — falling from height deals damage

---

## Upgrades

Purchased at the surface **Workshop** using collected resources.

| Upgrade            | Effect                          | Cost (example)        |
|--------------------|---------------------------------|-----------------------|
| Iron Pick          | +1 pick power                   | 10 iron chunks        |
| Gold Pick          | +2 pick power                   | 8 gold nuggets        |
| Crystal Pick       | +4 pick power                   | 5 crystal shards      |
| Inventory Bag I    | +5 inventory slots              | 15 stone chips        |
| Lantern            | Larger light radius underground | 10 coal               |
| Boots              | Reduce fall damage              | 12 iron chunks        |
| Dynamite (x5)      | Destroys a 3×3 area instantly   | 5 coal + 5 stone      |

---

## Hazards

- **Falling**: >5 blocks of freefall deals proportional damage
- **Cave-ins**: mining certain blocks may cause blocks above to fall
- **Darkness**: below surface, visibility is limited to a radius around the player (lantern upgrade extends this)
- **Lava pockets** (Core zone): instant death on contact

---

## UI / HUD

- **Health bar** — top left
- **Inventory bar** — bottom of screen (hotbar of 8 slots)
- **Depth indicator** — current depth in blocks, top right
- **Mining progress bar** — appears above the block being mined
- **Mini-map** — optional, shows explored area (unlockable upgrade)

---

## Controls

| Key          | Action              |
|--------------|---------------------|
| A / D        | Move left / right   |
| W / Space    | Jump                |
| Mouse click  | Mine block          |
| E            | Open full inventory |
| ESC          | Pause / main menu   |

---

## Win / Goal Conditions

The game is open-ended, but tracks:
- **Deepest depth reached** (personal record)
- **Rarest block mined** (achievement-style milestones)
- **Full collection**: mine at least one of every block type to "complete" the collection

---

## Technical Architecture

- **Language**: Python 3.x
- **Library**: Pygame
- **World storage**: 2D numpy array (or list of lists) of block IDs
- **Rendering**: only draw blocks within camera viewport; camera follows player
- **Chunk system** (optional): divide world into 16×16 chunks for efficient loading/saving
- **Save system**: pickle or JSON serialization of world state + player state

### Key Modules

| Module          | Responsibility                          |
|-----------------|-----------------------------------------|
| `main.py`       | Game loop, event handling               |
| `world.py`      | World generation, block data, chunk mgmt|
| `player.py`     | Player state, movement, mining logic    |
| `renderer.py`   | Camera, tile drawing, lighting          |
| `ui.py`         | HUD, inventory screen, upgrade shop     |
| `blocks.py`     | Block definitions (hardness, drops, etc)|
| `items.py`      | Item/resource definitions               |
