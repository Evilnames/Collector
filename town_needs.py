"""
town_needs.py — Town supply categories, item membership, and reward constants.
Pure data; no game state here.
"""

# ── Basic supply categories (all towns always want these) ────────────────────

TOWN_CATEGORIES = {
    "food": [
        "wheat", "carrot", "tomato", "corn", "pumpkin", "apple",
        "potato", "onion", "mushroom", "rice",
        "bread", "cooked_mutton", "cooked_beef", "cooked_chicken", "cooked_egg",
        "cooked_venison", "cooked_boar", "cooked_rabbit", "cooked_turkey",
        "cooked_bear", "cooked_duck", "cooked_bison", "cooked_pheasant",
    ],
    "wood": [
        "lumber",
        "walnut_plank", "teak_plank", "driftwood_plank", "ebony_plank",
        "mahogany_plank", "ash_plank", "nordic_plank", "charcoal_plank",
        "stave_plank",
    ],
    "stone": [
        "stone_chip", "limestone_chip",
    ],
    "metal": [
        "iron_chunk", "gold_nugget", "iron_bar", "gold_ingot",
    ],
}

# ── Luxury categories (biome-specialty; harder to make, higher rewards) ──────

LUXURY_CATEGORIES = {
    "wine": [
        "red_wine",        "white_wine",        "rose_wine",
        "sparkling_wine",  "dessert_wine",
        "red_wine_fine",   "white_wine_fine",   "rose_wine_fine",
        "sparkling_wine_fine", "dessert_wine_fine",
        "red_wine_reserve","white_wine_reserve", "rose_wine_reserve",
        "sparkling_wine_reserve", "dessert_wine_reserve",
    ],
    "coffee": [
        "drip_coffee",       "espresso",       "pour_over",
        "cold_brew",         "french_press",
        "drip_coffee_fine",  "espresso_fine",  "pour_over_fine",
        "cold_brew_fine",    "french_press_fine",
        "drip_coffee_superior", "espresso_superior", "pour_over_superior",
        "cold_brew_superior",   "french_press_superior",
    ],
    "spirits": [
        "whiskey",        "bourbon",        "rum",
        "gin",            "brandy",         "vodka",
        "whiskey_aged",   "bourbon_aged",   "rum_aged",
        "gin_aged",       "brandy_aged",    "vodka_aged",
        "whiskey_reserve","bourbon_reserve", "rum_reserve",
        "gin_reserve",    "brandy_reserve", "vodka_reserve",
    ],
    "pottery": [
        "clay_cooking_pot",        "clay_cooking_pot_fine",  "clay_cooking_pot_masterwork",
        "pottery_vase",            "pottery_vase_fine",      "pottery_vase_masterwork",
        "wine_amphora",            "wine_amphora_fine",      "wine_amphora_masterwork",
        "herb_storage_jar",        "herb_storage_jar_fine",  "herb_storage_jar_masterwork",
    ],
    "tea": [
        "green_tea",        "oolong_tea",        "black_tea",        "puerh_tea",
        "green_tea_fine",   "oolong_tea_fine",   "black_tea_fine",   "puerh_tea_fine",
        "green_tea_aged",   "oolong_tea_aged",   "black_tea_aged",   "puerh_tea_aged",
    ],
    "herbs": [
        "health_potion",     "speed_potion",     "mining_potion",
        "luck_potion",       "resilience_potion","soothe_potion",    "focus_potion",
        "health_potion_fine","speed_potion_fine", "mining_potion_fine",
        "luck_potion_fine",  "resilience_potion_fine","soothe_potion_fine","focus_potion_fine",
        "healing_elixir",    "swiftness_elixir", "mining_elixir",
        "fortune_elixir",    "fortitude_elixir",
        "dried_chamomile",   "dried_lavender",   "dried_mint",
        "dried_rosemary",    "dried_thyme",      "dried_sage",
        "dried_ginger",      "dried_garlic",
    ],
    "beer": [
        "ale",          "lager",          "stout",         "ipa",
        "wheat_beer",   "saison",         "porter",        "amber_ale",
        "pilsner",      "brown_ale",      "sour",          "barleywine",
        "ale_fine",     "lager_fine",     "stout_fine",    "ipa_fine",
        "wheat_beer_fine", "saison_fine", "porter_fine",   "amber_ale_fine",
        "pilsner_fine", "brown_ale_fine", "sour_fine",     "barleywine_fine",
        "ale_reserve",  "lager_reserve",  "stout_reserve", "ipa_reserve",
        "wheat_beer_reserve", "saison_reserve", "porter_reserve", "amber_ale_reserve",
        "pilsner_reserve", "brown_ale_reserve", "sour_reserve", "barleywine_reserve",
    ],
}

# ── Display metadata ─────────────────────────────────────────────────────────

CATEGORY_DISPLAY = {
    "food":    "Food",
    "wood":    "Wood",
    "stone":   "Stone",
    "metal":   "Metal",
    # Luxury (★ prefix marks craft goods)
    "wine":    "★ Wine",
    "coffee":  "★ Coffee",
    "spirits": "★ Spirits",
    "pottery": "★ Pottery",
    "tea":     "★ Tea",
    "herbs":   "★ Herbs & Potions",
    "beer":    "★ Beer",
}

CATEGORY_COLOR = {
    "food":    (200, 180,  60),
    "wood":    (140,  90,  50),
    "stone":   (150, 150, 140),
    "metal":   (160, 170, 185),
    # Luxury — richer, warmer tones
    "wine":    (180,  50,  90),
    "coffee":  (130,  80,  35),
    "spirits": (210, 160,  40),
    "pottery": (185, 110,  60),
    "tea":     ( 60, 160, 100),
    "herbs":   ( 70, 170,  80),
    "beer":    (190, 140,  50),
}

# ── Gold paid per unit delivered ─────────────────────────────────────────────

GOLD_PER_UNIT = {
    "food":    1,
    "wood":    2,
    "stone":   2,
    "metal":   6,
    # Luxury — 3-8× higher; reflects effort of the full craft pipeline
    "wine":    15,
    "coffee":  12,
    "spirits": 20,
    "pottery": 10,
    "tea":     12,
    "herbs":   8,
    "beer":    14,
}

# ── Base need amounts (multiplied by tier+1) ─────────────────────────────────

BASE_NEED_AMOUNT = {
    "food":  80,
    "wood":  60,
    "stone": 50,
    "metal": 30,
}

# Luxury needs are smaller quantities — each unit is much harder to produce
BASE_NEED_AMOUNT_LUXURY = {
    "wine":    12,
    "coffee":  15,
    "spirits": 10,
    "pottery": 12,
    "tea":     15,
    "herbs":   18,
    "beer":    14,
}

# ── Preferred variant pools (biome-biased; any quality of the base type counts) ──
# Keys are biome group names + "_default" fallback.
# Values are base item_id prefixes — "espresso" matches espresso/espresso_fine/etc.

LUXURY_VARIANT_POOLS: dict[str, dict[str, list[str]]] = {
    "wine": {
        "forest":        ["red_wine",     "rose_wine",      "white_wine"],
        "jungle":        ["white_wine",   "sparkling_wine", "rose_wine"],
        "wetland":       ["white_wine",   "rose_wine",      "sparkling_wine"],
        "desert":        ["dessert_wine", "red_wine",       "rose_wine"],
        "alpine":        ["red_wine",     "sparkling_wine", "white_wine"],
        "steppe":        ["red_wine",     "dessert_wine",   "rose_wine"],
        "coastal":       ["white_wine",   "sparkling_wine", "rose_wine"],
        "highland":      ["red_wine",     "rose_wine",      "sparkling_wine"],
        "mediterranean": ["red_wine",     "white_wine",     "rose_wine",    "sparkling_wine"],
        "levant":        ["red_wine",     "dessert_wine",   "white_wine"],
        "persia":        ["dessert_wine", "red_wine",       "rose_wine"],
        "silk_road":     ["white_wine",   "red_wine",       "sparkling_wine"],
        "_default":      ["red_wine",     "white_wine",     "rose_wine",    "dessert_wine"],
    },
    "coffee": {
        "forest":   ["pour_over",   "french_press"],
        "jungle":   ["espresso",    "cold_brew"],
        "wetland":  ["drip_coffee", "french_press"],
        "desert":   ["espresso",    "drip_coffee"],
        "alpine":   ["french_press","pour_over"],
        "steppe":   ["drip_coffee", "cold_brew"],
        "coastal":  ["cold_brew",   "pour_over"],
        "highland": ["french_press","drip_coffee"],
        "_default": ["drip_coffee", "espresso",    "pour_over"],
    },
    "spirits": {
        "forest":   ["whiskey",  "brandy"],
        "jungle":   ["rum",      "gin"],
        "wetland":  ["gin",      "vodka"],
        "desert":   ["brandy",   "rum"],
        "alpine":   ["whiskey",  "bourbon"],
        "steppe":   ["vodka",    "whiskey"],
        "coastal":  ["rum",      "gin"],
        "highland": ["bourbon",  "whiskey"],
        "_default": ["whiskey",  "bourbon", "rum"],
    },
    "pottery": {
        "forest":   ["herb_storage_jar",  "clay_cooking_pot"],
        "jungle":   ["pottery_vase",      "clay_cooking_pot"],
        "wetland":  ["clay_cooking_pot",  "herb_storage_jar"],
        "desert":   ["wine_amphora",      "pottery_vase"],
        "alpine":   ["clay_cooking_pot",  "wine_amphora"],
        "steppe":   ["clay_cooking_pot",  "pottery_vase"],
        "coastal":  ["wine_amphora",      "pottery_vase"],
        "highland": ["wine_amphora",      "clay_cooking_pot"],
        "_default": ["clay_cooking_pot",  "pottery_vase"],
    },
    "tea": {
        "forest":      ["green_tea",  "oolong_tea",  "puerh_tea"],
        "jungle":      ["green_tea",  "oolong_tea",  "black_tea"],
        "wetland":     ["black_tea",  "puerh_tea",   "oolong_tea"],
        "desert":      ["black_tea",  "puerh_tea",   "green_tea"],
        "alpine":      ["black_tea",  "puerh_tea",   "green_tea"],
        "steppe":      ["black_tea",  "green_tea",   "oolong_tea"],
        "coastal":     ["green_tea",  "oolong_tea",  "black_tea"],
        "highland":    ["black_tea",  "oolong_tea",  "puerh_tea"],
        "east_asian":  ["green_tea",  "oolong_tea",  "black_tea",  "puerh_tea"],
        "yunnan":      ["puerh_tea",  "black_tea",   "green_tea"],
        "south_asian": ["black_tea",  "green_tea",   "oolong_tea"],
        "_default":    ["green_tea",  "black_tea",   "oolong_tea", "puerh_tea"],
    },
    "beer": {
        "forest":        ["ale",       "porter",     "brown_ale"],
        "jungle":        ["wheat_beer","saison",     "sour"],
        "wetland":       ["stout",     "porter",     "brown_ale"],
        "desert":        ["barleywine","lager",      "amber_ale"],
        "alpine":        ["lager",     "ale",        "pilsner"],
        "steppe":        ["pilsner",   "lager",      "ale"],
        "coastal":       ["wheat_beer","ale",        "lager",   "saison"],
        "highland":      ["ale",       "amber_ale",  "stout"],
        "mediterranean": ["lager",     "wheat_beer", "pilsner"],
        "east_asian":    ["wheat_beer","pilsner",    "sour"],
        "_default":      ["ale",       "lager",      "wheat_beer", "amber_ale"],
    },
    "herbs": {
        "forest":   ["health_potion",     "soothe_potion"],
        "jungle":   ["luck_potion",        "focus_potion"],
        "wetland":  ["soothe_potion",      "resilience_potion"],
        "desert":   ["resilience_potion",  "health_potion"],
        "alpine":   ["health_potion",      "mining_potion"],
        "steppe":   ["speed_potion",       "resilience_potion"],
        "coastal":  ["focus_potion",       "luck_potion"],
        "highland": ["mining_potion",      "health_potion"],
        "_default": ["health_potion",      "speed_potion"],
    },
}

PREFERRED_BONUS_MULT = 1.5   # gold multiplier for delivering the preferred variant

# ── Reputation rewards ───────────────────────────────────────────────────────

REP_PER_NEED_FILLED    = 10   # basic supply categories
REP_PER_LUXURY_FILLED  = 25   # luxury craft categories (fully satisfying one)

# ── Military supply (only assigned to military-type towns) ───────────────────

MILITARY_CATEGORIES = {
    "weapons": [
        "wood_bow", "recurve_bow", "composite_bow", "longbow", "crossbow",
        "wood_arrow", "bone_arrow", "flint_arrow", "iron_arrow",
        "barbed_arrow", "broadhead_arrow", "poison_arrow", "gold_arrow",
    ],
}

CATEGORY_DISPLAY["weapons"]  = "* Weapons"
CATEGORY_COLOR["weapons"]    = (180, 130,  90)
GOLD_PER_UNIT["weapons"]     = 18

BASE_NEED_AMOUNT_MILITARY = {
    "weapons": 20,
}

# ── Reverse maps: item_id → category ────────────────────────────────────────

ITEM_TO_CATEGORY: dict[str, str] = {
    item: cat
    for cat, items in {**TOWN_CATEGORIES, **LUXURY_CATEGORIES, **MILITARY_CATEGORIES}.items()
    for item in items
}
