---
name: add-herb
description: Step-by-step guide for adding a new herb bush to CollectorBlocks. Covers block IDs, BLOCK_DATA, set registration, biome spawning, items, herbalism drying/recipes, tea additives, player harvest drops, and renderer drawing.
---

# Add a New Herb Bush

Herb bushes are surface-growing perennial crops defined across several files. Each herb has three block stages (bush → young crop → mature crop), a raw item, a seed item, a dried item, and optionally potion recipes or tea additive entries.

The four existing herbs are: **Chamomile** (302–304), **Lavender** (305–307), **Mint** (308–310), **Rosemary** (311–313). New herbs start at block ID **314**.

---

## Step 1 — Add block ID constants in blocks.py

Find the `# --- Herb bushes` section near line 293 in [blocks.py](../../../blocks.py) and add three consecutive IDs:

```python
THYME_BUSH          = 314  # surface bush; drops thyme_seed
THYME_CROP_YOUNG    = 315
THYME_CROP_MATURE   = 316  # harvest → thyme + seed; perennial
```

---

## Step 2 — Register in the block sets (blocks.py)

**BUSH_BLOCKS** — add the bush:
```python
CHAMOMILE_BUSH, LAVENDER_BUSH, MINT_BUSH, ROSEMARY_BUSH, THYME_BUSH}
```

**YOUNG_CROP_BLOCKS** — add young crop:
```python
CHAMOMILE_CROP_YOUNG, LAVENDER_CROP_YOUNG, MINT_CROP_YOUNG, ROSEMARY_CROP_YOUNG,
THYME_CROP_YOUNG,
```

**MATURE_CROP_BLOCKS** — add mature crop:
```python
CHAMOMILE_CROP_MATURE, LAVENDER_CROP_MATURE, MINT_CROP_MATURE, ROSEMARY_CROP_MATURE,
THYME_CROP_MATURE,
```

**PERENNIAL_CROP_MATURE** — herb crops regrow after harvest:
```python
CHAMOMILE_CROP_MATURE, LAVENDER_CROP_MATURE, MINT_CROP_MATURE, ROSEMARY_CROP_MATURE,
THYME_CROP_MATURE,
```

**MATURE_TO_YOUNG_CROP** — regrowth mapping:
```python
THYME_CROP_MATURE: THYME_CROP_YOUNG,
```

---

## Step 3 — Add BLOCK_DATA entries (blocks.py)

At the end of the `BLOCKS` dict, inside the `# --- Herb bushes ---` section:

```python
THYME_BUSH:            {"name": "Thyme Bush",            "hardness": 0.5, "color": (110, 160,  80), "drop": "thyme_seed",     "drop_chance": 1.0},
THYME_CROP_YOUNG:      {"name": "Thyme Plant",           "hardness": 0.5, "color": ( 95, 150,  70), "drop": "thyme_seed",     "drop_chance": 1.0},
THYME_CROP_MATURE:     {"name": "Thyme (Ripe)",          "hardness": 0.5, "color": (125, 175,  95), "drop": "thyme",          "drop_chance": 1.0},
```

Choose colors that visually distinguish the herb. Bush = base color, young = slightly darker/greener, mature = slightly brighter.

---

## Step 4 — Add biome spawning (world.py)

In `_BIOME_BUSHES` inside [world.py](../../../world.py), add `THYME_BUSH` to biomes that suit the herb's character. Thyme example (mediterranean/dry):

```python
"rolling_hills":  [..., THYME_BUSH],
"steppe":         [..., THYME_BUSH],
"arid_steppe":    [..., THYME_BUSH],
"steep_hills":    [..., THYME_BUSH],
```

Use doubles (e.g., `THYME_BUSH, THYME_BUSH`) to make it more common in a biome. world.py uses `from blocks import *` so no import needed.

---

## Step 5 — Add items (items.py)

In [items.py](../../../items.py):

**1. Add to the import** — extend the existing herb crop import line:
```python
CHAMOMILE_CROP_YOUNG, LAVENDER_CROP_YOUNG, MINT_CROP_YOUNG, ROSEMARY_CROP_YOUNG,
THYME_CROP_YOUNG)
```

**2. Add raw herb, seed, and dried item** in the `# Herb crops → raw ingredients` section:
```python
"thyme":             {"name": "Thyme",                "color": (115, 165,  85), "place_block": None, "edible": True, "hunger_restore": 2},
"thyme_seed":        {"name": "Thyme Seed",           "color": ( 90, 135,  65), "place_block": THYME_CROP_YOUNG},
```

Then in the dried ingredients section:
```python
"dried_thyme":       {"name": "Dried Thyme",          "color": ( 95, 140,  70), "place_block": None},
```

---

## Step 6 — Update herbalism.py

In [herbalism.py](../../../herbalism.py):

**INGREDIENT_DISPLAY_NAMES** — add the dried form:
```python
"dried_thyme": "Dried Thyme",
```

**DRYING_TABLE** — add raw → dried conversion:
```python
"thyme": "dried_thyme",
```

**Optional: add potion recipes** — follow the pattern of `soothe_potion` / `focus_potion`. Recipes need `"ingredients"`, `"station": "kiln"`, and `"tier": "basic"` or `"fine"`. Also add entries to `POTION_DESCS`, `POTION_COLORS`, and `BUFF_DESCS` if using a new buff name.

---

## Step 7 — Optional: add as tea additive (tea.py)

If the herb should be blendable in the Tea Cellar, add it to both dicts in [tea.py](../../../tea.py):

```python
# _HERBAL_NOTES
"thyme": ["woody thyme", "earthy herb"],

# HERBAL_ADDITIVES
"thyme": {
    "label":            "Thyme",
    "vegetal":          +0.08,
    "earthiness":       +0.12,
    "sweetness":        -0.05,
    "complexity_bonus": 0.04,
},
```

Flavor dimensions: `astringency`, `floral`, `vegetal`, `earthiness`, `sweetness`. All deltas are clamped to 0–1.

---

## Step 8 — Add player harvest drop (player.py)

In [player.py](../../../player.py):

**1. Add to the import block** (near the herb bush imports around line 32):
```python
CHAMOMILE_BUSH, LAVENDER_BUSH, MINT_BUSH, ROSEMARY_BUSH, THYME_BUSH,
CHAMOMILE_CROP_MATURE, LAVENDER_CROP_MATURE, MINT_CROP_MATURE, ROSEMARY_CROP_MATURE, THYME_CROP_MATURE,
```

**2. Add bush touch-drop** in the bush-interaction chain (search for `ROSEMARY_BUSH` — add after it):
```python
elif block_id == THYME_BUSH and random.random() < 0.25:
    self._add_item("thyme")
```

Typical drop chances: 0.15–0.30 depending on rarity. The mature crop drop is handled automatically via the `BLOCKS` dict `"drop"` field.

---

## Step 9 — Add renderer drawing (renderer.py)

In [renderer.py](../../../renderer.py):

**1. Add to the import block** (after `ROSEMARY_BUSH, ROSEMARY_CROP_YOUNG, ROSEMARY_CROP_MATURE,`):
```python
THYME_BUSH, THYME_CROP_YOUNG, THYME_CROP_MATURE,
```

**2. Add render code** in the block surface cache loop, directly after the `ROSEMARY_CROP_MATURE` block (before `if bid == CACTUS_YOUNG:`):

```python
if bid == THYME_BUSH:
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 20), (13, 24), (21, 18)]:
        pygame.draw.rect(s, (90, 145, 68), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (120, 170, 90), (stx - 3, ny, 4, 1))
            pygame.draw.rect(s, (120, 170, 90), (stx + 2, ny + 1, 4, 1))
    surfs[bid] = s
    continue
if bid == THYME_CROP_YOUNG:
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (23, 12)]:
        pygame.draw.rect(s, (95, 152, 72), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
            pygame.draw.rect(s, (118, 168, 88), (stx - 2, ny, 3, 1))
    surfs[bid] = s
    continue
if bid == THYME_CROP_MATURE:
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (20, 22)]:
        pygame.draw.rect(s, (90, 145, 68), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (125, 175, 95), (stx - 4, ny, 5, 1))
            pygame.draw.rect(s, (125, 175, 95), (stx + 2, ny + 1, 5, 1))
    surfs[bid] = s
    continue
```

Adapt colors and shapes to the herb's visual identity:
- **Leafy herbs** (mint, basil): ellipses for round leaves
- **Spike herbs** (lavender, sage): thin rect spike with `circle` dots up it
- **Needle herbs** (rosemary, thyme): horizontal stubs along a central stem

---

## Reference

| Field | Notes |
|-------|-------|
| Block IDs | Next available starts at 314; allocate 3 IDs (bush, young, mature) |
| Bush drop chance | 0.15–0.30; common herbs higher, rare lower |
| Drying Rack | Raw herb → dried herb; defined in `DRYING_TABLE` in herbalism.py |
| Tea additive | Optional; add to `_HERBAL_NOTES` and `HERBAL_ADDITIVES` in tea.py |
| Potion tier | `"basic"` = Alchemical Kiln; `"fine"` = Kiln + alchemy research; `"elixir"` = Resonance Chamber |
| Biome keys | Check [biomes.py](../../../biomes.py) or the existing `_BIOME_BUSHES` dict in world.py |

## Verification checklist

- [ ] Three block ID constants added in blocks.py (bush, young, mature)
- [ ] All five sets updated: `BUSH_BLOCKS`, `YOUNG_CROP_BLOCKS`, `MATURE_CROP_BLOCKS`, `PERENNIAL_CROP_MATURE`, `MATURE_TO_YOUNG_CROP`
- [ ] `BLOCKS` dict has entries for all three block IDs
- [ ] Herb bush added to at least one biome in `_BIOME_BUSHES` (world.py)
- [ ] Raw item, seed, and dried item added to `ITEMS` (items.py)
- [ ] Crop import added to items.py import block
- [ ] `DRYING_TABLE` and `INGREDIENT_DISPLAY_NAMES` updated (herbalism.py)
- [ ] Bush import and harvest drop added to player.py
- [ ] Import and render code added to renderer.py for all three block IDs
- [ ] (Optional) Tea additive entries added to tea.py
- [ ] (Optional) Potion recipe, desc, color, and buff entries added to herbalism.py + items.py
