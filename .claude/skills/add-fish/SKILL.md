---
name: add-fish
description: Step-by-step guide for adding a new fish species to CollectorBlocks. Covers FISH_TYPES entry, FISH_TYPE_ORDER, and FISH_BIOME_GROUPS registration.
---

# Add a New Fish

Fish are dictionary-based entities defined in [fish.py](../../../fish.py). Each species is an entry in `FISH_TYPES`, and individual caught fish are generated as `Fish` dataclass instances by `FishGenerator`.

## Step 1 — Add an entry to FISH_TYPES

Add a new key to the `FISH_TYPES` dict in [fish.py](../../../fish.py). Group it near other fish from the same biome or habitat for readability.

```python
"golden_koi": {
    "name": "Golden Koi",
    "rarity_pool": ["uncommon", "uncommon", "rare", "epic"],
    "habitat": "lake",                    # "river" or "lake"
    "biome_affinity": ["temperate"],      # [] = catchable anywhere
    "weight_range": (0.5, 8.0),           # kg, (min, max)
    "length_range": (20, 65),             # cm, (min, max)
    "pattern_pool": ["scaled", "spotted", "plain"],
    "colors": [
        ((230, 180, 40),  (200, 120, 20)),  # (primary_rgb, secondary_rgb)
        ((240, 210, 80),  (180, 100, 10)),
        ((255, 255, 255), (220, 160, 60)),  # white variant
    ],
    "description": "A prized ornamental fish with brilliant golden scales.",
},
```

**Rarity pool**: repeated entries increase probability. `"common"` x3 + `"uncommon"` x1 = 75% common, 25% uncommon.

Available patterns: `"striped"`, `"plain"`, `"spotted"`, `"banded"`, `"mottled"`, `"scaled"`, `"plated"`.

## Step 2 — Add to FISH_TYPE_ORDER

Find `FISH_TYPE_ORDER` near the bottom of [fish.py](../../../fish.py) and insert the key in the appropriate position (grouped by biome/habitat):

```python
FISH_TYPE_ORDER = [
    ..., "golden_koi", ...
]
```

## Step 3 — Add to FISH_BIOME_GROUPS (if biome-specific)

If `biome_affinity` is non-empty, add the key to the matching group in `FISH_BIOME_GROUPS`:

```python
FISH_BIOME_GROUPS = [
    ("Temperate", [..., "golden_koi", ...]),
    ...
]
```

Skip this step for universal fish (`biome_affinity: []`).

## Reference

| Field | Options / Notes |
|-------|----------------|
| `habitat` | `"river"` or `"lake"` |
| `biome_affinity` | Biome key list from [biomes.py](../../../biomes.py); `[]` = universal |
| `rarity_pool` | Any mix of `"common"`, `"uncommon"`, `"rare"`, `"epic"`, `"legendary"` |
| `weight_range` | `(min_kg, max_kg)`; reference: minnow 0.03–0.25, tuna 10–120 |
| `length_range` | `(min_cm, max_cm)`; reference: minnow 4–12, tuna 80–300 |
| `pattern_pool` | Subset of the 7 available patterns |
| `colors` | List of `(primary, secondary)` RGB tuple pairs; one is picked at generation |

## Verification checklist

- [ ] Dict key is unique in `FISH_TYPES`
- [ ] `biome_affinity` entries are valid keys (check [biomes.py](../../../biomes.py))
- [ ] Added to `FISH_TYPE_ORDER`
- [ ] Added to the correct group in `FISH_BIOME_GROUPS` (if biome-specific)
- [ ] Run the game, go fishing in the target biome/habitat — fish should appear and be trackable in the Codex
