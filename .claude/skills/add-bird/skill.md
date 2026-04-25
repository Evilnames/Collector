---
name: add-bird
description: Step-by-step guide for adding a new bird species to CollectorBlocks. Covers class definition, required attributes, registration in ALL_SPECIES, and renderer draw method.
---

# Add a New Bird

Birds are class-based entities defined in [birds.py](../../../birds.py). Each species is a subclass of `Bird` with class-level attributes. **Every new bird also requires a draw function in [Render/birds.py](../../../Render/birds.py)** — without it the bird spawns invisibly.

## Step 1 — Define the class

Add a new class near the end of [birds.py](../../../birds.py), before `ALL_SPECIES`. Use an existing bird as a reference (e.g., `Robin` for a simple common bird, `Eagle` for a rare soaring bird).

```python
class GoldenOriole(Bird):
    SPECIES       = "golden_oriole"        # lowercase, underscore-separated, unique
    RARITY        = "uncommon"             # "common", "uncommon", or "rare"
    BIOMES        = ["temperate", "jungle"] # [] = spawns in any biome
    IS_FLOCK      = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)             # height range above ground
    SPEED            = 70.0               # pixels/second
    W, H             = 14, 10             # sprite size in pixels
    BODY_COLOR    = (220, 180, 20)        # RGB
    WING_COLOR    = (30,  30,  30)
    BEAK_COLOR    = (200, 140, 40)
    HEAD_COLOR    = (220, 180, 20)
    ACCENT_COLOR  = (255, 220, 50)
```

**Flock birds** need `IS_FLOCK = True` and a `FLOCK_SIZE_RANGE` larger than `(1, 1)` — see `Starling` for an example.

## Step 2 — Register in ALL_SPECIES

Find `ALL_SPECIES` near the bottom of [birds.py](../../../birds.py) and add the new class:

```python
ALL_SPECIES = [
    Robin, BlueJay, ..., GoldenOriole,  # add here
]
```

`SPECIES_BY_ID` is auto-generated from `ALL_SPECIES` — no extra step needed.

## Step 3 — Add a dispatch entry in Render/birds.py

In `_draw_bird` inside [Render/birds.py](../../../Render/birds.py), add an `elif` branch after the last existing entry (search for the final `elif sp ==` line):

```python
elif sp == "golden_oriole":
    _draw_golden_oriole(screen, bird, sx, sy, wing_flap, perching)
```

## Step 4 — Add the draw function in Render/birds.py

Add the `_draw_*` function at the bottom of [Render/birds.py](../../../Render/birds.py). All draw functions receive `(screen, bird, sx, sy, wf, perching)` where `wf` is the wing-flap offset (0 when perching).

Use the bird's class-level color constants and `W`/`H` for all geometry. The standard structure is:

```python
def _draw_golden_oriole(screen, bird, sx, sy, wf, perching):
    W, H = bird.W, bird.H
    f = bird.facing           # 1 = right, -1 = left

    # Wings (drawn first so body overlaps them)
    if not perching:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx, sy + int(wf), W, H - 2))
    else:
        pygame.draw.ellipse(screen, bird.WING_COLOR,
                            (sx + 1, sy + 2, W - 2, H - 3))

    # Body
    pygame.draw.ellipse(screen, bird.BODY_COLOR,
                        (sx + 2, sy + 3, W - 4, H - 4))

    # Head — offset to facing side
    hx = sx + W - 5 if f == 1 else sx + 1
    pygame.draw.circle(screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)

    # Beak
    bx = hx + 5 if f == 1 else hx - 3
    pygame.draw.rect(screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

    # Eye
    pygame.draw.rect(screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
```

### Draw method tips

| Shape | Use for |
|-------|---------|
| Tall bird (heron/crane) | Long legs: two `pygame.draw.rect` calls before wings; neck as a `rect`, head as a small `circle` |
| Soaring bird (eagle/condor) | Widen wings with `W + 4` and offset `sx - 2`; add hooked beak with two rects |
| Ground bird (pheasant) | Draw tail rect first (behind body), keep `ALTITUDE_BLOCKS` low |
| Flock/small bird | Use smaller `W, H` (10×8); skip legs; keep draw calls minimal |

## Reference

| Attribute | Options / Notes |
|-----------|----------------|
| `RARITY` | `"common"`, `"uncommon"`, `"rare"` |
| `BIOMES` | Any biome key from [biomes.py](../../../biomes.py); `[]` = universal |
| `ALTITUDE_BLOCKS` | `(min, max)` blocks above ground; higher = soaring bird |
| `SPEED` | 50–90 typical range |
| `W, H` | Sprite size; most birds are 14×10 or 16×12 |
| Colors | RGB tuples `(r, g, b)`, values 0–255 |

## Verification checklist

- [ ] `SPECIES` string is unique across all classes in `ALL_SPECIES`
- [ ] `BIOMES` entries are valid keys (check [biomes.py](../../../biomes.py))
- [ ] Class added to `ALL_SPECIES`
- [ ] Dispatch `elif` added to `_draw_bird` in [Render/birds.py](../../../Render/birds.py)
- [ ] `_draw_*` function added to [Render/birds.py](../../../Render/birds.py)
- [ ] Run the game and visit the relevant biome — bird should spawn, be visible, and appear in the Codex
