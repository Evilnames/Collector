import pygame
from blocks import (BLOCKS, AIR, LADDER, SUPPORT, IRON_SUPPORT, DIAMOND_SUPPORT, STONE, WATER,
                    ALL_SUPPORTS, SUPPORT_RANGE, RESOURCE_BLOCKS, ALL_LOGS, ALL_LEAVES,
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
                    CAVE_MUSHROOM, CAVE_MUSHROOMS,
                    EMBER_CAP, PALE_GHOST, GOLD_CHANTERELLE, COBALT_CAP, MOSSY_CAP,
                    VIOLET_CROWN, BLOOD_CAP, SULFUR_DOME, IVORY_BELL, ASH_BELL,
                    TEAL_BELL, RUST_SHELF, COPPER_SHELF, OBSIDIAN_SHELF, COAL_PUFF,
                    STONE_PUFF, AMBER_PUFF, SULFUR_TUFT, HONEY_CLUSTER, CORAL_TUFT,
                    BONE_STALK, MAGMA_CAP, DEEP_INK, BIOLUME,
                    WOOD_FENCE, IRON_FENCE,
                    WOOD_DOOR_CLOSED, WOOD_DOOR_OPEN,
                    IRON_DOOR_CLOSED, IRON_DOOR_OPEN)
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, PLAYER_W, PLAYER_H, ROCK_WARM_ZONE
from biomes import BIOME_STONE_COLORS


def _darken(color, amount=25):
    return tuple(max(0, c - amount) for c in color)


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
        self._water_surfs = self._build_water_surfs()   # indexed by level-1 (0..7)
        self._resource_hint_surfs = self._build_resource_hint_surfs()
        self._biome_stone_surfs = self._build_biome_stone_surfs()
        self._biome_resource_hint_surfs = self._build_biome_resource_hint_surfs()
        self._support_zone_surf = self._build_support_zone_surf()
        self._log_variants  = self._build_log_variants()
        self._leaf_variants = self._build_leaf_variants()
        self._light_surf = pygame.Surface((SCREEN_W, SCREEN_H))
        self._mine_overlay = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        self._npc_font = pygame.font.SysFont("consolas", 14)
        self._minimap_surf  = None
        self._minimap_timer = 0.0
        self.minimap_visible = True
        self._mm_ctable     = self._build_mm_color_table()

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
            if bid == SUPPORT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                base = bdata["color"]
                dark = _darken(base, 30)
                s.fill(base)
                pygame.draw.line(s, dark, (2, 2), (BLOCK_SIZE - 3, BLOCK_SIZE - 3), 3)
                pygame.draw.line(s, dark, (BLOCK_SIZE - 3, 2), (2, BLOCK_SIZE - 3), 3)
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == IRON_SUPPORT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                base = bdata["color"]
                dark = _darken(base, 40)
                bright = tuple(min(255, c + 30) for c in base)
                s.fill(base)
                # I-beam shape: top/bottom plates + center web
                pygame.draw.rect(s, dark, (2, 2, BLOCK_SIZE - 4, 5))
                pygame.draw.rect(s, dark, (2, BLOCK_SIZE - 7, BLOCK_SIZE - 4, 5))
                pygame.draw.rect(s, dark, (BLOCK_SIZE // 2 - 3, 7, 6, BLOCK_SIZE - 14))
                pygame.draw.rect(s, bright, (BLOCK_SIZE // 2 - 2, 8, 4, BLOCK_SIZE - 16))
                pygame.draw.rect(s, dark, s.get_rect(), 1)
                surfs[bid] = s
                continue
            if bid == DIAMOND_SUPPORT:
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                base = bdata["color"]
                dark = _darken(base, 40)
                bright = tuple(min(255, c + 40) for c in base)
                s.fill(base)
                # Diamond/gem facet pattern
                cx, cy = BLOCK_SIZE // 2, BLOCK_SIZE // 2
                pts = [(cx, 3), (BLOCK_SIZE - 3, cy), (cx, BLOCK_SIZE - 3), (3, cy)]
                pygame.draw.polygon(s, dark, pts, 0)
                pygame.draw.polygon(s, bright, [(cx, 5), (BLOCK_SIZE - 5, cy), (cx, cy + 2), (5, cy)], 0)
                pygame.draw.polygon(s, dark, pts, 2)
                pygame.draw.line(s, bright, (cx, 5), (BLOCK_SIZE - 5, cy), 1)
                pygame.draw.line(s, bright, (5, cy), (cx, 5), 1)
                pygame.draw.rect(s, dark, s.get_rect(), 1)
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
            if bid == WATER:
                continue   # rendered per-level via _water_surfs
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

    def _build_support_zone_surf(self):
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        mid = BLOCK_SIZE // 2
        # Faint green tint over the cell
        s.fill((60, 200, 120, 40))
        # Visible X cross and horizontal bar
        col = (60, 210, 130, 200)
        pygame.draw.line(s, col, (mid - 6, mid - 6), (mid + 6, mid + 6), 2)
        pygame.draw.line(s, col, (mid + 6, mid - 6), (mid - 6, mid + 6), 2)
        pygame.draw.line(s, col, (mid - 8, mid),     (mid + 8, mid),     1)
        return s

    # ------------------------------------------------------------------
    # Camera
    # ------------------------------------------------------------------

    def update_camera(self, player, world):
        target_x = player.x - SCREEN_W // 2 + PLAYER_W // 2
        target_y = player.y - SCREEN_H // 2 + PLAYER_H // 2
        self.cam_x += (target_x - self.cam_x) * 0.12
        self.cam_y += (target_y - self.cam_y) * 0.12
        # Clamp to world bounds
        max_cx = world.width  * BLOCK_SIZE - SCREEN_W
        max_cy = world.height * BLOCK_SIZE - SCREEN_H
        self.cam_x = max(0.0, min(self.cam_x, float(max_cx)))
        self.cam_y = max(0.0, min(self.cam_y, float(max_cy)))

    # ------------------------------------------------------------------
    # Draw world
    # ------------------------------------------------------------------

    def draw_world(self, world, player=None):
        # Sky
        self.screen.fill((110, 170, 240))

        cam_xi = int(self.cam_x)
        cam_yi = int(self.cam_y)

        bx0 = max(0, cam_xi // BLOCK_SIZE)
        bx1 = min(world.width,  (cam_xi + SCREEN_W)  // BLOCK_SIZE + 2)
        by0 = max(0, cam_yi // BLOCK_SIZE)
        by1 = min(world.height, (cam_yi + SCREEN_H) // BLOCK_SIZE + 2)

        if player is not None:
            px_blk = player.x / BLOCK_SIZE
            py_blk = player.y / BLOCK_SIZE
            detect  = player.rock_detect_range
            warm    = detect + ROCK_WARM_ZONE
        else:
            px_blk = py_blk = detect = warm = None

        for by in range(by0, by1):
            for bx in range(bx0, bx1):
                bid = world.get_block(bx, by)
                if bid == AIR:
                    continue
                if bid == WATER:
                    level = world._water_level.get((bx, by), 8)
                    wsurf = self._water_surfs[level - 1]
                    wh = wsurf.get_height()
                    self.screen.blit(wsurf, (bx * BLOCK_SIZE - cam_xi,
                                             by * BLOCK_SIZE - cam_yi + BLOCK_SIZE - wh))
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
                biome = world.get_biome(bx)
                biome_stone = self._biome_stone_surfs.get(biome)
                if bid == STONE and biome_stone:
                    surf = biome_stone
                if bid in RESOURCE_BLOCKS and px_blk is not None:
                    dist = ((bx - px_blk) ** 2 + (by - py_blk) ** 2) ** 0.5
                    if dist > warm:
                        surf = biome_stone or self._block_surfs.get(STONE)
                    elif dist > detect:
                        biome_hints = self._biome_resource_hint_surfs.get(biome, self._resource_hint_surfs)
                        surf = biome_hints.get(bid, self._resource_hint_surfs[bid])
                if surf:
                    sx = bx * BLOCK_SIZE - cam_xi
                    sy = by * BLOCK_SIZE - cam_yi
                    self.screen.blit(surf, (sx, sy))

        self._draw_support_zones(world, bx0, bx1, by0, by1, cam_xi, cam_yi)

    def _draw_support_zones(self, world, bx0, bx1, by0, by1, cam_xi, cam_yi):
        max_r = max(SUPPORT_RANGE.values())
        ex0 = max(0, bx0 - max_r)
        ex1 = min(world.width, bx1 + max_r)
        ey0 = max(0, by0 - 1)
        ey1 = min(world.height, by1 + 2)

        covered = set()
        for sy in range(ey0, ey1):
            for sx in range(ex0, ex1):
                bid = world.get_block(sx, sy)
                if bid in ALL_SUPPORTS:
                    r = SUPPORT_RANGE[bid]
                    for dx in range(-r, r + 1):
                        nx = sx + dx
                        for cy in (sy, sy - 1):
                            if 0 <= nx < world.width and 0 <= cy < world.height:
                                covered.add((nx, cy))

        for (cx, cy) in covered:
            if bx0 <= cx < bx1 and by0 <= cy < by1:
                if world.get_block(cx, cy) == AIR:
                    px = cx * BLOCK_SIZE - cam_xi
                    py = cy * BLOCK_SIZE - cam_yi
                    self.screen.blit(self._support_zone_surf, (px, py))

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
            sx = int(e.x - self.cam_x)
            sy = int(e.y - self.cam_y)
            if e.animal_id == "sheep":
                self._draw_sheep(sx, sy, e)
            elif e.animal_id == "cow":
                self._draw_cow(sx, sy, e)
            elif e.animal_id == "chicken":
                self._draw_chicken(sx, sy, e)
            elif e.animal_id == "npc_quest":
                self._draw_npc_quest(sx, sy, e)
            elif e.animal_id == "npc_trade":
                self._draw_npc_trade(sx, sy, e)

    def draw_automations(self, automations):
        for a in automations:
            a.draw(self.screen, self.cam_x, self.cam_y)

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

    def _draw_sheep(self, sx, sy, sheep):
        W, H = sheep.W, sheep.H
        body_h = H - 8
        leg_y = sy + body_h

        # Legs
        leg_color = (80, 60, 40)
        for lx in [sx + 2, sx + 7, sx + 14, sx + 19]:
            pygame.draw.rect(self.screen, leg_color, (lx, leg_y, 3, 8))

        # Body
        body_color = (220, 220, 220) if sheep.has_wool else (175, 140, 95)
        pygame.draw.rect(self.screen, body_color, (sx, sy, W, body_h))

        # Head
        head_w, head_h = 9, 9
        head_color = (200, 200, 200) if sheep.has_wool else (155, 125, 85)
        hx = (sx + W - 2) if sheep.facing == 1 else (sx - head_w + 2)
        hy = sy - 1
        pygame.draw.rect(self.screen, head_color, (hx, hy, head_w, head_h))
        eye_x = (hx + head_w - 3) if sheep.facing == 1 else (hx + 1)
        pygame.draw.rect(self.screen, (30, 30, 30), (eye_x, hy + 3, 2, 2))

        # Harvest progress bar
        if sheep.being_harvested and sheep._harvest_time > 0:
            progress = sheep._harvest_time / sheep.HARVEST_TIME
            pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(self.screen, (100, 220, 100), (sx, sy - 7, int(W * progress), 4))

    def _draw_cow(self, sx, sy, cow):
        W, H = cow.W, cow.H
        body_h = H - 8
        leg_y = sy + body_h

        # Legs
        leg_color = (60, 40, 30)
        for lx in [sx + 2, sx + 8, sx + 18, sx + 24]:
            pygame.draw.rect(self.screen, leg_color, (lx, leg_y, 4, 8))

        # Body (brown base + black patches)
        pygame.draw.rect(self.screen, (140, 85, 45), (sx, sy, W, body_h))
        pygame.draw.rect(self.screen, (30, 20, 10), (sx + 8, sy + 2, 10, 5))
        pygame.draw.rect(self.screen, (30, 20, 10), (sx + 20, sy + 5, 6, 4))

        # Head
        head_w, head_h = 11, 11
        hx = (sx + W - 3) if cow.facing == 1 else (sx - head_w + 3)
        hy = sy - 2
        pygame.draw.rect(self.screen, (140, 85, 45), (hx, hy, head_w, head_h))
        # Nose/snout
        snout_x = (hx + head_w - 4) if cow.facing == 1 else hx
        pygame.draw.rect(self.screen, (190, 130, 100), (snout_x, hy + 6, 4, 4))
        eye_x = (hx + head_w - 4) if cow.facing == 1 else (hx + 1)
        pygame.draw.rect(self.screen, (20, 10, 5), (eye_x, hy + 2, 2, 2))

        # Udder indicator when has milk
        if cow.has_milk:
            udder_x = sx + W // 2 - 4
            pygame.draw.rect(self.screen, (220, 180, 180), (udder_x, leg_y - 3, 8, 3))

        # Harvest progress bar
        if cow.being_harvested and cow._harvest_time > 0:
            progress = cow._harvest_time / cow.HARVEST_TIME
            pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(self.screen, (80, 160, 220), (sx, sy - 7, int(W * progress), 4))

    def _draw_chicken(self, sx, sy, chicken):
        W, H = chicken.W, chicken.H

        # Legs
        for lx in [sx + 4, sx + 11]:
            pygame.draw.rect(self.screen, (220, 160, 30), (lx, sy + H - 6, 2, 6))

        # Body (white/cream oval)
        pygame.draw.ellipse(self.screen, (235, 235, 210), (sx + 1, sy + 2, W - 4, H - 8))

        # Head
        head_w, head_h = 8, 8
        hx = (sx + W - 4) if chicken.facing == 1 else (sx - head_w + 4)
        hy = sy - 2
        pygame.draw.ellipse(self.screen, (235, 235, 210), (hx, hy, head_w, head_h))
        # Beak
        beak_x = (hx + head_w - 1) if chicken.facing == 1 else (hx - 3)
        pygame.draw.rect(self.screen, (220, 160, 30), (beak_x, hy + 3, 3, 2))
        # Eye
        eye_x = (hx + head_w - 3) if chicken.facing == 1 else (hx + 1)
        pygame.draw.rect(self.screen, (20, 20, 20), (eye_x, hy + 2, 2, 2))
        # Comb
        pygame.draw.rect(self.screen, (220, 50, 50), (hx + 2, hy - 2, 4, 3))

        # Egg indicator
        if chicken.has_egg:
            pygame.draw.ellipse(self.screen, (245, 235, 200), (sx + W // 2 - 3, sy + H - 10, 6, 5))

        # Harvest progress bar
        if chicken.being_harvested and chicken._harvest_time > 0:
            progress = chicken._harvest_time / chicken.HARVEST_TIME
            pygame.draw.rect(self.screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(self.screen, (245, 220, 100), (sx, sy - 7, int(W * progress), 4))

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
        # Semi-transparent fill using the block's colour
        from blocks import BLOCKS
        color = BLOCKS.get(block_id, {}).get("color")
        if color:
            ghost = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            ghost.fill((*color, 120))
            self.screen.blit(ghost, (sx, sy))
        pygame.draw.rect(self.screen, (255, 255, 255), (sx, sy, BLOCK_SIZE, BLOCK_SIZE), 2)

    # ------------------------------------------------------------------
    # Water submersion overlay
    # ------------------------------------------------------------------

    def draw_water_overlay(self, player):
        if player._head_in_water():
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((30, 80, 180, 70))
            self.screen.blit(overlay, (0, 0))

    # ------------------------------------------------------------------
    # Lighting
    # ------------------------------------------------------------------

    def draw_lighting(self, player, depth):
        if depth <= 0:
            return

        # ambient brightness: 230 at surface, drops to 10 at depth 110+
        ambient = max(10, 230 - depth * 2)
        radius = max(70, 220 - depth)

        self._light_surf.fill((ambient, ambient, ambient))

        px = int(player.x - self.cam_x) + PLAYER_W // 2
        py = int(player.y - self.cam_y) + PLAYER_H // 2

        step = 5
        for r in range(radius, 0, -step):
            ratio = r / radius
            brightness = int(ambient + (255 - ambient) * (1 - ratio ** 0.6))
            brightness = min(255, brightness)
            pygame.draw.circle(self._light_surf, (brightness, brightness, brightness), (px, py), r)

        self.screen.blit(self._light_surf, (0, 0), special_flags=pygame.BLEND_MULT)

    # ------------------------------------------------------------------
    # Mini-map
    # ------------------------------------------------------------------

    def _build_mm_color_table(self):
        table = [(30, 28, 38)] * 256
        for bid, bdata in BLOCKS.items():
            if 0 <= bid < 256:
                col = bdata.get("color")
                table[bid] = col if col else (0, 0, 0)
        return table

    def _rebuild_minimap(self, world):
        W, H = world.width, world.height
        raw = pygame.Surface((W, H))
        ctable = self._mm_ctable
        mapped = [raw.map_rgb(*ctable[i]) for i in range(256)]
        pa = pygame.PixelArray(raw)
        for y in range(H):
            row = world.grid[y]
            for x in range(W):
                pa[x][y] = mapped[row[x]]
        del pa
        self._minimap_surf = pygame.transform.scale(raw, (_MM_W, _MM_H))

    def draw_minimap(self, world, player, dt):
        if not self.minimap_visible:
            return
        self._minimap_timer -= dt
        if self._minimap_surf is None or self._minimap_timer <= 0:
            self._rebuild_minimap(world)
            self._minimap_timer = 3.0

        mx = SCREEN_W - _MM_W - _MM_MARGIN
        my = SCREEN_H - _MM_H - 58 - _MM_MARGIN

        pygame.draw.rect(self.screen, (12, 10, 18), (mx - 4, my - 4, _MM_W + 8, _MM_H + 8))
        self.screen.blit(self._minimap_surf, (mx, my))
        pygame.draw.rect(self.screen, (65, 65, 75), (mx - 4, my - 4, _MM_W + 8, _MM_H + 8), 1)

        vx = int(self.cam_x / BLOCK_SIZE * _MM_W / world.width)
        vy = int(self.cam_y / BLOCK_SIZE * _MM_H / world.height)
        vw = max(2, int(SCREEN_W / BLOCK_SIZE * _MM_W / world.width))
        vh = max(2, int(SCREEN_H / BLOCK_SIZE * _MM_H / world.height))
        vx = max(0, min(_MM_W - 1, vx))
        vy = max(0, min(_MM_H - 1, vy))
        pygame.draw.rect(self.screen, (220, 215, 50), (mx + vx, my + vy, vw, vh), 1)

        px_map = int(player.x / BLOCK_SIZE * _MM_W / world.width)
        py_map = int(player.y / BLOCK_SIZE * _MM_H / world.height)
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
