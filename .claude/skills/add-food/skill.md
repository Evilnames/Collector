---
name: add-food
description: Step-by-step guide for adding a new food item to CollectorBlocks. Covers the ITEMS entry in items.py, crafting station recipes in crafting.py, and optional crop drop in blocks.py.
---

# Add a New Food Item

Food items are defined in the `ITEMS` dict in [items.py](../../../items.py). Any item with `"edible": True` is food — the player can eat it by pressing space while it is selected in the hotbar. Cooked/prepared foods are produced via station recipes in [crafting.py](../../../crafting.py).

## Step 1 — Add an entry to ITEMS

Add a new key to `ITEMS` in [items.py](../../../items.py). Place it near other food of the same type (raw crops near raw crops, baked goods near baked goods, etc.).

**Minimal food item** (raw ingredient or simple prepared dish):

```python
"apple_tart": {
    "name": "Apple Tart",
    "color": (220, 160, 60),
    "edible": True,
    "hunger_restore": 30,
},
```

**Food with a buff** (coffee, wine, or spirit buffs follow the same pattern):

```python
"spiced_cider": {
    "name": "Spiced Cider",
    "color": (180, 80, 20),
    "edible": True,
    "hunger_restore": 15,
    "wine_buff": "warmth",
    "wine_buff_duration": 90.0,
},
```

`hunger_restore` is added directly to the player's hunger stat (0–100). Health also gains `hunger_restore * 0.25` on each eat. A `place_block` key is not needed for food (it defaults to absent/None).

### Hunger value reference

| Category | Range | Examples |
|----------|-------|---------|
| Raw fruit / veg | 3–15 | strawberry 3, apple 8, corn 10 |
| Cooked meat | 40–78 | cooked_chicken 55, cooked_beef 72 |
| Simple baked goods | 20–35 | bread 25, corn_bread 28 |
| Hearty dishes | 35–60 | beef_stew 55, ramen 45 |
| Beverages | 5–15 | coffees/wines/spirits 8–12 |

### Available buffs

| Key | Type | Notes |
|-----|------|-------|
| `"coffee_buff"` | `"focus"`, `"rush"`, `"clarity"`, `"strength"`, `"endurance"` | Use `"coffee_buff_duration"` (default 60 s) |
| `"wine_buff"` | `"warmth"`, `"serenity"`, `"charm"`, `"vivacity"`, `"contemplation"` | Use `"wine_buff_duration"` (default 120 s) |
| `"spirit_buff"` | `"grit"`, `"warmth"`, etc. | Use `"spirit_buff_duration"` (default 120 s) |

Notable effects: `"endurance"` reduces hunger drain 40%; `"serenity"` reduces it 60%; `"rush"` increases movement speed; `"strength"` adds +1 pick power; `"vivacity"` prevents fall damage.

## Step 2 — Add a crafting recipe (if cooked/prepared)

If the food is made at a cooking station, add a recipe dict to the appropriate list in [crafting.py](../../../crafting.py). Pick the station that fits thematically:

| Station | List | Best for |
|---------|------|----------|
| Bakery | `BAKERY_RECIPES` | Breads, pies, cakes, dumplings, rice dishes |
| Wok | `WOK_RECIPES` | Stir-fries, fried dishes, quick sautés |
| Steamer | `STEAMER_RECIPES` | Steamed buns, dumplings, custards |
| Noodle Pot | `NOODLE_POT_RECIPES` | Noodles, soups, broths |
| BBQ Grill | `BBQ_GRILL_RECIPES` | Grilled veg, meat, skewers |
| Clay Pot | `CLAY_POT_RECIPES` | Stews, braised dishes, slow-cooked soups |

Recipe format (all stations use the same structure):

```python
{"name": "Apple Tart", "ingredients": {"apple": 2, "wheat": 1}, "output_id": "apple_tart", "output_count": 1},
```

`ingredients` maps item IDs to required counts. `output_count` is how many the recipe produces.

## Step 3 — Add a crop drop (if harvested from a block)

Skip this step if the food only comes from a recipe.

If the food drops from a crop or plant block, find or create the block entry in [blocks.py](../../../blocks.py) and set its `"drop"` field to your item ID:

```python
APPLE_TREE_FRUIT: {
    ...
    "drop": "apple",
    "drop_count": (1, 3),   # (min, max) random range
    ...
},
```

## Verification checklist

- [ ] Item key is unique in `ITEMS`
- [ ] `"edible": True` and `"hunger_restore"` are set
- [ ] Buff keys and durations are valid (see table above)
- [ ] Recipe is added to the correct station list (if cooked)
- [ ] `output_id` in the recipe matches the `ITEMS` key exactly
- [ ] Block drop set in [blocks.py](../../../blocks.py) (if harvested)
- [ ] Run the game, obtain the food, eat it — hunger bar should increase
