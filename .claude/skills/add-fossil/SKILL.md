---
name: add-fossil
description: Step-by-step guide for adding a new fossil type to CollectorBlocks. Covers FOSSIL_TYPES entry with age, depth, patterns, and specials_pool.
---

# Add a New Fossil

Fossils are dictionary-based entities defined in [fossils.py](../../../fossils.py). Each type is an entry in `FOSSIL_TYPES`. Individual found fossils are generated as `Fossil` dataclass instances by `FossilGenerator`.

`FOSSIL_TYPE_ORDER` auto-sorts by `min_depth` — no manual list maintenance needed.

## Step 1 — Add an entry to FOSSIL_TYPES

Add a new key to `FOSSIL_TYPES` in [fossils.py](../../../fossils.py). Group it with fossils from the same `age` era.

```python
"plesiosaur_vertebra": {
    "min_depth": 115,
    "age": "mesozoic",
    "rarity_pool": ["uncommon", "rare", "rare", "epic"],
    "color_pool": [
        ((175, 160, 130), (120, 100, 75)),
        ((190, 170, 140), (135, 115, 85)),
    ],
    "patterns": ["smooth", "ridged", "fractured"],
    "specials_pool": ["complete", "mineralized", "impression"],
},
```

**age** determines the era label shown in the Codex. Must be one of the three valid values.

**min_depth** sets the shallowest block level. Shallower = paleozoic; deeper = cenozoic.

**rarity_pool**: repeat entries to weight probability.

**patterns**: list drawn from randomly; repeat a pattern to increase its frequency.

**specials_pool**: qualities that can appear on a generated fossil instance. Use relevant ones from the table below.

## Reference

| Field | Options / Notes |
|-------|----------------|
| `age` | `"paleozoic"` (depth ~50–100), `"mesozoic"` (~100–150), `"cenozoic"` (~150+) |
| `min_depth` | Integer block depth |
| `rarity_pool` | Mix of `"common"`, `"uncommon"`, `"rare"`, `"epic"`, `"legendary"` |
| `color_pool` | List of `(primary, secondary)` RGB tuples; 2+ pairs recommended |
| `patterns` | `"smooth"`, `"ridged"`, `"spiral"`, `"fractured"` |
| `specials_pool` | `"complete"`, `"mineralized"`, `"impression"`, `"carbonized"`, `"opalized"`, `"amber_trace"` |

**specials guidance:**
- `"complete"` — unusually whole specimen; use for vertebrae, shells, teeth
- `"mineralized"` — replaced by minerals; universal
- `"impression"` — surface imprint only; good for soft-bodied fossils
- `"carbonized"` — carbon film; suits plant material and soft tissue
- `"opalized"` — replaced by opal; rare and valuable, use sparingly
- `"amber_trace"` — preserved in amber trace; suits insects and small flora

## Verification checklist

- [ ] Dict key is unique in `FOSSIL_TYPES`
- [ ] `age` matches the intended era
- [ ] Run the game and mine at the target depth — fossil should generate and appear in the Codex
