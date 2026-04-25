---
name: add-block
description: Step-by-step guide for adding a new block type to CollectorBlocks. Covers block ID constants, BLOCKS dict entry, renderer drawing, items linking, crafting recipes, and world spawning. Handles four block categories: simple/decorative, equipment/crafting stations, natural terrain (ores, deposits), and surface crop stages.
---

# Add a New Block

## Use the generator first

For categories A, B, and C below, run the generator before doing anything manually:

```bash
python3 generator/new_block.py decorative "Block Name" "R,G,B"
python3 generator/new_block.py equipment  "Block Name" "R,G,B"
python3 generator/new_block.py ore        "Block Name" "R,G,B"
```

Add `--dry-run` to preview without writing. The generator handles:
- ID constant (auto-detects next free ID)
- `BLOCKS` dict entry
- `EQUIPMENT_BLOCKS` / `RESOURCE_BLOCKS` set membership
- `ITEMS` entry + extends the `from blocks import` in items.py
- Placeholder `ARTISAN_RECIPES` entry (decorative/equipment)

It prints exactly what still needs manual work when it finishes. The remaining manual steps are always: renderer art, UI wiring (equipment), and world generation (ore). See the relevant category section below for those steps.

Options: `--hardness N`, `--drop item_id` (use `none` for no drop), `--comment "text"`.

---

## Category A — Simple / Decorative Block

A block that can be placed and mined, with an optional item drop. Artisan Bench decorative blocks are the most common example.

**Run the generator first** — it handles A1–A4 automatically.

### BLOCKS dict field reference

| Field | Notes |
|-------|-------|
| `name` | Display name shown in UI |
| `hardness` | Mining time multiplier. Decorative/equipment = 1, stone ≈ 3, ore = 4–7, indestructible = `float('inf')` |
| `color` | RGB tuple. If using custom renderer art, set to `None` |
| `drop` | Item ID string dropped when mined, or `None` |
| `drop_chance` | Optional float 0–1 (default 1.0). Omit unless you want a random drop |

### ARTISAN_RECIPES entry format ([crafting.py](../../../crafting.py))

The generator inserts a placeholder — update the ingredients:

```python
{"name": "My Block", "ingredients": {"stone_chip": 2, "iron_chunk": 1}, "output_id": "my_block", "output_count": 2},
```

For non-Artisan-Bench stations, find the matching list (`BAKERY_RECIPES`, `ROASTER_RECIPES`, etc.) and add an entry there instead.

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

**Run the generator first** — it handles the ID constant, BLOCKS entry, EQUIPMENT_BLOCKS membership, item, and ARTISAN_RECIPES placeholder automatically.

### B5 — Update crafting recipe (crafting.py)

The generator adds a placeholder to `ARTISAN_RECIPES`. Update the ingredients to the correct ones. Equipment is typically crafted at the Artisan Bench or a basic bench.

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

**Run the generator first** — it handles the ID constant, BLOCKS entry, RESOURCE_BLOCKS membership, and drop item automatically.

For special deposits (Rock, Fossil, Gem-style) that spawn a collectible instead of an item, pass `--drop none` and handle the drop manually in player.py (see C5 below).

### C4 — Add world generation (world.py)

In `_pick_block()` in [world.py](../../../world.py), add a depth/biome condition that returns the new block ID:

```python
if depth > 60 and biome in ("ferrous", "sedimentary") and random.random() < 0.04:
    return MY_ORE_BLOCK
```

Place it before the final `return STONE` line. Adjust depth range and probability to taste.

### C5 — Add renderer surface (renderer.py)

Ores use a custom drawn surface — typically a stone-colored rect with colored crystal/vein shapes on top. Follow the renderer pattern in Category A step A5.

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

**Generator covers (run it first):**
- [ ] Block ID constant added and is unique
- [ ] `BLOCKS` dict entry present with `name`, `hardness`, `color`, `drop`
- [ ] `ITEMS` entry created; items.py import extended (decorative/equipment)
- [ ] Drop item entry added (ore)
- [ ] Category-specific set updated (`EQUIPMENT_BLOCKS` or `RESOURCE_BLOCKS`)
- [ ] Placeholder `ARTISAN_RECIPES` entry added (decorative/equipment)

**Manual steps remaining:**
- [ ] Renderer surface defined — custom `if bid ==` art in `_build_block_surfs()` (renderer.py)
- [ ] Renderer imports the new block constant
- [ ] Crafting recipe ingredients updated from placeholder (decorative/equipment)
- [ ] UI interaction wired in main.py (equipment only)
- [ ] World generation entry added in `_pick_block()` (terrain/ore only)
- [ ] Run the game and verify the block places, renders, and drops correctly
