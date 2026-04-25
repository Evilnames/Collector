---
name: add-insect
description: Step-by-step guide for adding a new insect species to CollectorBlocks. Covers class definition, required attributes, and registration in ALL_INSECT_SPECIES.
---

# Add a New Insect

Insects are class-based entities defined in [insects.py](../../../insects.py). Each species is a subclass of `Insect` with class-level attributes. The total species count displayed in the Codex header is hardcoded to 30 in [UI/collections.py](../../../UI/collections.py) — update it if you add species.

## Step 1 — Define the class

Add a new class near the end of [insects.py](../../../insects.py), inside the appropriate family section, before `ALL_INSECT_SPECIES`. Use an existing species in the same family as a reference.

```python
class VioletEmperor(Insect):
    SPECIES      = "violet_emperor"   # lowercase, underscore-separated, unique
    RARITY       = "rare"             # "common", "uncommon", or "rare"
    BIOMES       = ["wetland", "swamp"]  # [] = spawns in any biome
    W, H         = 14, 6             # sprite size in pixels
    BODY_COLOR   = (80, 20, 140)     # elongated body
    WING_COLOR   = (160, 80, 220)    # wings
    ACCENT_COLOR = (210, 160, 255)   # spots / highlights
    HOVER_RANGE  = 60                # pixel radius around spawn point (default 40)
    SPEED        = 32.0              # pixels/second (default 28)
    WING_TYPE    = "dragonfly"       # see Wing Types table below
```

## Step 2 — Register in ALL_INSECT_SPECIES

Find `ALL_INSECT_SPECIES` near the bottom of [insects.py](../../../insects.py) and add the new class in the appropriate family section:

```python
ALL_INSECT_SPECIES = [
    # Dragonflies
    EmperorDragonfly, AzureDamselfly, BroadBodiedChaser,
    ScarceChaser, BandedDemoiselle, VioletEmperor,  # add here
    ...
]
```

`INSECT_SPECIES_BY_ID` is auto-generated from `ALL_INSECT_SPECIES` — no extra step needed.

## Step 3 — Update the Codex total

In [UI/collections.py](../../../UI/collections.py), find the line:

```python
n_insect_total  = 30
```

Increment it to match the new species count.

## Reference

### Wing Types

| `WING_TYPE` | Description | Rendered as |
|-------------|-------------|-------------|
| `"butterfly"` | Two large symmetrical wings | Paired ellipses, accent spots |
| `"moth"` | Broad flat wings, muted | Single wide ellipse, accent overlay |
| `"dragonfly"` | 4 narrow wings, long body | 4 thin ellipses, segmented body |
| `"firefly"` | Small oval body + glowing tail | Compact oval + accent dot (glows) |
| `"beetle"` | Oval elytra with centre seam | Oval with dividing line, accent head |
| `"other"` | Generic catch-all | Wing ellipse + body ellipse + accent dot |

Draw logic for each wing type lives in [Render/insects.py](../../../Render/insects.py). If you need a new `WING_TYPE`, add a `_draw_insect_*` function there and a matching branch in `_draw_insect`.

### Biomes (from [biomes.py](../../../biomes.py))

`temperate`, `boreal`, `birch_forest`, `jungle`, `wetland`, `redwood`, `tropical`, `savanna`, `wasteland`, `fungal`, `alpine_mountain`, `rocky_mountain`, `rolling_hills`, `steep_hills`, `steppe`, `arid_steppe`, `desert`, `tundra`, `swamp`, `beach`, `canyon`

### Attribute ranges

| Attribute | Typical range / notes |
|-----------|----------------------|
| `RARITY` | `"common"`, `"uncommon"`, `"rare"` |
| `BIOMES` | Any biome key above; `[]` = universal |
| `W, H` | 7–16 × 5–12 pixels |
| `HOVER_RANGE` | 30–80 pixels (smaller = stays close to spawn) |
| `SPEED` | 20–40 pixels/second |
| Colors | RGB tuples `(r, g, b)`, values 0–255 |

### Spawning rules

Insects only spawn near **wildflower patches** (`WILDFLOWER_PATCH` blocks) or **water-adjacent tiles**. A new species won't appear in a biome that has neither — keep that in mind when choosing `BIOMES`.

## Verification checklist

- [ ] `SPECIES` string is unique across all classes in `ALL_INSECT_SPECIES`
- [ ] `WING_TYPE` is one of the six valid values
- [ ] `BIOMES` entries are valid keys from [biomes.py](../../../biomes.py)
- [ ] Class added to `ALL_INSECT_SPECIES` in the correct family section
- [ ] `n_insect_total` updated in [UI/collections.py](../../../UI/collections.py)
- [ ] Run the game, visit the relevant biome near wildflowers/water — insect should spawn and appear in the Codex
