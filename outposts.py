import json
import random
from dataclasses import dataclass

from constants import CHUNK_W, BLOCK_SIZE, SURFACE_Y
from blocks import (STONE, BEDROCK, AIR, OUTPOST_FLAG_BLOCK, COBBLESTONE,
                    WOOD_FENCE, BANNER_BLOCK,
                    HOUSE_WALL, HOUSE_ROOF, HOUSE_WALL_STONE,
                    BAMBOO_FENCE_JP)

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

    "scriptorium": {
        "display_name":    "Scriptorium",
        "eligible_biomes": ["temperate", "rolling_hills", "highlands", "river_delta",
                            "alpine_mountain", "rocky_mountain", "grassland"],
        "sells": [("manuscript_rare", 240), ("manuscript_fine", 90),
                  ("manuscript_common", 50),
                  ("ink_indigo", 28), ("ink_cobalt", 28), ("parchment_fine", 14)],
        "buys":  [("flax_fiber", 3, 30), ("oak_gall", 5, 15),
                  ("ink_black", 18, 8), ("parchment", 6, 20)],
        "needs": [("lumber", 25), ("leather", 8)],
        "base_stock": 5, "clothing_key": "monk",
        "building_style": "shrine", "half_w": 15, "layout": "monastery",
    },

    "tournament_grounds": {
        "display_name":    "Tournament Grounds",
        "eligible_biomes": ["temperate", "rolling_hills", "grassland", "steppe",
                            "savanna", "mediterranean"],
        "sells": [("lance_shaft", 20), ("tournament_lance_head", 35),
                  ("horse_barding", 220),
                  ("armor_jousting_helmet", 180), ("armor_jousting_chestplate", 260),
                  ("armor_jousting_leggings", 210), ("armor_jousting_boots", 140),
                  ("training_wooden_lance", 22), ("training_riding_pad", 30),
                  ("tournament_blunt_arrow", 6),
                  ("pennant_kings_lists", 38), ("pennant_pay_day", 36),
                  ("coin_champion_medallion", 28), ("coin_first_blood", 18),
                  ("coin_unhorsed_penny", 14), ("trophy_first_pass_token", 22),
                  ("victory_garland", 35), ("rite_blade", 240),
                  ("knight_dossier", 75), ("muster_horn", 95),
                  ("field_marching_tent", 110), ("field_pavilion_pole", 60),
                  ("field_lance_rack", 70), ("field_arrow_chest", 65),
                  ("medicine_battlefield_kit", 90), ("medicine_horse_liniment", 25)],
        "buys":  [("tournament_pennant", 45, 6), ("lance_shaft", 8, 10),
                  ("trophy_broken_lance", 28, 8),
                  ("trophy_splintered_shield", 30, 6),
                  ("trophy_unhorsed_stirrup", 38, 5),
                  ("trophy_grandmaster_glove", 120, 2)],
        "needs": [("lumber", 18), ("iron_chunk", 6)],
        "base_stock": 4, "clothing_key": "soldier",
        "building_style": "house", "half_w": 22, "layout": "tournament",
    },

    "horde_ordu": {
        "display_name":    "Horde Ordu",
        "eligible_biomes": ["steppe", "arid_steppe", "savanna", "wasteland", "tundra"],
        "sells": [("mongol_composite_bow", 180), ("turkish_recurve", 165),
                  ("birch_bark_quiver", 28), ("mongol_arrow", 4),
                  ("saddle_nomad", 110), ("barding_lamellar_horde", 240),
                  ("barding_tug_caparison", 130),
                  ("armor_horde_lamellar_helm", 95),
                  ("livery_horde_deel", 55), ("nine_tail_standard", 320),
                  ("horsetail_charm", 28), ("mares_milk_drum", 45),
                  ("naadam_medal", 35), ("silver_stirrup", 110),
                  ("felt_of_a_hundred_winters", 65), ("coin_horde_tug", 16),
                  ("book_horde_yasa", 260), ("map_steppe_range", 70),
                  ("training_steppe_practice_bow", 22),
                  ("standard_nine_tail", 280), ("pennant_naadam", 38),
                  ("feast_naadam_dumplings", 14), ("feast_horde_buuz", 11),
                  ("feast_aaruul_curd", 7), ("drink_kumis", 6),
                  ("drink_airag", 7), ("drink_clan_butter_tea", 5),
                  ("instrument_naadam_drum", 90), ("instrument_morin_khuur", 140),
                  ("field_ger_panels", 75), ("field_water_skin", 22)],
        "buys":  [("trophy_khan_arrow", 40, 6), ("tournament_pennant", 50, 4),
                  ("wool", 5, 30)],
        "needs": [("lumber", 10), ("leather", 8)],
        "base_stock": 5, "clothing_key": "trapper",
        "building_style": "house", "half_w": 16, "layout": "estate",
    },

    "cataphract_sun_court": {
        "display_name":    "Cataphract Sun-Court",
        "eligible_biomes": ["mediterranean", "rolling_hills", "savanna",
                            "desert", "arid_steppe"],
        "sells": [("persian_horsebow", 175), ("kontos_lance_head", 60),
                  ("saddle_cataphract", 145),
                  ("barding_gilt_peacock", 360),
                  ("barding_persepolis_chamfron", 320),
                  ("armor_cataphract_spangenhelm", 130),
                  ("livery_silk_cloak", 95), ("standard_sun_banner", 280),
                  ("sun_disc_chamfron", 140), ("peacock_feather_crest", 75),
                  ("cedar_throne_shard", 110), ("lion_pommel", 90),
                  ("klivanion_scale", 35), ("mithras_lamp", 120),
                  ("coin_cataphract_sun", 22),
                  ("book_cataphract_strategikon", 280),
                  ("pennant_nowruz", 40), ("feast_nowruz_rice", 13),
                  ("feast_persian_kebab", 16), ("feast_sun_lord_pomegranate", 8),
                  ("drink_nowruz_sharbat", 6), ("drink_persian_doogh", 5),
                  ("instrument_kettle_drum", 110),
                  ("ink_cataphract_gold", 35),
                  ("training_padded_target", 45)],
        "buys":  [("trophy_cataphract_scale", 35, 8),
                  ("tournament_pennant", 50, 4),
                  ("gold_nugget", 15, 12)],
        "needs": [("lumber", 16), ("iron_chunk", 8)],
        "base_stock": 4, "clothing_key": "scholar",
        "building_style": "house", "half_w": 20, "layout": "estate",
    },

    "bushi_dojo": {
        "display_name":    "Bushi Dojo",
        "eligible_biomes": ["east_asian", "rolling_hills", "alpine_mountain",
                            "rocky_mountain", "temperate"],
        "sells": [("yumi_longbow", 195), ("katana_blade", 80),
                  ("wakizashi_blade", 50), ("lacquered_quiver", 32),
                  ("saddle_samurai", 130),
                  ("barding_uma_yoroi", 280),
                  ("barding_samurai_horo", 165),
                  ("armor_bushi_kabuto", 140),
                  ("livery_kataginu", 55), ("livery_haori", 50),
                  ("mon_banner", 200), ("standard_mon_banner", 280),
                  ("tea_bowl_first_vassal", 85), ("sashimono", 65),
                  ("wakizashi_keepsake", 320),
                  ("lacquered_helm_keepsake", 240),
                  ("death_poem_scroll", 40), ("sageo_cord", 18),
                  ("obi_cloth", 24), ("coin_bushi_mon", 20),
                  ("book_bushi_bushido", 280), ("pennant_mon", 40),
                  ("feast_bushi_onigiri", 9), ("feast_lord_tasted_rice", 11),
                  ("feast_mochi_celebration", 8),
                  ("feast_sashimi_set", 14), ("drink_sake_temple", 7),
                  ("drink_matcha_ceremony", 6),
                  ("instrument_taiko", 130), ("instrument_shakuhachi", 95),
                  ("ink_bushi_sumi", 32),
                  ("training_bokken", 22), ("training_makiwara", 38),
                  ("training_practice_yumi", 26)],
        "buys":  [("trophy_mon_torn", 35, 6), ("tournament_pennant", 50, 4)],
        "needs": [("lumber", 14), ("iron_chunk", 5)],
        "base_stock": 5, "clothing_key": "monk",
        "building_style": "shrine", "half_w": 18, "layout": "monastery",
    },

    "furusiyya_madrasa": {
        "display_name":    "Furusiyya Madrasa",
        "eligible_biomes": ["desert", "savanna", "mediterranean", "rolling_hills",
                            "arid_steppe"],
        "sells": [("turkish_recurve", 165), ("scimitar_blade", 55),
                  ("tulwar_blade", 60), ("saffron_quiver", 30),
                  ("saddle_mamluk", 140),
                  ("barding_saffron_caparison", 175),
                  ("barding_silk_parade", 110),
                  ("barding_crusader", 200),
                  ("armor_furusiyya_turban_helm", 110),
                  ("livery_jubbah", 55), ("livery_keffiyeh", 30),
                  ("standard_crescent", 280), ("crescent_pennant_relic", 130),
                  ("madrasa_astrolabe", 145), ("prayer_rope", 25),
                  ("mamluk_brand_iron", 80), ("damascened_pommel", 105),
                  ("saffron_saddle_cloth", 60), ("crescent_seal", 70),
                  ("faris_treatise", 90), ("coin_furusiyya_dinar", 24),
                  ("book_furusiyya_treatise", 280),
                  ("book_archery_treatise", 110), ("pennant_crescent", 42),
                  ("feast_crescent_lamb", 14), ("feast_madrasa_flatbread", 7),
                  ("feast_saffron_pilaf", 11),
                  ("drink_arak_madrasa", 7), ("drink_rosewater", 5),
                  ("instrument_oud", 120),
                  ("ink_furusiyya_saffron", 32),
                  ("training_blunted_tulwar", 28),
                  ("incense_oud", 18)],
        "buys":  [("trophy_crescent_torn", 35, 6),
                  ("tournament_pennant", 50, 4),
                  ("gold_nugget", 14, 12)],
        "needs": [("lumber", 14), ("iron_chunk", 5)],
        "base_stock": 5, "clothing_key": "scholar",
        "building_style": "shrine", "half_w": 19, "layout": "monastery",
    },

    "rajput_garh": {
        "display_name":    "Rajput Garh",
        "eligible_biomes": ["south_asian", "savanna", "rolling_hills",
                            "mediterranean"],
        "sells": [("rajput_dhanush", 180), ("khanda_blade", 85),
                  ("tulwar_blade", 60), ("saddle_rajput", 135),
                  ("barding_tiger_pakhar", 270),
                  ("barding_mughal_pakhar", 245),
                  ("armor_rajput_pagri", 95),
                  ("livery_jama", 60), ("livery_angavastram", 45),
                  ("standard_saffron_banner", 280),
                  ("vermilion_paint_pot", 22), ("saffron_sash", 32),
                  ("marigold_garland", 18), ("rudraksha_rosary", 28),
                  ("tiger_claw_gauntlet", 165),
                  ("sun_disc_shield", 195), ("lotus_seal", 110),
                  ("sandalwood_charm", 26), ("coin_rajput_mohur", 26),
                  ("book_rajput_charter", 280), ("pennant_dussehra", 44),
                  ("feast_dussehra_thali", 18), ("feast_rajput_laal_maas", 17),
                  ("feast_marigold_sweet", 6), ("drink_lassi_saffron", 6),
                  ("drink_chai_masala", 5),
                  ("ink_rajput_vermilion", 32), ("incense_sandalwood", 16),
                  ("prayer_beads_rudraksha", 30)],
        "buys":  [("trophy_rajput_sash_taken", 38, 5),
                  ("tournament_pennant", 50, 4),
                  ("gold_nugget", 14, 10)],
        "needs": [("lumber", 14), ("iron_chunk", 5)],
        "base_stock": 5, "clothing_key": "scholar",
        "building_style": "house", "half_w": 20, "layout": "estate",
    },

    "wine_estate": {
        "display_name":    "Wine Estate",
        "eligible_biomes": ["temperate", "birch_forest", "redwood", "rolling_hills",
                            "mediterranean", "steppe", "arid_steppe"],
        "sells": [("red_wine", 18), ("white_wine", 16),
                  ("red_wine_fine", 40), ("white_wine_fine", 38)],
        "buys":  [("red_wine_reserve", 90, 2), ("white_wine_reserve", 85, 2)],
        "needs": [("lumber", 20), ("iron_chunk", 5)],
        "base_stock": 5, "clothing_key": "winemaker",
        "building_style": "house", "half_w": 18, "layout": "estate",
    },

    "herb_monastery": {
        "display_name":    "Herb Monastery",
        "eligible_biomes": ["temperate", "birch_forest", "rolling_hills",
                            "redwood", "alpine_mountain", "rocky_mountain"],
        "sells": [("philosophers_scroll", 28), ("votive_tablet", 22),
                  ("olive_branch", 15)],
        "buys":  [("rare_mushroom", 40, 6), ("mushroom", 8, 12)],
        "needs": [("lumber", 12), ("coal", 8)],
        "base_stock": 5, "clothing_key": "monk",
        "building_style": "shrine", "half_w": 16, "layout": "monastery",
    },

    "trapper_post": {
        "display_name":    "Trapper Post",
        "eligible_biomes": ["boreal", "tundra", "steppe", "wasteland"],
        "sells": [],
        "buys":  [("rabbit_pelt", 20, 8), ("fox_pelt", 26, 6), ("bear_pelt", 42, 3)],
        "needs": [("lumber", 15), ("iron_chunk", 5)],
        "base_stock": 6, "clothing_key": "trapper",
        "building_style": "house", "half_w": 14, "layout": "watchtower",
    },

    "boreal_distillery": {
        "display_name":    "Boreal Distillery",
        "eligible_biomes": ["boreal", "tundra", "rocky_mountain", "wasteland"],
        "sells": [("whiskey", 20), ("whiskey_aged", 45),
                  ("bourbon", 22), ("bourbon_aged", 48)],
        "buys":  [("whiskey_reserve", 95, 2), ("bourbon_reserve", 95, 2)],
        "needs": [("lumber", 25), ("coal", 10), ("iron_chunk", 8)],
        "base_stock": 4, "clothing_key": "distiller",
        "building_style": "smithy", "half_w": 15, "layout": "default",
    },

    "coffee_plantation": {
        "display_name":    "Coffee Plantation",
        "eligible_biomes": ["jungle", "tropical", "wetland", "savanna", "south_asian"],
        "sells": [("drip_coffee", 14), ("espresso", 18),
                  ("pour_over", 16)],
        "buys":  [("drip_coffee_fine", 38, 4), ("espresso_fine", 35, 4),
                  ("pour_over_fine", 35, 4)],
        "needs": [("lumber", 12), ("iron_chunk", 6)],
        "base_stock": 5, "clothing_key": "plantation_worker",
        "building_style": "house", "half_w": 16, "layout": "estate",
    },

    "jungle_herbalist": {
        "display_name":    "Jungle Herbalist",
        "eligible_biomes": ["jungle", "tropical", "wetland", "swamp"],
        "sells": [("olive_branch", 12)],
        "buys":  [("mushroom", 8, 15), ("rare_mushroom", 36, 8)],
        "needs": [("lumber", 10)],
        "base_stock": 6, "clothing_key": "jungle_healer",
        "building_style": "house", "half_w": 13, "layout": "default",
    },

    "tea_house": {
        "display_name":    "Tea House",
        "eligible_biomes": ["east_asian", "alpine_mountain", "rolling_hills"],
        "sells": [("philosophers_scroll", 25), ("votive_tablet", 20), ("olive_branch", 15)],
        "buys":  [("wine_amphora", 22, 4), ("pottery_vase", 18, 4)],
        "needs": [("lumber", 8), ("coal", 6)],
        "base_stock": 5, "clothing_key": "tea_master",
        "building_style": "shrine", "half_w": 14, "layout": "monastery",
    },

    "pottery_workshop": {
        "display_name":    "Pottery Workshop",
        "eligible_biomes": ["east_asian", "south_asian", "mediterranean", "steppe",
                            "rolling_hills"],
        "sells": [("clay_cooking_pot", 18),
                  ("pottery_vase", 22), ("wine_amphora", 28)],
        "buys":  [("clay_cooking_pot_fine", 50, 3), ("pottery_vase_fine", 58, 3),
                  ("wine_amphora_fine", 70, 2)],
        "needs": [("coal", 15), ("stone_chip", 20)],
        "base_stock": 4, "clothing_key": "potter",
        "building_style": "smithy", "half_w": 13, "layout": "default",
    },

    "spice_market": {
        "display_name":    "Spice Market",
        "eligible_biomes": ["south_asian", "tropical", "jungle", "savanna"],
        "sells": [("votive_tablet", 18)],
        "buys":  [("mushroom", 7, 15), ("rare_mushroom", 34, 8)],
        "needs": [("lumber", 8), ("coal", 5)],
        "base_stock": 6, "clothing_key": "south_asian",
        "building_style": "house", "half_w": 14, "layout": "market",
    },

    "textile_guild": {
        "display_name":    "Textile Guild",
        "eligible_biomes": ["south_asian", "east_asian", "mediterranean", "temperate"],
        "sells": [],
        "buys":  [("rabbit_pelt", 18, 10), ("fox_pelt", 22, 8)],
        "needs": [("iron_chunk", 6), ("lumber", 10)],
        "base_stock": 6, "clothing_key": "weaver",
        "building_style": "house", "half_w": 13, "layout": "market",
    },

    "olive_press": {
        "display_name":    "Olive Press",
        "eligible_biomes": ["mediterranean", "arid_steppe", "savanna"],
        "sells": [("wine_amphora", 28)],
        "buys":  [("red_wine", 20, 8), ("white_wine", 18, 8), ("red_wine_fine", 48, 4)],
        "needs": [("lumber", 18), ("stone_chip", 15)],
        "base_stock": 5, "clothing_key": "mediterranean",
        "building_style": "house", "half_w": 15, "layout": "estate",
    },

    "salt_works": {
        "display_name":    "Salt Works",
        "eligible_biomes": ["mediterranean", "beach", "wetland", "swamp"],
        "sells": [("fine_salt", 12)],
        "buys":  [("coarse_salt", 10, 10)],
        "needs": [("coal", 12), ("iron_chunk", 5)],
        "base_stock": 7, "clothing_key": "saltworker",
        "building_style": "smithy", "half_w": 12, "layout": "default",
    },

    "desert_glassworks": {
        "display_name":    "Desert Glassworks",
        "eligible_biomes": ["desert", "arid_steppe", "canyon"],
        "sells": [],
        "buys":  [("crystal_shard", 20, 8), ("obsidian_slab", 30, 5),
                  ("stone_chip", 3, 20)],
        "needs": [("coal", 20), ("iron_chunk", 8)],
        "base_stock": 5, "clothing_key": "desert",
        "building_style": "smithy", "half_w": 14, "layout": "default",
    },

    "canyon_forge": {
        "display_name":    "Canyon Forge",
        "eligible_biomes": ["canyon", "rocky_mountain", "desert", "wasteland"],
        "sells": [("iron_bar", 20), ("tempered_iron", 58)],
        "buys":  [("iron_chunk", 5, 15), ("gold_nugget", 12, 8)],
        "needs": [("coal", 25), ("iron_chunk", 10)],
        "base_stock": 4, "clothing_key": "blacksmith",
        "building_style": "smithy", "half_w": 13, "layout": "underground",
    },

    "alpine_monastery": {
        "display_name":    "Alpine Monastery",
        "eligible_biomes": ["alpine_mountain", "rocky_mountain", "tundra"],
        "sells": [("philosophers_scroll", 28), ("votive_tablet", 22),
                  ("olive_branch", 15)],
        "buys":  [("rare_mushroom", 40, 6), ("mushroom", 8, 10)],
        "needs": [("lumber", 12), ("coal", 8)],
        "base_stock": 5, "clothing_key": "monk",
        "building_style": "shrine", "half_w": 16, "layout": "monastery",
    },

    "cheese_cave": {
        "display_name":    "Cheese Cave",
        "eligible_biomes": ["alpine_mountain", "rocky_mountain", "rolling_hills", "boreal"],
        "sells": [],
        "buys":  [("cheese", 18, 8)],
        "needs": [("lumber", 10), ("iron_chunk", 6), ("coarse_salt", 8)],
        "base_stock": 7, "clothing_key": "alpine",
        "building_style": "house", "half_w": 13, "layout": "underground",
    },

    "fungal_grove": {
        "display_name":    "Fungal Grove",
        "eligible_biomes": ["swamp", "wetland"],
        "sells": [],
        "buys":  [("mushroom", 7, 20), ("rare_mushroom", 35, 8)],
        "needs": [("lumber", 10)],
        "base_stock": 7, "clothing_key": "fungi_keeper",
        "building_style": "house", "half_w": 12, "layout": "default",
    },

    "swamp_alchemist": {
        "display_name":    "Swamp Alchemist",
        "eligible_biomes": ["swamp", "wetland"],
        "sells": [("philosophers_scroll", 24), ("votive_tablet", 18)],
        "buys":  [("mushroom", 7, 12), ("rare_mushroom", 36, 8)],
        "needs": [("coal", 10), ("iron_chunk", 4)],
        "base_stock": 5, "clothing_key": "alchemist",
        "building_style": "smithy", "half_w": 12, "layout": "default",
    },

    "fishing_outpost": {
        "display_name":    "Fishing Outpost",
        "eligible_biomes": ["beach", "wetland", "tropical"],
        "sells": [("bread", 8), ("cooked_beef", 14)],
        "buys":  [("fish", 15, 8)],
        "needs": [("lumber", 15), ("iron_chunk", 5)],
        "base_stock": 6, "clothing_key": "coastal",
        "building_style": "house", "half_w": 13, "layout": "default",
    },

    "coastal_saltworks": {
        "display_name":    "Coastal Salt Works",
        "eligible_biomes": ["beach", "mediterranean", "tropical"],
        "sells": [("fine_salt", 10)],
        "buys":  [("coarse_salt", 9, 12)],
        "needs": [("lumber", 10), ("stone_chip", 10)],
        "base_stock": 7, "clothing_key": "saltworker",
        "building_style": "house", "half_w": 12, "layout": "default",
    },

    "nomad_camp": {
        "display_name":    "Nomad Camp",
        "eligible_biomes": ["steppe", "arid_steppe", "savanna", "wasteland"],
        "sells": [("cooked_beef", 12)],
        "buys":  [("rabbit_pelt", 18, 10), ("fox_pelt", 22, 8), ("bear_pelt", 38, 3)],
        "needs": [("coal", 10), ("iron_chunk", 8)],
        "base_stock": 6, "clothing_key": "steppe_nomad",
        "building_style": "house", "half_w": 14, "layout": "warcamp",
    },

    "craft_brewery": {
        "display_name":    "Craft Brewery",
        "eligible_biomes": ["rolling_hills", "temperate", "canyon", "alpine_mountain",
                            "steep_hills", "birch_forest"],
        "sells": [("ale", 18), ("stout", 22), ("ipa", 24), ("porter", 20)],
        "buys":  [("ale_reserve", 72, 2), ("stout_reserve", 78, 2),
                  ("ipa_reserve", 88, 2), ("porter_reserve", 78, 2)],
        "needs": [("lumber", 20), ("coal", 8), ("iron_chunk", 6)],
        "base_stock": 4, "clothing_key": "distiller",
        "building_style": "smithy", "half_w": 15, "layout": "default",
    },

    "hill_taproom": {
        "display_name":    "Hill Taproom",
        "eligible_biomes": ["tropical", "savanna", "beach", "wetland", "swamp",
                            "jungle", "south_asian"],
        "sells": [("lager", 16), ("wheat_beer", 18), ("saison", 20), ("pilsner", 16)],
        "buys":  [("lager_reserve", 62, 2), ("wheat_beer_reserve", 70, 2),
                  ("saison_reserve", 82, 2)],
        "needs": [("lumber", 15), ("coal", 6), ("iron_chunk", 5)],
        "base_stock": 5, "clothing_key": "winemaker",
        "building_style": "house", "half_w": 14, "layout": "estate",
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
        "building_style": "smithy", "half_w": 15, "layout": "default",
    },

    "hillside_vineyard": {
        "display_name":    "Hillside Vineyard",
        "eligible_biomes": ["rolling_hills", "steep_hills", "temperate", "mediterranean"],
        "sells": [("red_wine", 16), ("white_wine", 15), ("red_wine_fine", 38)],
        "buys":  [("red_wine_reserve", 92, 2), ("white_wine_reserve", 88, 2)],
        "needs": [("lumber", 15), ("iron_chunk", 5)],
        "base_stock": 5, "clothing_key": "winemaker",
        "building_style": "house", "half_w": 16, "layout": "estate",
    },

    "sculpture_atelier": {
        "display_name":    "Sculpture Atelier",
        "eligible_biomes": ["steep_hills", "rocky_mountain", "canyon",
                            "mediterranean", "east_asian"],
        "sells": [("votive_tablet", 20)],
        "buys":  [("stone_chip", 4, 20), ("crystal_shard", 18, 8)],
        "needs": [("iron_chunk", 8), ("coal", 5)],
        "base_stock": 5, "clothing_key": "artisan",
        "building_style": "smithy", "half_w": 13, "layout": "default",
    },

    # --- Military outposts ---

    "border_garrison": {
        "display_name":    "Border Garrison",
        "eligible_biomes": ["temperate", "rolling_hills", "steep_hills", "birch_forest"],
        "sells": [("recurve_bow", 25), ("flint_arrow", 5), ("iron_bar", 22)],
        "buys":  [("iron_chunk", 6, 15), ("lumber", 3, 20), ("coal", 4, 12),
                  ("iron_arrow", 5, 20), ("wood_arrow", 2, 30)],
        "needs": [("iron_chunk", 10), ("coal", 15)],
        "base_stock": 4, "clothing_key": "soldier",
        "building_style": "smithy", "half_w": 16, "layout": "military_fort",
    },

    "highland_fortress": {
        "display_name":    "Highland Fortress",
        "eligible_biomes": ["rocky_mountain", "alpine_mountain", "steep_hills", "canyon"],
        "sells": [("longbow", 55), ("tempered_iron", 60)],
        "buys":  [("iron_chunk", 6, 15), ("coal", 4, 15), ("stone_chip", 3, 20),
                  ("broadhead_arrow", 10, 15), ("iron_arrow", 5, 15)],
        "needs": [("iron_chunk", 12), ("coal", 20)],
        "base_stock": 3, "clothing_key": "fortress_guard",
        "building_style": "smithy", "half_w": 18, "layout": "military_fort",
    },

    "desert_legion": {
        "display_name":    "Desert Legion",
        "eligible_biomes": ["desert", "arid_steppe", "canyon", "savanna"],
        "sells": [("crossbow", 80), ("composite_bow", 45), ("iron_bar", 22)],
        "buys":  [("iron_chunk", 6, 15), ("gold_nugget", 10, 5), ("coal", 4, 12),
                  ("iron_arrow", 5, 15), ("flint_arrow", 4, 20)],
        "needs": [("iron_chunk", 12), ("coal", 18)],
        "base_stock": 3, "clothing_key": "legion",
        "building_style": "smithy", "half_w": 17, "layout": "military_fort",
    },

    "steppe_warcamp": {
        "display_name":    "Steppe Warcamp",
        "eligible_biomes": ["steppe", "wasteland", "savanna", "arid_steppe"],
        "sells": [("composite_bow", 40)],
        "buys":  [("rabbit_pelt", 16, 10), ("wolf_pelt", 28, 6), ("iron_chunk", 6, 10),
                  ("wood_arrow", 3, 25), ("flint_arrow", 4, 20)],
        "needs": [("lumber", 15), ("coal", 8)],
        "base_stock": 5, "clothing_key": "warlord",
        "building_style": "house", "half_w": 15, "layout": "warcamp",
    },

    "coastal_citadel": {
        "display_name":    "Coastal Citadel",
        "eligible_biomes": ["beach", "mediterranean", "tropical"],
        "sells": [("iron_bar", 20), ("wood_bow", 14)],
        "buys":  [("lumber", 3, 20), ("iron_chunk", 6, 15), ("coal", 4, 10),
                  ("recurve_bow", 18, 3), ("iron_arrow", 5, 20)],
        "needs": [("lumber", 20), ("iron_chunk", 10)],
        "base_stock": 4, "clothing_key": "naval_guard",
        "building_style": "smithy", "half_w": 16, "layout": "military_fort",
    },

    # --- Region-flavored outposts ---

    "timber_camp": {
        "display_name":    "Timber Camp",
        "eligible_biomes": ["redwood", "boreal", "birch_forest", "temperate"],
        "sells": [("wood_arrow", 3), ("wood_bow", 14)],
        "buys":  [("lumber", 5, 25), ("sapling", 4, 15), ("elk_antler", 12, 6),
                  ("deer_hide", 14, 8)],
        "needs": [("iron_chunk", 8), ("coal", 6)],
        "base_stock": 8, "clothing_key": "lumberjack",
        "building_style": "smithy", "half_w": 15, "layout": "warcamp",
    },

    "reed_weaver": {
        "display_name":    "Reed Weaver",
        "eligible_biomes": ["wetland", "swamp", "tropical"],
        "sells": [("woven_rug", 22), ("textile_rug_natural", 26),
                  ("linen_fold", 18)],
        "buys":  [("reed_bundle", 7, 20), ("cattail", 5, 15), ("bulrush", 5, 15),
                  ("sedge", 4, 20), ("horsetail", 4, 15)],
        "needs": [("lumber", 10), ("iron_chunk", 4)],
        "base_stock": 6, "clothing_key": "weaver",
        "building_style": "house", "half_w": 13, "layout": "default",
    },

    "silk_pavilion": {
        "display_name":    "Silk Pavilion",
        "eligible_biomes": ["east_asian", "south_asian", "jungle", "tropical"],
        "sells": [("textile_rug_amber", 32), ("textile_tapestry_amber", 38),
                  ("andean_textile", 28)],
        "buys":  [("wool", 5, 20), ("golden_wool", 18, 8), ("cotton_fiber", 7, 20)],
        "needs": [("lumber", 10), ("coal", 6)],
        "base_stock": 5, "clothing_key": "silk_master",
        "building_style": "house", "half_w": 14, "layout": "market",
    },

    "creamery": {
        "display_name":    "Creamery",
        "eligible_biomes": ["temperate", "rolling_hills", "birch_forest",
                            "grassland", "river_delta"],
        "sells": [("cheese", 16), ("bread", 8)],
        "buys":  [("milk", 6, 25), ("sheep_milk", 8, 20), ("goat_milk", 8, 20),
                  ("egg", 5, 30), ("golden_milk", 32, 6), ("golden_egg", 36, 6)],
        "needs": [("lumber", 12), ("coarse_salt", 6)],
        "base_stock": 5, "clothing_key": "weaver",
        "building_style": "house", "half_w": 13, "layout": "default",
    },

    "carders_cottage": {
        "display_name":    "Carders' Cottage",
        "eligible_biomes": ["rolling_hills", "temperate", "alpine_mountain",
                            "steep_hills", "boreal", "tundra", "birch_forest"],
        "sells": [("textile_cloth", 22), ("dye_extract_ivory", 16),
                  ("dye_extract_ochre", 18)],
        "buys":  [("wool", 6, 25), ("golden_wool", 22, 8),
                  ("cashmere_fiber", 14, 12), ("sheep_droppings", 2, 20)],
        "needs": [("lumber", 10), ("coal", 4)],
        "base_stock": 5, "clothing_key": "weaver",
        "building_style": "house", "half_w": 12, "layout": "default",
    },

    "smokehouse": {
        "display_name":    "Smokehouse",
        "eligible_biomes": ["temperate", "rolling_hills", "boreal",
                            "redwood", "birch_forest", "grassland"],
        "sells": [("salt_cured_beef", 28), ("salt_cured_mutton", 24),
                  ("lardo", 22), ("cooked_beef", 14)],
        "buys":  [("raw_pork", 7, 20), ("lard", 9, 15),
                  ("raw_mutton", 7, 20), ("raw_beef", 8, 20),
                  ("raw_chicken", 6, 25)],
        "needs": [("lumber", 14), ("coarse_salt", 10), ("coal", 8)],
        "base_stock": 5, "clothing_key": "trapper",
        "building_style": "house", "half_w": 13, "layout": "default",
    },

    "rug_merchant": {
        "display_name":    "Rug Merchant",
        "eligible_biomes": ["south_asian", "east_asian", "mediterranean",
                            "arid_steppe", "desert"],
        "sells": [("dye_extract_crimson", 22), ("dye_extract_indigo", 22),
                  ("dye_extract_amber", 18)],
        "buys":  [("textile_cloth", 18, 12),
                  ("textile_rug_amber", 28, 6), ("textile_rug_crimson", 28, 6),
                  ("textile_tapestry_amber", 34, 4),
                  ("textile_tapestry_crimson", 34, 4),
                  ("andean_textile", 24, 8)],
        "needs": [("lumber", 8), ("coal", 4)],
        "base_stock": 5, "clothing_key": "silk_master",
        "building_style": "house", "half_w": 14, "layout": "market",
    },

    "highland_dairy": {
        "display_name":    "Highland Dairy",
        "eligible_biomes": ["alpine_mountain", "rocky_mountain", "steep_hills",
                            "tundra", "boreal"],
        "sells": [("cheese_cured_fine", 38), ("cheese", 16), ("coarse_salt", 9)],
        "buys":  [("milk", 7, 25), ("sheep_milk", 9, 20), ("goat_milk", 9, 20),
                  ("cheese", 14, 12), ("golden_milk", 36, 6)],
        "needs": [("lumber", 12), ("coal", 6), ("coarse_salt", 6)],
        "base_stock": 5, "clothing_key": "alpine",
        "building_style": "house", "half_w": 13, "layout": "default",
    },

    "charcuterie_house": {
        "display_name":    "Charcuterie House",
        "eligible_biomes": ["mediterranean", "rolling_hills", "temperate",
                            "birch_forest", "rocky_mountain"],
        "sells": [("cheese_cured_superior", 60), ("salt_cured_venison", 36),
                  ("dye_extract_amber", 18)],
        "buys":  [("salt_cured_beef", 34, 6), ("salt_cured_mutton", 30, 6),
                  ("lardo", 26, 8), ("lardo_fine", 38, 5),
                  ("lardo_superior", 52, 3),
                  ("cheese_cured_fine", 30, 6),
                  ("cheese_cured_superior", 48, 4),
                  ("cooked_beef", 16, 10), ("cooked_mutton", 14, 10),
                  ("cooked_pork", 16, 10), ("cooked_chicken", 12, 12)],
        "needs": [("lumber", 12), ("coarse_salt", 10)],
        "base_stock": 6, "clothing_key": "mediterranean",
        "building_style": "house", "half_w": 14, "layout": "market",
    },

    "compost_yard": {
        "display_name":    "Compost Yard",
        "eligible_biomes": ["rolling_hills", "temperate", "river_delta",
                            "grassland", "birch_forest", "wetland"],
        "sells": [("bread", 8)],
        "buys":  [("cow_manure", 3, 30), ("pig_manure", 3, 30),
                  ("sheep_droppings", 3, 30)],
        "needs": [("lumber", 8)],
        "base_stock": 3, "clothing_key": "lumberjack",
        "building_style": "house", "half_w": 11, "layout": "default",
    },

    "carpet_caravan": {
        "display_name":    "Carpet Caravan",
        "eligible_biomes": ["south_asian", "east_asian", "arid_steppe",
                            "desert", "mediterranean", "savanna"],
        "sells": [("dye_extract_violet", 22), ("dye_extract_verdant", 20),
                  ("dye_extract_cobalt", 22), ("dye_extract_rose", 20)],
        "buys":  [("textile_rug_natural",  22, 6), ("textile_rug_golden",  26, 6),
                  ("textile_rug_rose",     26, 6), ("textile_rug_cobalt",  26, 6),
                  ("textile_rug_violet",   28, 6), ("textile_rug_verdant", 26, 6),
                  ("textile_rug_ivory",    24, 6),
                  ("textile_tapestry_natural",  28, 4),
                  ("textile_tapestry_golden",   32, 4),
                  ("textile_tapestry_rose",     32, 4),
                  ("textile_tapestry_cobalt",   32, 4),
                  ("textile_tapestry_violet",   34, 4),
                  ("textile_tapestry_verdant",  32, 4),
                  ("textile_tapestry_ivory",    30, 4)],
        "needs": [("lumber", 8), ("coal", 4)],
        "base_stock": 5, "clothing_key": "steppe_nomad",
        "building_style": "house", "half_w": 14, "layout": "market",
    },

    "incense_lodge": {
        "display_name":    "Incense Lodge",
        "eligible_biomes": ["south_asian", "tropical", "jungle", "east_asian"],
        "sells": [("votive_tablet", 22), ("philosophers_scroll", 28)],
        "buys":  [("lotus_petal", 8, 15), ("water_iris", 6, 15), ("marsh_marigold", 6, 15),
                  ("dye_extract_amber", 18, 6), ("dye_extract_violet", 20, 6)],
        "needs": [("lumber", 8), ("coal", 5)],
        "base_stock": 5, "clothing_key": "south_asian",
        "building_style": "shrine", "half_w": 14, "layout": "monastery",
    },

    "glacier_camp": {
        "display_name":    "Glacier Camp",
        "eligible_biomes": ["tundra", "alpine_mountain", "boreal"],
        "sells": [("cheese", 16), ("cooked_venison", 18),
                  ("cooked_bear", 22), ("coarse_salt", 9)],
        "buys":  [("bear_pelt", 44, 4), ("fox_pelt", 28, 6), ("deer_hide", 16, 8),
                  ("fish", 14, 10)],
        "needs": [("lumber", 18), ("coal", 12)],
        "base_stock": 6, "clothing_key": "alpine",
        "building_style": "house", "half_w": 14, "layout": "warcamp",
    },

    "bog_apothecary": {
        "display_name":    "Bog Apothecary",
        "eligible_biomes": ["swamp", "wetland"],
        "sells": [("green_tea", 18), ("oolong_tea", 20), ("black_tea", 22),
                  ("puerh_tea", 26)],
        "buys":  [("tea_leaf", 6, 20), ("rare_mushroom", 36, 6), ("mushroom", 7, 15),
                  ("marsh_marigold", 6, 12)],
        "needs": [("lumber", 8), ("coal", 6)],
        "base_stock": 5, "clothing_key": "fungi_keeper",
        "building_style": "shrine", "half_w": 13, "layout": "default",
    },

    "pearl_diving_camp": {
        "display_name":    "Pearl Diving Camp",
        "eligible_biomes": ["pacific_island", "beach", "ocean"],
        "sells": [("pearl_necklace", 45), ("raw_pearl", 22), ("shell_ornament", 15)],
        "buys":  [("raw_pearl", 35, 8), ("shell_fragment", 5, 20), ("coral", 12, 10)],
        "needs": [("lumber", 8), ("coal", 4)],
        "base_stock": 5, "clothing_key": "polynesian",
        "building_style": "house", "half_w": 14, "layout": "market",
    },

    "canoe_trading_post": {
        "display_name":    "Canoe Trading Post",
        "eligible_biomes": ["pacific_island", "beach"],
        "sells": [("coconut_oil", 18), ("tapa_cloth", 22), ("tropical_spice", 30)],
        "buys":  [("iron_chunk", 20, 6), ("wheat", 5, 15), ("red_wine", 12, 8)],
        "needs": [("lumber", 10), ("coal", 5)],
        "base_stock": 5, "clothing_key": "polynesian",
        "building_style": "market_stall", "half_w": 14, "layout": "market",
    },

    "polynesian_shrine_outpost": {
        "display_name":    "Island Shrine",
        "eligible_biomes": ["pacific_island"],
        "sells": [("carved_idol", 55), ("bone_fishhook", 20), ("navigation_chart", 40)],
        "buys":  [("rare_fish", 35, 6), ("mint_leaves", 8, 12), ("obsidian_chunk", 22, 4)],
        "needs": [("lumber", 6), ("coal", 4)],
        "base_stock": 4, "clothing_key": "polynesian",
        "building_style": "shrine", "half_w": 12, "layout": "default",
    },

    "mountain_lodge": {
        "display_name":    "Mountain Lodge",
        "eligible_biomes": ["alpine_mountain", "rocky_mountain", "steep_hills", "rolling_hills"],
        "sells": [("dried_edelweiss", 22), ("dried_yarrow", 14), ("dried_lavender", 12), ("dried_chamomile", 10)],
        "buys":  [("mica_schist", 38, 4), ("hornfels", 30, 4), ("gneiss", 25, 4),
                  ("edelweiss", 10, 8), ("yarrow", 6, 12)],
        "needs": [("lumber", 15), ("coal", 6)],
        "base_stock": 4, "clothing_key": "ranger",
        "building_style": "house", "half_w": 16, "layout": "default",
    },

    "apiary": {
        "display_name":    "Apiary",
        "eligible_biomes": ["temperate", "rolling_hills", "birch_forest", "meadow",
                            "tropical", "jungle", "alpine_mountain"],
        "sells": [("beeswax", 12), ("honeycomb_raw", 10), ("mead", 28)],
        "buys":  [("honey_jar", 22, 8), ("honey_jar_fine", 48, 4),
                  ("honey_jar_artisan", 90, 2), ("mead_fine", 55, 3)],
        "needs": [("lumber", 12), ("wildflower", 10)],
        "base_stock": 5, "clothing_key": "beekeeper",
        "building_style": "house", "half_w": 14, "layout": "default",
    },

    "deep_mine_camp": {
        "display_name":    "Deep Mine Camp",
        "eligible_biomes": ["rocky_mountain", "alpine_mountain", "canyon",
                            "steep_hills", "wasteland"],
        "sells": [("iron_pickaxe", 90), ("tempered_pickaxe", 220),
                  ("torch", 4), ("mining_potion", 55),
                  ("mining_post_item", 140), ("coal_miner_item", 320)],
        "buys":  [("coal", 5, 30), ("iron_chunk", 9, 20),
                  ("raw_galena", 14, 10), ("raw_hematite", 16, 10),
                  ("raw_copper_ore", 14, 10), ("raw_cobalt_ore", 28, 6)],
        "needs": [("lumber", 25), ("coal", 12), ("iron_chunk", 6)],
        "base_stock": 5, "clothing_key": "blacksmith",
        "building_style": "smithy", "half_w": 16, "layout": "default",
    },

    "quarry_camp": {
        "display_name":    "Quarry Camp",
        "eligible_biomes": ["rocky_mountain", "canyon", "steep_hills",
                            "rolling_hills", "wasteland", "arid_steppe"],
        "sells": [("stone_pickaxe", 25), ("iron_pickaxe", 95),
                  ("rough_stone_wall", 6), ("torch", 4)],
        "buys":  [("hornfels", 28, 6), ("gneiss", 22, 6),
                  ("mica_schist", 36, 4), ("raw_ochre", 10, 12),
                  ("raw_umber", 10, 12), ("raw_sienna", 10, 12)],
        "needs": [("lumber", 18), ("iron_chunk", 4)],
        "base_stock": 6, "clothing_key": "blacksmith",
        "building_style": "smithy", "half_w": 15, "layout": "default",
    },

    "prospector_post": {
        "display_name":    "Prospector Post",
        "eligible_biomes": ["canyon", "wasteland", "arid_steppe", "desert",
                            "rocky_mountain", "steep_hills"],
        "sells": [("stone_pickaxe", 22), ("torch", 4),
                  ("mining_potion", 55), ("mining_potion_fine", 110)],
        "buys":  [("raw_lapis", 32, 6), ("raw_azurite", 30, 6),
                  ("raw_malachite", 26, 6), ("raw_cinnabar", 36, 4),
                  ("raw_realgar", 30, 4), ("raw_chrome_ore", 28, 6),
                  ("raw_antimony", 24, 6)],
        "needs": [("lumber", 12), ("coal", 8)],
        "base_stock": 5, "clothing_key": "trapper",
        "building_style": "house", "half_w": 13, "layout": "default",
    },

    "lapidary_atelier": {
        "display_name":    "Lapidary Atelier",
        "eligible_biomes": ["rocky_mountain", "alpine_mountain", "canyon",
                            "mediterranean", "east_asian", "steep_hills"],
        "sells": [("gem_cutter_item", 240), ("cut_crystal", 65),
                  ("ruby_dust", 30), ("amethyst_dust", 28),
                  ("topaz_dust", 26), ("sapphire_dust", 30)],
        "buys":  [("ruby", 110, 4), ("amethyst_gem", 85, 4),
                  ("diamond", 180, 2), ("obsidian_slab", 28, 8),
                  ("cut_crystal", 35, 4), ("gold_nugget", 45, 6)],
        "needs": [("lumber", 14), ("coal", 10), ("iron_chunk", 4)],
        "base_stock": 4, "clothing_key": "artisan",
        "building_style": "shrine", "half_w": 14, "layout": "default",
    },

    "coal_pit": {
        "display_name":    "Coal Pit",
        "eligible_biomes": ["boreal", "wasteland", "redwood", "rocky_mountain",
                            "steep_hills", "tundra"],
        "sells": [("torch", 3), ("coal", 8), ("iron_chunk", 12),
                  ("stone_pickaxe", 24)],
        "buys":  [("coal", 4, 60), ("raw_coal_dust", 6, 30),
                  ("raw_lignite", 8, 20), ("iron_chunk", 8, 25)],
        "needs": [("lumber", 30), ("iron_chunk", 5)],
        "base_stock": 8, "clothing_key": "blacksmith",
        "building_style": "smithy", "half_w": 14, "layout": "default",
    },

    "marble_quarry": {
        "display_name":    "Marble Quarry",
        "eligible_biomes": ["mediterranean", "rolling_hills", "steep_hills",
                            "canyon", "rocky_mountain", "east_asian"],
        "sells": [("limestone_block", 6), ("granite_slab", 7),
                  ("marble_chunk", 12), ("slate_tile", 5),
                  ("rough_stone_wall", 6), ("chisel", 35)],
        "buys":  [("marble_chunk", 9, 20), ("slate_chunk", 7, 20),
                  ("limestone_chip", 4, 30), ("granite_slab", 5, 20),
                  ("hornfels", 22, 6)],
        "needs": [("lumber", 22), ("iron_chunk", 6)],
        "base_stock": 7, "clothing_key": "mediterranean",
        "building_style": "shrine", "half_w": 17, "layout": "default",
    },

    "dwarven_hold": {
        "display_name":    "Dwarven Hold",
        "eligible_biomes": ["alpine_mountain", "rocky_mountain", "canyon"],
        "sells": [("gold_pickaxe", 320), ("tempered_pickaxe", 240),
                  ("mining_elixir", 280), ("obsidian_slab", 65),
                  ("ruby", 140), ("amethyst_gem", 110)],
        "buys":  [("gold_nugget", 55, 12), ("obsidian_slab", 32, 8),
                  ("iron_chunk", 11, 40), ("ruby", 95, 4),
                  ("diamond", 165, 2), ("marble_chunk", 14, 10)],
        "needs": [("lumber", 28), ("coal", 15), ("iron_chunk", 10)],
        "base_stock": 4, "clothing_key": "blacksmith",
        "building_style": "smithy", "half_w": 18, "layout": "estate",
        "spawn_chance_mult": 0.4,
    },

    "sulfur_pit": {
        "display_name":    "Sulfur Pit",
        "eligible_biomes": ["wasteland", "canyon", "arid_steppe", "desert"],
        "sells": [("torch", 3), ("mining_potion_fine", 105),
                  ("coal", 7), ("iron_pickaxe", 95)],
        "buys":  [("raw_realgar", 38, 6), ("raw_cinnabar", 42, 4),
                  ("raw_antimony", 30, 6), ("raw_coal_dust", 9, 20),
                  ("coal", 6, 25)],
        "needs": [("lumber", 14), ("iron_chunk", 5)],
        "base_stock": 5, "clothing_key": "alchemist",
        "building_style": "smithy", "half_w": 13, "layout": "default",
        "spawn_chance_mult": 0.7,
    },

    "gold_panning_camp": {
        "display_name":    "Gold Panning Camp",
        "eligible_biomes": ["wetland", "jungle", "tropical", "swamp", "savanna"],
        "sells": [("stone_pickaxe", 24), ("torch", 4), ("clay", 3),
                  ("mining_potion", 55)],
        "buys":  [("gold_nugget", 58, 10), ("raw_ochre", 11, 15),
                  ("raw_sienna", 11, 15), ("raw_umber", 11, 15),
                  ("clay", 2, 40)],
        "needs": [("lumber", 12), ("coal", 5)],
        "base_stock": 6, "clothing_key": "trapper",
        "building_style": "house", "half_w": 13, "layout": "default",
    },
}

# Flag pennant color per outpost type (RGB)
OUTPOST_FLAG_COLORS = {
    "scriptorium":       (175, 135,  70),
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
    "glacier_camp":           (200, 220, 240),
    "bog_apothecary":         ( 95, 145,  85),
    "pearl_diving_camp":      ( 70, 180, 210),
    "canoe_trading_post":     (200, 130,  50),
    "polynesian_shrine_outpost": (120, 80, 160),
    "mountain_lodge":            (100, 120, 155),
    "apiary":                    (210, 175,  55),
    "deep_mine_camp":            ( 75,  70,  78),
    "quarry_camp":               (160, 150, 135),
    "prospector_post":           (175, 130,  55),
    "lapidary_atelier":          (180,  80, 180),
    "coal_pit":                  ( 40,  38,  42),
    "marble_quarry":             (230, 226, 218),
    "dwarven_hold":              (135,  85,  35),
    "sulfur_pit":                (215, 195,  45),
    "gold_panning_camp":         (220, 185,  70),
    "horde_ordu":                (130,  95,  55),
    "cataphract_sun_court":      (235, 200,  85),
    "bushi_dojo":                ( 35,  35,  45),
    "furusiyya_madrasa":         (220, 175,  60),
    "rajput_garh":               (210,  55,  70),
    "creamery":                  (245, 240, 220),
    "carders_cottage":           (220, 200, 175),
    "smokehouse":                (140,  90,  70),
    "rug_merchant":              (180,  90, 160),
    "highland_dairy":            (230, 235, 245),
    "charcuterie_house":         (170,  85,  75),
    "compost_yard":              (105,  80,  50),
    "carpet_caravan":            (200, 120, 180),
}

_MILITARY_OUTPOST_TYPES = {
    "border_garrison", "highland_fortress", "desert_legion",
    "steppe_warcamp",  "coastal_citadel",
}

# Maps each biodome to its eligible outpost types
BIOME_OUTPOST_TYPES = {
    "temperate":       ("wine_estate",        "herb_monastery",    "border_garrison",
                        "timber_camp",         "apiary",            "scriptorium",
                        "tournament_grounds",  "tournament_grounds",
                        "creamery",            "smokehouse",        "carders_cottage",
                        "charcuterie_house",   "compost_yard"),
    "boreal":          ("trapper_post",        "boreal_distillery", "timber_camp",
                        "glacier_camp",        "coal_pit",
                        "smokehouse",          "carders_cottage",
                        "highland_dairy"),
    "birch_forest":    ("herb_monastery",      "hillside_vineyard", "border_garrison",
                        "timber_camp",         "apiary",
                        "creamery",            "smokehouse",        "carders_cottage",
                        "charcuterie_house",   "compost_yard"),
    "jungle":          ("coffee_plantation",   "jungle_herbalist",  "silk_pavilion",
                        "incense_lodge",       "apiary",            "gold_panning_camp"),
    "wetland":         ("fungal_grove",        "fishing_outpost",   "reed_weaver",
                        "bog_apothecary",      "gold_panning_camp",
                        "compost_yard"),
    "redwood":         ("herb_monastery",      "trapper_post",      "timber_camp",
                        "coal_pit",            "smokehouse"),
    "tropical":        ("coffee_plantation",   "spice_market",      "coastal_citadel",
                        "incense_lodge",       "reed_weaver",       "gold_panning_camp"),
    "savanna":         ("nomad_camp",          "spirit_distillery", "desert_legion",
                        "gold_panning_camp",
                        "tournament_grounds",
                        "furusiyya_madrasa",   "rajput_garh",
                        "cataphract_sun_court","horde_ordu",
                        "carpet_caravan"),
    "wasteland":       ("nomad_camp",          "canyon_forge",      "steppe_warcamp",
                        "deep_mine_camp",      "prospector_post",   "coal_pit",
                        "sulfur_pit",          "horde_ordu"),
    "alpine_mountain": ("alpine_monastery",    "cheese_cave",       "highland_fortress",
                        "glacier_camp",        "mountain_lodge",    "apiary",
                        "deep_mine_camp",      "lapidary_atelier",  "dwarven_hold",
                        "carders_cottage",     "highland_dairy"),
    "rocky_mountain":  ("cheese_cave",         "canyon_forge",      "highland_fortress",
                        "mountain_lodge",      "deep_mine_camp",    "quarry_camp",
                        "prospector_post",     "lapidary_atelier",  "coal_pit",
                        "marble_quarry",       "dwarven_hold",
                        "highland_dairy",      "charcuterie_house"),
    "rolling_hills":   ("hillside_vineyard",   "pottery_workshop",  "border_garrison",
                        "mountain_lodge",      "apiary",            "scriptorium",
                        "quarry_camp",         "marble_quarry",
                        "tournament_grounds",  "tournament_grounds",
                        "creamery",            "smokehouse",        "carders_cottage",
                        "charcuterie_house",   "compost_yard"),
    "steep_hills":     ("hillside_vineyard",   "sculpture_atelier", "highland_fortress",
                        "mountain_lodge",      "quarry_camp",       "prospector_post",
                        "lapidary_atelier",    "coal_pit",          "marble_quarry",
                        "carders_cottage",     "highland_dairy"),
    "steppe":          ("nomad_camp",          "spirit_distillery", "steppe_warcamp",
                        "tournament_grounds",  "tournament_grounds",
                        "horde_ordu",          "horde_ordu",        "horde_ordu"),
    "arid_steppe":     ("nomad_camp",          "desert_glassworks", "desert_legion",
                        "quarry_camp",         "prospector_post",   "sulfur_pit",
                        "horde_ordu",          "cataphract_sun_court",
                        "furusiyya_madrasa",   "rug_merchant",
                        "carpet_caravan"),
    "desert":          ("desert_glassworks",   "canyon_forge",      "desert_legion",
                        "prospector_post",     "sulfur_pit",
                        "furusiyya_madrasa",   "furusiyya_madrasa",
                        "cataphract_sun_court","carpet_caravan"),
    "tundra":          ("boreal_distillery",   "alpine_monastery",  "glacier_camp",
                        "coal_pit",            "carders_cottage",
                        "highland_dairy"),
    "swamp":           ("swamp_alchemist",     "salt_works",        "reed_weaver",
                        "bog_apothecary",      "gold_panning_camp"),
    "beach":           ("fishing_outpost",     "coastal_saltworks", "coastal_citadel"),
    "canyon":          ("canyon_forge",        "desert_glassworks", "highland_fortress",
                        "deep_mine_camp",      "quarry_camp",       "prospector_post",
                        "lapidary_atelier",    "marble_quarry",     "dwarven_hold",
                        "sulfur_pit"),
    "mediterranean":   ("olive_press",         "wine_estate",       "coastal_citadel",
                        "marble_quarry",
                        "tournament_grounds",  "tournament_grounds",
                        "cataphract_sun_court","furusiyya_madrasa",
                        "rug_merchant",        "charcuterie_house",
                        "carpet_caravan"),
    "east_asian":      ("tea_house",           "pottery_workshop",  "silk_pavilion",
                        "incense_lodge",       "lapidary_atelier",  "marble_quarry",
                        "bushi_dojo",          "bushi_dojo",        "bushi_dojo",
                        "rug_merchant",        "carpet_caravan"),
    "south_asian":     ("spice_market",        "textile_guild",     "silk_pavilion",
                        "incense_lodge",
                        "rajput_garh",         "rajput_garh",       "rajput_garh",
                        "rug_merchant",        "carpet_caravan"),
    "pacific_island":  ("pearl_diving_camp",   "canoe_trading_post",
                        "polynesian_shrine_outpost"),
}

# ---------------------------------------------------------------------------
# Kingdom (region) assignment — nearest town lookup
# ---------------------------------------------------------------------------

def region_for_outpost(op: "Outpost"):
    """Return the Region this outpost belongs to (nearest town's region, or None)."""
    from towns import TOWNS, REGIONS
    if not TOWNS:
        return None
    nearest = min(TOWNS.values(), key=lambda t: abs(t.center_bx - op.center_bx))
    return REGIONS.get(nearest.region_id)

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
    "scriptorium":       ["Scriptorium", "Library", "Manuscript House"],
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
    "apiary":            ["Apiary", "Bee Garden", "Honey House", "Meadow Apiary"],
    "deep_mine_camp":    ["Deep Mine", "Pit Camp", "Shaft Camp", "Lodebreak"],
    "quarry_camp":       ["Quarry", "Stoneworks", "Cutters' Camp", "Block Quarry"],
    "prospector_post":   ["Prospector Post", "Strike Camp", "Vein Camp", "Sluice Camp"],
    "lapidary_atelier":  ["Lapidary", "Gem Atelier", "Jewel Cutters", "Faceting House"],
    "coal_pit":          ["Coal Pit", "Collier Camp", "Sootworks", "Pit Head"],
    "marble_quarry":     ["Marble Quarry", "Stoneyard", "Cutter's Reach", "White Quarry"],
    "dwarven_hold":      ["Dwarven Hold", "Underhall", "Stonefast", "Deeproot Hold"],
    "sulfur_pit":        ["Sulfur Pit", "Brimstone Camp", "Cinder Works", "Yellow Pit"],
    "gold_panning_camp": ["Panning Camp", "Sluice Camp", "Riverstrike", "Gravel Bend"],
    "creamery":          ["Creamery", "Dairy", "Milk House", "Butter Cottage"],
    "carders_cottage":   ["Carders' Cottage", "Spinners' Cottage", "Wool House",
                          "Fleece Hall", "Distaff Cottage"],
    "smokehouse":        ["Smokehouse", "Butcher's Yard", "Curing House", "Meat Hall"],
    "rug_merchant":      ["Rug Merchant", "Carpet Bazaar", "Tapestry House",
                          "Loom Bazaar"],
    "highland_dairy":    ["Highland Dairy", "Mountain Creamery", "Alm Dairy",
                          "Shepherd's Cellar"],
    "charcuterie_house": ["Charcuterie House", "Cured Meats Hall", "Salumi House",
                          "Larder Market"],
    "compost_yard":      ["Compost Yard", "Manure Pits", "Dung Works",
                          "Field-Hand's Yard"],
    "carpet_caravan":    ["Carpet Caravan", "Dye-Loom Caravan", "Tapestry Caravan",
                          "Weavers' Caravan"],
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
# LEGO piece system — layout pieces + cursor placer
# ---------------------------------------------------------------------------

_CAMP_LONGHOUSE_BIOMES = {
    "tundra", "alpine_mountain", "boreal", "rocky_mountain",
    "temperate", "birch_forest", "redwood", "wasteland",
}


def _place_tilt_rail(world, left_x, sy, width, biodome, tournament=False):
    """Jousting tilt-rail: two end posts with a horizontal rail between them.

    Used by tournament_grounds (long lane with pennanted end-posts).
    East-asian / south-asian biomes use bamboo rails; everywhere else uses
    plain wood. Tournament lanes get a heraldic banner at each end-post.
    """
    if width < 3:
        return
    rail_block = BAMBOO_FENCE_JP if biodome in _EASTERN_CHAPTER_BIOMES else WOOD_FENCE
    rail_y     = sy - 1
    post_y_top = sy - 3
    # End posts — two-tall, foreground so they read as solid pillars
    for px in (left_x, left_x + width - 1):
        if not (0 <= px < world.width):
            continue
        for py in range(post_y_top, sy):
            if 0 <= py < world.height:
                world.set_block(px, py, rail_block)
        if tournament:
            banner_y = post_y_top - 1
            if 0 <= banner_y < world.height:
                world.set_bg_block(px, banner_y, BANNER_BLOCK)
    # Single rail row spanning between the posts — bg so the player can walk
    # the full length of the lane without snagging on it.
    for bx in range(left_x + 1, left_x + width - 1):
        if 0 <= bx < world.width and 0 <= rail_y < world.height:
            world.set_bg_block(bx, rail_y, rail_block)


def _place_mine_shaft(world, left_x, sy, width, depth):
    """Carve an open mine shaft downward from the surface."""
    for d in range(1, depth + 1):
        by = sy + d
        if not (0 <= by < world.height):
            break
        for bx in range(left_x, left_x + width):
            world.set_block(bx, by, AIR)
        # Cobblestone support beams every 4 rows; centre column stays open
        if d % 4 == 0:
            world.set_block(left_x,             by, COBBLESTONE)
            world.set_block(left_x + width - 1, by, COBBLESTONE)


def _dispatch_piece(world, rng, piece, left_x, sy, biodome, wall, roof):
    from cities import (
        _place_house, _place_house_two_story, _place_longhouse,
        _place_barn, _place_tower, _place_shrine_for_biome,
        _place_market_stall, _place_pavilion, _place_ruin,
        _place_standing_stones, _place_bedouin_tent,
        _place_farm_plot, _place_garden_plot,
    )
    ptype  = piece["type"]
    width  = piece["width"]
    height = piece.get("height", 3)
    if ptype == "gap":
        pass
    elif ptype == "primary":
        _place_primary(world, piece.get("style", "house"),
                       left_x, sy, width, height, wall, roof, biodome, rng)
    elif ptype == "house":
        _place_house(world, left_x, sy, width, height, wall, roof, rng)
    elif ptype == "house_2story":
        _place_house_two_story(world, left_x, sy, width,
                               piece.get("floor1", 3), piece.get("floor2", 3),
                               wall, roof, rng)
    elif ptype == "longhouse":
        _place_longhouse(world, left_x, sy, width, height, wall, roof, rng)
    elif ptype == "barn":
        _place_barn(world, left_x, sy, width, height, rng)
    elif ptype == "tower":
        _place_tower(world, left_x, sy, width, height, wall, roof)
    elif ptype == "shrine":
        _place_shrine_for_biome(world, left_x, sy, width, height, biodome)
    elif ptype == "stall":
        _place_market_stall(world, rng, left_x, sy, width, height)
    elif ptype == "pavilion":
        _place_pavilion(world, left_x, sy, width, height, wall, roof)
    elif ptype == "tent":
        _place_bedouin_tent(world, left_x, sy, width, height, rng)
    elif ptype == "ruin":
        _place_ruin(world, left_x, sy, width, height)
    elif ptype == "standing_stones":
        _place_standing_stones(world, left_x, sy, width, height)
    elif ptype == "garden":
        _place_garden_plot(world, rng, left_x + width // 2, sy, biodome, width // 2)
    elif ptype == "farm":
        _place_farm_plot(world, rng, left_x + width // 2, biodome, width // 2)
    elif ptype == "mine":
        _place_mine_shaft(world, left_x, sy, width, piece.get("depth", 12))
    elif ptype == "tilt_rail":
        _place_tilt_rail(world, left_x, sy, width, biodome,
                         tournament=piece.get("tournament", False))


def _place_outpost_pieces(world, rng, start_x, sy, biodome, wall, roof, pieces,
                          terrain_profile=None):
    """Walk pieces left-to-right (mirrors city cursor), return NPC and flag coords."""
    from cities import (_level_building_footprint, _building_floor_sy,
                        _place_terrace_stairs)
    cursor       = start_x
    npc_px       = npc_py = None
    flag_bx      = flag_by = None
    prev_right_x = None   # right edge of last non-gap piece
    prev_sy      = None   # floor sy of last non-gap piece

    for piece in pieces:
        width = piece["width"]
        # Level every piece (including gaps) to its terrain-profile height so
        # raw terrain is never left exposed between buildings.
        if terrain_profile:
            item_sy = _building_floor_sy(terrain_profile, cursor, width)
            _level_building_footprint(world, cursor, width, item_sy)
        else:
            item_sy = sy

        # Bridge height difference to the previous non-gap piece with stair blocks.
        if piece["type"] != "gap" and prev_right_x is not None and prev_sy != item_sy:
            _place_terrace_stairs(world, prev_right_x, cursor, prev_sy, item_sy)

        _dispatch_piece(world, rng, piece, cursor, item_sy, biodome, wall, roof)

        if piece.get("npc"):
            npc_px = (cursor + 1) * BLOCK_SIZE
            npc_py = (item_sy - 2) * BLOCK_SIZE
        if piece.get("flag"):
            flag_bx = cursor - 2
            flag_by = item_sy - piece.get("flag_dy", 1)

        if piece["type"] != "gap":
            prev_right_x = cursor + width
            prev_sy      = item_sy

        cursor += width
    return npc_px, npc_py, flag_bx, flag_by


# ---------------------------------------------------------------------------
# Layout builders — each returns a piece list
# ---------------------------------------------------------------------------

def _layout_default(half_w, wall, roof, rng, biodome, cfg):
    bld_w  = rng.randint(5, 7)
    bld_h  = rng.randint(3, 5)
    bld2_w = rng.randint(4, 6)
    bld2_h = rng.randint(3, 4)
    avail  = half_w * 2 - 1
    trail  = max(0, avail - bld_w - 2 - 7 - 2 - bld2_w)
    return [
        {"type": "primary", "width": bld_w,  "height": bld_h,
         "style": cfg["building_style"], "npc": True, "flag": True},
        {"type": "gap",     "width": 2},
        {"type": "garden",  "width": 7},
        {"type": "gap",     "width": 2},
        {"type": "house",   "width": bld2_w, "height": bld2_h},
        {"type": "gap",     "width": trail},
    ]


def _layout_military_fort(half_w, wall, roof, rng, biodome, cfg):
    inner = max(8, half_w * 2 - 11)
    return [
        {"type": "tower",    "width": 3, "height": 5,
         "flag": True, "flag_dy": 7},
        {"type": "gap",      "width": 2},
        {"type": "longhouse","width": inner, "height": 4, "npc": True},
        {"type": "gap",      "width": 2},
        {"type": "tower",    "width": 3, "height": 5},
    ]


def _layout_warcamp(half_w, wall, roof, rng, biodome, cfg):
    avail = half_w * 2 - 1
    if biodome in _CAMP_LONGHOUSE_BIOMES:
        trail = max(0, avail - 22)
        return [
            {"type": "longhouse", "width": 8, "height": 3, "npc": True, "flag": True},
            {"type": "gap",       "width": 2},
            {"type": "ruin",      "width": 6, "height": 3},
            {"type": "gap",       "width": 2},
            {"type": "house",     "width": 4, "height": 3},
            {"type": "gap",       "width": trail},
        ]
    else:
        trail = max(0, avail - 22)
        return [
            {"type": "tent", "width": 5, "height": 3, "flag": True},
            {"type": "gap",  "width": 3},
            {"type": "tent", "width": 5, "height": 3, "npc": True},
            {"type": "gap",  "width": 3},
            {"type": "ruin", "width": 6, "height": 3},
            {"type": "gap",  "width": trail},
        ]


def _layout_estate(half_w, wall, roof, rng, biodome, cfg):
    farm_w = max(6, half_w * 2 - 18)
    return [
        {"type": "house_2story", "width": 7, "floor1": 3, "floor2": 3,
         "npc": True, "flag": True},
        {"type": "gap",  "width": 2},
        {"type": "farm", "width": farm_w},
        {"type": "gap",  "width": 2},
        {"type": "barn", "width": 6, "height": 4},
    ]


def _layout_monastery(half_w, wall, roof, rng, biodome, cfg):
    garden_w = max(5, half_w * 2 - 23)
    return [
        {"type": "house",          "width": 4, "height": 3},
        {"type": "gap",            "width": 2},
        {"type": "shrine",         "width": 7, "height": 5, "npc": True, "flag": True},
        {"type": "gap",            "width": 2},
        {"type": "standing_stones","width": 5, "height": 4},
        {"type": "gap",            "width": 2},
        {"type": "garden",         "width": garden_w},
    ]


# Biome groups feeding tournament/jousting flavor. East-asian / south-asian
# biomes get bamboo rails on tilt-yards; everywhere else gets plain wood.
_EASTERN_CHAPTER_BIOMES = {"east_asian", "south_asian"}


def _layout_tournament(half_w, wall, roof, rng, biodome, cfg):
    """Tournament Grounds: viewing stand + jousting lane + stables.

    The long tilt-rail with pennanted end-posts is the unmistakable silhouette
    here — once spawned, it reads as a tilt-yard from across the chunk.
    """
    avail   = half_w * 2 - 1
    barn_w  = 6
    stand_w = 7
    lane_w  = max(13, avail - (stand_w + 2 + 2 + barn_w + 2))
    return [
        {"type": "house_2story", "width": stand_w, "floor1": 3, "floor2": 3,
                                 "npc": True, "flag": True},
        {"type": "gap",          "width": 2},
        {"type": "tilt_rail",    "width": lane_w, "tournament": True},
        {"type": "gap",          "width": 2},
        {"type": "barn",         "width": barn_w, "height": 4},
    ]


def _layout_watchtower(half_w, wall, roof, rng, biodome, cfg):
    trail = max(1, half_w * 2 - 12)
    return [
        {"type": "tower", "width": 3, "height": 6, "flag": True, "flag_dy": 8},
        {"type": "gap",   "width": 3},
        {"type": "house", "width": 5, "height": 3, "npc": True},
        {"type": "gap",   "width": trail},
    ]


def _layout_market(half_w, wall, roof, rng, biodome, cfg):
    trail = max(0, half_w * 2 - 22)
    return [
        {"type": "stall",   "width": 4, "height": 3, "flag": True},
        {"type": "gap",     "width": 1},
        {"type": "stall",   "width": 4, "height": 3, "npc": True},
        {"type": "gap",     "width": 1},
        {"type": "stall",   "width": 4, "height": 3},
        {"type": "gap",     "width": 2},
        {"type": "pavilion","width": 5, "height": 3},
        {"type": "gap",     "width": trail},
    ]


def _layout_underground(half_w, wall, roof, rng, biodome, cfg):
    trail = max(0, half_w * 2 - 20)
    return [
        {"type": "house", "width": 5, "height": 4, "npc": True, "flag": True},
        {"type": "gap",   "width": 2},
        {"type": "mine",  "width": 4, "depth": 14},
        {"type": "gap",   "width": 2},
        {"type": "ruin",  "width": 6, "height": 3},
        {"type": "gap",   "width": trail},
    ]


_LAYOUT_FNS = {
    "default":       _layout_default,
    "military_fort": _layout_military_fort,
    "warcamp":       _layout_warcamp,
    "estate":        _layout_estate,
    "monastery":     _layout_monastery,
    "tournament":    _layout_tournament,
    "watchtower":    _layout_watchtower,
    "market":        _layout_market,
    "underground":   _layout_underground,
}

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
    from cities import (_PLANT_BLOCKS, _city_terrain_profile,
                        _repair_city_walkability)

    cfg    = OUTPOST_TYPES[otype]
    half_w = cfg["half_w"]
    biodome = world.biodome_at(out_bx)
    sy      = world.surface_y_at(out_bx)

    # Pre-load chunks with a wider buffer so flattening doesn't read stale terrain
    chunk_lo = (out_bx - half_w - 10) // CHUNK_W
    chunk_hi = (out_bx + half_w + 10) // CHUNK_W
    for ci in range(chunk_lo, chunk_hi + 1):
        world.load_chunk(ci)

    # Build smoothed per-column elevation profile across the footprint
    terrain_profile = _city_terrain_profile(world, out_bx - half_w, out_bx + half_w)
    min_sy = min(terrain_profile.values())
    max_sy = max(terrain_profile.values())

    # Strip plants across the full height range of the footprint
    for bx in range(out_bx - half_w - 2, out_bx + half_w + 3):
        for by in range(max(0, min_sy - 35), max_sy + 1):
            if world.get_block(bx, by) in _PLANT_BLOCKS:
                world.set_block(bx, by, AIR)

    # Register zone so later generation won't overlap
    world.city_zones.append((out_bx - half_w, out_bx + half_w))

    wall, roof = _pick_palette(biodome, rng)

    layout_fn = _LAYOUT_FNS.get(cfg.get("layout", "default"), _layout_default)
    pieces    = layout_fn(half_w, wall, roof, rng, biodome, cfg)
    start_x   = out_bx - half_w + 1
    npc_px, npc_py, flag_bx, flag_by = _place_outpost_pieces(
        world, rng, start_x, sy, biodome, wall, roof, pieces,
        terrain_profile=terrain_profile)

    # Post-placement: smooth walkability between buildings
    _repair_city_walkability(world, out_bx - half_w, out_bx + half_w,
                             sy, terrain_profile)

    # Fallback NPC position if no piece tagged npc
    if npc_px is None:
        npc_px = (start_x + 1) * BLOCK_SIZE
        npc_py = (sy - 2)      * BLOCK_SIZE

    if flag_bx is not None and 0 <= flag_by < world.height:
        world.set_bg_block(flag_bx, flag_by, OUTPOST_FLAG_BLOCK)
    else:
        print(f"[WARNING] Outpost '{otype}' at bx={out_bx}: flag block not placed "
              f"(flag_bx={flag_bx}, flag_by={flag_by}). E-key will not work.")

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
    keeper = OutpostKeeperNPC(npc_px, npc_py, world, outpost_id, otype)
    keeper._setup_identity(outpost_id + 50000, 0, getattr(world, "seed", 0))
    world.entities.append(keeper)

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
            sol_py = (terrain_profile.get(pos_bx, sy) - 2) * BLOCK_SIZE
            world.entities.append(
                MilitarySoldierNPC(sol_px, sol_py, world, otype, clothing, patrol_half)
            )

    # Miners' Guild outposts get a branching underground mineshaft beneath
    # them — entrance offset from the building footprint so it doesn't punch
    # through a wall; depths/galleries randomized inside mine_structures.
    from guilds import OUTPOST_TYPE_TO_INDUSTRY, INDUSTRY_MINING
    if OUTPOST_TYPE_TO_INDUSTRY.get(otype) == INDUSTRY_MINING:
        from mine_structures import generate_mine
        mine_bx = out_bx + half_w - 4
        mine_sy = terrain_profile.get(mine_bx, sy)
        generate_mine(world, mine_bx, mine_sy, rng, outpost_type=otype)

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
    if biodome == "ocean":
        return
    if biodome in ("coastal", "beach", "pacific_island") and world.surface_height(slot_x) > SURFACE_Y:
        return
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
    """Return the nearest Outpost to (bx, by), or None if OUTPOSTS is empty."""
    if not OUTPOSTS:
        return None
    return min(OUTPOSTS.values(), key=lambda op: abs(op.center_bx - bx))

# ---------------------------------------------------------------------------
# Day tick (called from world.py alongside advance_day)
# ---------------------------------------------------------------------------

def tick_outpost_day(world_day: int, world_seed: int = 0) -> None:
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

    # Refresh sommelier request boards for wine outposts
    try:
        from sommelier import tick_sommelier_day
        tick_sommelier_day(world_seed, world_day)
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Init / restore on load
# ---------------------------------------------------------------------------

def _spawn_outpost_npcs(world, op: "Outpost") -> None:
    """Recreate keeper (and soldiers for military types) for an already-registered outpost."""
    from outpost_npcs import OutpostKeeperNPC, MilitarySoldierNPC, _resolve_clothing
    otype       = op.outpost_type
    hw          = OUTPOST_TYPES[otype]["half_w"]
    sy          = world.surface_y_at(op.center_bx)
    npc_px      = (op.center_bx - hw + 3) * BLOCK_SIZE
    npc_py      = (sy - 2) * BLOCK_SIZE
    keeper      = OutpostKeeperNPC(npc_px, npc_py, world, op.outpost_id, otype)
    keeper._setup_identity(op.outpost_id + 50000, 0, getattr(world, "seed", 0))
    world.entities.append(keeper)
    if otype in _MILITARY_OUTPOST_TYPES:
        cfg         = OUTPOST_TYPES[otype]
        clothing    = _resolve_clothing(cfg["clothing_key"])
        patrol_half = max(12, hw // 3)
        for pos_bx in [op.center_bx - hw // 3, op.center_bx, op.center_bx + hw // 3]:
            world.entities.append(
                MilitarySoldierNPC(pos_bx * BLOCK_SIZE, npc_py, world, otype, clothing, patrol_half)
            )


def _reconstruct_outpost_for_slot(world, seed: int, slot_x: int) -> None:
    """Rebuild a missing Outpost record (no block placement) for an orphaned slot.

    Used when a flag block survived in a chunk but the DB row was lost
    (e.g. game closed between chunk generation and the next autosave).
    Uses the same RNG sequence as _build_outpost so type/name are deterministic.
    """
    biodome = world.biodome_at(slot_x)
    if biodome == "ocean":
        return
    if biodome in ("coastal", "beach", "pacific_island") and world.surface_height(slot_x) > SURFACE_Y:
        return
    otype = _type_for_slot(seed, slot_x, biodome)
    if otype is None or otype not in OUTPOST_TYPES:
        return

    rng    = _slot_rng(seed, slot_x)
    rng.random(); rng.random()  # skip spawn + type rolls (match _build_outpost)
    jitter = rng.randint(-5, 5)
    out_bx = slot_x + jitter

    hw = OUTPOST_TYPES[otype]["half_w"]
    op_lo, op_hi = out_bx - hw, out_bx + hw
    if any(op_hi >= lo - 5 and op_lo <= hi + 5
           for lo, hi in getattr(world, "city_zones", [])):
        return

    cfg   = OUTPOST_TYPES[otype]
    op_id = (max(OUTPOSTS.keys()) + 1) if OUTPOSTS else 0
    op    = Outpost(
        outpost_id        = op_id,
        outpost_type      = otype,
        center_bx         = out_bx,
        slot_x            = slot_x,
        biome             = biodome,
        name              = _make_outpost_name(_slot_rng(seed, slot_x), otype, biodome),
        founded_day       = 0,
        needs             = {iid: {"required": amt, "supplied": 0}
                             for iid, amt in cfg["needs"]},
        needs_met_days    = 0,
        last_resupply_day = 0,
        stock             = {iid: cfg["base_stock"] for iid, _ in cfg["sells"]},
    )
    OUTPOSTS[op_id] = op
    world.city_zones.append((op_lo, op_hi))
    _spawn_outpost_npcs(world, op)
    print(f"[outposts] Recovered orphaned outpost '{op.name}' ({otype}) at bx={out_bx}.")


def init_outposts(world) -> None:
    OUTPOSTS.clear()
    if not hasattr(world, '_save_mgr') or world._save_mgr is None:
        return

    outpost_data = world._save_mgr._load_outposts()

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

        hw = OUTPOST_TYPES[otype]["half_w"]
        world.city_zones.append((op.center_bx - hw, op.center_bx + hw))
        _spawn_outpost_npcs(world, op)

    # Scan loaded chunks for slots whose DB record is missing (orphaned flag blocks).
    # This recovers outposts that were generated but not yet saved when the game closed.
    registered_slots = {op.slot_x for op in OUTPOSTS.values()}
    seed = getattr(world, "seed", 0)
    half = OUTPOST_SLOT_SPACING // 2
    for cx in list(world._chunks.keys()):
        base_x = cx * CHUNK_W
        for bx in range(base_x, base_x + CHUNK_W):
            if ((bx % OUTPOST_SLOT_SPACING) + OUTPOST_SLOT_SPACING) % OUTPOST_SLOT_SPACING == half:
                if bx not in registered_slots and _should_spawn(seed, bx):
                    _reconstruct_outpost_for_slot(world, seed, bx)
                break
