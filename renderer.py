import pygame
from blocks import (BLOCKS, AIR, COAL_ORE, LADDER, STONE, WATER, GRASS, DIRT, SAND, SNOW,
                    YOUNG_CROP_BLOCKS, MATURE_CROP_BLOCKS,
                    RESOURCE_BLOCKS, ALL_LOGS, ALL_LEAVES,
                    ALL_FRUIT_CLUSTERS, FRUIT_CLUSTER_LEAF_MAP,
                    STRAWBERRY_BUSH, WHEAT_BUSH,
                    CARROT_BUSH, TOMATO_BUSH, CORN_BUSH, PUMPKIN_BUSH, APPLE_BUSH,
                    STRAWBERRY_CROP_YOUNG, STRAWBERRY_CROP_MATURE,
                    WHEAT_CROP_YOUNG, WHEAT_CROP_MATURE,
                    CARROT_CROP_YOUNG, CARROT_CROP_MATURE,
                    TOMATO_CROP_YOUNG, TOMATO_CROP_MATURE,
                    CORN_CROP_YOUNG, CORN_CROP_MATURE,
                    PUMPKIN_CROP_YOUNG, PUMPKIN_CROP_MATURE,
                    APPLE_CROP_YOUNG, APPLE_CROP_MATURE,
                    RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, GARLIC_BUSH,
                    SCALLION_BUSH, CHILI_BUSH,
                    PEPPER_BUSH, ONION_BUSH, POTATO_BUSH, EGGPLANT_BUSH, CABBAGE_BUSH,
                    PEPPER_CROP_YOUNG, PEPPER_CROP_MATURE,
                    ONION_CROP_YOUNG, ONION_CROP_MATURE,
                    POTATO_CROP_YOUNG, POTATO_CROP_MATURE,
                    EGGPLANT_CROP_YOUNG, EGGPLANT_CROP_MATURE,
                    CABBAGE_CROP_YOUNG, CABBAGE_CROP_MATURE,
                    BBQ_GRILL_BLOCK, CLAY_POT_BLOCK,
                    RICE_CROP_YOUNG, RICE_CROP_MATURE,
                    GINGER_CROP_YOUNG, GINGER_CROP_MATURE,
                    BOK_CHOY_CROP_YOUNG, BOK_CHOY_CROP_MATURE,
                    GARLIC_CROP_YOUNG, GARLIC_CROP_MATURE,
                    SCALLION_CROP_YOUNG, SCALLION_CROP_MATURE,
                    CHILI_CROP_YOUNG, CHILI_CROP_MATURE,
                    BAKERY_BLOCK, WOK_BLOCK, STEAMER_BLOCK, NOODLE_POT_BLOCK,
                    WILDFLOWER_PATCH, WILDFLOWER_DISPLAY_BLOCK,
                    CRACKED_STONE, STALACTITE, STALAGMITE,
                    CAVE_MOSS, CAVE_CRYSTAL, GRAVEL,
                    CRYSTAL_ORE, RUBY_ORE, GEM_DEPOSIT,
                    CAVE_MUSHROOM, CAVE_MUSHROOMS,
                    EMBER_CAP, PALE_GHOST, GOLD_CHANTERELLE, COBALT_CAP, MOSSY_CAP,
                    VIOLET_CROWN, BLOOD_CAP, SULFUR_DOME, IVORY_BELL, ASH_BELL,
                    TEAL_BELL, RUST_SHELF, COPPER_SHELF, OBSIDIAN_SHELF, COAL_PUFF,
                    STONE_PUFF, AMBER_PUFF, SULFUR_TUFT, HONEY_CLUSTER, CORAL_TUFT,
                    BONE_STALK, MAGMA_CAP, DEEP_INK, BIOLUME,
                    WOOD_FENCE, IRON_FENCE, WOOD_FENCE_OPEN, IRON_FENCE_OPEN,
                    WOOD_DOOR_CLOSED, WOOD_DOOR_OPEN,
                    IRON_DOOR_CLOSED, IRON_DOOR_OPEN,
                    CHEST_BLOCK, SNOW, SAND,
                    SAPLING, MUSHROOM_STEM, MUSHROOM_CAP,
                    BEET_BUSH, BEET_CROP_YOUNG, BEET_CROP_MATURE,
                    TURNIP_BUSH, TURNIP_CROP_YOUNG, TURNIP_CROP_MATURE,
                    LEEK_BUSH, LEEK_CROP_YOUNG, LEEK_CROP_MATURE,
                    ZUCCHINI_BUSH, ZUCCHINI_CROP_YOUNG, ZUCCHINI_CROP_MATURE,
                    SWEET_POTATO_BUSH, SWEET_POTATO_CROP_YOUNG, SWEET_POTATO_CROP_MATURE,
                    WATERMELON_BUSH, WATERMELON_CROP_YOUNG, WATERMELON_CROP_MATURE,
                    RADISH_BUSH, RADISH_CROP_YOUNG, RADISH_CROP_MATURE,
                    PEA_BUSH, PEA_CROP_YOUNG, PEA_CROP_MATURE,
                    CELERY_BUSH, CELERY_CROP_YOUNG, CELERY_CROP_MATURE,
                    BROCCOLI_BUSH, BROCCOLI_CROP_YOUNG, BROCCOLI_CROP_MATURE,
                    CHAMOMILE_BUSH, CHAMOMILE_CROP_YOUNG, CHAMOMILE_CROP_MATURE,
                    LAVENDER_BUSH, LAVENDER_CROP_YOUNG, LAVENDER_CROP_MATURE,
                    MINT_BUSH, MINT_CROP_YOUNG, MINT_CROP_MATURE,
                    ROSEMARY_BUSH, ROSEMARY_CROP_YOUNG, ROSEMARY_CROP_MATURE,
                    THYME_BUSH, THYME_CROP_YOUNG, THYME_CROP_MATURE,
                    SAGE_BUSH, SAGE_CROP_YOUNG, SAGE_CROP_MATURE,
                    BASIL_BUSH, BASIL_CROP_YOUNG, BASIL_CROP_MATURE,
                    OREGANO_BUSH, OREGANO_CROP_YOUNG, OREGANO_CROP_MATURE,
                    DILL_BUSH, DILL_CROP_YOUNG, DILL_CROP_MATURE,
                    FENNEL_BUSH, FENNEL_CROP_YOUNG, FENNEL_CROP_MATURE,
                    TARRAGON_BUSH, TARRAGON_CROP_YOUNG, TARRAGON_CROP_MATURE,
                    LEMON_BALM_BUSH, LEMON_BALM_CROP_YOUNG, LEMON_BALM_CROP_MATURE,
                    ECHINACEA_BUSH, ECHINACEA_CROP_YOUNG, ECHINACEA_CROP_MATURE,
                    VALERIAN_BUSH, VALERIAN_CROP_YOUNG, VALERIAN_CROP_MATURE,
                    ST_JOHNS_WORT_BUSH, ST_JOHNS_WORT_CROP_YOUNG, ST_JOHNS_WORT_CROP_MATURE,
                    YARROW_BUSH, YARROW_CROP_YOUNG, YARROW_CROP_MATURE,
                    BERGAMOT_BUSH, BERGAMOT_CROP_YOUNG, BERGAMOT_CROP_MATURE,
                    WORMWOOD_BUSH, WORMWOOD_CROP_YOUNG, WORMWOOD_CROP_MATURE,
                    RUE_BUSH, RUE_CROP_YOUNG, RUE_CROP_MATURE,
                    LEMON_VERBENA_BUSH, LEMON_VERBENA_CROP_YOUNG, LEMON_VERBENA_CROP_MATURE,
                    HYSSOP_BUSH, HYSSOP_CROP_YOUNG, HYSSOP_CROP_MATURE,
                    CATNIP_BUSH, CATNIP_CROP_YOUNG, CATNIP_CROP_MATURE,
                    WOOD_SORREL_BUSH, WOOD_SORREL_CROP_YOUNG, WOOD_SORREL_CROP_MATURE,
                    MARJORAM_BUSH, MARJORAM_CROP_YOUNG, MARJORAM_CROP_MATURE,
                    SAVORY_BUSH, SAVORY_CROP_YOUNG, SAVORY_CROP_MATURE,
                    ANGELICA_BUSH, ANGELICA_CROP_YOUNG, ANGELICA_CROP_MATURE,
                    BORAGE_BUSH, BORAGE_CROP_YOUNG, BORAGE_CROP_MATURE,
                    COMFREY_BUSH, COMFREY_CROP_YOUNG, COMFREY_CROP_MATURE,
                    MUGWORT_BUSH, MUGWORT_CROP_YOUNG, MUGWORT_CROP_MATURE,
                    CACTUS_YOUNG, CACTUS_MATURE,
                    DATE_PALM_BUSH, DATE_PALM_CROP_YOUNG, DATE_PALM_CROP_MATURE,
                    AGAVE_BUSH, AGAVE_CROP_YOUNG, AGAVE_CROP_MATURE,
                    SAGUARO_YOUNG, SAGUARO_MATURE,
                    BARREL_CACTUS_YOUNG, BARREL_CACTUS_MATURE,
                    OCOTILLO_YOUNG, OCOTILLO_MATURE,
                    PRICKLY_PEAR_YOUNG, PRICKLY_PEAR_MATURE,
                    CHOLLA_YOUNG, CHOLLA_MATURE,
                    PALO_VERDE_YOUNG, PALO_VERDE_MATURE,
                    COFFEE_BUSH, COFFEE_CROP_YOUNG, COFFEE_CROP_MATURE,
                    GRAPEVINE_BUSH, GRAPEVINE_CROP_YOUNG, GRAPEVINE_CROP_MATURE,
                    BIRD_FEEDER_BLOCK, BIRD_BATH_BLOCK,
                    TILLED_SOIL,
                    POLISHED_GRANITE, POLISHED_MARBLE, SLATE_TILE, TERRACOTTA_BLOCK,
                    MOSSY_BRICK, CREAM_BRICK, CHARCOAL_PLANK, WALNUT_PLANK,
                    OAK_PANEL, BAMBOO_PANEL,
                    OBSIDIAN_TILE, COBBLESTONE, LAPIS_BRICK, BASALT_COLUMN,
                    LIMESTONE_BLOCK, COPPER_TILE, TEAK_PLANK, DRIFTWOOD_PLANK,
                    CEDAR_PANEL, JADE_PANEL,
                    ROSE_QUARTZ_BLOCK, GILDED_BRICK, AMETHYST_BLOCK, AMBER_TILE,
                    IVORY_BRICK, EBONY_PLANK, MAHOGANY_PLANK, ASH_PLANK,
                    FROSTED_GLASS, CRIMSON_BRICK,
                    TERRACOTTA_SHINGLE, THATCH_ROOF, VERDIGRIS_COPPER, SILVER_PANEL,
                    GOLD_LEAF_TRIM, STAINED_GLASS_RED, STAINED_GLASS_BLUE,
                    STAINED_GLASS_GREEN, QUARTZ_PILLAR, ONYX_INLAY,
                    STAIRS_RIGHT, STAIRS_LEFT,
                    WHITE_PLASTER_WALL, CARVED_PLASTER, MUQARNAS_BLOCK,
                    MASHRABIYA, ZELLIGE_TILE, ARABESQUE_PANEL,
                    CLAY_DEPOSIT, LIMESTONE_DEPOSIT,
                    ADOBE_BRICK, SPANISH_ROOF_TILE, WROUGHT_IRON_GRILLE,
                    TALAVERA_TILE, SALTILLO_TILE,
                    COBALT_DOOR_CLOSED, COBALT_DOOR_OPEN,
                    CRIMSON_CEDAR_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_OPEN,
                    TEAL_DOOR_CLOSED, TEAL_DOOR_OPEN,
                    SAFFRON_DOOR_CLOSED, SAFFRON_DOOR_OPEN,
                    STUDDED_OAK_DOOR_CLOSED, STUDDED_OAK_DOOR_OPEN,
                    VERMILION_DOOR_CLOSED, VERMILION_DOOR_OPEN,
                    SHOJI_DOOR_CLOSED, SHOJI_DOOR_OPEN,
                    GILDED_DOOR_CLOSED, GILDED_DOOR_OPEN,
                    BRONZE_DOOR_CLOSED, BRONZE_DOOR_OPEN,
                    SWAHILI_DOOR_CLOSED, SWAHILI_DOOR_OPEN,
                    SANDALWOOD_DOOR_CLOSED, SANDALWOOD_DOOR_OPEN,
                    STONE_SLAB_DOOR_CLOSED, STONE_SLAB_DOOR_OPEN,
                    HALF_TIMBER_WALL, ASHLAR_BLOCK, GOTHIC_TRACERY, FLUTED_COLUMN,
                    CORNICE_BLOCK, ROSE_WINDOW, HERRINGBONE_BRICK, BAROQUE_TRIM,
                    TUDOR_BEAM, VENETIAN_FLOOR, FLEMISH_BRICK, PILASTER,
                    DENTIL_TRIM, WATTLE_DAUB, NORDIC_PLANK, MANSARD_SLATE,
                    ROMAN_MOSAIC, SETT_STONE, ROMANESQUE_ARCH, DARK_SLATE_ROOF,
                    KEYSTONE, PLINTH_BLOCK, IRON_LANTERN, SANDSTONE_ASHLAR,
                    GARGOYLE_BLOCK, LIGHT_TRAP_BLOCK,
                    OGEE_ARCH, RUSTICATED_STONE, CHEVRON_STONE, TRIGLYPH_PANEL,
                    MARBLE_INLAY, BRICK_NOGGING, CRENELLATION, FAN_VAULT,
                    PORTCULLIS_BLOCK, ARROW_LOOP, MACHICOLATION, DRAWBRIDGE_PLANK,
                    ROUND_TOWER_WALL, CURTAIN_WALL, CORBEL_COURSE, TOWER_CAP,
                    GREAT_HALL_FLOOR, DUNGEON_WALL, CASTLE_FIREPLACE, HERALDIC_PANEL,
                    WALL_WALK_FLOOR, CASTLE_GATE_ARCH, DRAWBRIDGE_CHAIN, DUNGEON_GRATE,
                    MOAT_STONE, CHAPEL_STONE, MURDER_HOLE, GARDEROBE_CHUTE,
                    ACANTHUS_PANEL, PEBBLE_DASH, ENCAUSTIC_TILE, CHEQUERBOARD_MARBLE,
                    WROUGHT_IRON_BALUSTRADE, OPUS_INCERTUM, GROTESQUE_FRIEZE,
                    BARREL_VAULT, POINTED_ARCH, ENGLISH_BOND, RELIEF_PANEL,
                    DIAGONAL_TILE,
                    TAPESTRY_BLOCK, WOVEN_RUG, CELTIC_KNOTWORK, BYZANTINE_MOSAIC,
                    JAPANESE_SHOJI, OTTOMAN_TILE, LEADLIGHT_WINDOW, TUDOR_ROSE,
                    GREEK_KEY, VENETIAN_PLASTER, SCOTTISH_RUBBLE, ART_NOUVEAU_PANEL,
                    DUTCH_GABLE, STRIPED_ARCH, TIMBER_TRUSS, HEARTH_STONE,
                    LINEN_FOLD, PARQUET_FLOOR, COFFERED_CEILING, OPUS_SIGNINUM,
                    GLAZED_ROOF_TILE, LATTICE_SCREEN, MOON_GATE, PAINTED_BEAM,
                    DOUGONG, CERAMIC_PLANTER, STONE_LANTERN, LACQUER_PANEL,
                    PAPER_LANTERN, DRAGON_TILE, HAN_BRICK, PAVILION_FLOOR,
                    BAMBOO_SCREEN, CLOUD_MOTIF, COIN_TILE, BLUE_WHITE_TILE,
                    GARDEN_ROCK, STEPPED_WALL, PAGODA_EAVE, CINNABAR_WALL,
                    WHITEWASHED_WALL, MONASTERY_ROOF, MANI_STONE, PRAYER_FLAG_BLOCK,
                    MUGHAL_ARCH, PIETRA_DURA, EGYPTIAN_FRIEZE, SANDSTONE_COLUMN,
                    AZTEC_SUNSTONE, MAYA_RELIEF, VIKING_CARVING, RUNE_STONE,
                    PERSIAN_IWAN, KILIM_TILE, AFRICAN_MUD_BRICK, KENTE_PANEL,
                    WAT_FINIAL, KHMER_STONE, HANJI_SCREEN, DANCHEONG,
                    ART_DECO_PANEL, OBSIDIAN_CUT, OTTOMAN_ARCH, LOTUS_CAPITAL,
                    AZULEJO_TILE, MANUELINE_PANEL, TORII_PANEL, INCA_ASHLAR,
                    RUSSIAN_KOKOSHNIK, ONION_DOME_TILE, GEORGIAN_FANLIGHT, PALLADIAN_WINDOW,
                    STAVE_PLANK, IONIC_CAPITAL, MOORISH_STAR_TILE, CRAFTSMAN_PANEL,
                    BRUTALIST_PANEL, METOPE, ARMENIAN_KHACHKAR, BENIN_RELIEF,
                    MAORI_CARVING, MUGHAL_JALI, PERSIAN_TILE, SWISS_CHALET,
                    ANDEAN_TEXTILE, BAROQUE_ORNAMENT, POLYNESIAN_CARVED,
                    MOORISH_COLUMN, PORTUGUESE_CORK,
                    FLAX_BUSH, FLAX_CROP_YOUNG, FLAX_CROP_MATURE,
                    COTTON_BUSH, COTTON_CROP_YOUNG, COTTON_CROP_MATURE,
                    SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
                    TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
                    TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
                    TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY,
                    TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON,
                    TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
                    TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY,
                    LIMESTONE_STONE, GRANITE_STONE, BASALT_STONE, MAGMATIC_STONE, SMELTER_BLOCK,
                    TUMBLER_BLOCK, CRUSHER_BLOCK, GEM_CUTTER_BLOCK, KILN_BLOCK, RESONANCE_BLOCK,
                    DESERT_FORGE_BLOCK, ROASTER_BLOCK, BLEND_STATION_BLOCK, BREW_STATION_BLOCK,
                    FOSSIL_TABLE_BLOCK, ARTISAN_BENCH_BLOCK,
                    GRAPE_PRESS_BLOCK, FERMENTATION_BLOCK, WINE_CELLAR_BLOCK,
                    STILL_BLOCK, BARREL_ROOM_BLOCK, BOTTLING_BLOCK, COMPOST_BIN_BLOCK,
                    STABLE_BLOCK, HORSE_TROUGH_BLOCK,
                    WITHERING_RACK_BLOCK, OXIDATION_STATION_BLOCK, TEA_CELLAR_BLOCK,
                    DRYING_RACK_BLOCK, BAIT_STATION_BLOCK,
                    EVAPORATION_PAN_BLOCK, SALT_GRINDER_BLOCK,
                    DAIRY_VAT_BLOCK, CHEESE_PRESS_BLOCK, AGING_CAVE_BLOCK,
                    FLETCHING_TABLE_BLOCK, ANAEROBIC_TANK_BLOCK,
                    JEWELRY_WORKBENCH_BLOCK, SCULPTORS_BENCH,
                    GLASS_KILN_BLOCK,
                    CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON,
                    STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET,
                    STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY,
                    CATHEDRAL_WINDOW, MOSAIC_GLASS, SMOKED_GLASS,
                    RIBBED_GLASS, HAMMERED_GLASS, CRACKLED_GLASS,
                    OCULUS_WINDOW, LANCET_WINDOW, DIAMOND_PANE,
                    SEA_GLASS, MIRROR_GLASS, IRIDESCENT_GLASS,
                    SUNSET_GLASS, OBSIDIAN_GLASS, CRYSTAL_GLASS,
                    ELEVATOR_CABLE_BLOCK, ELEVATOR_STOP_BLOCK,
                    GARDEN_WORKSHOP_BLOCK,
                    ZELLIGE_BLUE, ZELLIGE_TERRACOTTA, ZELLIGE_EMERALD, ZELLIGE_WHITE,
                    GARDEN_STAR_TILE, GEOMETRIC_MOSAIC,
                    WATER_CHANNEL, ORNAMENTAL_POOL, FOUNTAIN_BASIN, TIERED_FOUNTAIN,
                    HORSESHOE_ARCH, MUQARNAS_PANEL, ARABESQUE_SCREEN,
                    GARDEN_COLUMN, MARBLE_PLINTH, GARDEN_OBELISK,
                    TOPIARY_CONE, TOPIARY_SPHERE, BOX_HEDGE, CLIMBING_ROSE,
                    STONE_BENCH, STONE_URN, TERRACOTTA_PLANTER, SUNDIAL, GARDEN_LANTERN,
                    GRAVEL_PATH, MOSAIC_PATH, TERRACOTTA_PATH, COBBLE_CIRCLE,
                    SCULPTURE_BLOCK_ROOT, SCULPTURE_BLOCK_BODY,
                    CUSTOM_TAPESTRY_ROOT, CUSTOM_TAPESTRY_BODY,
                    PERGOLA_POST, WISTERIA_ARCH, GARDEN_GATE, LOW_GARDEN_WALL, POOL_COPING,
                    STEPPING_STONE, OPUS_VERMICULATUM, PORPHYRY_TILE, BRICK_EDGING,
                    SPIRAL_TOPIARY, MAZE_HEDGE, WISTERIA_WALL, POTTED_CITRUS,
                    MARBLE_STATUE, MARBLE_BIRDBATH, GARDEN_TABLE, IRON_TRELLIS,
                    NASRID_PANEL, SCALLOP_NICHE, TERRACE_BALUSTRADE,
                    ZEN_GRAVEL, KARESANSUI_ROCK, MOSS_CARPET, TSUKUBAI,
                    TORO_LANTERN, YUKIMI_LANTERN, BAMBOO_FENCE_JP, ROJI_STONE,
                    PINE_TOPIARY_JP, JAPANESE_MAPLE, SHISHI_ODOSHI, RED_ARCH_BRIDGE,
                    WAVE_CERAMIC, ZEN_SAND_RING, BAMBOO_GATE_JP, WABI_STONE,
                    CHERRY_ARCH, TATAMI_PAVING, IKEBANA_STONE, KANJI_STONE,
                    MAPLE_LEAF_TILE, NOREN_PANEL, TSURU_TILE, PINE_SCREEN_JP, KARE_BRIDGE,
                    PEBBLE_MOSAIC_CN, ZIGZAG_BRIDGE, CLOUD_WALL, DRAGON_WALL_CN,
                    LOTUS_POND, HEX_PAVILION_TILE, COMPASS_PAVING, WAVE_BALUSTRADE_CN,
                    CERAMIC_SEAT, BONSAI_TRAY, SCHOLAR_SCREEN,
                    CHRYSANTHEMUM_TILE, PLUM_BLOSSOM_TILE, MOON_PAVEMENT,
                    BAMBOO_GROVE, OSMANTHUS_BUSH, WATER_LILY_TILE, KOI_POND,
                    LAKESIDE_ROCK, CLOUD_COLLAR_TILE, IMPERIAL_PAVING,
                    PAVILION_COLUMN_CN, EIGHT_DIAGRAM, TEA_HOUSE_STEP, LANTERN_FESTIVAL,
                    IONIC_COLUMN_BASE, DORIC_ENTABLATURE, RUSTICATED_BASE, GARDEN_LOGGIA,
                    TRIUMPHAL_ARCH_R, EXEDRA_SEAT, HERM_PILLAR, NYMPHAEUM_PANEL,
                    GROTTO_STONE, AMPHITHEATER_TIER,
                    GIOCHI_ACQUA, RILL_BLOCK, CASCADE_BLOCK, GROTTO_POOL, WALL_FOUNTAIN,
                    BASIN_SURROUND, CANAL_BLOCK, TERME_POOL,
                    PARTERRE_BRODERIE, PARTERRE_COMPARTMENT, ALLEE_TREE, PLEACHED_HEDGE,
                    ESPALIER_WALL, KNOT_GARDEN, TURF_THEATER, CARPET_BED,
                    OPUS_SECTILE, TRAVERTINE_FLOOR, HERRINGBONE_GARDEN, RAMP_STONE,
                    GARDEN_STEPS, SAND_ALLEE, PATTERNED_PAVEMENT, INLAID_MARBLE,
                    TALL_SUNDIAL, STONE_VASE, STONE_SPHERE, CURVED_BENCH, ORNATE_GATE,
                    LEAD_PLANTER, TERRACE_URN, STONE_PINEAPPLE,
                    GROTTO_ARCH, PERGOLA_BEAM, LOGGIA_ARCH, GARDEN_WALL_NICHE,
                    ORANGERY_WINDOW, BELVEDERE_PANEL, BOSCO_TREE, GIARDINO_SEGRETO,
                    MARBLE_VEIN, ALABASTER_VEIN, VERDITE_VEIN, ONYX_VEIN,
                    ALABASTER_BLOCK, VERDITE_BLOCK, ONYX_BLOCK,
                    PIETRA_SERENA, TRAVERTINE_WALL, MARBLE_FACADE, RUSTICATED_QUOIN,
                    BICOLOR_MARBLE, PINK_GRANITE_BASE, BLIND_ARCH, CONSOLE_CORNICE,
                    CORINTHIAN_CAPITAL, GIANT_PILASTER, ENGAGED_COLUMN, ATLAS_FIGURE,
                    CARYATID_COLUMN, COMPOSITE_CAPITAL,
                    INTARSIA_PANEL, STUDIOLO_WALL, GILT_LEATHER, FRESCO_LUNETTE,
                    WAINSCOT_MARBLE, TAPESTRY_FRAME,
                    LACUNAR_CEILING, BARREL_FRESCO, GOLDEN_CEILING, GROTESQUE_VAULT, CUPOLA_OCULUS,
                    COSMATESQUE_FLOOR, TERRAZZO_FLOOR_REN, OPUS_ALEXANDRINUM,
                    MARBLE_MEDALLION_REN, PALACE_FLOOR_TILE,
                    PALACE_PORTAL, AEDICULE_FRAME, THERMAL_WINDOW, BIFORA_WINDOW,
                    SERLIANA_WINDOW, PALAZZO_BALCONY,
                    ROMAN_ARCH_REN, BARREL_VAULT_COFFER, PENDENTIVE_BLOCK, GROIN_VAULT,
                    RENAISSANCE_MANTEL, CHIMNEY_BREAST_REN, PEDIMENTED_NICHE, SHELL_NICHE_REN,
                    CARTOUCHE_REN, PUTTI_FRIEZE, FESTOON_PANEL, TROPHY_PANEL_REN,
                    MEDALLION_PORTRAIT, LAUREL_FRIEZE,
                    POTTERY_WHEEL_BLOCK, POTTERY_KILN_BLOCK, POTTERY_DISPLAY_BLOCK,
                    CALCADA_PORTUGUESA, AZULEJO_GEOMETRIC, PAINTED_TILE_BORDER,
                    SPANISH_MAJOLICA, AZULEJO_STAIR,
                    PORTUGUESE_PINK_MARBLE, SPANISH_HEX_TILE, MUDEJAR_STAR_TILE,
                    ALBARRADA_PANEL, SGRAFFITO_WALL, TRENCADIS_PANEL,
                    AZULEJO_NAVY, AZULEJO_MANGANESE, PLATERESQUE_PANEL, AZULEJO_CORNICE,
                    TALAVERA_FOUNTAIN, BARCELONA_TILE, MOORISH_ARCHWAY_TILE,
                    PORTUGUESE_CHIMNEY, BARCELOS_TILE, REJA_PANEL,
                    ORANGE_TREE_PLANTER, WAVE_COBBLE, AZULEJO_FACADE_PANEL,
                    MUDEJAR_BRICK, PORTUGUESE_BENCH, SPANISH_PATIO_FLOOR,
                    ARABIC_ROOF_TILE, MOORISH_COLUMN_TILE, ESTREMOZ_MARBLE,
                    MEZQUITA_ARCH, MIHRAB_TILE, MEDINA_AZAHARA_STONE, CORDOBA_COLUMN,
                    ORANGE_COURT_FLOOR, CORDOBAN_LEATHER, UMAYYAD_MULTILOBED,
                    GOLD_TESSERA_PANEL, UMAYYAD_DOME_RIB, KUFIC_PANEL,
                    PATIO_FLOWER_WALL, CORDOBAN_PATIO_TILE, STAR_VAULT_PANEL,
                    ANDALUSIAN_FOUNTAIN, NASRID_HONEYCOMB,
                    GARDEN_BLOCK,
                    MCM_CONCRETE_PANEL, MCM_BREEZE_BLOCK, MCM_BOARD_BATTEN, MCM_WALNUT_PANEL,
                    MCM_TEAK_PANEL, MCM_ROMAN_BRICK, TERRAZZO_FLOOR_MCM, TRAVERTINE_FLOOR_MCM,
                    QUARRY_TILE, FLAGSTONE_PATIO, MCM_PARQUET, CORK_FLOOR_TILE,
                    AVOCADO_TILE, HARVEST_GOLD_TILE, BURNT_ORANGE_TILE, TURQUOISE_TILE,
                    PLATE_GLASS_PANEL, TINTED_GLASS_PANEL, RIBBED_GLASS_MCM,
                    BRASS_TRIM_PANEL, COPPER_SCREEN_MCM, ANODIZED_ALUMINUM,
                    RATTAN_SCREEN_MCM, SPLIT_BAMBOO_PANEL, LAVA_ROCK_WALL,
                    MCM_TONGUE_GROOVE, BUTTERFLY_BEAM, STARBURST_PANEL,
                    STACKED_STONE_VENEER, FIBERGLASS_SHELL,
                    MINE_TRACK_BLOCK, MINE_TRACK_STOP_BLOCK,
                    ORNAMENTAL_GRASS, FLOWERING_SHRUB, HOLLY_SHRUB,
                    TOPIARY_PEACOCK, TOPIARY_BEAR, TOPIARY_RABBIT,
                    ROSE_BED, TULIP_BED, COTTAGE_GARDEN_BED,
                    CHERUB_FOUNTAIN, LION_HEAD_FOUNTAIN, MOSAIC_FOUNTAIN,
                    LAVENDER_BED, SUNFLOWER_BED, DAHLIA_BED,
                    TOPIARY_SWAN, TOPIARY_FOX, TOPIARY_ELEPHANT,
                    PEONY_BUSH, FERN_CLUMP, RAISED_GARDEN_BED,
                    LILY_PAD_POND, BEE_SKEP, GARDEN_WHEELBARROW,
                    IRIS_BED, POPPY_BED, FOXGLOVE_PATCH, SNOWDROP_PATCH, MARIGOLD_BED,
                    BOXWOOD_BALL, RHODODENDRON_BUSH, BAMBOO_CLUMP, AGAPANTHUS_PATCH,
                    TOPIARY_DRAGON, TOPIARY_GIRAFFE, TOPIARY_HEDGEHOG,
                    BUBBLE_FOUNTAIN, SHELL_FOUNTAIN, MILLSTONE_FOUNTAIN,
                    TRELLIS_ARCH, COLD_FRAME, GARDEN_SWING, WICKER_FENCE,
                    HANGING_BASKET, STANDARD_ROSE, GARDEN_GNOME, TOPIARY_ARCH,
                    CHAMOMILE_LAWN, CREEPING_THYME,
                    HYDRANGEA_BUSH, ALLIUM_PATCH, SWEET_PEA_TRELLIS,
                    BLEEDING_HEART_PATCH, ASTILBE_PATCH, WISTERIA_PILLAR,
                    TOPIARY_SNAIL, TOPIARY_MUSHROOM, TOPIARY_OWL, TOPIARY_DINOSAUR,
                    KOI_POOL, STONE_TROUGH_PLANTER, RAIN_BARREL,
                    MOSS_PATCH, CLOVER_LAWN, BARK_MULCH,
                    STONE_FROG, GARDEN_DOVECOTE, STONE_HEDGEHOG, BIRD_TABLE,
                    GARDEN_CLOCK, GARDEN_OBELISK_METAL, POTTING_TABLE,
                    COMPOST_HEAP, GARDEN_TOAD_HOUSE,
                    ALPINE_BALCONY_RAIL, DARK_TIMBER_BEAM, ROUGH_STONE_WALL,
                    ALPINE_PLASTER, FLOWER_BOX, FIREWOOD_STACK, SLATE_SHINGLE,
                    CARVED_SHUTTER, BEAR_HIDE, ALPINE_HERB_RACK, HAY_BALE,
                    PINE_PLANK_WALL, GRANITE_ASHLAR, CUCKOO_CLOCK, GERANIUM_BOX,
                    ARCH_STONE, SWISS_PANEL, COPPER_COWBELL, WOODEN_GEAR,
                    STONE_BASIN, MILK_CHURN, ALPINE_CHEST, ALPINE_LANTERN,
                    WROUGHT_IRON_RAIL, ALPINE_CHANDELIER, WOVEN_TEXTILE,
                    COWBELL_RACK, ALPINE_STUCCO, CARVED_LINTEL, CHALET_DOOR,
                    CERAMIC_TILE_STOVE, CARVED_BARGEBOARD, DORMER_WINDOW,
                    WOODEN_SHINGLE, STONE_STEP, WATER_TROUGH, CARVED_BENCH,
                    CHEESE_WHEEL, ANTLER_MOUNT, EDELWEISS_WREATH, BOOT_RACK,
                    TALLOW_CANDLE, ALPINE_HEARTH, PINE_CONE_GARLAND,
                    IRON_HOOK_RACK, ALPINE_GATE, BUTTER_CHURN, CARVED_WAINSCOT,
                    CHIMNEY_CAP, FEATHER_DUVET,
                    GREEK_AMPHORA, KRATER, HYDRIA, LEKYTHOS, STORAGE_PITHOS,
                    KLINE, TRIPOD_BRAZIER, OLIVE_PRESS, LOOM_FRAME, MEANDER_BORDER,
                    SYMPOSIUM_TABLE, VOTIVE_TABLET, BRONZE_CUIRASS_STAND, CHARIOT_WHEEL,
                    TERRACOTTA_ROOF_TILE, ATTIC_VASE, GREEK_STONE_BENCH, STONE_ALTAR,
                    BRONZE_MIRROR, CLAY_OIL_LAMP, AGORA_SCALE, LAUREL_WREATH_MOUNT,
                    HERMES_STELE, DORIC_CAPITAL, VICTORY_STELE, BRONZE_SHIELD_MOUNT,
                    EGG_AND_DART, OLIVE_BRANCH, PHILOSOPHERS_SCROLL, GREEK_THEATRE_MASK,
                    TORCH, WALL_SCONCE, BRAZIER, CHANDELIER, CANDELABRA,
                    LANTERN_ORB, PENDANT_LAMP, FIRE_BOWL, CROSS_LANTERN,
                    STAR_LAMP, GLOW_VINE, LIGHT_EMITTERS,
                    TOWN_FLAG_BLOCK, OUTPOST_FLAG_BLOCK, LANDMARK_FLAG_BLOCK,
                    REED_BLOCK, CATTAIL_BLOCK, BULRUSH_BLOCK,
                    WATER_CRESS_BLOCK, POND_WEED_BLOCK,
                    WATER_HYACINTH_BLOCK, DUCKWEED_BLOCK, LOTUS_BLOCK, FROGBIT_BLOCK,
                    ARROWHEAD_BLOCK, HORSETAIL_BLOCK, MARSH_MARIGOLD_BLOCK,
                    WATER_IRIS_BLOCK, SEDGE_BLOCK, PICKERELWEED_BLOCK,
                    ICE_SHARD, FROZEN_BOG, STONE_BRIDGE)
import math
import soil as _soil
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, PLAYER_W, PLAYER_H, ROCK_WARM_ZONE
from biomes import BIOME_STONE_COLORS


_SHIMMER_BLOCKS = {
    CRYSTAL_ORE:  (200, 255, 255),
    RUBY_ORE:     (255, 190, 190),
    GEM_DEPOSIT:  (230, 200, 255),
    CAVE_CRYSTAL: (190, 250, 255),
}


def _los_clear(world, px, py, tx, ty):
    """DDA grid walk: True if only AIR blocks lie between player block and target block."""
    dx = tx - px
    dy = ty - py
    nx = abs(dx)
    ny = abs(dy)
    sign_x = 1 if dx > 0 else -1
    sign_y = 1 if dy > 0 else -1
    x, y = px, py
    ix = iy = 0
    while ix < nx or iy < ny:
        step_x = (0.5 + ix) / nx if nx else float('inf')
        step_y = (0.5 + iy) / ny if ny else float('inf')
        if step_x < step_y:
            x += sign_x
            ix += 1
        else:
            y += sign_y
            iy += 1
        if x == tx and y == ty:
            break
        if world.get_block(x, y) != AIR:
            return False
    return True


from Render.block_helpers import _darken, _lighter, _tinted, _MSTYLES, render_mushroom_preview


from Render.hud import _MM_W, _MM_H, _MM_MARGIN


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.cam_x = 0.0
        self.cam_y = 0.0
        self._block_surfs = self._build_block_surfs()
        self._tilled_soil_surfs = self._build_tilled_soil_surfs()
        self._water_surfs = self._build_water_surfs()   # indexed by level-1 (0..7)
        self._resource_hint_surfs = self._build_resource_hint_surfs()
        self._biome_stone_surfs = self._build_biome_stone_surfs()
        self._biome_resource_hint_surfs = self._build_biome_resource_hint_surfs()
        self._log_variants          = self._build_log_variants()
        self._leaf_variants         = self._build_leaf_variants()
        self._fruit_cluster_variants = self._build_fruit_cluster_variants()
        self._grass_variants = self._build_grass_variants()
        self._dirt_variants  = self._build_dirt_variants()
        self._sand_variants  = self._build_sand_variants()
        self._snow_variants  = self._build_snow_variants()
        self._bg_darken_surf = self._build_bg_darken_surf()
        self._bg_block_surfs = self._build_bg_block_surfs()
        self._cave_wall_surf = self._build_cave_wall_surf()
        self._light_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        self._light_gradient = None
        self._light_cache_key = None
        self._sky_surf = self._build_sky_surf()
        self._sky_night_surf = self._build_night_sky_surf()
        self.show_all_resources = True
        self._water_overlay_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        self._water_overlay_surf.fill((30, 80, 180, 70))
        self._ghost_surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        self._ghost_color_key = None
        self._mine_overlay = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        self._npc_font = pygame.font.SysFont("consolas", 14)
        self._minimap_surf  = None
        self._minimap_timer = 0.0
        self.minimap_visible = False
        self._mm_ctable     = self._build_mm_color_table()
        self._floating_texts = []  # list of {x, y, text, color, life, vy}
        self._light_grad_cache = {}  # (radius, pattern, flicker_frame) -> Surface
        self._town_flag_surfs   = {}  # region_id -> Surface (colored pennant, built lazily)
        self._outpost_flag_surfs = {}  # outpost_type -> Surface (colored pennant, built lazily)

    def _build_bg_darken_surf(self):
        from Render.surface.surfaceAndCamera import build_bg_darken_surf
        return build_bg_darken_surf()

    def _build_bg_block_surfs(self):
        from Render.surface.surfaceAndCamera import build_bg_block_surfs
        return build_bg_block_surfs(self._block_surfs, self._bg_darken_surf)

    def _build_cave_wall_surf(self):
        from Render.surface.surfaceAndCamera import build_cave_wall_surf
        return build_cave_wall_surf()

    def _build_tilled_soil_surfs(self):
        from Render.surface.surfaceAndCamera import build_tilled_soil_surfs
        return build_tilled_soil_surfs()

    def _build_block_surfs(self):
        from Render.blockRenderHandler import build_all_block_surfs
        return build_all_block_surfs()

    def _build_water_surfs(self):
        from Render.surface.biome import build_water_surfs
        return build_water_surfs()

    def _build_resource_hint_surfs(self):
        from Render.surface.biome import build_resource_hint_surfs
        return build_resource_hint_surfs()

    def _build_biome_resource_hint_surfs(self):
        from Render.surface.biome import build_biome_resource_hint_surfs
        return build_biome_resource_hint_surfs()

    def _build_biome_stone_surfs(self):
        from Render.surface.biome import build_biome_stone_surfs
        return build_biome_stone_surfs()

    def _get_town_flag_surf(self, region_id, flag_col):
        from Render.surface.flags import get_town_flag_surf
        return get_town_flag_surf(self._town_flag_surfs, region_id, flag_col)

    def _get_outpost_flag_surf(self, outpost_type, flag_col):
        from Render.surface.flags import get_outpost_flag_surf
        return get_outpost_flag_surf(self._outpost_flag_surfs, outpost_type, flag_col)

    def _build_log_variants(self):
        from Render.surface.terrain import build_log_variants
        return build_log_variants()

    def _build_leaf_variants(self):
        from Render.surface.terrain import build_leaf_variants
        return build_leaf_variants()

    def _build_fruit_cluster_variants(self):
        from Render.surface.terrain import build_fruit_cluster_variants
        return build_fruit_cluster_variants()

    def _build_grass_variants(self):
        from Render.surface.terrain import build_grass_variants
        return build_grass_variants()

    def _build_dirt_variants(self):
        from Render.surface.terrain import build_dirt_variants
        return build_dirt_variants()

    def _build_sand_variants(self):
        from Render.surface.terrain import build_sand_variants
        return build_sand_variants()

    def _build_snow_variants(self):
        from Render.surface.terrain import build_snow_variants
        return build_snow_variants()

    # ------------------------------------------------------------------
    # Camera
    # ------------------------------------------------------------------

    def update_camera(self, player, world):
        from Render.surface.surfaceAndCamera import update_camera
        self.cam_x, self.cam_y = update_camera(self.cam_x, self.cam_y, player, world)

    def _build_sky_surf(self):
        from Render.surface.flags import build_sky_surf
        return build_sky_surf()

    def _build_night_sky_surf(self):
        from Render.surface.flags import build_night_sky_surf
        return build_night_sky_surf()

    def _sky_night_alpha(self, time_of_day):
        from Render.surface.flags import sky_night_alpha
        return sky_night_alpha(time_of_day)

    # ------------------------------------------------------------------
    # Draw world
    # ------------------------------------------------------------------

    def draw_world(self, world, player=None):
        from Render.worldScene.scene import draw_world
        draw_world(self, world, player)

    def _draw_pottery_displays(self, world, cam_xi, cam_yi):
        from Render.worldScene.art import draw_pottery_displays
        draw_pottery_displays(self.screen, world, cam_xi, cam_yi)

    def _draw_sculpture_at(self, sc, root_bx, root_by):
        from Render.worldScene.art import draw_sculpture_at
        draw_sculpture_at(self.screen, self.cam_x, self.cam_y, sc, root_bx, root_by)

    def _draw_all_sculptures(self, world):
        from Render.worldScene.art import draw_all_sculptures
        draw_all_sculptures(self.screen, self.cam_x, self.cam_y, world)

    def _draw_tapestry_at(self, tp, root_bx, root_by):
        from Render.worldScene.art import draw_tapestry_at
        draw_tapestry_at(self.screen, self.cam_x, self.cam_y, tp, root_bx, root_by)

    def _draw_all_tapestries(self, world):
        from Render.worldScene.art import draw_all_tapestries
        draw_all_tapestries(self.screen, self.cam_x, self.cam_y, world)

    def _draw_garden_blocks(self, world, cam_xi, cam_yi):
        from Render.worldScene.art import draw_garden_blocks
        draw_garden_blocks(self.screen, world, cam_xi, cam_yi)

    def _draw_wildflower_displays(self, world, cam_xi, cam_yi):
        from Render.worldScene.art import draw_wildflower_displays
        draw_wildflower_displays(self.screen, world, cam_xi, cam_yi)

    # ------------------------------------------------------------------
    # Draw player
    # ------------------------------------------------------------------

    def draw_player(self, player):
        from Render.worldScene.scene import draw_player
        draw_player(self.screen, self.cam_x, self.cam_y, player)

    # ------------------------------------------------------------------
    # Draw animals
    # ------------------------------------------------------------------

    def draw_entities(self, entities):
        from Render.worldScene.scene import draw_entities
        draw_entities(self, entities)

    # ------------------------------------------------------------------
    # Huntable animal drawing
    # ------------------------------------------------------------------

    def _draw_deer(self, sx, sy, e):
        from Render.forestAnimal import draw_deer
        draw_deer(self.screen, sx, sy, e)

    def _draw_boar(self, sx, sy, e):
        from Render.forestAnimal import draw_boar
        draw_boar(self.screen, sx, sy, e)

    def _draw_rabbit(self, sx, sy, e):
        from Render.forestAnimal import draw_rabbit
        draw_rabbit(self.screen, sx, sy, e)

    def _draw_turkey(self, sx, sy, e):
        from Render.forestAnimal import draw_turkey
        draw_turkey(self.screen, sx, sy, e)

    def _draw_wolf(self, sx, sy, e):
        from Render.forestAnimal import draw_wolf
        draw_wolf(self.screen, sx, sy, e)

    def _draw_bear(self, sx, sy, e):
        from Render.forestAnimal import draw_bear
        draw_bear(self.screen, sx, sy, e)

    def _draw_duck(self, sx, sy, e):
        from Render.wetlandAnimal import draw_duck
        draw_duck(self.screen, sx, sy, e)

    def _draw_elk(self, sx, sy, e):
        from Render.wetlandAnimal import draw_elk
        draw_elk(self.screen, sx, sy, e)

    def _draw_bison(self, sx, sy, e):
        from Render.wetlandAnimal import draw_bison
        draw_bison(self.screen, sx, sy, e)

    def _draw_fox(self, sx, sy, e):
        from Render.wetlandAnimal import draw_fox
        draw_fox(self.screen, sx, sy, e)

    def _draw_arctic_fox(self, sx, sy, e):
        from Render.wetlandAnimal import draw_arctic_fox
        draw_arctic_fox(self.screen, sx, sy, e)

    def _draw_moose(self, sx, sy, e):
        from Render.wetlandAnimal import draw_moose
        draw_moose(self.screen, sx, sy, e)

    def _draw_bighorn(self, sx, sy, e):
        from Render.wetlandAnimal import draw_bighorn
        draw_bighorn(self.screen, sx, sy, e)

    def _draw_pheasant_animal(self, sx, sy, e):
        from Render.wetlandAnimal import draw_pheasant_animal
        draw_pheasant_animal(self.screen, sx, sy, e)

    def _draw_warthog(self, sx, sy, e):
        from Render.wetlandAnimal import draw_warthog
        draw_warthog(self.screen, sx, sy, e)

    def _draw_musk_ox(self, sx, sy, e):
        from Render.wetlandAnimal import draw_musk_ox
        draw_musk_ox(self.screen, sx, sy, e)

    def _draw_crocodile(self, sx, sy, e):
        from Render.wetlandAnimal import draw_crocodile
        draw_crocodile(self.screen, sx, sy, e)

    def _draw_goose(self, sx, sy, e):
        from Render.wetlandAnimal import draw_goose
        draw_goose(self.screen, sx, sy, e)

    def _draw_hare(self, sx, sy, e):
        from Render.wetlandAnimal import draw_hare
        draw_hare(self.screen, sx, sy, e)

    # ------------------------------------------------------------------
    # Arrow drawing
    # ------------------------------------------------------------------

    def draw_arrows(self, arrows):
        from Render.vehicles import draw_arrows
        draw_arrows(self.screen, arrows, self.cam_x, self.cam_y)

    @staticmethod
    def _fmt_fuel_time(fuel, fuel_rate):
        from Render.vehicles import fmt_fuel_time
        return fmt_fuel_time(fuel, fuel_rate)

    def draw_automations(self, automations):
        from Render.vehicles import draw_automations
        draw_automations(self.screen, automations, self.cam_x, self.cam_y, self._npc_font)

    def draw_farm_bots(self, farm_bots):
        from Render.vehicles import draw_farm_bots
        draw_farm_bots(self.screen, farm_bots, self.cam_x, self.cam_y, self._npc_font)

    def draw_backhoes(self, backhoes, player):
        from Render.vehicles import draw_backhoes
        draw_backhoes(self.screen, backhoes, self.cam_x, self.cam_y, self._npc_font, player)

    def draw_elevator_cars(self, elevator_cars, player=None):
        from Render.vehicles import draw_elevator_cars
        draw_elevator_cars(self.screen, elevator_cars, self.cam_x, self.cam_y, self._npc_font, player)

    def draw_minecarts(self, minecarts, player=None):
        from Render.vehicles import draw_minecarts
        draw_minecarts(self.screen, minecarts, self.cam_x, self.cam_y, self._npc_font, player)

    def _draw_backhoe(self, bh, is_mounted=False):
        from Render.vehicles import _draw_backhoe
        _draw_backhoe(self.screen, bh, self.cam_x, self.cam_y, self._npc_font, is_mounted)

    def _draw_npc_quest(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_quest
        draw_npc_quest(self.screen, sx, sy, npc, self._npc_font)

    def _draw_npc_trade(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_trade
        draw_npc_trade(self.screen, sx, sy, npc, self._npc_font)

    def _draw_npc_herbalist(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_herbalist
        draw_npc_herbalist(self.screen, sx, sy, npc)

    def _draw_npc_jeweler(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_jeweler
        draw_npc_jeweler(self.screen, sx, sy, npc)

    def _draw_npc_royal_curator(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_royal_curator
        draw_npc_royal_curator(self.screen, sx, sy, npc)

    def _draw_npc_royal_florist(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_royal_florist
        draw_npc_royal_florist(self.screen, sx, sy, npc)

    def _draw_npc_royal_jeweler(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_royal_jeweler
        draw_npc_royal_jeweler(self.screen, sx, sy, npc)

    def _draw_npc_royal_paleontologist(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_royal_paleontologist
        draw_npc_royal_paleontologist(self.screen, sx, sy, npc)

    def _draw_npc_royal_angler(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_royal_angler
        draw_npc_royal_angler(self.screen, sx, sy, npc)

    def _draw_npc_merchant(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_merchant
        draw_npc_merchant(self.screen, sx, sy, npc)

    def _draw_npc_outpost_keeper(self, sx, sy, npc):
        from Render.Servicenpcs import draw_npc_outpost_keeper
        draw_npc_outpost_keeper(self.screen, sx, sy, npc)

    def _draw_npc_soldier(self, sx, sy, npc):
        from Render.Workernpcs import draw_npc_soldier
        draw_npc_soldier(self.screen, sx, sy, npc)


    def _draw_npc_chef(self, sx, sy, npc):
        from Render.Workernpcs import draw_npc_chef
        draw_npc_chef(self.screen, sx, sy, npc, self._npc_font)

    def _draw_npc_monk(self, sx, sy, npc):
        from Render.Workernpcs import draw_npc_monk
        draw_npc_monk(self.screen, sx, sy, npc)

    def _draw_npc_leader(self, sx, sy, npc):
        from Render.Workernpcs import draw_npc_leader
        draw_npc_leader(self.screen, sx, sy, npc)

    def _draw_npc_farmer(self, sx, sy, npc):
        from Render.Workernpcs import draw_npc_farmer
        draw_npc_farmer(self.screen, sx, sy, npc)

    def _draw_npc_villager(self, sx, sy, npc):
        from Render.Workernpcs import draw_npc_villager
        draw_npc_villager(self.screen, sx, sy, npc)

    def _draw_npc_settler(self, sx, sy, npc):
        from Render.Workernpcs import draw_npc_settler
        draw_npc_settler(self.screen, sx, sy, npc)

    def _draw_npc_child(self, sx, sy, npc):
        from Render.Workernpcs import draw_npc_child
        draw_npc_child(self.screen, sx, sy, npc)

    def _draw_npc_guard(self, sx, sy, npc):
        from Render.Guardsystem import draw_npc_guard
        draw_npc_guard(self.screen, sx, sy, npc)

    def _draw_npc_elder(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_elder
        draw_npc_elder(self.screen, sx, sy, npc)

    def _draw_npc_beggar(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_beggar
        draw_npc_beggar(self.screen, sx, sy, npc)

    def _draw_npc_noble(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_noble
        draw_npc_noble(self.screen, sx, sy, npc)

    def _draw_npc_pilgrim(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_pilgrim
        draw_npc_pilgrim(self.screen, sx, sy, npc)

    def _draw_npc_drunkard(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_drunkard
        draw_npc_drunkard(self.screen, sx, sy, npc)

    def _draw_npc_blacksmith(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_blacksmith
        draw_npc_blacksmith(self.screen, sx, sy, npc)

    def _draw_npc_innkeeper(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_innkeeper
        draw_npc_innkeeper(self.screen, sx, sy, npc)

    def _draw_npc_scholar(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_scholar
        draw_npc_scholar(self.screen, sx, sy, npc)

    def _draw_npc_royal_spouse(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_royal_spouse
        draw_npc_royal_spouse(self.screen, sx, sy, npc)

    def _draw_npc_royal_child(self, sx, sy, npc):
        from Render.Socialnpcs import draw_npc_royal_child
        draw_npc_royal_child(self.screen, sx, sy, npc)

    def _draw_sheep(self, sx, sy, sheep):
        from Render.farmanimal import draw_sheep
        draw_sheep(self.screen, sx, sy, sheep)

    def _draw_goat(self, sx, sy, goat):
        from Render.farmanimal import draw_goat
        draw_goat(self.screen, sx, sy, goat)

    def _draw_cow(self, sx, sy, cow):
        from Render.farmanimal import draw_cow
        draw_cow(self.screen, sx, sy, cow)

    def _draw_chicken(self, sx, sy, chicken):
        from Render.farmanimal import draw_chicken
        draw_chicken(self.screen, sx, sy, chicken)

    def _draw_horse(self, sx, sy, horse):
        from Render.largeAnimal import draw_horse
        draw_horse(self.screen, sx, sy, horse)

    def _draw_dog(self, sx, sy, dog):
        from Render.largeAnimal import draw_dog
        draw_dog(self.screen, sx, sy, dog, self._npc_font)

    def _draw_snow_leopard(self, sx, sy, cat):
        from Render.largeAnimal import draw_snow_leopard
        draw_snow_leopard(self.screen, sx, sy, cat)

    def _draw_mountain_lion(self, sx, sy, cat):
        from Render.largeAnimal import draw_mountain_lion
        draw_mountain_lion(self.screen, sx, sy, cat)

    def _draw_tiger(self, sx, sy, cat):
        from Render.largeAnimal import draw_tiger
        draw_tiger(self.screen, sx, sy, cat)

    def _draw_capybara(self, sx, sy, cap):
        from Render.farmanimal import draw_capybara
        draw_capybara(self.screen, sx, sy, cap)

    # ------------------------------------------------------------------
    # Mining highlight
    # ------------------------------------------------------------------

    def draw_mining_indicator(self, player):
        from Render.hud import draw_mining_indicator as _draw_mining_indicator
        _draw_mining_indicator(self.screen, self.cam_x, self.cam_y, self._mine_overlay, player)

    # ------------------------------------------------------------------
    # Placement ghost
    # ------------------------------------------------------------------

    def draw_place_indicator(self, player):
        from Render.hud import draw_place_indicator as _draw_place_indicator
        _draw_place_indicator(self, player)

    # ------------------------------------------------------------------
    # Floating harvest text
    # ------------------------------------------------------------------

    def add_float_text(self, world_x, world_y, text, color):
        from Render.hud import add_float_text as _add_float_text
        _add_float_text(self._floating_texts, world_x, world_y, text, color)

    def tick_float_texts(self, dt):
        from Render.hud import tick_float_texts as _tick_float_texts
        self._floating_texts = _tick_float_texts(self._floating_texts, dt)

    def draw_float_texts(self):
        from Render.hud import draw_float_texts as _draw_float_texts
        _draw_float_texts(self.screen, self.cam_x, self.cam_y, self._floating_texts, self._npc_font)

    # ------------------------------------------------------------------
    # Farm sense: readiness indicator on targeted crop blocks
    # ------------------------------------------------------------------

    def draw_farm_sense(self, player, world):
        from Render.hud import draw_farm_sense as _draw_farm_sense
        _draw_farm_sense(self.screen, self.cam_x, self.cam_y, player, world, self._npc_font)

    def draw_logic_help(self, player, world):
        from Render.hud import draw_logic_help as _draw_logic_help
        _draw_logic_help(self.screen, self.cam_x, self.cam_y, player, world, self._npc_font)

    # ------------------------------------------------------------------
    # Water submersion overlay
    # ------------------------------------------------------------------

    def draw_water_overlay(self, player):
        from Render.hud import draw_water_overlay as _draw_water_overlay
        _draw_water_overlay(self.screen, self._water_overlay_surf, player)

    def draw_rain(self, world):
        from Render.hud import draw_rain as _draw_rain
        _draw_rain(self.screen, self.cam_x, world)

    # ------------------------------------------------------------------
    # Lighting
    # ------------------------------------------------------------------

    def _build_block_gradient(self, pattern, radius, flicker_frame=0):
        from Render.lights import build_block_gradient
        return build_block_gradient(pattern, radius, flicker_frame)

    def draw_lighting(self, player, world, depth, time_of_day=0.0):
        from Render.lights import draw_lighting as _draw_lighting
        _draw_lighting(self, player, world, depth, time_of_day)

    # ------------------------------------------------------------------
    # Mini-map
    # ------------------------------------------------------------------

    def _build_mm_color_table(self):
        from Render.hud import build_mm_color_table
        return build_mm_color_table()

    def _rebuild_minimap(self, world):
        from Render.hud import rebuild_minimap
        rebuild_minimap(self, world)

    def draw_minimap(self, world, player, dt):
        from Render.hud import draw_minimap as _draw_minimap
        _draw_minimap(self, world, player, dt)

    def draw_dropped_items(self, dropped_items):
        from Render.hud import draw_dropped_items as _draw_dropped_items
        _draw_dropped_items(self.screen, self.cam_x, self.cam_y, dropped_items, self._npc_font)

    # ------------------------------------------------------------------
    # Birds
    # ------------------------------------------------------------------

    def draw_birds(self, birds):
        from Render.birds import draw_birds as _draw_birds
        _draw_birds(self.screen, self.cam_x, self.cam_y, birds)

    def draw_nests(self, nests):
        from Render.birds import draw_nests as _draw_nests
        _draw_nests(self.screen, self.cam_x, self.cam_y, nests)

    def _draw_bird(self, bird, sx, sy):
        from Render.birds import _draw_bird as _db
        _db(self.screen, bird, sx, sy)

    # ------------------------------------------------------------------
    # Insects
    # ------------------------------------------------------------------

    def draw_insects(self, insects, time_of_day=0.0):
        from Render.insects import draw_insects as _draw_insects
        night_alpha = self._sky_night_alpha(time_of_day)
        _draw_insects(self.screen, self.cam_x, self.cam_y, insects, night_alpha, time_of_day)

