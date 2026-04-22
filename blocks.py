AIR              = 0
GRASS            = 1
DIRT             = 2
STONE            = 3
COAL_ORE         = 4
IRON_ORE         = 5
GOLD_ORE         = 6
CRYSTAL_ORE      = 7
RUBY_ORE         = 8
OBSIDIAN         = 9
BEDROCK          = 10
GATE_MID         = 11  # zone barrier: depth ~40, unlocked by mid_access research
GATE_DEEP        = 12  # zone barrier: depth ~100, unlocked by deep_access research
GATE_CORE        = 13  # zone barrier: depth ~160, unlocked by core_access research
TREE_LOG         = 14
TREE_LEAVES      = 15
ROCK_DEPOSIT     = 16  # special: mine → generates unique Rock object, no item drop
TUMBLER_BLOCK    = 17  # placed Rock Tumbler equipment
CRUSHER_BLOCK    = 18  # placed Stone Crusher equipment
GEM_CUTTER_BLOCK = 19  # placed Gem Cutter equipment
KILN_BLOCK       = 20  # placed Alchemical Kiln equipment
RESONANCE_BLOCK  = 21  # placed Resonance Chamber equipment
POLISHED_STONE_BLOCK = 22  # decorative placed polished stone
LADDER           = 23  # climbable; non-solid, player moves through it
SUPPORT          = 24  # structural support beam; prevents adjacent PHYSICS_BLOCKS from falling
WATER            = 25  # liquid; non-solid, flows into empty spaces, ignores supports
IRON_SUPPORT     = 26  # iron support beam; wider coverage than wood support
DIAMOND_SUPPORT  = 27  # diamond support beam; maximum coverage
SAPLING               = 28  # placeable sapling; grows into a tree when it has sky view
STRAWBERRY_BUSH       = 29  # surface bush; drops strawberry_seed, chance of strawberry
WHEAT_BUSH            = 30  # surface bush; drops wheat_seed, chance of wheat
STRAWBERRY_CROP_YOUNG = 31  # planted from seed; grows into mature
STRAWBERRY_CROP_MATURE= 32  # drops strawberry + seeds when mined
WHEAT_CROP_YOUNG      = 33
WHEAT_CROP_MATURE     = 34  # drops wheat + seeds when mined
BAKERY_BLOCK          = 35  # placed Bakery oven; converts ingredients → food
CARROT_BUSH           = 36  # surface bush; drops carrot_seed
TOMATO_BUSH           = 37  # surface bush; drops tomato_seed
CORN_BUSH             = 38  # surface bush; drops corn_seed
PUMPKIN_BUSH          = 39  # surface bush; drops pumpkin_seed
APPLE_BUSH            = 40  # surface bush; drops apple_seed
CARROT_CROP_YOUNG     = 41
CARROT_CROP_MATURE    = 42  # drops carrot + seeds when mined
TOMATO_CROP_YOUNG     = 43
TOMATO_CROP_MATURE    = 44  # drops tomato + seeds when mined
CORN_CROP_YOUNG       = 45
CORN_CROP_MATURE      = 46  # drops corn + seeds when mined
PUMPKIN_CROP_YOUNG    = 47
PUMPKIN_CROP_MATURE   = 48  # drops pumpkin + seeds when mined
APPLE_CROP_YOUNG      = 49
APPLE_CROP_MATURE     = 50  # drops apple + seeds when mined

# --- Biodome tree species (9 additional + existing oak = 10 total) ---
PINE_LOG       = 51
PINE_LEAVES    = 52
BIRCH_LOG      = 53
BIRCH_LEAVES   = 54
JUNGLE_LOG     = 55
JUNGLE_LEAVES  = 56
WILLOW_LOG     = 57
WILLOW_LEAVES  = 58
REDWOOD_LOG    = 59
REDWOOD_LEAVES = 60
PALM_LOG       = 61
PALM_LEAVES    = 62
ACACIA_LOG     = 63
ACACIA_LEAVES  = 64
DEAD_LOG       = 65   # skeletal wasteland tree — no leaves
MUSHROOM_STEM  = 66
MUSHROOM_CAP   = 67
NPC_QUEST_BLOCK = 68  # Rock Quest NPC marker (impassable, visual anchor)
NPC_TRADE_BLOCK = 69  # Trade NPC marker (impassable, visual anchor)
# --- Chinese cuisine crops ---
RICE_BUSH           = 70  # surface bush; drops rice_seed
GINGER_BUSH         = 71  # surface bush; drops ginger_seed
BOK_CHOY_BUSH       = 72  # surface bush; drops bok_choy_seed
GARLIC_BUSH         = 73  # surface bush; drops garlic_seed
RICE_CROP_YOUNG     = 74
RICE_CROP_MATURE    = 75  # drops rice + seeds when mined
GINGER_CROP_YOUNG   = 76
GINGER_CROP_MATURE  = 77  # drops ginger + seeds when mined
BOK_CHOY_CROP_YOUNG = 78
BOK_CHOY_CROP_MATURE= 79  # drops bok_choy + seeds when mined
GARLIC_CROP_YOUNG   = 80
GARLIC_CROP_MATURE  = 81  # drops garlic + seeds when mined
# --- Chinese cooking equipment ---
WOK_BLOCK          = 82  # placed Wok; stir-fry station
STEAMER_BLOCK      = 83  # placed Steamer; steam cooking station
NOODLE_POT_BLOCK   = 84  # placed Noodle Pot; noodle/soup station
# --- Extended crop supply chain ---
SCALLION_BUSH      = 85
CHILI_BUSH         = 86
SCALLION_CROP_YOUNG  = 87
SCALLION_CROP_MATURE = 88
CHILI_CROP_YOUNG   = 89
CHILI_CROP_MATURE  = 90
# --- New cooking equipment ---
BBQ_GRILL_BLOCK    = 91  # placed BBQ Grill; open-fire grilling station
CLAY_POT_BLOCK     = 92  # placed Clay Pot; slow-braised cooking station
# --- New crop supply chains ---
PEPPER_BUSH        = 93
ONION_BUSH         = 94
POTATO_BUSH        = 95
EGGPLANT_BUSH      = 96
CABBAGE_BUSH       = 97
PEPPER_CROP_YOUNG  = 98
PEPPER_CROP_MATURE = 99
ONION_CROP_YOUNG   = 100
ONION_CROP_MATURE  = 101
POTATO_CROP_YOUNG  = 102
POTATO_CROP_MATURE = 103
EGGPLANT_CROP_YOUNG  = 104
EGGPLANT_CROP_MATURE = 105
CABBAGE_CROP_YOUNG   = 106
CABBAGE_CROP_MATURE  = 107
HOUSE_WALL           = 108  # city house wall block; not a physics block so it won't collapse
HOUSE_ROOF           = 109  # city house roof block
WILDFLOWER_PATCH     = 110  # surface collectable; interact → generates unique Wildflower object
# --- Cave blocks ---
CRACKED_STONE = 111   # unstable ceiling; in PHYSICS_BLOCKS, cracks drawn by renderer
STALACTITE    = 112   # decorative spike hanging from cave ceiling (solid, minable)
STALAGMITE    = 113   # decorative spike growing from cave floor (solid, minable)
CAVE_MOSS     = 114   # mossy floor/wall coating in shallow/wet caves; soft, non-physics
CAVE_CRYSTAL  = 115   # glowing crystal cluster growing from walls in deep/crystal biomes
GRAVEL        = 116   # loose rock; in PHYSICS_BLOCKS, falls freely when unsupported
CAVE_MUSHROOM    = 117   # collectible mushroom; only spawns on cave floors
EMBER_CAP        = 118   # orange-red dome; igneous caves
PALE_GHOST       = 119   # ghostly white dome; void/shallow caves
GOLD_CHANTERELLE = 120   # golden dome; rare; sedimentary caves
COBALT_CAP       = 121   # deep blue dome; crystal caves
MOSSY_CAP        = 122   # olive-green dome; shallow damp caves
VIOLET_CROWN     = 123   # purple dome; rare; void caves
BLOOD_CAP        = 124   # deep crimson dome; igneous caves
SULFUR_DOME      = 125   # bright yellow dome; igneous/sedimentary
IVORY_BELL       = 126   # cream narrow bell; any cave
ASH_BELL         = 127   # ash-gray narrow bell; ferrous/void caves
TEAL_BELL        = 128   # teal bell; rare; crystal caves
RUST_SHELF       = 129   # rusty bracket shelf; ferrous/igneous
COPPER_SHELF     = 130   # verdigris bracket shelf; sedimentary
OBSIDIAN_SHELF   = 131   # near-black bracket; rare; deep caves
COAL_PUFF        = 132   # dark gray puffball; igneous zones
STONE_PUFF       = 133   # light gray puffball; any cave
AMBER_PUFF       = 134   # warm amber puffball; sedimentary
SULFUR_TUFT      = 135   # yellow cluster; igneous caves
HONEY_CLUSTER    = 136   # amber cluster; sedimentary caves
CORAL_TUFT       = 137   # coral pink cluster; rare; crystal caves
BONE_STALK       = 138   # tall cream bell; ferrous caves
MAGMA_CAP        = 139   # near-black with glow rim; rare; deep igneous
DEEP_INK         = 140   # dark purple dome; rare; deep void
BIOLUME          = 141   # cyan glowing dome; rare; deep crystal

WOOD_FENCE       = 142
IRON_FENCE       = 143
WOOD_DOOR_CLOSED = 144
WOOD_DOOR_OPEN   = 145
IRON_DOOR_CLOSED = 146
IRON_DOOR_OPEN   = 147
BED              = 148
CHEST_BLOCK      = 149

OPEN_DOORS = {WOOD_DOOR_OPEN, IRON_DOOR_OPEN}

CAVE_MUSHROOMS = {
    CAVE_MUSHROOM, EMBER_CAP, PALE_GHOST, GOLD_CHANTERELLE, COBALT_CAP,
    MOSSY_CAP, VIOLET_CROWN, BLOOD_CAP, SULFUR_DOME, IVORY_BELL,
    ASH_BELL, TEAL_BELL, RUST_SHELF, COPPER_SHELF, OBSIDIAN_SHELF,
    COAL_PUFF, STONE_PUFF, AMBER_PUFF, SULFUR_TUFT, HONEY_CLUSTER,
    CORAL_TUFT, BONE_STALK, MAGMA_CAP, DEEP_INK, BIOLUME,
}

ALL_LOGS   = {TREE_LOG, PINE_LOG, BIRCH_LOG, JUNGLE_LOG, WILLOW_LOG,
              REDWOOD_LOG, PALM_LOG, ACACIA_LOG, DEAD_LOG, MUSHROOM_STEM}
ALL_LEAVES = {TREE_LEAVES, PINE_LEAVES, BIRCH_LEAVES, JUNGLE_LEAVES, WILLOW_LEAVES,
              REDWOOD_LEAVES, PALM_LEAVES, ACACIA_LEAVES, MUSHROOM_CAP}
# Maps each leaf block to its paired log for decay checks
LEAF_LOG_MAP = {
    TREE_LEAVES:    TREE_LOG,
    PINE_LEAVES:    PINE_LOG,
    BIRCH_LEAVES:   BIRCH_LOG,
    JUNGLE_LEAVES:  JUNGLE_LOG,
    WILLOW_LEAVES:  WILLOW_LOG,
    REDWOOD_LEAVES: REDWOOD_LOG,
    PALM_LEAVES:    PALM_LOG,
    ACACIA_LEAVES:  ACACIA_LOG,
    MUSHROOM_CAP:   MUSHROOM_STEM,
}

EQUIPMENT_BLOCKS = {TUMBLER_BLOCK, CRUSHER_BLOCK, GEM_CUTTER_BLOCK, KILN_BLOCK, RESONANCE_BLOCK, BAKERY_BLOCK,
                    WOK_BLOCK, STEAMER_BLOCK, NOODLE_POT_BLOCK, BBQ_GRILL_BLOCK, CLAY_POT_BLOCK}
RESOURCE_BLOCKS  = {COAL_ORE, IRON_ORE, GOLD_ORE, CRYSTAL_ORE, RUBY_ORE, OBSIDIAN, ROCK_DEPOSIT}
PHYSICS_BLOCKS   = {GRASS, DIRT, CRACKED_STONE, GRAVEL}  # blocks that can fall when unsupported
ALL_SUPPORTS     = {SUPPORT, IRON_SUPPORT, DIAMOND_SUPPORT}
SUPPORT_RANGE    = {SUPPORT: 2, IRON_SUPPORT: 5, DIAMOND_SUPPORT: 10}  # half-width in blocks
BUSH_BLOCKS       = {STRAWBERRY_BUSH, WHEAT_BUSH, CARROT_BUSH, TOMATO_BUSH, CORN_BUSH, PUMPKIN_BUSH, APPLE_BUSH,
                     RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, GARLIC_BUSH, SCALLION_BUSH, CHILI_BUSH,
                     PEPPER_BUSH, ONION_BUSH, POTATO_BUSH, EGGPLANT_BUSH, CABBAGE_BUSH}
YOUNG_CROP_BLOCKS = {STRAWBERRY_CROP_YOUNG, WHEAT_CROP_YOUNG, CARROT_CROP_YOUNG, TOMATO_CROP_YOUNG, CORN_CROP_YOUNG, PUMPKIN_CROP_YOUNG, APPLE_CROP_YOUNG,
                     RICE_CROP_YOUNG, GINGER_CROP_YOUNG, BOK_CHOY_CROP_YOUNG, GARLIC_CROP_YOUNG,
                     SCALLION_CROP_YOUNG, CHILI_CROP_YOUNG,
                     PEPPER_CROP_YOUNG, ONION_CROP_YOUNG, POTATO_CROP_YOUNG, EGGPLANT_CROP_YOUNG, CABBAGE_CROP_YOUNG}
MATURE_CROP_BLOCKS= {STRAWBERRY_CROP_MATURE, WHEAT_CROP_MATURE, CARROT_CROP_MATURE, TOMATO_CROP_MATURE, CORN_CROP_MATURE, PUMPKIN_CROP_MATURE, APPLE_CROP_MATURE,
                     RICE_CROP_MATURE, GINGER_CROP_MATURE, BOK_CHOY_CROP_MATURE, GARLIC_CROP_MATURE,
                     SCALLION_CROP_MATURE, CHILI_CROP_MATURE,
                     PEPPER_CROP_MATURE, ONION_CROP_MATURE, POTATO_CROP_MATURE, EGGPLANT_CROP_MATURE, CABBAGE_CROP_MATURE}
CROP_BLOCKS       = YOUNG_CROP_BLOCKS | MATURE_CROP_BLOCKS

# Perennial crops regrow after harvest (each harvest has ~33% chance to die)
PERENNIAL_CROP_MATURE = {
    STRAWBERRY_CROP_MATURE, APPLE_CROP_MATURE, TOMATO_CROP_MATURE,
    PEPPER_CROP_MATURE, CHILI_CROP_MATURE, EGGPLANT_CROP_MATURE,
}

# Reverse mapping: mature → young, used for perennial regrowth
MATURE_TO_YOUNG_CROP = {
    STRAWBERRY_CROP_MATURE: STRAWBERRY_CROP_YOUNG,
    WHEAT_CROP_MATURE:      WHEAT_CROP_YOUNG,
    CARROT_CROP_MATURE:     CARROT_CROP_YOUNG,
    TOMATO_CROP_MATURE:     TOMATO_CROP_YOUNG,
    CORN_CROP_MATURE:       CORN_CROP_YOUNG,
    PUMPKIN_CROP_MATURE:    PUMPKIN_CROP_YOUNG,
    APPLE_CROP_MATURE:      APPLE_CROP_YOUNG,
    RICE_CROP_MATURE:       RICE_CROP_YOUNG,
    GINGER_CROP_MATURE:     GINGER_CROP_YOUNG,
    BOK_CHOY_CROP_MATURE:   BOK_CHOY_CROP_YOUNG,
    GARLIC_CROP_MATURE:     GARLIC_CROP_YOUNG,
    SCALLION_CROP_MATURE:   SCALLION_CROP_YOUNG,
    CHILI_CROP_MATURE:      CHILI_CROP_YOUNG,
    PEPPER_CROP_MATURE:     PEPPER_CROP_YOUNG,
    ONION_CROP_MATURE:      ONION_CROP_YOUNG,
    POTATO_CROP_MATURE:     POTATO_CROP_YOUNG,
    EGGPLANT_CROP_MATURE:   EGGPLANT_CROP_YOUNG,
    CABBAGE_CROP_MATURE:    CABBAGE_CROP_YOUNG,
}

BLOCKS = {
    AIR:              {"name": "Air",               "hardness": 0,            "color": None,            "drop": None},
    GRASS:            {"name": "Grass",             "hardness": 1,            "color": (58, 154, 58),   "drop": "dirt_clump"},
    DIRT:             {"name": "Dirt",              "hardness": 1,            "color": (115, 77, 38),   "drop": "dirt_clump"},
    STONE:            {"name": "Stone",             "hardness": 2,            "color": (120, 120, 120), "drop": "stone_chip"},
    COAL_ORE:         {"name": "Coal Ore",          "hardness": 3,            "color": (50, 50, 50),    "drop": "coal"},
    IRON_ORE:         {"name": "Iron Ore",          "hardness": 4,            "color": (185, 140, 110), "drop": "iron_chunk"},
    GOLD_ORE:         {"name": "Gold Ore",          "hardness": 5,            "color": (218, 182, 55),  "drop": "gold_nugget"},
    CRYSTAL_ORE:      {"name": "Crystal Ore",       "hardness": 6,            "color": (90, 220, 220),  "drop": "crystal_shard"},
    RUBY_ORE:         {"name": "Ruby Ore",          "hardness": 7,            "color": (210, 35, 35),   "drop": "ruby"},
    OBSIDIAN:         {"name": "Obsidian",          "hardness": 9,            "color": (28, 14, 42),    "drop": "obsidian_slab"},
    BEDROCK:          {"name": "Bedrock",           "hardness": float('inf'), "color": (20, 20, 20),    "drop": None},
    GATE_MID:         {"name": "Zone Barrier",      "hardness": float('inf'), "color": (160, 90, 20),   "drop": None},
    GATE_DEEP:        {"name": "Zone Barrier",      "hardness": float('inf'), "color": (130, 55, 10),   "drop": None},
    GATE_CORE:        {"name": "Zone Barrier",      "hardness": float('inf'), "color": (110, 25, 5),    "drop": None},
    TREE_LOG:         {"name": "Tree Log",          "hardness": 2,            "color": (101, 67, 33),   "drop": "lumber"},
    TREE_LEAVES:      {"name": "Leaves",            "hardness": 1,            "color": (34, 120, 34),   "drop": "sapling", "drop_chance": 0.10},
    ROCK_DEPOSIT:     {"name": "Rock Deposit",      "hardness": 4,            "color": (105, 88, 75),   "drop": None},
    TUMBLER_BLOCK:    {"name": "Rock Tumbler",      "hardness": 1, "color": (160, 120, 80),  "drop": "tumbler_item"},
    CRUSHER_BLOCK:    {"name": "Stone Crusher",     "hardness": 1, "color": (100, 100, 100), "drop": "crusher_item"},
    GEM_CUTTER_BLOCK: {"name": "Gem Cutter",        "hardness": 1, "color": (80, 190, 190),  "drop": "gem_cutter_item"},
    KILN_BLOCK:       {"name": "Alchemical Kiln",   "hardness": 1, "color": (200, 80, 40),   "drop": "kiln_item"},
    RESONANCE_BLOCK:  {"name": "Resonance Chamber", "hardness": 1, "color": (100, 50, 200),  "drop": "resonance_item"},
    POLISHED_STONE_BLOCK: {"name": "Polished Stone", "hardness": 2,            "color": (200, 200, 215), "drop": "polished_stone"},
    LADDER:               {"name": "Ladder",          "hardness": 1,            "color": (139, 90,  43),  "drop": "ladder_item"},
    SUPPORT:              {"name": "Support",         "hardness": 1,            "color": (180, 140, 80),  "drop": "support_item"},
    WATER:                {"name": "Water",           "hardness": float('inf'), "color": (40, 110, 220),  "drop": None},
    IRON_SUPPORT:         {"name": "Iron Support",    "hardness": 2,            "color": (160, 170, 185), "drop": "iron_support_item"},
    DIAMOND_SUPPORT:      {"name": "Diamond Support", "hardness": 3,            "color": (100, 230, 220), "drop": "diamond_support_item"},
    SAPLING:              {"name": "Sapling",         "hardness": 1,            "color": (60, 180, 60),   "drop": "sapling"},
    STRAWBERRY_BUSH:        {"name": "Strawberry Bush",       "hardness": 0.5, "color": (60, 160, 60),  "drop": "strawberry_seed", "drop_chance": 1.0},
    WHEAT_BUSH:             {"name": "Wheat Bush",            "hardness": 0.5, "color": (180, 160, 60), "drop": "wheat_seed",       "drop_chance": 1.0},
    STRAWBERRY_CROP_YOUNG:  {"name": "Strawberry Crop",       "hardness": 0.5, "color": (80, 180, 80),  "drop": "strawberry_seed", "drop_chance": 1.0},
    STRAWBERRY_CROP_MATURE: {"name": "Strawberry Crop (Ripe)","hardness": 0.5, "color": (220, 50, 80),  "drop": "strawberry",      "drop_chance": 1.0},
    WHEAT_CROP_YOUNG:       {"name": "Wheat Crop",            "hardness": 0.5, "color": (200, 190, 80), "drop": "wheat_seed",      "drop_chance": 1.0},
    WHEAT_CROP_MATURE:      {"name": "Wheat Crop (Ripe)",     "hardness": 0.5, "color": (230, 210, 60), "drop": "wheat",           "drop_chance": 1.0},
    BAKERY_BLOCK:           {"name": "Bakery",                "hardness": 1,   "color": (180, 100, 50), "drop": "bakery_item"},
    CARROT_BUSH:            {"name": "Carrot Bush",           "hardness": 0.5, "color": (255, 140, 0),  "drop": "carrot_seed",   "drop_chance": 1.0},
    TOMATO_BUSH:            {"name": "Tomato Bush",           "hardness": 0.5, "color": (160, 50,  50), "drop": "tomato_seed",   "drop_chance": 1.0},
    CORN_BUSH:              {"name": "Corn Bush",             "hardness": 0.5, "color": (200, 180, 50), "drop": "corn_seed",     "drop_chance": 1.0},
    PUMPKIN_BUSH:           {"name": "Pumpkin Bush",          "hardness": 0.5, "color": (200, 100, 30), "drop": "pumpkin_seed",  "drop_chance": 1.0},
    APPLE_BUSH:             {"name": "Apple Bush",            "hardness": 0.5, "color": (60,  160, 60), "drop": "apple_seed",    "drop_chance": 1.0},
    CARROT_CROP_YOUNG:      {"name": "Carrot Crop",           "hardness": 0.5, "color": (80,  180, 80), "drop": "carrot_seed",   "drop_chance": 1.0},
    CARROT_CROP_MATURE:     {"name": "Carrot Crop (Ripe)",    "hardness": 0.5, "color": (255, 140, 0),  "drop": "carrot",        "drop_chance": 1.0},
    TOMATO_CROP_YOUNG:      {"name": "Tomato Crop",           "hardness": 0.5, "color": (80,  180, 80), "drop": "tomato_seed",   "drop_chance": 1.0},
    TOMATO_CROP_MATURE:     {"name": "Tomato Crop (Ripe)",    "hardness": 0.5, "color": (210, 50,  50), "drop": "tomato",        "drop_chance": 1.0},
    CORN_CROP_YOUNG:        {"name": "Corn Crop",             "hardness": 0.5, "color": (130, 170, 60), "drop": "corn_seed",     "drop_chance": 1.0},
    CORN_CROP_MATURE:       {"name": "Corn Crop (Ripe)",      "hardness": 0.5, "color": (230, 210, 55), "drop": "corn",          "drop_chance": 1.0},
    PUMPKIN_CROP_YOUNG:     {"name": "Pumpkin Crop",          "hardness": 0.5, "color": (80,  180, 80), "drop": "pumpkin_seed",  "drop_chance": 1.0},
    PUMPKIN_CROP_MATURE:    {"name": "Pumpkin Crop (Ripe)",   "hardness": 0.5, "color": (200, 100, 30), "drop": "pumpkin",       "drop_chance": 1.0},
    APPLE_CROP_YOUNG:       {"name": "Apple Crop",            "hardness": 0.5, "color": (80,  180, 80), "drop": "apple_seed",    "drop_chance": 1.0},
    APPLE_CROP_MATURE:      {"name": "Apple Crop (Ripe)",     "hardness": 0.5, "color": (180, 40,  40), "drop": "apple",         "drop_chance": 1.0},
    # Biodome trees
    PINE_LOG:      {"name": "Pine Log",          "hardness": 2, "color": (65,  42,  20),  "drop": "lumber"},
    PINE_LEAVES:   {"name": "Pine Needles",      "hardness": 1, "color": (18,  80,  18),  "drop": "sapling", "drop_chance": 0.10},
    BIRCH_LOG:     {"name": "Birch Log",         "hardness": 2, "color": (218, 210, 185), "drop": "lumber"},
    BIRCH_LEAVES:  {"name": "Birch Leaves",      "hardness": 1, "color": (140, 195, 80),  "drop": "sapling", "drop_chance": 0.10},
    JUNGLE_LOG:    {"name": "Jungle Log",        "hardness": 2, "color": (48,  32,  14),  "drop": "lumber"},
    JUNGLE_LEAVES: {"name": "Jungle Leaves",     "hardness": 1, "color": (28,  155, 28),  "drop": "sapling", "drop_chance": 0.10},
    WILLOW_LOG:    {"name": "Willow Log",        "hardness": 2, "color": (95,  75,  50),  "drop": "lumber"},
    WILLOW_LEAVES: {"name": "Willow Leaves",     "hardness": 1, "color": (118, 168, 88),  "drop": "sapling", "drop_chance": 0.10},
    REDWOOD_LOG:   {"name": "Redwood Log",       "hardness": 3, "color": (95,  38,  18),  "drop": "lumber"},
    REDWOOD_LEAVES:{"name": "Redwood Needles",   "hardness": 1, "color": (14,  70,  14),  "drop": "sapling", "drop_chance": 0.10},
    PALM_LOG:      {"name": "Palm Log",          "hardness": 2, "color": (158, 128, 68),  "drop": "lumber"},
    PALM_LEAVES:   {"name": "Palm Fronds",       "hardness": 1, "color": (48,  178, 78),  "drop": "sapling", "drop_chance": 0.10},
    ACACIA_LOG:    {"name": "Acacia Log",        "hardness": 2, "color": (148, 108, 58),  "drop": "lumber"},
    ACACIA_LEAVES: {"name": "Acacia Leaves",     "hardness": 1, "color": (108, 138, 48),  "drop": "sapling", "drop_chance": 0.10},
    DEAD_LOG:      {"name": "Dead Wood",         "hardness": 2, "color": (88,  82,  78),  "drop": "lumber"},
    MUSHROOM_STEM: {"name": "Mushroom Stem",     "hardness": 1, "color": (228, 218, 198), "drop": "mushroom", "drop_chance": 1.0},
    MUSHROOM_CAP:  {"name": "Mushroom Cap",      "hardness": 1, "color": (175, 38,  38),  "drop": "mushroom", "drop_chance": 0.5},
    NPC_QUEST_BLOCK: {"name": "Rock Collector", "hardness": float('inf'), "color": (200, 160, 80),  "drop": None},
    NPC_TRADE_BLOCK: {"name": "Trader",         "hardness": float('inf'), "color": (80,  150, 200), "drop": None},
    # --- Chinese cuisine crops ---
    RICE_BUSH:           {"name": "Rice Bush",          "hardness": 0.5, "color": (200, 200, 140), "drop": "rice_seed",     "drop_chance": 1.0},
    GINGER_BUSH:         {"name": "Ginger Bush",        "hardness": 0.5, "color": (200, 160,  60), "drop": "ginger_seed",   "drop_chance": 1.0},
    BOK_CHOY_BUSH:       {"name": "Bok Choy Bush",      "hardness": 0.5, "color": ( 50, 170,  80), "drop": "bok_choy_seed", "drop_chance": 1.0},
    GARLIC_BUSH:         {"name": "Garlic Bush",        "hardness": 0.5, "color": (230, 225, 200), "drop": "garlic_seed",   "drop_chance": 1.0},
    RICE_CROP_YOUNG:     {"name": "Rice Crop",          "hardness": 0.5, "color": (160, 200, 120), "drop": "rice_seed",     "drop_chance": 1.0},
    RICE_CROP_MATURE:    {"name": "Rice Crop (Ripe)",   "hardness": 0.5, "color": (220, 210, 150), "drop": "rice",          "drop_chance": 1.0},
    GINGER_CROP_YOUNG:   {"name": "Ginger Crop",        "hardness": 0.5, "color": (100, 170,  80), "drop": "ginger_seed",   "drop_chance": 1.0},
    GINGER_CROP_MATURE:  {"name": "Ginger Crop (Ripe)", "hardness": 0.5, "color": (200, 160,  60), "drop": "ginger",        "drop_chance": 1.0},
    BOK_CHOY_CROP_YOUNG: {"name": "Bok Choy Crop",      "hardness": 0.5, "color": ( 80, 180,  80), "drop": "bok_choy_seed", "drop_chance": 1.0},
    BOK_CHOY_CROP_MATURE:{"name": "Bok Choy (Ripe)",    "hardness": 0.5, "color": ( 50, 170,  80), "drop": "bok_choy",      "drop_chance": 1.0},
    GARLIC_CROP_YOUNG:   {"name": "Garlic Crop",        "hardness": 0.5, "color": (180, 210, 150), "drop": "garlic_seed",   "drop_chance": 1.0},
    GARLIC_CROP_MATURE:  {"name": "Garlic Crop (Ripe)", "hardness": 0.5, "color": (230, 225, 200), "drop": "garlic",        "drop_chance": 1.0},
    # --- Chinese cooking equipment ---
    WOK_BLOCK:           {"name": "Wok",                "hardness": 1,   "color": (70, 55, 45),   "drop": "wok_item"},
    STEAMER_BLOCK:       {"name": "Steamer",             "hardness": 1,   "color": (175, 150, 105),"drop": "steamer_item"},
    NOODLE_POT_BLOCK:    {"name": "Noodle Pot",          "hardness": 1,   "color": (85, 70, 55),   "drop": "noodle_pot_item"},
    # --- Extended crops ---
    SCALLION_BUSH:         {"name": "Scallion Bush",           "hardness": 0.5, "color": (60, 190, 80),  "drop": "scallion_seed", "drop_chance": 1.0},
    CHILI_BUSH:            {"name": "Chili Bush",              "hardness": 0.5, "color": (210, 55, 35),  "drop": "chili_seed",    "drop_chance": 1.0},
    SCALLION_CROP_YOUNG:   {"name": "Scallion Crop",           "hardness": 0.5, "color": (50, 185, 75),  "drop": "scallion_seed", "drop_chance": 1.0},
    SCALLION_CROP_MATURE:  {"name": "Scallion Crop (Ripe)",    "hardness": 0.5, "color": (70, 200, 95),  "drop": "scallion",      "drop_chance": 1.0},
    CHILI_CROP_YOUNG:      {"name": "Chili Crop",              "hardness": 0.5, "color": (80, 175, 75),  "drop": "chili_seed",    "drop_chance": 1.0},
    CHILI_CROP_MATURE:     {"name": "Chili Crop (Ripe)",       "hardness": 0.5, "color": (215, 50, 35),  "drop": "chili",         "drop_chance": 1.0},
    # --- New cooking equipment ---
    BBQ_GRILL_BLOCK:       {"name": "BBQ Grill",               "hardness": 1,   "color": (55, 45, 35),   "drop": "bbq_grill_item"},
    CLAY_POT_BLOCK:        {"name": "Clay Pot",                "hardness": 1,   "color": (170, 100, 65), "drop": "clay_pot_item"},
    # --- New crops ---
    PEPPER_BUSH:           {"name": "Pepper Bush",             "hardness": 0.5, "color": (220, 80, 40),  "drop": "pepper_seed",   "drop_chance": 1.0},
    ONION_BUSH:            {"name": "Onion Bush",              "hardness": 0.5, "color": (180, 155, 90), "drop": "onion_seed",    "drop_chance": 1.0},
    POTATO_BUSH:           {"name": "Potato Bush",             "hardness": 0.5, "color": (160, 130, 70), "drop": "potato_seed",   "drop_chance": 1.0},
    EGGPLANT_BUSH:         {"name": "Eggplant Bush",           "hardness": 0.5, "color": (100, 50, 140), "drop": "eggplant_seed", "drop_chance": 1.0},
    CABBAGE_BUSH:          {"name": "Cabbage Bush",            "hardness": 0.5, "color": (80, 160, 90),  "drop": "cabbage_seed",  "drop_chance": 1.0},
    PEPPER_CROP_YOUNG:     {"name": "Pepper Crop",             "hardness": 0.5, "color": (80, 175, 75),  "drop": "pepper_seed",   "drop_chance": 1.0},
    PEPPER_CROP_MATURE:    {"name": "Pepper Crop (Ripe)",      "hardness": 0.5, "color": (220, 75, 35),  "drop": "pepper",        "drop_chance": 1.0},
    ONION_CROP_YOUNG:      {"name": "Onion Crop",              "hardness": 0.5, "color": (130, 190, 100),"drop": "onion_seed",    "drop_chance": 1.0},
    ONION_CROP_MATURE:     {"name": "Onion Crop (Ripe)",       "hardness": 0.5, "color": (175, 150, 85), "drop": "onion",         "drop_chance": 1.0},
    POTATO_CROP_YOUNG:     {"name": "Potato Crop",             "hardness": 0.5, "color": (110, 170, 80), "drop": "potato_seed",   "drop_chance": 1.0},
    POTATO_CROP_MATURE:    {"name": "Potato Crop (Ripe)",      "hardness": 0.5, "color": (165, 130, 65), "drop": "potato",        "drop_chance": 1.0},
    EGGPLANT_CROP_YOUNG:   {"name": "Eggplant Crop",           "hardness": 0.5, "color": (90, 165, 80),  "drop": "eggplant_seed", "drop_chance": 1.0},
    EGGPLANT_CROP_MATURE:  {"name": "Eggplant Crop (Ripe)",    "hardness": 0.5, "color": (95, 45, 135),  "drop": "eggplant",      "drop_chance": 1.0},
    CABBAGE_CROP_YOUNG:    {"name": "Cabbage Crop",            "hardness": 0.5, "color": (95, 180, 100), "drop": "cabbage_seed",  "drop_chance": 1.0},
    CABBAGE_CROP_MATURE:   {"name": "Cabbage Crop (Ripe)",     "hardness": 0.5, "color": (80, 160, 90),  "drop": "cabbage",       "drop_chance": 1.0},
    HOUSE_WALL:            {"name": "House Wall",              "hardness": 2,   "color": (160, 115, 70), "drop": "lumber"},
    HOUSE_ROOF:            {"name": "House Roof",              "hardness": 2,   "color": (90,  45,  30), "drop": "lumber"},
    WILDFLOWER_PATCH:      {"name": "Wildflower",              "hardness": 0.3, "color": (180, 220, 120), "drop": None},
    CRACKED_STONE:         {"name": "Cracked Stone",           "hardness": 2,   "color": (105, 100, 95),  "drop": "stone_chip"},
    STALACTITE:            {"name": "Stalactite",              "hardness": 2,   "color": (110, 108, 112), "drop": "stone_chip"},
    STALAGMITE:            {"name": "Stalagmite",              "hardness": 2,   "color": (110, 108, 112), "drop": "stone_chip"},
    CAVE_MOSS:             {"name": "Cave Moss",               "hardness": 0.5, "color": (45, 110, 55),   "drop": "dirt_clump"},
    CAVE_CRYSTAL:          {"name": "Cave Crystal",            "hardness": 3,   "color": (80, 200, 210),  "drop": "crystal_shard"},
    GRAVEL:                {"name": "Gravel",                  "hardness": 1,   "color": (118, 110, 100), "drop": "stone_chip"},
    CAVE_MUSHROOM:    {"name": "Cave Mushroom",      "hardness": 0.3, "color": (200,  55,  55), "drop": "cave_mushroom",  "drop_chance": 1.0},
    EMBER_CAP:        {"name": "Ember Cap",          "hardness": 0.3, "color": (220, 100,  30), "drop": "cave_mushroom",  "drop_chance": 1.0},
    PALE_GHOST:       {"name": "Pale Ghost",         "hardness": 0.3, "color": (225, 215, 235), "drop": "cave_mushroom",  "drop_chance": 1.0},
    GOLD_CHANTERELLE: {"name": "Golden Chanterelle", "hardness": 0.3, "color": (218, 175,  40), "drop": "rare_mushroom",  "drop_chance": 1.0},
    COBALT_CAP:       {"name": "Cobalt Cap",         "hardness": 0.3, "color": ( 45,  80, 185), "drop": "cave_mushroom",  "drop_chance": 1.0},
    MOSSY_CAP:        {"name": "Mossy Cap",          "hardness": 0.3, "color": ( 85, 115,  55), "drop": "cave_mushroom",  "drop_chance": 1.0},
    VIOLET_CROWN:     {"name": "Violet Crown",       "hardness": 0.3, "color": (130,  55, 175), "drop": "rare_mushroom",  "drop_chance": 1.0},
    BLOOD_CAP:        {"name": "Blood Cap",          "hardness": 0.3, "color": (145,  18,  18), "drop": "cave_mushroom",  "drop_chance": 1.0},
    SULFUR_DOME:      {"name": "Sulfur Dome",        "hardness": 0.3, "color": (210, 200,  30), "drop": "cave_mushroom",  "drop_chance": 1.0},
    IVORY_BELL:       {"name": "Ivory Bell",         "hardness": 0.3, "color": (240, 235, 215), "drop": "cave_mushroom",  "drop_chance": 1.0},
    ASH_BELL:         {"name": "Ash Bell",           "hardness": 0.3, "color": (165, 155, 150), "drop": "cave_mushroom",  "drop_chance": 1.0},
    TEAL_BELL:        {"name": "Teal Bell",          "hardness": 0.3, "color": ( 40, 175, 165), "drop": "rare_mushroom",  "drop_chance": 1.0},
    RUST_SHELF:       {"name": "Rust Shelf",         "hardness": 0.3, "color": (175,  90,  35), "drop": "cave_mushroom",  "drop_chance": 1.0},
    COPPER_SHELF:     {"name": "Copper Shelf",       "hardness": 0.3, "color": ( 80, 140,  90), "drop": "cave_mushroom",  "drop_chance": 1.0},
    OBSIDIAN_SHELF:   {"name": "Obsidian Shelf",     "hardness": 0.3, "color": ( 35,  25,  45), "drop": "rare_mushroom",  "drop_chance": 1.0},
    COAL_PUFF:        {"name": "Coal Puffball",      "hardness": 0.3, "color": ( 65,  60,  65), "drop": "cave_mushroom",  "drop_chance": 1.0},
    STONE_PUFF:       {"name": "Stone Puffball",     "hardness": 0.3, "color": (155, 150, 145), "drop": "cave_mushroom",  "drop_chance": 1.0},
    AMBER_PUFF:       {"name": "Amber Puffball",     "hardness": 0.3, "color": (195, 140,  45), "drop": "cave_mushroom",  "drop_chance": 1.0},
    SULFUR_TUFT:      {"name": "Sulfur Tuft",        "hardness": 0.3, "color": (210, 200,  30), "drop": "cave_mushroom",  "drop_chance": 1.0},
    HONEY_CLUSTER:    {"name": "Honey Cluster",      "hardness": 0.3, "color": (195, 145,  40), "drop": "cave_mushroom",  "drop_chance": 1.0},
    CORAL_TUFT:       {"name": "Coral Tuft",         "hardness": 0.3, "color": (220, 100, 130), "drop": "rare_mushroom",  "drop_chance": 1.0},
    BONE_STALK:       {"name": "Bone Stalk",         "hardness": 0.3, "color": (240, 235, 220), "drop": "cave_mushroom",  "drop_chance": 1.0},
    MAGMA_CAP:        {"name": "Magma Cap",          "hardness": 0.3, "color": ( 85,  20,  15), "drop": "rare_mushroom",  "drop_chance": 1.0},
    DEEP_INK:         {"name": "Deep Ink",           "hardness": 0.3, "color": ( 40,  20,  60), "drop": "rare_mushroom",  "drop_chance": 1.0},
    BIOLUME:          {"name": "Biolume",            "hardness": 0.3, "color": ( 30, 210, 195), "drop": "glowing_spore",  "drop_chance": 1.0},
    WOOD_FENCE:       {"name": "Wood Fence",       "hardness": 2,   "color": (139, 90,  43),  "drop": "wood_fence"},
    IRON_FENCE:       {"name": "Iron Fence",        "hardness": 4,   "color": (160, 160, 165), "drop": "iron_fence"},
    WOOD_DOOR_CLOSED: {"name": "Wood Door",         "hardness": 2,   "color": (139, 90,  43),  "drop": "wood_door"},
    WOOD_DOOR_OPEN:   {"name": "Wood Door (Open)",  "hardness": 2,   "color": (139, 90,  43),  "drop": "wood_door"},
    IRON_DOOR_CLOSED: {"name": "Iron Door",         "hardness": 4,   "color": (160, 160, 165), "drop": "iron_door"},
    IRON_DOOR_OPEN:   {"name": "Iron Door (Open)",  "hardness": 4,   "color": (160, 160, 165), "drop": "iron_door"},
    BED:              {"name": "Bed",               "hardness": 1.0, "color": (200, 80,  110), "drop": "bed"},
    CHEST_BLOCK:      {"name": "Chest",             "hardness": 1.5, "color": (160, 110, 55),  "drop": "chest_item"},
}
