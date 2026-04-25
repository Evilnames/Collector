---
name: add-pottery
description: Step-by-step guide for adding a new clay biome to CollectorBlocks. Covers CLAY_BIOME_PROFILES, _TEXTURE_NOTE_POOLS, _CODEX_BIOMES, BIOME_DISPLAY_NAMES, and world.py clay deposit spawning.
---

# Add a New Clay Biome

The Pottery & Ceramics system is biome-driven in [pottery.py](../../../pottery.py). Each biome produces clay with distinct thickness, evenness, and glaze affinity characteristics. Adding a new biome means touching `CLAY_BIOME_PROFILES`, `_TEXTURE_NOTE_POOLS`, `_CODEX_BIOMES`, `BIOME_DISPLAY_NAMES`, and the underground spawning condition in [world.py](../../../world.py).

Current biomes: **wetland** (earthenware), **tropical** (porcelain), **temperate** (stoneware), **river** (slipware).

---

## Step 1 — Add a profile to CLAY_BIOME_PROFILES (pottery.py)

Each profile maps to a clay variety with base attributes 0.0–1.0. The generator applies a small gaussian jitter per piece.

```python
CLAY_BIOME_PROFILES = {
    ...
    "desert": {
        "thickness":    0.75,   # walls are moderately thick
        "evenness":     0.50,   # rough hand-built feel
        "variety":      "terracotta",   # display label for the clay type
        "glaze_affinity": 0.30,  # harder to glaze; dry clay resists slip
    },
}
```

**Attribute guide:**
| Attribute | Low | High |
|---|---|---|
| `thickness` | thin-walled, delicate | thick, durable |
| `evenness` | rustic, irregular | perfectly uniform walls |
| `glaze_affinity` | glaze pools and runs | glaze sits evenly |

---

## Step 2 — Add texture note pool (pottery.py)

The generator picks 2–4 texture notes from this pool to describe the piece. Add a list of 5 evocative strings:

```python
_TEXTURE_NOTE_POOLS = {
    ...
    "desert": ["sandy inclusions", "sun-baked surface", "ochre swirls", "cracked rim", "dusty matte finish"],
}
```

---

## Step 3 — Add to _CODEX_BIOMES and BIOME_DISPLAY_NAMES (pottery.py)

`_CODEX_BIOMES` drives the codex grid column order. `TYPE_ORDER` is built from it automatically — no separate change needed.

```python
_CODEX_BIOMES = ["wetland", "tropical", "temperate", "river", "desert"]

BIOME_DISPLAY_NAMES = {
    ...
    "desert": "Desert",
}
```

---

## Step 4 — Enable clay deposit spawning (world.py)

In `_pick_block()` around line 1261, the clay deposit condition reads:

```python
if depth < 35 and biome in ("sedimentary", "temperate", "wetland", "river", "swamp"):
```

Add the new world biome key to this tuple:

```python
if depth < 35 and biome in ("sedimentary", "temperate", "wetland", "river", "swamp", "desert"):
```

**Note:** The biome key here is the world generation biome name (from [biomes.py](../../../biomes.py)), not the pottery display name. Check that the biome key matches what `world.get_biodome(bx)` returns.

---

## How the biome is recorded on a piece

When the player completes a piece at the Pottery Wheel, the mixin calls `player.world.get_biodome(bx)` and maps the world biome key to a clay biome via `clay_biome_map` in `_complete_pottery_wheel()` in [UI/pottery.py](../../../UI/pottery.py):

```python
clay_biome_map = {
    "wetland":  "wetland",
    "river":    "river",
    "swamp":    "wetland",
    "tropical": "tropical",
    "jungle":   "tropical",
}
# Everything else → "temperate"
```

If the new biome needs a non-default mapping, add it here:

```python
"desert":      "desert",
"arid_steppe": "desert",
```

---

## Codex discovery key

Discovery is tracked as `"biome_firinglevel"` strings in `player.discovered_pottery`. The codex grid (in `_draw_pottery_codex`) iterates `_CODEX_BIOMES × FIRING_LEVELS[1:]` automatically — no codex changes needed.

Firing levels tracked: `intact`, `fine`, `masterwork` (cracked pieces are not recorded).

---

## Verification checklist

- [ ] New biome key in `CLAY_BIOME_PROFILES` with all 4 fields
- [ ] 5-item texture note list in `_TEXTURE_NOTE_POOLS`
- [ ] Key appended to `_CODEX_BIOMES`
- [ ] Display name in `BIOME_DISPLAY_NAMES`
- [ ] World biome key added to the `biome in (...)` tuple in `world.py _pick_block()`
- [ ] `clay_biome_map` in `UI/pottery.py _complete_pottery_wheel()` maps the world biome to the new key
- [ ] Mine clay in the biome and shape a piece → clay_biome should be the new key
- [ ] Fire the piece → codex should show a new column for the biome
