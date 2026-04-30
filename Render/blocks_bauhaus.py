import pygame
import math
from blocks import BLOCKS
from blocks import *  # all block ID constants
from constants import BLOCK_SIZE
from Render.block_helpers import _darken, _lighter

# Steel frame colour shared by all glass blocks
_STEEL = (68, 76, 82)
_STEEL_LT = (90, 100, 108)


def _glass(c, s):
    """Base glass surface: light fill + diagonal reflection + 1px steel edge."""
    s.fill(c)
    lt = _lighter(c, 28)
    pygame.draw.line(s, lt, (3, 1), (BLOCK_SIZE - 2, BLOCK_SIZE - 4), 2)
    pygame.draw.line(s, lt, (2, 6), (10, 2), 1)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)


def _steel_bevel(c, s):
    """Base steel surface: fill + lighter top/left bevel, darker bottom/right."""
    s.fill(c)
    lt = _lighter(c, 18)
    dk = _darken(c, 18)
    pygame.draw.line(s, lt, (0, 0), (BLOCK_SIZE - 1, 0), 1)
    pygame.draw.line(s, lt, (0, 0), (0, BLOCK_SIZE - 1), 1)
    pygame.draw.line(s, dk, (BLOCK_SIZE - 1, 0), (BLOCK_SIZE - 1, BLOCK_SIZE - 1), 1)
    pygame.draw.line(s, dk, (0, BLOCK_SIZE - 1), (BLOCK_SIZE - 1, BLOCK_SIZE - 1), 1)


def build_bauhaus_surfs():
    surfs = {}
    BS = BLOCK_SIZE

    # ── BAUHAUS GLASS ────────────────────────────────────────────────────────

    bid = BAUHAUS_PLATE_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _glass(c, s)
    surfs[bid] = s

    bid = BAUHAUS_STRIP_WINDOW
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _glass(c, s)
    h1, h2 = BS // 3, 2 * BS // 3
    pygame.draw.line(s, _STEEL, (0, h1), (BS, h1), 2)
    pygame.draw.line(s, _STEEL, (0, h2), (BS, h2), 2)
    surfs[bid] = s

    bid = BAUHAUS_CORNER_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _glass(c, s)
    pygame.draw.line(s, _STEEL, (0, BS - 1), (BS - 1, 0), 2)
    surfs[bid] = s

    bid = BAUHAUS_CURTAIN_WALL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    pygame.draw.line(s, lt, (3, 1), (BS - 2, BS - 4), 1)
    # 2×3 steel grid
    mx = BS // 2
    for hy in (BS // 3, 2 * BS // 3):
        pygame.draw.line(s, _STEEL, (0, hy), (BS, hy), 1)
    pygame.draw.line(s, _STEEL, (mx, 0), (mx, BS), 1)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_GLASS_BRICK
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 20)
    # mortar grid: 2x2 glass bricks
    for line_x in (BS // 2,):
        pygame.draw.line(s, _STEEL, (line_x, 0), (line_x, BS), 2)
    for line_y in (BS // 2,):
        pygame.draw.line(s, _STEEL, (0, line_y), (BS, line_y), 2)
    # inner highlight on each brick
    for bx, by in ((2, 2), (BS // 2 + 2, 2), (2, BS // 2 + 2), (BS // 2 + 2, BS // 2 + 2)):
        pygame.draw.line(s, lt, (bx, by), (bx + BS // 2 - 5, by), 1)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_FROSTED_STRIP
    s = pygame.Surface((BS, BS))
    c = _lighter(BLOCKS[bid]["color"], 8)
    s.fill(c)
    lt = _lighter(c, 18)
    for y in range(4, BS, 8):
        pygame.draw.line(s, lt, (1, y), (BS - 2, y), 1)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_TINTED_STRIP
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    pygame.draw.line(s, lt, (2, 4), (BS - 3, 4), 2)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    for bid, highlight_amt in (
        (BAUHAUS_RED_PANEL, 30),
        (BAUHAUS_YELLOW_PANEL, 35),
        (BAUHAUS_BLUE_PANEL, 25),
    ):
        s = pygame.Surface((BS, BS))
        c = BLOCKS[bid]["color"]
        s.fill(c)
        lt = _lighter(c, highlight_amt)
        pygame.draw.line(s, lt, (2, 2), (BS - 3, 2), 1)
        pygame.draw.line(s, lt, (2, 2), (2, BS - 3), 1)
        pygame.draw.rect(s, _darken(c, 30), s.get_rect(), 1)
        surfs[bid] = s

    bid = BAUHAUS_BLACK_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 40)
    pygame.draw.line(s, lt, (2, 2), (BS - 3, BS - 5), 2)
    pygame.draw.rect(s, (50, 55, 60), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_WHITE_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    pygame.draw.line(s, _lighter(c, 8), (3, 2), (BS - 3, BS - 4), 1)
    pygame.draw.rect(s, (180, 185, 190), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_WIRE_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 18)
    pygame.draw.line(s, lt, (3, 1), (BS - 2, BS - 4), 1)
    wire = _darken(c, 40)
    for i in range(0, BS + BS, 8):
        pygame.draw.line(s, wire, (i, 0), (i - BS, BS), 1)
        pygame.draw.line(s, wire, (0, i), (BS, i - BS), 1)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CHANNEL_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 22)
    dk = _darken(c, 18)
    rib_w = BS // 6
    for i in range(6):
        col = lt if i % 2 == 0 else c
        pygame.draw.rect(s, col, (i * rib_w, 0, rib_w, BS))
        pygame.draw.line(s, dk, (i * rib_w, 0), (i * rib_w, BS), 1)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_SANDBLAST_GLASS
    s = pygame.Surface((BS, BS))
    c = _lighter(BLOCKS[bid]["color"], 6)
    s.fill(c)
    dk = _darken(c, 12)
    import random as _r
    _r.seed(bid)
    for _ in range(60):
        px, py = _r.randint(1, BS - 2), _r.randint(1, BS - 2)
        pygame.draw.rect(s, dk, (px, py, 1, 1))
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_ETCHED_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _glass(c, s)
    etch = _darken(c, 28)
    cx, cy, r = BS // 2, BS // 2, BS // 2 - 4
    pygame.draw.circle(s, etch, (cx, cy), r, 1)
    pygame.draw.rect(s, etch, (4, 4, BS - 8, BS - 8), 1)
    surfs[bid] = s

    bid = BAUHAUS_DOUBLE_PANE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 20)
    pygame.draw.line(s, lt, (3, 1), (BS - 3, BS - 4), 1)
    gap = _darken(c, 20)
    pygame.draw.rect(s, gap, s.get_rect(), 2)
    pygame.draw.rect(s, c, (3, 3, BS - 6, BS - 6))
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_GLASS_FLOOR
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 25)
    pygame.draw.line(s, lt, (1, BS - 3), (BS - 2, 2), 2)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CLERESTORY
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _glass(c, s)
    sill_y = 3 * BS // 4
    pygame.draw.line(s, _STEEL, (0, sill_y), (BS, sill_y), 3)
    pygame.draw.line(s, _STEEL, (0, 3), (BS, 3), 3)
    surfs[bid] = s

    bid = BAUHAUS_GREENHOUSE_PANE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 15)
    pygame.draw.line(s, lt, (3, 1), (BS - 2, BS - 4), 1)
    pygame.draw.line(s, _STEEL, (BS // 2, 0), (BS // 2, BS), 1)
    pygame.draw.line(s, _STEEL, (0, BS // 2), (BS, BS // 2), 1)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_FRAMELESS_WALL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    pygame.draw.line(s, lt, (3, 1), (BS - 2, BS - 4), 2)
    surfs[bid] = s  # deliberately no frame

    bid = BAUHAUS_CANOPY_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 25)
    # angled highlight suggesting slope
    pygame.draw.line(s, lt, (0, 2), (BS, 8), 3)
    pygame.draw.line(s, lt, (0, 6), (BS, 12), 1)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_SKYLIGHT
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _glass(c, s)
    pygame.draw.line(s, _STEEL, (BS // 2, 0), (BS // 2, BS), 2)
    pygame.draw.line(s, _STEEL, (0, BS // 2), (BS, BS // 2), 2)
    for bx, by in ((2, 2), (BS - 4, 2), (2, BS - 4), (BS - 4, BS - 4)):
        pygame.draw.rect(s, _STEEL, (bx, by, 3, 3))
    surfs[bid] = s

    bid = BAUHAUS_JALOUSIE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 10))
    lt = _lighter(c, 12)
    dk = _darken(c, 22)
    slat_h = BS // 5
    for i in range(4):
        y = 2 + i * (slat_h + 1)
        pygame.draw.rect(s, lt, (2, y, BS - 4, slat_h - 1))
        pygame.draw.line(s, dk, (2, y + slat_h - 1), (BS - 3, y + slat_h - 1), 1)
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_OPAQUE_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 14)
    import random as _r
    _r.seed(bid)
    for _ in range(25):
        px, py = _r.randint(1, BS - 2), _r.randint(1, BS - 2)
        pygame.draw.rect(s, dk, (px, py, 2, 1))
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_RIBBED_VERT
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    rib_w = BS // 6
    for i in range(6):
        col = lt if i % 2 == 0 else c
        pygame.draw.rect(s, col, (i * rib_w, 0, rib_w, BS))
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_RIBBED_HORIZ
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    rib_h = BS // 6
    for i in range(6):
        col = lt if i % 2 == 0 else c
        pygame.draw.rect(s, col, (0, i * rib_h, BS, rib_h))
    pygame.draw.rect(s, _STEEL, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_MIRROR_PANEL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 35)
    dk = _darken(c, 20)
    pygame.draw.line(s, lt, (0, 0), (BS, BS), 4)
    pygame.draw.line(s, lt, (0, 4), (BS - 4, BS), 2)
    pygame.draw.line(s, dk, (4, 0), (BS, BS - 4), 1)
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_PRISM_GLASS
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _glass(c, s)
    # subtle refraction bands near top-left
    pygame.draw.line(s, (200, 80, 80),  (6, 2), (14, 10), 1)
    pygame.draw.line(s, (80, 180, 80),  (8, 2), (16, 10), 1)
    pygame.draw.line(s, (80, 120, 200), (10, 2), (18, 10), 1)
    surfs[bid] = s

    bid = BAUHAUS_SPANDREL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    pygame.draw.rect(s, _lighter(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    # ── STEEL & METAL STRUCTURAL ─────────────────────────────────────────────

    bid = STEEL_I_BEAM
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    flange_h = 4
    web_w = 6
    cx = BS // 2
    # top flange
    pygame.draw.rect(s, lt, (2, 2, BS - 4, flange_h))
    # bottom flange
    pygame.draw.rect(s, lt, (2, BS - flange_h - 2, BS - 4, flange_h))
    # web
    pygame.draw.rect(s, dk, (cx - web_w // 2, flange_h + 2, web_w, BS - 2 * flange_h - 4))
    surfs[bid] = s

    bid = STEEL_H_COLUMN
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    flange_w = 4
    web_h = 6
    cy = BS // 2
    pygame.draw.rect(s, lt, (2, 2, flange_w, BS - 4))
    pygame.draw.rect(s, lt, (BS - flange_w - 2, 2, flange_w, BS - 4))
    pygame.draw.rect(s, dk, (flange_w + 2, cy - web_h // 2, BS - 2 * flange_w - 4, web_h))
    surfs[bid] = s

    bid = STEEL_ANGLE_BRACE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 18)
    # L-shape bottom-left
    pygame.draw.rect(s, lt, (2, 2, 5, BS - 4))   # vertical leg
    pygame.draw.rect(s, lt, (2, BS - 7, BS - 4, 5))  # horizontal leg
    surfs[bid] = s

    bid = STEEL_MESH_PANEL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    dk = _darken(c, 30)
    for gx in range(4, BS - 2, 6):
        for gy in range(4, BS - 2, 6):
            pygame.draw.rect(s, dk, (gx, gy, 3, 3))
    surfs[bid] = s

    bid = STEEL_GRATE_FLOOR
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    dk = _darken(c, 35)
    lt = _lighter(c, 10)
    for y in range(3, BS - 2, 5):
        pygame.draw.rect(s, lt, (2, y, BS - 4, 3))
        pygame.draw.line(s, dk, (2, y + 3), (BS - 3, y + 3), 1)
    surfs[bid] = s

    bid = STEEL_STAIR_TREAD
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    dk = _darken(c, 25)
    lt = _lighter(c, 15)
    for i in range(0, BS, 4):
        for j in range(0, BS, 4):
            if (i // 4 + j // 4) % 2 == 0:
                pygame.draw.rect(s, lt, (i, j, 4, 4))
            else:
                pygame.draw.rect(s, dk, (i, j, 3, 3))
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = STEEL_RAILING_POST
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 22)
    dk = _darken(c, 20)
    post_w = 6
    cx = BS // 2
    pygame.draw.rect(s, dk, (cx - post_w // 2, 4, post_w, BS - 8))
    pygame.draw.line(s, lt, (cx - post_w // 2 + 1, 5), (cx - post_w // 2 + 1, BS - 9), 1)
    pygame.draw.rect(s, lt, (2, 2, BS - 4, 4))
    pygame.draw.rect(s, lt, (2, BS - 6, BS - 4, 4))
    surfs[bid] = s

    bid = STEEL_CABLE_RAIL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 25)
    dk = _darken(c, 15)
    for y in (7, 13, 19, 25):
        pygame.draw.line(s, lt, (2, y), (BS - 3, y), 1)
        pygame.draw.line(s, dk, (2, y + 1), (BS - 3, y + 1), 1)
    surfs[bid] = s

    bid = STEEL_PERFORATED
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    hole = _darken(c, 40)
    for px in range(4, BS - 2, 5):
        for py in range(4, BS - 2, 5):
            pygame.draw.circle(s, hole, (px, py), 1)
    surfs[bid] = s

    bid = CORRUGATED_STEEL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    dk = _darken(c, 22)
    ridge_h = 4
    for i, y in enumerate(range(0, BS, ridge_h)):
        col = lt if i % 2 == 0 else dk
        pygame.draw.rect(s, col, (0, y, BS, ridge_h))
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = ALUMINUM_CLADDING
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 20)
    dk = _darken(c, 10)
    for y in range(0, BS, 3):
        pygame.draw.line(s, lt, (1, y), (BS - 2, y), 1)
        pygame.draw.line(s, dk, (1, y + 1), (BS - 2, y + 1), 1)
    pygame.draw.line(s, _lighter(c, 40), (2, 2), (BS - 3, 2), 1)
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = CHROME_TRIM
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 40)
    dk = _darken(c, 25)
    pygame.draw.rect(s, dk, (0, 0, BS, BS // 4))
    pygame.draw.rect(s, lt, (0, BS // 4, BS, BS // 2))
    pygame.draw.rect(s, dk, (0, 3 * BS // 4, BS, BS // 4))
    pygame.draw.line(s, _lighter(c, 55), (1, BS // 4 + 1), (BS - 2, BS // 4 + 1), 1)
    surfs[bid] = s

    bid = STEEL_DOOR_FRAME
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    dk = _darken(c, 30)
    pygame.draw.rect(s, dk, (3, 3, BS - 6, BS - 6), 3)
    surfs[bid] = s

    bid = STEEL_WINDOW_FRAME
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    dk = _darken(c, 25)
    pygame.draw.rect(s, dk, (4, 4, BS - 8, BS - 8), 2)
    surfs[bid] = s

    bid = STEEL_LOUVER
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    dk = _darken(c, 28)
    slat_h = BS // 5 - 1
    for i in range(5):
        y = 2 + i * (slat_h + 2)
        pygame.draw.rect(s, lt, (2, y, BS - 4, slat_h))
        pygame.draw.line(s, dk, (2, y + slat_h), (BS - 3, y + slat_h), 1)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = STEEL_SOFFIT
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    dk = _darken(c, 18)
    pygame.draw.line(s, dk, (4, BS // 2), (BS - 5, BS // 2), 1)
    surfs[bid] = s

    bid = STEEL_FASCIA
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    dk = _darken(c, 20)
    pygame.draw.rect(s, lt, (0, 0, BS, 4))
    pygame.draw.rect(s, dk, (0, BS - 4, BS, 4))
    pygame.draw.line(s, lt, (1, 1), (BS - 2, 1), 1)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = STEEL_BALCONY_DECK
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 15)
    dk = _darken(c, 18)
    for y in range(4, BS - 2, 5):
        pygame.draw.rect(s, lt, (2, y, BS - 4, 3))
        pygame.draw.line(s, dk, (2, y + 3), (BS - 3, y + 3), 1)
    pygame.draw.rect(s, dk, (2, BS - 5, BS - 4, 3))
    surfs[bid] = s

    bid = STEEL_SKYLIGHT_FRAME
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 20)
    dk = _darken(c, 22)
    pygame.draw.rect(s, dk, (3, 3, BS - 6, BS - 6), 2)
    # diagonal braces in corners
    pygame.draw.line(s, lt, (5, 5), (10, 10), 1)
    pygame.draw.line(s, lt, (BS - 6, 5), (BS - 11, 10), 1)
    pygame.draw.line(s, lt, (5, BS - 6), (10, BS - 11), 1)
    pygame.draw.line(s, lt, (BS - 6, BS - 6), (BS - 11, BS - 11), 1)
    surfs[bid] = s

    bid = ROUND_PIPE_COLUMN
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 10))
    lt = _lighter(c, 28)
    dk = _darken(c, 28)
    r = BS // 2 - 3
    pygame.draw.circle(s, c, (BS // 2, BS // 2), r)
    pygame.draw.circle(s, lt, (BS // 2 - r // 3, BS // 2 - r // 3), r // 3)
    pygame.draw.circle(s, dk, (BS // 2, BS // 2), r, 1)
    surfs[bid] = s

    bid = ROUND_PIPE_HORIZ
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 10))
    lt = _lighter(c, 28)
    dk = _darken(c, 28)
    r = BS // 4
    cy = BS // 2
    pygame.draw.ellipse(s, c, (2, cy - r, BS - 4, r * 2))
    pygame.draw.ellipse(s, lt, (4, cy - r + 2, (BS - 8) // 2, r // 2))
    pygame.draw.ellipse(s, dk, (2, cy - r, BS - 4, r * 2), 1)
    surfs[bid] = s

    bid = STEEL_GRID_CEILING
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    dk = _darken(c, 22)
    lt = _lighter(c, 12)
    grid = 8
    for x in range(0, BS, grid):
        pygame.draw.line(s, dk, (x, 0), (x, BS), 1)
        pygame.draw.line(s, lt, (x + 1, 0), (x + 1, BS), 1)
    for y in range(0, BS, grid):
        pygame.draw.line(s, dk, (0, y), (BS, y), 1)
        pygame.draw.line(s, lt, (0, y + 1), (BS, y + 1), 1)
    surfs[bid] = s

    bid = INDUSTRIAL_BRACKET
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 20)
    dk = _darken(c, 25)
    # Back plate
    pygame.draw.rect(s, dk, (2, 2, 8, BS - 4))
    # Horizontal arm
    pygame.draw.rect(s, lt, (10, BS // 2 - 3, BS - 12, 6))
    # Bolt dots
    for by in (5, BS - 7):
        pygame.draw.circle(s, lt, (6, by), 2)
    surfs[bid] = s

    bid = STEEL_THRESHOLD
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 22)
    pygame.draw.rect(s, lt, (2, BS // 2 - 3, BS - 4, 6))
    pygame.draw.line(s, _darken(c, 20), (2, BS // 2 - 3), (BS - 3, BS // 2 - 3), 1)
    surfs[bid] = s

    bid = RIVETED_STEEL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    _steel_bevel(c, s)
    lt = _lighter(c, 25)
    dk = _darken(c, 20)
    for rx in range(5, BS - 2, 8):
        for ry in range(5, BS - 2, 8):
            pygame.draw.circle(s, dk, (rx, ry), 2)
            pygame.draw.circle(s, lt, (rx - 1, ry - 1), 1)
    surfs[bid] = s

    # ── CONCRETE ─────────────────────────────────────────────────────────────

    bid = BAUHAUS_CONCRETE_SMOOTH
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 10)
    pygame.draw.rect(s, lt, (0, 0, BS, 2))
    pygame.draw.rect(s, lt, (0, 0, 2, BS))
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_BOARD
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 14)
    lt = _lighter(c, 8)
    import random as _r
    _r.seed(bid)
    for x in range(0, BS, 4):
        offset = _r.randint(-1, 1)
        col = lt if x % 8 == 0 else dk
        pygame.draw.line(s, col, (x + offset, 0), (x + offset, BS), 1)
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_POLISHED
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    pygame.draw.line(s, lt, (0, 0), (BS, BS), 3)
    pygame.draw.line(s, lt, (0, 6), (BS - 6, BS), 1)
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_WHITE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_CHARCOAL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 20)
    pygame.draw.line(s, lt, (1, 1), (BS - 2, 1), 1)
    pygame.draw.line(s, lt, (1, 1), (1, BS - 2), 1)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_WARM
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 12)
    import random as _r
    _r.seed(bid)
    for _ in range(20):
        px, py = _r.randint(1, BS - 2), _r.randint(1, BS - 2)
        pygame.draw.rect(s, lt, (px, py, 2, 1))
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_PILLAR
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 8))
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    r = BS // 2 - 2
    pygame.draw.circle(s, c, (BS // 2, BS // 2), r)
    pygame.draw.line(s, lt, (BS // 2 - r // 2, 2), (BS // 2 - r // 2, BS - 3), 1)
    pygame.draw.circle(s, dk, (BS // 2, BS // 2), r, 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_CEILING
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 18)
    for y in range(0, BS, 8):
        pygame.draw.line(s, dk, (0, y), (BS, y), 1)
    for x in range(0, BS, 8):
        pygame.draw.line(s, dk, (x, 0), (x, BS), 1)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_FASCIA
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    pygame.draw.rect(s, dk, (0, 0, BS, 3))
    pygame.draw.line(s, lt, (0, 3), (BS, 3), 1)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_SCREEN
    s = pygame.Surface((BS, BS))
    bg = _darken(BLOCKS[bid]["color"], 25)
    s.fill(bg)
    c = BLOCKS[bid]["color"]
    hole = _darken(c, 40)
    cell = BS // 3
    for gx in range(3):
        for gy in range(3):
            inner = 3
            pygame.draw.rect(s, c, (gx * cell, gy * cell, cell, cell))
            pygame.draw.rect(s, hole, (gx * cell + inner, gy * cell + inner,
                                       cell - inner * 2, cell - inner * 2))
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_CURB
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 14)
    dk = _darken(c, 18)
    pygame.draw.rect(s, lt, (0, 0, BS, BS // 3))
    pygame.draw.line(s, dk, (0, BS // 3), (BS, BS // 3), 2)
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_SILL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 16)
    dk = _darken(c, 20)
    sill_y = BS // 2 + 2
    pygame.draw.rect(s, lt, (1, sill_y, BS - 2, BS // 3))
    pygame.draw.line(s, dk, (1, sill_y), (BS - 2, sill_y), 2)
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_EXPOSED_AGGREGATE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    import random as _r
    _r.seed(bid)
    pebble_cols = [
        _darken(c, 25), _lighter(c, 20), (155, 140, 120), (140, 130, 115), (170, 160, 145),
    ]
    for _ in range(55):
        px = _r.randint(1, BS - 3)
        py = _r.randint(1, BS - 3)
        col = pebble_cols[_r.randint(0, len(pebble_cols) - 1)]
        w = _r.randint(2, 4)
        h = _r.randint(2, 3)
        pygame.draw.ellipse(s, col, (px, py, w, h))
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_POURED_FLOOR
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 16)
    pygame.draw.line(s, lt, (0, 2), (BS, 10), 2)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_PRECAST_PANEL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    for y in (BS // 3, 2 * BS // 3):
        pygame.draw.line(s, dk, (2, y), (BS - 3, y), 2)
        pygame.draw.line(s, _lighter(c, 10), (2, y + 2), (BS - 3, y + 2), 1)
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CEILING_COFFER
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 10)
    coffer = BS // 2 - 2
    for cx2, cy2 in ((3, 3), (BS // 2 + 1, 3), (3, BS // 2 + 1), (BS // 2 + 1, BS // 2 + 1)):
        pygame.draw.rect(s, dk, (cx2, cy2, coffer, coffer), 2)
        pygame.draw.line(s, lt, (cx2 + 1, cy2 + 1), (cx2 + coffer - 2, cy2 + 1), 1)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_THIN_SHELL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 18)
    dk = _darken(c, 18)
    pygame.draw.arc(s, lt, (2, 0, BS - 4, BS - 6), 0, math.pi, 4)
    pygame.draw.arc(s, dk, (4, 2, BS - 8, BS - 8), 0, math.pi, 2)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_STAIR_TREAD
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 8))
    lt = _lighter(c, 14)
    dk = _darken(c, 20)
    step_h = BS // 4
    step_w = BS // 4
    for i in range(4):
        pygame.draw.rect(s, lt, (i * step_w, BS - (i + 1) * step_h, BS - i * step_w, step_h))
        pygame.draw.line(s, dk, (i * step_w, BS - (i + 1) * step_h,), (BS, BS - (i + 1) * step_h), 1)
    surfs[bid] = s

    bid = BAUHAUS_HEARTH
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 14)
    opening = _darken(c, 55)
    pygame.draw.rect(s, lt, (2, 2, BS - 4, BS // 3))
    pygame.draw.rect(s, opening, (6, BS // 3, BS - 12, BS // 2))
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_CONCRETE_MOSAIC
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    import random as _r
    _r.seed(bid)
    chip_cols = [(198, 48, 38), (238, 208, 28), (28, 78, 178), _lighter(c, 20), _darken(c, 20)]
    for _ in range(40):
        px = _r.randint(1, BS - 3)
        py = _r.randint(1, BS - 3)
        col = chip_cols[_r.randint(0, len(chip_cols) - 1)]
        pygame.draw.rect(s, col, (px, py, 2, 2))
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    # ── WOOD & NATURAL TRIM ───────────────────────────────────────────────────

    bid = TEAK_SLAT_WALL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 10))
    lt = _lighter(c, 14)
    dk = _darken(c, 20)
    slat_h = BS // 5
    for i in range(5):
        y = i * slat_h
        pygame.draw.rect(s, lt if i % 2 == 0 else c, (1, y + 1, BS - 2, slat_h - 2))
        pygame.draw.line(s, dk, (1, y + slat_h - 1), (BS - 2, y + slat_h - 1), 1)
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = WALNUT_STRIP_FLOOR
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 12)
    dk = _darken(c, 14)
    strip_h = 4
    for i, y in enumerate(range(0, BS, strip_h)):
        col = lt if i % 2 == 0 else dk
        pygame.draw.line(s, col, (0, y), (BS, y), 1)
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = BIRCH_VENEER_PANEL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 14)
    import random as _r
    _r.seed(bid)
    for y in range(0, BS, 3):
        amt = _r.randint(-4, 4)
        pygame.draw.line(s, dk, (0, y), (BS, y + amt), 1)
    pygame.draw.rect(s, _darken(c, 16), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAMBOO_CEILING_BATTEN
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 10))
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    bw = 6
    for x in range(0, BS, bw + 1):
        pygame.draw.rect(s, c, (x, 1, bw, BS - 2))
        pygame.draw.line(s, lt, (x + 1, 1), (x + 1, BS - 2), 1)
        pygame.draw.line(s, dk, (x + bw - 1, 1), (x + bw - 1, BS - 2), 1)
    surfs[bid] = s

    bid = CORK_TILE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    import random as _r
    _r.seed(bid)
    dk = _darken(c, 18)
    lt = _lighter(c, 12)
    for _ in range(30):
        x = _r.randint(1, BS - 5)
        y = _r.randint(1, BS - 5)
        w = _r.randint(3, 7)
        h = _r.randint(2, 5)
        col = dk if _r.random() > 0.5 else lt
        pygame.draw.rect(s, col, (x, y, w, h), 1)
    pygame.draw.rect(s, _darken(c, 16), s.get_rect(), 1)
    surfs[bid] = s

    bid = MAPLE_STRIP_FLOOR
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 14)
    dk = _darken(c, 10)
    for i, y in enumerate(range(0, BS, 4)):
        pygame.draw.line(s, lt if i % 2 == 0 else dk, (0, y), (BS, y), 1)
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = WHITEWASH_PLANK
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 18)
    import random as _r
    _r.seed(bid)
    for y in range(0, BS, 5):
        pygame.draw.line(s, dk, (0, y), (BS, y), 1)
        for _ in range(3):
            gx = _r.randint(0, BS - 1)
            pygame.draw.line(s, dk, (gx, y), (gx, y + 4), 1)
    pygame.draw.rect(s, _darken(c, 16), s.get_rect(), 1)
    surfs[bid] = s

    bid = SMOKED_OAK_PANEL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 16)
    for y in range(0, BS, 4):
        pygame.draw.line(s, lt, (1, y), (BS - 2, y), 1)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = ASH_VENEER
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 12)
    import random as _r
    _r.seed(bid)
    for y in range(0, BS, 3):
        off = _r.randint(-2, 2)
        pygame.draw.line(s, dk, (0, y), (BS, y + off), 1)
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = TEAK_DECK_BOARD
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 12)
    dk = _darken(c, 18)
    board_h = 5
    for i, y in enumerate(range(0, BS, board_h + 1)):
        pygame.draw.rect(s, lt if i % 2 == 0 else c, (1, y, BS - 2, board_h))
        pygame.draw.line(s, dk, (1, y + board_h), (BS - 2, y + board_h), 1)
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = WENGE_ACCENT
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    for y in range(0, BS, 5):
        pygame.draw.line(s, lt, (1, y), (BS - 2, y), 1)
    pygame.draw.rect(s, (20, 14, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = ZEBRANO_PANEL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 35)
    lt = _lighter(c, 20)
    stripe_w = 4
    for i in range(BS // stripe_w + 1):
        col = dk if i % 2 == 0 else lt
        # diagonal stripe
        points = [
            (i * stripe_w, 0),
            (i * stripe_w + stripe_w, 0),
            (i * stripe_w + stripe_w - BS, BS),
            (i * stripe_w - BS, BS),
        ]
        valid = [(x, y) for x, y in points if 0 <= x <= BS]
        pygame.draw.polygon(s, col, points)
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = RECLAIMED_PINE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 18)
    lt = _lighter(c, 10)
    import random as _r
    _r.seed(bid)
    for y in range(0, BS, 5):
        pygame.draw.line(s, dk, (0, y), (BS, y), 1)
    for _ in range(4):
        kx = _r.randint(3, BS - 5)
        ky = _r.randint(3, BS - 5)
        pygame.draw.ellipse(s, dk, (kx, ky, 5, 4))
        pygame.draw.ellipse(s, lt, (kx + 1, ky + 1, 3, 2))
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = REED_SCREEN_PANEL
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 10))
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    reed_w = 3
    for x in range(0, BS, reed_w + 1):
        pygame.draw.rect(s, c, (x, 1, reed_w, BS - 2))
        pygame.draw.line(s, lt, (x, 1), (x, BS - 2), 1)
        pygame.draw.line(s, dk, (x + reed_w - 1, 1), (x + reed_w - 1, BS - 2), 1)
    surfs[bid] = s

    bid = HEMP_BOARD
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 14)
    lt = _lighter(c, 10)
    import random as _r
    _r.seed(bid)
    for y in range(0, BS, 3):
        pygame.draw.line(s, dk if _r.random() > 0.5 else lt, (0, y), (BS, y), 1)
    for x in range(0, BS, 6):
        pygame.draw.line(s, dk, (x, 0), (x, BS), 1)
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    # ── TILE, FLOOR & BAUHAUS COLOR ───────────────────────────────────────────

    bid = BLACK_CERAMIC_TILE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 55)
    # gloss highlight dot top-left
    pygame.draw.circle(s, lt, (5, 5), 3)
    pygame.draw.rect(s, _lighter(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = WHITE_PORCELAIN_TILE
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 18)
    lt = _lighter(c, 8)
    # grout lines
    pygame.draw.line(s, dk, (BS // 2, 0), (BS // 2, BS), 1)
    pygame.draw.line(s, dk, (0, BS // 2), (BS, BS // 2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    # gloss highlights on each tile
    for tx, ty in ((2, 2), (BS // 2 + 2, 2), (2, BS // 2 + 2), (BS // 2 + 2, BS // 2 + 2)):
        pygame.draw.rect(s, lt, (tx, ty, 4, 2))
    surfs[bid] = s

    bid = BAUHAUS_MOSAIC_TILE
    s = pygame.Surface((BS, BS))
    c = (200, 50, 40)   # red background
    s.fill(c)
    # yellow circle
    pygame.draw.circle(s, (238, 208, 28), (BS // 2, BS // 2), BS // 3 - 1)
    # blue triangle
    cx2 = BS // 2
    pygame.draw.polygon(s, (28, 78, 178), [
        (cx2, 4),
        (cx2 - 10, BS - 5),
        (cx2 + 10, BS - 5),
    ])
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = CHECKER_TILE
    s = pygame.Surface((BS, BS))
    half = BS // 2
    s.fill((240, 238, 235))
    black = (28, 28, 30)
    pygame.draw.rect(s, black, (0, 0, half, half))
    pygame.draw.rect(s, black, (half, half, BS - half, BS - half))
    pygame.draw.rect(s, (100, 100, 100), s.get_rect(), 1)
    surfs[bid] = s

    bid = BAUHAUS_TERRAZZO
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    import random as _r
    _r.seed(bid)
    chip_cols = [
        (218, 233, 245), (200, 50, 40), (238, 208, 28), (28, 78, 178),
        _lighter(c, 25), _darken(c, 20),
    ]
    for _ in range(50):
        px = _r.randint(1, BS - 3)
        py = _r.randint(1, BS - 3)
        col = chip_cols[_r.randint(0, len(chip_cols) - 1)]
        w = _r.randint(1, 3)
        h = _r.randint(1, 2)
        pygame.draw.rect(s, col, (px, py, w, h))
    pygame.draw.rect(s, _darken(c, 16), s.get_rect(), 1)
    surfs[bid] = s

    for bid, texture_lt in (
        (BAUHAUS_RED_WALL, 22),
        (BAUHAUS_YELLOW_WALL, 28),
        (BAUHAUS_BLUE_WALL, 20),
    ):
        s = pygame.Surface((BS, BS))
        c = BLOCKS[bid]["color"]
        s.fill(c)
        lt = _lighter(c, texture_lt)
        for y in (BS // 4, BS // 2, 3 * BS // 4):
            pygame.draw.line(s, lt, (2, y), (BS - 3, y), 1)
        pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
        surfs[bid] = s

    bid = WHITE_STUCCO
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 12)
    import random as _r
    _r.seed(bid)
    for _ in range(45):
        px = _r.randint(1, BS - 2)
        py = _r.randint(1, BS - 2)
        pygame.draw.rect(s, dk, (px, py, 1, 1))
    pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
    surfs[bid] = s

    bid = LIME_PLASTER
    s = pygame.Surface((BS, BS))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 14)
    lt = _lighter(c, 10)
    import random as _r
    _r.seed(bid)
    for _ in range(6):
        y = _r.randint(1, BS - 2)
        x1 = _r.randint(0, BS // 2)
        x2 = _r.randint(BS // 2, BS - 1)
        pygame.draw.line(s, dk if _r.random() > 0.5 else lt, (x1, y), (x2, y), 1)
    pygame.draw.rect(s, _darken(c, 16), s.get_rect(), 1)
    surfs[bid] = s

    return surfs
