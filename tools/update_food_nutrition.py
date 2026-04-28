#!/usr/bin/env python3
"""
Recompute hunger_restore for all crafted foods and add nutrition factor fields
to every edible item in items.py, based on the calorie/nutrition data stored
on base ingredients.

Run once from the project root:
    python tools/update_food_nutrition.py
"""
import sys
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from blocks import BLOCKS
from items import ITEMS
import crafting

# ---------------------------------------------------------------------------
# Station → block ID mapping for cooking_mult lookup
# ---------------------------------------------------------------------------
RECIPE_STATION_MAP = {
    "BAKERY_RECIPES":     35,
    "WOK_RECIPES":        82,
    "STEAMER_RECIPES":    83,
    "NOODLE_POT_RECIPES": 84,
    "BBQ_GRILL_RECIPES":  91,
    "CLAY_POT_RECIPES":   92,
}
DEFAULT_MULT = 1.10  # fallback for JUICER_RECIPES and any unlisted dicts

RECIPE_DICT_NAMES = [
    "BAKERY_RECIPES", "WOK_RECIPES", "STEAMER_RECIPES",
    "NOODLE_POT_RECIPES", "BBQ_GRILL_RECIPES", "CLAY_POT_RECIPES",
    "JUICER_RECIPES",
]

# Defaults for ingredients that have no nutrition data
DEFAULT_PROTEIN  = 0.12
DEFAULT_FIBER    = 0.10
DEFAULT_VITAMINS = 0.10
DEFAULT_SUGAR    = 0.05

# ---------------------------------------------------------------------------
# Step 1: Bootstrap nutrition maps from raw ingredient fields in ITEMS
# ---------------------------------------------------------------------------
cal_map      = {}
protein_map  = {}
fiber_map    = {}
vitamin_map  = {}
sugar_map    = {}

for item_id, data in ITEMS.items():
    if "calories" in data:
        cal_map[item_id]     = data["calories"]
        protein_map[item_id] = data.get("protein",  DEFAULT_PROTEIN)
        fiber_map[item_id]   = data.get("fiber",    DEFAULT_FIBER)
        vitamin_map[item_id] = data.get("vitamins", DEFAULT_VITAMINS)
        sugar_map[item_id]   = data.get("sugar",    DEFAULT_SUGAR)

# ---------------------------------------------------------------------------
# Step 2: Collect all recipes with their station multiplier
# ---------------------------------------------------------------------------
all_recipes = []  # (output_id, output_count, ingredients, mult, dict_name)

for dict_name in RECIPE_DICT_NAMES:
    recipes = getattr(crafting, dict_name, [])
    block_id = RECIPE_STATION_MAP.get(dict_name)
    if block_id is not None:
        mult = BLOCKS[block_id].get("cooking_mult", DEFAULT_MULT)
    else:
        mult = DEFAULT_MULT
    for recipe in recipes:
        output_id    = recipe.get("output_id")
        output_count = recipe.get("output_count", 1)
        ingredients  = recipe.get("ingredients", {})
        if output_id and ingredients:
            all_recipes.append((output_id, output_count, ingredients, mult, dict_name))

# ---------------------------------------------------------------------------
# Step 3: Iteratively resolve crafted items (max 10 passes for chains)
# ---------------------------------------------------------------------------
resolved_crafted = {}  # item_id → (hunger, protein_f, fiber_f, vitamin_f, sugar_f)
unresolved = list(all_recipes)

for _ in range(10):
    still_unresolved = []
    for (output_id, output_count, ingredients, mult, dict_name) in unresolved:
        if not all(ing in cal_map for ing in ingredients):
            still_unresolved.append((output_id, output_count, ingredients, mult, dict_name))
            continue

        total_cal = sum(cal_map[ing] * qty for ing, qty in ingredients.items())
        total_qty = sum(ingredients.values())
        if total_cal == 0:
            still_unresolved.append((output_id, output_count, ingredients, mult, dict_name))
            continue

        output_hunger = max(1, round(total_cal * mult / output_count))

        # Calorie-weighted: protein and sugar (dense-calorie sources dominate)
        protein = sum(cal_map[i] * q * protein_map.get(i, DEFAULT_PROTEIN)  for i, q in ingredients.items()) / total_cal
        sugar   = sum(cal_map[i] * q * sugar_map.get(i,   DEFAULT_SUGAR)    for i, q in ingredients.items()) / total_cal

        # Count-weighted: fiber and vitamins (preserves low-cal high-nutrient foods)
        fiber    = sum(q * fiber_map.get(i,    DEFAULT_FIBER)    for i, q in ingredients.items()) / total_qty
        vitamins = sum(q * vitamin_map.get(i,  DEFAULT_VITAMINS) for i, q in ingredients.items()) / total_qty

        resolved_crafted[output_id] = (output_hunger, round(protein, 2), round(fiber, 2),
                                       round(vitamins, 2), round(sugar, 2))

        # Feed computed values back for downstream recipes
        cal_map[output_id]     = output_hunger
        protein_map[output_id] = protein
        fiber_map[output_id]   = fiber
        vitamin_map[output_id] = vitamins
        sugar_map[output_id]   = sugar

    unresolved = still_unresolved
    if not unresolved:
        break

# Warn about anything still unresolved
if unresolved:
    print(f"\nWARNING: {len(unresolved)} recipes could not be resolved (missing base ingredient data):")
    for (output_id, _, ingredients, _, dict_name) in unresolved:
        missing = [i for i in ingredients if i not in cal_map]
        print(f"  {output_id} ({dict_name}): missing: {missing}")

# ---------------------------------------------------------------------------
# Step 4: Build raw-ingredient resolved set (add factor fields, keep hunger)
# ---------------------------------------------------------------------------
resolved_raw = {}  # item_id → (hunger, protein_f, fiber_f, vitamin_f, sugar_f)

for item_id, data in ITEMS.items():
    if data.get("edible") and "calories" in data and item_id not in resolved_crafted:
        resolved_raw[item_id] = (
            data.get("hunger_restore", data["calories"]),
            round(data.get("protein",  DEFAULT_PROTEIN),  2),
            round(data.get("fiber",    DEFAULT_FIBER),    2),
            round(data.get("vitamins", DEFAULT_VITAMINS), 2),
            round(data.get("sugar",    DEFAULT_SUGAR),    2),
        )

# ---------------------------------------------------------------------------
# Step 5: Write back to items.py
# ---------------------------------------------------------------------------
items_path = os.path.join(PROJECT_ROOT, "items.py")
with open(items_path, "r", encoding="utf-8") as f:
    lines = f.readlines()


def apply_factors_to_line(stripped, protein, fiber, vitamins, sugar):
    """Insert or update the four factor fields on a single item dict line."""
    factors = (f', "protein_factor": {protein:.2f}, "fiber_factor": {fiber:.2f}'
               f', "vitamin_factor": {vitamins:.2f}, "sugar_factor": {sugar:.2f}')
    if '"protein_factor"' in stripped:
        # Update in-place
        stripped = re.sub(r'"protein_factor":\s*[\d.]+', f'"protein_factor": {protein:.2f}', stripped)
        stripped = re.sub(r'"fiber_factor":\s*[\d.]+',   f'"fiber_factor": {fiber:.2f}',     stripped)
        stripped = re.sub(r'"vitamin_factor":\s*[\d.]+', f'"vitamin_factor": {vitamins:.2f}', stripped)
        stripped = re.sub(r'"sugar_factor":\s*[\d.]+',   f'"sugar_factor": {sugar:.2f}',      stripped)
    else:
        # Append before trailing }, or }
        if stripped.endswith('},'):
            stripped = stripped[:-2] + factors + '},'
        elif stripped.endswith('}'):
            stripped = stripped[:-1] + factors + '}'
    return stripped


changes = 0
new_lines = []

for line in lines:
    matched = False

    # Handle crafted foods: update hunger_restore + add factors
    for item_id, (new_hunger, protein, fiber, vitamins, sugar) in resolved_crafted.items():
        if f'"{item_id}"' in line and '"hunger_restore"' in line:
            stripped = line.rstrip()
            stripped = re.sub(r'"hunger_restore":\s*\d+', f'"hunger_restore": {new_hunger}', stripped)
            stripped = apply_factors_to_line(stripped, protein, fiber, vitamins, sugar)
            line = stripped + '\n'
            changes += 1
            matched = True
            break

    # Handle raw edible ingredients: only add factors (hunger_restore already correct)
    if not matched:
        for item_id, (_, protein, fiber, vitamins, sugar) in resolved_raw.items():
            if f'"{item_id}"' in line and '"hunger_restore"' in line:
                stripped = line.rstrip()
                stripped = apply_factors_to_line(stripped, protein, fiber, vitamins, sugar)
                line = stripped + '\n'
                changes += 1
                matched = True
                break

    new_lines.append(line)

# ---------------------------------------------------------------------------
# Step 6: Print diff summary
# ---------------------------------------------------------------------------
all_resolved = {**resolved_raw, **resolved_crafted}
print(f"\n{'Item':<32} {'Old':>5} {'New':>5} {'Prot':>5} {'Fib':>5} {'Vit':>5} {'Sug':>5}")
print("-" * 62)
for item_id, (new_hunger, protein, fiber, vitamins, sugar) in sorted(all_resolved.items()):
    old_hunger = ITEMS.get(item_id, {}).get("hunger_restore", "?")
    change_marker = " *" if str(old_hunger) != str(new_hunger) else ""
    print(f"{item_id:<32} {str(old_hunger):>5} {str(new_hunger):>5}"
          f" {protein:>5.2f} {fiber:>5.2f} {vitamins:>5.2f} {sugar:>5.2f}{change_marker}")

print(f"\nDone. {changes} item lines updated in items.py.")
if unresolved:
    print(f"WARNING: {len(unresolved)} recipes were not resolved.")

with open(items_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
