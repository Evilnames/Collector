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

# --- Tea supply chain ---
TEA_BUSH                = 293  # surface bush; drops tea_seed
TEA_CROP_YOUNG          = 294
TEA_CROP_MATURE         = 295  # special: mine → TeaLeaf object + tea_seed drop
WITHERING_RACK_BLOCK    = 296  # placed Withering Rack (wither method choice)
OXIDATION_STATION_BLOCK = 297  # placed Oxidation Station (oxidation timing mini-game)
TEA_CELLAR_BLOCK        = 298  # placed Tea Cellar (brew, blend, age)
ROASTING_KILN_BLOCK     = 1251 # placed Roasting Kiln (roast green/oolong → hojicha)
RESTAURANT_WALL         = 299  # city restaurant wall (warm terracotta)
RESTAURANT_AWNING       = 300  # city restaurant awning/roof (deep crimson)

# --- Herbalism supply chain ---
DRYING_RACK_BLOCK       = 301  # placed Drying Rack; converts raw herbs/mushrooms → dried ingredients

# --- Herb bushes (surface-growing crafting plants) ---
CHAMOMILE_BUSH          = 302  # surface bush; drops chamomile_seed
CHAMOMILE_CROP_YOUNG    = 303
CHAMOMILE_CROP_MATURE   = 304  # harvest → chamomile_item + seed; perennial
LAVENDER_BUSH           = 305  # surface bush; drops lavender_seed
LAVENDER_CROP_YOUNG     = 306
LAVENDER_CROP_MATURE    = 307  # harvest → lavender + seed; perennial
MINT_BUSH               = 308  # surface bush; drops mint_seed
MINT_CROP_YOUNG         = 309
MINT_CROP_MATURE        = 310  # harvest → mint + seed; perennial
ROSEMARY_BUSH           = 311  # surface bush; drops rosemary_seed
ROSEMARY_CROP_YOUNG     = 312
ROSEMARY_CROP_MATURE    = 313  # harvest → rosemary + seed; perennial
THYME_BUSH              = 314
THYME_CROP_YOUNG        = 315
THYME_CROP_MATURE       = 316
SAGE_BUSH               = 317
SAGE_CROP_YOUNG         = 318
SAGE_CROP_MATURE        = 319
BASIL_BUSH              = 320
BASIL_CROP_YOUNG        = 321
BASIL_CROP_MATURE       = 322
OREGANO_BUSH            = 323
OREGANO_CROP_YOUNG      = 324
OREGANO_CROP_MATURE     = 325
DILL_BUSH               = 326
DILL_CROP_YOUNG         = 327
DILL_CROP_MATURE        = 328
FENNEL_BUSH             = 1179

FENNEL_CROP_YOUNG       = 1180

FENNEL_CROP_MATURE      = 331
TARRAGON_BUSH           = 332
TARRAGON_CROP_YOUNG     = 333
TARRAGON_CROP_MATURE    = 334
LEMON_BALM_BUSH         = 335
LEMON_BALM_CROP_YOUNG   = 336
LEMON_BALM_CROP_MATURE  = 337
ECHINACEA_BUSH          = 338
ECHINACEA_CROP_YOUNG    = 339
ECHINACEA_CROP_MATURE   = 340
VALERIAN_BUSH           = 341
VALERIAN_CROP_YOUNG     = 342
VALERIAN_CROP_MATURE    = 343
ST_JOHNS_WORT_BUSH      = 344
ST_JOHNS_WORT_CROP_YOUNG= 345
ST_JOHNS_WORT_CROP_MATURE=346
YARROW_BUSH             = 347
YARROW_CROP_YOUNG       = 348
YARROW_CROP_MATURE      = 349
BERGAMOT_BUSH           = 350
BERGAMOT_CROP_YOUNG     = 351
BERGAMOT_CROP_MATURE    = 352
WORMWOOD_BUSH           = 353
WORMWOOD_CROP_YOUNG     = 354
WORMWOOD_CROP_MATURE    = 355
RUE_BUSH                = 356
RUE_CROP_YOUNG          = 357
RUE_CROP_MATURE         = 358
LEMON_VERBENA_BUSH      = 359
LEMON_VERBENA_CROP_YOUNG= 360
LEMON_VERBENA_CROP_MATURE=361
HYSSOP_BUSH             = 362
HYSSOP_CROP_YOUNG       = 363
HYSSOP_CROP_MATURE      = 364
CATNIP_BUSH             = 365
CATNIP_CROP_YOUNG       = 366
CATNIP_CROP_MATURE      = 367
WOOD_SORREL_BUSH        = 368
WOOD_SORREL_CROP_YOUNG  = 369
WOOD_SORREL_CROP_MATURE = 370
MARJORAM_BUSH           = 371
MARJORAM_CROP_YOUNG     = 372
MARJORAM_CROP_MATURE    = 373
SAVORY_BUSH             = 374
SAVORY_CROP_YOUNG       = 375
SAVORY_CROP_MATURE      = 376
ANGELICA_BUSH           = 377
ANGELICA_CROP_YOUNG     = 378
ANGELICA_CROP_MATURE    = 379
BORAGE_BUSH             = 380
BORAGE_CROP_YOUNG       = 381
BORAGE_CROP_MATURE      = 382
COMFREY_BUSH            = 383
COMFREY_CROP_YOUNG      = 384
COMFREY_CROP_MATURE     = 385
MUGWORT_BUSH            = 386
MUGWORT_CROP_YOUNG      = 387
MUGWORT_CROP_MATURE     = 388
BAIT_STATION_BLOCK      = 1181  # placed Bait Station; crafts fishing bait
CHICKPEA_CROP_YOUNG     = 911


CHICKPEA_CROP_MATURE    = 912


LENTIL_CROP_YOUNG       = 913


LENTIL_CROP_MATURE      = 914


SESAME_CROP_YOUNG       = 915


SESAME_CROP_MATURE      = 916


POMEGRANATE_TREE_YOUNG  = 917


POMEGRANATE_TREE_MATURE = 918


OLIVE_TREE_YOUNG        = 919


OLIVE_TREE_MATURE       = 920


SAFFRON_CROP_YOUNG      = 921


SAFFRON_CROP_MATURE     = 922



# --- Islamic architecture blocks (Artisan Bench) ---
# --- Mineable natural deposits ---
CLAY_DEPOSIT      = 329  # natural clay bed; shallow sedimentary/temperate zones
LIMESTONE_DEPOSIT = 330  # natural limestone layer; shallow-mid sedimentary zones

# --- Islamic architecture blocks (Artisan Bench) ---
WHITE_PLASTER_WALL = 923  # smooth white plaster wall
CARVED_PLASTER     = 924  # white plaster with gold arabesque geometric inlay
MUQARNAS_BLOCK     = 925  # stepped stalactite/honeycomb overhang element
MASHRABIYA         = 926  # carved wooden diamond-lattice screen
ZELLIGE_TILE       = 927  # colorful geometric mosaic tile (Moroccan style)
ARABESQUE_PANEL    = 928  # sandstone panel with interlaced geometric carving

# --- Spanish architecture blocks (Artisan Bench) ---
ADOBE_BRICK        = 929  # sun-dried mud brick; warm tan with straw texture
SPANISH_ROOF_TILE  = 930  # curved barrel roof tile in terracotta red
WROUGHT_IRON_GRILLE= 931  # decorative forged-iron scrollwork panel
TALAVERA_TILE      = 932  # blue-and-white hand-painted ceramic tile
SALTILLO_TILE      = 933  # unglazed terracotta floor tile

# --- Middle Eastern decorative doors (Artisan Bench) ---
COBALT_DOOR_CLOSED       = 934  # royal blue lacquered door with gold arabesque
COBALT_DOOR_OPEN         = 935


CRIMSON_CEDAR_DOOR_CLOSED= 936  # deep red cedar with carved diamond geometry
CRIMSON_CEDAR_DOOR_OPEN  = 937


TEAL_DOOR_CLOSED         = 938  # rich teal lacquered door with gold trim
TEAL_DOOR_OPEN           = 939

# --- Salt supply chain ---
SALT_DEPOSIT           = 940  # natural salt bed; spawns in arid/sedimentary zones underground
EVAPORATION_PAN_BLOCK  = 941  # placed Evaporation Pan (evaporation mini-game)
SALT_GRINDER_BLOCK     = 942  # placed Salt Grinder (grade selection)

# --- Minecart system ---
MINE_TRACK_BLOCK      = 943  # horizontal rail section
MINE_TRACK_STOP_BLOCK = 944  # station/stop on the rail where carts can be called

# --- Custom Tapestry system ---
TAPESTRY_FRAME_BLOCK  = 945  # crafting station for the tapestry design mini-game
CUSTOM_TAPESTRY_ROOT  = 946  # bottom block of a player-woven hanging tapestry
CUSTOM_TAPESTRY_BODY  = 947  # upper continuation blocks of a tall tapestry

# --- Gardening blocks ---
ORNAMENTAL_GRASS    = 948  # decorative feathery grass clump; placed decoration
FLOWERING_SHRUB     = 949  # rounded ornamental shrub with pink flowers
HOLLY_SHRUB         = 950  # dark glossy holly with red berries
TOPIARY_PEACOCK     = 951  # peacock-shaped clipped evergreen topiary
TOPIARY_BEAR        = 952  # bear-shaped clipped evergreen topiary
TOPIARY_RABBIT      = 953  # rabbit-shaped clipped evergreen topiary
ROSE_BED            = 954  # formal rose garden bed with red blooms
TULIP_BED           = 955  # Dutch-style multi-colour tulip bed
COTTAGE_GARDEN_BED  = 956  # informal mixed cottage wildflower garden bed
CHERUB_FOUNTAIN     = 957  # carved stone cherub/putto fountain
LION_HEAD_FOUNTAIN  = 958  # wall-mounted lion's head water spout
MOSAIC_FOUNTAIN     = 959  # mosaic-tiled round fountain basin
LAVENDER_BED        = 960  # rows of purple lavender in soil
SUNFLOWER_BED       = 961  # tall yellow sunflowers in soil
DAHLIA_BED          = 962  # mixed colour dahlia blooms in soil
TOPIARY_SWAN        = 963  # swan-shaped clipped evergreen topiary
TOPIARY_FOX         = 964  # fox-shaped clipped evergreen topiary
TOPIARY_ELEPHANT    = 965  # elephant-shaped clipped topiary with raised trunk
PEONY_BUSH          = 966  # ornamental peony with large fluffy blooms
FERN_CLUMP          = 967  # decorative shade-loving fern fronds
RAISED_GARDEN_BED   = 968  # stone-edged raised planting bed with mixed crops
LILY_PAD_POND       = 969  # small still pond with lily pads and flowers
BEE_SKEP            = 970  # traditional woven straw beehive decoration
GARDEN_WHEELBARROW  = 971  # decorative old wooden wheelbarrow filled with soil
IRIS_BED            = 972  # purple iris flowers with flag petals in soil
POPPY_BED           = 973  # bright red poppies with black centres in soil
FOXGLOVE_PATCH      = 974  # tall foxglove flower spires
SNOWDROP_PATCH      = 975  # delicate white drooping snowdrop bells
MARIGOLD_BED        = 976  # dense orange/yellow marigold pom-poms
BOXWOOD_BALL        = 977  # perfectly round clipped boxwood sphere on a stem
RHODODENDRON_BUSH   = 978  # large flowering rhododendron with pink blooms
BAMBOO_CLUMP        = 979  # ornamental tall bamboo stems with nodes
AGAPANTHUS_PATCH    = 980  # slender stems topped with globe blue flower heads
TOPIARY_DRAGON      = 981  # dragon-shaped clipped topiary with wing silhouette
TOPIARY_GIRAFFE     = 982  # giraffe-shaped topiary with long neck
TOPIARY_HEDGEHOG    = 983  # round spiky hedgehog topiary
BUBBLE_FOUNTAIN     = 984  # rounded boulder with water beading over it
SHELL_FOUNTAIN      = 985  # scallop shell bowl fountain on stone pedestal
MILLSTONE_FOUNTAIN  = 986  # flat millstone with water flowing over its rim
TRELLIS_ARCH        = 987  # wooden arch draped with climbing plants
COLD_FRAME          = 988  # glass-lidded wooden cold frame for seedlings
GARDEN_SWING        = 989  # wooden swing seat hanging on rope
WICKER_FENCE        = 990  # low woven wicker garden fence
HANGING_BASKET      = 991  # wall-mounted hanging flower basket with trailing blooms
STANDARD_ROSE       = 992  # rose trained on a tall single stem (lollipop form)
GARDEN_GNOME        = 993  # cheerful ceramic garden gnome statue
TOPIARY_ARCH        = 994  # clipped evergreen hedge archway block
CHAMOMILE_LAWN      = 995  # low fragrant chamomile ground cover with tiny flowers
CREEPING_THYME      = 996  # dense mat of creeping thyme with purple micro-flowers
HYDRANGEA_BUSH      = 997  # large mophead hydrangea with blue/pink flower globes
ALLIUM_PATCH        = 998  # tall stems topped with globe purple allium heads
SWEET_PEA_TRELLIS   = 999  # climbing sweet peas on bamboo cane trellis
BLEEDING_HEART_PATCH= 1000 # arching stems with heart-shaped pendant flowers
ASTILBE_PATCH       = 1001 # feathery plume flowers in pink/red
WISTERIA_PILLAR     = 1002 # freestanding stone column draped in wisteria
TOPIARY_SNAIL       = 1003 # snail-shaped clipped topiary
TOPIARY_MUSHROOM    = 1004 # mushroom-shaped clipped topiary
TOPIARY_OWL         = 1005 # owl-shaped clipped topiary
TOPIARY_DINOSAUR    = 1006 # dinosaur-shaped clipped topiary
KOI_POOL            = 1007 # formal rectangular pond with visible koi
STONE_TROUGH_PLANTER= 1008 # old stone livestock trough repurposed as planter
RAIN_BARREL         = 1009 # wooden rain barrel with brass tap
MOSS_PATCH          = 1010 # lush cushion moss ground cover
CLOVER_LAWN         = 1011 # white clover ground cover with small flowers
BARK_MULCH          = 1012 # brown bark chip mulch ground cover
STONE_FROG          = 1013 # decorative carved stone frog ornament
GARDEN_DOVECOTE     = 1014 # white domed dovecote on tall timber pole
STONE_HEDGEHOG      = 1015 # carved stone hedgehog garden ornament
BIRD_TABLE          = 1016 # wooden bird feeding table on a post
GARDEN_CLOCK        = 1017 # decorative verdigris garden clock on post
GARDEN_OBELISK_METAL= 1018 # wrought-iron obelisk frame for climbing plants
POTTING_TABLE       = 1019 # wooden potting table with tools hanging above
COMPOST_HEAP        = 1020 # open compost heap with layered organic matter
GARDEN_TOAD_HOUSE   = 1021 # ceramic arch toad shelter with painted door
TRADE_BLOCK         = 1182 # Trade Post: assign horse+cart, link to city, auto-deliver goods
FORGE_BLOCK         = 1183 # Smithing station — heat metal and hammer weapon parts
WEAPON_RACK_BLOCK   = 1184 # Weapon rack — equip and browse crafted weapons

# Logic & Automation blocks (1185–1224); next free: 1225
SWITCH_BLOCK_OFF        = 1185   # lever — player toggles with E
SWITCH_BLOCK_ON         = 1186
LATCH_BLOCK_OFF         = 1187   # toggle flip-flop — player toggles with E
LATCH_BLOCK_ON          = 1188
AND_GATE_BLOCK          = 1189   # visual powered state read from logic_state
OR_GATE_BLOCK           = 1190
NOT_GATE_BLOCK          = 1191
DAM_BLOCK_CLOSED        = 1192   # water barrier — opaque, solid when closed
DAM_BLOCK_OPEN          = 1193   # passable gap when open
PUMP_BLOCK_OFF          = 1194
PUMP_BLOCK_ON           = 1195
IRON_GATE_BLOCK_CLOSED  = 1196   # 1-tall controllable gate
IRON_GATE_BLOCK_OPEN    = 1197

# --- Brewery supply chain ---
HOP_VINE_BUSH        = 1198   # surface bush; drops hop_seed
HOP_VINE_YOUNG       = 1199
HOP_VINE_MATURE      = 1200   # special: mine → Beer object + hop_seed drop
BREW_KETTLE_BLOCK    = 1201   # placed Brew Kettle (mash + boil mini-game)
FERM_VESSEL_BLOCK    = 1202   # placed Fermentation Vessel (yeast + ferment mini-game)
TAPROOM_BLOCK        = 1203   # placed Taproom (conditioning + bottle)

# Logic & Automation — extended sensors, timers, RS latch, outputs
PRESSURE_PLATE_OFF   = 1204
PRESSURE_PLATE_ON    = 1205
DAY_SENSOR_BLOCK     = 1206   # outputs 1 during day; right-click to toggle day/night mode
NIGHT_SENSOR_BLOCK   = 1207
WATER_SENSOR_BLOCK   = 1208   # outputs 1 when adjacent water
CROP_SENSOR_BLOCK    = 1209   # outputs 1 when block below is mature crop
REPEATER_BLOCK       = 1210   # delays signal; right-click to cycle delay (0.25–4s)
PULSE_GEN_BLOCK      = 1211   # emits periodic pulses; right-click to cycle period
RS_LATCH_Q0          = 1212   # RS latch, Q=False
RS_LATCH_Q1          = 1213   # RS latch, Q=True
POWERED_LANTERN_OFF  = 1214
POWERED_LANTERN_ON   = 1215
ALARM_BELL_OFF       = 1216
ALARM_BELL_ON        = 1217
IRRIGATION_CHANNEL_BLOCK = 1218

# Redstone-style memory & state blocks
COUNTER_BLOCK        = 1219   # counts N input pulses → holds output; reset pin; right-click cycles threshold
COMPARATOR_BLOCK     = 1220   # reads adjacent chest fill (0-8), outputs when level ≥ threshold
OBSERVER_BLOCK       = 1221   # emits 1-tick pulse when watched block changes; facing = watch dir
SEQUENCER_BLOCK      = 1222   # 4-step round-robin; each pulse rotates active output; right-click = manual step
T_FLIPFLOP_BLOCK     = 1223   # toggles Q on every rising edge; right-click = manual toggle
DEPOSIT_TRIGGER_BLOCK = 1224  # rising-edge: dumps nearby bot inventories into adjacent chest
AUTOMATION_BENCH_BLOCK = 1225  # crafting station for logic components and fluid infrastructure
CHICKEN_COOP_BLOCK   = 1226  # chicken coop; accumulates eggs from live female chickens


SAFFRON_DOOR_CLOSED      = 860  # warm golden-yellow with dark carved panels
SAFFRON_DOOR_OPEN        = 861


# --- European architecture blocks (Artisan Bench) ---
HALF_TIMBER_WALL  = 862  # Tudor black timber framing on white plaster
ASHLAR_BLOCK      = 863  # precisely dressed stone with tight regular joints
GOTHIC_TRACERY    = 864  # pointed lancet arch tracery panel
FLUTED_COLUMN     = 865  # classical column shaft with vertical flute grooves
CORNICE_BLOCK     = 866  # classical stepped projecting molding
ROSE_WINDOW       = 867  # Gothic circular window tracery
HERRINGBONE_BRICK = 868  # diagonal herringbone brick floor
BAROQUE_TRIM      = 869  # elaborate carved stone scrollwork panel
TUDOR_BEAM        = 870  # dark exposed structural timber
VENETIAN_FLOOR    = 871  # pale stone with diamond inlay accents
FLEMISH_BRICK     = 872  # two-tone Flemish bond brick
PILASTER          = 873  # classical flat wall column with capital and base
DENTIL_TRIM       = 874  # classical tooth-molding band
WATTLE_DAUB       = 875  # medieval woven-straw plaster wall
NORDIC_PLANK      = 876  # dark weathered Nordic timber
MANSARD_SLATE     = 877  # French fish-scale roof slate
ROMAN_MOSAIC      = 878  # small square tiles in warm geometric pattern
SETT_STONE        = 879  # European granite street sett
ROMANESQUE_ARCH   = 880  # warm sandstone rounded arch voussoir panel
DARK_SLATE_ROOF   = 881  # overlapping dark grey-blue slate shingles
KEYSTONE          = 882  # arch keystone wedge block
PLINTH_BLOCK      = 883  # classical column base with recessed panel
IRON_LANTERN      = 884  # Victorian iron lantern frame with warm glow
SANDSTONE_ASHLAR  = 885  # warm sandstone with precise rectangular joints
GARGOYLE_BLOCK    = 886  # Gothic grotesque carved stone panel
OGEE_ARCH         = 887  # S-curved ogee arch with finial (Gothic/Venetian)
RUSTICATED_STONE  = 888  # Renaissance rough-faced stone with deep V-joints
CHEVRON_STONE     = 889  # Norman zigzag carved stone
TRIGLYPH_PANEL    = 890  # Doric frieze with vertical channels and guttae
MARBLE_INLAY      = 891  # Italian white marble with coloured geometric inlay
BRICK_NOGGING     = 892  # brick infill between timber frame panels
CRENELLATION      = 893  # castle battlement with merlons and crenels
FAN_VAULT         = 894  # Gothic fan vaulting panel with radiating ribs
ACANTHUS_PANEL    = 895  # Corinthian carved acanthus leaf panel
PEBBLE_DASH       = 896  # rough exterior render with embedded pebbles
ENCAUSTIC_TILE    = 897  # medieval inlaid terracotta floor tile
CHEQUERBOARD_MARBLE = 898  # alternating black and white marble squares
WROUGHT_IRON_BALUSTRADE = 899  # decorative iron balcony balustrade
OPUS_INCERTUM     = 900  # Roman irregular polygon stone facing
GROTESQUE_FRIEZE  = 901  # carved stone frieze with foliage and faces
BARREL_VAULT      = 902  # Romanesque semicircular vault section
POINTED_ARCH      = 903  # clean Gothic pointed arch
ENGLISH_BOND      = 904  # alternating header/stretcher brick courses
RELIEF_PANEL      = 905  # Classical carved stone relief
DIAGONAL_TILE     = 906  # European diagonal square floor tile
# --- Sonoran desert plants ---
SAGUARO_YOUNG       = 389
SAGUARO_MATURE      = 390
BARREL_CACTUS_YOUNG = 391
BARREL_CACTUS_MATURE= 392
OCOTILLO_YOUNG      = 393
OCOTILLO_MATURE     = 394
PRICKLY_PEAR_YOUNG  = 395
PRICKLY_PEAR_MATURE = 396
CHOLLA_YOUNG        = 397
CHOLLA_MATURE       = 398
PALO_VERDE_YOUNG    = 399
PALO_VERDE_MATURE   = 400

# --- More decorative/architectural blocks (Artisan Bench) ---
TAPESTRY_BLOCK    = 401  # woven textile wall hanging with colour bands
WOVEN_RUG         = 402  # geometric medallion floor rug
CELTIC_KNOTWORK   = 403  # interlaced Celtic knot carved stone
BYZANTINE_MOSAIC  = 404  # gold-ground tessera mosaic panel
JAPANESE_SHOJI    = 405  # rice-paper and wood grid screen
OTTOMAN_TILE      = 406  # Iznik white ceramic with deep-blue tulip
LEADLIGHT_WINDOW  = 407  # leaded diamond-pane window
TUDOR_ROSE        = 408  # heraldic rose carved stone panel
GREEK_KEY         = 409  # classical meander/fret border tile
VENETIAN_PLASTER  = 410  # burnished smooth marmorino plaster
SCOTTISH_RUBBLE   = 411  # random coursed rubble stone wall
ART_NOUVEAU_PANEL = 412  # sinuous organic carved panel
DUTCH_GABLE       = 413  # curved stepped gable element
STRIPED_ARCH      = 414  # alternating dark/light voussoir arch
TIMBER_TRUSS      = 415  # exposed structural A-frame truss
HEARTH_STONE      = 416  # decorative fireplace arch surround
LINEN_FOLD        = 417  # Gothic carved draped fabric panel
PARQUET_FLOOR     = 418  # French herringbone parquet
COFFERED_CEILING  = 419  # classical sunken panel ceiling block
OPUS_SIGNINUM     = 420  # Roman pink mortar with white tessera chips

# --- Textile supply chain ---
FLAX_BUSH           = 421  # surface bush; drops flax_seed
FLAX_CROP_YOUNG     = 422
FLAX_CROP_MATURE    = 423  # harvest → flax_fiber + flax_seed
SPINNING_WHEEL_BLOCK= 424  # placed Spinning Wheel (spinning mini-game)
DYE_VAT_BLOCK       = 425  # placed Dye Vat (wildflower extract → dye)
LOOM_BLOCK          = 426  # placed Loom (weaving mini-game)
# Textile rug blocks (9 dye families, placeable floor piece)
TEXTILE_RUG_NATURAL = 427
TEXTILE_RUG_GOLDEN  = 428
TEXTILE_RUG_CRIMSON = 429
TEXTILE_RUG_ROSE    = 430
TEXTILE_RUG_COBALT  = 431
TEXTILE_RUG_VIOLET  = 432
TEXTILE_RUG_VERDANT = 433
TEXTILE_RUG_AMBER   = 434
TEXTILE_RUG_IVORY   = 435
# Textile tapestry blocks (9 dye families, placeable wall piece)
TEXTILE_TAPESTRY_NATURAL = 436
TEXTILE_TAPESTRY_GOLDEN  = 437
TEXTILE_TAPESTRY_CRIMSON = 438
TEXTILE_TAPESTRY_ROSE    = 439
TEXTILE_TAPESTRY_COBALT  = 440
TEXTILE_TAPESTRY_VIOLET  = 441
TEXTILE_TAPESTRY_VERDANT = 442
TEXTILE_TAPESTRY_AMBER   = 443
TEXTILE_TAPESTRY_IVORY   = 444

# --- Chinese architecture blocks (Artisan Bench) ---
GLAZED_ROOF_TILE  = 445  # imperial green-glazed curved ceramic roof tile
LATTICE_SCREEN    = 446  # carved geometric wooden lattice window
MOON_GATE         = 447  # circular archway panel (round garden gate)
PAINTED_BEAM      = 448  # red lacquered structural beam with gold accents
DOUGONG           = 449  # stacked bracket-set corbel (classic Chinese joinery)
CERAMIC_PLANTER   = 450  # blue-and-white porcelain garden planter
STONE_LANTERN     = 451  # tiered stone garden lantern
LACQUER_PANEL     = 452  # deep red lacquered decorative wall panel
PAPER_LANTERN     = 453  # red paper lantern with tassel
DRAGON_TILE       = 454  # celadon tile with carved dragon scale motif
HAN_BRICK         = 455  # traditional grey Han fired brick
PAVILION_FLOOR    = 456  # smooth large-cut stone pavilion floor
BAMBOO_SCREEN     = 457  # woven split-bamboo screen
CLOUD_MOTIF       = 458  # stone panel with auspicious ruyi cloud carving
COIN_TILE         = 459  # floor tile with four cash-coin roundels
BLUE_WHITE_TILE   = 460  # blue-and-white porcelain willow tile
GARDEN_ROCK       = 461  # Taihu scholar's rock with natural voids
STEPPED_WALL      = 462  # rammed earth/grey brick wall
PAGODA_EAVE       = 463  # upturned pagoda roof eave element
CINNABAR_WALL     = 464  # deep red cinnabar wall with gilt nail-heads

# --- Himalayan / Snow-city architecture (used by city generator) ---
WHITEWASHED_WALL  = 465  # white plastered Tibetan-style wall with dark trim band
MONASTERY_ROOF    = 466  # dark maroon stepped monastery roof tile
MANI_STONE        = 467  # carved prayer-stone block for fortress bases and walls
PRAYER_FLAG_BLOCK = 468  # colorful prayer flags strung on a cord

# --- World architecture blocks — batch 4 (Artisan Bench) ---
MUGHAL_ARCH       = 469  # Mughal cusped multi-foil arch
PIETRA_DURA       = 470  # Mughal inlaid stone floral panel (Taj Mahal style)
EGYPTIAN_FRIEZE   = 471  # lotus-and-papyrus hieroglyphic border
SANDSTONE_COLUMN  = 472  # Egyptian papyrus-bundle column with spreading capital
AZTEC_SUNSTONE    = 473  # Aztec solar calendar carved stone disc
MAYA_RELIEF       = 474  # Maya stepped geometric relief panel
VIKING_CARVING    = 475  # Norse interlaced dragon/serpent wood carving
RUNE_STONE        = 476  # carved runestone with Elder Futhark symbols
PERSIAN_IWAN      = 477  # Persian pointed arch with muqarnas vault interior
KILIM_TILE        = 478  # Persian kilim carpet geometric tile
AFRICAN_MUD_BRICK = 479  # West African banco mud brick with timber-end studs
KENTE_PANEL       = 480  # West African kente woven-strip geometric block
WAT_FINIAL        = 481  # Thai Buddhist temple chofa spire element
KHMER_STONE       = 482  # Cambodian Angkor devata carved stone
HANJI_SCREEN      = 483  # Korean hanji paper flower-lattice screen
DANCHEONG         = 484  # Korean dancheong painted bracket (multicolour)
ART_DECO_PANEL    = 485  # Art Deco geometric sunburst fan panel
OBSIDIAN_CUT      = 486  # Aztec polished obsidian architectural block
OTTOMAN_ARCH      = 487  # Ottoman pointed arch with geometric spandrel
LOTUS_CAPITAL     = 488  # Buddhist lotus-petal column capital

# --- World architecture blocks — batch 5 (Artisan Bench) ---
AZULEJO_TILE       = 489  # Portuguese blue-and-white pictorial tile
MANUELINE_PANEL    = 490  # Portuguese Manueline twisted rope/armillary carving
TORII_PANEL        = 491  # Japanese red torii gate element
INCA_ASHLAR        = 492  # Incan precisely fitted polygonal stone
RUSSIAN_KOKOSHNIK  = 493  # Russian kokoshnik decorative arch/gable
ONION_DOME_TILE    = 494  # Russian onion dome metallic surface tile
GEORGIAN_FANLIGHT  = 495  # Georgian semi-circular fanlight window
PALLADIAN_WINDOW   = 496  # Palladian triple-arch window panel
STAVE_PLANK        = 497  # Norwegian stave church dragon-carved plank
IONIC_CAPITAL      = 498  # Greek Ionic volute column capital
MOORISH_STAR_TILE  = 499  # Moorish eight-pointed star-and-cross tile
CRAFTSMAN_PANEL    = 500  # Arts & Crafts stylised floral carved panel
BRUTALIST_PANEL    = 501  # Brutalist board-formed concrete
METOPE             = 502  # Greek Doric carved metope panel
ARMENIAN_KHACHKAR  = 503  # Armenian khachkar cross-stone
BENIN_RELIEF       = 504  # Benin Kingdom cast-bronze relief
MAORI_CARVING      = 505  # Māori koru spiral wood carving
MUGHAL_JALI        = 506  # Mughal pierced-stone jali screen
PERSIAN_TILE       = 507  # Persian turquoise glazed geometric tile
SWISS_CHALET       = 508  # Swiss chalet carved and painted wood panel
ANDEAN_TEXTILE     = 509  # Andean stepped-fret woven pattern block
BAROQUE_ORNAMENT   = 510  # German/Austrian Baroque gilded ornament
POLYNESIAN_CARVED  = 511  # Polynesian tapa/carved tiki pattern
MOORISH_COLUMN     = 512  # Slender Moorish column with muqarnas capital
PORTUGUESE_CORK    = 513  # Portuguese cork-board wall panel

# --- Cheese supply chain ---
DAIRY_VAT_BLOCK    = 514  # placed Dairy Vat (curdling mini-game)
CHEESE_PRESS_BLOCK = 515  # placed Cheese Press (pressing + type selection)
AGING_CAVE_BLOCK   = 516  # placed Aging Cave (duration + care aging)

# --- Hunting supply chain ---
FLETCHING_TABLE_BLOCK = 517  # placed Fletching Table; crafts bows and arrows

# --- Geological strata (replace generic STONE at increasing depths) ---
LIMESTONE_STONE = 518   # depth 15–60
GRANITE_STONE   = 519   # depth 60–120
BASALT_STONE    = 520   # depth 120–180
MAGMATIC_STONE  = 521   # depth 180+

# --- Ore processing ---
SMELTER_BLOCK        = 522   # placed Smelter; converts raw ore → refined metal
ANAEROBIC_TANK_BLOCK = 523   # placed Anaerobic Tank; advanced coffee processing

# --- Glass Kiln station + glass blocks ---
GLASS_KILN_BLOCK        = 524  # placed Glass Kiln; smelts sand + dye extracts into glass
CLEAR_GLASS             = 525  # plain clear glass pane
STAINED_GLASS_GOLDEN    = 526  # golden dye stained glass
STAINED_GLASS_CRIMSON   = 527  # crimson dye stained glass
STAINED_GLASS_ROSE      = 528  # rose dye stained glass
STAINED_GLASS_COBALT    = 529  # cobalt dye stained glass
STAINED_GLASS_VIOLET    = 530  # violet dye stained glass
STAINED_GLASS_VERDANT   = 531  # verdant dye stained glass
STAINED_GLASS_AMBER     = 532  # amber dye stained glass
STAINED_GLASS_IVORY     = 533  # ivory dye stained glass
CATHEDRAL_WINDOW        = 534  # ornate Gothic arch window
MOSAIC_GLASS            = 535  # multi-color mosaic tile glass
SMOKED_GLASS            = 536  # dark tinted smoked glass

# --- Elevator system ---
ELEVATOR_STOP_BLOCK  = 537  # call station placed at each floor
ELEVATOR_CABLE_BLOCK = 538  # vertical shaft connecting stops (same x-column)

# --- Additional glass varieties ---
RIBBED_GLASS            = 539  # vertical ribbed texture
HAMMERED_GLASS          = 540  # irregular hammered surface
CRACKLED_GLASS          = 541  # ice-crackle pattern
OCULUS_WINDOW           = 542  # circular porthole with spokes
LANCET_WINDOW           = 543  # tall narrow Gothic lancet
DIAMOND_PANE            = 544  # classic diamond-grid leaded panes
SEA_GLASS               = 545  # frosted seafoam beach glass
MIRROR_GLASS            = 546  # polished silver-mirror surface
IRIDESCENT_GLASS        = 547  # rainbow oil-slick shimmer
SUNSET_GLASS            = 548  # warm amber-to-rose gradient panes
OBSIDIAN_GLASS          = 549  # volcanic black glass from obsidian
CRYSTAL_GLASS           = 550  # pure crystal with sparkle facets
JEWELRY_WORKBENCH_BLOCK = 551  # placed Jewelry Workbench (custom jewelry mini-game)

# --- Garden Workshop system ---
GARDEN_WORKSHOP_BLOCK = 552  # placed Garden Workshop (Alhambra / Italian garden crafting)
ZELLIGE_BLUE          = 553  # Moorish glazed geometric tile — cobalt blue
ZELLIGE_TERRACOTTA    = 554  # Moorish glazed geometric tile — warm terracotta
ZELLIGE_EMERALD       = 555  # Moorish glazed geometric tile — deep emerald
ZELLIGE_WHITE         = 556  # Moorish glazed geometric tile — ivory white
GARDEN_STAR_TILE      = 557  # dark stone with 8-pointed star inlay
GEOMETRIC_MOSAIC      = 558  # multi-colour diamond/triangle mosaic paving
WATER_CHANNEL         = 559  # narrow acequia rill; still water strip
ORNAMENTAL_POOL       = 560  # shallow reflecting pool surface
FOUNTAIN_BASIN        = 561  # carved stone fountain basin with jet
TIERED_FOUNTAIN       = 562  # two-tier stone fountain
HORSESHOE_ARCH        = 563  # classic Moorish pointed horseshoe arch
MUQARNAS_PANEL        = 564  # honeycomb stalactite plaster corbel
ARABESQUE_SCREEN      = 565  # pierced geometric stone screen
GARDEN_COLUMN         = 566  # fluted stone column shaft
MARBLE_PLINTH         = 567  # pedestal / column base with molding
GARDEN_OBELISK        = 568  # tall tapered stone obelisk
TOPIARY_CONE          = 569  # clipped evergreen cone topiary
TOPIARY_SPHERE        = 570  # clipped evergreen sphere topiary
BOX_HEDGE             = 571  # formal low clipped box hedge
CLIMBING_ROSE         = 572  # roses climbing a timber trellis
STONE_BENCH           = 573  # stone garden bench
STONE_URN             = 574  # large decorative stone urn / vase
TERRACOTTA_PLANTER    = 575  # large terracotta garden pot
SUNDIAL               = 576  # garden sundial on stone pedestal
GARDEN_LANTERN        = 577  # Moorish-style iron lantern
GRAVEL_PATH           = 578  # fine crushed-stone garden path
MOSAIC_PATH           = 579  # ornamental coloured-stone mosaic path
TERRACOTTA_PATH       = 580  # warm terracotta floor tile path
COBBLE_CIRCLE         = 581  # circular cobblestone centrepiece

# --- Sculpture system ---
SCULPTURE_BLOCK_ROOT  = 582  # bottom block of a player-carved sculpture
SCULPTURE_BLOCK_BODY  = 583  # upper continuation blocks of a tall sculpture
SCULPTORS_BENCH       = 584  # crafting station for the sculpture mini-game

# --- Garden Workshop extension blocks ---
PERGOLA_POST          = 585  # timber pergola upright with climbing vine
WISTERIA_ARCH         = 586  # stone arch draped in purple wisteria
GARDEN_GATE           = 587  # ornamental wrought-iron gate panel
LOW_GARDEN_WALL       = 588  # coped stone garden boundary wall
POOL_COPING           = 589  # flat stone edge for pools and channels
STEPPING_STONE        = 590  # large flat irregular stepping stone in grass
OPUS_VERMICULATUM     = 591  # fine Roman worm-path mosaic floor
PORPHYRY_TILE         = 592  # deep purple-red igneous stone floor tile
BRICK_EDGING          = 593  # soldier-course brick border strip
SPIRAL_TOPIARY        = 594  # spiraling clipped column topiary
MAZE_HEDGE            = 595  # tall dense hedge for formal garden mazes
WISTERIA_WALL         = 596  # wall surface cascading in purple wisteria
POTTED_CITRUS         = 597  # orange/lemon tree in terracotta pot
MARBLE_STATUE         = 598  # classical draped marble figure on base
MARBLE_BIRDBATH       = 599  # ornate stone birdbath on pedestal
GARDEN_TABLE          = 600  # low stone garden table
IRON_TRELLIS          = 601  # decorative wrought-iron trellis panel
NASRID_PANEL          = 602  # elaborate Alhambra hall carved plaster
SCALLOP_NICHE         = 603  # shell-shaped Moorish wall niche
TERRACE_BALUSTRADE    = 604  # Italian terrace balustraded railing section

# --- Japanese garden blocks ---
ZEN_GRAVEL          = 605  # raked dry-garden gravel with rake-line texture
KARESANSUI_ROCK     = 606  # standalone dry-landscape garden rock
MOSS_CARPET         = 607  # soft dense green moss ground cover
TSUKUBAI            = 608  # low stone water basin with bamboo ladle
TORO_LANTERN        = 609  # tall stone tōrō garden lantern on pedestal
YUKIMI_LANTERN      = 610  # wide-capped snow-viewing yukimi-dōrō lantern
BAMBOO_FENCE_JP     = 611  # woven bamboo fence panel
ROJI_STONE          = 612  # irregular flat roji path stone in moss
PINE_TOPIARY_JP     = 613  # cloud-pruned niwaki pine
JAPANESE_MAPLE      = 614  # Japanese maple with red-orange autumn leaves
SHISHI_ODOSHI       = 615  # bamboo shishi-odoshi deer-scarer
RED_ARCH_BRIDGE     = 616  # red lacquer taiko arched garden bridge
WAVE_CERAMIC        = 617  # blue-white nami wave pattern ceramic floor
ZEN_SAND_RING       = 618  # flat sand with concentric raked circles
BAMBOO_GATE_JP      = 619  # rustic bamboo kakehi garden gate
WABI_STONE          = 620  # weathered moss-covered tachi-ishi standing stone
CHERRY_ARCH         = 621  # arch draped in pink sakura cherry blossom
TATAMI_PAVING       = 622  # flat square stone with subtle tatami grid
IKEBANA_STONE       = 623  # flat presentation stone for flower arrangement
KANJI_STONE         = 624  # carved stone with calligraphic brushstroke
MAPLE_LEAF_TILE     = 625  # stone tile with autumn maple-leaf inlay
NOREN_PANEL         = 626  # split indigo fabric noren entrance curtain
TSURU_TILE          = 627  # crane motif auspicious ceramic floor tile
PINE_SCREEN_JP      = 628  # pine-and-moon painted shōji-style screen
KARE_BRIDGE         = 629  # flat stone bridge crossing dry gravel stream

# --- Chinese garden blocks ---
PEBBLE_MOSAIC_CN    = 630  # traditional luanshi cobblestone pebble mosaic
ZIGZAG_BRIDGE       = 631  # segment of the classic jiuqu nine-turn bridge
CLOUD_WALL          = 632  # white-plastered wall with cloud-shaped leaking window
DRAGON_WALL_CN      = 633  # wall crest carved with sinuous dragon
LOTUS_POND          = 634  # water surface with floating lotus flowers
HEX_PAVILION_TILE   = 635  # hexagonal six-sided pavilion floor tile
COMPASS_PAVING      = 636  # large stone compass-rose medallion
WAVE_BALUSTRADE_CN  = 637  # cloud-and-wave carved stone balustrade
CERAMIC_SEAT        = 638  # blue-and-white porcelain barrel garden seat
BONSAI_TRAY         = 639  # flat stone tray with miniature potted bonsai
SCHOLAR_SCREEN      = 640  # lattice screen framing a scholar's rock viewing window
CHRYSANTHEMUM_TILE  = 641  # ceramic tile with chrysanthemum roundel
PLUM_BLOSSOM_TILE   = 642  # ceramic tile with plum-blossom meihua pattern
MOON_PAVEMENT       = 643  # circular moon-gate shaped stone paving inset
BAMBOO_GROVE        = 644  # dense cluster of green bamboo stalks
OSMANTHUS_BUSH      = 645  # sweet osmanthus guihua flowering shrub
WATER_LILY_TILE     = 646  # water tile with floating lily pads
KOI_POND            = 647  # ornamental koi pond with colourful fish visible
LAKESIDE_ROCK       = 648  # low flat rock at a water garden's edge
CLOUD_COLLAR_TILE   = 649  # ruyi cloud-collar shaped decorative floor tile
IMPERIAL_PAVING     = 650  # large-format imperial huabiao courtyard stone
PAVILION_COLUMN_CN  = 651  # red lacquered dougong pavilion column
EIGHT_DIAGRAM       = 652  # bagua eight-trigram carved stone tile
TEA_HOUSE_STEP      = 653  # worn stone step leading to a teahouse entrance
LANTERN_FESTIVAL    = 654  # red paper lanterns strung on a cord

# --- Renaissance garden blocks ---
# Classical architecture
IONIC_COLUMN_BASE   = 655  # Ionic column with volute capital and fluted shaft
DORIC_ENTABLATURE   = 656  # Doric frieze band with triglyphs and metopes
RUSTICATED_BASE     = 657  # heavy V-jointed rusticated stone plinth
GARDEN_LOGGIA       = 658  # open colonnaded loggia arch bay
TRIUMPHAL_ARCH_R    = 659  # classical Roman-style triumphal arch
EXEDRA_SEAT         = 660  # curved semicircular stone exedra bench
HERM_PILLAR         = 661  # classical herm/term boundary marker pillar
NYMPHAEUM_PANEL     = 662  # grotto niche with shell and cascade decoration
GROTTO_STONE        = 663  # rough tufa/rustic grotto stalactite stonework
AMPHITHEATER_TIER   = 664  # curved green theater seating tier
# Water features
GIOCHI_ACQUA        = 665  # surprise water jet hidden in paving (giochi d'acqua)
RILL_BLOCK          = 666  # long straight formal water rill channel
CASCADE_BLOCK       = 667  # stepped water cascade element
GROTTO_POOL         = 668  # dark mossy grotto pool surface
WALL_FOUNTAIN       = 669  # wall-mounted grotesque mask fountain
BASIN_SURROUND      = 670  # ornate carved stone basin rim
CANAL_BLOCK         = 671  # formal straight garden canal
TERME_POOL          = 672  # heated bathing/terme pool section
# Parterre and planting
PARTERRE_BRODERIE   = 673  # low clipped box embroidery parterre bed
PARTERRE_COMPARTMENT= 674  # geometric parterre garden compartment
ALLEE_TREE          = 675  # clipped allée tree for formal avenue
PLEACHED_HEDGE      = 676  # trained pleached lime/hornbeam screen
ESPALIER_WALL       = 677  # fruit tree trained flat against a wall
KNOT_GARDEN         = 678  # interlaced Renaissance knot garden bed
TURF_THEATER        = 679  # grassy amphitheater-style turf step
CARPET_BED          = 680  # colorful Victorian-style carpet bedding
# Paths and flooring
OPUS_SECTILE        = 681  # marble cut-shape geometric opus sectile floor
TRAVERTINE_FLOOR    = 682  # warm Roman travertine stone floor tile
HERRINGBONE_GARDEN  = 683  # outdoor herringbone brick garden path
RAMP_STONE          = 684  # gentle stone ramp / slope block
GARDEN_STEPS        = 685  # classical stone garden steps
SAND_ALLEE          = 686  # compacted sand formal allée path
PATTERNED_PAVEMENT  = 687  # complex two-tone geometric pavement
INLAID_MARBLE       = 688  # colored marble geometric inlay floor
# Furnishings and decorative
TALL_SUNDIAL        = 689  # tall sundial on ornate carved pedestal
STONE_VASE          = 690  # large classical stone amphora/vase
STONE_SPHERE        = 691  # decorative stone ball finial on plinth
CURVED_BENCH        = 692  # curved stone garden exedra bench section
ORNATE_GATE         = 693  # ornate wrought-iron scrollwork garden gate
LEAD_PLANTER        = 694  # lead-lined classical garden planter
TERRACE_URN         = 695  # large terrace urn on tall pedestal
STONE_PINEAPPLE     = 696  # stone pineapple finial (symbol of hospitality)
# Structural elements
GROTTO_ARCH         = 697  # rustic grotto arch with tufa/stalactite trim
PERGOLA_BEAM        = 698  # horizontal pergola beam/rafter with vine
LOGGIA_ARCH         = 699  # open loggia arch with paired columns
GARDEN_WALL_NICHE   = 700  # alcoved garden wall niche for a statue
ORANGERY_WINDOW     = 701  # tall orangery/greenhouse arched window
BELVEDERE_PANEL     = 702  # belvedere garden tower wall section
BOSCO_TREE          = 703  # wild bosco/wilderness garden tree
GIARDINO_SEGRETO    = 704  # secret garden high enclosed wall panel

# --- Rare sculptable stone veins (natural underground deposits) ---
MARBLE_VEIN         = 705  # white/gray veined marble; depth 25-80, sedimentary
ALABASTER_VEIN      = 706  # warm ivory alabaster; depth 15-55, sedimentary/temperate
VERDITE_VEIN        = 707  # deep forest-green verdite; depth 60-140, igneous
ONYX_VEIN           = 708  # near-black with white banding; depth 130-240, igneous

# --- Placed blocks for the rare stones ---
ALABASTER_BLOCK     = 709  # smooth ivory alabaster building block
VERDITE_BLOCK       = 710  # polished deep-green verdite tile
ONYX_BLOCK          = 711  # polished black onyx with faint banding

# --- Renaissance palace blocks (Artisan Bench / Garden Workshop) ---
# Facade stonework
PIETRA_SERENA        = 712  # blue-grey Florentine sandstone (Brunelleschi)
TRAVERTINE_WALL      = 713  # cut Roman travertine ashlar block with pitting
MARBLE_FACADE        = 714  # white Carrara marble smooth wall panel
RUSTICATED_QUOIN     = 715  # bossage rusticated corner quoin
BICOLOR_MARBLE       = 716  # two-tone white/green Florentine marble inlay
PINK_GRANITE_BASE    = 717  # polished pink granite socle / plinth
BLIND_ARCH           = 718  # decorative blind arch recess in ashlar wall
CONSOLE_CORNICE      = 719  # projecting modillion/console bracket cornice
# Columns and pilasters
CORINTHIAN_CAPITAL   = 720  # acanthus-leaf Corinthian column capital
GIANT_PILASTER       = 721  # colossal-order flat fluted pilaster strip
ENGAGED_COLUMN       = 722  # half-round fluted column engaged in wall
ATLAS_FIGURE         = 723  # male atlante/telamon figure support column
CARYATID_COLUMN      = 724  # female caryatid draped figure column
COMPOSITE_CAPITAL    = 725  # Ionic volutes + Corinthian acanthus composite capital
# Interior walls
INTARSIA_PANEL       = 726  # inlaid wood geometric intarsia wall panel
STUDIOLO_WALL        = 727  # trompe-l'oeil studiolo open-cabinet panel
GILT_LEATHER         = 728  # embossed gilded leather wall covering
FRESCO_LUNETTE       = 729  # arched fresco-painted lunette panel
WAINSCOT_MARBLE      = 730  # lower marble wall wainscoting strip
TAPESTRY_FRAME       = 731  # gilded carved frame for hanging tapestry
# Ceilings
LACUNAR_CEILING      = 732  # deep coffered lacunar ceiling with rosettes
BARREL_FRESCO        = 733  # barrel vault with painted fresco interior
GOLDEN_CEILING       = 734  # gilded flat palatial coffered ceiling
GROTESQUE_VAULT      = 735  # Renaissance grotesque painted vault panel
CUPOLA_OCULUS        = 736  # painted dome with central light oculus
# Floors
COSMATESQUE_FLOOR    = 737  # coloured Cosmatesque marble geometric floor
TERRAZZO_FLOOR_REN   = 738  # Venetian terrazzo aggregate chip floor
OPUS_ALEXANDRINUM    = 739  # porphyry and granite concentric medallion floor
MARBLE_MEDALLION_REN = 740  # large circular marble floor inlay medallion
PALACE_FLOOR_TILE    = 741  # large polished stone palace floor tile
# Doorways and windows
PALACE_PORTAL        = 742  # grand classical palace entrance portal arch
AEDICULE_FRAME       = 743  # tabernacle / aedicule pedimented door frame
THERMAL_WINDOW       = 744  # semicircular Diocletian thermal window
BIFORA_WINDOW        = 745  # divided twin-arch window with central column
SERLIANA_WINDOW      = 746  # Serliana triple-arch Venetian window
PALAZZO_BALCONY      = 747  # projecting balustraded palazzo balcony
# Arches and vaulting
ROMAN_ARCH_REN       = 748  # plain semicircular classical Roman arch
BARREL_VAULT_COFFER  = 749  # coffered barrel vault ceiling piece
PENDENTIVE_BLOCK     = 750  # triangular dome pendentive transition
GROIN_VAULT          = 751  # groin cross-vault ceiling with diagonal ribs
# Fireplaces and niches
RENAISSANCE_MANTEL   = 752  # carved marble fireplace mantelpiece
CHIMNEY_BREAST_REN   = 753  # projecting stone chimney breast
PEDIMENTED_NICHE     = 754  # triangular-pedimented wall niche for statuary
SHELL_NICHE_REN      = 755  # shell-hooded decorative wall niche
# Decorative ornament
CARTOUCHE_REN        = 756  # carved stone cartouche / shield surround
PUTTI_FRIEZE         = 757  # cherub putti relief frieze band
FESTOON_PANEL        = 758  # fruit and flower festoon garland panel
TROPHY_PANEL_REN     = 759  # armour and weapons trophy carved relief
MEDALLION_PORTRAIT   = 760  # round portrait bust medallion in carved frame
LAUREL_FRIEZE        = 761  # classical laurel-wreath border frieze

# --- Pottery & Ceramics ---
POTTERY_WHEEL_BLOCK  = 762  # shaping station — interactive profile editor
POTTERY_KILN_BLOCK   = 763  # firing station — temperature mini-game + glazing

# --- Portuguese / Spanish Ceramic Tiles ---
CALCADA_PORTUGUESA   = 764  # black & white wave-mosaic cobblestone pavement
AZULEJO_GEOMETRIC    = 765  # bold repeating diamond/compass geometric azulejo
PAINTED_TILE_BORDER  = 766  # blue & yellow decorative border/trim tile
SPANISH_MAJOLICA     = 767  # colorful folk-art majolica tile (cream, green, ochre)
AZULEJO_STAIR        = 768  # blue-painted azulejo stair-riser tile
PORTUGUESE_PINK_MARBLE = 769  # Estremoz rose-pink marble floor tile
SPANISH_HEX_TILE       = 770  # black & white hexagonal encaustic floor
MUDEJAR_STAR_TILE      = 771  # 8-pointed star Mudéjar ceramic tile
ALBARRADA_PANEL        = 772  # Portuguese vase-of-flowers azulejo panel
SGRAFFITO_WALL         = 773  # two-tone scraped-plaster wall
TRENCADIS_PANEL        = 774  # Gaudí broken-tile mosaic panel
AZULEJO_NAVY           = 775  # deep navy plain azulejo (dado/wainscoting)
AZULEJO_MANGANESE      = 776  # manganese-purple 17th-century azulejo
PLATERESQUE_PANEL      = 777  # ornate Spanish Plateresque carved stone relief
AZULEJO_CORNICE        = 778  # blue & white tile cornice frieze
TALAVERA_FOUNTAIN      = 779  # Talavera-tiled fountain basin piece
BARCELONA_TILE         = 780  # Catalan Modernista floor tile
MOORISH_ARCHWAY_TILE   = 781  # Mudéjar horseshoe-arch tile
PORTUGUESE_CHIMNEY     = 782  # ornamental Portuguese chimney pot
BARCELOS_TILE          = 783  # Portuguese Barcelos rooster folk-art tile
REJA_PANEL             = 784  # Spanish Rejas iron-grid window panel
ORANGE_TREE_PLANTER    = 785  # majolica-painted ceramic orange-tree planter
WAVE_COBBLE            = 786  # pale limestone wave-patterned pavement
AZULEJO_FACADE_PANEL   = 787  # large-format blue/white azulejo facade panel
MUDEJAR_BRICK          = 788  # ornamental Mudéjar geometric brickwork
PORTUGUESE_BENCH       = 789  # stone bench with azulejo-tiled seat
SPANISH_PATIO_FLOOR    = 790  # octagonal patio tile with dark corner inserts
ARABIC_ROOF_TILE       = 791  # half-round Arabic barrel roof tile
MOORISH_COLUMN_TILE    = 792  # zellige-clad decorative column section
ESTREMOZ_MARBLE        = 793  # white Estremoz marble tile
WILDFLOWER_DISPLAY_BLOCK = 794  # decorative vase; holds one wildflower from the player's collection

# --- Córdoba / Umayyad Architecture ---
MEZQUITA_ARCH          = 907  # alternating red & cream voussoir arch block

# --- Cotton supply chain ---
COTTON_BUSH         = 908  # surface bush; drops cotton_seed
COTTON_CROP_YOUNG   = 909
COTTON_CROP_MATURE  = 910  # harvest → cotton_fiber + cotton_seed
MIHRAB_TILE            = 795  # golden tessera mosaic mihrab niche panel
MEDINA_AZAHARA_STONE   = 796  # white marble carved acanthus relief (Medina Azahara)
CORDOBA_COLUMN         = 797  # slender Umayyad marble column section
ORANGE_COURT_FLOOR     = 798  # Court of Oranges geometric stone paving
CORDOBAN_LEATHER       = 799  # embossed guadamecil gold-on-leather wall panel
UMAYYAD_MULTILOBED     = 800  # multi-lobed polyfoil Umayyad arch tile
GOLD_TESSERA_PANEL     = 801  # Byzantine/Umayyad gold tessera mosaic panel
UMAYYAD_DOME_RIB       = 802  # rib section of a Umayyad stone vault
KUFIC_PANEL            = 803  # carved Kufic calligraphy stone panel
PATIO_FLOWER_WALL      = 804  # whitewashed wall with hanging ceramic geranium pots
CORDOBAN_PATIO_TILE    = 805  # small geometric Cordoban patio floor tile
STAR_VAULT_PANEL       = 806  # 8-pointed star Umayyad ceiling vault tile
ANDALUSIAN_FOUNTAIN    = 807  # small Cordoban courtyard basin fountain
NASRID_HONEYCOMB       = 808  # honeycomb muqarnas ceiling panel

# --- Pottery display ---
POTTERY_DISPLAY_BLOCK  = 809  # placeable pedestal; stores and displays a fired PotteryPiece vase

# --- Medieval Castle ---
PORTCULLIS_BLOCK       = 810  # iron drop-gate with vertical bars and pointed bases
ARROW_LOOP             = 811  # narrow cruciform arrow-slit in thick stone wall
MACHICOLATION          = 812  # projecting corbelled parapet with drop holes
DRAWBRIDGE_PLANK       = 813  # heavy oak drawbridge plank with iron strap bands
ROUND_TOWER_WALL       = 814  # curved ashlar tower wall section
CURTAIN_WALL           = 815  # thick castle curtain wall stone block
CORBEL_COURSE          = 816  # projecting stone corbel bracket course
TOWER_CAP              = 817  # conical slate tower roof cap
GREAT_HALL_FLOOR       = 818  # large stone-flagged great hall floor
DUNGEON_WALL           = 819  # rough-hewn stone with iron ring staple
CASTLE_FIREPLACE       = 820  # grand castle fireplace surround with hood
HERALDIC_PANEL         = 821  # carved stone heraldic escutcheon shield panel
WALL_WALK_FLOOR        = 822  # allure / chemin de ronde walkway paving
CASTLE_GATE_ARCH       = 823  # grand gatehouse stone arch with iron studs
DRAWBRIDGE_CHAIN       = 824  # heavy iron chain link decorative panel
DUNGEON_GRATE          = 825  # iron-barred dungeon floor grate
MOAT_STONE             = 826  # damp algae-stained moat-face stone
CHAPEL_STONE           = 827  # small castle chapel carved Gothic panel
MURDER_HOLE            = 828  # dark passage ceiling with drop hole
GARDEROBE_CHUTE        = 829  # projecting corbelled garderobe chute
# --- Mid-Century Modern ---
MCM_CONCRETE_PANEL     = 830  # smooth poured concrete wall panel
MCM_BREEZE_BLOCK       = 831  # open-grid decorative concrete screen
MCM_BOARD_BATTEN       = 832  # vertical cedar board-and-batten siding
MCM_WALNUT_PANEL       = 833  # horizontal walnut wood wall paneling
MCM_TEAK_PANEL         = 834  # warm teak horizontal plank wall
MCM_ROMAN_BRICK        = 835  # thin Roman-course horizontal brick
TERRAZZO_FLOOR_MCM     = 836  # speckled terrazzo floor tile
TRAVERTINE_FLOOR_MCM   = 837  # cream travertine stone floor tile
QUARRY_TILE            = 838  # unglazed terra-cotta quarry tile
FLAGSTONE_PATIO        = 839  # irregular grey flagstone paving
MCM_PARQUET            = 840  # herringbone parquet wood floor
CORK_FLOOR_TILE        = 841  # natural cork floor tile
AVOCADO_TILE           = 842  # avocado green glazed ceramic tile
HARVEST_GOLD_TILE      = 843  # harvest gold glazed ceramic tile
BURNT_ORANGE_TILE      = 844  # burnt orange glazed ceramic tile
TURQUOISE_TILE         = 845  # turquoise glazed ceramic tile
PLATE_GLASS_PANEL      = 846  # large clear plate-glass wall panel
TINTED_GLASS_PANEL     = 847  # dark tinted glass panel
RIBBED_GLASS_MCM       = 848  # frosted ribbed glass wall block
BRASS_TRIM_PANEL       = 849  # warm brass decorative wall panel
COPPER_SCREEN_MCM      = 850  # patinated copper screen panel
ANODIZED_ALUMINUM      = 851  # silver anodized aluminum panel
RATTAN_SCREEN_MCM      = 852  # woven rattan decorative screen
SPLIT_BAMBOO_PANEL     = 853  # split bamboo wall panel
LAVA_ROCK_WALL         = 854  # volcanic lava rock wall panel
MCM_TONGUE_GROOVE      = 855  # tongue-and-groove pine ceiling panel
BUTTERFLY_BEAM         = 856  # angled butterfly roof beam panel
STARBURST_PANEL        = 857  # geometric starburst ornamental panel
STACKED_STONE_VENEER   = 858  # thin stacked stone veneer panel
FIBERGLASS_SHELL       = 859  # molded fiberglass decorative panel

# --- Additional tree species (wave 2) ---
MANGROVE_LOG     = 1114
MANGROVE_LEAVES  = 1115
SPRUCE_LOG       = 1116
SPRUCE_LEAVES    = 1117
GINKGO_LOG       = 1118
GINKGO_LEAVES    = 1119
BANYAN_LOG       = 1120
BANYAN_LEAVES    = 1121
PEAR_LOG         = 1122
PEAR_LEAVES      = 1123
FIG_LOG          = 1124
FIG_LEAVES       = 1125
CITRUS_LOG       = 1126
CITRUS_LEAVES    = 1127
APPLE_LOG        = 1128
APPLE_LEAVES     = 1129
POMEGRANATE_LOG  = 1130
POMEGRANATE_LEAVES = 1131
APPLE_SAPLING        = 1132
PEAR_SAPLING         = 1133
FIG_SAPLING          = 1134
CITRUS_SAPLING       = 1135
POMEGRANATE_SAPLING  = 1136

ALL_FRUIT_SAPLINGS = {APPLE_SAPLING, PEAR_SAPLING, FIG_SAPLING, CITRUS_SAPLING, POMEGRANATE_SAPLING}

JUICER_BLOCK = 1137

KENNEL_BLOCK    = 1138  # placed kennel; triggers dog breeding UI
DOG_BOWL_BLOCK  = 1139  # placed dog bowl; speeds up taming nearby

# --- Waterside plants (naturally spawned near lakes/rivers) ---
REED_BLOCK           = 1140  # tall green reed stalks on water edges
CATTAIL_BLOCK        = 1141  # reeds with brown seed heads; wetland/swamp
BULRUSH_BLOCK        = 1142  # dense round-tipped rush clump; swamp/wetland
WATER_CRESS_BLOCK    = 1143  # low leafy cress on shallow water edges
POND_WEED_BLOCK      = 1144  # floating weed mat on open water surface
WATER_HYACINTH_BLOCK = 1145  # floating purple-flowered hyacinth; tropical/wetland
DUCKWEED_BLOCK       = 1146  # tiny floating green mat; still water
LOTUS_BLOCK          = 1147  # large pink floating lotus flower; tropical/jungle
FROGBIT_BLOCK        = 1148  # small round floating leaf rosettes
ARROWHEAD_BLOCK      = 1149  # emergent arrow-leaf aquatic plant; water edge
HORSETAIL_BLOCK      = 1150  # tall segmented ancient horsetail stalks; water edge
MARSH_MARIGOLD_BLOCK = 1151  # bright yellow flowers on muddy water edges
WATER_IRIS_BLOCK     = 1152  # yellow flag iris on water margins
SEDGE_BLOCK          = 1153  # dense tufted sedge grass; swamp/wetland
PICKERELWEED_BLOCK   = 1154  # emergent purple spike flower; wetland/swamp

# --- Palace doors ---
STUDDED_OAK_DOOR_CLOSED   = 1155
STUDDED_OAK_DOOR_OPEN     = 1156
VERMILION_DOOR_CLOSED     = 1157
VERMILION_DOOR_OPEN       = 1158
SHOJI_DOOR_CLOSED         = 1159
SHOJI_DOOR_OPEN           = 1160
GILDED_DOOR_CLOSED        = 1161
GILDED_DOOR_OPEN          = 1162
BRONZE_DOOR_CLOSED        = 1163
BRONZE_DOOR_OPEN          = 1164
SWAHILI_DOOR_CLOSED       = 1165
SWAHILI_DOOR_OPEN         = 1166
SANDALWOOD_DOOR_CLOSED    = 1167
SANDALWOOD_DOOR_OPEN      = 1168
STONE_SLAB_DOOR_CLOSED    = 1169
STONE_SLAB_DOOR_OPEN      = 1170
LANDMARK_FLAG_BLOCK       = 1171  # capital landmark interaction marker (non-mineable)

# --- Fruit tree harvest clusters (appear in canopy; mine to pick fruit) ---
APPLE_FRUIT_CLUSTER       = 1172  # ripe apple clusters; drops apple
PEAR_FRUIT_CLUSTER        = 1173  # ripe pear clusters; drops pear
FIG_FRUIT_CLUSTER         = 1174  # ripe fig clusters; drops fig
CITRUS_FRUIT_CLUSTER      = 1175  # ripe citrus/lemon clusters; drops lemon
POMEGRANATE_FRUIT_CLUSTER = 1176  # ripe pomegranate clusters; drops pomegranate
LIGHT_TRAP_BLOCK          = 1177  # craftable trap; attracts NIGHT_ONLY insects at night

ALL_FRUIT_CLUSTERS = {APPLE_FRUIT_CLUSTER, PEAR_FRUIT_CLUSTER, FIG_FRUIT_CLUSTER,
                      CITRUS_FRUIT_CLUSTER, POMEGRANATE_FRUIT_CLUSTER}

# Maps each fruit cluster to the plain leaf block it sits within
FRUIT_CLUSTER_LEAF_MAP = {
    APPLE_FRUIT_CLUSTER:       APPLE_LEAVES,
    PEAR_FRUIT_CLUSTER:        PEAR_LEAVES,
    FIG_FRUIT_CLUSTER:         FIG_LEAVES,
    CITRUS_FRUIT_CLUSTER:      CITRUS_LEAVES,
    POMEGRANATE_FRUIT_CLUSTER: POMEGRANATE_LEAVES,
}
# Reverse: leaf → fruit cluster
LEAF_FRUIT_CLUSTER_MAP = {v: k for k, v in FRUIT_CLUSTER_LEAF_MAP.items()}

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

OPEN_DOORS   = {WOOD_DOOR_OPEN, IRON_DOOR_OPEN, WOOD_FENCE_OPEN, IRON_FENCE_OPEN,
                COBALT_DOOR_OPEN, CRIMSON_CEDAR_DOOR_OPEN, TEAL_DOOR_OPEN, SAFFRON_DOOR_OPEN,
                STUDDED_OAK_DOOR_OPEN, VERMILION_DOOR_OPEN, SHOJI_DOOR_OPEN, GILDED_DOOR_OPEN,
                BRONZE_DOOR_OPEN, SWAHILI_DOOR_OPEN, SANDALWOOD_DOOR_OPEN, STONE_SLAB_DOOR_OPEN}
CLOSED_DOORS = {WOOD_DOOR_CLOSED, IRON_DOOR_CLOSED,
                COBALT_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_CLOSED, TEAL_DOOR_CLOSED, SAFFRON_DOOR_CLOSED,
                STUDDED_OAK_DOOR_CLOSED, VERMILION_DOOR_CLOSED, SHOJI_DOOR_CLOSED, GILDED_DOOR_CLOSED,
                BRONZE_DOOR_CLOSED, SWAHILI_DOOR_CLOSED, SANDALWOOD_DOOR_CLOSED, STONE_SLAB_DOOR_CLOSED}
ALL_DOORS    = OPEN_DOORS | CLOSED_DOORS
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
              MAPLE_LOG, CHERRY_LOG, CYPRESS_LOG, BAOBAB_LOG,
              MANGROVE_LOG, SPRUCE_LOG, GINKGO_LOG, BANYAN_LOG,
              PEAR_LOG, FIG_LOG, CITRUS_LOG, APPLE_LOG, POMEGRANATE_LOG}
ALL_LEAVES = {TREE_LEAVES, PINE_LEAVES, BIRCH_LEAVES, JUNGLE_LEAVES, WILLOW_LEAVES,
              REDWOOD_LEAVES, PALM_LEAVES, ACACIA_LEAVES, MUSHROOM_CAP,
              MAPLE_LEAVES, CHERRY_LEAVES, CYPRESS_LEAVES, BAOBAB_LEAVES,
              MANGROVE_LEAVES, SPRUCE_LEAVES, GINKGO_LEAVES, BANYAN_LEAVES,
              PEAR_LEAVES, FIG_LEAVES, CITRUS_LEAVES, APPLE_LEAVES, POMEGRANATE_LEAVES}
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
    MANGROVE_LEAVES: MANGROVE_LOG,
    SPRUCE_LEAVES:   SPRUCE_LOG,
    GINKGO_LEAVES:   GINKGO_LOG,
    BANYAN_LEAVES:   BANYAN_LOG,
    PEAR_LEAVES:        PEAR_LOG,
    FIG_LEAVES:         FIG_LOG,
    CITRUS_LEAVES:      CITRUS_LOG,
    APPLE_LEAVES:       APPLE_LOG,
    POMEGRANATE_LEAVES: POMEGRANATE_LOG,
}

GAMBLING_TABLE               = 1229  # inn gambling table; opens dice mini-game
RACING_RAIL                  = 1230  # perimeter fence/rail of the racing ring
BET_COUNTER                  = 1231  # racing ring bookkeeper counter; triggers racing UI
STARTING_GATE                = 1232  # decorative gate at race start line
WINNERS_POST                 = 1233  # trophy post at finish line

# --- Pacific / Polynesian crops ---
TARO_BUSH             = 1234
TARO_CROP_YOUNG       = 1235
TARO_CROP_MATURE      = 1236
BREADFRUIT_BUSH       = 1237
BREADFRUIT_CROP_YOUNG = 1238
BREADFRUIT_CROP_MATURE = 1239
COCONUT_BUSH          = 1240
COCONUT_CROP_YOUNG    = 1241
COCONUT_CROP_MATURE   = 1242

WEAPON_ASSEMBLER_BLOCK       = 1256  # weapon assembler
TEA_HOUSE_BLOCK              = 1257  # placed Tea House serving counter

EQUIPMENT_BLOCKS = {TUMBLER_BLOCK, CRUSHER_BLOCK, GEM_CUTTER_BLOCK, KILN_BLOCK, RESONANCE_BLOCK, BAKERY_BLOCK,
                    WOK_BLOCK, STEAMER_BLOCK, NOODLE_POT_BLOCK, BBQ_GRILL_BLOCK, CLAY_POT_BLOCK,
                    DESERT_FORGE_BLOCK,
                    ROASTER_BLOCK, BLEND_STATION_BLOCK, BREW_STATION_BLOCK,
                    GRAPE_PRESS_BLOCK, FERMENTATION_BLOCK, WINE_CELLAR_BLOCK,
                    STILL_BLOCK, BARREL_ROOM_BLOCK, BOTTLING_BLOCK,
                    FOSSIL_TABLE_BLOCK, ARTISAN_BENCH_BLOCK, COMPOST_BIN_BLOCK,
                    STABLE_BLOCK, HORSE_TROUGH_BLOCK,
                    WITHERING_RACK_BLOCK, OXIDATION_STATION_BLOCK, TEA_CELLAR_BLOCK, ROASTING_KILN_BLOCK,
                    DRYING_RACK_BLOCK, BAIT_STATION_BLOCK,
                    SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
                    DAIRY_VAT_BLOCK, CHEESE_PRESS_BLOCK, AGING_CAVE_BLOCK,
                    FLETCHING_TABLE_BLOCK,
                    SMELTER_BLOCK,
                    ANAEROBIC_TANK_BLOCK,
                    GLASS_KILN_BLOCK,
                    JEWELRY_WORKBENCH_BLOCK,
                    GARDEN_WORKSHOP_BLOCK,
                    GARDEN_BLOCK,
                    EVAPORATION_PAN_BLOCK, SALT_GRINDER_BLOCK,
                    SCULPTORS_BENCH,
                    TAPESTRY_FRAME_BLOCK,
                    JUICER_BLOCK,
                    KENNEL_BLOCK, DOG_BOWL_BLOCK,
                    FORGE_BLOCK, WEAPON_RACK_BLOCK,
                    SWITCH_BLOCK_OFF, LATCH_BLOCK_OFF,
                    BREW_KETTLE_BLOCK, FERM_VESSEL_BLOCK, TAPROOM_BLOCK,
                    AUTOMATION_BENCH_BLOCK,
                    CHICKEN_COOP_BLOCK,
                    GAMBLING_TABLE,
                    BET_COUNTER,
                    WEAPON_ASSEMBLER_BLOCK,
                    TEA_HOUSE_BLOCK}
RESOURCE_BLOCKS  = {COAL_ORE, IRON_ORE, GOLD_ORE, CRYSTAL_ORE, RUBY_ORE, OBSIDIAN, ROCK_DEPOSIT, FOSSIL_DEPOSIT, GEM_DEPOSIT,
                    CLAY_DEPOSIT, LIMESTONE_DEPOSIT, SALT_DEPOSIT}

LOGIC_SOURCE_BLOCKS  = {SWITCH_BLOCK_ON, LATCH_BLOCK_ON, PRESSURE_PLATE_ON, RS_LATCH_Q1}
LOGIC_GATE_BLOCKS    = {AND_GATE_BLOCK, OR_GATE_BLOCK, NOT_GATE_BLOCK}
LOGIC_SENSOR_BLOCKS  = {DAY_SENSOR_BLOCK, NIGHT_SENSOR_BLOCK, WATER_SENSOR_BLOCK, CROP_SENSOR_BLOCK}
LOGIC_TIMER_BLOCKS   = {REPEATER_BLOCK, PULSE_GEN_BLOCK}
LOGIC_ROTATEABLE_BLOCKS = {AND_GATE_BLOCK, OR_GATE_BLOCK, NOT_GATE_BLOCK,
                            REPEATER_BLOCK, RS_LATCH_Q0, RS_LATCH_Q1,
                            COUNTER_BLOCK, COMPARATOR_BLOCK, OBSERVER_BLOCK,
                            SEQUENCER_BLOCK, T_FLIPFLOP_BLOCK}
LOGIC_OUTPUT_PAIRS  = {
    DAM_BLOCK_CLOSED:       DAM_BLOCK_OPEN,
    DAM_BLOCK_OPEN:         DAM_BLOCK_CLOSED,
    PUMP_BLOCK_OFF:         PUMP_BLOCK_ON,
    PUMP_BLOCK_ON:          PUMP_BLOCK_OFF,
    IRON_GATE_BLOCK_CLOSED: IRON_GATE_BLOCK_OPEN,
    IRON_GATE_BLOCK_OPEN:   IRON_GATE_BLOCK_CLOSED,
    POWERED_LANTERN_OFF:    POWERED_LANTERN_ON,
    POWERED_LANTERN_ON:     POWERED_LANTERN_OFF,
    ALARM_BELL_OFF:         ALARM_BELL_ON,
    ALARM_BELL_ON:          ALARM_BELL_OFF,
}
LOGIC_OUTPUT_BLOCKS = set(LOGIC_OUTPUT_PAIRS)
BUSH_BLOCKS       = {STRAWBERRY_BUSH, WHEAT_BUSH, CARROT_BUSH, TOMATO_BUSH, CORN_BUSH, PUMPKIN_BUSH, APPLE_BUSH,
                     RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, GARLIC_BUSH, SCALLION_BUSH, CHILI_BUSH,
                     PEPPER_BUSH, ONION_BUSH, POTATO_BUSH, EGGPLANT_BUSH, CABBAGE_BUSH,
                     BEET_BUSH, TURNIP_BUSH, LEEK_BUSH, ZUCCHINI_BUSH, SWEET_POTATO_BUSH,
                     WATERMELON_BUSH, RADISH_BUSH, PEA_BUSH, CELERY_BUSH, BROCCOLI_BUSH,
                     DATE_PALM_BUSH, AGAVE_BUSH,
                     COFFEE_BUSH, GRAPEVINE_BUSH, GRAIN_CROP_BUSH, HOP_VINE_BUSH,
                     TEA_BUSH,
                     CHAMOMILE_BUSH, LAVENDER_BUSH, MINT_BUSH, ROSEMARY_BUSH,
                     THYME_BUSH, SAGE_BUSH, BASIL_BUSH, OREGANO_BUSH,
                     DILL_BUSH, FENNEL_BUSH, TARRAGON_BUSH, LEMON_BALM_BUSH,
                     ECHINACEA_BUSH, VALERIAN_BUSH, ST_JOHNS_WORT_BUSH, YARROW_BUSH,
                     BERGAMOT_BUSH, WORMWOOD_BUSH, RUE_BUSH, LEMON_VERBENA_BUSH,
                     HYSSOP_BUSH, CATNIP_BUSH, WOOD_SORREL_BUSH, MARJORAM_BUSH,
                     SAVORY_BUSH, ANGELICA_BUSH, BORAGE_BUSH, COMFREY_BUSH, MUGWORT_BUSH,
                     FLAX_BUSH, COTTON_BUSH,
                     TARO_BUSH, BREADFRUIT_BUSH, COCONUT_BUSH}
YOUNG_CROP_BLOCKS = {STRAWBERRY_CROP_YOUNG, WHEAT_CROP_YOUNG, CARROT_CROP_YOUNG, TOMATO_CROP_YOUNG, CORN_CROP_YOUNG, PUMPKIN_CROP_YOUNG, APPLE_CROP_YOUNG,
                     RICE_CROP_YOUNG, GINGER_CROP_YOUNG, BOK_CHOY_CROP_YOUNG, GARLIC_CROP_YOUNG,
                     SCALLION_CROP_YOUNG, CHILI_CROP_YOUNG,
                     PEPPER_CROP_YOUNG, ONION_CROP_YOUNG, POTATO_CROP_YOUNG, EGGPLANT_CROP_YOUNG, CABBAGE_CROP_YOUNG,
                     BEET_CROP_YOUNG, TURNIP_CROP_YOUNG, LEEK_CROP_YOUNG, ZUCCHINI_CROP_YOUNG, SWEET_POTATO_CROP_YOUNG,
                     WATERMELON_CROP_YOUNG, RADISH_CROP_YOUNG, PEA_CROP_YOUNG, CELERY_CROP_YOUNG, BROCCOLI_CROP_YOUNG,
                     CACTUS_YOUNG, DATE_PALM_CROP_YOUNG, AGAVE_CROP_YOUNG,
                     COFFEE_CROP_YOUNG, GRAPEVINE_CROP_YOUNG, GRAIN_CROP_YOUNG, TEA_CROP_YOUNG, HOP_VINE_YOUNG,
                     CHAMOMILE_CROP_YOUNG, LAVENDER_CROP_YOUNG, MINT_CROP_YOUNG, ROSEMARY_CROP_YOUNG,
                     THYME_CROP_YOUNG, SAGE_CROP_YOUNG, BASIL_CROP_YOUNG, OREGANO_CROP_YOUNG,
                     DILL_CROP_YOUNG, FENNEL_CROP_YOUNG, TARRAGON_CROP_YOUNG, LEMON_BALM_CROP_YOUNG,
                     ECHINACEA_CROP_YOUNG, VALERIAN_CROP_YOUNG, ST_JOHNS_WORT_CROP_YOUNG, YARROW_CROP_YOUNG,
                     BERGAMOT_CROP_YOUNG, WORMWOOD_CROP_YOUNG, RUE_CROP_YOUNG, LEMON_VERBENA_CROP_YOUNG,
                     HYSSOP_CROP_YOUNG, CATNIP_CROP_YOUNG, WOOD_SORREL_CROP_YOUNG, MARJORAM_CROP_YOUNG,
                     SAVORY_CROP_YOUNG, ANGELICA_CROP_YOUNG, BORAGE_CROP_YOUNG, COMFREY_CROP_YOUNG, MUGWORT_CROP_YOUNG,
                     CHICKPEA_CROP_YOUNG, LENTIL_CROP_YOUNG, SESAME_CROP_YOUNG, POMEGRANATE_TREE_YOUNG,
                     OLIVE_TREE_YOUNG, SAFFRON_CROP_YOUNG,
                     SAGUARO_YOUNG, BARREL_CACTUS_YOUNG, OCOTILLO_YOUNG,
                     PRICKLY_PEAR_YOUNG, CHOLLA_YOUNG, PALO_VERDE_YOUNG,
                     STRAWBERRY_CROP_YOUNG_P, TOMATO_CROP_YOUNG_P, WATERMELON_CROP_YOUNG_P,
                     CORN_CROP_YOUNG_P, RICE_CROP_YOUNG_P,
                     FLAX_CROP_YOUNG, COTTON_CROP_YOUNG,
                     TARO_CROP_YOUNG, BREADFRUIT_CROP_YOUNG, COCONUT_CROP_YOUNG}
# Desert plants that grow wild on SAND — bypass tilled-soil requirement
WILD_DESERT_PLANT_BLOCKS = {
    CACTUS_YOUNG, SAGUARO_YOUNG, BARREL_CACTUS_YOUNG, OCOTILLO_YOUNG,
    PRICKLY_PEAR_YOUNG, CHOLLA_YOUNG, PALO_VERDE_YOUNG,
}
MATURE_CROP_BLOCKS= {STRAWBERRY_CROP_MATURE, WHEAT_CROP_MATURE, CARROT_CROP_MATURE, TOMATO_CROP_MATURE, CORN_CROP_MATURE, PUMPKIN_CROP_MATURE, APPLE_CROP_MATURE,
                     RICE_CROP_MATURE, GINGER_CROP_MATURE, BOK_CHOY_CROP_MATURE, GARLIC_CROP_MATURE,
                     SCALLION_CROP_MATURE, CHILI_CROP_MATURE,
                     PEPPER_CROP_MATURE, ONION_CROP_MATURE, POTATO_CROP_MATURE, EGGPLANT_CROP_MATURE, CABBAGE_CROP_MATURE,
                     BEET_CROP_MATURE, TURNIP_CROP_MATURE, LEEK_CROP_MATURE, ZUCCHINI_CROP_MATURE, SWEET_POTATO_CROP_MATURE,
                     WATERMELON_CROP_MATURE, RADISH_CROP_MATURE, PEA_CROP_MATURE, CELERY_CROP_MATURE, BROCCOLI_CROP_MATURE,
                     CACTUS_MATURE, DATE_PALM_CROP_MATURE, AGAVE_CROP_MATURE,
                     COFFEE_CROP_MATURE, GRAPEVINE_CROP_MATURE, GRAIN_CROP_MATURE, TEA_CROP_MATURE, HOP_VINE_MATURE,
                     CHAMOMILE_CROP_MATURE, LAVENDER_CROP_MATURE, MINT_CROP_MATURE, ROSEMARY_CROP_MATURE,
                     THYME_CROP_MATURE, SAGE_CROP_MATURE, BASIL_CROP_MATURE, OREGANO_CROP_MATURE,
                     DILL_CROP_MATURE, FENNEL_CROP_MATURE, TARRAGON_CROP_MATURE, LEMON_BALM_CROP_MATURE,
                     ECHINACEA_CROP_MATURE, VALERIAN_CROP_MATURE, ST_JOHNS_WORT_CROP_MATURE, YARROW_CROP_MATURE,
                     BERGAMOT_CROP_MATURE, WORMWOOD_CROP_MATURE, RUE_CROP_MATURE, LEMON_VERBENA_CROP_MATURE,
                     HYSSOP_CROP_MATURE, CATNIP_CROP_MATURE, WOOD_SORREL_CROP_MATURE, MARJORAM_CROP_MATURE,
                     SAVORY_CROP_MATURE, ANGELICA_CROP_MATURE, BORAGE_CROP_MATURE, COMFREY_CROP_MATURE, MUGWORT_CROP_MATURE,
                     CHICKPEA_CROP_MATURE, LENTIL_CROP_MATURE, SESAME_CROP_MATURE, POMEGRANATE_TREE_MATURE,
                     OLIVE_TREE_MATURE, SAFFRON_CROP_MATURE,
                     SAGUARO_MATURE, BARREL_CACTUS_MATURE, OCOTILLO_MATURE,
                     PRICKLY_PEAR_MATURE, CHOLLA_MATURE, PALO_VERDE_MATURE,
                     STRAWBERRY_CROP_MATURE_P, TOMATO_CROP_MATURE_P, WATERMELON_CROP_MATURE_P,
                     CORN_CROP_MATURE_P, RICE_CROP_MATURE_P,
                     FLAX_CROP_MATURE, COTTON_CROP_MATURE,
                     TARO_CROP_MATURE, BREADFRUIT_CROP_MATURE, COCONUT_CROP_MATURE}
CROP_BLOCKS       = YOUNG_CROP_BLOCKS | MATURE_CROP_BLOCKS

# Perennial crops regrow after harvest (each harvest has ~33% chance to die)
PERENNIAL_CROP_MATURE = {
    STRAWBERRY_CROP_MATURE, APPLE_CROP_MATURE, TOMATO_CROP_MATURE,
    PEPPER_CROP_MATURE, CHILI_CROP_MATURE, EGGPLANT_CROP_MATURE,
    CACTUS_MATURE, COFFEE_CROP_MATURE, GRAPEVINE_CROP_MATURE, GRAIN_CROP_MATURE, TEA_CROP_MATURE, HOP_VINE_MATURE,
    CHAMOMILE_CROP_MATURE, LAVENDER_CROP_MATURE, MINT_CROP_MATURE, ROSEMARY_CROP_MATURE,
    THYME_CROP_MATURE, SAGE_CROP_MATURE, BASIL_CROP_MATURE, OREGANO_CROP_MATURE,
    DILL_CROP_MATURE, FENNEL_CROP_MATURE, TARRAGON_CROP_MATURE, LEMON_BALM_CROP_MATURE,
    ECHINACEA_CROP_MATURE, VALERIAN_CROP_MATURE, ST_JOHNS_WORT_CROP_MATURE, YARROW_CROP_MATURE,
    BERGAMOT_CROP_MATURE, WORMWOOD_CROP_MATURE, RUE_CROP_MATURE, LEMON_VERBENA_CROP_MATURE,
    HYSSOP_CROP_MATURE, CATNIP_CROP_MATURE, WOOD_SORREL_CROP_MATURE, MARJORAM_CROP_MATURE,
    SAVORY_CROP_MATURE, ANGELICA_CROP_MATURE, BORAGE_CROP_MATURE, COMFREY_CROP_MATURE, MUGWORT_CROP_MATURE,
    SAGUARO_MATURE, BARREL_CACTUS_MATURE, OCOTILLO_MATURE,
    PRICKLY_PEAR_MATURE, CHOLLA_MATURE, PALO_VERDE_MATURE,
    STRAWBERRY_CROP_MATURE_P, TOMATO_CROP_MATURE_P,
    FLAX_CROP_MATURE,
    COTTON_CROP_MATURE,
    TARO_CROP_MATURE,
    BREADFRUIT_CROP_MATURE,
    COCONUT_CROP_MATURE,
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
    TEA_CROP_MATURE:          TEA_CROP_YOUNG,
    CHAMOMILE_CROP_MATURE:    CHAMOMILE_CROP_YOUNG,
    LAVENDER_CROP_MATURE:     LAVENDER_CROP_YOUNG,
    MINT_CROP_MATURE:         MINT_CROP_YOUNG,
    ROSEMARY_CROP_MATURE:           ROSEMARY_CROP_YOUNG,
    THYME_CROP_MATURE:              THYME_CROP_YOUNG,
    SAGE_CROP_MATURE:               SAGE_CROP_YOUNG,
    BASIL_CROP_MATURE:              BASIL_CROP_YOUNG,
    OREGANO_CROP_MATURE:            OREGANO_CROP_YOUNG,
    DILL_CROP_MATURE:               DILL_CROP_YOUNG,
    FENNEL_CROP_MATURE:             FENNEL_CROP_YOUNG,
    TARRAGON_CROP_MATURE:           TARRAGON_CROP_YOUNG,
    LEMON_BALM_CROP_MATURE:         LEMON_BALM_CROP_YOUNG,
    ECHINACEA_CROP_MATURE:          ECHINACEA_CROP_YOUNG,
    VALERIAN_CROP_MATURE:           VALERIAN_CROP_YOUNG,
    ST_JOHNS_WORT_CROP_MATURE:      ST_JOHNS_WORT_CROP_YOUNG,
    YARROW_CROP_MATURE:             YARROW_CROP_YOUNG,
    BERGAMOT_CROP_MATURE:           BERGAMOT_CROP_YOUNG,
    WORMWOOD_CROP_MATURE:           WORMWOOD_CROP_YOUNG,
    RUE_CROP_MATURE:                RUE_CROP_YOUNG,
    LEMON_VERBENA_CROP_MATURE:      LEMON_VERBENA_CROP_YOUNG,
    HYSSOP_CROP_MATURE:             HYSSOP_CROP_YOUNG,
    CATNIP_CROP_MATURE:             CATNIP_CROP_YOUNG,
    WOOD_SORREL_CROP_MATURE:        WOOD_SORREL_CROP_YOUNG,
    MARJORAM_CROP_MATURE:           MARJORAM_CROP_YOUNG,
    SAVORY_CROP_MATURE:             SAVORY_CROP_YOUNG,
    ANGELICA_CROP_MATURE:           ANGELICA_CROP_YOUNG,
    BORAGE_CROP_MATURE:             BORAGE_CROP_YOUNG,
    COMFREY_CROP_MATURE:            COMFREY_CROP_YOUNG,
    MUGWORT_CROP_MATURE:            MUGWORT_CROP_YOUNG,
    CHICKPEA_CROP_MATURE:     CHICKPEA_CROP_YOUNG,
    LENTIL_CROP_MATURE:       LENTIL_CROP_YOUNG,
    SESAME_CROP_MATURE:       SESAME_CROP_YOUNG,
    POMEGRANATE_TREE_MATURE:  POMEGRANATE_TREE_YOUNG,
    OLIVE_TREE_MATURE:        OLIVE_TREE_YOUNG,
    SAFFRON_CROP_MATURE:      SAFFRON_CROP_YOUNG,
    SAGUARO_MATURE:           SAGUARO_YOUNG,
    BARREL_CACTUS_MATURE:     BARREL_CACTUS_YOUNG,
    OCOTILLO_MATURE:          OCOTILLO_YOUNG,
    PRICKLY_PEAR_MATURE:      PRICKLY_PEAR_YOUNG,
    CHOLLA_MATURE:            CHOLLA_YOUNG,
    PALO_VERDE_MATURE:        PALO_VERDE_YOUNG,
    STRAWBERRY_CROP_MATURE_P: STRAWBERRY_CROP_YOUNG_P,
    TOMATO_CROP_MATURE_P:     TOMATO_CROP_YOUNG_P,
    WATERMELON_CROP_MATURE_P: WATERMELON_CROP_YOUNG_P,
    CORN_CROP_MATURE_P:       CORN_CROP_YOUNG_P,
    RICE_CROP_MATURE_P:       RICE_CROP_YOUNG_P,
    FLAX_CROP_MATURE:         FLAX_CROP_YOUNG,
    COTTON_CROP_MATURE:       COTTON_CROP_YOUNG,
    TARO_CROP_MATURE:         TARO_CROP_YOUNG,
    BREADFRUIT_CROP_MATURE:   BREADFRUIT_CROP_YOUNG,
    COCONUT_CROP_MATURE:      COCONUT_CROP_YOUNG,
}

ALPINE_BALCONY_RAIL          = 1022  # alpine balcony rail
DARK_TIMBER_BEAM             = 1023  # dark timber beam
ROUGH_STONE_WALL             = 1024  # rough stone wall
ALPINE_PLASTER               = 1025  # alpine plaster
FLOWER_BOX                   = 1026  # flower box
FIREWOOD_STACK               = 1027  # firewood stack
SLATE_SHINGLE                = 1028  # slate shingle
CARVED_SHUTTER               = 1029  # carved shutter
BEAR_HIDE                    = 1030  # bear hide
ALPINE_HERB_RACK             = 1031  # alpine herb rack
HAY_BALE                     = 1032  # hay bale
PINE_PLANK_WALL              = 1033  # pine plank wall
GRANITE_ASHLAR               = 1034  # granite ashlar
CUCKOO_CLOCK                 = 1035  # cuckoo clock
GERANIUM_BOX                 = 1036  # geranium box
ARCH_STONE                   = 1037  # arch stone
SWISS_PANEL                  = 1038  # swiss panel
COPPER_COWBELL               = 1039  # copper cowbell
WOODEN_GEAR                  = 1040  # wooden gear
STONE_BASIN                  = 1041  # stone basin
MILK_CHURN                   = 1042  # milk churn
ALPINE_CHEST                 = 1043  # alpine chest
ALPINE_LANTERN               = 1044  # alpine lantern
WROUGHT_IRON_RAIL            = 1045  # wrought iron rail
ALPINE_CHANDELIER            = 1046  # alpine chandelier
WOVEN_TEXTILE                = 1047  # woven textile
COWBELL_RACK                 = 1048  # cowbell rack
ALPINE_STUCCO                = 1049  # alpine stucco
CARVED_LINTEL                = 1050  # carved lintel
CHALET_DOOR                  = 1051  # chalet door
CERAMIC_TILE_STOVE           = 1052  # ceramic tile stove
CARVED_BARGEBOARD            = 1053  # carved bargeboard
DORMER_WINDOW                = 1054  # dormer window
WOODEN_SHINGLE               = 1055  # wooden shingle
STONE_STEP                   = 1056  # stone step
WATER_TROUGH                 = 1057  # water trough
CARVED_BENCH                 = 1058  # carved bench
CHEESE_WHEEL                 = 1059  # cheese wheel
ANTLER_MOUNT                 = 1060  # antler mount
EDELWEISS_WREATH             = 1061  # edelweiss wreath
BOOT_RACK                    = 1062  # boot rack
TALLOW_CANDLE                = 1063  # tallow candle
ALPINE_HEARTH                = 1064  # alpine hearth
PINE_CONE_GARLAND            = 1065  # pine cone garland
IRON_HOOK_RACK               = 1066  # iron hook rack
ALPINE_GATE                  = 1067  # alpine gate
BUTTER_CHURN                 = 1068  # butter churn
CARVED_WAINSCOT              = 1069  # carved wainscot
CHIMNEY_CAP                  = 1070  # chimney cap
FEATHER_DUVET                = 1071  # feather duvet
GREEK_AMPHORA                = 1072  # greek amphora
KRATER                       = 1073  # krater
HYDRIA                       = 1074  # hydria
LEKYTHOS                     = 1075  # lekythos
STORAGE_PITHOS               = 1076  # storage pithos
KLINE                        = 1077  # kline
TRIPOD_BRAZIER               = 1078  # tripod brazier
OLIVE_PRESS                  = 1079  # olive press
LOOM_FRAME                   = 1080  # loom frame
MEANDER_BORDER               = 1081  # meander border
SYMPOSIUM_TABLE              = 1082  # symposium table
VOTIVE_TABLET                = 1083  # votive tablet
BRONZE_CUIRASS_STAND         = 1084  # bronze cuirass stand
CHARIOT_WHEEL                = 1085  # chariot wheel
TERRACOTTA_ROOF_TILE         = 1086  # terracotta roof tile
ATTIC_VASE                   = 1087  # attic vase
GREEK_STONE_BENCH            = 1088  # greek stone bench
STONE_ALTAR                  = 1089  # stone altar
BRONZE_MIRROR                = 1090  # bronze mirror
CLAY_OIL_LAMP                = 1091  # clay oil lamp
AGORA_SCALE                  = 1092  # agora scale
LAUREL_WREATH_MOUNT          = 1093  # laurel wreath mount
HERMES_STELE                 = 1094  # hermes stele
DORIC_CAPITAL                = 1095  # doric capital
VICTORY_STELE                = 1096  # victory stele
BRONZE_SHIELD_MOUNT          = 1097  # bronze shield mount
EGG_AND_DART                 = 1098  # egg and dart
OLIVE_BRANCH                 = 1099  # olive branch
PHILOSOPHERS_SCROLL          = 1100  # philosophers scroll
GREEK_THEATRE_MASK           = 1101  # greek theatre mask
TORCH                        = 1102  # basic torch
WALL_SCONCE                  = 1103  # wall-mounted iron sconce
BRAZIER                      = 1104  # iron brazier with fire
CHANDELIER                   = 1105  # hanging iron chandelier
CANDELABRA                   = 1106  # ornate floor candelabra
LANTERN_ORB                  = 1107  # glowing crystal orb lantern
PENDANT_LAMP                 = 1108  # hanging pendant lamp
FIRE_BOWL                    = 1109  # stone fire bowl
CROSS_LANTERN                = 1110  # cross-pane iron lantern
STAR_LAMP                    = 1111  # crystal star lamp
GLOW_VINE                    = 1112  # bioluminescent glow vine
TOWN_FLAG_BLOCK              = 1113  # town identity flag (non-mineable)
OUTPOST_FLAG_BLOCK           = 1178  # outpost identity flag (non-mineable)
ICE_SHARD                    = 1226  # ice shard
FROZEN_BOG                   = 1227  # frozen bog
STONE_BRIDGE                 = 1228  # stone road bridge spanning a city river
TIMBER_BRIDGE                = 1243  # log-and-plank bridge; boreal / birch-forest cities
MOSSY_BRIDGE                 = 1244  # weathered mossy-stone bridge; wetland / swamp cities
SANDSTONE_BRIDGE             = 1245  # warm sandstone bridge; jungle / tropical cities
BRICK_BRIDGE                 = 1246  # red-brick arch bridge; rolling-hills cities
COBBLE_BRIDGE                = 1247  # rough cobblestone bridge; steppe cities
DRIFTWOOD_BRIDGE             = 1248  # pale weathered driftwood bridge; coastal cities
CITY_BLOCK                   = 1249  # player-placed city anchor/management block
GROW_LAMP                    = 1250  # bg-layer artificial grow light; enables underground crop growth
MINING_POST_BLOCK            = 1252  # placed by player to assign a miner's work zone
BANNER_BLOCK                 = 1253  # decorative banner displaying a city's coat of arms
FISHING_SPOT_BLOCK           = 1254  # shimmering surface water; boosts rare fish chance
FISH_TROPHY_BLOCK            = 1255  # bg-layer wall-mounted decorative fish trophy
CLOUD_CIRRUS                 = 1258  # high sky layer, y 4–12, ice-blue wispy
CLOUD_CUMULUS                = 1259  # mid sky layer,  y 16–26, fluffy white
CLOUD_STRATUS                = 1260  # low sky layer,  y 30–38, flat gray
CLOUD_STORM                  = 1261  # near-surface,   y 37–43, dark charcoal

CLOUD_BLOCKS = {CLOUD_CIRRUS, CLOUD_CUMULUS, CLOUD_STRATUS, CLOUD_STORM}

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
    # Additional tree species (wave 2)
    MANGROVE_LOG:    {"name": "Mangrove Log",    "hardness": 2, "color": (55,  38,  18),  "drop": "lumber"},
    MANGROVE_LEAVES: {"name": "Mangrove Leaves", "hardness": 1, "color": (38,  148, 62),  "drop": "sapling", "drop_chance": 0.10},
    SPRUCE_LOG:      {"name": "Spruce Log",      "hardness": 2, "color": (52,  33,  16),  "drop": "lumber"},
    SPRUCE_LEAVES:   {"name": "Spruce Needles",  "hardness": 1, "color": (14,  60,  18),  "drop": "sapling", "drop_chance": 0.10},
    GINKGO_LOG:      {"name": "Ginkgo Log",      "hardness": 2, "color": (128, 98,  58),  "drop": "lumber"},
    GINKGO_LEAVES:   {"name": "Ginkgo Leaves",   "hardness": 1, "color": (195, 205, 45),  "drop": "sapling", "drop_chance": 0.10},
    BANYAN_LOG:      {"name": "Banyan Log",      "hardness": 2, "color": (60,  40,  20),  "drop": "lumber"},
    BANYAN_LEAVES:   {"name": "Banyan Leaves",   "hardness": 1, "color": (32,  145, 42),  "drop": "sapling", "drop_chance": 0.10},
    PEAR_LOG:        {"name": "Pear Log",        "hardness": 2, "color": (88,  62,  38),  "drop": "lumber"},
    PEAR_LEAVES:     {"name": "Pear Leaves",     "hardness": 1, "color": (95,  168, 62),  "drop": "pear",    "drop_chance": 0.20, "bonus_drop": "pear_sapling",  "bonus_drop_chance": 0.10},
    FIG_LOG:         {"name": "Fig Log",         "hardness": 2, "color": (75,  52,  32),  "drop": "lumber"},
    FIG_LEAVES:      {"name": "Fig Leaves",      "hardness": 1, "color": (42,  152, 52),  "drop": "fig",     "drop_chance": 0.20, "bonus_drop": "fig_sapling",    "bonus_drop_chance": 0.10},
    CITRUS_LOG:          {"name": "Citrus Log",          "hardness": 2, "color": (95,  70,  35),  "drop": "lumber"},
    CITRUS_LEAVES:       {"name": "Citrus Leaves",       "hardness": 1, "color": (38,  178, 62),  "drop": "lemon",       "drop_chance": 0.20, "bonus_drop": "citrus_sapling",      "bonus_drop_chance": 0.10},
    APPLE_LOG:           {"name": "Apple Log",           "hardness": 2, "color": (92,  65,  38),  "drop": "lumber"},
    APPLE_LEAVES:        {"name": "Apple Leaves",        "hardness": 1, "color": (62,  155, 58),  "drop": "apple",       "drop_chance": 0.20, "bonus_drop": "apple_sapling",       "bonus_drop_chance": 0.10},
    POMEGRANATE_LOG:     {"name": "Pomegranate Log",     "hardness": 2, "color": (78,  50,  35),  "drop": "lumber"},
    POMEGRANATE_LEAVES:  {"name": "Pomegranate Leaves",  "hardness": 1, "color": (55,  145, 55),  "drop": "pomegranate", "drop_chance": 0.20, "bonus_drop": "pomegranate_sapling", "bonus_drop_chance": 0.10},
    APPLE_SAPLING:       {"name": "Apple Sapling",       "hardness": 1, "color": (62,  155, 58),  "drop": "apple_sapling"},
    PEAR_SAPLING:        {"name": "Pear Sapling",        "hardness": 1, "color": (95,  168, 62),  "drop": "pear_sapling"},
    FIG_SAPLING:         {"name": "Fig Sapling",         "hardness": 1, "color": (42,  152, 52),  "drop": "fig_sapling"},
    CITRUS_SAPLING:      {"name": "Citrus Sapling",      "hardness": 1, "color": (38,  178, 62),  "drop": "citrus_sapling"},
    POMEGRANATE_SAPLING: {"name": "Pomegranate Sapling", "hardness": 1, "color": (55,  145, 55),  "drop": "pomegranate_sapling"},
    APPLE_FRUIT_CLUSTER:       {"name": "Apple Cluster",       "hardness": 0.3, "color": (180, 40,  40),  "drop": "apple",       "drop_chance": 1.0},
    PEAR_FRUIT_CLUSTER:        {"name": "Pear Cluster",        "hardness": 0.3, "color": (175, 195, 65),  "drop": "pear",        "drop_chance": 1.0},
    FIG_FRUIT_CLUSTER:         {"name": "Fig Cluster",         "hardness": 0.3, "color": (110, 55,  100), "drop": "fig",         "drop_chance": 1.0},
    CITRUS_FRUIT_CLUSTER:      {"name": "Citrus Cluster",      "hardness": 0.3, "color": (230, 180, 30),  "drop": "lemon",       "drop_chance": 1.0},
    POMEGRANATE_FRUIT_CLUSTER: {"name": "Pomegranate Cluster", "hardness": 0.3, "color": (175, 35,  55),  "drop": "pomegranate", "drop_chance": 1.0},
    JUICER_BLOCK:        {"name": "Juicer",              "hardness": 1, "color": (220, 160, 60),  "drop": "juicer_item"},
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
    RESTAURANT_WALL:       {"name": "Restaurant Wall",         "hardness": 2,   "color": (195, 110,  75), "drop": "lumber"},
    RESTAURANT_AWNING:     {"name": "Restaurant Awning",       "hardness": 2,   "color": (145,  30,  30), "drop": "lumber"},
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
    LIGHT_TRAP_BLOCK:          {"name": "Light Trap",                "hardness": 1.0, "color": (220, 190,  80), "drop": "light_trap", "interact": True},
    STAIRS_RIGHT:              {"name": "Stairs (Right)",            "hardness": 1.5, "color": (139, 100,  60), "drop": "wood_stairs"},
    STAIRS_LEFT:               {"name": "Stairs (Left)",             "hardness": 1.5, "color": (139, 100,  60), "drop": "wood_stairs"},
    GARDEN_BLOCK:              {"name": "Garden Block",              "hardness": 1.0, "color": ( 80, 140,  60), "drop": "garden_block"},
    WILDFLOWER_DISPLAY_BLOCK:  {"name": "Wildflower Display",        "hardness": 1.0, "color": (200, 230, 200), "drop": "wildflower_display"},
    STABLE_BLOCK:              {"name": "Stable",                   "hardness": 2.0, "color": (120,  85,  45), "drop": "stable_item"},
    HORSE_TROUGH_BLOCK:        {"name": "Horse Trough",             "hardness": 1.5, "color": ( 60, 100, 130), "drop": "horse_trough_item"},
    KENNEL_BLOCK:              {"name": "Kennel",                   "hardness": 2.0, "color": (100,  75,  40), "drop": "kennel_item"},
    DOG_BOWL_BLOCK:            {"name": "Dog Bowl",                 "hardness": 1.0, "color": (180, 140,  90), "drop": "dog_bowl_item"},
    # --- Waterside plants ---
    REED_BLOCK:           {"name": "Reeds",          "hardness": 0.3, "color": ( 75, 148,  60), "drop": "reed_bundle"},
    CATTAIL_BLOCK:        {"name": "Cattail",        "hardness": 0.3, "color": ( 70, 138,  55), "drop": "cattail"},
    BULRUSH_BLOCK:        {"name": "Bulrush",        "hardness": 0.3, "color": ( 50, 110,  48), "drop": "bulrush"},
    WATER_CRESS_BLOCK:    {"name": "Water Cress",    "hardness": 0.3, "color": ( 55, 155,  65), "drop": "water_cress"},
    POND_WEED_BLOCK:      {"name": "Pond Weed",      "hardness": 0.3, "color": ( 40, 105,  50), "drop": "pond_weed"},
    WATER_HYACINTH_BLOCK: {"name": "Water Hyacinth", "hardness": 0.3, "color": (140,  80, 185), "drop": "water_hyacinth"},
    DUCKWEED_BLOCK:       {"name": "Duckweed",       "hardness": 0.2, "color": ( 55, 130,  48), "drop": "duckweed"},
    LOTUS_BLOCK:          {"name": "Lotus",          "hardness": 0.3, "color": (220, 150, 175), "drop": "lotus_petal"},
    FROGBIT_BLOCK:        {"name": "Frogbit",        "hardness": 0.2, "color": ( 45, 120,  55), "drop": "frogbit"},
    ARROWHEAD_BLOCK:      {"name": "Arrowhead",      "hardness": 0.3, "color": ( 60, 145,  65), "drop": "arrowhead_tuber"},
    HORSETAIL_BLOCK:      {"name": "Horsetail",      "hardness": 0.3, "color": ( 68, 128,  52), "drop": "horsetail"},
    MARSH_MARIGOLD_BLOCK: {"name": "Marsh Marigold", "hardness": 0.3, "color": (225, 195,  30), "drop": "marsh_marigold"},
    WATER_IRIS_BLOCK:     {"name": "Water Iris",     "hardness": 0.3, "color": (220, 200,  40), "drop": "water_iris"},
    SEDGE_BLOCK:          {"name": "Sedge",          "hardness": 0.3, "color": ( 85, 148,  58), "drop": "sedge"},
    PICKERELWEED_BLOCK:   {"name": "Pickerelweed",   "hardness": 0.3, "color": ( 90,  80, 200), "drop": "pickerelweed"},
    # --- Herbalism supply chain ---
    DRYING_RACK_BLOCK:         {"name": "Drying Rack",            "hardness": 1.5, "color": (175, 145,  85), "drop": "drying_rack_item"},
    # --- Fishing supply chain ---
    BAIT_STATION_BLOCK:        {"name": "Bait Station",           "hardness": 1.5, "color": (100,  70,  40), "drop": "bait_station_item"},
    # --- Tea supply chain ---
    TEA_BUSH:                  {"name": "Tea Bush",                 "hardness": 0.5, "color": ( 60, 120,  50), "drop": "tea_seed",              "drop_chance": 1.0},
    TEA_CROP_YOUNG:            {"name": "Tea Plant",                "hardness": 0.5, "color": ( 75, 145,  65), "drop": "tea_seed",              "drop_chance": 1.0},
    TEA_CROP_MATURE:           {"name": "Tea Plant (Ripe)",         "hardness": 0.5, "color": (140, 185,  80), "drop": None},
    WITHERING_RACK_BLOCK:      {"name": "Withering Rack",           "hardness": 1.5, "color": (165, 130,  70), "drop": "withering_rack_item"},
    OXIDATION_STATION_BLOCK:   {"name": "Oxidation Station",        "hardness": 1.5, "color": ( 95,  75,  50), "drop": "oxidation_station_item"},
    TEA_CELLAR_BLOCK:          {"name": "Tea Cellar",               "hardness": 1.5, "color": ( 55,  45,  35), "drop": "tea_cellar_item"},
    ROASTING_KILN_BLOCK:       {"name": "Roasting Kiln",            "hardness": 2.0, "color": (110,  65,  30), "drop": "roasting_kiln_item"},
    # --- Herb bushes ---
    CHAMOMILE_BUSH:            {"name": "Chamomile Bush",           "hardness": 0.5, "color": (230, 215, 140), "drop": "chamomile_seed",  "drop_chance": 1.0},
    CHAMOMILE_CROP_YOUNG:      {"name": "Chamomile Plant",          "hardness": 0.5, "color": (130, 185,  90), "drop": "chamomile_seed",  "drop_chance": 1.0},
    CHAMOMILE_CROP_MATURE:     {"name": "Chamomile (Ripe)",         "hardness": 0.5, "color": (240, 230, 160), "drop": "chamomile_item",  "drop_chance": 1.0},
    LAVENDER_BUSH:             {"name": "Lavender Bush",            "hardness": 0.5, "color": (170, 130, 210), "drop": "lavender_seed",   "drop_chance": 1.0},
    LAVENDER_CROP_YOUNG:       {"name": "Lavender Plant",           "hardness": 0.5, "color": (120, 160, 100), "drop": "lavender_seed",   "drop_chance": 1.0},
    LAVENDER_CROP_MATURE:      {"name": "Lavender (Ripe)",          "hardness": 0.5, "color": (190, 150, 230), "drop": "lavender",        "drop_chance": 1.0},
    MINT_BUSH:                 {"name": "Mint Bush",                "hardness": 0.5, "color": ( 70, 200, 140), "drop": "mint_seed",       "drop_chance": 1.0},
    MINT_CROP_YOUNG:           {"name": "Mint Plant",               "hardness": 0.5, "color": ( 80, 185, 110), "drop": "mint_seed",       "drop_chance": 1.0},
    MINT_CROP_MATURE:          {"name": "Mint (Ripe)",              "hardness": 0.5, "color": ( 60, 210, 150), "drop": "mint",            "drop_chance": 1.0},
    ROSEMARY_BUSH:             {"name": "Rosemary Bush",            "hardness": 0.5, "color": (145, 165, 105), "drop": "rosemary_seed",   "drop_chance": 1.0},
    ROSEMARY_CROP_YOUNG:       {"name": "Rosemary Plant",           "hardness": 0.5, "color": (120, 155,  90), "drop": "rosemary_seed",   "drop_chance": 1.0},
    ROSEMARY_CROP_MATURE:      {"name": "Rosemary (Ripe)",          "hardness": 0.5, "color": (155, 175, 115), "drop": "rosemary",            "drop_chance": 1.0},
    THYME_BUSH:                {"name": "Thyme Bush",               "hardness": 0.5, "color": (110, 160,  80), "drop": "thyme_seed",           "drop_chance": 1.0},
    THYME_CROP_YOUNG:          {"name": "Thyme Plant",              "hardness": 0.5, "color": ( 95, 148,  68), "drop": "thyme_seed",           "drop_chance": 1.0},
    THYME_CROP_MATURE:         {"name": "Thyme (Ripe)",             "hardness": 0.5, "color": (125, 175,  95), "drop": "thyme",                "drop_chance": 1.0},
    SAGE_BUSH:                 {"name": "Sage Bush",                "hardness": 0.5, "color": (140, 158, 128), "drop": "sage_seed",            "drop_chance": 1.0},
    SAGE_CROP_YOUNG:           {"name": "Sage Plant",               "hardness": 0.5, "color": (120, 140, 108), "drop": "sage_seed",            "drop_chance": 1.0},
    SAGE_CROP_MATURE:          {"name": "Sage (Ripe)",              "hardness": 0.5, "color": (155, 172, 142), "drop": "sage",                 "drop_chance": 1.0},
    BASIL_BUSH:                {"name": "Basil Bush",               "hardness": 0.5, "color": ( 45, 162,  60), "drop": "basil_seed",           "drop_chance": 1.0},
    BASIL_CROP_YOUNG:          {"name": "Basil Plant",              "hardness": 0.5, "color": ( 38, 145,  52), "drop": "basil_seed",           "drop_chance": 1.0},
    BASIL_CROP_MATURE:         {"name": "Basil (Ripe)",             "hardness": 0.5, "color": ( 55, 180,  70), "drop": "basil",                "drop_chance": 1.0},
    OREGANO_BUSH:              {"name": "Oregano Bush",             "hardness": 0.5, "color": (100, 155,  75), "drop": "oregano_seed",         "drop_chance": 1.0},
    OREGANO_CROP_YOUNG:        {"name": "Oregano Plant",            "hardness": 0.5, "color": ( 85, 140,  65), "drop": "oregano_seed",         "drop_chance": 1.0},
    OREGANO_CROP_MATURE:       {"name": "Oregano (Ripe)",           "hardness": 0.5, "color": (115, 170,  85), "drop": "oregano",              "drop_chance": 1.0},
    DILL_BUSH:                 {"name": "Dill Bush",                "hardness": 0.5, "color": (130, 188,  72), "drop": "dill_seed",            "drop_chance": 1.0},
    DILL_CROP_YOUNG:           {"name": "Dill Plant",               "hardness": 0.5, "color": (115, 172,  62), "drop": "dill_seed",            "drop_chance": 1.0},
    DILL_CROP_MATURE:          {"name": "Dill (Ripe)",              "hardness": 0.5, "color": (148, 202,  85), "drop": "dill",                 "drop_chance": 1.0},
    FENNEL_BUSH:               {"name": "Fennel Bush",              "hardness": 0.5, "color": (122, 178,  68), "drop": "fennel_seed",          "drop_chance": 1.0},
    FENNEL_CROP_YOUNG:         {"name": "Fennel Plant",             "hardness": 0.5, "color": (108, 162,  58), "drop": "fennel_seed",          "drop_chance": 1.0},
    FENNEL_CROP_MATURE:        {"name": "Fennel (Ripe)",            "hardness": 0.5, "color": (138, 192,  80), "drop": "fennel",               "drop_chance": 1.0},
    TARRAGON_BUSH:             {"name": "Tarragon Bush",            "hardness": 0.5, "color": ( 90, 158,  80), "drop": "tarragon_seed",        "drop_chance": 1.0},
    TARRAGON_CROP_YOUNG:       {"name": "Tarragon Plant",           "hardness": 0.5, "color": ( 78, 142,  70), "drop": "tarragon_seed",        "drop_chance": 1.0},
    TARRAGON_CROP_MATURE:      {"name": "Tarragon (Ripe)",          "hardness": 0.5, "color": (102, 172,  90), "drop": "tarragon",             "drop_chance": 1.0},
    LEMON_BALM_BUSH:           {"name": "Lemon Balm Bush",          "hardness": 0.5, "color": ( 95, 192,  85), "drop": "lemon_balm_seed",      "drop_chance": 1.0},
    LEMON_BALM_CROP_YOUNG:     {"name": "Lemon Balm Plant",         "hardness": 0.5, "color": ( 82, 175,  74), "drop": "lemon_balm_seed",      "drop_chance": 1.0},
    LEMON_BALM_CROP_MATURE:    {"name": "Lemon Balm (Ripe)",        "hardness": 0.5, "color": (110, 208,  96), "drop": "lemon_balm",           "drop_chance": 1.0},
    ECHINACEA_BUSH:            {"name": "Echinacea Bush",           "hardness": 0.5, "color": (175, 100, 180), "drop": "echinacea_seed",       "drop_chance": 1.0},
    ECHINACEA_CROP_YOUNG:      {"name": "Echinacea Plant",          "hardness": 0.5, "color": (115, 155,  90), "drop": "echinacea_seed",       "drop_chance": 1.0},
    ECHINACEA_CROP_MATURE:     {"name": "Echinacea (Ripe)",         "hardness": 0.5, "color": (192, 115, 198), "drop": "echinacea",            "drop_chance": 1.0},
    VALERIAN_BUSH:             {"name": "Valerian Bush",            "hardness": 0.5, "color": (210, 212, 175), "drop": "valerian_seed",        "drop_chance": 1.0},
    VALERIAN_CROP_YOUNG:       {"name": "Valerian Plant",           "hardness": 0.5, "color": (128, 165, 100), "drop": "valerian_seed",        "drop_chance": 1.0},
    VALERIAN_CROP_MATURE:      {"name": "Valerian (Ripe)",          "hardness": 0.5, "color": (225, 225, 188), "drop": "valerian",             "drop_chance": 1.0},
    ST_JOHNS_WORT_BUSH:        {"name": "St. John's Wort Bush",     "hardness": 0.5, "color": (215, 198,  58), "drop": "st_johns_wort_seed",   "drop_chance": 1.0},
    ST_JOHNS_WORT_CROP_YOUNG:  {"name": "St. John's Wort Plant",    "hardness": 0.5, "color": (138, 168,  78), "drop": "st_johns_wort_seed",   "drop_chance": 1.0},
    ST_JOHNS_WORT_CROP_MATURE: {"name": "St. John's Wort (Ripe)",   "hardness": 0.5, "color": (232, 215,  70), "drop": "st_johns_wort",        "drop_chance": 1.0},
    YARROW_BUSH:               {"name": "Yarrow Bush",              "hardness": 0.5, "color": (235, 238, 230), "drop": "yarrow_seed",          "drop_chance": 1.0},
    YARROW_CROP_YOUNG:         {"name": "Yarrow Plant",             "hardness": 0.5, "color": (128, 165,  98), "drop": "yarrow_seed",          "drop_chance": 1.0},
    YARROW_CROP_MATURE:        {"name": "Yarrow (Ripe)",            "hardness": 0.5, "color": (248, 248, 242), "drop": "yarrow",               "drop_chance": 1.0},
    BERGAMOT_BUSH:             {"name": "Bergamot Bush",            "hardness": 0.5, "color": (200, 108, 188), "drop": "bergamot_seed",        "drop_chance": 1.0},
    BERGAMOT_CROP_YOUNG:       {"name": "Bergamot Plant",           "hardness": 0.5, "color": (112, 155,  90), "drop": "bergamot_seed",        "drop_chance": 1.0},
    BERGAMOT_CROP_MATURE:      {"name": "Bergamot (Ripe)",          "hardness": 0.5, "color": (215, 122, 202), "drop": "bergamot",             "drop_chance": 1.0},
    WORMWOOD_BUSH:             {"name": "Wormwood Bush",            "hardness": 0.5, "color": (165, 175, 145), "drop": "wormwood_seed",        "drop_chance": 1.0},
    WORMWOOD_CROP_YOUNG:       {"name": "Wormwood Plant",           "hardness": 0.5, "color": (145, 158, 128), "drop": "wormwood_seed",        "drop_chance": 1.0},
    WORMWOOD_CROP_MATURE:      {"name": "Wormwood (Ripe)",          "hardness": 0.5, "color": (180, 192, 158), "drop": "wormwood",             "drop_chance": 1.0},
    RUE_BUSH:                  {"name": "Rue Bush",                 "hardness": 0.5, "color": (128, 155, 162), "drop": "rue_seed",             "drop_chance": 1.0},
    RUE_CROP_YOUNG:            {"name": "Rue Plant",                "hardness": 0.5, "color": (112, 138, 145), "drop": "rue_seed",             "drop_chance": 1.0},
    RUE_CROP_MATURE:           {"name": "Rue (Ripe)",               "hardness": 0.5, "color": (142, 170, 178), "drop": "rue",                  "drop_chance": 1.0},
    LEMON_VERBENA_BUSH:        {"name": "Lemon Verbena Bush",       "hardness": 0.5, "color": (195, 215,  88), "drop": "lemon_verbena_seed",   "drop_chance": 1.0},
    LEMON_VERBENA_CROP_YOUNG:  {"name": "Lemon Verbena Plant",      "hardness": 0.5, "color": (175, 196,  78), "drop": "lemon_verbena_seed",   "drop_chance": 1.0},
    LEMON_VERBENA_CROP_MATURE: {"name": "Lemon Verbena (Ripe)",     "hardness": 0.5, "color": (212, 232,  98), "drop": "lemon_verbena",        "drop_chance": 1.0},
    HYSSOP_BUSH:               {"name": "Hyssop Bush",              "hardness": 0.5, "color": (128, 152, 212), "drop": "hyssop_seed",          "drop_chance": 1.0},
    HYSSOP_CROP_YOUNG:         {"name": "Hyssop Plant",             "hardness": 0.5, "color": (105, 145, 100), "drop": "hyssop_seed",          "drop_chance": 1.0},
    HYSSOP_CROP_MATURE:        {"name": "Hyssop (Ripe)",            "hardness": 0.5, "color": (142, 168, 228), "drop": "hyssop",               "drop_chance": 1.0},
    CATNIP_BUSH:               {"name": "Catnip Bush",              "hardness": 0.5, "color": (155, 175, 145), "drop": "catnip_seed",          "drop_chance": 1.0},
    CATNIP_CROP_YOUNG:         {"name": "Catnip Plant",             "hardness": 0.5, "color": (138, 158, 130), "drop": "catnip_seed",          "drop_chance": 1.0},
    CATNIP_CROP_MATURE:        {"name": "Catnip (Ripe)",            "hardness": 0.5, "color": (170, 192, 158), "drop": "catnip",               "drop_chance": 1.0},
    WOOD_SORREL_BUSH:          {"name": "Wood Sorrel Bush",         "hardness": 0.5, "color": ( 80, 178,  80), "drop": "wood_sorrel_seed",     "drop_chance": 1.0},
    WOOD_SORREL_CROP_YOUNG:    {"name": "Wood Sorrel Plant",        "hardness": 0.5, "color": ( 68, 160,  68), "drop": "wood_sorrel_seed",     "drop_chance": 1.0},
    WOOD_SORREL_CROP_MATURE:   {"name": "Wood Sorrel (Ripe)",       "hardness": 0.5, "color": ( 92, 195,  92), "drop": "wood_sorrel",          "drop_chance": 1.0},
    MARJORAM_BUSH:             {"name": "Marjoram Bush",            "hardness": 0.5, "color": (105, 162,  80), "drop": "marjoram_seed",        "drop_chance": 1.0},
    MARJORAM_CROP_YOUNG:       {"name": "Marjoram Plant",           "hardness": 0.5, "color": ( 90, 145,  70), "drop": "marjoram_seed",        "drop_chance": 1.0},
    MARJORAM_CROP_MATURE:      {"name": "Marjoram (Ripe)",          "hardness": 0.5, "color": (120, 178,  90), "drop": "marjoram",             "drop_chance": 1.0},
    SAVORY_BUSH:               {"name": "Savory Bush",              "hardness": 0.5, "color": (115, 152,  85), "drop": "savory_seed",          "drop_chance": 1.0},
    SAVORY_CROP_YOUNG:         {"name": "Savory Plant",             "hardness": 0.5, "color": (100, 135,  75), "drop": "savory_seed",          "drop_chance": 1.0},
    SAVORY_CROP_MATURE:        {"name": "Savory (Ripe)",            "hardness": 0.5, "color": (130, 168,  96), "drop": "savory",               "drop_chance": 1.0},
    ANGELICA_BUSH:             {"name": "Angelica Bush",            "hardness": 0.5, "color": ( 88, 172, 110), "drop": "angelica_seed",        "drop_chance": 1.0},
    ANGELICA_CROP_YOUNG:       {"name": "Angelica Plant",           "hardness": 0.5, "color": ( 75, 155,  98), "drop": "angelica_seed",        "drop_chance": 1.0},
    ANGELICA_CROP_MATURE:      {"name": "Angelica (Ripe)",          "hardness": 0.5, "color": (100, 188, 122), "drop": "angelica",             "drop_chance": 1.0},
    BORAGE_BUSH:               {"name": "Borage Bush",              "hardness": 0.5, "color": (118, 158, 218), "drop": "borage_seed",          "drop_chance": 1.0},
    BORAGE_CROP_YOUNG:         {"name": "Borage Plant",             "hardness": 0.5, "color": (105, 148, 100), "drop": "borage_seed",          "drop_chance": 1.0},
    BORAGE_CROP_MATURE:        {"name": "Borage (Ripe)",            "hardness": 0.5, "color": (132, 172, 235), "drop": "borage",               "drop_chance": 1.0},
    COMFREY_BUSH:              {"name": "Comfrey Bush",             "hardness": 0.5, "color": (158, 130, 202), "drop": "comfrey_seed",         "drop_chance": 1.0},
    COMFREY_CROP_YOUNG:        {"name": "Comfrey Plant",            "hardness": 0.5, "color": ( 98, 155,  90), "drop": "comfrey_seed",         "drop_chance": 1.0},
    COMFREY_CROP_MATURE:       {"name": "Comfrey (Ripe)",           "hardness": 0.5, "color": (172, 145, 218), "drop": "comfrey",              "drop_chance": 1.0},
    MUGWORT_BUSH:              {"name": "Mugwort Bush",             "hardness": 0.5, "color": (150, 165, 125), "drop": "mugwort_seed",         "drop_chance": 1.0},
    MUGWORT_CROP_YOUNG:        {"name": "Mugwort Plant",            "hardness": 0.5, "color": (130, 148, 110), "drop": "mugwort_seed",         "drop_chance": 1.0},
    MUGWORT_CROP_MATURE:       {"name": "Mugwort (Ripe)",           "hardness": 0.5, "color": (165, 182, 138), "drop": "mugwort",              "drop_chance": 1.0},
    # --- Middle Eastern crops ---
    CHICKPEA_CROP_YOUNG:       {"name": "Chickpea Crop",            "hardness": 0.5, "color": ( 90, 165,  80), "drop": "chickpea_seed",   "drop_chance": 1.0},
    CHICKPEA_CROP_MATURE:      {"name": "Chickpea Crop (Ripe)",     "hardness": 0.5, "color": (215, 195, 145), "drop": "chickpea",        "drop_chance": 1.0},
    LENTIL_CROP_YOUNG:         {"name": "Lentil Crop",              "hardness": 0.5, "color": ( 85, 155,  75), "drop": "lentil_seed",     "drop_chance": 1.0},
    LENTIL_CROP_MATURE:        {"name": "Lentil Crop (Ripe)",       "hardness": 0.5, "color": (185, 105,  65), "drop": "lentil",          "drop_chance": 1.0},
    SESAME_CROP_YOUNG:         {"name": "Sesame Crop",              "hardness": 0.5, "color": ( 80, 160,  85), "drop": "sesame_seed",       "drop_chance": 1.0},
    SESAME_CROP_MATURE:        {"name": "Sesame Crop (Ripe)",       "hardness": 0.5, "color": (240, 225, 180), "drop": "sesame_seeds",      "drop_chance": 1.0},
    POMEGRANATE_TREE_YOUNG:    {"name": "Pomegranate Tree",         "hardness": 0.5, "color": ( 55, 130,  55), "drop": "pomegranate_seed",  "drop_chance": 1.0},
    POMEGRANATE_TREE_MATURE:   {"name": "Pomegranate Tree (Ripe)",  "hardness": 0.5, "color": (175,  35,  55), "drop": "pomegranate",       "drop_chance": 1.0},
    # --- Spanish crops ---
    OLIVE_TREE_YOUNG:          {"name": "Olive Tree",               "hardness": 0.5, "color": ( 90, 140,  70), "drop": "olive_seed",        "drop_chance": 1.0},
    OLIVE_TREE_MATURE:         {"name": "Olive Tree (Ripe)",        "hardness": 0.5, "color": ( 60,  80,  45), "drop": "olive",             "drop_chance": 1.0},
    SAFFRON_CROP_YOUNG:        {"name": "Saffron Crop",             "hardness": 0.5, "color": ( 85, 160,  90), "drop": "saffron_seed",      "drop_chance": 1.0},
    SAFFRON_CROP_MATURE:       {"name": "Saffron Crop (Ripe)",      "hardness": 0.5, "color": (215, 130,  30), "drop": "saffron",           "drop_chance": 1.0},
    # --- Sonoran desert plants ---
    SAGUARO_YOUNG:             {"name": "Saguaro",                  "hardness": 0.5, "color": ( 52, 142,  48), "drop": "saguaro_seed",       "drop_chance": 1.0},
    SAGUARO_MATURE:            {"name": "Saguaro (Ripe)",           "hardness": 0.5, "color": ( 48, 130,  44), "drop": "saguaro_fruit",      "drop_chance": 1.0},
    BARREL_CACTUS_YOUNG:       {"name": "Barrel Cactus",           "hardness": 0.5, "color": ( 62, 148,  55), "drop": "barrel_cactus_seed", "drop_chance": 1.0},
    BARREL_CACTUS_MATURE:      {"name": "Barrel Cactus (Ripe)",    "hardness": 0.5, "color": ( 58, 142,  52), "drop": "barrel_cactus_pulp", "drop_chance": 1.0},
    OCOTILLO_YOUNG:            {"name": "Ocotillo",                 "hardness": 0.5, "color": (148,  82,  38), "drop": "ocotillo_seed",      "drop_chance": 1.0},
    OCOTILLO_MATURE:           {"name": "Ocotillo (Blooming)",      "hardness": 0.5, "color": (215,  52,  38), "drop": "ocotillo_flower",    "drop_chance": 1.0},
    PRICKLY_PEAR_YOUNG:        {"name": "Prickly Pear",             "hardness": 0.5, "color": ( 68, 155,  62), "drop": "prickly_pear_pad",   "drop_chance": 1.0},
    PRICKLY_PEAR_MATURE:       {"name": "Prickly Pear (Ripe)",      "hardness": 0.5, "color": (178,  42,  98), "drop": "prickly_pear_fruit", "drop_chance": 1.0},
    CHOLLA_YOUNG:              {"name": "Cholla",                   "hardness": 0.5, "color": ( 82, 155,  72), "drop": "cholla_segment",     "drop_chance": 1.0},
    CHOLLA_MATURE:             {"name": "Cholla (Mature)",          "hardness": 0.5, "color": ( 78, 150,  68), "drop": "cholla_joint",       "drop_chance": 1.0},
    PALO_VERDE_YOUNG:          {"name": "Palo Verde",               "hardness": 0.5, "color": ( 95, 148,  72), "drop": "palo_verde_seed",    "drop_chance": 1.0},
    PALO_VERDE_MATURE:         {"name": "Palo Verde (Flowering)",   "hardness": 0.5, "color": (225, 195,  45), "drop": "palo_verde_pod",     "drop_chance": 1.0},
    # --- Islamic architecture blocks ---
    WHITE_PLASTER_WALL: {"name": "White Plaster Wall", "hardness": 2, "color": (245, 240, 228), "drop": "white_plaster_wall"},
    CARVED_PLASTER:     {"name": "Carved Plaster",     "hardness": 2, "color": (245, 240, 228), "drop": "carved_plaster"},
    MUQARNAS_BLOCK:     {"name": "Muqarnas",           "hardness": 2, "color": (235, 228, 215), "drop": "muqarnas_block"},
    MASHRABIYA:         {"name": "Mashrabiya",          "hardness": 2, "color": (155, 105,  60), "drop": "mashrabiya"},
    ZELLIGE_TILE:       {"name": "Zellige Tile",        "hardness": 2, "color": ( 55, 130, 175), "drop": "zellige_tile"},
    ARABESQUE_PANEL:    {"name": "Arabesque Panel",     "hardness": 2, "color": (215, 195, 165), "drop": "arabesque_panel"},
    # --- Natural deposits ---
    CLAY_DEPOSIT:      {"name": "Clay Deposit",  "hardness": 0.8, "color": (165, 120,  85), "drop": "clay"},
    LIMESTONE_DEPOSIT: {"name": "Limestone Bed", "hardness": 1.5, "color": (210, 200, 180), "drop": "limestone_block"},
    # --- Spanish architecture blocks ---
    ADOBE_BRICK:         {"name": "Adobe Brick",          "hardness": 2, "color": (180, 155, 110), "drop": "adobe_brick"},
    SPANISH_ROOF_TILE:   {"name": "Spanish Roof Tile",    "hardness": 2, "color": (190,  90,  55), "drop": "spanish_roof_tile"},
    WROUGHT_IRON_GRILLE: {"name": "Wrought Iron Grille",  "hardness": 2, "color": ( 45,  38,  35), "drop": "wrought_iron_grille"},
    TALAVERA_TILE:       {"name": "Talavera Tile",         "hardness": 2, "color": (235, 240, 245), "drop": "talavera_tile"},
    SALTILLO_TILE:       {"name": "Saltillo Tile",         "hardness": 2, "color": (205, 130,  75), "drop": "saltillo_tile"},
    # --- Middle Eastern decorative doors ---
    COBALT_DOOR_CLOSED:        {"name": "Cobalt Door",           "hardness": 2, "color": ( 40,  75, 165), "drop": "cobalt_door"},
    COBALT_DOOR_OPEN:          {"name": "Cobalt Door (Open)",    "hardness": 2, "color": ( 40,  75, 165), "drop": "cobalt_door"},
    CRIMSON_CEDAR_DOOR_CLOSED: {"name": "Crimson Cedar Door",           "hardness": 2, "color": (140,  35,  40), "drop": "crimson_cedar_door"},
    CRIMSON_CEDAR_DOOR_OPEN:   {"name": "Crimson Cedar Door (Open)",    "hardness": 2, "color": (140,  35,  40), "drop": "crimson_cedar_door"},
    TEAL_DOOR_CLOSED:          {"name": "Teal Door",             "hardness": 2, "color": ( 45, 140, 135), "drop": "teal_door"},
    TEAL_DOOR_OPEN:            {"name": "Teal Door (Open)",      "hardness": 2, "color": ( 45, 140, 135), "drop": "teal_door"},
    # --- Salt supply chain ---
    SALT_DEPOSIT:          {"name": "Salt Deposit",    "hardness": 0.9, "color": (245, 242, 235), "drop": None},
    EVAPORATION_PAN_BLOCK: {"name": "Evaporation Pan", "hardness": 1.5, "color": (215, 210, 195), "drop": "evap_pan_item"},
    SALT_GRINDER_BLOCK:    {"name": "Salt Grinder",    "hardness": 1.5, "color": (190, 185, 175), "drop": "salt_grinder_item"},
    # --- Minecart system ---
    MINE_TRACK_BLOCK:      {"name": "Mine Track",      "hardness": 1,   "color": None,            "drop": "mine_track"},
    MINE_TRACK_STOP_BLOCK: {"name": "Track Stop",      "hardness": 2,   "color": None,            "drop": "mine_track_stop"},
    SAFFRON_DOOR_CLOSED:       {"name": "Saffron Door",          "hardness": 2, "color": (200, 155,  30), "drop": "saffron_door"},
    SAFFRON_DOOR_OPEN:         {"name": "Saffron Door (Open)",   "hardness": 2, "color": (200, 155,  30), "drop": "saffron_door"},
    # --- Palace doors ---
    STUDDED_OAK_DOOR_CLOSED:   {"name": "Studded Oak Door",         "hardness": 2, "color": (120,  80,  40), "drop": "studded_oak_door"},
    STUDDED_OAK_DOOR_OPEN:     {"name": "Studded Oak Door (Open)",  "hardness": 2, "color": (120,  80,  40), "drop": "studded_oak_door"},
    VERMILION_DOOR_CLOSED:     {"name": "Vermilion Door",           "hardness": 2, "color": (180,  40,  30), "drop": "vermilion_door"},
    VERMILION_DOOR_OPEN:       {"name": "Vermilion Door (Open)",    "hardness": 2, "color": (180,  40,  30), "drop": "vermilion_door"},
    SHOJI_DOOR_CLOSED:         {"name": "Shoji Door",               "hardness": 2, "color": (240, 230, 210), "drop": "shoji_door"},
    SHOJI_DOOR_OPEN:           {"name": "Shoji Door (Open)",        "hardness": 2, "color": (240, 230, 210), "drop": "shoji_door"},
    GILDED_DOOR_CLOSED:        {"name": "Gilded Door",              "hardness": 2, "color": (250, 220, 100), "drop": "gilded_door"},
    GILDED_DOOR_OPEN:          {"name": "Gilded Door (Open)",       "hardness": 2, "color": (250, 220, 100), "drop": "gilded_door"},
    BRONZE_DOOR_CLOSED:        {"name": "Bronze Door",              "hardness": 2, "color": (140, 100,  60), "drop": "bronze_door"},
    BRONZE_DOOR_OPEN:          {"name": "Bronze Door (Open)",       "hardness": 2, "color": (140, 100,  60), "drop": "bronze_door"},
    SWAHILI_DOOR_CLOSED:       {"name": "Swahili Door",             "hardness": 2, "color": (100,  60,  30), "drop": "swahili_door"},
    SWAHILI_DOOR_OPEN:         {"name": "Swahili Door (Open)",      "hardness": 2, "color": (100,  60,  30), "drop": "swahili_door"},
    SANDALWOOD_DOOR_CLOSED:    {"name": "Sandalwood Door",          "hardness": 2, "color": (150, 100,  60), "drop": "sandalwood_door"},
    SANDALWOOD_DOOR_OPEN:      {"name": "Sandalwood Door (Open)",   "hardness": 2, "color": (150, 100,  60), "drop": "sandalwood_door"},
    STONE_SLAB_DOOR_CLOSED:    {"name": "Stone Slab Door",          "hardness": 2, "color": (120, 120, 120), "drop": "stone_slab_door"},
    STONE_SLAB_DOOR_OPEN:      {"name": "Stone Slab Door (Open)",   "hardness": 2, "color": (120, 120, 120), "drop": "stone_slab_door"},
    # --- European architecture blocks ---
    HALF_TIMBER_WALL:  {"name": "Half-Timber Wall",   "hardness": 2, "color": (240, 235, 220), "drop": "half_timber_wall"},
    ASHLAR_BLOCK:      {"name": "Ashlar Block",        "hardness": 2, "color": (175, 170, 162), "drop": "ashlar_block"},
    GOTHIC_TRACERY:    {"name": "Gothic Tracery",      "hardness": 2, "color": ( 85,  82,  92), "drop": "gothic_tracery"},
    FLUTED_COLUMN:     {"name": "Fluted Column",       "hardness": 2, "color": (225, 218, 208), "drop": "fluted_column"},
    CORNICE_BLOCK:     {"name": "Cornice",             "hardness": 2, "color": (212, 206, 192), "drop": "cornice_block"},
    ROSE_WINDOW:       {"name": "Rose Window",         "hardness": 2, "color": ( 78,  75,  88), "drop": "rose_window"},
    HERRINGBONE_BRICK: {"name": "Herringbone Brick",   "hardness": 2, "color": (170,  82,  52), "drop": "herringbone_brick"},
    BAROQUE_TRIM:      {"name": "Baroque Trim",        "hardness": 2, "color": (232, 220, 193), "drop": "baroque_trim"},
    TUDOR_BEAM:        {"name": "Tudor Beam",          "hardness": 2, "color": ( 52,  36,  20), "drop": "tudor_beam"},
    VENETIAN_FLOOR:    {"name": "Venetian Floor",      "hardness": 2, "color": (228, 218, 198), "drop": "venetian_floor"},
    FLEMISH_BRICK:     {"name": "Flemish Brick",       "hardness": 2, "color": (158,  65,  42), "drop": "flemish_brick"},
    PILASTER:          {"name": "Pilaster",            "hardness": 2, "color": (200, 194, 182), "drop": "pilaster"},
    DENTIL_TRIM:       {"name": "Dentil Trim",         "hardness": 2, "color": (230, 225, 210), "drop": "dentil_trim"},
    WATTLE_DAUB:       {"name": "Wattle & Daub",       "hardness": 2, "color": (202, 178, 138), "drop": "wattle_daub"},
    NORDIC_PLANK:      {"name": "Nordic Plank",        "hardness": 2, "color": ( 58,  48,  40), "drop": "nordic_plank"},
    MANSARD_SLATE:     {"name": "Mansard Slate",       "hardness": 2, "color": ( 62,  67,  78), "drop": "mansard_slate"},
    ROMAN_MOSAIC:      {"name": "Roman Mosaic",        "hardness": 2, "color": (178, 162, 128), "drop": "roman_mosaic"},
    SETT_STONE:        {"name": "Sett Stone",          "hardness": 2, "color": (125, 120, 115), "drop": "sett_stone"},
    ROMANESQUE_ARCH:   {"name": "Romanesque Arch",     "hardness": 2, "color": (188, 178, 158), "drop": "romanesque_arch"},
    DARK_SLATE_ROOF:   {"name": "Dark Slate Roof",     "hardness": 2, "color": ( 55,  58,  68), "drop": "dark_slate_roof"},
    KEYSTONE:          {"name": "Keystone",            "hardness": 2, "color": (195, 188, 168), "drop": "keystone"},
    PLINTH_BLOCK:      {"name": "Plinth Block",        "hardness": 2, "color": (185, 182, 172), "drop": "plinth_block"},
    IRON_LANTERN:      {"name": "Iron Lantern",        "hardness": 2, "color": ( 42,  40,  36), "drop": "iron_lantern"},
    SANDSTONE_ASHLAR:  {"name": "Sandstone Ashlar",    "hardness": 2, "color": (215, 188, 142), "drop": "sandstone_ashlar"},
    GARGOYLE_BLOCK:    {"name": "Gargoyle Block",      "hardness": 2, "color": ( 82,  78,  88), "drop": "gargoyle_block"},
    OGEE_ARCH:               {"name": "Ogee Arch",             "hardness": 2, "color": ( 88,  82,  95), "drop": "ogee_arch"},
    RUSTICATED_STONE:        {"name": "Rusticated Stone",      "hardness": 2, "color": (158, 152, 140), "drop": "rusticated_stone"},
    CHEVRON_STONE:           {"name": "Chevron Stone",         "hardness": 2, "color": (178, 170, 158), "drop": "chevron_stone"},
    TRIGLYPH_PANEL:          {"name": "Triglyph Panel",        "hardness": 2, "color": (200, 195, 182), "drop": "triglyph_panel"},
    MARBLE_INLAY:            {"name": "Marble Inlay",          "hardness": 2, "color": (228, 222, 218), "drop": "marble_inlay"},
    BRICK_NOGGING:           {"name": "Brick Nogging",         "hardness": 2, "color": (162,  78,  52), "drop": "brick_nogging"},
    CRENELLATION:            {"name": "Crenellation",          "hardness": 2, "color": (168, 162, 150), "drop": "crenellation"},
    FAN_VAULT:               {"name": "Fan Vault",             "hardness": 2, "color": (205, 198, 185), "drop": "fan_vault"},
    ACANTHUS_PANEL:          {"name": "Acanthus Panel",        "hardness": 2, "color": (210, 202, 188), "drop": "acanthus_panel"},
    PEBBLE_DASH:             {"name": "Pebble Dash",           "hardness": 2, "color": (185, 175, 158), "drop": "pebble_dash"},
    ENCAUSTIC_TILE:          {"name": "Encaustic Tile",        "hardness": 2, "color": (142,  90,  50), "drop": "encaustic_tile"},
    CHEQUERBOARD_MARBLE:     {"name": "Chequerboard Marble",   "hardness": 2, "color": (218, 215, 212), "drop": "chequerboard_marble"},
    WROUGHT_IRON_BALUSTRADE: {"name": "Iron Balustrade",       "hardness": 2, "color": ( 42,  38,  35), "drop": "wrought_iron_balustrade"},
    OPUS_INCERTUM:           {"name": "Opus Incertum",         "hardness": 2, "color": (148, 142, 132), "drop": "opus_incertum"},
    GROTESQUE_FRIEZE:        {"name": "Grotesque Frieze",      "hardness": 2, "color": (190, 182, 165), "drop": "grotesque_frieze"},
    BARREL_VAULT:            {"name": "Barrel Vault",          "hardness": 2, "color": (198, 192, 178), "drop": "barrel_vault"},
    POINTED_ARCH:            {"name": "Pointed Arch",          "hardness": 2, "color": (180, 175, 165), "drop": "pointed_arch"},
    ENGLISH_BOND:            {"name": "English Bond",          "hardness": 2, "color": (155,  62,  42), "drop": "english_bond"},
    RELIEF_PANEL:            {"name": "Relief Panel",          "hardness": 2, "color": (205, 198, 182), "drop": "relief_panel"},
    DIAGONAL_TILE:           {"name": "Diagonal Tile",         "hardness": 2, "color": (215, 200, 172), "drop": "diagonal_tile"},
    TAPESTRY_BLOCK:    {"name": "Tapestry",          "hardness": 1, "color": (175,  88,  52), "drop": "tapestry_block"},
    WOVEN_RUG:         {"name": "Woven Rug",          "hardness": 1, "color": (138,  42,  42), "drop": "woven_rug"},
    CELTIC_KNOTWORK:   {"name": "Celtic Knotwork",    "hardness": 2, "color": ( 88,  88,  95), "drop": "celtic_knotwork"},
    BYZANTINE_MOSAIC:  {"name": "Byzantine Mosaic",   "hardness": 2, "color": (195, 165,  55), "drop": "byzantine_mosaic"},
    JAPANESE_SHOJI:    {"name": "Japanese Shoji",     "hardness": 1, "color": (240, 235, 225), "drop": "japanese_shoji"},
    OTTOMAN_TILE:      {"name": "Ottoman Tile",        "hardness": 2, "color": (240, 238, 235), "drop": "ottoman_tile"},
    LEADLIGHT_WINDOW:  {"name": "Leadlight Window",   "hardness": 2, "color": ( 62,  58,  52), "drop": "leadlight_window"},
    TUDOR_ROSE:        {"name": "Tudor Rose",          "hardness": 2, "color": (198, 188, 172), "drop": "tudor_rose"},
    GREEK_KEY:         {"name": "Greek Key",           "hardness": 2, "color": (215, 208, 192), "drop": "greek_key"},
    VENETIAN_PLASTER:  {"name": "Venetian Plaster",   "hardness": 2, "color": (235, 228, 215), "drop": "venetian_plaster"},
    SCOTTISH_RUBBLE:   {"name": "Scottish Rubble",    "hardness": 2, "color": (138, 132, 122), "drop": "scottish_rubble"},
    ART_NOUVEAU_PANEL: {"name": "Art Nouveau Panel",  "hardness": 2, "color": (222, 215, 195), "drop": "art_nouveau_panel"},
    DUTCH_GABLE:       {"name": "Dutch Gable",         "hardness": 2, "color": (162,  65,  45), "drop": "dutch_gable"},
    STRIPED_ARCH:      {"name": "Striped Arch",        "hardness": 2, "color": (182, 165, 142), "drop": "striped_arch"},
    TIMBER_TRUSS:      {"name": "Timber Truss",        "hardness": 2, "color": ( 70,  48,  28), "drop": "timber_truss"},
    HEARTH_STONE:      {"name": "Hearth Stone",        "hardness": 2, "color": (178, 162, 145), "drop": "hearth_stone"},
    LINEN_FOLD:        {"name": "Linen Fold",          "hardness": 2, "color": (155, 128,  90), "drop": "linen_fold"},
    PARQUET_FLOOR:     {"name": "Parquet Floor",       "hardness": 2, "color": (175, 130,  72), "drop": "parquet_floor"},
    COFFERED_CEILING:  {"name": "Coffered Ceiling",    "hardness": 2, "color": (205, 198, 182), "drop": "coffered_ceiling"},
    OPUS_SIGNINUM:     {"name": "Opus Signinum",       "hardness": 2, "color": (185, 115,  90), "drop": "opus_signinum"},
    # --- Textile supply chain ---
    FLAX_BUSH:                {"name": "Flax Bush",           "hardness": 0.5, "color": (170, 185, 210), "drop": "flax_seed",       "drop_chance": 1.0},
    FLAX_CROP_YOUNG:          {"name": "Flax Plant",          "hardness": 0.5, "color": (140, 185, 155), "drop": "flax_seed",       "drop_chance": 1.0},
    FLAX_CROP_MATURE:         {"name": "Flax Plant (Ripe)",   "hardness": 0.5, "color": (155, 185, 215), "drop": None},
    COTTON_BUSH:              {"name": "Cotton Bush",         "hardness": 0.5, "color": (210, 220, 175), "drop": "cotton_seed",     "drop_chance": 1.0},
    COTTON_CROP_YOUNG:        {"name": "Cotton Plant",        "hardness": 0.5, "color": (130, 190, 130), "drop": "cotton_seed",     "drop_chance": 1.0},
    COTTON_CROP_MATURE:       {"name": "Cotton Plant (Ripe)", "hardness": 0.5, "color": (240, 242, 235), "drop": None},
    # --- Pacific crops ---
    TARO_BUSH:                {"name": "Taro Bush",             "hardness": 0.5, "color": (135, 105, 155), "drop": "taro",       "drop_chance": 1.0},
    TARO_CROP_YOUNG:          {"name": "Taro Plant",            "hardness": 0.5, "color": (100, 150, 120), "drop": "taro",       "drop_chance": 1.0},
    TARO_CROP_MATURE:         {"name": "Taro Plant (Ripe)",     "hardness": 0.5, "color": (155, 130, 175), "drop": "taro"},
    BREADFRUIT_BUSH:          {"name": "Breadfruit Bush",       "hardness": 0.5, "color": (100, 150,  70), "drop": "breadfruit", "drop_chance": 1.0},
    BREADFRUIT_CROP_YOUNG:    {"name": "Breadfruit Sapling",    "hardness": 0.5, "color": ( 80, 140,  60), "drop": "breadfruit", "drop_chance": 1.0},
    BREADFRUIT_CROP_MATURE:   {"name": "Breadfruit Tree",       "hardness": 0.5, "color": (135, 165,  85), "drop": "breadfruit"},
    COCONUT_BUSH:             {"name": "Coconut Palm (Young)",  "hardness": 0.5, "color": ( 95, 130,  65), "drop": "coconut",    "drop_chance": 1.0},
    COCONUT_CROP_YOUNG:       {"name": "Coconut Palm",          "hardness": 0.5, "color": ( 75, 120,  55), "drop": "coconut",    "drop_chance": 1.0},
    COCONUT_CROP_MATURE:      {"name": "Coconut Palm (Ripe)",   "hardness": 0.5, "color": (120,  90,  55), "drop": "coconut"},
    SPINNING_WHEEL_BLOCK:     {"name": "Spinning Wheel",      "hardness": 1.5, "color": (165, 130,  75), "drop": "spinning_wheel_item"},
    DYE_VAT_BLOCK:            {"name": "Dye Vat",             "hardness": 1.5, "color": ( 85, 110, 155), "drop": "dye_vat_item"},
    LOOM_BLOCK:               {"name": "Loom",                "hardness": 1.5, "color": (140, 100,  55), "drop": "loom_item"},
    # Rug blocks (placeable floor pieces)
    TEXTILE_RUG_NATURAL:  {"name": "Rug (Natural)",  "hardness": 0.2, "color": (230, 215, 185), "drop": "textile_rug_natural"},
    TEXTILE_RUG_GOLDEN:   {"name": "Rug (Golden)",   "hardness": 0.2, "color": (215, 175,  40), "drop": "textile_rug_golden"},
    TEXTILE_RUG_CRIMSON:  {"name": "Rug (Crimson)",  "hardness": 0.2, "color": (185,  35,  45), "drop": "textile_rug_crimson"},
    TEXTILE_RUG_ROSE:     {"name": "Rug (Rose)",     "hardness": 0.2, "color": (220, 110, 155), "drop": "textile_rug_rose"},
    TEXTILE_RUG_COBALT:   {"name": "Rug (Cobalt)",   "hardness": 0.2, "color": ( 55,  90, 185), "drop": "textile_rug_cobalt"},
    TEXTILE_RUG_VIOLET:   {"name": "Rug (Violet)",   "hardness": 0.2, "color": (130,  65, 195), "drop": "textile_rug_violet"},
    TEXTILE_RUG_VERDANT:  {"name": "Rug (Verdant)",  "hardness": 0.2, "color": ( 60, 148,  75), "drop": "textile_rug_verdant"},
    TEXTILE_RUG_AMBER:    {"name": "Rug (Amber)",    "hardness": 0.2, "color": (200, 115,  35), "drop": "textile_rug_amber"},
    TEXTILE_RUG_IVORY:    {"name": "Rug (Ivory)",    "hardness": 0.2, "color": (245, 240, 220), "drop": "textile_rug_ivory"},
    # Tapestry blocks (placeable wall pieces)
    TEXTILE_TAPESTRY_NATURAL: {"name": "Tapestry (Natural)", "hardness": 0.2, "color": (210, 195, 165), "drop": "textile_tapestry_natural"},
    TEXTILE_TAPESTRY_GOLDEN:  {"name": "Tapestry (Golden)",  "hardness": 0.2, "color": (195, 155,  30), "drop": "textile_tapestry_golden"},
    TEXTILE_TAPESTRY_CRIMSON: {"name": "Tapestry (Crimson)", "hardness": 0.2, "color": (165,  25,  35), "drop": "textile_tapestry_crimson"},
    TEXTILE_TAPESTRY_ROSE:    {"name": "Tapestry (Rose)",    "hardness": 0.2, "color": (200,  90, 135), "drop": "textile_tapestry_rose"},
    TEXTILE_TAPESTRY_COBALT:  {"name": "Tapestry (Cobalt)",  "hardness": 0.2, "color": ( 40,  70, 165), "drop": "textile_tapestry_cobalt"},
    TEXTILE_TAPESTRY_VIOLET:  {"name": "Tapestry (Violet)",  "hardness": 0.2, "color": (110,  50, 175), "drop": "textile_tapestry_violet"},
    TEXTILE_TAPESTRY_VERDANT: {"name": "Tapestry (Verdant)", "hardness": 0.2, "color": ( 45, 128,  58), "drop": "textile_tapestry_verdant"},
    TEXTILE_TAPESTRY_AMBER:   {"name": "Tapestry (Amber)",   "hardness": 0.2, "color": (180,  95,  20), "drop": "textile_tapestry_amber"},
    TEXTILE_TAPESTRY_IVORY:   {"name": "Tapestry (Ivory)",   "hardness": 0.2, "color": (225, 220, 200), "drop": "textile_tapestry_ivory"},
    # --- Chinese architecture blocks ---
    GLAZED_ROOF_TILE: {"name": "Glazed Roof Tile",  "hardness": 2, "color": ( 78, 138,  75), "drop": "glazed_roof_tile"},
    LATTICE_SCREEN:   {"name": "Lattice Screen",    "hardness": 2, "color": (148,  98,  44), "drop": "lattice_screen"},
    MOON_GATE:        {"name": "Moon Gate",          "hardness": 2, "color": (185, 178, 165), "drop": "moon_gate"},
    PAINTED_BEAM:     {"name": "Painted Beam",       "hardness": 2, "color": (182,  32,  32), "drop": "painted_beam"},
    DOUGONG:          {"name": "Dougong",             "hardness": 2, "color": (162,  48,  36), "drop": "dougong"},
    CERAMIC_PLANTER:  {"name": "Ceramic Planter",    "hardness": 2, "color": ( 52,  92, 162), "drop": "ceramic_planter"},
    STONE_LANTERN:    {"name": "Stone Lantern",      "hardness": 2, "color": (158, 152, 142), "drop": "stone_lantern"},
    LACQUER_PANEL:    {"name": "Lacquer Panel",      "hardness": 2, "color": (162,  20,  20), "drop": "lacquer_panel"},
    PAPER_LANTERN:    {"name": "Paper Lantern",      "hardness": 1, "color": (215,  75,  48), "drop": "paper_lantern"},
    DRAGON_TILE:      {"name": "Dragon Tile",         "hardness": 2, "color": ( 60, 102,  65), "drop": "dragon_tile"},
    HAN_BRICK:        {"name": "Han Brick",           "hardness": 2, "color": ( 92,  88,  85), "drop": "han_brick"},
    PAVILION_FLOOR:   {"name": "Pavilion Floor",     "hardness": 2, "color": (188, 185, 178), "drop": "pavilion_floor"},
    BAMBOO_SCREEN:    {"name": "Bamboo Screen",      "hardness": 2, "color": (100, 138,  58), "drop": "bamboo_screen"},
    CLOUD_MOTIF:      {"name": "Cloud Motif",         "hardness": 2, "color": (215, 210, 198), "drop": "cloud_motif"},
    COIN_TILE:        {"name": "Coin Tile",           "hardness": 2, "color": ( 52,  98, 152), "drop": "coin_tile"},
    BLUE_WHITE_TILE:  {"name": "Blue & White Tile",  "hardness": 2, "color": (238, 236, 233), "drop": "blue_white_tile"},
    GARDEN_ROCK:      {"name": "Garden Rock",         "hardness": 2, "color": ( 98,  95, 105), "drop": "garden_rock_block"},
    STEPPED_WALL:     {"name": "Stepped Wall",        "hardness": 2, "color": (140, 132, 120), "drop": "stepped_wall"},
    PAGODA_EAVE:      {"name": "Pagoda Eave",         "hardness": 2, "color": (178,  32,  32), "drop": "pagoda_eave"},
    CINNABAR_WALL:    {"name": "Cinnabar Wall",       "hardness": 2, "color": (172,  32,  25), "drop": "cinnabar_wall"},
    # --- World architecture blocks — batch 4 ---
    MUGHAL_ARCH:       {"name": "Mughal Arch",        "hardness": 2, "color": (178, 168, 158), "drop": "mughal_arch"},
    PIETRA_DURA:       {"name": "Pietra Dura",        "hardness": 2, "color": (232, 228, 222), "drop": "pietra_dura"},
    EGYPTIAN_FRIEZE:   {"name": "Egyptian Frieze",    "hardness": 2, "color": (205, 180, 120), "drop": "egyptian_frieze"},
    SANDSTONE_COLUMN:  {"name": "Sandstone Column",   "hardness": 2, "color": (215, 185, 135), "drop": "sandstone_column"},
    AZTEC_SUNSTONE:    {"name": "Aztec Sunstone",     "hardness": 2, "color": ( 88,  82,  75), "drop": "aztec_sunstone"},
    MAYA_RELIEF:       {"name": "Maya Relief",        "hardness": 2, "color": (155, 148, 135), "drop": "maya_relief"},
    VIKING_CARVING:    {"name": "Viking Carving",     "hardness": 2, "color": ( 95,  68,  42), "drop": "viking_carving"},
    RUNE_STONE:        {"name": "Rune Stone",         "hardness": 2, "color": (148, 142, 132), "drop": "rune_stone"},
    PERSIAN_IWAN:      {"name": "Persian Iwan",       "hardness": 2, "color": (188, 168, 138), "drop": "persian_iwan"},
    KILIM_TILE:        {"name": "Kilim Tile",         "hardness": 2, "color": (168,  52,  42), "drop": "kilim_tile"},
    AFRICAN_MUD_BRICK: {"name": "African Mud Brick",  "hardness": 2, "color": (175, 118,  72), "drop": "african_mud_brick"},
    KENTE_PANEL:       {"name": "Kente Panel",        "hardness": 2, "color": (185, 148,  30), "drop": "kente_panel"},
    WAT_FINIAL:        {"name": "Wat Finial",         "hardness": 2, "color": (195, 162,  35), "drop": "wat_finial"},
    KHMER_STONE:       {"name": "Khmer Stone",        "hardness": 2, "color": (132, 128, 118), "drop": "khmer_stone"},
    HANJI_SCREEN:      {"name": "Hanji Screen",       "hardness": 2, "color": (238, 232, 222), "drop": "hanji_screen"},
    DANCHEONG:         {"name": "Dancheong",           "hardness": 2, "color": ( 55,  95, 158), "drop": "dancheong"},
    ART_DECO_PANEL:    {"name": "Art Deco Panel",     "hardness": 2, "color": (225, 215, 188), "drop": "art_deco_panel"},
    OBSIDIAN_CUT:      {"name": "Obsidian Cut",       "hardness": 2, "color": ( 28,  24,  32), "drop": "obsidian_cut"},
    OTTOMAN_ARCH:      {"name": "Ottoman Arch",       "hardness": 2, "color": (182, 172, 155), "drop": "ottoman_arch"},
    LOTUS_CAPITAL:     {"name": "Lotus Capital",      "hardness": 2, "color": (208, 188, 152), "drop": "lotus_capital"},
    # --- World architecture batch 5 ---
    AZULEJO_TILE:      {"name": "Azulejo Tile",       "hardness": 2, "color": (235, 240, 248), "drop": "azulejo_tile"},
    MANUELINE_PANEL:   {"name": "Manueline Panel",    "hardness": 2, "color": (195, 182, 162), "drop": "manueline_panel"},
    TORII_PANEL:       {"name": "Torii Panel",         "hardness": 2, "color": (195,  45,  32), "drop": "torii_panel"},
    INCA_ASHLAR:       {"name": "Inca Ashlar",         "hardness": 2, "color": (162, 148, 128), "drop": "inca_ashlar"},
    RUSSIAN_KOKOSHNIK: {"name": "Russian Kokoshnik",  "hardness": 2, "color": (215, 180, 145), "drop": "russian_kokoshnik"},
    ONION_DOME_TILE:   {"name": "Onion Dome Tile",    "hardness": 2, "color": ( 72, 130, 185), "drop": "onion_dome_tile"},
    GEORGIAN_FANLIGHT: {"name": "Georgian Fanlight",  "hardness": 2, "color": (215, 225, 240), "drop": "georgian_fanlight"},
    PALLADIAN_WINDOW:  {"name": "Palladian Window",   "hardness": 2, "color": (200, 195, 182), "drop": "palladian_window"},
    STAVE_PLANK:       {"name": "Stave Plank",         "hardness": 2, "color": ( 68,  48,  28), "drop": "stave_plank"},
    IONIC_CAPITAL:     {"name": "Ionic Capital",       "hardness": 2, "color": (222, 215, 202), "drop": "ionic_capital"},
    MOORISH_STAR_TILE: {"name": "Moorish Star Tile",  "hardness": 2, "color": ( 45,  85, 162), "drop": "moorish_star_tile"},
    CRAFTSMAN_PANEL:   {"name": "Craftsman Panel",    "hardness": 2, "color": (148, 105,  55), "drop": "craftsman_panel"},
    BRUTALIST_PANEL:   {"name": "Brutalist Panel",    "hardness": 2, "color": (155, 150, 145), "drop": "brutalist_panel"},
    METOPE:            {"name": "Metope",              "hardness": 2, "color": (210, 202, 188), "drop": "metope"},
    ARMENIAN_KHACHKAR: {"name": "Armenian Khachkar",  "hardness": 2, "color": (175, 165, 148), "drop": "armenian_khachkar"},
    BENIN_RELIEF:      {"name": "Benin Relief",        "hardness": 2, "color": (168, 128,  55), "drop": "benin_relief"},
    MAORI_CARVING:     {"name": "Māori Carving",       "hardness": 2, "color": ( 80,  55,  32), "drop": "maori_carving"},
    MUGHAL_JALI:       {"name": "Mughal Jali",         "hardness": 2, "color": (215, 208, 195), "drop": "mughal_jali"},
    PERSIAN_TILE:      {"name": "Persian Tile",        "hardness": 2, "color": ( 58, 148, 162), "drop": "persian_tile"},
    SWISS_CHALET:      {"name": "Swiss Chalet Panel",  "hardness": 2, "color": (165, 115,  55), "drop": "swiss_chalet"},
    ANDEAN_TEXTILE:    {"name": "Andean Textile",      "hardness": 2, "color": (168,  45,  42), "drop": "andean_textile"},
    BAROQUE_ORNAMENT:  {"name": "Baroque Ornament",    "hardness": 2, "color": (225, 205, 158), "drop": "baroque_ornament"},
    POLYNESIAN_CARVED: {"name": "Polynesian Carved",  "hardness": 2, "color": (105,  72,  42), "drop": "polynesian_carved"},
    MOORISH_COLUMN:    {"name": "Moorish Column",      "hardness": 2, "color": (198, 188, 172), "drop": "moorish_column"},
    PORTUGUESE_CORK:   {"name": "Portuguese Cork",    "hardness": 2, "color": (168, 128,  72), "drop": "portuguese_cork"},
    WHITEWASHED_WALL: {"name": "Whitewashed Wall",    "hardness": 2, "color": (238, 232, 218), "drop": "stone_chip"},
    MONASTERY_ROOF:   {"name": "Monastery Roof",      "hardness": 2, "color": ( 88,  22,  18), "drop": "lumber"},
    MANI_STONE:       {"name": "Mani Stone",           "hardness": 3, "color": (152, 144, 135), "drop": "stone_chip"},
    PRAYER_FLAG_BLOCK:{"name": "Prayer Flags",         "hardness": 1, "color": ( 60, 100, 175), "drop": None},
    # --- Cheese supply chain ---
    DAIRY_VAT_BLOCK:   {"name": "Dairy Vat",    "hardness": 1.5, "color": (220, 215, 200), "drop": "dairy_vat_item"},
    CHEESE_PRESS_BLOCK:{"name": "Cheese Press", "hardness": 1.5, "color": (175, 145, 100), "drop": "cheese_press_item"},
    AGING_CAVE_BLOCK:  {"name": "Aging Cave",   "hardness": 2.0, "color": (100,  88,  75), "drop": "aging_cave_item"},
    FLETCHING_TABLE_BLOCK: {"name": "Fletching Table", "hardness": 2, "color": (139, 110, 75), "drop": "fletching_table_item"},
    # Geological strata — depth-banded stone types
    LIMESTONE_STONE: {"name": "Limestone",     "hardness": 2,   "color": (200, 195, 170), "drop": "limestone_chip"},
    GRANITE_STONE:   {"name": "Granite",        "hardness": 2.5, "color": (165, 140, 130), "drop": "granite_slab"},
    BASALT_STONE:    {"name": "Basalt",         "hardness": 3,   "color": (80,  80,  90),  "drop": "basalt_shard"},
    MAGMATIC_STONE:  {"name": "Magmatic Stone", "hardness": 3.5, "color": (60,  40,  35),  "drop": "magmatic_shard"},
    SMELTER_BLOCK:        {"name": "Smelter",         "hardness": 2,   "color": (160, 80,  50),  "drop": "smelter_item"},
    ANAEROBIC_TANK_BLOCK: {"name": "Anaerobic Tank",  "hardness": 1.5, "color": ( 70, 90,  55),  "drop": "anaerobic_tank_item"},
    # --- Glass Kiln station ---
    GLASS_KILN_BLOCK:     {"name": "Glass Kiln",              "hardness": 1.5, "color": (145,  80,  50), "drop": "glass_kiln_item"},
    # --- Glass Kiln products ---
    CLEAR_GLASS:          {"name": "Clear Glass",             "hardness": 2,   "color": (230, 240, 250), "drop": "clear_glass"},
    STAINED_GLASS_GOLDEN: {"name": "Stained Glass (Golden)",  "hardness": 2,   "color": (215, 175,  40), "drop": "stained_glass_golden"},
    STAINED_GLASS_CRIMSON:{"name": "Stained Glass (Crimson)", "hardness": 2,   "color": (185,  35,  45), "drop": "stained_glass_crimson"},
    STAINED_GLASS_ROSE:   {"name": "Stained Glass (Rose)",    "hardness": 2,   "color": (220, 110, 155), "drop": "stained_glass_rose"},
    STAINED_GLASS_COBALT: {"name": "Stained Glass (Cobalt)",  "hardness": 2,   "color": ( 55,  90, 185), "drop": "stained_glass_cobalt"},
    STAINED_GLASS_VIOLET: {"name": "Stained Glass (Violet)",  "hardness": 2,   "color": (130,  65, 195), "drop": "stained_glass_violet"},
    STAINED_GLASS_VERDANT:{"name": "Stained Glass (Verdant)", "hardness": 2,   "color": ( 60, 148,  75), "drop": "stained_glass_verdant"},
    STAINED_GLASS_AMBER:  {"name": "Stained Glass (Amber)",   "hardness": 2,   "color": (200, 115,  35), "drop": "stained_glass_amber"},
    STAINED_GLASS_IVORY:  {"name": "Stained Glass (Ivory)",   "hardness": 2,   "color": (245, 240, 220), "drop": "stained_glass_ivory"},
    CATHEDRAL_WINDOW:     {"name": "Cathedral Window",         "hardness": 2,   "color": ( 80, 130, 200), "drop": "cathedral_window"},
    MOSAIC_GLASS:         {"name": "Mosaic Glass",             "hardness": 2,   "color": (160, 100, 190), "drop": "mosaic_glass"},
    SMOKED_GLASS:         {"name": "Smoked Glass",             "hardness": 2,   "color": ( 45,  55,  65), "drop": "smoked_glass"},
    # --- Elevator system ---
    ELEVATOR_STOP_BLOCK:  {"name": "Elevator Stop",  "hardness": 3,   "color": ( 90,  90, 110), "drop": "elevator_stop"},
    ELEVATOR_CABLE_BLOCK: {"name": "Elevator Cable", "hardness": 1,   "color": None,            "drop": "elevator_cable"},
    # --- Additional glass varieties ---
    RIBBED_GLASS:         {"name": "Ribbed Glass",             "hardness": 2,   "color": (210, 230, 248), "drop": "ribbed_glass"},
    HAMMERED_GLASS:       {"name": "Hammered Glass",           "hardness": 2,   "color": (195, 220, 235), "drop": "hammered_glass"},
    CRACKLED_GLASS:       {"name": "Crackled Glass",           "hardness": 2,   "color": (200, 235, 250), "drop": "crackled_glass"},
    OCULUS_WINDOW:        {"name": "Oculus Window",            "hardness": 2,   "color": ( 90, 150, 210), "drop": "oculus_window"},
    LANCET_WINDOW:        {"name": "Lancet Window",            "hardness": 2,   "color": ( 70, 120, 190), "drop": "lancet_window"},
    DIAMOND_PANE:         {"name": "Diamond Pane",             "hardness": 2,   "color": (220, 235, 245), "drop": "diamond_pane"},
    SEA_GLASS:            {"name": "Sea Glass",                "hardness": 2,   "color": (120, 195, 175), "drop": "sea_glass"},
    MIRROR_GLASS:         {"name": "Mirror Glass",             "hardness": 2,   "color": (210, 215, 225), "drop": "mirror_glass"},
    IRIDESCENT_GLASS:     {"name": "Iridescent Glass",         "hardness": 2,   "color": (175, 140, 210), "drop": "iridescent_glass"},
    SUNSET_GLASS:         {"name": "Sunset Glass",             "hardness": 2,   "color": (230, 120,  70), "drop": "sunset_glass"},
    OBSIDIAN_GLASS:       {"name": "Obsidian Glass",           "hardness": 2,   "color": ( 28,  18,  42), "drop": "obsidian_glass"},
    CRYSTAL_GLASS:        {"name": "Crystal Glass",            "hardness": 2,   "color": (215, 245, 255), "drop": "crystal_glass"},
    JEWELRY_WORKBENCH_BLOCK: {"name": "Jewelry Workbench",     "hardness": 3,   "color": (180, 150,  80), "drop": "jewelry_workbench_item", "drop_chance": 1.0},
    # --- Garden Workshop blocks ---
    GARDEN_WORKSHOP_BLOCK: {"name": "Garden Workshop",      "hardness": 2.0, "color": (160, 140, 110), "drop": "garden_workshop_item"},
    ZELLIGE_BLUE:          {"name": "Zellige Blue",         "hardness": 1.5, "color": ( 45, 100, 175), "drop": "zellige_blue"},
    ZELLIGE_TERRACOTTA:    {"name": "Zellige Terracotta",   "hardness": 1.5, "color": (195,  95,  55), "drop": "zellige_terracotta"},
    ZELLIGE_EMERALD:       {"name": "Zellige Emerald",      "hardness": 1.5, "color": ( 40, 130,  80), "drop": "zellige_emerald"},
    ZELLIGE_WHITE:         {"name": "Zellige Ivory",        "hardness": 1.5, "color": (230, 225, 210), "drop": "zellige_white"},
    GARDEN_STAR_TILE:      {"name": "Star Tile",            "hardness": 1.5, "color": ( 80,  70,  65), "drop": "garden_star_tile"},
    GEOMETRIC_MOSAIC:      {"name": "Geometric Mosaic",     "hardness": 1.5, "color": (160, 140, 100), "drop": "geometric_mosaic"},
    WATER_CHANNEL:         {"name": "Water Channel",        "hardness": 0.5, "color": ( 80, 155, 200), "drop": None},
    ORNAMENTAL_POOL:       {"name": "Ornamental Pool",      "hardness": 0.5, "color": ( 55, 130, 185), "drop": None},
    FOUNTAIN_BASIN:        {"name": "Fountain Basin",       "hardness": 2.0, "color": (150, 140, 130), "drop": "fountain_basin"},
    TIERED_FOUNTAIN:       {"name": "Tiered Fountain",      "hardness": 2.0, "color": (150, 140, 130), "drop": "tiered_fountain"},
    HORSESHOE_ARCH:        {"name": "Horseshoe Arch",       "hardness": 2.0, "color": (185, 175, 155), "drop": "horseshoe_arch"},
    MUQARNAS_PANEL:        {"name": "Muqarnas Panel",       "hardness": 1.5, "color": (220, 210, 195), "drop": "muqarnas_panel"},
    ARABESQUE_SCREEN:      {"name": "Arabesque Screen",     "hardness": 1.5, "color": (190, 180, 165), "drop": "arabesque_screen"},
    GARDEN_COLUMN:         {"name": "Garden Column",        "hardness": 2.5, "color": (200, 195, 185), "drop": "garden_column"},
    MARBLE_PLINTH:         {"name": "Marble Plinth",        "hardness": 2.5, "color": (215, 210, 205), "drop": "marble_plinth"},
    GARDEN_OBELISK:        {"name": "Garden Obelisk",       "hardness": 2.5, "color": (170, 165, 155), "drop": "garden_obelisk"},
    TOPIARY_CONE:          {"name": "Topiary Cone",         "hardness": 1.0, "color": ( 40, 105,  50), "drop": "topiary_cone"},
    TOPIARY_SPHERE:        {"name": "Topiary Sphere",       "hardness": 1.0, "color": ( 45, 115,  55), "drop": "topiary_sphere"},
    BOX_HEDGE:             {"name": "Box Hedge",            "hardness": 1.0, "color": ( 55, 100,  45), "drop": "box_hedge"},
    CLIMBING_ROSE:         {"name": "Climbing Rose",        "hardness": 0.5, "color": ( 60,  90,  50), "drop": "climbing_rose"},
    STONE_BENCH:           {"name": "Stone Bench",          "hardness": 1.5, "color": (175, 168, 158), "drop": "stone_bench"},
    STONE_URN:             {"name": "Stone Urn",            "hardness": 1.5, "color": (180, 172, 162), "drop": "stone_urn"},
    TERRACOTTA_PLANTER:    {"name": "Terracotta Planter",   "hardness": 1.0, "color": (185, 100,  65), "drop": "terracotta_planter"},
    SUNDIAL:               {"name": "Sundial",              "hardness": 1.5, "color": (170, 165, 150), "drop": "sundial"},
    GARDEN_LANTERN:        {"name": "Garden Lantern",       "hardness": 1.0, "color": ( 80,  75,  70), "drop": "garden_lantern"},
    GRAVEL_PATH:           {"name": "Gravel Path",          "hardness": 0.5, "color": (195, 188, 175), "drop": "gravel_path"},
    MOSAIC_PATH:           {"name": "Mosaic Path",          "hardness": 1.5, "color": (175, 155, 120), "drop": "mosaic_path"},
    TERRACOTTA_PATH:       {"name": "Terracotta Path",      "hardness": 1.0, "color": (190, 110,  75), "drop": "terracotta_path"},
    COBBLE_CIRCLE:         {"name": "Cobble Circle",        "hardness": 1.5, "color": (120, 115, 108), "drop": "cobble_circle"},

    # Sculpture system
    SCULPTURE_BLOCK_ROOT:  {"name": "Sculpture",            "hardness": 2.0, "color": (180, 175, 165), "drop": None},
    SCULPTURE_BLOCK_BODY:  {"name": "Sculpture (Body)",     "hardness": 2.0, "color": (180, 175, 165), "drop": None},
    SCULPTORS_BENCH:       {"name": "Sculptor's Bench",     "hardness": 1.0, "color": (160, 130,  90), "drop": "sculptors_bench_item"},
    # Custom Tapestry system
    TAPESTRY_FRAME_BLOCK:  {"name": "Tapestry Frame",       "hardness": 1.0, "color": (150, 110,  65), "drop": "tapestry_frame_item"},
    CUSTOM_TAPESTRY_ROOT:  {"name": "Tapestry",             "hardness": 1.0, "color": (210, 195, 160), "drop": None},
    CUSTOM_TAPESTRY_BODY:  {"name": "Tapestry (Body)",      "hardness": 1.0, "color": (210, 195, 160), "drop": None},
    # --- Garden Workshop extension ---
    PERGOLA_POST:          {"name": "Pergola Post",         "hardness": 1.0, "color": (140, 100,  55), "drop": "pergola_post"},
    WISTERIA_ARCH:         {"name": "Wisteria Arch",        "hardness": 1.5, "color": (185, 175, 160), "drop": "wisteria_arch"},
    GARDEN_GATE:           {"name": "Garden Gate",          "hardness": 1.5, "color": ( 55,  60,  65), "drop": "garden_gate"},
    LOW_GARDEN_WALL:       {"name": "Low Garden Wall",      "hardness": 2.0, "color": (175, 168, 155), "drop": "low_garden_wall"},
    POOL_COPING:           {"name": "Pool Coping",          "hardness": 1.5, "color": (205, 200, 190), "drop": "pool_coping"},
    STEPPING_STONE:        {"name": "Stepping Stone",       "hardness": 1.0, "color": (155, 150, 140), "drop": "stepping_stone"},
    OPUS_VERMICULATUM:     {"name": "Opus Vermiculatum",    "hardness": 1.5, "color": (170, 155, 125), "drop": "opus_vermiculatum"},
    PORPHYRY_TILE:         {"name": "Porphyry Tile",        "hardness": 2.0, "color": ( 90,  55,  80), "drop": "porphyry_tile"},
    BRICK_EDGING:          {"name": "Brick Edging",         "hardness": 0.5, "color": (170,  80,  50), "drop": "brick_edging"},
    SPIRAL_TOPIARY:        {"name": "Spiral Topiary",       "hardness": 1.0, "color": ( 38, 100,  48), "drop": "spiral_topiary"},
    MAZE_HEDGE:            {"name": "Maze Hedge",           "hardness": 1.5, "color": ( 30,  80,  38), "drop": "maze_hedge"},
    WISTERIA_WALL:         {"name": "Wisteria Wall",        "hardness": 0.5, "color": (140, 100, 170), "drop": "wisteria_wall"},
    POTTED_CITRUS:         {"name": "Potted Citrus",        "hardness": 0.5, "color": (185, 100,  60), "drop": "potted_citrus"},
    MARBLE_STATUE:         {"name": "Marble Statue",        "hardness": 2.5, "color": (220, 215, 208), "drop": "marble_statue"},
    MARBLE_BIRDBATH:       {"name": "Marble Birdbath",      "hardness": 2.0, "color": (215, 210, 202), "drop": "marble_birdbath"},
    GARDEN_TABLE:          {"name": "Garden Table",         "hardness": 1.5, "color": (185, 178, 165), "drop": "garden_table"},
    IRON_TRELLIS:          {"name": "Iron Trellis",         "hardness": 1.5, "color": ( 50,  55,  58), "drop": "iron_trellis"},
    NASRID_PANEL:          {"name": "Nasrid Panel",         "hardness": 1.5, "color": (228, 218, 195), "drop": "nasrid_panel"},
    SCALLOP_NICHE:         {"name": "Scallop Niche",        "hardness": 1.5, "color": (200, 190, 172), "drop": "scallop_niche"},
    TERRACE_BALUSTRADE:    {"name": "Terrace Balustrade",   "hardness": 2.0, "color": (210, 205, 195), "drop": "terrace_balustrade"},
    # Japanese garden blocks
    ZEN_GRAVEL:         {"name": "Zen Gravel",          "hardness": 0.5, "color": (200, 195, 182), "drop": "zen_gravel"},
    KARESANSUI_ROCK:    {"name": "Karesansui Rock",     "hardness": 2.5, "color": (130, 125, 118), "drop": "karesansui_rock"},
    MOSS_CARPET:        {"name": "Moss Carpet",         "hardness": 0.5, "color": ( 52,  95,  42), "drop": "moss_carpet"},
    TSUKUBAI:           {"name": "Tsukubai",            "hardness": 2.0, "color": (140, 135, 125), "drop": "tsukubai"},
    TORO_LANTERN:       {"name": "Toro Lantern",        "hardness": 2.0, "color": (155, 150, 140), "drop": "toro_lantern"},
    YUKIMI_LANTERN:     {"name": "Yukimi Lantern",      "hardness": 2.0, "color": (165, 160, 150), "drop": "yukimi_lantern"},
    BAMBOO_FENCE_JP:    {"name": "Bamboo Fence",        "hardness": 0.5, "color": (140, 160,  60), "drop": "bamboo_fence_jp"},
    ROJI_STONE:         {"name": "Roji Stone",          "hardness": 1.0, "color": (100,  95,  88), "drop": "roji_stone"},
    PINE_TOPIARY_JP:    {"name": "Cloud-Pruned Pine",   "hardness": 1.0, "color": ( 35,  85,  40), "drop": "pine_topiary_jp"},
    JAPANESE_MAPLE:     {"name": "Japanese Maple",      "hardness": 0.5, "color": (185,  60,  35), "drop": "japanese_maple"},
    SHISHI_ODOSHI:      {"name": "Shishi-odoshi",       "hardness": 0.5, "color": (140, 160,  60), "drop": "shishi_odoshi"},
    RED_ARCH_BRIDGE:    {"name": "Arched Bridge",       "hardness": 1.5, "color": (175,  35,  30), "drop": "red_arch_bridge"},
    WAVE_CERAMIC:       {"name": "Wave Ceramic",        "hardness": 1.5, "color": ( 45,  90, 165), "drop": "wave_ceramic"},
    ZEN_SAND_RING:      {"name": "Zen Sand Ring",       "hardness": 0.5, "color": (210, 205, 190), "drop": "zen_sand_ring"},
    BAMBOO_GATE_JP:     {"name": "Bamboo Gate",         "hardness": 0.5, "color": (130, 150,  55), "drop": "bamboo_gate_jp"},
    WABI_STONE:         {"name": "Wabi Stone",          "hardness": 2.5, "color": ( 85,  82,  75), "drop": "wabi_stone"},
    CHERRY_ARCH:        {"name": "Cherry Blossom Arch", "hardness": 1.0, "color": (195, 155, 175), "drop": "cherry_arch"},
    TATAMI_PAVING:      {"name": "Tatami Paving",       "hardness": 1.0, "color": (185, 172, 130), "drop": "tatami_paving"},
    IKEBANA_STONE:      {"name": "Ikebana Stone",       "hardness": 1.5, "color": (125, 120, 112), "drop": "ikebana_stone"},
    KANJI_STONE:        {"name": "Kanji Stone",         "hardness": 2.0, "color": (110, 108, 100), "drop": "kanji_stone"},
    MAPLE_LEAF_TILE:    {"name": "Maple Leaf Tile",     "hardness": 1.5, "color": (170,  55,  30), "drop": "maple_leaf_tile"},
    NOREN_PANEL:        {"name": "Noren Panel",         "hardness": 0.5, "color": ( 40,  55, 115), "drop": "noren_panel"},
    TSURU_TILE:         {"name": "Tsuru Tile",          "hardness": 1.5, "color": (215, 215, 215), "drop": "tsuru_tile"},
    PINE_SCREEN_JP:     {"name": "Pine Screen",         "hardness": 1.0, "color": (195, 185, 160), "drop": "pine_screen_jp"},
    KARE_BRIDGE:        {"name": "Kare Bridge",         "hardness": 1.5, "color": (150, 145, 135), "drop": "kare_bridge"},
    # Chinese garden blocks
    PEBBLE_MOSAIC_CN:   {"name": "Pebble Mosaic",       "hardness": 1.5, "color": (145, 138, 125), "drop": "pebble_mosaic_cn"},
    ZIGZAG_BRIDGE:      {"name": "Zigzag Bridge",       "hardness": 2.0, "color": (160, 155, 145), "drop": "zigzag_bridge"},
    CLOUD_WALL:         {"name": "Cloud Wall",          "hardness": 1.5, "color": (240, 238, 230), "drop": "cloud_wall"},
    DRAGON_WALL_CN:     {"name": "Dragon Wall",         "hardness": 2.0, "color": (180,  55,  45), "drop": "dragon_wall_cn"},
    LOTUS_POND:         {"name": "Lotus Pond",          "hardness": 0.5, "color": ( 60, 140, 170), "drop": None},
    HEX_PAVILION_TILE:  {"name": "Hexagonal Pavilion",  "hardness": 1.5, "color": (195, 185, 165), "drop": "hex_pavilion_tile"},
    COMPASS_PAVING:     {"name": "Compass Paving",      "hardness": 2.0, "color": (160, 152, 138), "drop": "compass_paving"},
    WAVE_BALUSTRADE_CN: {"name": "Wave Balustrade",     "hardness": 1.5, "color": (195, 190, 180), "drop": "wave_balustrade_cn"},
    CERAMIC_SEAT:       {"name": "Ceramic Garden Seat", "hardness": 1.5, "color": ( 45,  90, 165), "drop": "ceramic_seat"},
    BONSAI_TRAY:        {"name": "Bonsai Tray",         "hardness": 1.0, "color": (125, 118, 105), "drop": "bonsai_tray"},
    SCHOLAR_SCREEN:     {"name": "Scholar Screen",      "hardness": 1.0, "color": (155, 148, 135), "drop": "scholar_screen"},
    CHRYSANTHEMUM_TILE: {"name": "Chrysanthemum Tile",  "hardness": 1.5, "color": (210, 185,  55), "drop": "chrysanthemum_tile"},
    PLUM_BLOSSOM_TILE:  {"name": "Plum Blossom Tile",   "hardness": 1.5, "color": (210, 155, 175), "drop": "plum_blossom_tile"},
    MOON_PAVEMENT:      {"name": "Moon Pavement",       "hardness": 1.5, "color": (175, 168, 155), "drop": "moon_pavement"},
    BAMBOO_GROVE:       {"name": "Bamboo Grove",        "hardness": 0.5, "color": ( 90, 145,  55), "drop": "bamboo_grove"},
    OSMANTHUS_BUSH:     {"name": "Osmanthus Bush",      "hardness": 0.5, "color": ( 50, 110,  45), "drop": "osmanthus_bush"},
    WATER_LILY_TILE:    {"name": "Water Lily",          "hardness": 0.5, "color": ( 50, 125, 155), "drop": None},
    KOI_POND:           {"name": "Koi Pond",            "hardness": 0.5, "color": ( 55, 130, 170), "drop": None},
    LAKESIDE_ROCK:      {"name": "Lakeside Rock",       "hardness": 2.0, "color": (100,  96,  88), "drop": "lakeside_rock"},
    CLOUD_COLLAR_TILE:  {"name": "Cloud Collar Tile",   "hardness": 1.5, "color": (180, 172, 158), "drop": "cloud_collar_tile"},
    IMPERIAL_PAVING:    {"name": "Imperial Paving",     "hardness": 2.5, "color": (165, 158, 145), "drop": "imperial_paving"},
    PAVILION_COLUMN_CN: {"name": "Pavilion Column",     "hardness": 1.5, "color": (175,  45,  40), "drop": "pavilion_column_cn"},
    EIGHT_DIAGRAM:      {"name": "Eight Diagram",       "hardness": 2.0, "color": (105,  98,  88), "drop": "eight_diagram"},
    TEA_HOUSE_STEP:     {"name": "Teahouse Step",       "hardness": 1.5, "color": (140, 135, 125), "drop": "tea_house_step"},
    LANTERN_FESTIVAL:   {"name": "Lantern Festival",    "hardness": 0.5, "color": (195,  40,  40), "drop": "lantern_festival"},
    # Renaissance garden blocks
    IONIC_COLUMN_BASE:   {"name": "Ionic Column",        "hardness": 2.5, "color": (210, 205, 195), "drop": "ionic_column_base"},
    DORIC_ENTABLATURE:   {"name": "Doric Entablature",   "hardness": 2.0, "color": (200, 195, 182), "drop": "doric_entablature"},
    RUSTICATED_BASE:     {"name": "Rusticated Base",     "hardness": 2.5, "color": (170, 163, 150), "drop": "rusticated_base"},
    GARDEN_LOGGIA:       {"name": "Garden Loggia",       "hardness": 2.0, "color": (195, 188, 175), "drop": "garden_loggia"},
    TRIUMPHAL_ARCH_R:    {"name": "Triumphal Arch",      "hardness": 2.5, "color": (185, 178, 163), "drop": "triumphal_arch_r"},
    EXEDRA_SEAT:         {"name": "Exedra Seat",         "hardness": 2.0, "color": (190, 183, 170), "drop": "exedra_seat"},
    HERM_PILLAR:         {"name": "Herm Pillar",         "hardness": 2.0, "color": (180, 173, 160), "drop": "herm_pillar"},
    NYMPHAEUM_PANEL:     {"name": "Nymphaeum Panel",     "hardness": 1.5, "color": (160, 168, 148), "drop": "nymphaeum_panel"},
    GROTTO_STONE:        {"name": "Grotto Stone",        "hardness": 1.5, "color": ( 98,  96,  88), "drop": "grotto_stone"},
    AMPHITHEATER_TIER:   {"name": "Amphitheater Tier",   "hardness": 1.5, "color": ( 55, 100,  48), "drop": "amphitheater_tier"},
    GIOCHI_ACQUA:        {"name": "Giochi d'Acqua",      "hardness": 1.0, "color": ( 80, 160, 210), "drop": "giochi_acqua"},
    RILL_BLOCK:          {"name": "Garden Rill",         "hardness": 1.0, "color": ( 90, 165, 215), "drop": "rill_block"},
    CASCADE_BLOCK:       {"name": "Water Cascade",       "hardness": 1.5, "color": (150, 165, 175), "drop": "cascade_block"},
    GROTTO_POOL:         {"name": "Grotto Pool",         "hardness": 0.5, "color": ( 50, 100, 110), "drop": None},
    WALL_FOUNTAIN:       {"name": "Wall Fountain",       "hardness": 2.0, "color": (175, 168, 155), "drop": "wall_fountain"},
    BASIN_SURROUND:      {"name": "Basin Surround",      "hardness": 2.0, "color": (190, 183, 170), "drop": "basin_surround"},
    CANAL_BLOCK:         {"name": "Formal Canal",        "hardness": 0.5, "color": ( 60, 130, 180), "drop": None},
    TERME_POOL:          {"name": "Terme Pool",          "hardness": 0.5, "color": ( 70, 145, 175), "drop": None},
    PARTERRE_BRODERIE:   {"name": "Broderie Parterre",   "hardness": 0.5, "color": ( 48,  95,  42), "drop": "parterre_broderie"},
    PARTERRE_COMPARTMENT:{"name": "Parterre Bed",        "hardness": 0.5, "color": ( 55, 105,  48), "drop": "parterre_compartment"},
    ALLEE_TREE:          {"name": "Allée Tree",          "hardness": 1.0, "color": ( 40,  90,  40), "drop": "allee_tree"},
    PLEACHED_HEDGE:      {"name": "Pleached Hedge",      "hardness": 1.0, "color": ( 45,  95,  42), "drop": "pleached_hedge"},
    ESPALIER_WALL:       {"name": "Espalier Wall",       "hardness": 1.0, "color": ( 90, 120,  60), "drop": "espalier_wall"},
    KNOT_GARDEN:         {"name": "Knot Garden",         "hardness": 0.5, "color": ( 50, 100,  45), "drop": "knot_garden"},
    TURF_THEATER:        {"name": "Turf Theater",        "hardness": 0.5, "color": ( 60, 115,  50), "drop": "turf_theater"},
    CARPET_BED:          {"name": "Carpet Bedding",      "hardness": 0.5, "color": (185,  75,  55), "drop": "carpet_bed"},
    OPUS_SECTILE:        {"name": "Opus Sectile",        "hardness": 2.0, "color": (195, 175, 140), "drop": "opus_sectile"},
    TRAVERTINE_FLOOR:    {"name": "Travertine Floor",    "hardness": 1.5, "color": (210, 200, 182), "drop": "travertine_floor"},
    HERRINGBONE_GARDEN:  {"name": "Herringbone Path",    "hardness": 1.0, "color": (175,  88,  55), "drop": "herringbone_garden"},
    RAMP_STONE:          {"name": "Stone Ramp",          "hardness": 1.5, "color": (175, 168, 155), "drop": "ramp_stone"},
    GARDEN_STEPS:        {"name": "Garden Steps",        "hardness": 2.0, "color": (185, 178, 165), "drop": "garden_steps"},
    SAND_ALLEE:          {"name": "Sand Allée",          "hardness": 0.5, "color": (215, 205, 185), "drop": "sand_allee"},
    PATTERNED_PAVEMENT:  {"name": "Patterned Pavement",  "hardness": 2.0, "color": (160, 145, 120), "drop": "patterned_pavement"},
    INLAID_MARBLE:       {"name": "Inlaid Marble",       "hardness": 2.0, "color": (215, 205, 190), "drop": "inlaid_marble"},
    TALL_SUNDIAL:        {"name": "Tall Sundial",        "hardness": 1.5, "color": (165, 158, 145), "drop": "tall_sundial"},
    STONE_VASE:          {"name": "Stone Vase",          "hardness": 1.5, "color": (185, 178, 165), "drop": "stone_vase"},
    STONE_SPHERE:        {"name": "Stone Sphere",        "hardness": 1.5, "color": (180, 173, 162), "drop": "stone_sphere"},
    CURVED_BENCH:        {"name": "Curved Bench",        "hardness": 2.0, "color": (175, 168, 155), "drop": "curved_bench"},
    ORNATE_GATE:         {"name": "Ornate Gate",         "hardness": 1.5, "color": ( 48,  52,  56), "drop": "ornate_gate"},
    LEAD_PLANTER:        {"name": "Lead Planter",        "hardness": 1.5, "color": (100, 105, 108), "drop": "lead_planter"},
    TERRACE_URN:         {"name": "Terrace Urn",         "hardness": 1.5, "color": (185, 178, 165), "drop": "terrace_urn"},
    STONE_PINEAPPLE:     {"name": "Stone Pineapple",     "hardness": 1.5, "color": (175, 170, 155), "drop": "stone_pineapple"},
    GROTTO_ARCH:         {"name": "Grotto Arch",         "hardness": 2.0, "color": ( 95,  92,  84), "drop": "grotto_arch"},
    PERGOLA_BEAM:        {"name": "Pergola Beam",        "hardness": 1.0, "color": (135,  95,  50), "drop": "pergola_beam"},
    LOGGIA_ARCH:         {"name": "Loggia Arch",         "hardness": 2.0, "color": (195, 188, 175), "drop": "loggia_arch"},
    GARDEN_WALL_NICHE:   {"name": "Wall Niche",          "hardness": 2.0, "color": (180, 173, 160), "drop": "garden_wall_niche"},
    ORANGERY_WINDOW:     {"name": "Orangery Window",     "hardness": 1.5, "color": (180, 175, 165), "drop": "orangery_window"},
    BELVEDERE_PANEL:     {"name": "Belvedere Panel",     "hardness": 2.0, "color": (190, 183, 170), "drop": "belvedere_panel"},
    BOSCO_TREE:          {"name": "Bosco Tree",          "hardness": 1.0, "color": ( 42,  80,  38), "drop": "bosco_tree"},
    GIARDINO_SEGRETO:    {"name": "Secret Garden Wall",  "hardness": 2.0, "color": ( 88, 108,  68), "drop": "giardino_segreto"},

    # Rare sculptable stone veins
    MARBLE_VEIN:    {"name": "Marble Vein",    "hardness": 2.5, "color": (235, 232, 222), "drop": "marble_chunk",    "drop_chance": 1.0},
    ALABASTER_VEIN: {"name": "Alabaster Vein", "hardness": 2.0, "color": (232, 218, 198), "drop": "alabaster_chunk", "drop_chance": 1.0},
    VERDITE_VEIN:   {"name": "Verdite Vein",   "hardness": 2.5, "color": ( 38, 105,  58), "drop": "verdite_slab",    "drop_chance": 1.0},
    ONYX_VEIN:      {"name": "Onyx Vein",      "hardness": 3.0, "color": ( 28,  22,  38), "drop": "onyx_slab",       "drop_chance": 1.0},

    # Placed forms of the rare stones
    ALABASTER_BLOCK: {"name": "Alabaster",  "hardness": 2.0, "color": (235, 222, 204), "drop": "alabaster_chunk"},
    VERDITE_BLOCK:   {"name": "Verdite",    "hardness": 2.5, "color": ( 42, 108,  62), "drop": "verdite_slab"},
    ONYX_BLOCK:      {"name": "Onyx",       "hardness": 3.0, "color": ( 30,  24,  40), "drop": "onyx_slab"},
    # Renaissance palace blocks
    PIETRA_SERENA:        {"name": "Pietra Serena",        "hardness": 2.5, "color": (155, 160, 172), "drop": "pietra_serena"},
    TRAVERTINE_WALL:      {"name": "Travertine Wall",      "hardness": 2.0, "color": (215, 205, 185), "drop": "travertine_wall"},
    MARBLE_FACADE:        {"name": "Marble Facade",        "hardness": 2.5, "color": (242, 240, 236), "drop": "marble_facade"},
    RUSTICATED_QUOIN:     {"name": "Rusticated Quoin",     "hardness": 2.5, "color": (178, 172, 158), "drop": "rusticated_quoin"},
    BICOLOR_MARBLE:       {"name": "Bicolor Marble",       "hardness": 2.5, "color": (228, 225, 218), "drop": "bicolor_marble"},
    PINK_GRANITE_BASE:    {"name": "Pink Granite Base",    "hardness": 3.0, "color": (190, 168, 162), "drop": "pink_granite_base"},
    BLIND_ARCH:           {"name": "Blind Arch",           "hardness": 2.0, "color": (205, 200, 188), "drop": "blind_arch"},
    CONSOLE_CORNICE:      {"name": "Console Cornice",      "hardness": 2.0, "color": (215, 208, 195), "drop": "console_cornice"},
    CORINTHIAN_CAPITAL:   {"name": "Corinthian Capital",   "hardness": 2.5, "color": (218, 212, 198), "drop": "corinthian_capital"},
    GIANT_PILASTER:       {"name": "Giant Pilaster",       "hardness": 2.0, "color": (210, 205, 195), "drop": "giant_pilaster"},
    ENGAGED_COLUMN:       {"name": "Engaged Column",       "hardness": 2.5, "color": (222, 218, 208), "drop": "engaged_column"},
    ATLAS_FIGURE:         {"name": "Atlas Figure",         "hardness": 3.0, "color": (195, 185, 170), "drop": "atlas_figure"},
    CARYATID_COLUMN:      {"name": "Caryatid Column",      "hardness": 3.0, "color": (215, 208, 195), "drop": "caryatid_column"},
    COMPOSITE_CAPITAL:    {"name": "Composite Capital",    "hardness": 2.5, "color": (218, 212, 198), "drop": "composite_capital"},
    INTARSIA_PANEL:       {"name": "Intarsia Panel",       "hardness": 1.5, "color": (155, 112,  65), "drop": "intarsia_panel"},
    STUDIOLO_WALL:        {"name": "Studiolo Wall",        "hardness": 1.5, "color": (142, 105,  58), "drop": "studiolo_wall"},
    GILT_LEATHER:         {"name": "Gilt Leather Wall",    "hardness": 1.0, "color": (148, 105,  40), "drop": "gilt_leather"},
    FRESCO_LUNETTE:       {"name": "Fresco Lunette",       "hardness": 1.5, "color": (175, 165, 145), "drop": "fresco_lunette"},
    WAINSCOT_MARBLE:      {"name": "Marble Wainscoting",   "hardness": 2.0, "color": (218, 195, 185), "drop": "wainscot_marble"},
    TAPESTRY_FRAME:       {"name": "Tapestry Frame",       "hardness": 1.5, "color": (175, 145,  65), "drop": "tapestry_frame"},
    LACUNAR_CEILING:      {"name": "Lacunar Ceiling",      "hardness": 2.0, "color": (195, 188, 172), "drop": "lacunar_ceiling"},
    BARREL_FRESCO:        {"name": "Barrel Vault Fresco",  "hardness": 1.5, "color": (175, 178, 195), "drop": "barrel_fresco"},
    GOLDEN_CEILING:       {"name": "Golden Ceiling",       "hardness": 1.5, "color": (215, 188,  95), "drop": "golden_ceiling"},
    GROTESQUE_VAULT:      {"name": "Grotesque Vault",      "hardness": 1.5, "color": (185, 182, 175), "drop": "grotesque_vault"},
    CUPOLA_OCULUS:        {"name": "Cupola Oculus",        "hardness": 1.5, "color": (148, 168, 200), "drop": "cupola_oculus"},
    COSMATESQUE_FLOOR:    {"name": "Cosmatesque Floor",    "hardness": 2.5, "color": (188, 168, 142), "drop": "cosmatesque_floor"},
    TERRAZZO_FLOOR_REN:   {"name": "Terrazzo Floor",       "hardness": 2.0, "color": (198, 188, 178), "drop": "terrazzo_floor_ren"},
    OPUS_ALEXANDRINUM:    {"name": "Opus Alexandrinum",    "hardness": 3.0, "color": (145, 105, 110), "drop": "opus_alexandrinum"},
    MARBLE_MEDALLION_REN: {"name": "Marble Medallion",     "hardness": 2.5, "color": (215, 208, 200), "drop": "marble_medallion_ren"},
    PALACE_FLOOR_TILE:    {"name": "Palace Floor Tile",    "hardness": 2.0, "color": (200, 192, 180), "drop": "palace_floor_tile"},
    PALACE_PORTAL:        {"name": "Palace Portal",        "hardness": 2.5, "color": (185, 178, 162), "drop": "palace_portal"},
    AEDICULE_FRAME:       {"name": "Aedicule Frame",       "hardness": 2.5, "color": (195, 188, 175), "drop": "aedicule_frame"},
    THERMAL_WINDOW:       {"name": "Thermal Window",       "hardness": 1.5, "color": (195, 205, 215), "drop": "thermal_window"},
    BIFORA_WINDOW:        {"name": "Bifora Window",        "hardness": 1.5, "color": (198, 195, 185), "drop": "bifora_window"},
    SERLIANA_WINDOW:      {"name": "Serliana Window",      "hardness": 1.5, "color": (198, 192, 180), "drop": "serliana_window"},
    PALAZZO_BALCONY:      {"name": "Palazzo Balcony",      "hardness": 2.0, "color": (185, 178, 165), "drop": "palazzo_balcony"},
    ROMAN_ARCH_REN:       {"name": "Roman Arch",           "hardness": 2.5, "color": (195, 188, 175), "drop": "roman_arch_ren"},
    BARREL_VAULT_COFFER:  {"name": "Barrel Vault Coffer",  "hardness": 2.0, "color": (188, 182, 168), "drop": "barrel_vault_coffer"},
    PENDENTIVE_BLOCK:     {"name": "Pendentive",           "hardness": 2.0, "color": (205, 198, 185), "drop": "pendentive_block"},
    GROIN_VAULT:          {"name": "Groin Vault",          "hardness": 2.0, "color": (192, 188, 178), "drop": "groin_vault"},
    RENAISSANCE_MANTEL:   {"name": "Renaissance Mantel",   "hardness": 2.5, "color": (225, 220, 215), "drop": "renaissance_mantel"},
    CHIMNEY_BREAST_REN:   {"name": "Chimney Breast",       "hardness": 2.0, "color": (190, 185, 175), "drop": "chimney_breast_ren"},
    PEDIMENTED_NICHE:     {"name": "Pedimented Niche",     "hardness": 2.0, "color": (198, 192, 180), "drop": "pedimented_niche"},
    SHELL_NICHE_REN:      {"name": "Shell Niche",          "hardness": 2.0, "color": (200, 195, 185), "drop": "shell_niche_ren"},
    CARTOUCHE_REN:        {"name": "Cartouche",            "hardness": 2.0, "color": (215, 208, 195), "drop": "cartouche_ren"},
    PUTTI_FRIEZE:         {"name": "Putti Frieze",         "hardness": 2.0, "color": (210, 205, 195), "drop": "putti_frieze"},
    FESTOON_PANEL:        {"name": "Festoon Panel",        "hardness": 1.5, "color": (195, 188, 172), "drop": "festoon_panel"},
    TROPHY_PANEL_REN:     {"name": "Trophy Panel",         "hardness": 2.0, "color": (185, 178, 165), "drop": "trophy_panel_ren"},
    MEDALLION_PORTRAIT:   {"name": "Portrait Medallion",   "hardness": 2.0, "color": (205, 200, 188), "drop": "medallion_portrait"},
    LAUREL_FRIEZE:        {"name": "Laurel Frieze",        "hardness": 2.0, "color": (175, 188, 162), "drop": "laurel_frieze"},
    # --- Pottery & Ceramics ---
    POTTERY_WHEEL_BLOCK:  {"name": "Pottery Wheel",        "hardness": 3,   "color": (130,  95, 65),  "drop": "pottery_wheel_item"},
    POTTERY_KILN_BLOCK:   {"name": "Pottery Kiln",         "hardness": 3,   "color": ( 80,  60, 50),  "drop": "pottery_kiln_item"},
    # --- Portuguese / Spanish Ceramic Tiles ---
    CALCADA_PORTUGUESA:   {"name": "Calçada Portuguesa",   "hardness": 2,   "color": ( 30,  28,  26), "drop": "calcada_portuguesa"},
    AZULEJO_GEOMETRIC:    {"name": "Azulejo Geometric",    "hardness": 2,   "color": (245, 242, 235), "drop": "azulejo_geometric"},
    PAINTED_TILE_BORDER:  {"name": "Painted Tile Border",  "hardness": 2,   "color": (245, 240, 225), "drop": "painted_tile_border"},
    SPANISH_MAJOLICA:     {"name": "Spanish Majolica",     "hardness": 2,   "color": (242, 238, 218), "drop": "spanish_majolica"},
    AZULEJO_STAIR:        {"name": "Azulejo Stair",        "hardness": 2,   "color": (245, 242, 235), "drop": "azulejo_stair"},
    PORTUGUESE_PINK_MARBLE: {"name": "Portuguese Pink Marble", "hardness": 2, "color": (220, 175, 175), "drop": "portuguese_pink_marble"},
    SPANISH_HEX_TILE:       {"name": "Spanish Hex Tile",       "hardness": 2, "color": ( 22,  20,  18), "drop": "spanish_hex_tile"},
    MUDEJAR_STAR_TILE:      {"name": "Mudéjar Star Tile",      "hardness": 2, "color": (245, 238, 215), "drop": "mudejar_star_tile"},
    ALBARRADA_PANEL:        {"name": "Albarrada Panel",        "hardness": 2, "color": (245, 242, 238), "drop": "albarrada_panel"},
    SGRAFFITO_WALL:         {"name": "Sgraffito Wall",         "hardness": 2, "color": (225, 218, 200), "drop": "sgraffito_wall"},
    TRENCADIS_PANEL:        {"name": "Trencadís Panel",        "hardness": 2, "color": (185, 183, 178), "drop": "trencadis_panel"},
    AZULEJO_NAVY:           {"name": "Azulejo Navy",           "hardness": 2, "color": ( 28,  52, 120), "drop": "azulejo_navy"},
    AZULEJO_MANGANESE:      {"name": "Azulejo Manganese",      "hardness": 2, "color": (238, 235, 228), "drop": "azulejo_manganese"},
    PLATERESQUE_PANEL:      {"name": "Plateresque Panel",      "hardness": 2, "color": (205, 195, 175), "drop": "plateresque_panel"},
    AZULEJO_CORNICE:        {"name": "Azulejo Cornice",        "hardness": 2, "color": (245, 242, 235), "drop": "azulejo_cornice"},
    TALAVERA_FOUNTAIN:      {"name": "Talavera Fountain",      "hardness": 2, "color": (235, 240, 248), "drop": "talavera_fountain"},
    BARCELONA_TILE:         {"name": "Barcelona Tile",         "hardness": 2, "color": (195, 185, 120), "drop": "barcelona_tile"},
    MOORISH_ARCHWAY_TILE:   {"name": "Moorish Archway Tile",   "hardness": 2, "color": (205, 195, 175), "drop": "moorish_archway_tile"},
    PORTUGUESE_CHIMNEY:     {"name": "Portuguese Chimney",     "hardness": 2, "color": (190, 105,  65), "drop": "portuguese_chimney"},
    BARCELOS_TILE:          {"name": "Barcelos Tile",          "hardness": 2, "color": (242, 238, 222), "drop": "barcelos_tile"},
    REJA_PANEL:             {"name": "Reja Panel",             "hardness": 2, "color": (225, 218, 205), "drop": "reja_panel"},
    ORANGE_TREE_PLANTER:    {"name": "Orange Tree Planter",    "hardness": 1, "color": (242, 235, 218), "drop": "orange_tree_planter"},
    WAVE_COBBLE:            {"name": "Wave Cobble",            "hardness": 2, "color": (195, 192, 182), "drop": "wave_cobble"},
    AZULEJO_FACADE_PANEL:   {"name": "Azulejo Facade Panel",   "hardness": 2, "color": (243, 241, 238), "drop": "azulejo_facade_panel"},
    MUDEJAR_BRICK:          {"name": "Mudéjar Brick",          "hardness": 2, "color": (185, 105,  60), "drop": "mudejar_brick"},
    PORTUGUESE_BENCH:       {"name": "Portuguese Bench",       "hardness": 2, "color": (180, 172, 158), "drop": "portuguese_bench"},
    SPANISH_PATIO_FLOOR:    {"name": "Spanish Patio Floor",    "hardness": 2, "color": (215, 205, 185), "drop": "spanish_patio_floor"},
    ARABIC_ROOF_TILE:       {"name": "Arabic Roof Tile",       "hardness": 2, "color": (190, 105,  65), "drop": "arabic_roof_tile"},
    MOORISH_COLUMN_TILE:    {"name": "Moorish Column Tile",    "hardness": 2, "color": ( 35,  32,  30), "drop": "moorish_column_tile"},
    ESTREMOZ_MARBLE:        {"name": "Estremoz Marble",        "hardness": 2, "color": (240, 235, 230), "drop": "estremoz_marble"},
    # --- Córdoba / Umayyad Architecture ---
    MEZQUITA_ARCH:          {"name": "Mezquita Arch",          "hardness": 2, "color": (195,  65,  45), "drop": "mezquita_arch"},
    MIHRAB_TILE:            {"name": "Mihrab Tile",            "hardness": 2, "color": (200, 162,  50), "drop": "mihrab_tile"},
    MEDINA_AZAHARA_STONE:   {"name": "Medina Azahara Stone",   "hardness": 2, "color": (235, 230, 218), "drop": "medina_azahara_stone"},
    CORDOBA_COLUMN:         {"name": "Córdoba Column",         "hardness": 2, "color": (230, 225, 215), "drop": "cordoba_column"},
    ORANGE_COURT_FLOOR:     {"name": "Orange Court Floor",     "hardness": 2, "color": (210, 200, 178), "drop": "orange_court_floor"},
    CORDOBAN_LEATHER:       {"name": "Cordoban Leather",       "hardness": 1, "color": (135,  72,  30), "drop": "cordoban_leather"},
    UMAYYAD_MULTILOBED:     {"name": "Umayyad Multilobed Arch","hardness": 2, "color": (215, 208, 192), "drop": "umayyad_multilobed"},
    GOLD_TESSERA_PANEL:     {"name": "Gold Tessera Panel",     "hardness": 2, "color": (205, 165,  45), "drop": "gold_tessera_panel"},
    UMAYYAD_DOME_RIB:       {"name": "Umayyad Dome Rib",       "hardness": 2, "color": (215, 210, 198), "drop": "umayyad_dome_rib"},
    KUFIC_PANEL:            {"name": "Kufic Panel",            "hardness": 2, "color": (210, 202, 185), "drop": "kufic_panel"},
    PATIO_FLOWER_WALL:      {"name": "Patio Flower Wall",      "hardness": 2, "color": (245, 243, 238), "drop": "patio_flower_wall"},
    CORDOBAN_PATIO_TILE:    {"name": "Cordoban Patio Tile",    "hardness": 2, "color": (225, 218, 198), "drop": "cordoban_patio_tile"},
    STAR_VAULT_PANEL:       {"name": "Star Vault Panel",       "hardness": 2, "color": (195, 188, 172), "drop": "star_vault_panel"},
    ANDALUSIAN_FOUNTAIN:    {"name": "Andalusian Fountain",    "hardness": 2, "color": ( 65, 140, 190), "drop": "andalusian_fountain"},
    NASRID_HONEYCOMB:       {"name": "Nasrid Honeycomb",       "hardness": 2, "color": (215, 205, 182), "drop": "nasrid_honeycomb"},
    POTTERY_DISPLAY_BLOCK:  {"name": "Pottery Display",        "hardness": 1, "color": None,           "drop": "pottery_display"},
    # --- Medieval Castle ---
    PORTCULLIS_BLOCK:   {"name": "Portcullis",          "hardness": 3, "color": ( 48,  44,  40), "drop": "portcullis_block"},
    ARROW_LOOP:         {"name": "Arrow Loop",          "hardness": 3, "color": (155, 148, 136), "drop": "arrow_loop"},
    MACHICOLATION:      {"name": "Machicolation",       "hardness": 3, "color": (162, 155, 142), "drop": "machicolation"},
    DRAWBRIDGE_PLANK:   {"name": "Drawbridge Plank",    "hardness": 2, "color": ( 80,  55,  30), "drop": "drawbridge_plank"},
    ROUND_TOWER_WALL:   {"name": "Round Tower Wall",    "hardness": 3, "color": (158, 150, 138), "drop": "round_tower_wall"},
    CURTAIN_WALL:       {"name": "Curtain Wall",        "hardness": 3, "color": (148, 140, 128), "drop": "curtain_wall"},
    CORBEL_COURSE:      {"name": "Corbel Course",       "hardness": 3, "color": (165, 158, 145), "drop": "corbel_course"},
    TOWER_CAP:          {"name": "Tower Cap",           "hardness": 2, "color": ( 72,  80,  88), "drop": "tower_cap"},
    GREAT_HALL_FLOOR:   {"name": "Great Hall Floor",    "hardness": 2, "color": (185, 178, 162), "drop": "great_hall_floor"},
    DUNGEON_WALL:       {"name": "Dungeon Wall",        "hardness": 3, "color": ( 88,  82,  72), "drop": "dungeon_wall"},
    CASTLE_FIREPLACE:   {"name": "Castle Fireplace",    "hardness": 2, "color": (145, 136, 122), "drop": "castle_fireplace"},
    HERALDIC_PANEL:     {"name": "Heraldic Panel",      "hardness": 2, "color": (175, 168, 152), "drop": "heraldic_panel"},
    WALL_WALK_FLOOR:    {"name": "Wall-Walk Floor",     "hardness": 2, "color": (172, 165, 150), "drop": "wall_walk_floor"},
    CASTLE_GATE_ARCH:   {"name": "Castle Gate Arch",    "hardness": 3, "color": (152, 145, 132), "drop": "castle_gate_arch"},
    DRAWBRIDGE_CHAIN:   {"name": "Drawbridge Chain",    "hardness": 2, "color": ( 52,  48,  44), "drop": "drawbridge_chain"},
    DUNGEON_GRATE:      {"name": "Dungeon Grate",       "hardness": 2, "color": ( 45,  42,  38), "drop": "dungeon_grate"},
    MOAT_STONE:         {"name": "Moat Stone",          "hardness": 2, "color": ( 78,  92,  72), "drop": "moat_stone"},
    CHAPEL_STONE:       {"name": "Chapel Stone",        "hardness": 2, "color": (198, 192, 178), "drop": "chapel_stone"},
    MURDER_HOLE:        {"name": "Murder Hole",         "hardness": 3, "color": ( 55,  50,  45), "drop": "murder_hole"},
    GARDEROBE_CHUTE:    {"name": "Garderobe Chute",     "hardness": 2, "color": (148, 140, 125), "drop": "garderobe_chute"},
    # --- Mid-Century Modern ---
    MCM_CONCRETE_PANEL:   {"name": "Concrete Panel",      "hardness": 2, "color": (178, 174, 168), "drop": "mcm_concrete_panel"},
    MCM_BREEZE_BLOCK:     {"name": "Breeze Block",        "hardness": 2, "color": (192, 188, 182), "drop": "mcm_breeze_block"},
    MCM_BOARD_BATTEN:     {"name": "Board and Batten",    "hardness": 2, "color": (148, 108,  65), "drop": "mcm_board_batten"},
    MCM_WALNUT_PANEL:     {"name": "Walnut Panel",        "hardness": 2, "color": ( 88,  55,  28), "drop": "mcm_walnut_panel"},
    MCM_TEAK_PANEL:       {"name": "Teak Panel",          "hardness": 2, "color": (148,  95,  48), "drop": "mcm_teak_panel"},
    MCM_ROMAN_BRICK:      {"name": "Roman Brick",         "hardness": 2, "color": (185, 105,  68), "drop": "mcm_roman_brick"},
    TERRAZZO_FLOOR_MCM:   {"name": "Terrazzo Floor",      "hardness": 2, "color": (210, 208, 204), "drop": "terrazzo_floor_mcm"},
    TRAVERTINE_FLOOR_MCM: {"name": "Travertine Floor",    "hardness": 2, "color": (222, 215, 192), "drop": "travertine_floor_mcm"},
    QUARRY_TILE:          {"name": "Quarry Tile",         "hardness": 2, "color": (178,  82,  55), "drop": "quarry_tile"},
    FLAGSTONE_PATIO:      {"name": "Flagstone Patio",     "hardness": 2, "color": (148, 144, 136), "drop": "flagstone_patio"},
    MCM_PARQUET:          {"name": "Parquet Floor",       "hardness": 2, "color": (138,  90,  45), "drop": "mcm_parquet"},
    CORK_FLOOR_TILE:      {"name": "Cork Floor Tile",     "hardness": 2, "color": (175, 138,  80), "drop": "cork_floor_tile"},
    AVOCADO_TILE:         {"name": "Avocado Tile",        "hardness": 2, "color": (105, 128,  72), "drop": "avocado_tile"},
    HARVEST_GOLD_TILE:    {"name": "Harvest Gold Tile",   "hardness": 2, "color": (215, 165,  42), "drop": "harvest_gold_tile"},
    BURNT_ORANGE_TILE:    {"name": "Burnt Orange Tile",   "hardness": 2, "color": (195,  85,  35), "drop": "burnt_orange_tile"},
    TURQUOISE_TILE:       {"name": "Turquoise Tile",      "hardness": 2, "color": ( 50, 160, 172), "drop": "turquoise_tile"},
    PLATE_GLASS_PANEL:    {"name": "Plate Glass Panel",   "hardness": 1, "color": (185, 215, 228), "drop": "plate_glass_panel"},
    TINTED_GLASS_PANEL:   {"name": "Tinted Glass Panel",  "hardness": 1, "color": ( 42,  50,  56), "drop": "tinted_glass_panel"},
    RIBBED_GLASS_MCM:     {"name": "Ribbed Glass",        "hardness": 1, "color": (208, 218, 224), "drop": "ribbed_glass_mcm"},
    BRASS_TRIM_PANEL:     {"name": "Brass Trim Panel",    "hardness": 2, "color": (188, 152,  65), "drop": "brass_trim_panel"},
    COPPER_SCREEN_MCM:    {"name": "Copper Screen",       "hardness": 2, "color": ( 85, 148, 115), "drop": "copper_screen_mcm"},
    ANODIZED_ALUMINUM:    {"name": "Anodized Aluminum",   "hardness": 2, "color": (178, 182, 190), "drop": "anodized_aluminum"},
    RATTAN_SCREEN_MCM:    {"name": "Rattan Screen",       "hardness": 2, "color": (188, 152,  95), "drop": "rattan_screen_mcm"},
    SPLIT_BAMBOO_PANEL:   {"name": "Split Bamboo Panel",  "hardness": 2, "color": (172, 182, 118), "drop": "split_bamboo_panel"},
    LAVA_ROCK_WALL:       {"name": "Lava Rock Wall",      "hardness": 3, "color": ( 48,  42,  40), "drop": "lava_rock_wall"},
    MCM_TONGUE_GROOVE:    {"name": "Tongue and Groove",   "hardness": 2, "color": (218, 185, 128), "drop": "mcm_tongue_groove"},
    BUTTERFLY_BEAM:       {"name": "Butterfly Beam",      "hardness": 2, "color": (112,  72,  38), "drop": "butterfly_beam"},
    STARBURST_PANEL:      {"name": "Starburst Panel",     "hardness": 2, "color": (225, 215, 182), "drop": "starburst_panel"},
    STACKED_STONE_VENEER: {"name": "Stacked Stone Veneer","hardness": 2, "color": (155, 148, 136), "drop": "stacked_stone_veneer"},
    FIBERGLASS_SHELL:     {"name": "Fiberglass Shell",    "hardness": 1, "color": (228, 218, 198), "drop": "fiberglass_shell"},
    # --- Gardening blocks ---
    ORNAMENTAL_GRASS:    {"name": "Ornamental Grass",    "hardness": 0.5, "color": (165, 175,  80), "drop": "ornamental_grass"},
    FLOWERING_SHRUB:     {"name": "Flowering Shrub",     "hardness": 0.5, "color": ( 55, 110,  50), "drop": "flowering_shrub"},
    HOLLY_SHRUB:         {"name": "Holly Shrub",         "hardness": 0.5, "color": ( 35,  80,  40), "drop": "holly_shrub"},
    TOPIARY_PEACOCK:     {"name": "Topiary Peacock",     "hardness": 1.0, "color": ( 42, 100,  48), "drop": "topiary_peacock"},
    TOPIARY_BEAR:        {"name": "Topiary Bear",        "hardness": 1.0, "color": ( 38,  90,  42), "drop": "topiary_bear"},
    TOPIARY_RABBIT:      {"name": "Topiary Rabbit",      "hardness": 1.0, "color": ( 48, 110,  52), "drop": "topiary_rabbit"},
    ROSE_BED:            {"name": "Rose Bed",            "hardness": 0.5, "color": ( 55,  95,  45), "drop": "rose_bed"},
    TULIP_BED:           {"name": "Tulip Bed",           "hardness": 0.5, "color": ( 60, 105,  50), "drop": "tulip_bed"},
    COTTAGE_GARDEN_BED:  {"name": "Cottage Garden",      "hardness": 0.5, "color": ( 65, 115,  55), "drop": "cottage_garden_bed"},
    CHERUB_FOUNTAIN:     {"name": "Cherub Fountain",     "hardness": 2.0, "color": (185, 178, 162), "drop": "cherub_fountain"},
    LION_HEAD_FOUNTAIN:  {"name": "Lion Head Fountain",  "hardness": 2.0, "color": (175, 165, 148), "drop": "lion_head_fountain"},
    MOSAIC_FOUNTAIN:     {"name": "Mosaic Fountain",     "hardness": 2.0, "color": ( 55, 115, 168), "drop": "mosaic_fountain"},
    LAVENDER_BED:        {"name": "Lavender Bed",        "hardness": 0.5, "color": (150, 110, 195), "drop": "lavender_bed"},
    SUNFLOWER_BED:       {"name": "Sunflower Bed",       "hardness": 0.5, "color": (220, 185,  40), "drop": "sunflower_bed"},
    DAHLIA_BED:          {"name": "Dahlia Bed",          "hardness": 0.5, "color": (195,  70, 120), "drop": "dahlia_bed"},
    TOPIARY_SWAN:        {"name": "Topiary Swan",        "hardness": 1.0, "color": ( 40, 100,  46), "drop": "topiary_swan"},
    TOPIARY_FOX:         {"name": "Topiary Fox",         "hardness": 1.0, "color": ( 36,  88,  40), "drop": "topiary_fox"},
    TOPIARY_ELEPHANT:    {"name": "Topiary Elephant",    "hardness": 1.0, "color": ( 44, 108,  50), "drop": "topiary_elephant"},
    PEONY_BUSH:          {"name": "Peony Bush",          "hardness": 0.5, "color": ( 52, 105,  48), "drop": "peony_bush"},
    FERN_CLUMP:          {"name": "Fern Clump",          "hardness": 0.5, "color": ( 48, 118,  52), "drop": "fern_clump"},
    RAISED_GARDEN_BED:   {"name": "Raised Garden Bed",   "hardness": 1.0, "color": (115,  80,  45), "drop": "raised_garden_bed"},
    LILY_PAD_POND:       {"name": "Lily Pad Pond",       "hardness": 0.5, "color": ( 55, 135,  75), "drop": "lily_pad_pond"},
    BEE_SKEP:            {"name": "Bee Skep",            "hardness": 0.5, "color": (200, 165,  80), "drop": "bee_skep"},
    GARDEN_WHEELBARROW:  {"name": "Garden Wheelbarrow",  "hardness": 1.0, "color": (115,  75,  40), "drop": "garden_wheelbarrow"},
    IRIS_BED:            {"name": "Iris Bed",            "hardness": 0.5, "color": ( 90,  80, 190), "drop": "iris_bed"},
    POPPY_BED:           {"name": "Poppy Bed",           "hardness": 0.5, "color": (210,  45,  45), "drop": "poppy_bed"},
    FOXGLOVE_PATCH:      {"name": "Foxglove Patch",      "hardness": 0.5, "color": (210, 110, 175), "drop": "foxglove_patch"},
    SNOWDROP_PATCH:      {"name": "Snowdrop Patch",      "hardness": 0.5, "color": (235, 238, 242), "drop": "snowdrop_patch"},
    MARIGOLD_BED:        {"name": "Marigold Bed",        "hardness": 0.5, "color": (230, 145,  30), "drop": "marigold_bed"},
    BOXWOOD_BALL:        {"name": "Boxwood Ball",        "hardness": 1.0, "color": ( 50, 100,  44), "drop": "boxwood_ball"},
    RHODODENDRON_BUSH:   {"name": "Rhododendron",        "hardness": 0.5, "color": ( 48, 100,  44), "drop": "rhododendron_bush"},
    BAMBOO_CLUMP:        {"name": "Bamboo Clump",        "hardness": 0.5, "color": ( 88, 148,  58), "drop": "bamboo_clump"},
    AGAPANTHUS_PATCH:    {"name": "Agapanthus",          "hardness": 0.5, "color": ( 60,  90, 185), "drop": "agapanthus_patch"},
    TOPIARY_DRAGON:      {"name": "Topiary Dragon",      "hardness": 1.0, "color": ( 36,  88,  42), "drop": "topiary_dragon"},
    TOPIARY_GIRAFFE:     {"name": "Topiary Giraffe",     "hardness": 1.0, "color": ( 40,  96,  46), "drop": "topiary_giraffe"},
    TOPIARY_HEDGEHOG:    {"name": "Topiary Hedgehog",    "hardness": 1.0, "color": ( 44, 104,  48), "drop": "topiary_hedgehog"},
    BUBBLE_FOUNTAIN:     {"name": "Bubble Fountain",     "hardness": 2.0, "color": (155, 148, 135), "drop": "bubble_fountain"},
    SHELL_FOUNTAIN:      {"name": "Shell Fountain",      "hardness": 2.0, "color": (210, 200, 182), "drop": "shell_fountain"},
    MILLSTONE_FOUNTAIN:  {"name": "Millstone Fountain",  "hardness": 2.0, "color": (165, 158, 142), "drop": "millstone_fountain"},
    TRELLIS_ARCH:        {"name": "Trellis Arch",        "hardness": 1.0, "color": (120,  80,  40), "drop": "trellis_arch"},
    COLD_FRAME:          {"name": "Cold Frame",          "hardness": 1.0, "color": (140,  95,  50), "drop": "cold_frame"},
    GARDEN_SWING:        {"name": "Garden Swing",        "hardness": 1.0, "color": (130,  85,  45), "drop": "garden_swing"},
    WICKER_FENCE:        {"name": "Wicker Fence",        "hardness": 0.5, "color": (175, 135,  70), "drop": "wicker_fence"},
    HANGING_BASKET:      {"name": "Hanging Basket",      "hardness": 0.5, "color": (140,  95,  50), "drop": "hanging_basket"},
    STANDARD_ROSE:       {"name": "Standard Rose",       "hardness": 0.5, "color": ( 55, 105,  48), "drop": "standard_rose"},
    GARDEN_GNOME:        {"name": "Garden Gnome",        "hardness": 0.5, "color": (200,  55,  45), "drop": "garden_gnome"},
    TOPIARY_ARCH:        {"name": "Topiary Arch",        "hardness": 1.0, "color": ( 38,  90,  42), "drop": "topiary_arch"},
    CHAMOMILE_LAWN:      {"name": "Chamomile Lawn",      "hardness": 0.5, "color": (180, 195, 100), "drop": "chamomile_lawn"},
    CREEPING_THYME:      {"name": "Creeping Thyme",      "hardness": 0.5, "color": (145, 110, 180), "drop": "creeping_thyme"},
    HYDRANGEA_BUSH:      {"name": "Hydrangea",           "hardness": 0.5, "color": ( 90, 120, 195), "drop": "hydrangea_bush"},
    ALLIUM_PATCH:        {"name": "Allium Patch",        "hardness": 0.5, "color": (145,  80, 195), "drop": "allium_patch"},
    SWEET_PEA_TRELLIS:   {"name": "Sweet Pea Trellis",   "hardness": 0.5, "color": (215, 130, 185), "drop": "sweet_pea_trellis"},
    BLEEDING_HEART_PATCH:{"name": "Bleeding Heart",      "hardness": 0.5, "color": (210,  80, 130), "drop": "bleeding_heart_patch"},
    ASTILBE_PATCH:       {"name": "Astilbe Patch",       "hardness": 0.5, "color": (210, 100, 145), "drop": "astilbe_patch"},
    WISTERIA_PILLAR:     {"name": "Wisteria Pillar",     "hardness": 1.5, "color": (155, 120, 185), "drop": "wisteria_pillar"},
    TOPIARY_SNAIL:       {"name": "Topiary Snail",       "hardness": 1.0, "color": ( 42, 100,  46), "drop": "topiary_snail"},
    TOPIARY_MUSHROOM:    {"name": "Topiary Mushroom",    "hardness": 1.0, "color": ( 38,  94,  44), "drop": "topiary_mushroom"},
    TOPIARY_OWL:         {"name": "Topiary Owl",         "hardness": 1.0, "color": ( 44, 106,  50), "drop": "topiary_owl"},
    TOPIARY_DINOSAUR:    {"name": "Topiary Dinosaur",    "hardness": 1.0, "color": ( 36,  88,  40), "drop": "topiary_dinosaur"},
    KOI_POOL:            {"name": "Koi Pool",            "hardness": 1.5, "color": ( 45, 110, 160), "drop": "koi_pool"},
    STONE_TROUGH_PLANTER:{"name": "Stone Trough",        "hardness": 2.0, "color": (162, 155, 140), "drop": "stone_trough_planter"},
    RAIN_BARREL:         {"name": "Rain Barrel",         "hardness": 1.0, "color": (105,  65,  35), "drop": "rain_barrel"},
    MOSS_PATCH:          {"name": "Moss Patch",          "hardness": 0.5, "color": ( 60, 120,  50), "drop": "moss_patch"},
    CLOVER_LAWN:         {"name": "Clover Lawn",         "hardness": 0.5, "color": ( 75, 150,  60), "drop": "clover_lawn"},
    BARK_MULCH:          {"name": "Bark Mulch",          "hardness": 0.5, "color": (115,  72,  38), "drop": "bark_mulch"},
    STONE_FROG:          {"name": "Stone Frog",          "hardness": 1.5, "color": (148, 142, 128), "drop": "stone_frog"},
    GARDEN_DOVECOTE:     {"name": "Garden Dovecote",     "hardness": 1.0, "color": (225, 220, 210), "drop": "garden_dovecote"},
    STONE_HEDGEHOG:      {"name": "Stone Hedgehog",      "hardness": 1.5, "color": (150, 144, 130), "drop": "stone_hedgehog"},
    BIRD_TABLE:          {"name": "Bird Table",          "hardness": 1.0, "color": (130,  85,  45), "drop": "bird_table"},
    GARDEN_CLOCK:        {"name": "Garden Clock",        "hardness": 1.5, "color": ( 72, 118,  90), "drop": "garden_clock"},
    GARDEN_OBELISK_METAL:{"name": "Iron Obelisk",        "hardness": 2.0, "color": ( 52,  55,  58), "drop": "garden_obelisk_metal"},
    POTTING_TABLE:       {"name": "Potting Table",       "hardness": 1.0, "color": (125,  82,  42), "drop": "potting_table"},
    COMPOST_HEAP:        {"name": "Compost Heap",        "hardness": 0.5, "color": ( 75,  50,  25), "drop": "compost_heap"},
    GARDEN_TOAD_HOUSE:   {"name": "Toad House",          "hardness": 0.5, "color": (185, 130,  75), "drop": "garden_toad_house"},
    TRADE_BLOCK:         {"name": "Trade Post",          "hardness": 2.0, "color": (120,  85,  55), "drop": "trade_block"},
    FORGE_BLOCK:         {"name": "Forge",               "hardness": 3.0, "color": ( 80,  65,  55), "drop": "forge_item"},
    WEAPON_RACK_BLOCK:   {"name": "Weapon Rack",         "hardness": 1.5, "color": (100,  80,  60), "drop": "weapon_rack_item"},
    # Logic blocks
    SWITCH_BLOCK_OFF:       {"name": "Switch (Off)",    "hardness": 2.0, "color": ( 90,  80,  75), "drop": "switch_item"},
    SWITCH_BLOCK_ON:        {"name": "Switch (On)",     "hardness": 2.0, "color": ( 90,  80,  75), "drop": "switch_item"},
    LATCH_BLOCK_OFF:        {"name": "Toggle Latch (Off)", "hardness": 2.0, "color": ( 85,  85,  95), "drop": "latch_item"},
    LATCH_BLOCK_ON:         {"name": "Toggle Latch (On)",  "hardness": 2.0, "color": ( 85,  85,  95), "drop": "latch_item"},
    AND_GATE_BLOCK:         {"name": "AND Gate",        "hardness": 2.0, "color": ( 70,  90, 110), "drop": "and_gate_item"},
    OR_GATE_BLOCK:          {"name": "OR Gate",         "hardness": 2.0, "color": ( 70, 110,  90), "drop": "or_gate_item"},
    NOT_GATE_BLOCK:         {"name": "NOT Gate",        "hardness": 2.0, "color": (110,  70,  70), "drop": "not_gate_item"},
    DAM_BLOCK_CLOSED:       {"name": "Dam",             "hardness": 2.0, "color": (140, 130, 110), "drop": "dam_item"},
    DAM_BLOCK_OPEN:         {"name": "Dam (Open)",      "hardness": 2.0, "color": (140, 130, 110), "drop": "dam_item"},
    PUMP_BLOCK_OFF:         {"name": "Pump",            "hardness": 2.0, "color": ( 95, 100, 105), "drop": "pump_item"},
    PUMP_BLOCK_ON:          {"name": "Pump (On)",       "hardness": 2.0, "color": ( 95, 100, 105), "drop": "pump_item"},
    IRON_GATE_BLOCK_CLOSED: {"name": "Iron Gate",       "hardness": 2.0, "color": ( 75,  80,  85), "drop": "iron_gate_item"},
    IRON_GATE_BLOCK_OPEN:   {"name": "Iron Gate (Open)","hardness": 2.0, "color": ( 75,  80,  85), "drop": "iron_gate_item"},
    PRESSURE_PLATE_OFF:     {"name": "Pressure Plate",     "hardness": 1.0, "color": (160, 155, 145), "drop": "pressure_plate_item"},
    PRESSURE_PLATE_ON:      {"name": "Pressure Plate (On)", "hardness": 1.0, "color": (160, 155, 145), "drop": "pressure_plate_item"},
    DAY_SENSOR_BLOCK:       {"name": "Day Sensor",         "hardness": 1.5, "color": (220, 190,  60), "drop": "day_sensor_item"},
    NIGHT_SENSOR_BLOCK:     {"name": "Night Sensor",       "hardness": 1.5, "color": ( 60,  70, 140), "drop": "day_sensor_item"},
    WATER_SENSOR_BLOCK:     {"name": "Water Sensor",       "hardness": 1.5, "color": ( 60, 130, 200), "drop": "water_sensor_item"},
    CROP_SENSOR_BLOCK:      {"name": "Crop Sensor",        "hardness": 1.5, "color": ( 60, 160,  80), "drop": "crop_sensor_item"},
    REPEATER_BLOCK:         {"name": "Signal Repeater",    "hardness": 2.0, "color": ( 90,  90, 120), "drop": "repeater_item"},
    PULSE_GEN_BLOCK:        {"name": "Pulse Generator",    "hardness": 2.0, "color": (120,  80, 120), "drop": "pulse_gen_item"},
    RS_LATCH_Q0:            {"name": "RS Latch (Q=0)",     "hardness": 2.0, "color": ( 80, 100, 100), "drop": "rs_latch_item"},
    RS_LATCH_Q1:            {"name": "RS Latch (Q=1)",     "hardness": 2.0, "color": ( 80, 100, 100), "drop": "rs_latch_item"},
    POWERED_LANTERN_OFF:    {"name": "Powered Lantern",    "hardness": 1.5, "color": (180, 160,  80), "drop": "powered_lantern_item"},
    POWERED_LANTERN_ON:     {"name": "Powered Lantern (On)","hardness": 1.5, "color": (255, 220,  80), "drop": "powered_lantern_item"},
    ALARM_BELL_OFF:         {"name": "Alarm Bell",         "hardness": 1.5, "color": (170,  80,  40), "drop": "alarm_bell_item"},
    ALARM_BELL_ON:          {"name": "Alarm Bell (On)",    "hardness": 1.5, "color": (220, 100,  40), "drop": "alarm_bell_item"},
    IRRIGATION_CHANNEL_BLOCK: {"name": "Irrigation Channel", "hardness": 1.5, "color": (130, 110,  90), "drop": "irrigation_channel_item"},
    COUNTER_BLOCK:        {"name": "Counter",      "hardness": 2.0, "color": ( 80, 110, 140), "drop": "counter_item"},
    COMPARATOR_BLOCK:     {"name": "Comparator",   "hardness": 2.0, "color": (140,  80, 100), "drop": "comparator_item"},
    OBSERVER_BLOCK:       {"name": "Observer",     "hardness": 2.0, "color": ( 60,  80,  70), "drop": "observer_item"},
    SEQUENCER_BLOCK:      {"name": "Sequencer",    "hardness": 2.0, "color": (100,  80, 140), "drop": "sequencer_item"},
    T_FLIPFLOP_BLOCK:     {"name": "T Flip-Flop",  "hardness": 2.0, "color": (140, 120,  60), "drop": "t_flipflop_item"},
    DEPOSIT_TRIGGER_BLOCK:  {"name": "Deposit Trigger",   "hardness": 2.0, "color": (200, 140,  50), "drop": "deposit_trigger_item"},
    AUTOMATION_BENCH_BLOCK: {"name": "Automation Bench",  "hardness": 2.0, "color": ( 70,  90, 110), "drop": "automation_bench_item"},
    CHICKEN_COOP_BLOCK:    {"name": "Chicken Coop",      "hardness": 2.0, "color": (165, 125,  60), "drop": "chicken_coop_item"},
    GAMBLING_TABLE:        {"name": "Gambling Table",    "hardness": float('inf'), "color": (20, 80, 40),   "drop": None},
    RACING_RAIL:           {"name": "Racing Rail",       "hardness": 1.5, "color": (110, 80, 45),  "drop": "racing_rail"},
    BET_COUNTER:           {"name": "Bet Counter",       "hardness": float('inf'), "color": (80, 60, 35),   "drop": None},
    STARTING_GATE:         {"name": "Starting Gate",     "hardness": 1.5, "color": (200, 185, 160), "drop": "starting_gate"},
    WINNERS_POST:          {"name": "Winners Post",      "hardness": 1.5, "color": (195, 160, 50),  "drop": "winners_post"},
    ALPINE_BALCONY_RAIL:       {"name": "Alpine Balcony Rail", "hardness": 1, "color": (160, 110,  65), "drop": "alpine_balcony_rail"},
    DARK_TIMBER_BEAM:          {"name": "Dark Timber Beam", "hardness": 1, "color": ( 55,  40,  30), "drop": "dark_timber_beam"},
    ROUGH_STONE_WALL:          {"name": "Rough Stone Wall", "hardness": 1, "color": (130, 125, 120), "drop": "rough_stone_wall"},
    ALPINE_PLASTER:            {"name": "Alpine Plaster", "hardness": 1, "color": (230, 220, 205), "drop": "alpine_plaster"},
    FLOWER_BOX:                {"name": "Flower Box", "hardness": 1, "color": (110,  80,  50), "drop": "flower_box"},
    FIREWOOD_STACK:            {"name": "Firewood Stack", "hardness": 1, "color": (100,  70,  45), "drop": "firewood_stack"},
    SLATE_SHINGLE:             {"name": "Slate Shingle", "hardness": 1, "color": ( 65,  75,  90), "drop": "slate_shingle"},
    CARVED_SHUTTER:            {"name": "Carved Shutter", "hardness": 1, "color": (130,  95,  60), "drop": "carved_shutter"},
    BEAR_HIDE:                 {"name": "Bear Hide", "hardness": 1, "color": (100,  75,  50), "drop": "bear_hide"},
    ALPINE_HERB_RACK:          {"name": "Alpine Herb Rack", "hardness": 1, "color": ( 90,  65,  45), "drop": "alpine_herb_rack"},
    HAY_BALE:                  {"name": "Hay Bale", "hardness": 1, "color": (200, 175,  80), "drop": "hay_bale"},
    PINE_PLANK_WALL:           {"name": "Pine Plank Wall", "hardness": 1, "color": (210, 190, 150), "drop": "pine_plank_wall"},
    GRANITE_ASHLAR:            {"name": "Granite Ashlar", "hardness": 1, "color": (140, 130, 130), "drop": "granite_ashlar"},
    CUCKOO_CLOCK:              {"name": "Cuckoo Clock", "hardness": 1, "color": (110,  80,  55), "drop": "cuckoo_clock"},
    GERANIUM_BOX:              {"name": "Geranium Box", "hardness": 1, "color": (100,  70,  45), "drop": "geranium_box"},
    ARCH_STONE:                {"name": "Arch Stone", "hardness": 1, "color": (175, 165, 155), "drop": "arch_stone"},
    SWISS_PANEL:               {"name": "Swiss Panel", "hardness": 1, "color": (225, 215, 195), "drop": "swiss_panel"},
    COPPER_COWBELL:            {"name": "Copper Cowbell", "hardness": 1, "color": (185, 120,  70), "drop": "copper_cowbell"},
    WOODEN_GEAR:               {"name": "Wooden Gear", "hardness": 1, "color": (145, 110,  70), "drop": "wooden_gear"},
    STONE_BASIN:               {"name": "Stone Basin", "hardness": 1, "color": (150, 145, 140), "drop": "stone_basin"},
    MILK_CHURN:                {"name": "Milk Churn", "hardness": 1, "color": (190, 195, 200), "drop": "milk_churn"},
    ALPINE_CHEST:              {"name": "Alpine Chest", "hardness": 1, "color": ( 80,  55,  35), "drop": "alpine_chest"},
    ALPINE_LANTERN:            {"name": "Alpine Lantern", "hardness": 1, "color": ( 60,  60,  65), "drop": "alpine_lantern"},
    WROUGHT_IRON_RAIL:         {"name": "Wrought Iron Rail", "hardness": 1, "color": ( 70,  70,  75), "drop": "wrought_iron_rail"},
    ALPINE_CHANDELIER:         {"name": "Alpine Chandelier", "hardness": 1, "color": ( 65,  65,  70), "drop": "alpine_chandelier"},
    WOVEN_TEXTILE:             {"name": "Woven Textile", "hardness": 1, "color": (185,  60,  60), "drop": "woven_textile"},
    COWBELL_RACK:              {"name": "Cowbell Rack", "hardness": 1, "color": (110,  80,  50), "drop": "cowbell_rack"},
    ALPINE_STUCCO:             {"name": "Alpine Stucco", "hardness": 1, "color": (220, 210, 195), "drop": "alpine_stucco"},
    CARVED_LINTEL:             {"name": "Carved Lintel", "hardness": 1, "color": (180, 170, 160), "drop": "carved_lintel"},
    CHALET_DOOR:               {"name": "Chalet Door", "hardness": 1, "color": ( 90,  65,  40), "drop": "chalet_door"},
    CERAMIC_TILE_STOVE:        {"name": "Ceramic Tile Stove", "hardness": 1, "color": ( 80, 130, 100), "drop": "ceramic_tile_stove"},
    CARVED_BARGEBOARD:         {"name": "Carved Bargeboard", "hardness": 1, "color": ( 65,  45,  28), "drop": "carved_bargeboard"},
    DORMER_WINDOW:             {"name": "Dormer Window", "hardness": 1, "color": (130, 165, 190), "drop": "dormer_window"},
    WOODEN_SHINGLE:            {"name": "Wooden Shingle", "hardness": 1, "color": (165, 130,  80), "drop": "wooden_shingle"},
    STONE_STEP:                {"name": "Stone Step", "hardness": 1, "color": (155, 150, 145), "drop": "stone_step"},
    WATER_TROUGH:              {"name": "Water Trough", "hardness": 1, "color": (140, 135, 130), "drop": "water_trough"},
    CARVED_BENCH:              {"name": "Carved Bench", "hardness": 1, "color": (110,  80,  50), "drop": "carved_bench"},
    CHEESE_WHEEL:              {"name": "Cheese Wheel", "hardness": 1, "color": (215, 185,  80), "drop": "cheese_wheel"},
    ANTLER_MOUNT:              {"name": "Antler Mount", "hardness": 1, "color": (160, 125,  80), "drop": "antler_mount"},
    EDELWEISS_WREATH:          {"name": "Edelweiss Wreath", "hardness": 1, "color": ( 70, 100,  55), "drop": "edelweiss_wreath"},
    BOOT_RACK:                 {"name": "Boot Rack", "hardness": 1, "color": ( 75,  55,  38), "drop": "boot_rack"},
    TALLOW_CANDLE:             {"name": "Tallow Candle", "hardness": 1, "color": (235, 220, 185), "drop": "tallow_candle"},
    ALPINE_HEARTH:             {"name": "Alpine Hearth", "hardness": 1, "color": ( 95,  88,  82), "drop": "alpine_hearth"},
    PINE_CONE_GARLAND:         {"name": "Pine Cone Garland", "hardness": 1, "color": ( 95,  70,  40), "drop": "pine_cone_garland"},
    IRON_HOOK_RACK:            {"name": "Iron Hook Rack", "hardness": 1, "color": ( 65,  65,  70), "drop": "iron_hook_rack"},
    ALPINE_GATE:               {"name": "Alpine Gate", "hardness": 1, "color": ( 85,  60,  38), "drop": "alpine_gate"},
    BUTTER_CHURN:              {"name": "Butter Churn", "hardness": 1, "color": (130, 105,  70), "drop": "butter_churn"},
    CARVED_WAINSCOT:           {"name": "Carved Wainscot", "hardness": 1, "color": ( 80,  58,  38), "drop": "carved_wainscot"},
    CHIMNEY_CAP:               {"name": "Chimney Cap", "hardness": 1, "color": (100,  95,  90), "drop": "chimney_cap"},
    FEATHER_DUVET:             {"name": "Feather Duvet", "hardness": 1, "color": (235, 230, 240), "drop": "feather_duvet"},
    GREEK_AMPHORA:             {"name": "Greek Amphora", "hardness": 1, "color": (175,  95,  55), "drop": "greek_amphora"},
    KRATER:                    {"name": "Krater", "hardness": 1, "color": (170,  88,  48), "drop": "krater"},
    HYDRIA:                    {"name": "Hydria", "hardness": 1, "color": (165,  85,  50), "drop": "hydria"},
    LEKYTHOS:                  {"name": "Lekythos", "hardness": 1, "color": (215, 175, 120), "drop": "lekythos"},
    STORAGE_PITHOS:            {"name": "Storage Pithos", "hardness": 1, "color": (160,  90,  52), "drop": "storage_pithos"},
    KLINE:                     {"name": "Kline", "hardness": 1, "color": (140, 105,  68), "drop": "kline"},
    TRIPOD_BRAZIER:            {"name": "Tripod Brazier", "hardness": 1, "color": (100,  78,  50), "drop": "tripod_brazier"},
    OLIVE_PRESS:               {"name": "Olive Press", "hardness": 1, "color": (120, 100,  68), "drop": "olive_press"},
    LOOM_FRAME:                {"name": "Loom Frame", "hardness": 1, "color": (130, 100,  65), "drop": "loom_frame"},
    MEANDER_BORDER:            {"name": "Meander Border", "hardness": 1, "color": (225, 218, 205), "drop": "meander_border"},
    SYMPOSIUM_TABLE:           {"name": "Symposium Table", "hardness": 1, "color": (140, 108,  70), "drop": "symposium_table"},
    VOTIVE_TABLET:             {"name": "Votive Tablet", "hardness": 1, "color": (195, 185, 172), "drop": "votive_tablet"},
    BRONZE_CUIRASS_STAND:      {"name": "Bronze Cuirass Stand", "hardness": 1, "color": (120,  95,  55), "drop": "bronze_cuirass_stand"},
    CHARIOT_WHEEL:             {"name": "Chariot Wheel", "hardness": 1, "color": (115,  85,  52), "drop": "chariot_wheel"},
    TERRACOTTA_ROOF_TILE:      {"name": "Terracotta Roof Tile", "hardness": 1, "color": (185, 100,  62), "drop": "terracotta_roof_tile"},
    ATTIC_VASE:                {"name": "Attic Vase", "hardness": 1, "color": (180,  85,  42), "drop": "attic_vase"},
    GREEK_STONE_BENCH:         {"name": "Greek Stone Bench", "hardness": 1, "color": (230, 226, 218), "drop": "greek_stone_bench"},
    STONE_ALTAR:               {"name": "Stone Altar", "hardness": 1, "color": (178, 168, 158), "drop": "stone_altar"},
    BRONZE_MIRROR:             {"name": "Bronze Mirror", "hardness": 1, "color": (135,  98,  52), "drop": "bronze_mirror"},
    CLAY_OIL_LAMP:             {"name": "Clay Oil Lamp", "hardness": 1, "color": (170, 120,  72), "drop": "clay_oil_lamp"},
    AGORA_SCALE:               {"name": "Agora Scale", "hardness": 1, "color": (130, 105,  58), "drop": "agora_scale"},
    LAUREL_WREATH_MOUNT:       {"name": "Laurel Wreath Mount", "hardness": 1, "color": ( 55,  95,  42), "drop": "laurel_wreath_mount"},
    HERMES_STELE:              {"name": "Hermes Stele", "hardness": 1, "color": (190, 182, 172), "drop": "hermes_stele"},
    DORIC_CAPITAL:             {"name": "Doric Capital", "hardness": 1, "color": (232, 228, 218), "drop": "doric_capital"},
    VICTORY_STELE:             {"name": "Victory Stele", "hardness": 1, "color": (220, 215, 205), "drop": "victory_stele"},
    BRONZE_SHIELD_MOUNT:       {"name": "Bronze Shield Mount", "hardness": 1, "color": (115,  90,  48), "drop": "bronze_shield_mount"},
    EGG_AND_DART:              {"name": "Egg and Dart", "hardness": 1, "color": (215, 210, 200), "drop": "egg_and_dart"},
    OLIVE_BRANCH:              {"name": "Olive Branch", "hardness": 1, "color": ( 62,  98,  45), "drop": "olive_branch"},
    PHILOSOPHERS_SCROLL:       {"name": "Philosophers Scroll", "hardness": 1, "color": (215, 195, 150), "drop": "philosophers_scroll"},
    GREEK_THEATRE_MASK:        {"name": "Greek Theatre Mask", "hardness": 1,   "color": (230, 190, 140), "drop": "greek_theatre_mask"},
    TORCH:                     {"name": "Torch",              "hardness": 0.5, "color": (200, 140,  50), "drop": "torch"},
    WALL_SCONCE:               {"name": "Wall Sconce",        "hardness": 1.0, "color": ( 55,  55,  60), "drop": "wall_sconce"},
    BRAZIER:                   {"name": "Brazier",            "hardness": 1.5, "color": ( 65,  60,  55), "drop": "brazier"},
    CHANDELIER:                {"name": "Chandelier",         "hardness": 1.0, "color": ( 55,  55,  60), "drop": "chandelier"},
    CANDELABRA:                {"name": "Candelabra",         "hardness": 1.0, "color": ( 60,  55,  50), "drop": "candelabra"},
    LANTERN_ORB:               {"name": "Lantern Orb",        "hardness": 1.0, "color": (180, 220, 240), "drop": "lantern_orb"},
    PENDANT_LAMP:              {"name": "Pendant Lamp",       "hardness": 1.0, "color": ( 55,  55,  60), "drop": "pendant_lamp"},
    FIRE_BOWL:                 {"name": "Fire Bowl",          "hardness": 2.0, "color": ( 90,  85,  80), "drop": "fire_bowl"},
    CROSS_LANTERN:             {"name": "Cross Lantern",      "hardness": 1.0, "color": ( 55,  55,  60), "drop": "cross_lantern"},
    STAR_LAMP:                 {"name": "Star Lamp",          "hardness": 1.0, "color": (200, 240, 255), "drop": "star_lamp"},
    GLOW_VINE:                 {"name": "Glow Vine",          "hardness": 0.5, "color": ( 40, 100,  60), "drop": "glow_vine"},
    TOWN_FLAG_BLOCK:           {"name": "Town Flag",          "hardness": float('inf'), "color": (200, 80, 40), "drop": None},
    OUTPOST_FLAG_BLOCK:        {"name": "Outpost Flag",       "hardness": float('inf'), "color": (180, 140, 60), "drop": None},
    LANDMARK_FLAG_BLOCK:       {"name": "Landmark Flag",      "hardness": float('inf'), "color": (190, 150,  60), "drop": None},
    # --- Brewery supply chain ---
    HOP_VINE_BUSH:             {"name": "Hop Vine Bush",      "hardness": 0.5, "color": ( 90, 145,  55), "drop": "hop_seed",          "drop_chance": 1.0},
    HOP_VINE_YOUNG:            {"name": "Hop Vine",           "hardness": 0.5, "color": (100, 160,  60), "drop": "hop_seed",          "drop_chance": 1.0},
    HOP_VINE_MATURE:           {"name": "Hop Vine (Ripe)",    "hardness": 0.5, "color": (160, 195,  55), "drop": None},
    BREW_KETTLE_BLOCK:         {"name": "Brew Kettle",        "hardness": 1.5, "color": (185, 130,  55), "drop": "brew_kettle_item"},
    FERM_VESSEL_BLOCK:         {"name": "Fermentation Vessel","hardness": 1.5, "color": ( 95, 130,  80), "drop": "ferm_vessel_item"},
    TAPROOM_BLOCK:             {"name": "Taproom",            "hardness": 1.5, "color": ( 95,  65,  40), "drop": "taproom_item"},
    ICE_SHARD:                 {"name": "Ice Shard", "hardness": 1, "color": (185, 225, 248), "drop": "ice_shard"},
    FROZEN_BOG:                {"name": "Frozen Bog", "hardness": 1, "color": ( 95, 120, 138), "drop": "frozen_bog"},
    STONE_BRIDGE:              {"name": "Stone Bridge",     "hardness": 2.5, "color": (118, 112, 102), "drop": "stone_chip"},
    TIMBER_BRIDGE:             {"name": "Timber Bridge",    "hardness": 2.0, "color": (110,  75,  42), "drop": "lumber"},
    MOSSY_BRIDGE:              {"name": "Mossy Bridge",     "hardness": 2.0, "color": ( 78,  95,  72), "drop": "stone_chip"},
    SANDSTONE_BRIDGE:          {"name": "Sandstone Bridge", "hardness": 2.5, "color": (192, 158, 100), "drop": "stone_chip"},
    BRICK_BRIDGE:              {"name": "Brick Bridge",     "hardness": 2.5, "color": (168,  82,  52), "drop": "stone_chip"},
    COBBLE_BRIDGE:             {"name": "Cobble Bridge",    "hardness": 2.5, "color": (108,  98,  84), "drop": "stone_chip"},
    DRIFTWOOD_BRIDGE:          {"name": "Driftwood Bridge", "hardness": 1.5, "color": (185, 172, 148), "drop": "lumber"},
    CITY_BLOCK:                {"name": "City Block",       "hardness": float('inf'), "color": (180, 155, 90), "drop": None},
    GROW_LAMP:                 {"name": "Grow Lamp",        "hardness": 1.5,          "color": (210, 255, 160), "drop": "grow_lamp_item"},
    MINING_POST_BLOCK:         {"name": "Mining Post",      "hardness": 2.0,          "color": (110,  85,  60), "drop": "mining_post_item"},
    BANNER_BLOCK:              {"name": "Banner",           "hardness": 1.0,          "color": (160,  80,  40), "drop": "banner_item"},
    FISHING_SPOT_BLOCK:        {"name": "Fishing Spot",     "hardness": -1,           "color": ( 50, 140, 235), "drop": None},
    FISH_TROPHY_BLOCK:         {"name": "Fish Trophy",      "hardness": 0.5,          "color": (160, 110,  60), "drop": "fish_trophy_item"},
    WEAPON_ASSEMBLER_BLOCK:    {"name": "Weapon Assembler", "hardness": 1,  "color": (120,  90,  60), "drop": "weapon_assembler"},
    TEA_HOUSE_BLOCK:           {"name": "Tea House",        "hardness": 1,  "color": (122,  92,  58), "drop": "tea_house_item"},
    CLOUD_CIRRUS:              {"name": "Cirrus Cloud",     "hardness": -1, "color": (220, 235, 255), "drop": None},
    CLOUD_CUMULUS:             {"name": "Cumulus Cloud",    "hardness": -1, "color": (240, 240, 245), "drop": None},
    CLOUD_STRATUS:             {"name": "Stratus Cloud",    "hardness": -1, "color": (190, 195, 205), "drop": None},
    CLOUD_STORM:               {"name": "Storm Cloud",      "hardness": -1, "color": (100,  95, 120), "drop": None},
}

# Light-emitting blocks: {block_id: (radius_px, pattern)}
# Patterns: circle, wide_oval, tall_oval, wide_flat, soft, dim,
#           cone_up, cone_down, cross, star, flicker
LIGHT_EMITTERS = {
    TORCH:           (100, "circle"),
    WALL_SCONCE:     ( 90, "wide_oval"),
    BRAZIER:         (115, "cone_up"),
    CHANDELIER:      (130, "wide_flat"),
    CANDELABRA:      ( 85, "tall_oval"),
    LANTERN_ORB:     (140, "soft"),
    PENDANT_LAMP:    (105, "cone_down"),
    FIRE_BOWL:       ( 95, "flicker"),
    CROSS_LANTERN:   ( 80, "cross"),
    STAR_LAMP:       ( 75, "star"),
    GLOW_VINE:       ( 55, "dim"),
    # City / decorative lanterns
    GARDEN_LANTERN:  ( 90, "circle"),
    IRON_LANTERN:    ( 85, "soft"),
    TRIPOD_BRAZIER:  (100, "flicker"),
    PAPER_LANTERN:   ( 90, "soft"),
    STONE_LANTERN:   ( 65, "dim"),
    TORO_LANTERN:    ( 70, "dim"),
    YUKIMI_LANTERN:  ( 70, "soft"),
    LANTERN_FESTIVAL:(105, "wide_oval"),
    ALPINE_LANTERN:  ( 85, "circle"),
    ALPINE_CHANDELIER:(125, "wide_flat"),
    # Logic output
    POWERED_LANTERN_ON: (80, "circle"),
    # Farming
    GROW_LAMP:          (170, "wide_flat"),
    # Fireplaces & hearths
    HEARTH_STONE:        (110, "flicker"),
    ALPINE_HEARTH:       (120, "flicker"),
    CASTLE_FIREPLACE:    (115, "flicker"),
    RENAISSANCE_MANTEL:  (100, "flicker"),
    TALLOW_CANDLE:       ( 55, "soft"),
    # Windows — soft glow from warm interiors
    LEADLIGHT_WINDOW:    ( 70, "soft"),
    ROSE_WINDOW:         ( 75, "soft"),
    PALLADIAN_WINDOW:    ( 75, "soft"),
    CATHEDRAL_WINDOW:    ( 80, "soft"),
    OCULUS_WINDOW:       ( 70, "soft"),
    LANCET_WINDOW:       ( 65, "soft"),
    ORANGERY_WINDOW:     ( 80, "soft"),
    THERMAL_WINDOW:      ( 70, "soft"),
    BIFORA_WINDOW:       ( 70, "soft"),
    SERLIANA_WINDOW:     ( 75, "soft"),
    DORMER_WINDOW:       ( 65, "soft"),
}

# Blocks that cast warm amber light (additive color pass on top of darkness).
# Separate from LIGHT_EMITTERS so the two passes can be tuned independently.
WARM_EMITTERS = {
    # Fire sources — intense, flickering
    HEARTH_STONE:        (100, "flicker"),
    ALPINE_HEARTH:       (110, "flicker"),
    CASTLE_FIREPLACE:    (105, "flicker"),
    RENAISSANCE_MANTEL:  ( 90, "flicker"),
    TALLOW_CANDLE:       ( 45, "flicker"),
    FIRE_BOWL:           ( 85, "flicker"),
    BRAZIER:             ( 95, "flicker"),
    TRIPOD_BRAZIER:      ( 90, "flicker"),
    TORCH:               ( 80, "flicker"),
    WALL_SCONCE:         ( 75, "flicker"),
    CANDELABRA:          ( 70, "flicker"),
    # Windows — softer spill, no flicker
    LEADLIGHT_WINDOW:    ( 65, "soft"),
    ROSE_WINDOW:         ( 70, "soft"),
    PALLADIAN_WINDOW:    ( 70, "soft"),
    CATHEDRAL_WINDOW:    ( 75, "soft"),
    OCULUS_WINDOW:       ( 65, "soft"),
    LANCET_WINDOW:       ( 60, "soft"),
    ORANGERY_WINDOW:     ( 75, "soft"),
    THERMAL_WINDOW:      ( 65, "soft"),
    BIFORA_WINDOW:       ( 65, "soft"),
    SERLIANA_WINDOW:     ( 70, "soft"),
    DORMER_WINDOW:       ( 60, "soft"),
    PAPER_LANTERN:       ( 75, "soft"),
    IRON_LANTERN:        ( 70, "soft"),
    GARDEN_LANTERN:      ( 72, "soft"),
    ALPINE_LANTERN:      ( 70, "soft"),
    LANTERN_FESTIVAL:    ( 85, "soft"),
}
