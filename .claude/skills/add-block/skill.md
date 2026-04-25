---
name: add-block
description: Step-by-step guide for adding a new block type to CollectorBlocks. Covers block ID constants, BLOCKS dict entry, renderer drawing, items linking, crafting recipes, and world spawning. Handles four block categories: simple/decorative, equipment/crafting stations, natural terrain (ores, deposits), and surface crop stages.
---

# Add a New Block

Blocks in CollectorBlocks are defined by a numeric ID constant, a `BLOCKS` dict entry, and a renderer surface. Beyond those three things, what else is required depends on the block's category. Read the category that matches your block and follow only those steps.

**Current highest block ID:** 513 (`PORTUGUESE_CORK`). New blocks start at **514**.

---

## Category A — Simple / Decorative Block

A block that can be placed and mined, with an optional item drop. Artisan Bench decorative blocks are the most common example.

### A1 — Assign an ID constant (blocks.py)

Add at the end of the relevant section near line 510 in [blocks.py](../../../blocks.py):

```python
MY_NEW_BLOCK = 514  # short description of what it is
```

### A2 — Add to BLOCKS dict (blocks.py)

Find the `BLOCKS = {` definition and add an entry:

```python
MY_NEW_BLOCK: {"name": "My New Block", "hardness": 2, "color": (180, 160, 130), "drop": "my_new_block_item"},
```

| Field | Notes |
|-------|-------|
| `name` | Display name shown in UI |
| `hardness` | Mining time multiplier. Equipment/decorative = 1, stone ≈ 3, ore = 5, indestructible = `float('inf')` |
| `color` | RGB fallback. If drawing custom art in renderer, set to `None` |
| `drop` | Item ID string dropped when mined, or `None` for no drop |
| `drop_chance` | Optional float 0–1 (default 1.0). Omit unless you want a random drop |

### A3 — Add item entry (items.py)

In [items.py](../../../items.py), add the item that places or represents the block:

```python
"my_new_block_item": {"name": "My New Block", "color": (180, 160, 130), "place_block": MY_NEW_BLOCK},
```

Import the block constant in items.py — extend the relevant import line at the top of the file.

### A4 — Add crafting recipe (crafting.py)

For Artisan Bench outputs, add to the `ARTISAN_BENCH_RECIPES` list in [crafting.py](../../../crafting.py):

```python
{"output": "my_new_block_item", "count": 4, "ingredients": {"stone": 2, "iron_ore": 1}},
```

For other stations, find the matching recipe list (`BAKERY_RECIPES`, `ROASTER_RECIPES`, etc.) and follow the same pattern.

### A5 — Add renderer surface (renderer.py)

In `_build_block_surfs()` in [renderer.py](../../../renderer.py), import the new constant and add drawing code **before** the `# ── fallback` comment at the bottom of the loop:

**Option 1 — Solid color block** (set `"color"` in BLOCKS and no renderer entry needed — it's auto-generated)

**Option 2 — Custom drawn block:**

```python
if bid == MY_NEW_BLOCK:
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    # draw your block here using pygame.draw.rect/circle/polygon
    pygame.draw.rect(s, (180, 160, 130), (2, 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))
    pygame.draw.rect(s, (140, 120, 100), (4, 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8))
    surfs[bid] = s
    continue
```

Extend the import block in renderer.py to include the new constant.

---

## Category B — Equipment / Crafting Station Block

A placeable block that opens a UI when the player interacts with it (ovens, fermenters, looms, etc.).

### B1–B3: Follow steps A1–A3

Use `"hardness": 1` and `"drop": "my_station_item"` in BLOCKS. The item `place_block` links it back to the block ID.

### B4 — Add to EQUIPMENT_BLOCKS set (blocks.py)

Find `EQUIPMENT_BLOCKS` (around line 621) and add the new constant:

```python
EQUIPMENT_BLOCKS = {..., MY_STATION_BLOCK}
```

### B5 — Add crafting recipe (crafting.py)

Add a recipe that outputs the item. Equipment is typically crafted at the basic bench or Artisan Bench.

### B6 — Add renderer surface (renderer.py)

Equipment blocks almost always need custom art — follow Option 2 in step A5. Draw the station from scratch using rects and circles. Keep it readable at 32×32 pixels.

### B7 — Wire up the UI interaction (main.py)

In [main.py](../../../main.py), find the `handle_block_interact` method (search for `BAKERY_BLOCK` for an example). Add an `elif` branch that opens the relevant UI screen:

```python
elif block_id == MY_STATION_BLOCK:
    self.open_my_station_ui()
```

Implement `open_my_station_ui()` following an existing station as a model.

---

## Category C — Natural Terrain Block (Ore / Deposit)

A block that spawns in the world underground and is mined for resources.

### C1–C2: Follow steps A1–A2

For ores: `"hardness": 3–7`, `"drop": "ore_item"`. For special deposits (Rock, Fossil, Gem-style): `"drop": None` — the drop is handled in player.py.

### C3 — Add to RESOURCE_BLOCKS set (blocks.py)

```python
RESOURCE_BLOCKS = {..., MY_ORE_BLOCK}
```

### C4 — Add world generation (world.py)

In `_pick_block()` in [world.py](../../../world.py), add a depth/biome condition that returns the new block ID:

```python
if depth > 60 and biome in ("ferrous", "sedimentary") and random.random() < 0.04:
    return MY_ORE_BLOCK
```

Place it before the final `return STONE` line. Adjust depth range and probability to taste.

### C5 — Add item and renderer surface

Follow steps A3 and A5. Ores use a custom drawn surface — typically a stone-colored rect with colored crystal/vein shapes on top.

### C6 — Special deposit (no item drop)

If the block spawns a collectible object (like Rock or Fossil) instead of an item, add handling in [player.py](../../../player.py) `mine_block()`, following the pattern of `ROCK_DEPOSIT` around line 553:

```python
elif block_id == MY_DEPOSIT:
    obj = MyCollectible(x, y, ...)
    self.world.collectibles.append(obj)
    # no item added to inventory
    return
```

---

## Category D — Surface Crop Stages (Bush / Young / Mature)

Three-stage plants that spawn on grass and grow over time. Use the **[add-herb](../add-herb/skill.md)** or **[add-food](../add-food/skill.md)** skills instead — they cover crop blocks end-to-end including biome spawning, player harvest drops, and perennial regrowth.

---

## Verification checklist

- [ ] Block ID constant added and is unique
- [ ] `BLOCKS` dict entry present with `name`, `hardness`, `color`, `drop`
- [ ] Renderer surface defined (auto from `color`, or custom `if bid ==` block)
- [ ] Renderer imports the new block constant
- [ ] `ITEMS` entry created with `place_block` pointing at the block ID (if placeable)
- [ ] items.py imports the new block constant
- [ ] Crafting recipe added (if craftable)
- [ ] Category-specific sets updated (`EQUIPMENT_BLOCKS`, `RESOURCE_BLOCKS`, etc.)
- [ ] UI interaction wired in main.py (equipment blocks only)
- [ ] World generation entry added (terrain blocks only)
- [ ] Run the game and verify the block places, renders, and drops correctly
