---
name: add-reptile
description: Step-by-step guide for adding a new reptile (or frog) species to CollectorBlocks. Covers class definition, required attributes, registration in ALL_REPTILE_SPECIES, and the frog body type renderer.
---

# Add a New Reptile (or Frog)

Reptiles and frogs are class-based entities defined in [reptiles.py](../../../reptiles.py). Each species is a subclass of `Reptile` with class-level attributes. **No renderer changes are needed** — the draw function in [Render/reptiles.py](../../../Render/reptiles.py) dispatches automatically by `BODY_TYPE`. The only exception is if you add a brand new `BODY_TYPE` (see Step 3 below).

## Step 1 — Define the class

Add a new class in [reptiles.py](../../../reptiles.py) inside the appropriate section (snakes, lizards, turtles, or frogs), before `ALL_REPTILE_SPECIES`.

### Snake example

```python
class KingSnake(Reptile):
    SPECIES       = "king_snake"          # lowercase, underscore-separated, unique
    RARITY        = "common"              # "common", "uncommon", or "rare"
    BIOMES        = ["temperate", "boreal"]  # [] = spawns in any biome
    BODY_TYPE     = "snake"
    SPEED         = 32.0                  # px/s while patrolling
    W, H          = 18, 6                 # sprite size in pixels
    BODY_COLOR    = (28, 25, 18)          # RGB
    PATTERN_COLOR = (230, 228, 218)
    BELLY_COLOR   = (240, 238, 222)
```

### Lizard example

```python
class SandLizard(Reptile):
    SPECIES       = "sand_lizard"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "steppe"]
    BODY_TYPE     = "lizard"
    SPEED         = 38.0
    W, H          = 14, 6
    BODY_COLOR    = (170, 150, 95)
    PATTERN_COLOR = (120, 100, 58)
    BELLY_COLOR   = (225, 215, 180)
```

### Turtle / tortoise example

```python
class StarTortoise(Reptile):
    SPECIES       = "star_tortoise"
    RARITY        = "uncommon"
    BIOMES        = ["tropical", "savanna"]
    BODY_TYPE     = "turtle"
    SPEED         = 9.0
    PATROL_RANGE  = 26                    # px each side of spawn before turning
    W, H          = 13, 10
    BODY_COLOR    = (28, 25, 18)
    PATTERN_COLOR = (215, 195, 95)
    BELLY_COLOR   = (205, 190, 148)
```

### Frog / toad example

```python
class RainFrog(Reptile):
    SPECIES       = "rain_frog"
    RARITY        = "common"
    BIOMES        = ["savanna", "tropical"]
    BODY_TYPE     = "frog"
    SPEED         = 35.0
    PATROL_RANGE  = 28
    W, H          = 10, 8
    BODY_COLOR    = (130, 115, 75)
    PATTERN_COLOR = (88, 78, 48)
    BELLY_COLOR   = (220, 215, 185)
```

## Step 2 — Register in ALL_REPTILE_SPECIES

Find `ALL_REPTILE_SPECIES` near the bottom of [reptiles.py](../../../reptiles.py) and add the new class in the appropriate section comment:

```python
ALL_REPTILE_SPECIES = [
    # Snakes ...
    KingSnake,       # add here
    # Lizards ...
    # Turtles ...
    # Frogs ...
]
```

That's it — discovery, spawning, save/load, and the Codex tab all pick it up automatically.

## Step 3 — New BODY_TYPE only (rare)

The four supported body types are `"snake"`, `"lizard"`, `"turtle"`, and `"frog"`. If you need a new one (e.g. `"crocodilian"`):

1. Add a `_draw_crocodilian()` function to [Render/reptiles.py](../../../Render/reptiles.py)
2. Add an `elif bt == "crocodilian":` branch in `_draw_reptile()` in the same file
3. Add a matching icon drawing path in `_draw_reptile_codex()` in [UI/collections.py](../../../UI/collections.py)

## Reference

### Body types and their rendered appearance

| `BODY_TYPE` | Rendered as |
|-------------|-------------|
| `"snake"` | Three connected ellipses (tail → mid → head), belly stripe, pattern bands |
| `"lizard"` | Ellipse body, 4 leg lines, tail ellipse, circle head, pattern dots |
| `"turtle"` | Dome polygon shell with scute lines, stubby legs, peeking head |
| `"frog"` | Wide squat body, prominent gold eyes on top, bent back legs, belly patch |

### Valid biomes (from [biomes.py](../../../biomes.py))

`temperate`, `boreal`, `birch_forest`, `jungle`, `wetland`, `redwood`, `tropical`, `savanna`, `wasteland`, `alpine_mountain`, `rocky_mountain`, `rolling_hills`, `steep_hills`, `steppe`, `arid_steppe`, `desert`, `tundra`, `swamp`, `beach`, `canyon`, `mediterranean`, `east_asian`, `south_asian`

**Common mistakes:** `"wetlands"` (use `"wetland"`), `"forest"` (use `"boreal"`), `"grassland"` (use `"steppe"`), `"mesa"` (use `"canyon"`), `"badlands"` (use `"wasteland"`), `"ocean_beach"` (use `"beach"`). Wrong biome names produce no candidates and the species silently never spawns.

### Optional class attributes

| Attribute | Default | Notes |
|-----------|---------|-------|
| `SPEED` | `30.0` | px/s while patrolling; snakes ~30–45, turtles ~6–14, frogs ~35–55 |
| `PATROL_RANGE` | `48` | px each side of spawn before turning; turtles/tortoises use 20–36 |
| `SPOOK_RADIUS` | `6` | blocks — fast player within this triggers flee |
| `OBS_RADIUS` | `4` | blocks — slow player within this accumulates discovery timer |
| `W, H` | `16, 8` | sprite bounding box in pixels |

### Discovery mechanic

Reptiles are discovered by **slow approach** — no tool required. The player must stay within `OBS_RADIUS` blocks moving slower than `OBS_SPEED_THRESH` (40 px/s) for 1.5 seconds. Fast movement within `SPOOK_RADIUS` causes the reptile to flee without discovery.

### Spawning rules

- Spawns on **solid land surface only** — water tiles are skipped.
- Biome must match `cls.BIOMES`, or `BIOMES = []` to spawn anywhere.
- Spawn rate: ~35% chance per 10-block spacing within a chunk.
- Seeded per-chunk — same seed produces the same reptiles each world load.

## Verification checklist

- [ ] `SPECIES` string is unique across all entries in `ALL_REPTILE_SPECIES`
- [ ] `BIOMES` entries are valid keys from the table above (no `"wetlands"`, `"forest"`, etc.)
- [ ] `BODY_TYPE` is one of: `"snake"`, `"lizard"`, `"turtle"`, `"frog"`
- [ ] Class added to `ALL_REPTILE_SPECIES`
- [ ] Run `python3 -m py_compile reptiles.py` — should produce no output
- [ ] Run the game, visit the relevant biome — reptile should spawn, be visible, and appear in the REPTILES Codex tab
