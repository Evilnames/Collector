from blocks import FACTORY_BLOCK

_DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

MAX_INPUT_SLOTS   = 4
MAX_OUTPUT_SLOTS  = 2
DEFAULT_CRAFT_TIME = 5.0
DEFAULT_INV_CAP   = 64
FLASH_DURATION    = 0.45   # seconds the completion flash lasts


def register_factory(world, bx, by):
    world.factory_data[(bx, by)] = {
        "recipe": {
            "inputs":     [None] * MAX_INPUT_SLOTS,
            "outputs":    [None] * MAX_OUTPUT_SLOTS,
            "craft_time": DEFAULT_CRAFT_TIME,
        },
        "inventory": {},
        "progress":  0.0,
        "inv_cap":   DEFAULT_INV_CAP,
    }


def factory_tick(world, dt):
    # Decrement completion flash timers
    flash = world.factory_flash
    for k in list(flash):
        flash[k] -= dt
        if flash[k] <= 0:
            del flash[k]

    for (bx, by), state in list(world.factory_data.items()):
        if world.get_block(bx, by) != FACTORY_BLOCK:
            continue
        if _wire_disabled(world, bx, by):
            state["progress"] = 0.0
            continue

        recipe     = state.get("recipe", {})
        inputs     = [s for s in recipe.get("inputs",  []) if s]
        outputs    = [s for s in recipe.get("outputs", []) if s]
        if not inputs or not outputs:
            state["progress"] = 0.0
            continue

        inv        = state.setdefault("inventory", {})
        craft_time = max(0.5, recipe.get("craft_time", DEFAULT_CRAFT_TIME))
        inv_cap    = state.get("inv_cap", DEFAULT_INV_CAP)

        # Stop if inventory is at cap — wait for outputs to be drained
        if sum(inv.values()) >= inv_cap:
            state["progress"] = 0.0
            continue

        # All inputs must be present
        if all(inv.get(s["item_id"], 0) >= s["count"] for s in inputs):
            state["progress"] = state.get("progress", 0.0) + dt
            if state["progress"] >= craft_time:
                for s in inputs:
                    inv[s["item_id"]] -= s["count"]
                    if inv[s["item_id"]] <= 0:
                        del inv[s["item_id"]]
                for s in outputs:
                    inv[s["item_id"]] = inv.get(s["item_id"], 0) + s["count"]
                state["progress"] = 0.0
                flash[(bx, by)] = FLASH_DURATION   # trigger completion flash
        else:
            state["progress"] = 0.0


def _wire_disabled(world, bx, by):
    has_wire = any(world.get_wire(bx + dx, by + dy) == 1 for dx, dy in _DIRS)
    if not has_wire:
        return False
    return not any((bx + dx, by + dy) in world.powered_wires for dx, dy in _DIRS)
