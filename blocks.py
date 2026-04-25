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
FENNEL_BUSH             = 329
FENNEL_CROP_YOUNG       = 330
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
BAIT_STATION_BLOCK      = 314  # placed Bait Station; crafts fishing bait
CHICKPEA_CROP_YOUNG     = 315
CHICKPEA_CROP_MATURE    = 316
LENTIL_CROP_YOUNG       = 317
LENTIL_CROP_MATURE      = 318
SESAME_CROP_YOUNG       = 319
SESAME_CROP_MATURE      = 320
POMEGRANATE_TREE_YOUNG  = 321
POMEGRANATE_TREE_MATURE = 322
OLIVE_TREE_YOUNG        = 323
OLIVE_TREE_MATURE       = 324
SAFFRON_CROP_YOUNG      = 325
SAFFRON_CROP_MATURE     = 326

# --- Islamic architecture blocks (Artisan Bench) ---
# --- Mineable natural deposits ---
CLAY_DEPOSIT      = 329  # natural clay bed; shallow sedimentary/temperate zones
LIMESTONE_DEPOSIT = 330  # natural limestone layer; shallow-mid sedimentary zones

# --- Islamic architecture blocks (Artisan Bench) ---
WHITE_PLASTER_WALL = 323  # smooth white plaster wall
CARVED_PLASTER     = 324  # white plaster with gold arabesque geometric inlay
MUQARNAS_BLOCK     = 325  # stepped stalactite/honeycomb overhang element
MASHRABIYA         = 326  # carved wooden diamond-lattice screen
ZELLIGE_TILE       = 327  # colorful geometric mosaic tile (Moroccan style)
ARABESQUE_PANEL    = 328  # sandstone panel with interlaced geometric carving

# --- Spanish architecture blocks (Artisan Bench) ---
ADOBE_BRICK        = 331  # sun-dried mud brick; warm tan with straw texture
SPANISH_ROOF_TILE  = 332  # curved barrel roof tile in terracotta red
WROUGHT_IRON_GRILLE= 333  # decorative forged-iron scrollwork panel
TALAVERA_TILE      = 334  # blue-and-white hand-painted ceramic tile
SALTILLO_TILE      = 335  # unglazed terracotta floor tile

# --- Middle Eastern decorative doors (Artisan Bench) ---
COBALT_DOOR_CLOSED       = 336  # royal blue lacquered door with gold arabesque
COBALT_DOOR_OPEN         = 337
CRIMSON_CEDAR_DOOR_CLOSED= 338  # deep red cedar with carved diamond geometry
CRIMSON_CEDAR_DOOR_OPEN  = 339
TEAL_DOOR_CLOSED         = 340  # rich teal lacquered door with gold trim
TEAL_DOOR_OPEN           = 341
SAFFRON_DOOR_CLOSED      = 342  # warm golden-yellow with dark carved panels
SAFFRON_DOOR_OPEN        = 343

# --- European architecture blocks (Artisan Bench) ---
HALF_TIMBER_WALL  = 344  # Tudor black timber framing on white plaster
ASHLAR_BLOCK      = 345  # precisely dressed stone with tight regular joints
GOTHIC_TRACERY    = 346  # pointed lancet arch tracery panel
FLUTED_COLUMN     = 347  # classical column shaft with vertical flute grooves
CORNICE_BLOCK     = 348  # classical stepped projecting molding
ROSE_WINDOW       = 349  # Gothic circular window tracery
HERRINGBONE_BRICK = 350  # diagonal herringbone brick floor
BAROQUE_TRIM      = 351  # elaborate carved stone scrollwork panel
TUDOR_BEAM        = 352  # dark exposed structural timber
VENETIAN_FLOOR    = 353  # pale stone with diamond inlay accents
FLEMISH_BRICK     = 354  # two-tone Flemish bond brick
PILASTER          = 355  # classical flat wall column with capital and base
DENTIL_TRIM       = 356  # classical tooth-molding band
WATTLE_DAUB       = 357  # medieval woven-straw plaster wall
NORDIC_PLANK      = 358  # dark weathered Nordic timber
MANSARD_SLATE     = 359  # French fish-scale roof slate
ROMAN_MOSAIC      = 360  # small square tiles in warm geometric pattern
SETT_STONE        = 361  # European granite street sett
ROMANESQUE_ARCH   = 362  # warm sandstone rounded arch voussoir panel
DARK_SLATE_ROOF   = 363  # overlapping dark grey-blue slate shingles
KEYSTONE          = 364  # arch keystone wedge block
PLINTH_BLOCK      = 365  # classical column base with recessed panel
IRON_LANTERN      = 366  # Victorian iron lantern frame with warm glow
SANDSTONE_ASHLAR  = 367  # warm sandstone with precise rectangular joints
GARGOYLE_BLOCK    = 368  # Gothic grotesque carved stone panel
OGEE_ARCH         = 369  # S-curved ogee arch with finial (Gothic/Venetian)
RUSTICATED_STONE  = 370  # Renaissance rough-faced stone with deep V-joints
CHEVRON_STONE     = 371  # Norman zigzag carved stone
TRIGLYPH_PANEL    = 372  # Doric frieze with vertical channels and guttae
MARBLE_INLAY      = 373  # Italian white marble with coloured geometric inlay
BRICK_NOGGING     = 374  # brick infill between timber frame panels
CRENELLATION      = 375  # castle battlement with merlons and crenels
FAN_VAULT         = 376  # Gothic fan vaulting panel with radiating ribs
ACANTHUS_PANEL    = 377  # Corinthian carved acanthus leaf panel
PEBBLE_DASH       = 378  # rough exterior render with embedded pebbles
ENCAUSTIC_TILE    = 379  # medieval inlaid terracotta floor tile
CHEQUERBOARD_MARBLE = 380  # alternating black and white marble squares
WROUGHT_IRON_BALUSTRADE = 381  # decorative iron balcony balustrade
OPUS_INCERTUM     = 382  # Roman irregular polygon stone facing
GROTESQUE_FRIEZE  = 383  # carved stone frieze with foliage and faces
BARREL_VAULT      = 384  # Romanesque semicircular vault section
POINTED_ARCH      = 385  # clean Gothic pointed arch
ENGLISH_BOND      = 386  # alternating header/stretcher brick courses
RELIEF_PANEL      = 387  # Classical carved stone relief
DIAGONAL_TILE     = 388  # European diagonal square floor tile
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
                COBALT_DOOR_OPEN, CRIMSON_CEDAR_DOOR_OPEN, TEAL_DOOR_OPEN, SAFFRON_DOOR_OPEN}
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
                    STABLE_BLOCK, HORSE_TROUGH_BLOCK,
                    WITHERING_RACK_BLOCK, OXIDATION_STATION_BLOCK, TEA_CELLAR_BLOCK,
                    DRYING_RACK_BLOCK, BAIT_STATION_BLOCK,
                    SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
                    DAIRY_VAT_BLOCK, CHEESE_PRESS_BLOCK, AGING_CAVE_BLOCK,
                    FLETCHING_TABLE_BLOCK,
                    SMELTER_BLOCK,
                    ANAEROBIC_TANK_BLOCK,
                    GLASS_KILN_BLOCK,
                    JEWELRY_WORKBENCH_BLOCK,
                    GARDEN_WORKSHOP_BLOCK}
RESOURCE_BLOCKS  = {COAL_ORE, IRON_ORE, GOLD_ORE, CRYSTAL_ORE, RUBY_ORE, OBSIDIAN, ROCK_DEPOSIT, FOSSIL_DEPOSIT, GEM_DEPOSIT,
                    CLAY_DEPOSIT, LIMESTONE_DEPOSIT}
BUSH_BLOCKS       = {STRAWBERRY_BUSH, WHEAT_BUSH, CARROT_BUSH, TOMATO_BUSH, CORN_BUSH, PUMPKIN_BUSH, APPLE_BUSH,
                     RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, GARLIC_BUSH, SCALLION_BUSH, CHILI_BUSH,
                     PEPPER_BUSH, ONION_BUSH, POTATO_BUSH, EGGPLANT_BUSH, CABBAGE_BUSH,
                     BEET_BUSH, TURNIP_BUSH, LEEK_BUSH, ZUCCHINI_BUSH, SWEET_POTATO_BUSH,
                     WATERMELON_BUSH, RADISH_BUSH, PEA_BUSH, CELERY_BUSH, BROCCOLI_BUSH,
                     DATE_PALM_BUSH, AGAVE_BUSH,
                     COFFEE_BUSH, GRAPEVINE_BUSH, GRAIN_CROP_BUSH,
                     TEA_BUSH,
                     CHAMOMILE_BUSH, LAVENDER_BUSH, MINT_BUSH, ROSEMARY_BUSH,
                     THYME_BUSH, SAGE_BUSH, BASIL_BUSH, OREGANO_BUSH,
                     DILL_BUSH, FENNEL_BUSH, TARRAGON_BUSH, LEMON_BALM_BUSH,
                     ECHINACEA_BUSH, VALERIAN_BUSH, ST_JOHNS_WORT_BUSH, YARROW_BUSH,
                     BERGAMOT_BUSH, WORMWOOD_BUSH, RUE_BUSH, LEMON_VERBENA_BUSH,
                     HYSSOP_BUSH, CATNIP_BUSH, WOOD_SORREL_BUSH, MARJORAM_BUSH,
                     SAVORY_BUSH, ANGELICA_BUSH, BORAGE_BUSH, COMFREY_BUSH, MUGWORT_BUSH,
                     FLAX_BUSH}
YOUNG_CROP_BLOCKS = {STRAWBERRY_CROP_YOUNG, WHEAT_CROP_YOUNG, CARROT_CROP_YOUNG, TOMATO_CROP_YOUNG, CORN_CROP_YOUNG, PUMPKIN_CROP_YOUNG, APPLE_CROP_YOUNG,
                     RICE_CROP_YOUNG, GINGER_CROP_YOUNG, BOK_CHOY_CROP_YOUNG, GARLIC_CROP_YOUNG,
                     SCALLION_CROP_YOUNG, CHILI_CROP_YOUNG,
                     PEPPER_CROP_YOUNG, ONION_CROP_YOUNG, POTATO_CROP_YOUNG, EGGPLANT_CROP_YOUNG, CABBAGE_CROP_YOUNG,
                     BEET_CROP_YOUNG, TURNIP_CROP_YOUNG, LEEK_CROP_YOUNG, ZUCCHINI_CROP_YOUNG, SWEET_POTATO_CROP_YOUNG,
                     WATERMELON_CROP_YOUNG, RADISH_CROP_YOUNG, PEA_CROP_YOUNG, CELERY_CROP_YOUNG, BROCCOLI_CROP_YOUNG,
                     CACTUS_YOUNG, DATE_PALM_CROP_YOUNG, AGAVE_CROP_YOUNG,
                     COFFEE_CROP_YOUNG, GRAPEVINE_CROP_YOUNG, GRAIN_CROP_YOUNG, TEA_CROP_YOUNG,
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
                     FLAX_CROP_YOUNG}
MATURE_CROP_BLOCKS= {STRAWBERRY_CROP_MATURE, WHEAT_CROP_MATURE, CARROT_CROP_MATURE, TOMATO_CROP_MATURE, CORN_CROP_MATURE, PUMPKIN_CROP_MATURE, APPLE_CROP_MATURE,
                     RICE_CROP_MATURE, GINGER_CROP_MATURE, BOK_CHOY_CROP_MATURE, GARLIC_CROP_MATURE,
                     SCALLION_CROP_MATURE, CHILI_CROP_MATURE,
                     PEPPER_CROP_MATURE, ONION_CROP_MATURE, POTATO_CROP_MATURE, EGGPLANT_CROP_MATURE, CABBAGE_CROP_MATURE,
                     BEET_CROP_MATURE, TURNIP_CROP_MATURE, LEEK_CROP_MATURE, ZUCCHINI_CROP_MATURE, SWEET_POTATO_CROP_MATURE,
                     WATERMELON_CROP_MATURE, RADISH_CROP_MATURE, PEA_CROP_MATURE, CELERY_CROP_MATURE, BROCCOLI_CROP_MATURE,
                     CACTUS_MATURE, DATE_PALM_CROP_MATURE, AGAVE_CROP_MATURE,
                     COFFEE_CROP_MATURE, GRAPEVINE_CROP_MATURE, GRAIN_CROP_MATURE, TEA_CROP_MATURE,
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
                     FLAX_CROP_MATURE}
CROP_BLOCKS       = YOUNG_CROP_BLOCKS | MATURE_CROP_BLOCKS

# Perennial crops regrow after harvest (each harvest has ~33% chance to die)
PERENNIAL_CROP_MATURE = {
    STRAWBERRY_CROP_MATURE, APPLE_CROP_MATURE, TOMATO_CROP_MATURE,
    PEPPER_CROP_MATURE, CHILI_CROP_MATURE, EGGPLANT_CROP_MATURE,
    CACTUS_MATURE, COFFEE_CROP_MATURE, GRAPEVINE_CROP_MATURE, GRAIN_CROP_MATURE, TEA_CROP_MATURE,
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
    STAIRS_RIGHT:              {"name": "Stairs (Right)",            "hardness": 1.5, "color": (139, 100,  60), "drop": "wood_stairs"},
    STAIRS_LEFT:               {"name": "Stairs (Left)",             "hardness": 1.5, "color": (139, 100,  60), "drop": "wood_stairs"},
    GARDEN_BLOCK:              {"name": "Garden Block",              "hardness": 1.0, "color": ( 80, 140,  60), "drop": "garden_block"},
    STABLE_BLOCK:              {"name": "Stable",                   "hardness": 2.0, "color": (120,  85,  45), "drop": "stable_item"},
    HORSE_TROUGH_BLOCK:        {"name": "Horse Trough",             "hardness": 1.5, "color": ( 60, 100, 130), "drop": "horse_trough_item"},
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
    SAFFRON_DOOR_CLOSED:       {"name": "Saffron Door",          "hardness": 2, "color": (200, 155,  30), "drop": "saffron_door"},
    SAFFRON_DOOR_OPEN:         {"name": "Saffron Door (Open)",   "hardness": 2, "color": (200, 155,  30), "drop": "saffron_door"},
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
}
