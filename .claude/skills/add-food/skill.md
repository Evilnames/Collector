---
name: add-food
description: Step-by-step guide for adding a new food item to CollectorBlocks. Covers the ITEMS entry in items.py, nutrition fields, crafting station recipes in crafting.py, running the nutrition script, and optional crop drop in blocks.py.
---

# Add a New Food Item

Food items are defined in the `ITEMS` dict in [items.py](../../../items.py). Any item with `"edible": True` is food — the player can eat it by pressing space while it is selected in the hotbar. Cooked/prepared foods are produced via station recipes in [crafting.py](../../../crafting.py).

Hunger and health recovery are driven by a nutrition system. Base ingredients carry `calories`, `protein`, `fiber`, `vitamins`, and `sugar` fields. After adding any new food or ingredient, run the update script (Step 4) to recompute all derived values automatically.

## Step 1 — Add an entry to ITEMS

Add a new key to `ITEMS` in [items.py](../../../items.py). Place it near other food of the same type (raw crops near raw crops, baked goods near baked goods, etc.).

### Cooked/prepared dish (output of a recipe)

Just declare the item with a placeholder `hunger_restore` — the script will overwrite it:

```python
"apple_tart": {
    "name": "Apple Tart",
    "color": (220, 160, 60),
    "edible": True,
    "hunger_restore": 0,
},
```

### Raw ingredient (eaten directly or used in recipes)

Raw ingredients also need the five nutrition source fields. The script uses these to compute `hunger_restore` and the four factor fields for every dish that contains this ingredient:

```python
"quince": {
    "name": "Quince",
    "color": (220, 195, 60),
    "edible": True,
    "hunger_restore": 10,   # what eating it raw gives (can differ from calories)
    "calories":  10,        # caloric contribution when used as a recipe ingredient
    "protein":  0.08,       # 0.0–0.5  (meat ~0.45, legumes ~0.28, fruit ~0.08)
    "fiber":    0.40,       # 0.0–1.0  (legumes ~0.8, leafy veg ~0.6, fruit ~0.4)
    "vitamins": 0.45,       # 0.0–1.0  (citrus ~0.9, leafy greens ~0.8, fruit ~0.45)
    "sugar":    0.50,       # 0.0–1.0  (dates ~0.9, agave ~0.85, fruit ~0.5)
},
```

`hunger_restore` on a raw ingredient is what the player gets from eating it directly (eating raw meat is penalised vs its `calories` value). `calories` is its contribution inside a recipe.

### Nutrition field reference

| Category | calories | protein | fiber | vitamins | sugar |
|----------|----------|---------|-------|----------|-------|
| Grains (wheat, rice) | 10–12 | 0.10–0.15 | 0.25–0.55 | 0.08–0.10 | 0.08–0.10 |
| Meat (raw) | 16–30 | 0.42–0.52 | 0.00 | 0.10 | 0.00 |
| Egg / Milk | 8–12 | 0.20–0.35 | 0.00 | 0.18–0.20 | 0.02–0.15 |
| Legumes (lentil, chickpea) | 7–10 | 0.22–0.30 | 0.70–0.85 | 0.18–0.35 | 0.05–0.08 |
| Root veg (potato, carrot) | 5–12 | 0.10 | 0.40–0.50 | 0.25–0.60 | 0.08–0.12 |
| Leafy veg (broccoli, cabbage) | 4–7 | 0.10–0.20 | 0.45–0.85 | 0.55–0.80 | 0.05–0.08 |
| Fruit (apple, pear) | 7–14 | 0.08–0.10 | 0.35–0.45 | 0.30–0.75 | 0.50–0.65 |
| Sweet fruit / syrup | 6–20 | 0.00–0.10 | 0.05–0.40 | 0.05–0.20 | 0.70–0.95 |
| Aromatics (garlic, chili) | 2–8 | 0.05–0.12 | 0.15–0.25 | 0.30–0.70 | 0.02–0.10 |

### What the four factors do in-game

After the script runs, every edible item gains four computed fields that drive gameplay effects:

| Field | Computed from | Effect when eaten |
|-------|---------------|-------------------|
| `protein_factor` | calorie-weighted avg protein | HP recovery = `hunger_restore × protein_factor` (default 0.25 if absent) |
| `fiber_factor` | count-weighted avg fiber | `> 0.25` → `well_fed` buff: hunger drains 30% slower for up to 240 s |
| `vitamin_factor` | count-weighted avg vitamins | `> 0.25` → `nourished` buff: +0.5 HP/s passive regen for up to 180 s |
| `sugar_factor` | count-weighted avg sugar | `> 0.40` → instant +bonus hunger now, then a 60 s sugar crash 3 min later |

### Food with a buff

Buffs stack on top of the nutrition system:

```python
"spiced_cider": {
    "name": "Spiced Cider",
    "color": (180, 80, 20),
    "edible": True,
    "hunger_restore": 0,    # script will set this
    "wine_buff": "warmth",
    "wine_buff_duration": 90.0,
},
```

| Key | Types | Notes |
|-----|-------|-------|
| `"coffee_buff"` | `"focus"`, `"rush"`, `"clarity"`, `"strength"`, `"endurance"` | `"coffee_buff_duration"` (default 60 s) |
| `"wine_buff"` | `"warmth"`, `"serenity"`, `"charm"`, `"vivacity"`, `"contemplation"` | `"wine_buff_duration"` (default 120 s) |
| `"spirit_buff"` | `"grit"`, `"warmth"`, etc. | `"spirit_buff_duration"` (default 120 s) |

Notable effects: `"endurance"` reduces hunger drain 40%; `"serenity"` reduces it 60%; `"rush"` increases movement speed; `"strength"` adds +1 pick power; `"vivacity"` prevents fall damage.

## Step 2 — Add a crafting recipe (if cooked/prepared)

If the food is made at a cooking station, add a recipe dict to the appropriate list in [crafting.py](../../../crafting.py).

| Station | List | `cooking_mult` | Best for |
|---------|------|---------------|----------|
| Bakery | `BAKERY_RECIPES` | 1.10 | Breads, pies, cakes, dumplings, rice dishes |
| Wok | `WOK_RECIPES` | 1.20 | Stir-fries, fried dishes, quick sautés |
| Steamer | `STEAMER_RECIPES` | 1.18 | Steamed buns, dumplings, custards |
| Noodle Pot | `NOODLE_POT_RECIPES` | 1.22 | Noodles, soups, broths |
| BBQ Grill | `BBQ_GRILL_RECIPES` | 1.15 | Grilled veg, meat, skewers |
| Clay Pot | `CLAY_POT_RECIPES` | 1.30 | Stews, braised dishes, slow-cooked soups |

Recipe format:

```python
{"name": "Apple Tart", "ingredients": {"apple": 2, "wheat": 1}, "output_id": "apple_tart", "output_count": 1},
```

`hunger_restore` for the output is computed by: `sum(calories[ing] × qty) × cooking_mult / output_count`.

## Step 3 — Add a crop drop (if harvested from a block)

Skip this step if the food only comes from a recipe.

```python
APPLE_TREE_FRUIT: {
    ...
    "drop": "apple",
    "drop_count": (1, 3),
    ...
},
```

## Step 4 — Run the nutrition script

After adding the ingredient or recipe, run:

```
python tools/update_food_nutrition.py
```

This resolves the full recipe graph and writes `hunger_restore`, `protein_factor`, `fiber_factor`, `vitamin_factor`, and `sugar_factor` back into [items.py](../../../items.py) for every affected food item. Check the printed diff table to confirm the new item's values look sensible. Any ingredient with missing `calories` data is printed as a warning.

## Verification checklist

- [ ] Item key is unique in `ITEMS`
- [ ] `"edible": True` is set
- [ ] If raw ingredient: `calories`, `protein`, `fiber`, `vitamins`, `sugar` are set
- [ ] Buff keys and durations are valid (see table above)
- [ ] Recipe added to the correct station list (if cooked)
- [ ] `output_id` in the recipe matches the `ITEMS` key exactly
- [ ] Block drop set in [blocks.py](../../../blocks.py) (if harvested)
- [ ] `python tools/update_food_nutrition.py` run — new item appears in diff with sensible values
- [ ] Run the game, obtain the food, eat it — hunger bar increases, correct buff triggers if any
