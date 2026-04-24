import pygame
from blocks import (BLOCKS, AIR, COAL_ORE, LADDER, STONE, WATER,
                    YOUNG_CROP_BLOCKS, MATURE_CROP_BLOCKS,
                    RESOURCE_BLOCKS, ALL_LOGS, ALL_LEAVES,
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
                    WILDFLOWER_PATCH,
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
                    HALF_TIMBER_WALL, ASHLAR_BLOCK, GOTHIC_TRACERY, FLUTED_COLUMN,
                    CORNICE_BLOCK, ROSE_WINDOW, HERRINGBONE_BRICK, BAROQUE_TRIM,
                    TUDOR_BEAM, VENETIAN_FLOOR, FLEMISH_BRICK, PILASTER,
                    DENTIL_TRIM, WATTLE_DAUB, NORDIC_PLANK, MANSARD_SLATE,
                    ROMAN_MOSAIC, SETT_STONE, ROMANESQUE_ARCH, DARK_SLATE_ROOF,
                    KEYSTONE, PLINTH_BLOCK, IRON_LANTERN, SANDSTONE_ASHLAR,
                    GARGOYLE_BLOCK,
                    OGEE_ARCH, RUSTICATED_STONE, CHEVRON_STONE, TRIGLYPH_PANEL,
                    MARBLE_INLAY, BRICK_NOGGING, CRENELLATION, FAN_VAULT,
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
                    SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
                    TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
                    TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
                    TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY,
                    TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON,
                    TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
                    TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
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


def _darken(color, amount=25):
    return tuple(max(0, c - amount) for c in color)


def _lighter(color, amt=25):
    return tuple(min(255, v + amt) for v in color)


def _tinted(base_color, shift):
    """Apply float shift tuple (-0.25..0.25) per channel to an RGB color."""
    return tuple(max(0, min(255, int(base_color[i] + shift[i] * 255))) for i in range(3))


# Mushroom style table: shape, cap_col, stem_col, spots [(x,y,r)…]|None, extra|None
_MSTYLES = {
    CAVE_MUSHROOM:   ("dome",     (200, 55,  55),  (235,225,200), [(8,13,2),(15,11,2),(21,14,2)], None),
    EMBER_CAP:       ("dome",     (220,100,  30),  (220,200,170), None,                           None),
    PALE_GHOST:      ("dome",     (225,215, 235),  (240,235,245), [(10,14,1),(16,11,1),(20,15,1)],None),
    GOLD_CHANTERELLE:("dome",     (218,175,  40),  (235,220,160), [(9,13,2),(16,11,2),(21,14,2)], None),
    COBALT_CAP:      ("dome",     ( 45, 80, 185),  (160,175,210), [(9,13,2),(16,12,2),(21,14,2)], None),
    MOSSY_CAP:       ("dome",     ( 85,115,  55),  (120, 95, 60), [(8,14,2),(15,12,2),(22,13,2)], None),
    VIOLET_CROWN:    ("dome",     (130, 55, 175),  (200,180,215), [(8,13,2),(15,11,2),(21,14,2)], None),
    BLOOD_CAP:       ("dome",     (145, 18,  18),  (180,150,140), None,                           None),
    SULFUR_DOME:     ("dome",     (210,200,  30),  (235,230,190), [(8,14,2),(16,11,2),(22,13,2)], None),
    IVORY_BELL:      ("bell",     (240,235, 215),  (245,240,225), None,                           None),
    ASH_BELL:        ("bell",     (165,155, 150),  (200,195,190), [(12,12,1),(18,15,1)],          None),
    TEAL_BELL:       ("bell",     ( 40,175, 165),  (160,220,215), [(11,12,2),(19,15,2)],          None),
    RUST_SHELF:      ("flat",     (175, 90,  35),  (155,110, 70), None,                           None),
    COPPER_SHELF:    ("flat",     ( 80,140,  90),  (110,130, 85), None,                           None),
    OBSIDIAN_SHELF:  ("flat",     ( 35, 25,  45),  ( 50, 40, 55), None,                           None),
    COAL_PUFF:       ("puffball", ( 65, 60,  65),  ( 90, 85, 85), None,                           None),
    STONE_PUFF:      ("puffball", (155,150, 145),  (180,175,170), None,                           None),
    AMBER_PUFF:      ("puffball", (195,140,  45),  (215,185,130), None,                           None),
    SULFUR_TUFT:     ("cluster",  (210,200,  30),  (195,185,120), None,                           None),
    HONEY_CLUSTER:   ("cluster",  (195,145,  40),  (185,160, 90), None,                           None),
    CORAL_TUFT:      ("cluster",  (220,100, 130),  (230,185,185), None,                           None),
    BONE_STALK:      ("bell",     (240,235, 220),  (245,240,230), None,                           "tall"),
    MAGMA_CAP:       ("dome",     ( 85, 20,  15),  (100, 60, 50), None,                           "glow"),
    DEEP_INK:        ("dome",     ( 40, 20,  60),  ( 60, 40, 80), None,                           None),
    BIOLUME:         ("dome",     ( 30,210, 195),  (140,230,225), [(9,12,2),(16,10,2),(22,13,2)], None),
}


def render_mushroom_preview(bid, size=58):
    """Render a mushroom surface at `size` pixels, suitable for UI and in-world use."""
    style = _MSTYLES.get(bid)
    if not style:
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        return s
    BS = BLOCK_SIZE
    shape, cap, stem, spots, extra = style
    s = pygame.Surface((BS, BS), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    dc = _darken(cap, 35)
    ds = _darken(stem, 20)
    if shape == "dome":
        pygame.draw.rect(s, stem, (12, 20, 8, 12))
        pygame.draw.rect(s, ds,   (12, 20, 8, 12), 1)
        pygame.draw.ellipse(s, cap, (4, 10, 24, 14))
        pygame.draw.ellipse(s, dc,  (4, 10, 24, 14), 1)
        if extra == "glow":
            pygame.draw.ellipse(s, (255, 140, 30), (5, 11, 22, 12), 2)
    elif shape == "bell":
        sy0 = 15 if extra == "tall" else 18
        pygame.draw.rect(s, stem, (13, sy0, 6, BS - sy0))
        pygame.draw.rect(s, ds,   (13, sy0, 6, BS - sy0), 1)
        pygame.draw.ellipse(s, cap, (9, sy0 - 14, 14, 16))
        pygame.draw.ellipse(s, dc,  (9, sy0 - 14, 14, 16), 1)
    elif shape == "flat":
        pygame.draw.rect(s, stem, (11, 22, 10, 10))
        pygame.draw.rect(s, ds,   (11, 22, 10, 10), 1)
        pygame.draw.ellipse(s, cap,              (2, 14, 28, 12))
        pygame.draw.ellipse(s, _darken(cap, 50), (4, 18, 24,  7))
        pygame.draw.ellipse(s, dc,               (2, 14, 28, 12), 1)
    elif shape == "puffball":
        pygame.draw.ellipse(s, _darken(cap, 20), (6, 13, 20, 19))
        pygame.draw.ellipse(s, cap,               (7, 12, 18, 18))
        pygame.draw.ellipse(s, dc,                (7, 12, 18, 18), 1)
        pygame.draw.rect(s, _darken(cap, 30), (12, 28, 8, 4))
    elif shape == "cluster":
        for cx2, cy2, r in [(8, 22, 5), (16, 17, 6), (24, 21, 5)]:
            pygame.draw.rect(s, stem, (cx2 - 2, cy2 + r, 4, BS - cy2 - r))
            pygame.draw.circle(s, cap, (cx2, cy2), r)
            pygame.draw.circle(s, dc,  (cx2, cy2), r, 1)
    if spots:
        for sx2, sy2, r in spots:
            pygame.draw.circle(s, (245, 245, 235), (sx2, sy2), r)
    if size != BS:
        s = pygame.transform.smoothscale(s, (size, size))
    return s


_MM_W      = 180
_MM_H      = 120
_MM_MARGIN = 8


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
        self._log_variants  = self._build_log_variants()
        self._leaf_variants = self._build_leaf_variants()
        self._bg_darken_surf = self._build_bg_darken_surf()
        self._bg_block_surfs = self._build_bg_block_surfs()
        self._cave_wall_surf = self._build_cave_wall_surf()
        self._light_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        self._light_gradient = None
        self._light_cache_key = None
        self._sky_surf = self._build_sky_surf()
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

    def _build_bg_darken_surf(self):
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        s.fill((0, 0, 0, 110))
        return s

    def _build_bg_block_surfs(self):
        """Pre-bake each block surface with the bg darkening already applied.
        Replaces 2 blits (block + darken overlay) with 1 blit per bg block."""
        darken = self._bg_darken_surf
        result = {}
        for bid, surf in self._block_surfs.items():
            baked = surf.copy().convert_alpha()
            baked.blit(darken, (0, 0))
            result[bid] = baked
        return result

    def _build_cave_wall_surf(self):
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        s.fill((55, 47, 40))
        pygame.draw.rect(s, (45, 38, 32), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
        return s

    def _build_tilled_soil_surfs(self):
        """Return [dry, wet] TILLED_SOIL surfaces, each with horizontal furrow grooves."""
        variants = [
            {"base": (150, 108, 62), "groove": (58, 38, 22)},  # dry: tan
            {"base": ( 88,  58, 28), "groove": (36, 22, 12)},  # wet: dark brown
        ]
        surfs = []
        for v in variants:
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            s.fill(v["base"])
            for gy in (8, 16, 24):
                pygame.draw.line(s, v["groove"], (2, gy), (BLOCK_SIZE - 2, gy), 2)
            pygame.draw.rect(s, _darken(v["base"], 40), s.get_rect(), 1)
            surfs.append(s)
        return surfs

    def _build_block_surfs(self):
        surfs = {}
        for bid, bdata in BLOCKS.items():
            if bdata["color"] is None:
                continue
            if bid == LADDER:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                rail = bdata["color"]
                dark = _darken(rail)
                pygame.draw.rect(s, rail, (4,                  0, 4, BLOCK_SIZE))
                pygame.draw.rect(s, rail, (BLOCK_SIZE - 8,     0, 4, BLOCK_SIZE))
                for ry in [3, 11, 19, 27]:
                    pygame.draw.rect(s, dark, (4, ry, BLOCK_SIZE - 8, 3))
                surfs[bid] = s
                continue
            if bid == STRAWBERRY_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (40, 140, 40),  (2, 12, 28, 18))
                pygame.draw.rect(s, (55, 165, 55),  (6, 5,  20, 20))
                for bx2, by2 in [(6, 8), (14, 14), (20, 9), (23, 16)]:
                    pygame.draw.rect(s, (220, 40, 70), (bx2, by2, 4, 4))
                surfs[bid] = s
                continue
            if bid == WHEAT_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                stalk_col = (160, 140, 50)
                head_col  = (220, 200, 60)
                for stx, sth in [(4, 22), (9, 18), (14, 26), (19, 20), (24, 16)]:
                    pygame.draw.rect(s, stalk_col, (stx, BLOCK_SIZE - sth, 2, sth))
                    pygame.draw.rect(s, head_col,  (stx - 1, BLOCK_SIZE - sth - 5, 4, 6))
                surfs[bid] = s
                continue
            if bid == STRAWBERRY_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (50, 160, 50), (15, 20, 3, 12))
                pygame.draw.rect(s, (70, 190, 70), (9,  22, 8, 4))
                pygame.draw.rect(s, (70, 190, 70), (16, 19, 8, 4))
                surfs[bid] = s
                continue
            if bid == STRAWBERRY_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (50, 150, 50), (14, 10, 4, 20))
                pygame.draw.rect(s, (70, 185, 70), (5,  14, 12, 5))
                pygame.draw.rect(s, (70, 185, 70), (16, 10, 12, 5))
                for bx2, by2 in [(6, 8), (18, 6), (10, 18), (22, 14)]:
                    pygame.draw.rect(s, (220, 40, 70), (bx2, by2, 5, 5))
                surfs[bid] = s
                continue
            if bid == WHEAT_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [10, 16, 22]:
                    pygame.draw.rect(s, (130, 160, 60), (stx, 18, 2, 14))
                surfs[bid] = s
                continue
            if bid == WHEAT_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [5, 10, 15, 20, 25]:
                    pygame.draw.rect(s, (190, 175, 55), (stx, 8, 3, 22))
                    pygame.draw.rect(s, (230, 210, 55), (stx - 1, 3, 5, 7))
                surfs[bid] = s
                continue
            if bid == BAKERY_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = bdata["color"]
                dark = _darken(base, 40)
                s.fill(base)
                # Oven door (dark square)
                pygame.draw.rect(s, dark, (7, 10, 18, 16))
                # Door handle
                pygame.draw.rect(s, (220, 200, 150), (13, 17, 6, 3))
                # Chimney top
                pygame.draw.rect(s, dark, (22, 2, 6, 8))
                # Glow inside door
                pygame.draw.rect(s, (220, 120, 30), (9, 12, 14, 12))
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CARROT_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (50, 150, 50), (4, 14, 24, 16))
                for bx2 in [6, 13, 20]:
                    pygame.draw.rect(s, (255, 140, 0), (bx2, 18, 5, 9))
                    pygame.draw.rect(s, (80, 200, 80), (bx2 + 1, 12, 3, 7))
                surfs[bid] = s
                continue
            if bid == TOMATO_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (40, 140, 40), (2, 10, 28, 20))
                for bx2, by2 in [(5, 10), (14, 7), (21, 12), (9, 18)]:
                    pygame.draw.circle(s, (210, 50, 50), (bx2, by2), 4)
                surfs[bid] = s
                continue
            if bid == CORN_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 26), (14, 22), (22, 24)]:
                    pygame.draw.rect(s, (100, 160, 50), (stx, BLOCK_SIZE - sth, 3, sth))
                    pygame.draw.rect(s, (230, 210, 55), (stx - 1, BLOCK_SIZE - sth, 5, 10))
                surfs[bid] = s
                continue
            if bid == PUMPKIN_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (50, 150, 50), (4, 16, 24, 14))
                for bx2, by2 in [(5, 17), (13, 14), (21, 18)]:
                    pygame.draw.ellipse(s, (200, 100, 30), (bx2, by2, 8, 7))
                surfs[bid] = s
                continue
            if bid == APPLE_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (40, 140, 40), (2, 8, 28, 22))
                for bx2, by2 in [(6, 10), (16, 8), (22, 14), (10, 18)]:
                    pygame.draw.circle(s, (180, 40, 40), (bx2, by2), 4)
                    pygame.draw.rect(s, (80, 160, 50), (bx2, by2 - 6, 2, 4))
                surfs[bid] = s
                continue
            if bid == CARROT_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [10, 16, 22]:
                    pygame.draw.rect(s, (80, 190, 80), (stx, 20, 2, 12))
                surfs[bid] = s
                continue
            if bid == CARROT_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [7, 14, 21]:
                    pygame.draw.rect(s, (80, 190, 80), (stx, 10, 3, 12))
                    pygame.draw.rect(s, (255, 140, 0), (stx, 22, 4, 8))
                surfs[bid] = s
                continue
            if bid == TOMATO_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [10, 16, 22]:
                    pygame.draw.rect(s, (70, 180, 70), (stx, 18, 2, 14))
                surfs[bid] = s
                continue
            if bid == TOMATO_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (60, 170, 60), (12, 8, 4, 18))
                for bx2, by2 in [(5, 12), (19, 10), (8, 20), (21, 18)]:
                    pygame.draw.circle(s, (210, 50, 50), (bx2, by2), 4)
                surfs[bid] = s
                continue
            if bid == CORN_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [10, 16, 22]:
                    pygame.draw.rect(s, (120, 170, 55), (stx, 14, 3, 18))
                surfs[bid] = s
                continue
            if bid == CORN_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [6, 14, 22]:
                    pygame.draw.rect(s, (130, 175, 55), (stx, 4, 4, 26))
                    pygame.draw.rect(s, (230, 210, 55), (stx - 1, 8, 6, 12))
                surfs[bid] = s
                continue
            if bid == PUMPKIN_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (70, 180, 70), (12, 16, 3, 16))
                pygame.draw.rect(s, (80, 190, 80), (5, 20, 22, 4))
                surfs[bid] = s
                continue
            if bid == PUMPKIN_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (60, 170, 60), (14, 4, 3, 12))
                pygame.draw.ellipse(s, (200, 100, 30), (4, 14, 24, 16))
                pygame.draw.rect(s, (60, 120, 40), (13, 13, 5, 4))
                surfs[bid] = s
                continue
            if bid == APPLE_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (60, 170, 60), (14, 14, 3, 18))
                pygame.draw.rect(s, (70, 185, 70), (8, 16, 16, 5))
                surfs[bid] = s
                continue
            if bid == APPLE_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (50, 160, 50), (14, 4, 4, 16))
                pygame.draw.rect(s, (60, 175, 60), (6, 10, 20, 6))
                for bx2, by2 in [(6, 14), (17, 12), (10, 20), (22, 18)]:
                    pygame.draw.circle(s, (180, 40, 40), (bx2, by2), 4)
                    pygame.draw.rect(s, (70, 160, 50), (bx2, by2 - 5, 2, 3))
                surfs[bid] = s
                continue
            if bid == RICE_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(5, 20), (10, 16), (15, 22), (20, 18), (25, 14)]:
                    pygame.draw.rect(s, (120, 160, 60), (stx, BLOCK_SIZE - sth, 2, sth))
                    pygame.draw.rect(s, (210, 200, 130), (stx - 1, BLOCK_SIZE - sth - 4, 4, 5))
                surfs[bid] = s
                continue
            if bid == GINGER_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (80, 150, 60), (4, 12, 24, 18))
                for bx2, by2 in [(6, 18), (14, 13), (22, 19)]:
                    pygame.draw.ellipse(s, (200, 160, 60), (bx2, by2, 7, 5))
                surfs[bid] = s
                continue
            if bid == BOK_CHOY_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth, sw in [(6, 20, 5), (13, 24, 6), (21, 18, 5)]:
                    pygame.draw.rect(s, (50, 170, 80), (stx, BLOCK_SIZE - sth, sw, sth))
                    pygame.draw.rect(s, (240, 240, 210), (stx + 1, BLOCK_SIZE - sth + 2, 2, sth - 4))
                surfs[bid] = s
                continue
            if bid == GARLIC_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(7, 22), (14, 18), (21, 20)]:
                    pygame.draw.rect(s, (140, 175, 90), (stx, BLOCK_SIZE - sth, 3, sth))
                    pygame.draw.ellipse(s, (230, 225, 200), (stx - 2, BLOCK_SIZE - sth - 6, 7, 7))
                surfs[bid] = s
                continue
            if bid == RICE_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [9, 15, 21]:
                    pygame.draw.rect(s, (130, 175, 65), (stx, 16, 2, 16))
                surfs[bid] = s
                continue
            if bid == RICE_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [6, 12, 18, 24]:
                    pygame.draw.rect(s, (150, 170, 65), (stx, 6, 3, 20))
                    pygame.draw.rect(s, (220, 205, 135), (stx - 1, 1, 5, 7))
                surfs[bid] = s
                continue
            if bid == GINGER_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (90, 160, 65), (12, 14, 3, 18))
                pygame.draw.rect(s, (100, 170, 70), (6, 20, 20, 4))
                surfs[bid] = s
                continue
            if bid == GINGER_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (80, 150, 60), (13, 6, 4, 16))
                pygame.draw.rect(s, (90, 160, 65), (6, 14, 20, 5))
                for bx2, by2 in [(5, 20), (13, 22), (21, 19)]:
                    pygame.draw.ellipse(s, (200, 160, 60), (bx2, by2, 8, 5))
                surfs[bid] = s
                continue
            if bid == BOK_CHOY_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(9, 16), (15, 20), (21, 14)]:
                    pygame.draw.rect(s, (70, 185, 80), (stx, BLOCK_SIZE - sth, 4, sth))
                surfs[bid] = s
                continue
            if bid == BOK_CHOY_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(4, 24), (11, 28), (18, 22), (24, 20)]:
                    pygame.draw.rect(s, (50, 170, 80), (stx, BLOCK_SIZE - sth, 5, sth))
                    pygame.draw.rect(s, (240, 240, 210), (stx + 1, BLOCK_SIZE - sth + 3, 2, sth - 6))
                surfs[bid] = s
                continue
            if bid == GARLIC_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [10, 16, 22]:
                    pygame.draw.rect(s, (155, 185, 100), (stx, 16, 3, 16))
                surfs[bid] = s
                continue
            if bid == GARLIC_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [8, 14, 20]:
                    pygame.draw.rect(s, (140, 175, 90), (stx, 8, 3, 18))
                    pygame.draw.ellipse(s, (230, 225, 200), (stx - 2, 2, 8, 8))
                surfs[bid] = s
                continue
            if bid == SCALLION_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 24), (12, 20), (18, 26), (24, 18)]:
                    pygame.draw.rect(s, (50, 185, 70), (stx, BLOCK_SIZE - sth, 3, sth))
                    pygame.draw.rect(s, (80, 210, 100), (stx - 1, BLOCK_SIZE - sth, 5, 6))
                surfs[bid] = s
                continue
            if bid == CHILI_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (50, 145, 50), (3, 10, 26, 20))
                for bx2, by2 in [(5, 12), (13, 8), (21, 13), (9, 20), (18, 18)]:
                    pygame.draw.rect(s, (210, 50, 35), (bx2, by2, 3, 7))
                    pygame.draw.rect(s, (80, 160, 50), (bx2 + 1, by2 - 3, 2, 4))
                surfs[bid] = s
                continue
            if bid == SCALLION_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [9, 15, 21]:
                    pygame.draw.rect(s, (60, 195, 80), (stx, 14, 3, 18))
                surfs[bid] = s
                continue
            if bid == SCALLION_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [6, 12, 18, 24]:
                    pygame.draw.rect(s, (50, 185, 70), (stx, 6, 3, 24))
                    pygame.draw.rect(s, (240, 240, 200), (stx + 1, 8, 2, 12))
                surfs[bid] = s
                continue
            if bid == CHILI_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [9, 15, 21]:
                    pygame.draw.rect(s, (80, 178, 70), (stx, 16, 2, 16))
                surfs[bid] = s
                continue
            if bid == CHILI_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (60, 165, 60), (13, 6, 4, 18))
                pygame.draw.rect(s, (70, 178, 65), (6, 14, 20, 4))
                for bx2, by2 in [(5, 18), (14, 16), (21, 20), (10, 24)]:
                    pygame.draw.rect(s, (215, 50, 35), (bx2, by2, 3, 7))
                surfs[bid] = s
                continue
            if bid == WOK_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = (70, 55, 45)
                dark = _darken(base, 30)
                bright = (110, 90, 75)
                s.fill(base)
                # Wok bowl shape (ellipse opening)
                pygame.draw.ellipse(s, dark, (4, 8, 24, 14))
                pygame.draw.ellipse(s, (30, 20, 15), (6, 10, 20, 10))
                # Steam wisps
                pygame.draw.rect(s, bright, (10, 4, 2, 5))
                pygame.draw.rect(s, bright, (16, 2, 2, 6))
                pygame.draw.rect(s, bright, (22, 4, 2, 4))
                # Handle stub
                pygame.draw.rect(s, dark, (24, 14, 7, 4))
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == STEAMER_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = (175, 150, 105)
                dark = _darken(base, 30)
                s.fill(base)
                # Bamboo steamer layers (3 bands)
                for ly in [6, 14, 22]:
                    pygame.draw.rect(s, dark, (3, ly, 26, 6))
                    pygame.draw.rect(s, (200, 175, 130), (4, ly + 1, 24, 3))
                # Lid (top strip)
                pygame.draw.rect(s, (155, 130, 85), (3, 2, 26, 5))
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == NOODLE_POT_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = (85, 70, 55)
                dark = _darken(base, 30)
                bright = (120, 100, 80)
                s.fill(base)
                # Pot body
                pygame.draw.ellipse(s, dark, (4, 12, 24, 18))
                pygame.draw.ellipse(s, (50, 35, 20), (6, 14, 20, 14))
                # Noodle swirl inside
                pygame.draw.arc(s, (220, 200, 140), (8, 16, 14, 10), 0.3, 3.0, 2)
                # Rim
                pygame.draw.rect(s, bright, (3, 10, 26, 4))
                # Steam
                pygame.draw.rect(s, bright, (12, 4, 2, 7))
                pygame.draw.rect(s, bright, (18, 6, 2, 5))
                # Handles
                pygame.draw.rect(s, dark, (0, 14, 4, 5))
                pygame.draw.rect(s, dark, (28, 14, 4, 5))
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PEPPER_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (50, 145, 50), (3, 12, 26, 18))
                for bx2, by2 in [(5, 10), (12, 7), (20, 11), (8, 18), (19, 19)]:
                    pygame.draw.rect(s, (220, 70, 30), (bx2, by2, 4, 8))
                    pygame.draw.rect(s, (70, 165, 55), (bx2 + 1, by2 - 3, 2, 4))
                surfs[bid] = s
                continue
            if bid == ONION_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(7, 22), (13, 26), (20, 20)]:
                    pygame.draw.rect(s, (130, 175, 90), (stx, BLOCK_SIZE - sth, 3, sth))
                for bx2, by2 in [(5, 14), (13, 10), (20, 15)]:
                    pygame.draw.ellipse(s, (175, 148, 85), (bx2, by2, 8, 6))
                surfs[bid] = s
                continue
            if bid == POTATO_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (95, 165, 75), (4, 10, 24, 18))
                for bx2, by2 in [(5, 22), (12, 24), (20, 21), (9, 27)]:
                    pygame.draw.ellipse(s, (160, 128, 62), (bx2, by2, 7, 5))
                surfs[bid] = s
                continue
            if bid == EGGPLANT_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (55, 150, 60), (3, 10, 26, 16))
                for bx2, by2 in [(5, 9), (14, 6), (21, 10), (9, 18)]:
                    pygame.draw.ellipse(s, (95, 45, 135), (bx2, by2, 6, 10))
                    pygame.draw.rect(s, (70, 170, 65), (bx2 + 2, by2 - 3, 2, 4))
                surfs[bid] = s
                continue
            if bid == CABBAGE_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for bx2, by2, bw2, bh2 in [(3, 16, 14, 14), (14, 14, 15, 16), (7, 8, 18, 12)]:
                    pygame.draw.ellipse(s, (75, 155, 85), (bx2, by2, bw2, bh2))
                pygame.draw.ellipse(s, (95, 175, 100), (8, 10, 16, 12))
                surfs[bid] = s
                continue
            if bid == WILDFLOWER_PATCH:
                import math as _math
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                # Stem
                pygame.draw.line(s, (50, 140, 40, 210), (16, 10), (16, 30), 2)
                # Small leaf nub
                pygame.draw.line(s, (60, 155, 50, 200), (16, 22), (21, 19), 1)
                # 5 petals in alternating warm colours, simple offset circles
                petal_colors = [(255, 220, 30), (255, 100, 160), (255, 255, 255),
                                (180, 120, 255), (255, 160, 40)]
                for i in range(5):
                    ang = i * 2 * _math.pi / 5 - _math.pi / 2
                    px = int(16 + 6 * _math.cos(ang))
                    py = int(10 + 6 * _math.sin(ang))
                    pygame.draw.circle(s, petal_colors[i] + (225,), (px, py), 4)
                # Yellow centre
                pygame.draw.circle(s, (255, 215, 50, 255), (16, 10), 3)
                surfs[bid] = s
                continue
            if bid == PEPPER_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [9, 15, 21]:
                    pygame.draw.rect(s, (75, 178, 65), (stx, 16, 3, 16))
                surfs[bid] = s
                continue
            if bid == PEPPER_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (60, 165, 55), (14, 6, 4, 18))
                pygame.draw.rect(s, (70, 178, 65), (7, 14, 18, 4))
                for bx2, by2 in [(5, 18), (14, 15), (21, 19), (10, 23)]:
                    pygame.draw.rect(s, (220, 70, 30), (bx2, by2, 4, 8))
                surfs[bid] = s
                continue
            if bid == ONION_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(8, 18), (14, 22), (20, 16)]:
                    pygame.draw.rect(s, (120, 185, 90), (stx, BLOCK_SIZE - sth, 3, sth))
                surfs[bid] = s
                continue
            if bid == ONION_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 22), (13, 26), (20, 20)]:
                    pygame.draw.rect(s, (110, 175, 80), (stx, BLOCK_SIZE - sth, 3, sth))
                for bx2 in [5, 12, 19]:
                    pygame.draw.ellipse(s, (175, 148, 85), (bx2, BLOCK_SIZE - 10, 9, 8))
                surfs[bid] = s
                continue
            if bid == POTATO_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [8, 14, 20]:
                    pygame.draw.rect(s, (100, 170, 75), (stx, 14, 4, 18))
                surfs[bid] = s
                continue
            if bid == POTATO_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (90, 160, 70), (5, 6, 6, 20))
                pygame.draw.rect(s, (90, 160, 70), (14, 4, 6, 22))
                pygame.draw.rect(s, (90, 160, 70), (22, 8, 4, 16))
                for bx2, by2 in [(3, 22), (12, 24), (21, 20)]:
                    pygame.draw.ellipse(s, (160, 128, 62), (bx2, by2, 8, 6))
                surfs[bid] = s
                continue
            if bid == EGGPLANT_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [8, 14, 20]:
                    pygame.draw.rect(s, (85, 168, 75), (stx, 16, 3, 16))
                surfs[bid] = s
                continue
            if bid == EGGPLANT_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (65, 158, 60), (14, 4, 4, 20))
                pygame.draw.rect(s, (75, 165, 70), (7, 12, 18, 4))
                for bx2, by2 in [(5, 14), (16, 12), (8, 22)]:
                    pygame.draw.ellipse(s, (95, 45, 135), (bx2, by2, 7, 12))
                    pygame.draw.rect(s, (70, 170, 60), (bx2 + 2, by2 - 4, 2, 5))
                surfs[bid] = s
                continue
            if bid == CABBAGE_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for bx2, by2, bw2, bh2 in [(6, 18, 10, 10), (16, 16, 12, 12)]:
                    pygame.draw.ellipse(s, (90, 175, 95), (bx2, by2, bw2, bh2))
                surfs[bid] = s
                continue
            if bid == CABBAGE_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for bx2, by2, bw2, bh2 in [(2, 16, 14, 14), (15, 14, 14, 16), (7, 8, 18, 14)]:
                    pygame.draw.ellipse(s, (75, 155, 85), (bx2, by2, bw2, bh2))
                pygame.draw.ellipse(s, (95, 175, 100), (8, 9, 16, 12))
                pygame.draw.ellipse(s, (115, 190, 115), (10, 11, 12, 8))
                surfs[bid] = s
                continue
            if bid == BBQ_GRILL_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = (55, 45, 35)
                dark = _darken(base, 25)
                s.fill(base)
                # Grill grate (horizontal bars)
                grate = (80, 68, 55)
                for gy in [10, 14, 18, 22]:
                    pygame.draw.rect(s, grate, (3, gy, 26, 2))
                # Vertical grate bars
                for gx in [7, 14, 21]:
                    pygame.draw.rect(s, grate, (gx, 8, 2, 18))
                # Fire glow underneath
                pygame.draw.rect(s, (190, 80, 20), (5, 26, 22, 4))
                pygame.draw.rect(s, (230, 140, 30), (8, 27, 16, 2))
                # Legs
                pygame.draw.rect(s, dark, (4, 2, 24, 6))
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CLAY_POT_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = (170, 100, 65)
                dark = _darken(base, 30)
                bright = (195, 130, 90)
                s.fill(base)
                # Pot body — wide rounded silhouette
                pygame.draw.ellipse(s, dark, (3, 10, 26, 20))
                pygame.draw.ellipse(s, (140, 75, 40), (5, 12, 22, 16))
                # Rim
                pygame.draw.rect(s, bright, (3, 8, 26, 4))
                # Steam wisps
                pygame.draw.rect(s, bright, (10, 2, 2, 6))
                pygame.draw.rect(s, bright, (16, 4, 2, 5))
                pygame.draw.rect(s, bright, (22, 2, 2, 4))
                # Side handles (small nubs)
                pygame.draw.rect(s, dark, (0, 12, 4, 5))
                pygame.draw.rect(s, dark, (28, 12, 4, 5))
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CAVE_MOSS:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = bdata["color"]
                dark = _darken(base, 30)
                light = tuple(min(255, c + 25) for c in base)
                s.fill(base)
                # Irregular moss patches — small dark and light blobs
                for mx, my, mw, mh, col in [
                    (3,  4,  8, 5, dark),  (14, 2,  6, 4, light),
                    (22, 6,  5, 4, dark),  (7,  14, 9, 4, light),
                    (18, 18, 7, 5, dark),  (2,  22, 6, 4, light),
                    (24, 22, 5, 4, dark),
                ]:
                    pygame.draw.ellipse(s, col, (mx, my, mw, mh))
                pygame.draw.rect(s, _darken(base), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CAVE_CRYSTAL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                base = bdata["color"]
                dark = _darken(base, 40)
                bright = tuple(min(255, c + 50) for c in base)
                # Three crystal shards of varying heights
                for cx2, ch, cw in [(5, 22, 6), (13, 28, 5), (21, 18, 6)]:
                    pts = [(cx2, BLOCK_SIZE), (cx2 + cw, BLOCK_SIZE),
                           (cx2 + cw // 2 + 1, BLOCK_SIZE - ch)]
                    pygame.draw.polygon(s, base, pts)
                    pygame.draw.polygon(s, dark, pts, 1)
                    pygame.draw.line(s, bright, (cx2 + cw // 2, BLOCK_SIZE),
                                     (cx2 + cw // 2 + 1, BLOCK_SIZE - ch + 3), 1)
                surfs[bid] = s
                continue
            if bid == GRAVEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = bdata["color"]
                dark = _darken(base, 20)
                light = tuple(min(255, c + 18) for c in base)
                s.fill(base)
                # Scattered pebble dots of varying sizes
                for gx, gy, gc, gsz in [
                    (4,  3,  dark,  4), (10, 8,  light, 3), (18, 4,  dark,  5),
                    (25, 10, light, 3), (6,  17, light, 4), (14, 22, dark,  3),
                    (22, 19, light, 5), (28, 25, dark,  3), (3,  27, light, 4),
                    (16, 14, dark,  3), (8,  25, dark,  3), (26, 3,  light, 4),
                ]:
                    pygame.draw.ellipse(s, gc, (gx, gy, gsz, gsz))
                pygame.draw.rect(s, _darken(base), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CRACKED_STONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = bdata["color"]
                dark = _darken(base, 40)
                s.fill(base)
                pygame.draw.line(s, dark, (4, 6),  (14, 22), 1)
                pygame.draw.line(s, dark, (18, 3), (26, 15), 1)
                pygame.draw.line(s, dark, (8, 20), (15, 28), 1)
                pygame.draw.rect(s, _darken(base), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == STALACTITE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                base = bdata["color"]
                dark = _darken(base, 30)
                pts = [(8, 0), (24, 0), (16, BLOCK_SIZE - 2)]
                pygame.draw.polygon(s, base, pts)
                pygame.draw.polygon(s, dark, pts, 1)
                surfs[bid] = s
                continue
            if bid in CAVE_MUSHROOMS:
                surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)
                continue
            if bid == STALAGMITE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                base = bdata["color"]
                dark = _darken(base, 30)
                pts = [(16, 2), (8, BLOCK_SIZE), (24, BLOCK_SIZE)]
                pygame.draw.polygon(s, base, pts)
                pygame.draw.polygon(s, dark, pts, 1)
                surfs[bid] = s
                continue
            if bid == WOOD_FENCE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                brown = (139, 90, 43)
                dbrown = (100, 65, 30)
                pygame.draw.rect(s, brown,  (12, 0, 8, 32))
                pygame.draw.rect(s, dbrown, (11, 0, 10, 3))
                pygame.draw.rect(s, brown,  (0, 10, 32, 4))
                pygame.draw.rect(s, brown,  (0, 20, 32, 4))
                surfs[bid] = s
                continue
            if bid == IRON_FENCE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                gray = (160, 160, 165)
                dgray = (110, 110, 118)
                pygame.draw.rect(s, gray,  (12, 0, 8, 32))
                pygame.draw.rect(s, dgray, (11, 0, 10, 3))
                pygame.draw.rect(s, gray,  (0, 10, 32, 4))
                pygame.draw.rect(s, gray,  (0, 20, 32, 4))
                pygame.draw.polygon(s, dgray, [(16, 0), (13, 5), (19, 5)])
                surfs[bid] = s
                continue
            if bid == WOOD_FENCE_OPEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                brown = (139, 90, 43)
                dbrown = (100, 65, 30)
                # Post (left side, gate swung open along the wall)
                pygame.draw.rect(s, brown,  (0, 0, 8, 32))
                pygame.draw.rect(s, dbrown, (0, 0, 9, 3))
                # Gate rails drawn horizontally (rotated 90° open)
                pygame.draw.rect(s, brown,  (0, 8,  20, 4))
                pygame.draw.rect(s, brown,  (0, 18, 20, 4))
                surfs[bid] = s
                continue
            if bid == IRON_FENCE_OPEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                gray = (160, 160, 165)
                dgray = (110, 110, 118)
                # Post (left side, gate swung open along the wall)
                pygame.draw.rect(s, gray,  (0, 0, 8, 32))
                pygame.draw.rect(s, dgray, (0, 0, 9, 3))
                # Gate rails drawn horizontally (rotated 90° open)
                pygame.draw.rect(s, gray,  (0, 8,  20, 4))
                pygame.draw.rect(s, gray,  (0, 18, 20, 4))
                pygame.draw.polygon(s, dgray, [(4, 0), (1, 5), (7, 5)])
                surfs[bid] = s
                continue
            if bid == WOOD_DOOR_CLOSED:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(s, (110, 70, 30),  (0,  0, 32, 32))
                pygame.draw.rect(s, (160, 105, 55), (3,  3, 26, 26))
                pygame.draw.rect(s, (145, 95,  45), (6,  8, 20, 16))
                pygame.draw.circle(s, (220, 180, 80), (22, 16), 2)
                surfs[bid] = s
                continue
            if bid == WOOD_DOOR_OPEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (160, 105, 55), (0, 0, 8, 32))
                pygame.draw.rect(s, (100,  65, 30), (7, 0, 1, 32))
                surfs[bid] = s
                continue
            if bid == IRON_DOOR_CLOSED:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(s, (120, 120, 128), (0,  0, 32, 32))
                pygame.draw.rect(s, (175, 175, 182), (3,  3, 26, 26))
                pygame.draw.rect(s, (100, 100, 108), (3, 15, 26,  2))
                for rx, ry in ((5, 5), (27, 5), (5, 27), (27, 27)):
                    pygame.draw.circle(s, (100, 100, 108), (rx, ry), 2)
                pygame.draw.rect(s, (200, 200, 90), (22, 13, 4, 6))
                surfs[bid] = s
                continue
            if bid == IRON_DOOR_OPEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (175, 175, 182), (0, 0, 8, 32))
                pygame.draw.rect(s, (100, 100, 108), (7, 0, 1, 32))
                pygame.draw.circle(s, (100, 100, 108), (4, 16), 2)
                surfs[bid] = s
                continue
            # --- Middle Eastern decorative doors ---
            if bid == COBALT_DOOR_CLOSED:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                frame = (28, 55, 140)
                panel = (55, 95, 185)
                gold  = (210, 170, 55)
                s.fill(frame)
                pygame.draw.rect(s, panel, (3, 3, 26, 26))
                # 8-pointed star arabesque
                cx2, cy2 = 16, 15
                for i in range(8):
                    a = math.pi * i / 4
                    ex, ey = cx2 + int(9 * math.cos(a)), cy2 + int(9 * math.sin(a))
                    pygame.draw.line(s, gold, (cx2, cy2), (ex, ey), 1)
                pygame.draw.circle(s, gold, (cx2, cy2), 3, 1)
                # gold border
                pygame.draw.rect(s, gold, (3, 3, 26, 26), 1)
                # brass handle
                pygame.draw.circle(s, gold, (24, 16), 2)
                surfs[bid] = s
                continue
            if bid == COBALT_DOOR_OPEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (55, 95, 185), (0, 0, 8, 32))
                pygame.draw.rect(s, (28, 55, 140), (7, 0, 1, 32))
                surfs[bid] = s
                continue
            if bid == CRIMSON_CEDAR_DOOR_CLOSED:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                frame = (105, 25, 28)
                panel = (155, 45, 48)
                gold  = (210, 170, 55)
                s.fill(frame)
                pygame.draw.rect(s, panel, (3, 3, 26, 26))
                # diamond grid pattern
                for dx2, dy2 in [(16, 9), (16, 23)]:
                    pygame.draw.polygon(s, frame, [(dx2, dy2-5),(dx2+6,dy2),(dx2,dy2+5),(dx2-6,dy2)], 1)
                    pygame.draw.line(s, frame, (3, dy2), (29, dy2), 1)
                pygame.draw.line(s, frame, (16, 3), (16, 29), 1)
                pygame.draw.rect(s, gold, (3, 3, 26, 26), 1)
                pygame.draw.circle(s, gold, (24, 16), 2)
                surfs[bid] = s
                continue
            if bid == CRIMSON_CEDAR_DOOR_OPEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (155, 45, 48), (0, 0, 8, 32))
                pygame.draw.rect(s, (105, 25, 28), (7, 0, 1, 32))
                surfs[bid] = s
                continue
            if bid == TEAL_DOOR_CLOSED:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                frame = (30, 105, 100)
                panel = (60, 150, 145)
                gold  = (210, 170, 55)
                s.fill(frame)
                pygame.draw.rect(s, panel, (3, 3, 26, 26))
                # horseshoe arch motif
                pygame.draw.arc(s, gold, (8, 5, 16, 16), 0, math.pi, 2)
                pygame.draw.line(s, gold, (8, 13), (8, 20), 2)
                pygame.draw.line(s, gold, (24, 13), (24, 20), 2)
                # lower panel divider
                pygame.draw.line(s, gold, (3, 22), (29, 22), 1)
                pygame.draw.rect(s, gold, (3, 3, 26, 26), 1)
                pygame.draw.circle(s, gold, (24, 16), 2)
                surfs[bid] = s
                continue
            if bid == TEAL_DOOR_OPEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (60, 150, 145), (0, 0, 8, 32))
                pygame.draw.rect(s, (30, 105, 100), (7, 0, 1, 32))
                surfs[bid] = s
                continue
            if bid == SAFFRON_DOOR_CLOSED:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                frame = (160, 115, 18)
                panel = (210, 165, 42)
                dk    = (120,  85, 12)
                s.fill(frame)
                pygame.draw.rect(s, panel, (3, 3, 26, 26))
                # three vertical carved panels
                pygame.draw.rect(s, dk, (3,  3, 8, 26))
                pygame.draw.rect(s, dk, (12, 3, 8, 26))
                pygame.draw.rect(s, dk, (21, 3, 8, 26))
                pygame.draw.rect(s, _lighter(panel, 18), (4, 4, 6, 24))
                pygame.draw.rect(s, _lighter(panel, 18), (13, 4, 6, 24))
                pygame.draw.rect(s, _lighter(panel, 18), (22, 4, 6, 24))
                pygame.draw.circle(s, (210, 170, 55), (24, 16), 2)
                surfs[bid] = s
                continue
            if bid == SAFFRON_DOOR_OPEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (210, 165, 42), (0, 0, 8, 32))
                pygame.draw.rect(s, (160, 115, 18), (7, 0, 1, 32))
                surfs[bid] = s
                continue
            if bid in (STAIRS_RIGHT, STAIRS_LEFT):
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                wood  = bdata["color"]
                dark  = _darken(wood, 40)
                light = tuple(min(255, c + 30) for c in wood)
                step_h = BLOCK_SIZE // 3
                # Three steps rising in the facing direction
                for i in range(3):
                    if bid == STAIRS_RIGHT:
                        sx2 = i * (BLOCK_SIZE // 3)
                        sw  = BLOCK_SIZE - sx2
                    else:
                        sw  = BLOCK_SIZE - i * (BLOCK_SIZE // 3)
                        sx2 = 0
                    sy2 = i * step_h
                    sh  = BLOCK_SIZE - sy2
                    pygame.draw.rect(s, wood,  (sx2, sy2, sw, sh))
                    pygame.draw.rect(s, light, (sx2, sy2, sw, 2))
                    pygame.draw.rect(s, dark,  (sx2, sy2, sw, sh), 1)
                surfs[bid] = s
                continue
            if bid == CHEST_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                base = (160, 110, 55)
                dark = _darken(base, 35)
                bright = tuple(min(255, c + 25) for c in base)
                s.fill(base)
                # plank lines
                pygame.draw.line(s, dark, (0, 10), (BLOCK_SIZE, 10), 1)
                pygame.draw.line(s, dark, (0, 22), (BLOCK_SIZE, 22), 1)
                # iron band across middle
                pygame.draw.rect(s, (130, 130, 140), (0, 12, BLOCK_SIZE, 8))
                pygame.draw.rect(s, (90, 90, 100), (0, 12, BLOCK_SIZE, 8), 1)
                # clasp / lock
                pygame.draw.rect(s, (200, 175, 80), (12, 14, 8, 5))
                pygame.draw.rect(s, (150, 130, 50), (12, 14, 8, 5), 1)
                # outer border
                pygame.draw.rect(s, dark, s.get_rect(), 2)
                surfs[bid] = s
                continue
            if bid == BIRD_FEEDER_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                wood      = (160, 115,  65)
                dark_wood = (110,  75,  35)
                roof_col  = ( 95,  62,  28)
                # Post
                pygame.draw.rect(s, dark_wood, (13, 17,  6, 15))
                pygame.draw.rect(s, wood,      (14, 17,  2, 15))
                # Tray platform
                pygame.draw.rect(s, wood,      ( 3, 13, 26,  5))
                pygame.draw.rect(s, dark_wood, ( 3, 17, 26,  1))
                # Seeds in tray
                for sx2, sy2 in [(6, 14), (11, 13), (17, 14), (22, 13)]:
                    pygame.draw.rect(s, (210, 185, 70), (sx2, sy2, 2, 2))
                # Roof beam
                pygame.draw.rect(s, roof_col,  ( 1,  7, 30,  7))
                pygame.draw.rect(s, dark_wood, ( 1,  7, 30,  7), 1)
                # Roof peak
                pygame.draw.polygon(s, wood, [(16, 1), (1, 8), (31, 8)])
                pygame.draw.polygon(s, dark_wood, [(16, 1), (1, 8), (31, 8)], 1)
                surfs[bid] = s
                continue
            if bid == BIRD_BATH_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                stone      = (185, 180, 172)
                dark_stone = (135, 130, 122)
                water_col  = ( 75, 148, 215)
                # Pedestal column
                pygame.draw.rect(s, stone,      (12, 13,  8, 19))
                pygame.draw.rect(s, dark_stone, (12, 13,  2, 19))
                pygame.draw.rect(s, dark_stone, (12, 13,  8, 19), 1)
                # Basin rim
                pygame.draw.rect(s, stone,      ( 2,  8, 28,  6))
                pygame.draw.rect(s, dark_stone, ( 2,  8, 28,  6), 1)
                # Water in basin
                pygame.draw.rect(s, water_col,  ( 4,  9, 24,  4))
                pygame.draw.rect(s, (100, 170, 230), (6, 10, 8, 1))
                surfs[bid] = s
                continue
            if bid == WATER:
                continue   # rendered per-level via _water_surfs
            if bid == COAL_ORE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                stone_base = (118, 112, 108)
                s.fill(stone_base)
                coal = (22, 20, 18)
                coal_light = (40, 37, 34)
                # Scattered coal chunks — irregular rectangles
                for rx, ry, rw, rh in [(3, 4, 7, 5), (14, 2, 6, 8), (22, 8, 7, 4),
                                        (5, 15, 8, 6), (17, 18, 9, 7), (6, 25, 5, 4),
                                        (21, 25, 7, 5)]:
                    pygame.draw.rect(s, coal, (rx, ry, rw, rh))
                    pygame.draw.rect(s, coal_light, (rx, ry, rw, rh), 1)
                pygame.draw.rect(s, _darken(stone_base, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CLAY_DEPOSIT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                stone_base = (118, 112, 108)
                clay_col = (165, 120, 85)
                clay_dk  = _darken(clay_col, 20)
                s.fill(stone_base)
                for rx, ry, rw, rh in [(2, 3, 9, 6), (13, 1, 8, 9), (23, 6, 7, 5),
                                        (4, 14, 11, 7), (18, 16, 8, 8), (7, 25, 9, 5),
                                        (22, 24, 8, 6)]:
                    pygame.draw.rect(s, clay_col, (rx, ry, rw, rh))
                    pygame.draw.rect(s, clay_dk,  (rx, ry, rw, rh), 1)
                pygame.draw.rect(s, _darken(stone_base, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == LIMESTONE_DEPOSIT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = (210, 200, 180)
                s.fill(c)
                dk = _darken(c, 18)
                lt = _lighter(c, 10)
                for ly in [5, 11, 17, 23]:
                    pygame.draw.line(s, dk, (0, ly),   (BLOCK_SIZE, ly),   1)
                    pygame.draw.line(s, lt, (0, ly+1), (BLOCK_SIZE, ly+1), 1)
                for fx, fy in [(4, 7), (19, 3), (27, 14), (8, 19), (24, 22), (13, 28)]:
                    pygame.draw.rect(s, dk, (fx, fy, 5, 2))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == SAPLING:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (101, 67, 33), (14, 20, 4, 12))
                pygame.draw.circle(s, (50, 170, 50), (16, 14), 7)
                pygame.draw.circle(s, (70, 190, 70), (13, 11), 4)
                pygame.draw.circle(s, (70, 190, 70), (20, 12), 4)
                surfs[bid] = s
                continue
            if bid == MUSHROOM_STEM:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                base = (228, 218, 198)
                dark = _darken(base, 20)
                s.fill(base)
                pygame.draw.rect(s, dark, (0, 0, 4, 32))
                pygame.draw.rect(s, dark, (28, 0, 4, 32))
                pygame.draw.rect(s, tuple(min(255, c + 15) for c in base), (4, 0, 24, 32))
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MUSHROOM_CAP:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                base = (175, 38, 38)
                dark = _darken(base, 30)
                pygame.draw.ellipse(s, base, (0, 8, 32, 24))
                pygame.draw.ellipse(s, dark, (0, 8, 32, 24), 1)
                for sx, sy in [(7, 14), (16, 11), (23, 15)]:
                    pygame.draw.circle(s, (240, 235, 220), (sx, sy), 3)
                surfs[bid] = s
                continue
            if bid == BEET_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 20), (13, 24), (21, 18)]:
                    pygame.draw.rect(s, (80, 140, 60), (stx, BLOCK_SIZE - sth, 3, sth - 10))
                for bx2, by2 in [(4, 18), (12, 15), (20, 19)]:
                    pygame.draw.ellipse(s, (130, 25, 55), (bx2, by2, 9, 8))
                    pygame.draw.rect(s, (80, 140, 60), (bx2 + 3, by2 - 4, 2, 5))
                surfs[bid] = s
                continue
            if bid == BEET_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(7, 14), (14, 18), (21, 12)]:
                    pygame.draw.rect(s, (85, 155, 65), (stx, BLOCK_SIZE - sth, 3, sth))
                surfs[bid] = s
                continue
            if bid == BEET_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 20), (13, 24), (21, 18)]:
                    pygame.draw.rect(s, (80, 140, 60), (stx, BLOCK_SIZE - sth, 3, sth - 8))
                for bx2 in [4, 12, 20]:
                    pygame.draw.ellipse(s, (130, 25, 55), (bx2, BLOCK_SIZE - 10, 9, 8))
                surfs[bid] = s
                continue
            if bid == TURNIP_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 20), (14, 24), (21, 18)]:
                    pygame.draw.rect(s, (90, 155, 70), (stx, BLOCK_SIZE - sth, 3, sth - 8))
                for bx2, by2 in [(4, 17), (12, 14), (20, 18)]:
                    pygame.draw.ellipse(s, (210, 188, 212), (bx2, by2, 9, 9))
                    pygame.draw.ellipse(s, (170, 60, 90), (bx2, by2 + 5, 9, 4))
                    pygame.draw.rect(s, (90, 155, 70), (bx2 + 3, by2 - 4, 2, 5))
                surfs[bid] = s
                continue
            if bid == TURNIP_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(7, 14), (14, 18), (21, 12)]:
                    pygame.draw.rect(s, (90, 165, 75), (stx, BLOCK_SIZE - sth, 3, sth))
                surfs[bid] = s
                continue
            if bid == TURNIP_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 20), (13, 24), (21, 18)]:
                    pygame.draw.rect(s, (90, 155, 70), (stx, BLOCK_SIZE - sth, 3, sth - 8))
                for bx2 in [4, 12, 20]:
                    pygame.draw.ellipse(s, (210, 188, 212), (bx2, BLOCK_SIZE - 11, 9, 9))
                    pygame.draw.ellipse(s, (170, 60, 90), (bx2, BLOCK_SIZE - 6, 9, 4))
                surfs[bid] = s
                continue
            if bid == LEEK_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, scol in [(4, (55, 180, 75)), (10, (65, 195, 85)),
                                   (17, (50, 170, 70)), (23, (60, 185, 80))]:
                    pygame.draw.rect(s, scol, (stx, 2, 4, 22))
                    pygame.draw.rect(s, (230, 240, 220), (stx, 22, 4, 8))
                surfs[bid] = s
                continue
            if bid == LEEK_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [8, 15, 22]:
                    pygame.draw.rect(s, (60, 185, 80), (stx, 10, 3, 22))
                surfs[bid] = s
                continue
            if bid == LEEK_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [6, 13, 20]:
                    pygame.draw.rect(s, (60, 185, 75), (stx, 2, 4, 22))
                    pygame.draw.rect(s, (220, 235, 215), (stx, 22, 4, 10))
                surfs[bid] = s
                continue
            if bid == ZUCCHINI_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (60, 140, 50), (3, 12, 26, 14))
                for zx, zy in [(4, 16), (14, 13), (20, 18)]:
                    pygame.draw.rect(s, (55, 130, 45), (zx, zy, 12, 5))
                    pygame.draw.ellipse(s, (80, 160, 65), (zx - 1, zy - 1, 14, 7))
                    pygame.draw.rect(s, (100, 180, 80), (zx + 11, zy, 3, 4))
                surfs[bid] = s
                continue
            if bid == ZUCCHINI_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [7, 14, 21]:
                    pygame.draw.rect(s, (80, 170, 65), (stx, 12, 4, 20))
                    pygame.draw.ellipse(s, (100, 185, 80), (stx - 2, 9, 8, 6))
                surfs[bid] = s
                continue
            if bid == ZUCCHINI_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (60, 145, 50), (5, 10, 22, 10))
                for zx, zy in [(3, 18), (14, 15)]:
                    pygame.draw.rect(s, (60, 138, 48), (zx, zy, 13, 5))
                    pygame.draw.ellipse(s, (78, 158, 62), (zx - 1, zy - 1, 15, 7))
                    pygame.draw.rect(s, (95, 175, 75), (zx + 12, zy, 3, 4))
                surfs[bid] = s
                continue
            if bid == SWEET_POTATO_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for vx, vy in [(3, 14), (10, 10), (20, 12)]:
                    pygame.draw.rect(s, (80, 155, 65), (vx, vy, 10, 3))
                    pygame.draw.ellipse(s, (75, 150, 62), (vx - 1, vy - 2, 12, 7))
                for bx2, by2 in [(5, 19), (15, 16), (21, 21)]:
                    pygame.draw.ellipse(s, (190, 95, 45), (bx2, by2, 9, 6))
                surfs[bid] = s
                continue
            if bid == SWEET_POTATO_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for vx, vy in [(5, 18), (13, 14), (21, 20)]:
                    pygame.draw.rect(s, (95, 170, 75), (vx, vy, 8, 3))
                    pygame.draw.ellipse(s, (110, 185, 85), (vx - 1, vy - 2, 10, 6))
                surfs[bid] = s
                continue
            if bid == SWEET_POTATO_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for vx, vy in [(3, 12), (12, 8), (20, 13)]:
                    pygame.draw.rect(s, (80, 155, 65), (vx, vy, 10, 3))
                    pygame.draw.ellipse(s, (75, 150, 62), (vx - 1, vy - 2, 12, 7))
                for bx2, by2 in [(4, 20), (14, 17), (20, 22)]:
                    pygame.draw.ellipse(s, (190, 95, 45), (bx2, by2, 10, 7))
                surfs[bid] = s
                continue
            if bid == WATERMELON_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (55, 135, 48), (3, 16, 26, 8))
                pygame.draw.ellipse(s, (50, 128, 42), (5, 8, 22, 18))
                for sx2 in [7, 12, 17, 22]:
                    pygame.draw.line(s, (35, 100, 30), (sx2, 8), (sx2 - 1, 26), 1)
                pygame.draw.ellipse(s, (210, 55, 65), (9, 12, 14, 10))
                surfs[bid] = s
                continue
            if bid == WATERMELON_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [6, 14, 22]:
                    pygame.draw.rect(s, (65, 158, 58), (stx, 14, 4, 18))
                    pygame.draw.ellipse(s, (85, 175, 72), (stx - 2, 10, 8, 7))
                surfs[bid] = s
                continue
            if bid == WATERMELON_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.ellipse(s, (50, 128, 42), (4, 6, 24, 20))
                for sx2 in [8, 13, 18, 23]:
                    pygame.draw.line(s, (35, 100, 30), (sx2, 6), (sx2 - 1, 26), 1)
                pygame.draw.rect(s, (55, 135, 48), (2, 20, 28, 6))
                surfs[bid] = s
                continue
            if bid == RADISH_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 18), (13, 22), (21, 16)]:
                    pygame.draw.rect(s, (75, 145, 60), (stx, BLOCK_SIZE - sth, 3, sth - 8))
                for bx2, by2 in [(4, 18), (12, 15), (20, 19)]:
                    pygame.draw.ellipse(s, (215, 55, 75), (bx2, by2, 8, 8))
                    pygame.draw.ellipse(s, (240, 240, 240), (bx2 + 1, by2 + 5, 6, 4))
                    pygame.draw.rect(s, (75, 145, 60), (bx2 + 3, by2 - 4, 2, 5))
                surfs[bid] = s
                continue
            if bid == RADISH_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(7, 14), (14, 18), (21, 12)]:
                    pygame.draw.rect(s, (85, 165, 70), (stx, BLOCK_SIZE - sth, 3, sth))
                surfs[bid] = s
                continue
            if bid == RADISH_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 18), (13, 22), (21, 16)]:
                    pygame.draw.rect(s, (75, 145, 60), (stx, BLOCK_SIZE - sth, 3, sth - 7))
                for bx2 in [4, 12, 20]:
                    pygame.draw.ellipse(s, (215, 55, 75), (bx2, BLOCK_SIZE - 10, 8, 8))
                    pygame.draw.ellipse(s, (240, 240, 240), (bx2 + 1, BLOCK_SIZE - 5, 6, 4))
                surfs[bid] = s
                continue
            if bid == PEA_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for vx, vy in [(3, 8), (12, 5), (20, 9), (6, 18), (18, 16)]:
                    pygame.draw.rect(s, (85, 175, 60), (vx, vy, 10, 3))
                for px2, py2 in [(4, 12), (13, 9), (20, 13), (7, 20), (19, 19)]:
                    pygame.draw.rect(s, (95, 180, 65), (px2, py2, 10, 5))
                    for dot in range(3):
                        pygame.draw.circle(s, (120, 200, 80), (px2 + 2 + dot * 3, py2 + 2), 2)
                surfs[bid] = s
                continue
            if bid == PEA_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for vx, vy in [(5, 16), (13, 12), (21, 18)]:
                    pygame.draw.rect(s, (100, 185, 70), (vx, vy, 8, 3))
                    pygame.draw.ellipse(s, (115, 195, 80), (vx - 1, vy - 2, 10, 6))
                surfs[bid] = s
                continue
            if bid == PEA_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for vx, vy in [(3, 8), (14, 5), (20, 10)]:
                    pygame.draw.rect(s, (85, 175, 60), (vx, vy, 10, 3))
                for px2, py2 in [(3, 14), (13, 11), (19, 16)]:
                    pygame.draw.rect(s, (100, 182, 62), (px2, py2, 11, 5))
                    for dot in range(3):
                        pygame.draw.circle(s, (130, 200, 80), (px2 + 2 + dot * 3, py2 + 2), 2)
                surfs[bid] = s
                continue
            if bid == CELERY_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth, scol in [(4, 28, (90, 178, 98)), (9, 30, (80, 168, 88)),
                                        (15, 26, (95, 182, 102)), (21, 28, (85, 175, 95)),
                                        (26, 24, (90, 178, 98))]:
                    pygame.draw.rect(s, scol, (stx, BLOCK_SIZE - sth, 4, sth))
                    pygame.draw.line(s, _darken(scol, 20), (stx + 2, BLOCK_SIZE - sth + 2),
                                     (stx + 2, BLOCK_SIZE - 2), 1)
                surfs[bid] = s
                continue
            if bid == CELERY_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [7, 14, 21]:
                    pygame.draw.rect(s, (85, 172, 92), (stx, 14, 4, 18))
                    pygame.draw.line(s, (65, 148, 72), (stx + 2, 16), (stx + 2, 30), 1)
                surfs[bid] = s
                continue
            if bid == CELERY_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(5, 26), (10, 28), (16, 24), (22, 26)]:
                    pygame.draw.rect(s, (90, 178, 98), (stx, BLOCK_SIZE - sth, 4, sth))
                    pygame.draw.line(s, (68, 152, 75), (stx + 2, BLOCK_SIZE - sth + 2),
                                     (stx + 2, BLOCK_SIZE - 2), 1)
                surfs[bid] = s
                continue
            if bid == BROCCOLI_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(6, 16), (14, 20), (22, 14)]:
                    pygame.draw.rect(s, (50, 125, 55), (stx, BLOCK_SIZE - sth, 4, sth - 8))
                for bx2, by2 in [(4, 10), (13, 6), (21, 11)]:
                    pygame.draw.ellipse(s, (42, 118, 50), (bx2, by2, 10, 8))
                    pygame.draw.ellipse(s, (55, 135, 62), (bx2 + 1, by2, 4, 4))
                    pygame.draw.ellipse(s, (55, 135, 62), (bx2 + 5, by2 + 1, 4, 4))
                surfs[bid] = s
                continue
            if bid == BROCCOLI_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx in [8, 16]:
                    pygame.draw.rect(s, (60, 148, 65), (stx, 16, 4, 16))
                    pygame.draw.ellipse(s, (48, 130, 55), (stx - 1, 10, 8, 8))
                surfs[bid] = s
                continue
            if bid == BROCCOLI_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(5, 18), (14, 22), (22, 16)]:
                    pygame.draw.rect(s, (50, 125, 55), (stx, BLOCK_SIZE - sth, 4, sth - 9))
                for bx2, by2 in [(3, 8), (12, 4), (20, 9)]:
                    pygame.draw.ellipse(s, (40, 112, 48), (bx2, by2, 12, 10))
                    pygame.draw.ellipse(s, (55, 130, 60), (bx2 + 1, by2, 5, 5))
                    pygame.draw.ellipse(s, (55, 130, 60), (bx2 + 6, by2 + 1, 5, 5))
                    pygame.draw.ellipse(s, (65, 145, 70), (bx2 + 3, by2 - 1, 5, 4))
                surfs[bid] = s
                continue
            if bid == CHAMOMILE_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(5, 18), (13, 22), (22, 16)]:
                    pygame.draw.rect(s, (100, 165, 75), (stx, BLOCK_SIZE - sth, 2, sth - 8))
                for fx, fy in [(3, 8), (12, 5), (20, 9)]:
                    for dx, dy in [(-4,0),(4,0),(0,-4),(0,4),(-3,-3),(3,-3),(-3,3),(3,3)]:
                        pygame.draw.ellipse(s, (240, 240, 220), (fx + dx, fy + dy, 4, 3))
                    pygame.draw.circle(s, (230, 210, 60), (fx, fy), 3)
                surfs[bid] = s
                continue
            if bid == CHAMOMILE_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(7, 14), (15, 18), (23, 12)]:
                    pygame.draw.rect(s, (110, 175, 85), (stx, BLOCK_SIZE - sth, 2, sth))
                surfs[bid] = s
                continue
            if bid == CHAMOMILE_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(4, 22), (13, 26), (22, 20)]:
                    pygame.draw.rect(s, (100, 165, 75), (stx, BLOCK_SIZE - sth, 2, sth - 9))
                for fx, fy in [(2, 6), (12, 2), (20, 7)]:
                    for dx, dy in [(-5,0),(5,0),(0,-5),(0,5),(-3,-3),(3,-3),(-3,3),(3,3)]:
                        pygame.draw.ellipse(s, (245, 245, 230), (fx + dx, fy + dy, 5, 4))
                    pygame.draw.circle(s, (235, 215, 55), (fx, fy), 4)
                surfs[bid] = s
                continue
            if bid == LAVENDER_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(5, 22), (13, 26), (21, 20)]:
                    pygame.draw.rect(s, (115, 145, 100), (stx, BLOCK_SIZE - sth, 2, sth - 10))
                    pygame.draw.rect(s, (175, 130, 215), (stx - 1, BLOCK_SIZE - sth - 2, 4, 10))
                    for dy in range(1, 9, 2):
                        pygame.draw.circle(s, (195, 150, 230), (stx + 1, BLOCK_SIZE - sth - 2 + dy), 2)
                surfs[bid] = s
                continue
            if bid == LAVENDER_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(7, 14), (15, 18), (23, 12)]:
                    pygame.draw.rect(s, (120, 150, 105), (stx, BLOCK_SIZE - sth, 2, sth))
                surfs[bid] = s
                continue
            if bid == LAVENDER_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(4, 26), (13, 30), (21, 24)]:
                    pygame.draw.rect(s, (115, 145, 100), (stx, BLOCK_SIZE - sth, 2, sth - 12))
                    pygame.draw.rect(s, (185, 140, 220), (stx - 2, BLOCK_SIZE - sth - 2, 5, 12))
                    for dy in range(1, 11, 2):
                        pygame.draw.circle(s, (205, 160, 235), (stx + 1, BLOCK_SIZE - sth - 2 + dy), 2)
                surfs[bid] = s
                continue
            if bid == MINT_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(5, 20), (13, 24), (21, 18)]:
                    pygame.draw.rect(s, (55, 180, 110), (stx, BLOCK_SIZE - sth, 3, sth - 6))
                for lx, ly in [(3, 12), (11, 8), (19, 13), (7, 18), (16, 17)]:
                    pygame.draw.ellipse(s, (60, 200, 140), (lx, ly, 9, 7))
                    pygame.draw.line(s, (40, 160, 110), (lx + 4, ly + 1), (lx + 4, ly + 6), 1)
                surfs[bid] = s
                continue
            if bid == MINT_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(7, 14), (15, 18), (23, 12)]:
                    pygame.draw.rect(s, (60, 185, 115), (stx, BLOCK_SIZE - sth, 3, sth - 4))
                    pygame.draw.ellipse(s, (70, 200, 130), (stx - 2, BLOCK_SIZE - sth - 4, 7, 6))
                surfs[bid] = s
                continue
            if bid == MINT_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(4, 22), (13, 26), (21, 20)]:
                    pygame.draw.rect(s, (55, 180, 110), (stx, BLOCK_SIZE - sth, 3, sth - 7))
                for lx, ly in [(2, 8), (11, 4), (19, 9), (6, 17), (15, 15)]:
                    pygame.draw.ellipse(s, (65, 210, 150), (lx, ly, 11, 8))
                    pygame.draw.line(s, (45, 165, 115), (lx + 5, ly + 1), (lx + 5, ly + 7), 1)
                surfs[bid] = s
                continue
            if bid == ROSEMARY_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(5, 22), (12, 26), (20, 20)]:
                    pygame.draw.rect(s, (105, 140, 80), (stx, BLOCK_SIZE - sth, 2, sth))
                    for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
                        pygame.draw.rect(s, (125, 155, 95), (stx - 3, ny, 4, 1))
                        pygame.draw.rect(s, (125, 155, 95), (stx + 2, ny + 1, 4, 1))
                surfs[bid] = s
                continue
            if bid == ROSEMARY_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(7, 14), (15, 18), (23, 12)]:
                    pygame.draw.rect(s, (110, 148, 85), (stx, BLOCK_SIZE - sth, 2, sth))
                    for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
                        pygame.draw.rect(s, (130, 162, 98), (stx - 2, ny, 3, 1))
                surfs[bid] = s
                continue
            if bid == ROSEMARY_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(4, 24), (12, 28), (20, 22)]:
                    pygame.draw.rect(s, (105, 140, 80), (stx, BLOCK_SIZE - sth, 2, sth))
                    for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
                        pygame.draw.rect(s, (130, 158, 98), (stx - 4, ny, 5, 1))
                        pygame.draw.rect(s, (130, 158, 98), (stx + 2, ny + 1, 5, 1))
                surfs[bid] = s
                continue
            if bid == CACTUS_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (60, 148, 55), (12, 4, 8, 28))
                pygame.draw.rect(s, (80, 168, 72), (13, 4, 4, 28))
                for sy in range(6, 30, 5):
                    pygame.draw.rect(s, (45, 125, 42), (11, sy, 10, 1))
                surfs[bid] = s
                continue
            if bid == CACTUS_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (55, 138, 48), (12, 2, 8, 30))
                pygame.draw.rect(s, (75, 158, 65), (13, 2, 4, 30))
                pygame.draw.rect(s, (55, 138, 48), (4, 10, 8, 6))
                pygame.draw.rect(s, (55, 138, 48), (20, 14, 8, 6))
                pygame.draw.rect(s, (55, 138, 48), (4, 4, 4, 8))
                pygame.draw.rect(s, (55, 138, 48), (24, 8, 4, 8))
                for sy in range(4, 30, 5):
                    pygame.draw.rect(s, (40, 112, 38), (11, sy, 10, 1))
                surfs[bid] = s
                continue
            if bid == DATE_PALM_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (158, 128, 68), (14, 18, 4, 14))
                for ang, ly in [(-0.8, 10), (-0.3, 5), (0.3, 5), (0.8, 10), (0.0, 3)]:
                    ex = int(14 + 14 * math.sin(ang))
                    ey = int(10 - 10 * math.cos(abs(ang)))
                    pygame.draw.line(s, (48, 175, 78), (14, 12), (ex, ey + ly), 2)
                    pygame.draw.ellipse(s, (55, 185, 82), (ex - 3, ey + ly - 2, 8, 4))
                surfs[bid] = s
                continue
            if bid == DATE_PALM_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (158, 128, 68), (14, 22, 4, 10))
                for ang2 in [-0.6, 0.0, 0.6]:
                    ex2 = int(14 + 10 * math.sin(ang2))
                    ey2 = int(16 - 8 * math.cos(abs(ang2)))
                    pygame.draw.line(s, (55, 182, 80), (14, 18), (ex2, ey2), 2)
                    pygame.draw.ellipse(s, (65, 192, 88), (ex2 - 2, ey2 - 2, 6, 4))
                surfs[bid] = s
                continue
            if bid == DATE_PALM_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (158, 128, 68), (14, 14, 4, 18))
                for ang3 in [-0.9, -0.4, 0.0, 0.4, 0.9]:
                    ex3 = int(14 + 14 * math.sin(ang3))
                    ey3 = int(10 - 10 * math.cos(abs(ang3)))
                    pygame.draw.line(s, (48, 175, 78), (14, 12), (ex3, ey3 + 2), 2)
                    pygame.draw.ellipse(s, (55, 185, 82), (ex3 - 3, ey3, 8, 4))
                for dx3, dy3 in [(10, 16), (16, 14), (20, 18)]:
                    pygame.draw.ellipse(s, (175, 108, 28), (dx3, dy3, 5, 7))
                surfs[bid] = s
                continue
            if bid == AGAVE_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for ang4, base_y, dist in [(-0.7, 22, 12), (0.7, 22, 12),
                                            (-0.3, 20, 14), (0.3, 20, 14), (0.0, 18, 16)]:
                    ex4 = int(16 + dist * math.sin(ang4))
                    ey4 = int(base_y - dist * math.cos(abs(ang4)))
                    pygame.draw.line(s, (75, 150, 95), (16, base_y), (ex4, ey4), 5)
                    pygame.draw.polygon(s, (55, 128, 78),
                                        [(ex4 - 2, ey4), (ex4 + 2, ey4), (ex4, ey4 - 3)])
                surfs[bid] = s
                continue
            if bid == AGAVE_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for ang5, dist5 in [(-0.5, 10), (0.0, 12), (0.5, 10)]:
                    ex5 = int(16 + dist5 * math.sin(ang5))
                    ey5 = int(24 - dist5 * math.cos(abs(ang5)))
                    pygame.draw.line(s, (70, 162, 88), (16, 26), (ex5, ey5), 4)
                    pygame.draw.polygon(s, (55, 145, 75),
                                        [(ex5 - 2, ey5), (ex5 + 2, ey5), (ex5, ey5 - 3)])
                surfs[bid] = s
                continue
            if bid == AGAVE_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for ang6, dist6, base_y6 in [(-0.8, 12, 22), (-0.4, 14, 20), (0.0, 16, 18),
                                              (0.4, 14, 20), (0.8, 12, 22)]:
                    ex6 = int(16 + dist6 * math.sin(ang6))
                    ey6 = int(base_y6 - dist6 * math.cos(abs(ang6)))
                    pygame.draw.line(s, (80, 158, 100), (16, base_y6), (ex6, ey6), 5)
                    pygame.draw.polygon(s, (60, 138, 82),
                                        [(ex6 - 2, ey6), (ex6 + 2, ey6), (ex6, ey6 - 4)])
                pygame.draw.rect(s, (100, 175, 115), (14, 2, 4, 16))
                pygame.draw.polygon(s, (80, 158, 100), [(16, 0), (13, 4), (19, 4)])
                surfs[bid] = s
                continue
            if bid == SAGUARO_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (52, 142, 48), (13, 2, 6, 30))
                pygame.draw.rect(s, (72, 162, 65), (14, 2, 3, 30))
                for ry in range(4, 30, 4):
                    pygame.draw.rect(s, (40, 115, 38), (12, ry, 8, 1))
                surfs[bid] = s
                continue
            if bid == SAGUARO_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (52, 142, 48), (12, 0, 8, 32))
                pygame.draw.rect(s, (72, 162, 65), (13, 0, 4, 32))
                pygame.draw.rect(s, (52, 142, 48), (4, 12, 8, 6))
                pygame.draw.rect(s, (52, 142, 48), (4, 2, 6, 12))
                pygame.draw.rect(s, (72, 162, 65), (5, 2, 3, 12))
                pygame.draw.rect(s, (52, 142, 48), (20, 16, 8, 6))
                pygame.draw.rect(s, (52, 142, 48), (22, 6, 6, 12))
                pygame.draw.rect(s, (72, 162, 65), (23, 6, 3, 12))
                for ry in range(2, 30, 4):
                    pygame.draw.rect(s, (40, 115, 38), (11, ry, 10, 1))
                surfs[bid] = s
                continue
            if bid == BARREL_CACTUS_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.ellipse(s, (62, 148, 55), (6, 8, 20, 22))
                pygame.draw.ellipse(s, (78, 165, 68), (8, 10, 14, 16))
                for rx in range(9, 26, 3):
                    pygame.draw.line(s, (48, 122, 42), (rx, 9), (rx, 29), 1)
                for sx_off in [-3, 0, 3]:
                    pygame.draw.line(s, (210, 192, 128), (16 + sx_off, 8), (16 + sx_off, 4), 1)
                surfs[bid] = s
                continue
            if bid == BARREL_CACTUS_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.ellipse(s, (58, 142, 52), (5, 6, 22, 24))
                pygame.draw.ellipse(s, (74, 158, 64), (7, 8, 16, 18))
                for rx in range(8, 27, 3):
                    pygame.draw.line(s, (45, 118, 40), (rx, 8), (rx, 29), 1)
                pygame.draw.ellipse(s, (235, 175, 35), (10, 2, 12, 7))
                pygame.draw.ellipse(s, (255, 145, 15), (12, 3, 8, 5))
                surfs[bid] = s
                continue
            if bid == OCOTILLO_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                tips_y = [(10, 1), (14, 0), (18, 2), (22, 4)]
                for tx, ty in tips_y:
                    pygame.draw.line(s, (148, 82, 38), (16, 30), (tx, ty), 2)
                    for t in [0.3, 0.55, 0.75]:
                        mx = int(16 + (tx - 16) * t)
                        my = int(30 + (ty - 30) * t)
                        pygame.draw.line(s, (175, 108, 55), (mx, my), (mx - 2, my - 2), 1)
                surfs[bid] = s
                continue
            if bid == OCOTILLO_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                tips_m = [(9, 2), (14, 0), (18, 1), (23, 3)]
                for tx, ty in tips_m:
                    pygame.draw.line(s, (142, 78, 35), (16, 30), (tx, ty), 2)
                    for t in [0.3, 0.55, 0.75]:
                        mx = int(16 + (tx - 16) * t)
                        my = int(30 + (ty - 30) * t)
                        pygame.draw.line(s, (170, 105, 52), (mx, my), (mx - 2, my - 2), 1)
                    pygame.draw.ellipse(s, (215, 52, 38), (tx - 3, ty - 2, 7, 5))
                    pygame.draw.ellipse(s, (235, 75, 55), (tx - 2, ty - 1, 5, 3))
                surfs[bid] = s
                continue
            if bid == PRICKLY_PEAR_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.ellipse(s, (68, 155, 62), (5, 14, 14, 18))
                pygame.draw.ellipse(s, (72, 162, 68), (10, 5, 13, 17))
                for px_s, py_s in [(10, 18), (16, 16), (13, 22), (14, 9), (18, 12)]:
                    pygame.draw.circle(s, (205, 192, 135), (px_s, py_s), 1)
                surfs[bid] = s
                continue
            if bid == PRICKLY_PEAR_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.ellipse(s, (62, 148, 58), (3, 16, 14, 16))
                pygame.draw.ellipse(s, (68, 155, 62), (14, 12, 14, 18))
                pygame.draw.ellipse(s, (65, 152, 60), (9, 4, 12, 16))
                for px_s, py_s in [(8, 20), (18, 16), (14, 7), (11, 25)]:
                    pygame.draw.circle(s, (200, 188, 130), (px_s, py_s), 1)
                pygame.draw.ellipse(s, (178, 42, 98), (15, 4, 8, 10))
                pygame.draw.ellipse(s, (155, 32, 82), (5, 14, 7, 9))
                surfs[bid] = s
                continue
            if bid == CHOLLA_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (82, 155, 72), (13, 14, 6, 18))
                pygame.draw.rect(s, (82, 155, 72), (13, 10, 6, 6))
                pygame.draw.rect(s, (82, 155, 72), (6, 10, 7, 5))
                pygame.draw.rect(s, (82, 155, 72), (5, 4, 6, 8))
                pygame.draw.rect(s, (82, 155, 72), (19, 12, 7, 5))
                for cy in range(15, 31, 3):
                    pygame.draw.line(s, (215, 200, 148), (12, cy), (9, cy - 2), 1)
                    pygame.draw.line(s, (215, 200, 148), (19, cy), (22, cy - 2), 1)
                surfs[bid] = s
                continue
            if bid == CHOLLA_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (78, 150, 68), (13, 8, 6, 24))
                pygame.draw.rect(s, (78, 150, 68), (5, 8, 8, 5))
                pygame.draw.rect(s, (78, 150, 68), (4, 2, 6, 8))
                pygame.draw.rect(s, (78, 150, 68), (19, 12, 8, 5))
                pygame.draw.rect(s, (78, 150, 68), (21, 5, 6, 8))
                for cy in range(9, 31, 3):
                    pygame.draw.line(s, (210, 195, 142), (12, cy), (9, cy - 2), 1)
                    pygame.draw.line(s, (210, 195, 142), (19, cy), (22, cy - 2), 1)
                for fx, fy in [(13, 8), (13, 16), (19, 13)]:
                    pygame.draw.ellipse(s, (155, 178, 75), (fx, fy, 6, 5))
                surfs[bid] = s
                continue
            if bid == PALO_VERDE_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (95, 148, 72), (14, 14, 4, 18))
                for ang_pv, base_pv in [(-0.6, 14), (0.5, 14)]:
                    ex_pv = int(16 + 10 * math.sin(ang_pv))
                    ey_pv = int(14 - 8 * math.cos(abs(ang_pv)))
                    pygame.draw.line(s, (95, 148, 72), (16, 14), (ex_pv, ey_pv), 2)
                    pygame.draw.ellipse(s, (78, 168, 62), (ex_pv - 4, ey_pv - 3, 10, 6))
                surfs[bid] = s
                continue
            if bid == PALO_VERDE_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (88, 142, 68), (14, 16, 4, 16))
                for ang_pvm in [-0.8, -0.25, 0.25, 0.8]:
                    ex_pvm = int(16 + 13 * math.sin(ang_pvm))
                    ey_pvm = int(14 - 10 * math.cos(abs(ang_pvm)))
                    pygame.draw.line(s, (88, 142, 68), (16, 16), (ex_pvm, ey_pvm), 2)
                    pygame.draw.ellipse(s, (225, 195, 45), (ex_pvm - 4, ey_pvm - 3, 10, 6))
                    pygame.draw.ellipse(s, (242, 215, 58), (ex_pvm - 2, ey_pvm - 1, 6, 3))
                surfs[bid] = s
                continue
            if bid == COFFEE_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (95, 65, 40), (15, 16, 2, 16))
                for lx, ly in [(4, 14), (20, 12), (8, 7), (18, 5), (12, 18)]:
                    pygame.draw.ellipse(s, (40, 100, 45), (lx, ly, 9, 5))
                    pygame.draw.ellipse(s, (62, 128, 58), (lx + 2, ly + 1, 5, 2))
                for cx, cy in [(11, 13), (21, 15), (16, 9)]:
                    pygame.draw.circle(s, (175, 40, 32), (cx, cy), 2)
                    pygame.draw.circle(s, (215, 85, 55), (cx - 1, cy - 1), 1)
                surfs[bid] = s
                continue
            if bid == COFFEE_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (95, 65, 40), (15, 18, 2, 14))
                pygame.draw.ellipse(s, (55, 135, 60), (6, 16, 10, 5))
                pygame.draw.ellipse(s, (55, 135, 60), (16, 14, 10, 5))
                pygame.draw.ellipse(s, (80, 165, 80), (8, 17, 6, 2))
                pygame.draw.ellipse(s, (80, 165, 80), (18, 15, 6, 2))
                surfs[bid] = s
                continue
            if bid == COFFEE_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (95, 65, 40), (15, 3, 2, 29))
                pygame.draw.rect(s, (95, 65, 40), (6, 11, 10, 1))
                pygame.draw.rect(s, (95, 65, 40), (16, 15, 10, 1))
                pygame.draw.rect(s, (95, 65, 40), (6, 22, 10, 1))
                pygame.draw.rect(s, (95, 65, 40), (16, 19, 10, 1))
                for lx, ly in [(2, 6), (19, 4), (3, 16), (20, 12), (4, 23), (20, 23)]:
                    pygame.draw.ellipse(s, (35, 92, 40), (lx, ly, 9, 5))
                    pygame.draw.ellipse(s, (58, 128, 58), (lx + 2, ly + 1, 5, 2))
                for cx, cy in [(7, 12), (11, 13), (19, 16), (23, 16),
                               (8, 23), (12, 24), (20, 20), (24, 20)]:
                    pygame.draw.circle(s, (180, 38, 28), (cx, cy), 2)
                    pygame.draw.circle(s, (225, 90, 55), (cx - 1, cy - 1), 1)
                surfs[bid] = s
                continue
            if bid == GRAPEVINE_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (90, 58, 30), (15, 18, 2, 14))
                for lx, ly in [(3, 14), (19, 12), (7, 7), (17, 5), (10, 18)]:
                    pygame.draw.ellipse(s, (45, 110, 40), (lx, ly, 10, 6))
                    pygame.draw.ellipse(s, (70, 145, 60), (lx + 2, ly + 1, 6, 3))
                for cx, cy in [(10, 17), (13, 15), (20, 19), (18, 16)]:
                    pygame.draw.circle(s, (90, 30, 100), (cx, cy), 2)
                    pygame.draw.circle(s, (135, 70, 148), (cx - 1, cy - 1), 1)
                surfs[bid] = s
                continue
            if bid == GRAPEVINE_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (100, 68, 38), (15, 10, 2, 22))
                pygame.draw.ellipse(s, (55, 135, 55), (5, 16, 10, 6))
                pygame.draw.ellipse(s, (55, 135, 55), (17, 13, 10, 6))
                pygame.draw.ellipse(s, (85, 170, 80), (7, 17, 6, 2))
                pygame.draw.ellipse(s, (85, 170, 80), (19, 14, 6, 2))
                surfs[bid] = s
                continue
            if bid == GRAPEVINE_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.rect(s, (100, 68, 38), (15, 3, 2, 29))
                pygame.draw.rect(s, (70, 50, 30), (5, 9, 10, 1))
                pygame.draw.rect(s, (70, 50, 30), (17, 12, 10, 1))
                for lx, ly in [(2, 4), (18, 2), (3, 13), (19, 9), (4, 21), (19, 19)]:
                    pygame.draw.ellipse(s, (38, 100, 42), (lx, ly, 10, 6))
                    pygame.draw.ellipse(s, (62, 135, 62), (lx + 2, ly + 1, 6, 2))
                for cx, cy in [(6, 14), (9, 14), (12, 14), (7, 18), (10, 18), (8, 22)]:
                    pygame.draw.circle(s, (95, 28, 105), (cx, cy), 2)
                    pygame.draw.circle(s, (140, 70, 150), (cx - 1, cy - 1), 1)
                for cx, cy in [(19, 17), (22, 17), (25, 17), (20, 21), (23, 21), (21, 25)]:
                    pygame.draw.circle(s, (95, 28, 105), (cx, cy), 2)
                    pygame.draw.circle(s, (140, 70, 150), (cx - 1, cy - 1), 1)
                surfs[bid] = s
                continue
            # -- artisan bench decorative blocks --
            if bid == POLISHED_GRANITE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 22)
                lt = _lighter(c, 15)
                for px2, py2 in [(5,4),(13,8),(21,5),(8,18),(26,14),(17,23),(3,27),(28,7),(10,29)]:
                    pygame.draw.rect(s, dk, (px2, py2, 2, 1))
                    pygame.draw.rect(s, dk, (px2+1, py2+1, 1, 2))
                pygame.draw.line(s, lt, (2, 2), (BLOCK_SIZE-2, 4), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == POLISHED_MARBLE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                vn = _darken(c, 50)
                lt = _lighter(c, 10)
                pygame.draw.line(s, vn, (6, 0), (30, 26), 1)
                pygame.draw.line(s, lt, (7, 0), (31, 26), 1)
                pygame.draw.line(s, vn, (0, 8), (22, 32), 1)
                pygame.draw.line(s, vn, (14, 0), (32, 18), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == SLATE_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 22)
                dk = _darken(c, 30)
                pygame.draw.line(s, dk, (16, 0), (16, BLOCK_SIZE), 2)
                pygame.draw.line(s, dk, (0, 16), (BLOCK_SIZE, 16), 2)
                for tx2, ty2 in [(2,2),(18,2),(2,18),(18,18)]:
                    pygame.draw.line(s, lt, (tx2, ty2), (tx2+12, ty2), 1)
                pygame.draw.rect(s, dk, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == TERRACOTTA_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 20)
                pygame.draw.ellipse(s, dk, (5, 7, 22, 18), 1)
                pygame.draw.ellipse(s, dk, (9, 11, 14, 10), 1)
                pygame.draw.ellipse(s, lt, (7, 9, 18, 14), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid in (MOSSY_BRICK, CREAM_BRICK, LAPIS_BRICK, GILDED_BRICK, IVORY_BRICK, CRIMSON_BRICK):
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                mortar_amt = 45 if bid == CRIMSON_BRICK else 35
                s.fill(_darken(c, mortar_amt))
                bw, bh, gap = 13, 7, 2
                for row in range(4):
                    off = (bw // 2 + 1) if row % 2 else 0
                    y2 = row * (bh + gap) + 1
                    for col in range(-1, 3):
                        x2 = col * (bw + gap) + off
                        cx2 = max(0, x2)
                        cw2 = min(x2 + bw, BLOCK_SIZE) - cx2
                        if cw2 <= 0:
                            continue
                        pygame.draw.rect(s, c, (cx2, y2, cw2, bh))
                if bid == MOSSY_BRICK:
                    for mx2, my2 in [(2,2),(18,10),(5,20),(24,17),(11,28)]:
                        pygame.draw.rect(s, (75, 125, 50), (mx2, my2, 3, 2))
                elif bid == LAPIS_BRICK:
                    for gx2, gy2 in [(7,0),(22,9),(14,18),(4,27),(29,0)]:
                        pygame.draw.circle(s, (225, 190, 60), (gx2, gy2), 1)
                elif bid == GILDED_BRICK:
                    for gy2 in [0, 9, 18, 27]:
                        pygame.draw.line(s, (235, 200, 55), (0, gy2), (BLOCK_SIZE, gy2), 2)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid in (CHARCOAL_PLANK, WALNUT_PLANK, TEAK_PLANK, CEDAR_PANEL, EBONY_PLANK, MAHOGANY_PLANK):
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 16)
                grain = _darken(c, 13)
                pygame.draw.line(s, dk, (0, 10), (BLOCK_SIZE, 10), 2)
                pygame.draw.line(s, dk, (0, 21), (BLOCK_SIZE, 21), 2)
                pygame.draw.line(s, lt, (0, 1), (BLOCK_SIZE, 1), 1)
                pygame.draw.line(s, lt, (0, 12), (BLOCK_SIZE, 12), 1)
                pygame.draw.line(s, lt, (0, 23), (BLOCK_SIZE, 23), 1)
                for gx2 in [7, 16, 25]:
                    pygame.draw.line(s, grain, (gx2, 2), (gx2, 9), 1)
                    pygame.draw.line(s, grain, (gx2, 13), (gx2, 20), 1)
                    pygame.draw.line(s, grain, (gx2, 24), (gx2, 30), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == OAK_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                grain = _darken(c, 14)
                for py2 in [7, 15, 23]:
                    pygame.draw.line(s, dk, (0, py2), (BLOCK_SIZE, py2), 2)
                pygame.draw.line(s, lt, (0, 1), (BLOCK_SIZE, 1), 1)
                for gx2 in [8, 18, 26]:
                    for sy2, sh2 in [(1,5),(9,5),(17,5),(25,5)]:
                        pygame.draw.line(s, grain, (gx2, sy2+1), (gx2, sy2+sh2-1), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BAMBOO_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 25)
                lt = _lighter(c, 20)
                for sy2 in range(0, BLOCK_SIZE, 5):
                    pygame.draw.line(s, dk, (0, sy2+4), (BLOCK_SIZE, sy2+4), 1)
                for nx2 in [6, 18, 28]:
                    for ny2 in [1, 6, 11, 16, 21, 26]:
                        pygame.draw.rect(s, lt, (nx2-2, ny2, 4, 2))
                        pygame.draw.rect(s, dk, (nx2-2, ny2+2, 4, 1))
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == OBSIDIAN_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 35)
                pygame.draw.line(s, lt, (17, 0), (17, BLOCK_SIZE), 2)
                pygame.draw.line(s, lt, (0, 17), (BLOCK_SIZE, 17), 2)
                pygame.draw.rect(s, lt, (2, 2, 7, 3))
                pygame.draw.rect(s, lt, (19, 2, 7, 3))
                pygame.draw.rect(s, lt, (2, 19, 7, 3))
                pygame.draw.rect(s, lt, (19, 19, 7, 3))
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == COBBLESTONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 30))
                lt = _lighter(c, 20)
                for cx2, cy2, cw2, ch2 in [
                    (1,1,12,8),(15,2,15,7),(1,10,9,8),(11,10,11,8),(23,10,7,8),
                    (1,19,14,8),(16,19,14,8),(1,28,10,3),(12,28,8,3),(21,28,9,3),
                ]:
                    pygame.draw.ellipse(s, c, (cx2, cy2, cw2, ch2))
                    pygame.draw.ellipse(s, lt, (cx2+1, cy2+1, max(3, cw2-4), 2))
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BASALT_COLUMN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 25)
                dk = _darken(c, 20)
                for cx2 in [5, 11, 17, 23]:
                    pygame.draw.line(s, dk, (cx2, 0), (cx2, BLOCK_SIZE), 1)
                    pygame.draw.line(s, lt, (cx2+1, 0), (cx2+1, BLOCK_SIZE), 1)
                pygame.draw.line(s, dk, (0, 16), (BLOCK_SIZE, 16), 2)
                pygame.draw.line(s, lt, (0, 17), (BLOCK_SIZE, 17), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == LIMESTONE_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 20)
                lt = _lighter(c, 12)
                for sy2 in [8, 16, 24]:
                    pygame.draw.line(s, dk, (0, sy2), (BLOCK_SIZE, sy2), 1)
                    pygame.draw.line(s, lt, (0, sy2+1), (BLOCK_SIZE, sy2+1), 1)
                pygame.draw.ellipse(s, dk, (18, 3, 8, 5), 1)
                pygame.draw.line(s, dk, (22, 3), (22, 7), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == COPPER_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 20)
                pygame.draw.line(s, dk, (16, 0), (16, BLOCK_SIZE), 2)
                pygame.draw.line(s, dk, (0, 16), (BLOCK_SIZE, 16), 2)
                for rx2, ry2 in [(4,4),(24,4),(4,24),(24,24)]:
                    pygame.draw.circle(s, dk, (rx2, ry2), 2)
                    pygame.draw.circle(s, lt, (rx2-1, ry2-1), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == DRIFTWOOD_PLANK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 25)
                lt = _lighter(c, 15)
                grain = _darken(c, 12)
                pygame.draw.line(s, dk, (0, 10), (BLOCK_SIZE, 10), 2)
                pygame.draw.line(s, dk, (0, 22), (BLOCK_SIZE, 22), 2)
                for gx2 in [5, 13, 21, 29]:
                    pygame.draw.line(s, grain, (gx2, 1), (gx2, 9), 1)
                    pygame.draw.line(s, grain, (gx2+1, 12), (gx2+1, 21), 1)
                    pygame.draw.line(s, grain, (gx2, 24), (gx2, 30), 1)
                pygame.draw.line(s, dk, (19, 12), (21, 20), 1)
                pygame.draw.line(s, dk, (8, 1), (9, 8), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == JADE_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                vn = _darken(c, 35)
                lt = _lighter(c, 20)
                pygame.draw.line(s, vn, (3, 0), (20, 32), 1)
                pygame.draw.line(s, lt, (4, 0), (21, 32), 1)
                pygame.draw.line(s, vn, (22, 0), (32, 12), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ROSE_QUARTZ_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 20)
                dk = _darken(c, 30)
                pygame.draw.line(s, dk, (16, 0), (32, 16), 1)
                pygame.draw.line(s, lt, (17, 0), (32, 15), 1)
                pygame.draw.line(s, dk, (0, 16), (16, 32), 1)
                pygame.draw.line(s, lt, (0, 15), (15, 0), 1)
                pygame.draw.line(s, dk, (0, 0), (32, 32), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == AMETHYST_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 30)
                dk = _darken(c, 40)
                for cx2, cw2, ch2 in [(2,6,14),(9,5,20),(16,6,16),(22,5,12),(27,4,18)]:
                    pygame.draw.polygon(s, dk, [(cx2, BLOCK_SIZE), (cx2+cw2, BLOCK_SIZE), (cx2+cw2//2, BLOCK_SIZE-ch2)])
                    pygame.draw.line(s, lt, (cx2+cw2//2, BLOCK_SIZE-ch2), (cx2+cw2//2-1, BLOCK_SIZE-ch2//2), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == AMBER_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 25)
                dk = _darken(c, 30)
                pygame.draw.line(s, lt, (2, 3), (28, 6), 1)
                pygame.draw.ellipse(s, dk, (8, 12, 5, 4), 1)
                pygame.draw.ellipse(s, dk, (19, 8, 4, 3), 1)
                pygame.draw.ellipse(s, dk, (14, 20, 6, 5), 1)
                pygame.draw.ellipse(s, lt, (9, 13, 2, 2))
                pygame.draw.ellipse(s, lt, (15, 21, 2, 2))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ASH_PLANK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 22)
                lt = _lighter(c, 14)
                grain = _darken(c, 10)
                for py2 in [7, 15, 23]:
                    pygame.draw.line(s, dk, (0, py2), (BLOCK_SIZE, py2), 2)
                pygame.draw.line(s, lt, (0, 1), (BLOCK_SIZE, 1), 1)
                for gx2 in [9, 20, 28]:
                    for sy2, sh2 in [(1,5),(9,5),(17,5),(25,5)]:
                        pygame.draw.line(s, grain, (gx2, sy2+1), (gx2, sy2+sh2-1), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == FROSTED_GLASS:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 22)
                dk = _darken(c, 20)
                for fx, fy in [(9, 9), (23, 23), (9, 23)]:
                    for dx2, dy2 in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]:
                        ex2 = min(max(fx + dx2*7, 0), BLOCK_SIZE-1)
                        ey2 = min(max(fy + dy2*7, 0), BLOCK_SIZE-1)
                        pygame.draw.line(s, lt, (fx, fy), (ex2, ey2), 1)
                pygame.draw.rect(s, dk, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == TERRACOTTA_SHINGLE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 18)
                for row in range(3):
                    sy2 = row * 11 + 2
                    off = 8 if row % 2 else 0
                    for col in range(-1, 3):
                        sx2 = col * 16 + off
                        pygame.draw.arc(s, dk, (sx2, sy2, 16, 14), 0, math.pi, 2)
                        pygame.draw.line(s, lt, (sx2+2, sy2+2), (sx2+14, sy2+2), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == THATCH_ROOF:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                for i in range(-2, 6):
                    ox = i * 6
                    pygame.draw.line(s, dk, (ox, 0), (ox+BLOCK_SIZE, BLOCK_SIZE), 1)
                    pygame.draw.line(s, lt, (ox+2, 0), (ox+2+BLOCK_SIZE, BLOCK_SIZE), 1)
                for hy2 in [8, 16, 24]:
                    pygame.draw.line(s, dk, (0, hy2), (BLOCK_SIZE, hy2), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == VERDIGRIS_COPPER:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 22)
                for px2, py2, pw2, ph2 in [(3,2,8,6),(18,5,7,5),(6,16,9,7),(20,18,8,6),(2,26,6,4)]:
                    pygame.draw.ellipse(s, lt, (px2, py2, pw2, ph2))
                    pygame.draw.ellipse(s, dk, (px2+1, py2+1, max(2, pw2-2), max(2, ph2-2)), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == SILVER_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 25)
                dk = _darken(c, 20)
                for ly2 in range(1, BLOCK_SIZE-1, 3):
                    col2 = lt if (ly2 // 3) % 2 == 0 else dk
                    pygame.draw.line(s, col2, (1, ly2), (BLOCK_SIZE-2, ly2), 1)
                pygame.draw.line(s, dk, (BLOCK_SIZE//2, 0), (BLOCK_SIZE//2, BLOCK_SIZE), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == GOLD_LEAF_TRIM:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 20)
                dk = _darken(c, 35)
                for py2 in [5, 12, 19, 26]:
                    pygame.draw.line(s, dk, (0, py2), (BLOCK_SIZE, py2+3), 1)
                    pygame.draw.line(s, lt, (0, py2+1), (BLOCK_SIZE, py2+4), 1)
                for px2 in [8, 18, 26]:
                    pygame.draw.line(s, dk, (px2, 0), (px2-2, BLOCK_SIZE), 1)
                pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid in (STAINED_GLASS_RED, STAINED_GLASS_BLUE, STAINED_GLASS_GREEN):
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 40)
                s.fill(lt)
                lead = (30, 30, 30)
                pygame.draw.rect(s, lead, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 3)
                pygame.draw.line(s, lead, (BLOCK_SIZE//2, 0), (BLOCK_SIZE//2, BLOCK_SIZE), 3)
                pygame.draw.line(s, lead, (0, BLOCK_SIZE//2), (BLOCK_SIZE, BLOCK_SIZE//2), 3)
                for qx2, qy2 in [(3,3),(19,3),(3,19),(19,19)]:
                    pygame.draw.rect(s, c, (qx2+1, qy2+1, 11, 11))
                    pygame.draw.line(s, lt, (qx2+1, qy2+1), (qx2+7, qy2+1), 1)
                    pygame.draw.line(s, lt, (qx2+1, qy2+1), (qx2+1, qy2+5), 1)
                pygame.draw.rect(s, lead, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == QUARTZ_PILLAR:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 12)
                dk = _darken(c, 20)
                for cx2 in [4, 10, 16, 22, 28]:
                    pygame.draw.line(s, dk, (cx2, 2), (cx2, BLOCK_SIZE-3), 1)
                    pygame.draw.line(s, lt, (cx2+1, 2), (cx2+1, BLOCK_SIZE-3), 1)
                pygame.draw.line(s, dk, (1, 3), (BLOCK_SIZE-2, 3), 2)
                pygame.draw.line(s, dk, (1, BLOCK_SIZE-4), (BLOCK_SIZE-2, BLOCK_SIZE-4), 2)
                pygame.draw.line(s, lt, (1, 4), (BLOCK_SIZE-2, 4), 1)
                pygame.draw.line(s, lt, (1, BLOCK_SIZE-3), (BLOCK_SIZE-2, BLOCK_SIZE-3), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ONYX_INLAY:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 35)
                cx2, cy2 = BLOCK_SIZE // 2, BLOCK_SIZE // 2
                pygame.draw.polygon(s, lt, [(cx2, cy2-9),(cx2+9, cy2),(cx2, cy2+9),(cx2-9, cy2)], 2)
                pygame.draw.polygon(s, lt, [(cx2, cy2-4),(cx2+4, cy2),(cx2, cy2+4),(cx2-4, cy2)])
                pygame.draw.line(s, lt, (2, 2), (8, 4), 1)
                pygame.draw.line(s, lt, (2, 3), (6, 3), 1)
                pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == WHITE_PLASTER_WALL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 12)
                pygame.draw.line(s, dk, (0, 10), (BLOCK_SIZE, 10), 1)
                pygame.draw.line(s, dk, (0, 21), (BLOCK_SIZE, 21), 1)
                pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CARVED_PLASTER:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                gold = (200, 165, 60)
                cx2, cy2 = BLOCK_SIZE // 2, BLOCK_SIZE // 2
                pts = []
                for i in range(16):
                    a = math.pi * i / 8
                    r = 11 if i % 2 == 0 else 5
                    pts.append((cx2 + int(r * math.cos(a)), cy2 + int(r * math.sin(a))))
                pygame.draw.polygon(s, gold, pts, 1)
                for ox, oy in [(4, 4), (BLOCK_SIZE-4, 4), (4, BLOCK_SIZE-4), (BLOCK_SIZE-4, BLOCK_SIZE-4)]:
                    pygame.draw.polygon(s, gold, [(ox, oy-3), (ox+3, oy), (ox, oy+3), (ox-3, oy)], 1)
                pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MUQARNAS_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                for nx in [1, 11, 21]:
                    pygame.draw.rect(s, dk, (nx, 6, 9, 24))
                    pygame.draw.line(s, lt, (nx+1, 7), (nx+1, 28), 1)
                    pygame.draw.rect(s, c, (nx+2, 13, 5, 17))
                    pygame.draw.rect(s, _darken(c, 42), (nx+3, 20, 3, 10))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MASHRABIYA:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_lighter(c, 25))
                for i in range(-BLOCK_SIZE, BLOCK_SIZE * 2, 7):
                    pygame.draw.line(s, c, (i, 0), (i + BLOCK_SIZE, BLOCK_SIZE), 2)
                    pygame.draw.line(s, c, (i, BLOCK_SIZE), (i + BLOCK_SIZE, 0), 2)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ZELLIGE_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                tile_colors = [
                    (55, 130, 175),
                    (215, 165, 45),
                    (235, 235, 220),
                    (40, 90, 160),
                ]
                tsz = 8
                for ty in range(0, BLOCK_SIZE, tsz):
                    for tx in range(0, BLOCK_SIZE, tsz):
                        tc = tile_colors[((tx // tsz) + (ty // tsz)) % len(tile_colors)]
                        pygame.draw.rect(s, tc, (tx+1, ty+1, tsz-2, tsz-2))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ARABESQUE_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 22)
                cx2, cy2 = BLOCK_SIZE // 2, BLOCK_SIZE // 2
                hex_pts = [(cx2 + int(12 * math.cos(math.pi * i / 3)),
                            cy2 + int(12 * math.sin(math.pi * i / 3))) for i in range(6)]
                pygame.draw.polygon(s, dk, hex_pts, 1)
                star_pts = []
                for i in range(12):
                    a = math.pi * i / 6
                    r = 8 if i % 2 == 0 else 4
                    star_pts.append((cx2 + int(r * math.cos(a)), cy2 + int(r * math.sin(a))))
                pygame.draw.polygon(s, dk, star_pts, 1)
                for ox, oy in [(4, 4), (BLOCK_SIZE-4, 4), (4, BLOCK_SIZE-4), (BLOCK_SIZE-4, BLOCK_SIZE-4)]:
                    pygame.draw.circle(s, lt, (ox, oy), 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ADOBE_BRICK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                mortar = _darken(c, 40)
                s.fill(mortar)
                bw, bh, gap = 14, 8, 2
                for row in range(4):
                    off = (bw // 2 + 1) if row % 2 else 0
                    y2 = row * (bh + gap) + 1
                    for col in range(-1, 3):
                        x2 = col * (bw + gap) + off
                        cx2 = max(0, x2)
                        cw2 = min(x2 + bw, BLOCK_SIZE) - cx2
                        if cw2 <= 0:
                            continue
                        pygame.draw.rect(s, c, (cx2, y2, cw2, bh))
                        # straw flecks
                        pygame.draw.line(s, _darken(c, 15), (cx2+2, y2+3), (cx2+6, y2+2), 1)
                        pygame.draw.line(s, _darken(c, 15), (cx2+8, y2+5), (cx2+12, y2+4), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == SPANISH_ROOF_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 30))
                lt = _lighter(c, 18)
                for tx in [0, 11, 22]:
                    pygame.draw.ellipse(s, c,  (tx,  0, 10, BLOCK_SIZE))
                    pygame.draw.line(s, lt, (tx+2, 2), (tx+2, BLOCK_SIZE-3), 1)
                    pygame.draw.line(s, _darken(c, 25), (tx+9, 3), (tx+9, BLOCK_SIZE-3), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == WROUGHT_IRON_GRILLE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_lighter(c, 15))
                iron = c
                lt   = _lighter(c, 30)
                # vertical bars
                for vx in [4, 12, 20, 28]:
                    pygame.draw.line(s, iron, (vx, 1), (vx, BLOCK_SIZE-2), 2)
                # horizontal rails
                pygame.draw.line(s, iron, (1, 4),          (BLOCK_SIZE-2, 4),          2)
                pygame.draw.line(s, iron, (1, BLOCK_SIZE-5), (BLOCK_SIZE-2, BLOCK_SIZE-5), 2)
                # scroll curls between bars
                for sx in [8, 24]:
                    pygame.draw.circle(s, lt, (sx, 11), 3, 1)
                    pygame.draw.circle(s, lt, (sx, BLOCK_SIZE-12), 3, 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == TALAVERA_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                blue     = (55, 95, 175)
                mid_blue = (100, 140, 210)
                cx2, cy2 = BLOCK_SIZE // 2, BLOCK_SIZE // 2
                # central floral motif
                pygame.draw.circle(s, blue, (cx2, cy2), 7, 1)
                pygame.draw.circle(s, mid_blue, (cx2, cy2), 3)
                for i in range(4):
                    a = math.pi * i / 2
                    px, py = cx2 + int(9 * math.cos(a)), cy2 + int(9 * math.sin(a))
                    pygame.draw.circle(s, blue, (px, py), 3)
                # corner accents
                for ox, oy in [(3, 3), (BLOCK_SIZE-3, 3), (3, BLOCK_SIZE-3), (BLOCK_SIZE-3, BLOCK_SIZE-3)]:
                    pygame.draw.polygon(s, mid_blue, [(ox, oy-3), (ox+3, oy), (ox, oy+3), (ox-3, oy)])
                # border line
                pygame.draw.rect(s, blue, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == SALTILLO_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 22)
                lt = _lighter(c, 12)
                # square tile grid (2×2)
                half = BLOCK_SIZE // 2
                pygame.draw.line(s, dk, (half, 0), (half, BLOCK_SIZE), 2)
                pygame.draw.line(s, dk, (0, half), (BLOCK_SIZE, half), 2)
                # subtle surface variation per quadrant
                for qx, qy in [(2, 2), (half+2, 2), (2, half+2), (half+2, half+2)]:
                    pygame.draw.rect(s, lt, (qx, qy, 5, 3))
                pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
                surfs[bid] = s
                continue
            # ---- European architecture blocks ----
            if bid == HALF_TIMBER_WALL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                plaster = bdata["color"]
                beam    = (38, 25, 14)
                s.fill(plaster)
                pygame.draw.line(s, beam, (0, 15), (BLOCK_SIZE, 15), 3)  # horizontal rail
                pygame.draw.line(s, beam, (15, 0), (15, BLOCK_SIZE), 3)  # vertical stud
                pygame.draw.line(s, beam, (0, 0),  (15, 15),  2)         # diagonal TL
                pygame.draw.line(s, beam, (15, 15),(BLOCK_SIZE, 0), 2)   # diagonal TR
                pygame.draw.line(s, beam, (0, BLOCK_SIZE),(15, 15), 2)   # diagonal BL
                pygame.draw.line(s, beam, (15, 15),(BLOCK_SIZE, BLOCK_SIZE), 2)  # diagonal BR
                pygame.draw.rect(s, _darken(plaster, 12), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ASHLAR_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                mortar = _darken(c, 30)
                s.fill(mortar)
                for row, bh, off in [(0, 10, 0), (1, 10, 8), (2, 10, 0)]:
                    y2 = row * 11 + 1
                    for bx2 in range(-1, 3):
                        x2 = bx2 * 17 + off
                        cx2 = max(0, x2); cw2 = min(x2 + 15, BLOCK_SIZE) - cx2
                        if cw2 > 0:
                            pygame.draw.rect(s, c, (cx2, y2, cw2, bh))
                            pygame.draw.line(s, _lighter(c, 10), (cx2, y2), (cx2 + cw2, y2), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == GOTHIC_TRACERY:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 35)
                # Two lancet arches side by side
                for ax in [5, 18]:
                    pygame.draw.rect(s, lt, (ax, 14, 9, 16))
                    pygame.draw.arc(s, lt, (ax, 8, 9, 12), 0, math.pi, 2)
                # trefoil at top center
                for tx, ty in [(16, 5), (12, 3), (20, 3)]:
                    pygame.draw.circle(s, lt, (tx, ty), 3, 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == FLUTED_COLUMN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 14)
                for fx in [3, 9, 15, 21, 27]:
                    pygame.draw.line(s, dk, (fx, 3), (fx, BLOCK_SIZE-4), 1)
                    pygame.draw.line(s, lt, (fx+1, 3), (fx+1, BLOCK_SIZE-4), 1)
                pygame.draw.line(s, dk, (1, 2), (BLOCK_SIZE-2, 2), 2)
                pygame.draw.line(s, dk, (1, BLOCK_SIZE-3), (BLOCK_SIZE-2, BLOCK_SIZE-3), 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CORNICE_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 25)
                lt = _lighter(c, 15)
                # Top crown
                pygame.draw.rect(s, lt, (0, 0, BLOCK_SIZE, 8))
                pygame.draw.line(s, dk, (0, 8), (BLOCK_SIZE, 8), 2)
                # Middle bed
                pygame.draw.rect(s, _darken(c, 10), (2, 10, BLOCK_SIZE-4, 10))
                pygame.draw.line(s, dk, (0, 20), (BLOCK_SIZE, 20), 1)
                # Bottom soffit
                pygame.draw.rect(s, _darken(c, 18), (4, 22, BLOCK_SIZE-8, BLOCK_SIZE-24))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ROSE_WINDOW:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                gem  = (110, 160, 220)
                gold = (190, 160, 50)
                pygame.draw.circle(s, _lighter(c, 20), (cx2, cy2), 13, 2)
                pygame.draw.circle(s, gem, (cx2, cy2), 4)
                for i in range(8):
                    a = math.pi * i / 4
                    px = cx2 + int(9 * math.cos(a)); py = cy2 + int(9 * math.sin(a))
                    pygame.draw.line(s, gold, (cx2, cy2), (px, py), 1)
                    pygame.draw.circle(s, gem, (px, py), 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == HERRINGBONE_BRICK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 35))
                lt = _lighter(c, 8)
                bw, bh = 10, 4
                # Diagonal herringbone in two orientations
                for row in range(8):
                    for col in range(8):
                        x2 = (col - row) * (bw//2) + row * bh
                        y2 = row * (bh + 1)
                        if row % 2 == 0:
                            pygame.draw.rect(s, c,  (x2, y2, bw, bh))
                            pygame.draw.line(s, lt, (x2, y2), (x2+bw, y2), 1)
                        else:
                            pygame.draw.rect(s, _darken(c, 12), (x2, y2, bw, bh))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BAROQUE_TRIM:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                # Central cartouche
                pygame.draw.ellipse(s, dk, (8, 8, 16, 16), 1)
                pygame.draw.circle(s, lt, (16, 16), 4)
                # S-scroll arms
                pygame.draw.arc(s, dk, (0, 6, 10, 10), math.pi*0.5, math.pi*1.5, 2)
                pygame.draw.arc(s, dk, (22, 6, 10, 10), math.pi*1.5, math.pi*2.5, 2)
                pygame.draw.arc(s, dk, (4, 18, 8, 10), 0, math.pi, 2)
                pygame.draw.arc(s, dk, (20, 18, 8, 10), math.pi, math.pi*2, 2)
                # Border
                pygame.draw.line(s, dk, (0, 2), (BLOCK_SIZE, 2), 1)
                pygame.draw.line(s, dk, (0, BLOCK_SIZE-3), (BLOCK_SIZE, BLOCK_SIZE-3), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == TUDOR_BEAM:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt  = _lighter(c, 18)
                mid = _lighter(c, 8)
                # Wide horizontal plank bands
                for y2 in [0, 10, 21]:
                    pygame.draw.rect(s, mid, (0, y2, BLOCK_SIZE, 9))
                    pygame.draw.line(s, lt, (0, y2+1), (BLOCK_SIZE, y2+1), 1)
                    pygame.draw.line(s, _darken(c, 15), (0, y2+9), (BLOCK_SIZE, y2+9), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == VENETIAN_FLOOR:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                rose  = (200, 155, 155)
                gold  = (200, 175, 100)
                dk    = _darken(c, 20)
                half  = BLOCK_SIZE // 2
                pygame.draw.line(s, dk, (half, 0), (half, BLOCK_SIZE), 1)
                pygame.draw.line(s, dk, (0, half), (BLOCK_SIZE, half), 1)
                # Diamond insets in each quadrant
                for qx, qy, col in [(half//2, half//2, rose), (half + half//2, half//2, gold),
                                    (half//2, half + half//2, gold), (half + half//2, half + half//2, rose)]:
                    pygame.draw.polygon(s, col, [(qx, qy-5),(qx+5,qy),(qx,qy+5),(qx-5,qy)])
                    pygame.draw.polygon(s, dk,  [(qx, qy-5),(qx+5,qy),(qx,qy+5),(qx-5,qy)], 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == FLEMISH_BRICK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c  = bdata["color"]
                dk = _darken(c, 25)
                mortar = _darken(c, 40)
                s.fill(mortar)
                bh, gap = 7, 2
                for row in range(4):
                    y2 = row * (bh + gap) + 1
                    # Flemish bond: alternating header(5) stretcher(12) per row, offset each row
                    col_pos = 2 if row % 2 else 0
                    for bw2, bc in [(12, c), (5, dk), (12, c), (5, dk)]:
                        pygame.draw.rect(s, bc, (col_pos, y2, bw2, bh))
                        col_pos += bw2 + gap
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PILASTER:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c    = bdata["color"]
                shaft= _lighter(c, 12)
                dk   = _darken(c, 22)
                s.fill(c)
                # Capital at top
                pygame.draw.rect(s, shaft, (6, 1, 20, 5))
                pygame.draw.line(s, dk, (6, 6), (26, 6), 1)
                # Shaft
                pygame.draw.rect(s, shaft, (10, 7, 12, 18))
                pygame.draw.line(s, dk, (10, 7), (10, 25), 1)
                pygame.draw.line(s, _lighter(c, 20), (11, 7), (11, 25), 1)
                # Base
                pygame.draw.rect(s, shaft, (6, 25, 20, 5))
                pygame.draw.line(s, dk, (6, 25), (26, 25), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == DENTIL_TRIM:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 15)
                # Top dentil row
                for tx in range(1, BLOCK_SIZE, 6):
                    pygame.draw.rect(s, dk, (tx, 1, 4, 7))
                # Bottom dentil row
                for tx in range(1, BLOCK_SIZE, 6):
                    pygame.draw.rect(s, dk, (tx, BLOCK_SIZE-8, 4, 7))
                # Central plain band
                pygame.draw.line(s, lt, (0, 12), (BLOCK_SIZE, 12), 1)
                pygame.draw.line(s, lt, (0, BLOCK_SIZE-13), (BLOCK_SIZE, BLOCK_SIZE-13), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == WATTLE_DAUB:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                wattle = _darken(c, 32)
                crack  = _darken(c, 20)
                # Woven wattle diagonals visible through thin plaster
                for i in range(-BLOCK_SIZE, BLOCK_SIZE*2, 6):
                    pygame.draw.line(s, wattle, (i, 0), (i+BLOCK_SIZE, BLOCK_SIZE), 1)
                    pygame.draw.line(s, wattle, (i, BLOCK_SIZE), (i+BLOCK_SIZE, 0), 1)
                # Plaster patches obscuring most of the wattle
                for px2, py2, pw2, ph2 in [(0,0,10,12),(12,0,20,8),(0,14,8,18),(10,10,22,12),(0,24,18,8),(20,20,12,12)]:
                    pygame.draw.rect(s, c, (px2, py2, pw2, ph2))
                # Crack lines
                pygame.draw.line(s, crack, (10, 12), (14, 22), 1)
                pygame.draw.line(s, crack, (20, 8),  (24, 16), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == NORDIC_PLANK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c  = bdata["color"]
                lt = _lighter(c, 15)
                dk = _darken(c, 15)
                s.fill(c)
                # Three distinct planks with grain
                for y2, shade in [(0, lt), (10, c), (21, dk)]:
                    pygame.draw.rect(s, shade, (0, y2, BLOCK_SIZE, 9))
                    pygame.draw.line(s, _darken(shade, 12), (0, y2+1), (BLOCK_SIZE, y2+1), 1)
                # Knots
                for kx2, ky2 in [(7, 4), (22, 15), (12, 24)]:
                    pygame.draw.circle(s, dk, (kx2, ky2), 2, 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MANSARD_SLATE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 18)
                s.fill(_darken(c, 15))
                # Fish-scale rows
                for row in range(4):
                    y2 = row * 8
                    off = 4 if row % 2 else 0
                    for col in range(-1, 5):
                        cx3 = col * 8 + off
                        pygame.draw.arc(s, lt, (cx3, y2, 8, 10), 0, math.pi, 2)
                        pygame.draw.line(s, _darken(c, 25), (cx3, y2+5), (cx3+8, y2+5), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ROMAN_MOSAIC:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 25))
                palette = [(178, 162, 128), (200, 140,  80), (215, 195, 155), (145,  95,  60)]
                tsz = 4
                for ty in range(0, BLOCK_SIZE, tsz):
                    for tx in range(0, BLOCK_SIZE, tsz):
                        tc = palette[((tx//tsz)*3 + (ty//tsz)*2) % len(palette)]
                        pygame.draw.rect(s, tc, (tx+1, ty+1, tsz-1, tsz-1))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == SETT_STONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 30))
                lt = _lighter(c, 10)
                for row in range(4):
                    off = 4 if row % 2 else 0
                    for col in range(-1, 4):
                        rx2 = col * 9 + off; ry2 = row * 8 + 1
                        if 0 <= rx2 < BLOCK_SIZE:
                            pygame.draw.rect(s, c, (rx2, ry2, 7, 6))
                            pygame.draw.line(s, lt, (rx2, ry2), (rx2+7, ry2), 1)
                            pygame.draw.line(s, lt, (rx2, ry2), (rx2, ry2+6), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ROMANESQUE_ARCH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 15)
                cx2 = BLOCK_SIZE // 2
                # Rounded arch with voussoir wedges
                pygame.draw.arc(s, dk, (4, 2, 24, 20), 0, math.pi, 3)
                # Voussoir joints radiating from arch center
                for i in range(6):
                    a = math.pi * i / 5
                    r1, r2 = 10, 16
                    x1 = cx2 + int(r1 * math.cos(a)); y1 = 12 - int(r1 * math.sin(a))
                    x2 = cx2 + int(r2 * math.cos(a)); y2 = 12 - int(r2 * math.sin(a))
                    pygame.draw.line(s, dk, (x1, y1), (x2, y2), 1)
                # Impost blocks at sides
                pygame.draw.rect(s, dk, (2, 12, 4, 18))
                pygame.draw.rect(s, dk, (26, 12, 4, 18))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == DARK_SLATE_ROOF:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 15)
                s.fill(_darken(c, 15))
                # Overlapping rectangular slate courses
                for row in range(5):
                    off = 5 if row % 2 else 0
                    y2 = row * 7
                    for col in range(-1, 4):
                        sx2 = col * 11 + off
                        pygame.draw.rect(s, c,  (sx2, y2, 9, 6))
                        pygame.draw.line(s, lt, (sx2, y2), (sx2+9, y2), 1)
                        pygame.draw.line(s, _darken(c, 20), (sx2, y2+6), (sx2+9, y2+6), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == KEYSTONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c  = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 15)
                s.fill(dk)
                # Trapezoidal wedge shape — wider at top
                pts = [(4, 0), (28, 0), (22, BLOCK_SIZE), (10, BLOCK_SIZE)]
                pygame.draw.polygon(s, c, pts)
                pygame.draw.polygon(s, lt, [(5, 1), (27, 1), (22, 3), (10, 3)])
                pygame.draw.polygon(s, dk, pts, 1)
                # Center incised line
                pygame.draw.line(s, dk, (16, 2), (16, BLOCK_SIZE-2), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PLINTH_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 25)
                lt = _lighter(c, 15)
                # Top step
                pygame.draw.rect(s, lt, (0, 0, BLOCK_SIZE, 5))
                pygame.draw.line(s, dk, (0, 5), (BLOCK_SIZE, 5), 1)
                # Recessed central panel
                pygame.draw.rect(s, _darken(c, 12), (3, 7, BLOCK_SIZE-6, 14))
                pygame.draw.line(s, dk, (3, 7), (3, 21), 1)
                pygame.draw.line(s, dk, (3, 7), (BLOCK_SIZE-3, 7), 1)
                # Bottom step
                pygame.draw.line(s, dk, (0, 22), (BLOCK_SIZE, 22), 1)
                pygame.draw.rect(s, lt, (0, 23, BLOCK_SIZE, 5))
                pygame.draw.rect(s, _darken(c, 28), (0, 28, BLOCK_SIZE, 4))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == IRON_LANTERN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c    = bdata["color"]
                glow = (220, 175, 60)
                s.fill(c)
                # Octagonal frame
                pts = [(10,1),(22,1),(29,8),(29,22),(22,29),(10,29),(3,22),(3,8)]
                pygame.draw.polygon(s, _lighter(c, 20), pts, 2)
                # Glow interior
                pygame.draw.polygon(s, _darken(glow, 15), pts)
                pygame.draw.polygon(s, glow, [(12,4),(20,4),(27,11),(27,21),(20,28),(12,28),(5,21),(5,11)])
                pygame.draw.circle(s, _lighter(glow, 30), (16, 15), 5)
                # Frame over glow
                pygame.draw.polygon(s, c, pts, 2)
                # Cross bars
                pygame.draw.line(s, c, (3, 15), (29, 15), 1)
                pygame.draw.line(s, c, (16, 1), (16, 29), 1)
                surfs[bid] = s
                continue
            if bid == SANDSTONE_ASHLAR:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                mortar = _darken(c, 28)
                s.fill(mortar)
                bw, bh = [18, 10], 9
                for row in range(3):
                    y2 = row * 10 + 1
                    x2 = 1 if row % 2 == 0 else 0
                    for w in (bw[row % 2], bw[(row+1) % 2], bw[row % 2]):
                        if x2 >= BLOCK_SIZE: break
                        aw = min(w, BLOCK_SIZE - x2 - 1)
                        pygame.draw.rect(s, c, (x2, y2, aw, bh))
                        pygame.draw.line(s, _lighter(c, 12), (x2, y2), (x2+aw, y2), 1)
                        x2 += w + 1
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == GARGOYLE_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c  = bdata["color"]
                lt = _lighter(c, 30)
                dk = _darken(c, 30)
                s.fill(c)
                # Stone texture
                pygame.draw.line(s, dk, (0, 10), (BLOCK_SIZE, 10), 1)
                pygame.draw.line(s, dk, (0, 21), (BLOCK_SIZE, 21), 1)
                # Grotesque face — head circle
                pygame.draw.circle(s, _darken(c, 15), (16, 12), 10, 1)
                # Brow ridge
                pygame.draw.arc(s, dk, (8, 5, 16, 8), 0, math.pi, 2)
                # Eye sockets
                pygame.draw.circle(s, dk, (12, 11), 2)
                pygame.draw.circle(s, dk, (20, 11), 2)
                # Nose
                pygame.draw.polygon(s, dk, [(16, 13), (14, 17), (18, 17)])
                # Open maw
                pygame.draw.arc(s, dk, (10, 16, 12, 7), math.pi, math.pi*2, 2)
                # Horns
                pygame.draw.line(s, dk, (8, 5),  (5, 1),  2)
                pygame.draw.line(s, dk, (24, 5), (27, 1), 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == OGEE_ARCH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 28)
                # S-curve ogee: concave bottom half, convex top, finial spike
                pygame.draw.arc(s, lt, (4, 14, 12, 16), 0, math.pi, 2)       # concave left
                pygame.draw.arc(s, lt, (16, 14, 12, 16), 0, math.pi, 2)      # concave right
                pygame.draw.arc(s, lt, (8, 4, 16, 16), math.pi, math.pi*2, 2) # convex top
                pygame.draw.line(s, lt, (16, 4), (16, 0), 2)                  # finial stem
                pygame.draw.circle(s, lt, (16, 1), 2)                         # finial ball
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == RUSTICATED_STONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 35)
                lt = _lighter(c, 8)
                # Two large blocks, deep V-cut joints
                pygame.draw.line(s, dk, (0, 15), (BLOCK_SIZE, 15), 3)
                pygame.draw.line(s, dk, (16, 0), (16, 15), 3)
                pygame.draw.line(s, dk, (16, 15), (16, BLOCK_SIZE), 3)
                # Rough stipple on each face
                for rx2, ry2 in [(3,3),(8,7),(5,11),(13,4),(11,10),(22,2),(20,8),(26,5),(19,12),(25,11),(4,20),(10,18),(7,26),(14,22),(21,19),(27,24)]:
                    pygame.draw.rect(s, _darken(c, 15), (rx2, ry2, 2, 1))
                pygame.draw.line(s, lt, (1, 1), (14, 1), 1)
                pygame.draw.line(s, lt, (17, 1), (BLOCK_SIZE-2, 1), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CHEVRON_STONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 32)
                lt = _lighter(c, 18)
                # Three rows of zigzag chevron bands
                for y2 in [2, 11, 20]:
                    for x2 in range(0, BLOCK_SIZE, 8):
                        pygame.draw.polygon(s, dk, [(x2,y2+4),(x2+4,y2),(x2+8,y2+4),(x2+4,y2+8)])
                        pygame.draw.line(s, lt, (x2, y2+4), (x2+4, y2), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == TRIGLYPH_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                # Three triglyphs (pairs of grooves)
                for tx2 in [3, 13, 23]:
                    pygame.draw.rect(s, dk, (tx2, 1, 2, 24))
                    pygame.draw.rect(s, dk, (tx2+4, 1, 2, 24))
                # Guttae (drops) below each triglyph
                for tx2 in [4, 9, 14, 19, 24, 29]:
                    pygame.draw.circle(s, dk, (tx2, 27), 2)
                pygame.draw.line(s, dk, (0, 25), (BLOCK_SIZE, 25), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MARBLE_INLAY:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                # White marble veins
                vein = _darken(c, 18)
                pygame.draw.line(s, vein, (3, 0), (18, BLOCK_SIZE), 1)
                pygame.draw.line(s, vein, (12, 0), (28, 20), 1)
                # Coloured inlay diamonds at intersections
                for ix2, iy2, ic in [(8, 8, (180, 80, 80)), (24, 8, (80, 130, 180)),
                                     (8, 24, (80, 160, 100)), (24, 24, (190, 155, 60))]:
                    pygame.draw.polygon(s, ic, [(ix2, iy2-5),(ix2+5,iy2),(ix2,iy2+5),(ix2-5,iy2)])
                pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BRICK_NOGGING:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                mortar = _darken(c, 40)
                s.fill(mortar)
                # Diagonal herringbone bricks within the panel
                bw, bh = 9, 4
                for row in range(7):
                    for col in range(7):
                        if (row + col) % 2 == 0:
                            x2 = col * 5 - row * 2
                            y2 = row * 5
                            pygame.draw.rect(s, c, (x2, y2, bw, bh))
                        else:
                            x2 = col * 5 - row * 2
                            y2 = row * 5
                            pygame.draw.rect(s, _darken(c, 15), (x2, y2, bh, bw))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CRENELLATION:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 15)
                # Merlons (raised) and crenels (open gaps) at top
                for mx2 in [0, 12, 24]:
                    pygame.draw.rect(s, c, (mx2, 0, 10, 14))
                    pygame.draw.line(s, lt, (mx2, 0), (mx2, 14), 1)
                    pygame.draw.line(s, lt, (mx2, 0), (mx2+10, 0), 1)
                # Crenel shadows
                for cx3 in [10, 22]:
                    pygame.draw.rect(s, dk, (cx3, 0, 4, 14))
                # Wall body
                pygame.draw.rect(s, _darken(c, 12), (0, 14, BLOCK_SIZE, BLOCK_SIZE-14))
                pygame.draw.line(s, dk, (0, 14), (BLOCK_SIZE, 14), 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == FAN_VAULT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                # Radiating ribs from two springing points
                for sp_x in [8, 24]:
                    sp_y = BLOCK_SIZE - 2
                    for i in range(7):
                        a = math.pi * (0.15 + i * 0.12)
                        ex = sp_x + int(22 * math.cos(a))
                        ey = sp_y - int(22 * math.sin(a))
                        pygame.draw.line(s, dk, (sp_x, sp_y), (ex, ey), 1)
                # Webbing arc lines
                for r in [8, 14, 20]:
                    for sp_x in [8, 24]:
                        pygame.draw.arc(s, _darken(c, 15), (sp_x-r, BLOCK_SIZE-2-r, r*2, r*2), math.pi*0.1, math.pi*0.9, 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ACANTHUS_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                # Central stem
                pygame.draw.line(s, dk, (16, BLOCK_SIZE-2), (16, 6), 2)
                # Curling leaf pairs at three heights
                for ly2, lw in [(22, 10), (14, 12), (6, 8)]:
                    pygame.draw.arc(s, dk, (6, ly2-lw//2, lw, lw), 0, math.pi, 2)
                    pygame.draw.arc(s, dk, (16, ly2-lw//2, lw, lw), math.pi, math.pi*2, 2)
                    pygame.draw.arc(s, lt, (7, ly2-lw//2+1, lw-2, lw-2), 0, math.pi, 1)
                pygame.draw.circle(s, dk, (16, 4), 3, 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PEBBLE_DASH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                for px2, py2, pr in [(3,3,2),(8,7,3),(13,2,2),(20,5,3),(26,3,2),(5,12,3),
                                     (11,15,2),(18,12,3),(25,14,2),(2,20,2),(8,24,3),(15,21,2),
                                     (22,22,3),(28,19,2),(4,28,3),(12,29,2),(20,27,3),(27,29,2)]:
                    pygame.draw.ellipse(s, dk, (px2-pr, py2-pr, pr*2+1, pr*2))
                    pygame.draw.ellipse(s, _lighter(c, 10), (px2-pr+1, py2-pr, pr, pr))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ENCAUSTIC_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                cream = (230, 215, 185)
                s.fill(c)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                # Four-petal inlaid design
                for a in [0, math.pi/2, math.pi, 3*math.pi/2]:
                    px2 = cx2 + int(7 * math.cos(a)); py2 = cy2 + int(7 * math.sin(a))
                    pygame.draw.ellipse(s, cream, (px2-4, py2-3, 8, 6))
                pygame.draw.circle(s, cream, (cx2, cy2), 4)
                # Corner triangles
                for ox2, oy2 in [(0,0),(BLOCK_SIZE,0),(0,BLOCK_SIZE),(BLOCK_SIZE,BLOCK_SIZE)]:
                    sx2 = min(ox2, BLOCK_SIZE-1); sy2 = min(oy2, BLOCK_SIZE-1)
                    pygame.draw.polygon(s, cream,
                        [(sx2, sy2), (sx2 + (6 if ox2==0 else -6), sy2), (sx2, sy2 + (6 if oy2==0 else -6))])
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CHEQUERBOARD_MARBLE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                black = (28, 25, 30)
                tsz = 8
                for ty in range(0, BLOCK_SIZE, tsz):
                    for tx in range(0, BLOCK_SIZE, tsz):
                        if (tx//tsz + ty//tsz) % 2 == 0:
                            pygame.draw.rect(s, c, (tx, ty, tsz, tsz))
                            pygame.draw.line(s, _darken(c, 15), (tx, ty), (tx+tsz, ty), 1)
                        else:
                            pygame.draw.rect(s, black, (tx, ty, tsz, tsz))
                            pygame.draw.line(s, _lighter(black, 10), (tx, ty), (tx+tsz, ty), 1)
                surfs[bid] = s
                continue
            if bid == WROUGHT_IRON_BALUSTRADE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 25)
                s.fill(_lighter(c, 18))
                # Top and bottom rails
                pygame.draw.rect(s, c, (0, 1, BLOCK_SIZE, 3))
                pygame.draw.rect(s, c, (0, BLOCK_SIZE-4, BLOCK_SIZE, 3))
                pygame.draw.line(s, lt, (0, 1), (BLOCK_SIZE, 1), 1)
                # Decorative balusters
                for bx2 in [4, 11, 18, 25]:
                    pygame.draw.line(s, c, (bx2+1, 4), (bx2+1, BLOCK_SIZE-5), 2)
                    pygame.draw.circle(s, lt, (bx2+1, 9), 2, 1)
                    pygame.draw.circle(s, lt, (bx2+1, BLOCK_SIZE//2), 2, 1)
                    pygame.draw.circle(s, lt, (bx2+1, BLOCK_SIZE-10), 2, 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == OPUS_INCERTUM:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 30))
                lt = _lighter(c, 12)
                # Irregular polygon stones
                stones = [
                    [(1,1),(10,1),(12,7),(8,11),(1,9)],
                    [(11,1),(20,1),(22,8),(14,10),(11,6)],
                    [(21,1),(31,1),(31,8),(23,10)],
                    [(1,10),(9,12),(10,18),(3,20),(1,16)],
                    [(10,10),(22,10),(20,18),(12,20),(8,16)],
                    [(22,10),(31,10),(31,20),(22,19)],
                    [(1,20),(11,20),(12,28),(5,31),(1,28)],
                    [(12,20),(24,19),(25,31),(13,31)],
                    [(23,20),(31,20),(31,31),(24,30)],
                ]
                for pts in stones:
                    pygame.draw.polygon(s, c, pts)
                    pygame.draw.polygon(s, lt, pts, 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == GROTESQUE_FRIEZE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                # Vine scrolls left and right
                pygame.draw.arc(s, dk, (1, 8, 10, 12), math.pi*0.5, math.pi*1.5, 2)
                pygame.draw.arc(s, dk, (21, 8, 10, 12), math.pi*1.5, math.pi*0.5, 2)
                # Small leaf tufts on scrolls
                for lx2, ly2 in [(3, 6), (3, 22), (28, 6), (28, 22)]:
                    pygame.draw.ellipse(s, dk, (lx2-2, ly2-2, 5, 4))
                # Central grotesque face
                pygame.draw.circle(s, _darken(c, 12), (16, 16), 7, 1)
                pygame.draw.circle(s, dk, (13, 14), 1)
                pygame.draw.circle(s, dk, (19, 14), 1)
                pygame.draw.arc(s, dk, (12, 16, 8, 5), math.pi, math.pi*2, 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BARREL_VAULT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 15)
                # Concentric semicircular vault ribs
                for r in [14, 11, 8, 5]:
                    pygame.draw.arc(s, dk, (BLOCK_SIZE//2-r, 2, r*2, r*2), 0, math.pi, 2)
                    pygame.draw.arc(s, lt, (BLOCK_SIZE//2-r+1, 3, r*2-2, r*2-2), 0, math.pi, 1)
                # Imposts
                pygame.draw.rect(s, dk, (1, 16, 5, BLOCK_SIZE-18))
                pygame.draw.rect(s, dk, (BLOCK_SIZE-6, 16, 5, BLOCK_SIZE-18))
                pygame.draw.line(s, lt, (2, 16), (2, BLOCK_SIZE-3), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == POINTED_ARCH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                void = _darken(c, 45)
                s.fill(c)
                dk = _darken(c, 22)
                # Pointed arch void
                pygame.draw.polygon(s, void, [(8, BLOCK_SIZE-1),(8, 14),(16, 3),(24, 14),(24, BLOCK_SIZE-1)])
                # Arch ring / reveal
                pygame.draw.lines(s, dk, False, [(8, BLOCK_SIZE-1),(8, 14),(16, 3),(24, 14),(24, BLOCK_SIZE-1)], 2)
                # Highlight on inner edge
                lt = _lighter(c, 18)
                pygame.draw.lines(s, lt, False, [(9, BLOCK_SIZE-1),(9, 14),(16, 4),(23, 14),(23, BLOCK_SIZE-1)], 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ENGLISH_BOND:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                mortar = _darken(c, 42)
                s.fill(mortar)
                bh, gap = 7, 2
                for row in range(4):
                    y2 = row * (bh + gap) + 1
                    if row % 2 == 0:
                        # Stretcher course — long bricks
                        for bx2 in range(-1, 3):
                            pygame.draw.rect(s, c, (bx2*17, y2, 15, bh))
                    else:
                        # Header course — short bricks, two-tone
                        hc = _darken(c, 18)
                        for bx2 in range(5):
                            col2 = c if bx2 % 2 == 0 else hc
                            pygame.draw.rect(s, col2, (bx2*7, y2, 5, bh))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == RELIEF_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                # Classical urn / vase in relief
                pygame.draw.polygon(s, _darken(c, 12), [(11,28),(21,28),(23,20),(20,16),(20,10),(12,10),(12,16),(9,20)])
                pygame.draw.lines(s, dk, False, [(11,28),(21,28),(23,20),(20,16),(20,10),(12,10),(12,16),(9,20),(11,28)], 1)
                # Neck and rim
                pygame.draw.line(s, dk, (12, 10), (20, 10), 1)
                pygame.draw.ellipse(s, lt, (11, 8, 10, 4))
                # Handle curls
                pygame.draw.arc(s, dk, (6, 14, 6, 8), math.pi*0.5, math.pi*1.5, 1)
                pygame.draw.arc(s, dk, (20, 14, 6, 8), math.pi*1.5, math.pi*0.5, 1)
                # Border
                pygame.draw.rect(s, dk, (2, 2, BLOCK_SIZE-4, BLOCK_SIZE-4), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == DIAGONAL_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                grout = _darken(c, 30)
                s.fill(grout)
                lt = _lighter(c, 12)
                # Diamond tiles at 45 degrees — draw filled rotated squares
                for ty in range(-1, 5):
                    for tx in range(-1, 5):
                        cx3 = tx * 10 + (5 if ty % 2 else 0)
                        cy3 = ty * 10 + 5
                        pts = [(cx3, cy3-6),(cx3+6,cy3),(cx3,cy3+6),(cx3-6,cy3)]
                        pygame.draw.polygon(s, c, pts)
                        pygame.draw.polygon(s, lt, [(cx3, cy3-5),(cx3+5,cy3),(cx3,cy3-1)], 0)
                pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == TAPESTRY_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                bands = [(175,88,52),(230,200,160),(140,40,40),(215,175,90),(175,88,52),(80,45,28)]
                bh2 = BLOCK_SIZE // len(bands)
                for i, bc in enumerate(bands):
                    pygame.draw.rect(s, bc, (0, i*bh2, BLOCK_SIZE, bh2))
                    for wx in range(0, BLOCK_SIZE, 3):
                        pygame.draw.line(s, _darken(bc, 18), (wx, i*bh2), (wx, i*bh2+bh2), 1)
                pygame.draw.rect(s, _darken(bands[0], 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == WOVEN_RUG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                gold = (185, 148, 55)
                cream = (230, 210, 175)
                s.fill(c)
                pygame.draw.rect(s, gold, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 3)
                pygame.draw.rect(s, cream, (3, 3, BLOCK_SIZE-6, BLOCK_SIZE-6), 1)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                pygame.draw.polygon(s, gold, [(cx2,cy2-9),(cx2+9,cy2),(cx2,cy2+9),(cx2-9,cy2)])
                pygame.draw.polygon(s, cream, [(cx2,cy2-5),(cx2+5,cy2),(cx2,cy2+5),(cx2-5,cy2)])
                for ox2, oy2 in [(5,5),(BLOCK_SIZE-5,5),(5,BLOCK_SIZE-5),(BLOCK_SIZE-5,BLOCK_SIZE-5)]:
                    pygame.draw.polygon(s, gold, [(ox2,oy2-3),(ox2+3,oy2),(ox2,oy2+3),(ox2-3,oy2)])
                surfs[bid] = s
                continue
            if bid == CELTIC_KNOTWORK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 35)
                pygame.draw.ellipse(s, lt, (4,  4, 14, 14), 2)
                pygame.draw.ellipse(s, lt, (14, 4, 14, 14), 2)
                pygame.draw.ellipse(s, lt, (4, 14, 14, 14), 2)
                pygame.draw.ellipse(s, lt, (14,14, 14, 14), 2)
                for px2, py2 in [(11,8),(11,18),(21,8),(21,18)]:
                    pygame.draw.rect(s, c, (px2-1, py2-2, 3, 4))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BYZANTINE_MOSAIC:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dark = _darken(c, 30)
                tsz = 4
                for ty in range(0, BLOCK_SIZE, tsz):
                    for tx in range(0, BLOCK_SIZE, tsz):
                        d = ((tx - 16)**2 + (ty - 12)**2) ** 0.5
                        tc = dark if d < 10 else _lighter(c, 8)
                        pygame.draw.rect(s, tc, (tx+1, ty+1, tsz-1, tsz-1))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == JAPANESE_SHOJI:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                wood = (120, 88, 48)
                s.fill(c)
                pygame.draw.rect(s, wood, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
                for x2 in [10, 21]:
                    pygame.draw.line(s, wood, (x2, 2), (x2, BLOCK_SIZE-3), 1)
                for y2 in [10, 21]:
                    pygame.draw.line(s, wood, (2, y2), (BLOCK_SIZE-3, y2), 1)
                surfs[bid] = s
                continue
            if bid == OTTOMAN_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                blue = (40, 80, 175)
                teal = (35, 140, 130)
                s.fill(c)
                pygame.draw.line(s, teal, (16, 28), (16, 16), 2)
                pygame.draw.line(s, teal, (16, 22), (10, 18), 1)
                pygame.draw.line(s, teal, (16, 22), (22, 18), 1)
                pygame.draw.ellipse(s, blue, (11, 7, 10, 10))
                pygame.draw.ellipse(s, teal, (13, 5, 6, 5))
                for fx2 in [5, 27]:
                    pygame.draw.circle(s, blue, (fx2, 20), 3)
                    pygame.draw.line(s, teal, (fx2, 23), (fx2, 28), 1)
                pygame.draw.rect(s, blue, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
                surfs[bid] = s
                continue
            if bid == LEADLIGHT_WINDOW:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                pane_colors = [(120,160,210),(180,210,140),(210,160,90),(160,120,200)]
                s.fill(c)
                tsz = 8
                for ty in range(0, BLOCK_SIZE, tsz):
                    off = tsz//2 if (ty//tsz) % 2 else 0
                    for tx in range(-tsz//2, BLOCK_SIZE, tsz):
                        pc = pane_colors[((tx//tsz + ty//tsz) % len(pane_colors))]
                        pts = [(tx+off, ty+tsz//2),(tx+off+tsz//2, ty),(tx+off+tsz, ty+tsz//2),(tx+off+tsz//2, ty+tsz)]
                        pygame.draw.polygon(s, pc, pts)
                        pygame.draw.polygon(s, c, pts, 1)
                surfs[bid] = s
                continue
            if bid == TUDOR_ROSE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                s.fill(c)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                for i in range(5):
                    a = math.pi * 2 * i / 5 - math.pi/2
                    pygame.draw.circle(s, dk, (cx2+int(10*math.cos(a)), cy2+int(10*math.sin(a))), 4)
                for i in range(5):
                    a = math.pi * 2 * i / 5
                    pygame.draw.circle(s, lt, (cx2+int(6*math.cos(a)), cy2+int(6*math.sin(a))), 3)
                pygame.draw.circle(s, (175, 45, 45), (cx2, cy2), 3)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == GREEK_KEY:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 35)
                meander = [(0,2),(6,2),(6,0),(12,0),(12,6),(2,6),(2,4),(10,4),(10,2),(8,2),(8,8),(0,8)]
                for rep_x, rep_y in [(1,1),(1,17),(17,1),(17,17)]:
                    pts = [(x+rep_x, y+rep_y) for x, y in meander]
                    pygame.draw.lines(s, dk, False, pts, 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == VENETIAN_PLASTER:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 12)
                dk = _darken(c, 8)
                for i in range(0, BLOCK_SIZE*2, 6):
                    shade = lt if (i // 6) % 2 == 0 else dk
                    pygame.draw.line(s, shade, (i - BLOCK_SIZE, 0), (i, BLOCK_SIZE), 1)
                pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == SCOTTISH_RUBBLE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 30))
                lt = _lighter(c, 10)
                for rx2, ry2, rw2, rh2 in [(1,1,12,8),(14,1,8,5),(23,1,8,8),(1,10,6,10),
                                            (8,7,14,6),(23,10,8,6),(1,21,9,9),(11,14,10,8),
                                            (22,17,9,5),(11,23,10,7),(22,23,9,7)]:
                    pygame.draw.rect(s, c, (rx2, ry2, rw2, rh2))
                    pygame.draw.line(s, lt, (rx2, ry2), (rx2+rw2, ry2), 1)
                    pygame.draw.line(s, lt, (rx2, ry2), (rx2, ry2+rh2), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ART_NOUVEAU_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 20)
                pygame.draw.arc(s, dk, (6, 14, 12, 16), math.pi*1.5, math.pi*2.5, 2)
                pygame.draw.arc(s, dk, (14, 2, 12, 16), math.pi*0.5, math.pi*1.5, 2)
                pygame.draw.ellipse(s, dk, (2, 4, 8, 12), 1)
                pygame.draw.ellipse(s, lt, (3, 5, 6, 10), 1)
                pygame.draw.ellipse(s, dk, (22, 16, 8, 12), 1)
                pygame.draw.ellipse(s, lt, (23, 17, 6, 10), 1)
                pygame.draw.circle(s, dk, (20, 8), 4, 1)
                pygame.draw.circle(s, lt, (20, 8), 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == DUTCH_GABLE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 40))
                lt = _lighter(c, 10)
                for row in range(4):
                    y2 = row * 7 + 17; off = 4 if row % 2 else 0
                    for bx2 in range(-1, 4):
                        rx2 = bx2 * 10 + off
                        if 0 <= rx2 < BLOCK_SIZE:
                            pygame.draw.rect(s, c, (rx2, y2, 8, 5))
                for gx2, gy2, gr in [(8,14,6),(16,8,5),(24,14,6)]:
                    pygame.draw.circle(s, c, (gx2, gy2), gr)
                    pygame.draw.circle(s, lt, (gx2, gy2-gr+1), 2)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == STRIPED_ARCH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                cx2 = BLOCK_SIZE // 2
                for i in range(9):
                    a1 = math.pi * i / 8; a2 = math.pi * (i+1) / 8
                    r1, r2 = 10, 15
                    shade = _darken(c, 35) if i % 2 == 0 else _lighter(c, 15)
                    pts = [
                        (cx2 + int(r1*math.cos(a1)), BLOCK_SIZE - int(r1*math.sin(a1))),
                        (cx2 + int(r2*math.cos(a1)), BLOCK_SIZE - int(r2*math.sin(a1))),
                        (cx2 + int(r2*math.cos(a2)), BLOCK_SIZE - int(r2*math.sin(a2))),
                        (cx2 + int(r1*math.cos(a2)), BLOCK_SIZE - int(r1*math.sin(a2))),
                    ]
                    pygame.draw.polygon(s, shade, pts)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == TIMBER_TRUSS:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 18)
                s.fill(_darken(c, 25))
                pygame.draw.rect(s, c, (0, 24, BLOCK_SIZE, 5))
                pygame.draw.line(s, lt, (0, 24), (BLOCK_SIZE, 24), 1)
                pygame.draw.line(s, c, (0, 24), (16, 2), 4)
                pygame.draw.line(s, c, (BLOCK_SIZE, 24), (16, 2), 4)
                pygame.draw.line(s, lt, (1, 24), (16, 3), 1)
                pygame.draw.line(s, lt, (BLOCK_SIZE-1, 24), (16, 3), 1)
                pygame.draw.line(s, c, (16, 24), (16, 8), 3)
                pygame.draw.circle(s, lt, (16, 2), 2)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == HEARTH_STONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 15)
                s.fill(c)
                pygame.draw.rect(s, lt, (0, 5, BLOCK_SIZE, 4))
                pygame.draw.line(s, dk, (0, 9), (BLOCK_SIZE, 9), 1)
                opening = _darken(c, 50)
                pygame.draw.rect(s, opening, (6, 10, 20, 20))
                pygame.draw.arc(s, opening, (6, 6, 20, 10), 0, math.pi)
                pygame.draw.arc(s, dk, (5, 5, 22, 12), 0, math.pi, 2)
                pygame.draw.line(s, dk, (5, 11), (5, 30), 2)
                pygame.draw.line(s, dk, (27, 11), (27, 30), 2)
                pygame.draw.ellipse(s, (200, 110, 30), (9, 22, 14, 6))
                pygame.draw.ellipse(s, (230, 160, 40), (11, 23, 10, 4))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == LINEN_FOLD:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 22)
                dk = _darken(c, 25)
                s.fill(c)
                for fx in [4, 10, 16, 22, 28]:
                    pygame.draw.line(s, dk, (fx, 1), (fx, BLOCK_SIZE-2), 1)
                for fx in [7, 13, 19, 25]:
                    pygame.draw.line(s, lt, (fx, 1), (fx, BLOCK_SIZE-2), 1)
                pygame.draw.arc(s, dk, (1, 0, 12, 8), math.pi, math.pi*2, 2)
                pygame.draw.arc(s, dk, (13, 0, 12, 8), math.pi, math.pi*2, 2)
                pygame.draw.arc(s, lt, (1, BLOCK_SIZE-8, 12, 8), 0, math.pi, 2)
                pygame.draw.arc(s, lt, (13, BLOCK_SIZE-8, 12, 8), 0, math.pi, 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PARQUET_FLOOR:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 22)
                lt = _lighter(c, 14)
                s.fill(_darken(c, 30))
                for row in range(12):
                    for col in range(8):
                        x2 = col * 4; y2 = row * 3 - col
                        if (row + col) % 2 == 0:
                            pygame.draw.rect(s, c, (x2, y2, 6, 3))
                            pygame.draw.line(s, lt, (x2, y2), (x2+6, y2), 1)
                        else:
                            pygame.draw.rect(s, dk, (x2, y2, 3, 6))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == COFFERED_CEILING:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 30)
                lt = _lighter(c, 18)
                s.fill(c)
                half = BLOCK_SIZE // 2
                for cx3, cy3 in [(0,0),(half,0),(0,half),(half,half)]:
                    pygame.draw.rect(s, dk, (cx3+1, cy3+1, half-2, half-2), 2)
                    pygame.draw.rect(s, lt, (cx3+4, cy3+4, half-8, half-8))
                    pygame.draw.rect(s, dk, (cx3+4, cy3+4, half-8, half-8), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == OPUS_SIGNINUM:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                for tx2, ty2, ts in [(3,4,2),(7,8,3),(12,3,2),(18,6,3),(24,2,2),(28,7,3),
                                     (2,14,3),(8,18,2),(14,13,3),(20,16,2),(26,13,3),
                                     (5,23,2),(10,27,3),(16,22,2),(22,25,3),(29,20,2),
                                     (1,29,3),(13,30,2),(20,29,3),(28,28,2)]:
                    pygame.draw.rect(s, (230, 225, 215), (tx2, ty2, ts, ts))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            # ---- Himalayan architecture blocks ----
            if bid == WHITEWASHED_WALL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 12)
                for hy in [7, 15, 23]:
                    pygame.draw.line(s, dk, (1, hy), (BLOCK_SIZE - 2, hy), 1)
                pygame.draw.rect(s, (80, 18, 15), (0, 0, BLOCK_SIZE, 4))
                pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MONASTERY_ROOF:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                lt = _lighter(c, 20)
                dk = _darken(c, 25)
                for row in range(4):
                    ry = row * 8
                    shade = lt if row % 2 == 0 else dk
                    pygame.draw.rect(s, shade, (0, ry, BLOCK_SIZE, 5))
                    pygame.draw.line(s, dk, (0, ry + 5), (BLOCK_SIZE, ry + 5), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MANI_STONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 20))
                lt = _lighter(c, 12)
                dk = _darken(c, 30)
                for rx2, ry2, rw2, rh2 in [(1,1,18,9),(20,1,10,7),(1,11,8,9),(10,11,20,8),
                                            (1,21,14,7),(16,20,14,9)]:
                    pygame.draw.rect(s, c, (rx2, ry2, rw2, rh2))
                    pygame.draw.line(s, lt, (rx2, ry2), (rx2 + rw2, ry2), 1)
                pygame.draw.ellipse(s, dk, (11, 12, 8, 6), 1)
                pygame.draw.rect(s, _darken(c, 22), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PRAYER_FLAG_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                pygame.draw.line(s, (80, 60, 40), (0, 8), (BLOCK_SIZE, 8), 1)
                for i, fc in enumerate([(60, 100, 175), (230, 225, 210), (180, 35, 30),
                                        (45, 135, 60), (200, 175, 30)]):
                    fx2 = i * 6 + 1
                    pygame.draw.rect(s, fc, (fx2, 9, 5, 8))
                    pygame.draw.rect(s, _darken(fc, 20), (fx2, 9, 5, 8), 1)
                surfs[bid] = s
                continue
            # ---- Chinese architecture blocks ----
            if bid == GLAZED_ROOF_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_darken(c, 25))
                lt = _lighter(c, 20)
                # Curved barrel tiles in green glaze
                for tx in [0, 11, 22]:
                    pygame.draw.ellipse(s, c, (tx, 0, 10, BLOCK_SIZE))
                    pygame.draw.line(s, lt, (tx+2, 3), (tx+2, BLOCK_SIZE-4), 1)
                    pygame.draw.line(s, _darken(c, 30), (tx+9, 3), (tx+9, BLOCK_SIZE-4), 1)
                # Upturned eave hint at bottom
                pygame.draw.arc(s, _lighter(c, 30), (0, BLOCK_SIZE-8, BLOCK_SIZE, 10), 0, math.pi, 2)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == LATTICE_SCREEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(_lighter(c, 30))
                dk = _darken(c, 15)
                # Geometric square-within-diamond lattice
                for y2 in range(0, BLOCK_SIZE, 8):
                    for x2 in range(0, BLOCK_SIZE, 8):
                        cx3, cy3 = x2+4, y2+4
                        pygame.draw.polygon(s, c, [(cx3,cy3-4),(cx3+4,cy3),(cx3,cy3+4),(cx3-4,cy3)], 1)
                        pygame.draw.rect(s, dk, (cx3-2, cy3-2, 4, 4), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MOON_GATE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                void = _darken(c, 48)
                s.fill(c)
                dk = _darken(c, 25)
                lt = _lighter(c, 15)
                # Large circular opening
                pygame.draw.circle(s, void, (16, 16), 11)
                pygame.draw.circle(s, dk, (16, 16), 11, 2)
                pygame.draw.circle(s, lt, (16, 16), 13, 1)
                # Wall texture
                pygame.draw.line(s, dk, (0, 10), (4, 10), 1)
                pygame.draw.line(s, dk, (28, 10), (BLOCK_SIZE, 10), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PAINTED_BEAM:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                gold = (215, 178, 45)
                lt = _lighter(c, 18)
                s.fill(c)
                # Beam ends with decorative gold painted borders
                pygame.draw.rect(s, _darken(c, 20), (0, 0, 6, BLOCK_SIZE))
                pygame.draw.rect(s, _darken(c, 20), (BLOCK_SIZE-6, 0, 6, BLOCK_SIZE))
                pygame.draw.line(s, gold, (6, 2), (BLOCK_SIZE-6, 2), 1)
                pygame.draw.line(s, gold, (6, BLOCK_SIZE-3), (BLOCK_SIZE-6, BLOCK_SIZE-3), 1)
                # Central painted panel with gold cloud motif
                for cx3, cy3 in [(16, 10), (16, 22)]:
                    pygame.draw.arc(s, gold, (cx3-5, cy3-3, 10, 6), 0, math.pi, 1)
                    pygame.draw.circle(s, gold, (cx3, cy3-3), 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == DOUGONG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                s.fill(_darken(c, 20))
                # Stacked bracket layers (wide bottom, narrowing up)
                for i, (w, y2, h) in enumerate([(30,24,6),(24,17,6),(18,11,5),(12,6,4),(24,2,3)]):
                    x2 = (BLOCK_SIZE - w) // 2
                    shade = c if i % 2 == 0 else _darken(c, 12)
                    pygame.draw.rect(s, shade, (x2, y2, w, h))
                    pygame.draw.line(s, lt, (x2, y2), (x2+w, y2), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CERAMIC_PLANTER:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                white = (235, 235, 230)
                dk = _darken(c, 30)
                s.fill(c)
                # Rounded planter body
                pygame.draw.ellipse(s, white, (4, 6, 24, 22))
                pygame.draw.ellipse(s, c, (4, 6, 24, 22), 2)
                # Rim at top
                pygame.draw.ellipse(s, white, (3, 4, 26, 6))
                pygame.draw.ellipse(s, dk, (3, 4, 26, 6), 1)
                # Blue decorative band
                pygame.draw.arc(s, dk, (6, 10, 20, 10), 0, math.pi, 1)
                pygame.draw.arc(s, dk, (8, 13, 16, 8), 0, math.pi, 1)
                # Base
                pygame.draw.ellipse(s, _darken(c, 15), (6, 26, 20, 4))
                surfs[bid] = s
                continue
            if bid == STONE_LANTERN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 15)
                glow = (215, 175, 55)
                s.fill(_darken(c, 25))
                # Base
                pygame.draw.rect(s, c, (8, 28, 16, 3))
                # Shaft
                pygame.draw.rect(s, c, (13, 20, 6, 8))
                # Lantern body with glow
                pygame.draw.rect(s, c, (6, 12, 20, 10))
                pygame.draw.rect(s, glow, (8, 13, 16, 8))
                pygame.draw.line(s, dk, (16, 12), (16, 22), 1)
                pygame.draw.line(s, dk, (6, 17), (26, 17), 1)
                # Pagoda cap
                pygame.draw.polygon(s, c, [(16,3),(26,12),(6,12)])
                pygame.draw.line(s, lt, (16,3),(26,12), 1)
                pygame.draw.line(s, lt, (16,3),(6,12), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == LACQUER_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                gold = (210, 175, 45)
                lt = _lighter(c, 12)
                s.fill(c)
                # Gold border
                pygame.draw.rect(s, gold, (2, 2, BLOCK_SIZE-4, BLOCK_SIZE-4), 2)
                # Inner panel
                pygame.draw.rect(s, _darken(c, 10), (5, 5, BLOCK_SIZE-10, BLOCK_SIZE-10))
                # Central gold roundel
                pygame.draw.circle(s, gold, (16, 16), 6, 1)
                pygame.draw.circle(s, gold, (16, 16), 3)
                # Corner dots
                for ox2, oy2 in [(7,7),(25,7),(7,25),(25,25)]:
                    pygame.draw.circle(s, gold, (ox2, oy2), 2)
                surfs[bid] = s
                continue
            if bid == PAPER_LANTERN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 25)
                dk = _darken(c, 25)
                s.fill(_darken(c, 35))
                # Oval lantern body
                pygame.draw.ellipse(s, c, (7, 3, 18, 22))
                # Rib lines
                for ry2 in [7, 11, 15, 19]:
                    pygame.draw.line(s, dk, (7, ry2), (25, ry2), 1)
                    pygame.draw.line(s, lt, (8, ry2-1), (24, ry2-1), 1)
                # Top and bottom caps
                pygame.draw.line(s, dk, (12, 3), (20, 3), 2)
                pygame.draw.line(s, dk, (12, 25), (20, 25), 2)
                # Tassel
                for tx2 in [13, 16, 19]:
                    pygame.draw.line(s, dk, (tx2, 25), (tx2, 30), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == DRAGON_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 32)
                lt = _lighter(c, 22)
                s.fill(c)
                # Dragon scale pattern — overlapping arcs
                for row in range(5):
                    off = 4 if row % 2 else 0
                    y2 = row * 7
                    for col in range(-1, 5):
                        cx3 = col * 8 + off
                        pygame.draw.arc(s, dk, (cx3, y2, 8, 8), 0, math.pi, 2)
                        pygame.draw.arc(s, lt, (cx3+1, y2+1, 6, 6), 0, math.pi, 1)
                pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == HAN_BRICK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                mortar = _darken(c, 32)
                s.fill(mortar)
                # Narrow elongated bricks (Han style)
                bw, bh, gap = 14, 5, 2
                for row in range(4):
                    off = (bw // 2 + 1) if row % 2 else 0
                    y2 = row * (bh + gap) + 2
                    for col in range(-1, 3):
                        x2 = col * (bw + gap) + off
                        cx2 = max(0, x2); cw2 = min(x2+bw, BLOCK_SIZE) - cx2
                        if cw2 > 0:
                            pygame.draw.rect(s, c, (cx2, y2, cw2, bh))
                            pygame.draw.line(s, _lighter(c, 8), (cx2, y2), (cx2+cw2, y2), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PAVILION_FLOOR:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 20)
                lt = _lighter(c, 12)
                s.fill(c)
                # Large smooth stone squares with fine joint
                half = BLOCK_SIZE // 2
                pygame.draw.line(s, dk, (half, 0), (half, BLOCK_SIZE), 1)
                pygame.draw.line(s, dk, (0, half), (BLOCK_SIZE, half), 1)
                for qx, qy in [(1,1),(half+1,1),(1,half+1),(half+1,half+1)]:
                    pygame.draw.line(s, lt, (qx, qy), (qx+half-3, qy), 1)
                    pygame.draw.line(s, lt, (qx, qy), (qx, qy+half-3), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BAMBOO_SCREEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 30)
                lt = _lighter(c, 18)
                s.fill(_darken(c, 20))
                # Vertical bamboo stalks with node rings
                for bx2, bw2 in [(1,5),(7,5),(13,5),(19,5),(25,5)]:
                    shade = c if (bx2//6) % 2 == 0 else _darken(c, 10)
                    pygame.draw.rect(s, shade, (bx2, 0, bw2, BLOCK_SIZE))
                    pygame.draw.line(s, lt, (bx2+1, 0), (bx2+1, BLOCK_SIZE), 1)
                    for ny in range(6, BLOCK_SIZE, 8):
                        pygame.draw.line(s, dk, (bx2, ny), (bx2+bw2, ny), 2)
                        pygame.draw.line(s, lt, (bx2, ny+1), (bx2+bw2, ny+1), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CLOUD_MOTIF:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 20)
                # Ruyi cloud — interlocking S/circle motif
                for cx3, cy3 in [(9, 10), (23, 10), (9, 22), (23, 22)]:
                    pygame.draw.circle(s, dk, (cx3, cy3), 5, 2)
                    pygame.draw.circle(s, lt, (cx3, cy3), 3, 1)
                # Connecting arcs
                pygame.draw.arc(s, dk, (9, 7, 14, 10), math.pi, math.pi*2, 2)
                pygame.draw.arc(s, dk, (9, 15, 14, 10), 0, math.pi, 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == COIN_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 20)
                dk = _darken(c, 22)
                s.fill(c)
                # Four cash coins with square holes
                for cx3, cy3 in [(8,8),(24,8),(8,24),(24,24)]:
                    pygame.draw.circle(s, lt, (cx3, cy3), 6, 2)
                    pygame.draw.rect(s, dk, (cx3-2, cy3-2, 4, 4))
                    pygame.draw.rect(s, lt, (cx3-1, cy3-1, 2, 2), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BLUE_WHITE_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                blue = (50, 85, 170)
                s.fill(c)
                # Willow-pattern scene — simplified pagoda silhouette
                pygame.draw.rect(s, blue, (12, 20, 8, 10))      # building
                pygame.draw.polygon(s, blue, [(10,20),(20,14),(30,20)])  # roof
                pygame.draw.polygon(s, blue, [(12,14),(20,10),(28,14)])  # upper roof
                pygame.draw.line(s, blue, (20, 10), (20, 6), 1)         # spire
                # Water ripples at base
                for wy2 in [28, 30]:
                    pygame.draw.arc(s, blue, (2, wy2, 8, 4), 0, math.pi, 1)
                    pygame.draw.arc(s, blue, (12, wy2, 8, 4), 0, math.pi, 1)
                    pygame.draw.arc(s, blue, (22, wy2, 8, 4), 0, math.pi, 1)
                # Border
                pygame.draw.rect(s, blue, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
                surfs[bid] = s
                continue
            if bid == GARDEN_ROCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 22)
                dk = _darken(c, 28)
                s.fill(_darken(c, 35))
                # Taihu rock — irregular eroded silhouette with holes
                pygame.draw.polygon(s, c, [(6,28),(4,20),(7,14),(5,8),(10,4),(16,2),(22,5),(26,10),(28,18),(24,26),(16,30)])
                pygame.draw.polygon(s, dk, [(6,28),(4,20),(7,14),(5,8),(10,4),(16,2),(22,5),(26,10),(28,18),(24,26),(16,30)], 1)
                # Void holes
                pygame.draw.ellipse(s, _darken(c, 45), (10, 8, 7, 5))
                pygame.draw.ellipse(s, _darken(c, 45), (18, 15, 6, 6))
                # Highlight edges
                pygame.draw.line(s, lt, (10, 4), (22, 5), 1)
                pygame.draw.line(s, lt, (5, 8), (7, 14), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == STEPPED_WALL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 10)
                s.fill(c)
                # Regular horizontal brick courses, slightly tapered feel
                for row in range(5):
                    y2 = row * 7
                    pygame.draw.line(s, dk, (0, y2), (BLOCK_SIZE, y2), 1)
                    pygame.draw.line(s, lt, (0, y2+1), (BLOCK_SIZE, y2+1), 1)
                # Vertical joints offset per row
                for row in range(5):
                    off = 8 if row % 2 else 0
                    y2 = row * 7
                    for vx in range(off, BLOCK_SIZE, 16):
                        pygame.draw.line(s, dk, (vx, y2+1), (vx, y2+6), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PAGODA_EAVE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                green = (65, 130, 65)
                gold  = (210, 175, 45)
                s.fill(_darken(c, 25))
                # Main eave — upturned curved roof shape
                pts = [(0, 20),(BLOCK_SIZE, 20),(BLOCK_SIZE-2, 14),(BLOCK_SIZE, 8),(24, 4),(16, 2),(8, 4),(2, 8),(0, 14)]
                pygame.draw.polygon(s, c, pts)
                pygame.draw.polygon(s, _lighter(c, 15), pts, 1)
                # Green glazed tile hints on top face
                for tx2 in range(2, BLOCK_SIZE-2, 5):
                    pygame.draw.rect(s, green, (tx2, 14, 3, 4))
                # Gold ridge line
                pygame.draw.line(s, gold, (4, 8), (BLOCK_SIZE-4, 8), 1)
                # Upturned corner tips
                pygame.draw.line(s, gold, (0, 14), (0, 8), 2)
                pygame.draw.line(s, gold, (BLOCK_SIZE, 14), (BLOCK_SIZE, 8), 2)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == CINNABAR_WALL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                gold = (210, 175, 45)
                lt = _lighter(c, 12)
                s.fill(c)
                # Subtle plaster texture lines
                pygame.draw.line(s, _darken(c, 8), (0, 10), (BLOCK_SIZE, 10), 1)
                pygame.draw.line(s, _darken(c, 8), (0, 21), (BLOCK_SIZE, 21), 1)
                # Gold nail-head studs (like Forbidden City gates)
                for nx2, ny2 in [(5,5),(12,5),(19,5),(26,5),
                                  (5,16),(12,16),(19,16),(26,16),
                                  (5,27),(12,27),(19,27),(26,27)]:
                    pygame.draw.circle(s, gold, (nx2, ny2), 2)
                    pygame.draw.circle(s, _lighter(gold, 20), (nx2-1, ny2-1), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            # ---- World architecture batch 4 ----
            if bid == MUGHAL_ARCH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                void = _darken(c, 45)
                # Cusped multi-foil arch — three lobes
                pygame.draw.rect(s, void, (7, 14, 18, 16))
                pygame.draw.arc(s, void, (7, 8, 18, 12), 0, math.pi)
                for lx2 in [7, 14, 21]:
                    pygame.draw.arc(s, c, (lx2, 8, 9, 10), 0, math.pi)
                pygame.draw.arc(s, dk, (6, 7, 20, 14), 0, math.pi, 2)
                pygame.draw.line(s, dk, (6, 14), (6, 30), 2)
                pygame.draw.line(s, dk, (26, 14), (26, 30), 2)
                pygame.draw.line(s, lt, (7, 7), (25, 7), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PIETRA_DURA:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                # Inlaid stone floral: central flower, 4 petals, corner leaves
                petal_cols = [(180, 80, 80),(80, 150, 100),(80, 110, 180),(175, 140, 60)]
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                for i, pc in enumerate(petal_cols):
                    a = math.pi * i / 2
                    px2 = cx2 + int(7 * math.cos(a)); py2 = cy2 + int(7 * math.sin(a))
                    pygame.draw.ellipse(s, pc, (px2-4, py2-3, 8, 6))
                pygame.draw.circle(s, (210, 175, 45), (cx2, cy2), 4)
                for ox2, oy2, lc in [(4,4,(75,130,75)),(28,4,(75,130,75)),(4,28,(75,130,75)),(28,28,(75,130,75))]:
                    pygame.draw.ellipse(s, lc, (ox2-3, oy2-2, 6, 4))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == EGYPTIAN_FRIEZE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 35)
                blue = (65, 100, 160)
                red  = (170, 55, 45)
                # Lotus band at top
                for lx2 in [3, 11, 19, 27]:
                    pygame.draw.line(s, dk, (lx2+2, 10), (lx2+2, 3), 1)
                    pygame.draw.ellipse(s, blue, (lx2, 1, 5, 4))
                pygame.draw.line(s, dk, (0, 11), (BLOCK_SIZE, 11), 1)
                # Hieroglyphic symbols in middle band
                for sx2, sy2, shape in [(4,14,0),(12,14,1),(20,14,2),(28,14,3)]:
                    if shape == 0: pygame.draw.circle(s, dk, (sx2, sy2+3), 3, 1)
                    elif shape == 1: pygame.draw.polygon(s, dk, [(sx2,sy2),(sx2+5,sy2+6),(sx2-1,sy2+6)], 1)
                    elif shape == 2: pygame.draw.rect(s, dk, (sx2-2, sy2, 5, 5), 1)
                    else: pygame.draw.line(s, dk, (sx2-2,sy2+6),(sx2+2,sy2),(sx2+3,sy2+6), 1) if False else pygame.draw.lines(s, dk, False, [(sx2-2,sy2+6),(sx2,sy2),(sx2+2,sy2+6)], 1)
                pygame.draw.line(s, dk, (0, 22), (BLOCK_SIZE, 22), 1)
                # Papyrus band at base
                for px2 in [3, 11, 19, 27]:
                    pygame.draw.line(s, dk, (px2+2, 22), (px2+2, 28), 1)
                    pygame.draw.ellipse(s, red, (px2, 27, 5, 4))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == SANDSTONE_COLUMN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 25)
                lt = _lighter(c, 18)
                s.fill(c)
                # Papyrus-bundle shaft — clustered round stems
                for fx in [9, 13, 17, 21]:
                    pygame.draw.line(s, dk, (fx, 8), (fx, 28), 1)
                    pygame.draw.line(s, lt, (fx+1, 8), (fx+1, 28), 1)
                # Spreading fan capital at top
                for i in range(7):
                    a = math.pi * (0.15 + i * 0.12)
                    pygame.draw.line(s, dk, (16, 7), (16 + int(13*math.cos(a)), 7 - int(6*math.sin(a))), 1)
                pygame.draw.line(s, lt, (2, 2), (BLOCK_SIZE-2, 2), 2)
                # Base
                pygame.draw.rect(s, dk, (5, 27, 22, 4))
                pygame.draw.line(s, lt, (5, 27), (27, 27), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == AZTEC_SUNSTONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 28)
                dk = _darken(c, 22)
                s.fill(_darken(c, 18))
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                # Concentric rings
                for r in [14, 11, 8]:
                    pygame.draw.circle(s, lt, (cx2, cy2), r, 1)
                # Sun-ray divisions
                for i in range(20):
                    a = math.pi * 2 * i / 20
                    x1 = cx2 + int(9 * math.cos(a)); y1 = cy2 + int(9 * math.sin(a))
                    x2 = cx2 + int(13 * math.cos(a)); y2 = cy2 + int(13 * math.sin(a))
                    pygame.draw.line(s, lt, (x1, y1), (x2, y2), 1)
                # Central face dot
                pygame.draw.circle(s, lt, (cx2, cy2), 3)
                pygame.draw.circle(s, dk, (cx2, cy2), 2)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MAYA_RELIEF:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 32)
                lt = _lighter(c, 18)
                # Stepped T-shape and hook pattern
                pygame.draw.rect(s, dk, (2, 2, BLOCK_SIZE-4, 5))
                pygame.draw.rect(s, dk, (2, BLOCK_SIZE-7, BLOCK_SIZE-4, 5))
                for sx2 in [2, 14, 26]:
                    pygame.draw.rect(s, dk, (sx2, 7, 4, 18))
                # Stepped hooks between verticals
                for hx2 in [7, 19]:
                    pygame.draw.lines(s, dk, False, [(hx2,8),(hx2+5,8),(hx2+5,13),(hx2+2,13)], 2)
                    pygame.draw.lines(s, lt, False, [(hx2,9),(hx2+4,9),(hx2+4,12)], 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == VIKING_CARVING:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 30)
                s.fill(c)
                # Interlaced serpent body — figure-8 looping
                pygame.draw.arc(s, lt, (4, 4, 14, 14), 0, math.pi*1.5, 3)
                pygame.draw.arc(s, lt, (14, 4, 14, 14), math.pi*0.5, math.pi*2, 3)
                pygame.draw.arc(s, lt, (4, 14, 14, 14), math.pi*1.5, math.pi*3, 3)
                pygame.draw.arc(s, lt, (14, 14, 14, 14), math.pi, math.pi*2.5, 3)
                # Cover crossings
                for px2, py2 in [(11,11),(21,11),(11,21),(21,21)]:
                    pygame.draw.rect(s, c, (px2-2, py2-2, 4, 4))
                # Dragon head hint top-left
                pygame.draw.circle(s, lt, (5, 3), 2)
                pygame.draw.line(s, lt, (5,3),(3,1),1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == RUNE_STONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 38)
                lt = _lighter(c, 12)
                # Stone surface
                pygame.draw.line(s, dk, (0, 15), (BLOCK_SIZE, 15), 1)
                # Rune characters (simplified)
                runes = [
                    [(3,3),(3,9)],         # |
                    [(6,3),(9,6),(6,9)],   # < (Tiwaz)
                    [(12,3),(12,9),(15,3),(15,9),(12,6),(15,6)],  # H (Hagalaz)
                    [(18,3),(21,9),(18,9)],  # zigzag
                    [(3,17),(6,17),(6,23),(3,23)],  # square
                    [(9,17),(12,20),(9,23)],  # < inverted
                    [(15,17),(18,17),(18,23),(21,23)],  # L
                    [(24,17),(27,20),(24,23)],  # rune stroke
                ]
                for pts in runes:
                    if len(pts) >= 2:
                        pygame.draw.lines(s, dk, False, pts, 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PERSIAN_IWAN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 18)
                void = _darken(c, 45)
                # Pointed arch opening
                pygame.draw.polygon(s, void, [(8,30),(8,14),(16,4),(24,14),(24,30)])
                pygame.draw.lines(s, dk, False, [(8,30),(8,14),(16,4),(24,14),(24,30)], 2)
                # Muqarnas rows inside arch (stepped niches)
                for iy in [10, 15, 20]:
                    for ix2 in [10, 14, 18]:
                        if ix2 > iy-2 and ix2 < BLOCK_SIZE-iy+2:
                            pygame.draw.rect(s, _lighter(void, 10), (ix2-1, iy, 4, 4))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == KILIM_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                cols = [(168,52,42),(210,175,45),(235,220,190),(80,120,160),(95,145,80)]
                # Horizontal stripe bands with chevron/diamond accents
                for row, stripe_c in enumerate(cols):
                    y2 = row * 7
                    pygame.draw.rect(s, stripe_c, (0, y2, BLOCK_SIZE, 6))
                    if row % 2 == 0:
                        for dx2 in range(0, BLOCK_SIZE, 6):
                            pygame.draw.polygon(s, _darken(stripe_c, 25), [(dx2,y2+3),(dx2+3,y2),(dx2+6,y2+3),(dx2+3,y2+6)])
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == AFRICAN_MUD_BRICK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 25)
                lt = _lighter(c, 15)
                # Horizontal mud courses
                for y2 in [8, 17, 26]:
                    pygame.draw.line(s, dk, (0, y2), (BLOCK_SIZE, y2), 2)
                    pygame.draw.line(s, lt, (0, y2-1), (BLOCK_SIZE, y2-1), 1)
                # Timber pole ends protruding from wall
                for tx2, ty2 in [(4, 4),(12, 4),(20, 4),(28, 4),(8, 13),(16, 13),(24, 13),(4, 22),(12, 22),(20, 22),(28, 22)]:
                    pygame.draw.circle(s, dk, (tx2, ty2), 2)
                    pygame.draw.circle(s, lt, (tx2-1, ty2-1), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == KENTE_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                strips = [(185,148,30),(35,90,160),(200,60,40),(90,160,70),(185,148,30),(35,90,160)]
                sw = BLOCK_SIZE // len(strips)
                for i, sc in enumerate(strips):
                    pygame.draw.rect(s, sc, (i*sw, 0, sw, BLOCK_SIZE))
                    # Cross-woven accents
                    for y2 in range(0, BLOCK_SIZE, 4):
                        if y2 % 8 == 0:
                            pygame.draw.line(s, _darken(sc, 25), (i*sw, y2), (i*sw+sw, y2), 1)
                        else:
                            pygame.draw.line(s, _lighter(sc, 15), (i*sw, y2), (i*sw+sw, y2), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == WAT_FINIAL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 22)
                s.fill(_darken(c, 30))
                # Stacked rings narrowing to a point (chofa spire)
                for i, (w, y2) in enumerate([(18,26),(14,21),(10,17),(8,13),(6,10),(4,7),(2,4),(2,2)]):
                    x2 = (BLOCK_SIZE - w) // 2
                    shade = c if i % 2 == 0 else _lighter(c, 12)
                    pygame.draw.rect(s, shade, (x2, y2, w, 4))
                    pygame.draw.line(s, lt, (x2, y2), (x2+w, y2), 1)
                pygame.draw.line(s, lt, (16, 1), (16, 3), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == KHMER_STONE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 30)
                lt = _lighter(c, 18)
                s.fill(c)
                # Devata face — simplified Angkor carving
                pygame.draw.ellipse(s, dk, (9, 5, 14, 12), 1)
                # Crown/headdress
                for cx3 in [12, 16, 20]:
                    pygame.draw.line(s, dk, (cx3, 5), (cx3, 1), 2)
                pygame.draw.line(s, dk, (10, 4), (22, 4), 1)
                # Eyes
                pygame.draw.line(s, dk, (11, 9), (14, 9), 2)
                pygame.draw.line(s, dk, (18, 9), (21, 9), 2)
                # Smile
                pygame.draw.arc(s, dk, (12, 12, 8, 5), math.pi, math.pi*2, 1)
                # Body panel with flame pattern
                pygame.draw.rect(s, _darken(c, 10), (6, 18, 20, 12))
                for fx2 in [8, 13, 18, 23]:
                    pygame.draw.lines(s, dk, False, [(fx2,28),(fx2+1,23),(fx2+2,28)], 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == HANJI_SCREEN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                wood = (118, 85, 45)
                dk = _darken(c, 12)
                s.fill(c)
                # Outer frame
                pygame.draw.rect(s, wood, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
                # Delicate flower-lattice grid
                for y2 in range(4, BLOCK_SIZE-4, 8):
                    for x2 in range(4, BLOCK_SIZE-4, 8):
                        # Small 4-petal flower
                        pygame.draw.circle(s, dk, (x2, y2), 3, 1)
                        pygame.draw.line(s, dk, (x2-3, y2), (x2+3, y2), 1)
                        pygame.draw.line(s, dk, (x2, y2-3), (x2, y2+3), 1)
                surfs[bid] = s
                continue
            if bid == DANCHEONG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                # Korean dancheong — colorful bands of blue/red/green/white
                bands = [(55,95,158),(200,60,45),(80,155,80),(230,220,200),(55,95,158),(200,60,45)]
                bw2 = BLOCK_SIZE // len(bands)
                for i, bc in enumerate(bands):
                    pygame.draw.rect(s, bc, (i*bw2, 0, bw2, BLOCK_SIZE))
                    # Geometric inner pattern
                    mid_y = BLOCK_SIZE // 2
                    pygame.draw.line(s, _darken(bc, 30), (i*bw2, mid_y), (i*bw2+bw2, mid_y), 1)
                    pygame.draw.circle(s, _lighter(bc, 20), (i*bw2 + bw2//2, mid_y), 2)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ART_DECO_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                gold = (200, 165, 45)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE
                # Fan sunburst radiating from bottom centre
                for i in range(13):
                    a = math.pi * (0.1 + i * 0.068)
                    r1, r2 = 4, 26
                    x1 = cx2 + int(r1 * math.cos(a)); y1 = cy2 - int(r1 * math.sin(a))
                    x2 = cx2 + int(r2 * math.cos(a)); y2 = cy2 - int(r2 * math.sin(a))
                    shade = gold if i % 2 == 0 else dk
                    pygame.draw.line(s, shade, (x1, y1), (x2, y2), 2 if i % 2 == 0 else 1)
                # Concentric arc bands
                for r in [10, 18, 25]:
                    pygame.draw.arc(s, dk, (cx2-r, cy2-r, r*2, r*2), 0, math.pi, 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == OBSIDIAN_CUT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 40)
                mid = _lighter(c, 20)
                s.fill(c)
                # Polished angular facets
                pygame.draw.polygon(s, mid, [(0,0),(BLOCK_SIZE,0),(BLOCK_SIZE//2, BLOCK_SIZE//2)])
                pygame.draw.polygon(s, _lighter(c, 8), [(0,0),(0,BLOCK_SIZE),(BLOCK_SIZE//2, BLOCK_SIZE//2)])
                # Highlight edge
                pygame.draw.line(s, lt, (0, 0), (BLOCK_SIZE, 0), 2)
                pygame.draw.line(s, lt, (0, 0), (0, BLOCK_SIZE), 1)
                # Subtle sheen dots
                for px2, py2 in [(4,4),(8,2),(2,8),(14,6),(6,14)]:
                    pygame.draw.rect(s, lt, (px2, py2, 1, 1))
                pygame.draw.rect(s, _lighter(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == OTTOMAN_ARCH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 15)
                void = _darken(c, 45)
                # Pointed arch opening
                pygame.draw.polygon(s, void, [(8,30),(8,14),(16,5),(24,14),(24,30)])
                pygame.draw.lines(s, dk, False, [(8,30),(8,14),(16,5),(24,14),(24,30)], 2)
                pygame.draw.lines(s, lt, False, [(9,30),(9,14),(16,6),(23,14),(23,30)], 1)
                # Spandrel geometric fill (each side of arch)
                for sx2, sy2 in [(2,4),(26,4)]:
                    pygame.draw.polygon(s, dk, [(sx2,sy2),(sx2+4,sy2),(sx2+2,sy2+4)], 1)
                    pygame.draw.circle(s, dk, (sx2+2, sy2+6), 2, 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == LOTUS_CAPITAL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 20)
                s.fill(c)
                # Column shaft
                pygame.draw.rect(s, _darken(c, 15), (12, 22, 8, BLOCK_SIZE-22))
                pygame.draw.line(s, lt, (13, 22), (13, BLOCK_SIZE-1), 1)
                # Lotus petals opening outward
                for i in range(8):
                    a = math.pi * i / 4
                    r = 11
                    px2 = 16 + int(r * math.cos(a)); py2 = 14 + int(r * math.sin(a))
                    pygame.draw.ellipse(s, c, (px2-3, py2-5, 6, 10))
                    pygame.draw.ellipse(s, dk, (px2-3, py2-5, 6, 10), 1)
                    pygame.draw.line(s, lt, (px2, py2-4), (px2, py2+3), 1)
                # Centre disc
                pygame.draw.circle(s, _lighter(c, 12), (16, 14), 5)
                pygame.draw.circle(s, dk, (16, 14), 5, 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            # ---- World architecture batch 5 ----
            if bid == AZULEJO_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                blue = (45, 85, 165)
                s.fill(c)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                # Pictorial scene: simple tree with birds
                pygame.draw.line(s, blue, (cx2, 28), (cx2, 14), 2)
                pygame.draw.circle(s, blue, (cx2, 11), 7, 1)
                pygame.draw.circle(s, blue, (cx2-5, 14), 4, 1)
                pygame.draw.circle(s, blue, (cx2+5, 14), 4, 1)
                # Border pattern
                pygame.draw.rect(s, blue, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
                for bx2 in range(3, BLOCK_SIZE-3, 6):
                    pygame.draw.circle(s, blue, (bx2, 2), 1)
                    pygame.draw.circle(s, blue, (bx2, BLOCK_SIZE-2), 1)
                for by2 in range(3, BLOCK_SIZE-3, 6):
                    pygame.draw.circle(s, blue, (2, by2), 1)
                    pygame.draw.circle(s, blue, (BLOCK_SIZE-2, by2), 1)
                surfs[bid] = s
                continue
            if bid == MANUELINE_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 18)
                # Twisted rope motif down both sides
                for rx2 in [3, BLOCK_SIZE-5]:
                    for ry2 in range(0, BLOCK_SIZE, 5):
                        twist = 2 if (ry2//5) % 2 else -2
                        pygame.draw.ellipse(s, dk, (rx2+twist, ry2, 4, 5))
                # Central armillary sphere
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                pygame.draw.circle(s, dk, (cx2, cy2), 7, 1)
                pygame.draw.ellipse(s, dk, (cx2-7, cy2-3, 14, 6), 1)
                pygame.draw.line(s, dk, (cx2, cy2-7), (cx2, cy2+7), 1)
                pygame.draw.line(s, lt, (cx2-7, cy2), (cx2+7, cy2), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == TORII_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 20)
                dk = _darken(c, 20)
                s.fill(_darken(c, 35))
                # Two columns
                pygame.draw.rect(s, c, (4, 8, 5, 24))
                pygame.draw.rect(s, c, (23, 8, 5, 24))
                pygame.draw.line(s, lt, (4, 8), (4, 32), 1)
                pygame.draw.line(s, lt, (23, 8), (23, 32), 1)
                # Kasagi (top rail — slightly upcurved)
                pygame.draw.rect(s, c, (1, 4, 30, 4))
                pygame.draw.line(s, lt, (1, 4), (31, 4), 1)
                pygame.draw.arc(s, lt, (0, 3, 32, 6), 0, math.pi, 1)
                # Nuki (middle tie rail)
                pygame.draw.rect(s, c, (3, 13, 26, 3))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == INCA_ASHLAR:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 14)
                # Irregular multi-sided stones fitted without mortar
                polys = [
                    [(1,1),(14,1),(16,7),(12,14),(1,12)],
                    [(15,1),(31,1),(31,10),(18,12),(16,7)],
                    [(1,13),(12,15),(14,22),(8,28),(1,25)],
                    [(13,15),(18,13),(31,11),(31,22),(20,25),(14,23)],
                    [(1,26),(8,29),(12,31),(1,31)],
                    [(9,29),(14,24),(20,26),(22,31),(9,31)],
                    [(21,27),(31,23),(31,31),(22,31)],
                ]
                for pts in polys:
                    pygame.draw.polygon(s, c, pts)
                    pygame.draw.polygon(s, dk, pts, 1)
                    pygame.draw.line(s, lt, pts[0], pts[1], 1)
                pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == RUSSIAN_KOKOSHNIK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 28)
                lt = _lighter(c, 20)
                gold = (205, 165, 45)
                # Onion-curved arch with ornate border
                pygame.draw.arc(s, dk, (3, 3, 26, 22), 0, math.pi, 3)
                pygame.draw.arc(s, gold, (5, 5, 22, 18), 0, math.pi, 1)
                # Decorative scallop border
                for i in range(6):
                    ax2 = 4 + i * 4
                    pygame.draw.arc(s, gold, (ax2, 2, 5, 5), 0, math.pi, 1)
                # Side columns
                pygame.draw.line(s, dk, (3, 14), (3, 30), 2)
                pygame.draw.line(s, dk, (29, 14), (29, 30), 2)
                pygame.draw.line(s, gold, (4, 14), (4, 30), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ONION_DOME_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 22)
                dk = _darken(c, 20)
                gold = (205, 165, 45)
                s.fill(c)
                # Metallic scale tiles in staggered rows
                for row in range(5):
                    off = 4 if row % 2 else 0
                    y2 = row * 7
                    for col in range(-1, 5):
                        cx3 = col * 8 + off
                        pygame.draw.arc(s, dk, (cx3, y2, 8, 9), 0, math.pi, 2)
                        pygame.draw.arc(s, lt, (cx3+1, y2+1, 6, 7), 0, math.pi, 1)
                # Gold highlight line
                pygame.draw.line(s, gold, (0, 3), (BLOCK_SIZE, 3), 1)
                pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == GEORGIAN_FANLIGHT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lead = (55, 52, 48)
                s.fill(lead)
                glass = c
                cx2 = BLOCK_SIZE//2
                # Semi-circular fanlight with radiating glazing bars
                pygame.draw.ellipse(s, glass, (2, 2, BLOCK_SIZE-4, BLOCK_SIZE-4))
                pygame.draw.rect(s, lead, (0, BLOCK_SIZE//2, BLOCK_SIZE, BLOCK_SIZE))
                for i in range(9):
                    a = math.pi * i / 8
                    r = BLOCK_SIZE//2 - 2
                    pygame.draw.line(s, lead, (cx2, BLOCK_SIZE//2), (cx2+int(r*math.cos(a)), BLOCK_SIZE//2-int(r*math.sin(a))), 1)
                # Concentric rings
                for r in [5, 9, 13]:
                    pygame.draw.circle(s, lead, (cx2, BLOCK_SIZE//2), r, 1)
                surfs[bid] = s
                continue
            if bid == PALLADIAN_WINDOW:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                void = _darken(c, 42)
                dk = _darken(c, 25)
                s.fill(c)
                # Central arched opening + two flanking flat-topped openings
                pygame.draw.rect(s, void, (12, 10, 8, 20))
                pygame.draw.arc(s, void, (12, 5, 8, 10), 0, math.pi)
                pygame.draw.rect(s, void, (2, 14, 8, 16))
                pygame.draw.rect(s, void, (22, 14, 8, 16))
                # Reveals
                for ox2, ow2, oy2 in [(12,8,5),(2,8,14),(22,8,14)]:
                    pygame.draw.rect(s, dk, (ox2, oy2, ow2, 1))
                pygame.draw.line(s, dk, (10, 5), (10, 30), 1)
                pygame.draw.line(s, dk, (22, 5), (22, 30), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == STAVE_PLANK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 20)
                dk = _darken(c, 18)
                s.fill(c)
                # Vertical planks with dragon-head carving at top
                for px2 in [0, 10, 21]:
                    pygame.draw.line(s, dk, (px2+8, 0), (px2+8, BLOCK_SIZE), 1)
                # Dragon head hints
                for hx2 in [5, 16, 27]:
                    pygame.draw.arc(s, lt, (hx2-3, 1, 6, 6), 0, math.pi, 2)
                    pygame.draw.line(s, lt, (hx2-1, 4), (hx2-3, 7), 1)
                    pygame.draw.line(s, lt, (hx2+1, 4), (hx2+3, 7), 1)
                # Tarring/weathering streaks
                for wx2 in [3, 13, 24]:
                    pygame.draw.line(s, _darken(c, 22), (wx2, 10), (wx2, 25), 1)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == IONIC_CAPITAL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 15)
                s.fill(c)
                # Abacus (flat top slab)
                pygame.draw.rect(s, _darken(c, 10), (0, 1, BLOCK_SIZE, 5))
                pygame.draw.line(s, lt, (0, 1), (BLOCK_SIZE, 1), 1)
                pygame.draw.line(s, dk, (0, 6), (BLOCK_SIZE, 6), 1)
                # Volute scrolls (left and right)
                for vx2 in [5, BLOCK_SIZE-5]:
                    pygame.draw.arc(s, dk, (vx2-6, 7, 12, 12), 0, math.pi*1.5, 2)
                    pygame.draw.arc(s, dk, (vx2-3, 10, 6, 6), math.pi*0.5, math.pi*2.5, 2)
                    pygame.draw.circle(s, dk, (vx2, 13), 2)
                # Echinus (egg-and-dart band)
                for ex2 in range(3, BLOCK_SIZE-3, 6):
                    pygame.draw.ellipse(s, dk, (ex2-2, 20, 5, 6))
                    pygame.draw.line(s, dk, (ex2+3, 20), (ex2+3, 26), 1)
                # Column shaft top
                pygame.draw.rect(s, _darken(c, 8), (10, 26, 12, 6))
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MOORISH_STAR_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                cream = (230, 218, 195)
                s.fill(c)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                # 8-pointed star
                star_pts = []
                for i in range(16):
                    a = math.pi * i / 8 - math.pi/8
                    r = 12 if i % 2 == 0 else 6
                    star_pts.append((cx2+int(r*math.cos(a)), cy2+int(r*math.sin(a))))
                pygame.draw.polygon(s, cream, star_pts)
                pygame.draw.polygon(s, _darken(c, 20), star_pts, 1)
                # Cross infill between star points
                for i in range(4):
                    a = math.pi * i / 2
                    px2 = cx2 + int(14*math.cos(a)); py2 = cy2 + int(14*math.sin(a))
                    pygame.draw.polygon(s, cream, [(px2-3,py2-3),(px2+3,py2-3),(px2+3,py2+3),(px2-3,py2+3)])
                surfs[bid] = s
                continue
            if bid == CRAFTSMAN_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 25)
                dk = _darken(c, 28)
                s.fill(c)
                # Stylised tulip/plant motif
                pygame.draw.line(s, dk, (16, 30), (16, 16), 2)
                pygame.draw.line(s, dk, (16, 24), (10, 18), 1)
                pygame.draw.line(s, dk, (16, 24), (22, 18), 1)
                # Three tulip heads
                for fx2, fy2 in [(16, 10), (9, 15), (23, 15)]:
                    pygame.draw.ellipse(s, dk, (fx2-3, fy2-5, 7, 8), 1)
                    pygame.draw.ellipse(s, lt, (fx2-2, fy2-4, 5, 6))
                # Decorative border
                pygame.draw.rect(s, dk, (1, 1, BLOCK_SIZE-2, BLOCK_SIZE-2), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BRUTALIST_PANEL:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 22)
                lt = _lighter(c, 10)
                # Board-formed concrete — horizontal plank-form impressions
                for y2 in [0, 6, 13, 20, 27]:
                    pygame.draw.line(s, dk, (0, y2), (BLOCK_SIZE, y2), 1)
                    pygame.draw.line(s, lt, (0, y2+1), (BLOCK_SIZE, y2+1), 1)
                # Tie-hole circles (formwork bolts)
                for tx2, ty2 in [(4,3),(12,3),(20,3),(28,3),(4,16),(12,16),(20,16),(28,16)]:
                    pygame.draw.circle(s, dk, (tx2, ty2), 2)
                # Aggregate pebble texture
                for px2, py2 in [(6,8),(15,9),(24,7),(9,22),(18,23),(27,22)]:
                    pygame.draw.circle(s, dk, (px2, py2), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == METOPE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 18)
                # Simple framed square panel with carved interior scene
                pygame.draw.rect(s, dk, (2, 2, BLOCK_SIZE-4, BLOCK_SIZE-4), 2)
                # Simplified warrior/helmet silhouette
                pygame.draw.circle(s, dk, (16, 9), 5, 1)
                pygame.draw.line(s, dk, (12, 7), (10, 3), 2)  # helmet crest left
                pygame.draw.line(s, dk, (20, 7), (22, 3), 2)  # helmet crest right
                pygame.draw.rect(s, dk, (12, 14, 8, 12))    # torso
                pygame.draw.line(s, dk, (10, 16), (6, 24), 2) # arm/shield
                pygame.draw.line(s, dk, (22, 16), (26, 24), 2)# spear
                pygame.draw.line(s, lt, (16, 14), (16, 26), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ARMENIAN_KHACHKAR:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 35)
                lt = _lighter(c, 20)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                # Cross with trefoil arm-ends
                for dx2, dy2 in [(0,-1),(0,1),(1,0),(-1,0)]:
                    ax2, ay2 = cx2+dx2*10, cy2+dy2*10
                    pygame.draw.line(s, dk, (cx2, cy2), (ax2, ay2), 3)
                    pygame.draw.circle(s, dk, (ax2, ay2), 3, 1)
                    pygame.draw.circle(s, lt, (ax2, ay2), 2)
                pygame.draw.circle(s, dk, (cx2, cy2), 4, 1)
                # Interlaced geometric infill
                for r in [6, 10, 14]:
                    pygame.draw.circle(s, dk, (cx2, cy2), r, 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == BENIN_RELIEF:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 30)
                lt = _lighter(c, 22)
                # Bronze cast face — Oba face with coral bead collar
                pygame.draw.ellipse(s, dk, (8, 4, 16, 14), 1)
                # Eyes
                pygame.draw.ellipse(s, dk, (10, 9, 4, 3))
                pygame.draw.ellipse(s, dk, (18, 9, 4, 3))
                # Scarification dots on forehead
                for fx2, fy2 in [(12,5),(14,5),(16,5),(18,5),(14,7),(16,7)]:
                    pygame.draw.circle(s, lt, (fx2, fy2), 1)
                # Coral bead collar
                for row in range(3):
                    for bx2 in range(5, BLOCK_SIZE-5, 4):
                        pygame.draw.circle(s, _darken(c, 15 + row*8), (bx2, 20+row*4), 2)
                # Crown hints
                for cx3 in [12, 16, 20]:
                    pygame.draw.line(s, lt, (cx3, 4), (cx3, 1), 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MAORI_CARVING:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 30)
                s.fill(c)
                # Koru spirals — fern frond uncoiling
                for kx2, ky2, r, a_start in [(8, 24, 7, 0.2), (24, 8, 7, math.pi+0.2)]:
                    pygame.draw.arc(s, lt, (kx2-r, ky2-r, r*2, r*2), a_start, a_start+math.pi*1.5, 3)
                    pygame.draw.arc(s, lt, (kx2-r//2, ky2-r//2, r, r), a_start+0.3, a_start+math.pi*1.2, 2)
                    pygame.draw.circle(s, lt, (kx2, ky2), 3, 1)
                # Connecting organic line
                pygame.draw.line(s, lt, (8, 17), (24, 15), 2)
                # Serrated border (notched)
                for i in range(8):
                    bx2 = i * 4
                    pygame.draw.polygon(s, lt, [(bx2, 0),(bx2+2, 3),(bx2+4, 0)])
                    pygame.draw.polygon(s, lt, [(bx2, BLOCK_SIZE),(bx2+2, BLOCK_SIZE-3),(bx2+4, BLOCK_SIZE)])
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MUGHAL_JALI:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                void = _darken(c, 40)
                s.fill(c)
                # Repeating pierced hexagonal lattice
                for row in range(5):
                    off = 5 if row % 2 else 0
                    y2 = row * 7
                    for col in range(-1, 4):
                        cx3 = col * 10 + off
                        # Hexagon outline
                        hex_pts = [(cx3+5, y2), (cx3+8, y2+3), (cx3+8, y2+7),
                                   (cx3+5, y2+10), (cx3+2, y2+7), (cx3+2, y2+3)]
                        pygame.draw.polygon(s, void, hex_pts)
                        pygame.draw.polygon(s, _darken(c, 15), hex_pts, 1)
                pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PERSIAN_TILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                white = (232, 228, 220)
                dk = _darken(c, 25)
                s.fill(c)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                # Eight-pointed star in white on turquoise
                star_pts = []
                for i in range(16):
                    a = math.pi * i / 8
                    r = 11 if i % 2 == 0 else 5
                    star_pts.append((cx2+int(r*math.cos(a)), cy2+int(r*math.sin(a))))
                pygame.draw.polygon(s, white, star_pts)
                pygame.draw.polygon(s, dk, star_pts, 1)
                pygame.draw.circle(s, dk, (cx2, cy2), 3)
                surfs[bid] = s
                continue
            if bid == SWISS_CHALET:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 22)
                dk = _darken(c, 25)
                s.fill(c)
                # Horizontal plank grain
                for y2 in [0, 8, 16, 24]:
                    pygame.draw.line(s, dk, (0, y2), (BLOCK_SIZE, y2), 1)
                    pygame.draw.line(s, lt, (0, y2+1), (BLOCK_SIZE, y2+1), 1)
                # Carved heart motif (Swiss traditional)
                pygame.draw.arc(s, dk, (9, 11, 6, 6), 0, math.pi, 2)
                pygame.draw.arc(s, dk, (15, 11, 6, 6), 0, math.pi, 2)
                pygame.draw.lines(s, dk, False, [(9, 14),(12, 21),(16, 14)], 2)
                pygame.draw.lines(s, dk, False, [(15, 14),(18, 21),(21, 14)], 2)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == ANDEAN_TEXTILE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                cols = [(168,45,42),(210,165,40),(45,100,168),(80,160,80),(232,220,195)]
                # Stepped fret (chakana cross) pattern
                for row in range(5):
                    for col in range(5):
                        tc = cols[(row + col) % len(cols)]
                        pygame.draw.rect(s, tc, (col*6+1, row*6+1, 5, 5))
                        # Stepped inner element
                        if (row + col) % 2 == 0:
                            pygame.draw.rect(s, _darken(tc, 25), (col*6+2, row*6+2, 3, 3))
                surfs[bid] = s
                continue
            if bid == BAROQUE_ORNAMENT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                gold = (210, 168, 38)
                dk = _darken(c, 20)
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                # Central fleur-de-lis / cartouche
                pygame.draw.ellipse(s, gold, (cx2-4, cy2-7, 8, 14), 1)
                pygame.draw.circle(s, gold, (cx2, cy2-8), 3, 1)
                pygame.draw.circle(s, gold, (cx2, cy2+7), 3, 1)
                # Side acanthus volutes
                for sx2 in [5, BLOCK_SIZE-5]:
                    pygame.draw.arc(s, gold, (sx2-5, cy2-6, 10, 10), 0, math.pi*1.5, 2)
                    pygame.draw.circle(s, gold, (sx2, cy2+4), 2)
                # Gold border
                pygame.draw.rect(s, gold, (1, 1, BLOCK_SIZE-2, BLOCK_SIZE-2), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == POLYNESIAN_CARVED:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                lt = _lighter(c, 28)
                dk = _darken(c, 20)
                s.fill(c)
                # Tiki face — large circular eyes, wide mouth
                pygame.draw.circle(s, lt, (11, 11), 5, 2)
                pygame.draw.circle(s, lt, (21, 11), 5, 2)
                pygame.draw.circle(s, dk, (11, 11), 2)
                pygame.draw.circle(s, dk, (21, 11), 2)
                # Brow notches
                pygame.draw.line(s, lt, (6, 6), (16, 6), 2)
                pygame.draw.line(s, lt, (16, 6), (26, 6), 2)
                # Wide mouth
                pygame.draw.rect(s, lt, (6, 20, 20, 5), 2)
                # Teeth
                for tx2 in [8, 13, 18, 23]:
                    pygame.draw.line(s, lt, (tx2, 20), (tx2, 25), 1)
                # Geometric border
                pygame.draw.rect(s, lt, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
                for i in range(4, BLOCK_SIZE, 8):
                    pygame.draw.circle(s, lt, (i, 1), 2)
                    pygame.draw.circle(s, lt, (i, BLOCK_SIZE-2), 2)
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == MOORISH_COLUMN:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                dk = _darken(c, 28)
                lt = _lighter(c, 18)
                gold = (205, 168, 45)
                s.fill(_darken(c, 20))
                # Slender shaft
                pygame.draw.rect(s, c, (12, 8, 8, 18))
                pygame.draw.line(s, lt, (12, 8), (12, 26), 1)
                pygame.draw.line(s, dk, (19, 8), (19, 26), 1)
                # Muqarnas capital — small stacked niches
                for i, (w, y2) in enumerate([(20,4),(16,6),(12,3)]):
                    x2 = (BLOCK_SIZE - w) // 2
                    shade = c if i % 2 == 0 else _lighter(c, 10)
                    pygame.draw.rect(s, shade, (x2, y2, w, 3))
                    pygame.draw.line(s, gold, (x2, y2), (x2+w, y2), 1)
                # Base
                pygame.draw.rect(s, c, (9, 26, 14, 4))
                pygame.draw.line(s, lt, (9, 26), (23, 26), 1)
                pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == PORTUGUESE_CORK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                dk = _darken(c, 25)
                lt = _lighter(c, 18)
                # Cork cell texture — irregular small polygons
                for cy3 in range(0, BLOCK_SIZE, 5):
                    for cx3 in range(0, BLOCK_SIZE, 5):
                        off_x = (cy3 // 5) % 2 * 2
                        shade = _darken(c, 10) if (cx3 + cy3) % 10 == 0 else c
                        pygame.draw.rect(s, shade, (cx3+off_x, cy3, 4, 4))
                        pygame.draw.rect(s, dk, (cx3+off_x, cy3, 4, 4), 1)
                pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
                surfs[bid] = s
                continue
            # --- Textile supply chain ---
            if bid == FLAX_BUSH:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(5, 16), (13, 20), (21, 14)]:
                    pygame.draw.rect(s, (130, 165, 195), (stx, BLOCK_SIZE - sth, 2, sth - 6))
                for fx, fy in [(4, 10), (12, 6), (21, 11)]:
                    pygame.draw.ellipse(s, (140, 175, 215), (fx-3, fy-2, 8, 5))
                    pygame.draw.ellipse(s, (165, 195, 230), (fx-2, fy-1, 5, 3))
                surfs[bid] = s
                continue
            if bid == FLAX_CROP_YOUNG:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(8, 14), (16, 18), (24, 12)]:
                    pygame.draw.rect(s, (120, 180, 140), (stx, BLOCK_SIZE - sth, 2, sth))
                surfs[bid] = s
                continue
            if bid == FLAX_CROP_MATURE:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 0))
                for stx, sth in [(5, 24), (13, 28), (21, 22)]:
                    pygame.draw.rect(s, (145, 175, 210), (stx, BLOCK_SIZE - sth, 2, sth - 8))
                    pygame.draw.ellipse(s, (155, 185, 220), (stx-3, BLOCK_SIZE - sth - 2, 8, 5))
                    pygame.draw.ellipse(s, (175, 200, 235), (stx-2, BLOCK_SIZE - sth - 1, 5, 3))
                surfs[bid] = s
                continue
            if bid == SPINNING_WHEEL_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                s.fill((30, 22, 14))
                c = (165, 130, 75)
                # Wheel
                pygame.draw.circle(s, c, (22, 16), 11, 2)
                for a in range(0, 360, 45):
                    ax = 22 + int(9 * math.cos(math.radians(a)))
                    ay = 16 + int(9 * math.sin(math.radians(a)))
                    pygame.draw.line(s, c, (22, 16), (ax, ay), 1)
                # Frame legs
                pygame.draw.line(s, c, (10, 28), (18, 28), 2)
                pygame.draw.line(s, c, (18, 28), (22, 5), 2)
                pygame.draw.line(s, c, (30, 28), (22, 5), 2)
                # Spindle
                pygame.draw.line(s, (200, 180, 120), (28, 26), (32, 10), 1)
                pygame.draw.rect(s, _darken((30, 22, 14), 10), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == DYE_VAT_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                s.fill((30, 22, 14))
                c = (85, 110, 155)
                # Vat body
                pygame.draw.ellipse(s, c, (5, 14, 22, 14))
                pygame.draw.rect(s, c, (5, 20, 22, 8))
                pygame.draw.ellipse(s, _darken(c, 20), (5, 26, 22, 8))
                # Liquid surface
                pygame.draw.ellipse(s, _lighter(c, 30), (6, 14, 20, 10))
                # Legs
                pygame.draw.line(s, (100, 75, 45), (6, 28), (4, BLOCK_SIZE-2), 2)
                pygame.draw.line(s, (100, 75, 45), (26, 28), (28, BLOCK_SIZE-2), 2)
                pygame.draw.rect(s, _darken((30, 22, 14), 10), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == LOOM_BLOCK:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                s.fill((30, 22, 14))
                c = (140, 100, 55)
                # Frame
                pygame.draw.rect(s, c, (4, 4, 24, 24), 2)
                # Warp threads (vertical)
                for tx in range(7, 29, 4):
                    pygame.draw.line(s, (200, 185, 145), (tx, 5), (tx, 27), 1)
                # Weft thread (horizontal)
                pygame.draw.line(s, (185, 135, 80), (4, 15), (28, 15), 2)
                pygame.draw.rect(s, _darken((30, 22, 14), 10), s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
                       TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
                       TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY):
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                # Border
                pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 3)
                lt = _lighter(c, 30)
                # Simple geometric pattern lines
                for gx in range(4, BLOCK_SIZE - 4, 5):
                    pygame.draw.line(s, lt, (gx, 4), (gx, BLOCK_SIZE - 4), 1)
                for gy in range(4, BLOCK_SIZE - 4, 5):
                    pygame.draw.line(s, _darken(c, 15), (4, gy), (BLOCK_SIZE - 4, gy), 1)
                # Centre medallion
                cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
                pygame.draw.polygon(s, _darken(c, 30), [(cx2,cy2-6),(cx2+6,cy2),(cx2,cy2+6),(cx2-6,cy2)])
                pygame.draw.polygon(s, lt, [(cx2,cy2-3),(cx2+3,cy2),(cx2,cy2+3),(cx2-3,cy2)])
                surfs[bid] = s
                continue
            if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON,
                       TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
                       TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY):
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                c = bdata["color"]
                s.fill(c)
                # Tapestry is taller-looking: decorative border top+bottom
                pygame.draw.rect(s, _darken(c, 30), (0, 0, BLOCK_SIZE, 3))
                pygame.draw.rect(s, _darken(c, 30), (0, BLOCK_SIZE-3, BLOCK_SIZE, 3))
                pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
                lt = _lighter(c, 28)
                # Horizontal colour bands like a real tapestry
                bands_c = [c, _darken(c, 20), lt, _darken(c, 20), c]
                bh3 = (BLOCK_SIZE - 6) // len(bands_c)
                for bi2, bc2 in enumerate(bands_c):
                    pygame.draw.rect(s, bc2, (1, 3 + bi2*bh3, BLOCK_SIZE-2, bh3))
                    for wx2 in range(1, BLOCK_SIZE-2, 3):
                        pygame.draw.line(s, _darken(bc2, 12), (wx2, 3+bi2*bh3), (wx2, 3+(bi2+1)*bh3), 1)
                surfs[bid] = s
                continue
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            s.fill(bdata["color"])
            pygame.draw.rect(s, _darken(bdata["color"]), s.get_rect(), 1)
            surfs[bid] = s
        return surfs

    def _build_water_surfs(self):
        surfs = []
        for level in range(1, 9):
            h = max(4, level * BLOCK_SIZE // 8)   # level 1=4px … level 8=32px
            s = pygame.Surface((BLOCK_SIZE, h), pygame.SRCALPHA)
            alpha = 110 + level * 7               # deeper = more opaque
            s.fill((40, 110, 220, alpha))
            shimmer = pygame.Surface((BLOCK_SIZE, 2), pygame.SRCALPHA)
            shimmer.fill((100, 180, 255, 55))
            for ry in range(3, h - 1, 9):
                s.blit(shimmer, (0, ry))
            surfs.append(s)
        return surfs

    def _build_resource_hint_surfs(self):
        stone_col = BLOCKS[STONE]["color"]
        hints = {}
        for bid in RESOURCE_BLOCKS:
            res_col  = BLOCKS[bid]["color"]
            hint_col = tuple(int(stone_col[i] * 0.8 + res_col[i] * 0.2) for i in range(3))
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            s.fill(hint_col)
            pygame.draw.rect(s, _darken(hint_col), s.get_rect(), 1)
            hints[bid] = s
        return hints

    def _build_biome_resource_hint_surfs(self):
        result = {}
        for biome, stone_col in BIOME_STONE_COLORS.items():
            hints = {}
            for bid in RESOURCE_BLOCKS:
                res_col = BLOCKS[bid]["color"]
                hint_col = tuple(int(stone_col[i] * 0.8 + res_col[i] * 0.2) for i in range(3))
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                s.fill(hint_col)
                pygame.draw.rect(s, _darken(hint_col), s.get_rect(), 1)
                hints[bid] = s
            result[biome] = hints
        return result

    def _build_biome_stone_surfs(self):
        surfs = {}
        for biome, color in BIOME_STONE_COLORS.items():
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            s.fill(color)
            pygame.draw.rect(s, _darken(color), s.get_rect(), 1)
            surfs[biome] = s
        return surfs

    def _build_log_variants(self):
        # 8 variants per log type
        # Trunk widths: full, full, medium(18), thin(12), full×4
        # Brightness shifts and texture details differ per variant
        trunk_widths  = [BLOCK_SIZE, BLOCK_SIZE, 18, 12, BLOCK_SIZE, BLOCK_SIZE, 18, BLOCK_SIZE]
        bright_shifts = [0, 18, 0, -14, 0, 14, -8, 0]
        grain_gaps    = [5,  4,  5,   4,  6,   5,  4,  5]
        variants = {}
        for bid in ALL_LOGS:
            bdata = BLOCKS.get(bid)
            if not bdata or not bdata.get("color"):
                continue
            base = bdata["color"]
            surfs = []
            for v in range(8):
                shift = bright_shifts[v]
                tone  = tuple(max(0, min(255, c + shift)) for c in base)
                dark  = _darken(tone, 32)
                tw    = trunk_widths[v]
                cx    = (BLOCK_SIZE - tw) // 2
                gs    = grain_gaps[v]
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                side_col = _darken(tone, 50)
                s.fill(side_col if tw < BLOCK_SIZE else tone)
                if tw < BLOCK_SIZE:
                    pygame.draw.rect(s, tone, (cx, 0, tw, BLOCK_SIZE))
                # Vertical grain lines
                grain = _darken(tone, 24)
                for gx in range(cx + 3, cx + tw - 2, gs):
                    pygame.draw.line(s, grain, (gx, 1), (gx, BLOCK_SIZE - 2), 1)
                # Highlight stripe
                hi = tuple(min(255, c + 14) for c in tone)
                if cx + 2 < cx + tw - 1:
                    pygame.draw.line(s, hi, (cx + 2, 1), (cx + 2, BLOCK_SIZE - 2), 1)
                # v4: knot — dark oval near centre
                if v == 4:
                    kx, ky = BLOCK_SIZE // 2, BLOCK_SIZE // 2 + 4
                    knot = _darken(tone, 55)
                    pygame.draw.ellipse(s, knot,             (kx - 4, ky - 3, 8, 6))
                    pygame.draw.ellipse(s, _darken(knot, 20),(kx - 2, ky - 1, 4, 3))
                # v5: moss patches
                if v == 5:
                    moss = (max(0, tone[0] - 22), min(255, tone[1] + 32), max(0, tone[2] - 22))
                    for mx, my in [(4, 2), (BLOCK_SIZE - 10, 5),
                                   (6, BLOCK_SIZE - 10), (BLOCK_SIZE - 8, BLOCK_SIZE - 8)]:
                        pygame.draw.rect(s, moss,             (mx, my, 5, 4))
                        pygame.draw.rect(s, _darken(moss, 18),(mx + 1, my + 1, 3, 2))
                # v7: horizontal bark rings
                if v == 7:
                    ring = _darken(tone, 28)
                    for ry in range(4, BLOCK_SIZE - 2, 7):
                        pygame.draw.line(s, ring, (cx + 1, ry), (cx + tw - 2, ry), 1)
                border_rect = (cx, 0, tw, BLOCK_SIZE) if tw < BLOCK_SIZE else s.get_rect()
                pygame.draw.rect(s, dark, border_rect, 1)
                surfs.append(s)
            variants[bid] = surfs
        return variants

    def _build_leaf_variants(self):
        # 8 variants: 4 solid (base, light, very-light, dark) + 4 speckled
        # v6 gets an autumn warm-shift; v7 gets a darkened interior (shadow depth)
        bright_shifts = [0, 20, 38, -16, 0, 20, 0, -16]
        speckled      = [False, False, False, False, True, True, True, True]
        _spots  = [(3,3),(9,11),(15,4),(21,8),(27,2),(5,19),(12,24),(19,17),(25,21),(7,28),(22,27),(14,14)]
        _bright = [(6,7),(18,5),(11,20),(24,15)]
        variants = {}
        for bid in ALL_LEAVES:
            bdata = BLOCKS.get(bid)
            if not bdata or not bdata.get("color"):
                continue
            base = bdata["color"]
            surfs = []
            for v in range(8):
                shift = bright_shifts[v]
                tone  = tuple(max(0, min(255, c + shift)) for c in base)
                # v6: autumn — warm shift (boost red, pull green/blue)
                if v == 6:
                    tone = (min(255, tone[0] + 28), max(0, tone[1] - 12), max(0, tone[2] - 18))
                dark  = _darken(tone, 28)
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                s.fill(tone)
                if speckled[v]:
                    spot_col   = _darken(tone, 40)
                    bright_col = tuple(min(255, c + 20) for c in tone)
                    for sx2, sy2 in _spots:
                        if sx2 + 3 <= BLOCK_SIZE and sy2 + 3 <= BLOCK_SIZE:
                            pygame.draw.rect(s, spot_col, (sx2, sy2, 3, 3))
                    for sx2, sy2 in _bright:
                        if sx2 + 2 <= BLOCK_SIZE and sy2 + 2 <= BLOCK_SIZE:
                            pygame.draw.rect(s, bright_col, (sx2, sy2, 2, 2))
                # v7: deep-shadow interior
                if v == 7:
                    inner = _darken(tone, 22)
                    pygame.draw.rect(s, inner, (2, 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs.append(s)
            variants[bid] = surfs
        return variants

    # ------------------------------------------------------------------
    # Camera
    # ------------------------------------------------------------------

    def update_camera(self, player, world):
        target_x = player.x - SCREEN_W // 2 + PLAYER_W // 2
        target_y = player.y - SCREEN_H // 2 + PLAYER_H // 2
        self.cam_x += (target_x - self.cam_x) * 0.12
        self.cam_y += (target_y - self.cam_y) * 0.12
        # Clamp only vertical bounds; horizontal is infinite
        max_cy = world.height * BLOCK_SIZE - SCREEN_H
        self.cam_y = max(0.0, min(self.cam_y, float(max_cy)))

    def _build_sky_surf(self):
        sky_top    = (55,  110, 210)
        sky_bottom = (130, 190, 250)
        surf = pygame.Surface((SCREEN_W, SCREEN_H)).convert()
        for y in range(SCREEN_H):
            t = y / (SCREEN_H - 1)
            r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * t)
            g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * t)
            b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_W - 1, y))
        return surf

    # ------------------------------------------------------------------
    # Draw world
    # ------------------------------------------------------------------

    def draw_world(self, world, player=None):
        # Sky gradient: deep blue at top, lighter cyan-blue at horizon
        self.screen.blit(self._sky_surf, (0, 0))

        cam_xi = int(self.cam_x)
        cam_yi = int(self.cam_y)

        bx0 = cam_xi // BLOCK_SIZE
        bx1 = (cam_xi + SCREEN_W) // BLOCK_SIZE + 2
        by0 = max(0, cam_yi // BLOCK_SIZE)
        by1 = min(world.height, (cam_yi + SCREEN_H) // BLOCK_SIZE + 2)

        if player is not None:
            px_blk = player.x / BLOCK_SIZE
            py_blk = player.y / BLOCK_SIZE
            detect  = player.rock_detect_range
            warm    = detect + ROCK_WARM_ZONE
        else:
            px_blk = py_blk = detect = warm = None

        # Precompute per-column values to avoid repeated calls inside the block loop
        surface_ys = {bx: world.surface_height(bx) for bx in range(bx0, bx1)}
        biomes = {bx: world.get_biome(bx) for bx in range(bx0, bx1)}

        for by in range(by0, by1):
            for bx in range(bx0, bx1):
                bid = world.get_block(bx, by)
                if bid == AIR:
                    sx = bx * BLOCK_SIZE - cam_xi
                    sy = by * BLOCK_SIZE - cam_yi
                    bg_bid = world.get_bg_block(bx, by)
                    if bg_bid != AIR:
                        bg_surf = self._bg_block_surfs.get(bg_bid)
                        if bg_surf:
                            self.screen.blit(bg_surf, (sx, sy))
                    elif by > surface_ys.get(bx, 100):
                        self.screen.blit(self._cave_wall_surf, (sx, sy))
                    continue
                if bid == WATER:
                    level = world._water_level.get((bx, by), 8)
                    wsurf = self._water_surfs[level - 1]
                    wh = wsurf.get_height()
                    self.screen.blit(wsurf, (bx * BLOCK_SIZE - cam_xi,
                                             by * BLOCK_SIZE - cam_yi + BLOCK_SIZE - wh))
                    continue
                if bid == TILLED_SOIL:
                    moisture = world._soil_moisture.get((bx, by), 0)
                    tsurf = self._tilled_soil_surfs[1 if moisture >= 4 else 0]
                    self.screen.blit(tsurf, (bx * BLOCK_SIZE - cam_xi, by * BLOCK_SIZE - cam_yi))
                    continue
                surf = self._block_surfs.get(bid)
                # Tree block variants — color + grain/size variation seeded by position
                if bid in ALL_LOGS:
                    var = self._log_variants.get(bid)
                    if var:
                        surf = var[(bx * 97 + world.seed) % len(var)]
                elif bid in ALL_LEAVES:
                    var = self._leaf_variants.get(bid)
                    if var:
                        surf = var[(bx * 97 + by * 31 + world.seed) % len(var)]
                biome = biomes[bx]
                biome_stone = self._biome_stone_surfs.get(biome)
                if bid == STONE and biome_stone:
                    surf = biome_stone
                dist = 0.0
                ore_visible = True
                if bid in RESOURCE_BLOCKS and px_blk is not None and not self.show_all_resources:
                    dist = ((bx - px_blk) ** 2 + (by - py_blk) ** 2) ** 0.5
                    underground = by > surface_ys.get(bx, 100)
                    ore_visible = (not underground) or (
                        dist <= warm and _los_clear(world, int(px_blk), int(py_blk), bx, by)
                    )
                    if not ore_visible or dist > warm:
                        surf = biome_stone or self._block_surfs.get(STONE)
                    elif dist > detect:
                        biome_hints = self._biome_resource_hint_surfs.get(biome, self._resource_hint_surfs)
                        surf = biome_hints.get(bid, self._resource_hint_surfs[bid])
                if surf:
                    sx = bx * BLOCK_SIZE - cam_xi
                    sy = by * BLOCK_SIZE - cam_yi
                    self.screen.blit(surf, (sx, sy))
                    if bid in _SHIMMER_BLOCKS and ore_visible and (px_blk is None or dist <= detect):
                        now = pygame.time.get_ticks()
                        sc = _SHIMMER_BLOCKS[bid]
                        h = bx * 1283 + by * 7919
                        for i in range(4):
                            phase = (h + i * 4999) % 65536
                            if ((now + phase) // 350) % 5 == 0:
                                spx = 1 + (h * (i + 3) * 43) % 28
                                spy = 1 + (h * (i + 3) * 97) % 28
                                pygame.draw.rect(self.screen, sc, (sx + spx, sy + spy, 2, 2))

    # ------------------------------------------------------------------
    # Draw player
    # ------------------------------------------------------------------

    def draw_player(self, player):
        px = int(player.x - self.cam_x)
        py = int(player.y - self.cam_y)
        head_h = 10
        body_h = PLAYER_H - head_h
        # Head
        pygame.draw.rect(self.screen, (255, 210, 160), (px + 2, py, PLAYER_W - 4, head_h))
        # Eye on facing side
        eye_x = (px + PLAYER_W - 6) if player.facing == 1 else (px + 2)
        pygame.draw.rect(self.screen, (30, 30, 30), (eye_x, py + 3, 3, 3))
        # Body
        pygame.draw.rect(self.screen, (70, 120, 190), (px, py + head_h, PLAYER_W, body_h))
        # Arm on facing side (pickaxe hand)
        arm_x = (px + PLAYER_W) if player.facing == 1 else (px - 3)
        pygame.draw.rect(self.screen, (255, 210, 160), (arm_x, py + head_h + 2, 3, 8))
        # Legs
        pygame.draw.rect(self.screen, (50, 80, 140), (px, py + head_h + body_h - 6, 8, 6))
        pygame.draw.rect(self.screen, (50, 80, 140), (px + PLAYER_W - 8, py + head_h + body_h - 6, 8, 6))

    # ------------------------------------------------------------------
    # Draw animals
    # ------------------------------------------------------------------

    def draw_entities(self, entities):
        for e in entities:
            if getattr(e, 'dead', False):
                continue
            sx = int(e.x - self.cam_x)
            sy = int(e.y - self.cam_y)
            if e.animal_id == "sheep":
                self._draw_sheep(sx, sy, e)
            elif e.animal_id == "cow":
                self._draw_cow(sx, sy, e)
            elif e.animal_id == "chicken":
                self._draw_chicken(sx, sy, e)
            elif e.animal_id == "snow_leopard":
                self._draw_snow_leopard(sx, sy, e)
            elif e.animal_id == "mountain_lion":
                self._draw_mountain_lion(sx, sy, e)
            elif e.animal_id == "horse":
                self._draw_horse(sx, sy, e)
            elif e.animal_id == "npc_quest":
                self._draw_npc_quest(sx, sy, e)
            elif e.animal_id == "npc_trade":
                self._draw_npc_trade(sx, sy, e)
            elif e.animal_id == "npc_herbalist":
                self._draw_npc_herbalist(sx, sy, e)
            elif e.animal_id == "npc_jeweler":
                self._draw_npc_jeweler(sx, sy, e)
            elif e.animal_id == "npc_merchant":
                self._draw_npc_merchant(sx, sy, e)
            elif e.animal_id == "npc_chef":
                self._draw_npc_chef(sx, sy, e)
            elif e.animal_id == "npc_monk":
                self._draw_npc_monk(sx, sy, e)

    @staticmethod
    def _fmt_fuel_time(fuel, fuel_rate):
        if fuel <= 0 or fuel_rate <= 0:
            return None
        secs = fuel / fuel_rate
        if secs >= 3600:
            return f"{int(secs // 3600)}h{int((secs % 3600) // 60):02d}m"
        if secs >= 60:
            return f"{int(secs // 60)}m"
        return f"{int(secs)}s"

    def draw_automations(self, automations):
        for a in automations:
            a.draw(self.screen, self.cam_x, self.cam_y)
            label = self._fmt_fuel_time(a.fuel, a._def["fuel_rate"])
            if label:
                sx = int(a.x - self.cam_x)
                sy = int(a.y - self.cam_y)
                txt = self._npc_font.render(label, True, (220, 160, 40))
                self.screen.blit(txt, (sx + a.W // 2 - txt.get_width() // 2, sy - 27))

    def draw_farm_bots(self, farm_bots):
        for fb in farm_bots:
            fb.draw(self.screen, self.cam_x, self.cam_y)
            label = self._fmt_fuel_time(fb.fuel, fb._def["fuel_rate"])
            if label:
                sx = int(fb.x - self.cam_x)
                sy = int(fb.y - self.cam_y)
                txt = self._npc_font.render(label, True, (220, 160, 40))
                self.screen.blit(txt, (sx + fb.W // 2 - txt.get_width() // 2, sy - 22))

    def draw_backhoes(self, backhoes, player):
        for bh in backhoes:
            self._draw_backhoe(bh, is_mounted=(player.mounted_machine is bh))

    def _draw_backhoe(self, bh, is_mounted=False):
        sx = int(bh.x - self.cam_x)
        sy = int(bh.y - self.cam_y)
        W, H = bh.W, bh.H

        BODY_COLOR = (210, 160, 30)
        BODY_DARK  = (130, 95, 15)
        CAB_COLOR  = (240, 200, 50)

        # Main body (lower 2/3)
        body_rect = (sx, sy + H // 3, W, H * 2 // 3)
        pygame.draw.rect(self.screen, BODY_COLOR, body_rect)
        pygame.draw.rect(self.screen, BODY_DARK, body_rect, 2)

        # Cab (upper-left portion)
        cab_rect = (sx + 2, sy, W // 2, H // 2 + 4)
        pygame.draw.rect(self.screen, CAB_COLOR, cab_rect)
        pygame.draw.rect(self.screen, BODY_DARK, cab_rect, 2)
        pygame.draw.rect(self.screen, (180, 230, 240), (sx + 5, sy + 3, W // 2 - 8, H // 3))

        # Wheels
        wheel_y = sy + H - 5
        for wx in (sx + 9, sx + W - 9):
            pygame.draw.circle(self.screen, (30, 30, 30), (wx, wheel_y), 6)
            pygame.draw.circle(self.screen, (80, 80, 80), (wx, wheel_y), 3)

        # Arm: line from body centre to arm-target block centre
        cbx, cby = bh.center_block()
        body_cx = int(cbx * BLOCK_SIZE - self.cam_x + BLOCK_SIZE // 2)
        body_cy = int(cby * BLOCK_SIZE - self.cam_y + BLOCK_SIZE // 2)
        tbx, tby = bh.arm_target_block()
        tip_x = int(tbx * BLOCK_SIZE - self.cam_x + BLOCK_SIZE // 2)
        tip_y = int(tby * BLOCK_SIZE - self.cam_y + BLOCK_SIZE // 2)
        pygame.draw.line(self.screen, BODY_DARK,  (body_cx, body_cy), (tip_x, tip_y), 4)
        pygame.draw.line(self.screen, BODY_COLOR, (body_cx, body_cy), (tip_x, tip_y), 2)
        # Bucket end
        pygame.draw.rect(self.screen, (60, 50, 20), (tip_x - 4, tip_y - 4, 8, 8))
        pygame.draw.rect(self.screen, BODY_DARK, (tip_x - 4, tip_y - 4, 8, 8), 1)

        # Target block highlight
        hx = tbx * BLOCK_SIZE - int(self.cam_x)
        hy = tby * BLOCK_SIZE - int(self.cam_y)
        if is_mounted:
            pygame.draw.rect(self.screen, (255, 200, 0), (hx, hy, BLOCK_SIZE, BLOCK_SIZE), 3)
        else:
            pygame.draw.rect(self.screen, (160, 120, 0), (hx, hy, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Mining progress bar below target block
        prog = bh.mine_progress
        if prog > 0:
            pygame.draw.rect(self.screen, (30, 30, 30), (hx, hy + BLOCK_SIZE + 1, BLOCK_SIZE, 3))
            pygame.draw.rect(self.screen, (80, 200, 80),
                             (hx, hy + BLOCK_SIZE + 1, int(BLOCK_SIZE * prog), 3))

        # Fuel bar above body
        frac = bh.fuel / bh.FUEL_TANK if bh.FUEL_TANK > 0 else 0
        pygame.draw.rect(self.screen, (30, 30, 30), (sx, sy - 6, W, 4))
        pygame.draw.rect(self.screen, (200, 140, 30), (sx, sy - 6, int(W * frac), 4))

        # Mounted hint
        if is_mounted:
            hint = self._npc_font.render("[E] Dismount", True, (255, 220, 100))
            self.screen.blit(hint, (sx + W // 2 - hint.get_width() // 2, sy - 22))

    def _draw_npc_quest(self, sx, sy, npc):
        bob = int(npc._bob_offset)
        # Body
        pygame.draw.rect(self.screen, (190, 140, 70), (sx, sy + bob, 20, 18))
        # Head
        pygame.draw.rect(self.screen, (255, 215, 160), (sx + 2, sy - 10 + bob, 16, 12))
        # Eyes
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 4, sy - 7 + bob, 3, 3))
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
        # Exclamation marker above head
        txt = self._npc_font.render("!", True, (255, 220, 30))
        self.screen.blit(txt, (sx + 7, sy - 24 + bob))

    def _draw_npc_trade(self, sx, sy, npc):
        bob = int(npc._bob_offset)
        # Body
        pygame.draw.rect(self.screen, (60, 120, 175), (sx, sy + bob, 20, 18))
        # Head
        pygame.draw.rect(self.screen, (255, 215, 160), (sx + 2, sy - 10 + bob, 16, 12))
        # Eyes
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 4, sy - 7 + bob, 3, 3))
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
        # Dollar marker above head
        txt = self._npc_font.render("$", True, (80, 230, 120))
        self.screen.blit(txt, (sx + 6, sy - 24 + bob))

    def _draw_npc_herbalist(self, sx, sy, npc):
        bob = int(npc._bob_offset)
        # Body — earthy green tunic
        pygame.draw.rect(self.screen, (60, 140, 70), (sx, sy + bob, 20, 18))
        # Belt
        pygame.draw.rect(self.screen, (90, 55, 20), (sx, sy + 11 + bob, 20, 3))
        # Head
        pygame.draw.rect(self.screen, (255, 215, 160), (sx + 2, sy - 10 + bob, 16, 12))
        # Eyes
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 4, sy - 7 + bob, 3, 3))
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
        # Flower indicator above head (4 petals + centre)
        fx, fy = sx + 10, sy - 22 + bob
        for dx, dy in ((0, -4), (0, 4), (-4, 0), (4, 0)):
            pygame.draw.circle(self.screen, (100, 220, 100), (fx + dx, fy + dy), 2)
        pygame.draw.circle(self.screen, (255, 230, 50), (fx, fy), 2)

    def _draw_npc_jeweler(self, sx, sy, npc):
        bob = int(npc._bob_offset)
        # Body — deep purple coat
        pygame.draw.rect(self.screen, (110, 50, 160), (sx, sy + bob, 20, 18))
        # Coat trim
        pygame.draw.rect(self.screen, (160, 90, 210), (sx + 8, sy + bob, 4, 18))
        # Head
        pygame.draw.rect(self.screen, (255, 215, 160), (sx + 2, sy - 10 + bob, 16, 12))
        # Eyes
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 4, sy - 7 + bob, 3, 3))
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
        # Diamond indicator above head
        gx, gy = sx + 10, sy - 22 + bob
        pygame.draw.polygon(self.screen, (190, 110, 255),
                            [(gx, gy - 5), (gx + 4, gy), (gx, gy + 5), (gx - 4, gy)])
        pygame.draw.polygon(self.screen, (230, 180, 255),
                            [(gx, gy - 5), (gx + 4, gy), (gx, gy + 5), (gx - 4, gy)], 1)

    def _draw_npc_merchant(self, sx, sy, npc):
        bob = int(npc._bob_offset)
        # Body — dark brown merchant coat
        pygame.draw.rect(self.screen, (90, 55, 25), (sx, sy + bob, 20, 18))
        # Coat lapel stripe
        pygame.draw.rect(self.screen, (120, 75, 35), (sx + 8, sy + bob, 4, 12))
        # Head
        pygame.draw.rect(self.screen, (255, 215, 160), (sx + 2, sy - 10 + bob, 16, 12))
        # Eyes
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 4, sy - 7 + bob, 3, 3))
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
        # Gold coin above head
        gx, gy = sx + 10, sy - 21 + bob
        pygame.draw.circle(self.screen, (220, 175, 40), (gx, gy), 5)
        pygame.draw.circle(self.screen, (180, 140, 20), (gx, gy), 5, 1)

    def _draw_npc_chef(self, sx, sy, npc):
        bob = int(npc._bob_offset)
        # Body — white apron over dark tunic
        pygame.draw.rect(self.screen, (70, 55, 45), (sx, sy + bob, 20, 18))
        pygame.draw.rect(self.screen, (240, 235, 220), (sx + 5, sy + bob, 10, 18))
        # Chef's hat (tall white rectangle above head)
        pygame.draw.rect(self.screen, (245, 242, 235), (sx + 4, sy - 18 + bob, 12, 10))
        pygame.draw.rect(self.screen, (200, 195, 185), (sx + 4, sy - 18 + bob, 12, 2))
        # Head
        pygame.draw.rect(self.screen, (255, 215, 160), (sx + 2, sy - 10 + bob, 16, 12))
        # Eyes
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 4, sy - 7 + bob, 3, 3))
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
        # Tilde food indicator above hat
        txt = self._npc_font.render("~", True, (240, 120, 30))
        self.screen.blit(txt, (sx + 6, sy - 28 + bob))

    def _draw_npc_monk(self, sx, sy, npc):
        bob = int(npc._bob_offset)
        # Body — saffron robe
        pygame.draw.rect(self.screen, (210, 130, 40), (sx, sy + bob, 20, 18))
        # Robe inner fold
        pygame.draw.rect(self.screen, (175, 100, 25), (sx + 8, sy + bob, 5, 18))
        # Head — slightly different skin tone (warmer)
        pygame.draw.rect(self.screen, (240, 200, 150), (sx + 2, sy - 10 + bob, 16, 12))
        # Eyes
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 4, sy - 7 + bob, 3, 3))
        pygame.draw.rect(self.screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
        # 4-pointed star above head
        gx, gy = sx + 10, sy - 22 + bob
        for dx, dy in ((0, -5), (0, 5), (-5, 0), (5, 0)):
            pygame.draw.line(self.screen, (240, 220, 100), (gx, gy), (gx + dx, gy + dy), 2)
        pygame.draw.circle(self.screen, (255, 240, 130), (gx, gy), 2)

    def _draw_sheep(self, sx, sy, sheep):
        W, H = sheep.W, sheep.H
        traits = getattr(sheep, 'traits', {})
        shift = traits.get("color_shift", (0, 0, 0))
        s = traits.get("size", 1.0)
        body_h = H - int(8 * s)
        leg_y = sy + body_h

        # Legs
        for lx_off in [2, 7, 14, 19]:
            pygame.draw.rect(self.screen, (80, 60, 40),
                             (sx + int(lx_off * s), leg_y, max(1, int(3 * s)), int(8 * s)))

        # Body
        body_color = _tinted((220, 220, 220) if sheep.has_wool else (175, 140, 95), shift)
        pygame.draw.rect(self.screen, body_color, (sx, sy, W, body_h))

        # Head
        head_w, head_h = int(9 * s), int(9 * s)
        head_color = _tinted((200, 200, 200) if sheep.has_wool else (155, 125, 85), shift)
        hx = (sx + W - int(2 * s)) if sheep.facing == 1 else (sx - head_w + int(2 * s))
        hy = sy - max(1, int(1 * s))
        pygame.draw.rect(self.screen, head_color, (hx, hy, head_w, head_h))
        eye_x = (hx + head_w - int(3 * s)) if sheep.facing == 1 else (hx + max(1, int(1 * s)))
        pygame.draw.rect(self.screen, (30, 30, 30), (eye_x, hy + int(3 * s), 2, 2))

        # Tame indicator
        if getattr(sheep, 'tamed', False):
            pygame.draw.circle(self.screen, (255, 80, 120), (sx + W // 2, sy - 10), 4)

        # Attack / harvest progress bar
        if sheep.being_harvested:
            if sheep._kill_timer > 0:
                progress = sheep._kill_timer / 0.5
                pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 7, W, 4))
                pygame.draw.rect(self.screen, (220, 60, 60), (sx, sy - 7, int(W * progress), 4))
            elif sheep._harvest_time > 0:
                progress = sheep._harvest_time / sheep.HARVEST_TIME
                pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 7, W, 4))
                pygame.draw.rect(self.screen, (100, 220, 100), (sx, sy - 7, int(W * progress), 4))

        # Health bar when damaged
        if sheep.health < 3:
            pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 13, W, 3))
            pygame.draw.rect(self.screen, (220, 50, 50), (sx, sy - 13, int(W * sheep.health / 3), 3))

    def _draw_cow(self, sx, sy, cow):
        W, H = cow.W, cow.H
        traits = getattr(cow, 'traits', {})
        shift = traits.get("color_shift", (0, 0, 0))
        s = traits.get("size", 1.0)
        body_h = H - int(8 * s)
        leg_y = sy + body_h

        # Legs
        for lx_off in [2, 8, 18, 24]:
            pygame.draw.rect(self.screen, (60, 40, 30),
                             (sx + int(lx_off * s), leg_y, max(1, int(4 * s)), int(8 * s)))

        # Body (brown base + black patches)
        body_color = _tinted((140, 85, 45), shift)
        pygame.draw.rect(self.screen, body_color, (sx, sy, W, body_h))
        pygame.draw.rect(self.screen, (30, 20, 10),
                         (sx + int(8 * s), sy + int(2 * s), int(10 * s), int(5 * s)))
        pygame.draw.rect(self.screen, (30, 20, 10),
                         (sx + int(20 * s), sy + int(5 * s), int(6 * s), int(4 * s)))

        # Head
        head_w, head_h = int(11 * s), int(11 * s)
        hx = (sx + W - int(3 * s)) if cow.facing == 1 else (sx - head_w + int(3 * s))
        hy = sy - int(2 * s)
        head_color = _tinted((140, 85, 45), shift)
        pygame.draw.rect(self.screen, head_color, (hx, hy, head_w, head_h))
        snout_x = (hx + head_w - int(4 * s)) if cow.facing == 1 else hx
        pygame.draw.rect(self.screen, _tinted((190, 130, 100), shift),
                         (snout_x, hy + int(6 * s), int(4 * s), int(4 * s)))
        eye_x = (hx + head_w - int(4 * s)) if cow.facing == 1 else (hx + max(1, int(1 * s)))
        pygame.draw.rect(self.screen, (20, 10, 5), (eye_x, hy + int(2 * s), 2, 2))

        # Udder indicator when has milk
        if cow.has_milk:
            udder_x = sx + W // 2 - int(4 * s)
            pygame.draw.rect(self.screen, (220, 180, 180),
                             (udder_x, leg_y - int(3 * s), int(8 * s), int(3 * s)))

        # Tame indicator
        if getattr(cow, 'tamed', False):
            pygame.draw.circle(self.screen, (255, 80, 120), (sx + W // 2, sy - 10), 4)

        # Attack / harvest progress bar
        if cow.being_harvested:
            if cow._kill_timer > 0:
                progress = cow._kill_timer / 0.5
                pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 7, W, 4))
                pygame.draw.rect(self.screen, (220, 60, 60), (sx, sy - 7, int(W * progress), 4))
            elif cow._harvest_time > 0:
                progress = cow._harvest_time / cow.HARVEST_TIME
                pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 7, W, 4))
                pygame.draw.rect(self.screen, (80, 160, 220), (sx, sy - 7, int(W * progress), 4))

        # Health bar when damaged
        if cow.health < 3:
            pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 13, W, 3))
            pygame.draw.rect(self.screen, (220, 50, 50), (sx, sy - 13, int(W * cow.health / 3), 3))

    def _draw_chicken(self, sx, sy, chicken):
        W, H = chicken.W, chicken.H
        traits = getattr(chicken, 'traits', {})
        shift = traits.get("color_shift", (0, 0, 0))
        s = traits.get("size", 1.0)

        # Legs
        for lx_off in [4, 11]:
            pygame.draw.rect(self.screen, (220, 160, 30),
                             (sx + int(lx_off * s), sy + H - int(6 * s), max(1, int(2 * s)), int(6 * s)))

        # Body (cream oval)
        body_color = _tinted((235, 235, 210), shift)
        pygame.draw.ellipse(self.screen, body_color,
                            (sx + max(1, int(1 * s)), sy + int(2 * s), W - int(4 * s), H - int(8 * s)))

        # Head
        head_w, head_h = int(8 * s), int(8 * s)
        hx = (sx + W - int(4 * s)) if chicken.facing == 1 else (sx - head_w + int(4 * s))
        hy = sy - int(2 * s)
        pygame.draw.ellipse(self.screen, body_color, (hx, hy, head_w, head_h))
        beak_x = (hx + head_w - max(1, int(1 * s))) if chicken.facing == 1 else (hx - int(3 * s))
        pygame.draw.rect(self.screen, (220, 160, 30),
                         (beak_x, hy + int(3 * s), int(3 * s), int(2 * s)))
        eye_x = (hx + head_w - int(3 * s)) if chicken.facing == 1 else (hx + max(1, int(1 * s)))
        pygame.draw.rect(self.screen, (20, 20, 20), (eye_x, hy + int(2 * s), 2, 2))
        pygame.draw.rect(self.screen, (220, 50, 50),
                         (hx + int(2 * s), hy - int(2 * s), int(4 * s), int(3 * s)))

        # Egg indicator
        if chicken.has_egg:
            pygame.draw.ellipse(self.screen, (245, 235, 200),
                                (sx + W // 2 - int(3 * s), sy + H - int(10 * s), int(6 * s), int(5 * s)))

        # Tame indicator
        if getattr(chicken, 'tamed', False):
            pygame.draw.circle(self.screen, (255, 80, 120), (sx + W // 2, sy - 10), 4)

        # Attack / harvest progress bar
        if chicken.being_harvested:
            if chicken._kill_timer > 0:
                progress = chicken._kill_timer / 0.5
                pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 7, W, 4))
                pygame.draw.rect(self.screen, (220, 60, 60), (sx, sy - 7, int(W * progress), 4))
            elif chicken._harvest_time > 0:
                progress = chicken._harvest_time / chicken.HARVEST_TIME
                pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 7, W, 4))
                pygame.draw.rect(self.screen, (245, 220, 100), (sx, sy - 7, int(W * progress), 4))

        # Health bar when damaged
        if chicken.health < 3:
            pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 13, W, 3))
            pygame.draw.rect(self.screen, (220, 50, 50),
                             (sx, sy - 13, int(W * chicken.health / 3), 3))

    def _draw_horse(self, sx, sy, horse):
        W, H = horse.W, horse.H
        traits    = getattr(horse, 'traits', {})
        s         = traits.get("size", 1.0)
        shift     = traits.get("color_shift", (0, 0, 0))
        coat      = traits.get("coat_color", (160, 115, 65))
        body_color = _tinted(coat, shift)
        dark_coat  = tuple(max(0, c - 40) for c in body_color)
        mane_color = tuple(max(0, c - 60) for c in body_color)

        body_h = int(H * 0.65)
        leg_h  = H - body_h
        leg_y  = sy + body_h

        # Legs (4 legs)
        leg_w = max(1, int(4 * s))
        for lx_off in [3, 9, 22, 28]:
            pygame.draw.rect(self.screen, dark_coat,
                             (sx + int(lx_off * s), leg_y, leg_w, leg_h))
        # Hooves
        hoof_c = (30, 25, 20)
        for lx_off in [3, 9, 22, 28]:
            pygame.draw.rect(self.screen, hoof_c,
                             (sx + int(lx_off * s), leg_y + leg_h - 2, leg_w, 2))

        # Body
        pygame.draw.rect(self.screen, body_color, (sx, sy, W, body_h))

        # Mane stripe along top
        pygame.draw.rect(self.screen, mane_color,
                         (sx + int(4 * s), sy, int((W - 8) * s), max(2, int(4 * s))))

        # Tail
        tail_x = sx if horse.facing == 1 else sx + W - int(5 * s)
        pygame.draw.rect(self.screen, mane_color,
                         (tail_x, sy + int(4 * s), max(2, int(4 * s)), int(body_h * 0.6)))

        # Head
        head_w = int(12 * s)
        head_h = int(12 * s)
        hx = (sx + W - int(2 * s)) if horse.facing == 1 else (sx - head_w + int(2 * s))
        hy = sy - int(4 * s)
        pygame.draw.rect(self.screen, body_color, (hx, hy, head_w, head_h))

        # Muzzle
        muzzle_w = int(5 * s)
        muzzle_x = (hx + head_w - muzzle_w) if horse.facing == 1 else hx
        pygame.draw.rect(self.screen, _tinted((200, 175, 145), shift),
                         (muzzle_x, hy + int(6 * s), muzzle_w, int(5 * s)))

        # Eye
        eye_x = (hx + head_w - int(5 * s)) if horse.facing == 1 else (hx + max(1, int(2 * s)))
        pygame.draw.rect(self.screen, (15, 10, 5), (eye_x, hy + int(3 * s), 2, 2))

        # Ear
        ear_x = (hx + int(2 * s)) if horse.facing == 1 else (hx + head_w - int(4 * s))
        pygame.draw.rect(self.screen, dark_coat, (ear_x, hy - int(4 * s), max(2, int(3 * s)), int(4 * s)))

        # Saddle indicator (brown patch on back when tamed and broken)
        if getattr(horse, 'tamed', False) and getattr(horse, '_broken', False):
            saddle_x = sx + int(W * 0.3)
            saddle_w = int(W * 0.4)
            pygame.draw.rect(self.screen, (110, 65, 25),
                             (saddle_x, sy, saddle_w, max(2, int(5 * s))))

        # Tame heart indicator (pink dot above)
        if getattr(horse, 'tamed', False) and not getattr(horse, '_broken', False):
            pygame.draw.circle(self.screen, (255, 80, 120), (sx + W // 2, sy - 10), 4)
        elif getattr(horse, 'tamed', False):
            pygame.draw.circle(self.screen, (80, 180, 255), (sx + W // 2, sy - 10), 4)

        # Temperament color pip (top-left corner)
        temp = traits.get("temperament", "spirited")
        temp_colors = {"calm": (80, 200, 80), "spirited": (220, 180, 40), "wild": (220, 60, 60)}
        pygame.draw.circle(self.screen, temp_colors.get(temp, (180, 180, 180)),
                           (sx + 4, sy - 6), 3)

    def _draw_snow_leopard(self, sx, sy, cat):
        W, H = cat.W, cat.H
        s = cat.traits.get("size", 1.0)
        shift = cat.traits.get("color_shift", (0, 0, 0))
        body_h = int(12 * s)
        leg_h = H - body_h
        leg_y = sy + body_h

        fur    = _tinted((215, 215, 222), shift)
        spot   = _tinted((68, 68, 82),    shift)
        leg_c  = _tinted((195, 195, 205), shift)
        eye_c  = (95, 165, 130)

        # Tail — extends behind the body
        tail_seg1_len = int(11 * s)
        tail_seg2_len = int(7 * s)
        tail_w = max(2, int(3 * s))
        tail_y1 = sy + int(5 * s)
        tail_y2 = sy + int(2 * s)
        if cat.facing == 1:
            pygame.draw.rect(self.screen, fur, (sx - tail_seg1_len, tail_y1, tail_seg1_len, tail_w))
            pygame.draw.rect(self.screen, spot, (sx - int(4 * s), tail_y1, max(1, int(2 * s)), tail_w))
            pygame.draw.rect(self.screen, fur, (sx - tail_seg1_len - tail_seg2_len, tail_y2, tail_seg2_len, tail_w))
        else:
            tx = sx + W
            pygame.draw.rect(self.screen, fur, (tx, tail_y1, tail_seg1_len, tail_w))
            pygame.draw.rect(self.screen, spot, (tx + int(7 * s), tail_y1, max(1, int(2 * s)), tail_w))
            pygame.draw.rect(self.screen, fur, (tx + tail_seg1_len, tail_y2, tail_seg2_len, tail_w))

        # Legs
        for lx_off in [int(4 * s), int(10 * s), int(22 * s), int(28 * s)]:
            pygame.draw.rect(self.screen, leg_c, (sx + lx_off, leg_y, max(1, int(3 * s)), leg_h))

        # Body
        pygame.draw.rect(self.screen, fur, (sx, sy, W, body_h))

        # Spots (3 rosette clusters)
        for bx_off, by_off in [(int(5 * s), int(2 * s)), (int(14 * s), int(6 * s)), (int(23 * s), int(2 * s))]:
            pygame.draw.rect(self.screen, spot, (sx + bx_off, sy + by_off, max(2, int(4 * s)), max(2, int(3 * s))))
            pygame.draw.rect(self.screen, spot, (sx + bx_off + max(1, int(2 * s)), sy + by_off - max(1, int(1 * s)), max(1, int(2 * s)), max(1, int(2 * s))))

        # Head
        head_w, head_h = int(10 * s), int(12 * s)
        hx = (sx + W - max(1, int(2 * s))) if cat.facing == 1 else (sx - head_w + max(1, int(2 * s)))
        hy = sy - max(1, int(2 * s))
        pygame.draw.rect(self.screen, fur, (hx, hy, head_w, head_h))

        # Ears
        ear_w, ear_h = max(2, int(3 * s)), max(2, int(4 * s))
        pygame.draw.rect(self.screen, leg_c, (hx + max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))
        pygame.draw.rect(self.screen, leg_c, (hx + head_w - ear_w - max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))

        # Eye
        eye_x = (hx + head_w - max(2, int(4 * s))) if cat.facing == 1 else (hx + max(1, int(2 * s)))
        pygame.draw.rect(self.screen, eye_c, (eye_x, hy + max(2, int(4 * s)), 2, 2))

    def _draw_mountain_lion(self, sx, sy, cat):
        W, H = cat.W, cat.H
        s = cat.traits.get("size", 1.0)
        shift = cat.traits.get("color_shift", (0, 0, 0))
        body_h = int(14 * s)
        leg_h = H - body_h
        leg_y = sy + body_h

        fur      = _tinted((188, 148, 78),  shift)
        belly    = _tinted((218, 192, 138), shift)
        tail_tip = _tinted((65,  50,  25),  shift)
        leg_c    = _tinted((170, 135, 70),  shift)
        eye_c    = (200, 155, 40)

        # Tail
        tail_seg1_len = int(12 * s)
        tail_seg2_len = int(7 * s)
        tail_w = max(2, int(3 * s))
        tail_y1 = sy + int(5 * s)
        tail_y2 = sy + int(3 * s)
        if cat.facing == 1:
            pygame.draw.rect(self.screen, fur, (sx - tail_seg1_len, tail_y1, tail_seg1_len, tail_w))
            pygame.draw.rect(self.screen, tail_tip, (sx - tail_seg1_len - tail_seg2_len, tail_y2, tail_seg2_len, tail_w))
        else:
            tx = sx + W
            pygame.draw.rect(self.screen, fur, (tx, tail_y1, tail_seg1_len, tail_w))
            pygame.draw.rect(self.screen, tail_tip, (tx + tail_seg1_len, tail_y2, tail_seg2_len, tail_w))

        # Legs
        for lx_off in [int(4 * s), int(11 * s), int(24 * s), int(31 * s)]:
            pygame.draw.rect(self.screen, leg_c, (sx + lx_off, leg_y, max(1, int(3 * s)), leg_h))

        # Body
        pygame.draw.rect(self.screen, fur, (sx, sy, W, body_h))
        # Lighter belly stripe
        belly_w = int(18 * s)
        pygame.draw.rect(self.screen, belly,
                         (sx + (W - belly_w) // 2, sy + int(6 * s), belly_w, int(5 * s)))

        # Head
        head_w, head_h = int(11 * s), int(13 * s)
        hx = (sx + W - max(1, int(3 * s))) if cat.facing == 1 else (sx - head_w + max(1, int(3 * s)))
        hy = sy - max(1, int(3 * s))
        pygame.draw.rect(self.screen, fur, (hx, hy, head_w, head_h))

        # Muzzle
        muzzle_w, muzzle_h = max(2, int(5 * s)), max(2, int(4 * s))
        muzzle_x = (hx + head_w - muzzle_w) if cat.facing == 1 else hx
        pygame.draw.rect(self.screen, belly, (muzzle_x, hy + int(7 * s), muzzle_w, muzzle_h))

        # Ears
        ear_w, ear_h = max(2, int(3 * s)), max(2, int(4 * s))
        pygame.draw.rect(self.screen, leg_c, (hx + max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))
        pygame.draw.rect(self.screen, leg_c, (hx + head_w - ear_w - max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))

        # Eye
        eye_x = (hx + head_w - max(2, int(4 * s))) if cat.facing == 1 else (hx + max(1, int(2 * s)))
        pygame.draw.rect(self.screen, eye_c, (eye_x, hy + max(2, int(4 * s)), 2, 2))

    # ------------------------------------------------------------------
    # Mining highlight
    # ------------------------------------------------------------------

    def draw_mining_indicator(self, player):
        if not player.mining_block or player.mine_progress <= 0:
            return
        bx, by = player.mining_block
        sx = bx * BLOCK_SIZE - int(self.cam_x)
        sy = by * BLOCK_SIZE - int(self.cam_y)
        # Dark crack overlay
        alpha = int(200 * player.mine_progress)
        self._mine_overlay.fill((0, 0, 0, alpha))
        self.screen.blit(self._mine_overlay, (sx, sy))
        # White border
        pygame.draw.rect(self.screen, (255, 255, 255), (sx, sy, BLOCK_SIZE, BLOCK_SIZE), 2)

    # ------------------------------------------------------------------
    # Placement ghost
    # ------------------------------------------------------------------

    def draw_place_indicator(self, player):
        if not player.place_target:
            return
        _, block_id = player._selected_place_block()
        if block_id is None:
            return
        bx, by = player.place_target
        sx = bx * BLOCK_SIZE - int(self.cam_x)
        sy = by * BLOCK_SIZE - int(self.cam_y)
        from blocks import BLOCKS
        color = BLOCKS.get(block_id, {}).get("color")
        bg_mode = getattr(player, 'bg_place_mode', False)
        if bg_mode:
            ghost_color = (max(0, color[0] - 30), max(0, color[1] - 10), min(255, color[2] + 60)) if color else (60, 80, 180)
            key = ("bg", ghost_color)
            if self._ghost_color_key != key:
                self._ghost_color_key = key
                self._ghost_surf.fill((0, 0, 0, 0))
                self._ghost_surf.fill((*ghost_color, 100))
            self.screen.blit(self._ghost_surf, (sx, sy))
            pygame.draw.rect(self.screen, (100, 160, 255), (sx, sy, BLOCK_SIZE, BLOCK_SIZE), 2)
        else:
            if color:
                if self._ghost_color_key != color:
                    self._ghost_color_key = color
                    self._ghost_surf.fill((0, 0, 0, 0))
                    self._ghost_surf.fill((*color, 120))
                self.screen.blit(self._ghost_surf, (sx, sy))
            pygame.draw.rect(self.screen, (255, 255, 255), (sx, sy, BLOCK_SIZE, BLOCK_SIZE), 2)

    # ------------------------------------------------------------------
    # Floating harvest text
    # ------------------------------------------------------------------

    def add_float_text(self, world_x, world_y, text, color):
        self._floating_texts.append({
            "x": float(world_x), "y": float(world_y),
            "text": text, "color": color, "life": 2.0, "vy": -40.0,
        })

    def tick_float_texts(self, dt):
        for ft in self._floating_texts:
            ft["y"] += ft["vy"] * dt
            ft["life"] -= dt
        self._floating_texts = [ft for ft in self._floating_texts if ft["life"] > 0]

    def draw_float_texts(self):
        for ft in self._floating_texts:
            sx = int(ft["x"] - self.cam_x)
            sy = int(ft["y"] - self.cam_y)
            alpha = min(255, int(255 * ft["life"]))
            surf = self._npc_font.render(ft["text"], True, ft["color"])
            surf.set_alpha(alpha)
            self.screen.blit(surf, (sx - surf.get_width() // 2, sy))

    # ------------------------------------------------------------------
    # Farm sense: readiness indicator on targeted crop blocks
    # ------------------------------------------------------------------

    def draw_farm_sense(self, player, world):
        tb = player.target_block
        if tb is None:
            return
        bx, by = tb
        block_id = world.get_block(bx, by)
        sx = bx * BLOCK_SIZE - int(self.cam_x)
        sy = by * BLOCK_SIZE - int(self.cam_y)
        if block_id in MATURE_CROP_BLOCKS:
            pygame.draw.rect(self.screen, (255, 210, 0), (sx - 1, sy - 1, BLOCK_SIZE + 2, BLOCK_SIZE + 2), 3)
            label = self._npc_font.render("Ready!", True, (255, 210, 0))
            self.screen.blit(label, (sx, sy - label.get_height() - 2))
            return
        if block_id in YOUNG_CROP_BLOCKS:
            pygame.draw.rect(self.screen, (140, 140, 140), (sx - 1, sy - 1, BLOCK_SIZE + 2, BLOCK_SIZE + 2), 2)
            moisture  = world._soil_moisture.get((bx, by + 1), 0)
            fertility = world._soil_fertility.get((bx, by + 1), world.max_fertility)
            progress  = world._crop_progress.get((bx, by), 0)
            text = f"M:{moisture}/{_soil.MAX_MOISTURE}  F:{fertility}/{world.max_fertility}  {progress}%"
            label = self._npc_font.render(text, True, (210, 210, 120))
            self.screen.blit(label, (sx, sy - label.get_height() - 2))
            return
        if block_id == TILLED_SOIL:
            moisture  = world._soil_moisture.get((bx, by), 0)
            fertility = world._soil_fertility.get((bx, by), world.max_fertility)
            m_color = (120, 180, 220) if moisture >= 4 else (200, 170, 110)
            f_color = (100, 180, 80) if fertility >= world.max_fertility // 2 else (200, 130, 60)
            pygame.draw.rect(self.screen, m_color, (sx - 1, sy - 1, BLOCK_SIZE + 2, BLOCK_SIZE + 2), 2)
            label = self._npc_font.render(
                f"M:{moisture}/{_soil.MAX_MOISTURE}  F:{fertility}/{world.max_fertility}",
                True, m_color)
            self.screen.blit(label, (sx, sy - label.get_height() - 2))

    # ------------------------------------------------------------------
    # Water submersion overlay
    # ------------------------------------------------------------------

    def draw_water_overlay(self, player):
        if player._head_in_water():
            self.screen.blit(self._water_overlay_surf, (0, 0))

    def draw_rain(self, world):
        """Draw downward rain streaks when a rain event is active."""
        if not world._rain_active:
            return
        from constants import SCREEN_W, SCREEN_H
        streak_color = (160, 190, 230, 90)
        surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        cx_off = int(self.cam_x) % 18
        # Time-based Y offset so streaks fall even when the camera is stationary.
        time_off = (pygame.time.get_ticks() // 25) % SCREEN_H
        for sx in range(-cx_off, SCREEN_W, 18):
            seed_val = (sx + int(self.cam_x) // 18) & 0xFFFF
            start_y  = (seed_val * 137 % SCREEN_H + time_off) % SCREEN_H
            length   = 8 + (seed_val * 53 % 12)
            pygame.draw.line(surf, streak_color, (sx, start_y), (sx - 2, start_y + length), 1)
        self.screen.blit(surf, (0, 0))

    # ------------------------------------------------------------------
    # Lighting
    # ------------------------------------------------------------------

    def draw_lighting(self, player, depth):
        if depth <= 0:
            return

        # ambient brightness: 230 at surface, drops to 10 at depth 110+
        ambient = max(10, 230 - depth * 2)
        radius = max(70, 220 - depth)
        darkness = 255 - ambient

        # Rebuild gradient only when lighting params change (not every frame)
        if self._light_cache_key != (ambient, radius):
            self._light_cache_key = (ambient, radius)
            size = radius * 2 + 1
            # Gradient is an SRCALPHA surface: alpha=0 at center (fully bright),
            # alpha=darkness at edge. BLEND_RGBA_MIN punches this as a hole into
            # the dark overlay, avoiding a full-screen BLEND_MULT each frame.
            grad = pygame.Surface((size, size), pygame.SRCALPHA)
            grad.fill((0, 0, 0, darkness))
            step = 5
            for r in range(radius, 0, -step):
                ratio = r / radius
                brightness = int(ambient + (255 - ambient) * (1 - ratio ** 0.6))
                alpha = 255 - min(255, brightness)
                pygame.draw.circle(grad, (0, 0, 0, alpha), (radius, radius), r)
            self._light_gradient = grad

        px = int(player.x - self.cam_x) + PLAYER_W // 2
        py = int(player.y - self.cam_y) + PLAYER_H // 2

        self._light_surf.fill((0, 0, 0, darkness))
        self._light_surf.blit(self._light_gradient, (px - radius, py - radius),
                              special_flags=pygame.BLEND_RGBA_MIN)
        self.screen.blit(self._light_surf, (0, 0))

    # ------------------------------------------------------------------
    # Mini-map
    # ------------------------------------------------------------------

    def _build_mm_color_table(self):
        from blocks import (GRASS, DIRT, OBSIDIAN, BEDROCK, GATE_MID, GATE_DEEP, GATE_CORE,
                            HOUSE_WALL, HOUSE_ROOF,
                            HOUSE_WALL_STONE, HOUSE_ROOF_STONE,
                            HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK,
                            HOUSE_WALL_DARK, HOUSE_ROOF_DARK,
                            RESTAURANT_WALL, RESTAURANT_AWNING,
                            POLISHED_GRANITE, POLISHED_MARBLE, SLATE_TILE,
                            TERRACOTTA_BLOCK, MOSSY_BRICK, CREAM_BRICK,
                            CHARCOAL_PLANK, WALNUT_PLANK, OAK_PANEL, BAMBOO_PANEL,
                            OBSIDIAN_TILE, COBBLESTONE, LAPIS_BRICK, BASALT_COLUMN,
                            LIMESTONE_BLOCK, COPPER_TILE, TEAK_PLANK,
                            DRIFTWOOD_PLANK, CEDAR_PANEL, JADE_PANEL,
                            ROSE_QUARTZ_BLOCK, GILDED_BRICK, AMETHYST_BLOCK,
                            AMBER_TILE, IVORY_BRICK, EBONY_PLANK,
                            MAHOGANY_PLANK, ASH_PLANK, FROSTED_GLASS, CRIMSON_BRICK,
                            TERRACOTTA_SHINGLE, THATCH_ROOF, VERDIGRIS_COPPER,
                            SILVER_PANEL, GOLD_LEAF_TRIM,
                            STAINED_GLASS_RED, STAINED_GLASS_BLUE, STAINED_GLASS_GREEN,
                            QUARTZ_PILLAR, ONYX_INLAY,
                            WHITE_PLASTER_WALL, CARVED_PLASTER, MUQARNAS_BLOCK,
                            MASHRABIYA, ZELLIGE_TILE, ARABESQUE_PANEL,
                            ADOBE_BRICK, SPANISH_ROOF_TILE, WROUGHT_IRON_GRILLE,
                            TALAVERA_TILE, SALTILLO_TILE,
                            COBALT_DOOR_CLOSED, COBALT_DOOR_OPEN,
                            CRIMSON_CEDAR_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_OPEN,
                            TEAL_DOOR_CLOSED, TEAL_DOOR_OPEN,
                            SAFFRON_DOOR_CLOSED, SAFFRON_DOOR_OPEN,
                            HALF_TIMBER_WALL, ASHLAR_BLOCK, GOTHIC_TRACERY, FLUTED_COLUMN,
                            CORNICE_BLOCK, ROSE_WINDOW, HERRINGBONE_BRICK, BAROQUE_TRIM,
                            TUDOR_BEAM, VENETIAN_FLOOR, FLEMISH_BRICK, PILASTER,
                            DENTIL_TRIM, WATTLE_DAUB, NORDIC_PLANK, MANSARD_SLATE,
                            ROMAN_MOSAIC, SETT_STONE, ROMANESQUE_ARCH, DARK_SLATE_ROOF,
                            KEYSTONE, PLINTH_BLOCK, IRON_LANTERN, SANDSTONE_ASHLAR,
                            GARGOYLE_BLOCK,
                            OGEE_ARCH, RUSTICATED_STONE, CHEVRON_STONE, TRIGLYPH_PANEL,
                            MARBLE_INLAY, BRICK_NOGGING, CRENELLATION, FAN_VAULT,
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
                            SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
                            TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
                            TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
                            TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY,
                            TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN,
                            TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE,
                            TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
                            TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER,
                            TEXTILE_TAPESTRY_IVORY)
        # Only terrain and surface landmarks show their real color; ores/resources/NPCs
        # blend into stone so the minimap doesn't reveal their locations.
        TERRAIN_IDS = (
            {AIR, GRASS, DIRT, STONE, OBSIDIAN, BEDROCK, WATER, GRAVEL,
             GATE_MID, GATE_DEEP, GATE_CORE,
             CRACKED_STONE, STALACTITE, STALAGMITE, CAVE_MOSS,
             HOUSE_WALL, HOUSE_ROOF,
             HOUSE_WALL_STONE, HOUSE_ROOF_STONE,
             HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK,
             HOUSE_WALL_DARK, HOUSE_ROOF_DARK,
             RESTAURANT_WALL, RESTAURANT_AWNING,
             POLISHED_GRANITE, POLISHED_MARBLE, SLATE_TILE,
             TERRACOTTA_BLOCK, MOSSY_BRICK, CREAM_BRICK,
             CHARCOAL_PLANK, WALNUT_PLANK, OAK_PANEL, BAMBOO_PANEL,
             OBSIDIAN_TILE, COBBLESTONE, LAPIS_BRICK, BASALT_COLUMN,
             LIMESTONE_BLOCK, COPPER_TILE, TEAK_PLANK,
             DRIFTWOOD_PLANK, CEDAR_PANEL, JADE_PANEL,
             ROSE_QUARTZ_BLOCK, GILDED_BRICK, AMETHYST_BLOCK,
             AMBER_TILE, IVORY_BRICK, EBONY_PLANK,
             MAHOGANY_PLANK, ASH_PLANK, FROSTED_GLASS, CRIMSON_BRICK,
             TERRACOTTA_SHINGLE, THATCH_ROOF, VERDIGRIS_COPPER,
             SILVER_PANEL, GOLD_LEAF_TRIM,
             STAINED_GLASS_RED, STAINED_GLASS_BLUE, STAINED_GLASS_GREEN,
             QUARTZ_PILLAR, ONYX_INLAY,
             WHITE_PLASTER_WALL, CARVED_PLASTER, MUQARNAS_BLOCK,
             MASHRABIYA, ZELLIGE_TILE, ARABESQUE_PANEL,
             ADOBE_BRICK, SPANISH_ROOF_TILE, WROUGHT_IRON_GRILLE,
             TALAVERA_TILE, SALTILLO_TILE,
             COBALT_DOOR_CLOSED, COBALT_DOOR_OPEN,
             CRIMSON_CEDAR_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_OPEN,
             TEAL_DOOR_CLOSED, TEAL_DOOR_OPEN,
             SAFFRON_DOOR_CLOSED, SAFFRON_DOOR_OPEN,
             HALF_TIMBER_WALL, ASHLAR_BLOCK, GOTHIC_TRACERY, FLUTED_COLUMN,
             CORNICE_BLOCK, ROSE_WINDOW, HERRINGBONE_BRICK, BAROQUE_TRIM,
             TUDOR_BEAM, VENETIAN_FLOOR, FLEMISH_BRICK, PILASTER,
             DENTIL_TRIM, WATTLE_DAUB, NORDIC_PLANK, MANSARD_SLATE,
             ROMAN_MOSAIC, SETT_STONE, ROMANESQUE_ARCH, DARK_SLATE_ROOF,
             KEYSTONE, PLINTH_BLOCK, IRON_LANTERN, SANDSTONE_ASHLAR,
             GARGOYLE_BLOCK,
             OGEE_ARCH, RUSTICATED_STONE, CHEVRON_STONE, TRIGLYPH_PANEL,
             MARBLE_INLAY, BRICK_NOGGING, CRENELLATION, FAN_VAULT,
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
             SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
             TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
             TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
             TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY,
             TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON,
             TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
             TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY,
             SNOW, SAND}
            | ALL_LOGS | ALL_LEAVES
        )
        stone_col = BLOCKS[STONE]["color"]
        table = [(30, 28, 38)] * 512
        for bid, bdata in BLOCKS.items():
            if 0 <= bid < 512:
                if bid in TERRAIN_IDS:
                    col = bdata.get("color")
                    table[bid] = col if col else stone_col
                else:
                    table[bid] = stone_col
        return table

    def _rebuild_minimap(self, world):
        from constants import CHUNK_W, WORLD_H
        if not world._chunks:
            self._minimap_surf = None
            return
        cxs = sorted(world._chunks.keys())
        min_cx, max_cx = cxs[0], cxs[-1]
        raw_w = (max_cx - min_cx + 1) * CHUNK_W
        raw_h = WORLD_H
        self._mm_min_bx = min_cx * CHUNK_W
        self._mm_span_bx = raw_w
        raw = pygame.Surface((raw_w, raw_h))
        ctable = self._mm_ctable
        mapped = [raw.map_rgb(*ctable[i]) for i in range(len(ctable))]
        pa = pygame.PixelArray(raw)
        mask = len(ctable) - 1  # ctable size is power of 2, so this wraps safely
        for cx in cxs:
            chunk = world._chunks[cx]
            base_x = (cx - min_cx) * CHUNK_W
            for lx in range(CHUNK_W):
                for y in range(raw_h):
                    pa[base_x + lx][y] = mapped[chunk[y][lx] & mask]
        del pa
        self._minimap_surf = pygame.transform.scale(raw, (_MM_W, _MM_H))

    def draw_minimap(self, world, player, dt):
        if not self.minimap_visible:
            return
        self._minimap_timer -= dt
        if self._minimap_surf is None or self._minimap_timer <= 0:
            self._rebuild_minimap(world)
            self._minimap_timer = 3.0
        if self._minimap_surf is None:
            return

        mx = SCREEN_W - _MM_W - _MM_MARGIN
        my = SCREEN_H - _MM_H - 58 - _MM_MARGIN

        pygame.draw.rect(self.screen, (12, 10, 18), (mx - 4, my - 4, _MM_W + 8, _MM_H + 8))
        self.screen.blit(self._minimap_surf, (mx, my))
        pygame.draw.rect(self.screen, (65, 65, 75), (mx - 4, my - 4, _MM_W + 8, _MM_H + 8), 1)

        mm_off = getattr(self, '_mm_min_bx', 0)
        mm_span = max(1, getattr(self, '_mm_span_bx', 1))
        h = world.height

        vx = int((self.cam_x / BLOCK_SIZE - mm_off) / mm_span * _MM_W)
        vy = int(self.cam_y / BLOCK_SIZE * _MM_H / h)
        vw = max(2, int(SCREEN_W / BLOCK_SIZE / mm_span * _MM_W))
        vh = max(2, int(SCREEN_H / BLOCK_SIZE * _MM_H / h))
        vx = max(0, min(_MM_W - 1, vx))
        vy = max(0, min(_MM_H - 1, vy))
        pygame.draw.rect(self.screen, (220, 215, 50), (mx + vx, my + vy, vw, vh), 1)

        px_map = int((player.x / BLOCK_SIZE - mm_off) / mm_span * _MM_W)
        py_map = int(player.y / BLOCK_SIZE * _MM_H / h)
        px_map = max(1, min(_MM_W - 2, px_map))
        py_map = max(1, min(_MM_H - 2, py_map))
        pygame.draw.rect(self.screen, (255, 255, 255), (mx + px_map - 1, my + py_map - 1, 3, 3))

    def draw_dropped_items(self, dropped_items):
        from items import ITEMS
        for item in dropped_items:
            sx = int(item.x - self.cam_x)
            sy = int(item.y - self.cam_y)
            if not (-20 <= sx <= SCREEN_W + 20 and -20 <= sy <= SCREEN_H + 20):
                continue
            col = ITEMS.get(item.item_id, {}).get("color", (200, 200, 200))
            pygame.draw.rect(self.screen, col, (sx - 8, sy - 8, 16, 16))
            pygame.draw.rect(self.screen, (255, 255, 255), (sx - 8, sy - 8, 16, 16), 1)
            if item.count > 1:
                txt = self._npc_font.render(str(item.count), True, (255, 255, 255))
                self.screen.blit(txt, (sx - txt.get_width() // 2, sy - txt.get_height() // 2))

    # ------------------------------------------------------------------
    # Birds
    # ------------------------------------------------------------------

    def draw_birds(self, birds):
        for bird in birds:
            sx = int(bird.x - self.cam_x)
            sy = int(bird.y - self.cam_y)
            if sx < -40 or sx > SCREEN_W + 40 or sy < -40 or sy > SCREEN_H + 40:
                continue
            self._draw_bird(bird, sx, sy)

    def _draw_bird(self, bird, sx, sy):
        sp = bird.SPECIES
        perching = (bird.state == "perching")
        wing_flap = abs(math.sin(bird._wing_phase)) * 5 if not perching else 0

        # Clickable perch indicator — subtle white outline
        if perching:
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (sx - 1, sy - 1, bird.W + 2, bird.H + 2), 1)

        if sp == "robin":
            self._draw_robin(bird, sx, sy, wing_flap, perching)
        elif sp == "blue_jay":
            self._draw_bluejay(bird, sx, sy, wing_flap, perching)
        elif sp == "eagle":
            self._draw_eagle(bird, sx, sy, wing_flap, perching)
        elif sp == "pelican":
            self._draw_pelican(bird, sx, sy, wing_flap, perching)
        elif sp == "parrot":
            self._draw_parrot(bird, sx, sy, wing_flap, perching)
        elif sp == "sparrow":
            self._draw_sparrow(bird, sx, sy, wing_flap, perching)
        elif sp == "heron":
            self._draw_heron(bird, sx, sy, wing_flap, perching)
        elif sp == "hummingbird":
            self._draw_hummingbird(bird, sx, sy, wing_flap, perching)
        elif sp == "owl":
            self._draw_owl(bird, sx, sy, wing_flap, perching)
        elif sp == "crow":
            self._draw_crow(bird, sx, sy, wing_flap, perching)
        elif sp == "flamingo":
            self._draw_flamingo(bird, sx, sy, wing_flap, perching)
        elif sp == "toucan":
            self._draw_toucan(bird, sx, sy, wing_flap, perching)
        elif sp == "cardinal":
            self._draw_cardinal(bird, sx, sy, wing_flap, perching)
        elif sp == "puffin":
            self._draw_puffin(bird, sx, sy, wing_flap, perching)
        elif sp == "vulture":
            self._draw_vulture(bird, sx, sy, wing_flap, perching)
        elif sp == "roadrunner":
            self._draw_roadrunner(bird, sx, sy, wing_flap, perching)
        elif sp == "peacock":
            self._draw_peacock(bird, sx, sy, wing_flap, perching)
        elif sp == "kookaburra":
            self._draw_kookaburra(bird, sx, sy, wing_flap, perching)
        elif sp == "sandpiper":
            self._draw_sandpiper(bird, sx, sy, wing_flap, perching)
        elif sp == "kingfisher":
            self._draw_kingfisher(bird, sx, sy, wing_flap, perching)
        elif sp == "woodpecker":
            self._draw_woodpecker(bird, sx, sy, wing_flap, perching)
        elif sp == "finch":
            self._draw_finch(bird, sx, sy, wing_flap, perching)
        elif sp == "stork":
            self._draw_stork(bird, sx, sy, wing_flap, perching)
        elif sp == "macaw":
            self._draw_macaw(bird, sx, sy, wing_flap, perching)
        elif sp == "pheasant":
            self._draw_pheasant(bird, sx, sy, wing_flap, perching)
        elif sp == "condor":
            self._draw_condor(bird, sx, sy, wing_flap, perching)
        elif sp == "snow_bunting":
            self._draw_snow_bunting(bird, sx, sy, wing_flap, perching)
        elif sp == "prairie_falcon":
            self._draw_prairie_falcon(bird, sx, sy, wing_flap, perching)
        elif sp == "nightjar":
            self._draw_nightjar(bird, sx, sy, wing_flap, perching)
        elif sp == "ibis":
            self._draw_ibis(bird, sx, sy, wing_flap, perching)
        elif sp == "albatross":
            self._draw_albatross(bird, sx, sy, wing_flap, perching)
        elif sp == "raven":
            self._draw_raven(bird, sx, sy, wing_flap, perching)
        elif sp == "swallow":
            self._draw_swallow(bird, sx, sy, wing_flap, perching)
        elif sp == "crane":
            self._draw_crane(bird, sx, sy, wing_flap, perching)
        elif sp == "spoonbill":
            self._draw_spoonbill(bird, sx, sy, wing_flap, perching)
        elif sp == "peregrine_falcon":
            self._draw_peregrine_falcon(bird, sx, sy, wing_flap, perching)
        elif sp == "barn_owl":
            self._draw_barn_owl(bird, sx, sy, wing_flap, perching)
        elif sp == "magpie":
            self._draw_magpie(bird, sx, sy, wing_flap, perching)
        elif sp == "golden_oriole":
            self._draw_golden_oriole(bird, sx, sy, wing_flap, perching)
        elif sp == "hoopoe":
            self._draw_hoopoe(bird, sx, sy, wing_flap, perching)
        elif sp == "sunbird":
            self._draw_sunbird(bird, sx, sy, wing_flap, perching)
        elif sp == "ptarmigan":
            self._draw_ptarmigan(bird, sx, sy, wing_flap, perching)
        elif sp == "bittern":
            self._draw_bittern(bird, sx, sy, wing_flap, perching)
        elif sp == "cedar_waxwing":
            self._draw_cedar_waxwing(bird, sx, sy, wing_flap, perching)
        elif sp == "mockingbird":
            self._draw_mockingbird(bird, sx, sy, wing_flap, perching)
        elif sp == "egret":
            self._draw_egret(bird, sx, sy, wing_flap, perching)
        elif sp == "arctic_tern":
            self._draw_arctic_tern(bird, sx, sy, wing_flap, perching)
        elif sp == "cormorant":
            self._draw_cormorant(bird, sx, sy, wing_flap, perching)
        elif sp == "curlew":
            self._draw_curlew(bird, sx, sy, wing_flap, perching)
        elif sp == "avocet":
            self._draw_avocet(bird, sx, sy, wing_flap, perching)
        elif sp == "jacana":
            self._draw_jacana(bird, sx, sy, wing_flap, perching)
        elif sp == "lyrebird":
            self._draw_lyrebird(bird, sx, sy, wing_flap, perching)
        elif sp == "bee_eater":
            self._draw_bee_eater(bird, sx, sy, wing_flap, perching)
        elif sp == "roller":
            self._draw_roller(bird, sx, sy, wing_flap, perching)
        elif sp == "hornbill":
            self._draw_hornbill(bird, sx, sy, wing_flap, perching)
        elif sp == "quetzal":
            self._draw_quetzal(bird, sx, sy, wing_flap, perching)
        elif sp == "snowy_owl":
            self._draw_snowy_owl(bird, sx, sy, wing_flap, perching)
        elif sp == "osprey":
            self._draw_osprey(bird, sx, sy, wing_flap, perching)
        elif sp == "golden_pheasant":
            self._draw_golden_pheasant(bird, sx, sy, wing_flap, perching)
        elif sp == "treecreeper":
            self._draw_treecreeper(bird, sx, sy, wing_flap, perching)
        elif sp == "wren":
            self._draw_wren(bird, sx, sy, wing_flap, perching)
        elif sp == "nuthatch":
            self._draw_nuthatch(bird, sx, sy, wing_flap, perching)
        elif sp == "gannet":
            self._draw_gannet(bird, sx, sy, wing_flap, perching)
        elif sp == "frigatebird":
            self._draw_frigatebird(bird, sx, sy, wing_flap, perching)
        elif sp == "night_heron":
            self._draw_night_heron(bird, sx, sy, wing_flap, perching)
        elif sp == "lapwing":
            self._draw_lapwing(bird, sx, sy, wing_flap, perching)
        elif sp == "wheatear":
            self._draw_wheatear(bird, sx, sy, wing_flap, perching)
        elif sp == "redstart":
            self._draw_redstart(bird, sx, sy, wing_flap, perching)
        elif sp == "warbler":
            self._draw_warbler(bird, sx, sy, wing_flap, perching)
        elif sp == "long_tailed_tit":
            self._draw_long_tailed_tit(bird, sx, sy, wing_flap, perching)
        elif sp == "oystercatcher":
            self._draw_oystercatcher(bird, sx, sy, wing_flap, perching)
        elif sp == "kite":
            self._draw_kite(bird, sx, sy, wing_flap, perching)
        elif sp == "harrier":
            self._draw_harrier(bird, sx, sy, wing_flap, perching)
        elif sp == "snipe":
            self._draw_snipe(bird, sx, sy, wing_flap, perching)
        elif sp == "merlin":
            self._draw_merlin(bird, sx, sy, wing_flap, perching)
        elif sp == "goshawk":
            self._draw_goshawk(bird, sx, sy, wing_flap, perching)
        elif sp == "shoebill":
            self._draw_shoebill(bird, sx, sy, wing_flap, perching)
        elif sp == "booby":
            self._draw_booby(bird, sx, sy, wing_flap, perching)
        elif sp == "tropicbird":
            self._draw_tropicbird(bird, sx, sy, wing_flap, perching)
        elif sp == "dunlin":
            self._draw_dunlin(bird, sx, sy, wing_flap, perching)
        elif sp == "godwit":
            self._draw_godwit(bird, sx, sy, wing_flap, perching)
        elif sp == "oxpecker":
            self._draw_oxpecker(bird, sx, sy, wing_flap, perching)
        elif sp == "dipper":
            self._draw_dipper(bird, sx, sy, wing_flap, perching)
        elif sp == "skua":
            self._draw_skua(bird, sx, sy, wing_flap, perching)
        elif sp == "firecrest":
            self._draw_firecrest(bird, sx, sy, wing_flap, perching)
        elif sp == "red_crowned_crane":
            self._draw_red_crowned_crane(bird, sx, sy, wing_flap, perching)
        elif sp == "mandarin_duck":
            self._draw_mandarin_duck(bird, sx, sy, wing_flap, perching)
        elif sp == "chinese_monal":
            self._draw_chinese_monal(bird, sx, sy, wing_flap, perching)
        elif sp == "silver_pheasant":
            self._draw_silver_pheasant(bird, sx, sy, wing_flap, perching)
        elif sp == "crested_ibis":
            self._draw_crested_ibis(bird, sx, sy, wing_flap, perching)
        elif sp == "chinese_pond_heron":
            self._draw_chinese_pond_heron(bird, sx, sy, wing_flap, perching)
        elif sp == "fairy_pitta":
            self._draw_fairy_pitta(bird, sx, sy, wing_flap, perching)
        elif sp == "hwamei":
            self._draw_hwamei(bird, sx, sy, wing_flap, perching)
        elif sp == "black_drongo":
            self._draw_black_drongo(bird, sx, sy, wing_flap, perching)
        elif sp == "red_billed_blue_magpie":
            self._draw_red_billed_blue_magpie(bird, sx, sy, wing_flap, perching)
        elif sp == "african_fish_eagle":
            self._draw_african_fish_eagle(bird, sx, sy, wing_flap, perching)
        elif sp == "secretary_bird":
            self._draw_secretary_bird(bird, sx, sy, wing_flap, perching)
        elif sp == "martial_eagle":
            self._draw_martial_eagle(bird, sx, sy, wing_flap, perching)
        elif sp == "marabou_stork":
            self._draw_marabou_stork(bird, sx, sy, wing_flap, perching)
        elif sp == "superb_starling":
            self._draw_superb_starling(bird, sx, sy, wing_flap, perching)
        elif sp == "cape_weaver":
            self._draw_cape_weaver(bird, sx, sy, wing_flap, perching)
        elif sp == "hamerkop":
            self._draw_hamerkop(bird, sx, sy, wing_flap, perching)
        elif sp == "african_grey_parrot":
            self._draw_african_grey_parrot(bird, sx, sy, wing_flap, perching)
        elif sp == "ground_hornbill":
            self._draw_ground_hornbill(bird, sx, sy, wing_flap, perching)
        elif sp == "african_penguin":
            self._draw_african_penguin(bird, sx, sy, wing_flap, perching)

    def _draw_robin(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 3))
        # Breast (orange-red)
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 6, H - 5))
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 1 + int(wf), W, H - 4))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
        # Head
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Eye
        ex = hx + 3 if f == 1 else hx + 1
        pygame.draw.rect(self.screen, (20, 20, 20), (ex, sy + 1, 2, 2))
        # Beak
        bx = hx + 4 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

    def _draw_bluejay(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        # White underside
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 5, W - 6, H - 7))
        # Black necklace
        pygame.draw.rect(self.screen, (30, 30, 40), (sx + 3, sy + 4, W - 6, 2))
        # Head + crest
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Crest
        cx = hx + 2
        pygame.draw.line(self.screen, bird.BODY_COLOR, (cx, sy + 2), (cx - f, sy - 3), 2)
        # Eye
        ex = hx + 3 if f == 1 else hx + 1
        pygame.draw.rect(self.screen, (15, 15, 20), (ex, sy + 1, 2, 2))
        # Beak
        bx = hx + 5 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

    def _draw_eagle(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wide wings when flying
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
        # White head
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 5)
        # Eye
        ex = hx + 4 if f == 1 else hx + 2
        pygame.draw.rect(self.screen, (30, 25, 10), (ex, sy + 2, 2, 2))
        # Hooked beak
        bx = hx + 7 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 4, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -1), sy + 5, 2, 2))
        # Tail fan
        tx = sx + 2 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 4, 4, 4))

    def _draw_pelican(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 2, sy + 1 + int(wf), W + 4, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 2))
        # Head
        hx = sx + W - 7 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
        # Long beak
        bx = hx + 6 if f == 1 else hx - 7
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 7, 2))
        # Pouch
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (bx + (0 if f == 1 else 2), sy + 5, 5, 3))
        # Eye
        ex = hx + 4 if f == 1 else hx + 1
        pygame.draw.rect(self.screen, (20, 20, 20), (ex, sy + 2, 2, 2))

    def _draw_parrot(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings (bright green)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 2))
            # Yellow wing-bar
            pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR,
                                (sx + 2, sy + 2 + int(wf), W - 4, 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        # Long tail
        tx = sx + 2 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, (30, 140, 45), (tx, sy + H - 2, 3, 5))
        # Red head
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Eye
        ex = hx + 3 if f == 1 else hx + 1
        pygame.draw.rect(self.screen, (240, 230, 50), (ex, sy + 1, 2, 2))
        # Curved beak
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, (200, 70, 30), (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (180, 60, 25), (bx + (0 if f == 1 else 1), sy + 4, 2, 2))

    def _draw_sparrow(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Dark crown stripe
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx, sy, 3, 2))
        # Beak
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 0), sy, 1, 1))

    def _draw_heron(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Long legs (perching or standing pose)
        for lx_off in [3, W - 5]:
            pygame.draw.rect(self.screen, (180, 170, 130),
                             (sx + lx_off, sy + H - 8, 2, 8))
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 3 + int(wf), W, H - 6))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 8))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 8))
        # Long neck
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 8))
        # Head
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        # Dark crown
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (nx - 1, sy - 1, 4, 2))
        # Dagger beak
        bx = nx + 3 if f == 1 else nx - 6
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy, 6, 2))
        # Eye
        ex = nx + 2 if f == 1 else nx
        pygame.draw.rect(self.screen, (20, 20, 20), (ex, sy, 2, 2))

    def _draw_hummingbird(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Blur-wings (fast wingbeat) — wide translucent blur when flying
        if not perching:
            pygame.draw.ellipse(self.screen, (100, 200, 160),
                                (sx - 2, sy + 1, W + 4, 4))
        # Body (iridescent green)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Red throat
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 5, 3))
        # Head
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 2), 3)
        # Long thin beak
        bx = hx + 3 if f == 1 else hx - 6
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 6, 1))
        # Eye
        pygame.draw.rect(self.screen, (200, 200, 255), (hx + (1 if f == 1 else 0), sy + 1, 2, 2))

    def _draw_owl(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 2 + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
        # Body (rounded)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 3))
        # Facial disc
        pygame.draw.circle(self.screen, bird.ACCENT_COLOR, (sx + W // 2, sy + 4), 5)
        # Big eyes
        el = sx + W // 2 - 3
        er = sx + W // 2 + 1
        pygame.draw.circle(self.screen, (255, 190, 40), (el, sy + 4), 2)
        pygame.draw.circle(self.screen, (255, 190, 40), (er, sy + 4), 2)
        pygame.draw.circle(self.screen, (20, 20, 20), (el, sy + 4), 1)
        pygame.draw.circle(self.screen, (20, 20, 20), (er, sy + 4), 1)
        # Small beak
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (sx + W // 2 - 1, sy + 6, 2, 2))
        # Ear tufts
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (sx + W // 2 - 4, sy, 2, 3))
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (sx + W // 2 + 2, sy, 2, 3))

    def _draw_crow(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings (all black)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 1, sy + int(wf), W + 2, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        # Fan tail
        tx = sx + 1 if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 4, 5, 5))
        # Head
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Sheen highlight
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx + 1, sy, 2, 2))
        # Eye (white dot)
        ex = hx + 3 if f == 1 else hx + 1
        pygame.draw.rect(self.screen, (200, 210, 220), (ex, sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (10, 10, 12), (ex, sy + 1, 1, 1))
        # Beak
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

    # ------------------------------------------------------------------
    # New species (11–35)
    # ------------------------------------------------------------------

    def _draw_flamingo(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Long legs
        for lx in [sx + 4, sx + W - 6]:
            pygame.draw.rect(self.screen, (200, 90, 105), (lx, sy + H - 6, 2, 6))
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 4 + int(wf), W, H - 8))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 10))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 9))
        # Long S-curve neck
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 8))
        # Head
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        # Bent beak (knee-shaped)
        bx = nx + 3 if f == 1 else nx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
        pygame.draw.rect(self.screen, (215, 180, 60), (bx, sy + 1, 2, 2))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy, 2, 2))

    def _draw_toucan(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        # Yellow chest
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 6, H - 8))
        # Head
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Giant beak
        bx = hx + 5 if f == 1 else hx - 7
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 8, 3))
        pygame.draw.rect(self.screen, (60, 175, 60), (bx, sy + 2, 8, 1))
        pygame.draw.rect(self.screen, (210, 50, 30), (bx + (3 if f == 1 else 0), sy + 3, 5, 2))
        # Eye (yellow)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_cardinal(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        # Head + crest
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.line(self.screen, bird.BODY_COLOR, (hx + 2, sy + 2), (hx + 2 - f, sy - 3), 2)
        # Black mask
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR,
                         (hx + (2 if f == 1 else 0), sy + 2, 3, 2))
        # Beak
        bx = hx + 4 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_puffin(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings (black)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        # Body (black)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # White belly
        pygame.draw.ellipse(self.screen, (245, 243, 240), (sx + 2, sy + 4, W - 7, H - 6))
        # White face
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        # Bright orange beak
        bx = hx + 5 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 3))
        pygame.draw.rect(self.screen, (245, 200, 50), (bx, sy + 2, 4, 1))

    def _draw_vulture(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Very wide wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 2, sy + 2 + int(wf), W + 4, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
        # Body (hunched)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 4))
        # Small bare head (skin-colored)
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Hooked beak
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else -1), sy + 4, 2, 2))
        # Eye
        pygame.draw.rect(self.screen, (15, 15, 15), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_roadrunner(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Long tail
        tx = sx if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.WING_COLOR, (tx, sy + 3, 6, 3))
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx + 2, sy + 1 + int(wf), W - 4, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
        # Streaked pattern
        for i in range(3):
            pygame.draw.rect(self.screen, (130, 120, 90),
                             (sx + 4 + i * 3, sy + 3, 1, H - 5))
        # Crest
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
        pygame.draw.line(self.screen, bird.BODY_COLOR, (hx + 2, sy + 2), (hx + 2 - f, sy - 2), 2)
        # Blue eye-ring
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx + (2 if f == 1 else 1), sy + 1, 2, 2))
        # Beak
        bx = hx + 4 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))

    def _draw_peacock(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Tail fan (perching only — spread tail behind)
        if perching:
            for i in range(5):
                tx = sx + (W - 2 - i * 3) if f == 1 else sx + 2 + i * 3
                pygame.draw.line(self.screen, bird.ACCENT_COLOR,
                                 (tx, sy + H - 2), (tx - f * 4, sy + H + 6 + i), 2)
                pygame.draw.circle(self.screen, (60, 40, 160), (tx - f * 4, sy + H + 6 + i), 2)
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Body (teal)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        # Head + crown
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        for i in range(3):
            pygame.draw.circle(self.screen, bird.ACCENT_COLOR, (hx + i * 2, sy - 2), 1)
        # Eye
        pygame.draw.rect(self.screen, (240, 220, 50), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        # Beak
        bx = hx + 5 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

    def _draw_kookaburra(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings (brown)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Blue wing-bar
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 1, sy + 3, W - 2, 3))
        # Body (cream)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        # Large head
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 5)
        # Brown crown patch
        pygame.draw.rect(self.screen, bird.WING_COLOR, (hx, sy, 5, 3))
        # Big beak
        bx = hx + 6 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_sandpiper(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Pale belly
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 5, H - 6))
        # Thin legs
        for lx in [sx + 3, sx + W - 5]:
            pygame.draw.rect(self.screen, (130, 110, 80), (lx, sy + H - 2, 1, 3))
        # Head
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        # Long thin beak
        bx = hx + 3 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 1))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + 1, sy, 1, 1))

    def _draw_kingfisher(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings (bright blue)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Orange breast
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 5, H - 6))
        # Large head
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.BODY_COLOR, (hx + 2, sy + 2), 4)
        # Spear beak
        bx = hx + 5 if f == 1 else hx - 6
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 6, 2))
        # Eye
        pygame.draw.rect(self.screen, (240, 230, 200), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_woodpecker(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings (black with white bars)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 2 + int(wf), W, H - 4))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
        # White wingbars
        for row in [4, 7]:
            pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + row, W - 4, 1))
        # Body (black)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 6))
        # White cheek patch
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.ACCENT_COLOR, (hx + 2, sy + 4), 4)
        # Red crown
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
        # Chisel beak
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 3, 2))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 3, 2, 2))

    def _draw_finch(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings (dark)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        # Body (yellow)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Head
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        # Conical beak
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 2))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 0), sy, 1, 1))

    def _draw_stork(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Long legs
        for lx in [sx + 4, sx + W - 6]:
            pygame.draw.rect(self.screen, (190, 80, 40), (lx, sy + H - 8, 2, 8))
        # Wings (white with black tips)
        if not perching:
            pygame.draw.ellipse(self.screen, (220, 220, 220),
                                (sx, sy + 4 + int(wf), W, H - 8))
            # Black wingtips
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), 4, H - 9))
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + W - 4, sy + 4 + int(wf), 4, H - 9))
        else:
            pygame.draw.ellipse(self.screen, (220, 220, 220), (sx + 1, sy + 5, W - 2, H - 10))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 10))
        # Long neck
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 8))
        # Head
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        # Long orange beak
        bx = nx + 3 if f == 1 else nx - 7
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy, 7, 2))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (1 if f == 1 else 0), sy, 2, 2))

    def _draw_macaw(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Blue wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 1, sy + int(wf), W + 2, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Red body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        # Green neck accent
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 4, W - 8, 4))
        # Long tail
        tx = sx + 1 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 2, 3, 6))
        pygame.draw.rect(self.screen, bird.WING_COLOR, (tx + 1, sy + H - 2, 1, 6))
        # Yellow face
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Beak (curved)
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 4, 2, 2))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_pheasant(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Long tail
        tx = sx if f == 1 else sx + W - 7
        pygame.draw.rect(self.screen, (200, 120, 40), (tx, sy + 3, 7, 3))
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx + 3, sy + 2 + int(wf), W - 6, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 3, sy + 2, W - 6, H - 4))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 4))
        # Dark green head
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Red wattle
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (hx + (2 if f == 1 else 0), sy + 3, 3, 2))
        # Beak
        bx = hx + 5 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        # Eye (gold ring)
        pygame.draw.rect(self.screen, (230, 190, 60), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_condor(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Huge wings (near-black)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 3, sy + 3 + int(wf), W + 6, H - 4))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 6))
        # White collar ruff
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + W // 2 - 5, sy + 4, 10, 5))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 4, sy + 4, W - 8, H - 6))
        # Bare orange head
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
        # Hooked beak
        bx = hx + 7 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else -1), sy + 4, 2, 2))
        # Eye
        pygame.draw.rect(self.screen, (220, 50, 30), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (4 if f == 1 else 2), sy + 1, 1, 1))

    def _draw_snow_bunting(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Black wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        # White body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Buff tinge on sides
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 1, sy + 3, 3, H - 5))
        # Head (white)
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.BODY_COLOR, (hx + 1, sy + 1), 3)
        # Beak
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 0), sy, 1, 1))

    def _draw_prairie_falcon(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Pointed wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 1, sy + 1 + int(wf), W + 2, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Body (pale brown)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        # Streaked belly
        for i in range(3):
            pygame.draw.rect(self.screen, (130, 100, 60), (sx + 4 + i * 3, sy + 5, 1, H - 7))
        # Head
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        # Dark malar stripe
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR,
                         (hx + (2 if f == 1 else 0), sy + 3, 2, 3))
        # Beak with yellow cere
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 2))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (bx + (1 if f == 1 else -1), sy + 3, 2, 2))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_nightjar(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Cryptic mottled wings (overlapping ellipses for pattern)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 1))
            pygame.draw.ellipse(self.screen, (150, 130, 95), (sx + 2, sy + 1 + int(wf), W - 5, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
            pygame.draw.ellipse(self.screen, (150, 130, 95), (sx + 2, sy + 2, W - 5, H - 4))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        # White throat bar
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 6, 2))
        # Head (flat/cryptic)
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
        # Tiny wide mouth (gape)
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 2, 3, 1))
        # Eye (large for nocturnal)
        pygame.draw.rect(self.screen, (80, 70, 50), (hx + (2 if f == 1 else 0), sy + 1, 3, 3))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 0), sy + 1, 2, 2))

    def _draw_ibis(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Long legs
        for lx in [sx + 4, sx + W - 6]:
            pygame.draw.rect(self.screen, (180, 60, 50), (lx, sy + H - 7, 2, 7))
        # Wings (scarlet)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 3 + int(wf), W, H - 7))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 9))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 8))
        # Long curved neck
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 7))
        # Head
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        # Down-curved beak
        bx = nx + 3 if f == 1 else nx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else 0), sy + 3, 3, 2))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy, 2, 2))

    def _draw_albatross(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Very wide dark wingtips
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 3, sy + 2 + int(wf), W + 6, H - 3))
            # White inner wing
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR,
                                (sx + 2, sy + 2 + int(wf), W - 4, H - 5))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
        # White body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 5))
        # Head (white)
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 5)
        # Large pale beak
        bx = hx + 7 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 5, 2))
        pygame.draw.rect(self.screen, (180, 150, 110), (bx + (2 if f == 1 else 0), sy + 5, 3, 2))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

    def _draw_raven(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Wings (glossy black)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 1, sy + int(wf), W + 2, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        # Purple iridescent sheen
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 2, W - 8, 4))
        # Wedge tail (distinctive from crow)
        tx = sx + 2 if f == 1 else sx + W - 6
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 4, 6, 5))
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx + 2, sy + H - 2, 2, 3))
        # Head (large)
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 5)
        # Heavy beak
        bx = hx + 6 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 4, 3))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else -1), sy + 4, 3, 2))
        # Eye (white iris)
        pygame.draw.rect(self.screen, (180, 185, 190), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_swallow(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Forked tail
        tx = sx + 1 if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 2, 2, 4))
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx + 3, sy + H - 2, 2, 4))
        # Wings (sleek, swept-back)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        # Body (deep blue)
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        # Orange-rust breast
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 4, W - 6, H - 6))
        # Head
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.BODY_COLOR, (hx + 1, sy + 1), 3)
        # Tiny beak
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

    def _draw_crane(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Long legs
        for lx in [sx + 4, sx + W - 6]:
            pygame.draw.rect(self.screen, (170, 165, 130), (lx, sy + H - 8, 2, 8))
        # Wings
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 4 + int(wf), W, H - 8))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 10))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 10))
        # Long neck (extended forward when flying)
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (nx, sy + 1, 3, H - 7))
        # Head
        pygame.draw.circle(self.screen, (220, 220, 225), (nx + 1, sy + 1), 3)
        # Red crown cap
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy - 1, 3, 3))
        # Beak
        bx = nx + 3 if f == 1 else nx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy, 5, 2))
        # Eye
        pygame.draw.rect(self.screen, (240, 235, 100), (nx + (2 if f == 1 else 0), sy, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy, 1, 1))

    def _draw_spoonbill(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        # Long legs
        for lx in [sx + 4, sx + W - 6]:
            pygame.draw.rect(self.screen, (160, 120, 130), (lx, sy + H - 7, 2, 7))
        # Wings (pink)
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 3 + int(wf), W, H - 7))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 9))
        # Body
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 8))
        # Yellow eye area
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + W // 2 - 3, sy + 2, 6, 4))
        # Long neck
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 7))
        # Head
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        # Spatula / spoon beak (flat wide tip)
        bx = nx + 3 if f == 1 else nx - 7
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else 0), sy, 3, 4))
        # Eye
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy, 2, 2))

    # ------------------------------------------------------------------
    # Species 36–85 draw functions
    # ------------------------------------------------------------------

    def _draw_peregrine_falcon(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 4))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 6, W - 8, H - 8))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 5)
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 5, 5, 3))
        bx = hx + 7 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 3, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 5, 2, 2))
        pygame.draw.rect(self.screen, (240, 230, 200), (hx + (2 if f == 1 else 2), sy + 2, 2, 2))

    def _draw_barn_owl(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 4))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (sx + W // 2, sy + 4), 6)
        # Heart-shaped face disc
        pygame.draw.ellipse(self.screen, (250, 245, 235), (sx + W // 2 - 5, sy + 2, 10, 8))
        pygame.draw.circle(self.screen, (230, 180, 100), (sx + W // 2 - 2, sy + 4), 2)
        pygame.draw.circle(self.screen, (230, 180, 100), (sx + W // 2 + 2, sy + 4), 2)
        pygame.draw.circle(self.screen, (20, 20, 20), (sx + W // 2 - 2, sy + 4), 1)
        pygame.draw.circle(self.screen, (20, 20, 20), (sx + W // 2 + 2, sy + 4), 1)
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (sx + W // 2 - 1, sy + 6, 2, 2))

    def _draw_magpie(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 7))
        tx = sx + 1 if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 2, 4, 6))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.rect(self.screen, (220, 230, 255), (hx + (1 if f == 1 else 1), sy, 3, 2))
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (200, 210, 230), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_golden_oriole(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx + (0 if f == 1 else 1), sy + 1, 4, 2))
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_hoopoe(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 4, W - 8, H - 6))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        for i in range(4):
            pygame.draw.rect(self.screen, bird.HEAD_COLOR, (hx + 1 - i, sy - 1 - i, 2, 2))
            pygame.draw.rect(self.screen, (22, 22, 28), (hx + 1 - i, sy - 1 - i, 1, 1))
        bx = hx + 5 if f == 1 else hx - 6
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 6, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_sunbird(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 4, H - 6))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        bx = hx + 3 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

    def _draw_ptarmigan(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 1), sy, 3, 2))
        bx = hx + 4 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_bittern(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 3, sx + W - 5]:
            pygame.draw.rect(self.screen, (155, 128, 75), (lx, sy + H - 6, 2, 6))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 8))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 9))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 9))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 11))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 8))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        bx = nx + 3 if f == 1 else nx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy, 5, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

    def _draw_cedar_waxwing(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        tx = sx + 1 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (tx, sy + H - 2, 3, 3))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.line(self.screen, (22, 22, 28), (hx, sy + 2), (hx + 4, sy + 2), 1)
        cx = hx + 2
        pygame.draw.line(self.screen, bird.HEAD_COLOR, (cx, sy + 2), (cx - f, sy - 3), 2)
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_mockingbird(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 3, 5, 3))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_egret(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 3, sx + W - 5]:
            pygame.draw.rect(self.screen, (170, 160, 120), (lx, sy + H - 8, 2, 8))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 6))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 8))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 8))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, H - 8))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        bx = nx + 3 if f == 1 else nx - 6
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy, 6, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

    def _draw_arctic_tern(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 2, sy + int(wf), W + 4, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        tx = sx + 1 if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 3, 2, 4))
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx + (0 if f == 1 else 2), sy + H - 3, 2, 4))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
        bx = hx + 4 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
        pygame.draw.rect(self.screen, (240, 240, 245), (hx + (1 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_cormorant(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 1, sy + 1 + int(wf), W + 2, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        nx = sx + W - 5 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, 5))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        bx = nx + 4 if f == 1 else nx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else 0), sy + 3, 3, 2))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (nx + (1 if f == 1 else 1), sy + 3, 4, 2))
        pygame.draw.rect(self.screen, (230, 210, 180), (nx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_curlew(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 3, sx + W - 5]:
            pygame.draw.rect(self.screen, (145, 118, 78), (lx, sy + H - 6, 2, 6))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 5))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 7))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, 5))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        bx = nx + 3 if f == 1 else nx - 8
        for i in range(4):
            ox = i if f == 1 else -i
            pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + ox, sy + 1 + i // 2, 2, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

    def _draw_avocet(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 3, sx + W - 5]:
            pygame.draw.rect(self.screen, (170, 160, 140), (lx, sy + H - 6, 2, 6))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 6))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 7))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 7))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, 5))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        bx = nx + 3 if f == 1 else nx - 7
        for i in range(4):
            ox = i if f == 1 else -i
            pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + ox, sy + 2 - i // 3, 2, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

    def _draw_jacana(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 2, sx + W - 4, sx + 5, sx + W - 7]:
            pygame.draw.rect(self.screen, (100, 52, 22), (lx, sy + H - 5, 1, 5))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 5))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (hx + (0 if f == 1 else 1), sy, 5, 3))
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_lyrebird(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        tx = sx + 1 if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (tx - 1, sy + H - 2, 2, 8))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (tx + 2, sy + H - 2, 2, 8))
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 2, 2, 6))
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_bee_eater(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.HEAD_COLOR, (sx + 3, sy + 4, W - 8, H - 7))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 6, W - 10, H - 9))
        tx = sx + 1 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 2, 2, 4))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_roller(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 8))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_hornbill(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.HEAD_COLOR, (sx + 3, sy + 4, W - 7, H - 8))
        hx = sx + W - 7 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
        bx = hx + 6 if f == 1 else hx - 7
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 7, 3))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (bx, sy + 1, 5, 3))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 2), sy + 2, 2, 2))

    def _draw_quetzal(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 8))
        tx = sx + 1 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, bird.WING_COLOR, (tx, sy + H - 2, 3, 8))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.BODY_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (240, 230, 200), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_snowy_owl(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 3))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (sx + W // 2, sy + 4), 6)
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + W // 2 - 5, sy + 2, 10, 8))
        pygame.draw.circle(self.screen, (240, 220, 80), (sx + W // 2 - 2, sy + 4), 3)
        pygame.draw.circle(self.screen, (240, 220, 80), (sx + W // 2 + 2, sy + 4), 3)
        pygame.draw.circle(self.screen, (20, 20, 20), (sx + W // 2 - 2, sy + 4), 2)
        pygame.draw.circle(self.screen, (20, 20, 20), (sx + W // 2 + 2, sy + 4), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (sx + W // 2 - 1, sy + 3), 1)
        pygame.draw.circle(self.screen, (255, 255, 255), (sx + W // 2 + 3, sy + 3), 1)
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (sx + W // 2 - 1, sy + 7, 2, 2))

    def _draw_osprey(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
        pygame.draw.ellipse(self.screen, (245, 242, 238), (sx + 4, sy + 6, W - 10, H - 8))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 5)
        pygame.draw.rect(self.screen, (45, 38, 30), (hx + (0 if f == 1 else 2), sy + 3, 7, 2))
        bx = hx + 7 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 4, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 5, 3, 2))
        pygame.draw.rect(self.screen, (240, 225, 80), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

    def _draw_golden_pheasant(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 8))
        tx = sx + 1 if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 2, 3, 7))
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.rect(self.screen, (240, 215, 30), (hx + (0 if f == 1 else 1), sy - 1, 4, 2))
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_treecreeper(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 3, H - 6))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        bx = hx + 3 if f == 1 else hx - 4
        for i in range(3):
            ox = i if f == 1 else -i
            pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + ox, sy + 2 + i // 2, 1, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

    def _draw_wren(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 1))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        tx = sx + W - 2 if f == 1 else sx
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy, 2, 4))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx, sy, 2, 1))
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

    def _draw_nuthatch(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 3, H - 6))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
        pygame.draw.rect(self.screen, (22, 22, 28), (hx + (0 if f == 1 else 1), sy + 1, W - 6, 2))
        bx = hx + 4 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_gannet(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 3, sy + int(wf), W + 6, H - 2))
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 4, sy + 2, W - 8, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 5))
        hx = sx + W - 8 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (hx, sy, 8, 5))
        bx = hx + 7 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 2), sy + 1, 2, 2))

    def _draw_frigatebird(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 3, sy + 1 + int(wf), W + 6, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 5, sy + 2, W - 10, H - 3))
        tx = sx + 2 if f == 1 else sx + W - 6
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 3, 2, 5))
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx + (3 if f == 1 else -3), sy + H - 3, 2, 5))
        hx = sx + W - 8 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (hx + 1, sy + 4, 5, 4))
        bx = hx + 7 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 3, 2))
        pygame.draw.rect(self.screen, (200, 210, 220), (hx + (3 if f == 1 else 2), sy + 1, 2, 2))

    def _draw_night_heron(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 3, sx + W - 5]:
            pygame.draw.rect(self.screen, (165, 148, 108), (lx, sy + H - 6, 2, 6))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 7))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 8))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 8))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (nx, sy + 2, 3, 5))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 4)
        pygame.draw.rect(self.screen, (22, 22, 28), (nx - 1, sy, 5, 3))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (nx + (1 if f == 1 else 0), sy - 1, 2, 5))
        bx = nx + 4 if f == 1 else nx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
        pygame.draw.rect(self.screen, (220, 80, 40), (nx + (3 if f == 1 else 1), sy, 2, 2))

    def _draw_lapwing(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 7))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.line(self.screen, (22, 22, 28), (hx + 2, sy + 2), (hx + 2, sy - 4), 2)
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_wheatear(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 3, H - 5))
        tx = sx + 1 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (tx, sy + H - 3, 3, 3))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        pygame.draw.rect(self.screen, bird.WING_COLOR, (hx - 1, sy + 1, 4, 2))
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

    def _draw_redstart(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        tx = sx + 1 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (tx, sy + H - 3, 3, 5))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
        pygame.draw.rect(self.screen, (200, 210, 230), (hx + (1 if f == 1 else 0), sy, 1, 1))

    def _draw_warbler(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 1, sy + 4, W - 3, H - 6))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

    def _draw_long_tailed_tit(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 3, W - 4, H - 5))
        tx = sx + 1 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, bird.WING_COLOR, (tx, sy + H - 2, 2, 7))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        pygame.draw.rect(self.screen, bird.WING_COLOR, (hx, sy, 3, 2))
        bx = hx + 3 if f == 1 else hx - 1
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 1, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

    def _draw_oystercatcher(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 7))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
        pygame.draw.circle(self.screen, (240, 50, 30), (hx + (3 if f == 1 else 1), sy + 1), 2)
        pygame.draw.circle(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1), 1)

    def _draw_kite(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 4))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
        tx = sx + 2 if f == 1 else sx + W - 6
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 3, 2, 5))
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx + (3 if f == 1 else -3), sy + H - 4, 2, 6))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
        bx = hx + 6 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 2))
        pygame.draw.rect(self.screen, (240, 225, 100), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

    def _draw_harrier(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 4))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 4, sy + 6, W - 10, H - 8))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
        bx = hx + 6 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 3, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 5, 2, 2))
        pygame.draw.rect(self.screen, (240, 225, 80), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

    def _draw_snipe(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 1, W - 6, H - 4))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 1), 3)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx, sy, 4, 2))
        bx = hx + 4 if f == 1 else hx - 6
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 6, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy, 2, 2))

    def _draw_merlin(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 8))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 2))
        pygame.draw.rect(self.screen, (240, 220, 80), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_goshawk(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 5))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 4))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 4, sy + 5, W - 10, H - 7))
        for i in range(3):
            pygame.draw.rect(self.screen, bird.WING_COLOR,
                             (sx + 4 + i * 3, sy + 5, 2, H - 8))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
        pygame.draw.rect(self.screen, (22, 22, 32), (hx, sy + 1, 7, 3))
        pygame.draw.rect(self.screen, (235, 232, 220), (hx + 1, sy + 4, 5, 2))
        bx = hx + 7 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 4, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 5, 3, 2))
        pygame.draw.rect(self.screen, (240, 230, 90), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

    def _draw_shoebill(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 3, sx + W - 5]:
            pygame.draw.rect(self.screen, (100, 115, 130), (lx, sy + H - 8, 2, 8))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 8))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 10))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 9))
        nx = sx + W - 5 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 2, 4, 6))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 2, sy + 2), 4)
        bx = nx + 5 if f == 1 else nx - 7
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 7, 4))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (bx + (4 if f == 1 else 0), sy + 4, 3, 3))
        pygame.draw.rect(self.screen, (180, 80, 30), (nx + (3 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_booby(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 2, sy + 1 + int(wf), W + 4, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 3), 4)
        bx = hx + 6 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + H - 4, W - 8, 3))
        pygame.draw.rect(self.screen, (230, 215, 180), (hx + (3 if f == 1 else 2), sy + 2, 2, 2))

    def _draw_tropicbird(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 2, sy + int(wf), W + 4, H - 2))
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 4))
        tx = sx + 2 if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (tx, sy + H - 2, 2, 8))
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_dunlin(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 1))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 3, W - 5, H - 5))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 2)
        bx = hx + 3 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy, 1, 1))

    def _draw_godwit(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 3, sx + W - 5]:
            pygame.draw.rect(self.screen, (160, 108, 55), (lx, sy + H - 5, 2, 5))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 2 + int(wf), W, H - 5))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 6))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, H - 9))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 3, 5))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        bx = nx + 3 if f == 1 else nx - 7
        for i in range(4):
            ox = i if f == 1 else -i
            pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + ox, sy + 1 - i // 4, 2, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (1 if f == 1 else 1), sy, 2, 2))

    def _draw_oxpecker(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        bx = hx + 3 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 3, 2))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy, 3, 3))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

    def _draw_dipper(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 2, W - 5, H - 6))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
        pygame.draw.rect(self.screen, (200, 210, 230), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

    def _draw_skua(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx - 2, sy + 2 + int(wf), W + 4, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 2, W - 6, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 5, sy + 4, 8, 4))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 4)
        bx = hx + 6 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (1 if f == 1 else 0), sy + 4, 2, 2))
        pygame.draw.rect(self.screen, (180, 170, 130), (hx + (3 if f == 1 else 2), sy + 1, 2, 2))

    def _draw_firecrest(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 1, W, H - 1))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 1), 3)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx, sy - 1, 3, 2))
        bx = hx + 3 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 2, 1))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (1 if f == 1 else 0), sy + 1, 1, 1))

    def _draw_red_crowned_crane(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 4, sx + W - 6]:
            pygame.draw.rect(self.screen, (185, 175, 140), (lx, sy + H - 10, 2, 10))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx, sy + 4 + int(wf), W, H - 8))
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 4 + int(wf), 5, H - 10))
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + W - 5, sy + 4 + int(wf), 5, H - 10))
        else:
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 5, W - 2, H - 12))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 12))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 10))
        pygame.draw.circle(self.screen, bird.BODY_COLOR, (nx + 1, sy + 1), 3)
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx - 1, sy - 1, 5, 3))
        pygame.draw.rect(self.screen, (22, 22, 28), (nx, sy + 2, 3, 2))
        bx = nx + 3 if f == 1 else nx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 5, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy + 1, 2, 2))

    def _draw_mandarin_duck(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 4))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 8, 2))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy + 3, 3, 2))
        bx = hx + 5 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 3, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_chinese_monal(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        tx = sx if f == 1 else sx + W - 7
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (tx, sy + 3, 7, 3))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 2, sy + 2 + int(wf), W - 4, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 2, sy + 2, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 4))
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (230, 190, 50), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_silver_pheasant(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        tx = sx if f == 1 else sx + W - 7
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + 3, 7, 3))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 2, sy + 2 + int(wf), W - 4, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 2, sy + 2, W - 4, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 4, sy + 3, W - 8, H - 4))
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (hx + (2 if f == 1 else 0), sy + 3, 3, 2))
        bx = hx + 5 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (220, 195, 50), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_crested_ibis(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 4, sx + W - 6]:
            pygame.draw.rect(self.screen, (185, 140, 130), (lx, sy + H - 8, 2, 8))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 6))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 4, W - 2, H - 9))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 4, W - 4, H - 9))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 7))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 3)
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (nx, sy - 2, 2, 3))
        bx = nx + 3 if f == 1 else nx - 6
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -1), sy + 4, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (2 if f == 1 else 0), sy + 1, 2, 2))

    def _draw_chinese_pond_heron(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 2, sx + W - 4]:
            pygame.draw.rect(self.screen, (180, 160, 90), (lx, sy + H - 6, 2, 6))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + 3 + int(wf), W, H - 7))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 8))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 8))
        nx = sx + W - 3 if f == 1 else sx + 1
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 2, H - 7))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 1), 3)
        bx = nx + 3 if f == 1 else nx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy, 5, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (nx + (1 if f == 1 else 0), sy, 2, 2))

    def _draw_fairy_pitta(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 5, W - 7, H - 7))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (220, 190, 50), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_hwamei(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 1))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, (210, 185, 140), (sx + 2, sy + 4, W - 5, H - 5))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy + 1, 4, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))
        bx = hx + 5 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

    def _draw_black_drongo(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        tx = sx + 1 if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 3, 2, 4))
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx + 3, sy + H - 3, 2, 4))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 3, sy + 3, W - 8, H - 6))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 4, 2, 2))
        pygame.draw.rect(self.screen, (200, 30, 30), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_red_billed_blue_magpie(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        tx = sx + 1 if f == 1 else sx + W - 5
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (tx, sy + H - 3, 4, 7))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (tx + 1, sy + H + 1, 2, 3))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 5))
        hx = sx + W - 6 if f == 1 else sx + 2
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 5)
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (hx, sy + 3, 6, 4))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + W // 2 - 2, sy + 3, 4, 2))
        bx = hx + 6 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, (240, 230, 50), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (20, 20, 20), (hx + (4 if f == 1 else 2), sy + 1, 1, 1))

    def _draw_african_fish_eagle(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (sx + 5, sy + 4, W - 12, H - 6))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
        bx = hx + 7 if f == 1 else hx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 3))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else 0), sy + 5, 3, 2))
        pygame.draw.rect(self.screen, (30, 25, 15), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

    def _draw_secretary_bird(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 4, sx + W - 6]:
            pygame.draw.rect(self.screen, (215, 165, 130), (lx, sy + H - 10, 2, 10))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 4 + int(wf), W, H - 12))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 14))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 13))
        pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 4, sy + H - 14, W - 10, 5))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.BODY_COLOR, (nx, sy + 1, 3, H - 12))
        pygame.draw.circle(self.screen, bird.BODY_COLOR, (nx + 1, sy + 2), 4)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (nx, sy + 1, 4, 4))
        for i in range(3):
            qx = nx + 1
            pygame.draw.line(self.screen, bird.WING_COLOR,
                             (qx, sy + 2), (qx - f * (2 + i), sy - 3 - i), 1)
        bx = nx + 4 if f == 1 else nx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
        pygame.draw.rect(self.screen, (22, 22, 22), (nx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_martial_eagle(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 3, W - 6, H - 3))
        for i in range(3):
            pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + 5 + i * 4, sy + 5, 2, 2))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 3, sy + 2), 5)
        bx = hx + 7 if f == 1 else hx - 4
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 4, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -1), sy + 4, 2, 2))
        pygame.draw.rect(self.screen, (235, 230, 215), (hx + (4 if f == 1 else 2), sy + 1, 2, 2))

    def _draw_marabou_stork(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        for lx in [sx + 4, sx + W - 6]:
            pygame.draw.rect(self.screen, (185, 165, 145), (lx, sy + H - 8, 2, 8))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 4 + int(wf), W, H - 10))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 5, W - 2, H - 12))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 5, W - 4, H - 12))
        nx = sx + W - 4 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 2, 3, H - 12))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 1, sy + 2), 4)
        pygame.draw.ellipse(self.screen, bird.ACCENT_COLOR, (nx - 1, sy + 5, 5, 4))
        bx = nx + 4 if f == 1 else nx - 8
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 1, 8, 3))
        pygame.draw.rect(self.screen, (22, 22, 22), (nx + (2 if f == 1 else 0), sy + 1, 2, 2))

    def _draw_superb_starling(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (sx + 2, sy + 3, W - 4, 2))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
        bx = hx + 4 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 1))
        pygame.draw.rect(self.screen, (240, 235, 200), (hx + (2 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_cape_weaver(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx + (2 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))
        bx = hx + 4 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))

    def _draw_hamerkop(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx, sy + 2 + int(wf), W, H - 4))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 3, W - 2, H - 6))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 3, W - 4, H - 5))
        nx = sx + W - 5 if f == 1 else sx + 2
        pygame.draw.rect(self.screen, bird.HEAD_COLOR, (nx, sy + 1, 4, H - 6))
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (nx + 2, sy + 2), 4)
        cx = nx - 3 if f == 1 else nx + 5
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (cx, sy + 1, 5, 3))
        bx = nx + 5 if f == 1 else nx - 5
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 5, 2))
        pygame.draw.rect(self.screen, (22, 22, 22), (nx + (3 if f == 1 else 1), sy + 1, 2, 2))

    def _draw_african_grey_parrot(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        tx = sx + 1 if f == 1 else sx + W - 4
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (tx, sy + H - 2, 3, 5))
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 2))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 3))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 3))
        hx = sx + W - 5 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 4)
        bx = hx + 5 if f == 1 else hx - 3
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 3, 2))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (0 if f == 1 else 1), sy + 4, 2, 2))
        pygame.draw.rect(self.screen, (245, 240, 230), (hx + (3 if f == 1 else 1), sy + 1, 2, 2))
        pygame.draw.rect(self.screen, (22, 22, 22), (hx + (3 if f == 1 else 1), sy + 1, 1, 1))

    def _draw_ground_hornbill(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR,
                                (sx - 2, sy + 2 + int(wf), W + 4, H - 2))
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx + 3, sy + 3 + int(wf), 8, H - 6))
            pygame.draw.ellipse(self.screen, bird.WING_COLOR,
                                (sx + W - 11, sy + 3 + int(wf), 8, H - 6))
        else:
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 1, sy + 3, W - 2, H - 4))
        pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 3, sy + 4, W - 6, H - 5))
        hx = sx + W - 7 if f == 1 else sx + 3
        pygame.draw.circle(self.screen, bird.BODY_COLOR, (hx + 3, sy + 3), 5)
        pygame.draw.ellipse(self.screen, bird.HEAD_COLOR, (hx + 1, sy + 2, 6, 5))
        bx = hx + 7 if f == 1 else hx - 8
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 8, 3))
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx + (2 if f == 1 else -2), sy, 5, 3))
        pygame.draw.rect(self.screen, (22, 22, 22), (hx + (4 if f == 1 else 2), sy + 2, 2, 2))

    def _draw_african_penguin(self, bird, sx, sy, wf, perching):
        W, H = bird.W, bird.H
        f = bird.facing
        if not perching:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx, sy + int(wf), W, H - 3))
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 5))
        else:
            pygame.draw.ellipse(self.screen, bird.WING_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
            pygame.draw.ellipse(self.screen, bird.BODY_COLOR, (sx + 2, sy + 2, W - 4, H - 5))
        hx = sx + W - 4 if f == 1 else sx + 1
        pygame.draw.circle(self.screen, bird.HEAD_COLOR, (hx + 2, sy + 2), 3)
        pygame.draw.rect(self.screen, bird.ACCENT_COLOR, (hx + (1 if f == 1 else 0), sy + 2, 3, 2))
        bx = hx + 4 if f == 1 else hx - 2
        pygame.draw.rect(self.screen, bird.BEAK_COLOR, (bx, sy + 2, 2, 2))
        pygame.draw.rect(self.screen, (22, 22, 22), (hx + (2 if f == 1 else 1), sy + 1, 1, 1))

    # ------------------------------------------------------------------
    # Insects
    # ------------------------------------------------------------------

    def draw_insects(self, insects):
        for ins in insects:
            if ins.spooked:
                continue
            sx = int(ins.x - self.cam_x)
            sy = int(ins.y - self.cam_y)
            if sx < -30 or sx > SCREEN_W + 30 or sy < -30 or sy > SCREEN_H + 30:
                continue
            self._draw_insect(ins, sx, sy)

    def _draw_insect(self, ins, sx, sy):
        wt = ins.WING_TYPE
        wf = abs(math.sin(ins._hover_phase)) * 3
        if wt == "butterfly":
            self._draw_insect_butterfly(ins, sx, sy, wf)
        elif wt == "moth":
            self._draw_insect_moth(ins, sx, sy, wf)
        elif wt == "dragonfly":
            self._draw_insect_dragonfly(ins, sx, sy, wf)
        elif wt == "firefly":
            self._draw_insect_firefly(ins, sx, sy)
        elif wt == "beetle":
            self._draw_insect_beetle(ins, sx, sy)
        else:
            self._draw_insect_generic(ins, sx, sy, wf)

    def _draw_insect_butterfly(self, ins, sx, sy, wf):
        W, H = ins.W, ins.H
        wo = int(wf)
        # Upper wings
        pygame.draw.ellipse(self.screen, ins.WING_COLOR,
                            (sx, sy - wo, W // 2, H))
        pygame.draw.ellipse(self.screen, ins.WING_COLOR,
                            (sx + W // 2, sy - wo, W // 2, H))
        # Accent spots
        pygame.draw.ellipse(self.screen, ins.ACCENT_COLOR,
                            (sx + 2, sy - wo + 2, W // 2 - 3, H // 2))
        pygame.draw.ellipse(self.screen, ins.ACCENT_COLOR,
                            (sx + W // 2 + 1, sy - wo + 2, W // 2 - 3, H // 2))
        # Body
        pygame.draw.ellipse(self.screen, ins.BODY_COLOR,
                            (sx + W // 2 - 1, sy, 3, H))

    def _draw_insect_moth(self, ins, sx, sy, wf):
        W, H = ins.W, ins.H
        wo = int(wf)
        # Broad flat wings
        pygame.draw.ellipse(self.screen, ins.WING_COLOR,
                            (sx, sy + 1 - wo, W, H - 2))
        pygame.draw.ellipse(self.screen, ins.ACCENT_COLOR,
                            (sx + 2, sy + 2 - wo, W - 4, H - 4))
        # Body
        pygame.draw.ellipse(self.screen, ins.BODY_COLOR,
                            (sx + W // 2 - 1, sy, 3, H))

    def _draw_insect_dragonfly(self, ins, sx, sy, wf):
        W, H = ins.W, ins.H
        wo = int(wf)
        cx = sx + W // 2
        # 4 narrow wings
        pygame.draw.ellipse(self.screen, ins.WING_COLOR,
                            (sx, sy - 1 - wo, W // 2, 3))
        pygame.draw.ellipse(self.screen, ins.WING_COLOR,
                            (cx, sy - 1 - wo, W // 2, 3))
        pygame.draw.ellipse(self.screen, ins.WING_COLOR,
                            (sx + 2, sy + 2 - wo, W // 2 - 2, 2))
        pygame.draw.ellipse(self.screen, ins.WING_COLOR,
                            (cx - 2, sy + 2 - wo, W // 2 - 2, 2))
        # Elongated segmented body
        pygame.draw.ellipse(self.screen, ins.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        pygame.draw.ellipse(self.screen, ins.ACCENT_COLOR,
                            (sx + 3, sy + 2, W - 6, H - 4))

    def _draw_insect_firefly(self, ins, sx, sy):
        W, H = ins.W, ins.H
        # Small oval body
        pygame.draw.ellipse(self.screen, ins.BODY_COLOR, (sx, sy + 1, W, H - 2))
        pygame.draw.ellipse(self.screen, ins.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
        # Glowing tail — pulse with hover_phase
        glow_a = int(abs(math.sin(ins._hover_phase * 0.5)) * 200 + 55)
        gc = (
            min(255, ins.ACCENT_COLOR[0]),
            min(255, ins.ACCENT_COLOR[1]),
            min(255, ins.ACCENT_COLOR[2]),
        )
        tail_x = sx + W - 3
        pygame.draw.circle(self.screen, gc, (tail_x, sy + H // 2), 2)

    def _draw_insect_beetle(self, ins, sx, sy):
        W, H = ins.W, ins.H
        # Elytra (wing covers)
        pygame.draw.ellipse(self.screen, ins.WING_COLOR, (sx, sy, W, H))
        pygame.draw.ellipse(self.screen, ins.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
        # Central seam
        pygame.draw.line(self.screen, ins.WING_COLOR,
                         (sx + W // 2, sy + 1), (sx + W // 2, sy + H - 2))
        # Head
        pygame.draw.circle(self.screen, ins.ACCENT_COLOR,
                           (sx + W // 6, sy + H // 2), H // 3)

    def _draw_insect_generic(self, ins, sx, sy, wf):
        W, H = ins.W, ins.H
        wo = int(wf)
        pygame.draw.ellipse(self.screen, ins.WING_COLOR,
                            (sx, sy - wo, W, H + wo))
        pygame.draw.ellipse(self.screen, ins.BODY_COLOR,
                            (sx + W // 4, sy + 1, W // 2, H - 2))
        pygame.draw.circle(self.screen, ins.ACCENT_COLOR,
                           (sx + W // 2, sy), H // 3)
