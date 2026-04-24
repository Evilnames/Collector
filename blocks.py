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
SUPPORT          = 24  # legacy (reserved block ID)
WATER            = 25  # liquid; non-solid, flows into empty spaces
IRON_SUPPORT     = 26  # legacy (reserved block ID)
DIAMOND_SUPPORT  = 27  # legacy (reserved block ID)
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
# --- New vegetable crop supply chains ---
BEET_BUSH              = 154
TURNIP_BUSH            = 157
LEEK_BUSH              = 160
ZUCCHINI_BUSH          = 163
SWEET_POTATO_BUSH      = 166
WATERMELON_BUSH        = 169
RADISH_BUSH            = 172
PEA_BUSH               = 175
CELERY_BUSH            = 178
BROCCOLI_BUSH          = 181
BEET_CROP_YOUNG        = 155
BEET_CROP_MATURE       = 156
TURNIP_CROP_YOUNG      = 158
TURNIP_CROP_MATURE     = 159
LEEK_CROP_YOUNG        = 161
LEEK_CROP_MATURE       = 162
ZUCCHINI_CROP_YOUNG    = 164
ZUCCHINI_CROP_MATURE   = 165
SWEET_POTATO_CROP_YOUNG  = 167
SWEET_POTATO_CROP_MATURE = 168
WATERMELON_CROP_YOUNG  = 170
WATERMELON_CROP_MATURE = 171
RADISH_CROP_YOUNG      = 173
RADISH_CROP_MATURE     = 174
PEA_CROP_YOUNG         = 176
PEA_CROP_MATURE        = 177
CELERY_CROP_YOUNG      = 179
CELERY_CROP_MATURE     = 180
BROCCOLI_CROP_YOUNG    = 182
BROCCOLI_CROP_MATURE   = 183
# --- Desert/cactus supply chain ---
CACTUS_YOUNG           = 184
CACTUS_MATURE          = 185
SANDSTONE_BLOCK        = 186
DESERT_FORGE_BLOCK     = 187
DATE_PALM_BUSH         = 188
DATE_PALM_CROP_YOUNG   = 189
DATE_PALM_CROP_MATURE  = 190
AGAVE_BUSH             = 191
AGAVE_CROP_YOUNG       = 192
AGAVE_CROP_MATURE      = 193
OIL                    = 194  # static underground liquid pocket; harvested by empty_barrel

HOUSE_WALL_STONE = 195  # stone city house wall
HOUSE_ROOF_STONE = 196  # stone city house roof
HOUSE_WALL_BRICK = 197  # brick city house wall
HOUSE_ROOF_BRICK = 198  # brick city house roof
HOUSE_WALL_DARK  = 199  # dark-timber city house wall
HOUSE_ROOF_DARK  = 200  # dark-timber city house roof

# --- Additional tree species ---
MAPLE_LOG      = 201
MAPLE_LEAVES   = 202
CHERRY_LOG     = 203
CHERRY_LEAVES  = 204
CYPRESS_LOG    = 205
CYPRESS_LEAVES = 206
BAOBAB_LOG     = 207
BAOBAB_LEAVES  = 208

BIRD_FEEDER_BLOCK = 209
BIRD_BATH_BLOCK   = 210

COFFEE_BUSH           = 211
COFFEE_CROP_YOUNG     = 212
COFFEE_CROP_MATURE    = 213   # special: mine → CoffeeBean object + coffee_seed drop
ROASTER_BLOCK         = 214
BLEND_STATION_BLOCK   = 215
BREW_STATION_BLOCK    = 216
WOOD_FENCE_OPEN      = 217
IRON_FENCE_OPEN      = 218
FOSSIL_TABLE_BLOCK   = 219  # placed Fossil Prep Table equipment
# --- Artisan Bench: refines raw materials into decorative building blocks ---
ARTISAN_BENCH_BLOCK  = 220  # placed Artisan Bench equipment
POLISHED_GRANITE     = 221  # decorative: cool pink-gray stone
POLISHED_MARBLE      = 222  # decorative: clean off-white stone
SLATE_TILE           = 223  # decorative: dark blue-gray tile
TERRACOTTA_BLOCK     = 224  # decorative: warm orange-red clay
MOSSY_BRICK          = 225  # decorative: green-tinted brick
CREAM_BRICK          = 226  # decorative: warm cream sandstone brick
CHARCOAL_PLANK       = 227  # decorative: near-black charred timber
WALNUT_PLANK         = 228  # decorative: rich dark brown plank
OAK_PANEL            = 229  # decorative: honey-light wood panel
BAMBOO_PANEL         = 230  # decorative: pale green-yellow panel

# --- Wine supply chain ---
GRAPEVINE_BUSH        = 231   # surface bush; drops grape_seed
GRAPEVINE_CROP_YOUNG  = 232
GRAPEVINE_CROP_MATURE = 233   # special: mine → Grape object + grape_seed drop
GRAPE_PRESS_BLOCK     = 234   # placed Grape Press (crush mini-game)
FERMENTATION_BLOCK    = 235   # placed Fermentation Tank (multi-control mini-game)
WINE_CELLAR_BLOCK     = 236   # placed Wine Cellar (blend/age/bottle)

# --- Second wave of Artisan Bench decorative blocks ---
OBSIDIAN_TILE        = 237  # deep black-purple volcanic tile
COBBLESTONE          = 238  # rough rustic gray stone
LAPIS_BRICK          = 239  # royal blue ornamental brick
BASALT_COLUMN        = 240  # near-black columnar basalt
LIMESTONE_BLOCK      = 241  # pale beige stone
COPPER_TILE          = 242  # warm orange-metal accent tile
TEAK_PLANK           = 243  # rich medium-brown plank
DRIFTWOOD_PLANK      = 244  # weathered gray wood
CEDAR_PANEL          = 245  # reddish-brown cedar panel
JADE_PANEL           = 246  # luxurious green-stone panel

# --- Third wave of Artisan Bench decorative blocks ---
ROSE_QUARTZ_BLOCK    = 247  # soft rosy-pink ornamental stone
GILDED_BRICK         = 248  # golden-accent decorative brick
AMETHYST_BLOCK       = 249  # vibrant purple crystal block
AMBER_TILE           = 250  # warm glowing amber tile
IVORY_BRICK          = 251  # pure cream neutral brick
EBONY_PLANK          = 252  # near-black polished wood
MAHOGANY_PLANK       = 253  # rich red-brown luxury wood
ASH_PLANK            = 254  # pale blonde sanded plank
FROSTED_GLASS        = 255  # pale blue-white translucent
CRIMSON_BRICK        = 256  # deep red ornate brick

# --- Sentinels ---
SKY_OPENING          = 257  # bg sentinel: tile mined clear of cave-wall backdrop (renders as sky)

# --- Fourth wave of Artisan Bench decorative blocks ---
TERRACOTTA_SHINGLE   = 258  # Mediterranean roof shingle
THATCH_ROOF          = 259  # rustic straw roof
VERDIGRIS_COPPER     = 260  # aged green copper patina
SILVER_PANEL         = 261  # polished silvery metal
GOLD_LEAF_TRIM       = 262  # gilded ornamental trim
STAINED_GLASS_RED    = 263  # translucent crimson
STAINED_GLASS_BLUE   = 264  # translucent azure
STAINED_GLASS_GREEN  = 265  # translucent emerald
QUARTZ_PILLAR        = 266  # white columnar stone
ONYX_INLAY           = 267  # polished black accent stone
TILLED_SOIL          = 268  # prepared farm soil; required under young crops
COMPOST_BIN_BLOCK    = 269  # placed compost processing structure

# --- Premium crop variants (Phase 3 — unlocked by selective_breeding research) ---
STRAWBERRY_CROP_YOUNG_P   = 270  # premium strawberry; wider moisture tolerance
STRAWBERRY_CROP_MATURE_P  = 271
TOMATO_CROP_YOUNG_P       = 272
TOMATO_CROP_MATURE_P      = 273
WATERMELON_CROP_YOUNG_P   = 274
WATERMELON_CROP_MATURE_P  = 275
CORN_CROP_YOUNG_P         = 276
CORN_CROP_MATURE_P        = 277
RICE_CROP_YOUNG_P         = 278
RICE_CROP_MATURE_P        = 279
WELL_BLOCK                = 280  # placeable well; refills watering can

# --- Distillery supply chain ---
GRAIN_CROP_BUSH    = 281   # surface bush; drops grain_seed
GRAIN_CROP_YOUNG   = 282
GRAIN_CROP_MATURE  = 283   # special: mine → Spirit object + grain_seed drop
STILL_BLOCK        = 284   # placed Copper Still (distillation mini-game)
BARREL_ROOM_BLOCK  = 285   # placed Barrel Room (aging)
BOTTLING_BLOCK     = 286   # placed Bottling Station (blend + bottle)
INSECT_DISPLAY_CASE_BLOCK = 287  # craftable display case furniture
STAIRS_RIGHT = 288  # wood stairs; player steps up when walking right into them
STAIRS_LEFT  = 289  # wood stairs; player steps up when walking left into them
GARDEN_BLOCK = 290  # placed garden bed; attracts insects when wildflowers are stored inside

# --- Horse system ---
STABLE_BLOCK       = 291  # placed stable; triggers breeding UI; required for Horse._breed
HORSE_TROUGH_BLOCK = 292  # placed trough; passively speeds up taming when horse is nearby

HOUSE_WALL           = 108  # city house wall block
HOUSE_ROOF           = 109  # city house roof block
WILDFLOWER_PATCH     = 110  # surface collectable; interact → generates unique Wildflower object
# --- Cave blocks ---
CRACKED_STONE = 111   # cracked ceiling block; cracks drawn by renderer
STALACTITE    = 112   # decorative spike hanging from cave ceiling (solid, minable)
STALAGMITE    = 113   # decorative spike growing from cave floor (solid, minable)
CAVE_MOSS     = 114   # mossy floor/wall coating in shallow/wet caves; soft
CAVE_CRYSTAL  = 115   # glowing crystal cluster growing from walls in deep/crystal biomes
GRAVEL        = 116   # loose rock
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
FOSSIL_DEPOSIT   = 150  # special: mine → generates unique Fossil object, no item drop
GEM_DEPOSIT      = 151  # special: mine → generates unique Gemstone object, no item drop
SNOW             = 152  # alpine_mountain surface block; falls like grass
SAND             = 153  # desert/beach surface block; falls like snow

OPEN_DOORS   = {WOOD_DOOR_OPEN, IRON_DOOR_OPEN, WOOD_FENCE_OPEN, IRON_FENCE_OPEN}
STAIR_BLOCKS = {STAIRS_RIGHT, STAIRS_LEFT}

CAVE_MUSHROOMS = {
    CAVE_MUSHROOM, EMBER_CAP, PALE_GHOST, GOLD_CHANTERELLE, COBALT_CAP,
    MOSSY_CAP, VIOLET_CROWN, BLOOD_CAP, SULFUR_DOME, IVORY_BELL,
    ASH_BELL, TEAL_BELL, RUST_SHELF, COPPER_SHELF, OBSIDIAN_SHELF,
    COAL_PUFF, STONE_PUFF, AMBER_PUFF, SULFUR_TUFT, HONEY_CLUSTER,
    CORAL_TUFT, BONE_STALK, MAGMA_CAP, DEEP_INK, BIOLUME,
}

ALL_LOGS   = {TREE_LOG, PINE_LOG, BIRCH_LOG, JUNGLE_LOG, WILLOW_LOG,
              REDWOOD_LOG, PALM_LOG, ACACIA_LOG, DEAD_LOG, MUSHROOM_STEM,
              MAPLE_LOG, CHERRY_LOG, CYPRESS_LOG, BAOBAB_LOG}
ALL_LEAVES = {TREE_LEAVES, PINE_LEAVES, BIRCH_LEAVES, JUNGLE_LEAVES, WILLOW_LEAVES,
              REDWOOD_LEAVES, PALM_LEAVES, ACACIA_LEAVES, MUSHROOM_CAP,
              MAPLE_LEAVES, CHERRY_LEAVES, CYPRESS_LEAVES, BAOBAB_LEAVES}
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
    MAPLE_LEAVES:   MAPLE_LOG,
    CHERRY_LEAVES:  CHERRY_LOG,
    CYPRESS_LEAVES: CYPRESS_LOG,
    BAOBAB_LEAVES:  BAOBAB_LOG,
}

EQUIPMENT_BLOCKS = {TUMBLER_BLOCK, CRUSHER_BLOCK, GEM_CUTTER_BLOCK, KILN_BLOCK, RESONANCE_BLOCK, BAKERY_BLOCK,
                    WOK_BLOCK, STEAMER_BLOCK, NOODLE_POT_BLOCK, BBQ_GRILL_BLOCK, CLAY_POT_BLOCK,
                    DESERT_FORGE_BLOCK,
                    ROASTER_BLOCK, BLEND_STATION_BLOCK, BREW_STATION_BLOCK,
                    GRAPE_PRESS_BLOCK, FERMENTATION_BLOCK, WINE_CELLAR_BLOCK,
                    STILL_BLOCK, BARREL_ROOM_BLOCK, BOTTLING_BLOCK,
                    FOSSIL_TABLE_BLOCK, ARTISAN_BENCH_BLOCK, COMPOST_BIN_BLOCK,
                    STABLE_BLOCK, HORSE_TROUGH_BLOCK}
RESOURCE_BLOCKS  = {COAL_ORE, IRON_ORE, GOLD_ORE, CRYSTAL_ORE, RUBY_ORE, OBSIDIAN, ROCK_DEPOSIT, FOSSIL_DEPOSIT, GEM_DEPOSIT}
BUSH_BLOCKS       = {STRAWBERRY_BUSH, WHEAT_BUSH, CARROT_BUSH, TOMATO_BUSH, CORN_BUSH, PUMPKIN_BUSH, APPLE_BUSH,
                     RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, GARLIC_BUSH, SCALLION_BUSH, CHILI_BUSH,
                     PEPPER_BUSH, ONION_BUSH, POTATO_BUSH, EGGPLANT_BUSH, CABBAGE_BUSH,
                     BEET_BUSH, TURNIP_BUSH, LEEK_BUSH, ZUCCHINI_BUSH, SWEET_POTATO_BUSH,
                     WATERMELON_BUSH, RADISH_BUSH, PEA_BUSH, CELERY_BUSH, BROCCOLI_BUSH,
                     DATE_PALM_BUSH, AGAVE_BUSH,
                     COFFEE_BUSH, GRAPEVINE_BUSH, GRAIN_CROP_BUSH}
YOUNG_CROP_BLOCKS = {STRAWBERRY_CROP_YOUNG, WHEAT_CROP_YOUNG, CARROT_CROP_YOUNG, TOMATO_CROP_YOUNG, CORN_CROP_YOUNG, PUMPKIN_CROP_YOUNG, APPLE_CROP_YOUNG,
                     RICE_CROP_YOUNG, GINGER_CROP_YOUNG, BOK_CHOY_CROP_YOUNG, GARLIC_CROP_YOUNG,
                     SCALLION_CROP_YOUNG, CHILI_CROP_YOUNG,
                     PEPPER_CROP_YOUNG, ONION_CROP_YOUNG, POTATO_CROP_YOUNG, EGGPLANT_CROP_YOUNG, CABBAGE_CROP_YOUNG,
                     BEET_CROP_YOUNG, TURNIP_CROP_YOUNG, LEEK_CROP_YOUNG, ZUCCHINI_CROP_YOUNG, SWEET_POTATO_CROP_YOUNG,
                     WATERMELON_CROP_YOUNG, RADISH_CROP_YOUNG, PEA_CROP_YOUNG, CELERY_CROP_YOUNG, BROCCOLI_CROP_YOUNG,
                     CACTUS_YOUNG, DATE_PALM_CROP_YOUNG, AGAVE_CROP_YOUNG,
                     COFFEE_CROP_YOUNG, GRAPEVINE_CROP_YOUNG, GRAIN_CROP_YOUNG,
                     STRAWBERRY_CROP_YOUNG_P, TOMATO_CROP_YOUNG_P, WATERMELON_CROP_YOUNG_P,
                     CORN_CROP_YOUNG_P, RICE_CROP_YOUNG_P}
MATURE_CROP_BLOCKS= {STRAWBERRY_CROP_MATURE, WHEAT_CROP_MATURE, CARROT_CROP_MATURE, TOMATO_CROP_MATURE, CORN_CROP_MATURE, PUMPKIN_CROP_MATURE, APPLE_CROP_MATURE,
                     RICE_CROP_MATURE, GINGER_CROP_MATURE, BOK_CHOY_CROP_MATURE, GARLIC_CROP_MATURE,
                     SCALLION_CROP_MATURE, CHILI_CROP_MATURE,
                     PEPPER_CROP_MATURE, ONION_CROP_MATURE, POTATO_CROP_MATURE, EGGPLANT_CROP_MATURE, CABBAGE_CROP_MATURE,
                     BEET_CROP_MATURE, TURNIP_CROP_MATURE, LEEK_CROP_MATURE, ZUCCHINI_CROP_MATURE, SWEET_POTATO_CROP_MATURE,
                     WATERMELON_CROP_MATURE, RADISH_CROP_MATURE, PEA_CROP_MATURE, CELERY_CROP_MATURE, BROCCOLI_CROP_MATURE,
                     CACTUS_MATURE, DATE_PALM_CROP_MATURE, AGAVE_CROP_MATURE,
                     COFFEE_CROP_MATURE, GRAPEVINE_CROP_MATURE, GRAIN_CROP_MATURE,
                     STRAWBERRY_CROP_MATURE_P, TOMATO_CROP_MATURE_P, WATERMELON_CROP_MATURE_P,
                     CORN_CROP_MATURE_P, RICE_CROP_MATURE_P}
CROP_BLOCKS       = YOUNG_CROP_BLOCKS | MATURE_CROP_BLOCKS

# Perennial crops regrow after harvest (each harvest has ~33% chance to die)
PERENNIAL_CROP_MATURE = {
    STRAWBERRY_CROP_MATURE, APPLE_CROP_MATURE, TOMATO_CROP_MATURE,
    PEPPER_CROP_MATURE, CHILI_CROP_MATURE, EGGPLANT_CROP_MATURE,
    CACTUS_MATURE, COFFEE_CROP_MATURE, GRAPEVINE_CROP_MATURE, GRAIN_CROP_MATURE,
    STRAWBERRY_CROP_MATURE_P, TOMATO_CROP_MATURE_P,
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
    CABBAGE_CROP_MATURE:      CABBAGE_CROP_YOUNG,
    BEET_CROP_MATURE:         BEET_CROP_YOUNG,
    TURNIP_CROP_MATURE:       TURNIP_CROP_YOUNG,
    LEEK_CROP_MATURE:         LEEK_CROP_YOUNG,
    ZUCCHINI_CROP_MATURE:     ZUCCHINI_CROP_YOUNG,
    SWEET_POTATO_CROP_MATURE: SWEET_POTATO_CROP_YOUNG,
    WATERMELON_CROP_MATURE:   WATERMELON_CROP_YOUNG,
    RADISH_CROP_MATURE:       RADISH_CROP_YOUNG,
    PEA_CROP_MATURE:          PEA_CROP_YOUNG,
    CELERY_CROP_MATURE:       CELERY_CROP_YOUNG,
    BROCCOLI_CROP_MATURE:     BROCCOLI_CROP_YOUNG,
    CACTUS_MATURE:            CACTUS_YOUNG,
    DATE_PALM_CROP_MATURE:    DATE_PALM_CROP_YOUNG,
    AGAVE_CROP_MATURE:        AGAVE_CROP_YOUNG,
    COFFEE_CROP_MATURE:       COFFEE_CROP_YOUNG,
    GRAPEVINE_CROP_MATURE:    GRAPEVINE_CROP_YOUNG,
    GRAIN_CROP_MATURE:        GRAIN_CROP_YOUNG,
    STRAWBERRY_CROP_MATURE_P: STRAWBERRY_CROP_YOUNG_P,
    TOMATO_CROP_MATURE_P:     TOMATO_CROP_YOUNG_P,
    WATERMELON_CROP_MATURE_P: WATERMELON_CROP_YOUNG_P,
    CORN_CROP_MATURE_P:       CORN_CROP_YOUNG_P,
    RICE_CROP_MATURE_P:       RICE_CROP_YOUNG_P,
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
    SUPPORT:              {"name": "Support",         "hardness": 2,            "color": (180, 140, 80),  "drop": None},
    WATER:                {"name": "Water",           "hardness": float('inf'), "color": (40, 110, 220),  "drop": None},
    IRON_SUPPORT:         {"name": "Iron Support",    "hardness": 2,            "color": (160, 170, 185), "drop": None},
    DIAMOND_SUPPORT:      {"name": "Diamond Support", "hardness": 3,            "color": (100, 230, 220), "drop": None},
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
    MAPLE_LOG:     {"name": "Maple Log",         "hardness": 2, "color": (118, 72,  38),  "drop": "lumber"},
    MAPLE_LEAVES:  {"name": "Maple Leaves",      "hardness": 1, "color": (185, 108, 35),  "drop": "sapling", "drop_chance": 0.10},
    CHERRY_LOG:    {"name": "Cherry Log",        "hardness": 2, "color": (72,  52,  60),  "drop": "lumber"},
    CHERRY_LEAVES: {"name": "Cherry Blossoms",   "hardness": 1, "color": (205, 130, 158), "drop": "sapling", "drop_chance": 0.10},
    CYPRESS_LOG:   {"name": "Cypress Log",       "hardness": 2, "color": (78,  55,  35),  "drop": "lumber"},
    CYPRESS_LEAVES:{"name": "Cypress Needles",   "hardness": 1, "color": (22,  88,  28),  "drop": "sapling", "drop_chance": 0.10},
    BAOBAB_LOG:    {"name": "Baobab Log",        "hardness": 3, "color": (165, 145, 115), "drop": "lumber"},
    BAOBAB_LEAVES: {"name": "Baobab Leaves",     "hardness": 1, "color": (82,  120, 45),  "drop": "sapling", "drop_chance": 0.10},
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
    HOUSE_WALL_STONE:      {"name": "Stone Wall",              "hardness": 3,   "color": (140, 135, 128), "drop": "stone_chip"},
    HOUSE_ROOF_STONE:      {"name": "Stone Roof",              "hardness": 3,   "color": ( 80,  75,  70), "drop": "stone_chip"},
    HOUSE_WALL_BRICK:      {"name": "Brick Wall",              "hardness": 2,   "color": (165,  90,  75), "drop": "lumber"},
    HOUSE_ROOF_BRICK:      {"name": "Brick Roof",              "hardness": 2,   "color": (110,  50,  40), "drop": "lumber"},
    HOUSE_WALL_DARK:       {"name": "Dark Timber Wall",        "hardness": 2,   "color": ( 90,  55,  35), "drop": "lumber"},
    HOUSE_ROOF_DARK:       {"name": "Dark Timber Roof",        "hardness": 2,   "color": ( 50,  25,  15), "drop": "lumber"},
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
    WOOD_FENCE:       {"name": "Wood Fence",         "hardness": 2,   "color": (139, 90,  43),  "drop": "wood_fence"},
    IRON_FENCE:       {"name": "Iron Fence",          "hardness": 4,   "color": (160, 160, 165), "drop": "iron_fence"},
    WOOD_FENCE_OPEN:  {"name": "Wood Fence (Open)",   "hardness": 2,   "color": (139, 90,  43),  "drop": "wood_fence"},
    IRON_FENCE_OPEN:  {"name": "Iron Fence (Open)",   "hardness": 4,   "color": (160, 160, 165), "drop": "iron_fence"},
    WOOD_DOOR_CLOSED: {"name": "Wood Door",         "hardness": 2,   "color": (139, 90,  43),  "drop": "wood_door"},
    WOOD_DOOR_OPEN:   {"name": "Wood Door (Open)",  "hardness": 2,   "color": (139, 90,  43),  "drop": "wood_door"},
    IRON_DOOR_CLOSED: {"name": "Iron Door",         "hardness": 4,   "color": (160, 160, 165), "drop": "iron_door"},
    IRON_DOOR_OPEN:   {"name": "Iron Door (Open)",  "hardness": 4,   "color": (160, 160, 165), "drop": "iron_door"},
    BED:              {"name": "Bed",               "hardness": 1.0, "color": (200, 80,  110), "drop": "bed"},
    CHEST_BLOCK:      {"name": "Chest",             "hardness": 1.5, "color": (160, 110, 55),  "drop": "chest_item"},
    FOSSIL_DEPOSIT:   {"name": "Fossil Deposit",    "hardness": 5,   "color": (140, 125, 105), "drop": None},
    GEM_DEPOSIT:      {"name": "Gem Deposit",       "hardness": 6,   "color": (88,  72,  105), "drop": None},
    SNOW:             {"name": "Snow",              "hardness": 1,   "color": (220, 232, 245), "drop": "stone_chip"},
    SAND:             {"name": "Sand",              "hardness": 1,   "color": (210, 190, 140), "drop": "sand_grain"},
    # --- New vegetable crops ---
    BEET_BUSH:              {"name": "Beet Bush",                "hardness": 0.5, "color": (140,  30,  60), "drop": "beet_seed",         "drop_chance": 1.0},
    BEET_CROP_YOUNG:        {"name": "Beet Crop",                "hardness": 0.5, "color": ( 90, 165,  80), "drop": "beet_seed",         "drop_chance": 1.0},
    BEET_CROP_MATURE:       {"name": "Beet Crop (Ripe)",         "hardness": 0.5, "color": (140,  30,  60), "drop": "beet",              "drop_chance": 1.0},
    TURNIP_BUSH:            {"name": "Turnip Bush",              "hardness": 0.5, "color": (210, 190, 215), "drop": "turnip_seed",       "drop_chance": 1.0},
    TURNIP_CROP_YOUNG:      {"name": "Turnip Crop",              "hardness": 0.5, "color": ( 95, 170,  85), "drop": "turnip_seed",       "drop_chance": 1.0},
    TURNIP_CROP_MATURE:     {"name": "Turnip Crop (Ripe)",       "hardness": 0.5, "color": (210, 190, 215), "drop": "turnip",            "drop_chance": 1.0},
    LEEK_BUSH:              {"name": "Leek Bush",                "hardness": 0.5, "color": ( 80, 195,  90), "drop": "leek_seed",         "drop_chance": 1.0},
    LEEK_CROP_YOUNG:        {"name": "Leek Crop",                "hardness": 0.5, "color": ( 60, 180,  80), "drop": "leek_seed",         "drop_chance": 1.0},
    LEEK_CROP_MATURE:       {"name": "Leek Crop (Ripe)",         "hardness": 0.5, "color": ( 90, 210, 100), "drop": "leek",              "drop_chance": 1.0},
    ZUCCHINI_BUSH:          {"name": "Zucchini Bush",            "hardness": 0.5, "color": ( 70, 150,  55), "drop": "zucchini_seed",     "drop_chance": 1.0},
    ZUCCHINI_CROP_YOUNG:    {"name": "Zucchini Crop",            "hardness": 0.5, "color": ( 85, 175,  70), "drop": "zucchini_seed",     "drop_chance": 1.0},
    ZUCCHINI_CROP_MATURE:   {"name": "Zucchini Crop (Ripe)",     "hardness": 0.5, "color": ( 65, 145,  50), "drop": "zucchini",          "drop_chance": 1.0},
    SWEET_POTATO_BUSH:      {"name": "Sweet Potato Bush",        "hardness": 0.5, "color": (195, 100,  50), "drop": "sweet_potato_seed", "drop_chance": 1.0},
    SWEET_POTATO_CROP_YOUNG:  {"name": "Sweet Potato Crop",      "hardness": 0.5, "color": (100, 175,  85), "drop": "sweet_potato_seed", "drop_chance": 1.0},
    SWEET_POTATO_CROP_MATURE: {"name": "Sweet Potato Crop (Ripe)","hardness": 0.5,"color": (195, 100,  50), "drop": "sweet_potato",      "drop_chance": 1.0},
    WATERMELON_BUSH:        {"name": "Watermelon Bush",          "hardness": 0.5, "color": ( 55, 140,  50), "drop": "watermelon_seed",   "drop_chance": 1.0},
    WATERMELON_CROP_YOUNG:  {"name": "Watermelon Crop",          "hardness": 0.5, "color": ( 70, 160,  65), "drop": "watermelon_seed",   "drop_chance": 1.0},
    WATERMELON_CROP_MATURE: {"name": "Watermelon Crop (Ripe)",   "hardness": 0.5, "color": ( 55, 140,  50), "drop": "watermelon",        "drop_chance": 1.0},
    RADISH_BUSH:            {"name": "Radish Bush",              "hardness": 0.5, "color": (220,  60,  80), "drop": "radish_seed",       "drop_chance": 1.0},
    RADISH_CROP_YOUNG:      {"name": "Radish Crop",              "hardness": 0.5, "color": ( 90, 170,  80), "drop": "radish_seed",       "drop_chance": 1.0},
    RADISH_CROP_MATURE:     {"name": "Radish Crop (Ripe)",       "hardness": 0.5, "color": (220,  60,  80), "drop": "radish",            "drop_chance": 1.0},
    PEA_BUSH:               {"name": "Pea Bush",                 "hardness": 0.5, "color": (100, 185,  70), "drop": "pea_seed",          "drop_chance": 1.0},
    PEA_CROP_YOUNG:         {"name": "Pea Crop",                 "hardness": 0.5, "color": (110, 190,  80), "drop": "pea_seed",          "drop_chance": 1.0},
    PEA_CROP_MATURE:        {"name": "Pea Crop (Ripe)",          "hardness": 0.5, "color": (110, 185,  65), "drop": "pea",               "drop_chance": 1.0},
    CELERY_BUSH:            {"name": "Celery Bush",              "hardness": 0.5, "color": ( 95, 185, 100), "drop": "celery_seed",       "drop_chance": 1.0},
    CELERY_CROP_YOUNG:      {"name": "Celery Crop",              "hardness": 0.5, "color": ( 80, 175,  90), "drop": "celery_seed",       "drop_chance": 1.0},
    CELERY_CROP_MATURE:     {"name": "Celery Crop (Ripe)",       "hardness": 0.5, "color": (100, 190, 105), "drop": "celery",            "drop_chance": 1.0},
    BROCCOLI_BUSH:          {"name": "Broccoli Bush",            "hardness": 0.5, "color": ( 45, 120,  55), "drop": "broccoli_seed",     "drop_chance": 1.0},
    BROCCOLI_CROP_YOUNG:    {"name": "Broccoli Crop",            "hardness": 0.5, "color": ( 65, 155,  70), "drop": "broccoli_seed",     "drop_chance": 1.0},
    BROCCOLI_CROP_MATURE:   {"name": "Broccoli Crop (Ripe)",     "hardness": 0.5, "color": ( 40, 115,  50), "drop": "broccoli",          "drop_chance": 1.0},
    # --- Desert/cactus supply chain ---
    CACTUS_YOUNG:           {"name": "Cactus",                   "hardness": 0.5, "color": ( 65, 155,  60), "drop": "cactus_spine",      "drop_chance": 1.0},
    CACTUS_MATURE:          {"name": "Cactus (Ripe)",            "hardness": 0.5, "color": ( 45, 135,  40), "drop": "cactus_fruit",      "drop_chance": 1.0},
    SANDSTONE_BLOCK:        {"name": "Sandstone",                "hardness": 2,   "color": (210, 185, 120), "drop": "sandstone"},
    DESERT_FORGE_BLOCK:     {"name": "Desert Forge",             "hardness": 1,   "color": (175,  95,  40), "drop": "desert_forge_item"},
    DATE_PALM_BUSH:         {"name": "Date Palm Bush",           "hardness": 0.5, "color": ( 90, 140,  55), "drop": "date_palm_seed",    "drop_chance": 1.0},
    DATE_PALM_CROP_YOUNG:   {"name": "Date Palm",                "hardness": 0.5, "color": ( 80, 150,  55), "drop": "date_palm_seed",    "drop_chance": 1.0},
    DATE_PALM_CROP_MATURE:  {"name": "Date Palm (Ripe)",         "hardness": 0.5, "color": (180, 110,  30), "drop": "date_palm_fruit",   "drop_chance": 1.0},
    AGAVE_BUSH:             {"name": "Agave Bush",               "hardness": 0.5, "color": ( 80, 155, 100), "drop": "agave_seed",        "drop_chance": 1.0},
    AGAVE_CROP_YOUNG:       {"name": "Agave Plant",              "hardness": 0.5, "color": ( 70, 165,  90), "drop": "agave_seed",        "drop_chance": 1.0},
    AGAVE_CROP_MATURE:      {"name": "Agave Plant (Ripe)",       "hardness": 0.5, "color": ( 95, 185, 105), "drop": "agave",             "drop_chance": 1.0},
    OIL:                    {"name": "Oil",                      "hardness": float('inf'),    "color": ( 30,  22,  10), "drop": None},
    BIRD_FEEDER_BLOCK:      {"name": "Bird Feeder",              "hardness": 1.5,             "color": (160, 115,  65), "drop": "bird_feeder"},
    BIRD_BATH_BLOCK:        {"name": "Bird Bath",                "hardness": 2.0,             "color": (185, 180, 172), "drop": "bird_bath"},
    # --- Coffee supply chain ---
    COFFEE_BUSH:            {"name": "Coffee Bush",              "hardness": 0.5, "color": ( 60, 100,  40), "drop": "coffee_seed",    "drop_chance": 1.0},
    COFFEE_CROP_YOUNG:      {"name": "Coffee Plant",             "hardness": 0.5, "color": ( 75, 140,  60), "drop": "coffee_seed",    "drop_chance": 1.0},
    COFFEE_CROP_MATURE:     {"name": "Coffee Plant (Ripe)",      "hardness": 0.5, "color": (160,  45,  30), "drop": None},
    ROASTER_BLOCK:          {"name": "Coffee Roaster",           "hardness": 1.5, "color": ( 95,  55,  25), "drop": "roaster_item"},
    BLEND_STATION_BLOCK:    {"name": "Blend Station",            "hardness": 1.5, "color": (110,  75,  40), "drop": "blend_station_item"},
    BREW_STATION_BLOCK:     {"name": "Brew Station",             "hardness": 1.5, "color": ( 75,  60,  45), "drop": "brew_station_item"},
    FOSSIL_TABLE_BLOCK:     {"name": "Fossil Prep Table",        "hardness": 2,   "color": (110,  88,  62), "drop": "fossil_table_item"},
    # --- Artisan Bench + decorative house blocks ---
    ARTISAN_BENCH_BLOCK:    {"name": "Artisan Bench",            "hardness": 1.5, "color": (135, 100,  70), "drop": "artisan_bench_item"},
    POLISHED_GRANITE:       {"name": "Polished Granite",         "hardness": 2,   "color": (130, 115, 120), "drop": "polished_granite"},
    POLISHED_MARBLE:        {"name": "Polished Marble",          "hardness": 2,   "color": (235, 230, 225), "drop": "polished_marble"},
    SLATE_TILE:             {"name": "Slate Tile",               "hardness": 2,   "color": ( 55,  65,  80), "drop": "slate_tile"},
    TERRACOTTA_BLOCK:       {"name": "Terracotta",               "hardness": 2,   "color": (195, 105,  70), "drop": "terracotta"},
    MOSSY_BRICK:            {"name": "Mossy Brick",              "hardness": 2,   "color": (115, 140,  90), "drop": "mossy_brick"},
    CREAM_BRICK:            {"name": "Cream Brick",              "hardness": 2,   "color": (220, 200, 165), "drop": "cream_brick"},
    CHARCOAL_PLANK:         {"name": "Charcoal Plank",           "hardness": 2,   "color": ( 55,  50,  55), "drop": "charcoal_plank"},
    WALNUT_PLANK:           {"name": "Walnut Plank",             "hardness": 2,   "color": ( 90,  60,  40), "drop": "walnut_plank"},
    OAK_PANEL:              {"name": "Oak Panel",                "hardness": 2,   "color": (180, 140,  90), "drop": "oak_panel"},
    BAMBOO_PANEL:           {"name": "Bamboo Panel",             "hardness": 2,   "color": (210, 200, 130), "drop": "bamboo_panel"},
    # --- Wine supply chain ---
    GRAPEVINE_BUSH:         {"name": "Grapevine Bush",           "hardness": 0.5, "color": ( 80, 130,  60), "drop": "grape_seed", "drop_chance": 1.0},
    GRAPEVINE_CROP_YOUNG:   {"name": "Grapevine",                "hardness": 0.5, "color": ( 95, 150,  70), "drop": "grape_seed", "drop_chance": 1.0},
    GRAPEVINE_CROP_MATURE:  {"name": "Grapevine (Ripe)",         "hardness": 0.5, "color": (110,  40,  95), "drop": None},
    GRAPE_PRESS_BLOCK:      {"name": "Grape Press",              "hardness": 1.5, "color": (150, 110,  80), "drop": "grape_press_item"},
    FERMENTATION_BLOCK:     {"name": "Fermentation Tank",        "hardness": 1.5, "color": (115,  95,  80), "drop": "fermentation_item"},
    WINE_CELLAR_BLOCK:      {"name": "Wine Cellar",              "hardness": 1.5, "color": ( 75,  45,  55), "drop": "wine_cellar_item"},
    # --- Distillery supply chain ---
    GRAIN_CROP_BUSH:        {"name": "Grain Bush",               "hardness": 0.5, "color": (180, 160,  70), "drop": "grain_seed", "drop_chance": 0.4},
    GRAIN_CROP_YOUNG:       {"name": "Grain Crop (Young)",       "hardness": 0.5, "color": (130, 160,  55), "drop": "grain_seed", "drop_chance": 0.5},
    GRAIN_CROP_MATURE:      {"name": "Grain Crop (Ripe)",        "hardness": 0.5, "color": (200, 175,  55), "drop": None},
    STILL_BLOCK:            {"name": "Copper Still",             "hardness": 1.5, "color": (175, 110,  50), "drop": "still_item"},
    BARREL_ROOM_BLOCK:      {"name": "Barrel Room",              "hardness": 1.5, "color": (110,  70,  35), "drop": "barrel_room_item"},
    BOTTLING_BLOCK:         {"name": "Bottling Station",         "hardness": 1.5, "color": ( 90,  80,  70), "drop": "bottling_item"},
    # --- Second wave of artisan decorative blocks ---
    OBSIDIAN_TILE:          {"name": "Obsidian Tile",            "hardness": 2,   "color": ( 30,  25,  40), "drop": "obsidian_tile"},
    COBBLESTONE:            {"name": "Cobblestone",              "hardness": 2,   "color": (100,  95,  90), "drop": "cobblestone"},
    LAPIS_BRICK:            {"name": "Lapis Brick",              "hardness": 2,   "color": ( 55,  85, 165), "drop": "lapis_brick"},
    BASALT_COLUMN:          {"name": "Basalt Column",            "hardness": 2,   "color": ( 60,  55,  65), "drop": "basalt_column"},
    LIMESTONE_BLOCK:        {"name": "Limestone",                "hardness": 2,   "color": (225, 215, 195), "drop": "limestone_block"},
    COPPER_TILE:            {"name": "Copper Tile",              "hardness": 2,   "color": (180, 110,  75), "drop": "copper_tile"},
    TEAK_PLANK:             {"name": "Teak Plank",               "hardness": 2,   "color": (140,  95,  60), "drop": "teak_plank"},
    DRIFTWOOD_PLANK:        {"name": "Driftwood Plank",          "hardness": 2,   "color": (165, 155, 145), "drop": "driftwood_plank"},
    CEDAR_PANEL:            {"name": "Cedar Panel",              "hardness": 2,   "color": (160, 105,  75), "drop": "cedar_panel"},
    JADE_PANEL:             {"name": "Jade Panel",               "hardness": 2,   "color": ( 95, 165, 125), "drop": "jade_panel"},
    # --- Third wave of artisan decorative blocks ---
    ROSE_QUARTZ_BLOCK:      {"name": "Rose Quartz",              "hardness": 2,   "color": (245, 175, 185), "drop": "rose_quartz_block"},
    GILDED_BRICK:           {"name": "Gilded Brick",             "hardness": 2,   "color": (215, 170,  70), "drop": "gilded_brick"},
    AMETHYST_BLOCK:         {"name": "Amethyst Block",           "hardness": 2,   "color": (155,  95, 200), "drop": "amethyst_block"},
    AMBER_TILE:             {"name": "Amber Tile",               "hardness": 2,   "color": (215, 140,  50), "drop": "amber_tile"},
    IVORY_BRICK:            {"name": "Ivory Brick",              "hardness": 2,   "color": (240, 230, 205), "drop": "ivory_brick"},
    EBONY_PLANK:            {"name": "Ebony Plank",              "hardness": 2,   "color": ( 35,  25,  25), "drop": "ebony_plank"},
    MAHOGANY_PLANK:         {"name": "Mahogany Plank",           "hardness": 2,   "color": (115,  50,  35), "drop": "mahogany_plank"},
    ASH_PLANK:              {"name": "Ash Plank",                "hardness": 2,   "color": (200, 195, 175), "drop": "ash_plank"},
    FROSTED_GLASS:          {"name": "Frosted Glass",            "hardness": 2,   "color": (210, 230, 240), "drop": "frosted_glass"},
    CRIMSON_BRICK:          {"name": "Crimson Brick",            "hardness": 2,   "color": (160,  40,  50), "drop": "crimson_brick"},
    SKY_OPENING:            {"name": "Sky",                      "hardness": 0,   "color": None,            "drop": None},
    # --- Fourth wave of artisan decorative blocks ---
    TERRACOTTA_SHINGLE:     {"name": "Terracotta Shingle",       "hardness": 2,   "color": (140,  60,  45), "drop": "terracotta_shingle"},
    THATCH_ROOF:            {"name": "Thatch Roof",              "hardness": 1,   "color": (175, 140,  75), "drop": "thatch_roof"},
    VERDIGRIS_COPPER:       {"name": "Verdigris Copper",         "hardness": 2,   "color": ( 90, 165, 140), "drop": "verdigris_copper"},
    SILVER_PANEL:           {"name": "Silver Panel",             "hardness": 2,   "color": (190, 195, 205), "drop": "silver_panel"},
    GOLD_LEAF_TRIM:         {"name": "Gold Leaf Trim",           "hardness": 2,   "color": (230, 200,  90), "drop": "gold_leaf_trim"},
    STAINED_GLASS_RED:      {"name": "Stained Glass (Red)",      "hardness": 2,   "color": (180,  50,  55), "drop": "stained_glass_red"},
    STAINED_GLASS_BLUE:     {"name": "Stained Glass (Blue)",     "hardness": 2,   "color": ( 60,  90, 180), "drop": "stained_glass_blue"},
    STAINED_GLASS_GREEN:    {"name": "Stained Glass (Green)",    "hardness": 2,   "color": ( 60, 150,  95), "drop": "stained_glass_green"},
    QUARTZ_PILLAR:          {"name": "Quartz Pillar",            "hardness": 2,   "color": (220, 220, 210), "drop": "quartz_pillar"},
    ONYX_INLAY:             {"name": "Onyx Inlay",               "hardness": 2,   "color": ( 40,  35,  45), "drop": "onyx_inlay"},
    TILLED_SOIL:            {"name": "Tilled Soil",              "hardness": 1,   "color": (100,  66,  32), "drop": "dirt_clump"},
    COMPOST_BIN_BLOCK:      {"name": "Compost Bin",              "hardness": 1,   "color": (100,  70,  40), "drop": "compost_bin_item"},
    WELL_BLOCK:             {"name": "Well",                     "hardness": 3,   "color": ( 80, 115, 145), "drop": "well_item"},
    # --- Premium crop variants ---
    STRAWBERRY_CROP_YOUNG_P:   {"name": "Premium Strawberry",        "hardness": 0.5, "color": (255, 100, 140), "drop": "strawberry_seed_premium", "drop_chance": 1.0},
    STRAWBERRY_CROP_MATURE_P:  {"name": "Premium Strawberry (Ripe)", "hardness": 0.5, "color": (255, 100, 140), "drop": "strawberry",               "drop_chance": 1.0},
    TOMATO_CROP_YOUNG_P:       {"name": "Premium Tomato",            "hardness": 0.5, "color": (255, 100, 100), "drop": "tomato_seed_premium",      "drop_chance": 1.0},
    TOMATO_CROP_MATURE_P:      {"name": "Premium Tomato (Ripe)",     "hardness": 0.5, "color": (255, 100, 100), "drop": "tomato",                   "drop_chance": 1.0},
    WATERMELON_CROP_YOUNG_P:   {"name": "Premium Watermelon",        "hardness": 0.5, "color": (100, 220, 120), "drop": "watermelon_seed_premium",  "drop_chance": 1.0},
    WATERMELON_CROP_MATURE_P:  {"name": "Premium Watermelon (Ripe)", "hardness": 0.5, "color": (100, 220, 120), "drop": "watermelon",               "drop_chance": 1.0},
    CORN_CROP_YOUNG_P:         {"name": "Premium Corn",              "hardness": 0.5, "color": (255, 240, 100), "drop": "corn_seed_premium",        "drop_chance": 1.0},
    CORN_CROP_MATURE_P:        {"name": "Premium Corn (Ripe)",       "hardness": 0.5, "color": (255, 240, 100), "drop": "corn",                     "drop_chance": 1.0},
    RICE_CROP_YOUNG_P:         {"name": "Premium Rice",              "hardness": 0.5, "color": (200, 235, 180), "drop": "rice_seed_premium",        "drop_chance": 1.0},
    RICE_CROP_MATURE_P:        {"name": "Premium Rice (Ripe)",       "hardness": 0.5, "color": (200, 235, 180), "drop": "rice",                     "drop_chance": 1.0},
    INSECT_DISPLAY_CASE_BLOCK: {"name": "Insect Display Case",       "hardness": 1.5, "color": (180, 160, 120), "drop": "insect_display_case"},
    STAIRS_RIGHT:              {"name": "Stairs (Right)",            "hardness": 1.5, "color": (139, 100,  60), "drop": "wood_stairs"},
    STAIRS_LEFT:               {"name": "Stairs (Left)",             "hardness": 1.5, "color": (139, 100,  60), "drop": "wood_stairs"},
    GARDEN_BLOCK:              {"name": "Garden Block",              "hardness": 1.0, "color": ( 80, 140,  60), "drop": "garden_block"},
    STABLE_BLOCK:              {"name": "Stable",                   "hardness": 2.0, "color": (120,  85,  45), "drop": "stable_item"},
    HORSE_TROUGH_BLOCK:        {"name": "Horse Trough",             "hardness": 1.5, "color": ( 60, 100, 130), "drop": "horse_trough_item"},
}
