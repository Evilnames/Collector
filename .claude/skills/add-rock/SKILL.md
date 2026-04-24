---
name: add-rock
description: Step-by-step guide for adding a new rock type to CollectorBlocks. Covers ROCK_TYPES entry and optional ROCK_BIOME_AFFINITY registration.
---

# Add a New Rock

Rocks are dictionary-based entities defined in [rocks.py](../../../rocks.py). Each type is an entry in `ROCK_TYPES`. Individual found rocks are generated as `Rock` dataclass instances by `RockGenerator`.

`ROCK_TYPE_ORDER` auto-sorts by `min_depth` — no manual list maintenance needed.

## Step 1 — Add an entry to ROCK_TYPES

Add a new key to `ROCK_TYPES` in [rocks.py](../../../rocks.py). Group it near rocks of similar `min_depth` for readability.

```python
"rose_quartz": {
    "min_depth": 25,
    "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
    "color_pool": [
        ((240, 190, 200), (200, 140, 160)),
        ((250, 200, 210), (210, 155, 170)),
    ],
    "patterns": ["solid", "veined", "speckled"],
},
```

**min_depth** sets the shallowest block level the rock spawns at. Lower = shallower.

**rarity_pool**: repeat entries to weight probability — e.g. `["common", "common", "uncommon"]` = 2/3 chance common.

**color_pool**: list of `(primary_rgb, secondary_rgb)` pairs; one is picked per rock instance.

**patterns**: list drawn from randomly; repeat a pattern to make it more likely.

Available patterns: `"solid"`, `"banded"`, `"veined"`, `"spotted"`, `"speckled"`.

## Step 2 — Add to ROCK_BIOME_AFFINITY (optional)

If the rock should be biome-biased (more likely to generate in certain terrain), add its key to the relevant set in `ROCK_BIOME_AFFINITY`:

```python
ROCK_BIOME_AFFINITY = {
    "igneous":     {...},
    "sedimentary": {..., "rose_quartz"},   # add here for sedimentary bias
    "crystal":     {..., "rose_quartz"},   # or here for crystal-heavy biomes
    "ferrous":     {...},
    "void":        {...},
}
```

Rocks not in any affinity set can still generate anywhere — affinity just makes them preferred in matching biomes.

## Reference

| Field | Options / Notes |
|-------|----------------|
| `min_depth` | Integer block depth; reference: granite=6, quartz=20, voidite=180 |
| `rarity_pool` | Mix of `"common"`, `"uncommon"`, `"rare"`, `"epic"`, `"legendary"` |
| `color_pool` | List of `(primary, secondary)` RGB tuples; 2+ pairs recommended |
| `patterns` | Subset of `"solid"`, `"banded"`, `"veined"`, `"spotted"`, `"speckled"` |
| Biome affinity | `"igneous"`, `"sedimentary"`, `"crystal"`, `"ferrous"`, `"void"` |

## Verification checklist

- [ ] Dict key is unique in `ROCK_TYPES`
- [ ] Added to `ROCK_BIOME_AFFINITY` if biome-specific
- [ ] Run the game and mine at the target depth — rock should generate and appear in the Codex
