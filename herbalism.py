"""
Herbalism & Alchemy — recipe discovery, ingredient processing, potion crafting.
No dataclass: potions are inventory items; the "collection" is discovered_recipes.
"""

DRYING_RACK_SLOTS = 6  # number of concurrent drying slots
DRY_DURATION_DAYS = 1  # game days to dry one herb

# ── Ingredient display names ─────────────────────────────────────────────────

INGREDIENT_DISPLAY_NAMES = {
    "dried_mushroom":      "Dried Mushroom",
    "dried_rare_mushroom": "Rare Dried Mushroom",
    "pressed_flower":      "Pressed Flower",
    "pressed_rare_flower": "Pressed Rare Flower",
    "dried_ginger":        "Dried Ginger",
    "dried_garlic":        "Dried Garlic",
    "dried_chamomile":     "Dried Chamomile",
    "dried_lavender":      "Dried Lavender",
    "dried_mint":          "Dried Mint",
    "dried_rosemary":      "Dried Rosemary",
    "dried_thyme":         "Dried Thyme",
    "dried_sage":          "Dried Sage",
    "dried_basil":         "Dried Basil",
    "dried_oregano":       "Dried Oregano",
    "dried_dill":          "Dried Dill",
    "dried_fennel":        "Dried Fennel",
    "dried_tarragon":      "Dried Tarragon",
    "dried_lemon_balm":    "Dried Lemon Balm",
    "dried_echinacea":     "Dried Echinacea",
    "dried_valerian":      "Dried Valerian",
    "dried_st_johns_wort": "Dried St. John's Wort",
    "dried_yarrow":        "Dried Yarrow",
    "dried_bergamot":      "Dried Bergamot",
    "dried_wormwood":      "Dried Wormwood",
    "dried_rue":           "Dried Rue",
    "dried_lemon_verbena": "Dried Lemon Verbena",
    "dried_hyssop":        "Dried Hyssop",
    "dried_catnip":        "Dried Catnip",
    "dried_wood_sorrel":   "Dried Wood Sorrel",
    "dried_marjoram":      "Dried Marjoram",
    "dried_savory":        "Dried Savory",
    "dried_angelica":      "Dried Angelica",
    "dried_borage":        "Dried Borage",
    "dried_comfrey":       "Dried Comfrey",
    "dried_mugwort":       "Dried Mugwort",
    "crystal_shard":       "Crystal Shard",
    "ruby":                "Ruby",
    "cave_mushroom":       "Cave Mushroom",
    "rare_mushroom":       "Rare Mushroom",
    "mushroom":            "Mushroom",
}

# Source item → dried/processed output (Drying Rack conversions)
DRYING_TABLE = {
    "mushroom":       "dried_mushroom",
    "cave_mushroom":  "dried_mushroom",
    "rare_mushroom":  "dried_rare_mushroom",
    "ginger":         "dried_ginger",
    "garlic":         "dried_garlic",
    "chamomile_item": "dried_chamomile",
    "lavender":       "dried_lavender",
    "mint":           "dried_mint",
    "rosemary":       "dried_rosemary",
    "thyme":          "dried_thyme",
    "sage":           "dried_sage",
    "basil":          "dried_basil",
    "oregano":        "dried_oregano",
    "dill":           "dried_dill",
    "fennel":         "dried_fennel",
    "tarragon":       "dried_tarragon",
    "lemon_balm":     "dried_lemon_balm",
    "echinacea":      "dried_echinacea",
    "valerian":       "dried_valerian",
    "st_johns_wort":  "dried_st_johns_wort",
    "yarrow":         "dried_yarrow",
    "bergamot":       "dried_bergamot",
    "wormwood":       "dried_wormwood",
    "rue":            "dried_rue",
    "lemon_verbena":  "dried_lemon_verbena",
    "hyssop":         "dried_hyssop",
    "catnip":         "dried_catnip",
    "wood_sorrel":    "dried_wood_sorrel",
    "marjoram":       "dried_marjoram",
    "savory":         "dried_savory",
    "angelica":       "dried_angelica",
    "borage":         "dried_borage",
    "comfrey":        "dried_comfrey",
    "mugwort":        "dried_mugwort",
}

DRYABLE_ITEMS = list(DRYING_TABLE.keys())

# ── Recipe definitions ────────────────────────────────────────────────────────
# "ingredients" dict must match exactly (item_key → count) to produce output.
# Wildflower rarity determines pressed_rare_flower vs pressed_flower at press time.

RECIPES = {
    # ── Basic potions — Alchemical Kiln (tincture_crafting) ──
    "health_potion": {
        "ingredients": {"dried_mushroom": 2, "pressed_flower": 1},
        "station": "kiln",
        "tier": "basic",
    },
    "speed_potion": {
        "ingredients": {"dried_ginger": 2, "pressed_flower": 1},
        "station": "kiln",
        "tier": "basic",
    },
    "mining_potion": {
        "ingredients": {"dried_mushroom": 1, "dried_ginger": 1, "crystal_shard": 1},
        "station": "kiln",
        "tier": "basic",
    },
    "luck_potion": {
        "ingredients": {"dried_rare_mushroom": 1, "pressed_rare_flower": 1, "dried_garlic": 1},
        "station": "kiln",
        "tier": "basic",
    },
    "resilience_potion": {
        "ingredients": {"dried_mushroom": 1, "dried_rare_mushroom": 1, "pressed_flower": 1},
        "station": "kiln",
        "tier": "basic",
    },
    "soothe_potion": {
        "ingredients": {"dried_lavender": 2, "pressed_flower": 1},
        "station": "kiln",
        "tier": "basic",
    },
    "focus_potion": {
        "ingredients": {"dried_rosemary": 2, "dried_mushroom": 1},
        "station": "kiln",
        "tier": "basic",
    },
    # ── Fine potions — Alchemical Kiln (alchemy research) ──
    "health_potion_fine": {
        "ingredients": {"dried_mushroom": 2, "dried_rare_mushroom": 1, "pressed_flower": 1},
        "station": "kiln",
        "tier": "fine",
    },
    "speed_potion_fine": {
        "ingredients": {"dried_ginger": 2, "pressed_rare_flower": 1, "crystal_shard": 1},
        "station": "kiln",
        "tier": "fine",
    },
    "mining_potion_fine": {
        "ingredients": {"dried_rare_mushroom": 2, "dried_ginger": 1, "crystal_shard": 1},
        "station": "kiln",
        "tier": "fine",
    },
    "luck_potion_fine": {
        "ingredients": {"dried_rare_mushroom": 2, "pressed_rare_flower": 2},
        "station": "kiln",
        "tier": "fine",
    },
    "resilience_potion_fine": {
        "ingredients": {"dried_rare_mushroom": 2, "pressed_rare_flower": 1, "crystal_shard": 1},
        "station": "kiln",
        "tier": "fine",
    },
    "soothe_potion_fine": {
        "ingredients": {"dried_lavender": 2, "pressed_rare_flower": 1, "dried_chamomile": 1},
        "station": "kiln",
        "tier": "fine",
    },
    "focus_potion_fine": {
        "ingredients": {"dried_rosemary": 2, "dried_rare_mushroom": 1, "crystal_shard": 1},
        "station": "kiln",
        "tier": "fine",
    },
    # ── Elixirs — Resonance Chamber (resonance_mastery research) ──
    "healing_elixir": {
        "ingredients": {"dried_rare_mushroom": 2, "pressed_rare_flower": 2, "ruby": 1},
        "station": "resonance",
        "tier": "elixir",
    },
    "swiftness_elixir": {
        "ingredients": {"dried_ginger": 3, "pressed_rare_flower": 1, "ruby": 1},
        "station": "resonance",
        "tier": "elixir",
    },
    "mining_elixir": {
        "ingredients": {"dried_rare_mushroom": 2, "dried_ginger": 2, "ruby": 1},
        "station": "resonance",
        "tier": "elixir",
    },
    "fortune_elixir": {
        "ingredients": {"dried_rare_mushroom": 3, "pressed_rare_flower": 2, "ruby": 1},
        "station": "resonance",
        "tier": "elixir",
    },
    "fortitude_elixir": {
        "ingredients": {"dried_rare_mushroom": 2, "pressed_flower": 2, "ruby": 2},
        "station": "resonance",
        "tier": "elixir",
    },
}

# Sorted display order: basic first, fine second, elixirs last
RECIPE_ORDER = (
    [k for k, v in RECIPES.items() if v["tier"] == "basic"] +
    [k for k, v in RECIPES.items() if v["tier"] == "fine"] +
    [k for k, v in RECIPES.items() if v["tier"] == "elixir"]
)

# All potion / elixir output IDs
ALL_POTION_IDS = list(RECIPES.keys()) + ["mystery_flask"]

# ── Potion display data ───────────────────────────────────────────────────────

POTION_DESCS = {
    "health_potion":         "Restores 25 HP instantly",
    "speed_potion":          "Move speed +35% for 60s",
    "mining_potion":         "Mining speed +25%, +1 pick power for 90s",
    "luck_potion":           "Rare drop chance +40% for 120s",
    "resilience_potion":     "Max health +20 for 90s",
    "soothe_potion":         "Hunger drain -30% for 90s",
    "focus_potion":          "Discovery XP +25% for 90s",
    "health_potion_fine":    "Restores 50 HP instantly",
    "speed_potion_fine":     "Move speed +35% for 100s",
    "mining_potion_fine":    "Mining speed +25%, +1 pick power for 150s",
    "luck_potion_fine":      "Rare drop chance +40% for 180s",
    "resilience_potion_fine":"Max health +20 for 150s",
    "soothe_potion_fine":    "Hunger drain -30% for 150s",
    "focus_potion_fine":     "Discovery XP +25% for 150s",
    "healing_elixir":        "Restores 60 HP instantly",
    "swiftness_elixir":      "Move speed +50% for 120s",
    "mining_elixir":         "Mining speed +40%, +2 pick power for 180s",
    "fortune_elixir":        "Rare drop chance +70% for 180s",
    "fortitude_elixir":      "Max health +40 for 180s",
    "mystery_flask":         "Unknown effect — drink to discover",
}

POTION_COLORS = {
    "health_potion":         (220,  60,  80),
    "speed_potion":          ( 80, 200, 240),
    "mining_potion":         (200, 180,  60),
    "luck_potion":           (255, 215,  50),
    "resilience_potion":     ( 60, 200, 130),
    "soothe_potion":         (190, 155, 230),
    "focus_potion":          (155, 175, 115),
    "health_potion_fine":    (235,  80, 100),
    "speed_potion_fine":     (100, 220, 255),
    "mining_potion_fine":    (215, 200,  80),
    "luck_potion_fine":      (255, 230,  80),
    "resilience_potion_fine":( 80, 220, 155),
    "soothe_potion_fine":    (205, 170, 245),
    "focus_potion_fine":     (175, 195, 135),
    "healing_elixir":        (255, 100, 120),
    "swiftness_elixir":      (120, 240, 255),
    "mining_elixir":         (255, 240,  90),
    "fortune_elixir":        (255, 230,  60),
    "fortitude_elixir":      ( 90, 230, 165),
    "mystery_flask":         (130, 200, 180),
}

TIER_LABELS = {"basic": "Basic", "fine": "Fine", "elixir": "Elixir"}

BUFF_DESCS = {
    "haste":         "Move speed +35%",
    "keen_eye":      "Mining speed +25%  +1 pick power",
    "fortune":       "Rare drop chance +40%",
    "resilience":    "Max health +20",
    "soothing":      "Hunger drain -30%",
    "focus":         "Discovery XP +25%",
    "swiftness":     "Move speed +50%",
    "mastery":       "Mining speed +40%  +2 pick power",
    "great_fortune": "Rare drop chance +70%",
    "fortitude":     "Max health +40",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def match_recipe(slot_items: dict, station: str) -> "str | None":
    """
    slot_items = {item_key: count} — zero-count entries should be excluded.
    Returns output_id if slot_items exactly matches a recipe for this station,
    otherwise None.
    """
    clean = {k: v for k, v in slot_items.items() if v > 0}
    for out_id, recipe in RECIPES.items():
        if recipe["station"] == station and recipe["ingredients"] == clean:
            return out_id
    return None


def get_dried_item(source_key: str) -> "str | None":
    return DRYING_TABLE.get(source_key)


def can_press_flower(rarity: str) -> str:
    return "pressed_rare_flower" if rarity in ("rare", "epic", "legendary") else "pressed_flower"


def recipe_requires_research(out_id: str, research) -> bool:
    """Returns True if the player has the required research node unlocked."""
    tier = RECIPES.get(out_id, {}).get("tier", "basic")
    if tier == "fine":
        return research is not None and research.nodes.get("alchemy", None) and \
               research.nodes["alchemy"].unlocked
    if tier == "elixir":
        return research is not None and research.nodes.get("resonance_mastery", None) and \
               research.nodes["resonance_mastery"].unlocked
    # basic potions require tincture_crafting
    return research is not None and research.nodes.get("tincture_crafting", None) and \
           research.nodes["tincture_crafting"].unlocked
