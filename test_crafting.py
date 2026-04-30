"""
Crafting validation script.

Runs in two phases:
  1. Lint  — py_compile every .py file in the project tree.
  2. Craft — simulate each recipe across all stations and assert the correct
             item and count end up in a mock inventory.

No pygame required; crafting.py and items.py are pure-data modules.
"""

import sys
import os
import py_compile
import glob
import traceback

# ---------------------------------------------------------------------------
# Phase 1 — lint
# ---------------------------------------------------------------------------

def lint_project(root: str) -> list[str]:
    errors = []
    pattern = os.path.join(root, "**", "*.py")
    files = glob.glob(pattern, recursive=True)
    for path in sorted(files):
        try:
            py_compile.compile(path, doraise=True)
        except py_compile.PyCompileError as e:
            errors.append(f"  SYNTAX {path}: {e}")
    return errors


# ---------------------------------------------------------------------------
# Minimal mock player — mirrors the real _add_item / inventory contract
# ---------------------------------------------------------------------------

HOTBAR_SIZE = 10  # must match constants.py

class MockPlayer:
    def __init__(self, inventory: dict):
        self.inventory = dict(inventory)
        self.hotbar = [None] * HOTBAR_SIZE
        self.hotbar_uses = [None] * HOTBAR_SIZE
        self.discovered_foods: set = set()
        self.foods_cooked: dict = {}
        self.pending_notifications: list = []

    def _add_item(self, item_id: str, count: int = 1):
        self.inventory[item_id] = self.inventory.get(item_id, 0) + count
        if item_id not in self.hotbar:
            for i in range(HOTBAR_SIZE):
                if self.hotbar[i] is None:
                    self.hotbar[i] = item_id
                    break


def _craft(player: MockPlayer, recipe: dict) -> bool:
    """Simulate one craft: deduct ingredients, add output. Returns False if
    the player lacks ingredients (recipe skipped, not a failure)."""
    for item_id, needed in recipe["ingredients"].items():
        if player.inventory.get(item_id, 0) < needed:
            return False
    for item_id, needed in recipe["ingredients"].items():
        player.inventory[item_id] -= needed
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
    for _ in range(recipe["output_count"]):
        player._add_item(recipe["output_id"])
    return True


# ---------------------------------------------------------------------------
# Phase 2 — crafting tests
# ---------------------------------------------------------------------------

def _all_recipe_lists():
    """Import every recipe list from crafting.py."""
    from crafting import (
        BAKERY_RECIPES, WOK_RECIPES, STEAMER_RECIPES, NOODLE_POT_RECIPES,
        BBQ_GRILL_RECIPES, CLAY_POT_RECIPES, FORGE_RECIPES, ARTISAN_RECIPES,
        BAIT_STATION_RECIPES, FLETCHING_RECIPES, SMELTER_RECIPES,
        GLASS_KILN_RECIPES, GARDEN_WORKSHOP_RECIPES, JUICER_RECIPES,
        AUTOMATION_RECIPES, TANNING_RACK_RECIPES,
    )
    return {
        "BAKERY":           BAKERY_RECIPES,
        "WOK":              WOK_RECIPES,
        "STEAMER":          STEAMER_RECIPES,
        "NOODLE_POT":       NOODLE_POT_RECIPES,
        "BBQ_GRILL":        BBQ_GRILL_RECIPES,
        "CLAY_POT":         CLAY_POT_RECIPES,
        "FORGE":            FORGE_RECIPES,
        "ARTISAN":          ARTISAN_RECIPES,
        "BAIT_STATION":     BAIT_STATION_RECIPES,
        "FLETCHING":        FLETCHING_RECIPES,
        "SMELTER":          SMELTER_RECIPES,
        "GLASS_KILN":       GLASS_KILN_RECIPES,
        "GARDEN_WORKSHOP":  GARDEN_WORKSHOP_RECIPES,
        "JUICER":           JUICER_RECIPES,
        "AUTOMATION":       AUTOMATION_RECIPES,
        "TANNING_RACK":     TANNING_RACK_RECIPES,
    }


def _validate_recipe_structure(station: str, idx: int, recipe: dict) -> list[str]:
    """Return a list of structural errors for a single recipe dict."""
    errs = []
    loc = f"{station}[{idx}] {recipe.get('name', '?')!r}"
    for key in ("name", "ingredients", "output_id", "output_count"):
        if key not in recipe:
            errs.append(f"  MISSING_KEY  {loc}: missing '{key}'")
    if "ingredients" in recipe and not isinstance(recipe["ingredients"], dict):
        errs.append(f"  BAD_INGREDS  {loc}: 'ingredients' must be a dict")
    if "output_count" in recipe:
        if not isinstance(recipe["output_count"], int) or recipe["output_count"] < 1:
            errs.append(f"  BAD_COUNT    {loc}: 'output_count' must be int >= 1")
    return errs


def _run_craft_test(station: str, idx: int, recipe: dict) -> list[str]:
    """Craft the recipe with exactly enough ingredients and assert the result."""
    errs = []
    loc = f"{station}[{idx}] {recipe.get('name', '?')!r}"
    start_inv = dict(recipe["ingredients"])  # exactly enough to craft once
    player = MockPlayer(start_inv)
    try:
        crafted = _craft(player, recipe)
    except Exception:
        errs.append(f"  EXCEPTION    {loc}:\n{traceback.format_exc()}")
        return errs

    if not crafted:
        errs.append(f"  NOT_CRAFTED  {loc}: craft returned False despite sufficient inventory")
        return errs

    output_id = recipe["output_id"]
    expected  = recipe["output_count"]
    actual    = player.inventory.get(output_id, 0)

    if actual != expected:
        errs.append(
            f"  WRONG_COUNT  {loc}: expected {expected}x '{output_id}', "
            f"got {actual}"
        )

    for item_id in recipe["ingredients"]:
        remaining = player.inventory.get(item_id, 0)
        if remaining != 0:
            errs.append(
                f"  INGRED_LEAK  {loc}: ingredient '{item_id}' not fully consumed "
                f"(remaining: {remaining})"
            )
    return errs


def test_crafting() -> list[str]:
    errors = []
    try:
        station_map = _all_recipe_lists()
    except Exception:
        errors.append(f"  IMPORT_ERROR crafting.py:\n{traceback.format_exc()}")
        return errors

    total = 0
    for station, recipes in station_map.items():
        for idx, recipe in enumerate(recipes):
            errors.extend(_validate_recipe_structure(station, idx, recipe))
            if not errors:  # only run craft sim if structure is valid
                errors.extend(_run_craft_test(station, idx, recipe))
            total += 1

    if not errors:
        print(f"  Tested {total} recipes across {len(station_map)} stations — all passed.")
    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)  # ensure crafting.py imports work via relative path
    sys.path.insert(0, root)

    all_errors = []

    print("=" * 60)
    print("Phase 1: Lint")
    print("=" * 60)
    lint_errors = lint_project(root)
    if lint_errors:
        print(f"FAIL — {len(lint_errors)} syntax error(s):")
        for e in lint_errors:
            print(e)
        all_errors.extend(lint_errors)
    else:
        print("All .py files compile cleanly.")

    print()
    print("=" * 60)
    print("Phase 2: Crafting")
    print("=" * 60)
    craft_errors = test_crafting()
    if craft_errors:
        print(f"FAIL — {len(craft_errors)} error(s):")
        for e in craft_errors:
            print(e)
        all_errors.extend(craft_errors)

    print()
    if all_errors:
        print(f"OVERALL: FAILED ({len(all_errors)} error(s))")
        sys.exit(1)
    else:
        print("OVERALL: PASSED")


if __name__ == "__main__":
    main()
