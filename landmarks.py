"""
landmarks.py — Capital landmarks: one structure per agenda, one effect per visit.

Each region's capital hosts a landmark whose form and effect match the leader's
agenda. The structure is a small platform (~5 wide) with characteristic decor
and a LANDMARK_FLAG_BLOCK that the player interacts with.

Per-region cooldown: Region.landmark_used_day stores the last in-game day a
landmark was triggered. Effects fire at most once per day per region.
"""

import random

from blocks import (
    LANDMARK_FLAG_BLOCK,
    POLISHED_MARBLE, LIMESTONE_BLOCK,
    TROPHY_PANEL_REN, FORGE_BLOCK,
    PRAYER_FLAG_BLOCK, OLIVE_BRANCH,
    MARBLE_PLINTH, MARBLE_STATUE,
    BRAZIER, TORCH,
    AIR,
    WEAPON_RACK_BLOCK, COMPASS_PAVING,
    STONE_LANTERN, PHILOSOPHERS_SCROLL,
    TALL_SUNDIAL, SHELL_FOUNTAIN,
    PAPER_LANTERN, TRIPOD_BRAZIER,
    GRAPEVINE_CROP_MATURE,
    SUNDIAL,
)
from landmark_buildings import place_landmark_building


# ---------------------------------------------------------------------------
# Per-agenda landmark definitions
# ---------------------------------------------------------------------------

LANDMARK_TYPES = {
    # --- Agenda-only fallbacks (one per agenda) ---
    "martial": {
        "name":         "Arena",
        "tagline":      "where champions are made and broken",
        "marker_block": TROPHY_PANEL_REN,
        "effect":       "arena",
    },
    "mercantile": {
        "name":         "Grand Bazaar",
        "tagline":      "every trade route ends here",
        "marker_block": MARBLE_PLINTH,
        "effect":       "bazaar",
    },
    "scholarly": {
        "name":         "Archive",
        "tagline":      "where every page is a doorway",
        "marker_block": MARBLE_STATUE,
        "effect":       "archive",
    },
    "pious": {
        "name":         "Great Shrine",
        "tagline":      "the prayer that the city keeps",
        "marker_block": PRAYER_FLAG_BLOCK,
        "effect":       "shrine",
    },
    "builder": {
        "name":         "Stoneworks",
        "tagline":      "the city's hands and its tools",
        "marker_block": FORGE_BLOCK,
        "effect":       "stoneworks",
    },
    "hedonist": {
        "name":         "Pleasure Garden",
        "tagline":      "no day worth living is without one",
        "marker_block": OLIVE_BRANCH,
        "effect":       "garden",
    },

    # --- Biome-flavored variants: (agenda, biome_group) composite keys ---
    ("martial", "steppe"): {
        "name":         "War Camp",
        "tagline":      "the steppe sharpens the warrior",
        "marker_block": WEAPON_RACK_BLOCK,
        "effect":       "war_camp",
    },
    ("martial", "desert"): {
        "name":         "Gladiator Pits",
        "tagline":      "the sands drink glory and blood alike",
        "marker_block": TROPHY_PANEL_REN,
        "effect":       "gladiator",
    },
    ("mercantile", "coastal"): {
        "name":         "Harbor Exchange",
        "tagline":      "where the sea brings every price",
        "marker_block": COMPASS_PAVING,
        "effect":       "harbor",
    },
    ("mercantile", "silk_road"): {
        "name":         "Caravanserai",
        "tagline":      "rest here, then carry the world forward",
        "marker_block": STONE_LANTERN,
        "effect":       "caravanserai",
    },
    ("scholarly", "east_asian"): {
        "name":         "Imperial Library",
        "tagline":      "ten thousand scrolls, one truth",
        "marker_block": PHILOSOPHERS_SCROLL,
        "effect":       "imperial_library",
    },
    ("scholarly", "mediterranean"): {
        "name":         "Observatory",
        "tagline":      "the stars were the first map",
        "marker_block": TALL_SUNDIAL,
        "effect":       "observatory",
    },
    ("pious", "coastal"): {
        "name":         "Sea Temple",
        "tagline":      "offerings cast upon the tide",
        "marker_block": SHELL_FOUNTAIN,
        "effect":       "sea_temple",
    },
    ("pious", "jungle"): {
        "name":         "Canopy Sanctum",
        "tagline":      "the forest itself is the god here",
        "marker_block": PAPER_LANTERN,
        "effect":       "canopy_sanctum",
    },
    ("builder", "alpine"): {
        "name":         "Stonecutters Guild",
        "tagline":      "the mountain gives; they shape",
        "marker_block": TRIPOD_BRAZIER,
        "effect":       "stonecutters",
    },
    ("hedonist", "mediterranean"): {
        "name":         "Vineyard Hall",
        "tagline":      "the vine makes time worth tasting",
        "marker_block": GRAPEVINE_CROP_MATURE,
        "effect":       "vineyard",
    },
}


def landmark_for(agenda: str, biome_group: str = "") -> dict:
    """Return the landmark spec, preferring the (agenda, biome_group) composite key."""
    if biome_group:
        spec = LANDMARK_TYPES.get((agenda, biome_group))
        if spec:
            return spec
    return LANDMARK_TYPES.get(agenda, LANDMARK_TYPES["mercantile"])


# ---------------------------------------------------------------------------
# Placement
# ---------------------------------------------------------------------------

def place_landmark(world, town, region) -> int:
    """Build the grand landmark structure to the LEFT of the town (opposite the palace).

    Returns the block-x of the landmark flag (the interaction point), or -1 if
    no region/agenda is set.
    """
    if region is None or not region.agenda:
        return -1

    spec     = landmark_for(region.agenda, getattr(region, "biome_group", ""))
    right_bx = town.center_bx - town.half_w - 4
    sy       = world.surface_y_at(right_bx)
    rng      = random.Random(town.center_bx ^ (world.seed * 0x517CC1B7))

    return place_landmark_building(
        world, spec, getattr(region, "biome_group", ""),
        right_bx, sy, rng, region,
    )


# ---------------------------------------------------------------------------
# Effects — invoked by LandmarkNPC when the player triggers the landmark
# ---------------------------------------------------------------------------

def _apply_arena(player, region):
    """Martial: open the arena spectator UI if games are scheduled today."""
    from gladiators import is_games_day, days_until_games, generate_arena_week
    world      = getattr(player, "world", None)
    day_count  = getattr(world, "day_count", 0)
    rseed      = getattr(region, "region_id", 0) * 1013 + hash(getattr(region, "name", ""))
    biome      = getattr(region, "biome_group", "temperate")

    if not is_games_day(rseed, day_count):
        left = days_until_games(rseed, day_count)
        return ("The arena is quiet.", f"Next games in {left} day{'s' if left != 1 else ''}.")

    bouts = generate_arena_week(rseed, day_count, biome)
    if world is not None:
        world.pending_arena_open = bouts
    return ("The crowd roars — the games begin!", "Enter the arena to watch and wager.")

def _apply_bazaar(player, region):
    """Mercantile: rare slot bonus is communicated; actual stock bonus would
    require a per-region flag — for v1 we grant a one-time gold + small rep."""
    player.money += 60
    return ("Traders unfold rare goods for you.", "+60g, fresh rare wares this trip")

def _apply_archive(player, region):
    """Scholarly: reveals one undiscovered crafting recipe at random."""
    revealed = None
    try:
        from crafting import ARTISAN_RECIPES
        all_outputs = list(ARTISAN_RECIPES.keys()) if isinstance(ARTISAN_RECIPES, dict) else []
        unknown = [o for o in all_outputs if o not in player.discovered_recipes]
        if unknown:
            revealed = random.choice(unknown)
            player.discovered_recipes.add(revealed)
    except Exception:
        pass
    if revealed:
        return ("The Archive opens a page for you.", f"Recipe revealed: {revealed}")
    return ("The Archive's pages are familiar to you.", "Nothing new today.")

def _apply_shrine(player, region):
    """Pious: long blessing, stronger than a normal shrine."""
    player.blessing_timer = 480.0
    player.blessing_mult  = 1.25
    return ("The shrine's blessing settles on you.", "Loot ×1.25 for 8 minutes")

def _apply_stoneworks(player, region):
    """Builder: hand the player a stack of building blocks."""
    inv = getattr(player, "inventory", None)
    if inv is not None:
        inv["stone_chip"] = inv.get("stone_chip", 0) + 24
        inv["lumber"]     = inv.get("lumber", 0) + 16
    return ("The masons load your packs.", "+24 stone chip, +16 lumber")

def _apply_garden(player, region):
    """Hedonist: stack a few buffs."""
    if hasattr(player, "active_buffs") and isinstance(player.active_buffs, dict):
        player.active_buffs["pleasure_garden"] = {"duration": 600.0}
    return ("The garden lingers on the senses.", "Buffs for 10 minutes")


def _apply_war_camp(player, region):
    """Martial/steppe: training bonus — gold and a short speed buff."""
    player.money += 60
    if hasattr(player, "active_buffs") and isinstance(player.active_buffs, dict):
        player.active_buffs["war_camp_speed"] = {"duration": 300.0}
    return ("The war camp drills you hard.", "+60g, speed buff for 5 minutes")

def _apply_gladiator(player, region):
    """Martial/desert: open the arena (gladiator pit variant)."""
    from gladiators import is_games_day, days_until_games, generate_arena_week
    world      = getattr(player, "world", None)
    day_count  = getattr(world, "day_count", 0)
    rseed      = getattr(region, "region_id", 0) * 1013 + hash(getattr(region, "name", ""))
    biome      = "desert"

    if not is_games_day(rseed, day_count):
        left = days_until_games(rseed, day_count)
        return ("The sands are empty today.", f"Next fights in {left} day{'s' if left != 1 else ''}.")

    bouts = generate_arena_week(rseed, day_count, biome)
    if world is not None:
        world.pending_arena_open = bouts
    return ("The pit masters call for blood!", "Enter the gladiator pits to watch and wager.")

def _apply_harbor(player, region):
    """Mercantile/coastal: sea-trade windfall."""
    player.money += 70
    return ("The harbor master cuts you in on the catch.", "+70g, sea-trade bonus")

def _apply_caravanserai(player, region):
    """Mercantile/silk_road: rest at the waystation — gold and exotic resupply."""
    player.money += 50
    inv = getattr(player, "inventory", None)
    if inv is not None:
        inv["dried_fruit"] = inv.get("dried_fruit", 0) + 6
    return ("The caravanserai fills your pack.", "+50g, +6 dried fruit")

def _apply_imperial_library(player, region):
    """Scholarly/east_asian: reveals two recipes if available."""
    revealed = []
    try:
        from crafting import ARTISAN_RECIPES
        all_outputs = list(ARTISAN_RECIPES.keys()) if isinstance(ARTISAN_RECIPES, dict) else []
        unknown = [o for o in all_outputs if o not in player.discovered_recipes]
        for pick in random.sample(unknown, min(2, len(unknown))):
            player.discovered_recipes.add(pick)
            revealed.append(pick)
    except Exception:
        pass
    if revealed:
        return ("The Imperial Library opens its stacks.", f"Recipes revealed: {', '.join(revealed)}")
    return ("The library's secrets are already yours.", "Nothing new today.")

def _apply_observatory(player, region):
    """Scholarly/mediterranean: reveal a recipe and grant a navigation clarity buff."""
    revealed = None
    try:
        from crafting import ARTISAN_RECIPES
        all_outputs = list(ARTISAN_RECIPES.keys()) if isinstance(ARTISAN_RECIPES, dict) else []
        unknown = [o for o in all_outputs if o not in player.discovered_recipes]
        if unknown:
            revealed = random.choice(unknown)
            player.discovered_recipes.add(revealed)
    except Exception:
        pass
    if hasattr(player, "active_buffs") and isinstance(player.active_buffs, dict):
        player.active_buffs["clarity"] = {"duration": 480.0}
    label = f"Recipe revealed: {revealed}" if revealed else "No new recipes"
    return ("The stars speak tonight.", f"{label}; clarity buff 8 min")

def _apply_sea_temple(player, region):
    """Pious/coastal: fishing blessing — boosts catch rate for the day."""
    player.blessing_timer = 360.0
    player.blessing_mult  = 1.15
    if hasattr(player, "active_buffs") and isinstance(player.active_buffs, dict):
        player.active_buffs["fishing_blessing"] = {"duration": 600.0}
    return ("The sea goddess blesses your nets.", "Fishing ×1.2, loot ×1.15 for 6–10 min")

def _apply_canopy_sanctum(player, region):
    """Pious/jungle: nature blessing — better insect/creature encounter odds."""
    player.blessing_timer = 600.0
    player.blessing_mult  = 1.2
    if hasattr(player, "active_buffs") and isinstance(player.active_buffs, dict):
        player.active_buffs["canopy_blessing"] = {"duration": 600.0}
    return ("The jungle breathes through you.", "Loot ×1.2 for 10 minutes")

def _apply_stonecutters(player, region):
    """Builder/alpine: hand the player alpine stone and ore."""
    inv = getattr(player, "inventory", None)
    if inv is not None:
        inv["stone_chip"]   = inv.get("stone_chip", 0)   + 32
        inv["iron_ore"]     = inv.get("iron_ore", 0)     + 8
        inv["alpine_stone"] = inv.get("alpine_stone", 0) + 16
    return ("The guild loads your cart.", "+32 stone chip, +8 iron ore, +16 alpine stone")

def _apply_vineyard(player, region):
    """Hedonist/mediterranean: wine and long-duration food buff."""
    inv = getattr(player, "inventory", None)
    if inv is not None:
        inv["grape"] = inv.get("grape", 0) + 12
    if hasattr(player, "active_buffs") and isinstance(player.active_buffs, dict):
        player.active_buffs["wine_glow"] = {"duration": 900.0}
    return ("The vineyard pours generously.", "+12 grapes, wine buff 15 minutes")


_EFFECT_FNS = {
    "arena":           _apply_arena,
    "bazaar":          _apply_bazaar,
    "archive":         _apply_archive,
    "shrine":          _apply_shrine,
    "stoneworks":      _apply_stoneworks,
    "garden":          _apply_garden,
    "war_camp":        _apply_war_camp,
    "gladiator":       _apply_gladiator,
    "harbor":          _apply_harbor,
    "caravanserai":    _apply_caravanserai,
    "imperial_library":_apply_imperial_library,
    "observatory":     _apply_observatory,
    "sea_temple":      _apply_sea_temple,
    "canopy_sanctum":  _apply_canopy_sanctum,
    "stonecutters":    _apply_stonecutters,
    "vineyard":        _apply_vineyard,
}


def apply_effect(player, region, day_count: int) -> tuple[bool, str, str]:
    """Try to fire the landmark effect for `region`. Returns (success, title, detail).

    On cooldown, success is False and detail explains when it'll be ready.
    """
    if region is None or not region.agenda:
        return False, "Nothing happens.", ""

    if region.landmark_used_day == day_count:
        return False, "The landmark is quiet today.", "Try again tomorrow."

    spec = landmark_for(region.agenda, getattr(region, "biome_group", ""))
    fn = _EFFECT_FNS.get(spec["effect"])
    if fn is None:
        return False, "Nothing happens.", ""

    title, detail = fn(player, region)
    region.landmark_used_day = day_count

    # Reputation share — visiting a capital landmark always nudges the region
    # (small flat bump, similar to fulfilling a contract).
    from towns import TOWNS
    for tid in region.member_town_ids:
        t = TOWNS.get(tid)
        if t:
            t.reputation += 5

    return True, title, detail
