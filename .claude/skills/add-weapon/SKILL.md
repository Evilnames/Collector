---
name: add-weapon
description: Step-by-step guide for adding a new weapon type to CollectorBlocks (with its forge shaping mini-game). Covers WEAPON_TYPES, PART_TEMPLATES, ASSEMBLY_HANDLES, the part/handle items, the handle recipe, and armorer/garrison pricing.
---

# Add a New Weapon

Weapons are data-driven: the forge UI, weapons codex, weapon rack, armorer, and Garrison Commander all read off the registries below. Adding a weapon is purely a matter of registering it in the right dicts/lists — no UI changes needed (unless you exceed the codex grid capacity, see Step 6).

Each weapon has:
- A **type** (e.g. `"sabre"`) with stats (damage, range, cooldown).
- One or more **smithed parts** with a 16×10 shaping template for the hammer mini-game.
- A **handle/haft** item assembled at the crafting bench from lumber.
- A **material** dimension (iron / gold / steel) — automatic, no work needed.

## Step 1 — Register the weapon in [weapons.py](../../../weapons.py)

Add four entries, all keyed by your new weapon type id (lowercase, snake_case).

```python
# WEAPON_TYPES — combat stats + which parts require smithing
"sabre": {"name": "Sabre", "parts": ["sabre_blade"], "base_damage": 3, "attack_range": 1, "cooldown": 0.55},

# PART_ITEM_PREFIX — maps part_key → item_id stem (material is prefixed at runtime)
"sabre_blade": "sabre_blade",

# ASSEMBLY_HANDLES — handle item consumed when assembling
"sabre": "sabre_grip",

# WEAPON_TYPE_ORDER — append to the list (or insert near similar weapons)
WEAPON_TYPE_ORDER = [..., "sabre"]
```

**Stat reference** (existing weapons for calibration):

| Type    | Damage | Range | Cooldown |
|---------|--------|-------|----------|
| dagger  | 2      | 1     | 0.40     |
| rapier  | 3      | 1     | 0.35     |
| sword   | 3      | 1     | 0.60     |
| spear   | 3      | 2     | 0.70     |
| glaive  | 4      | 2     | 0.85     |
| axe     | 4      | 1     | 0.90     |
| trident | 4      | 2     | 0.80     |
| mace    | 5      | 1     | 1.10     |
| halberd | 5      | 2     | 1.20     |
| scythe  | 6      | 2     | 1.30     |

Heavier / longer-reach weapons should have higher cooldown.

## Step 2 — Add the shaping template to PART_TEMPLATES

The forge mini-game is a 16-column × 10-row grid. `True` cells are metal that should remain (the part silhouette); `False` cells are excess the player hammers away. Use the `_row((lo, hi))` helper for contiguous ranges, or `_row_multi((lo1, hi1), (lo2, hi2), ...)` for non-contiguous shapes (e.g. the trident's three prongs).

```python
PART_TEMPLATES = {
    ...,
    "sabre_blade": [
        _row(( 9, 12)),  # curved tip
        _row(( 7, 11)),
        _row(( 5, 10)),
        _row(( 4,  9)),
        _row(( 4,  9)),
        _row(( 5,  9)),
        _row(( 6,  8)),
        _row(( 6,  8)),  # tang
        _row(( 6,  8)),
        _row(( 6,  8)),
    ],
}
```

Aim for **roughly 30–70 target cells out of 160**. Too few → trivial mini-game; too many → there's nothing to hammer. Existing reference (target / excess):

- rapier_blade  26 / 134  (very thin)
- dagger_blade  40 / 120
- sword_blade   44 / 116
- mace_head     68 /  92  (heaviest silhouette)

## Step 3 — Register part + handle items in [items.py](../../../items.py)

Add **3 metal parts** (one per material) and **1 handle** to the `ITEMS` dict, alongside the existing weapon entries near the `# --- Weapon Crafting ---` comment block.

```python
"iron_sabre_blade":  {"name": "Iron Sabre Blade",  "color": (160, 165, 175), "place_block": None, "weapon_part": True},
"gold_sabre_blade":  {"name": "Gold Sabre Blade",  "color": (220, 185,  50), "place_block": None, "weapon_part": True},
"steel_sabre_blade": {"name": "Steel Sabre Blade", "color": (110, 120, 135), "place_block": None, "weapon_part": True},

# Handle (placed in the second weapon block)
"sabre_grip": {"name": "Sabre Grip", "color": (139, 90, 43), "place_block": None},
```

The `weapon_part: True` flag matters — these items are held in `pending_parts`, not the regular inventory.

If the weapon has multiple parts (e.g. a hilt + blade), repeat the 3-material set for each part.

## Step 4 — Add the handle recipe to [crafting.py](../../../crafting.py)

Add an entry to the `ARTISAN_RECIPES` list (search for the `# Weapon handles (crafting bench)` comment — handles live there, not in `RECIPES`):

```python
{"name": "Sabre Grip", "ingredients": {"lumber": 2}, "output_id": "sabre_grip", "output_count": 1},
```

**Lumber cost guidance**: dagger/rapier handles = 1, short hafts (sword/mace/axe) = 2, full polearms (spear/glaive/trident) = 3, long polearms (halberd/scythe) = 4.

## Step 5 — Update pricing + quest pool in [cities.py](../../../cities.py)

Two edits, both near `class WeaponArmorerNPC`:

```python
# Base sale price at the Weapon Armorer (gold)
_WEAPON_ARMORER_BASE = {..., "sabre": 33}

# Garrison Commander quest pool — add the new weapon id
def _build_garrison_quest(rng, difficulty):
    wtype = rng.choice([..., "sabre", None])
```

**Price guidance**: roughly proportional to base damage × cooldown × range — see existing values (rapier 32, sword 35, axe 40, scythe 60).

## Step 6 — Codex grid capacity check (only if exceeding 10 weapons)

The Weapons Codex in [UI/collections.py](../../../UI/collections.py) renders a vertical grid with one row per weapon type. Current sizing (`CELL_W, CELL_H, GAP = 130, 44, 6`) fits up to 10 rows on a 720px screen. If you push past 10, shrink `CELL_H`/`GAP` further or change the codex to a 2-column layout.

## Verification

```bash
python3 -c "
import weapons, crafting, cities
from items import ITEMS
artisan_ids = {r['output_id'] for r in crafting.ARTISAN_RECIPES}
for wt in weapons.WEAPON_TYPE_ORDER:
    h = weapons.ASSEMBLY_HANDLES[wt]
    assert h in artisan_ids and h in ITEMS
    assert wt in cities._WEAPON_ARMORER_BASE
    for mat in weapons.MATERIAL_ORDER:
        for pk in weapons.WEAPON_TYPES[wt]['parts']:
            assert f'{mat}_{weapons.PART_ITEM_PREFIX[pk]}' in ITEMS
            assert pk in weapons.PART_TEMPLATES
            t = weapons.PART_TEMPLATES[pk]
            assert len(t) == 10 and all(len(r) == 16 for r in t)
print('OK')
"
```

## Verification checklist

- [ ] `WEAPON_TYPES`, `PART_ITEM_PREFIX`, `ASSEMBLY_HANDLES`, `WEAPON_TYPE_ORDER` all updated in [weapons.py](../../../weapons.py)
- [ ] `PART_TEMPLATES` entry has 10 rows × 16 cells, with 30–70 target cells
- [ ] All 3 material variants of each part added to `ITEMS` with `weapon_part: True`
- [ ] Handle item added to `ITEMS`
- [ ] Handle recipe added to `ARTISAN_RECIPES` (not `RECIPES`)
- [ ] Armorer base price added to `_WEAPON_ARMORER_BASE`
- [ ] Quest weapon pool updated in `_build_garrison_quest`
- [ ] Smoke-test snippet above runs clean
- [ ] In-game: forge mini-game shows correct silhouette; weapon appears in codex/rack; Armorer appraises it; Garrison quest can request it
