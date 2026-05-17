"""
sommelier.py — Sommelier request board for wine-themed outposts.

Each wine outpost periodically posts 1–3 requests for a specific wine style,
optionally with a vintage-age or weather preference, plus a food pairing.
Player fulfils by surrendering an aged Grape (preferred — carries vintage info)
or a bottled wine item from inventory, alongside the pairing food.
"""

import random
import hashlib

from wine import WINE_STYLE_DESCS, WEATHER_TYPES, DAYS_PER_YEAR

# Outpost types that host a sommelier board
WINE_OUTPOST_TYPES = {"wine_estate", "hillside_vineyard", "olive_press"}

# How many active requests each outpost holds; refreshed every N days
REQUESTS_PER_OUTPOST = 3
REQUEST_LIFESPAN_DAYS = 6

# Bottled item tiers per style (matches items.py)
_BOTTLED_BY_STYLE = {
    "red":       ["red_wine",       "red_wine_fine",       "red_wine_reserve"],
    "white":     ["white_wine",     "white_wine_fine",     "white_wine_reserve"],
    "rose":      ["rose_wine",      "rose_wine_fine",      "rose_wine_reserve"],
    "sparkling": ["sparkling_wine", "sparkling_wine_fine", "sparkling_wine_reserve"],
    "dessert":   ["dessert_wine",   "dessert_wine_fine",   "dessert_wine_reserve"],
}

SOMMELIER_ARCHETYPES = {
    "critic":       {"label": "Critic",       "styles": ["red", "white"],
                     "wants_pairing": True,  "reward_bias": 1.0},
    "collector":    {"label": "Collector",    "styles": ["red", "dessert"],
                     "wants_pairing": False, "reward_bias": 1.2},
    "aristocrat":   {"label": "Aristocrat",   "styles": ["red", "sparkling"],
                     "wants_pairing": True,  "reward_bias": 1.3},
    "restaurateur": {"label": "Restaurateur", "styles": ["red", "white", "rose"],
                     "wants_pairing": True,  "reward_bias": 0.95},
    "courtier":     {"label": "Courtier",     "styles": ["sparkling", "rose"],
                     "wants_pairing": True,  "reward_bias": 1.1},
    "vintner":      {"label": "Visiting Vintner", "styles": ["white", "rose", "red"],
                     "wants_pairing": False, "reward_bias": 0.9},
}

_SOMMELIER_NAMES = [
    "Auberon", "Briselle", "Calixto", "Damaris", "Evrard", "Fenice", "Galiana",
    "Hesper", "Isolde", "Jovan", "Kestrel", "Loredan", "Marisette", "Norel",
    "Oriane", "Perrin", "Quentin", "Rosalind", "Severin", "Talia", "Ursin",
    "Verity", "Wendell", "Xavier", "Yolande", "Zephyrine",
]

# Pairings: which foods complement which style. Reward bonus when supplied.
PAIRINGS = {
    "red":       ["cheese", "cooked_beef", "cooked_mutton", "cheese_bread",
                  "fig_lamb_tagine", "grilled_mushroom"],
    "white":     ["cooked_chicken", "cooked_egg", "cheese", "grilled_corn",
                  "grilled_pear_cheese", "bread"],
    "rose":      ["grilled_watermelon", "cheese", "fig_roll", "fig",
                  "cooked_chicken", "grilled_corn"],
    "sparkling": ["cheese", "fig_brioche", "fig_tart", "cooked_egg",
                  "grilled_pear_cheese"],
    "dessert":   ["fig", "fig_jam", "fig_cake", "fig_date_pudding",
                  "fig_tart", "cheese"],
}

_FLAVOR_LINES = [
    "“Bring me a {style} with character — I'll judge the rest.”",
    "“The estate's table calls for a proper {style}.”",
    "“A {style} for an old friend's birthday.”",
    "“I'm hosting a tasting. Need a {style} that won't embarrass me.”",
    "“My cellar is short a {style}. Premium paid.”",
    "“The patrons demand a {style}. Don't disappoint.”",
]


# ---------------------------------------------------------------------------
# Request storage — keyed by outpost_id
# ---------------------------------------------------------------------------

SOMMELIER_REQUESTS: dict[int, list[dict]] = {}


def _quality_tier(item_id: str) -> str:
    if item_id.endswith("_reserve"):
        return "reserve"
    if item_id.endswith("_fine"):
        return "fine"
    return "base"


def _request_rng(world_seed: int, outpost_id: int, day: int) -> random.Random:
    return random.Random((world_seed * 7919 + outpost_id * 1009 + day * 31) & 0xFFFFFFFF)


def _make_request(world_seed: int, outpost_id: int, day: int, slot: int) -> dict:
    rng = _request_rng(world_seed, outpost_id, day + slot * 17)
    archetype = rng.choice(list(SOMMELIER_ARCHETYPES.keys()))
    cfg       = SOMMELIER_ARCHETYPES[archetype]
    style     = rng.choice(cfg["styles"])
    name      = rng.choice(_SOMMELIER_NAMES)

    # Tier scales reward: any / fine / reserve
    tier_roll = rng.random()
    if tier_roll < 0.55:
        min_tier = "base";    tier_mult = 1.0
    elif tier_roll < 0.85:
        min_tier = "fine";    tier_mult = 1.8
    else:
        min_tier = "reserve"; tier_mult = 3.0

    # Vintage age preference (in years) — 30% have a minimum
    vintage_year_min = 0
    if rng.random() < 0.30:
        vintage_year_min = rng.randint(1, 3)

    # Weather preference — 25% have one
    weather_pref = ""
    if rng.random() < 0.25:
        weather_pref = rng.choice([k for k in WEATHER_TYPES.keys() if k != "balanced"])

    # Food pairing
    pairing_item = ""
    if cfg["wants_pairing"]:
        pairing_item = rng.choice(PAIRINGS.get(style, ["bread"]))

    base_reward = int(round(40 * tier_mult * cfg["reward_bias"]))
    vintage_bonus = vintage_year_min * 25 if vintage_year_min else 0
    weather_bonus = 30 if weather_pref else 0
    pairing_bonus = 20 if pairing_item else 0

    flavor = rng.choice(_FLAVOR_LINES).format(style=WINE_STYLE_DESCS.get(style, style).split(" — ")[0])

    rid = int(hashlib.md5(
        f"som_{world_seed}_{outpost_id}_{day}_{slot}".encode()
    ).hexdigest()[:8], 16)

    return {
        "request_id":      rid,
        "outpost_id":      outpost_id,
        "sommelier_name":  name,
        "archetype":       archetype,
        "wine_style":      style,
        "min_tier":        min_tier,
        "vintage_year_min": vintage_year_min,
        "weather_pref":    weather_pref,
        "pairing_item":    pairing_item,
        "base_reward":     base_reward,
        "vintage_bonus":   vintage_bonus,
        "weather_bonus":   weather_bonus,
        "pairing_bonus":   pairing_bonus,
        "posted_day":      day,
        "expires_day":     day + REQUEST_LIFESPAN_DAYS,
        "flavor_text":     flavor,
    }


def refresh_outpost_requests(outpost_id: int, world_seed: int, day: int) -> None:
    """Refill an outpost's request list, removing expired and topping up to capacity."""
    cur = SOMMELIER_REQUESTS.setdefault(outpost_id, [])
    cur[:] = [r for r in cur if r["expires_day"] > day]
    slot = len(cur)
    while len(cur) < REQUESTS_PER_OUTPOST:
        cur.append(_make_request(world_seed, outpost_id, day, slot))
        slot += 1


def tick_sommelier_day(world_seed: int, world_day: int) -> None:
    """Called once per in-game day. Refreshes requests for every wine outpost."""
    from outposts import OUTPOSTS
    for op in OUTPOSTS.values():
        if op.outpost_type not in WINE_OUTPOST_TYPES:
            continue
        refresh_outpost_requests(op.outpost_id, world_seed, world_day)


def get_requests(outpost_id: int) -> list[dict]:
    return SOMMELIER_REQUESTS.get(outpost_id, [])


# ---------------------------------------------------------------------------
# Fulfillment
# ---------------------------------------------------------------------------

def _tier_rank(tier: str) -> int:
    return {"base": 0, "fine": 1, "reserve": 2}.get(tier, 0)


def _find_aged_grape(player, style: str, min_year: int) -> "Grape | None":
    """Best matching aged/blended grape for style (highest year, then quality)."""
    candidates = []
    for g in getattr(player, "wine_grapes", []):
        if g.state not in ("aged", "blended", "fermented"):
            continue
        if g.style != style:
            continue
        if getattr(g, "vintage_year", 0) < min_year:
            continue
        candidates.append(g)
    if not candidates:
        return None
    candidates.sort(key=lambda g: (getattr(g, "vintage_year", 0),
                                   getattr(g, "ferment_quality", 0.0)),
                    reverse=True)
    return candidates[0]


def _find_bottled(player, style: str, min_tier: str) -> str | None:
    """Inventory item id of cheapest bottle meeting style+min_tier, else None."""
    need_rank = _tier_rank(min_tier)
    inv = getattr(player, "inventory", {})
    for item_id in _BOTTLED_BY_STYLE.get(style, []):
        if _tier_rank(_quality_tier(item_id)) < need_rank:
            continue
        if inv.get(item_id, 0) > 0:
            return item_id
    return None


def find_request(request_id: int) -> dict | None:
    for reqs in SOMMELIER_REQUESTS.values():
        for r in reqs:
            if r["request_id"] == request_id:
                return r
    return None


def preview_fulfillment(player, request: dict) -> dict:
    """Show what the player would get without consuming anything.

    Returns a dict with: can_fulfill, source ("grape"|"bottle"|None), source_label,
    pairing_ready, total_reward, breakdown (list of (label, amount))."""
    style = request["wine_style"]
    min_year = request["vintage_year_min"]
    grape = _find_aged_grape(player, style, min_year)
    bottle = _find_bottled(player, style, request["min_tier"])

    breakdown = []
    total = 0
    source = None
    source_label = ""

    if grape is not None:
        source = "grape"
        from wine import WEATHER_TYPES
        wlabel = WEATHER_TYPES.get(getattr(grape, "weather", "balanced"), {}).get("label", "")
        source_label = f"Aged {style.title()} Y{getattr(grape, 'vintage_year', 0)} ({wlabel})"
        breakdown.append(("Base", request["base_reward"]))
        total += request["base_reward"]
        if request["vintage_year_min"] and getattr(grape, "vintage_year", 0) >= request["vintage_year_min"]:
            breakdown.append((f"Vintage Y{getattr(grape, 'vintage_year', 0)}", request["vintage_bonus"]))
            total += request["vintage_bonus"]
        if request["weather_pref"] and getattr(grape, "weather", "") == request["weather_pref"]:
            breakdown.append((f"{WEATHER_TYPES[request['weather_pref']]['label']} vintage", request["weather_bonus"]))
            total += request["weather_bonus"]
    elif bottle is not None:
        source = "bottle"
        source_label = bottle.replace("_", " ").title()
        # Bottled tier above minimum gives a small premium
        actual_rank = _tier_rank(_quality_tier(bottle))
        need_rank   = _tier_rank(request["min_tier"])
        tier_bonus  = max(0, actual_rank - need_rank) * 15
        breakdown.append(("Base", request["base_reward"]))
        total += request["base_reward"]
        if tier_bonus:
            breakdown.append(("Quality premium", tier_bonus))
            total += tier_bonus

    pairing_item = request["pairing_item"]
    pairing_ready = bool(pairing_item) and getattr(player, "inventory", {}).get(pairing_item, 0) > 0
    if pairing_item and pairing_ready:
        breakdown.append(("Pairing", request["pairing_bonus"]))
        total += request["pairing_bonus"]

    return {
        "can_fulfill":  source is not None,
        "source":       source,
        "source_label": source_label,
        "pairing_ready": pairing_ready,
        "total_reward": total,
        "breakdown":    breakdown,
    }


def fulfill_request(player, request_id: int) -> tuple[bool, int, str]:
    """Consume wine + (optional) pairing from player; pay reward; remove request.

    Returns (success, reward_paid, message)."""
    req = find_request(request_id)
    if req is None:
        return False, 0, "Request no longer posted."

    preview = preview_fulfillment(player, req)
    if not preview["can_fulfill"]:
        return False, 0, "You have no matching wine."

    # Consume wine source
    if preview["source"] == "grape":
        grape = _find_aged_grape(player, req["wine_style"], req["vintage_year_min"])
        if grape is None:
            return False, 0, "Wine no longer available."
        player.wine_grapes.remove(grape)
    elif preview["source"] == "bottle":
        bottle_id = _find_bottled(player, req["wine_style"], req["min_tier"])
        if bottle_id is None:
            return False, 0, "Wine no longer available."
        player.inventory[bottle_id] -= 1
        if player.inventory[bottle_id] <= 0:
            del player.inventory[bottle_id]

    # Consume pairing if supplied & in inventory
    pairing_item = req["pairing_item"]
    if pairing_item and preview["pairing_ready"]:
        player.inventory[pairing_item] -= 1
        if player.inventory[pairing_item] <= 0:
            del player.inventory[pairing_item]

    # Pay
    player.money += preview["total_reward"]

    # Remove from board
    lst = SOMMELIER_REQUESTS.get(req["outpost_id"], [])
    SOMMELIER_REQUESTS[req["outpost_id"]] = [r for r in lst if r["request_id"] != request_id]

    return True, preview["total_reward"], f"{req['sommelier_name']} pays {preview['total_reward']}g."
