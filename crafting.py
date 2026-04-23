# ---------------------------------------------------------------------------
# Bakery recipes (ingredient dict → output)
# ---------------------------------------------------------------------------

BAKERY_RECIPES = [
    {"name": "Bread",          "ingredients": {"wheat": 3},                   "output_id": "bread",          "output_count": 1},
    {"name": "Strawberry Jam", "ingredients": {"strawberry": 3},              "output_id": "strawberry_jam", "output_count": 1},
    {"name": "Cheese",      "ingredients": {"milk": 3},                    "output_id": "cheese",      "output_count": 1},
    {"name": "Tomato Soup", "ingredients": {"tomato": 3},                  "output_id": "tomato_soup", "output_count": 1},
    {"name": "Corn Bread",  "ingredients": {"corn": 2, "wheat": 1},        "output_id": "corn_bread",  "output_count": 1},
    {"name": "Pumpkin Pie", "ingredients": {"pumpkin": 1, "wheat": 2},     "output_id": "pumpkin_pie", "output_count": 1},
    {"name": "Apple Pie",   "ingredients": {"apple": 2, "wheat": 2},       "output_id": "apple_pie",   "output_count": 1},
    {"name": "Carrot Cake",    "ingredients": {"carrot": 2, "wheat": 2},                  "output_id": "carrot_cake",    "output_count": 1},
    {"name": "Cheese Bread",   "ingredients": {"bread": 1, "cheese": 1},                  "output_id": "cheese_bread",   "output_count": 1},
    # --- Chinese cuisine ---
    {"name": "Tofu",           "ingredients": {"corn": 3},                                 "output_id": "tofu",           "output_count": 1},
    {"name": "Steamed Rice",   "ingredients": {"rice": 2},                                 "output_id": "steamed_rice",   "output_count": 1},
    {"name": "Egg Fried Rice", "ingredients": {"rice": 1, "egg": 1, "carrot": 1},          "output_id": "egg_fried_rice", "output_count": 1},
    {"name": "Congee",         "ingredients": {"rice": 2, "milk": 1},                      "output_id": "congee",         "output_count": 1},
    {"name": "Mapo Tofu",      "ingredients": {"tofu": 1, "tomato": 1, "ginger": 1},       "output_id": "mapo_tofu",      "output_count": 1},
    {"name": "Dumplings",      "ingredients": {"wheat": 1, "carrot": 1, "ginger": 1},      "output_id": "dumplings",      "output_count": 2},
    {"name": "Wonton Soup",    "ingredients": {"wheat": 1, "mushroom": 1, "ginger": 1},    "output_id": "wonton_soup",    "output_count": 1},
    {"name": "Kung Pao",       "ingredients": {"corn": 1, "pumpkin": 1, "ginger": 1},      "output_id": "kung_pao",       "output_count": 1},
    {"name": "Moon Cake",      "ingredients": {"wheat": 1, "pumpkin": 1, "egg": 1},        "output_id": "moon_cake",      "output_count": 2},
    {"name": "Hot & Sour Soup","ingredients": {"mushroom": 1, "tomato": 1, "egg": 1},      "output_id": "hot_sour_soup",  "output_count": 1},
    {"name": "Sweet Rice Ball","ingredients": {"rice": 1, "pumpkin": 1},                   "output_id": "sweet_rice_ball","output_count": 2},
    {"name": "Sweet Potato Pie",   "ingredients": {"sweet_potato": 2, "wheat": 1},         "output_id": "sweet_potato_pie",   "output_count": 1},
    # --- Desert bakery ---
    {"name": "Date Cake",     "ingredients": {"date_palm_fruit": 2, "wheat": 1},             "output_id": "date_cake",     "output_count": 1},
    {"name": "Cactus Candy",  "ingredients": {"cactus_fruit": 2, "agave_syrup": 1},          "output_id": "cactus_candy",  "output_count": 2},
]

# ---------------------------------------------------------------------------
# Wok recipes
# ---------------------------------------------------------------------------

WOK_RECIPES = [
    {"name": "Scallion Pancake", "ingredients": {"scallion": 2, "wheat": 1},                    "output_id": "scallion_pancake", "output_count": 2},
    {"name": "Chili Oil Tofu",   "ingredients": {"tofu": 1, "chili": 1, "ginger": 1},           "output_id": "chili_oil_tofu",   "output_count": 1},
    {"name": "Stir Fried Rice",  "ingredients": {"rice": 1, "scallion": 1, "egg": 1},           "output_id": "stir_fried_rice",  "output_count": 1},
    {"name": "Spicy Corn",       "ingredients": {"corn": 2, "chili": 1},                         "output_id": "spicy_corn",       "output_count": 2},
    {"name": "Chili Bok Choy",   "ingredients": {"bok_choy": 2, "chili": 1, "garlic": 1},       "output_id": "chili_bok_choy",   "output_count": 1},
    {"name": "Scallion Eggs",    "ingredients": {"egg": 2, "scallion": 1},                       "output_id": "scallion_eggs",    "output_count": 1},
    {"name": "Cooked Egg",       "ingredients": {"egg": 1},                                      "output_id": "cooked_egg",       "output_count": 1},
    {"name": "Omelette",         "ingredients": {"egg": 2},                                      "output_id": "omelette",         "output_count": 1},
    {"name": "Garlic Bok Choy",  "ingredients": {"bok_choy": 2, "garlic": 1},                   "output_id": "garlic_bok_choy",  "output_count": 1},
    {"name": "Turnip Mash",      "ingredients": {"turnip": 2, "ginger": 1},                      "output_id": "turnip_mash",      "output_count": 1},
    {"name": "Zucchini Stir Fry","ingredients": {"zucchini": 2, "garlic": 1},                    "output_id": "zucchini_stir_fry","output_count": 1},
    {"name": "Celery Stir Fry",  "ingredients": {"celery": 2, "scallion": 1},                    "output_id": "celery_stir_fry",  "output_count": 1},
    {"name": "Broccoli Stir Fry","ingredients": {"broccoli": 2, "garlic": 1},                    "output_id": "broccoli_stir_fry","output_count": 1},
    # --- Desert wok ---
    {"name": "Desert Salad",     "ingredients": {"cactus_fruit": 1, "watermelon": 1, "chili": 1}, "output_id": "desert_salad",     "output_count": 1},
]

# ---------------------------------------------------------------------------
# Steamer recipes
# ---------------------------------------------------------------------------

STEAMER_RECIPES = [
    {"name": "Steamed Bun",    "ingredients": {"wheat": 2},                                      "output_id": "steamed_bun",    "output_count": 2},
    {"name": "Lotus Rice",     "ingredients": {"rice": 2, "mushroom": 1},                        "output_id": "lotus_rice",     "output_count": 1},
    {"name": "Crystal Rolls",  "ingredients": {"wheat": 1, "bok_choy": 1, "scallion": 1},       "output_id": "crystal_rolls",  "output_count": 2},
    {"name": "Steamed Egg",    "ingredients": {"egg": 2, "milk": 1},                             "output_id": "steamed_egg",    "output_count": 1},
    {"name": "Pumpkin Cake",   "ingredients": {"pumpkin": 1, "rice": 1},                         "output_id": "pumpkin_cake",   "output_count": 2},
]

# ---------------------------------------------------------------------------
# Noodle Pot recipes
# ---------------------------------------------------------------------------

NOODLE_POT_RECIPES = [
    {"name": "Soy Sauce",     "ingredients": {"wheat": 3},                                       "output_id": "soy_sauce",     "output_count": 1},
    {"name": "Noodles",       "ingredients": {"wheat": 2},                                       "output_id": "noodles",       "output_count": 2},
    {"name": "Ramen",         "ingredients": {"noodles": 1, "soy_sauce": 1, "scallion": 1},     "output_id": "ramen",         "output_count": 1},
    {"name": "Chili Noodles", "ingredients": {"noodles": 1, "chili": 1, "garlic": 1},           "output_id": "chili_noodles", "output_count": 1},
    {"name": "Noodle Soup",   "ingredients": {"noodles": 1, "bok_choy": 1, "mushroom": 1},      "output_id": "noodle_soup",   "output_count": 1},
    {"name": "Sesame Noodles","ingredients": {"noodles": 1, "ginger": 1},                        "output_id": "sesame_noodles","output_count": 1},
    {"name": "Hot Pot Broth", "ingredients": {"mushroom": 2, "ginger": 1, "chili": 1},          "output_id": "hot_pot_broth", "output_count": 1},
    {"name": "Scallion Soup",     "ingredients": {"scallion": 2, "tofu": 1},                    "output_id": "scallion_soup",    "output_count": 1},
    {"name": "Leek & Potato Soup","ingredients": {"leek": 1, "potato": 2},                       "output_id": "leek_potato_soup", "output_count": 1},
    {"name": "Pea Soup",          "ingredients": {"pea": 2, "onion": 1},                         "output_id": "pea_soup",         "output_count": 1},
]

# ---------------------------------------------------------------------------
# BBQ Grill recipes
# ---------------------------------------------------------------------------

BBQ_GRILL_RECIPES = [
    {"name": "Grilled Corn",     "ingredients": {"corn": 2},                                    "output_id": "grilled_corn",     "output_count": 2},
    {"name": "Potato Wedges",    "ingredients": {"potato": 2},                                  "output_id": "potato_wedges",    "output_count": 2},
    {"name": "BBQ Eggplant",     "ingredients": {"eggplant": 1, "scallion": 1},                 "output_id": "bbq_eggplant",     "output_count": 1},
    {"name": "Grilled Mushroom", "ingredients": {"mushroom": 2, "garlic": 1},                   "output_id": "grilled_mushroom", "output_count": 2},
    {"name": "Stuffed Pepper",   "ingredients": {"pepper": 1, "rice": 1, "egg": 1},             "output_id": "stuffed_pepper",   "output_count": 1},
    {"name": "Eggplant Skewer",  "ingredients": {"eggplant": 2, "chili": 1, "scallion": 1},    "output_id": "eggplant_skewer",  "output_count": 2},
    {"name": "Corn Ribs",        "ingredients": {"corn": 1, "chili": 1, "garlic": 1},           "output_id": "corn_ribs",        "output_count": 2},
    {"name": "BBQ Tofu",         "ingredients": {"tofu": 1, "pepper": 1, "scallion": 1},        "output_id": "bbq_tofu",         "output_count": 1},
    {"name": "Roast Onion",      "ingredients": {"onion": 2, "garlic": 1},                      "output_id": "roast_onion",      "output_count": 2},
    {"name": "Grilled Cabbage",   "ingredients": {"cabbage": 2, "garlic": 1},                   "output_id": "grilled_cabbage",   "output_count": 1},
    {"name": "Sweet Potato Wedges","ingredients": {"sweet_potato": 2},                            "output_id": "sweet_potato_wedges","output_count": 2},
    {"name": "Grilled Leek",      "ingredients": {"leek": 3},                                    "output_id": "grilled_leek",      "output_count": 2},
    {"name": "Watermelon Salad",  "ingredients": {"watermelon": 2},                              "output_id": "watermelon_salad",  "output_count": 1},
    # --- Desert BBQ ---
    {"name": "Grilled Cactus",   "ingredients": {"cactus_fruit": 2},                             "output_id": "grilled_cactus",    "output_count": 2},
    # --- Meat ---
    {"name": "Cooked Mutton",    "ingredients": {"raw_mutton": 1},                                "output_id": "cooked_mutton",     "output_count": 1},
    {"name": "Cooked Beef",      "ingredients": {"raw_beef": 1},                                  "output_id": "cooked_beef",       "output_count": 1},
    {"name": "Cooked Chicken",   "ingredients": {"raw_chicken": 1},                               "output_id": "cooked_chicken",    "output_count": 1},
]

# ---------------------------------------------------------------------------
# Clay Pot recipes
# ---------------------------------------------------------------------------

CLAY_POT_RECIPES = [
    {"name": "Potato Stew",          "ingredients": {"potato": 2, "carrot": 1},                      "output_id": "potato_stew",          "output_count": 1},
    {"name": "Cabbage Soup",         "ingredients": {"cabbage": 2, "onion": 1},                       "output_id": "cabbage_soup",         "output_count": 1},
    {"name": "Braised Eggplant",     "ingredients": {"eggplant": 1, "garlic": 1, "soy_sauce": 1},    "output_id": "braised_eggplant",     "output_count": 1},
    {"name": "Pepper Soup",          "ingredients": {"pepper": 1, "mushroom": 1, "tofu": 1},          "output_id": "pepper_soup",          "output_count": 1},
    {"name": "Onion Broth",          "ingredients": {"onion": 2, "ginger": 1},                        "output_id": "onion_broth",          "output_count": 1},
    {"name": "Potato Mushroom Stew", "ingredients": {"potato": 1, "mushroom": 2, "onion": 1},         "output_id": "potato_mushroom_stew", "output_count": 1},
    {"name": "Stuffed Cabbage",      "ingredients": {"cabbage": 1, "rice": 1, "egg": 1},              "output_id": "stuffed_cabbage",      "output_count": 1},
    {"name": "Braised Tofu",         "ingredients": {"tofu": 1, "bok_choy": 1, "soy_sauce": 1},       "output_id": "braised_tofu",         "output_count": 1},
    {"name": "Pepper Pot",           "ingredients": {"pepper": 2, "chili": 1, "garlic": 1},           "output_id": "pepper_pot",           "output_count": 1},
    {"name": "Harvest Stew",      "ingredients": {"carrot": 1, "potato": 1, "cabbage": 1},          "output_id": "harvest_stew",     "output_count": 1},
    {"name": "Beet Soup",         "ingredients": {"beet": 2, "onion": 1},                            "output_id": "beet_soup",        "output_count": 1},
    {"name": "Root Medley",       "ingredients": {"beet": 1, "turnip": 1, "carrot": 1},              "output_id": "root_medley",      "output_count": 1},
    {"name": "Radish Kimchi",     "ingredients": {"radish": 2, "chili": 1, "garlic": 1},             "output_id": "radish_kimchi",    "output_count": 1},
    {"name": "Stuffed Zucchini",  "ingredients": {"zucchini": 2, "rice": 1},                         "output_id": "stuffed_zucchini", "output_count": 1},
    {"name": "Garden Soup",       "ingredients": {"broccoli": 1, "pea": 1, "celery": 1},             "output_id": "garden_soup",      "output_count": 1},
    # --- Desert clay pot ---
    {"name": "Date Palm Broth",  "ingredients": {"date_palm_fruit": 2, "onion": 1},                "output_id": "date_palm_broth",  "output_count": 1},
]

# ---------------------------------------------------------------------------
# Desert Forge recipes (ingredient dict → output, same pattern as cooking stations)
# ---------------------------------------------------------------------------

FORGE_RECIPES = [
    {"name": "Desert Glass",  "ingredients": {"sand_grain": 3},                              "output_id": "desert_glass",  "output_count": 1},
    {"name": "Sandstone",     "ingredients": {"sand_grain": 4, "stone_chip": 1},             "output_id": "sandstone",     "output_count": 2},
    {"name": "Tempered Iron", "ingredients": {"iron_chunk": 2, "coal": 3},                   "output_id": "tempered_iron", "output_count": 1},
    {"name": "Cactus Fiber",  "ingredients": {"cactus_spine": 3},                            "output_id": "cactus_fiber",  "output_count": 2},
    {"name": "Agave Syrup",   "ingredients": {"agave": 3},                                   "output_id": "agave_syrup",   "output_count": 1},
]

# ---------------------------------------------------------------------------
# Shaped 3x3 grid recipes
# ---------------------------------------------------------------------------

RECIPES = [
    # --- Utility ---
    {
        "name": "Ladder",
        "pattern": [
            ["lumber", None, None],
            [None,     None, None],
            [None,     None, None],
        ],
        "output_id":    "ladder_item",
        "output_count": 5,
    },
    {
        "name": "Diamond",
        "pattern": [
            [None,   "ruby", None],
            ["ruby",   None, "ruby"],
            [None,   "ruby", None],
        ],
        "output_id":    "diamond",
        "output_count": 1,
    },
    # --- Tools ---
    {
        "name": "Stone Pickaxe",
        "pattern": [
            ["stone_chip",  "stone_chip",  "stone_chip"],
            [None,          "lumber",      None        ],
            [None,          "lumber",      None        ],
        ],
        "output_id":    "stone_pickaxe",
        "output_count": 1,
    },
    {
        "name": "Iron Pickaxe",
        "pattern": [
            ["iron_chunk",  "iron_chunk",  "iron_chunk"],
            [None,          "lumber",      None        ],
            [None,          "lumber",      None        ],
        ],
        "output_id":    "iron_pickaxe",
        "output_count": 1,
    },
    {
        "name": "Gold Pickaxe",
        "pattern": [
            ["gold_nugget", "gold_nugget", "gold_nugget"],
            [None,          "lumber",      None         ],
            [None,          "lumber",      None         ],
        ],
        "output_id":    "gold_pickaxe",
        "output_count": 1,
    },
    # --- Axes ---
    {
        "name": "Stone Axe",
        "pattern": [
            ["stone_chip", "stone_chip", None],
            ["stone_chip", "lumber",     None],
            [None,         "lumber",     None],
        ],
        "output_id":    "stone_axe",
        "output_count": 1,
    },
    {
        "name": "Iron Axe",
        "pattern": [
            ["iron_chunk", "iron_chunk", None],
            ["iron_chunk", "lumber",     None],
            [None,         "lumber",     None],
        ],
        "output_id":    "iron_axe",
        "output_count": 1,
    },
    {
        "name": "Gold Axe",
        "pattern": [
            ["gold_nugget", "gold_nugget", None],
            ["gold_nugget", "lumber",      None],
            [None,          "lumber",      None],
        ],
        "output_id":    "gold_axe",
        "output_count": 1,
    },
    # --- Animal harvesting tools ---
    {
        "name": "Shears",
        "pattern": [
            [None,         "iron_chunk", None       ],
            ["iron_chunk", None,         None       ],
            [None,         None,         None       ],
        ],
        "output_id":    "shears",
        "output_count": 1,
    },
    {
        "name": "Bucket",
        "pattern": [
            ["iron_chunk", None,         "iron_chunk"],
            [None,         "iron_chunk", None        ],
            [None,         None,         None        ],
        ],
        "output_id":    "bucket",
        "output_count": 1,
    },
    # --- Refinery equipment ---
    {
        "name": "Rock Tumbler",
        "pattern": [
            ["iron_chunk",  "stone_chip", "iron_chunk"],
            ["stone_chip",  "stone_chip", "stone_chip"],
            ["iron_chunk",  None,         "iron_chunk"],
        ],
        "output_id":    "tumbler_item",
        "output_count": 1,
    },
    {
        "name": "Stone Crusher",
        "pattern": [
            ["gold_nugget", "iron_chunk",  "gold_nugget"],
            ["iron_chunk",  "iron_chunk",  "iron_chunk" ],
            ["gold_nugget", "iron_chunk",  "gold_nugget"],
        ],
        "output_id":    "crusher_item",
        "output_count": 1,
    },
    {
        "name": "Gem Cutter",
        "pattern": [
            ["crystal_shard", "gold_nugget",   "crystal_shard"],
            ["gold_nugget",   "crystal_shard", "gold_nugget"  ],
            ["crystal_shard", "gold_nugget",   "crystal_shard"],
        ],
        "output_id":    "gem_cutter_item",
        "output_count": 1,
    },
    {
        "name": "Alchemical Kiln",
        "pattern": [
            ["crystal_shard", "ruby",          "crystal_shard"],
            ["crystal_shard", "crystal_shard", "crystal_shard"],
            ["crystal_shard", "ruby",          "crystal_shard"],
        ],
        "output_id":    "kiln_item",
        "output_count": 1,
    },
    {
        "name": "Resonance Chamber",
        "pattern": [
            ["obsidian_slab", "ruby",          "obsidian_slab"],
            ["ruby",          "obsidian_slab", "ruby"         ],
            ["obsidian_slab", "ruby",          "obsidian_slab"],
        ],
        "output_id":    "resonance_item",
        "output_count": 1,
    },
    {
        "name": "Bakery",
        "pattern": [
            ["iron_chunk", "coal",       "iron_chunk"],
            ["stone_chip", "coal",       "stone_chip"],
            ["iron_chunk", "stone_chip", "iron_chunk"],
        ],
        "output_id":    "bakery_item",
        "output_count": 1,
    },
    {
        "name": "Wok",
        "pattern": [
            ["iron_chunk", None,         "iron_chunk"],
            [None,         "iron_chunk", None        ],
            ["stone_chip", "coal",       "stone_chip"],
        ],
        "output_id":    "wok_item",
        "output_count": 1,
    },
    {
        "name": "Steamer",
        "pattern": [
            ["lumber",     "lumber",     "lumber"    ],
            ["lumber",     None,         "lumber"    ],
            ["iron_chunk", "iron_chunk", "iron_chunk"],
        ],
        "output_id":    "steamer_item",
        "output_count": 1,
    },
    {
        "name": "Noodle Pot",
        "pattern": [
            ["iron_chunk", "coal",       "iron_chunk"],
            ["iron_chunk", None,         "iron_chunk"],
            [None,         "stone_chip", None        ],
        ],
        "output_id":    "noodle_pot_item",
        "output_count": 1,
    },
    {
        "name": "BBQ Grill",
        "pattern": [
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            ["stone_chip", "coal",       "stone_chip"],
            ["iron_chunk", None,         "iron_chunk"],
        ],
        "output_id":    "bbq_grill_item",
        "output_count": 1,
    },
    {
        "name": "Clay Pot",
        "pattern": [
            ["stone_chip", "coal",       "stone_chip"],
            ["stone_chip", None,         "stone_chip"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "clay_pot_item",
        "output_count": 1,
    },
    {
        "name": "Desert Forge",
        "pattern": [
            ["stone_chip",  "coal",       "stone_chip"],
            ["stone_chip",  "iron_chunk", "stone_chip"],
            ["stone_chip",  "coal",       "stone_chip"],
        ],
        "output_id":    "desert_forge_item",
        "output_count": 1,
    },
    # --- Tempered tools ---
    {
        "name": "Tempered Pickaxe",
        "pattern": [
            ["tempered_iron", "tempered_iron", "tempered_iron"],
            [None,            "lumber",        None           ],
            [None,            "lumber",        None           ],
        ],
        "output_id":    "tempered_pickaxe",
        "output_count": 1,
    },
    {
        "name": "Tempered Axe",
        "pattern": [
            ["tempered_iron", "tempered_iron", None],
            ["tempered_iron", "lumber",        None],
            [None,            "lumber",        None],
        ],
        "output_id":    "tempered_axe",
        "output_count": 1,
    },
    # --- Fences & Doors ---
    {
        "name": "Wood Fence",
        "pattern": [
            ["lumber", "lumber", None],
            ["lumber", "lumber", None],
            [None,     None,     None],
        ],
        "output_id":    "wood_fence",
        "output_count": 4,
    },
    {
        "name": "Iron Fence",
        "pattern": [
            ["iron_chunk", "iron_chunk", None],
            ["iron_chunk", "iron_chunk", None],
            [None,         None,         None],
        ],
        "output_id":    "iron_fence",
        "output_count": 4,
    },
    {
        "name": "Wood Door",
        "pattern": [
            ["lumber", "lumber", None],
            ["lumber", "lumber", None],
            ["lumber", "lumber", None],
        ],
        "output_id":    "wood_door",
        "output_count": 1,
    },
    {
        "name": "Iron Door",
        "pattern": [
            ["iron_chunk", "iron_chunk", None],
            ["iron_chunk", "iron_chunk", None],
            ["iron_chunk", "iron_chunk", None],
        ],
        "output_id":    "iron_door",
        "output_count": 1,
    },
    # --- Furniture ---
    {
        "name": "Bed",
        "pattern": [
            ["wool",   "wool",   "wool"  ],
            ["lumber", "lumber", "lumber"],
            [None,     None,     None   ],
        ],
        "output_id":    "bed",
        "output_count": 1,
    },
    # --- Automations ---
    {
        "name": "Coal Miner",
        "pattern": [
            ["iron_chunk", "iron_chunk", "iron_chunk"],
            ["iron_chunk", "coal",       None        ],
            ["stone_chip", "stone_chip", None        ],
        ],
        "output_id":    "coal_miner_item",
        "output_count": 1,
    },
    {
        "name": "Iron Miner",
        "pattern": [
            ["iron_chunk", "gold_nugget", "iron_chunk"],
            ["iron_chunk", "coal",        "iron_chunk"],
            ["iron_chunk", "gold_nugget", "iron_chunk"],
        ],
        "output_id":    "iron_miner_item",
        "output_count": 1,
    },
    {
        "name": "Crystal Miner",
        "pattern": [
            ["crystal_shard", "iron_chunk",  "crystal_shard"],
            ["iron_chunk",    "gold_nugget", "iron_chunk"   ],
            ["crystal_shard", "iron_chunk",  "crystal_shard"],
        ],
        "output_id":    "crystal_miner_item",
        "output_count": 1,
    },
    {
        "name": "Chest",
        "pattern": [
            ["lumber", "lumber",     "lumber"],
            ["lumber", None,         "lumber"],
            ["lumber", "iron_chunk", "lumber"],
        ],
        "output_id":    "chest_item",
        "output_count": 1,
    },
    # --- Farm Bots ---
    {
        "name": "Farm Bot",
        "pattern": [
            ["lumber",     "iron_chunk", "lumber"    ],
            ["iron_chunk", "coal",       "iron_chunk"],
            ["lumber",     "iron_chunk", "lumber"    ],
        ],
        "output_id":    "farm_bot_item",
        "output_count": 1,
    },
    {
        "name": "Iron Farm Bot",
        "pattern": [
            ["iron_chunk", "gold_nugget", "iron_chunk"],
            ["gold_nugget", "iron_chunk", "gold_nugget"],
            ["iron_chunk", "gold_nugget", "iron_chunk"],
        ],
        "output_id":    "iron_farm_bot_item",
        "output_count": 1,
    },
    {
        "name": "Crystal Farm Bot",
        "pattern": [
            ["crystal_shard", "gold_nugget",   "crystal_shard"],
            ["gold_nugget",   "iron_chunk",     "gold_nugget"  ],
            ["crystal_shard", "gold_nugget",    "crystal_shard"],
        ],
        "output_id":    "crystal_farm_bot_item",
        "output_count": 1,
    },
    # --- Construction Equipment ---
    {
        "name": "Empty Barrel",
        "pattern": [
            ["iron_chunk", None,          "iron_chunk"],
            ["iron_chunk", None,          "iron_chunk"],
            ["iron_chunk", "iron_chunk",  "iron_chunk"],
        ],
        "output_id":    "empty_barrel",
        "output_count": 1,
    },
    {
        "name": "Backhoe",
        "pattern": [
            ["iron_chunk", "lumber",      "iron_chunk"],
            ["iron_chunk", "coal",        "iron_chunk"],
            ["iron_chunk", "iron_chunk",  "iron_chunk"],
        ],
        "output_id":    "backhoe_item",
        "output_count": 1,
    },
    {
        "name": "Hunting Knife",
        "pattern": [
            [None, "stone_chip", None],
            [None, "lumber",     None],
            [None, None,         None],
        ],
        "output_id":    "hunting_knife",
        "output_count": 1,
    },
    # --- Fishing ---
    {
        "name": "Fishing Pole",
        "pattern": [
            [None,     None,     "lumber"],
            [None,     "lumber", None    ],
            ["lumber", None,     None    ],
        ],
        "output_id":    "fishing_pole",
        "output_count": 1,
    },
    # --- Bird furniture ---
    {
        "name": "Bird Feeder",
        "pattern": [
            ["lumber", "lumber", "lumber"],
            [None,     "lumber", None    ],
            ["lumber", "lumber", "lumber"],
        ],
        "output_id":    "bird_feeder",
        "output_count": 1,
    },
    {
        "name": "Bird Bath",
        "pattern": [
            ["stone_chip", "stone_chip", "stone_chip"],
            [None,         "stone_chip", None        ],
            [None,         "stone_chip", None        ],
        ],
        "output_id":    "bird_bath",
        "output_count": 1,
    },
    # --- Coffee equipment ---
    {
        "name": "Coffee Roaster",
        "pattern": [
            ["stone_chip",  "iron_chunk",  "stone_chip"],
            ["iron_chunk",  "coal",        "iron_chunk"],
            ["stone_chip",  "lumber",      "stone_chip"],
        ],
        "output_id":    "roaster_item",
        "output_count": 1,
    },
    {
        "name": "Blend Station",
        "pattern": [
            ["lumber",     "lumber",     "lumber"    ],
            ["iron_chunk", None,         "iron_chunk"],
            ["stone_chip", "stone_chip", "stone_chip"],
        ],
        "output_id":    "blend_station_item",
        "output_count": 1,
    },
    {
        "name": "Brew Station",
        "pattern": [
            ["iron_chunk", "lumber",     "iron_chunk"],
            ["lumber",     None,         "lumber"    ],
            ["stone_chip", "iron_chunk", "stone_chip"],
        ],
        "output_id":    "brew_station_item",
        "output_count": 1,
    },
    {
        "name": "Fossil Prep Table",
        "pattern": [
            ["stone_chip", "stone_chip", "stone_chip"],
            ["lumber",     "lumber",     "lumber"    ],
            ["lumber",     "lumber",     "lumber"    ],
        ],
        "output_id":    "fossil_table_item",
        "output_count": 1,
    },
]


# Maps output_id -> research node_id required before that recipe is available.
RESEARCH_LOCKED_RECIPES = {
    "farm_bot_item":         "soil_prep",
    "iron_farm_bot_item":    "selective_breeding",
    "crystal_farm_bot_item": "agri_automation",
    "roaster_item":          "coffee_basics",
    "blend_station_item":    "blend_arts",
    "brew_station_item":     "brew_expertise",
    "bird_feeder":           "bird_watching",
    "bird_bath":             "bird_sanctuary",
}


def match_recipe(grid):
    """Return (output_id, output_count) if grid matches a shaped recipe, else (None, 0)."""
    for recipe in RECIPES:
        pat = recipe["pattern"]
        if all(grid[r][c] == pat[r][c] for r in range(3) for c in range(3)):
            return recipe["output_id"], recipe["output_count"]
    return None, 0


def craft_costs(grid):
    """Return {item_id: count} for all non-None cells in the grid."""
    costs = {}
    for row in grid:
        for cell in row:
            if cell:
                costs[cell] = costs.get(cell, 0) + 1
    return costs


def can_craft(grid, inventory):
    """Return True if grid matches a recipe and inventory has the required items."""
    out_id, _ = match_recipe(grid)
    if not out_id:
        return False
    return all(inventory.get(iid, 0) >= needed
               for iid, needed in craft_costs(grid).items())


def is_research_locked(out_id, research):
    """Return True if out_id requires research that hasn't been unlocked."""
    if research is None or out_id not in RESEARCH_LOCKED_RECIPES:
        return False
    node = research.nodes.get(RESEARCH_LOCKED_RECIPES[out_id])
    return node is None or not node.unlocked


def can_craft_with_research(grid, inventory, research=None):
    """Like can_craft but also checks research locks."""
    out_id, _ = match_recipe(grid)
    if not out_id:
        return False
    if is_research_locked(out_id, research):
        return False
    return all(inventory.get(iid, 0) >= needed
               for iid, needed in craft_costs(grid).items())
