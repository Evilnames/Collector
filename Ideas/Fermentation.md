# Fermentation System

## Concept

A recipe-driven fermentation system where quality depends on **what ingredients you combine** and **how long you ferment them** — not the biome. Player packs vegetables into a crock, tends the ferment during a mini-game, and harvests a finished product (kimchi, sauerkraut, pickles, etc.). This is the first collectible system with no biome dependency; recipes are discovered through ingredient experimentation.

---

## New Blocks (next free ID: 1636)

| Constant | ID | Purpose |
|---|---|---|
| `FERMENT_CROCK_BLOCK` | 1636 | Crafting station — opens fermentation UI |
| `CUCUMBER_CROP_YOUNG` | 1637 | Growing cucumber plant |
| `CUCUMBER_CROP_MATURE` | 1638 | Harvestable cucumber plant |

Cucumber is added because pickles are explicitly requested and no cucumber exists in the game. All other recipes use existing vegetables (cabbage, radish, carrot, garlic, pepper, onion, beet, turnip, leek, zucchini, tomato).

---

## Recipes (10 total)

Each recipe defines **required** ingredients + **optional** boosters. The system auto-detects the best-matching recipe from whatever the player packs.

| Key | Required | Optional Boosters |
|---|---|---|
| `kimchi` | cabbage ×2 | radish, garlic, pepper (spicy boost) |
| `sauerkraut` | cabbage ×3 | carrot, leek |
| `dill_pickles` | cucumber ×3 | garlic |
| `pickled_beets` | beet ×2 | turnip |
| `fermented_turnips` | turnip ×3 | beet (color/sweetness) |
| `fermented_carrots` | carrot ×3 | garlic |
| `hot_sauce` | pepper ×4 | garlic, onion |
| `fermented_salsa` | tomato ×2 + pepper ×1 + onion ×1 | garlic |
| `pickled_radish` | radish ×4 | — |
| `garlic_confit` | garlic ×6 | — |

Unmatched combinations → `plain_ferment` (low quality fallback).

---

## Output Items (30 + 4 utility)

Each recipe has three quality tiers driven by mini-game performance:
- Base (quality < 0.4): `kimchi`, `sauerkraut`, etc.
- Fine (0.4–0.7): `kimchi_fine`, `sauerkraut_fine`, etc.
- Superior (≥ 0.7): `kimchi_superior`, `sauerkraut_superior`, etc.

Utility items: `ferment_crock_item` (places block), `cucumber_seed` (places young crop), `cucumber` (raw harvest), `table_salt` (ingredient, purchasable from merchants).

**Buffs on consumed output:**
- `probiotic` — passive health regen for 90s
- `spicy` — heat resistance + melee speed for 60s (kimchi / hot_sauce / fermented_salsa)
- `tangy` — stamina/energy for 90s (sauerkraut / pickles)
- `prebiotic` — hunger efficiency (food lasts longer) for 120s
- `umami` — cooking quality synergy bonus for 60s (garlic_confit / fermented_salsa)

---

## Data Module: `fermentation.py`

```python
@dataclass
class FermentedBatch:
    uid: str
    recipe_key: str          # "kimchi", "sauerkraut", etc.
    ingredients: dict        # {item_id: count} — JSON-serialized
    salt_level: float        # 0.0–1.0 (ideal 0.35–0.55)
    vessel_type: str         # "ceramic_crock" | "glass_jar" | "oak_barrel"
    ferment_time_frac: float # 0.0–1.0 (how far through optimal window)
    sourness: float          # rises with ferment time
    heat: float              # from pepper content
    complexity: float        # more ingredients = higher
    crunch: float            # falls with over-fermentation
    quality: float           # composite
    flavor_notes: list
    seed: int
    blend_components: list = field(default_factory=list)
```

Key module contents:
- `FERMENT_RECIPES` — 10 recipe dicts (required, optional, ideal_salt, ideal_days, buff_key, flavor_base)
- `VESSEL_TYPES` — 3 vessels with attribute modifiers (ceramic +sourness, glass +crunch, oak +complexity)
- `FERMENT_TIME_BANDS` — under (0–0.25) / active (0.25–0.65) / peak (0.65–0.8) / over (0.8–1.0)
- `_FLAVOR_POOLS` — per-attribute flavor note lists + per-recipe exclusive notes
- `detect_recipe(ingredients)` — scores each recipe by required+optional match, returns best key
- `apply_ferment_result(batch, salt_band_frac, burp_score, time_frac, vessel_type, penalties)` — mutates batch
- `get_ferment_output_id(recipe_key, quality)` — returns tiered item id string
- `FermentationGenerator` — stateful (world_seed + counter), `generate(ingredients, salt_level, vessel_type)` method
- `FERMENT_TYPE_ORDER` — `[f"{recipe}_{tier}" for recipe in RECIPE_ORDER for tier in ["base","fine","superior"]]`
- `RECIPE_DISPLAY_NAMES` — user-friendly names

---

## Mini-game

### Phases
1. **`select_ingredients`** — 8-slot ingredient picker from player inventory. Salt slider (0–100% of ideal). Real-time recipe detection label ("This looks like: Kimchi"). Confirm → phase 2.
2. **`select_vessel`** — 3 vessel buttons with descriptions. Confirm → phase 3.
3. **`tending`** — Active mini-game (45 seconds real-time):
   - **Activity bar** (horizontal, center): oscillates via physics (velocity + random target drift). Shows an orange "burp window" when activity peaks above threshold.
   - **SPACE = burp the lid**: gives +quality if in the window, nothing outside. Timed windows appear every ~8–12s.
   - **Ferment progress bar** (bottom): fills left-to-right. Color zones: gray (under) → green (active/peak) → red (over). Sourness/crunch tradeoff tooltip shows current projection.
   - **"OPEN NOW" button**: harvest at any time — earlier = crunchier/milder, later = sourer/softer. Over-fermented (past 0.8) = penalty.
   - **Temperature creep** (small bar, top-right): slowly rises. Click "Keep Cool" button to reset (allowed twice). Excess heat = sourness penalty.
4. **`result`** — Displays: recipe name, quality stars (1–5), flavor notes, buff granted. Grants output item to player inventory. Updates `discovered_ferments`.

Quality formula:
```
quality = salt_band_frac × 0.30
        + burp_hits / expected_burps × 0.30
        + time_in_optimal × 0.25
        - penalties × 0.12
        + vessel_bonus
```
Clamped to [0, 1].

---

## Files to Touch

| File | Change |
|---|---|
| `fermentation.py` (NEW) | Dataclass, recipes, generator, flavor pools, result functions |
| `blocks.py` | 3 block IDs + BLOCKS entries + set registrations |
| `world.py` | Add cucumber to `_CROP_MATURE_MAP` |
| `items.py` | cucumber_seed, cucumber, table_salt, crock placer, 30 outputs |
| `player.py` | `fermented_batches`, `discovered_ferments`, `_ferment_gen`, cucumber harvest hook, apply_save |
| `save_manager.py` | `fermented_batches` table + save method + load query |
| `crafting.py` | Research lock for `ferment_crock_item` |
| `Render/blocks_crafting.py` | Draw crock (clay pot silhouette) + cucumber crops (vine) |
| `UI/fermentation.py` (NEW) | `FermentationMixin` — all draw + click + key handlers |
| `UI/__init__.py` | Mixin import + state variables |
| `UI/collections.py` | Filter button, codex tab, `_draw_fermentation_codex` (recipe × tier grid) |
| `UI/handlers.py` | Dispatch `FERMENT_CROCK_BLOCK` to mixin |
| `main.py` | Keydown + per-frame key routing |

---

## Codex Design

Grid: **rows = 10 recipes**, **cols = 3 quality tiers** (Base / Fine / Superior) = 30 discoverable entries.

- Discovered cell: recipe name + quality stars
- Undiscovered cell: "???"
- Detail panel: required/optional ingredients, flavor notes, buff description
- Discovery key format: `"kimchi_superior"`, `"sauerkraut_fine"`, etc.

---

## Verification Checklist

- [ ] Harvest cucumber from mature crop → cucumber + seed added to inventory
- [ ] Open fermentation crock → ingredient picker shows vegetables from inventory
- [ ] Pack kimchi ingredients (cabbage + garlic + pepper) → recipe label reads "Kimchi"
- [ ] Pack sauerkraut (cabbage only) → recipe label reads "Sauerkraut"
- [ ] Pack unknown combo → label reads "Plain Ferment"
- [ ] Tending phase: activity bar oscillates; SPACE in burp window gives "+Burp!" flash
- [ ] "OPEN NOW" early → crunchier result, milder sourness; late → sourer, softer
- [ ] Over-ferment (past red zone) → quality penalty applied
- [ ] Output item granted in correct tier (base / fine / superior) based on quality
- [ ] `discovered_ferments` set updates after first batch of each type + tier
- [ ] Save and reload → `fermented_batches` + `discovered_ferments` survive
- [ ] Encyclopedia tab shows fermentation codex with correct discovered/total count
- [ ] Codex grid: discovered cells show recipe name + stars; undiscovered = "???"
- [ ] Collection filter "FERMENTS" shows only fermented output items
- [ ] Buffs apply when eating output item
