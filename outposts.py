import json
import random
from dataclasses import dataclass

from constants import CHUNK_W, BLOCK_SIZE
from blocks import STONE, BEDROCK, AIR, OUTPOST_FLAG_BLOCK

# ---------------------------------------------------------------------------
# Spawn constants
# ---------------------------------------------------------------------------

OUTPOST_SLOT_SPACING = 80   # one candidate slot every 80 blocks
OUTPOST_SPAWN_CHANCE = 0.20 # 20% → avg ~1 outpost per 400 blocks

# ---------------------------------------------------------------------------
# Type definitions
# Each entry: display_name, eligible_biomes, sells [(item_id, gold_cost)],
#   buys [(item_id, gold_pay, max_qty)], needs [(item_id, daily_required)],
#   base_stock (units per sell slot), clothing_key, building_style, half_w
# ---------------------------------------------------------------------------

OUTPOST_TYPES = {

    "wine_estate": {
        "display_name":    "Wine Estate",
        "eligible_biomes": ["temperate", "birch_forest", "redwood", "rolling_hills",
                            "mediterranean", "steppe", "arid_steppe"],
        "sells": [("red_wine", 18), ("white_wine", 16),
                  ("red_wine_fine", 40), ("white_wine_fine", 38)],
        "buys":  [("red_wine_reserve", 90, 2), ("white_wine_reserve", 85, 2)],
        "needs": [("lumber", 20), ("iron_chunk", 5)],
        "base_stock": 5, "clothing_key": "winemaker",
        "building_style": "house", "half_w": 18,
    },

    "herb_monastery": {
        "display_name":    "Herb Monastery",
        "eligible_biomes": ["temperate", "birch_forest", "rolling_hills",
                            "redwood", "alpine_mountain", "rocky_mountain"],
        "sells": [("philosophers_scroll", 28), ("votive_tablet", 22),
                  ("rare_mushroom", 35), ("olive_branch", 15)],
        "buys":  [("rare_mushroom", 40, 6), ("mushroom", 8, 12)],
        "needs": [("lumber", 12), ("coal", 8)],
        "base_stock": 5, "clothing_key": "monk",
        "building_style": "shrine", "half_w": 16,
    },

    "trapper_post": {
        "display_name":    "Trapper Post",
        "eligible_biomes": ["boreal", "tundra", "steppe", "wasteland"],
        "sells": [("rabbit_pelt", 18), ("fox_pelt", 22)],
        "buys":  [("rabbit_pelt", 20, 8), ("fox_pelt", 26, 6), ("bear_pelt", 42, 3)],
        "needs": [("lumber", 15), ("iron_chunk", 5)],
        "base_stock": 6, "clothing_key": "trapper",
        "building_style": "house", "half_w": 14,
    },

    "boreal_distillery": {
        "display_name":    "Boreal Distillery",
        "eligible_biomes": ["boreal", "tundra", "rocky_mountain", "wasteland"],
        "sells": [("whiskey", 20), ("whiskey_aged", 45),
                  ("bourbon", 22), ("bourbon_aged", 48)],
        "buys":  [("whiskey_reserve", 95, 2), ("bourbon_reserve", 95, 2)],
        "needs": [("lumber", 25), ("coal", 10), ("iron_chunk", 8)],
        "base_stock": 4, "clothing_key": "distiller",
        "building_style": "smithy", "half_w": 15,
    },

    "coffee_plantation": {
        "display_name":    "Coffee Plantation",
        "eligible_biomes": ["jungle", "tropical", "wetland", "savanna", "south_asian"],
        "sells": [("drip_coffee", 14), ("espresso", 18),
                  ("pour_over", 16), ("drip_coffee_fine", 30)],
        "buys":  [("drip_coffee_fine", 38, 4), ("espresso_fine", 35, 4),
                  ("pour_over_fine", 35, 4)],
        "needs": [("lumber", 12), ("iron_chunk", 6)],
        "base_stock": 5, "clothing_key": "plantation_worker",
        "building_style": "house", "half_w": 16,
    },

    "jungle_herbalist": {
        "display_name":    "Jungle Herbalist",
        "eligible_biomes": ["jungle", "tropical", "wetland", "swamp"],
        "sells": [("rare_mushroom", 30), ("mushroom", 6), ("olive_branch", 12)],
        "buys":  [("mushroom", 8, 15), ("rare_mushroom", 36, 8)],
        "needs": [("lumber", 10)],
        "base_stock": 6, "clothing_key": "jungle_healer",
        "building_style": "house", "half_w": 13,
    },

    "tea_house": {
        "display_name":    "Tea House",
        "eligible_biomes": ["east_asian", "alpine_mountain", "rolling_hills"],
        "sells": [("philosophers_scroll", 25), ("votive_tablet", 20), ("olive_branch", 15)],
        "buys":  [("wine_amphora", 22, 4), ("pottery_vase", 18, 4)],
        "needs": [("lumber", 8), ("coal", 6)],
        "base_stock": 5, "clothing_key": "tea_master",
        "building_style": "shrine", "half_w": 14,
    },

    "pottery_workshop": {
        "display_name":    "Pottery Workshop",
        "eligible_biomes": ["east_asian", "south_asian", "mediterranean", "steppe",
                            "rolling_hills"],
        "sells": [("clay_cooking_pot", 18), ("clay_cooking_pot_fine", 40),
                  ("pottery_vase", 22), ("wine_amphora", 28)],
        "buys":  [("clay_cooking_pot_fine", 50, 3), ("pottery_vase_fine", 58, 3),
                  ("wine_amphora_fine", 70, 2)],
        "needs": [("coal", 15), ("stone_chip", 20)],
        "base_stock": 4, "clothing_key": "potter",
        "building_style": "smithy", "half_w": 13,
    },

    "spice_market": {
        "display_name":    "Spice Market",
        "eligible_biomes": ["south_asian", "tropical", "jungle", "savanna"],
        "sells": [("rare_mushroom", 28), ("mushroom", 5), ("votive_tablet", 18)],
        "buys":  [("mushroom", 7, 15), ("rare_mushroom", 34, 8)],
        "needs": [("lumber", 8), ("coal", 5)],
        "base_stock": 6, "clothing_key": "south_asian",
        "building_style": "house", "half_w": 14,
    },

    "textile_guild": {
        "display_name":    "Textile Guild",
        "eligible_biomes": ["south_asian", "east_asian", "mediterranean", "temperate"],
        "sells": [("rabbit_pelt", 16), ("fox_pelt", 20)],
        "buys":  [("rabbit_pelt", 18, 10), ("fox_pelt", 22, 8)],
        "needs": [("iron_chunk", 6), ("lumber", 10)],
        "base_stock": 6, "clothing_key": "weaver",
        "building_style": "house", "half_w": 13,
    },

    "olive_press": {
        "display_name":    "Olive Press",
        "eligible_biomes": ["mediterranean", "arid_steppe", "savanna"],
        "sells": [("wine_amphora", 28), ("red_wine", 15), ("white_wine", 14)],
        "buys":  [("red_wine", 20, 8), ("white_wine", 18, 8), ("red_wine_fine", 48, 4)],
        "needs": [("lumber", 18), ("stone_chip", 15)],
        "base_stock": 5, "clothing_key": "mediterranean",
        "building_style": "house", "half_w": 15,
    },

    "salt_works": {
        "display_name":    "Salt Works",
        "eligible_biomes": ["mediterranean", "beach", "wetland", "swamp"],
        "sells": [("coarse_salt", 8), ("fine_salt", 12)],
        "buys":  [("coarse_salt", 10, 10)],
        "needs": [("coal", 12), ("iron_chunk", 5)],
        "base_stock": 7, "clothing_key": "saltworker",
        "building_style": "smithy", "half_w": 12,
    },

    "desert_glassworks": {
        "display_name":    "Desert Glassworks",
        "eligible_biomes": ["desert", "arid_steppe", "canyon"],
        "sells": [("crystal_shard", 18), ("obsidian_slab", 25)],
        "buys":  [("crystal_shard", 20, 8), ("obsidian_slab", 30, 5),
                  ("stone_chip", 3, 20)],
        "needs": [("coal", 20), ("iron_chunk", 8)],
        "base_stock": 5, "clothing_key": "desert",
        "building_style": "smithy", "half_w": 14,
    },

    "canyon_forge": {
        "display_name":    "Canyon Forge",
        "eligible_biomes": ["canyon", "rocky_mountain", "desert", "wasteland"],
        "sells": [("iron_bar", 20), ("tempered_iron", 58)],
        "buys":  [("iron_chunk", 5, 15), ("gold_nugget", 12, 8)],
        "needs": [("coal", 25), ("iron_chunk", 10)],
        "base_stock": 4, "clothing_key": "blacksmith",
        "building_style": "smithy", "half_w": 13,
    },

    "alpine_monastery": {
        "display_name":    "Alpine Monastery",
        "eligible_biomes": ["alpine_mountain", "rocky_mountain", "tundra"],
        "sells": [("philosophers_scroll", 28), ("votive_tablet", 22),
                  ("rare_mushroom", 35), ("olive_branch", 15)],
        "buys":  [("rare_mushroom", 40, 6), ("mushroom", 8, 10)],
        "needs": [("lumber", 12), ("coal", 8)],
        "base_stock": 5, "clothing_key": "monk",
        "building_style": "shrine", "half_w": 16,
    },

    "cheese_cave": {
        "display_name":    "Cheese Cave",
        "eligible_biomes": ["alpine_mountain", "rocky_mountain", "rolling_hills", "boreal"],
        "sells": [("cheese", 14)],
        "buys":  [("cheese", 18, 8)],
        "needs": [("lumber", 10), ("iron_chunk", 6), ("coarse_salt", 8)],
        "base_stock": 7, "clothing_key": "alpine",
        "building_style": "house", "half_w": 13,
    },

    "fungal_grove": {
        "display_name":    "Fungal Grove",
        "eligible_biomes": ["fungal", "swamp", "wetland"],
        "sells": [("mushroom", 5), ("rare_mushroom", 28)],
        "buys":  [("mushroom", 7, 20), ("rare_mushroom", 35, 8)],
        "needs": [("lumber", 10)],
        "base_stock": 7, "clothing_key": "fungi_keeper",
        "building_style": "house", "half_w": 12,
    },

    "swamp_alchemist": {
        "display_name":    "Swamp Alchemist",
        "eligible_biomes": ["swamp", "wetland", "fungal"],
        "sells": [("rare_mushroom", 30), ("philosophers_scroll", 24), ("votive_tablet", 18)],
        "buys":  [("mushroom", 7, 12), ("rare_mushroom", 36, 8)],
        "needs": [("coal", 10), ("iron_chunk", 4)],
        "base_stock": 5, "clothing_key": "alchemist",
        "building_style": "smithy", "half_w": 12,
    },

    "fishing_outpost": {
        "display_name":    "Fishing Outpost",
        "eligible_biomes": ["beach", "wetland", "tropical"],
        "sells": [("bread", 8), ("cooked_beef", 14), ("fish", 12)],
        "buys":  [("fish", 15, 8)],
        "needs": [("lumber", 15), ("iron_chunk", 5)],
        "base_stock": 6, "clothing_key": "coastal",
        "building_style": "house", "half_w": 13,
    },

    "coastal_saltworks": {
        "display_name":    "Coastal Salt Works",
        "eligible_biomes": ["beach", "mediterranean", "tropical"],
        "sells": [("coarse_salt", 7), ("fine_salt", 10)],
        "buys":  [("coarse_salt", 9, 12)],
        "needs": [("lumber", 10), ("stone_chip", 10)],
        "base_stock": 7, "clothing_key": "saltworker",
        "building_style": "house", "half_w": 12,
    },

    "nomad_camp": {
        "display_name":    "Nomad Camp",
        "eligible_biomes": ["steppe", "arid_steppe", "savanna", "wasteland"],
        "sells": [("rabbit_pelt", 16), ("fox_pelt", 20), ("cooked_beef", 12)],
        "buys":  [("rabbit_pelt", 18, 10), ("fox_pelt", 22, 8), ("bear_pelt", 38, 3)],
        "needs": [("coal", 10), ("iron_chunk", 8)],
        "base_stock": 6, "clothing_key": "steppe_nomad",
        "building_style": "house", "half_w": 14,
    },

    "spirit_distillery": {
        "display_name":    "Spirit Distillery",
        "eligible_biomes": ["steppe", "arid_steppe", "savanna", "temperate",
                            "rolling_hills", "mediterranean"],
        "sells": [("rum", 20), ("brandy", 22), ("whiskey", 20), ("bourbon", 22)],
        "buys":  [("whiskey_reserve", 95, 2), ("bourbon_reserve", 95, 2),
                  ("brandy_aged", 55, 3)],
        "needs": [("lumber", 20), ("coal", 15), ("iron_chunk", 6)],
        "base_stock": 4, "clothing_key": "distiller",
        "building_style": "smithy", "half_w": 15,
    },

    "hillside_vineyard": {
        "display_name":    "Hillside Vineyard",
        "eligible_biomes": ["rolling_hills", "steep_hills", "temperate", "mediterranean"],
        "sells": [("red_wine", 16), ("white_wine", 15), ("red_wine_fine", 38)],
        "buys":  [("red_wine_reserve", 92, 2), ("white_wine_reserve", 88, 2)],
        "needs": [("lumber", 15), ("iron_chunk", 5)],
        "base_stock": 5, "clothing_key": "winemaker",
        "building_style": "house", "half_w": 16,
    },

    "sculpture_atelier": {
        "display_name":    "Sculpture Atelier",
        "eligible_biomes": ["steep_hills", "rocky_mountain", "canyon",
                            "mediterranean", "east_asian"],
        "sells": [("votive_tablet", 20), ("crystal_shard", 16), ("stone_chip", 3)],
        "buys":  [("stone_chip", 4, 20), ("crystal_shard", 18, 8)],
        "needs": [("iron_chunk", 8), ("coal", 5)],
        "base_stock": 5, "clothing_key": "artisan",
        "building_style": "smithy", "half_w": 13,
    },

    # --- Military outposts ---

    "border_garrison": {
        "display_name":    "Border Garrison",
        "eligible_biomes": ["temperate", "rolling_hills", "steep_hills", "birch_forest"],
        "sells": [("recurve_bow", 25), ("iron_arrow", 8), ("flint_arrow", 5), ("iron_bar", 22)],
        "buys":  [("iron_chunk", 6, 15), ("lumber", 3, 20), ("coal", 4, 12),
                  ("iron_arrow", 5, 20), ("wood_arrow", 2, 30)],
        "needs": [("iron_chunk", 10), ("coal", 15)],
        "base_stock": 4, "clothing_key": "soldier",
        "building_style": "smithy", "half_w": 16,
    },

    "highland_fortress": {
        "display_name":    "Highland Fortress",
        "eligible_biomes": ["rocky_mountain", "alpine_mountain", "steep_hills", "canyon"],
        "sells": [("longbow", 55), ("broadhead_arrow", 12), ("tempered_iron", 60), ("iron_arrow", 8)],
        "buys":  [("iron_chunk", 6, 15), ("coal", 4, 15), ("stone_chip", 3, 20),
                  ("broadhead_arrow", 10, 15), ("iron_arrow", 5, 15)],
        "needs": [("iron_chunk", 12), ("coal", 20)],
        "base_stock": 3, "clothing_key": "fortress_guard",
        "building_style": "smithy", "half_w": 18,
    },

    "desert_legion": {
        "display_name":    "Desert Legion",
        "eligible_biomes": ["desert", "arid_steppe", "canyon", "savanna"],
        "sells": [("crossbow", 80), ("composite_bow", 45), ("iron_arrow", 8), ("iron_bar", 22)],
        "buys":  [("iron_chunk", 6, 15), ("gold_nugget", 10, 5), ("coal", 4, 12),
                  ("iron_arrow", 5, 15), ("flint_arrow", 4, 20)],
        "needs": [("iron_chunk", 12), ("coal", 18)],
        "base_stock": 3, "clothing_key": "legion",
        "building_style": "smithy", "half_w": 17,
    },

    "steppe_warcamp": {
        "display_name":    "Steppe Warcamp",
        "eligible_biomes": ["steppe", "wasteland", "savanna", "arid_steppe"],
        "sells": [("composite_bow", 40), ("flint_arrow", 6), ("wood_arrow", 4), ("iron_chunk", 7)],
        "buys":  [("rabbit_pelt", 16, 10), ("wolf_pelt", 28, 6), ("iron_chunk", 6, 10),
                  ("wood_arrow", 3, 25), ("flint_arrow", 4, 20)],
        "needs": [("lumber", 15), ("coal", 8)],
        "base_stock": 5, "clothing_key": "warlord",
        "building_style": "house", "half_w": 15,
    },

    "coastal_citadel": {
        "display_name":    "Coastal Citadel",
        "eligible_biomes": ["beach", "mediterranean", "tropical"],
        "sells": [("recurve_bow", 25), ("iron_arrow", 8), ("iron_bar", 20), ("wood_bow", 14)],
        "buys":  [("lumber", 3, 20), ("iron_chunk", 6, 15), ("coal", 4, 10),
                  ("recurve_bow", 18, 3), ("iron_arrow", 5, 20)],
        "needs": [("lumber", 20), ("iron_chunk", 10)],
        "base_stock": 4, "clothing_key": "naval_guard",
        "building_style": "smithy", "half_w": 16,
    },

    # --- Region-flavored outposts ---

    "timber_camp": {
        "display_name":    "Timber Camp",
        "eligible_biomes": ["redwood", "boreal", "birch_forest", "temperate"],
        "sells": [("lumber", 4), ("sapling", 6), ("wood_arrow", 3), ("wood_bow", 14)],
        "buys":  [("lumber", 5, 25), ("sapling", 4, 15), ("elk_antler", 12, 6),
                  ("deer_hide", 14, 8)],
        "needs": [("iron_chunk", 8), ("coal", 6)],
        "base_stock": 8, "clothing_key": "lumberjack",
        "building_style": "smithy", "half_w": 15,
    },

    "reed_weaver": {
        "display_name":    "Reed Weaver",
        "eligible_biomes": ["wetland", "swamp", "tropical"],
        "sells": [("woven_rug", 22), ("textile_rug_natural", 26),
                  ("linen_fold", 18), ("reed_bundle", 6)],
        "buys":  [("reed_bundle", 7, 20), ("cattail", 5, 15), ("bulrush", 5, 15),
                  ("sedge", 4, 20), ("horsetail", 4, 15)],
        "needs": [("lumber", 10), ("iron_chunk", 4)],
        "base_stock": 6, "clothing_key": "weaver",
        "building_style": "house", "half_w": 13,
    },

    "silk_pavilion": {
        "display_name":    "Silk Pavilion",
        "eligible_biomes": ["east_asian", "south_asian", "jungle", "tropical"],
        "sells": [("textile_rug_amber", 32), ("textile_tapestry_amber", 38),
                  ("andean_textile", 28), ("golden_wool", 22)],
        "buys":  [("wool", 5, 20), ("golden_wool", 18, 8), ("cotton_fiber", 7, 20)],
        "needs": [("lumber", 10), ("coal", 6)],
        "base_stock": 5, "clothing_key": "silk_master",
        "building_style": "house", "half_w": 14,
    },

    "incense_lodge": {
        "display_name":    "Incense Lodge",
        "eligible_biomes": ["south_asian", "tropical", "jungle", "east_asian"],
        "sells": [("votive_tablet", 22), ("philosophers_scroll", 28),
                  ("dye_extract_amber", 16), ("dye_extract_violet", 18)],
        "buys":  [("lotus_petal", 8, 15), ("water_iris", 6, 15), ("marsh_marigold", 6, 15),
                  ("dye_extract_amber", 18, 6), ("dye_extract_violet", 20, 6)],
        "needs": [("lumber", 8), ("coal", 5)],
        "base_stock": 5, "clothing_key": "south_asian",
        "building_style": "shrine", "half_w": 14,
    },

    "glacier_camp": {
        "display_name":    "Glacier Camp",
        "eligible_biomes": ["tundra", "alpine_mountain", "boreal"],
        "sells": [("cheese", 16), ("fish", 14), ("cooked_venison", 18),
                  ("cooked_bear", 22), ("coarse_salt", 9)],
        "buys":  [("bear_pelt", 44, 4), ("fox_pelt", 28, 6), ("deer_hide", 16, 8),
                  ("fish", 14, 10)],
        "needs": [("lumber", 18), ("coal", 12)],
        "base_stock": 6, "clothing_key": "alpine",
        "building_style": "house", "half_w": 14,
    },

    "bog_apothecary": {
        "display_name":    "Bog Apothecary",
        "eligible_biomes": ["swamp", "fungal", "wetland"],
        "sells": [("green_tea", 18), ("oolong_tea", 20), ("black_tea", 22),
                  ("puerh_tea", 26), ("rare_mushroom", 30)],
        "buys":  [("tea_leaf", 6, 20), ("rare_mushroom", 36, 6), ("mushroom", 7, 15),
                  ("marsh_marigold", 6, 12)],
        "needs": [("lumber", 8), ("coal", 6)],
        "base_stock": 5, "clothing_key": "fungi_keeper",
        "building_style": "shrine", "half_w": 13,
    },
}

# Flag pennant color per outpost type (RGB)
OUTPOST_FLAG_COLORS = {
    "wine_estate":       (140,  20,  55),
    "herb_monastery":    (110,  55, 170),
    "trapper_post":      (130,  75,  35),
    "boreal_distillery": (190, 130,  20),
    "coffee_plantation": ( 90,  50,  25),
    "jungle_herbalist":  ( 50, 140,  70),
    "tea_house":         ( 50, 150, 120),
    "pottery_workshop":  (200,  90,  50),
    "spice_market":      (210, 150,  25),
    "textile_guild":     (130,  70, 190),
    "olive_press":       (110, 150,  35),
    "salt_works":        (130, 175, 210),
    "desert_glassworks": ( 90, 170, 210),
    "canyon_forge":      (150, 110,  70),
    "alpine_monastery":  (190, 200, 215),
    "cheese_cave":       (215, 195, 110),
    "fungal_grove":      (155,  70, 195),
    "swamp_alchemist":   ( 65, 130,  90),
    "fishing_outpost":   ( 50, 110, 195),
    "coastal_saltworks": (125, 180, 215),
    "nomad_camp":        (195, 170,  90),
    "spirit_distillery": (170,  90,  35),
    "hillside_vineyard": (155,  25,  45),
    "sculpture_atelier": (195, 188, 172),
    "border_garrison":   ( 55,  75, 155),
    "highland_fortress": ( 90,  90, 120),
    "desert_legion":     (195, 155,  35),
    "steppe_warcamp":    (195,  45,  45),
    "coastal_citadel":   ( 35,  55, 155),
    "timber_camp":       (110,  78,  40),
    "reed_weaver":       (160, 175, 100),
    "silk_pavilion":     (215, 175, 110),
    "incense_lodge":     (175, 105, 165),
    "glacier_camp":      (200, 220, 240),
    "bog_apothecary":    ( 95, 145,  85),
}

_MILITARY_OUTPOST_TYPES = {
    "border_garrison", "highland_fortress", "desert_legion",
    "steppe_warcamp",  "coastal_citadel",
}

# Maps each biodome to its eligible outpost types
BIOME_OUTPOST_TYPES = {
    "temperate":       ("wine_estate",        "herb_monastery",    "border_garrison",
                        "timber_camp"),
    "boreal":          ("trapper_post",        "boreal_distillery", "timber_camp",
                        "glacier_camp"),
    "birch_forest":    ("herb_monastery",      "hillside_vineyard", "border_garrison",
                        "timber_camp"),
    "jungle":          ("coffee_plantation",   "jungle_herbalist",  "silk_pavilion",
                        "incense_lodge"),
    "wetland":         ("fungal_grove",        "fishing_outpost",   "reed_weaver",
                        "bog_apothecary"),
    "redwood":         ("herb_monastery",      "trapper_post",      "timber_camp"),
    "tropical":        ("coffee_plantation",   "spice_market",      "coastal_citadel",
                        "incense_lodge",       "reed_weaver"),
    "savanna":         ("nomad_camp",          "spirit_distillery", "desert_legion"),
    "wasteland":       ("nomad_camp",          "canyon_forge",      "steppe_warcamp"),
    "fungal":          ("fungal_grove",        "swamp_alchemist",   "bog_apothecary"),
    "alpine_mountain": ("alpine_monastery",    "cheese_cave",       "highland_fortress",
                        "glacier_camp"),
    "rocky_mountain":  ("cheese_cave",         "canyon_forge",      "highland_fortress"),
    "rolling_hills":   ("hillside_vineyard",   "pottery_workshop",  "border_garrison"),
    "steep_hills":     ("hillside_vineyard",   "sculpture_atelier", "highland_fortress"),
    "steppe":          ("nomad_camp",          "spirit_distillery", "steppe_warcamp"),
    "arid_steppe":     ("nomad_camp",          "desert_glassworks", "desert_legion"),
    "desert":          ("desert_glassworks",   "canyon_forge",      "desert_legion"),
    "tundra":          ("boreal_distillery",   "alpine_monastery",  "glacier_camp"),
    "swamp":           ("swamp_alchemist",     "salt_works",        "reed_weaver",
                        "bog_apothecary"),
    "beach":           ("fishing_outpost",     "coastal_saltworks", "coastal_citadel"),
    "canyon":          ("canyon_forge",        "desert_glassworks", "highland_fortress"),
    "mediterranean":   ("olive_press",         "wine_estate",       "coastal_citadel"),
    "east_asian":      ("tea_house",           "pottery_workshop",  "silk_pavilion",
                        "incense_lodge"),
    "south_asian":     ("spice_market",        "textile_guild",     "silk_pavilion",
                        "incense_lodge"),
}

# ---------------------------------------------------------------------------
# Kingdom (region) assignment — derived deterministically from center_bx
# using the same city-slot scheme as towns: every 3 city slots form a region.
# ---------------------------------------------------------------------------

def region_id_for_bx(bx: int) -> int:
    """Region id for any world x — matches cities._city_slot_metadata.
    Slots sit at n * CITY_SPACING + CITY_SPACING//2, three slots per region.
    The nearest slot to bx has index floor(bx / CITY_SPACING)."""
    from constants import CITY_SPACING
    return (bx // CITY_SPACING) // 3


def region_for_outpost(op: "Outpost"):
    """Return the Region this outpost belongs to (or None if uncharted)."""
    from towns import REGIONS
    return REGIONS.get(region_id_for_bx(op.center_bx))

# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Outpost:
    outpost_id:        int
    outpost_type:      str
    center_bx:         int
    slot_x:            int
    biome:             str
    name:              str
    founded_day:       int
    needs:             dict   # {item_id: {"required": int, "supplied": int}}
    needs_met_days:    int
    last_resupply_day: int
    stock:             dict   # {item_id: int}  current sell inventory


# Global registry — populated by generation and restored on load
OUTPOSTS: dict[int, Outpost] = {}

# ---------------------------------------------------------------------------
# Name generation
# ---------------------------------------------------------------------------

_NAME_ADJ = {
    "alpine_mountain":  ["High", "Stone", "Peak", "Frost", "Eagle's", "Glacier", "Snowline"],
    "tundra":           ["Frost", "Ice", "Northern", "Silent", "Pale", "Hoar", "Aurora"],
    "rocky_mountain":   ["Stone", "Cliff", "Iron", "Grey", "Granite", "Rookery", "Talus"],
    "east_asian":       ["Jade", "Silk", "Lotus", "Cloud", "Bamboo", "Crane", "Mistveil"],
    "south_asian":      ["Spice", "Amber", "Coral", "Dawn", "Saffron", "Monsoon", "Sandalwood"],
    "mediterranean":    ["Sun", "Golden", "Stone", "Amber", "Olive", "Cypress", "Harbor"],
    "desert":           ["Dune", "Sand", "Hollow", "Dry", "Sun-Bleached", "Mirage", "Caravan"],
    "arid_steppe":      ["Dust", "Copper", "Arid", "Bare", "Salt-Crust", "Tumbleweed"],
    "savanna":          ["Dusty", "Red", "Open", "Pale", "Acacia", "Lion's"],
    "canyon":           ["Red", "Deep", "Canyon", "Carved", "Echo", "Sunken", "Ochre"],
    "jungle":           ["Green", "Deep", "Wild", "Vine", "Canopy", "Tigerfern", "Jaguar"],
    "tropical":         ["Azure", "Palm", "Warm", "Bright", "Lagoon", "Coral", "Trade-Wind"],
    "wetland":          ["Marsh", "Reed", "Misty", "Damp", "Heron's", "Cattail", "Fenwater"],
    "swamp":            ["Bog", "Dark", "Hollow", "Mossy", "Cypress", "Blackwater", "Mire"],
    "fungal":           ["Spore", "Mycel", "Deep", "Quiet", "Cap-Hollow", "Glowcap", "Veiled"],
    "boreal":           ["Pine", "Dark", "Cold", "Ancient", "Spruce", "Wolf-Track", "Black-Pine"],
    "birch_forest":     ["Silver", "Light", "White", "Birch", "Whitebark", "Aspen", "Goldleaf"],
    "redwood":          ["Tall", "Old", "Red", "Deep", "Giant", "Fern-Hollow", "Mossback"],
    "steppe":           ["Wind", "Flat", "Open", "Far", "Horse-Ridden", "Sky-Vault"],
    "wasteland":        ["Ashen", "Bare", "Old", "Bleak", "Cinder", "Rust", "Crag"],
    "beach":            ["Shore", "Tide", "Salt", "Sea", "Driftwood", "Foam", "Gull's"],
    "temperate":        ["Old", "Green", "Valley", "River", "Oakshire", "Three-Mill", "Greenfield"],
    "rolling_hills":    ["Hill", "Vale", "Gentle", "Broad", "Hawthorne", "Meadow", "Sheep-Run"],
    "steep_hills":      ["Ridge", "High", "Crest", "Summit", "Goat-Path", "Gable"],
}
_NAME_ADJ_DEFAULT = ["Old", "Ancient", "Hidden", "Lost", "Wild"]

# Place-noun fragments that occasionally replace the adjective for richer
# regional flavor — e.g. "Saltmarsh Reed Loom", "Whitebark Trapper's Lodge".
_NAME_PLACE = {
    "alpine_mountain":  ["Hawk's Eye", "Skystep", "Cloudpass", "Glacierhold"],
    "tundra":           ["Bone Hollow", "Wolfwind", "Polar Reach", "Driftbreak"],
    "rocky_mountain":   ["Greystone", "Iron Notch", "Stonebreak", "Talushold"],
    "east_asian":       ["Bamboo Hollow", "Crane Garden", "Jade Pavilion", "Misty Ford"],
    "south_asian":      ["Sandalwood Grove", "Saffron Bazaar", "Pearl Estuary", "Monsoon Reach"],
    "mediterranean":    ["Olive Bay", "Cypress Hill", "Sunharbor", "Goldcove"],
    "desert":           ["Caravan Crossing", "Mirage Wells", "Sandbasin", "Dunehold"],
    "arid_steppe":      ["Salt-Crust Flats", "Tumbleweed Pass", "Dustreach"],
    "savanna":          ["Acacia Reach", "Lion Plain", "Red Earth"],
    "canyon":           ["Echo Wash", "Ochre Mesa", "Sunken Bend", "Redrock"],
    "jungle":           ["Vine Hollow", "Jaguar Reach", "Tigerfern Glade", "Canopy Step"],
    "tropical":         ["Coral Lagoon", "Palm Reach", "Trade-Wind Cove"],
    "wetland":          ["Heron Marsh", "Cattail Bend", "Saltmarsh", "Fenwater"],
    "swamp":            ["Blackwater", "Cypress Bog", "Mire Hollow", "Bayou Crossing"],
    "fungal":           ["Cap Hollow", "Glowcap Glen", "Spore Garden", "Veiled Grove"],
    "boreal":           ["Black Pine", "Wolf Track", "Spruce Hollow", "Frostpine"],
    "birch_forest":     ["Whitebark", "Aspen Vale", "Goldleaf", "Silvertree"],
    "redwood":          ["Giant's Stand", "Fern Hollow", "Mossback Glade", "Old-Growth"],
    "steppe":           ["Horse Plain", "Sky Vault", "Far Reach"],
    "wasteland":        ["Cinder Reach", "Rust Hollow", "Crag's End"],
    "beach":            ["Driftwood Cove", "Gull's Reach", "Foam Bay", "Saltspit"],
    "temperate":        ["Oakshire", "Three Mills", "Greenfield", "River Bend"],
    "rolling_hills":    ["Hawthorne Vale", "Sheep Run", "Meadow Cross", "Broadhill"],
    "steep_hills":      ["Goat Path", "Gable Ridge", "Crestfall"],
}

_TYPE_SUFFIXES = {
    "wine_estate":       ["Vineyard", "Wine Estate", "Winery"],
    "herb_monastery":    ["Monastery", "Abbey", "Herb House"],
    "trapper_post":      ["Trading Post", "Trapper's Lodge", "Fur Post"],
    "boreal_distillery": ["Distillery", "Still House", "Boreal Still"],
    "coffee_plantation": ["Plantation", "Coffee Estate", "Coffee Grove"],
    "jungle_herbalist":  ["Herbalist's Grove", "Jungle Remedy", "Herb Hut"],
    "tea_house":         ["Tea House", "Tea Garden", "Teahouse"],
    "pottery_workshop":  ["Pottery Works", "Clay Studio", "Kiln House"],
    "spice_market":      ["Spice Market", "Spice Hall", "Bazaar"],
    "textile_guild":     ["Textile Guild", "Weaver's Hall", "Thread House"],
    "olive_press":       ["Olive Press", "Press House", "Olive Works"],
    "salt_works":        ["Salt Works", "Salt House", "Saltery"],
    "desert_glassworks": ["Glassworks", "Glass Forge", "Crystal Works"],
    "canyon_forge":      ["Forge", "Iron Works", "Canyon Forge"],
    "alpine_monastery":  ["Monastery", "Mountain Abbey", "High Priory"],
    "cheese_cave":       ["Cheese Cave", "Dairy Cave", "Aging House"],
    "fungal_grove":      ["Fungal Grove", "Mushroom House", "Spore Garden"],
    "swamp_alchemist":   ["Alchemist's Hut", "Marsh Lab", "Swamp Still"],
    "fishing_outpost":   ["Fishing Outpost", "Shore Station", "Fisher's Dock"],
    "coastal_saltworks": ["Salt Works", "Coastal Saltery", "Tidal Works"],
    "nomad_camp":        ["Nomad Camp", "Traveler's Rest", "Steppe Camp"],
    "spirit_distillery": ["Distillery", "Spirit Works", "Barrel House"],
    "hillside_vineyard": ["Vineyard", "Hillside Winery", "Terrace Winery"],
    "sculpture_atelier": ["Atelier", "Stone Studio", "Sculptor's Lodge"],
    "border_garrison":   ["Garrison", "Watch Post", "Border Fort", "King's Watch"],
    "highland_fortress": ["Fortress", "Citadel", "Stronghold", "Keep"],
    "desert_legion":     ["Legion Camp", "War Post", "Legion Outpost", "Sun Garrison"],
    "steppe_warcamp":    ["Warcamp", "Battle Camp", "War Band", "Horde Camp"],
    "coastal_citadel":   ["Sea Citadel", "Coastal Fort", "Harbor Guard", "Shore Keep"],
    "timber_camp":       ["Timber Camp", "Sawmill", "Lumber Yard", "Logger's Camp"],
    "reed_weaver":       ["Reed Loom", "Weaver's Hut", "Marsh Loom", "Reed Works"],
    "silk_pavilion":     ["Silk Pavilion", "Silk Garden", "Loom Pavilion", "Spool House"],
    "incense_lodge":     ["Incense Lodge", "Sandalwood Shrine", "Censer Hall", "Smoke Hermitage"],
    "glacier_camp":      ["Glacier Camp", "Ice Station", "Frost Outpost", "Cold Camp"],
    "bog_apothecary":    ["Bog Apothecary", "Marsh Steepery", "Peat Tea House", "Mire Apothecary"],
}

def _make_outpost_name(rng, otype: str, biodome: str) -> str:
    suffixes  = _TYPE_SUFFIXES.get(otype, ["Outpost"])
    place_pool = _NAME_PLACE.get(biodome)
    if place_pool and rng.random() < 0.4:
        prefix = rng.choice(place_pool)
    else:
        prefix = rng.choice(_NAME_ADJ.get(biodome, _NAME_ADJ_DEFAULT))
    return f"{prefix} {rng.choice(suffixes)}"

# ---------------------------------------------------------------------------
# RNG helpers
# ---------------------------------------------------------------------------

def _slot_rng(seed: int, slot_x: int) -> random.Random:
    return random.Random(seed + slot_x * 4481 + 99991)


def _should_spawn(seed: int, slot_x: int) -> bool:
    return _slot_rng(seed, slot_x).random() < OUTPOST_SPAWN_CHANCE


def _type_for_slot(seed: int, slot_x: int, biodome: str) -> str | None:
    types = BIOME_OUTPOST_TYPES.get(biodome)
    if not types:
        return None
    rng = _slot_rng(seed, slot_x)
    rng.random()  # skip spawn-chance roll
    return rng.choice(types)

# ---------------------------------------------------------------------------
# Palette selection (mirrors _build_single_city logic)
# ---------------------------------------------------------------------------

_DESERT_BIOMES     = {"desert", "arid_steppe", "savanna"}
_HIMALAYAN_BIOMES  = {"alpine_mountain", "tundra"}
_MEDITERR_BIOMES   = {"mediterranean"}
_EAST_ASIAN_BIOMES = {"east_asian"}
_SOUTH_ASIAN_BIOMES = {"south_asian"}

def _pick_palette(biodome: str, rng):
    from cities import (
        _DESERT_PALETTE, _HIMALAYAN_PALETTE, _EAST_ASIAN_PALETTE,
        _MEDITERRANEAN_PALETTES, _SOUTH_ASIAN_PALETTES, BUILDING_PALETTES,
    )
    if biodome in _DESERT_BIOMES:
        return _DESERT_PALETTE
    if biodome in _HIMALAYAN_BIOMES:
        return _HIMALAYAN_PALETTE
    if biodome in _MEDITERR_BIOMES:
        return rng.choice(_MEDITERRANEAN_PALETTES)
    if biodome in _EAST_ASIAN_BIOMES:
        return _EAST_ASIAN_PALETTE
    if biodome in _SOUTH_ASIAN_BIOMES:
        return rng.choice(_SOUTH_ASIAN_PALETTES)
    return rng.choice(BUILDING_PALETTES)

# ---------------------------------------------------------------------------
# Structure generation
# ---------------------------------------------------------------------------

def _place_primary(world, style: str, left_x, sy, width, height, wall, roof, biodome, rng):
    from cities import _place_house, _place_smithy, _place_shrine_for_biome
    if style == "smithy":
        _place_smithy(world, left_x, sy, width, height, wall)
    elif style == "shrine":
        _place_shrine_for_biome(world, left_x, sy, width, height, biodome)
    else:
        _place_house(world, left_x, sy, width, height, wall, roof)


def _build_outpost(world, rng, out_bx: int, otype: str, slot_x: int) -> None:
    from cities import _place_house, _place_garden_plot

    from cities import _PLANT_BLOCKS

    cfg    = OUTPOST_TYPES[otype]
    half_w = cfg["half_w"]
    biodome = world.biodome_at(out_bx)
    sy      = world.surface_y_at(out_bx)

    # Pre-load chunks with a wider buffer so flattening doesn't read stale terrain
    chunk_lo = (out_bx - half_w - 10) // CHUNK_W
    chunk_hi = (out_bx + half_w + 10) // CHUNK_W
    for ci in range(chunk_lo, chunk_hi + 1):
        world.load_chunk(ci)

    # Strip plants in/just-around the footprint before flattening (mirrors cities)
    for bx in range(out_bx - half_w - 2, out_bx + half_w + 3):
        for by in range(max(0, sy - 35), sy):
            if world.get_block(bx, by) in _PLANT_BLOCKS:
                world.set_block(bx, by, AIR)

    # Flatten terrain across the footprint to sy (mirrors _build_single_city)
    for bx in range(out_bx - half_w, out_bx + half_w + 1):
        col_sy = world.surface_y_at(bx)
        # Hill: clear solid blocks above the outpost floor
        for by in range(col_sy, sy):
            blk = world.get_block(bx, by)
            if blk not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
        # Valley: fill air below the outpost floor with stone
        for by in range(sy, col_sy + 1):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)

    # Stone floor across the full footprint
    for bx in range(out_bx - half_w, out_bx + half_w + 1):
        if world.get_block(bx, sy) != BEDROCK:
            world.set_block(bx, sy, STONE)

    # Register zone so later generation won't overlap
    world.city_zones.append((out_bx - half_w, out_bx + half_w))

    wall, roof = _pick_palette(biodome, rng)

    # Primary building left-of-centre
    bld_w  = rng.randint(5, 7)
    bld_h  = rng.randint(3, 5)
    left_x = out_bx - half_w + 2
    _place_primary(world, cfg["building_style"],
                   left_x, sy, bld_w, bld_h, wall, roof, biodome, rng)
    npc_px = (left_x + 1) * BLOCK_SIZE
    npc_py = (sy - 2) * BLOCK_SIZE

    # Flag planted to the left of the primary building, at ground level.
    flag_bx = left_x - 2
    flag_by = world.surface_y_at(flag_bx) - 1
    if 0 <= flag_by < world.height and world.get_block(flag_bx, flag_by) == AIR:
        world.set_bg_block(flag_bx, flag_by, OUTPOST_FLAG_BLOCK)

    # Secondary house right-of-centre
    bld2_w = rng.randint(4, 6)
    bld2_h = rng.randint(3, 4)
    _place_house(world, out_bx + 4, sy, bld2_w, bld2_h, wall, roof)

    # Decorative garden between the two buildings
    _place_garden_plot(world, rng, out_bx, sy, biodome, 3)

    # Build initial stock dict
    initial_stock = {item_id: cfg["base_stock"] for item_id, _ in cfg["sells"]}

    # Register Outpost record
    outpost_id = (max(OUTPOSTS.keys()) + 1) if OUTPOSTS else 0
    needs_dict = {item_id: {"required": amt, "supplied": 0}
                  for item_id, amt in cfg["needs"]}
    name = _make_outpost_name(rng, otype, biodome)
    op   = Outpost(
        outpost_id        = outpost_id,
        outpost_type      = otype,
        center_bx         = out_bx,
        slot_x            = slot_x,
        biome             = biodome,
        name              = name,
        founded_day       = getattr(world, "day_count", 0),
        needs             = needs_dict,
        needs_met_days    = 0,
        last_resupply_day = 0,
        stock             = initial_stock,
    )
    OUTPOSTS[outpost_id] = op

    from outpost_npcs import OutpostKeeperNPC, MilitarySoldierNPC, _resolve_clothing
    world.entities.append(OutpostKeeperNPC(npc_px, npc_py, world, outpost_id, otype))

    if otype in _MILITARY_OUTPOST_TYPES:
        clothing = _resolve_clothing(cfg["clothing_key"])
        soldier_positions = [
            out_bx - half_w + half_w // 3,
            out_bx,
            out_bx + half_w - half_w // 3,
        ]
        patrol_half = max(12, half_w // 3)
        for pos_bx in soldier_positions:
            sol_px = pos_bx * BLOCK_SIZE
            sol_py = (sy - 2) * BLOCK_SIZE
            world.entities.append(
                MilitarySoldierNPC(sol_px, sol_py, world, otype, clothing, patrol_half)
            )

# ---------------------------------------------------------------------------
# Chunk-streaming spawn (called from world.py alongside generate_city_for_chunk)
# ---------------------------------------------------------------------------

def generate_outpost_for_chunk(world, seed: int, cx: int) -> None:
    base_x = cx * CHUNK_W
    half   = OUTPOST_SLOT_SPACING // 2

    slot_x = None
    for bx in range(base_x, base_x + CHUNK_W):
        if ((bx % OUTPOST_SLOT_SPACING) + OUTPOST_SLOT_SPACING) % OUTPOST_SLOT_SPACING == half:
            slot_x = bx
            break
    if slot_x is None:
        return
    if not _should_spawn(seed, slot_x):
        return

    biodome = world.biodome_at(slot_x)
    otype   = _type_for_slot(seed, slot_x, biodome)
    if otype is None:
        return

    rng    = _slot_rng(seed, slot_x)
    rng.random(); rng.random()  # advance past spawn + type rolls
    jitter = rng.randint(-5, 5)
    out_bx = slot_x + jitter
    hw     = OUTPOST_TYPES[otype]["half_w"]

    # Reject if the outpost footprint would overlap any registered city/outpost zone
    op_lo, op_hi = out_bx - hw, out_bx + hw
    if any(op_hi >= lo - 5 and op_lo <= hi + 5
           for lo, hi in getattr(world, "city_zones", [])):
        return

    _build_outpost(world, rng, out_bx, otype, slot_x)


def get_outpost_for_block(bx: int, by: int) -> Outpost | None:
    """Return the Outpost whose footprint contains (bx, by), or None."""
    for op in OUTPOSTS.values():
        hw = OUTPOST_TYPES[op.outpost_type]["half_w"]
        if op.center_bx - hw - 3 <= bx <= op.center_bx + hw + 3:
            return op
    return None

# ---------------------------------------------------------------------------
# Day tick (called from world.py alongside advance_day)
# ---------------------------------------------------------------------------

def tick_outpost_day(world_day: int) -> None:
    for op in OUTPOSTS.values():
        cfg = OUTPOST_TYPES[op.outpost_type]
        all_met = all(nd["supplied"] >= nd["required"] for nd in op.needs.values())
        if all_met:
            op.needs_met_days += 1
        else:
            op.needs_met_days = 0

        # Replenish or drain stock
        base = cfg["base_stock"]
        for item_id in op.stock:
            if all_met:
                op.stock[item_id] = min(op.stock[item_id] + 1, base)
            else:
                op.stock[item_id] = max(op.stock[item_id] - 1, 0)

        # Reset supplied for the new day
        for nd in op.needs.values():
            nd["supplied"] = 0

# ---------------------------------------------------------------------------
# Init / restore on load
# ---------------------------------------------------------------------------

def init_outposts(world) -> None:
    OUTPOSTS.clear()
    if not hasattr(world, '_save_mgr') or world._save_mgr is None:
        return

    outpost_data = world._save_mgr._load_outposts()
    if not outpost_data:
        return

    from outpost_npcs import OutpostKeeperNPC, MilitarySoldierNPC, _resolve_clothing

    for d in outpost_data:
        otype = d["outpost_type"]
        if otype not in OUTPOST_TYPES:
            continue
        op = Outpost(
            outpost_id        = d["outpost_id"],
            outpost_type      = otype,
            center_bx         = d["center_bx"],
            slot_x            = d["slot_x"],
            biome             = d["biome"],
            name              = d["name"],
            founded_day       = d["founded_day"],
            needs             = d["needs"],
            needs_met_days    = d["needs_met_days"],
            last_resupply_day = d["last_resupply_day"],
            stock             = d["stock"],
        )
        OUTPOSTS[op.outpost_id] = op

        # Re-register zone so streaming generation won't overlap
        hw = OUTPOST_TYPES[otype]["half_w"]
        world.city_zones.append((op.center_bx - hw, op.center_bx + hw))

        sy     = world.surface_y_at(op.center_bx)
        npc_bx = op.center_bx - hw + 3
        npc_px = npc_bx * BLOCK_SIZE
        npc_py = (sy - 2) * BLOCK_SIZE
        world.entities.append(
            OutpostKeeperNPC(npc_px, npc_py, world, op.outpost_id, otype)
        )

        if otype in _MILITARY_OUTPOST_TYPES:
            cfg      = OUTPOST_TYPES[otype]
            clothing = _resolve_clothing(cfg["clothing_key"])
            patrol_half = max(12, hw // 3)
            for pos_bx in [op.center_bx - hw // 3, op.center_bx, op.center_bx + hw // 3]:
                world.entities.append(
                    MilitarySoldierNPC(pos_bx * BLOCK_SIZE, npc_py, world, otype, clothing, patrol_half)
                )
