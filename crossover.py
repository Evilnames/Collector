"""
Cross-system data tables and helpers.

Generalizes the HERBAL_ADDITIVES pattern (tea.py) to all systems so future
crossovers (jewelry buffs, fossil display effects, etc.) can plug in by adding
rows to the tables below — no new modules, no new player state.

Three crossovers ship in v1:
  - Pollination:    insects observed near a crop block boost yield/quality.
  - Pairing buffs:  drinking complementary beverages stacks bonus duration.
  - Aging vessels:  pottery clay biome modifies aged beverage flavor profile.
"""

from blocks import (
    COFFEE_CROP_MATURE, GRAPEVINE_CROP_MATURE,
    TEA_CROP_MATURE, WILDFLOWER_PATCH,
)


# ---------------------------------------------------------------------------
# POLLINATION_AFFINITY
# ---------------------------------------------------------------------------
# Insect species_id -> {crop_block_id: {"yield": float, "quality": float}}
# yield  : multiplier added to harvest count   (0.20 = +20%)
# quality: multiplier added to terroir/quality (0.10 = +10%)
# An insect is considered "near" a crop if it has been observed in the same
# biome — fine-grained position tracking would be expensive and the observation
# system already captures presence.
POLLINATION_AFFINITY = {
    "honeybee": {
        COFFEE_CROP_MATURE:    {"yield": 0.25, "quality": 0.05},
        GRAPEVINE_CROP_MATURE: {"yield": 0.20, "quality": 0.05},
        TEA_CROP_MATURE:       {"yield": 0.15, "quality": 0.05},
        WILDFLOWER_PATCH:      {"yield": 0.10, "quality": 0.10},
    },
    "carpenter_bee": {
        COFFEE_CROP_MATURE:    {"yield": 0.20, "quality": 0.05},
        GRAPEVINE_CROP_MATURE: {"yield": 0.15, "quality": 0.05},
        WILDFLOWER_PATCH:      {"yield": 0.15, "quality": 0.10},
    },
    "sonoran_bumblebee": {
        COFFEE_CROP_MATURE:    {"yield": 0.20, "quality": 0.10},
        WILDFLOWER_PATCH:      {"yield": 0.15, "quality": 0.10},
    },
    "tundra_bumblebee": {
        TEA_CROP_MATURE:       {"yield": 0.20, "quality": 0.10},
        WILDFLOWER_PATCH:      {"yield": 0.15, "quality": 0.10},
    },
    "arctic_bumblebee": {
        TEA_CROP_MATURE:       {"yield": 0.15, "quality": 0.15},
        WILDFLOWER_PATCH:      {"yield": 0.10, "quality": 0.15},
    },
    "arabian_bee": {
        COFFEE_CROP_MATURE:    {"yield": 0.15, "quality": 0.10},
        WILDFLOWER_PATCH:      {"yield": 0.10, "quality": 0.10},
    },
    "monarch": {
        WILDFLOWER_PATCH:      {"yield": 0.05, "quality": 0.20},
        GRAPEVINE_CROP_MATURE: {"yield": 0.00, "quality": 0.10},
    },
    "swallowtail": {
        WILDFLOWER_PATCH:      {"yield": 0.05, "quality": 0.20},
        TEA_CROP_MATURE:       {"yield": 0.00, "quality": 0.15},
    },
    "blue_morpho": {
        WILDFLOWER_PATCH:      {"yield": 0.10, "quality": 0.25},
        COFFEE_CROP_MATURE:    {"yield": 0.00, "quality": 0.20},
    },
    "hummingbird_hawk_moth": {
        WILDFLOWER_PATCH:      {"yield": 0.10, "quality": 0.20},
        TEA_CROP_MATURE:       {"yield": 0.05, "quality": 0.15},
    },
    "ladybug": {
        # Ladybugs eat aphids → reduce yield variance (modest yield, big quality).
        COFFEE_CROP_MATURE:    {"yield": 0.05, "quality": 0.15},
        GRAPEVINE_CROP_MATURE: {"yield": 0.05, "quality": 0.15},
        TEA_CROP_MATURE:       {"yield": 0.05, "quality": 0.15},
        WILDFLOWER_PATCH:      {"yield": 0.00, "quality": 0.10},
    },
    "flower_mantis": {
        WILDFLOWER_PATCH:      {"yield": 0.00, "quality": 0.25},
    },
}


# ---------------------------------------------------------------------------
# PAIRING_TABLE
# ---------------------------------------------------------------------------
# A pairing matches when buffs from BOTH systems in the key are simultaneously
# active. On match, the just-applied buff's duration is multiplied by
# duration_mult, and the pairing is added to player.discovered_pairings.
#
# Key: frozenset of (system_tag, buff_name) tuples.
# system_tag is one of: "coffee", "wine", "tea", "spirit", "herb", "cheese",
# "pottery", "salt".
PAIRING_TABLE = {
    frozenset({("wine", "serenity"),    ("cheese", "satiation")}):
        {"name": "Pastoral Harmony",  "duration_mult": 1.50},
    frozenset({("wine", "vivacity"),    ("cheese", "vigor")}):
        {"name": "Tuscan Feast",      "duration_mult": 1.40},
    frozenset({("wine", "warmth"),      ("cheese", "vitality")}):
        {"name": "Hearthside Supper", "duration_mult": 1.40},

    frozenset({("coffee", "focus"),     ("herb", "keen_eye")}):
        {"name": "Working Breakfast", "duration_mult": 1.50},
    frozenset({("coffee", "rush"),      ("herb", "haste")}):
        {"name": "Morning Sprint",    "duration_mult": 1.60},
    frozenset({("coffee", "endurance"), ("cheese", "satiation")}):
        {"name": "Cafe Brunch",       "duration_mult": 1.40},
    frozenset({("coffee", "clarity"),   ("herb", "focus")}):
        {"name": "Scholar's Cup",     "duration_mult": 1.50},

    frozenset({("spirit", "grit"),      ("herb", "fortune")}):
        {"name": "Hunter's Edge",     "duration_mult": 1.40},
    frozenset({("spirit", "warmth"),    ("salt", "preservation")}):
        {"name": "Sailor's Ration",   "duration_mult": 1.50},
    frozenset({("spirit", "refinement"),("pottery", "wine_complex")}):
        {"name": "Cellar Master",     "duration_mult": 1.60},
    frozenset({("spirit", "sea_legs"),  ("cheese", "nimbleness")}):
        {"name": "Tavern Brawl",      "duration_mult": 1.40},

    frozenset({("tea", "tranquility"),  ("herb", "soothing")}):
        {"name": "Quiet Garden",      "duration_mult": 1.50},
    frozenset({("tea", "harmony"),      ("pottery", "irrigate")}):
        {"name": "Tea Ceremony",      "duration_mult": 1.60},
    frozenset({("tea", "alertness"),    ("coffee", "focus")}):
        {"name": "Twin Peaks",        "duration_mult": 1.30},
    frozenset({("tea", "longevity"),    ("herb", "resilience")}):
        {"name": "Apothecary's Brew", "duration_mult": 1.50},

    frozenset({("cheese", "abundance"), ("pottery", "cook_yield")}):
        {"name": "Granary Spread",    "duration_mult": 1.50},
}


# ---------------------------------------------------------------------------
# AGING_VESSEL_PROFILE
# ---------------------------------------------------------------------------
# Clay biome (from pottery.CLAY_BIOME_PROFILES) -> flavor modifiers applied
# when a beverage is aged inside a vessel made from that clay.
# time_factor scales how quickly aging completes (1.0 = baseline).
AGING_VESSEL_PROFILE = {
    # Dimensions match real beverage fields where possible (Grape / Spirit /
    # TeaLeaf attributes). Unknown dimensions become flavor_notes tags.
    "wetland":       {"earthiness": +0.10, "smoothness": +0.05, "complexity": +0.05, "time_factor": 0.95},
    "tropical":      {"floral":     +0.10, "sweetness":  +0.05, "complexity": +0.05, "time_factor": 1.00},
    "temperate":     {"smoothness": +0.10, "complexity": +0.10, "body":       +0.05, "time_factor": 1.00},
    "river":         {"smoothness": +0.10, "astringency": -0.05, "complexity":+0.05, "time_factor": 0.90},
    "mediterranean": {"aromatics":  +0.10, "sweetness":  +0.05, "complexity": +0.10, "time_factor": 1.05},
    "celadon":       {"floral":     +0.10, "complexity": +0.10, "astringency": -0.05, "time_factor": 1.10},
    "blue_white":    {"smoothness": +0.05, "complexity": +0.15, "aromatics":  +0.05, "time_factor": 1.10},
    "jun":           {"smokiness":  +0.15, "complexity": +0.15, "earthiness": +0.05, "time_factor": 1.20},
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_pollination_bonus(player, biome, crop_block_id):
    """
    Returns {"yield": float, "quality": float} based on pollinators observed
    in the same biome as the crop. Bonuses from multiple species sum.
    """
    total = {"yield": 0.0, "quality": 0.0}
    for species, obs in player.insects_observed.items():
        if obs.get("biome") != biome:
            continue
        affinity = POLLINATION_AFFINITY.get(species)
        if not affinity:
            continue
        crop_bonus = affinity.get(crop_block_id)
        if not crop_bonus:
            continue
        # Diminishing returns by observation count: 1 obs = 50%, 5+ = 100%.
        scale = min(1.0, 0.5 + 0.1 * obs.get("count", 1))
        total["yield"]   += crop_bonus["yield"]   * scale
        total["quality"] += crop_bonus["quality"] * scale
    return total


def _system_buff_dicts(player):
    """Returns a list of (system_tag, buff_dict) for every per-system buff pool."""
    return [
        ("coffee",  player.active_buffs),
        ("wine",    player.wine_buffs),
        ("tea",     player.tea_buffs),
        ("spirit",  player.spirit_buffs),
        ("herb",    player.herb_buffs),
        ("cheese",  player.cheese_buffs),
        ("pottery", player.pottery_buffs),
        ("salt",    player.salt_buffs),
    ]


def detect_active_pairings(player):
    """
    Scan all per-system buff dicts. Returns a list of pairing dicts whose
    required buffs are all currently active.
    Each result: {"key": frozenset, "name": str, "duration_mult": float}
    """
    active = set()
    for system_tag, buffs in _system_buff_dicts(player):
        for buff_name in buffs:
            active.add((system_tag, buff_name))
    matched = []
    for key, info in PAIRING_TABLE.items():
        if key.issubset(active):
            matched.append({"key": key, **info})
    return matched


def apply_pairing_to_buff(player, just_added_system, just_added_buff):
    """
    Called immediately after a buff is added. If the new buff completes a
    pairing, extend the new buff's duration by the pairing multiplier and
    record the pairing as discovered.

    Returns the matched pairing dict, or None.
    """
    target_dict = dict(_system_buff_dicts(player)).get(just_added_system)
    if target_dict is None or just_added_buff not in target_dict:
        return None
    for pairing in detect_active_pairings(player):
        if (just_added_system, just_added_buff) in pairing["key"]:
            mult = pairing["duration_mult"]
            target_dict[just_added_buff]["duration"] *= mult
            player.discovered_pairings.add(pairing["name"])
            player.pending_notifications.append(
                ("Pairing", pairing["name"], "rare"))
            return pairing
    return None


AGING_SATURATION_DAYS = 3.0  # in-game days for full vessel effect


def apply_aging_modifier(beverage, vessel_clay_biome, days_aged):
    """
    Mutates a beverage object (Grape / Spirit / TeaLeaf) in place, adding
    aging contributions scaled by days_aged. Numeric fields that exist on the
    object are bumped; unknown dimensions are appended as tags to flavor_notes.
    Returns the mutated beverage.
    """
    profile = AGING_VESSEL_PROFILE.get(vessel_clay_biome)
    if not profile:
        return beverage
    progress = min(1.0, days_aged / AGING_SATURATION_DAYS) * profile.get("time_factor", 1.0)
    new_notes = []
    for dim, delta in profile.items():
        if dim == "time_factor":
            continue
        scaled = delta * progress
        if hasattr(beverage, dim):
            cur = getattr(beverage, dim)
            if isinstance(cur, (int, float)):
                setattr(beverage, dim, max(0.0, min(1.0, cur + scaled)))
                continue
        sign = "+" if scaled > 0 else "-"
        new_notes.append(f"vessel:{dim}{sign}")
    if new_notes and hasattr(beverage, "flavor_notes"):
        beverage.flavor_notes = list(beverage.flavor_notes) + new_notes
    return beverage
