import pygame
import math
import random as _rnd
from blocks import BLOCKS
from blocks import *  # all block ID constants
from constants import BLOCK_SIZE
from Render.block_helpers import _darken, _lighter, _tinted, _MSTYLES, CAVE_MUSHROOMS, render_mushroom_preview


def build_decor_surfs():
    surfs = {}
    bid = ORANGE_TREE_PLANTER
    # if bid == ORANGE_TREE_PLANTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    tc = (175, 80, 40)
    cb = (42, 88, 172)
    orange = (215, 125, 35)
    green = (45, 118, 55)
    BS = BLOCK_SIZE
    cx2 = BS//2
    pygame.draw.rect(s, (100, 70, 40), (cx2-2, 8, 4, 12))
    pygame.draw.circle(s, green, (cx2, 6), 7)
    pygame.draw.polygon(s, (215, 195, 165), [(4, 20), (6, BS-2), (BS-7, BS-2), (BS-5, 20)])
    pygame.draw.rect(s, tc, (2, 18, BS-4, 4))
    for ox, oy in [(8, 25), (cx2, 26), (BS-9, 25)]:
        pygame.draw.circle(s, orange, (ox, oy), 3)
    pygame.draw.arc(s, cb, (cx2-4, BS-9, 8, 6), 0, math.pi, 1)
    pygame.draw.rect(s, _darken(tc, 18), s.get_rect(), 1)
    surfs[bid] = s

    bid = WAVE_COBBLE
    # if bid == WAVE_COBBLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((195, 192, 182))
    w = (225, 222, 215)
    dk = (148, 145, 135)
    BS = BLOCK_SIZE
    for row in range(4):
        y2 = row * 8 + 2
        x_off = 4 if row % 2 else 0
        for col in range(5):
            wx = col * 7 + x_off - 3
            if 0 <= wx <= BS - 6:
                c2 = w if (row + col) % 2 == 0 else dk
                pygame.draw.ellipse(s, c2, (wx, y2, 6, 5))
    pygame.draw.rect(s, (130, 127, 118), s.get_rect(), 1)
    surfs[bid] = s

    bid = AZULEJO_FACADE_PANEL
    # if bid == AZULEJO_FACADE_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((243, 241, 238))
    cb = (35, 75, 160)
    md = (75, 118, 195)
    BS = BLOCK_SIZE
    cx2 = BS//2
    pygame.draw.rect(s, cb, s.get_rect(), 3)
    for wy in range(BS-9, BS-3):
        pygame.draw.line(s, md, (4, wy), (BS-5, wy), 1)
    pygame.draw.polygon(s, cb, [(cx2-7, 20), (cx2+7, 20), (cx2+9, 26), (cx2-9, 26)])
    pygame.draw.line(s, cb, (cx2, 20), (cx2, 8), 2)
    pygame.draw.polygon(s, md, [(cx2, 8), (cx2+8, 13), (cx2, 20)])
    pygame.draw.polygon(s, md, [(cx2, 10), (cx2-6, 14), (cx2, 20)])
    surfs[bid] = s

    bid = MUDEJAR_BRICK
    # if bid == MUDEJAR_BRICK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    mortar = _darken(c, 40)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    for row in range(5):
        y2 = row * 7 - 2
        for col in range(5):
            bx2 = col * 10 + (5 if row % 2 else 0)
            pts = [(bx2, y2+3), (bx2+8, y2), (bx2+9, y2+3), (bx2+1, y2+6)]
            if all(0 <= p[0] <= BS and 0 <= p[1] <= BS for p in pts):
                pygame.draw.polygon(s, lt, pts)
                pygame.draw.polygon(s, mortar, pts, 1)
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = PORTUGUESE_BENCH
    # if bid == PORTUGUESE_BENCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 25)
    cb = (42, 88, 172)
    BS = BLOCK_SIZE
    pygame.draw.rect(s, (245, 242, 235), (1, 4, BS-2, 10))
    for tx in range(3, BS-2, 7):
        pygame.draw.line(s, cb, (tx, 4), (tx, 14), 1)
    pygame.draw.line(s, cb, (1, 9), (BS-2, 9), 1)
    pygame.draw.rect(s, cb, (1, 4, BS-2, 10), 1)
    pygame.draw.rect(s, c, (3, 14, 8, BS-15))
    pygame.draw.rect(s, c, (BS-11, 14, 8, BS-15))
    pygame.draw.rect(s, dk, (3, 14, 8, BS-15), 1)
    pygame.draw.rect(s, dk, (BS-11, 14, 8, BS-15), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = SPANISH_PATIO_FLOOR
    # if bid == SPANISH_PATIO_FLOOR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = (215, 205, 185)
    s.fill(c)
    dk = (50, 45, 40)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    sq = 5
    for cx2, cy2 in [(0, 0), (BS-sq, 0), (0, BS-sq), (BS-sq, BS-sq)]:
        pygame.draw.rect(s, dk, (cx2, cy2, sq, sq))
    cut = 5
    pts = [(cut,0),(BS-cut,0),(BS,cut),(BS,BS-cut),(BS-cut,BS),(cut,BS),(0,BS-cut),(0,cut)]
    pygame.draw.polygon(s, lt, pts, 1)
    pygame.draw.circle(s, lt, (BS//2, BS//2), 6, 1)
    pygame.draw.rect(s, (165, 155, 138), s.get_rect(), 1)
    surfs[bid] = s

    bid = ARABIC_ROOF_TILE
    # if bid == ARABIC_ROOF_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 16))
    dk = _darken(c, 32)
    lt = _lighter(c, 15)
    BS = BLOCK_SIZE
    for bx2, w2 in [(3, 12), (BS//2+1, 12)]:
        pygame.draw.rect(s, c, (bx2, 2, w2, BS-4))
        pygame.draw.line(s, lt, (bx2+2, 3), (bx2+2, BS-4), 1)
        pygame.draw.line(s, dk, (bx2+w2-1, 3), (bx2+w2-1, BS-4), 1)
        for by2 in range(8, BS-4, 8):
            pygame.draw.line(s, dk, (bx2, by2), (bx2+w2, by2), 1)
    pygame.draw.line(s, dk, (BS//2, 0), (BS//2, BS), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MOORISH_COLUMN_TILE
    # if bid == MOORISH_COLUMN_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((35, 32, 30))
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    cols = [(42,88,172),(40,130,80),(200,162,50),(185,60,55),(230,225,210)]
    r_out = 14
    for i in range(12):
        a1 = 2*math.pi*i/12
        a2 = 2*math.pi*(i+1)/12
        pts = [
            (cx2+int(6*math.cos(a1)), cy2+int(6*math.sin(a1))),
            (cx2+int(r_out*math.cos(a1)), cy2+int(r_out*math.sin(a1))),
            (cx2+int(r_out*math.cos(a2)), cy2+int(r_out*math.sin(a2))),
            (cx2+int(6*math.cos(a2)), cy2+int(6*math.sin(a2))),
        ]
        pygame.draw.polygon(s, cols[i % len(cols)], pts)
    pygame.draw.circle(s, (230, 225, 210), (cx2, cy2), 5)
    pygame.draw.circle(s, (35, 32, 30), (cx2, cy2), 2)
    surfs[bid] = s

    bid = ESTREMOZ_MARBLE
    # if bid == ESTREMOZ_MARBLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 10)
    dk = _darken(c, 18)
    pink = (220, 185, 182)
    BS = BLOCK_SIZE
    pygame.draw.line(s, pink, (4, 2), (BS-2, BS-6), 1)
    pygame.draw.line(s, pink, (2, 10), (14, 2), 1)
    pygame.draw.line(s, pink, (BS-8, BS-2), (BS-2, BS-10), 1)
    pygame.draw.line(s, lt, (2, 2), (8, 6), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MEZQUITA_ARCH
    # if bid == MEZQUITA_ARCH
    # Iconic alternating red & cream voussoir bands in a horseshoe arch
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    red   = (195, 65, 45)
    cream = (238, 228, 205)
    dk    = (140, 40, 28)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    s.fill((28, 25, 22))
    # draw alternating voussoir wedges radiating from arch center
    for i in range(9):
        a1 = math.pi * i / 8
        a2 = math.pi * (i + 1) / 8
        c2 = red if i % 2 == 0 else cream
        pts = [
            (cx2 + int(14 * math.cos(math.pi - a1)), 16 + int(14 * math.sin(math.pi - a1))),
            (cx2 + int(14 * math.cos(math.pi - a2)), 16 + int(14 * math.sin(math.pi - a2))),
            (cx2 + int(6  * math.cos(math.pi - a2)), 16 + int(6  * math.sin(math.pi - a2))),
            (cx2 + int(6  * math.cos(math.pi - a1)), 16 + int(6  * math.sin(math.pi - a1))),
        ]
        pygame.draw.polygon(s, c2, pts)
        pygame.draw.polygon(s, dk, pts, 1)
    # column stubs
    pygame.draw.rect(s, cream, (2, 16, 5, BS-17))
    pygame.draw.rect(s, cream, (BS-7, 16, 5, BS-17))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MIHRAB_TILE
    # if bid == MIHRAB_TILE
    # Golden tessera mosaic panel — rich gold/amber ground with blue border gems
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    gold  = (200, 162, 50)
    dk_g  = (150, 110, 25)
    blue  = (42, 88, 172)
    ivory = (245, 240, 215)
    BS = BLOCK_SIZE
    s.fill(gold)
    # tessera grid
    for gx in range(2, BS-1, 4):
        for gy in range(2, BS-1, 4):
            pygame.draw.rect(s, dk_g, (gx, gy, 3, 3), 1)
    # inner arch niche
    cx2 = BS // 2
    pygame.draw.arc(s, blue, (4, 4, BS-8, 18), 0, math.pi, 2)
    pygame.draw.rect(s, ivory, (4, 13, BS-8, BS-17))
    # blue gem border dots
    for bx2 in range(5, BS-4, 5):
        pygame.draw.circle(s, blue, (bx2, 2), 2)
        pygame.draw.circle(s, blue, (bx2, BS-3), 2)
    for by2 in range(5, BS-4, 5):
        pygame.draw.circle(s, blue, (2, by2), 2)
        pygame.draw.circle(s, blue, (BS-3, by2), 2)
    surfs[bid] = s

    bid = MEDINA_AZAHARA_STONE
    # if bid == MEDINA_AZAHARA_STONE
    # White marble with carved acanthus scrollwork in relief
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    # central acanthus flower
    pygame.draw.circle(s, dk, (cx2, cy2), 7, 1)
    pygame.draw.circle(s, lt, (cx2, cy2), 3)
    # leaf scrolls in 4 quadrants
    for ax, ay, start, end in [
        (8, 8, 0, math.pi/2),
        (BS-9, 8, math.pi/2, math.pi),
        (BS-9, BS-9, math.pi, 3*math.pi/2),
        (8, BS-9, 3*math.pi/2, 2*math.pi),
    ]:
        pygame.draw.arc(s, dk, (ax-4, ay-4, 8, 8), start, end, 2)
    # feathered border
    for i in range(3, BS-2, 5):
        pygame.draw.line(s, dk, (i, 1), (i+2, 4), 1)
        pygame.draw.line(s, dk, (i, BS-2), (i+2, BS-5), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CORDOBA_COLUMN
    # if bid == CORDOBA_COLUMN
    # Slender Umayyad column — white shaft, decorated capital, torus base
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 12))
    lt = _lighter(c, 15)
    dk = _darken(c, 30)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # shaft
    pygame.draw.rect(s, c, (cx2-4, 8, 8, BS-16))
    pygame.draw.line(s, lt, (cx2-3, 9), (cx2-3, BS-8), 1)
    # capital (flared top)
    pygame.draw.polygon(s, c, [(cx2-4, 8), (cx2+4, 8), (cx2+7, 3), (cx2-7, 3)])
    pygame.draw.line(s, lt, (cx2-6, 3), (cx2+6, 3), 1)
    # volute detail on capital
    pygame.draw.arc(s, dk, (cx2-7, 2, 6, 6), 0, math.pi, 1)
    pygame.draw.arc(s, dk, (cx2+1, 2, 6, 6), 0, math.pi, 1)
    # torus base
    pygame.draw.ellipse(s, c, (cx2-7, BS-10, 14, 6))
    pygame.draw.ellipse(s, lt, (cx2-6, BS-10, 12, 4), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = ORANGE_COURT_FLOOR
    # if bid == ORANGE_COURT_FLOOR
    # Court of Oranges paving — stone grid with small orange-tree dot accents
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 10)
    orange = (210, 120, 30)
    green  = (55, 110, 50)
    BS = BLOCK_SIZE
    # stone slab grid (2×2)
    h = BS // 2
    pygame.draw.line(s, dk, (h, 0), (h, BS), 2)
    pygame.draw.line(s, dk, (0, h), (BS, h), 2)
    # highlight per slab
    for qx, qy in [(2, 2), (h+2, 2), (2, h+2), (h+2, h+2)]:
        pygame.draw.line(s, lt, (qx, qy), (qx+6, qy), 1)
    # orange tree motif in each quadrant
    for qx, qy in [(h//2, h//2), (h+h//2, h//2), (h//2, h+h//2), (h+h//2, h+h//2)]:
        pygame.draw.circle(s, green, (qx, qy-2), 3)
        pygame.draw.circle(s, orange, (qx, qy-2), 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = CORDOBAN_LEATHER
    # if bid == CORDOBAN_LEATHER
    # Embossed guadamecil: warm brown with gold stamped floral roundels
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    gold  = (195, 152, 38)
    lt_g  = (220, 185, 80)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    # tooled border
    pygame.draw.rect(s, gold, s.get_rect(), 2)
    pygame.draw.rect(s, gold, (4, 4, BS-8, BS-8), 1)
    # central embossed roundel
    pygame.draw.circle(s, gold, (cx2, cy2), 8, 1)
    pygame.draw.circle(s, lt_g, (cx2, cy2), 4)
    # corner pressed rosettes
    for pcx, pcy in [(7, 7), (BS-8, 7), (7, BS-8), (BS-8, BS-8)]:
        pygame.draw.circle(s, gold, (pcx, pcy), 4, 1)
        pygame.draw.circle(s, lt_g, (pcx, pcy), 2)
    surfs[bid] = s

    bid = UMAYYAD_MULTILOBED
    # if bid == UMAYYAD_MULTILOBED
    # Multi-lobed (polyfoil) Umayyad arch — stone background, pale arch shape
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 20))
    lt = _lighter(c, 12)
    dk = _darken(c, 35)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # draw 5 lobes along the arch using small circles
    lobe_y = 14
    for i in range(5):
        a = math.pi * i / 4
        lx = cx2 + int(10 * math.cos(math.pi - a))
        ly = lobe_y + int(10 * math.sin(math.pi - a))
        pygame.draw.circle(s, c, (lx, ly), 5)
        pygame.draw.circle(s, lt, (lx, ly), 3, 1)
    # column stubs
    pygame.draw.rect(s, c, (2, lobe_y, 5, BS-lobe_y-1))
    pygame.draw.rect(s, c, (BS-7, lobe_y, 5, BS-lobe_y-1))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GOLD_TESSERA_PANEL
    # if bid == GOLD_TESSERA_PANEL
    # Byzantine/Umayyad gold tessera mosaic — rich golden ground, jewel accents
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    gold  = (205, 165, 45)
    dk_g  = (148, 110, 20)
    blue  = (42, 88, 172)
    red2  = (175, 55, 45)
    BS = BLOCK_SIZE
    s.fill(gold)
    # tessera lines
    for gx in range(1, BS, 3):
        pygame.draw.line(s, dk_g, (gx, 0), (gx, BS), 1)
    for gy in range(1, BS, 3):
        pygame.draw.line(s, dk_g, (0, gy), (BS, gy), 1)
    # jewel accent strip at top
    pygame.draw.rect(s, dk_g, (0, 0, BS, 6))
    for bx2 in range(3, BS-2, 6):
        pygame.draw.circle(s, blue, (bx2, 3), 2)
        pygame.draw.circle(s, red2, (bx2+3, 3), 1)
    # cross motif
    cx2, cy2 = BS//2, BS//2
    pygame.draw.rect(s, dk_g, (cx2-1, 8, 2, BS-16))
    pygame.draw.rect(s, dk_g, (8, cy2-1, BS-16, 2))
    surfs[bid] = s

    bid = UMAYYAD_DOME_RIB
    # if bid == UMAYYAD_DOME_RIB
    # Stone dome rib section — pale stone with protruding ribs radiating from corner
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 10))
    lt = _lighter(c, 18)
    dk = _darken(c, 28)
    BS = BLOCK_SIZE
    # radiating ribs from bottom-center (dome apex below)
    origin = (BS//2, BS)
    for i in range(5):
        a = math.pi * (i + 1) / 6
        ex = origin[0] + int(BS * 1.2 * math.cos(a))
        ey = origin[1] - int(BS * 1.2 * math.sin(a))
        pygame.draw.line(s, c, origin, (ex, ey), 4)
        pygame.draw.line(s, lt, origin, (ex, ey), 1)
    # coffers between ribs (small recessed squares)
    for i in range(4):
        a = math.pi * (i + 1.5) / 6
        rx = origin[0] + int(12 * math.cos(a))
        ry = origin[1] - int(12 * math.sin(a))
        pygame.draw.circle(s, dk, (rx, ry), 3)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = KUFIC_PANEL
    # if bid == KUFIC_PANEL
    # Carved Kufic calligraphy — stone with angular geometric letter-forms
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 35)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    pygame.draw.rect(s, dk, (2, 2, BS-4, BS-4), 1)
    # horizontal base line
    pygame.draw.rect(s, dk, (3, BS//2+3, BS-6, 2))
    # angular letter-form blocks rising from baseline
    glyphs = [(3,6),(4,10),(8,4),(9,8),(14,5),(15,9),(20,6),(21,10),(25,4),(26,8)]
    for gx, gh in glyphs:
        pygame.draw.rect(s, dk, (gx, BS//2+5-gh, 3, gh))
    # horizontal connectors
    pygame.draw.rect(s, dk, (4, BS//2-5, 6, 2))
    pygame.draw.rect(s, dk, (14, BS//2-4, 7, 2))
    pygame.draw.rect(s, dk, (24, BS//2-3, 4, 2))
    surfs[bid] = s

    bid = PATIO_FLOWER_WALL
    # if bid == PATIO_FLOWER_WALL
    # Whitewashed wall with hanging ceramic pots and geranium flowers
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    white = BLOCKS[bid]["color"]
    s.fill(white)
    pot   = (175, 85, 42)
    red2  = (195, 50, 45)
    green = (50, 110, 48)
    BS = BLOCK_SIZE
    # iron bracket lines
    for px2 in [6, 17, 26]:
        pygame.draw.line(s, (60, 55, 50), (px2, 3), (px2, 10), 1)
    # ceramic pots
    for px2 in [5, 16, 24]:
        pygame.draw.ellipse(s, pot, (px2, 10, 6, 7))
        pygame.draw.rect(s, _darken(pot, 15), (px2+1, 10, 4, 2))
        # flowers
        for fx in [-2, 0, 2]:
            pygame.draw.circle(s, red2, (px2+3+fx, 8), 2)
        pygame.draw.circle(s, green, (px2+3, 9), 1)
    # wall texture — subtle lime wash
    for wy in range(22, BS-2, 6):
        pygame.draw.line(s, _darken(white, 8), (2, wy), (BS-3, wy), 1)
    pygame.draw.rect(s, _darken(white, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = CORDOBAN_PATIO_TILE
    # if bid == CORDOBAN_PATIO_TILE
    # Small geometric patio tile — cream with 4-way interlocking star pattern
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 28)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    # 4-pointed compass rose
    for a in [0, math.pi/2, math.pi, 3*math.pi/2]:
        px2 = cx2 + int(10 * math.cos(a))
        py2 = cy2 + int(10 * math.sin(a))
        pygame.draw.line(s, dk, (cx2, cy2), (px2, py2), 2)
    # interlocking squares
    pygame.draw.rect(s, dk, (cx2-4, cy2-4, 8, 8), 1)
    rot_pts = [(cx2, cy2-7), (cx2+7, cy2), (cx2, cy2+7), (cx2-7, cy2)]
    pygame.draw.polygon(s, dk, rot_pts, 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = STAR_VAULT_PANEL
    # if bid == STAR_VAULT_PANEL
    # 8-pointed star Umayyad ceiling vault — dark stone with pale star ribs
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 25))
    lt = _lighter(c, 20)
    dk = _darken(c, 35)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    # 8-pointed star outline (two overlapping squares)
    r = 12
    for rot in [0, math.pi/4]:
        pts = [(cx2 + int(r * math.cos(math.pi/2 + math.pi*i/2 + rot)),
                cy2 + int(r * math.sin(math.pi/2 + math.pi*i/2 + rot)))
               for i in range(4)]
        pygame.draw.polygon(s, lt, pts, 2)
    # ribs from center to each star point
    r2 = 13
    for i in range(8):
        a = math.pi * i / 4
        pygame.draw.line(s, lt, (cx2, cy2),
                         (cx2+int(r2*math.cos(a)), cy2+int(r2*math.sin(a))), 1)
    pygame.draw.circle(s, lt, (cx2, cy2), 3)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = ANDALUSIAN_FOUNTAIN
    # if bid == ANDALUSIAN_FOUNTAIN
    # Small Cordoban courtyard basin fountain — blue/white tiled bowl
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((215, 210, 198))
    blue  = (65, 140, 190)
    lt_b  = (110, 175, 215)
    white = (245, 242, 238)
    dk    = (45, 42, 38)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    # basin bowl
    pygame.draw.ellipse(s, blue, (3, cy2-2, BS-6, BS//2))
    pygame.draw.ellipse(s, lt_b, (5, cy2, BS-10, BS//2-6))
    # water ripple lines
    for ry in range(cy2+4, BS-6, 4):
        pygame.draw.line(s, white, (8, ry), (BS-9, ry), 1)
    # rim tiles
    pygame.draw.ellipse(s, white, (2, cy2-4, BS-4, 8))
    for bx2 in range(5, BS-4, 5):
        pygame.draw.line(s, blue, (bx2, cy2-3), (bx2, cy2+3), 1)
    # spout / jet
    pygame.draw.line(s, lt_b, (cx2, cy2-2), (cx2, cy2-8), 2)
    pygame.draw.circle(s, lt_b, (cx2, cy2-10), 3)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = NASRID_HONEYCOMB
    # if bid == NASRID_HONEYCOMB
    # Honeycomb muqarnas ceiling — warm stone with regular hexagonal cells
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 18))
    lt = _lighter(c, 22)
    dk = _darken(c, 35)
    BS = BLOCK_SIZE
    # draw hex cells using flat-top hexagons at 32×32 scale
    for row in range(4):
        for col in range(4):
            hx = col * 9 + (4 if row % 2 else 0)
            hy = row * 8 + 4
            pts = [
                (hx+3, hy), (hx+6, hy), (hx+8, hy+3),
                (hx+6, hy+6), (hx+3, hy+6), (hx+1, hy+3),
            ]
            pygame.draw.polygon(s, c, pts)
            pygame.draw.polygon(s, lt, pts, 1)
            pygame.draw.circle(s, lt, (hx+4, hy+3), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GARDEN_STAR_TILE
    # if bid == GARDEN_STAR_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 28)
    cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
    o, i2 = 7, 4
    pygame.draw.rect(s, lt, (cx2-i2, cy2-o, i2*2, o*2))
    pygame.draw.rect(s, lt, (cx2-o, cy2-i2, o*2, i2*2))
    dd = 5
    for dx2, dy2 in [(-dd, -dd), (dd, -dd), (-dd, dd), (dd, dd)]:
        pygame.draw.rect(s, lt, (cx2+dx2-2, cy2+dy2-2, 4, 4))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = GEOMETRIC_MOSAIC
    # if bid == GEOMETRIC_MOSAIC
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    cols = [c, _darken(c, 22), _lighter(c, 18), _darken(c, 10)]
    pygame.draw.polygon(s, cols[0], [(0,0), (BS,0), (BS//2, BS//2)])
    pygame.draw.polygon(s, cols[1], [(BS,0), (BS,BS), (BS//2, BS//2)])
    pygame.draw.polygon(s, cols[2], [(0,BS), (BS,BS), (BS//2, BS//2)])
    pygame.draw.polygon(s, cols[3], [(0,0), (0,BS), (BS//2, BS//2)])
    pygame.draw.rect(s, _darken(c, 30), s.get_rect(), 1)
    surfs[bid] = s

    bid = WATER_CHANNEL
    # if bid == WATER_CHANNEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 20))
    lt = _lighter(c, 20)
    pygame.draw.rect(s, c, (2, BLOCK_SIZE//2-4, BLOCK_SIZE-4, 8))
    for ry in [BLOCK_SIZE//2-2, BLOCK_SIZE//2, BLOCK_SIZE//2+2]:
        pygame.draw.line(s, lt, (4, ry), (BLOCK_SIZE-5, ry), 1)
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = ORNAMENTAL_POOL
    # if bid == ORNAMENTAL_POOL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 15))
    lt = _lighter(c, 18)
    cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
    pygame.draw.ellipse(s, c, (2, 4, BLOCK_SIZE-4, BLOCK_SIZE-8))
    for r2 in [10, 7, 4]:
        pygame.draw.ellipse(s, lt, (cx2-r2, cy2-r2+1, r2*2, r2*2-2), 1)
    pygame.draw.rect(s, _darken(c, 30), s.get_rect(), 1)
    surfs[bid] = s

    bid = FOUNTAIN_BASIN
    # if bid == FOUNTAIN_BASIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 20)
    water = (80, 155, 200)
    pygame.draw.rect(s, lt, (2, 2, BLOCK_SIZE-4, BLOCK_SIZE//2-2))
    pygame.draw.rect(s, dk, (1, BLOCK_SIZE//2, BLOCK_SIZE-2, BLOCK_SIZE//2-1))
    pygame.draw.ellipse(s, water, (5, 16, BLOCK_SIZE-10, 10))
    pygame.draw.line(s, _lighter(water, 20), (BLOCK_SIZE//2, 14), (BLOCK_SIZE//2, 8), 1)
    pygame.draw.circle(s, (220, 235, 255), (BLOCK_SIZE//2, 7), 2)
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = TIERED_FOUNTAIN
    # if bid == TIERED_FOUNTAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 10))
    water = (80, 155, 200)
    pygame.draw.ellipse(s, c, (8, 2, 16, 6))
    pygame.draw.ellipse(s, _darken(c, 15), (8, 2, 16, 6), 1)
    pygame.draw.ellipse(s, c, (4, 16, 24, 8))
    pygame.draw.ellipse(s, _darken(c, 15), (4, 16, 24, 8), 1)
    pygame.draw.ellipse(s, water, (9, 3, 14, 4))
    pygame.draw.ellipse(s, water, (5, 17, 22, 6))
    pygame.draw.rect(s, c, (13, 8, 6, 8))
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = HORSESHOE_ARCH
    # if bid == HORSESHOE_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 25)
    lt = _lighter(c, 10)
    inside = _darken(c, 45)
    s.fill(c)
    ax, aw = 6, BLOCK_SIZE - 12
    at = 6
    pygame.draw.rect(s, inside, (ax+1, at+aw//2, aw-2, BLOCK_SIZE - at - aw//2 - 2))
    pygame.draw.arc(s, dk, (ax, at, aw, aw), 0, math.pi, 3)
    pygame.draw.line(s, dk, (ax, at+aw//2), (ax, BLOCK_SIZE-2), 3)
    pygame.draw.line(s, dk, (ax+aw, at+aw//2), (ax+aw, BLOCK_SIZE-2), 3)
    pygame.draw.line(s, lt, (1, 2), (BLOCK_SIZE-2, 2), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = MUQARNAS_PANEL
    # if bid == MUQARNAS_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 28)
    for row in range(3):
        for col in range(4):
            cx2 = col * 8 + (4 if row % 2 else 0)
            cy2 = row * 9 + 3
            pygame.draw.arc(s, dk, (cx2-1, cy2, 8, 8), 0, math.pi, 2)
            pygame.draw.line(s, dk, (cx2-1, cy2+4), (cx2-1, cy2+8), 1)
            pygame.draw.line(s, dk, (cx2+7, cy2+4), (cx2+7, cy2+8), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = ARABESQUE_SCREEN
    # if bid == ARABESQUE_SCREEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 50)
    BS = BLOCK_SIZE
    half = BS // 2
    for dx2, dy2 in [(half//2, half//2), (half+half//2, half//2),
                     (half//2, half+half//2), (half+half//2, half+half//2)]:
        d = 5
        pts = [(dx2, dy2-d), (dx2+d, dy2), (dx2, dy2+d), (dx2-d, dy2)]
        pygame.draw.polygon(s, dk, pts)
    pygame.draw.line(s, _darken(c, 15), (0, half), (BS, half), 1)
    pygame.draw.line(s, _darken(c, 15), (half, 0), (half, BS), 1)
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = GARDEN_COLUMN
    # if bid == GARDEN_COLUMN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 25)
    lt = _lighter(c, 15)
    BS = BLOCK_SIZE
    pygame.draw.rect(s, dk, (1, 1, BS-2, 4))
    pygame.draw.line(s, lt, (1, 2), (BS-2, 2), 1)
    pygame.draw.rect(s, dk, (1, BS-5, BS-2, 4))
    pygame.draw.line(s, lt, (1, BS-4), (BS-2, BS-4), 1)
    for fx in [5, 10, 15, 20, 25]:
        pygame.draw.line(s, dk, (fx, 5), (fx, BS-5), 1)
        pygame.draw.line(s, lt, (fx+1, 5), (fx+1, BS-5), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = MARBLE_PLINTH
    # if bid == MARBLE_PLINTH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 20)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    pygame.draw.rect(s, dk, (0, 0, BS, 3))
    pygame.draw.line(s, lt, (0, 3), (BS, 3), 1)
    pygame.draw.rect(s, dk, (0, BS-3, BS, 3))
    pygame.draw.line(s, lt, (0, BS-4), (BS, BS-4), 1)
    pygame.draw.rect(s, _darken(c, 12), (3, 6, BS-6, BS-12))
    pygame.draw.rect(s, lt, (3, 6, BS-6, BS-12), 1)
    surfs[bid] = s

    bid = GARDEN_OBELISK
    # if bid == GARDEN_OBELISK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 30))
    lt = _lighter(c, 12)
    dk = _darken(c, 15)
    BS = BLOCK_SIZE
    pts = [(BS//2-5, BS-2), (BS//2+5, BS-2), (BS//2+2, 3), (BS//2-2, 3)]
    pygame.draw.polygon(s, c, pts)
    pygame.draw.polygon(s, lt, [(BS//2-2, 3), (BS//2+2, 3), (BS//2, 1)])
    for ly in [8, 14, 20, 26]:
        pygame.draw.line(s, dk, (BS//2-4, ly), (BS//2+4, ly), 1)
    pygame.draw.line(s, lt, (BS//2-1, 4), (BS//2-4, BS-3), 1)
    surfs[bid] = s

    bid = TOPIARY_CONE
    # if bid == TOPIARY_CONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    trunk = (100, 65, 35)
    pygame.draw.rect(s, trunk, (BS//2-2, BS-6, 4, 6))
    pygame.draw.polygon(s, dk, [(BS//2, 1), (BS-3, BS-6), (2, BS-6)])
    pygame.draw.polygon(s, c, [(BS//2, 1), (BS//2-3, BS//2), (4, BS-6)])
    for ty in range(10, BS-6, 5):
        half_w = max(1, (ty - 1) * (BS//2 - 4) // BS)
        for tx in range(BS//2 - half_w, BS//2 + half_w, 3):
            pygame.draw.rect(s, lt, (tx, ty, 2, 1))
    surfs[bid] = s

    bid = TOPIARY_SPHERE
    # if bid == TOPIARY_SPHERE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    trunk = (100, 65, 35)
    pygame.draw.rect(s, trunk, (BS//2-2, BS-7, 4, 7))
    pygame.draw.circle(s, dk, (BS//2, BS//2-2), BS//2-4)
    pygame.draw.circle(s, c, (BS//2-2, BS//2-4), BS//2-6)
    pygame.draw.circle(s, lt, (BS//2-3, BS//2-6), 3)
    surfs[bid] = s

    bid = BOX_HEDGE
    # if bid == BOX_HEDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    s.fill(c)
    pygame.draw.rect(s, lt, (0, 0, BS, 5))
    for ty in range(0, BS, 4):
        for tx in range(0, BS, 4):
            leaf_c = dk if (tx//4 + ty//4) % 2 == 0 else lt
            pygame.draw.rect(s, leaf_c, (tx+1, ty+1, 2, 2))
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = CLIMBING_ROSE
    # if bid == CLIMBING_ROSE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    trellis = (110, 75, 40)
    pygame.draw.line(s, trellis, (BS//4, 0), (BS//4, BS), 2)
    pygame.draw.line(s, trellis, (3*BS//4, 0), (3*BS//4, BS), 2)
    pygame.draw.line(s, trellis, (0, BS//3), (BS, BS//3), 2)
    pygame.draw.line(s, trellis, (0, 2*BS//3), (BS, 2*BS//3), 2)
    rose = (200, 70, 90)
    for rx, ry in [(5, 5), (20, 10), (12, 20), (26, 25), (6, 27)]:
        pygame.draw.circle(s, rose, (rx, ry), 3)
        pygame.draw.circle(s, _darken(rose, 20), (rx, ry), 2)
    surfs[bid] = s

    bid = STONE_BENCH
    # if bid == STONE_BENCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 30))
    pygame.draw.rect(s, c, (1, BS//2-3, BS-2, 6))
    pygame.draw.line(s, lt, (1, BS//2-3), (BS-2, BS//2-3), 1)
    pygame.draw.rect(s, dk, (3, BS//2+3, 5, BS//2-4))
    pygame.draw.rect(s, dk, (BS-8, BS//2+3, 5, BS//2-4))
    pygame.draw.line(s, lt, (4, BS//2+3), (4, BS-5), 1)
    surfs[bid] = s

    bid = STONE_URN
    # if bid == STONE_URN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    pygame.draw.rect(s, dk, (BS//2-4, BS-5, 8, 5))
    pygame.draw.ellipse(s, c, (4, BS//2-2, BS-8, 14))
    pygame.draw.ellipse(s, lt, (5, BS//2-1, BS-10, 5))
    pygame.draw.rect(s, dk, (BS//2-3, BS//2-8, 6, 6))
    pygame.draw.rect(s, c, (BS//2-6, BS//2-11, 12, 4))
    pygame.draw.line(s, lt, (BS//2-5, BS//2-11), (BS//2+5, BS//2-11), 1)
    surfs[bid] = s

    bid = TERRACOTTA_PLANTER
    # if bid == TERRACOTTA_PLANTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    pts = [(4, BS-3), (BS-4, BS-3), (BS-7, BS//2+2), (7, BS//2+2)]
    pygame.draw.polygon(s, c, pts)
    pygame.draw.polygon(s, lt, pts, 1)
    pygame.draw.rect(s, dk, (5, BS//2-1, BS-10, 3))
    pygame.draw.line(s, lt, (5, BS//2-1), (BS-5, BS//2-1), 1)
    pygame.draw.ellipse(s, (80, 55, 35), (7, BS//2-8, BS-14, 7))
    pygame.draw.line(s, (60, 130, 55), (BS//2, BS//2-7), (BS//2, BS//2-12), 1)
    pygame.draw.circle(s, (55, 150, 60), (BS//2-3, BS//2-12), 2)
    pygame.draw.circle(s, (55, 150, 60), (BS//2+3, BS//2-11), 2)
    surfs[bid] = s

    bid = SUNDIAL
    # if bid == SUNDIAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    pygame.draw.rect(s, dk, (BS//2-3, BS//2+2, 6, BS//2-3))
    pygame.draw.rect(s, c, (BS//2-5, BS-5, 10, 5))
    pygame.draw.circle(s, c, (BS//2, BS//2-2), 9)
    pygame.draw.circle(s, lt, (BS//2, BS//2-2), 9, 1)
    pygame.draw.polygon(s, dk, [(BS//2, BS//2-10), (BS//2+8, BS//2-2), (BS//2, BS//2-2)])
    for ai in range(6):
        ang = math.pi * ai / 6 - math.pi / 2
        ex2 = BS//2 + int(7 * math.cos(ang))
        ey2 = BS//2 - 2 + int(7 * math.sin(ang))
        pygame.draw.line(s, dk, (BS//2, BS//2-2), (ex2, ey2), 1)
    surfs[bid] = s

    bid = GARDEN_LANTERN
    # if bid == GARDEN_LANTERN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    amber = (200, 140, 50)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 40))
    pygame.draw.line(s, c, (BS//2, 0), (BS//2, 4), 1)
    cx2, cy2 = BS//2, BS//2+2
    r_lan = 9
    hex_pts = [(cx2 + int(r_lan*math.cos(math.pi*i/3)),
                cy2 + int(r_lan*math.sin(math.pi*i/3))) for i in range(6)]
    pygame.draw.polygon(s, amber, hex_pts)
    pygame.draw.polygon(s, c, hex_pts, 1)
    pygame.draw.circle(s, _lighter(amber, 20), (cx2, cy2), 5)
    pygame.draw.line(s, c, (cx2-5, cy2-r_lan), (cx2+5, cy2-r_lan), 2)
    pygame.draw.line(s, c, (cx2-5, cy2+r_lan), (cx2+5, cy2+r_lan), 2)
    surfs[bid] = s

    bid = GRAVEL_PATH
    # if bid == GRAVEL_PATH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 18)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    dots = [(3,4),(8,2),(14,7),(20,3),(27,5),(5,11),(12,15),(18,10),(25,13),
            (2,19),(9,22),(16,18),(23,24),(6,27),(13,29),(21,26),(28,20),
            (4,16),(10,8),(22,17),(29,11),(7,25),(15,21),(26,7),(1,29)]
    for dx2, dy2 in dots:
        if 0 <= dx2 < BS and 0 <= dy2 < BS:
            pygame.draw.rect(s, dk if (dx2+dy2)%3!=0 else lt, (dx2, dy2, 2, 1))
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = MOSAIC_PATH
    # if bid == MOSAIC_PATH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    half = BS // 2
    cols = [c, _darken(c, 20), _lighter(c, 15), _darken(c, 12), _lighter(c, 8), _darken(c, 30)]
    triangles = [
        [(0,0),(BS,0),(half,half)],
        [(BS,0),(BS,BS),(half,half)],
        [(0,BS),(BS,BS),(half,half)],
        [(0,0),(0,BS),(half,half)],
        [(0,0),(half,0),(0,half)],
        [(half,0),(BS,0),(BS,half)],
    ]
    for i, tri in enumerate(triangles):
        pygame.draw.polygon(s, cols[i], tri)
    pygame.draw.line(s, _darken(c, 35), (0,0), (BS,BS), 1)
    pygame.draw.line(s, _darken(c, 35), (BS,0), (0,BS), 1)
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = TERRACOTTA_PATH
    # if bid == TERRACOTTA_PATH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    grout = _darken(c, 35)
    BS = BLOCK_SIZE
    half = BS // 2
    for tx, ty in [(0,0),(half,0),(0,half),(half,half)]:
        tile_c = c if (tx+ty) % (half*2) == 0 else _darken(c, 8)
        pygame.draw.rect(s, tile_c, (tx+1, ty+1, half-2, half-2))
        pygame.draw.line(s, lt, (tx+1, ty+1), (tx+half-2, ty+1), 1)
    pygame.draw.line(s, grout, (half, 0), (half, BS), 1)
    pygame.draw.line(s, grout, (0, half), (BS, half), 1)
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = COBBLE_CIRCLE
    # if bid == COBBLE_CIRCLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 20))
    cx2, cy2 = BS//2, BS//2
    for i in range(8):
        ang = math.pi * i / 4
        rx = cx2 + int(10 * math.cos(ang))
        ry = cy2 + int(10 * math.sin(ang))
        pygame.draw.ellipse(s, c, (rx-3, ry-2, 6, 4))
        pygame.draw.ellipse(s, lt, (rx-2, ry-1, 4, 2))
    pygame.draw.circle(s, dk, (cx2, cy2), 4)
    pygame.draw.circle(s, c, (cx2, cy2), 3)
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = PERGOLA_POST
    # if bid == PERGOLA_POST
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 40))
    # vertical timber post
    pygame.draw.rect(s, c, (BS//2-3, 0, 6, BS))
    pygame.draw.line(s, lt, (BS//2-2, 0), (BS//2-2, BS), 1)
    pygame.draw.line(s, dk, (BS//2+2, 0), (BS//2+2, BS), 1)
    # horizontal crossbeam at top
    pygame.draw.rect(s, dk, (0, 4, BS, 4))
    pygame.draw.line(s, lt, (0, 4), (BS, 4), 1)
    # vine tendrils
    vine = (55, 110, 45)
    for vy in [8, 14, 20, 26]:
        pygame.draw.line(s, vine, (BS//2+3, vy), (BS//2+8, vy+3), 1)
        pygame.draw.line(s, vine, (BS//2-3, vy+2), (BS//2-8, vy+5), 1)
    surfs[bid] = s

    bid = WISTERIA_ARCH
    # if bid == WISTERIA_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 25)
    lt = _lighter(c, 10)
    wist = (160, 100, 190)
    BS = BLOCK_SIZE
    s.fill(c)
    inside = _darken(c, 40)
    ax, aw = 5, BS - 10
    at = 4
    pygame.draw.rect(s, inside, (ax+2, at+aw//2, aw-4, BS - at - aw//2 - 2))
    pygame.draw.arc(s, dk, (ax, at, aw, aw), 0, math.pi, 3)
    pygame.draw.line(s, dk, (ax, at+aw//2), (ax, BS-2), 3)
    pygame.draw.line(s, dk, (ax+aw, at+aw//2), (ax+aw, BS-2), 3)
    # wisteria clusters hanging from arch
    for wx in range(2, BS-1, 5):
        drop_len = 4 + (wx % 3)
        pygame.draw.line(s, (80, 55, 30), (wx, 5), (wx, 5+drop_len), 1)
        pygame.draw.circle(s, wist, (wx, 5+drop_len+2), 2)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = GARDEN_GATE
    # if bid == GARDEN_GATE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 25)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 50))
    # top and bottom rails
    pygame.draw.rect(s, c, (0, 2, BS, 3))
    pygame.draw.rect(s, c, (0, BS-5, BS, 3))
    pygame.draw.line(s, lt, (0, 2), (BS, 2), 1)
    pygame.draw.line(s, lt, (0, BS-5), (BS, BS-5), 1)
    # vertical bars
    for bx2 in range(3, BS-1, 5):
        pygame.draw.line(s, c, (bx2, 5), (bx2, BS-5), 2)
        # spear tips
        pygame.draw.polygon(s, lt, [(bx2-1, 3), (bx2+2, 3), (bx2, 0)])
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = LOW_GARDEN_WALL
    # if bid == LOW_GARDEN_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(c)
    # coping stone on top
    pygame.draw.rect(s, _lighter(c, 18), (0, 0, BS, 6))
    pygame.draw.line(s, lt, (0, 1), (BS, 1), 1)
    pygame.draw.line(s, dk, (0, 6), (BS, 6), 1)
    # coursed stone below
    for ry in range(7, BS, 6):
        pygame.draw.line(s, dk, (0, ry), (BS, ry), 1)
    for rx in [0, 14, 28]:
        pygame.draw.line(s, dk, (rx, 7), (rx, BS), 1)
    for rx in [7, 21]:
        pygame.draw.line(s, dk, (rx, 13), (rx, BS), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = POOL_COPING
    # if bid == POOL_COPING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    s.fill(c)
    # smooth flat stone with subtle shadow on one edge
    pygame.draw.line(s, lt, (0, 0), (BS, 0), 2)
    pygame.draw.line(s, lt, (0, 0), (0, BS), 2)
    pygame.draw.line(s, dk, (0, BS-2), (BS, BS-2), 2)
    pygame.draw.line(s, dk, (BS-2, 0), (BS-2, BS), 2)
    pygame.draw.rect(s, _darken(c, 12), (4, 4, BS-8, BS-8), 1)
    surfs[bid] = s

    bid = STEPPING_STONE
    # if bid == STEPPING_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    # grass background
    grass = (60, 105, 45)
    s.fill(grass)
    # irregular stone shape using polygon
    stone_pts = [(5, 8), (BS-6, 6), (BS-4, BS-7), (7, BS-5)]
    pygame.draw.polygon(s, c, stone_pts)
    pygame.draw.polygon(s, lt, stone_pts, 1)
    # surface cracks
    pygame.draw.line(s, dk, (10, 14), (17, 20), 1)
    pygame.draw.line(s, dk, (BS-10, 10), (BS-14, 18), 1)
    surfs[bid] = s

    bid = OPUS_VERMICULATUM
    # if bid == OPUS_VERMICULATUM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(c)
    # worm-path: sinuous lines of small dark tessera
    for wy in range(2, BS-1, 5):
        ox2 = (wy // 5) % 4
        for wx in range(0, BS, 2):
            seg_y = wy + int(2 * math.sin((wx + ox2*3) * 0.6))
            if 0 <= seg_y < BS:
                pygame.draw.rect(s, dk, (wx, seg_y, 2, 2))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = PORPHYRY_TILE
    # if bid == PORPHYRY_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    dk = _darken(c, 15)
    BS = BLOCK_SIZE
    s.fill(c)
    # crystal inclusions
    for px2, py2 in [(4,5),(9,14),(17,8),(22,20),(6,24),(28,12),(14,28)]:
        pygame.draw.rect(s, lt, (px2, py2, 2, 2))
    # polished sheen diagonal
    pygame.draw.line(s, _lighter(c, 8), (0, 0), (BS, BS), 3)
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = BRICK_EDGING
    # if bid == BRICK_EDGING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    grout = _darken(c, 38)
    BS = BLOCK_SIZE
    s.fill(grout)
    # soldier course: tall narrow bricks on end
    bw = 5
    for bx2 in range(1, BS, bw+1):
        pygame.draw.rect(s, c, (bx2, 2, bw-1, BS-4))
        pygame.draw.line(s, lt, (bx2, 2), (bx2, BS-4), 1)
    surfs[bid] = s

    bid = SPIRAL_TOPIARY
    # if bid == SPIRAL_TOPIARY
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    trunk = (100, 65, 35)
    pygame.draw.rect(s, trunk, (BS//2-2, BS-6, 4, 6))
    # spiral: draw ellipses that shrink and shift as they go up
    for layer in range(4):
        t = layer / 3.0
        w = int(BS * (0.9 - t * 0.5))
        h = 8
        x2 = (BS - w) // 2
        y2 = BS - 10 - layer * 6
        col = lt if layer % 2 == 0 else dk
        if w > 2 and y2 > 0:
            pygame.draw.ellipse(s, col, (x2, y2, w, h))
            pygame.draw.ellipse(s, c, (x2, y2, w, h), 1)
    surfs[bid] = s

    bid = MAZE_HEDGE
    # if bid == MAZE_HEDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    s.fill(c)
    # very dense, slightly lighter top surface
    pygame.draw.rect(s, lt, (0, 0, BS, 4))
    # deep stipple texture — darker than box hedge to feel taller/denser
    for ty in range(0, BS, 3):
        for tx in range(0, BS, 3):
            if (tx//3 + ty//3) % 2 == 0:
                pygame.draw.rect(s, dk, (tx+1, ty+1, 2, 2))
    # subtle vertical shadow bands
    for sx2 in range(0, BS, 8):
        pygame.draw.line(s, dk, (sx2, 4), (sx2, BS), 1)
    pygame.draw.rect(s, _darken(c, 30), s.get_rect(), 1)
    surfs[bid] = s

    bid = ORNAMENTAL_GRASS
    # if bid == ORNAMENTAL_GRASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (80, 55, 30)
    pygame.draw.rect(s, soil, (0, BS - 6, BS, 6))
    c = BLOCKS[bid]["color"]
    gold = (200, 185, 70)
    cx2 = BS // 2
    base_y = BS - 6
    for i, (dx2, tip_x, tip_y) in enumerate([
        (-8, -14, 2), (-5, -10, 5), (-2, -4, 2),
        (0, 0, 0), (2, 4, 2), (5, 10, 5), (8, 14, 2)
    ]):
        col = gold if i % 2 == 0 else c
        pygame.draw.line(s, col, (cx2 + dx2, base_y), (cx2 + tip_x, base_y - 18 + tip_y), 1)
    surfs[bid] = s

    bid = FLOWERING_SHRUB
    # if bid == FLOWERING_SHRUB
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    dk = _darken(c, 20)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 35))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, dk, (2, 6, BS - 4, BS - 10))
    pygame.draw.ellipse(s, c, (4, 8, BS - 10, BS - 14))
    flower = (230, 130, 165)
    for fx, fy in [(6, 10), (18, 8), (12, 16), (22, 18), (8, 22), (16, 24)]:
        pygame.draw.circle(s, flower, (fx, fy), 2)
        pygame.draw.circle(s, _lighter(flower, 20), (fx, fy), 1)
    surfs[bid] = s

    bid = HOLLY_SHRUB
    # if bid == HOLLY_SHRUB
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    trunk = (80, 55, 30)
    s.fill(_darken(c, 30))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, c, (2, 5, BS - 4, BS - 9))
    for i in range(0, 360, 30):
        r = BS // 2 - 5
        hx = BS // 2 + int(r * math.cos(math.radians(i)))
        hy = BS // 2 - 2 + int(r * math.sin(math.radians(i)))
        pygame.draw.circle(s, lt, (hx, hy), 1)
    berry = (200, 40, 40)
    for bx2, by2 in [(8, 12), (20, 10), (14, 18), (22, 22), (7, 22)]:
        pygame.draw.circle(s, berry, (bx2, by2), 2)
    surfs[bid] = s

    bid = TOPIARY_PEACOCK
    # if bid == TOPIARY_PEACOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, c, (BS//2 - 5, BS - 16, 10, 10))
    pygame.draw.line(s, c, (BS//2, BS - 14), (BS//2 - 2, BS - 22), 3)
    pygame.draw.circle(s, c, (BS//2 - 2, BS - 23), 3)
    for angle in range(-60, 70, 15):
        r = 12
        tx2 = BS//2 + int(r * math.sin(math.radians(angle)))
        ty2 = BS - 18 - int(r * math.cos(math.radians(angle)))
        col = lt if abs(angle) < 30 else dk
        pygame.draw.circle(s, col, (tx2, ty2), 2)
        pygame.draw.line(s, dk, (BS//2, BS - 14), (tx2, ty2), 1)
    surfs[bid] = s

    bid = TOPIARY_BEAR
    # if bid == TOPIARY_BEAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, dk, (BS//2 - 7, BS - 20, 14, 14))
    pygame.draw.ellipse(s, c, (BS//2 - 6, BS - 19, 12, 12))
    pygame.draw.circle(s, dk, (BS//2, BS - 24), 6)
    pygame.draw.circle(s, c, (BS//2, BS - 25), 5)
    pygame.draw.circle(s, c, (BS//2 - 4, BS - 29), 2)
    pygame.draw.circle(s, c, (BS//2 + 4, BS - 29), 2)
    pygame.draw.circle(s, lt, (BS//2 - 1, BS - 23), 2)
    surfs[bid] = s

    bid = TOPIARY_RABBIT
    # if bid == TOPIARY_RABBIT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, dk, (BS//2 - 6, BS - 18, 12, 12))
    pygame.draw.ellipse(s, c, (BS//2 - 5, BS - 17, 10, 10))
    pygame.draw.circle(s, c, (BS//2, BS - 22), 4)
    pygame.draw.ellipse(s, dk, (BS//2 - 5, BS - 32, 4, 10))
    pygame.draw.ellipse(s, c, (BS//2 - 4, BS - 31, 3, 8))
    pygame.draw.ellipse(s, dk, (BS//2 + 2, BS - 32, 4, 10))
    pygame.draw.ellipse(s, c, (BS//2 + 3, BS - 31, 3, 8))
    surfs[bid] = s

    bid = ROSE_BED
    # if bid == ROSE_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    soil = (90, 60, 35)
    s.fill(soil)
    edge = (150, 138, 120)
    pygame.draw.rect(s, edge, (0, BS - 5, BS, 5))
    stem = (50, 90, 45)
    red = (195, 45, 55)
    red_lt = (230, 90, 100)
    for rx, ry in [(5, 8), (13, 5), (21, 7), (7, 18), (16, 16), (24, 19)]:
        pygame.draw.line(s, stem, (rx, BS - 6), (rx, ry + 4), 1)
        pygame.draw.circle(s, red, (rx, ry), 3)
        pygame.draw.circle(s, red_lt, (rx - 1, ry - 1), 1)
    surfs[bid] = s

    bid = TULIP_BED
    # if bid == TULIP_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    soil = (90, 60, 35)
    s.fill(soil)
    edge = (150, 138, 120)
    pygame.draw.rect(s, edge, (0, BS - 5, BS, 5))
    stem = (65, 115, 55)
    tulip_colors = [(220, 60, 65), (240, 185, 50), (90, 100, 195), (230, 120, 170), (50, 165, 75)]
    for i, (tx2, ty2) in enumerate([(4, 6), (11, 4), (18, 7), (8, 17), (20, 15)]):
        pygame.draw.line(s, stem, (tx2, BS - 6), (tx2, ty2 + 5), 1)
        col = tulip_colors[i % len(tulip_colors)]
        pygame.draw.ellipse(s, col, (tx2 - 3, ty2, 6, 6))
        pygame.draw.ellipse(s, _lighter(col, 20), (tx2 - 2, ty2 + 1, 4, 3))
    surfs[bid] = s

    bid = COTTAGE_GARDEN_BED
    # if bid == COTTAGE_GARDEN_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    soil = (85, 58, 32)
    s.fill(soil)
    edge = (120, 108, 90)
    pygame.draw.rect(s, edge, (0, BS - 4, BS, 4))
    stems = (55, 105, 50)
    blooms = [(200, 80, 85), (240, 195, 60), (140, 90, 195), (70, 170, 90), (230, 140, 60)]
    positions = [(3, 18), (8, 10), (13, 6), (18, 14), (23, 8), (27, 17), (5, 24), (20, 22)]
    for i, (px2, py2) in enumerate(positions):
        pygame.draw.line(s, stems, (px2, BS - 5), (px2, py2 + 3), 1)
        pygame.draw.circle(s, blooms[i % len(blooms)], (px2, py2), 2)
    surfs[bid] = s

    bid = CHERUB_FOUNTAIN
    # if bid == CHERUB_FOUNTAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 20)
    water = (80, 155, 200)
    s.fill(_darken(c, 15))
    pygame.draw.rect(s, dk, (4, BS - 6, BS - 8, 6))
    pygame.draw.rect(s, c, (5, BS - 5, BS - 10, 4))
    pygame.draw.ellipse(s, dk, (3, BS - 14, BS - 6, 8))
    pygame.draw.ellipse(s, water, (5, BS - 13, BS - 10, 5))
    pygame.draw.rect(s, c, (BS//2 - 2, BS - 20, 4, 7))
    pygame.draw.ellipse(s, lt, (BS//2 - 4, BS - 27, 8, 7))
    pygame.draw.circle(s, lt, (BS//2, BS - 28), 3)
    pygame.draw.arc(s, lt, (BS//2 - 8, BS - 28, 6, 6), 0, math.pi, 2)
    pygame.draw.arc(s, lt, (BS//2 + 2, BS - 28, 6, 6), 0, math.pi, 2)
    pygame.draw.arc(s, water, (BS//2 - 3, BS - 30, 6, 8), math.pi * 0.2, math.pi * 0.8, 1)
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = LION_HEAD_FOUNTAIN
    # if bid == LION_HEAD_FOUNTAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 20)
    water = (80, 155, 200)
    s.fill(dk)
    pygame.draw.circle(s, _lighter(c, 5), (BS//2, BS//2 - 2), 11)
    pygame.draw.circle(s, lt, (BS//2, BS//2 - 2), 7)
    pygame.draw.circle(s, dk, (BS//2 - 3, BS//2 - 4), 1)
    pygame.draw.circle(s, dk, (BS//2 + 3, BS//2 - 4), 1)
    pygame.draw.circle(s, c, (BS//2, BS//2 - 1), 2)
    pygame.draw.rect(s, dk, (BS//2 - 3, BS//2 + 2, 6, 3))
    for wy in range(BS//2 + 5, BS - 2, 3):
        pygame.draw.circle(s, water, (BS//2, wy), 1)
    pygame.draw.ellipse(s, water, (4, BS - 7, BS - 8, 5))
    pygame.draw.rect(s, _darken(c, 30), s.get_rect(), 1)
    surfs[bid] = s

    bid = MOSAIC_FOUNTAIN
    # if bid == MOSAIC_FOUNTAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    stone = (175, 168, 155)
    water = (80, 155, 200)
    s.fill(_darken(stone, 18))
    pygame.draw.ellipse(s, stone, (1, BS//4, BS - 2, BS - BS//4 - 1))
    pygame.draw.ellipse(s, _darken(stone, 20), (1, BS//4, BS - 2, BS - BS//4 - 1), 2)
    tile_colors = [(220, 60, 65), (240, 195, 50), (50, 130, 200), (55, 160, 80), (190, 80, 190)]
    for ti, angle in enumerate(range(0, 360, 30)):
        mx = BS//2 + int(11 * math.cos(math.radians(angle)))
        my = BS//2 + 2 + int(5 * math.sin(math.radians(angle)))
        pygame.draw.rect(s, tile_colors[ti % len(tile_colors)], (mx - 1, my - 1, 3, 3))
    pygame.draw.ellipse(s, water, (4, BS//4 + 4, BS - 8, BS - BS//4 - 10))
    pygame.draw.line(s, _lighter(water, 25), (BS//2, BS//4 + 2), (BS//2, 4), 1)
    pygame.draw.circle(s, (220, 235, 255), (BS//2, 3), 2)
    pygame.draw.rect(s, _darken(stone, 28), s.get_rect(), 1)
    surfs[bid] = s

    bid = LAVENDER_BED
    # if bid == LAVENDER_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    soil = (90, 60, 35)
    s.fill(soil)
    edge = (150, 138, 120)
    pygame.draw.rect(s, edge, (0, BS - 5, BS, 5))
    stem = (80, 110, 60)
    lav = (160, 110, 210)
    lav_lt = _lighter(lav, 20)
    for lx, ly in [(4, 10), (9, 6), (14, 10), (19, 6), (24, 10)]:
        pygame.draw.line(s, stem, (lx, BS - 6), (lx, ly + 6), 1)
        for dy2 in range(ly, ly + 7, 2):
            pygame.draw.circle(s, lav if dy2 % 4 == 0 else lav_lt, (lx, dy2), 1)
    surfs[bid] = s

    bid = SUNFLOWER_BED
    # if bid == SUNFLOWER_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    soil = (90, 60, 35)
    s.fill(soil)
    edge = (150, 138, 120)
    pygame.draw.rect(s, edge, (0, BS - 5, BS, 5))
    stem = (65, 115, 45)
    petal = (240, 190, 40)
    centre = (90, 55, 20)
    for sx2, sy2 in [(7, 5), (18, 4), (26, 7)]:
        pygame.draw.line(s, stem, (sx2, BS - 6), (sx2, sy2 + 5), 2)
        for ang in range(0, 360, 45):
            px3 = sx2 + int(5 * math.cos(math.radians(ang)))
            py3 = sy2 + int(5 * math.sin(math.radians(ang)))
            pygame.draw.line(s, petal, (sx2, sy2), (px3, py3), 2)
        pygame.draw.circle(s, centre, (sx2, sy2), 3)
    surfs[bid] = s

    bid = DAHLIA_BED
    # if bid == DAHLIA_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    soil = (90, 60, 35)
    s.fill(soil)
    edge = (150, 138, 120)
    pygame.draw.rect(s, edge, (0, BS - 5, BS, 5))
    stem = (65, 115, 45)
    dahlia_colors = [(210, 60, 110), (240, 145, 40), (160, 60, 200), (220, 80, 65), (240, 200, 50)]
    for i, (dx2, dy2) in enumerate([(6, 8), (15, 5), (24, 9), (10, 19), (22, 18)]):
        pygame.draw.line(s, stem, (dx2, BS - 6), (dx2, dy2 + 5), 1)
        col = dahlia_colors[i % len(dahlia_colors)]
        for ang in range(0, 360, 30):
            px3 = dx2 + int(4 * math.cos(math.radians(ang)))
            py3 = dy2 + int(4 * math.sin(math.radians(ang)))
            pygame.draw.line(s, col, (dx2, dy2), (px3, py3), 1)
        pygame.draw.circle(s, _lighter(col, 20), (dx2, dy2), 2)
    surfs[bid] = s

    bid = TOPIARY_SWAN
    # if bid == TOPIARY_SWAN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    # body — large oval leaning right
    pygame.draw.ellipse(s, dk, (BS//2 - 4, BS - 19, 14, 13))
    pygame.draw.ellipse(s, c, (BS//2 - 3, BS - 18, 12, 11))
    # neck curves up-left
    pygame.draw.line(s, dk, (BS//2 + 2, BS - 16), (BS//2 - 4, BS - 26), 4)
    pygame.draw.line(s, c, (BS//2 + 2, BS - 16), (BS//2 - 4, BS - 26), 2)
    # head
    pygame.draw.circle(s, c, (BS//2 - 5, BS - 27), 3)
    # beak hint
    pygame.draw.line(s, _darken(c, 30), (BS//2 - 5, BS - 27), (BS//2 - 9, BS - 27), 1)
    # tail upturn
    pygame.draw.line(s, lt, (BS//2 + 8, BS - 14), (BS//2 + 11, BS - 19), 2)
    surfs[bid] = s

    bid = TOPIARY_FOX
    # if bid == TOPIARY_FOX
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    # body
    pygame.draw.ellipse(s, dk, (BS//2 - 7, BS - 18, 14, 12))
    pygame.draw.ellipse(s, c, (BS//2 - 6, BS - 17, 12, 10))
    # head — slightly pointed snout
    pygame.draw.circle(s, c, (BS//2, BS - 22), 5)
    pygame.draw.polygon(s, c, [(BS//2 - 2, BS - 22), (BS//2 + 2, BS - 22), (BS//2 + 6, BS - 20)])
    # pointed ears
    pygame.draw.polygon(s, dk, [(BS//2 - 4, BS - 26), (BS//2 - 6, BS - 31), (BS//2 - 1, BS - 27)])
    pygame.draw.polygon(s, dk, [(BS//2 + 2, BS - 26), (BS//2 + 5, BS - 31), (BS//2 + 6, BS - 26)])
    # fluffy tail
    pygame.draw.ellipse(s, lt, (BS//2 + 6, BS - 16, 6, 8))
    surfs[bid] = s

    bid = TOPIARY_ELEPHANT
    # if bid == TOPIARY_ELEPHANT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    trunk_col = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk_col, (BS//2 - 2, BS - 6, 4, 6))
    # large body
    pygame.draw.ellipse(s, dk, (BS//2 - 8, BS - 20, 16, 14))
    pygame.draw.ellipse(s, c, (BS//2 - 7, BS - 19, 14, 12))
    # head
    pygame.draw.circle(s, c, (BS//2 - 1, BS - 24), 6)
    # big ears
    pygame.draw.ellipse(s, lt, (BS//2 - 9, BS - 27, 7, 10))
    pygame.draw.ellipse(s, lt, (BS//2 + 3, BS - 27, 7, 10))
    # raised trunk curls up from face
    pygame.draw.arc(s, dk, (BS//2 - 6, BS - 28, 8, 10), math.pi * 1.2, math.pi * 2.2, 3)
    surfs[bid] = s

    bid = PEONY_BUSH
    # if bid == PEONY_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 20)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 35))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    # green foliage base
    pygame.draw.ellipse(s, dk, (2, 10, BS - 4, BS - 14))
    pygame.draw.ellipse(s, c, (4, 12, BS - 10, BS - 18))
    # large fluffy peony blooms
    pink = (235, 120, 160)
    pink_lt = _lighter(pink, 18)
    for fx, fy, r in [(7, 9, 5), (19, 7, 6), (13, 17, 4)]:
        for layer in range(r, 0, -1):
            alpha = 1 if layer == r else 0
            col = pink if layer % 2 == 0 else pink_lt
            pygame.draw.circle(s, col, (fx, fy), layer)
        pygame.draw.circle(s, _lighter(pink_lt, 10), (fx, fy), 1)
    surfs[bid] = s

    bid = FERN_CLUMP
    # if bid == FERN_CLUMP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (75, 52, 28)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 20)
    frond_angles = [-65, -40, -15, 10, 35, 60]
    for ang in frond_angles:
        rad = math.radians(ang - 90)
        length = 14
        ex = BS//2 + int(length * math.cos(rad))
        ey = BS - 5 + int(length * math.sin(rad))
        pygame.draw.line(s, dk, (BS//2, BS - 5), (ex, ey), 1)
        # small leaflets along frond
        for t in range(3, length, 3):
            lx = BS//2 + int(t * math.cos(rad))
            ly = BS - 5 + int(t * math.sin(rad))
            side = math.radians(ang - 90 + 70)
            lx2 = lx + int(3 * math.cos(side))
            ly2 = ly + int(3 * math.sin(side))
            pygame.draw.line(s, c, (lx, ly), (lx2, ly2), 1)
            pygame.draw.line(s, c, (lx, ly), (lx - (lx2 - lx), ly - (ly2 - ly)), 1)
    surfs[bid] = s

    bid = RAISED_GARDEN_BED
    # if bid == RAISED_GARDEN_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    wood = (130, 85, 45)
    wood_lt = _lighter(wood, 12)
    soil = (80, 52, 28)
    s.fill(wood)
    pygame.draw.rect(s, wood_lt, (0, 0, BS, 3))
    pygame.draw.rect(s, _darken(wood, 15), (0, BS - 6, BS, 6))
    pygame.draw.rect(s, soil, (3, 6, BS - 6, BS - 14))
    # plank lines
    for px2 in range(0, BS, 8):
        pygame.draw.line(s, _darken(wood, 20), (px2, 0), (px2, BS), 1)
    # a few plant nubs
    green = (70, 130, 55)
    for gx, gy in [(6, 9), (13, 7), (20, 10), (26, 8)]:
        pygame.draw.circle(s, green, (gx, gy), 2)
    pygame.draw.rect(s, _darken(wood, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = LILY_PAD_POND
    # if bid == LILY_PAD_POND
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    water = (50, 120, 170)
    water_lt = _lighter(water, 15)
    s.fill(water)
    pygame.draw.ellipse(s, water_lt, (2, 4, BS - 4, BS - 8))
    # lily pads
    pad = (45, 130, 60)
    pad_dk = _darken(pad, 20)
    for px2, py2, pr in [(7, 10, 5), (19, 8, 4), (12, 20, 5), (23, 22, 3)]:
        pygame.draw.circle(s, pad_dk, (px2, py2), pr)
        pygame.draw.circle(s, pad, (px2, py2), pr - 1)
        # wedge cut
        pygame.draw.line(s, water, (px2, py2), (px2, py2 - pr), 1)
    # flowers
    for fx, fy, col in [(7, 10, (240, 220, 240)), (19, 8, (250, 180, 90))]:
        pygame.draw.circle(s, col, (fx, fy), 2)
        pygame.draw.circle(s, _lighter(col, 15), (fx, fy), 1)
    surfs[bid] = s

    bid = REED_BLOCK
    # if bid == REED_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (70, 100, 55)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    stalk = (85, 155, 60)
    stalk_dk = _darken(stalk, 18)
    for sx2, sw, sh in [(4, 2, 20), (10, 2, 17), (17, 2, 22), (23, 2, 15), (28, 1, 18)]:
        pygame.draw.rect(s, stalk_dk, (sx2, BS - 5 - sh, sw, sh))
        pygame.draw.rect(s, stalk, (sx2 + 1, BS - 5 - sh, 1, sh))
        # small leaf sprout midway up
        mid = BS - 5 - sh // 2
        pygame.draw.line(s, stalk, (sx2 + sw, mid), (sx2 + sw + 4, mid - 3), 1)
    surfs[bid] = s

    bid = CATTAIL_BLOCK
    # if bid == CATTAIL_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (70, 100, 55)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    stalk = (85, 155, 60)
    stalk_dk = _darken(stalk, 18)
    head = (110, 68, 28)
    head_dk = _darken(head, 15)
    for sx2, sw, sh, has_head in [(3, 2, 22, True), (11, 2, 18, False), (18, 2, 24, True), (25, 2, 16, False)]:
        pygame.draw.rect(s, stalk_dk, (sx2, BS - 5 - sh, sw, sh))
        pygame.draw.rect(s, stalk, (sx2 + 1, BS - 5 - sh, 1, sh))
        if has_head:
            hy = BS - 5 - sh
            pygame.draw.rect(s, head_dk, (sx2 - 1, hy, sw + 2, 7))
            pygame.draw.rect(s, head, (sx2, hy + 1, sw, 5))
    surfs[bid] = s

    bid = BULRUSH_BLOCK
    # if bid == BULRUSH_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (60, 90, 50)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    c = (52, 118, 50)
    dk = _darken(c, 20)
    for sx2, sh in [(3, 19), (8, 15), (14, 21), (19, 17), (24, 14), (28, 18)]:
        pygame.draw.line(s, dk, (sx2, BS - 5), (sx2, BS - 5 - sh), 2)
        pygame.draw.circle(s, dk, (sx2, BS - 5 - sh), 3)
        pygame.draw.circle(s, c, (sx2, BS - 5 - sh), 2)
    surfs[bid] = s

    bid = WATER_CRESS_BLOCK
    # if bid == WATER_CRESS_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (60, 95, 55)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    c = (58, 168, 70)
    dk = _darken(c, 20)
    for lx2, ly2, lr in [(5, BS - 9, 4), (12, BS - 8, 4), (19, BS - 10, 4),
                         (8, BS - 13, 3), (16, BS - 14, 3), (24, BS - 9, 4)]:
        pygame.draw.circle(s, dk, (lx2, ly2), lr)
        pygame.draw.circle(s, c, (lx2, ly2), lr - 1)
        pygame.draw.circle(s, _lighter(c, 15), (lx2, ly2 - 1), 1)
    surfs[bid] = s

    bid = POND_WEED_BLOCK
    # if bid == POND_WEED_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    water = (50, 120, 170)
    water_lt = _lighter(water, 12)
    s.fill(water)
    pygame.draw.ellipse(s, water_lt, (3, 5, BS - 6, BS - 10))
    c = (38, 105, 48)
    lt = _lighter(c, 15)
    for wx2, wy2 in [(4, BS - 8), (9, BS - 5), (16, BS - 9), (21, BS - 6), (26, BS - 10)]:
        pygame.draw.line(s, c, (wx2, BS - 3), (wx2 + 3, wy2), 1)
        pygame.draw.line(s, lt, (wx2 + 1, BS - 3), (wx2 + 4, wy2), 1)
    for wx2, wy2 in [(6, BS - 12), (14, BS - 14), (22, BS - 11)]:
        pygame.draw.ellipse(s, c, (wx2 - 3, wy2 - 2, 6, 4))
        pygame.draw.ellipse(s, lt, (wx2 - 2, wy2 - 1, 4, 2))
    surfs[bid] = s

    bid = WATER_HYACINTH_BLOCK
    # if bid == WATER_HYACINTH_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    water = (50, 118, 168)
    s.fill(water)
    pygame.draw.ellipse(s, _lighter(water, 12), (3, 5, BS - 6, BS - 10))
    pad = (42, 125, 55)
    for px2, py2, pr in [(7, BS - 7, 5), (20, BS - 6, 4), (13, BS - 10, 4)]:
        pygame.draw.circle(s, _darken(pad, 15), (px2, py2), pr)
        pygame.draw.circle(s, pad, (px2, py2), pr - 1)
    violet = (155, 85, 210)
    violet_lt = _lighter(violet, 20)
    for fx, fy in [(7, BS - 15), (14, BS - 18), (21, BS - 14)]:
        for ang in range(0, 360, 60):
            ex = fx + int(4 * math.cos(math.radians(ang)))
            ey = fy + int(4 * math.sin(math.radians(ang)))
            pygame.draw.line(s, violet, (fx, fy), (ex, ey), 1)
        pygame.draw.circle(s, violet_lt, (fx, fy), 2)
    surfs[bid] = s

    bid = DUCKWEED_BLOCK
    # if bid == DUCKWEED_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    water = (48, 115, 165)
    s.fill(water)
    pygame.draw.ellipse(s, _lighter(water, 10), (4, 6, BS - 8, BS - 12))
    c = (52, 138, 50)
    dk = _darken(c, 15)
    for dx2, dy2, dr in [(4, 8, 2), (8, 14, 2), (13, 6, 3), (16, 17, 2),
                         (20, 10, 2), (24, 6, 3), (26, 19, 2), (10, 21, 2)]:
        pygame.draw.circle(s, dk, (dx2, dy2), dr)
        pygame.draw.circle(s, c, (dx2, dy2), dr - 1)
    surfs[bid] = s

    bid = LOTUS_BLOCK
    # if bid == LOTUS_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    water = (48, 115, 168)
    s.fill(water)
    pygame.draw.ellipse(s, _lighter(water, 12), (2, 4, BS - 4, BS - 8))
    pad = (40, 128, 52)
    pygame.draw.circle(s, _darken(pad, 15), (BS // 2, BS - 6), 8)
    pygame.draw.circle(s, pad, (BS // 2, BS - 6), 7)
    pygame.draw.line(s, water, (BS // 2, BS - 6), (BS // 2, BS - 14), 1)
    pink = (225, 148, 178)
    pink_lt = _lighter(pink, 18)
    cx2 = BS // 2
    cy2 = BS - 14
    for ang in range(0, 360, 40):
        ex = cx2 + int(7 * math.cos(math.radians(ang)))
        ey = cy2 + int(5 * math.sin(math.radians(ang)))
        pygame.draw.line(s, pink, (cx2, cy2), (ex, ey), 2)
    pygame.draw.circle(s, (240, 225, 80), (cx2, cy2), 3)
    pygame.draw.circle(s, pink_lt, (cx2, cy2), 2)
    surfs[bid] = s

    bid = FROGBIT_BLOCK
    # if bid == FROGBIT_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    water = (50, 120, 168)
    s.fill(water)
    pygame.draw.ellipse(s, _lighter(water, 10), (3, 5, BS - 6, BS - 10))
    c = (48, 132, 55)
    dk = _darken(c, 18)
    for fx2, fy2, fr in [(6, BS - 8, 5), (16, BS - 6, 4), (24, BS - 10, 4),
                         (11, BS - 14, 4), (21, BS - 15, 3)]:
        pygame.draw.circle(s, dk, (fx2, fy2), fr)
        pygame.draw.circle(s, c, (fx2, fy2), fr - 1)
        pygame.draw.line(s, dk, (fx2, fy2), (fx2, fy2 - fr + 1), 1)
    surfs[bid] = s

    bid = ARROWHEAD_BLOCK
    # if bid == ARROWHEAD_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (65, 100, 52)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    c = (62, 148, 65)
    dk = _darken(c, 20)
    stem = (75, 138, 58)
    for sx2, sh in [(8, 18), (19, 22)]:
        pygame.draw.line(s, stem, (sx2, BS - 5), (sx2, BS - 5 - sh), 1)
        tip_y = BS - 5 - sh
        pts = [(sx2, tip_y - 6), (sx2 - 5, tip_y + 2), (sx2, tip_y),
               (sx2 + 5, tip_y + 2)]
        pygame.draw.polygon(s, dk, pts)
        pygame.draw.polygon(s, c, pts, 0)
        lobe_y = tip_y + 4
        pygame.draw.line(s, dk, (sx2 - 5, lobe_y), (sx2 - 8, lobe_y + 4), 1)
        pygame.draw.line(s, dk, (sx2 + 5, lobe_y), (sx2 + 8, lobe_y + 4), 1)
    surfs[bid] = s

    bid = HORSETAIL_BLOCK
    # if bid == HORSETAIL_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (65, 100, 52)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    c = (72, 138, 55)
    dk = _darken(c, 22)
    for sx2, sh in [(5, 22), (12, 18), (19, 24), (26, 19)]:
        for seg_y in range(BS - 5 - sh, BS - 5, 5):
            pygame.draw.rect(s, dk, (sx2 - 1, seg_y, 3, 4))
            pygame.draw.rect(s, c, (sx2, seg_y + 1, 1, 2))
            spoke_y = seg_y + 2
            for sdx in [-4, 4]:
                pygame.draw.line(s, c, (sx2, spoke_y), (sx2 + sdx, spoke_y - 1), 1)
    surfs[bid] = s

    bid = MARSH_MARIGOLD_BLOCK
    # if bid == MARSH_MARIGOLD_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (62, 95, 50)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    stem = (68, 128, 52)
    yellow = (232, 198, 32)
    yellow_lt = _lighter(yellow, 18)
    for fx2, fy2 in [(6, BS - 11), (16, BS - 14), (25, BS - 10)]:
        pygame.draw.line(s, stem, (fx2, BS - 5), (fx2, fy2 + 4), 1)
        for ang in range(0, 360, 60):
            ex = fx2 + int(5 * math.cos(math.radians(ang)))
            ey = fy2 + int(4 * math.sin(math.radians(ang)))
            pygame.draw.line(s, yellow, (fx2, fy2), (ex, ey), 2)
        pygame.draw.circle(s, yellow_lt, (fx2, fy2), 2)
    surfs[bid] = s

    bid = WATER_IRIS_BLOCK
    # if bid == WATER_IRIS_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (62, 95, 50)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    stem = (68, 128, 52)
    yellow = (228, 205, 40)
    yellow_lt = _lighter(yellow, 15)
    purple = (150, 100, 210)
    for fx2, fy2 in [(7, BS - 16), (19, BS - 18)]:
        pygame.draw.line(s, stem, (fx2, BS - 5), (fx2, fy2 + 6), 1)
        pygame.draw.ellipse(s, yellow, (fx2 - 4, fy2 + 2, 8, 5))
        pygame.draw.ellipse(s, yellow_lt, (fx2 - 2, fy2 + 3, 4, 3))
        for ang in [-40, 0, 40]:
            rad = math.radians(ang - 90)
            ex = fx2 + int(6 * math.cos(rad))
            ey = fy2 + int(6 * math.sin(rad))
            pygame.draw.line(s, purple, (fx2, fy2), (ex, ey), 2)
    surfs[bid] = s

    bid = SEDGE_BLOCK
    # if bid == SEDGE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (68, 100, 52)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    c = (88, 152, 58)
    dk = _darken(c, 18)
    for sx2, sh, curve in [(3, 20, 3), (8, 16, -4), (13, 22, 2), (18, 17, -3),
                           (23, 19, 4), (27, 14, -2)]:
        mid_y = BS - 5 - sh // 2
        pygame.draw.line(s, dk, (sx2, BS - 5), (sx2 + curve // 2, mid_y), 1)
        pygame.draw.line(s, c, (sx2 + curve // 2, mid_y), (sx2 + curve, BS - 5 - sh), 1)
    surfs[bid] = s

    bid = PICKERELWEED_BLOCK
    # if bid == PICKERELWEED_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    soil = (65, 98, 52)
    pygame.draw.rect(s, soil, (0, BS - 5, BS, 5))
    stem = (68, 128, 52)
    leaf = (58, 140, 62)
    purple = (92, 82, 205)
    purple_lt = _lighter(purple, 20)
    for sx2, sh in [(8, 22), (20, 20)]:
        pygame.draw.line(s, stem, (sx2, BS - 5), (sx2, BS - 5 - sh), 1)
        leaf_y = BS - 5 - sh // 2
        pygame.draw.ellipse(s, leaf, (sx2 + 1, leaf_y - 3, 6, 8))
        spike_y = BS - 5 - sh
        for sy2 in range(spike_y, spike_y + 8, 2):
            r = 2 if (sy2 - spike_y) < 4 else 1
            pygame.draw.circle(s, purple_lt if r == 1 else purple, (sx2, sy2), r)
    surfs[bid] = s

    bid = BEE_SKEP
    # if bid == BEE_SKEP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 20)
    lt = _lighter(c, 18)
    s.fill(_darken(c, 35))
    # base slab
    pygame.draw.rect(s, dk, (3, BS - 7, BS - 6, 4))
    # domed skep body — draw horizontal coils
    widths = [10, 14, 16, 16, 14, 10, 6]
    for row, w in enumerate(widths):
        y2 = BS - 11 - row * 3
        x2 = BS//2 - w//2
        pygame.draw.ellipse(s, c if row % 2 == 0 else lt, (x2, y2, w, 3))
        pygame.draw.ellipse(s, dk, (x2, y2, w, 3), 1)
    # entrance hole
    pygame.draw.ellipse(s, _darken(c, 40), (BS//2 - 3, BS - 12, 6, 4))
    surfs[bid] = s

    bid = GARDEN_WHEELBARROW
    # if bid == GARDEN_WHEELBARROW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    wood = (130, 85, 45)
    wood_dk = _darken(wood, 20)
    iron = (90, 88, 85)
    soil = (85, 58, 30)
    s.fill(_darken(wood, 38))
    # wheel
    pygame.draw.circle(s, iron, (8, BS - 7), 5)
    pygame.draw.circle(s, _lighter(iron, 15), (8, BS - 7), 3)
    # tray body — angled rectangle
    pts = [(6, BS - 12), (BS - 4, BS - 14), (BS - 6, BS - 7), (8, BS - 6)]
    pygame.draw.polygon(s, wood, pts)
    pygame.draw.polygon(s, wood_dk, pts, 1)
    # soil fill
    soil_pts = [(8, BS - 11), (BS - 5, BS - 13), (BS - 7, BS - 8), (9, BS - 7)]
    pygame.draw.polygon(s, soil, soil_pts)
    # handles extend back
    pygame.draw.line(s, wood, (6, BS - 12), (4, BS - 20), 2)
    pygame.draw.line(s, wood, (BS - 4, BS - 14), (BS - 2, BS - 20), 2)
    surfs[bid] = s

    bid = IRIS_BED
    # if bid == IRIS_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((90, 60, 35))
    pygame.draw.rect(s, (150, 138, 120), (0, BS - 5, BS, 5))
    stem = (60, 105, 50)
    iris = (100, 85, 210)
    iris_lt = _lighter(iris, 18)
    for ix, iy in [(5, 12), (14, 8), (23, 12), (9, 20), (20, 18)]:
        pygame.draw.line(s, stem, (ix, BS - 6), (ix, iy + 5), 1)
        pygame.draw.ellipse(s, iris, (ix - 3, iy - 2, 6, 5))
        pygame.draw.ellipse(s, iris_lt, (ix - 2, iy + 2, 4, 3))
    surfs[bid] = s

    bid = POPPY_BED
    # if bid == POPPY_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((90, 60, 35))
    pygame.draw.rect(s, (150, 138, 120), (0, BS - 5, BS, 5))
    stem = (60, 105, 50)
    red = (215, 40, 40)
    for px2, py2 in [(5, 9), (13, 6), (22, 10), (8, 19), (19, 17)]:
        pygame.draw.line(s, stem, (px2, BS - 6), (px2, py2 + 4), 1)
        pygame.draw.circle(s, red, (px2, py2), 4)
        pygame.draw.circle(s, (15, 10, 10), (px2, py2), 2)
        pygame.draw.circle(s, _lighter(red, 20), (px2 - 1, py2 - 1), 1)
    surfs[bid] = s

    bid = FOXGLOVE_PATCH
    # if bid == FOXGLOVE_PATCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((90, 60, 35))
    pygame.draw.rect(s, (150, 138, 120), (0, BS - 5, BS, 5))
    stem = (65, 110, 50)
    bell = (220, 110, 175)
    bell_lt = _lighter(bell, 18)
    for sx2, in_y in [(7, 4), (18, 3), (26, 6)]:
        pygame.draw.line(s, stem, (sx2, BS - 6), (sx2, in_y), 2)
        for dy2 in range(in_y + 2, BS - 8, 4):
            pygame.draw.ellipse(s, bell, (sx2 - 3, dy2, 6, 4))
            pygame.draw.ellipse(s, bell_lt, (sx2 - 2, dy2, 4, 2))
    surfs[bid] = s

    bid = SNOWDROP_PATCH
    # if bid == SNOWDROP_PATCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((90, 60, 35))
    pygame.draw.rect(s, (150, 138, 120), (0, BS - 5, BS, 5))
    stem = (80, 130, 70)
    white = (235, 238, 242)
    green_tip = (90, 150, 80)
    for sx2, sy2 in [(5, 10), (11, 7), (18, 11), (24, 8)]:
        pygame.draw.line(s, stem, (sx2, BS - 6), (sx2, sy2), 1)
        pygame.draw.line(s, stem, (sx2, sy2), (sx2 - 2, sy2 + 4), 1)
        pygame.draw.ellipse(s, white, (sx2 - 4, sy2 + 3, 4, 5))
        pygame.draw.circle(s, green_tip, (sx2 - 2, sy2 + 3), 1)
    surfs[bid] = s

    bid = MARIGOLD_BED
    # if bid == MARIGOLD_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((90, 60, 35))
    pygame.draw.rect(s, (150, 138, 120), (0, BS - 5, BS, 5))
    stem = (65, 110, 50)
    for mx, my, col in [(6, 9, (235, 148, 28)), (15, 6, (245, 190, 35)), (23, 10, (220, 120, 25)), (10, 19, (240, 165, 30)), (21, 17, (230, 140, 28))]:
        pygame.draw.line(s, stem, (mx, BS - 6), (mx, my + 4), 1)
        for ang in range(0, 360, 40):
            ex = mx + int(4 * math.cos(math.radians(ang)))
            ey = my + int(4 * math.sin(math.radians(ang)))
            pygame.draw.line(s, col, (mx, my), (ex, ey), 2)
        pygame.draw.circle(s, _darken(col, 20), (mx, my), 2)
    surfs[bid] = s

    bid = BOXWOOD_BALL
    # if bid == BOXWOOD_BALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.rect(s, trunk, (BS//2 - 1, BS - 14, 2, 8))
    pygame.draw.circle(s, dk, (BS//2, BS - 17), 8)
    pygame.draw.circle(s, c, (BS//2, BS - 18), 7)
    pygame.draw.circle(s, lt, (BS//2 - 2, BS - 20), 2)
    surfs[bid] = s

    bid = RHODODENDRON_BUSH
    # if bid == RHODODENDRON_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 18)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 32))
    pygame.draw.rect(s, trunk, (BS//2 - 3, BS - 6, 6, 6))
    pygame.draw.ellipse(s, dk, (1, 7, BS - 2, BS - 11))
    pygame.draw.ellipse(s, c, (3, 9, BS - 8, BS - 15))
    bloom = (220, 100, 175)
    bloom_lt = _lighter(bloom, 15)
    for fx, fy in [(5, 10), (14, 7), (22, 11), (9, 17), (20, 16)]:
        pygame.draw.circle(s, bloom, (fx, fy), 4)
        pygame.draw.circle(s, bloom_lt, (fx - 1, fy - 1), 2)
    surfs[bid] = s

    bid = BAMBOO_CLUMP
    # if bid == BAMBOO_CLUMP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((30, 45, 20))
    stalk_cols = [(88, 148, 58), (72, 128, 48), (100, 158, 65)]
    for i, (bx2, bw) in enumerate([(4, 4), (11, 3), (18, 4), (24, 3)]):
        col = stalk_cols[i % 3]
        pygame.draw.rect(s, col, (bx2, 0, bw, BS))
        pygame.draw.rect(s, _darken(col, 15), (bx2, 0, 1, BS))
        for ny in range(4, BS, 7):
            pygame.draw.line(s, _darken(col, 20), (bx2, ny), (bx2 + bw, ny), 1)
        leaf_col = _lighter(col, 10)
        for ny in range(5, BS, 7):
            pygame.draw.line(s, leaf_col, (bx2 + bw, ny), (bx2 + bw + 4, ny - 3), 1)
    surfs[bid] = s

    bid = AGAPANTHUS_PATCH
    # if bid == AGAPANTHUS_PATCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((90, 60, 35))
    pygame.draw.rect(s, (150, 138, 120), (0, BS - 5, BS, 5))
    stem = (65, 110, 50)
    blue = (70, 100, 200)
    blue_lt = _lighter(blue, 20)
    for ax, ay in [(7, 4), (18, 3), (26, 6)]:
        pygame.draw.line(s, stem, (ax, BS - 6), (ax, ay + 5), 1)
        for ang in range(0, 360, 45):
            ex = ax + int(5 * math.cos(math.radians(ang)))
            ey = ay + int(3 * math.sin(math.radians(ang)))
            pygame.draw.line(s, blue, (ax, ay), (ex, ey), 1)
        pygame.draw.circle(s, blue_lt, (ax, ay), 2)
    surfs[bid] = s

    bid = TOPIARY_DRAGON
    # if bid == TOPIARY_DRAGON
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, c, (BS//2 - 7, BS - 20, 14, 10))
    pygame.draw.line(s, dk, (BS//2 + 5, BS - 16), (BS//2 + 8, BS - 25), 3)
    pygame.draw.circle(s, c, (BS//2 + 8, BS - 26), 3)
    pygame.draw.polygon(s, lt, [(BS//2 + 7, BS - 28), (BS//2 + 10, BS - 31), (BS//2 + 10, BS - 26)])
    pygame.draw.polygon(s, dk, [(BS//2 - 7, BS - 16), (BS//2 - 13, BS - 24), (BS//2 - 4, BS - 22)])
    pygame.draw.polygon(s, dk, [(BS//2 + 6, BS - 18), (BS//2 + 12, BS - 24), (BS//2 + 7, BS - 22)])
    surfs[bid] = s

    bid = TOPIARY_GIRAFFE
    # if bid == TOPIARY_GIRAFFE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, c, (BS//2 - 6, BS - 18, 12, 10))
    pygame.draw.line(s, dk, (BS//2, BS - 15), (BS//2 - 1, BS - 29), 4)
    pygame.draw.line(s, c, (BS//2, BS - 15), (BS//2 - 1, BS - 29), 2)
    pygame.draw.circle(s, c, (BS//2 - 1, BS - 30), 3)
    pygame.draw.line(s, lt, (BS//2 - 1, BS - 32), (BS//2 - 1, BS - 35), 1)
    pygame.draw.line(s, lt, (BS//2 + 1, BS - 32), (BS//2 + 1, BS - 35), 1)
    surfs[bid] = s

    bid = TOPIARY_HEDGEHOG
    # if bid == TOPIARY_HEDGEHOG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 25)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, c, (BS//2 - 8, BS - 18, 16, 12))
    pygame.draw.circle(s, c, (BS//2 + 6, BS - 14), 4)
    pygame.draw.circle(s, _darken(c, 30), (BS//2 + 8, BS - 14), 1)
    for ang in range(180, 360, 20):
        ex = BS//2 - 1 + int(9 * math.cos(math.radians(ang)))
        ey = BS - 12 + int(7 * math.sin(math.radians(ang)))
        pygame.draw.line(s, dk, (BS//2 - 1, BS - 12), (ex, ey), 1)
    surfs[bid] = s

    bid = BUBBLE_FOUNTAIN
    # if bid == BUBBLE_FOUNTAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 22)
    water = (80, 155, 200)
    s.fill(_darken(c, 18))
    pygame.draw.ellipse(s, dk, (3, BS//2 - 2, BS - 6, BS//2))
    pygame.draw.ellipse(s, c, (4, BS//2 - 1, BS - 8, BS//2 - 2))
    pygame.draw.ellipse(s, lt, (6, BS//2, BS - 14, 6))
    for bx2, by2 in [(BS//2 - 2, BS//2 - 4), (BS//2 + 3, BS//2 - 6), (BS//2, BS//2 - 8)]:
        pygame.draw.circle(s, water, (bx2, by2), 2)
        pygame.draw.circle(s, (220, 238, 255), (bx2, by2), 1)
    pygame.draw.rect(s, _darken(c, 28), s.get_rect(), 1)
    surfs[bid] = s

    bid = SHELL_FOUNTAIN
    # if bid == SHELL_FOUNTAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    water = (80, 155, 200)
    stone = (165, 158, 142)
    s.fill(_darken(stone, 15))
    pygame.draw.rect(s, stone, (BS//2 - 2, BS - 8, 4, 5))
    pygame.draw.ellipse(s, stone, (3, BS - 12, BS - 6, 5))
    for rib in range(4, BS - 4, 3):
        pygame.draw.arc(s, dk, (rib, 6, BS - rib * 2, BS//2), 0, math.pi, 1)
    pygame.draw.ellipse(s, c, (5, 8, BS - 10, BS//2 - 4))
    pygame.draw.ellipse(s, water, (7, 10, BS - 14, BS//2 - 8))
    pygame.draw.line(s, _lighter(water, 20), (BS//2, 8), (BS//2, 3), 1)
    pygame.draw.circle(s, (220, 235, 255), (BS//2, 2), 2)
    pygame.draw.rect(s, _darken(stone, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = MILLSTONE_FOUNTAIN
    # if bid == MILLSTONE_FOUNTAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 22)
    water = (80, 155, 200)
    s.fill(_darken(c, 20))
    pygame.draw.ellipse(s, dk, (2, BS//4, BS - 4, BS//2))
    pygame.draw.ellipse(s, c, (3, BS//4 + 1, BS - 6, BS//2 - 2))
    pygame.draw.ellipse(s, lt, (4, BS//4 + 2, BS - 8, BS//2 - 4))
    pygame.draw.circle(s, water, (BS//2, BS//2), 5)
    for ang in range(0, 360, 45):
        gx = BS//2 + int(8 * math.cos(math.radians(ang)))
        gy = BS//2 + int(4 * math.sin(math.radians(ang)))
        pygame.draw.line(s, dk, (BS//2, BS//2), (gx, gy), 1)
    for wx in range(2, BS - 2, 4):
        pygame.draw.circle(s, water, (wx, BS//4 + BS//4), 1)
    pygame.draw.rect(s, _darken(c, 28), s.get_rect(), 1)
    surfs[bid] = s

    bid = TRELLIS_ARCH
    # if bid == TRELLIS_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    wood = (130, 85, 45)
    wood_dk = _darken(wood, 22)
    green = (55, 115, 48)
    s.fill((25, 40, 18))
    pygame.draw.rect(s, wood, (2, 0, 4, BS))
    pygame.draw.rect(s, wood, (BS - 6, 0, 4, BS))
    pygame.draw.arc(s, wood, (2, 2, BS - 4, BS//2), 0, math.pi, 4)
    for ty2 in range(0, BS, 5):
        pygame.draw.line(s, wood_dk, (4, ty2), (6, ty2), 1)
        pygame.draw.line(s, wood_dk, (BS - 6, ty2), (BS - 4, ty2), 1)
    for gx, gy in [(4, 4), (BS - 6, 6), (6, 14), (BS - 8, 12), (5, 24), (BS - 7, 22)]:
        pygame.draw.circle(s, green, (gx, gy), 2)
    pygame.draw.rect(s, _darken(wood, 30), s.get_rect(), 1)
    surfs[bid] = s

    bid = COLD_FRAME
    # if bid == COLD_FRAME
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    wood = (130, 85, 45)
    wood_dk = _darken(wood, 20)
    glass = (190, 218, 228)
    soil = (80, 52, 28)
    s.fill(wood)
    pygame.draw.rect(s, wood_dk, (0, 0, BS, 3))
    pygame.draw.rect(s, soil, (3, 3, BS - 6, BS - 10))
    for px2 in range(0, BS, 8):
        pygame.draw.line(s, wood_dk, (px2, 0), (px2, BS), 1)
    pygame.draw.polygon(s, glass, [(0, BS - 9), (BS, BS - 11), (BS, BS - 6), (0, BS - 4)])
    pygame.draw.line(s, _lighter(glass, 20), (0, BS - 8), (BS, BS - 10), 1)
    green = (70, 130, 55)
    for gx in range(5, BS - 4, 7):
        pygame.draw.circle(s, green, (gx, BS//2 - 2), 2)
    pygame.draw.rect(s, wood_dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GARDEN_SWING
    # if bid == GARDEN_SWING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    wood = (130, 85, 45)
    rope = (175, 145, 90)
    s.fill((40, 55, 35))
    pygame.draw.line(s, wood, (2, 2), (BS - 2, 2), 3)
    pygame.draw.line(s, rope, (6, 3), (6, BS - 8), 1)
    pygame.draw.line(s, rope, (BS - 6, 3), (BS - 6, BS - 8), 1)
    pygame.draw.rect(s, wood, (4, BS - 9, BS - 8, 4))
    pygame.draw.rect(s, _lighter(wood, 15), (4, BS - 9, BS - 8, 2))
    pygame.draw.line(s, wood, (0, 0), (0, BS - 3), 3)
    pygame.draw.line(s, wood, (BS - 1, 0), (BS - 1, BS - 3), 3)
    pygame.draw.rect(s, _darken(wood, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = WICKER_FENCE
    # if bid == WICKER_FENCE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    s.fill(_darken(c, 35))
    for py2 in range(2, BS - 4, 5):
        pygame.draw.line(s, c if (py2 // 5) % 2 == 0 else lt, (0, py2), (BS, py2), 2)
    for px2 in range(0, BS, 5):
        for py2 in range(0, BS, 10):
            offset = 5 if (px2 // 5) % 2 == 0 else 0
            pygame.draw.line(s, dk, (px2, py2 + offset), (px2, py2 + offset + 5), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = HANGING_BASKET
    # if bid == HANGING_BASKET
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    bracket = (80, 78, 75)
    basket = (145, 100, 55)
    basket_dk = _darken(basket, 20)
    s.fill(_darken(basket, 40))
    pygame.draw.line(s, bracket, (BS//2, 0), (BS//2 + 4, 4), 2)
    pygame.draw.line(s, bracket, (BS//2 + 4, 4), (BS//2 + 4, 8), 2)
    pygame.draw.ellipse(s, basket_dk, (BS//2 - 5, 8, 14, 14))
    pygame.draw.ellipse(s, basket, (BS//2 - 4, 9, 12, 11))
    for wr in range(10, 20, 3):
        pygame.draw.line(s, basket_dk, (BS//2 - 4, wr), (BS//2 + 8, wr), 1)
    blooms = [(210, 80, 120), (240, 185, 45), (90, 160, 220)]
    for i, (fx, fy) in enumerate([(BS//2 - 3, 8), (BS//2 + 1, 7), (BS//2 + 5, 9)]):
        pygame.draw.circle(s, blooms[i % 3], (fx, fy), 3)
    trailing = (70, 140, 55)
    for tx2, ty2 in [(BS//2 - 5, 18), (BS//2 + 7, 17), (BS//2, 20)]:
        pygame.draw.line(s, trailing, (tx2, ty2), (tx2 - 2, ty2 + 6), 1)
    surfs[bid] = s

    bid = STANDARD_ROSE
    # if bid == STANDARD_ROSE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.rect(s, trunk, (BS//2 - 1, 10, 2, BS - 16))
    pygame.draw.circle(s, _darken(c, 22), (BS//2, 9), 7)
    pygame.draw.circle(s, c, (BS//2, 8), 6)
    rose = (210, 60, 85)
    rose_lt = _lighter(rose, 20)
    for rx, ry in [(BS//2 - 3, 6), (BS//2 + 2, 5), (BS//2, 10), (BS//2 - 4, 10), (BS//2 + 3, 11)]:
        pygame.draw.circle(s, rose, (rx, ry), 2)
        pygame.draw.circle(s, rose_lt, (rx, ry), 1)
    surfs[bid] = s

    bid = GARDEN_GNOME
    # if bid == GARDEN_GNOME
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((55, 75, 45))
    body_col = (55, 110, 185)
    hat_col = (200, 50, 40)
    skin = (230, 188, 145)
    beard = (235, 230, 220)
    pygame.draw.rect(s, body_col, (BS//2 - 4, BS - 12, 8, 8))
    pygame.draw.rect(s, _lighter(body_col, 15), (BS//2 - 3, BS - 11, 6, 2))
    pygame.draw.circle(s, skin, (BS//2, BS - 16), 4)
    pygame.draw.ellipse(s, beard, (BS//2 - 3, BS - 16, 6, 5))
    pygame.draw.circle(s, skin, (BS//2, BS - 17), 3)
    pygame.draw.polygon(s, hat_col, [(BS//2 - 4, BS - 20), (BS//2 + 4, BS - 20), (BS//2, BS - 30)])
    pygame.draw.line(s, _lighter(hat_col, 15), (BS//2 - 4, BS - 20), (BS//2, BS - 30), 1)
    pygame.draw.rect(s, _darken(body_col, 20), (BS//2 - 5, BS - 5, 4, 5))
    pygame.draw.rect(s, _darken(body_col, 20), (BS//2 + 1, BS - 5, 4, 5))
    surfs[bid] = s

    bid = TOPIARY_ARCH
    # if bid == TOPIARY_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 20)
    interior = (20, 35, 15)
    s.fill(c)
    pygame.draw.arc(s, lt, (3, 2, BS - 6, BS - 4), 0, math.pi, 3)
    pygame.draw.arc(s, dk, (3, 2, BS - 6, BS - 4), 0, math.pi, 1)
    inner_r = BS//2 - 7
    pygame.draw.ellipse(s, interior, (BS//2 - inner_r, 4, inner_r * 2, BS//2 - 2))
    pygame.draw.rect(s, interior, (BS//2 - inner_r, BS//2 - 2, inner_r * 2, BS//2 + 2))
    pygame.draw.rect(s, _lighter(c, 5), (0, 0, 4, BS))
    pygame.draw.rect(s, _lighter(c, 5), (BS - 4, 0, 4, BS))
    for lx, ly in [(1, 8), (BS - 3, 10), (1, 18), (BS - 3, 20)]:
        pygame.draw.circle(s, lt, (lx, ly), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CHAMOMILE_LAWN
    # if bid == CHAMOMILE_LAWN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    green = (130, 168, 80)
    green_dk = _darken(green, 15)
    s.fill(green)
    for gy in range(0, BS, 4):
        for gx in range(0, BS, 4):
            if (gx + gy) % 8 == 0:
                pygame.draw.rect(s, green_dk, (gx, gy, 2, 2))
    white = (242, 240, 228)
    yellow = (230, 210, 50)
    for fx, fy in [(3, 4), (10, 2), (18, 6), (25, 3), (6, 12), (14, 15), (22, 13), (28, 17), (4, 22), (12, 25), (20, 23), (27, 26)]:
        for ang in range(0, 360, 60):
            ex = fx + int(3 * math.cos(math.radians(ang)))
            ey = fy + int(3 * math.sin(math.radians(ang)))
            pygame.draw.line(s, white, (fx, fy), (ex, ey), 1)
        pygame.draw.circle(s, yellow, (fx, fy), 1)
    surfs[bid] = s

    bid = CREEPING_THYME
    # if bid == CREEPING_THYME
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    green = (90, 135, 70)
    green_lt = _lighter(green, 15)
    s.fill(green)
    for gy in range(0, BS, 3):
        for gx in range(0, BS, 3):
            if (gx // 3 + gy // 3) % 2 == 0:
                pygame.draw.rect(s, green_lt, (gx, gy, 2, 2))
    purple = (160, 100, 195)
    purple_lt = _lighter(purple, 18)
    for fx, fy in [(2, 3), (8, 1), (14, 4), (20, 2), (26, 5), (5, 9), (11, 12), (17, 10), (23, 13), (3, 18), (9, 21), (15, 19), (21, 22), (27, 20), (6, 27), (13, 28), (19, 26), (25, 29)]:
        pygame.draw.circle(s, purple, (fx, fy), 1)
        pygame.draw.circle(s, purple_lt, (fx, fy), 1)
    surfs[bid] = s

    bid = HYDRANGEA_BUSH
    # if bid == HYDRANGEA_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 20)
    trunk = (100, 65, 35)
    green = (50, 105, 45)
    s.fill(_darken(green, 30))
    pygame.draw.rect(s, trunk, (BS//2 - 3, BS - 6, 6, 6))
    pygame.draw.ellipse(s, _darken(green, 15), (1, 10, BS - 2, BS - 14))
    pygame.draw.ellipse(s, green, (3, 12, BS - 8, BS - 18))
    for hx, hy, r in [(7, 8, 5), (19, 6, 6), (13, 16, 5)]:
        for ang in range(0, 360, 30):
            px2 = hx + int(r * 0.7 * math.cos(math.radians(ang)))
            py2 = hy + int(r * 0.5 * math.sin(math.radians(ang)))
            pygame.draw.circle(s, c, (px2, py2), 2)
        pygame.draw.circle(s, _lighter(c, 18), (hx, hy), 1)
    surfs[bid] = s

    bid = ALLIUM_PATCH
    # if bid == ALLIUM_PATCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((90, 60, 35))
    pygame.draw.rect(s, (150, 138, 120), (0, BS - 5, BS, 5))
    stem = (70, 115, 55)
    purple = (150, 75, 200)
    purple_lt = _lighter(purple, 20)
    for ax, ay in [(6, 3), (16, 2), (25, 5)]:
        pygame.draw.line(s, stem, (ax, BS - 6), (ax, ay + 6), 2)
        for ang in range(0, 360, 30):
            ex = ax + int(5 * math.cos(math.radians(ang)))
            ey = ay + int(5 * math.sin(math.radians(ang)))
            pygame.draw.circle(s, purple, (ex, ey), 1)
        pygame.draw.circle(s, purple_lt, (ax, ay), 2)
    surfs[bid] = s

    bid = SWEET_PEA_TRELLIS
    # if bid == SWEET_PEA_TRELLIS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    cane = (165, 138, 80)
    cane_dk = _darken(cane, 20)
    green = (60, 120, 50)
    s.fill((28, 42, 20))
    for cx2 in range(4, BS - 2, 7):
        pygame.draw.line(s, cane, (cx2, 0), (cx2, BS), 1)
    for cy2 in range(0, BS, 6):
        pygame.draw.line(s, cane_dk, (0, cy2), (BS, cy2), 1)
    pea_cols = [(230, 140, 185), (250, 190, 210), (200, 120, 220), (240, 160, 200)]
    for i, (px2, py2) in enumerate([(5, 4), (12, 9), (19, 5), (26, 11), (8, 18), (22, 20), (15, 25)]):
        pygame.draw.circle(s, pea_cols[i % 4], (px2, py2), 3)
        pygame.draw.line(s, green, (px2, py2 + 3), (px2 + 3, py2 + 7), 1)
    surfs[bid] = s

    bid = BLEEDING_HEART_PATCH
    # if bid == BLEEDING_HEART_PATCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((90, 60, 35))
    pygame.draw.rect(s, (150, 138, 120), (0, BS - 5, BS, 5))
    stem = (70, 118, 55)
    pink = (215, 80, 130)
    white = (240, 220, 230)
    for sx2, arch_y in [(8, 6), (20, 4)]:
        pygame.draw.arc(s, stem, (sx2 - 6, arch_y, 12, 10), 0, math.pi, 1)
        for tx2 in range(sx2 - 4, sx2 + 5, 4):
            hang_y = arch_y + 2 + abs(tx2 - sx2) // 2
            pygame.draw.circle(s, pink, (tx2, hang_y + 3), 3)
            pygame.draw.ellipse(s, white, (tx2 - 1, hang_y + 5, 3, 4))
    surfs[bid] = s

    bid = ASTILBE_PATCH
    # if bid == ASTILBE_PATCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    s.fill((90, 60, 35))
    pygame.draw.rect(s, (150, 138, 120), (0, BS - 5, BS, 5))
    stem = (70, 115, 55)
    plume = (210, 100, 145)
    plume_lt = _lighter(plume, 20)
    for ax, ay in [(6, 2), (16, 1), (25, 4)]:
        pygame.draw.line(s, stem, (ax, BS - 6), (ax, ay + 8), 2)
        for dy2 in range(ay + 2, ay + 10, 2):
            spread = (dy2 - ay) // 2 + 1
            for dx2 in range(-spread, spread + 1, 2):
                col = plume if dy2 % 4 == 0 else plume_lt
                if 0 <= ax + dx2 < BS:
                    pygame.draw.circle(s, col, (ax + dx2, dy2), 1)
    surfs[bid] = s

    bid = WISTERIA_PILLAR
    # if bid == WISTERIA_PILLAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    stone = (165, 158, 142)
    stone_dk = _darken(stone, 18)
    wist = (175, 120, 210)
    wist_lt = _lighter(wist, 18)
    leaf = (60, 110, 50)
    s.fill(_darken(stone, 22))
    pygame.draw.rect(s, stone_dk, (BS//2 - 4, 0, 8, BS))
    pygame.draw.rect(s, stone, (BS//2 - 3, 0, 6, BS))
    pygame.draw.rect(s, _lighter(stone, 12), (BS//2 - 2, 0, 2, BS))
    for cx2 in range(3, BS - 3, 6):
        drop = 2 + (cx2 % 4)
        pygame.draw.line(s, leaf, (cx2, 0), (cx2, drop + 4), 1)
        for dy2 in range(drop, drop + 10, 3):
            if dy2 < BS:
                pygame.draw.circle(s, wist, (cx2, dy2), 2)
                if dy2 + 2 < BS:
                    pygame.draw.circle(s, wist_lt, (cx2 - 1, dy2), 1)
    pygame.draw.rect(s, stone_dk, (BS//2 - 5, 0, 10, 4))
    pygame.draw.rect(s, stone_dk, (BS//2 - 5, BS - 4, 10, 4))
    surfs[bid] = s

    bid = TOPIARY_SNAIL
    # if bid == TOPIARY_SNAIL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, c, (4, BS - 18, 16, 10))
    for r in range(7, 2, -2):
        col = lt if r % 4 < 2 else dk
        pygame.draw.circle(s, col, (BS//2 + 2, BS - 16), r)
    pygame.draw.circle(s, _darken(c, 35), (BS//2 + 2, BS - 16), 2)
    pygame.draw.line(s, c, (4, BS - 15), (2, BS - 22), 2)
    pygame.draw.circle(s, lt, (2, BS - 23), 2)
    pygame.draw.line(s, c, (5, BS - 16), (3, BS - 23), 1)
    surfs[bid] = s

    bid = TOPIARY_MUSHROOM
    # if bid == TOPIARY_MUSHROOM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.rect(s, _lighter(trunk, 15), (BS//2 - 3, BS - 18, 6, 12))
    pygame.draw.ellipse(s, dk, (2, BS - 26, BS - 4, 14))
    pygame.draw.ellipse(s, c, (3, BS - 25, BS - 6, 12))
    pygame.draw.ellipse(s, lt, (5, BS - 24, BS - 12, 6))
    for sx2 in range(6, BS - 4, 5):
        pygame.draw.line(s, dk, (sx2, BS - 24), (sx2 - 2, BS - 20), 1)
    surfs[bid] = s

    bid = TOPIARY_OWL
    # if bid == TOPIARY_OWL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, c, (BS//2 - 6, BS - 20, 12, 14))
    pygame.draw.circle(s, c, (BS//2, BS - 24), 5)
    pygame.draw.ellipse(s, dk, (BS//2 - 5, BS - 28, 4, 5))
    pygame.draw.ellipse(s, dk, (BS//2 + 1, BS - 28, 4, 5))
    pygame.draw.circle(s, _lighter(dk, 10), (BS//2 - 3, BS - 26), 2)
    pygame.draw.circle(s, _lighter(dk, 10), (BS//2 + 3, BS - 26), 2)
    pygame.draw.polygon(s, lt, [(BS//2 - 1, BS - 22), (BS//2, BS - 20), (BS//2 + 1, BS - 22)])
    surfs[bid] = s

    bid = TOPIARY_DINOSAUR
    # if bid == TOPIARY_DINOSAUR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    trunk = (100, 65, 35)
    s.fill(_darken(c, 38))
    pygame.draw.rect(s, trunk, (BS//2 - 2, BS - 6, 4, 6))
    pygame.draw.ellipse(s, c, (BS//2 - 8, BS - 18, 16, 10))
    pygame.draw.line(s, dk, (BS//2 + 6, BS - 14), (BS//2 + 12, BS - 10), 3)
    pygame.draw.circle(s, c, (BS//2 - 5, BS - 22), 5)
    pygame.draw.line(s, dk, (BS//2 - 5, BS - 22), (BS//2 - 10, BS - 19), 3)
    for sx2 in range(BS//2 - 4, BS//2 + 6, 3):
        pygame.draw.polygon(s, lt, [(sx2, BS - 18), (sx2 + 1, BS - 22), (sx2 + 2, BS - 18)])
    surfs[bid] = s

    bid = KOI_POOL
    # if bid == KOI_POOL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    stone = (160, 152, 138)
    water = (45, 110, 165)
    water_lt = _lighter(water, 15)
    s.fill(stone)
    pygame.draw.rect(s, _darken(stone, 20), s.get_rect(), 3)
    pygame.draw.rect(s, water, (4, 4, BS - 8, BS - 8))
    pygame.draw.rect(s, water_lt, (5, 5, BS - 10, 4))
    koi_cols = [(220, 80, 40), (240, 185, 50), (220, 220, 220), (200, 60, 60)]
    for i, (kx, ky, ka) in enumerate([(8, 10, 20), (18, 8, -15), (12, 18, 45), (22, 20, -30)]):
        col = koi_cols[i % 4]
        ex = kx + int(5 * math.cos(math.radians(ka)))
        ey = ky + int(5 * math.sin(math.radians(ka)))
        pygame.draw.line(s, col, (kx, ky), (ex, ey), 3)
        pygame.draw.circle(s, _lighter(col, 15), (kx, ky), 2)
    surfs[bid] = s

    bid = STONE_TROUGH_PLANTER
    # if bid == STONE_TROUGH_PLANTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 20)
    soil = (80, 52, 28)
    s.fill(_darken(c, 22))
    pygame.draw.rect(s, dk, (1, BS//2, BS - 2, BS//2 - 1))
    pygame.draw.rect(s, c, (2, BS//2 + 1, BS - 4, BS//2 - 3))
    pygame.draw.rect(s, lt, (2, BS//2 + 1, BS - 4, 3))
    pygame.draw.rect(s, soil, (3, BS//2 - 6, BS - 6, 8))
    pygame.draw.rect(s, _lighter(soil, 10), (3, BS//2 - 6, BS - 6, 2))
    green = (65, 130, 52)
    for gx in range(5, BS - 4, 6):
        pygame.draw.ellipse(s, green, (gx - 2, BS//2 - 10, 4, 5))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = RAIN_BARREL
    # if bid == RAIN_BARREL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    wood = (105, 65, 35)
    wood_lt = _lighter(wood, 15)
    hoop = (70, 68, 65)
    tap = (160, 128, 50)
    s.fill(_darken(wood, 30))
    pygame.draw.ellipse(s, _darken(wood, 10), (3, 2, BS - 6, 6))
    pygame.draw.rect(s, wood, (3, 4, BS - 6, BS - 10))
    for hy in [8, 14, 20]:
        pygame.draw.line(s, hoop, (3, hy), (BS - 3, hy), 2)
    for vx in range(3, BS - 2, 4):
        pygame.draw.line(s, wood_lt if (vx // 4) % 2 == 0 else _darken(wood, 10), (vx, 4), (vx, BS - 6), 1)
    pygame.draw.ellipse(s, _darken(wood, 10), (3, BS - 8, BS - 6, 5))
    pygame.draw.rect(s, tap, (BS//2 - 2, BS - 8, 5, 4))
    pygame.draw.circle(s, _lighter(tap, 20), (BS//2 + 2, BS - 7), 1)
    pygame.draw.rect(s, _darken(wood, 28), s.get_rect(), 1)
    surfs[bid] = s

    bid = MOSS_PATCH
    # if bid == MOSS_PATCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 15)
    s.fill(c)
    for gy in range(0, BS, 3):
        for gx in range(0, BS, 3):
            v = (gx * 3 + gy) % 9
            col = lt if v < 3 else (dk if v < 6 else c)
            pygame.draw.rect(s, col, (gx, gy, 3, 3))
    for bx2, by2 in [(2, 2), (7, 5), (14, 1), (20, 7), (27, 3), (5, 14), (11, 18), (18, 13), (25, 17), (3, 24), (9, 28), (16, 22), (23, 26)]:
        pygame.draw.circle(s, lt, (bx2, by2), 2)
    surfs[bid] = s

    bid = CLOVER_LAWN
    # if bid == CLOVER_LAWN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    green = (75, 150, 60)
    green_dk = _darken(green, 12)
    s.fill(green)
    for gy in range(0, BS, 5):
        for gx in range(0, BS, 5):
            pygame.draw.circle(s, green_dk if (gx + gy) % 10 == 0 else green, (gx + 2, gy + 2), 2)
    white = (235, 235, 228)
    for fx, fy in [(4, 5), (12, 3), (20, 7), (28, 4), (7, 14), (16, 17), (24, 13), (3, 23), (11, 26), (19, 22), (27, 25)]:
        for ang in range(0, 360, 120):
            ex = fx + int(2 * math.cos(math.radians(ang)))
            ey = fy + int(2 * math.sin(math.radians(ang)))
            pygame.draw.circle(s, white, (ex, ey), 2)
    surfs[bid] = s

    bid = BARK_MULCH
    # if bid == BARK_MULCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    s.fill(c)
    import random as _rnd
    _rng = _rnd.Random(42)
    for _ in range(22):
        bx2 = _rng.randint(0, BS - 6)
        by2 = _rng.randint(0, BS - 3)
        blen = _rng.randint(4, 8)
        col = lt if _rng.random() > 0.5 else dk
        pygame.draw.rect(s, col, (bx2, by2, blen, 2))
    surfs[bid] = s

    bid = STONE_FROG
    # if bid == STONE_FROG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 20)
    s.fill(_darken(c, 28))
    pygame.draw.ellipse(s, dk, (BS//2 - 7, BS - 17, 14, 10))
    pygame.draw.ellipse(s, c, (BS//2 - 6, BS - 16, 12, 8))
    pygame.draw.circle(s, c, (BS//2, BS - 20), 5)
    pygame.draw.circle(s, lt, (BS//2 - 2, BS - 21), 3)
    pygame.draw.circle(s, dk, (BS//2 - 2, BS - 22), 1)
    pygame.draw.circle(s, dk, (BS//2 + 2, BS - 22), 1)
    pygame.draw.line(s, c, (BS//2 - 7, BS - 14), (BS//2 - 11, BS - 10), 2)
    pygame.draw.line(s, c, (BS//2 + 7, BS - 14), (BS//2 + 11, BS - 10), 2)
    surfs[bid] = s

    bid = GARDEN_DOVECOTE
    # if bid == GARDEN_DOVECOTE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 20)
    pole = (110, 72, 38)
    s.fill((40, 55, 38))
    pygame.draw.line(s, pole, (BS//2, BS - 1), (BS//2, BS - 12), 2)
    pygame.draw.rect(s, dk, (BS//2 - 6, BS - 24, 12, 12))
    pygame.draw.rect(s, c, (BS//2 - 5, BS - 23, 10, 10))
    for hx in range(BS//2 - 4, BS//2 + 4, 4):
        pygame.draw.ellipse(s, dk, (hx, BS - 20, 3, 4))
    pygame.draw.polygon(s, dk, [(BS//2 - 7, BS - 24), (BS//2, BS - 30), (BS//2 + 7, BS - 24)])
    pygame.draw.polygon(s, lt, [(BS//2 - 6, BS - 24), (BS//2, BS - 29), (BS//2 + 6, BS - 24)])
    surfs[bid] = s

    bid = STONE_HEDGEHOG
    # if bid == STONE_HEDGEHOG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    s.fill(_darken(c, 28))
    pygame.draw.ellipse(s, dk, (4, BS - 17, 20, 11))
    pygame.draw.ellipse(s, c, (5, BS - 16, 18, 9))
    pygame.draw.circle(s, c, (21, BS - 14), 4)
    pygame.draw.circle(s, lt, (21, BS - 15), 2)
    pygame.draw.circle(s, dk, (22, BS - 15), 1)
    for ang in range(200, 340, 18):
        ex = 13 + int(11 * math.cos(math.radians(ang)))
        ey = BS - 12 + int(6 * math.sin(math.radians(ang)))
        pygame.draw.line(s, dk, (13, BS - 12), (ex, ey), 1)
    surfs[bid] = s

    bid = BIRD_TABLE
    # if bid == BIRD_TABLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    wood = (125, 80, 42)
    wood_dk = _darken(wood, 20)
    wood_lt = _lighter(wood, 15)
    s.fill((38, 52, 32))
    pygame.draw.line(s, wood, (BS//2, BS - 1), (BS//2, 12), 3)
    pygame.draw.rect(s, wood_dk, (2, 10, BS - 4, 4))
    pygame.draw.rect(s, wood, (3, 10, BS - 6, 3))
    pygame.draw.rect(s, wood_lt, (3, 10, BS - 6, 1))
    pygame.draw.polygon(s, wood_dk, [(2, 10), (BS//2, 4), (BS - 2, 10)])
    pygame.draw.polygon(s, wood, [(3, 10), (BS//2, 5), (BS - 3, 10)])
    for sx2, sy2 in [(6, 12), (12, 13), (20, 12), (25, 13)]:
        pygame.draw.circle(s, (190, 168, 120), (sx2, sy2), 1)
    surfs[bid] = s

    bid = GARDEN_CLOCK
    # if bid == GARDEN_CLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    face = (232, 228, 210)
    post = (80, 75, 70)
    s.fill((38, 52, 32))
    pygame.draw.line(s, post, (BS//2, BS - 1), (BS//2, BS - 14), 2)
    pygame.draw.circle(s, _darken(c, 20), (BS//2, BS - 20), 9)
    pygame.draw.circle(s, c, (BS//2, BS - 20), 8)
    pygame.draw.circle(s, face, (BS//2, BS - 20), 7)
    for hh in range(0, 12):
        hx = BS//2 + int(6 * math.cos(math.radians(hh * 30 - 90)))
        hy = BS - 20 + int(6 * math.sin(math.radians(hh * 30 - 90)))
        pygame.draw.circle(s, _darken(face, 25), (hx, hy), 1)
    pygame.draw.line(s, _darken(c, 30), (BS//2, BS - 20), (BS//2 + 3, BS - 24), 1)
    pygame.draw.line(s, _darken(c, 30), (BS//2, BS - 20), (BS//2 - 2, BS - 23), 1)
    surfs[bid] = s

    bid = GARDEN_OBELISK_METAL
    # if bid == GARDEN_OBELISK_METAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 15)
    s.fill((25, 35, 20))
    for cx2, cw in [(BS//2 - 5, 2), (BS//2 + 3, 2)]:
        pygame.draw.line(s, c, (cx2, BS - 2), (BS//2 - 1 + (cx2 - BS//2 + 5) // 5, 2), cw)
    for hy in range(6, BS - 2, 6):
        w = max(2, (BS - 2 - hy) // 4)
        pygame.draw.line(s, lt, (BS//2 - w - 3, hy), (BS//2 + w + 3, hy), 1)
    pygame.draw.circle(s, lt, (BS//2, 2), 2)
    green = (50, 110, 45)
    for gx2, gy2 in [(BS//2 - 4, 10), (BS//2 + 3, 15), (BS//2 - 3, 22)]:
        pygame.draw.line(s, green, (gx2, gy2), (gx2 + 4, gy2 - 3), 1)
    surfs[bid] = s

    bid = POTTING_TABLE
    # if bid == POTTING_TABLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    wood = (125, 82, 42)
    wood_dk = _darken(wood, 20)
    soil = (80, 52, 28)
    s.fill(_darken(wood, 32))
    pygame.draw.rect(s, wood_dk, (1, BS//2 - 2, BS - 2, BS//2))
    pygame.draw.rect(s, wood, (2, BS//2 - 1, BS - 4, BS//2 - 2))
    pygame.draw.rect(s, _lighter(wood, 12), (2, BS//2 - 1, BS - 4, 3))
    for px2 in range(2, BS - 2, 6):
        pygame.draw.line(s, wood_dk, (px2, BS//2 - 1), (px2, BS - 2), 1)
    pygame.draw.rect(s, soil, (3, BS//2 + 2, 8, 6))
    pygame.draw.rect(s, _lighter(soil, 15), (3, BS//2 + 2, 8, 2))
    tool_col = (130, 108, 80)
    pygame.draw.line(s, tool_col, (16, BS//2 - 6), (16, BS//2 - 12), 1)
    pygame.draw.ellipse(s, tool_col, (14, BS//2 - 14, 4, 3))
    pygame.draw.line(s, tool_col, (22, BS//2 - 6), (22, BS//2 - 12), 1)
    pygame.draw.polygon(s, tool_col, [(20, BS//2 - 12), (22, BS//2 - 15), (24, BS//2 - 12)])
    surfs[bid] = s

    bid = COMPOST_HEAP
    # if bid == COMPOST_HEAP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    base = BLOCKS[bid]["color"]
    mid = _lighter(base, 15)
    top_col = (95, 75, 35)
    s.fill(_darken(base, 20))
    pygame.draw.ellipse(s, base, (2, BS//3, BS - 4, BS - BS//3 - 1))
    pygame.draw.ellipse(s, mid, (4, BS//3 + 2, BS - 8, BS - BS//3 - 7))
    pygame.draw.ellipse(s, _darken(top_col, 10), (6, BS//3 - 2, BS - 12, BS//4))
    pygame.draw.ellipse(s, top_col, (7, BS//3 - 1, BS - 14, BS//4 - 2))
    green = (70, 130, 48)
    brown = (120, 78, 35)
    for cx2, cy2 in [(5, BS//2), (14, BS//2 + 2), (22, BS//2 - 1), (9, BS//2 + 7), (19, BS//2 + 6)]:
        pygame.draw.circle(s, green if (cx2 + cy2) % 3 == 0 else brown, (cx2, cy2), 2)
    surfs[bid] = s

    bid = GARDEN_TOAD_HOUSE
    # if bid == GARDEN_TOAD_HOUSE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    door = (80, 52, 28)
    s.fill((38, 52, 32))
    pygame.draw.ellipse(s, dk, (3, BS - 20, BS - 6, 18))
    pygame.draw.ellipse(s, c, (4, BS - 19, BS - 8, 16))
    pygame.draw.ellipse(s, lt, (5, BS - 18, BS - 12, 8))
    pygame.draw.ellipse(s, door, (BS//2 - 4, BS - 16, 8, 10))
    pygame.draw.ellipse(s, _darken(door, 30), (BS//2 - 3, BS - 15, 6, 8))
    pygame.draw.circle(s, lt, (BS//2 + 2, BS - 12), 1)
    pygame.draw.ellipse(s, _lighter(c, 12), (6, BS - 19, 5, 4))
    for sx2 in [8, 20]:
        pygame.draw.circle(s, lt, (sx2, BS - 22), 2)
    surfs[bid] = s

    bid = WISTERIA_WALL
    # if bid == WISTERIA_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    wist = (160, 100, 190)
    wist_lt = _lighter(wist, 18)
    BS = BLOCK_SIZE
    # stone wall background
    stone = (145, 138, 125)
    s.fill(stone)
    # cascading wisteria clusters
    stem = (85, 60, 35)
    for cx2 in range(3, BS, 7):
        drop = 4 + (cx2 % 5)
        pygame.draw.line(s, stem, (cx2, 0), (cx2, drop), 1)
        for dy2 in range(drop, drop + 10, 3):
            if dy2 < BS:
                pygame.draw.circle(s, wist, (cx2, dy2), 2)
                if dy2 + 2 < BS:
                    pygame.draw.circle(s, wist_lt, (cx2-1, dy2), 1)
    # some green leaves between clusters
    leaf = (65, 110, 50)
    for lx, ly in [(2,4),(9,2),(16,6),(23,3),(29,5)]:
        pygame.draw.circle(s, leaf, (lx, ly), 2)
    surfs[bid] = s

    bid = POTTED_CITRUS
    # if bid == POTTED_CITRUS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # pot (same shape as TERRACOTTA_PLANTER)
    pts = [(5, BS-3), (BS-5, BS-3), (BS-8, BS//2+2), (8, BS//2+2)]
    pygame.draw.polygon(s, c, pts)
    pygame.draw.line(s, lt, (5, BS-3), (BS-5, BS-3), 1)
    # soil
    pygame.draw.ellipse(s, (75, 52, 30), (8, BS//2-6, BS-16, 6))
    # trunk
    trunk = (110, 75, 40)
    pygame.draw.line(s, trunk, (BS//2, BS//2-5), (BS//2, BS//2-12), 2)
    # canopy
    foliage = (50, 120, 45)
    pygame.draw.circle(s, foliage, (BS//2, BS//2-16), 8)
    # citrus fruit dots
    fruit = (230, 140, 30)
    for fx, fy in [(BS//2-4, BS//2-18), (BS//2+4, BS//2-15), (BS//2, BS//2-13),
                   (BS//2-5, BS//2-13)]:
        if fy > 0:
            pygame.draw.circle(s, fruit, (fx, fy), 2)
    surfs[bid] = s

    bid = MARBLE_STATUE
    # if bid == MARBLE_STATUE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # base plinth
    pygame.draw.rect(s, dk, (4, BS-6, BS-8, 6))
    pygame.draw.line(s, lt, (4, BS-6), (BS-4, BS-6), 1)
    # figure body (draped form)
    pygame.draw.rect(s, c, (BS//2-5, BS//2-4, 10, BS//2))
    # folds
    pygame.draw.line(s, dk, (BS//2-3, BS//2-2), (BS//2-5, BS-7), 1)
    pygame.draw.line(s, dk, (BS//2+2, BS//2), (BS//2+4, BS-7), 1)
    # head
    pygame.draw.circle(s, c, (BS//2, BS//2-8), 5)
    pygame.draw.circle(s, lt, (BS//2-1, BS//2-9), 2)
    # arm raised
    pygame.draw.line(s, c, (BS//2+5, BS//2-2), (BS-3, BS//2-10), 2)
    surfs[bid] = s

    bid = MARBLE_BIRDBATH
    # if bid == MARBLE_BIRDBATH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 20)
    water = (100, 165, 210)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # base
    pygame.draw.rect(s, dk, (BS//2-5, BS-5, 10, 5))
    # pedestal shaft
    pygame.draw.rect(s, c, (BS//2-2, BS//2, 4, BS//2-5))
    # basin (wide shallow bowl)
    pygame.draw.ellipse(s, c, (3, BS//2-5, BS-6, 10))
    pygame.draw.ellipse(s, lt, (3, BS//2-5, BS-6, 10), 1)
    # water surface
    pygame.draw.ellipse(s, water, (5, BS//2-3, BS-10, 6))
    # ripple
    pygame.draw.ellipse(s, _lighter(water, 18), (BS//2-4, BS//2-2, 8, 3), 1)
    surfs[bid] = s

    bid = GARDEN_TABLE
    # if bid == GARDEN_TABLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # legs
    leg = dk
    pygame.draw.rect(s, leg, (4, BS//2+1, 3, BS//2-2))
    pygame.draw.rect(s, leg, (BS-7, BS//2+1, 3, BS//2-2))
    # tabletop slab
    pygame.draw.rect(s, c, (1, BS//2-4, BS-2, 6))
    pygame.draw.line(s, lt, (1, BS//2-4), (BS-2, BS//2-4), 1)
    pygame.draw.line(s, lt, (1, BS//2-4), (1, BS//2+2), 1)
    # surface detail: small flower/object on table
    pygame.draw.circle(s, (190, 155, 60), (BS//2, BS//2-2), 2)
    surfs[bid] = s

    bid = IRON_TRELLIS
    # if bid == IRON_TRELLIS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 28)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 50))
    # diagonal lattice
    for i in range(-BS, BS*2, 8):
        pygame.draw.line(s, c, (i, 0), (i+BS, BS), 1)
        pygame.draw.line(s, c, (i, BS), (i+BS, 0), 1)
    # border frame
    pygame.draw.rect(s, lt, (0, 0, BS, 2))
    pygame.draw.rect(s, lt, (0, BS-2, BS, 2))
    pygame.draw.rect(s, lt, (0, 0, 2, BS))
    pygame.draw.rect(s, lt, (BS-2, 0, 2, BS))
    surfs[bid] = s

    bid = NASRID_PANEL
    # if bid == NASRID_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 30)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    s.fill(c)
    # dense Nasrid-style geometric inlay: radiating star lines
    cx2, cy2 = BS//2, BS//2
    for ai in range(8):
        ang = math.pi * ai / 4
        ex2 = cx2 + int(12 * math.cos(ang))
        ey2 = cy2 + int(12 * math.sin(ang))
        pygame.draw.line(s, dk, (cx2, cy2), (ex2, ey2), 1)
    # concentric octagon
    r8 = 10
    oct_pts = [(cx2 + int(r8*math.cos(math.pi*i/4 + math.pi/8)),
                cy2 + int(r8*math.sin(math.pi*i/4 + math.pi/8)))
               for i in range(8)]
    pygame.draw.polygon(s, lt, oct_pts, 1)
    # corner floral motifs
    for cxf, cyf in [(4,4),(BS-5,4),(4,BS-5),(BS-5,BS-5)]:
        pygame.draw.circle(s, dk, (cxf, cyf), 3, 1)
        for ai2 in [0, math.pi/2, math.pi, 3*math.pi/2]:
            pygame.draw.line(s, dk, (cxf, cyf),
                             (cxf+int(3*math.cos(ai2)), cyf+int(3*math.sin(ai2))), 1)
    pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
    surfs[bid] = s

    bid = SCALLOP_NICHE
    # if bid == SCALLOP_NICHE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 28)
    lt = _lighter(c, 14)
    inside = _darken(c, 40)
    BS = BLOCK_SIZE
    s.fill(c)
    # niche recess (dark interior)
    pygame.draw.ellipse(s, inside, (4, 4, BS-8, BS-8))
    # scallop shell ribs radiating from bottom center
    cx2 = BS//2
    cy2 = BS - 4
    for ai in range(-4, 5):
        ang = math.pi * ai / 8
        ex2 = cx2 + int(12 * math.cos(ang - math.pi/2))
        ey2 = cy2 + int(12 * math.sin(ang - math.pi/2))
        pygame.draw.line(s, dk, (cx2, cy2), (ex2, ey2), 1)
    # arch border
    pygame.draw.arc(s, dk, (3, 3, BS-6, BS-6), 0, math.pi, 2)
    pygame.draw.line(s, lt, (1, 2), (BS-2, 2), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = TERRACE_BALUSTRADE
    # if bid == TERRACE_BALUSTRADE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 30))
    # top and bottom rail
    pygame.draw.rect(s, c, (0, 1, BS, 4))
    pygame.draw.rect(s, c, (0, BS-5, BS, 4))
    pygame.draw.line(s, lt, (0, 1), (BS, 1), 1)
    pygame.draw.line(s, lt, (0, BS-5), (BS, BS-5), 1)
    # classical vase-shaped balusters
    for bx2 in [4, 12, 20, 28]:
        # shaft
        pygame.draw.line(s, c, (bx2+1, 5), (bx2+1, BS-5), 2)
        # belly swell
        pygame.draw.ellipse(s, lt, (bx2-1, BS//2-3, 5, 6))
        # top cap
        pygame.draw.rect(s, dk, (bx2-1, 4, 4, 2))
        # base cap
        pygame.draw.rect(s, dk, (bx2-1, BS-7, 4, 2))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = ZEN_GRAVEL
    # if bid == ZEN_GRAVEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    # parallel raked lines
    for ry in range(3, BS, 5):
        pygame.draw.line(s, dk, (0, ry), (BS, ry), 1)
    # perpendicular crossing rakes (lighter)
    for rx in range(BS//3, BS, BS//3):
        pygame.draw.line(s, _darken(c, 8), (rx, 0), (rx, BS), 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = KARESANSUI_ROCK
    # if bid == KARESANSUI_ROCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    # sand bed
    sand = _lighter(c, 30)
    s.fill(sand)
    # concentric rings around rock
    for r2 in [11, 8]:
        pygame.draw.ellipse(s, _darken(sand, 10), (BS//2-r2, BS//2-r2+2, r2*2, r2*2-4), 1)
    # rock mass
    pts = [(BS//2-5, BS//2+4), (BS//2+5, BS//2+4), (BS//2+7, BS//2-1),
           (BS//2+3, BS//2-6), (BS//2-3, BS//2-6), (BS//2-7, BS//2-1)]
    pygame.draw.polygon(s, c, pts)
    pygame.draw.polygon(s, lt, pts, 1)
    pygame.draw.circle(s, lt, (BS//2-2, BS//2-3), 2)
    surfs[bid] = s

    bid = MOSS_CARPET
    # if bid == MOSS_CARPET
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(c)
    # bumpy moss texture
    for ty in range(0, BS, 4):
        for tx in range(0, BS, 4):
            bump = lt if (tx + ty) % 8 == 0 else dk
            pygame.draw.circle(s, bump, (tx+2, ty+2), 2)
    surfs[bid] = s

    bid = TSUKUBAI
    # if bid == TSUKUBAI
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    water = (80, 155, 205)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # low stone basin
    pygame.draw.rect(s, c, (3, BS//2, BS-6, BS//2-3))
    pygame.draw.line(s, lt, (3, BS//2), (BS-3, BS//2), 1)
    # water surface
    pygame.draw.ellipse(s, water, (5, BS//2+2, BS-10, 8))
    # bamboo spout above
    bamboo = (130, 150, 55)
    pygame.draw.line(s, bamboo, (BS//2+4, 4), (BS//2, BS//2+1), 2)
    pygame.draw.line(s, _lighter(bamboo, 15), (BS//2+5, 4), (BS//2+5, BS//2-2), 1)
    surfs[bid] = s

    bid = TORO_LANTERN
    # if bid == TORO_LANTERN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 22)
    amber = (210, 155, 60)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 40))
    # base slab
    pygame.draw.rect(s, dk, (4, BS-5, BS-8, 5))
    # shaft
    pygame.draw.rect(s, c, (BS//2-2, BS//2, 4, BS//2-5))
    # cap platform
    pygame.draw.rect(s, c, (3, BS//2-3, BS-6, 4))
    pygame.draw.line(s, lt, (3, BS//2-3), (BS-3, BS//2-3), 1)
    # lantern chamber
    pygame.draw.rect(s, _darken(c, 15), (6, 8, BS-12, BS//2-10))
    pygame.draw.rect(s, amber, (7, 9, BS-14, BS//2-12))
    # roof cap
    pygame.draw.rect(s, c, (2, 5, BS-4, 4))
    pygame.draw.line(s, lt, (2, 5), (BS-2, 5), 1)
    surfs[bid] = s

    bid = YUKIMI_LANTERN
    # if bid == YUKIMI_LANTERN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 22)
    amber = (210, 155, 60)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 40))
    # three short legs
    for lx in [5, BS//2, BS-7]:
        pygame.draw.line(s, dk, (lx, BS-2), (lx, BS//2+4), 2)
    # wide cap roof (large flat overhang)
    pygame.draw.rect(s, c, (0, 4, BS, 5))
    pygame.draw.line(s, lt, (0, 4), (BS, 4), 1)
    # lantern body
    pygame.draw.ellipse(s, amber, (5, 9, BS-10, BS//2-4))
    pygame.draw.ellipse(s, _lighter(amber, 20), (7, 11, BS-14, 6))
    surfs[bid] = s

    bid = BAMBOO_FENCE_JP
    # if bid == BAMBOO_FENCE_JP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 45))
    # vertical bamboo poles
    for bx2 in range(3, BS, 6):
        pygame.draw.rect(s, c, (bx2, 0, 4, BS))
        pygame.draw.line(s, lt, (bx2+1, 0), (bx2+1, BS), 1)
        # internodes
        for ky in range(6, BS, 8):
            pygame.draw.line(s, dk, (bx2, ky), (bx2+4, ky), 1)
    # horizontal lashing cords
    for ry in [BS//3, 2*BS//3]:
        pygame.draw.line(s, (110, 80, 40), (0, ry), (BS, ry), 1)
    surfs[bid] = s

    bid = ROJI_STONE
    # if bid == ROJI_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    BS = BLOCK_SIZE
    moss = (52, 90, 38)
    s.fill(moss)
    # irregular stone
    pts = [(4, 10), (BS-6, 7), (BS-4, BS-8), (6, BS-6)]
    pygame.draw.polygon(s, c, pts)
    pygame.draw.polygon(s, lt, pts, 1)
    # moss edges
    for mx, my in [(2,8),(BS-4,6),(3,BS-5),(BS-3,BS-4)]:
        pygame.draw.circle(s, moss, (mx, my), 2)
    surfs[bid] = s

    bid = PINE_TOPIARY_JP
    # if bid == PINE_TOPIARY_JP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    trunk = (100, 65, 35)
    s.fill(_darken(c, 50))
    pygame.draw.rect(s, trunk, (BS//2-1, BS-6, 3, 6))
    # cloud-pruned: 3 rounded cloud puffs at different heights
    for cx2, cy2, r2 in [(BS//2, BS-10, 6), (BS//2-5, BS-18, 5), (BS//2+5, BS-18, 5),
                         (BS//2, BS-26, 5)]:
        if cy2 > 0:
            pygame.draw.circle(s, dk, (cx2, cy2), r2)
            pygame.draw.circle(s, c, (cx2-1, cy2-1), r2-2)
            pygame.draw.circle(s, lt, (cx2-2, cy2-2), 2)
    surfs[bid] = s

    bid = JAPANESE_MAPLE
    # if bid == JAPANESE_MAPLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 15)
    BS = BLOCK_SIZE
    trunk = (90, 60, 35)
    s.fill(_darken(c, 50))
    pygame.draw.rect(s, trunk, (BS//2-1, BS-8, 3, 8))
    # airy maple canopy using scattered small circles
    for cx2, cy2, r2 in [(BS//2, BS//2-4, 7), (BS//2-6, BS//2-2, 5),
                         (BS//2+6, BS//2-2, 5), (BS//2-3, BS//2-10, 4),
                         (BS//2+3, BS//2-10, 4)]:
        if cy2 > 0:
            pygame.draw.circle(s, dk, (cx2, cy2), r2)
            pygame.draw.circle(s, c, (cx2, cy2), r2-1)
            pygame.draw.circle(s, lt, (cx2-1, cy2-1), 2)
    surfs[bid] = s

    bid = SHISHI_ODOSHI
    # if bid == SHISHI_ODOSHI
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(_darken(c, 45))
    bamboo = (130, 155, 55)
    stone = (120, 115, 108)
    # basin stone
    pygame.draw.ellipse(s, stone, (2, BS-8, BS-4, 7))
    pygame.draw.ellipse(s, _lighter(stone, 10), (2, BS-8, BS-4, 7), 1)
    # pivot post
    pygame.draw.line(s, bamboo, (BS//2, BS//2), (BS//2, BS-8), 2)
    # clapper arm (angled)
    pygame.draw.line(s, bamboo, (4, 8), (BS//2, BS//2), 3)
    pygame.draw.line(s, _lighter(bamboo, 15), (5, 8), (BS//2+1, BS//2), 1)
    # water droplet
    pygame.draw.circle(s, (100, 170, 210), (6, 10), 2)
    surfs[bid] = s

    bid = RED_ARCH_BRIDGE
    # if bid == RED_ARCH_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 50))
    # arch body
    pts = [(0, BS-4), (BS, BS-4), (BS-2, BS//2), (2, BS//2)]
    pygame.draw.polygon(s, c, pts)
    # arch curve underside
    pygame.draw.arc(s, dk, (2, BS//2-6, BS-4, 12), 0, math.pi, 3)
    # handrails
    pygame.draw.line(s, lt, (2, BS//2), (2, BS-4), 2)
    pygame.draw.line(s, lt, (BS-2, BS//2), (BS-2, BS-4), 2)
    # deck planks
    for py in range(BS//2+4, BS-3, 4):
        pygame.draw.line(s, lt, (2, py), (BS-2, py), 1)
    surfs[bid] = s

    bid = WAVE_CERAMIC
    # if bid == WAVE_CERAMIC
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 25)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 20))
    # white background
    bg = (230, 235, 245)
    pygame.draw.rect(s, bg, (1, 1, BS-2, BS-2))
    # blue wave arcs
    for wy in range(4, BS, 8):
        for wx in range(-4, BS+4, 12):
            pygame.draw.arc(s, c, (wx, wy-2, 12, 8), 0, math.pi, 2)
    pygame.draw.rect(s, _darken(c, 30), s.get_rect(), 1)
    surfs[bid] = s

    bid = ZEN_SAND_RING
    # if bid == ZEN_SAND_RING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    s.fill(c)
    cx2, cy2 = BS//2, BS//2
    # concentric raked circles
    for r2 in [12, 9, 6, 3]:
        pygame.draw.circle(s, dk, (cx2, cy2), r2, 1)
    # center stone
    pygame.draw.circle(s, _darken(c, 35), (cx2, cy2), 3)
    pygame.draw.circle(s, _lighter(c, 10), (cx2-1, cy2-1), 1)
    surfs[bid] = s

    bid = BAMBOO_GATE_JP
    # if bid == BAMBOO_GATE_JP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 50))
    bamboo = c
    # two vertical posts
    for px2 in [3, BS-7]:
        pygame.draw.rect(s, bamboo, (px2, 0, 4, BS))
        for ky in range(6, BS, 8):
            pygame.draw.line(s, dk, (px2, ky), (px2+4, ky), 1)
    # horizontal cross rails
    for ry in [BS//4, BS//2, 3*BS//4]:
        pygame.draw.rect(s, bamboo, (7, ry-1, BS-14, 3))
        pygame.draw.line(s, lt, (7, ry-1), (BS-7, ry-1), 1)
    surfs[bid] = s

    bid = WABI_STONE
    # if bid == WABI_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    moss = (50, 85, 38)
    s.fill(_darken(c, 40))
    # irregular weathered stone
    pts = [(5, 12), (BS-7, 9), (BS-5, BS-8), (8, BS-5), (3, BS//2)]
    pygame.draw.polygon(s, c, pts)
    pygame.draw.polygon(s, lt, pts, 1)
    # moss patches
    for mx, my in [(6, 11), (BS-8, 10), (7, BS-7)]:
        pygame.draw.circle(s, moss, (mx, my), 3)
    # cracks
    pygame.draw.line(s, dk, (10, 16), (16, 22), 1)
    surfs[bid] = s

    bid = CHERRY_ARCH
    # if bid == CHERRY_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    inside = _darken(c, 40)
    s.fill(c)
    ax, aw = 5, BS - 10
    at = 4
    pygame.draw.rect(s, inside, (ax+2, at+aw//2, aw-4, BS - at - aw//2 - 2))
    pygame.draw.arc(s, dk, (ax, at, aw, aw), 0, math.pi, 3)
    pygame.draw.line(s, dk, (ax, at+aw//2), (ax, BS-2), 3)
    pygame.draw.line(s, dk, (ax+aw, at+aw//2), (ax+aw, BS-2), 3)
    # cherry blossoms
    blossom = (240, 180, 195)
    for bx2, by2 in [(4,5),(9,3),(14,6),(20,3),(26,5),(7,10),(22,9)]:
        pygame.draw.circle(s, blossom, (bx2, by2), 2)
        pygame.draw.circle(s, (220, 140, 160), (bx2, by2), 1)
    surfs[bid] = s

    bid = TATAMI_PAVING
    # if bid == TATAMI_PAVING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 18)
    border = _darken(c, 30)
    BS = BLOCK_SIZE
    s.fill(c)
    half = BS // 2
    # two tatami rectangles side by side
    pygame.draw.rect(s, lt, (1, 1, half-2, BS-2))
    pygame.draw.rect(s, c, (half+1, 1, half-2, BS-2))
    # tatami weave lines on each half
    for ty in range(3, BS-2, 4):
        pygame.draw.line(s, dk, (1, ty), (half-2, ty), 1)
        pygame.draw.line(s, dk, (half+1, ty), (BS-2, ty), 1)
    # border strip
    pygame.draw.line(s, border, (half-1, 0), (half-1, BS), 1)
    pygame.draw.line(s, border, (half, 0), (half, BS), 1)
    pygame.draw.rect(s, border, s.get_rect(), 1)
    surfs[bid] = s

    bid = IKEBANA_STONE
    # if bid == IKEBANA_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 30))
    # flat presentation stone
    pygame.draw.rect(s, c, (2, BS//2, BS-4, BS//2-3))
    pygame.draw.line(s, lt, (2, BS//2), (BS-2, BS//2), 1)
    # simple flower arrangement above
    stem = (80, 120, 50)
    pygame.draw.line(s, stem, (BS//2, BS//2-1), (BS//2, 6), 1)
    pygame.draw.line(s, stem, (BS//2, BS//4), (BS//2-5, 4), 1)
    pygame.draw.line(s, stem, (BS//2, BS//4), (BS//2+5, 4), 1)
    pygame.draw.circle(s, (200, 100, 130), (BS//2, 5), 3)
    pygame.draw.circle(s, (220, 180, 60), (BS//2-6, 3), 2)
    pygame.draw.circle(s, (200, 100, 130), (BS//2+6, 3), 2)
    surfs[bid] = s

    bid = KANJI_STONE
    # if bid == KANJI_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 30)
    BS = BLOCK_SIZE
    s.fill(c)
    pygame.draw.line(s, lt, (1, 2), (BS-2, 2), 1)
    # brushstroke-style kanji: horizontal bar + vertical + diagonals
    pygame.draw.line(s, dk, (6, 8), (BS-6, 8), 2)
    pygame.draw.line(s, dk, (BS//2, 8), (BS//2, BS-6), 2)
    pygame.draw.line(s, dk, (8, 14), (BS//2-2, 20), 1)
    pygame.draw.line(s, dk, (BS-8, 14), (BS//2+2, 20), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = MAPLE_LEAF_TILE
    # if bid == MAPLE_LEAF_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    dk = _darken(c, 20)
    stone = (175, 168, 155)
    BS = BLOCK_SIZE
    s.fill(stone)
    cx2, cy2 = BS//2, BS//2
    # five-pointed maple leaf using lines from center
    for ai in range(5):
        ang = math.pi * ai * 2 / 5 - math.pi / 2
        ex2 = cx2 + int(10 * math.cos(ang))
        ey2 = cy2 + int(10 * math.sin(ang))
        pygame.draw.line(s, c, (cx2, cy2), (ex2, ey2), 2)
        pygame.draw.circle(s, lt, (ex2, ey2), 2)
    pygame.draw.circle(s, c, (cx2, cy2), 3)
    pygame.draw.rect(s, _darken(stone, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = NOREN_PANEL
    # if bid == NOREN_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 40))
    # top rod
    pygame.draw.rect(s, (100, 80, 50), (0, 2, BS, 3))
    # two split fabric panels
    panel_c = c
    pygame.draw.rect(s, panel_c, (1, 5, BS//2-2, BS-7))
    pygame.draw.rect(s, _darken(c, 15), (BS//2+1, 5, BS//2-2, BS-7))
    # fabric stripes
    for sy in range(8, BS-5, 6):
        pygame.draw.line(s, lt, (1, sy), (BS//2-2, sy), 1)
        pygame.draw.line(s, lt, (BS//2+1, sy), (BS-2, sy), 1)
    surfs[bid] = s

    bid = TSURU_TILE
    # if bid == TSURU_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 25)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    s.fill(c)
    pygame.draw.line(s, lt, (1, 2), (BS-2, 2), 1)
    # simplified crane silhouette: body + neck + wing
    cx2, cy2 = BS//2, BS//2+2
    # body oval
    pygame.draw.ellipse(s, dk, (cx2-6, cy2-4, 12, 8))
    # long neck + head
    pygame.draw.line(s, dk, (cx2-4, cy2-4), (cx2-8, cy2-12), 2)
    pygame.draw.circle(s, dk, (cx2-9, cy2-13), 2)
    # red head dot
    pygame.draw.circle(s, (180, 30, 30), (cx2-9, cy2-14), 1)
    # wing spread
    pygame.draw.line(s, dk, (cx2+4, cy2-2), (cx2+12, cy2-8), 2)
    pygame.draw.line(s, dk, (cx2+4, cy2-2), (cx2+12, cy2+2), 1)
    # legs
    pygame.draw.line(s, dk, (cx2-2, cy2+4), (cx2-4, cy2+10), 1)
    pygame.draw.line(s, dk, (cx2+2, cy2+4), (cx2+2, cy2+10), 1)
    pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
    surfs[bid] = s

    bid = PINE_SCREEN_JP
    # if bid == PINE_SCREEN_JP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    s.fill(c)
    # shōji grid
    pygame.draw.line(s, dk, (BS//2, 0), (BS//2, BS), 1)
    pygame.draw.line(s, dk, (0, BS//3), (BS, BS//3), 1)
    pygame.draw.line(s, dk, (0, 2*BS//3), (BS, 2*BS//3), 1)
    # pine bough in upper-right panel
    pine = (45, 90, 40)
    pygame.draw.line(s, (100, 70, 40), (BS//2+2, 2), (BS-2, BS//3-2), 1)
    for nx in range(BS//2+4, BS-2, 4):
        pygame.draw.line(s, pine, (nx, 4), (nx+2, 8), 1)
        pygame.draw.line(s, pine, (nx, 4), (nx-2, 8), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = KARE_BRIDGE
    # if bid == KARE_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    # gravel below
    gravel = (200, 195, 182)
    s.fill(gravel)
    for ry in range(3, BS, 5):
        pygame.draw.line(s, _darken(gravel, 12), (0, ry), (BS, ry), 1)
    # flat stone bridge slabs
    pygame.draw.rect(s, c, (1, BS//2-4, BS-2, 8))
    pygame.draw.line(s, lt, (1, BS//2-4), (BS-2, BS//2-4), 1)
    # plank lines
    for px2 in range(5, BS-2, 6):
        pygame.draw.line(s, dk, (px2, BS//2-4), (px2, BS//2+4), 1)
    surfs[bid] = s

    bid = PEBBLE_MOSAIC_CN
    # if bid == PEBBLE_MOSAIC_CN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(_darken(c, 20))
    # scattered small pebbles in alternating colors
    peb_cols = [c, _lighter(c, 20), _darken(c, 18), _lighter(c, 8)]
    positions = [(3,4),(7,2),(12,6),(17,3),(22,5),(27,4),(2,11),(6,9),(11,13),
                 (16,10),(21,12),(26,9),(4,18),(8,15),(13,19),(18,16),(23,18),
                 (28,14),(3,24),(7,22),(12,26),(17,23),(22,25),(27,21),(5,29)]
    for i, (px2, py2) in enumerate(positions):
        if px2 < BS and py2 < BS:
            pygame.draw.ellipse(s, peb_cols[i%4], (px2-2, py2-1, 4, 3))
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = ZIGZAG_BRIDGE
    # if bid == ZIGZAG_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    water = (60, 130, 175)
    BS = BLOCK_SIZE
    s.fill(water)
    # zigzag planks
    pts = [(0, BS-6), (BS//3, BS-6), (BS//3, BS//2), (2*BS//3, BS//2),
           (2*BS//3, 6), (BS, 6)]
    for i in range(len(pts)-1):
        pygame.draw.line(s, c, pts[i], pts[i+1], 5)
        pygame.draw.line(s, lt, pts[i], pts[i+1], 1)
    surfs[bid] = s

    bid = CLOUD_WALL
    # if bid == CLOUD_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(c)
    pygame.draw.line(s, dk, (1, 2), (BS-2, 2), 1)
    pygame.draw.line(s, dk, (1, BS-3), (BS-2, BS-3), 1)
    # cloud-shaped window opening (dark inside)
    inside = _darken(c, 45)
    cx2, cy2 = BS//2, BS//2
    # cloud outline: circles
    pygame.draw.circle(s, inside, (cx2, cy2), 7)
    pygame.draw.circle(s, inside, (cx2-5, cy2+2), 5)
    pygame.draw.circle(s, inside, (cx2+5, cy2+2), 5)
    pygame.draw.circle(s, inside, (cx2-5, cy2-2), 5)
    pygame.draw.circle(s, inside, (cx2+5, cy2-2), 5)
    surfs[bid] = s

    bid = DRAGON_WALL_CN
    # if bid == DRAGON_WALL_CN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 22)
    dk = _darken(c, 25)
    wall_c = (175, 168, 155)
    BS = BLOCK_SIZE
    s.fill(wall_c)
    pygame.draw.line(s, _darken(wall_c, 15), (0, BS//2), (BS, BS//2), 1)
    # sinuous dragon crest on top half
    prev = (0, BS//3)
    for wx in range(0, BS, 4):
        wy = BS//3 + int(4 * math.sin(wx * 0.4))
        pygame.draw.line(s, c, prev, (wx, wy), 2)
        pygame.draw.line(s, lt, prev, (wx, wy-1), 1)
        prev = (wx, wy)
    # scales: small arcs along the dragon
    for wx in range(4, BS, 8):
        wy = BS//3 + int(4 * math.sin(wx * 0.4))
        pygame.draw.arc(s, dk, (wx-3, wy-2, 6, 4), 0, math.pi, 1)
    surfs[bid] = s

    bid = LOTUS_POND
    # if bid == LOTUS_POND
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 15))
    pygame.draw.ellipse(s, c, (1, 3, BS-2, BS-6))
    # lily pads
    pad = (45, 115, 50)
    for px2, py2 in [(6, BS//2-2), (BS-10, BS//2+2), (BS//2, BS//2-4)]:
        pygame.draw.circle(s, pad, (px2, py2), 4)
        pygame.draw.line(s, _darken(pad, 20), (px2, py2), (px2+2, py2-4), 1)
    # lotus flowers
    lotus = (230, 160, 185)
    pygame.draw.circle(s, lotus, (6, BS//2-2), 2)
    pygame.draw.circle(s, (240, 240, 200), (BS//2, BS//2-4), 2)
    surfs[bid] = s

    bid = HEX_PAVILION_TILE
    # if bid == HEX_PAVILION_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 15))
    cx2, cy2 = BS//2, BS//2
    r2 = 11
    # hexagon
    hex_pts = [(cx2 + int(r2*math.cos(math.pi*i/3 - math.pi/6)),
                cy2 + int(r2*math.sin(math.pi*i/3 - math.pi/6))) for i in range(6)]
    pygame.draw.polygon(s, c, hex_pts)
    pygame.draw.polygon(s, lt, hex_pts, 1)
    # inner decoration lines
    for pt in hex_pts:
        pygame.draw.line(s, dk, (cx2, cy2), pt, 1)
    surfs[bid] = s

    bid = COMPASS_PAVING
    # if bid == COMPASS_PAVING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    dk = _darken(c, 28)
    BS = BLOCK_SIZE
    s.fill(c)
    cx2, cy2 = BS//2, BS//2
    # eight compass points
    for ai in range(8):
        ang = math.pi * ai / 4
        ex2 = cx2 + int(12 * math.cos(ang))
        ey2 = cy2 + int(12 * math.sin(ang))
        col = dk if ai % 2 == 0 else _darken(c, 14)
        pygame.draw.line(s, col, (cx2, cy2), (ex2, ey2), 2)
    pygame.draw.circle(s, lt, (cx2, cy2), 4)
    pygame.draw.circle(s, dk, (cx2, cy2), 4, 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = WAVE_BALUSTRADE_CN
    # if bid == WAVE_BALUSTRADE_CN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 30))
    # top and bottom rails
    pygame.draw.rect(s, c, (0, 1, BS, 4))
    pygame.draw.rect(s, c, (0, BS-5, BS, 4))
    pygame.draw.line(s, lt, (0, 1), (BS, 1), 1)
    # wave-carved middle band
    prev = (0, BS//2)
    for wx in range(0, BS):
        wy = BS//2 + int(3 * math.sin(wx * 0.5))
        pygame.draw.line(s, dk, prev, (wx, wy), 1)
        prev = (wx, wy)
    # cloud motif balusters
    for bx2 in [6, BS//2, BS-8]:
        pygame.draw.ellipse(s, c, (bx2-3, 5, 6, 4))
        pygame.draw.line(s, c, (bx2, 9), (bx2, BS-5), 1)
    surfs[bid] = s

    bid = CERAMIC_SEAT
    # if bid == CERAMIC_SEAT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 25)
    white = (235, 238, 245)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 40))
    # barrel shape
    pygame.draw.ellipse(s, white, (4, 2, BS-8, BS-4))
    pygame.draw.ellipse(s, c, (6, 4, BS-12, BS-8), 1)
    # blue wave decoration band
    for wx in range(6, BS-6, 3):
        wy = BS//2 + int(3 * math.sin(wx * 0.6))
        pygame.draw.circle(s, c, (wx, wy), 1)
    # top surface
    pygame.draw.ellipse(s, white, (5, 2, BS-10, 6))
    surfs[bid] = s

    bid = BONSAI_TRAY
    # if bid == BONSAI_TRAY
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # tray slab
    pygame.draw.rect(s, c, (2, BS//2+1, BS-4, BS//2-4))
    pygame.draw.line(s, lt, (2, BS//2+1), (BS-2, BS//2+1), 1)
    # small tree: trunk + cloud puffs
    trunk = (90, 60, 35)
    pygame.draw.line(s, trunk, (BS//2, BS//2), (BS//2, BS//2-12), 2)
    pygame.draw.line(s, trunk, (BS//2, BS//2-8), (BS//2-5, BS//2-14), 1)
    foliage = (38, 92, 42)
    for cx2, cy2, r2 in [(BS//2-4, BS//2-16, 4), (BS//2+4, BS//2-16, 4),
                         (BS//2, BS//2-20, 4)]:
        if cy2 > 0:
            pygame.draw.circle(s, foliage, (cx2, cy2), r2)
    surfs[bid] = s

    bid = SCHOLAR_SCREEN
    # if bid == SCHOLAR_SCREEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 30))
    # lattice frame
    pygame.draw.rect(s, c, (1, 1, BS-2, BS-2), 2)
    for ry in [BS//3, 2*BS//3]:
        pygame.draw.line(s, c, (3, ry), (BS-3, ry), 1)
    for rx in [BS//3, 2*BS//3]:
        pygame.draw.line(s, c, (rx, 3), (rx, BS-3), 1)
    # scholar's rock silhouette in center cell
    rock = (95, 90, 82)
    pts = [(BS//2-4, BS//2+3), (BS//2+4, BS//2+3), (BS//2+6, BS//2-2),
           (BS//2+2, BS//2-6), (BS//2-2, BS//2-6), (BS//2-6, BS//2-2)]
    pygame.draw.polygon(s, rock, pts)
    surfs[bid] = s

    bid = CHRYSANTHEMUM_TILE
    # if bid == CHRYSANTHEMUM_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 25)
    white = (235, 230, 220)
    BS = BLOCK_SIZE
    s.fill(white)
    cx2, cy2 = BS//2, BS//2
    # petal radiating lines
    for ai in range(12):
        ang = math.pi * ai / 6
        ex2 = cx2 + int(11 * math.cos(ang))
        ey2 = cy2 + int(11 * math.sin(ang))
        pygame.draw.line(s, c, (cx2, cy2), (ex2, ey2), 2)
    pygame.draw.circle(s, lt, (cx2, cy2), 4)
    pygame.draw.circle(s, _darken(c, 20), (cx2, cy2), 4, 1)
    pygame.draw.rect(s, _darken(white, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = PLUM_BLOSSOM_TILE
    # if bid == PLUM_BLOSSOM_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 22)
    white = (235, 230, 220)
    BS = BLOCK_SIZE
    s.fill(white)
    cx2, cy2 = BS//2, BS//2
    # 5 petals around center
    for ai in range(5):
        ang = math.pi * ai * 2 / 5 - math.pi / 2
        px2 = cx2 + int(7 * math.cos(ang))
        py2 = cy2 + int(7 * math.sin(ang))
        pygame.draw.circle(s, c, (px2, py2), 4)
    pygame.draw.circle(s, lt, (cx2, cy2), 3)
    pygame.draw.circle(s, (220, 180, 50), (cx2, cy2), 2)
    pygame.draw.rect(s, _darken(white, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = MOON_PAVEMENT
    # if bid == MOON_PAVEMENT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 15))
    # circular moon-gate paving inset
    pygame.draw.circle(s, c, (BS//2, BS//2), BS//2-2)
    pygame.draw.circle(s, lt, (BS//2, BS//2), BS//2-2, 2)
    pygame.draw.circle(s, _darken(c, 10), (BS//2, BS//2), BS//2-8, 1)
    # radial spoke lines
    for ai in range(8):
        ang = math.pi * ai / 4
        ex2 = BS//2 + int((BS//2-4) * math.cos(ang))
        ey2 = BS//2 + int((BS//2-4) * math.sin(ang))
        pygame.draw.line(s, dk, (BS//2, BS//2), (ex2, ey2), 1)
    surfs[bid] = s

    bid = BAMBOO_GROVE
    # if bid == BAMBOO_GROVE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 50))
    # multiple bamboo stalks
    for bx2, boff in [(4, 0), (10, 2), (16, -1), (22, 1), (28, -2)]:
        pygame.draw.rect(s, c, (bx2, boff, 4, BS-boff))
        pygame.draw.line(s, lt, (bx2+1, boff), (bx2+1, BS), 1)
        for ky in range(boff+6, BS, 8):
            pygame.draw.line(s, dk, (bx2, ky), (bx2+4, ky), 1)
    # leaves at top
    leaf = (70, 130, 48)
    for lx, ly in [(6, 4), (12, 2), (18, 5), (24, 3)]:
        pygame.draw.line(s, leaf, (lx, ly), (lx+6, ly-4), 1)
        pygame.draw.line(s, leaf, (lx, ly), (lx-4, ly-3), 1)
    surfs[bid] = s

    bid = OSMANTHUS_BUSH
    # if bid == OSMANTHUS_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    trunk = (90, 60, 35)
    s.fill(_darken(c, 45))
    pygame.draw.rect(s, trunk, (BS//2-1, BS-7, 3, 7))
    # rounded bush
    pygame.draw.circle(s, dk, (BS//2, BS//2-2), BS//2-4)
    pygame.draw.circle(s, c, (BS//2, BS//2-2), BS//2-6)
    # tiny golden flower dots
    flower = (230, 175, 50)
    for fx, fy in [(BS//2-4, BS//2-6), (BS//2+4, BS//2-4), (BS//2, BS//2-10),
                   (BS//2-6, BS//2-2), (BS//2+6, BS//2-8)]:
        pygame.draw.circle(s, flower, (fx, fy), 2)
    surfs[bid] = s

    bid = WATER_LILY_TILE
    # if bid == WATER_LILY_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 15))
    pygame.draw.ellipse(s, c, (1, 3, BS-2, BS-6))
    # lily pads (large)
    pad = (40, 110, 50)
    for px2, py2, r2 in [(7, BS//2, 6), (BS-9, BS//2+2, 5)]:
        pygame.draw.circle(s, pad, (px2, py2), r2)
        pygame.draw.line(s, _darken(pad, 20), (px2, py2-r2), (px2, py2+r2), 1)
    # white lily flower
    pygame.draw.circle(s, (245, 245, 235), (BS//2, BS//2-2), 4)
    for ai in range(6):
        ang = math.pi * ai / 3
        pygame.draw.line(s, (235, 235, 220), (BS//2, BS//2-2),
                         (BS//2+int(5*math.cos(ang)), BS//2-2+int(5*math.sin(ang))), 1)
    surfs[bid] = s

    bid = KOI_POND
    # if bid == KOI_POND
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 15))
    pygame.draw.ellipse(s, c, (1, 3, BS-2, BS-6))
    # koi fish
    koi_cols = [(210, 80, 40), (240, 200, 50), (230, 230, 230)]
    koi_pos = [(8, BS//2-2, 0), (BS//2, BS//2+2, math.pi/4), (BS-9, BS//2-3, -0.3)]
    for kx, ky, ka in koi_pos:
        col = koi_cols[kx % len(koi_cols)]
        pygame.draw.ellipse(s, col, (kx-4, ky-2, 8, 4))
        # tail
        tx = kx + int(5*math.cos(ka+math.pi))
        ty = ky + int(5*math.sin(ka+math.pi))
        pygame.draw.line(s, col, (kx, ky), (tx, ty), 2)
    surfs[bid] = s

    bid = LAKESIDE_ROCK
    # if bid == LAKESIDE_ROCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    water = (60, 130, 175)
    s.fill(water)
    # flat low rock
    pts = [(2, BS//2), (BS-2, BS//2+2), (BS-3, BS-3), (3, BS-4)]
    pygame.draw.polygon(s, c, pts)
    pygame.draw.polygon(s, lt, pts, 1)
    # water ripple above rock
    pygame.draw.arc(s, _lighter(water, 20), (4, BS//2-5, BS-8, 6), 0, math.pi, 1)
    surfs[bid] = s

    bid = CLOUD_COLLAR_TILE
    # if bid == CLOUD_COLLAR_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(c)
    cx2, cy2 = BS//2, BS//2
    # four ruyi cloud-collar lobes
    for ai in range(4):
        ang = math.pi * ai / 2
        ox2 = int(7 * math.cos(ang))
        oy2 = int(7 * math.sin(ang))
        pygame.draw.circle(s, lt, (cx2+ox2, cy2+oy2), 6, 1)
    pygame.draw.circle(s, dk, (cx2, cy2), 4)
    pygame.draw.circle(s, lt, (cx2, cy2), 2)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = IMPERIAL_PAVING
    # if bid == IMPERIAL_PAVING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    s.fill(c)
    # single large-format stone with tight joints
    pygame.draw.line(s, lt, (0, 0), (BS, 0), 2)
    pygame.draw.line(s, lt, (0, 0), (0, BS), 2)
    pygame.draw.line(s, dk, (0, BS-2), (BS, BS-2), 2)
    pygame.draw.line(s, dk, (BS-2, 0), (BS-2, BS), 2)
    # subtle grain texture
    for ty in range(5, BS-3, 6):
        pygame.draw.line(s, _darken(c, 5), (2, ty), (BS-3, ty), 1)
    surfs[bid] = s

    bid = PAVILION_COLUMN_CN
    # if bid == PAVILION_COLUMN_CN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    dk = _darken(c, 25)
    gold = (210, 165, 50)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 40))
    # red column shaft
    pygame.draw.rect(s, c, (BS//2-4, 0, 8, BS))
    pygame.draw.line(s, lt, (BS//2-3, 0), (BS//2-3, BS), 1)
    # gold dougong bracket at top
    pygame.draw.rect(s, gold, (BS//2-8, 3, 16, 4))
    pygame.draw.rect(s, _darken(gold, 20), (BS//2-6, 7, 12, 3))
    # cloud motif on shaft
    for cy2 in [BS//3, 2*BS//3]:
        pygame.draw.ellipse(s, lt, (BS//2-3, cy2-2, 6, 4), 1)
    surfs[bid] = s

    bid = EIGHT_DIAGRAM
    # if bid == EIGHT_DIAGRAM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(c)
    cx2, cy2 = BS//2, BS//2
    # outer octagon
    r2 = 12
    oct_pts = [(cx2+int(r2*math.cos(math.pi*i/4)), cy2+int(r2*math.sin(math.pi*i/4)))
               for i in range(8)]
    pygame.draw.polygon(s, lt, oct_pts, 1)
    # trigram lines (3 lines per sector — simplified)
    for ai in range(8):
        ang = math.pi * ai / 4
        for offset in [-2, 0, 2]:
            sx2 = cx2 + int((r2-3) * math.cos(ang)) + int(offset * math.cos(ang+math.pi/2))
            sy2 = cy2 + int((r2-3) * math.sin(ang)) + int(offset * math.sin(ang+math.pi/2))
            ex2 = cx2 + int(6 * math.cos(ang))
            ey2 = cy2 + int(6 * math.sin(ang))
            pygame.draw.line(s, dk, (sx2, sy2), (ex2, ey2), 1)
    # yin-yang center (simplified)
    pygame.draw.circle(s, lt, (cx2, cy2), 4)
    pygame.draw.circle(s, dk, (cx2, cy2-2), 1)
    pygame.draw.circle(s, lt, (cx2, cy2+2), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = TEA_HOUSE_STEP
    # if bid == TEA_HOUSE_STEP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 20))
    # three worn stone steps
    for i in range(3):
        step_y = BS//2 - 4 + i * 6
        step_x = 2 + i * 4
        pygame.draw.rect(s, _lighter(c, 8-i*3), (step_x, step_y, BS-step_x*2, 6))
        pygame.draw.line(s, lt, (step_x, step_y), (BS-step_x, step_y), 1)
        pygame.draw.line(s, dk, (step_x, step_y+5), (BS-step_x, step_y+5), 1)
    surfs[bid] = s

    bid = LANTERN_FESTIVAL
    # if bid == LANTERN_FESTIVAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 50))
    # cord
    pygame.draw.line(s, (80, 60, 35), (0, 6), (BS, 6), 1)
    # multiple red paper lanterns
    lantern_positions = [3, 10, 18, 25]
    for lx in lantern_positions:
        drop_y = 6 + (lx % 4)
        pygame.draw.line(s, (80, 60, 35), (lx+3, 6), (lx+3, drop_y), 1)
        pygame.draw.ellipse(s, c, (lx, drop_y, 7, 11))
        pygame.draw.ellipse(s, lt, (lx+1, drop_y+1, 5, 4))
        # tassel
        pygame.draw.line(s, (180, 140, 40), (lx+3, drop_y+11), (lx+3, drop_y+14), 1)
    surfs[bid] = s

    bid = TAPESTRY_BLOCK
    # if bid == TAPESTRY_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    bands = [(175,88,52),(230,200,160),(140,40,40),(215,175,90),(175,88,52),(80,45,28)]
    bh2 = BLOCK_SIZE // len(bands)
    for i, bc in enumerate(bands):
        pygame.draw.rect(s, bc, (0, i*bh2, BLOCK_SIZE, bh2))
        for wx in range(0, BLOCK_SIZE, 3):
            pygame.draw.line(s, _darken(bc, 18), (wx, i*bh2), (wx, i*bh2+bh2), 1)
    pygame.draw.rect(s, _darken(bands[0], 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = WOVEN_RUG
    # if bid == WOVEN_RUG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CELTIC_KNOTWORK
    # if bid == CELTIC_KNOTWORK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BYZANTINE_MOSAIC
    # if bid == BYZANTINE_MOSAIC
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dark = _darken(c, 30)
    tsz = 4
    for ty in range(0, BLOCK_SIZE, tsz):
        for tx in range(0, BLOCK_SIZE, tsz):
            d = ((tx - 16)**2 + (ty - 12)**2) ** 0.5
            tc = dark if d < 10 else _lighter(c, 8)
            pygame.draw.rect(s, tc, (tx+1, ty+1, tsz-1, tsz-1))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = TEXTILE_RUG_NATURAL
    # if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON, TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET, TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_RUG_GOLDEN
    # if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON, TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET, TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_RUG_CRIMSON
    # if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON, TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET, TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_RUG_ROSE
    # if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON, TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET, TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_RUG_COBALT
    # if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON, TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET, TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_RUG_VIOLET
    # if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON, TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET, TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_RUG_VERDANT
    # if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON, TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET, TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_RUG_AMBER
    # if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON, TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET, TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_RUG_IVORY
    # if bid in (TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON, TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET, TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_TAPESTRY_NATURAL
    # if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET, TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_TAPESTRY_GOLDEN
    # if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET, TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_TAPESTRY_CRIMSON
    # if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET, TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_TAPESTRY_ROSE
    # if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET, TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_TAPESTRY_COBALT
    # if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET, TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_TAPESTRY_VIOLET
    # if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET, TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_TAPESTRY_VERDANT
    # if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET, TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_TAPESTRY_AMBER
    # if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET, TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEXTILE_TAPESTRY_IVORY
    # if bid in (TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET, TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STACKED_STONE_VENEER
    # if bid == STACKED_STONE_VENEER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    mortar_c = _darken(c, 20)
    s.fill(mortar_c)
    dk = _darken(c, 15)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    rh = 6
    for row in range(BS // rh + 1):
        sy = row * rh
        ox = (row % 3) * 7
        for sx in range(-7, BS + 7, 15):
            pygame.draw.rect(s, c, (sx + ox, sy, 13, 4))
            pygame.draw.line(s, lt, (sx + ox, sy), (sx + ox + 13, sy), 1)
            pygame.draw.rect(s, dk, (sx + ox, sy, 13, 4), 1)
    pygame.draw.rect(s, mortar_c, s.get_rect(), 1)
    surfs[bid] = s

    bid = ALPINE_BALCONY_RAIL
    # if bid == ALPINE_BALCONY_RAIL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    wood = (160, 110, 65); dk = _darken(wood, 25)
    pygame.draw.rect(s, wood, (0, 0, BS, 5))
    pygame.draw.rect(s, dk,   (0, 0, BS, 5), 1)
    pygame.draw.rect(s, wood, (0, BS - 4, BS, 4))
    for x in range(3, BS - 3, 7):
        pygame.draw.rect(s, wood, (x, 5, 3, BS - 9))
        pygame.draw.rect(s, dk,   (x, 5, 3, BS - 9), 1)
    surfs[bid] = s

    bid = DARK_TIMBER_BEAM
    # if bid == DARK_TIMBER_BEAM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (55, 40, 30); lt = _lighter(c, 15); dk = _darken(c, 15)
    s.fill(c)
    for y in range(4, BS, 8):
        pygame.draw.line(s, lt, (0, y), (BS, y), 1)
    for x in range(0, BS, 12):
        pygame.draw.line(s, dk, (x, 0), (x, BS), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = ROUGH_STONE_WALL
    # if bid == ROUGH_STONE_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (130, 125, 120); lt = _lighter(c, 12); dk = _darken(c, 18)
    s.fill(c)
    import random as _rnd
    _r = _rnd.Random(42)
    for _ in range(14):
        rx, ry = _r.randint(1, BS-8), _r.randint(1, BS-8)
        rw, rh = _r.randint(5, 12), _r.randint(3, 8)
        col = lt if _r.random() > 0.5 else dk
        pygame.draw.rect(s, col, (rx, ry, rw, rh))
        pygame.draw.rect(s, dk, (rx, ry, rw, rh), 1)
    surfs[bid] = s

    bid = ALPINE_PLASTER
    # if bid == ALPINE_PLASTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (230, 220, 205); lt = _lighter(c, 8); dk = _darken(c, 12)
    s.fill(c)
    import random as _rnd
    _r = _rnd.Random(7)
    for _ in range(20):
        x, y = _r.randint(0, BS-2), _r.randint(0, BS-2)
        pygame.draw.line(s, lt if _r.random() > 0.5 else dk, (x, y), (x + _r.randint(1, 4), y + _r.randint(0, 2)), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = FLOWER_BOX
    # if bid == FLOWER_BOX
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    box = (110, 80, 50); bdk = _darken(box, 20)
    pygame.draw.rect(s, box, (1, BS//2, BS - 2, BS//2 - 1))
    pygame.draw.rect(s, bdk, (1, BS//2, BS - 2, BS//2 - 1), 1)
    pygame.draw.line(s, bdk, (1, BS//2 + 4), (BS - 2, BS//2 + 4), 1)
    soil = (80, 55, 35)
    pygame.draw.rect(s, soil, (3, BS//2 + 1, BS - 6, 5))
    for cx in [5, 11, 17, 23]:
        pygame.draw.circle(s, (210, 50, 50), (cx, BS//2 - 2), 3)
        pygame.draw.circle(s, (255, 80, 80), (cx, BS//2 - 2), 2)
        pygame.draw.line(s, (60, 120, 40), (cx, BS//2 + 1), (cx, BS//2 - 2), 1)
    surfs[bid] = s

    bid = FIREWOOD_STACK
    # if bid == FIREWOOD_STACK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    bg = (60, 42, 28)
    s.fill(bg)
    log = (120, 80, 48); end = (170, 120, 75); dk = _darken(log, 20)
    for row, y in enumerate([2, 10, 18, 24]):
        for x in range(0, BS - 4, 6):
            ox = 2 if row % 2 else 0
            pygame.draw.rect(s, log, (x + ox, y, 5, 7))
            pygame.draw.ellipse(s, end, (x + ox, y + 1, 5, 5))
            pygame.draw.ellipse(s, dk,  (x + ox, y + 1, 5, 5), 1)
            pygame.draw.circle(s, (90, 55, 30), (x + ox + 2, y + 3), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = SLATE_SHINGLE
    # if bid == SLATE_SHINGLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (65, 75, 90); lt = _lighter(c, 14); dk = _darken(c, 18)
    s.fill(c)
    for row, y in enumerate(range(0, BS, 7)):
        ox = 6 if row % 2 else 0
        for x in range(-ox, BS, 12):
            pygame.draw.rect(s, lt, (x + 1, y + 1, 10, 5))
            pygame.draw.rect(s, dk, (x + 1, y + 1, 10, 5), 1)
    surfs[bid] = s

    bid = CARVED_SHUTTER
    # if bid == CARVED_SHUTTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    c = (130, 95, 60); dk = _darken(c, 22); lt = _lighter(c, 15)
    pygame.draw.rect(s, c, (1, 0, BS - 2, BS))
    pygame.draw.rect(s, dk, (1, 0, BS - 2, BS), 1)
    pygame.draw.line(s, dk, (BS//2, 0), (BS//2, BS), 2)
    for y in range(3, BS - 2, 5):
        pygame.draw.line(s, dk, (2, y), (BS//2 - 2, y), 1)
        pygame.draw.line(s, dk, (BS//2 + 2, y), (BS - 2, y), 1)
    pygame.draw.rect(s, lt, (2, 1, 3, BS - 2), 1)
    surfs[bid] = s

    bid = BEAR_HIDE
    # if bid == BEAR_HIDE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (100, 75, 50); dk = _darken(c, 20); lt = _lighter(c, 18)
    s.fill(dk)
    import random as _rnd
    _r = _rnd.Random(13)
    for _ in range(60):
        x, y = _r.randint(1, BS-2), _r.randint(1, BS-2)
        lc = lt if _r.random() > 0.6 else c
        dx, dy = _r.randint(-2, 2), _r.randint(-3, 0)
        pygame.draw.line(s, lc, (x, y), (x + dx, y + dy), 1)
    pygame.draw.rect(s, (60, 42, 28), s.get_rect(), 2)
    surfs[bid] = s

    bid = ALPINE_HERB_RACK
    # if bid == ALPINE_HERB_RACK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    wood = (90, 65, 45); dk = _darken(wood, 20)
    pygame.draw.rect(s, wood, (0, 2, BS, 4))
    pygame.draw.rect(s, dk,   (0, 2, BS, 4), 1)
    pygame.draw.rect(s, wood, (0, BS - 6, BS, 4))
    pygame.draw.rect(s, dk,   (0, BS - 6, BS, 4), 1)
    for x in [3, BS//2 - 2, BS - 8]:
        pygame.draw.line(s, dk, (x + 2, 6), (x + 2, BS - 6), 1)
        herbs = [(60, 100, 40), (80, 130, 50), (100, 80, 30)]
        for i, hc in enumerate(herbs):
            pygame.draw.ellipse(s, hc, (x, 8 + i*7, 5, 4))
    surfs[bid] = s

    bid = HAY_BALE
    # if bid == HAY_BALE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (200, 175, 80); lt = _lighter(c, 15); dk = _darken(c, 20)
    s.fill(c)
    for y in range(2, BS, 4):
        pygame.draw.line(s, dk, (0, y), (BS, y), 1)
    for x in range(3, BS, 10):
        pygame.draw.line(s, lt, (x, 0), (x, BS), 1)
    pygame.draw.rect(s, (155, 120, 45), s.get_rect(), 2)
    surfs[bid] = s

    bid = PINE_PLANK_WALL
    # if bid == PINE_PLANK_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (210, 190, 150); dk = _darken(c, 18); lt = _lighter(c, 10)
    s.fill(c)
    for y in range(0, BS, 8):
        pygame.draw.line(s, dk, (0, y), (BS, y), 2)
        pygame.draw.line(s, lt, (0, y + 1), (BS, y + 1), 1)
    for x in range(8, BS, 16):
        pygame.draw.line(s, dk, (x, 0), (x, BS//2), 1)
    for x in range(0, BS, 16):
        pygame.draw.line(s, dk, (x, BS//2), (x, BS), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GRANITE_ASHLAR
    # if bid == GRANITE_ASHLAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (140, 130, 130); lt = _lighter(c, 12); dk = _darken(c, 15)
    s.fill(c)
    import random as _rnd
    _r = _rnd.Random(99)
    for _ in range(8):
        x, y = _r.randint(0, BS-4), _r.randint(0, BS-4)
        pygame.draw.circle(s, lt if _r.random() > 0.5 else dk, (x, y), _r.randint(1, 3))
    pygame.draw.line(s, dk, (0, BS//2), (BS, BS//2), 2)
    pygame.draw.line(s, dk, (BS//2, 0), (BS//2, BS//2), 2)
    pygame.draw.line(s, dk, (BS//4, BS//2), (BS//4, BS), 2)
    pygame.draw.line(s, dk, (3*BS//4, BS//2), (3*BS//4, BS), 2)
    pygame.draw.rect(s, lt, (1, 1, BS//2 - 2, BS//2 - 2), 1)
    surfs[bid] = s

    bid = CUCKOO_CLOCK
    # if bid == CUCKOO_CLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    wood = (110, 80, 55); dk = _darken(wood, 22); cream = (235, 225, 200)
    pygame.draw.rect(s, wood, (3, 4, BS - 6, BS - 5))
    pygame.draw.rect(s, dk,   (3, 4, BS - 6, BS - 5), 1)
    pts = [(BS//2, 0), (2, 6), (BS - 2, 6)]
    pygame.draw.polygon(s, dk, pts)
    pygame.draw.polygon(s, wood, [(BS//2, 1), (3, 6), (BS - 3, 6)])
    pygame.draw.circle(s, cream, (BS//2, BS//2 - 1), 8)
    pygame.draw.circle(s, dk,    (BS//2, BS//2 - 1), 8, 1)
    pygame.draw.line(s, dk, (BS//2, BS//2 - 1), (BS//2, BS//2 - 7), 2)
    pygame.draw.line(s, dk, (BS//2, BS//2 - 1), (BS//2 + 5, BS//2 - 3), 1)
    door = (75, 50, 30)
    pygame.draw.rect(s, door, (BS//2 - 3, BS//2 + 7, 6, 7))
    pygame.draw.circle(s, door, (BS//2, BS//2 + 7), 3)
    surfs[bid] = s

    bid = GERANIUM_BOX
    # if bid == GERANIUM_BOX
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    box = (100, 70, 45); bdk = _darken(box, 22)
    pygame.draw.rect(s, box, (1, BS//2 + 2, BS - 2, BS//2 - 3))
    pygame.draw.rect(s, bdk, (1, BS//2 + 2, BS - 2, BS//2 - 3), 1)
    pygame.draw.line(s, bdk, (1, BS//2 + 6), (BS - 2, BS//2 + 6), 1)
    soil = (70, 48, 28)
    pygame.draw.rect(s, soil, (3, BS//2 + 3, BS - 6, 4))
    for cx in [4, 9, 14, 20, 25]:
        stem = (50, 90, 35)
        pygame.draw.line(s, stem, (cx, BS//2 + 3), (cx + 1, BS//2 - 4), 1)
        for petal in range(5):
            import math as _m
            angle = petal * _m.pi * 2 / 5
            px = int(cx + 1 + 3 * _m.cos(angle))
            py = int(BS//2 - 5 + 3 * _m.sin(angle))
            pygame.draw.circle(s, (220, 50, 50), (px, py), 2)
        pygame.draw.circle(s, (255, 210, 50), (cx + 1, BS//2 - 5), 1)
    surfs[bid] = s

    bid = ARCH_STONE
    # if bid == ARCH_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (175, 165, 155); lt = _lighter(c, 12); dk = _darken(c, 18)
    s.fill(c)
    pygame.draw.arc(s, dk, (2, -BS//2, BS - 4, BS), 0, 3.14159, 3)
    pygame.draw.arc(s, lt, (4, -BS//2 + 2, BS - 8, BS - 2), 0, 3.14159, 2)
    pygame.draw.rect(s, dk, (0, 0, 5, BS))
    pygame.draw.rect(s, lt, (1, 0, 3, BS), 1)
    pygame.draw.rect(s, dk, (BS - 5, 0, 5, BS))
    pygame.draw.rect(s, lt, (BS - 4, 0, 3, BS), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = SWISS_PANEL
    # if bid == SWISS_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (225, 215, 195); dk = _darken(c, 20); red = (190, 40, 40)
    s.fill(c)
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    pygame.draw.line(s, dk, (2, 2), (2, BS - 3), 1)
    pygame.draw.line(s, dk, (BS - 3, 2), (BS - 3, BS - 3), 1)
    pygame.draw.line(s, red, (BS//2 - 1, 5), (BS//2 - 1, BS - 5), 2)
    pygame.draw.line(s, red, (5, BS//2 - 1), (BS - 5, BS//2 - 1), 2)
    for cx, cy in [(BS//2 - 5, 8), (BS//2 + 3, 8), (BS//2 - 5, BS - 12), (BS//2 + 3, BS - 12)]:
        pygame.draw.circle(s, red, (cx, cy), 2)
    surfs[bid] = s

    bid = COPPER_COWBELL
    # if bid == COPPER_COWBELL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    cop = (185, 120, 70); dk = _darken(cop, 25); lt = _lighter(cop, 20)
    strap = (80, 55, 30)
    pygame.draw.rect(s, strap, (BS//2 - 3, 1, 6, 5))
    pygame.draw.rect(s, _darken(strap, 20), (BS//2 - 3, 1, 6, 5), 1)
    bell_pts = [(BS//2 - 7, 5), (BS//2 + 7, 5), (BS//2 + 10, BS - 5), (BS//2 - 10, BS - 5)]
    pygame.draw.polygon(s, cop, bell_pts)
    pygame.draw.polygon(s, dk, bell_pts, 2)
    pygame.draw.line(s, lt, (BS//2 - 5, 8), (BS//2 - 7, BS - 8), 1)
    pygame.draw.line(s, lt, (BS//2 - 3, 6), (BS//2 - 4, BS - 7), 1)
    pygame.draw.ellipse(s, dk, (BS//2 - 6, BS - 9, 12, 6))
    pygame.draw.circle(s, dk, (BS//2, BS - 6), 2)
    surfs[bid] = s

    bid = WOODEN_GEAR
    # if bid == WOODEN_GEAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    import math as _m
    wood = (145, 110, 70); dk = _darken(wood, 25); lt = _lighter(wood, 15)
    cx, cy, r = BS//2, BS//2, BS//2 - 4
    pygame.draw.circle(s, wood, (cx, cy), r)
    pygame.draw.circle(s, dk,   (cx, cy), r, 2)
    for i in range(8):
        angle = i * _m.pi / 4
        tx = int(cx + r * _m.cos(angle))
        ty = int(cy + r * _m.sin(angle))
        pygame.draw.rect(s, wood, (tx - 2, ty - 2, 5, 5))
        pygame.draw.rect(s, dk,   (tx - 2, ty - 2, 5, 5), 1)
    pygame.draw.circle(s, lt, (cx, cy), 5)
    pygame.draw.circle(s, dk, (cx, cy), 5, 1)
    pygame.draw.circle(s, dk, (cx, cy), 2)
    surfs[bid] = s

    bid = STONE_BASIN
    # if bid == STONE_BASIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (150, 145, 140); lt = _lighter(c, 12); dk = _darken(c, 20)
    s.fill((40, 55, 70))
    pygame.draw.rect(s, c, (2, BS//3, BS - 4, BS - BS//3 - 2))
    pygame.draw.rect(s, dk, (2, BS//3, BS - 4, BS - BS//3 - 2), 1)
    pygame.draw.rect(s, lt, (3, BS//3 + 1, BS - 8, 3))
    water = (80, 130, 180, 180)
    pygame.draw.ellipse(s, (80, 150, 200), (5, BS//3 + 4, BS - 10, BS//3 - 2))
    pygame.draw.rect(s, c, (0, BS//3, 3, BS - BS//3 - 1))
    pygame.draw.rect(s, c, (BS - 3, BS//3, 3, BS - BS//3 - 1))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MILK_CHURN
    # if bid == MILK_CHURN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    sil = (190, 195, 200); dk = _darken(sil, 22); lt = _lighter(sil, 15)
    iron = (130, 135, 140)
    pygame.draw.ellipse(s, sil, (BS//2 - 7, 4, 14, 6))
    pygame.draw.ellipse(s, dk,  (BS//2 - 7, 4, 14, 6), 1)
    pygame.draw.polygon(s, sil, [(BS//2 - 9, 8), (BS//2 + 9, 8), (BS//2 + 11, BS - 4), (BS//2 - 11, BS - 4)])
    pygame.draw.polygon(s, dk,  [(BS//2 - 9, 8), (BS//2 + 9, 8), (BS//2 + 11, BS - 4), (BS//2 - 11, BS - 4)], 1)
    pygame.draw.line(s, lt, (BS//2 - 7, 9), (BS//2 - 9, BS - 5), 1)
    for y in [BS//3, 2*BS//3]:
        pygame.draw.ellipse(s, iron, (BS//2 - 12, y - 2, 24, 4))
        pygame.draw.ellipse(s, _darken(iron, 15), (BS//2 - 12, y - 2, 24, 4), 1)
    pygame.draw.ellipse(s, sil, (BS//2 - 10, BS - 6, 20, 5))
    pygame.draw.ellipse(s, dk,  (BS//2 - 10, BS - 6, 20, 5), 1)
    surfs[bid] = s

    bid = ALPINE_CHEST
    # if bid == ALPINE_CHEST
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (80, 55, 35); lt = _lighter(c, 18); dk = _darken(c, 22)
    iron = (100, 100, 110)
    s.fill(c)
    pygame.draw.rect(s, lt, (1, 1, BS - 2, BS//2 - 3))
    pygame.draw.rect(s, c,  (1, 1, BS - 2, BS//2 - 3), 1)
    pygame.draw.line(s, dk, (0, BS//2 - 2), (BS, BS//2 - 2), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    for x in [3, BS - 5]:
        pygame.draw.rect(s, iron, (x, 2, 4, BS//2 - 4))
        pygame.draw.rect(s, iron, (x, BS//2, 4, BS//2 - 2))
    pygame.draw.rect(s, iron, (BS//2 - 3, BS//2 - 4, 6, 6))
    pygame.draw.rect(s, dk,   (BS//2 - 3, BS//2 - 4, 6, 6), 1)
    pygame.draw.circle(s, lt, (BS//2, BS//2 - 1), 2)
    surfs[bid] = s

    bid = ALPINE_LANTERN
    # if bid == ALPINE_LANTERN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (55, 55, 60); dk = _darken(iron, 20)
    glow = (255, 210, 100)
    pygame.draw.line(s, iron, (BS//2, 0), (BS//2, 5), 2)
    pygame.draw.rect(s, iron, (BS//2 - 8, 5, 16, 3))
    pygame.draw.rect(s, glow, (BS//2 - 7, 8, 14, BS - 13))
    pygame.draw.rect(s, iron, (BS//2 - 8, 8, 16, BS - 12), 2)
    for x in [BS//2 - 8, BS//2 + 7]:
        pygame.draw.line(s, iron, (x, 8), (x, BS - 4), 1)
    pygame.draw.rect(s, iron, (BS//2 - 6, BS - 5, 12, 3))
    pygame.draw.ellipse(s, (255, 220, 130), (BS//2 - 5, 10, 10, 8))
    surfs[bid] = s

    bid = WROUGHT_IRON_RAIL
    # if bid == WROUGHT_IRON_RAIL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (70, 70, 75); lt = _lighter(iron, 18)
    pygame.draw.rect(s, iron, (0, 0, BS, 4))
    pygame.draw.rect(s, lt,   (0, 0, BS, 4), 1)
    pygame.draw.rect(s, iron, (0, BS - 4, BS, 4))
    for x in range(3, BS - 3, 8):
        pygame.draw.rect(s, iron, (x, 4, 3, BS - 8))
        pygame.draw.rect(s, lt,   (x, 4, 3, BS - 8), 1)
        pygame.draw.circle(s, lt, (x + 1, BS//2), 2)
    surfs[bid] = s

    bid = ALPINE_CHANDELIER
    # if bid == ALPINE_CHANDELIER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (65, 65, 70); dk = _darken(iron, 15)
    candle = (240, 230, 210); flame = (255, 180, 50)
    pygame.draw.line(s, iron, (BS//2, 0), (BS//2, 8), 2)
    pygame.draw.ellipse(s, iron, (4, 8, BS - 8, 6))
    pygame.draw.ellipse(s, dk,   (4, 8, BS - 8, 6), 1)
    for cx in [5, BS//2, BS - 6]:
        pygame.draw.line(s, iron, (cx, 11), (cx, BS - 12), 1)
        pygame.draw.rect(s, candle, (cx - 2, BS - 12, 4, 6))
        pygame.draw.ellipse(s, flame, (cx - 2, BS - 14, 4, 4))
        pygame.draw.ellipse(s, (255, 230, 100), (cx - 1, BS - 13, 2, 2))
    pygame.draw.ellipse(s, iron, (6, 9, BS - 12, 4))
    surfs[bid] = s

    bid = WOVEN_TEXTILE
    # if bid == WOVEN_TEXTILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c1 = (185, 50, 50); c2 = (220, 200, 160); c3 = (50, 80, 160)
    s.fill(c2)
    for y in range(0, BS, 4):
        col = c1 if (y // 4) % 3 == 0 else (c3 if (y // 4) % 3 == 1 else c2)
        pygame.draw.line(s, col, (0, y), (BS, y), 2)
    for x in range(0, BS, 4):
        col = c2 if (x // 4) % 2 == 0 else c1
        for y in range((x // 4) % 4, BS, 8):
            pygame.draw.line(s, col, (x, y), (x, y + 3), 2)
    pygame.draw.rect(s, _darken(c2, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = COWBELL_RACK
    # if bid == COWBELL_RACK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    wood = (110, 80, 50); dk = _darken(wood, 22)
    cop = (185, 120, 70); cop_dk = _darken(cop, 25)
    pygame.draw.rect(s, wood, (0, 2, BS, 5))
    pygame.draw.rect(s, dk,   (0, 2, BS, 5), 1)
    for x in [4, BS//2 - 3, BS - 10]:
        pygame.draw.line(s, dk, (x + 2, 7), (x + 2, 12), 1)
        bell_pts = [(x, 12), (x + 5, 12), (x + 7, BS - 5), (x - 2, BS - 5)]
        pygame.draw.polygon(s, cop, bell_pts)
        pygame.draw.polygon(s, cop_dk, bell_pts, 1)
        pygame.draw.circle(s, cop_dk, (x + 2, BS - 5), 2)
    surfs[bid] = s

    bid = ALPINE_STUCCO
    # if bid == ALPINE_STUCCO
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (220, 210, 195); lt = _lighter(c, 8); dk = _darken(c, 15)
    s.fill(c)
    import random as _rnd
    _r = _rnd.Random(55)
    for _ in range(30):
        x, y = _r.randint(0, BS-1), _r.randint(0, BS-1)
        pygame.draw.circle(s, lt if _r.random() > 0.5 else dk, (x, y), 1)
    pygame.draw.line(s, dk, (0, BS//2), (BS, BS//2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CARVED_LINTEL
    # if bid == CARVED_LINTEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (180, 170, 160); lt = _lighter(c, 14); dk = _darken(c, 18)
    s.fill(c)
    pygame.draw.rect(s, lt, (2, 2, BS - 4, 6))
    pygame.draw.rect(s, dk, (2, 2, BS - 4, 6), 1)
    for x in range(5, BS - 5, 8):
        pygame.draw.arc(s, dk, (x, 4, 6, 6), 0, 3.14159, 1)
    pygame.draw.rect(s, dk, (2, BS - 8, BS - 4, 6))
    pygame.draw.rect(s, lt, (2, BS - 8, BS - 4, 6), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CHALET_DOOR
    # if bid == CHALET_DOOR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (90, 65, 40); lt = _lighter(c, 18); dk = _darken(c, 22)
    iron = (80, 80, 88)
    s.fill(c)
    pygame.draw.line(s, dk, (BS//2, 0), (BS//2, BS), 2)
    for y in range(6, BS - 4, 8):
        pygame.draw.line(s, dk, (2, y), (BS - 2, y), 1)
        pygame.draw.line(s, lt, (2, y + 1), (BS - 2, y + 1), 1)
    pygame.draw.line(s, iron, (2, 4), (BS - 3, BS - 5), 2)
    pygame.draw.line(s, iron, (3, BS - 5), (BS - 2, 4), 2)
    pygame.draw.circle(s, iron, (BS - 5, BS//2), 3)
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = CERAMIC_TILE_STOVE
    # if bid == CERAMIC_TILE_STOVE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    body = (80, 130, 100); dk = _darken(body, 22); lt = _lighter(body, 18)
    cream = (240, 235, 220)
    s.fill(body)
    for ty in range(2, BS - 2, 7):
        for tx in range(2, BS - 2, 7):
            pygame.draw.rect(s, cream, (tx, ty, 5, 5))
            pygame.draw.rect(s, dk,    (tx, ty, 5, 5), 1)
    iron = (80, 82, 88)
    pygame.draw.rect(s, iron, (BS//2 - 4, BS - 10, 8, 8))
    pygame.draw.rect(s, _darken(iron, 20), (BS//2 - 4, BS - 10, 8, 8), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = CARVED_BARGEBOARD
    # if bid == CARVED_BARGEBOARD
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    c = (65, 45, 28); lt = _lighter(c, 18); dk = _darken(c, 18)
    pygame.draw.rect(s, c, (0, 0, BS, 6))
    pygame.draw.rect(s, dk, (0, 0, BS, 6), 1)
    pygame.draw.rect(s, c, (0, BS - 6, BS, 6))
    pygame.draw.rect(s, dk, (0, BS - 6, BS, 6), 1)
    for x in range(4, BS - 4, 8):
        pygame.draw.circle(s, lt, (x, 3), 2)
        pygame.draw.polygon(s, c, [(x - 3, 7), (x + 3, 7), (x, 12)])
        pygame.draw.polygon(s, dk, [(x - 3, 7), (x + 3, 7), (x, 12)], 1)
    surfs[bid] = s

    bid = DORMER_WINDOW
    # if bid == DORMER_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    frame = (90, 65, 40); dk = _darken(frame, 22)
    glass = (130, 165, 190); glass_lt = _lighter(glass, 20)
    s.fill(frame)
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    pts = [(BS//2, 1), (1, BS//2), (BS - 1, BS//2)]
    pygame.draw.polygon(s, dk, pts)
    pygame.draw.polygon(s, frame, [(BS//2, 3), (3, BS//2), (BS - 3, BS//2)])
    pygame.draw.rect(s, glass, (4, BS//2 + 1, BS - 8, BS//2 - 5))
    pygame.draw.rect(s, glass_lt, (5, BS//2 + 2, (BS - 8)//2 - 1, (BS//2 - 5)//2))
    pygame.draw.line(s, dk, (BS//2, BS//2 + 1), (BS//2, BS - 5), 2)
    pygame.draw.line(s, dk, (4, BS//2 + BS//8), (BS - 4, BS//2 + BS//8), 2)
    pygame.draw.rect(s, dk, (4, BS//2 + 1, BS - 8, BS//2 - 5), 1)
    surfs[bid] = s

    bid = WOODEN_SHINGLE
    # if bid == WOODEN_SHINGLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (165, 130, 80); lt = _lighter(c, 14); dk = _darken(c, 20)
    s.fill(c)
    for row, y in enumerate(range(0, BS, 8)):
        ox = 8 if row % 2 else 0
        for x in range(-ox, BS, 16):
            pygame.draw.rect(s, lt, (x + 1, y + 1, 13, 6))
            pygame.draw.rect(s, dk, (x + 1, y + 1, 13, 6), 1)
            pygame.draw.line(s, lt, (x + 3, y + 1), (x + 3, y + 6), 1)
    surfs[bid] = s

    bid = STONE_STEP
    # if bid == STONE_STEP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (155, 150, 145); lt = _lighter(c, 15); dk = _darken(c, 20)
    s.fill(c)
    for i, (y, h) in enumerate([(0, 8), (8, 8), (16, 8), (24, 8)]):
        indent = i * 4
        pygame.draw.rect(s, lt, (indent, y, BS - indent, h))
        pygame.draw.rect(s, dk, (indent, y, BS - indent, h), 1)
        pygame.draw.line(s, lt, (indent + 1, y + 1), (BS - 1, y + 1), 1)
    surfs[bid] = s

    bid = WATER_TROUGH
    # if bid == WATER_TROUGH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (140, 135, 130); lt = _lighter(c, 12); dk = _darken(c, 20)
    s.fill(c)
    pygame.draw.rect(s, dk, (1, BS//3, BS - 2, BS - BS//3 - 2))
    pygame.draw.rect(s, lt, (2, BS//3 + 1, BS - 4, BS - BS//3 - 4))
    water = (70, 130, 175)
    pygame.draw.rect(s, water, (3, BS//3 + 3, BS - 6, BS - BS//3 - 8))
    pygame.draw.line(s, _lighter(water, 20), (4, BS//3 + 5), (BS - 5, BS//3 + 5), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CARVED_BENCH
    # if bid == CARVED_BENCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    c = (110, 80, 50); dk = _darken(c, 22); lt = _lighter(c, 15)
    pygame.draw.rect(s, c, (1, BS//2 - 3, BS - 2, 6))
    pygame.draw.rect(s, lt, (1, BS//2 - 3, BS - 2, 3))
    pygame.draw.rect(s, dk, (1, BS//2 - 3, BS - 2, 6), 1)
    for x in [3, BS - 7]:
        pygame.draw.rect(s, c, (x, BS//2 + 3, 4, BS//2 - 5))
        pygame.draw.rect(s, dk, (x, BS//2 + 3, 4, BS//2 - 5), 1)
    for cx in [4, 10, 18, 24]:
        pygame.draw.circle(s, lt, (cx, BS//2 - 2), 1)
    surfs[bid] = s

    bid = CHEESE_WHEEL
    # if bid == CHEESE_WHEEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    c = (215, 185, 80); dk = _darken(c, 22); lt = _lighter(c, 15)
    rind = (180, 145, 50)
    pygame.draw.ellipse(s, rind, (2, BS//4, BS - 4, BS//2))
    pygame.draw.ellipse(s, c,    (3, BS//4 + 1, BS - 6, BS//2 - 2))
    pygame.draw.ellipse(s, dk,   (3, BS//4 + 1, BS - 6, BS//2 - 2), 1)
    pygame.draw.ellipse(s, lt,   (4, BS//4 + 2, (BS - 6)//2, (BS//2 - 2)//2))
    for hx, hy in [(8, BS//2), (18, BS//2 - 2), (13, BS//2 + 4)]:
        pygame.draw.circle(s, dk, (hx, hy), 2)
        pygame.draw.circle(s, (240, 215, 110), (hx, hy), 1)
    surfs[bid] = s

    bid = ANTLER_MOUNT
    # if bid == ANTLER_MOUNT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    c = (160, 125, 80); dk = _darken(c, 25)
    mount = (80, 55, 35)
    pygame.draw.ellipse(s, mount, (BS//2 - 5, BS - 10, 10, 8))
    pygame.draw.ellipse(s, _darken(mount, 20), (BS//2 - 5, BS - 10, 10, 8), 1)
    pygame.draw.line(s, c, (BS//2 - 1, BS - 6), (4, BS//4), 3)
    pygame.draw.line(s, c, (BS//2 + 1, BS - 6), (BS - 4, BS//4), 3)
    pygame.draw.line(s, dk, (BS//2 - 1, BS - 6), (4, BS//4), 1)
    pygame.draw.line(s, c, (5, BS//4 + 2), (3, 4), 2)
    pygame.draw.line(s, c, (6, BS//4 + 5), (12, 3), 2)
    pygame.draw.line(s, c, (BS - 5, BS//4 + 2), (BS - 3, 4), 2)
    pygame.draw.line(s, c, (BS - 6, BS//4 + 5), (BS - 12, 3), 2)
    surfs[bid] = s

    bid = EDELWEISS_WREATH
    # if bid == EDELWEISS_WREATH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    import math as _m
    green = (60, 95, 45); lt_green = _lighter(green, 20)
    cx, cy, r = BS//2, BS//2, BS//2 - 3
    pygame.draw.circle(s, green, (cx, cy), r, 5)
    white = (245, 245, 240); yellow = (230, 200, 60)
    for i in range(6):
        angle = i * _m.pi * 2 / 6 - _m.pi / 2
        fx = int(cx + r * _m.cos(angle))
        fy = int(cy + r * _m.sin(angle))
        for j in range(5):
            pa = angle + j * _m.pi * 2 / 5
            px = int(fx + 3 * _m.cos(pa))
            py = int(fy + 3 * _m.sin(pa))
            pygame.draw.circle(s, white, (px, py), 2)
        pygame.draw.circle(s, yellow, (fx, fy), 2)
    surfs[bid] = s

    bid = BOOT_RACK
    # if bid == BOOT_RACK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    wood = (75, 55, 38); dk = _darken(wood, 22)
    boot = (45, 32, 22); boot_lt = _lighter(boot, 15)
    pygame.draw.rect(s, wood, (0, 2, BS, 4))
    pygame.draw.rect(s, dk,   (0, 2, BS, 4), 1)
    pygame.draw.rect(s, wood, (0, BS - 6, BS, 4))
    pygame.draw.rect(s, dk,   (0, BS - 6, BS, 4), 1)
    for bx in [3, BS//2 + 1]:
        pygame.draw.rect(s, boot, (bx, 6, 6, BS - 12))
        pygame.draw.rect(s, boot_lt, (bx + 1, 7, 2, 4))
        pygame.draw.ellipse(s, boot, (bx - 2, BS - 12, 10, 6))
        pygame.draw.ellipse(s, boot_lt, (bx - 1, BS - 11, 4, 3))
    surfs[bid] = s

    bid = TALLOW_CANDLE
    # if bid == TALLOW_CANDLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    wax = (235, 220, 185); dk = _darken(wax, 20)
    flame = (255, 175, 40); inner = (255, 230, 100)
    w = 6
    pygame.draw.rect(s, wax, (BS//2 - w//2, BS//3, w, 2*BS//3 - 2))
    pygame.draw.rect(s, dk,  (BS//2 - w//2, BS//3, w, 2*BS//3 - 2), 1)
    pygame.draw.line(s, dk, (BS//2 - w//2 + 1, BS//3 + 3), (BS//2 - w//2 + 1, 2*BS//3), 1)
    wick = (80, 60, 40)
    pygame.draw.line(s, wick, (BS//2, BS//3), (BS//2, BS//3 - 3), 1)
    pygame.draw.ellipse(s, flame, (BS//2 - 3, BS//3 - 9, 6, 8))
    pygame.draw.ellipse(s, inner, (BS//2 - 1, BS//3 - 7, 3, 4))
    surfs[bid] = s

    bid = ALPINE_HEARTH
    # if bid == ALPINE_HEARTH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (95, 88, 82); lt = _lighter(c, 14); dk = _darken(c, 20)
    soot = (40, 35, 30)
    s.fill(c)
    pygame.draw.rect(s, dk, (2, 2, BS - 4, BS - 8), 2)
    pygame.draw.rect(s, soot, (5, 5, BS - 10, BS - 14))
    pygame.draw.arc(s, lt, (3, 3, BS - 6, BS//2), 0, 3.14159, 3)
    ember1 = (220, 80, 20); ember2 = (240, 160, 30)
    for ex, ey in [(7, BS - 12), (13, BS - 10), (18, BS - 13), (22, BS - 11)]:
        pygame.draw.ellipse(s, ember1, (ex, ey, 4, 3))
    for ex, ey in [(9, BS - 11), (16, BS - 9)]:
        pygame.draw.ellipse(s, ember2, (ex, ey, 3, 2))
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = PINE_CONE_GARLAND
    # if bid == PINE_CONE_GARLAND
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    cord = (80, 60, 38); cone = (105, 72, 42); cone_lt = _lighter(cone, 18)
    import math as _m
    for x in range(0, BS + 1, 4):
        y = int(BS//4 + 6 * _m.sin(x * _m.pi * 2 / BS))
        pygame.draw.circle(s, cord, (x, y), 1)
    for cx in [4, 11, 18, 25]:
        cy = int(BS//4 + 6 * _m.sin(cx * _m.pi * 2 / BS)) + 2
        for scale, col in [(5, cone), (4, cone_lt), (3, cone)]:
            pygame.draw.ellipse(s, col, (cx - scale//2, cy, scale, scale + 2))
            cy += scale + 1
    surfs[bid] = s

    bid = IRON_HOOK_RACK
    # if bid == IRON_HOOK_RACK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    wood = (80, 58, 38); dk = _darken(wood, 22)
    iron = (65, 65, 70); iron_lt = _lighter(iron, 18)
    pygame.draw.rect(s, wood, (0, 2, BS, 7))
    pygame.draw.rect(s, dk,   (0, 2, BS, 7), 1)
    for hx in [5, BS//2 - 1, BS - 8]:
        pygame.draw.line(s, iron, (hx + 1, 9), (hx + 1, 14), 2)
        pygame.draw.arc(s, iron, (hx - 2, 10, 7, 8), 3.14159, 2 * 3.14159, 2)
        pygame.draw.circle(s, iron_lt, (hx + 1, 9), 1)
    surfs[bid] = s

    bid = ALPINE_GATE
    # if bid == ALPINE_GATE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (85, 60, 38); lt = _lighter(c, 16); dk = _darken(c, 22)
    iron = (70, 70, 78)
    s.fill(c)
    pygame.draw.line(s, dk, (BS//2, 0), (BS//2, BS), 2)
    for y in range(4, BS, 6):
        pygame.draw.line(s, dk, (1, y), (BS - 1, y), 1)
        pygame.draw.line(s, lt, (1, y + 1), (BS - 1, y + 1), 1)
    pygame.draw.line(s, iron, (1, 2), (BS//2 - 2, BS - 3), 2)
    pygame.draw.line(s, iron, (BS//2 + 2, 2), (BS - 2, BS - 3), 2)
    for x in [3, BS - 6]:
        pygame.draw.rect(s, iron, (x, BS//4, 3, BS//2))
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = BUTTER_CHURN
    # if bid == BUTTER_CHURN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    c = (130, 105, 70); lt = _lighter(c, 18); dk = _darken(c, 22)
    hoop = (90, 72, 48)
    pygame.draw.ellipse(s, c, (BS//2 - 7, 3, 14, 5))
    pygame.draw.ellipse(s, dk, (BS//2 - 7, 3, 14, 5), 1)
    pygame.draw.polygon(s, lt, [(BS//2 - 8, 6), (BS//2 + 8, 6), (BS//2 + 6, BS - 5), (BS//2 - 6, BS - 5)])
    pygame.draw.polygon(s, dk, [(BS//2 - 8, 6), (BS//2 + 8, 6), (BS//2 + 6, BS - 5), (BS//2 - 6, BS - 5)], 1)
    for y in [BS//3 + 2, 2*BS//3]:
        pygame.draw.ellipse(s, hoop, (BS//2 - 9, y - 2, 18, 4))
        pygame.draw.ellipse(s, _darken(hoop, 15), (BS//2 - 9, y - 2, 18, 4), 1)
    handle_c = (100, 78, 50)
    pygame.draw.line(s, handle_c, (BS//2, 3), (BS//2, 0), 2)
    pygame.draw.ellipse(s, c, (BS//2 - 5, BS - 6, 10, 4))
    pygame.draw.ellipse(s, dk, (BS//2 - 5, BS - 6, 10, 4), 1)
    surfs[bid] = s

    bid = CARVED_WAINSCOT
    # if bid == CARVED_WAINSCOT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (80, 58, 38); lt = _lighter(c, 16); dk = _darken(c, 22)
    s.fill(c)
    pygame.draw.rect(s, lt, (2, 2, BS - 4, BS//3 - 2))
    pygame.draw.rect(s, dk, (2, 2, BS - 4, BS//3 - 2), 1)
    pygame.draw.rect(s, lt, (2, BS//3 + 1, BS - 4, BS - BS//3 - 4))
    pygame.draw.rect(s, dk, (2, BS//3 + 1, BS - 4, BS - BS//3 - 4), 1)
    pygame.draw.rect(s, dk, (0, BS//3 - 1, BS, 3))
    for x in range(5, BS - 5, 10):
        pygame.draw.line(s, lt, (x, 4), (x, BS//3 - 3), 1)
        pygame.draw.line(s, lt, (x, BS//3 + 3), (x, BS - 6), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CHIMNEY_CAP
    # if bid == CHIMNEY_CAP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (100, 95, 90); lt = _lighter(c, 14); dk = _darken(c, 20)
    iron = (60, 60, 65)
    s.fill(c)
    pygame.draw.rect(s, lt, (1, 1, BS - 2, 6))
    pygame.draw.rect(s, dk, (1, 1, BS - 2, 6), 1)
    pygame.draw.rect(s, dk, (4, 7, BS - 8, BS - 14))
    for sx in [5, BS//2 - 2, BS - 9]:
        pygame.draw.rect(s, iron, (sx, 8, 4, BS - 15))
        pygame.draw.rect(s, lt, (sx + 1, 9, 2, BS - 17), 1)
    pygame.draw.rect(s, lt, (1, BS - 7, BS - 2, 6))
    pygame.draw.rect(s, dk, (1, BS - 7, BS - 2, 6), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = FEATHER_DUVET
    # if bid == FEATHER_DUVET
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    c = (235, 230, 240); lt = _lighter(c, 8); dk = _darken(c, 12)
    stripe = (210, 195, 225)
    s.fill(c)
    for x in range(0, BS, 8):
        pygame.draw.rect(s, stripe, (x, 0, 4, BS))
    import random as _rnd
    _r = _rnd.Random(77)
    for _ in range(12):
        px, py = _r.randint(2, BS-4), _r.randint(2, BS-4)
        pygame.draw.ellipse(s, lt, (px, py, _r.randint(4, 9), _r.randint(3, 6)))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GREEK_AMPHORA
    # if bid == GREEK_AMPHORA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (175, 95, 55); dk = _darken(c, 25); lt = _lighter(c, 18); blk = (30, 20, 15)
    pygame.draw.ellipse(s, c,  (BS//2-4, 1, 8, 5))
    pygame.draw.ellipse(s, dk, (BS//2-4, 1, 8, 5), 1)
    pygame.draw.polygon(s, c,  [(BS//2-7,6),(BS//2+7,6),(BS//2+9,BS-5),(BS//2-9,BS-5)])
    pygame.draw.polygon(s, dk, [(BS//2-7,6),(BS//2+7,6),(BS//2+9,BS-5),(BS//2-9,BS-5)], 1)
    pygame.draw.ellipse(s, c,  (BS//2-8, BS-7, 16, 5))
    pygame.draw.ellipse(s, dk, (BS//2-8, BS-7, 16, 5), 1)
    for hx in [BS//2-9, BS//2+5]:
        pygame.draw.arc(s, c, (hx, BS//3, 8, 8), 0, 3.14159, 3)
    pygame.draw.line(s, blk, (BS//2-5, BS//3), (BS//2-3, 2*BS//3), 1)
    pygame.draw.line(s, lt,  (BS//2-6, 7), (BS//2-7, BS-6), 1)
    surfs[bid] = s

    bid = KRATER
    # if bid == KRATER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (170, 88, 48); dk = _darken(c, 25); lt = _lighter(c, 18); blk = (28, 18, 12)
    pygame.draw.polygon(s, c,  [(3,BS//2),(BS-3,BS//2),(BS-5,BS-4),(5,BS-4)])
    pygame.draw.polygon(s, dk, [(3,BS//2),(BS-3,BS//2),(BS-5,BS-4),(5,BS-4)], 1)
    pygame.draw.ellipse(s, c,  (2, BS//2-6, BS-4, 12))
    pygame.draw.ellipse(s, dk, (2, BS//2-6, BS-4, 12), 1)
    pygame.draw.ellipse(s, lt, (4, BS//2-4, (BS-4)//2, 5))
    pygame.draw.ellipse(s, c,  (BS//2-3, BS-6, 6, 4))
    for hx in [1, BS-7]:
        pygame.draw.arc(s, c, (hx, BS//2-5, 8, 10), 0, 3.14159, 3)
    for lx in [BS//2-5, BS//2+2]:
        pygame.draw.line(s, blk, (lx, BS//2), (lx+1, BS-5), 1)
    surfs[bid] = s

    bid = HYDRIA
    # if bid == HYDRIA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (165, 85, 50); dk = _darken(c, 25); lt = _lighter(c, 18)
    pygame.draw.ellipse(s, c,  (BS//2-4, 1, 8, 5))
    pygame.draw.ellipse(s, dk, (BS//2-4, 1, 8, 5), 1)
    pygame.draw.ellipse(s, c,  (BS//2-8, BS//4, 16, BS//2))
    pygame.draw.ellipse(s, dk, (BS//2-8, BS//4, 16, BS//2), 1)
    pygame.draw.polygon(s, c,  [(BS//2-6,BS//4+BS//2-2),(BS//2+6,BS//4+BS//2-2),(BS//2+4,BS-4),(BS//2-4,BS-4)])
    pygame.draw.polygon(s, dk, [(BS//2-6,BS//4+BS//2-2),(BS//2+6,BS//4+BS//2-2),(BS//2+4,BS-4),(BS//2-4,BS-4)], 1)
    pygame.draw.ellipse(s, c,  (BS//2-5, BS-6, 10, 4))
    for hx in [BS//2-9, BS//2+4]:
        pygame.draw.arc(s, c, (hx, BS//4+4, 8, 8), 0, 3.14159, 2)
    pygame.draw.line(s, lt, (BS//2-6, BS//4+1), (BS//2-5, BS//4+BS//2-4), 1)
    surfs[bid] = s

    bid = LEKYTHOS
    # if bid == LEKYTHOS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (215, 175, 120); dk = _darken(c, 22); lt = _lighter(c, 15); blk = (40, 25, 15)
    pygame.draw.ellipse(s, c,  (BS//2-3, 1, 6, 4))
    pygame.draw.ellipse(s, dk, (BS//2-3, 1, 6, 4), 1)
    pygame.draw.rect(s, c, (BS//2-2, 5, 4, 6))
    pygame.draw.ellipse(s, c,  (BS//2-6, 10, 12, 8))
    pygame.draw.ellipse(s, dk, (BS//2-6, 10, 12, 8), 1)
    pygame.draw.polygon(s, c,  [(BS//2-5,17),(BS//2+5,17),(BS//2+4,BS-4),(BS//2-4,BS-4)])
    pygame.draw.polygon(s, dk, [(BS//2-5,17),(BS//2+5,17),(BS//2+4,BS-4),(BS//2-4,BS-4)], 1)
    pygame.draw.ellipse(s, c,  (BS//2-5, BS-6, 10, 4))
    pygame.draw.line(s, blk, (BS//2-2, 18), (BS//2-2, BS-5), 1)
    pygame.draw.line(s, lt,  (BS//2-4, 18), (BS//2-4, BS-5), 1)
    surfs[bid] = s

    bid = STORAGE_PITHOS
    # if bid == STORAGE_PITHOS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (160, 90, 52); dk = _darken(c, 25); lt = _lighter(c, 18)
    pygame.draw.ellipse(s, c,  (BS//2-6, 2, 12, 6))
    pygame.draw.ellipse(s, dk, (BS//2-6, 2, 12, 6), 1)
    pygame.draw.ellipse(s, c,  (1, BS//5, BS-2, 3*BS//5))
    pygame.draw.ellipse(s, dk, (1, BS//5, BS-2, 3*BS//5), 1)
    pygame.draw.polygon(s, c,  [(BS//2-5,BS//5+3*BS//5-3),(BS//2+5,BS//5+3*BS//5-3),(BS//2+3,BS-2),(BS//2-3,BS-2)])
    pygame.draw.polygon(s, dk, [(BS//2-5,BS//5+3*BS//5-3),(BS//2+5,BS//5+3*BS//5-3),(BS//2+3,BS-2),(BS//2-3,BS-2)], 1)
    pygame.draw.line(s, lt, (3, BS//5+3), (2, BS//5+3*BS//5-5), 1)
    for y in [BS//5+6, BS//5+14, BS//5+22]:
        pygame.draw.line(s, dk, (2, y), (BS-2, y), 1)
    surfs[bid] = s

    bid = KLINE
    # if bid == KLINE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (140, 105, 68); dk = _darken(c, 22); lt = _lighter(c, 18)
    fabric = (200, 175, 140); pillow = (230, 210, 175)
    pygame.draw.rect(s, c,      (0, BS//2, BS, BS//3)); pygame.draw.rect(s, dk, (0, BS//2, BS, BS//3), 1)
    pygame.draw.rect(s, fabric, (1, BS//2-5, BS-2, BS//3+3)); pygame.draw.rect(s, dk, (1, BS//2-5, BS-2, BS//3+3), 1)
    pygame.draw.line(s, lt, (2, BS//2-4), (BS-2, BS//2-4), 1)
    pygame.draw.rect(s, pillow, (1, BS//2-11, BS//3, 8)); pygame.draw.rect(s, dk, (1, BS//2-11, BS//3, 8), 1)
    for lx in [3, BS-7]:
        pygame.draw.rect(s, c,  (lx, BS//2+BS//3, 4, BS//3-2))
        pygame.draw.rect(s, dk, (lx, BS//2+BS//3, 4, BS//3-2), 1)
    surfs[bid] = s

    bid = TRIPOD_BRAZIER
    # if bid == TRIPOD_BRAZIER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (100, 78, 50); dk = _darken(c, 25)
    ember = (220, 90, 20); flame = (255, 170, 40)
    pygame.draw.line(s, c, (BS//2, BS//3), (4, BS-4), 2)
    pygame.draw.line(s, c, (BS//2, BS//3), (BS//2, BS-4), 2)
    pygame.draw.line(s, c, (BS//2, BS//3), (BS-4, BS-4), 2)
    pygame.draw.line(s, dk, (4, BS-3), (BS-4, BS-3), 1)
    pygame.draw.ellipse(s, c,     (BS//2-8, BS//3-5, 16, 10))
    pygame.draw.ellipse(s, dk,    (BS//2-8, BS//3-5, 16, 10), 1)
    pygame.draw.ellipse(s, ember, (BS//2-6, BS//3-3, 12, 6))
    pygame.draw.ellipse(s, flame, (BS//2-3, BS//3-6, 6, 6))
    pygame.draw.ellipse(s, (255, 220, 100), (BS//2-1, BS//3-5, 3, 3))
    surfs[bid] = s

    bid = OLIVE_PRESS
    # if bid == OLIVE_PRESS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); BS = BLOCK_SIZE
    stone = (150, 140, 130); sdk = _darken(stone, 20); slt = _lighter(stone, 12)
    wood = (120, 90, 58); wdk = _darken(wood, 20)
    s.fill(stone)
    pygame.draw.ellipse(s, sdk, (2, BS//2, BS-4, BS//2-4))
    pygame.draw.ellipse(s, slt, (3, BS//2+1, BS-6, BS//2-6))
    pygame.draw.circle(s, sdk, (BS//2, BS//2+4), BS//4)
    pygame.draw.circle(s, stone, (BS//2, BS//2+4), BS//4-2)
    pygame.draw.line(s, wood, (BS//2, 2), (BS//2, BS//2+4), 3)
    pygame.draw.line(s, wdk,  (BS//2+1, 2), (BS//2+1, BS//2+4), 1)
    pygame.draw.rect(s, sdk, s.get_rect(), 1)
    surfs[bid] = s

    bid = LOOM_FRAME
    # if bid == LOOM_FRAME
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (130, 100, 65); dk = _darken(c, 22)
    thread = (230, 210, 185); thread2 = (180, 140, 100)
    pygame.draw.rect(s, c, (2, 0, 4, BS)); pygame.draw.rect(s, dk, (2, 0, 4, BS), 1)
    pygame.draw.rect(s, c, (BS-6, 0, 4, BS)); pygame.draw.rect(s, dk, (BS-6, 0, 4, BS), 1)
    pygame.draw.rect(s, c, (2, 2, BS-4, 4)); pygame.draw.rect(s, dk, (2, 2, BS-4, 4), 1)
    for y in range(8, BS-4, 3):
        pygame.draw.line(s, thread if (y//3)%2==0 else thread2, (6, y), (BS-6, y), 1)
    pygame.draw.rect(s, c, (6, BS//2-1, BS-12, 3)); pygame.draw.rect(s, dk, (6, BS//2-1, BS-12, 3), 1)
    surfs[bid] = s

    bid = MEANDER_BORDER
    # if bid == MEANDER_BORDER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); BS = BLOCK_SIZE
    c = (225, 218, 205); dk = _darken(c, 25); key = (80, 70, 60)
    s.fill(c)
    for ox in range(0, BS, 8):
        pygame.draw.line(s, key, (ox,   BS//2-4), (ox+4, BS//2-4), 2)
        pygame.draw.line(s, key, (ox+4, BS//2-4), (ox+4, BS//2+2), 2)
        pygame.draw.line(s, key, (ox+4, BS//2+2), (ox+8, BS//2+2), 2)
        pygame.draw.line(s, key, (ox+8, BS//2+2), (ox+8, BS//2-6), 2)
    pygame.draw.rect(s, dk, (0, BS//2-6, BS, 1)); pygame.draw.rect(s, dk, (0, BS//2+4, BS, 1))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = SYMPOSIUM_TABLE
    # if bid == SYMPOSIUM_TABLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (140, 108, 70); dk = _darken(c, 22); lt = _lighter(c, 15)
    pygame.draw.rect(s, c,  (1, BS//2-2, BS-2, 5)); pygame.draw.rect(s, lt, (1, BS//2-2, BS-2, 2)); pygame.draw.rect(s, dk, (1, BS//2-2, BS-2, 5), 1)
    cup = (170, 88, 48); cdk = _darken(cup, 22)
    for cx2, cy2 in [(4, BS//2-8), (BS-14, BS//2-7)]:
        pygame.draw.ellipse(s, cup, (cx2, cy2, 8, 6)); pygame.draw.ellipse(s, cdk, (cx2, cy2, 8, 6), 1)
    for lx in [3, BS-7]:
        pygame.draw.rect(s, c,  (lx, BS//2+3, 3, BS//2-5))
        pygame.draw.rect(s, dk, (lx, BS//2+3, 3, BS//2-5), 1)
    surfs[bid] = s

    bid = VOTIVE_TABLET
    # if bid == VOTIVE_TABLET
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (195, 185, 172); dk = _darken(c, 20); lt = _lighter(c, 12)
    pygame.draw.rect(s, c,  (2, 3, BS-4, BS-6)); pygame.draw.rect(s, dk, (2, 3, BS-4, BS-6), 1)
    pygame.draw.rect(s, lt, (3, 4, BS-8, 4))
    for y in range(11, BS-8, 5):
        pygame.draw.line(s, dk, (5, y), (BS-5, y), 1)
    pygame.draw.circle(s, dk, (BS//2, 6), 2)
    surfs[bid] = s

    bid = BRONZE_CUIRASS_STAND
    # if bid == BRONZE_CUIRASS_STAND
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    brnz = (120, 95, 55); dk = _darken(brnz, 25); lt = _lighter(brnz, 20); stand = (90, 68, 40)
    pygame.draw.rect(s, stand, (BS//2-2, BS//2, 4, BS//2-3)); pygame.draw.rect(s, _darken(stand,20), (BS//2-2, BS//2, 4, BS//2-3), 1)
    pygame.draw.ellipse(s, stand, (BS//2-8, BS-8, 16, 5))
    pygame.draw.ellipse(s, brnz, (BS//2-9, 2, 18, BS//2+2)); pygame.draw.ellipse(s, dk, (BS//2-9, 2, 18, BS//2+2), 2)
    pygame.draw.ellipse(s, lt,   (BS//2-6, 4, 8, BS//4))
    pygame.draw.line(s, dk, (BS//2, 5), (BS//2, BS//2), 2)
    for sx in [BS//2-8, BS//2+5]:
        pygame.draw.arc(s, dk, (sx, BS//4, 6, 8), 0, 3.14159, 2)
    surfs[bid] = s

    bid = CHARIOT_WHEEL
    # if bid == CHARIOT_WHEEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    import math as _m
    wood = (115, 85, 52); dk = _darken(wood, 25); lt = _lighter(wood, 18); iron = (80, 78, 82)
    cx, cy, r = BS//2, BS//2, BS//2-2
    pygame.draw.circle(s, iron, (cx, cy), r, 3); pygame.draw.circle(s, lt, (cx, cy), r-2, 1)
    for i in range(8):
        angle = i * _m.pi / 4
        ex, ey = int(cx+r*_m.cos(angle)), int(cy+r*_m.sin(angle))
        pygame.draw.line(s, wood, (cx, cy), (ex, ey), 2)
        pygame.draw.line(s, dk,   (cx, cy), (ex, ey), 1)
    pygame.draw.circle(s, iron, (cx, cy), 4); pygame.draw.circle(s, lt, (cx, cy), 2)
    surfs[bid] = s

    bid = TERRACOTTA_ROOF_TILE
    # if bid == TERRACOTTA_ROOF_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); BS = BLOCK_SIZE
    c = (185, 100, 62); dk = _darken(c, 22); lt = _lighter(c, 15)
    s.fill(c)
    for row, y in enumerate(range(0, BS, 8)):
        ox = 4 if row % 2 else 0
        for x in range(-ox, BS, 8):
            pygame.draw.ellipse(s, lt, (x+1, y+1, 7, 6)); pygame.draw.ellipse(s, dk, (x+1, y+1, 7, 6), 1)
            pygame.draw.ellipse(s, c,  (x+2, y+2, 3, 4))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = ATTIC_VASE
    # if bid == ATTIC_VASE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (180, 85, 42); dk = _darken(c, 25); lt = _lighter(c, 18); blk = (22, 14, 8)
    pygame.draw.ellipse(s, c,  (BS//2-5, 2, 10, 5)); pygame.draw.ellipse(s, dk, (BS//2-5, 2, 10, 5), 1)
    pygame.draw.ellipse(s, c,  (BS//2-9, BS//4, 18, BS//2)); pygame.draw.ellipse(s, dk, (BS//2-9, BS//4, 18, BS//2), 1)
    pygame.draw.polygon(s, c,  [(BS//2-6,BS//4+BS//2-2),(BS//2+6,BS//4+BS//2-2),(BS//2+4,BS-3),(BS//2-4,BS-3)])
    pygame.draw.polygon(s, dk, [(BS//2-6,BS//4+BS//2-2),(BS//2+6,BS//4+BS//2-2),(BS//2+4,BS-3),(BS//2-4,BS-3)], 1)
    pygame.draw.ellipse(s, c,   (BS//2-5, BS-5, 10, 3))
    pygame.draw.ellipse(s, blk, (BS//2-6, BS//4+2, 12, BS//2-4))
    pygame.draw.ellipse(s, c,   (BS//2-4, BS//4+4, 8, BS//2-8))
    for hx in [BS//2-10, BS//2+4]:
        pygame.draw.arc(s, c, (hx, BS//4+4, 8, 8), 0, 3.14159, 3)
    surfs[bid] = s

    bid = GREEK_STONE_BENCH
    # if bid == GREEK_STONE_BENCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (230, 226, 218); dk = _darken(c, 20); lt = _lighter(c, 8)
    pygame.draw.rect(s, c,  (1, BS//2-4, BS-2, 7)); pygame.draw.rect(s, lt, (1, BS//2-4, BS-2, 3)); pygame.draw.rect(s, dk, (1, BS//2-4, BS-2, 7), 1)
    for lx in [3, BS-8]:
        pygame.draw.rect(s, c,  (lx, BS//2+3, 5, BS//2-5)); pygame.draw.rect(s, dk, (lx, BS//2+3, 5, BS//2-5), 1)
        pygame.draw.rect(s, c,  (lx-1, BS-6, 7, 3));         pygame.draw.rect(s, dk, (lx-1, BS-6, 7, 3), 1)
    surfs[bid] = s

    bid = STONE_ALTAR
    # if bid == STONE_ALTAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); BS = BLOCK_SIZE
    c = (178, 168, 158); dk = _darken(c, 22); lt = _lighter(c, 14)
    s.fill(c)
    pygame.draw.rect(s, lt, (2, 2, BS-4, 5));    pygame.draw.rect(s, dk, (2, 2, BS-4, 5), 1)
    pygame.draw.rect(s, lt, (4, 7, BS-8, BS-16)); pygame.draw.rect(s, dk, (4, 7, BS-8, BS-16), 1)
    pygame.draw.ellipse(s, (210, 80, 20), (6, 8, BS-12, 6))
    pygame.draw.ellipse(s, (255, 160, 30), (8, 9, BS-16, 4))
    pygame.draw.ellipse(s, (255, 220, 80), (BS//2-3, 9, 6, 3))
    pygame.draw.rect(s, lt, (2, BS-8, BS-4, 6)); pygame.draw.rect(s, dk, (2, BS-8, BS-4, 6), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = BRONZE_MIRROR
    # if bid == BRONZE_MIRROR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    brnz = (135, 98, 52); dk = _darken(brnz, 25); lt = _lighter(brnz, 22); handle = (110, 80, 40)
    pygame.draw.line(s, handle, (BS//2, BS//2+4), (BS//2, BS-3), 3)
    pygame.draw.ellipse(s, handle, (BS//2-3, BS-5, 6, 3))
    pygame.draw.circle(s, brnz,         (BS//2, BS//2-2), BS//2-4)
    pygame.draw.circle(s, dk,            (BS//2, BS//2-2), BS//2-4, 2)
    pygame.draw.circle(s, (180, 150, 90),(BS//2, BS//2-2), BS//2-6)
    pygame.draw.ellipse(s, lt, (BS//2-5, BS//2-8, 6, 4))
    surfs[bid] = s

    bid = CLAY_OIL_LAMP
    # if bid == CLAY_OIL_LAMP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (170, 120, 72); dk = _darken(c, 22); lt = _lighter(c, 18)
    pygame.draw.ellipse(s, c,  (BS//2-8, BS//2-2, 16, 10)); pygame.draw.ellipse(s, dk, (BS//2-8, BS//2-2, 16, 10), 1)
    pygame.draw.ellipse(s, lt, (BS//2-5, BS//2-1, 6, 4))
    spout = [(BS//2+6,BS//2+1),(BS//2+10,BS//2-2),(BS//2+10,BS//2+3),(BS//2+7,BS//2+5)]
    pygame.draw.polygon(s, c, spout); pygame.draw.polygon(s, dk, spout, 1)
    pygame.draw.arc(s, c, (BS//2-9, BS//2-6, 6, 6), 0, 3.14159, 2)
    pygame.draw.ellipse(s, (255,175,40), (BS//2+7, BS//2-7, 4, 5))
    pygame.draw.ellipse(s, (255,230,100),(BS//2+8, BS//2-6, 2, 3))
    surfs[bid] = s

    bid = AGORA_SCALE
    # if bid == AGORA_SCALE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (130, 105, 58); dk = _darken(c, 25)
    pygame.draw.line(s, c, (BS//2, 2), (BS//2, BS//2), 2)
    pygame.draw.line(s, c, (4, BS//3), (BS-4, BS//3), 2)
    pygame.draw.line(s, c, (4, BS//3), (6, BS//2+4), 1)
    pygame.draw.line(s, c, (BS-4, BS//3), (BS-6, BS//2+4), 1)
    for ex, ey in [(2, BS//2+2), (BS-10, BS//2)]:
        pygame.draw.ellipse(s, c,  (ex, ey, 8, 5)); pygame.draw.ellipse(s, dk, (ex, ey, 8, 5), 1)
    pygame.draw.circle(s, dk, (BS//2, 2), 2)
    pygame.draw.rect(s, c, (BS//2-2, BS//2, 4, BS//2-3))
    pygame.draw.rect(s, dk, (BS//2-4, BS-4, 8, 3))
    surfs[bid] = s

    bid = LAUREL_WREATH_MOUNT
    # if bid == LAUREL_WREATH_MOUNT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    import math as _m
    green = (55, 95, 42); lt_g = _lighter(green, 20); dk_g = _darken(green, 20)
    cx, cy, r = BS//2, BS//2, BS//2-3
    for i in range(16):
        angle = i * _m.pi / 8
        lx = int(cx + r * _m.cos(angle)); ly = int(cy + r * _m.sin(angle))
        col = lt_g if i % 2 == 0 else green
        pygame.draw.ellipse(s, col,  (lx-3, ly-2, 6, 4))
        pygame.draw.ellipse(s, dk_g, (lx-3, ly-2, 6, 4), 1)
    pygame.draw.circle(s, green, (cx, cy), r, 3)
    for dx in [-r//2, r//2]:
        pygame.draw.circle(s, (210, 180, 50), (cx+dx, cy), 3)
    surfs[bid] = s

    bid = HERMES_STELE
    # if bid == HERMES_STELE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (190, 182, 172); dk = _darken(c, 22); lt = _lighter(c, 12)
    pygame.draw.rect(s, c,  (BS//2-5, 2, 10, BS-6)); pygame.draw.rect(s, dk, (BS//2-5, 2, 10, BS-6), 1)
    pygame.draw.rect(s, lt, (BS//2-5, 2, 10, 4))
    pygame.draw.ellipse(s, c,  (BS//2-6, 2, 12, 10)); pygame.draw.ellipse(s, dk, (BS//2-6, 2, 12, 10), 1)
    pygame.draw.rect(s, c,  (BS//2-7, BS-6, 14, 4)); pygame.draw.rect(s, dk, (BS//2-7, BS-6, 14, 4), 1)
    for y in [BS//3, BS//2, 2*BS//3]:
        pygame.draw.line(s, dk, (BS//2-4, y), (BS//2+4, y), 1)
    surfs[bid] = s

    bid = DORIC_CAPITAL
    # if bid == DORIC_CAPITAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); BS = BLOCK_SIZE
    c = (232, 228, 218); dk = _darken(c, 20); lt = _lighter(c, 8)
    s.fill(c)
    pygame.draw.rect(s, lt, (0, 0, BS, 5));    pygame.draw.rect(s, dk, (0, 0, BS, 5), 1)
    pygame.draw.rect(s, lt, (2, 5, BS-4, 4));  pygame.draw.rect(s, dk, (2, 5, BS-4, 4), 1)
    pygame.draw.ellipse(s, lt, (4, 9, BS-8, 8)); pygame.draw.ellipse(s, dk, (4, 9, BS-8, 8), 1)
    pygame.draw.rect(s, c,  (BS//4, 17, BS//2, BS-19)); pygame.draw.rect(s, dk, (BS//4, 17, BS//2, BS-19), 1)
    for x in range(BS//4+3, BS//4+BS//2-3, 5):
        pygame.draw.line(s, dk, (x, 18), (x, BS-3), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = VICTORY_STELE
    # if bid == VICTORY_STELE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (220, 215, 205); dk = _darken(c, 22); lt = _lighter(c, 10)
    pygame.draw.rect(s, c,  (BS//2-6, 4, 12, BS-8)); pygame.draw.rect(s, dk, (BS//2-6, 4, 12, BS-8), 1)
    pygame.draw.rect(s, lt, (BS//2-6, 4, 12, 4))
    pygame.draw.ellipse(s, c,  (BS//2-7, 2, 14, 8)); pygame.draw.ellipse(s, dk, (BS//2-7, 2, 14, 8), 1)
    pygame.draw.rect(s, c,  (BS//2-8, BS-6, 16, 4)); pygame.draw.rect(s, dk, (BS//2-8, BS-6, 16, 4), 1)
    for y in range(10, BS-10, 6):
        pygame.draw.line(s, dk, (BS//2-5, y),   (BS//2+4, y),   1)
        pygame.draw.line(s, lt, (BS//2-4, y+1), (BS//2+3, y+1), 1)
    pygame.draw.arc(s, (200, 170, 90), (BS//2-4, 12, 8, 6), 0, 3.14159, 2)
    surfs[bid] = s

    bid = BRONZE_SHIELD_MOUNT
    # if bid == BRONZE_SHIELD_MOUNT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    import math as _m
    brnz = (115, 90, 48); dk = _darken(brnz, 28); lt = _lighter(brnz, 22); boss = (140, 110, 58)
    r = BS//2-2
    pygame.draw.circle(s, brnz, (BS//2, BS//2), r); pygame.draw.circle(s, dk, (BS//2, BS//2), r, 2)
    pygame.draw.circle(s, lt,   (BS//2, BS//2), r-3, 1)
    pygame.draw.circle(s, boss, (BS//2, BS//2), r//3+1); pygame.draw.circle(s, dk, (BS//2, BS//2), r//3+1, 1)
    pygame.draw.circle(s, lt,   (BS//2, BS//2), r//3-1)
    for i in range(8):
        angle = i * _m.pi / 4
        pygame.draw.circle(s, dk, (int(BS//2+(r-4)*_m.cos(angle)), int(BS//2+(r-4)*_m.sin(angle))), 2)
    surfs[bid] = s

    bid = EGG_AND_DART
    # if bid == EGG_AND_DART
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); BS = BLOCK_SIZE
    c = (215, 210, 200); dk = _darken(c, 22); lt = _lighter(c, 10); egg = (230, 225, 215)
    s.fill(c)
    pygame.draw.rect(s, dk, (0, 0, BS, 3)); pygame.draw.rect(s, dk, (0, BS-3, BS, 3))
    for x in range(2, BS-2, 10):
        pygame.draw.ellipse(s, egg, (x, 4, 7, 10)); pygame.draw.ellipse(s, dk, (x, 4, 7, 10), 1)
        pygame.draw.ellipse(s, lt,  (x+1, 5, 3, 4))
        dart = x + 8
        if dart < BS-2:
            pygame.draw.polygon(s, dk, [(dart, 4), (dart+2, BS-5), (dart-1, BS-5)])
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = OLIVE_BRANCH
    # if bid == OLIVE_BRANCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    import math as _m
    stem = (90, 70, 40); green = (62, 98, 45); lt_g = _lighter(green, 20)
    pygame.draw.line(s, stem, (3, BS-4), (BS-3, 4), 2)
    for i in range(5):
        t = i / 4
        bx = int(3 + (BS-6) * t); by = int((BS-4) - (BS-8) * t)
        for side in [-1, 1]:
            angle = side * _m.pi / 4 - _m.pi / 2
            lx = int(bx + 7 * _m.cos(angle + t*0.5)); ly = int(by + 7 * _m.sin(angle + t*0.5))
            pygame.draw.ellipse(s, green, (min(bx,lx), min(by,ly), 6, 4))
            pygame.draw.ellipse(s, lt_g,  (min(bx,lx)+1, min(by,ly)+1, 3, 2))
    surfs[bid] = s

    bid = PHILOSOPHERS_SCROLL
    # if bid == PHILOSOPHERS_SCROLL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    pap = (215, 195, 150); dk = _darken(pap, 22); lt = _lighter(pap, 12); roll = (180, 155, 110)
    for rx in [0, BS-6]:
        pygame.draw.ellipse(s, roll, (rx, BS//4, 6, BS//2)); pygame.draw.ellipse(s, dk, (rx, BS//4, 6, BS//2), 1)
    pygame.draw.rect(s, pap, (3, BS//4, BS-6, BS//2)); pygame.draw.rect(s, dk, (3, BS//4, BS-6, BS//2), 1)
    pygame.draw.line(s, lt, (4, BS//4+1), (BS-4, BS//4+1), 1)
    for y in range(BS//4+5, BS//4+BS//2-4, 5):
        pygame.draw.line(s, dk, (5, y), (BS-5, y), 1)
    surfs[bid] = s

    bid = GREEK_THEATRE_MASK
    # if bid == GREEK_THEATRE_MASK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0)); BS = BLOCK_SIZE
    c = (230, 190, 140); dk = _darken(c, 25); lt = _lighter(c, 18); brow = (80, 55, 30)
    pygame.draw.ellipse(s, c,  (3, 2, BS-6, BS-4)); pygame.draw.ellipse(s, dk, (3, 2, BS-6, BS-4), 1)
    pygame.draw.ellipse(s, lt, (5, 3, (BS-6)//2, (BS-4)//3))
    pygame.draw.ellipse(s, (30, 20, 15), (BS//2-5, BS//3-1, 4, 6))
    pygame.draw.ellipse(s, (30, 20, 15), (BS//2+1,  BS//3-1, 4, 6))
    pygame.draw.arc(s, brow, (BS//2-6, BS//3-4, 5, 4), 0, 3.14159, 2)
    pygame.draw.arc(s, brow, (BS//2+1,  BS//3-4, 5, 4), 0, 3.14159, 2)
    mouth = [(BS//2-5,2*BS//3),(BS//2+5,2*BS//3),(BS//2+4,2*BS//3+5),(BS//2-4,2*BS//3+5)]
    pygame.draw.polygon(s, (30, 20, 15), mouth)
    pygame.draw.arc(s, dk, (BS//2-6, 2*BS//3-2, 12, 8), 3.14159, 2*3.14159, 2)
    surfs[bid] = s

    bid = TORCH
    # if bid == TORCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    stick = (120, 75, 30); slt = _lighter(stick, 15)
    flame = (255, 150, 20); inner = (255, 230, 80)
    pygame.draw.line(s, stick, (BS//2 - 1, BS - 4), (BS//2 + 1, BS//4 + 4), 3)
    pygame.draw.line(s, slt,   (BS//2,     BS - 4), (BS//2 + 2, BS//4 + 4), 1)
    pygame.draw.ellipse(s, flame, (BS//2 - 3, BS//4 - 4, 7, 9))
    pygame.draw.ellipse(s, inner, (BS//2 - 1, BS//4 - 2, 4, 5))
    surfs[bid] = s

    bid = WALL_SCONCE
    # if bid == WALL_SCONCE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (55, 55, 60); dk = _darken(iron, 20)
    glow = (255, 200, 80); warm = (255, 230, 150)
    pygame.draw.rect(s, iron, (2, BS//2 - 2, BS//2 + 2, 4))
    pygame.draw.rect(s, dk,   (2, BS//2 - 2, BS//2 + 2, 4), 1)
    pygame.draw.line(s, iron, (3, BS//2 - 2), (3, BS//2 + 5), 3)
    pygame.draw.circle(s, iron, (BS - 6, BS//2), 7)
    pygame.draw.circle(s, glow, (BS - 6, BS//2), 5)
    pygame.draw.circle(s, warm, (BS - 6, BS//2), 3)
    surfs[bid] = s

    bid = BRAZIER
    # if bid == BRAZIER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (65, 60, 55); dk = _darken(iron, 20)
    fire1 = (230, 80, 20); fire2 = (255, 160, 40); fire3 = (255, 230, 80)
    pygame.draw.line(s, iron, (BS//2, BS//2), (4,      BS - 4), 2)
    pygame.draw.line(s, iron, (BS//2, BS//2), (BS - 4, BS - 4), 2)
    pygame.draw.line(s, iron, (BS//2, BS//2), (BS//2,  BS - 2), 2)
    pygame.draw.ellipse(s, iron, (4, BS//3, BS - 8, 8), 2)
    pygame.draw.ellipse(s, fire1, (6,  BS//3 - 10, BS - 12, 12))
    pygame.draw.ellipse(s, fire2, (9,  BS//3 -  8, BS - 18,  9))
    pygame.draw.ellipse(s, fire3, (12, BS//3 -  5, BS - 24,  6))
    surfs[bid] = s

    bid = CHANDELIER
    # if bid == CHANDELIER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (55, 55, 60)
    candle = (240, 228, 200); flame = (255, 175, 40); inner = (255, 230, 90)
    for y in range(0, 8, 3):
        pygame.draw.rect(s, iron, (BS//2 - 1, y, 2, 2))
    pygame.draw.ellipse(s, iron, (3, 8, BS - 6, 5), 2)
    for cx2 in [5, BS//2, BS - 6]:
        pygame.draw.line(s, iron, (cx2, 11), (cx2, BS - 12), 1)
        pygame.draw.rect(s, candle, (cx2 - 2, BS - 12, 4, 7))
        pygame.draw.ellipse(s, flame, (cx2 - 2, BS - 14, 5, 5))
        pygame.draw.ellipse(s, inner, (cx2 - 1, BS - 13, 3, 3))
    surfs[bid] = s

    bid = CANDELABRA
    # if bid == CANDELABRA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (60, 55, 50)
    candle = (240, 228, 200); flame = (255, 175, 40); inner = (255, 230, 90)
    pygame.draw.rect(s, iron, (BS//2 - 5, BS - 5, 10, 4))
    pygame.draw.line(s, iron, (BS//2, BS - 5), (BS//2, BS//3), 2)
    pygame.draw.line(s, iron, (4, BS//3 + 4), (BS - 4, BS//3 + 4), 2)
    for cx2, cy2 in [(8, BS//3), (BS//2, BS//3 - 2), (BS - 8, BS//3)]:
        pygame.draw.line(s, iron, (cx2, BS//3 + 4), (cx2, cy2), 1)
        pygame.draw.rect(s, candle, (cx2 - 2, cy2 - 7, 4, 7))
        pygame.draw.ellipse(s, flame, (cx2 - 2, cy2 - 10, 4, 5))
        pygame.draw.ellipse(s, inner, (cx2 - 1, cy2 - 9, 2, 3))
    surfs[bid] = s

    bid = LANTERN_ORB
    # if bid == LANTERN_ORB
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (50, 50, 58)
    ob = (160, 220, 250); om = (200, 235, 255); oi = (240, 250, 255)
    for y in range(0, 5, 2):
        pygame.draw.rect(s, iron, (BS//2 - 1, y, 2, 2))
    pygame.draw.circle(s, iron, (BS//2, BS//2 + 3), 11, 1)
    pygame.draw.circle(s, ob, (BS//2, BS//2 + 3), 9)
    pygame.draw.circle(s, om, (BS//2, BS//2 + 3), 6)
    pygame.draw.circle(s, oi, (BS//2, BS//2 + 3), 3)
    pygame.draw.circle(s, (255, 255, 255), (BS//2 - 2, BS//2 + 1), 2)
    surfs[bid] = s

    bid = PENDANT_LAMP
    # if bid == PENDANT_LAMP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (55, 55, 60)
    glass = (255, 220, 120); warm = (255, 240, 170)
    for y in range(0, BS//3, 2):
        pygame.draw.circle(s, iron, (BS//2, y + 1), 1)
    pygame.draw.rect(s, iron, (BS//2 - 5, BS//3, 10, 3))
    pygame.draw.ellipse(s, iron, (BS//2 - 6, BS//3 + 2, 12, 14), 1)
    pygame.draw.ellipse(s, glass, (BS//2 - 5, BS//3 + 3, 10, 12))
    pygame.draw.ellipse(s, warm,  (BS//2 - 3, BS//3 + 5,  6,  8))
    pygame.draw.line(s, iron, (BS//2, BS//3 + 16), (BS//2, BS//3 + 19), 2)
    surfs[bid] = s

    bid = FIRE_BOWL
    # if bid == FIRE_BOWL
    import math as _bm2
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    stone = (100, 95, 88); dk = _darken(stone, 25)
    fire1 = (220, 70, 15); fire2 = (255, 155, 35); fire3 = (255, 225, 70)
    pygame.draw.arc(s, stone, (2, BS//2 - 2, BS - 4, BS//2 + 2),
                    _bm2.pi, 2 * _bm2.pi, 5)
    pygame.draw.line(s, stone, (2, BS//2 - 2), (BS - 2, BS//2 - 2), 3)
    pygame.draw.ellipse(s, fire1, (4,  BS//4,     BS - 8,  BS//3))
    pygame.draw.ellipse(s, fire2, (8,  BS//4 - 3, BS - 16, BS//4 + 2))
    pygame.draw.ellipse(s, fire3, (12, BS//4 - 5, BS - 24, BS//5))
    surfs[bid] = s

    bid = CROSS_LANTERN
    # if bid == CROSS_LANTERN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    iron = (50, 50, 55)
    glass = (255, 195, 60); glow = (255, 225, 130)
    cx2 = BS // 2; cy2 = BS // 2
    for gx, gy in [(cx2 - 9, cy2 - 9), (cx2 + 1, cy2 - 9),
                   (cx2 - 9, cy2 + 1), (cx2 + 1, cy2 + 1)]:
        pygame.draw.rect(s, glass, (gx, gy, 8, 8))
        pygame.draw.rect(s, glow,  (gx + 2, gy + 2, 4, 4))
    pygame.draw.rect(s, iron, (cx2 - 2, 1, 4, BS - 2))
    pygame.draw.rect(s, iron, (1, cy2 - 2, BS - 2, 4))
    pygame.draw.rect(s, iron, (1, 1, BS - 2, BS - 2), 2)
    surfs[bid] = s

    bid = STAR_LAMP
    # if bid == STAR_LAMP
    import math as _bm3
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    cx2 = BS // 2; cy2 = BS // 2
    frame = (80, 75, 95)
    crystal = (190, 235, 255); glow = (225, 248, 255)
    for deg in range(0, 360, 45):
        angle = _bm3.radians(deg)
        ex = int(cx2 + _bm3.cos(angle) * 13)
        ey = int(cy2 + _bm3.sin(angle) * 13)
        pygame.draw.line(s, frame, (cx2, cy2), (ex, ey), 2)
    pygame.draw.circle(s, crystal, (cx2, cy2), 8)
    pygame.draw.circle(s, glow,    (cx2, cy2), 5)
    pygame.draw.circle(s, (255, 255, 255), (cx2 - 2, cy2 - 2), 2)
    surfs[bid] = s

    bid = GLOW_VINE
    # if bid == GLOW_VINE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    vine = (38, 85, 42); vine_lt = _lighter(vine, 18)
    glow_c = (60, 220, 170); glow_lt = (140, 255, 220)
    pts1 = [(4,2),(7,8),(10,5),(14,12),(18,8),(22,15),(26,11),(28,18)]
    for i in range(len(pts1) - 1):
        pygame.draw.line(s, vine, pts1[i], pts1[i+1], 2)
    pts2 = [(6,14),(10,20),(14,17),(18,24),(22,20),(25,28)]
    for i in range(len(pts2) - 1):
        pygame.draw.line(s, vine, pts2[i], pts2[i+1], 2)
    for bx2, by2 in [(7,6),(14,10),(21,7),(10,18),(17,22),(24,14),(5,26)]:
        pygame.draw.circle(s, glow_c,  (bx2, by2), 3)
        pygame.draw.circle(s, glow_lt, (bx2, by2), 1)
    surfs[bid] = s

    bid = TOWN_FLAG_BLOCK
    # if bid == TOWN_FLAG_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    pole = (120, 100, 70)
    # Flagpole — thin vertical bar
    pygame.draw.rect(s, pole, (BS // 2 - 2, 0, 3, BS))
    # Pennant: triangle jutting right from pole top
    flag_col = (200, 55, 40)
    pts = [(BS // 2 + 1, 3), (BS - 4, 9), (BS // 2 + 1, 16)]
    pygame.draw.polygon(s, flag_col, pts)
    pygame.draw.polygon(s, _darken(flag_col), pts, 1)
    surfs[bid] = s

    bid = OUTPOST_FLAG_BLOCK
    # if bid == OUTPOST_FLAG_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    pole = (120, 100, 70)
    pygame.draw.rect(s, pole, (BS // 2 - 2, 0, 3, BS))
    flag_col = (180, 140, 60)
    pts = [(BS // 2 + 1, 3), (BS - 4, 9), (BS // 2 + 1, 16)]
    pygame.draw.polygon(s, flag_col, pts)
    pygame.draw.polygon(s, _darken(flag_col), pts, 1)
    surfs[bid] = s

    bid = LANDMARK_FLAG_BLOCK
    # if bid == LANDMARK_FLAG_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    pole = (110,  90,  60)
    pygame.draw.rect(s, pole, (BS // 2 - 2, 0, 3, BS))
    # Tall split-tail banner — distinguishes from town/outpost flags
    flag_col = (190, 150,  60)
    pygame.draw.polygon(s, flag_col,
        [(BS // 2 + 1,  2), (BS - 3,  6),
         (BS // 2 + 6, 11), (BS - 3, 16),
         (BS // 2 + 1, 20)])
    pygame.draw.polygon(s, _darken(flag_col),
        [(BS // 2 + 1,  2), (BS - 3,  6),
         (BS // 2 + 6, 11), (BS - 3, 16),
         (BS // 2 + 1, 20)], 1)
    # Gold ball atop pole — marks "important place"
    pygame.draw.circle(s, (230, 200,  90), (BS // 2 - 1, 2), 2)
    surfs[bid] = s

    bid = ICE_SHARD
    # if bid == ICE_SHARD
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    snow = (220, 232, 245)
    pygame.draw.rect(s, snow, (0, BS - 4, BS, 4))
    c_base = (185, 225, 248)
    c_bright = (228, 245, 255)
    c_dark = _darken(c_base, 28)
    for cx2, base_h, w2 in [(4, 14, 3), (10, 20, 4), (18, 16, 3), (25, 11, 2)]:
        tip_y = BS - 4 - base_h
        pts = [(cx2 - w2, BS - 4), (cx2 + w2, BS - 4), (cx2, tip_y)]
        pygame.draw.polygon(s, c_base, pts)
        pygame.draw.polygon(s, c_dark, pts, 1)
        hi_x = cx2 - w2 // 2
        pygame.draw.line(s, c_bright, (hi_x, BS - 5), (hi_x, tip_y + base_h // 3), 1)
    surfs[bid] = s

    bid = FROZEN_BOG
    # if bid == FROZEN_BOG
    rng_bog = _rnd.Random(0xB0CEFE)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    BS = BLOCK_SIZE
    bog_dark = (32, 48, 58)
    bog_mid = (52, 75, 90)
    bog_ice = (148, 185, 210)
    bog_ice2 = (178, 210, 228)
    pygame.draw.rect(s, bog_dark, (0, 0, BS, BS))
    for _ in range(6):
        rx = rng_bog.randint(1, BS - 5)
        ry = rng_bog.randint(1, BS - 5)
        rw = rng_bog.randint(3, 8)
        rh = rng_bog.randint(2, 5)
        pygame.draw.ellipse(s, bog_mid, (rx, ry, rw, rh))
    for _ in range(4):
        lx2 = rng_bog.randint(2, BS - 4)
        ly2 = rng_bog.randint(2, BS - 4)
        ex = rng_bog.randint(3, 9)
        ey = rng_bog.randint(1, 3)
        pygame.draw.ellipse(s, bog_ice, (lx2, ly2, ex, ey))
        pygame.draw.ellipse(s, bog_ice2, (lx2 + 1, ly2, ex - 2, max(1, ey - 1)))
    surfs[bid] = s

    bid = CITY_BLOCK
    # if bid == CITY_BLOCK — stone pillar with gold trim and a crown atop
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    stone  = (160, 148, 128)
    stone2 = (180, 168, 148)
    gold   = (200, 168,  72)
    gold_d = (150, 120,  42)
    # Base
    pygame.draw.rect(s, stone,  (3,       BS - 6, BS - 6, 6))
    pygame.draw.rect(s, stone2, (4,       BS - 5, BS - 8, 4))
    # Shaft
    pygame.draw.rect(s, stone,  (BS//2 - 5, 10, 10, BS - 16))
    pygame.draw.rect(s, stone2, (BS//2 - 4, 11,  5, BS - 18))
    # Capital (top block)
    pygame.draw.rect(s, stone,  (2, 6, BS - 4, 8))
    pygame.draw.rect(s, stone2, (3, 7, BS - 6, 5))
    # Gold trim band on capital
    pygame.draw.rect(s, gold,   (2, 6,  BS - 4, 2))
    pygame.draw.rect(s, gold,   (2, 12, BS - 4, 2))
    # Crown atop: five gold spikes
    for i, cx_off in enumerate(range(2, BS - 2, (BS - 4) // 5)):
        h = 5 if i % 2 == 0 else 3
        pygame.draw.rect(s, gold,   (cx_off, 2 - h, 2, h + 2))
        pygame.draw.rect(s, gold_d, (cx_off, 2 - h, 1, h + 2))
    surfs[bid] = s

    bid = MINING_POST_BLOCK
    # Wooden post with iron mounting plate and a directional arrow
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    wood  = (120,  85,  50)
    wood2 = (145, 105,  65)
    iron  = (150, 145, 140)
    iron2 = (180, 175, 170)
    # Post shaft
    pygame.draw.rect(s, wood,  (BS//2 - 3, 6, 6, BS - 8))
    pygame.draw.rect(s, wood2, (BS//2 - 2, 7, 3, BS - 10))
    # Iron mounting bracket (horizontal bar near top)
    pygame.draw.rect(s, iron,  (4, 10, BS - 8, 5))
    pygame.draw.rect(s, iron2, (5, 11, BS - 10, 3))
    # Iron base plate
    pygame.draw.rect(s, iron,  (4, BS - 8, BS - 8, 5))
    pygame.draw.rect(s, iron2, (5, BS - 7, BS - 10, 3))
    # Pickaxe symbol: diagonal handle + head
    hx, hy = BS//2 - 1, 15
    pygame.draw.line(s, iron, (hx, hy), (hx + 6, hy + 6), 2)
    pygame.draw.rect(s, iron2, (hx - 1, hy - 2, 4, 3))
    surfs[bid] = s

    bid = BANNER_BLOCK
    # Vertical wooden pole with a rectangular banner cloth hanging from a crossbar
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    BS = BLOCK_SIZE
    pole  = (110,  80,  45)
    pole2 = (140, 105,  60)
    cloth = ( 60, 100, 180)   # default field color (blue)
    cloth2 = _darken(cloth)
    gold  = (200, 168,  72)
    # Pole shaft (left-side vertical)
    pygame.draw.rect(s, pole,  (4,       0, 4, BS))
    pygame.draw.rect(s, pole2, (5,       1, 2, BS - 2))
    # Crossbar at top
    pygame.draw.rect(s, pole,  (4, 4, BS - 6, 3))
    pygame.draw.rect(s, pole2, (5, 5, BS - 8, 1))
    # Banner cloth hanging from crossbar (right of pole)
    bx0, by0 = 8, 7
    bw,  bh  = BS - 10, BS - 14
    pygame.draw.rect(s, cloth,  (bx0,     by0, bw, bh))
    pygame.draw.rect(s, cloth2, (bx0 + 1, by0, bw - 2, 2))
    # Gold border stripe
    pygame.draw.rect(s, gold, (bx0, by0,      bw, 2))
    pygame.draw.rect(s, gold, (bx0, by0 + bh - 2, bw, 2))
    # Small gold cross charge placeholder
    cx2 = bx0 + bw // 2
    cy2 = by0 + bh // 2
    pygame.draw.rect(s, gold, (cx2 - 1, by0 + 4, 2, bh - 8))
    pygame.draw.rect(s, gold, (bx0 + 3, cy2 - 1, bw - 6, 2))
    surfs[bid] = s

    return surfs
