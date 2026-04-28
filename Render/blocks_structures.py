import pygame
import math
import random as _rnd
from blocks import BLOCKS
from blocks import *  # all block ID constants
from constants import BLOCK_SIZE
from Render.block_helpers import _darken, _lighter, _tinted, _MSTYLES, CAVE_MUSHROOMS, render_mushroom_preview


def build_structure_surfs():
    surfs = {}
    bid = POLISHED_GRANITE
    # if bid == POLISHED_GRANITE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 15)
    for px2, py2 in [(5,4),(13,8),(21,5),(8,18),(26,14),(17,23),(3,27),(28,7),(10,29)]:
        pygame.draw.rect(s, dk, (px2, py2, 2, 1))
        pygame.draw.rect(s, dk, (px2+1, py2+1, 1, 2))
    pygame.draw.line(s, lt, (2, 2), (BLOCK_SIZE-2, 4), 1)
    pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
    surfs[bid] = s

    bid = POLISHED_MARBLE
    # if bid == POLISHED_MARBLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    vn = _darken(c, 50)
    lt = _lighter(c, 10)
    pygame.draw.line(s, vn, (6, 0), (30, 26), 1)
    pygame.draw.line(s, lt, (7, 0), (31, 26), 1)
    pygame.draw.line(s, vn, (0, 8), (22, 32), 1)
    pygame.draw.line(s, vn, (14, 0), (32, 18), 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = SLATE_TILE
    # if bid == SLATE_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    dk = _darken(c, 30)
    pygame.draw.line(s, dk, (16, 0), (16, BLOCK_SIZE), 2)
    pygame.draw.line(s, dk, (0, 16), (BLOCK_SIZE, 16), 2)
    for tx2, ty2 in [(2,2),(18,2),(2,18),(18,18)]:
        pygame.draw.line(s, lt, (tx2, ty2), (tx2+12, ty2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = TERRACOTTA_BLOCK
    # if bid == TERRACOTTA_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    lt = _lighter(c, 20)
    pygame.draw.ellipse(s, dk, (5, 7, 22, 18), 1)
    pygame.draw.ellipse(s, dk, (9, 11, 14, 10), 1)
    pygame.draw.ellipse(s, lt, (7, 9, 18, 14), 1)
    pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
    surfs[bid] = s

    bid = MOSSY_BRICK
    # if bid in (MOSSY_BRICK, CREAM_BRICK, LAPIS_BRICK, GILDED_BRICK, IVORY_BRICK, CRIMSON_BRICK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CREAM_BRICK
    # if bid in (MOSSY_BRICK, CREAM_BRICK, LAPIS_BRICK, GILDED_BRICK, IVORY_BRICK, CRIMSON_BRICK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = LAPIS_BRICK
    # if bid in (MOSSY_BRICK, CREAM_BRICK, LAPIS_BRICK, GILDED_BRICK, IVORY_BRICK, CRIMSON_BRICK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = GILDED_BRICK
    # if bid in (MOSSY_BRICK, CREAM_BRICK, LAPIS_BRICK, GILDED_BRICK, IVORY_BRICK, CRIMSON_BRICK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = IVORY_BRICK
    # if bid in (MOSSY_BRICK, CREAM_BRICK, LAPIS_BRICK, GILDED_BRICK, IVORY_BRICK, CRIMSON_BRICK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CRIMSON_BRICK
    # if bid in (MOSSY_BRICK, CREAM_BRICK, LAPIS_BRICK, GILDED_BRICK, IVORY_BRICK, CRIMSON_BRICK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CHARCOAL_PLANK
    # if bid in (CHARCOAL_PLANK, WALNUT_PLANK, TEAK_PLANK, CEDAR_PANEL, EBONY_PLANK, MAHOGANY_PLANK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = WALNUT_PLANK
    # if bid in (CHARCOAL_PLANK, WALNUT_PLANK, TEAK_PLANK, CEDAR_PANEL, EBONY_PLANK, MAHOGANY_PLANK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TEAK_PLANK
    # if bid in (CHARCOAL_PLANK, WALNUT_PLANK, TEAK_PLANK, CEDAR_PANEL, EBONY_PLANK, MAHOGANY_PLANK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CEDAR_PANEL
    # if bid in (CHARCOAL_PLANK, WALNUT_PLANK, TEAK_PLANK, CEDAR_PANEL, EBONY_PLANK, MAHOGANY_PLANK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = EBONY_PLANK
    # if bid in (CHARCOAL_PLANK, WALNUT_PLANK, TEAK_PLANK, CEDAR_PANEL, EBONY_PLANK, MAHOGANY_PLANK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MAHOGANY_PLANK
    # if bid in (CHARCOAL_PLANK, WALNUT_PLANK, TEAK_PLANK, CEDAR_PANEL, EBONY_PLANK, MAHOGANY_PLANK)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_RED
    # if bid in (STAINED_GLASS_RED, STAINED_GLASS_BLUE, STAINED_GLASS_GREEN)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_BLUE
    # if bid in (STAINED_GLASS_RED, STAINED_GLASS_BLUE, STAINED_GLASS_GREEN)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_GREEN
    # if bid in (STAINED_GLASS_RED, STAINED_GLASS_BLUE, STAINED_GLASS_GREEN)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CLEAR_GLASS
    # if bid in (CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON, STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET, STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_GOLDEN
    # if bid in (CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON, STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET, STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_CRIMSON
    # if bid in (CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON, STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET, STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_ROSE
    # if bid in (CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON, STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET, STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_COBALT
    # if bid in (CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON, STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET, STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_VIOLET
    # if bid in (CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON, STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET, STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_VERDANT
    # if bid in (CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON, STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET, STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_AMBER
    # if bid in (CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON, STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET, STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAINED_GLASS_IVORY
    # if bid in (CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON, STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET, STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CATHEDRAL_WINDOW
    # if bid == CATHEDRAL_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    bg   = (20, 30, 55)
    pane = ( 55,  90, 185)
    gold = (190, 160,  50)
    lead = (30, 30, 30)
    s.fill(bg)
    # two colored panes flanking center lead
    pygame.draw.rect(s, pane, (2, 14, 11, 14))
    pygame.draw.rect(s, pane, (19, 14, 11, 14))
    # pointed arch outline
    cx2 = BLOCK_SIZE // 2
    pygame.draw.line(s, lead, (2, 28), (cx2, 2), 2)
    pygame.draw.line(s, lead, (cx2, 2), (BLOCK_SIZE-3, 28), 2)
    pygame.draw.line(s, lead, (2, 28), (BLOCK_SIZE-3, 28), 2)
    # central vertical lead bar
    pygame.draw.line(s, lead, (cx2, 2), (cx2, 30), 2)
    # gold tracery circle at top
    pygame.draw.circle(s, gold, (cx2, 10), 5, 1)
    pygame.draw.circle(s, pane, (cx2, 10), 3)
    # base fill below arch
    pygame.draw.rect(s, _darken(bg, 10), (2, 28, BLOCK_SIZE-4, BLOCK_SIZE-30))
    pygame.draw.rect(s, lead, s.get_rect(), 1)
    surfs[bid] = s

    bid = MOSAIC_GLASS
    # if bid == MOSAIC_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = _lighter(BLOCKS[bid]["color"], 30)
    s.fill(base)
    lead = (30, 30, 30)
    tile_colors = [
        (215, 175, 40), (55, 90, 185), (220, 110, 155),
        (130, 65, 195), (60, 148, 75), (200, 115, 35),
        (185, 35, 45),  (245, 240, 220),
    ]
    positions = [
        (2, 2), (10, 2), (18, 2), (26, 2),
        (2,10), (10,10), (18,10), (26,10),
        (2,18), (10,18), (18,18), (26,18),
        (2,26), (10,26), (18,26), (26,26),
    ]
    for i, (tx, ty) in enumerate(positions):
        col = tile_colors[i % len(tile_colors)]
        pygame.draw.rect(s, col, (tx, ty, 7, 7))
        pygame.draw.rect(s, lead, (tx, ty, 7, 7), 1)
    pygame.draw.rect(s, lead, s.get_rect(), 1)
    surfs[bid] = s

    bid = SMOKED_GLASS
    # if bid == SMOKED_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    s.fill(c)
    pygame.draw.line(s, lt, (0, BLOCK_SIZE), (BLOCK_SIZE, 0), 1)
    pygame.draw.line(s, lt, (4, BLOCK_SIZE), (BLOCK_SIZE, 4), 1)
    pygame.draw.line(s, lt, (0, BLOCK_SIZE-4), (BLOCK_SIZE-4, 0), 1)
    pygame.draw.rect(s, (20, 25, 30), s.get_rect(), 2)
    surfs[bid] = s

    bid = RIBBED_GLASS
    # if bid == RIBBED_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
    lt = _lighter(c, 30)
    dk = _darken(c, 15)
    s.fill(c)
    for rx in range(2, BLOCK_SIZE - 1, 5):
        pygame.draw.line(s, lt, (rx,   0), (rx,   BLOCK_SIZE), 1)
        pygame.draw.line(s, dk, (rx+2, 0), (rx+2, BLOCK_SIZE), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = HAMMERED_GLASS
    # if bid == HAMMERED_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
    lt = _lighter(c, 28)
    dk = _darken(c, 18)
    s.fill(c)
    import random as _rnd
    rng = _rnd.Random(42)
    for _ in range(22):
        bx2 = rng.randint(1, BLOCK_SIZE - 5)
        by2 = rng.randint(1, BLOCK_SIZE - 5)
        w2  = rng.randint(3, 6)
        h2  = rng.randint(3, 6)
        col2 = lt if rng.random() > 0.5 else dk
        pygame.draw.ellipse(s, col2, (bx2, by2, w2, h2))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CRACKLED_GLASS
    # if bid == CRACKLED_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
    lt = _lighter(c, 35)
    dk = _darken(c, 20)
    s.fill(lt)
    crack = dk
    cx2, cy2 = BLOCK_SIZE // 2, BLOCK_SIZE // 2
    endpoints = [(3, 3), (BLOCK_SIZE-4, 3), (3, BLOCK_SIZE-4),
                 (BLOCK_SIZE-4, BLOCK_SIZE-4), (BLOCK_SIZE//2, 2),
                 (2, BLOCK_SIZE//2), (BLOCK_SIZE-2, BLOCK_SIZE//2)]
    for ex2, ey2 in endpoints:
        pygame.draw.line(s, crack, (cx2, cy2), (ex2, ey2), 1)
    pygame.draw.circle(s, c, (cx2, cy2), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = OCULUS_WINDOW
    # if bid == OCULUS_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c    = BLOCKS[bid]["color"]
    lt   = _lighter(c, 35)
    lead = (30, 30, 30)
    gold = (180, 150, 45)
    s.fill(_darken(c, 30))
    r = BLOCK_SIZE // 2 - 2
    cx2, cy2 = BLOCK_SIZE // 2, BLOCK_SIZE // 2
    pygame.draw.circle(s, lt, (cx2, cy2), r)
    pygame.draw.circle(s, lead, (cx2, cy2), r, 2)
    for i in range(8):
        angle = math.pi * i / 4
        ex2 = cx2 + int(r * math.cos(angle))
        ey2 = cy2 + int(r * math.sin(angle))
        pygame.draw.line(s, lead, (cx2, cy2), (ex2, ey2), 1)
    pygame.draw.circle(s, gold, (cx2, cy2), 3)
    pygame.draw.rect(s, lead, s.get_rect(), 1)
    surfs[bid] = s

    bid = LANCET_WINDOW
    # if bid == LANCET_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c    = BLOCKS[bid]["color"]
    lt   = _lighter(c, 40)
    lead = (30, 30, 30)
    s.fill(_darken(c, 25))
    cx2 = BLOCK_SIZE // 2
    # narrow pane
    pygame.draw.rect(s, lt, (cx2 - 5, 14, 10, 16))
    # pointed arch lines
    pygame.draw.line(s, lead, (cx2 - 5, 30), (cx2,   4), 2)
    pygame.draw.line(s, lead, (cx2 + 5, 30), (cx2,   4), 2)
    pygame.draw.line(s, lead, (cx2 - 5, 30), (cx2 + 5, 30), 2)
    pygame.draw.line(s, lead, (cx2,  4), (cx2, 30), 1)
    pygame.draw.rect(s, lead, s.get_rect(), 1)
    surfs[bid] = s

    bid = DIAMOND_PANE
    # if bid == DIAMOND_PANE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c    = BLOCKS[bid]["color"]
    lt   = _lighter(c, 38)
    lead = (35, 35, 35)
    s.fill(lt)
    for i in range(-1, 3):
        ox = i * 8
        pygame.draw.line(s, lead, (ox,      0),          (ox + BLOCK_SIZE, BLOCK_SIZE), 1)
        pygame.draw.line(s, lead, (ox,      BLOCK_SIZE), (ox + BLOCK_SIZE, 0),          1)
    pygame.draw.rect(s, lead, s.get_rect(), 1)
    surfs[bid] = s

    bid = SEA_GLASS
    # if bid == SEA_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
    lt = _lighter(c, 35)
    dk = _darken(c, 20)
    s.fill(lt)
    for bx2, by2, br in [(6, 6, 4), (20, 9, 3), (10, 20, 5), (24, 22, 3), (16, 14, 2)]:
        pygame.draw.circle(s, c,  (bx2, by2), br)
        pygame.draw.circle(s, lt, (bx2 - 1, by2 - 1), max(1, br - 1), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MIRROR_GLASS
    # if bid == MIRROR_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c   = BLOCKS[bid]["color"]
    lt  = _lighter(c, 40)
    dk  = _darken(c, 20)
    s.fill(c)
    pygame.draw.rect(s, lt, (3, 2, 6, BLOCK_SIZE - 4))
    pygame.draw.rect(s, dk, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
    surfs[bid] = s

    bid = IRIDESCENT_GLASS
    # if bid == IRIDESCENT_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
    lt = _lighter(c, 30)
    s.fill(lt)
    layers = [
        ((215, 175, 40),  (3,  3, 14, 14)),
        ((55,  90, 185),  (14, 3, 14, 14)),
        ((220,110, 155),  (8, 14, 14, 14)),
        ((60, 148,  75),  (3, 14, 10, 10)),
        ((130, 65, 195),  (18, 14, 10, 10)),
    ]
    for col2, rect2 in layers:
        surf2 = pygame.Surface((rect2[2], rect2[3]), pygame.SRCALPHA)
        surf2.fill((*col2, 110))
        s.blit(surf2, (rect2[0], rect2[1]))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = SUNSET_GLASS
    # if bid == SUNSET_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c     = BLOCKS[bid]["color"]
    bands = [(240, 90, 50), (230, 130, 60), (215, 170, 55), (200, 115, 35)]
    band_h = BLOCK_SIZE // len(bands)
    for i, bc in enumerate(bands):
        pygame.draw.rect(s, bc, (0, i * band_h, BLOCK_SIZE, band_h + 1))
    lead = (40, 30, 20)
    pygame.draw.line(s, lead, (BLOCK_SIZE//2, 0), (BLOCK_SIZE//2, BLOCK_SIZE), 2)
    pygame.draw.rect(s, lead, s.get_rect(), 1)
    surfs[bid] = s

    bid = OBSIDIAN_GLASS
    # if bid == OBSIDIAN_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
    lt = _lighter(c, 30)
    s.fill(c)
    pygame.draw.ellipse(s, (60, 30, 80), (4, 4, 12, 10))
    pygame.draw.ellipse(s, lt,            (5, 5, 6,  5))
    pygame.draw.rect(s, (50, 30, 70), s.get_rect(), 2)
    surfs[bid] = s

    bid = CRYSTAL_GLASS
    # if bid == CRYSTAL_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 10)
    s.fill(lt)
    # sparkle stars at four spots
    for sx2, sy2 in [(6, 6), (22, 8), (10, 22), (24, 24)]:
        for angle in [0, math.pi/2, math.pi/4, 3*math.pi/4]:
            ex2 = sx2 + int(4 * math.cos(angle))
            ey2 = sy2 + int(4 * math.sin(angle))
            pygame.draw.line(s, (255, 255, 255), (sx2, sy2), (ex2, ey2), 1)
        pygame.draw.circle(s, (255, 255, 255), (sx2, sy2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = ZELLIGE_BLUE
    # if bid in {ZELLIGE_BLUE, ZELLIGE_TERRACOTTA, ZELLIGE_EMERALD, ZELLIGE_WHITE}
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    dk = _darken(c, 30)
    cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
    r_out, r_in = 10, 4
    pts = [(cx2 + (r_out if i%2==0 else r_in)*math.cos(math.pi*i/8 - math.pi/16),
            cy2 + (r_out if i%2==0 else r_in)*math.sin(math.pi*i/8 - math.pi/16))
           for i in range(16)]
    pygame.draw.polygon(s, lt, pts)
    pygame.draw.polygon(s, dk, pts, 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = ZELLIGE_TERRACOTTA
    # if bid in {ZELLIGE_BLUE, ZELLIGE_TERRACOTTA, ZELLIGE_EMERALD, ZELLIGE_WHITE}
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    dk = _darken(c, 30)
    cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
    r_out, r_in = 10, 4
    pts = [(cx2 + (r_out if i%2==0 else r_in)*math.cos(math.pi*i/8 - math.pi/16),
            cy2 + (r_out if i%2==0 else r_in)*math.sin(math.pi*i/8 - math.pi/16))
           for i in range(16)]
    pygame.draw.polygon(s, lt, pts)
    pygame.draw.polygon(s, dk, pts, 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = ZELLIGE_EMERALD
    # if bid in {ZELLIGE_BLUE, ZELLIGE_TERRACOTTA, ZELLIGE_EMERALD, ZELLIGE_WHITE}
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    dk = _darken(c, 30)
    cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
    r_out, r_in = 10, 4
    pts = [(cx2 + (r_out if i%2==0 else r_in)*math.cos(math.pi*i/8 - math.pi/16),
            cy2 + (r_out if i%2==0 else r_in)*math.sin(math.pi*i/8 - math.pi/16))
           for i in range(16)]
    pygame.draw.polygon(s, lt, pts)
    pygame.draw.polygon(s, dk, pts, 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = ZELLIGE_WHITE
    # if bid in {ZELLIGE_BLUE, ZELLIGE_TERRACOTTA, ZELLIGE_EMERALD, ZELLIGE_WHITE}
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    dk = _darken(c, 30)
    cx2, cy2 = BLOCK_SIZE//2, BLOCK_SIZE//2
    r_out, r_in = 10, 4
    pts = [(cx2 + (r_out if i%2==0 else r_in)*math.cos(math.pi*i/8 - math.pi/16),
            cy2 + (r_out if i%2==0 else r_in)*math.sin(math.pi*i/8 - math.pi/16))
           for i in range(16)]
    pygame.draw.polygon(s, lt, pts)
    pygame.draw.polygon(s, dk, pts, 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = CALCADA_PORTUGUESA
    # if bid == CALCADA_PORTUGUESA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((32, 30, 28))
    w = (218, 215, 205)   # white limestone
    b = (20, 18, 16)      # black basalt
    BS = BLOCK_SIZE
    for row in range(4):
        y2 = row * 8 + 2
        x_off = 4 if row % 2 else 0
        for col in range(5):
            wx = col * 7 + x_off - 3
            if 0 <= wx <= BS - 6:
                c2 = w if (row + col) % 2 == 0 else b
                pygame.draw.ellipse(s, c2, (wx, y2, 6, 5))
    pygame.draw.rect(s, (18, 16, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = AZULEJO_GEOMETRIC
    # if bid == AZULEJO_GEOMETRIC
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((245, 242, 235))
    cb = (42, 88, 172)
    BS = BLOCK_SIZE
    H = BS // 2
    pygame.draw.rect(s, cb, s.get_rect(), 2)
    pygame.draw.rect(s, cb, (4, 4, BS - 8, BS - 8), 1)
    # center diamond
    cx2, cy2 = H, H
    r = 8
    pygame.draw.polygon(s, cb, [(cx2, cy2-r), (cx2+r, cy2), (cx2, cy2+r), (cx2-r, cy2)])
    # corner accent diamonds
    r2 = 3
    for pcx, pcy in [(3, 3), (BS-4, 3), (3, BS-4), (BS-4, BS-4)]:
        pygame.draw.polygon(s, cb, [(pcx, pcy-r2), (pcx+r2, pcy), (pcx, pcy+r2), (pcx-r2, pcy)])
    surfs[bid] = s

    bid = PAINTED_TILE_BORDER
    # if bid == PAINTED_TILE_BORDER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((245, 240, 225))
    cb = (42, 88, 172)
    gold = (200, 162, 50)
    BS = BLOCK_SIZE
    # cobalt bands top and bottom
    pygame.draw.rect(s, cb, (0, 0, BS, 6))
    pygame.draw.rect(s, cb, (0, BS - 6, BS, 6))
    # golden centre stripe
    pygame.draw.rect(s, gold, (0, BS//2 - 2, BS, 4))
    # dot accents on cobalt bands
    for bx2 in range(5, BS - 4, 6):
        pygame.draw.circle(s, (245, 240, 225), (bx2, 3), 2)
        pygame.draw.circle(s, (245, 240, 225), (bx2, BS - 4), 2)
    pygame.draw.rect(s, _darken(cb, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = SPANISH_MAJOLICA
    # if bid == SPANISH_MAJOLICA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((242, 238, 218))
    c_green = (35, 112, 62)
    c_ochre = (195, 128, 40)
    c_red   = (185, 58, 48)
    BS = BLOCK_SIZE
    cx2, cy2 = BS // 2, BS // 2
    # border
    pygame.draw.rect(s, c_green, s.get_rect(), 2)
    # corner leaf squares
    for lx, ly in [(3, 3), (BS-7, 3), (3, BS-7), (BS-7, BS-7)]:
        pygame.draw.rect(s, c_green, (lx, ly, 4, 4))
    # ochre petals around center
    for i in range(4):
        a = math.pi * i / 2
        px2 = cx2 + int(7 * math.cos(a))
        py2 = cy2 + int(7 * math.sin(a))
        pygame.draw.circle(s, c_ochre, (px2, py2), 3)
    # red center dot
    pygame.draw.circle(s, c_red, (cx2, cy2), 4)
    pygame.draw.circle(s, (242, 238, 218), (cx2, cy2), 2)
    surfs[bid] = s

    bid = AZULEJO_STAIR
    # if bid == AZULEJO_STAIR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((245, 242, 235))
    cb = (42, 88, 172)
    md = (90, 130, 210)
    BS = BLOCK_SIZE
    # solid cobalt bottom band (the riser face)
    pygame.draw.rect(s, cb, (0, BS * 2 // 3, BS, BS // 3))
    # geometric stripe pattern in the blue band
    stripe_y = BS * 2 // 3 + 3
    for bx2 in range(0, BS, 6):
        pygame.draw.line(s, md, (bx2, stripe_y), (bx2 + 4, BS - 2), 1)
    # thin dividing line
    pygame.draw.line(s, cb, (0, BS * 2 // 3 - 1), (BS, BS * 2 // 3 - 1), 2)
    # upper tile: simple frame
    pygame.draw.rect(s, cb, (2, 2, BS - 4, BS * 2 // 3 - 4), 1)
    pygame.draw.rect(s, _darken(cb, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = PORTUGUESE_PINK_MARBLE
    # if bid == PORTUGUESE_PINK_MARBLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 25)
    dk = _darken(c, 15)
    pink = (215, 150, 150)
    pygame.draw.line(s, pink, (4, 2), (BLOCK_SIZE-2, BLOCK_SIZE-6), 1)
    pygame.draw.line(s, pink, (2, 10), (14, 2), 1)
    pygame.draw.line(s, pink, (BLOCK_SIZE-8, BLOCK_SIZE-2), (BLOCK_SIZE-2, BLOCK_SIZE-10), 1)
    pygame.draw.line(s, lt, (2, 2), (8, 6), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = SPANISH_HEX_TILE
    # if bid == SPANISH_HEX_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((22, 20, 18))
    w = (225, 222, 215)
    BS = BLOCK_SIZE
    for row in range(3):
        for col in range(3):
            cx2 = col * 12 + (6 if row % 2 else 0)
            cy2 = row * 10 + 5
            pts = [(int(cx2 + 5 * math.cos(math.pi/2 + math.pi*i/3)),
                    int(cy2 + 5 * math.sin(math.pi/2 + math.pi*i/3))) for i in range(6)]
            pygame.draw.polygon(s, w, pts, 1)
    pygame.draw.rect(s, (10, 8, 8), s.get_rect(), 1)
    surfs[bid] = s

    bid = MUDEJAR_STAR_TILE
    # if bid == MUDEJAR_STAR_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((245, 238, 215))
    cb = (42, 88, 172)
    teal = (40, 130, 130)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    r_out, r_in = 11, 5
    pts8 = [(int(cx2 + (r_out if i%2==0 else r_in) * math.cos(math.pi*i/4 - math.pi/8)),
             int(cy2 + (r_out if i%2==0 else r_in) * math.sin(math.pi*i/4 - math.pi/8)))
            for i in range(8)]
    pygame.draw.polygon(s, cb, pts8)
    pygame.draw.circle(s, teal, (cx2, cy2), 4)
    pygame.draw.rect(s, cb, s.get_rect(), 2)
    surfs[bid] = s

    bid = ALBARRADA_PANEL
    # if bid == ALBARRADA_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((245, 242, 238))
    cb = (42, 88, 172)
    md = (85, 130, 210)
    BS = BLOCK_SIZE
    cx2 = BS//2
    pygame.draw.rect(s, cb, (cx2-4, 20, 8, 10))
    pygame.draw.rect(s, cb, (cx2-3, 18, 6, 3))
    pygame.draw.rect(s, cb, (cx2-6, 28, 12, 2))
    pygame.draw.line(s, cb, (cx2, 18), (cx2-5, 10), 1)
    pygame.draw.line(s, cb, (cx2, 18), (cx2+5, 10), 1)
    pygame.draw.line(s, cb, (cx2, 18), (cx2, 8), 1)
    for fx, fy in [(cx2-5, 10), (cx2+5, 10), (cx2, 8)]:
        pygame.draw.circle(s, md, (fx, fy), 3)
    pygame.draw.rect(s, cb, s.get_rect(), 2)
    for bx2 in range(4, BS-3, 6):
        pygame.draw.circle(s, cb, (bx2, 2), 1)
        pygame.draw.circle(s, cb, (bx2, BS-2), 1)
    surfs[bid] = s

    bid = SGRAFFITO_WALL
    # if bid == SGRAFFITO_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 35)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    for gx in range(4, BS-3, 7):
        pygame.draw.line(s, dk, (gx, 2), (gx, BS-3), 1)
    for gy in range(4, BS-3, 7):
        pygame.draw.line(s, dk, (2, gy), (BS-3, gy), 1)
    cx2, cy2 = BS//2, BS//2
    r = 9
    pygame.draw.polygon(s, lt, [(cx2, cy2-r), (cx2+r, cy2), (cx2, cy2+r), (cx2-r, cy2)], 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = TRENCADIS_PANEL
    # if bid == TRENCADIS_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((185, 183, 178))
    pieces = [
        (1,1,7,5,(55,90,185)), (9,2,5,4,(210,175,50)), (15,1,8,4,(185,60,55)),
        (24,2,6,5,(55,155,70)), (2,7,4,6,(175,80,170)), (7,7,6,5,(245,242,230)),
        (14,6,5,6,(55,90,185)), (20,7,8,4,(60,160,175)), (1,14,8,4,(210,175,50)),
        (10,13,5,5,(55,155,70)), (16,13,7,4,(185,60,55)), (24,14,6,5,(245,242,230)),
        (2,19,5,6,(175,80,170)), (8,20,6,4,(55,90,185)), (15,19,8,5,(210,175,50)),
        (24,20,6,4,(55,155,70)), (1,26,7,4,(185,60,55)), (9,25,5,5,(60,160,175)),
        (15,26,7,4,(175,80,170)), (23,25,7,5,(245,242,230)),
    ]
    for px2, py2, pw, ph, pc in pieces:
        pygame.draw.rect(s, pc, (px2, py2, pw, ph))
    pygame.draw.rect(s, (145, 143, 138), s.get_rect(), 1)
    surfs[bid] = s

    bid = AZULEJO_NAVY
    # if bid == AZULEJO_NAVY
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 20)
    BS = BLOCK_SIZE
    pygame.draw.rect(s, lt, (3, 3, BS-6, BS-6), 1)
    cx2, cy2 = BS//2, BS//2
    pygame.draw.line(s, lt, (cx2, 5), (cx2, BS-6), 1)
    pygame.draw.line(s, lt, (5, cy2), (BS-6, cy2), 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = AZULEJO_MANGANESE
    # if bid == AZULEJO_MANGANESE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((238, 235, 228))
    pm = (110, 60, 130)
    md = (155, 100, 175)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    pygame.draw.rect(s, pm, s.get_rect(), 2)
    pygame.draw.rect(s, pm, (5, 5, BS-10, BS-10), 1)
    pygame.draw.circle(s, pm, (cx2, cy2), 7, 1)
    pygame.draw.circle(s, md, (cx2, cy2), 3)
    for i in range(4):
        a = math.pi * i / 2 + math.pi/4
        px2 = cx2 + int(10 * math.cos(a))
        py2 = cy2 + int(10 * math.sin(a))
        pygame.draw.circle(s, pm, (px2, py2), 2)
    surfs[bid] = s

    bid = PLATERESQUE_PANEL
    # if bid == PLATERESQUE_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    lt = _lighter(c, 18)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    for rx in [3, BS-6]:
        for ry in range(5, BS-4, 4):
            pygame.draw.rect(s, dk, (rx, ry, 3, 2))
    pygame.draw.rect(s, dk, (4, 6, BS-8, 2))
    pygame.draw.rect(s, dk, (4, BS-8, BS-8, 2))
    pygame.draw.circle(s, dk, (cx2, cy2), 7, 1)
    pygame.draw.circle(s, lt, (cx2, cy2), 4)
    for ax, ay in [(8, 14), (BS-10, 14), (8, BS-14), (BS-10, BS-14)]:
        pygame.draw.arc(s, dk, (ax-3, ay-3, 6, 6), 0, math.pi, 1)
    surfs[bid] = s

    bid = AZULEJO_CORNICE
    # if bid == AZULEJO_CORNICE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((245, 242, 235))
    cb = (42, 88, 172)
    BS = BLOCK_SIZE
    pygame.draw.rect(s, cb, (0, 0, BS, 8))
    for bx2 in range(2, BS-2, 8):
        pygame.draw.rect(s, (245, 242, 235), (bx2, 2, 5, 4))
    for bx2 in range(0, BS, 8):
        pygame.draw.line(s, cb, (bx2, 8), (bx2, BS), 1)
    pygame.draw.arc(s, cb, (4, 10, 10, 8), 0, math.pi, 1)
    pygame.draw.arc(s, cb, (18, 10, 10, 8), math.pi, 2*math.pi, 1)
    pygame.draw.rect(s, _darken(cb, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = TALAVERA_FOUNTAIN
    # if bid == TALAVERA_FOUNTAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((235, 240, 248))
    cb = (42, 88, 172)
    md = (90, 135, 215)
    gold = (200, 162, 50)
    green = (35, 112, 62)
    BS = BLOCK_SIZE
    cx2 = BS//2
    pygame.draw.arc(s, cb, (3, 3, BS-6, 20), 0, math.pi, 3)
    for ty in range(14, BS-4, 5):
        pygame.draw.line(s, md, (5, ty), (BS-6, ty), 1)
    for fx in [8, cx2, BS-9]:
        pygame.draw.circle(s, gold, (fx, 19), 3)
    for fx in [6, 13, cx2-3, cx2+3, BS-14, BS-7]:
        pygame.draw.circle(s, green, (fx, 26), 2)
    pygame.draw.rect(s, _darken(cb, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = BARCELONA_TILE
    # if bid == BARCELONA_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 22)
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    pygame.draw.ellipse(s, lt, (5, 5, BS-10, BS-10), 1)
    pygame.draw.ellipse(s, lt, (8, 3, BS-16, 12))
    pygame.draw.ellipse(s, lt, (8, BS-15, BS-16, 12))
    pygame.draw.ellipse(s, lt, (2, 8, 12, BS-16))
    pygame.draw.ellipse(s, lt, (BS-14, 8, 12, BS-16))
    pygame.draw.circle(s, dk, (cx2, cy2), 4)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MOORISH_ARCHWAY_TILE
    # if bid == MOORISH_ARCHWAY_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 22))
    lt = _lighter(c, 12)
    dk = _darken(c, 35)
    BS = BLOCK_SIZE
    pygame.draw.rect(s, c, (3, 14, 6, BS-15))
    pygame.draw.rect(s, c, (BS-9, 14, 6, BS-15))
    pygame.draw.arc(s, c, (2, 2, BS-4, 24), 0, math.pi, 4)
    pygame.draw.arc(s, lt, (4, 4, BS-8, 20), 0.1, math.pi-0.1, 1)
    for i in range(7):
        a = math.pi * i / 6
        rx = int(BS//2 + 11 * math.cos(a))
        ry = int(14 - 11 * math.sin(a))
        if 0 <= rx <= BS:
            pygame.draw.rect(s, dk, (rx-1, ry, 2, 2))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = PORTUGUESE_CHIMNEY
    # if bid == PORTUGUESE_CHIMNEY
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 22))
    dk = _darken(c, 32)
    lt = _lighter(c, 18)
    BS = BLOCK_SIZE
    cx2 = BS//2
    pygame.draw.rect(s, c, (cx2-6, 8, 12, 20))
    pygame.draw.line(s, lt, (cx2-5, 8), (cx2-5, 28), 1)
    for by2 in [12, 17, 22]:
        pygame.draw.rect(s, dk, (cx2-7, by2, 14, 2))
    pygame.draw.rect(s, c, (cx2-8, 5, 4, 6))
    pygame.draw.rect(s, c, (cx2-2, 3, 4, 8))
    pygame.draw.rect(s, c, (cx2+4, 5, 4, 6))
    pygame.draw.rect(s, c, (cx2-9, 27, 18, 4))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = BARCELOS_TILE
    # if bid == BARCELOS_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((242, 238, 222))
    cb = (42, 88, 172)
    BS = BLOCK_SIZE
    pygame.draw.ellipse(s, cb, (10, 14, 12, 10))
    pygame.draw.circle(s, cb, (19, 11), 4)
    pygame.draw.line(s, cb, (10, 16), (4, 8), 2)
    pygame.draw.line(s, cb, (10, 18), (3, 14), 2)
    pygame.draw.line(s, cb, (10, 20), (4, 22), 2)
    pygame.draw.line(s, cb, (14, 24), (13, 29), 2)
    pygame.draw.line(s, cb, (17, 24), (18, 29), 2)
    pygame.draw.polygon(s, cb, [(18, 8), (20, 5), (22, 8), (24, 5), (26, 8)])
    pygame.draw.rect(s, cb, s.get_rect(), 2)
    surfs[bid] = s

    bid = REJA_PANEL
    # if bid == REJA_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((225, 218, 205))
    iron = (35, 32, 30)
    lt = (62, 56, 52)
    BS = BLOCK_SIZE
    for bx2 in [5, 12, 19, 26]:
        pygame.draw.rect(s, iron, (bx2, 2, 3, BS-4))
        pygame.draw.line(s, lt, (bx2, 2), (bx2, BS-4), 1)
    for by2 in [6, 14, 22]:
        pygame.draw.rect(s, iron, (2, by2, BS-4, 3))
    for bx2 in [6, 13, 20, 27]:
        for by2 in [7, 15, 23]:
            pygame.draw.circle(s, lt, (bx2, by2), 2)
    pygame.draw.rect(s, iron, s.get_rect(), 2)
    surfs[bid] = s

    bid = IONIC_COLUMN_BASE
    # if bid == IONIC_COLUMN_BASE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(c)
    # base moulding
    pygame.draw.rect(s, dk, (0, BS-4, BS, 4))
    pygame.draw.line(s, lt, (0, BS-4), (BS, BS-4), 1)
    # shaft with flutes
    for fx in [5, 10, 15, 20, 25]:
        pygame.draw.line(s, dk, (fx, 4), (fx, BS-4), 1)
        pygame.draw.line(s, lt, (fx+1, 4), (fx+1, BS-4), 1)
    # Ionic volute capital (twin scrolls)
    pygame.draw.arc(s, dk, (3, 1, 8, 8), 0, math.pi*2, 2)
    pygame.draw.arc(s, dk, (BS-11, 1, 8, 8), 0, math.pi*2, 2)
    pygame.draw.rect(s, dk, (0, 2, BS, 3))
    pygame.draw.line(s, lt, (0, 2), (BS, 2), 1)
    surfs[bid] = s

    bid = DORIC_ENTABLATURE
    # if bid == DORIC_ENTABLATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(c)
    pygame.draw.line(s, lt, (0, 2), (BS, 2), 1)
    pygame.draw.line(s, dk, (0, BS-3), (BS, BS-3), 2)
    # triglyph channels
    for tx in [4, 12, 20, 28]:
        pygame.draw.rect(s, dk, (tx, 4, 2, BS-8))
        pygame.draw.rect(s, dk, (tx+3, 4, 2, BS-8))
    # metope panels between
    for mx in [8, 16, 24]:
        pygame.draw.rect(s, _lighter(c, 6), (mx, 5, 4, BS-10))
    surfs[bid] = s

    bid = RUSTICATED_BASE
    # if bid == RUSTICATED_BASE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 10)
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    s.fill(c)
    # deep V-joint courses
    for ry in [BS//3, 2*BS//3]:
        pygame.draw.line(s, dk, (0, ry), (BS, ry), 2)
        pygame.draw.line(s, lt, (0, ry+2), (BS, ry+2), 1)
    # vertical joints offset per course
    for rx in [BS//2]:
        pygame.draw.line(s, dk, (rx, 0), (rx, BS//3), 1)
    for rx in [BS//4, 3*BS//4]:
        pygame.draw.line(s, dk, (rx, BS//3), (rx, 2*BS//3), 1)
    for rx in [BS//2]:
        pygame.draw.line(s, dk, (rx, 2*BS//3), (rx, BS), 1)
    # bold outer border
    pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 2)
    surfs[bid] = s

    bid = GARDEN_LOGGIA
    # if bid == GARDEN_LOGGIA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 28)
    lt = _lighter(c, 12)
    inside = _darken(c, 45)
    BS = BLOCK_SIZE
    s.fill(c)
    # arch opening
    ax, aw, at = 5, BS-10, 4
    pygame.draw.rect(s, inside, (ax+2, at+aw//2, aw-4, BS-at-aw//2-2))
    pygame.draw.arc(s, dk, (ax, at, aw, aw), 0, math.pi, 3)
    pygame.draw.line(s, dk, (ax, at+aw//2), (ax, BS-2), 3)
    pygame.draw.line(s, dk, (ax+aw, at+aw//2), (ax+aw, BS-2), 3)
    # entablature band at top
    pygame.draw.rect(s, dk, (0, 0, BS, 4))
    pygame.draw.line(s, lt, (0, 4), (BS, 4), 1)
    surfs[bid] = s

    bid = TRIUMPHAL_ARCH_R
    # if bid == TRIUMPHAL_ARCH_R
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 25)
    lt = _lighter(c, 10)
    inside = _darken(c, 45)
    BS = BLOCK_SIZE
    s.fill(c)
    ax, aw, at = 6, BS-12, 6
    pygame.draw.rect(s, inside, (ax+2, at+aw//2, aw-4, BS-at-aw//2-2))
    pygame.draw.arc(s, dk, (ax, at, aw, aw), 0, math.pi, 4)
    pygame.draw.line(s, dk, (ax, at+aw//2), (ax, BS-2), 4)
    pygame.draw.line(s, dk, (ax+aw, at+aw//2), (ax+aw, BS-2), 4)
    # attic storey
    pygame.draw.rect(s, dk, (0, 0, BS, 5))
    pygame.draw.line(s, lt, (0, 5), (BS, 5), 1)
    # keystone
    pygame.draw.polygon(s, lt, [(BS//2-3, at), (BS//2+3, at), (BS//2, at+5)])
    surfs[bid] = s

    bid = EXEDRA_SEAT
    # if bid == EXEDRA_SEAT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 30))
    # curved back wall (arc)
    pygame.draw.arc(s, c, (2, 2, BS-4, BS-4), 0, math.pi, 6)
    # seat (flat horizontal)
    pygame.draw.rect(s, c, (1, BS//2, BS-2, 6))
    pygame.draw.line(s, lt, (1, BS//2), (BS-2, BS//2), 1)
    # legs
    pygame.draw.rect(s, dk, (3, BS//2+6, 4, BS//2-7))
    pygame.draw.rect(s, dk, (BS-7, BS//2+6, 4, BS//2-7))
    surfs[bid] = s

    bid = HERM_PILLAR
    # if bid == HERM_PILLAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # tapering shaft (wider at base)
    pygame.draw.polygon(s, c, [(BS//2-4, BS-2), (BS//2+4, BS-2), (BS//2+3, 10), (BS//2-3, 10)])
    # base block
    pygame.draw.rect(s, dk, (BS//2-5, BS-5, 10, 5))
    # head portrait (simplified)
    pygame.draw.circle(s, c, (BS//2, 7), 6)
    pygame.draw.circle(s, lt, (BS//2-1, 6), 2)
    pygame.draw.line(s, dk, (BS//2-2, 10), (BS//2+2, 10), 1)
    surfs[bid] = s

    bid = NYMPHAEUM_PANEL
    # if bid == NYMPHAEUM_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 28)
    lt = _lighter(c, 12)
    water = (80, 155, 200)
    BS = BLOCK_SIZE
    s.fill(c)
    # shell-shaped niche
    cx2, cy2 = BS//2, BS//2+2
    pygame.draw.ellipse(s, _darken(c, 35), (4, 4, BS-8, BS-8))
    # shell ribs
    for ai in range(-3, 4):
        ang = math.pi * ai / 6
        ex2 = cx2 + int(11 * math.cos(ang - math.pi/2))
        ey2 = cy2 + int(11 * math.sin(ang - math.pi/2))
        pygame.draw.line(s, dk, (cx2, cy2+4), (ex2, ey2), 1)
    # water cascade line
    pygame.draw.line(s, water, (cx2, cy2+2), (cx2, BS-3), 2)
    pygame.draw.ellipse(s, water, (cx2-4, BS-6, 8, 4))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = GROTTO_STONE
    # if bid == GROTTO_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    s.fill(c)
    # rough tufa texture: random bumps and hollows
    for ty in range(0, BS, 5):
        for tx in range(0, BS, 5):
            offset = (tx * 7 + ty * 11) % 5
            col = lt if offset < 2 else dk
            pygame.draw.circle(s, col, (tx+2, ty+2), 2)
    # stalactite tips at top
    for sx2 in [4, 10, 17, 23, 29]:
        drop = 3 + sx2 % 4
        pygame.draw.polygon(s, dk, [(sx2-2, 0), (sx2+2, 0), (sx2, drop)])
    pygame.draw.rect(s, _darken(c, 22), s.get_rect(), 1)
    surfs[bid] = s

    bid = AMPHITHEATER_TIER
    # if bid == AMPHITHEATER_TIER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    stone = (175, 168, 155)
    s.fill(c)
    # turf step
    pygame.draw.rect(s, c, (0, 0, BS, BS//2))
    # stone riser
    pygame.draw.rect(s, stone, (0, BS//2, BS, BS//2))
    pygame.draw.line(s, _lighter(stone, 12), (0, BS//2), (BS, BS//2), 1)
    pygame.draw.line(s, _darken(stone, 18), (0, BS-2), (BS, BS-2), 1)
    surfs[bid] = s

    bid = GIOCHI_ACQUA
    # if bid == GIOCHI_ACQUA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 25)
    stone = (175, 168, 155)
    BS = BLOCK_SIZE
    s.fill(stone)
    pygame.draw.line(s, _darken(stone, 15), (0, BS//2), (BS, BS//2), 1)
    pygame.draw.line(s, _darken(stone, 15), (BS//2, 0), (BS//2, BS), 1)
    # surprise jet at center
    jet_col = c
    pygame.draw.line(s, jet_col, (BS//2, BS//2), (BS//2, 4), 2)
    pygame.draw.line(s, lt, (BS//2-1, BS//2), (BS//2-1, 5), 1)
    # spray droplets
    for dx2, dy2 in [(-3, 3), (3, 3), (-5, 6), (5, 6), (0, 2)]:
        if 0 < BS//2+dx2 < BS and 0 < 4+dy2 < BS:
            pygame.draw.circle(s, lt, (BS//2+dx2, 4+dy2), 1)
    pygame.draw.circle(s, lt, (BS//2, 3), 2)
    surfs[bid] = s

    bid = RILL_BLOCK
    # if bid == RILL_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 22)
    stone = (185, 178, 165)
    BS = BLOCK_SIZE
    s.fill(stone)
    # stone channel edges
    pygame.draw.rect(s, _darken(stone, 18), (0, 0, BS, 6))
    pygame.draw.rect(s, _darken(stone, 18), (0, BS-6, BS, 6))
    # water channel
    pygame.draw.rect(s, c, (0, 6, BS, BS-12))
    for ry in [BS//2-1, BS//2+1]:
        pygame.draw.line(s, lt, (0, ry), (BS, ry), 1)
    surfs[bid] = s

    bid = CASCADE_BLOCK
    # if bid == CASCADE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    stone = (165, 158, 145)
    BS = BLOCK_SIZE
    s.fill(stone)
    water = (80, 160, 210)
    # three descending stone shelves
    for i in range(3):
        sy = i * BS//3
        pygame.draw.rect(s, stone, (i*3, sy, BS-i*3, BS//3))
        pygame.draw.line(s, _lighter(stone, 10), (i*3, sy), (BS-i*3, sy), 1)
        pygame.draw.line(s, water, (i*3, sy+BS//3-2), (BS-i*3, sy+BS//3-2), 2)
        pygame.draw.line(s, lt, (i*3, sy+BS//3-1), (BS-i*3, sy+BS//3-1), 1)
    surfs[bid] = s

    bid = GROTTO_POOL
    # if bid == GROTTO_POOL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 20))
    pygame.draw.ellipse(s, c, (2, 4, BS-4, BS-8))
    # dark mossy tone
    for r2 in [10, 7]:
        pygame.draw.ellipse(s, lt, (BS//2-r2, BS//2-r2+2, r2*2, r2*2-4), 1)
    # moss dots at edge
    moss = (42, 78, 35)
    for mx, my in [(3,8),(BS-5,9),(4,BS-7),(BS-4,BS-8)]:
        pygame.draw.circle(s, moss, (mx, my), 2)
    surfs[bid] = s

    bid = WALL_FOUNTAIN
    # if bid == WALL_FOUNTAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    water = (80, 160, 210)
    BS = BLOCK_SIZE
    s.fill(c)
    # mask face (grotesque)
    pygame.draw.circle(s, dk, (BS//2, 8), 6)
    pygame.draw.circle(s, lt, (BS//2-1, 7), 2)
    # open mouth spout
    pygame.draw.ellipse(s, _darken(c, 40), (BS//2-2, 11, 4, 3))
    # water stream down
    pygame.draw.line(s, water, (BS//2, 14), (BS//2, BS//2+2), 2)
    pygame.draw.line(s, _lighter(water, 20), (BS//2-1, 14), (BS//2-1, BS//2+2), 1)
    # basin
    pygame.draw.ellipse(s, c, (4, BS//2+2, BS-8, 8))
    pygame.draw.ellipse(s, lt, (4, BS//2+2, BS-8, 8), 1)
    pygame.draw.ellipse(s, water, (6, BS//2+3, BS-12, 5))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = BASIN_SURROUND
    # if bid == BASIN_SURROUND
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    water = (80, 155, 205)
    BS = BLOCK_SIZE
    s.fill(c)
    # outer carved rim
    pygame.draw.ellipse(s, dk, (1, 3, BS-2, BS-6), 3)
    pygame.draw.ellipse(s, lt, (2, 4, BS-4, BS-8), 1)
    # water inside
    pygame.draw.ellipse(s, water, (6, 8, BS-12, BS-16))
    # decorative egg-and-dart moulding hint
    for ai in range(6):
        ang = math.pi * ai / 3
        ex2 = BS//2 + int(13 * math.cos(ang))
        ey2 = BS//2 + int(7 * math.sin(ang))
        pygame.draw.circle(s, dk, (ex2, ey2), 2)
    surfs[bid] = s

    bid = CANAL_BLOCK
    # if bid == CANAL_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 22)
    stone = (180, 173, 160)
    BS = BLOCK_SIZE
    s.fill(stone)
    pygame.draw.rect(s, c, (3, 0, BS-6, BS))
    for ry in [BS//3, 2*BS//3]:
        pygame.draw.line(s, lt, (3, ry), (BS-3, ry), 1)
    pygame.draw.line(s, _darker(stone, 15) if hasattr(stone, '__call__') else _darken((180,173,160), 15), (3, 0), (3, BS), 1)
    pygame.draw.line(s, _darken(stone, 15), (BS-3, 0), (BS-3, BS), 1)
    surfs[bid] = s

    bid = TERME_POOL
    # if bid == TERME_POOL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 22)
    stone = (175, 168, 155)
    BS = BLOCK_SIZE
    s.fill(stone)
    pygame.draw.rect(s, _darken(stone, 18), (0, 0, BS, 4))
    pygame.draw.rect(s, _darken(stone, 18), (0, BS-4, BS, 4))
    pygame.draw.rect(s, _darken(stone, 18), (0, 0, 4, BS))
    pygame.draw.rect(s, _darken(stone, 18), (BS-4, 0, 4, BS))
    pygame.draw.rect(s, c, (4, 4, BS-8, BS-8))
    # steam wisps
    for sx2 in [8, BS//2, BS-8]:
        pygame.draw.arc(s, lt, (sx2-3, 6, 6, 5), 0, math.pi, 1)
    surfs[bid] = s

    bid = PARTERRE_BRODERIE
    # if bid == PARTERRE_BRODERIE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    sand = (210, 200, 178)
    BS = BLOCK_SIZE
    s.fill(sand)
    # embroidery curves: S-curves of clipped box
    for cy2 in range(4, BS, 8):
        for cx2 in range(0, BS, 4):
            wy = cy2 + int(3 * math.sin(cx2 * 0.5))
            if 0 <= wy < BS:
                pygame.draw.rect(s, c, (cx2, wy, 3, 3))
    surfs[bid] = s

    bid = PARTERRE_COMPARTMENT
    # if bid == PARTERRE_COMPARTMENT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    sand = (210, 200, 178)
    BS = BLOCK_SIZE
    s.fill(sand)
    half = BS // 2
    # four quadrant beds edged with clipped box
    for (x1, y1, w, h) in [(1,1,half-2,half-2),(half+1,1,half-2,half-2),
                            (1,half+1,half-2,half-2),(half+1,half+1,half-2,half-2)]:
        pygame.draw.rect(s, c, (x1, y1, w, h), 2)
        pygame.draw.rect(s, _darken(sand, 10), (x1+2, y1+2, w-4, h-4))
    # cross paths
    pygame.draw.line(s, sand, (half, 0), (half, BS), 1)
    pygame.draw.line(s, sand, (0, half), (BS, half), 1)
    surfs[bid] = s

    bid = ALLEE_TREE
    # if bid == ALLEE_TREE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    trunk = (95, 62, 32)
    s.fill(_darken(c, 50))
    pygame.draw.rect(s, trunk, (BS//2-1, BS-7, 3, 7))
    # clipped cone/column shape — tight formal allée silhouette
    w = 6
    for ty in range(4, BS-6, 3):
        pygame.draw.rect(s, dk, (BS//2-w//2, ty, w, 3))
        pygame.draw.rect(s, c, (BS//2-w//2+1, ty, w-2, 2))
        if ty > BS//3:
            w = max(4, w)
    surfs[bid] = s

    bid = PLEACHED_HEDGE
    # if bid == PLEACHED_HEDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    trunk = (95, 62, 32)
    s.fill(_darken(c, 40))
    # trunks at edges and center
    for tx in [3, BS//2, BS-5]:
        pygame.draw.rect(s, trunk, (tx, BS//2, 3, BS//2))
    # horizontal pleached canopy band
    pygame.draw.rect(s, dk, (0, 4, BS, BS//2-4))
    pygame.draw.rect(s, c, (1, 5, BS-2, BS//2-6))
    pygame.draw.line(s, lt, (1, 5), (BS-2, 5), 1)
    # branch lines
    for bx2 in range(4, BS-3, 7):
        pygame.draw.line(s, trunk, (bx2, BS//2), (bx2, BS//4), 1)
    surfs[bid] = s

    bid = ESPALIER_WALL
    # if bid == ESPALIER_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    wall = (185, 175, 158)
    BS = BLOCK_SIZE
    s.fill(wall)
    # horizontal training wires
    for ry in [BS//4, BS//2, 3*BS//4]:
        pygame.draw.line(s, _darken(wall, 18), (0, ry), (BS, ry), 1)
    # espalier branches and leaves
    branch = (90, 62, 32)
    leaf = c
    pygame.draw.line(s, branch, (BS//2, BS-2), (BS//2, 2), 1)
    for ly in [BS//4, BS//2, 3*BS//4]:
        pygame.draw.line(s, branch, (BS//2, ly), (4, ly-3), 1)
        pygame.draw.line(s, branch, (BS//2, ly), (BS-4, ly-3), 1)
        for lx in [6, BS-6, 12, BS-12]:
            pygame.draw.circle(s, leaf, (lx, ly-3), 3)
    surfs[bid] = s

    bid = KNOT_GARDEN
    # if bid == KNOT_GARDEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    sand = (210, 200, 178)
    BS = BLOCK_SIZE
    s.fill(sand)
    # interlaced knot: two crossing sine waves in clipped box
    dk = _darken(c, 15)
    lt = _lighter(c, 10)
    for cx2 in range(0, BS, 2):
        wy1 = BS//2 + int(10 * math.sin(cx2 * 0.4))
        wy2 = BS//2 - int(10 * math.sin(cx2 * 0.4 + math.pi/2))
        if 0 <= wy1 < BS:
            pygame.draw.rect(s, c, (cx2, wy1-1, 2, 3))
        if 0 <= wy2 < BS:
            pygame.draw.rect(s, dk, (cx2, wy2-1, 2, 3))
    surfs[bid] = s

    bid = TURF_THEATER
    # if bid == TURF_THEATER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    stone = (175, 168, 155)
    BS = BLOCK_SIZE
    s.fill(c)
    # green turf step with stone riser
    pygame.draw.rect(s, stone, (0, 2*BS//3, BS, BS//3))
    pygame.draw.line(s, _lighter(stone, 12), (0, 2*BS//3), (BS, 2*BS//3), 1)
    # curved arc hint at top edge
    pygame.draw.arc(s, lt, (2, 2, BS-4, BS//2), 0, math.pi, 2)
    surfs[bid] = s

    bid = BED
    # if bid == BED — sleeping bed: frame + pillow + blanket
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    frame   = (120,  70,  40)   # wooden frame
    blanket = (180,  60,  90)   # pink/red blanket
    pillow  = (240, 220, 210)   # off-white pillow
    s.fill(frame)
    # blanket fills most of the block
    pygame.draw.rect(s, blanket, (2, BS//3, BS-4, BS*2//3 - 2))
    # pillow at the top
    pygame.draw.rect(s, pillow,  (3, 2, BS-6, BS//3 - 2))
    pygame.draw.rect(s, _darken(pillow, 20), (3, 2, BS-6, BS//3 - 2), 1)
    # blanket fold line
    pygame.draw.line(s, _darken(blanket, 20), (2, BS//3 + 4), (BS-3, BS//3 + 4), 1)
    # outer frame border
    pygame.draw.rect(s, _darken(frame, 20), s.get_rect(), 2)
    surfs[bid] = s

    bid = CARPET_BED
    # if bid == CARPET_BED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    cols = [c, _lighter(c, 20), (80, 130, 55), (210, 185, 55), (190, 80, 55)]
    # tight geometric carpet blocks
    cell = BS // 4
    for ty in range(4):
        for tx in range(4):
            col = cols[(tx + ty*2) % len(cols)]
            pygame.draw.rect(s, col, (tx*cell+1, ty*cell+1, cell-2, cell-2))
    surfs[bid] = s

    bid = OPUS_SECTILE
    # if bid == OPUS_SECTILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 10))
    # cut marble shapes: diamonds and triangles
    half = BS // 2
    pygame.draw.polygon(s, c, [(half, 2), (BS-2, half), (half, BS-2), (2, half)])
    pygame.draw.polygon(s, lt, [(half, 2), (BS-2, half), (half, BS-2), (2, half)], 1)
    pygame.draw.polygon(s, dk, [(2, 2), (half, 2), (2, half)])
    pygame.draw.polygon(s, dk, [(BS-2, 2), (half, 2), (BS-2, half)])
    pygame.draw.polygon(s, _lighter(c, 8), [(2, BS-2), (half, BS-2), (2, half)])
    pygame.draw.polygon(s, _lighter(c, 8), [(BS-2, BS-2), (half, BS-2), (BS-2, half)])
    pygame.draw.rect(s, _darken(c, 25), s.get_rect(), 1)
    surfs[bid] = s

    bid = TRAVERTINE_FLOOR
    # if bid == TRAVERTINE_FLOOR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 10)
    dk = _darken(c, 12)
    BS = BLOCK_SIZE
    s.fill(c)
    # travertine voids and strata
    for ty in range(3, BS-2, 6):
        pygame.draw.line(s, dk, (0, ty), (BS, ty), 1)
        pygame.draw.line(s, lt, (0, ty+1), (BS, ty+1), 1)
    # small voids
    for vx, vy in [(5,5),(18,11),(8,19),(24,7),(12,25),(28,22)]:
        pygame.draw.ellipse(s, _darken(c, 20), (vx, vy, 4, 2))
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = HERRINGBONE_GARDEN
    # if bid == HERRINGBONE_GARDEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 25))
    bw, bh = 10, 4
    for row in range(8):
        for col in range(8):
            x2 = (col - row) * (bw//2) + row * bh
            y2 = row * (bh + 1)
            if row % 2 == 0:
                pygame.draw.rect(s, c, (x2, y2, bw, bh))
                pygame.draw.line(s, lt, (x2, y2), (x2+bw, y2), 1)
            else:
                pygame.draw.rect(s, dk, (x2, y2, bw, bh))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = RAMP_STONE
    # if bid == RAMP_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 25))
    # diagonal ramp surface
    pygame.draw.polygon(s, c, [(0, BS-2), (BS, 2), (BS, BS-2)])
    pygame.draw.line(s, lt, (0, BS-2), (BS, 2), 1)
    # stone texture lines
    for i in range(1, 4):
        y1 = BS-2 - i * BS//4
        y2 = max(2, y1 - 2)
        pygame.draw.line(s, dk, (i*BS//4, y1), (BS, y2), 1)
    surfs[bid] = s

    bid = GARDEN_STEPS
    # if bid == GARDEN_STEPS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 25))
    for i in range(4):
        step_y = i * BS//4
        step_x = i * 4
        pygame.draw.rect(s, c, (step_x, step_y, BS-step_x, BS//4))
        pygame.draw.line(s, lt, (step_x, step_y), (BS-1, step_y), 1)
        pygame.draw.line(s, dk, (step_x, step_y+BS//4-1), (BS-1, step_y+BS//4-1), 1)
    surfs[bid] = s

    bid = SAND_ALLEE
    # if bid == SAND_ALLEE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 12)
    BS = BLOCK_SIZE
    s.fill(c)
    # light compacted sand — subtle rake marks
    for ry in range(4, BS, 6):
        pygame.draw.line(s, dk, (0, ry), (BS, ry), 1)
    # footprint-like impressions
    for fx, fy in [(6, 8), (20, 14), (10, 22), (24, 26)]:
        pygame.draw.ellipse(s, _darken(c, 18), (fx, fy, 5, 3))
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = PATTERNED_PAVEMENT
    # if bid == PATTERNED_PAVEMENT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    c2 = _darken(c, 28)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    s.fill(c2)
    # two-tone geometric: alternating diagonal squares
    cell = BS // 4
    for ty in range(4):
        for tx in range(4):
            col = c if (tx + ty) % 2 == 0 else c2
            pygame.draw.rect(s, col, (tx*cell+1, ty*cell+1, cell-2, cell-2))
            if col == c:
                pygame.draw.line(s, lt, (tx*cell+1, ty*cell+1), (tx*cell+cell-2, ty*cell+1), 1)
    pygame.draw.rect(s, _darken(c, 30), s.get_rect(), 1)
    surfs[bid] = s

    bid = INLAID_MARBLE
    # if bid == INLAID_MARBLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    inlay = (80, 115, 175)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    s.fill(c)
    pygame.draw.line(s, lt, (1, 2), (BS-2, 2), 1)
    # colored marble inlay geometric bands
    pygame.draw.rect(s, inlay, (3, BS//4, BS-6, 4))
    pygame.draw.rect(s, inlay, (3, 3*BS//4-4, BS-6, 4))
    pygame.draw.rect(s, _darken(inlay, 20), (3, BS//4, BS-6, 4), 1)
    pygame.draw.rect(s, _darken(inlay, 20), (3, 3*BS//4-4, BS-6, 4), 1)
    # vertical accents
    pygame.draw.rect(s, inlay, (BS//4, 3, 4, BS-6))
    pygame.draw.rect(s, inlay, (3*BS//4-4, 3, 4, BS-6))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = TALL_SUNDIAL
    # if bid == TALL_SUNDIAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # ornate pedestal: wider base, narrowing shaft, wider top
    pygame.draw.rect(s, dk, (BS//2-6, BS-5, 12, 5))
    pygame.draw.rect(s, c, (BS//2-4, BS//2+2, 8, BS//2-7))
    pygame.draw.line(s, lt, (BS//2-4, BS//2+2), (BS//2+4, BS//2+2), 1)
    # decorative knop on shaft
    pygame.draw.ellipse(s, c, (BS//2-5, BS//2-2, 10, 6))
    # dial platform
    pygame.draw.rect(s, c, (BS//2-8, BS//2-5, 16, 4))
    # gnomon
    pygame.draw.polygon(s, dk, [(BS//2, BS//2-5), (BS//2+7, BS//2-5), (BS//2, 6)])
    # hour lines on dial
    for ai in range(5):
        ang = math.pi * ai / 8 - math.pi/4
        ex2 = BS//2 + int(6 * math.cos(ang))
        ey2 = BS//2 - 3 + int(4 * math.sin(ang))
        pygame.draw.line(s, dk, (BS//2, BS//2-3), (ex2, ey2), 1)
    surfs[bid] = s

    bid = STONE_VASE
    # if bid == STONE_VASE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 15)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # tall amphora shape
    pygame.draw.rect(s, dk, (BS//2-3, BS-4, 6, 4))
    pygame.draw.ellipse(s, c, (5, BS//3, BS-10, 2*BS//3-4))
    pygame.draw.ellipse(s, lt, (6, BS//3+1, BS-12, 8))
    # narrow neck
    pygame.draw.rect(s, dk, (BS//2-3, BS//4, 6, BS//3-BS//4+2))
    # wide lip
    pygame.draw.rect(s, c, (BS//2-6, BS//4-4, 12, 5))
    pygame.draw.line(s, lt, (BS//2-5, BS//4-4), (BS//2+5, BS//4-4), 1)
    # handles
    pygame.draw.arc(s, dk, (1, BS//3, 6, 8), math.pi*0.5, math.pi*1.5, 2)
    pygame.draw.arc(s, dk, (BS-7, BS//3, 6, 8), math.pi*1.5, math.pi*2.5, 2)
    surfs[bid] = s

    bid = STONE_SPHERE
    # if bid == STONE_SPHERE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # sphere
    pygame.draw.circle(s, c, (BS//2, BS//2-2), BS//2-5)
    pygame.draw.circle(s, lt, (BS//2-3, BS//2-5), 5)
    pygame.draw.circle(s, dk, (BS//2, BS//2-2), BS//2-5, 1)
    # small plinth base
    pygame.draw.rect(s, dk, (BS//2-5, BS//2+BS//2-7, 10, 5))
    pygame.draw.line(s, lt, (BS//2-5, BS//2+BS//2-7), (BS//2+5, BS//2+BS//2-7), 1)
    surfs[bid] = s

    bid = CURVED_BENCH
    # if bid == CURVED_BENCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 30))
    # curved seat (arc-shaped top view)
    pygame.draw.arc(s, c, (2, BS//4, BS-4, BS//2), 0, math.pi, 6)
    pygame.draw.arc(s, lt, (3, BS//4+1, BS-6, BS//2-2), 0, math.pi, 1)
    # legs
    pygame.draw.rect(s, dk, (3, BS//2+4, 4, BS//2-5))
    pygame.draw.rect(s, dk, (BS//2-2, BS//2+4, 4, BS//2-5))
    pygame.draw.rect(s, dk, (BS-7, BS//2+4, 4, BS//2-5))
    surfs[bid] = s

    bid = ORNATE_GATE
    # if bid == ORNATE_GATE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 28)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 50))
    # ornate scrollwork arch at top
    pygame.draw.arc(s, c, (3, 2, BS-6, 12), 0, math.pi, 2)
    # main bars
    for bx2 in range(3, BS-1, 5):
        pygame.draw.line(s, c, (bx2, 14), (bx2, BS-2), 2)
        pygame.draw.polygon(s, lt, [(bx2-1, 13), (bx2+2, 13), (bx2, 10)])
    # scrollwork between bars
    for bx2 in range(5, BS-4, 10):
        pygame.draw.arc(s, c, (bx2, BS//2-3, 6, 6), 0, math.pi*2, 1)
    # top and bottom rails
    pygame.draw.rect(s, c, (0, 13, BS, 2))
    pygame.draw.rect(s, c, (0, BS-3, BS, 2))
    surfs[bid] = s

    bid = LEAD_PLANTER
    # if bid == LEAD_PLANTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # rectangular lead box
    pygame.draw.rect(s, c, (2, BS//3, BS-4, 2*BS//3-3))
    pygame.draw.rect(s, lt, (2, BS//3, BS-4, 4))
    # riveted corner decoration
    for cx2 in [3, BS-4]:
        for cy2 in [BS//3+2, BS-5]:
            pygame.draw.circle(s, dk, (cx2, cy2), 1)
    # soil and plant
    pygame.draw.ellipse(s, (70, 50, 30), (4, BS//3+4, BS-8, 6))
    pygame.draw.line(s, (55, 110, 45), (BS//2, BS//3+4), (BS//2-4, BS//4), 1)
    pygame.draw.line(s, (55, 110, 45), (BS//2, BS//3+4), (BS//2+4, BS//4), 1)
    pygame.draw.circle(s, (80, 140, 55), (BS//2, BS//4+1), 3)
    surfs[bid] = s

    bid = TERRACE_URN
    # if bid == TERRACE_URN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # tall pedestal
    pygame.draw.rect(s, dk, (BS//2-3, BS-4, 6, 4))
    pygame.draw.rect(s, c, (BS//2-2, BS//2+2, 4, BS//2-6))
    pygame.draw.rect(s, dk, (BS//2-5, BS//2-1, 10, 4))
    # large urn body
    pygame.draw.ellipse(s, c, (4, 6, BS-8, 2*BS//5))
    pygame.draw.ellipse(s, lt, (5, 7, BS-10, 8))
    # neck
    pygame.draw.rect(s, dk, (BS//2-3, 3, 6, 4))
    # wide rim
    pygame.draw.rect(s, c, (BS//2-7, 1, 14, 4))
    pygame.draw.line(s, lt, (BS//2-6, 1), (BS//2+6, 1), 1)
    # handles
    pygame.draw.arc(s, dk, (1, 10, 6, 8), math.pi*0.5, math.pi*1.5, 1)
    pygame.draw.arc(s, dk, (BS-7, 10, 6, 8), math.pi*1.5, math.pi*2.5, 1)
    surfs[bid] = s

    bid = STONE_PINEAPPLE
    # if bid == STONE_PINEAPPLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 35))
    # small plinth base
    pygame.draw.rect(s, dk, (BS//2-4, BS-4, 8, 4))
    # pineapple body (oval)
    pygame.draw.ellipse(s, c, (BS//2-6, 10, 12, BS//2))
    # diamond scale pattern
    for sy in range(12, 10+BS//2, 4):
        for sx2 in range(BS//2-5, BS//2+6, 4):
            pygame.draw.rect(s, dk, (sx2, sy, 3, 3), 1)
    # crown leaves
    for ai in range(5):
        ang = math.pi * ai / 5 - math.pi/2
        lx = BS//2 + int(5 * math.cos(ang))
        ly = 10 + int(5 * math.sin(ang))
        pygame.draw.line(s, (55, 110, 48), (BS//2, 10), (lx, ly), 2)
    surfs[bid] = s

    bid = GROTTO_ARCH
    # if bid == GROTTO_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 22)
    inside = _darken(c, 50)
    BS = BLOCK_SIZE
    s.fill(c)
    # rough tufa fill
    for ty in range(0, BS, 5):
        for tx in range(0, BS, 5):
            bump_c = lt if (tx*3+ty*7)%7 < 3 else dk
            pygame.draw.circle(s, bump_c, (tx+2, ty+2), 2)
    # arch opening
    ax, aw, at = 6, BS-12, 6
    pygame.draw.rect(s, inside, (ax+2, at+aw//2, aw-4, BS-at-aw//2-2))
    pygame.draw.arc(s, _darken(c, 40), (ax, at, aw, aw), 0, math.pi, 3)
    pygame.draw.line(s, _darken(c, 40), (ax, at+aw//2), (ax, BS-2), 3)
    pygame.draw.line(s, _darken(c, 40), (ax+aw, at+aw//2), (ax+aw, BS-2), 3)
    # stalactites
    for sx2 in [ax+4, ax+aw//2, ax+aw-4]:
        drop = 4 + sx2 % 3
        pygame.draw.polygon(s, _darken(c, 30), [(sx2-2, at+aw//2), (sx2+2, at+aw//2), (sx2, at+aw//2+drop)])
    surfs[bid] = s

    bid = PERGOLA_BEAM
    # if bid == PERGOLA_BEAM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 18)
    dk = _darken(c, 25)
    BS = BLOCK_SIZE
    s.fill(_darken(c, 40))
    # horizontal beam (full width)
    pygame.draw.rect(s, c, (0, BS//2-3, BS, 6))
    pygame.draw.line(s, lt, (0, BS//2-3), (BS, BS//2-3), 1)
    pygame.draw.line(s, dk, (0, BS//2+3), (BS, BS//2+3), 1)
    # grain lines
    for gx in range(4, BS-2, 6):
        pygame.draw.line(s, dk, (gx, BS//2-2), (gx+2, BS//2+2), 1)
    # vine tendrils hanging down
    vine = (50, 105, 40)
    for vx in range(4, BS-2, 8):
        drop = 3 + vx % 4
        pygame.draw.line(s, vine, (vx, BS//2+3), (vx+1, BS//2+3+drop), 1)
        pygame.draw.circle(s, _lighter(vine, 20), (vx+1, BS//2+3+drop), 1)
    surfs[bid] = s

    bid = LOGGIA_ARCH
    # if bid == LOGGIA_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 25)
    lt = _lighter(c, 12)
    inside = _darken(c, 45)
    BS = BLOCK_SIZE
    s.fill(c)
    ax, aw, at = 4, BS-8, 3
    pygame.draw.rect(s, inside, (ax+2, at+aw//2, aw-4, BS-at-aw//2-2))
    pygame.draw.arc(s, dk, (ax, at, aw, aw), 0, math.pi, 3)
    pygame.draw.line(s, dk, (ax, at+aw//2), (ax, BS-2), 3)
    pygame.draw.line(s, dk, (ax+aw, at+aw//2), (ax+aw, BS-2), 3)
    # column capitals
    pygame.draw.rect(s, dk, (ax-2, at+aw//2-3, 6, 4))
    pygame.draw.rect(s, dk, (ax+aw-4, at+aw//2-3, 6, 4))
    pygame.draw.line(s, lt, (1, 2), (BS-2, 2), 1)
    surfs[bid] = s

    bid = GARDEN_WALL_NICHE
    # if bid == GARDEN_WALL_NICHE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 22)
    inside = _darken(c, 40)
    BS = BLOCK_SIZE
    s.fill(c)
    # niche recess
    pygame.draw.rect(s, inside, (5, 6, BS-10, BS-10))
    pygame.draw.arc(s, dk, (5, 4, BS-10, 10), 0, math.pi, 2)
    pygame.draw.line(s, dk, (5, 9), (5, BS-4), 2)
    pygame.draw.line(s, dk, (BS-5, 9), (BS-5, BS-4), 2)
    # small statue silhouette inside
    statue = _lighter(inside, 18)
    pygame.draw.circle(s, statue, (BS//2, 14), 3)
    pygame.draw.rect(s, statue, (BS//2-2, 17, 4, 8))
    pygame.draw.line(s, lt, (1, 2), (BS-2, 2), 1)
    surfs[bid] = s

    bid = ORANGERY_WINDOW
    # if bid == ORANGERY_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 22)
    lt = _lighter(c, 12)
    glass = (195, 215, 230)
    BS = BLOCK_SIZE
    s.fill(c)
    # tall arched window
    ax, aw, at = 4, BS-8, 4
    # stone frame
    pygame.draw.arc(s, dk, (ax, at, aw, aw//2*2), 0, math.pi, 2)
    pygame.draw.line(s, dk, (ax, at+aw//2), (ax, BS-2), 2)
    pygame.draw.line(s, dk, (ax+aw, at+aw//2), (ax+aw, BS-2), 2)
    # glass fill
    pygame.draw.arc(s, glass, (ax+2, at+2, aw-4, aw//2*2-4), 0, math.pi, 0)
    pygame.draw.rect(s, glass, (ax+2, at+aw//2, aw-4, BS-at-aw//2-2))
    # glazing bars
    pygame.draw.line(s, dk, (BS//2, at+4), (BS//2, BS-2), 1)
    pygame.draw.line(s, dk, (ax+2, BS//2), (ax+aw-2, BS//2), 1)
    pygame.draw.line(s, lt, (1, 2), (BS-2, 2), 1)
    surfs[bid] = s

    bid = BELVEDERE_PANEL
    # if bid == BELVEDERE_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 12)
    dk = _darken(c, 20)
    BS = BLOCK_SIZE
    s.fill(c)
    # wall panel with blind arches
    pygame.draw.line(s, lt, (0, 2), (BS, 2), 1)
    pygame.draw.line(s, dk, (0, BS-3), (BS, BS-3), 1)
    # two blind arch panels
    for ax2 in [3, BS//2+2]:
        aw2 = BS//2-5
        pygame.draw.arc(s, dk, (ax2, 5, aw2, 12), 0, math.pi, 1)
        pygame.draw.line(s, dk, (ax2, 11), (ax2, BS-4), 1)
        pygame.draw.line(s, dk, (ax2+aw2, 11), (ax2+aw2, BS-4), 1)
        pygame.draw.rect(s, _darken(c, 12), (ax2+1, 11, aw2-2, BS-15))
    surfs[bid] = s

    bid = BOSCO_TREE
    # if bid == BOSCO_TREE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 16)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    trunk = (90, 58, 28)
    s.fill(_darken(c, 50))
    # gnarled wild trunk (offset from center)
    pygame.draw.line(s, trunk, (BS//2-2, BS-2), (BS//2+1, BS//3), 3)
    pygame.draw.line(s, trunk, (BS//2+1, BS//3), (BS//2-4, 6), 2)
    # irregular wild canopy — not formally clipped
    for cx2, cy2, r2 in [(BS//2-2, BS//4, 8), (BS//2+5, BS//4+3, 6),
                         (BS//2-5, BS//4+5, 5), (BS//2+2, BS//4-5, 5)]:
        if cy2 > 0:
            pygame.draw.circle(s, dk, (cx2, cy2), r2)
            pygame.draw.circle(s, c, (cx2-1, cy2-1), r2-2)
            pygame.draw.circle(s, lt, (cx2-2, cy2-2), 2)
    surfs[bid] = s

    bid = GIARDINO_SEGRETO
    # if bid == GIARDINO_SEGRETO
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    lt = _lighter(c, 14)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    wall = (170, 162, 148)
    s.fill(wall)
    pygame.draw.rect(s, _darken(wall, 15), (0, 0, BS, 4))
    pygame.draw.rect(s, _darken(wall, 10), (0, BS-4, BS, 4))
    # ivy/creeper covering
    ivy = c
    for ty in range(4, BS-4, 4):
        for tx in range(0, BS, 4):
            if (tx//4 + ty//4 + tx*3) % 3 != 0:
                pygame.draw.circle(s, ivy, (tx+2, ty+2), 2)
                pygame.draw.circle(s, lt, (tx+2, ty+1), 1)
    # hidden gate hint
    pygame.draw.rect(s, _darken(wall, 25), (BS//2-4, BS//3, 8, 2*BS//3))
    pygame.draw.arc(s, _darken(wall, 25), (BS//2-4, BS//3-4, 8, 8), 0, math.pi, 2)
    surfs[bid] = s

    bid = PIETRA_SERENA
    # if bid == PIETRA_SERENA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    # Three coursed stone rows with staggered vertical joints
    for row, y0 in enumerate([(0, 10), (10, 21), (21, BS)]):
        y1, y2 = y0
        pygame.draw.line(s, dk, (0, y2), (BS, y2), 1)
        offset = (row % 2) * (BS // 3)
        for x in range(offset, BS, BS // 3):
            pygame.draw.line(s, dk, (x, y1), (x, y2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = TRAVERTINE_WALL
    # if bid == TRAVERTINE_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 14)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    # Ashlar grid 2×2
    pygame.draw.line(s, dk, (0, BS // 2), (BS, BS // 2), 1)
    pygame.draw.line(s, dk, (BS // 2, 0), (BS // 2, BS // 2), 1)
    pygame.draw.line(s, dk, (BS // 4, BS // 2), (BS // 4, BS), 1)
    pygame.draw.line(s, dk, (3 * BS // 4, BS // 2), (3 * BS // 4, BS), 1)
    # Travertine pitting dots
    import random as _rnd
    _rng = _rnd.Random(706)
    for _ in range(12):
        px, py = _rng.randint(2, BS - 3), _rng.randint(2, BS - 3)
        pygame.draw.circle(s, dk, (px, py), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MARBLE_FACADE
    # if bid == MARBLE_FACADE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    vein = (195, 190, 188)
    BS = BLOCK_SIZE
    # Diagonal veins
    pygame.draw.line(s, vein, (0, 8), (BS, 20), 1)
    pygame.draw.line(s, vein, (4, 0), (BS, 22), 1)
    pygame.draw.line(s, vein, (0, 20), (18, BS), 1)
    pygame.draw.line(s, (210, 207, 205), (BS - 8, 0), (BS, 12), 1)
    pygame.draw.rect(s, _darken(c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = RUSTICATED_QUOIN
    # if bid == RUSTICATED_QUOIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 20)
    lt = _lighter(c, 10)
    # Two large bosses
    for rx, ry, rw, rh in [(2, 2, BS - 4, BS // 2 - 2), (2, BS // 2 + 1, BS - 4, BS // 2 - 3)]:
        pygame.draw.rect(s, lt, (rx, ry, rw, rh))
        pygame.draw.rect(s, dk, (rx, ry, rw, rh), 2)
        pygame.draw.line(s, dk, (rx, ry + rh), (rx + rw, ry + rh), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = BICOLOR_MARBLE
    # if bid == BICOLOR_MARBLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    green = (62, 108, 72)
    # Diamond grid of green inlay
    cx2, cy2 = BS // 2, BS // 2
    pygame.draw.polygon(s, green, [(cx2, 2), (BS - 2, cy2), (cx2, BS - 2), (2, cy2)], 2)
    pygame.draw.polygon(s, green, [(cx2, 8), (BS - 8, cy2), (cx2, BS - 8), (8, cy2)], 1)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = PINK_GRANITE_BASE
    # if bid == PINK_GRANITE_BASE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    # Polished look: subtle sparkle flecks
    import random as _rnd
    _rng = _rnd.Random(710)
    for _ in range(18):
        fx, fy = _rng.randint(1, BS - 2), _rng.randint(1, BS - 2)
        col = _rng.choice([(215, 190, 185), (120, 100, 95), (240, 230, 228), (80, 60, 58)])
        s.set_at((fx, fy), col)
    pygame.draw.line(s, _lighter(c, 14), (2, 2), (BS - 3, 2), 1)
    pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
    surfs[bid] = s

    bid = BLIND_ARCH
    # if bid == BLIND_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    BS = BLOCK_SIZE
    # Wall with recessed blind arch
    recess = _darken(c, 14)
    cx2 = BS // 2
    arch_w, arch_top = 14, BS // 4
    pygame.draw.rect(s, recess, (cx2 - 7, arch_top + 7, 14, BS - arch_top - 9))
    pygame.draw.arc(s, recess, (cx2 - 7, arch_top, 14, 14), 0, math.pi, 14)
    pygame.draw.arc(s, dk, (cx2 - 7, arch_top, 14, 14), 0, math.pi, 2)
    pygame.draw.rect(s, dk, (cx2 - 7, arch_top + 7, 14, BS - arch_top - 9), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CONSOLE_CORNICE
    # if bid == CONSOLE_CORNICE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    # Top fascia band
    pygame.draw.rect(s, lt, (0, 0, BS, 6))
    pygame.draw.line(s, dk, (0, 6), (BS, 6), 1)
    # Three console brackets
    for bx2 in [3, BS // 2 - 4, BS - 12]:
        pygame.draw.rect(s, lt, (bx2, 6, 6, BS - 7))
        pygame.draw.line(s, dk, (bx2, 6), (bx2, BS - 1), 1)
        pygame.draw.line(s, dk, (bx2 + 6, 6), (bx2 + 6, BS - 1), 1)
        pygame.draw.line(s, dk, (bx2, BS - 1), (bx2 + 6, BS - 1), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CORINTHIAN_CAPITAL
    # if bid == CORINTHIAN_CAPITAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 20)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    # Abacus slab at top
    pygame.draw.rect(s, lt, (0, 0, BS, 5))
    pygame.draw.line(s, dk, (0, 5), (BS, 5), 1)
    # Acanthus leaf fan
    leaf = (172, 160, 130)
    for lx in [4, 10, 16, 22, 28]:
        pygame.draw.line(s, leaf, (BS // 2, BS - 2), (lx, 8), 2)
    for lx in [1, 7, 15, 23, 31]:
        pygame.draw.line(s, dk, (BS // 2, BS - 2), (lx, 12), 1)
    # Scrolls at corners
    pygame.draw.arc(s, dk, (0, 4, 8, 8), 0, math.pi, 2)
    pygame.draw.arc(s, dk, (BS - 8, 4, 8, 8), 0, math.pi, 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GIANT_PILASTER
    # if bid == GIANT_PILASTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 18)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    # Capital band top, base band bottom
    pygame.draw.rect(s, lt, (0, 0, BS, 4))
    pygame.draw.rect(s, lt, (0, BS - 4, BS, 4))
    pygame.draw.line(s, dk, (0, 4), (BS, 4), 1)
    pygame.draw.line(s, dk, (0, BS - 4), (BS, BS - 4), 1)
    # Flute grooves
    for fx in range(4, BS - 2, 5):
        pygame.draw.line(s, dk, (fx, 5), (fx, BS - 5), 1)
        pygame.draw.line(s, lt, (fx + 1, 5), (fx + 1, BS - 5), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = ENGAGED_COLUMN
    # if bid == ENGAGED_COLUMN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 8))
    dk = _darken(c, 22)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # Half-column drum on left
    pygame.draw.rect(s, c, (0, 2, cx2, BS - 4))
    pygame.draw.line(s, lt, (2, 2), (2, BS - 3), 1)
    for fx in range(5, cx2 - 2, 5):
        pygame.draw.line(s, dk, (fx, 2), (fx, BS - 3), 1)
    pygame.draw.line(s, dk, (cx2, 2), (cx2, BS - 3), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = ATLAS_FIGURE
    # if bid == ATLAS_FIGURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # Entablature load at top
    pygame.draw.rect(s, lt, (0, 0, BS, 5))
    pygame.draw.line(s, dk, (0, 5), (BS, 5), 1)
    # Simplified figure: head + torso + arms
    pygame.draw.circle(s, c, (cx2, 10), 4)
    pygame.draw.line(s, dk, (cx2 - 4, 8), (cx2 + 4, 8), 1)
    pygame.draw.rect(s, _darken(c, 12), (cx2 - 4, 14, 8, 10))
    pygame.draw.line(s, dk, (cx2 - 8, 8), (cx2 - 4, 16), 2)
    pygame.draw.line(s, dk, (cx2 + 8, 8), (cx2 + 4, 16), 2)
    pygame.draw.rect(s, _darken(c, 8), (cx2 - 3, 24, 6, BS - 26))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CARYATID_COLUMN
    # if bid == CARYATID_COLUMN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # Entablature at top
    pygame.draw.rect(s, lt, (0, 0, BS, 4))
    pygame.draw.line(s, dk, (0, 4), (BS, 4), 1)
    # Slender draped figure
    pygame.draw.circle(s, c, (cx2, 10), 3)
    pygame.draw.rect(s, _darken(c, 10), (cx2 - 3, 13, 6, 14))
    # Drapery folds
    for fold_y in range(14, 27, 3):
        pygame.draw.line(s, dk, (cx2 - 3, fold_y), (cx2 + 2, fold_y), 1)
    pygame.draw.rect(s, _darken(c, 8), (cx2 - 4, 27, 8, BS - 29))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = COMPOSITE_CAPITAL
    # if bid == COMPOSITE_CAPITAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 20)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    # Abacus top
    pygame.draw.rect(s, lt, (0, 0, BS, 4))
    pygame.draw.line(s, dk, (0, 4), (BS, 4), 1)
    # Ionic volutes at corners
    pygame.draw.arc(s, dk, (1, 3, 8, 8), -math.pi / 2, math.pi / 2, 2)
    pygame.draw.arc(s, dk, (BS - 9, 3, 8, 8), math.pi / 2, 3 * math.pi / 2, 2)
    # Acanthus leaves below volutes
    leaf = (172, 160, 130)
    for lx in [4, 9, 16, 23, 28]:
        pygame.draw.line(s, leaf, (BS // 2, BS - 2), (lx, 10), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = INTARSIA_PANEL
    # if bid == INTARSIA_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dark_wood = _darken(c, 30)
    lt = _lighter(c, 22)
    # Geometric intarsia: octagon-and-square
    cx2, cy2 = BS // 2, BS // 2
    pygame.draw.polygon(s, dark_wood, [(cx2, 2), (BS - 2, cy2), (cx2, BS - 2), (2, cy2)], 2)
    pygame.draw.rect(s, lt, (cx2 - 5, cy2 - 5, 10, 10))
    pygame.draw.rect(s, dark_wood, (cx2 - 5, cy2 - 5, 10, 10), 1)
    # Corner triangles
    pygame.draw.polygon(s, dark_wood, [(2, 2), (cx2, 2), (2, cy2)], 1)
    pygame.draw.polygon(s, dark_wood, [(BS - 2, 2), (cx2, 2), (BS - 2, cy2)], 1)
    pygame.draw.rect(s, _darken(c, 22), s.get_rect(), 1)
    surfs[bid] = s

    bid = STUDIOLO_WALL
    # if bid == STUDIOLO_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 24)
    lt = _lighter(c, 18)
    # Trompe-l'oeil cabinet: two doors with keyhole
    pygame.draw.rect(s, lt, (2, 2, BS // 2 - 3, BS - 4))
    pygame.draw.rect(s, lt, (BS // 2 + 1, 2, BS // 2 - 3, BS - 4))
    pygame.draw.rect(s, dk, (2, 2, BS // 2 - 3, BS - 4), 1)
    pygame.draw.rect(s, dk, (BS // 2 + 1, 2, BS // 2 - 3, BS - 4), 1)
    # Keyholes
    for kx in [BS // 4, 3 * BS // 4]:
        pygame.draw.circle(s, dk, (kx, BS // 2 - 2), 2)
        pygame.draw.rect(s, dk, (kx - 1, BS // 2, 2, 4))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GILT_LEATHER
    # if bid == GILT_LEATHER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 20)
    lt = _lighter(c, 22)
    # Embossed diamond grid with rosette dots
    for gy in range(0, BS, 8):
        for gx in range(0 if (gy // 8) % 2 == 0 else 4, BS, 8):
            pygame.draw.rect(s, dk, (gx, gy, 6, 6), 1)
            s.set_at((gx + 3, gy + 3), lt)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = FRESCO_LUNETTE
    # if bid == FRESCO_LUNETTE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    wall = BLOCKS[bid]["color"]
    s.fill(wall)
    sky = (155, 180, 212)
    plaster = _lighter(wall, 8)
    # Arch border
    pygame.draw.arc(s, _darken(wall, 18), (3, 2, BS - 6, BS), 0, math.pi, 3)
    # Sky fill inside arch
    pygame.draw.ellipse(s, sky, (5, 3, BS - 10, BS - 2))
    # Simple motif: stylised cloud/figure suggestion
    pygame.draw.ellipse(s, _lighter(sky, 18), (BS // 2 - 5, 8, 10, 6))
    pygame.draw.rect(s, _darken(wall, 18), s.get_rect(), 1)
    surfs[bid] = s

    bid = WAINSCOT_MARBLE
    # if bid == WAINSCOT_MARBLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    # Rose-pink marble with veining
    vein = (185, 155, 148)
    pygame.draw.line(s, vein, (0, 6), (BS, 14), 1)
    pygame.draw.line(s, vein, (0, 18), (BS, 26), 1)
    # Horizontal banding lines
    dk = _darken(c, 15)
    pygame.draw.line(s, dk, (0, 0), (BS, 0), 2)
    pygame.draw.line(s, dk, (0, BS - 1), (BS, BS - 1), 2)
    pygame.draw.line(s, dk, (0, BS // 2), (BS, BS // 2), 1)
    surfs[bid] = s

    bid = TAPESTRY_FRAME
    # if bid == TAPESTRY_FRAME
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 25)
    lt = _lighter(c, 22)
    inner = _darken(c, 35)
    # Frame border
    pygame.draw.rect(s, lt, (0, 0, BS, BS), 4)
    pygame.draw.rect(s, dk, (0, 0, BS, BS), 1)
    pygame.draw.rect(s, dk, (4, 4, BS - 8, BS - 8), 1)
    pygame.draw.rect(s, inner, (5, 5, BS - 10, BS - 10))
    # Corner rosettes
    for rx2, ry2 in [(2, 2), (BS - 4, 2), (2, BS - 4), (BS - 4, BS - 4)]:
        pygame.draw.circle(s, lt, (rx2, ry2), 2)
    surfs[bid] = s

    bid = LACUNAR_CEILING
    # if bid == LACUNAR_CEILING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 20)
    lt = _lighter(c, 10)
    deep = _darken(c, 38)
    # Four coffers in 2×2 grid
    for cx2, cy2 in [(BS // 4, BS // 4), (3 * BS // 4, BS // 4),
                      (BS // 4, 3 * BS // 4), (3 * BS // 4, 3 * BS // 4)]:
        hw = BS // 4 - 2
        pygame.draw.rect(s, deep, (cx2 - hw + 2, cy2 - hw + 2, hw * 2 - 4, hw * 2 - 4))
        pygame.draw.rect(s, dk, (cx2 - hw + 1, cy2 - hw + 1, hw * 2 - 2, hw * 2 - 2), 1)
        pygame.draw.rect(s, lt, (cx2 - hw, cy2 - hw, hw * 2, hw * 2), 1)
        pygame.draw.circle(s, lt, (cx2, cy2), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = BARREL_FRESCO
    # if bid == BARREL_FRESCO
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    BS = BLOCK_SIZE
    sky = BLOCKS[bid]["color"]
    s.fill(sky)
    gold = (195, 168, 80)
    lt = _lighter(sky, 18)
    # Curved vault ribs
    for ry in range(0, BS, 8):
        pygame.draw.line(s, _darken(sky, 14), (0, ry), (BS, ry + 4), 1)
    # Painted figure suggestion
    pygame.draw.ellipse(s, lt, (BS // 2 - 6, 6, 12, 8))
    pygame.draw.line(s, gold, (0, 0), (BS, 0), 3)
    pygame.draw.line(s, gold, (0, BS - 1), (BS, BS - 1), 3)
    pygame.draw.rect(s, gold, s.get_rect(), 1)
    surfs[bid] = s

    bid = GOLDEN_CEILING
    # if bid == GOLDEN_CEILING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 22)
    lt = _lighter(c, 22)
    deep = _darken(c, 38)
    # Gilded coffers
    for cx2, cy2 in [(BS // 4, BS // 4), (3 * BS // 4, BS // 4),
                      (BS // 4, 3 * BS // 4), (3 * BS // 4, 3 * BS // 4)]:
        hw = BS // 4 - 1
        pygame.draw.rect(s, deep, (cx2 - hw + 2, cy2 - hw + 2, hw * 2 - 4, hw * 2 - 4))
        pygame.draw.rect(s, lt, (cx2 - hw, cy2 - hw, hw * 2, hw * 2), 2)
        pygame.draw.circle(s, lt, (cx2, cy2), 2)
    # Gold grid lines
    pygame.draw.line(s, dk, (0, BS // 2), (BS, BS // 2), 1)
    pygame.draw.line(s, dk, (BS // 2, 0), (BS // 2, BS), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GROTESQUE_VAULT
    # if bid == GROTESQUE_VAULT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 22)
    lt = _lighter(c, 10)
    # Candelabra axis
    pygame.draw.line(s, dk, (BS // 2, 0), (BS // 2, BS), 1)
    pygame.draw.line(s, dk, (0, BS // 2), (BS, BS // 2), 1)
    # Grotesque curls at quadrant corners
    for ax, ay in [(BS // 4, BS // 4), (3 * BS // 4, BS // 4),
                    (BS // 4, 3 * BS // 4), (3 * BS // 4, 3 * BS // 4)]:
        pygame.draw.circle(s, dk, (ax, ay), 4, 1)
        pygame.draw.circle(s, lt, (ax, ay), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CUPOLA_OCULUS
    # if bid == CUPOLA_OCULUS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 20)
    lt = _lighter(c, 22)
    cx2, cy2 = BS // 2, BS // 2
    # Painted dome rings
    for r in range(14, 2, -4):
        pygame.draw.circle(s, _darken(c, (14 - r) * 2), (cx2, cy2), r, 1)
    # Central oculus light
    pygame.draw.circle(s, (240, 238, 232), (cx2, cy2), 5)
    pygame.draw.circle(s, lt, (cx2, cy2), 3)
    pygame.draw.circle(s, dk, (cx2, cy2), 14, 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = COSMATESQUE_FLOOR
    # if bid == COSMATESQUE_FLOOR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    red = (168, 52, 42)
    green = (52, 108, 62)
    gold = (195, 162, 58)
    dk = _darken(c, 18)
    cx2, cy2 = BS // 2, BS // 2
    # Central roundel
    pygame.draw.circle(s, red, (cx2, cy2), 8)
    pygame.draw.circle(s, dk, (cx2, cy2), 8, 1)
    # Corner triangles
    pygame.draw.polygon(s, green, [(0, 0), (10, 0), (0, 10)])
    pygame.draw.polygon(s, green, [(BS, 0), (BS - 10, 0), (BS, 10)])
    pygame.draw.polygon(s, green, [(0, BS), (10, BS), (0, BS - 10)])
    pygame.draw.polygon(s, green, [(BS, BS), (BS - 10, BS), (BS, BS - 10)])
    # Gold bands
    pygame.draw.line(s, gold, (0, cy2), (cx2 - 8, cy2), 2)
    pygame.draw.line(s, gold, (cx2 + 8, cy2), (BS, cy2), 2)
    pygame.draw.line(s, gold, (cx2, 0), (cx2, cy2 - 8), 2)
    pygame.draw.line(s, gold, (cx2, cy2 + 8), (cx2, BS), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = TERRAZZO_FLOOR_REN
    # if bid == TERRAZZO_FLOOR_REN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    import random as _rnd
    _rng = _rnd.Random(738)
    chips = [(168, 80, 58), (88, 128, 88), (48, 44, 40), (215, 210, 205), (140, 105, 78)]
    for _ in range(30):
        cx2, cy2 = _rng.randint(1, BS - 2), _rng.randint(1, BS - 2)
        col = _rng.choice(chips)
        sz = _rng.randint(1, 3)
        pygame.draw.rect(s, col, (cx2, cy2, sz, sz))
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = OPUS_ALEXANDRINUM
    # if bid == OPUS_ALEXANDRINUM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    light_stone = (198, 185, 180)
    dk = _darken(c, 18)
    cx2, cy2 = BS // 2, BS // 2
    # Concentric stone rings
    for r in range(14, 0, -4):
        col = c if (r // 4) % 2 == 0 else light_stone
        pygame.draw.circle(s, col, (cx2, cy2), r)
        pygame.draw.circle(s, dk, (cx2, cy2), r, 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MARBLE_MEDALLION_REN
    # if bid == MARBLE_MEDALLION_REN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 20)
    gold = (195, 165, 72)
    cx2, cy2 = BS // 2, BS // 2
    # Radiating sections
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        ex = int(cx2 + 14 * math.cos(rad))
        ey = int(cy2 + 14 * math.sin(rad))
        pygame.draw.line(s, dk, (cx2, cy2), (ex, ey), 1)
    pygame.draw.circle(s, gold, (cx2, cy2), 14, 2)
    pygame.draw.circle(s, _lighter(c, 12), (cx2, cy2), 6)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = PALACE_FLOOR_TILE
    # if bid == PALACE_FLOOR_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 16)
    lt = _lighter(c, 10)
    # Large format tile: single joint cross with chamfer corners
    pygame.draw.line(s, dk, (0, BS // 2), (BS, BS // 2), 1)
    pygame.draw.line(s, dk, (BS // 2, 0), (BS // 2, BS), 1)
    pygame.draw.line(s, lt, (2, 2), (BS - 2, 2), 1)
    pygame.draw.line(s, lt, (2, 2), (2, BS - 2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = PALACE_PORTAL
    # if bid == PALACE_PORTAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 22)
    lt = _lighter(c, 10)
    void = (22, 18, 14)
    cx2 = BS // 2
    arch_w = 10
    # Pilasters either side
    pygame.draw.rect(s, lt, (1, 4, 5, BS - 5))
    pygame.draw.rect(s, lt, (BS - 6, 4, 5, BS - 5))
    # Arch opening
    pygame.draw.rect(s, void, (cx2 - arch_w // 2, BS // 3, arch_w, 2 * BS // 3))
    pygame.draw.arc(s, void, (cx2 - arch_w // 2, BS // 3 - arch_w // 2, arch_w, arch_w), 0, math.pi)
    pygame.draw.arc(s, dk, (cx2 - arch_w // 2, BS // 3 - arch_w // 2, arch_w, arch_w), 0, math.pi, 2)
    # Keystone
    pygame.draw.polygon(s, lt, [(cx2 - 3, BS // 3 - 5), (cx2 + 3, BS // 3 - 5), (cx2, BS // 3 + 1)])
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = AEDICULE_FRAME
    # if bid == AEDICULE_FRAME
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    BS = BLOCK_SIZE
    dk = _darken(c, 22)
    lt = _lighter(c, 12)
    void = (22, 18, 14)
    cx2 = BS // 2
    # Pediment triangle at top
    pygame.draw.polygon(s, lt, [(cx2, 2), (2, 10), (BS - 2, 10)])
    pygame.draw.polygon(s, dk, [(cx2, 2), (2, 10), (BS - 2, 10)], 1)
    # Flanking pilasters
    pygame.draw.rect(s, lt, (2, 10, 4, BS - 12))
    pygame.draw.rect(s, lt, (BS - 6, 10, 4, BS - 12))
    # Central opening
    pygame.draw.rect(s, void, (cx2 - 6, 12, 12, BS - 14))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = THERMAL_WINDOW
    # if bid == THERMAL_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    glass = (165, 192, 220)
    dk = _darken(c, 22)
    cx2 = BS // 2
    half_h = BS // 2
    # Semicircular thermal window
    pygame.draw.ellipse(s, glass, (3, 3, BS - 6, half_h * 2 - 4))
    pygame.draw.ellipse(s, dk, (3, 3, BS - 6, half_h * 2 - 4), 2)
    # Three mullion dividers
    pygame.draw.line(s, dk, (cx2, 3), (cx2, BS // 2 + 5), 2)
    pygame.draw.line(s, dk, (cx2 - (BS // 4), 8), (cx2 - (BS // 4), BS // 2 + 3), 1)
    pygame.draw.line(s, dk, (cx2 + (BS // 4), 8), (cx2 + (BS // 4), BS // 2 + 3), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = BIFORA_WINDOW
    # if bid == BIFORA_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    glass = (165, 192, 220)
    dk = _darken(c, 22)
    q = BS // 4
    # Two pointed arch openings
    for wx2 in [q, 3 * q]:
        pygame.draw.rect(s, glass, (wx2 - 5, BS // 4, 10, BS // 2))
        pygame.draw.arc(s, glass, (wx2 - 5, BS // 4 - 6, 10, 12), 0, math.pi)
        pygame.draw.arc(s, dk, (wx2 - 5, BS // 4 - 6, 10, 12), 0, math.pi, 1)
        pygame.draw.rect(s, dk, (wx2 - 5, BS // 4, 10, BS // 2), 1)
    # Central column
    pygame.draw.rect(s, _lighter(c, 10), (BS // 2 - 2, BS // 4, 4, BS // 2))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = SERLIANA_WINDOW
    # if bid == SERLIANA_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    glass = (165, 192, 220)
    dk = _darken(c, 22)
    cx2 = BS // 2
    # Central arched opening (wider)
    pygame.draw.rect(s, glass, (cx2 - 8, BS // 4 + 2, 16, BS - BS // 4 - 4))
    pygame.draw.arc(s, glass, (cx2 - 8, BS // 4 - 6, 16, 16), 0, math.pi)
    pygame.draw.arc(s, dk, (cx2 - 8, BS // 4 - 6, 16, 16), 0, math.pi, 1)
    # Two side square lights
    for sx in [2, BS - 9]:
        pygame.draw.rect(s, glass, (sx, BS // 3, 7, BS - BS // 3 - 3))
        pygame.draw.rect(s, dk, (sx, BS // 3, 7, BS - BS // 3 - 3), 1)
    # Entablature band
    pygame.draw.line(s, dk, (0, BS // 4), (BS, BS // 4), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = PALAZZO_BALCONY
    # if bid == PALAZZO_BALCONY
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 12)
    # Projecting floor slab
    pygame.draw.rect(s, lt, (0, 0, BS, 6))
    pygame.draw.line(s, dk, (0, 6), (BS, 6), 1)
    # Baluster shapes
    for bx2 in range(3, BS - 2, 6):
        pygame.draw.line(s, dk, (bx2, 6), (bx2, BS - 6), 1)
        pygame.draw.circle(s, dk, (bx2, 12), 2, 1)
        pygame.draw.circle(s, dk, (bx2, BS - 12), 2, 1)
    # Top and bottom rails
    pygame.draw.line(s, dk, (0, 6), (BS, 6), 2)
    pygame.draw.line(s, dk, (0, BS - 6), (BS, BS - 6), 2)
    # Corbel brackets underneath
    pygame.draw.polygon(s, lt, [(2, BS - 6), (6, BS), (0, BS)])
    pygame.draw.polygon(s, lt, [(BS - 2, BS - 6), (BS - 6, BS), (BS, BS)])
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = ROMAN_ARCH_REN
    # if bid == ROMAN_ARCH_REN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 24)
    lt = _lighter(c, 10)
    void = (22, 18, 14)
    cx2 = BS // 2
    # Arch opening with voussoir lines
    pygame.draw.rect(s, void, (cx2 - 9, BS // 2, 18, BS // 2 + 1))
    pygame.draw.arc(s, void, (cx2 - 9, BS // 2 - 9, 18, 18), 0, math.pi)
    pygame.draw.arc(s, dk, (cx2 - 9, BS // 2 - 9, 18, 18), 0, math.pi, 2)
    # Voussoir wedge lines on arch extrados
    for ang_deg in range(20, 170, 25):
        rad = math.radians(ang_deg)
        ix = int(cx2 + 9 * math.cos(rad))
        iy = int(BS // 2 - 9 * math.sin(rad))
        ox = int(cx2 + 13 * math.cos(rad))
        oy = int(BS // 2 - 13 * math.sin(rad))
        pygame.draw.line(s, dk, (ix, iy), (ox, oy), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = BARREL_VAULT_COFFER
    # if bid == BARREL_VAULT_COFFER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 10)
    deep = _darken(c, 38)
    # Three coffers in a row with curved top suggestion
    for ci, cx2 in enumerate([BS // 6, BS // 2, 5 * BS // 6]):
        w, h = 7, BS - 6
        pygame.draw.rect(s, deep, (cx2 - w // 2 + 1, 4, w - 2, h - 2))
        pygame.draw.rect(s, dk, (cx2 - w // 2, 3, w, h), 1)
        pygame.draw.line(s, lt, (cx2 - w // 2, 3), (cx2 + w // 2, 3), 1)
    # Curved barrel indication
    pygame.draw.arc(s, _darken(c, 12), (1, 0, BS - 2, BS), 0, math.pi, 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = PENDENTIVE_BLOCK
    # if bid == PENDENTIVE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 20)
    deep = _darken(c, 35)
    lt = _lighter(c, 10)
    # Triangular pendentive: darker concave triangle in corner
    pygame.draw.polygon(s, deep, [(0, 0), (BS, 0), (0, BS)])
    pygame.draw.polygon(s, c, [(4, 4), (BS - 4, 4), (4, BS - 4)])
    # Curved line suggesting spherical triangle
    pygame.draw.arc(s, dk, (-BS // 2, -BS // 2, BS * 2, BS * 2), 0, math.pi / 2, 3)
    pygame.draw.polygon(s, dk, [(0, 0), (BS, 0), (0, BS)], 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GROIN_VAULT
    # if bid == GROIN_VAULT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 12)
    cx2, cy2 = BS // 2, BS // 2
    # Diagonal groin ribs
    pygame.draw.line(s, dk, (0, 0), (BS, BS), 2)
    pygame.draw.line(s, dk, (BS, 0), (0, BS), 2)
    pygame.draw.line(s, lt, (1, 1), (BS - 1, BS - 1), 1)
    pygame.draw.line(s, lt, (BS - 1, 1), (1, BS - 1), 1)
    # Boss at center
    pygame.draw.circle(s, lt, (cx2, cy2), 4)
    pygame.draw.circle(s, dk, (cx2, cy2), 4, 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = RENAISSANCE_MANTEL
    # if bid == RENAISSANCE_MANTEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 20)
    lt = _lighter(c, 12)
    black = (18, 14, 10)
    # Fireplace opening (dark rectangular void)
    pygame.draw.rect(s, black, (6, BS // 3, BS - 12, BS - BS // 3 - 2))
    # Pilasters either side of opening
    pygame.draw.rect(s, lt, (2, BS // 3, 4, BS - BS // 3 - 2))
    pygame.draw.rect(s, lt, (BS - 6, BS // 3, 4, BS - BS // 3 - 2))
    # Mantelshelf
    pygame.draw.rect(s, lt, (0, BS // 3 - 5, BS, 5))
    pygame.draw.line(s, dk, (0, BS // 3 - 5), (BS, BS // 3 - 5), 1)
    pygame.draw.line(s, dk, (0, BS // 3), (BS, BS // 3), 1)
    # Vein on mantelshelf
    pygame.draw.line(s, (195, 190, 188), (4, BS // 3 - 3), (BS - 4, BS // 3 - 2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CHIMNEY_BREAST_REN
    # if bid == CHIMNEY_BREAST_REN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 20)
    lt = _lighter(c, 10)
    # Projecting central breast (lighter tone)
    pygame.draw.rect(s, lt, (BS // 4, 0, BS // 2, BS))
    pygame.draw.line(s, dk, (BS // 4, 0), (BS // 4, BS), 1)
    pygame.draw.line(s, dk, (3 * BS // 4, 0), (3 * BS // 4, BS), 1)
    # Herringbone brick pattern in projection
    brick = _darken(lt, 18)
    for hy in range(2, BS - 2, 4):
        off = (hy // 4) % 2 * 4
        for hx in range(BS // 4 + off, 3 * BS // 4, 8):
            pygame.draw.line(s, brick, (hx, hy), (hx + 4, hy + 4), 1)
    # Cornice at top
    pygame.draw.rect(s, lt, (BS // 4 - 2, 0, BS // 2 + 4, 4))
    pygame.draw.line(s, dk, (BS // 4 - 2, 4), (3 * BS // 4 + 2, 4), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = PEDIMENTED_NICHE
    # if bid == PEDIMENTED_NICHE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 10)
    recess = _darken(c, 32)
    cx2 = BS // 2
    # Triangular pediment
    pygame.draw.polygon(s, lt, [(cx2, 2), (4, 10), (BS - 4, 10)])
    pygame.draw.polygon(s, dk, [(cx2, 2), (4, 10), (BS - 4, 10)], 1)
    # Niche recess
    pygame.draw.rect(s, recess, (cx2 - 8, 10, 16, BS - 12))
    pygame.draw.arc(s, recess, (cx2 - 8, 6, 16, 10), 0, math.pi)
    # Figure hint in niche
    pygame.draw.circle(s, _lighter(recess, 12), (cx2, 16), 3)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = SHELL_NICHE_REN
    # if bid == SHELL_NICHE_REN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 10)
    recess = _darken(c, 28)
    cx2 = BS // 2
    # Niche opening
    pygame.draw.rect(s, recess, (cx2 - 8, BS // 4, 16, 3 * BS // 4 - 2))
    # Scallop shell fan at top
    pygame.draw.semicircle(s, lt, (cx2, BS // 4), 8, 0) if hasattr(pygame.draw, 'semicircle') else pygame.draw.arc(s, lt, (cx2 - 8, BS // 4 - 8, 16, 16), 0, math.pi, 6)
    for ray in range(-3, 4):
        sx2 = cx2 + ray * 2
        pygame.draw.line(s, dk, (cx2, BS // 4), (sx2, BS // 4 - 7), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CARTOUCHE_REN
    # if bid == CARTOUCHE_REN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 12)
    cx2, cy2 = BS // 2, BS // 2
    # Oval cartouche with scroll edges
    pygame.draw.ellipse(s, lt, (cx2 - 10, cy2 - 12, 20, 24), 2)
    pygame.draw.ellipse(s, dk, (cx2 - 10, cy2 - 12, 20, 24), 1)
    # Scroll curls top and bottom
    pygame.draw.arc(s, dk, (cx2 - 4, cy2 - 15, 8, 6), 0, math.pi, 2)
    pygame.draw.arc(s, dk, (cx2 - 4, cy2 + 9, 8, 6), math.pi, 2 * math.pi, 2)
    # Border
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = PUTTI_FRIEZE
    # if bid == PUTTI_FRIEZE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 14)
    # Two simplified putti figures
    for px2 in [BS // 4, 3 * BS // 4]:
        # Head
        pygame.draw.circle(s, lt, (px2, BS // 2 - 6), 4)
        # Wings (arcs)
        pygame.draw.arc(s, _darken(c, 12), (px2 - 8, BS // 2 - 10, 6, 10), -math.pi / 4, math.pi / 2, 2)
        pygame.draw.arc(s, _darken(c, 12), (px2 + 2, BS // 2 - 10, 6, 10), math.pi / 2, math.pi + math.pi / 4, 2)
        # Body
        pygame.draw.ellipse(s, lt, (px2 - 3, BS // 2 - 2, 6, 8))
    # Garland swag below
    for gx2 in range(2, BS - 2, 4):
        gy2 = int(BS * 3 // 4 + 4 * math.sin(gx2 * math.pi / (BS - 4)))
        s.set_at((gx2, gy2), dk)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = FESTOON_PANEL
    # if bid == FESTOON_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 20)
    # Hanging swag curve
    for gx2 in range(0, BS):
        gy2 = int(BS // 3 + (BS // 3) * math.sin(gx2 * math.pi / BS))
        s.set_at((gx2, gy2), dk)
        if gx2 % 4 == 0:
            pygame.draw.circle(s, _darken(c, 14), (gx2, gy2), 2)
    # Tie ribbons at corners
    pygame.draw.line(s, dk, (4, 2), (4, BS // 3), 1)
    pygame.draw.line(s, dk, (BS - 4, 2), (BS - 4, BS // 3), 1)
    # Bow at center top
    pygame.draw.arc(s, dk, (BS // 2 - 5, 1, 5, 5), 0, math.pi, 2)
    pygame.draw.arc(s, dk, (BS // 2, 1, 5, 5), 0, math.pi, 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = TROPHY_PANEL_REN
    # if bid == TROPHY_PANEL_REN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 12)
    cx2 = BS // 2
    # Central oval shield
    pygame.draw.ellipse(s, lt, (cx2 - 7, BS // 2 - 8, 14, 16))
    pygame.draw.ellipse(s, dk, (cx2 - 7, BS // 2 - 8, 14, 16), 1)
    # Helmet at top
    pygame.draw.ellipse(s, lt, (cx2 - 5, 2, 10, 8))
    pygame.draw.line(s, dk, (cx2 - 5, 6), (cx2 + 5, 6), 1)
    # Crossed swords
    pygame.draw.line(s, dk, (4, 4), (BS - 4, BS - 4), 2)
    pygame.draw.line(s, dk, (BS - 4, 4), (4, BS - 4), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MEDALLION_PORTRAIT
    # if bid == MEDALLION_PORTRAIT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 14)
    cx2, cy2 = BS // 2, BS // 2
    # Carved frame ring with bead molding
    pygame.draw.circle(s, lt, (cx2, cy2), 13, 3)
    for ang in range(0, 360, 20):
        rad = math.radians(ang)
        bx2 = int(cx2 + 12 * math.cos(rad))
        by2 = int(cy2 + 12 * math.sin(rad))
        pygame.draw.circle(s, dk, (bx2, by2), 1)
    # Profile bust silhouette inside
    pygame.draw.ellipse(s, _darken(c, 18), (cx2 - 5, cy2 - 7, 9, 11))
    pygame.draw.circle(s, _darken(c, 16), (cx2, cy2 - 7), 4)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = LAUREL_FRIEZE
    # if bid == LAUREL_FRIEZE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    BS = BLOCK_SIZE
    s.fill(c)
    dk = _darken(c, 20)
    leaf_col = (95, 118, 72)
    berry_col = (145, 52, 42)
    # Border lines
    pygame.draw.line(s, dk, (0, 2), (BS, 2), 1)
    pygame.draw.line(s, dk, (0, BS - 2), (BS, BS - 2), 1)
    # Wavy stem
    for sx2 in range(0, BS):
        sy2 = int(BS // 2 + 3 * math.sin(sx2 * 2 * math.pi / BS))
        s.set_at((sx2, sy2), dk)
    # Leaves at intervals
    for lx in range(2, BS - 2, 6):
        ly = int(BS // 2 + 3 * math.sin(lx * 2 * math.pi / BS))
        pygame.draw.ellipse(s, leaf_col, (lx - 2, ly - 3, 4, 6))
    # Berries
    for bx2 in range(5, BS - 2, 12):
        by2 = int(BS // 2 + 3 * math.sin(bx2 * 2 * math.pi / BS))
        pygame.draw.circle(s, berry_col, (bx2, by2 - 4), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = QUARTZ_PILLAR
    # if bid == QUARTZ_PILLAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ONYX_INLAY
    # if bid == ONYX_INLAY
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 35)
    cx2, cy2 = BLOCK_SIZE // 2, BLOCK_SIZE // 2
    pygame.draw.polygon(s, lt, [(cx2, cy2-9),(cx2+9, cy2),(cx2, cy2+9),(cx2-9, cy2)], 2)
    pygame.draw.polygon(s, lt, [(cx2, cy2-4),(cx2+4, cy2),(cx2, cy2+4),(cx2-4, cy2)])
    pygame.draw.line(s, lt, (2, 2), (8, 4), 1)
    pygame.draw.line(s, lt, (2, 3), (6, 3), 1)
    pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
    surfs[bid] = s

    bid = WHITE_PLASTER_WALL
    # if bid == WHITE_PLASTER_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 12)
    pygame.draw.line(s, dk, (0, 10), (BLOCK_SIZE, 10), 1)
    pygame.draw.line(s, dk, (0, 21), (BLOCK_SIZE, 21), 1)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = CARVED_PLASTER
    # if bid == CARVED_PLASTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MUQARNAS_BLOCK
    # if bid == MUQARNAS_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MASHRABIYA
    # if bid == MASHRABIYA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_lighter(c, 25))
    for i in range(-BLOCK_SIZE, BLOCK_SIZE * 2, 7):
        pygame.draw.line(s, c, (i, 0), (i + BLOCK_SIZE, BLOCK_SIZE), 2)
        pygame.draw.line(s, c, (i, BLOCK_SIZE), (i + BLOCK_SIZE, 0), 2)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = ZELLIGE_TILE
    # if bid == ZELLIGE_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ARABESQUE_PANEL
    # if bid == ARABESQUE_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ADOBE_BRICK
    # if bid == ADOBE_BRICK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = SPANISH_ROOF_TILE
    # if bid == SPANISH_ROOF_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 30))
    lt = _lighter(c, 18)
    for tx in [0, 11, 22]:
        pygame.draw.ellipse(s, c,  (tx,  0, 10, BLOCK_SIZE))
        pygame.draw.line(s, lt, (tx+2, 2), (tx+2, BLOCK_SIZE-3), 1)
        pygame.draw.line(s, _darken(c, 25), (tx+9, 3), (tx+9, BLOCK_SIZE-3), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = WROUGHT_IRON_GRILLE
    # if bid == WROUGHT_IRON_GRILLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TALAVERA_TILE
    # if bid == TALAVERA_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = SALTILLO_TILE
    # if bid == SALTILLO_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = HALF_TIMBER_WALL
    # if bid == HALF_TIMBER_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    plaster = BLOCKS[bid]["color"]
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

    bid = ASHLAR_BLOCK
    # if bid == ASHLAR_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = GOTHIC_TRACERY
    # if bid == GOTHIC_TRACERY
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = FLUTED_COLUMN
    # if bid == FLUTED_COLUMN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CORNICE_BLOCK
    # if bid == CORNICE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ROSE_WINDOW
    # if bid == ROSE_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = HERRINGBONE_BRICK
    # if bid == HERRINGBONE_BRICK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BAROQUE_TRIM
    # if bid == BAROQUE_TRIM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TUDOR_BEAM
    # if bid == TUDOR_BEAM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = VENETIAN_FLOOR
    # if bid == VENETIAN_FLOOR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = FLEMISH_BRICK
    # if bid == FLEMISH_BRICK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
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

    bid = PILASTER
    # if bid == PILASTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c    = BLOCKS[bid]["color"]
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

    bid = DENTIL_TRIM
    # if bid == DENTIL_TRIM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = WATTLE_DAUB
    # if bid == WATTLE_DAUB
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = NORDIC_PLANK
    # if bid == NORDIC_PLANK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
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

    bid = MANSARD_SLATE
    # if bid == MANSARD_SLATE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ROMAN_MOSAIC
    # if bid == ROMAN_MOSAIC
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 25))
    palette = [(178, 162, 128), (200, 140,  80), (215, 195, 155), (145,  95,  60)]
    tsz = 4
    for ty in range(0, BLOCK_SIZE, tsz):
        for tx in range(0, BLOCK_SIZE, tsz):
            tc = palette[((tx//tsz)*3 + (ty//tsz)*2) % len(palette)]
            pygame.draw.rect(s, tc, (tx+1, ty+1, tsz-1, tsz-1))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = SETT_STONE
    # if bid == SETT_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ROMANESQUE_ARCH
    # if bid == ROMANESQUE_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = DARK_SLATE_ROOF
    # if bid == DARK_SLATE_ROOF
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = KEYSTONE
    # if bid == KEYSTONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
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

    bid = PLINTH_BLOCK
    # if bid == PLINTH_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = IRON_LANTERN
    # if bid == IRON_LANTERN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c    = BLOCKS[bid]["color"]
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

    bid = LIGHT_TRAP_BLOCK
    # if bid == LIGHT_TRAP_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    wood = (100, 72, 38)
    glass = (185, 218, 225)
    glow  = (200, 230, 80)
    s.fill(wood)
    # Glass cage sides
    pygame.draw.rect(s, glass, (4, 4, 24, 24))
    pygame.draw.rect(s, _darken(glass, 30), (4, 4, 24, 24), 1)
    # Lantern glow inside
    pygame.draw.circle(s, _lighter(glow, 20), (16, 16), 6)
    pygame.draw.circle(s, glow, (16, 16), 4)
    # Wooden corner posts
    for cx, cy in ((4, 4), (24, 4), (4, 24), (24, 24)):
        pygame.draw.rect(s, wood, (cx - 1, cy - 1, 3, 3))
    # Top hook
    pygame.draw.line(s, wood, (15, 0), (15, 4), 2)
    pygame.draw.line(s, wood, (13, 0), (18, 0), 2)
    surfs[bid] = s

    bid = SANDSTONE_ASHLAR
    # if bid == SANDSTONE_ASHLAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = GARGOYLE_BLOCK
    # if bid == GARGOYLE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c  = BLOCKS[bid]["color"]
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

    bid = OGEE_ARCH
    # if bid == OGEE_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = RUSTICATED_STONE
    # if bid == RUSTICATED_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CHEVRON_STONE
    # if bid == CHEVRON_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TRIGLYPH_PANEL
    # if bid == TRIGLYPH_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MARBLE_INLAY
    # if bid == MARBLE_INLAY
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BRICK_NOGGING
    # if bid == BRICK_NOGGING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PORTCULLIS_BLOCK
    # if bid == PORTCULLIS_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((22, 20, 18))
    iron = (62, 58, 54)
    lt   = (88, 82, 76)
    BS = BLOCK_SIZE
    # vertical bars with pointed bases
    for bx2 in [4, 10, 16, 22, 28]:
        pygame.draw.rect(s, iron, (bx2, 0, 3, BS-5))
        pygame.draw.polygon(s, iron, [(bx2, BS-5), (bx2+1, BS-1), (bx2+2, BS-5)])
        pygame.draw.line(s, lt, (bx2, 0), (bx2, BS-5), 1)
    # horizontal cross-rails
    for by2 in [6, 18]:
        pygame.draw.rect(s, iron, (1, by2, BS-2, 3))
        pygame.draw.line(s, lt, (1, by2), (BS-2, by2), 1)
    pygame.draw.rect(s, (40, 36, 32), s.get_rect(), 1)
    surfs[bid] = s

    bid = ARROW_LOOP
    # if bid == ARROW_LOOP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 35)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # thick wall — subtle block courses
    for gy in range(8, BS, 8):
        pygame.draw.line(s, dk, (0, gy), (BS, gy), 1)
    for gx, gy, gw, gh in [(2,8,14,6),(18,8,12,6),(3,16,12,6),(17,16,13,6)]:
        pygame.draw.line(s, lt, (gx, gy+1), (gx+gw, gy+1), 1)
    # arrow slit: narrow vertical + short horizontal (cross shape)
    pygame.draw.rect(s, (12, 10, 8), (cx2-1, 3, 3, BS-5))
    pygame.draw.rect(s, (12, 10, 8), (cx2-4, BS//2-1, 9, 3))
    # splay: slit widens on interior (left side)
    pygame.draw.polygon(s, _darken(c, 20),
        [(0, BS//2-5), (cx2-1, BS//2-1), (cx2-1, BS//2+2), (0, BS//2+6)])
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MACHICOLATION
    # if bid == MACHICOLATION
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    # main parapet body (upper 60%)
    pygame.draw.rect(s, c, (0, 0, BS, BS*3//5))
    pygame.draw.line(s, lt, (0, 1), (BS, 1), 1)
    # corbels projecting down
    for cx2 in [3, 13, 22]:
        pygame.draw.rect(s, c, (cx2, BS*3//5, 8, 6))
        pygame.draw.line(s, lt, (cx2, BS*3//5), (cx2+8, BS*3//5), 1)
    # drop holes between corbels (dark)
    for hx in [11, 20]:
        pygame.draw.rect(s, (18, 16, 14), (hx, BS*3//5, 3, BS*2//5))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = DRAWBRIDGE_PLANK
    # if bid == DRAWBRIDGE_PLANK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    wood  = BLOCKS[bid]["color"]
    dk_w  = _darken(wood, 28)
    lt_w  = _lighter(wood, 12)
    iron  = (48, 44, 40)
    BS = BLOCK_SIZE
    s.fill(wood)
    # plank grain lines (vertical)
    for gx in range(5, BS, 6):
        pygame.draw.line(s, dk_w, (gx, 0), (gx, BS), 1)
    for gx in range(2, BS, 6):
        pygame.draw.line(s, lt_w, (gx, 0), (gx, BS), 1)
    # iron strap bands (horizontal)
    for by2 in [5, BS//2-2, BS-8]:
        pygame.draw.rect(s, iron, (0, by2, BS, 4))
        pygame.draw.line(s, _lighter(iron, 15), (0, by2), (BS, by2), 1)
        # strap bolt heads
        for bx2 in [4, BS//2, BS-5]:
            pygame.draw.circle(s, _lighter(iron, 20), (bx2, by2+2), 2)
    pygame.draw.rect(s, dk_w, s.get_rect(), 1)
    surfs[bid] = s

    bid = ROUND_TOWER_WALL
    # if bid == ROUND_TOWER_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 28)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    # curved stone courses: slightly arcing mortar lines
    for row in range(4):
        gy = row * 8 + 4
        # arc the mortar line (concave to simulate looking at curve)
        pts = [(x2, gy + int(2 * math.sin(math.pi * x2 / BS))) for x2 in range(BS)]
        for i in range(len(pts)-1):
            pygame.draw.line(s, dk, pts[i], pts[i+1], 1)
    # vertical joints (staggered per row)
    for row in range(4):
        gy = row * 8
        offset = 8 if row % 2 else 0
        for gx in range(offset, BS, 16):
            pygame.draw.line(s, dk, (gx, gy), (gx, gy+8), 1)
    # subtle highlight per block
    pygame.draw.line(s, lt, (2, 2), (12, 2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CURTAIN_WALL
    # if bid == CURTAIN_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    mortar = _darken(c, 32)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    s.fill(mortar)
    # large regular ashlar courses
    for row, off in [(0, 0), (1, 9), (2, 0), (3, 9)]:
        gy = row * 8 + 1
        for col in range(-1, 3):
            bx2 = col * 18 + off
            bw = min(bx2 + 16, BS) - max(bx2, 0)
            if bw > 0:
                pygame.draw.rect(s, c, (max(bx2, 0), gy, bw, 7))
                pygame.draw.line(s, lt, (max(bx2, 0), gy), (max(bx2,0)+bw, gy), 1)
    pygame.draw.rect(s, mortar, s.get_rect(), 1)
    surfs[bid] = s

    bid = CORBEL_COURSE
    # if bid == CORBEL_COURSE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    # wall body
    pygame.draw.line(s, dk, (0, BS//2), (BS, BS//2), 1)
    # projecting corbels (four brackets)
    for cx2 in [2, 10, 18, 26]:
        # bracket profile: wider at bottom, angled face
        pts = [(cx2, BS//2), (cx2+6, BS//2), (cx2+5, BS-3), (cx2+1, BS-3)]
        pygame.draw.polygon(s, c, pts)
        pygame.draw.polygon(s, dk, pts, 1)
        pygame.draw.line(s, lt, (cx2, BS//2), (cx2+6, BS//2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = TOWER_CAP
    # if bid == TOWER_CAP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    slate = BLOCKS[bid]["color"]
    dk = _darken(slate, 25)
    lt = _lighter(slate, 18)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    s.fill(dk)
    # conical roof: horizontal slate courses narrowing to apex
    for row in range(8):
        inset = row * 2
        gy = row * 4
        w2 = BS - inset * 2
        if w2 > 0:
            c2 = slate if row % 2 == 0 else _darken(slate, 10)
            pygame.draw.rect(s, c2, (inset, gy, w2, 4))
            pygame.draw.line(s, lt, (inset, gy), (inset + w2, gy), 1)
    # apex finial
    pygame.draw.polygon(s, lt, [(cx2, 0), (cx2-2, 4), (cx2+2, 4)])
    surfs[bid] = s

    bid = GREAT_HALL_FLOOR
    # if bid == GREAT_HALL_FLOOR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    H = BS // 2
    # large 2×2 flag stones
    pygame.draw.line(s, dk, (H, 0), (H, BS), 2)
    pygame.draw.line(s, dk, (0, H), (BS, H), 2)
    # bevel highlight per slab
    for qx, qy in [(1,1), (H+1,1), (1,H+1), (H+1,H+1)]:
        pygame.draw.line(s, lt, (qx, qy), (qx+H-3, qy), 1)
        pygame.draw.line(s, lt, (qx, qy), (qx, qy+H-3), 1)
    # worn centre marks
    for qx, qy in [(H//2, H//2), (H+H//2, H//2), (H//2, H+H//2), (H+H//2, H+H//2)]:
        pygame.draw.circle(s, _darken(c, 10), (qx, qy), 2)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = DUNGEON_WALL
    # if bid == DUNGEON_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 35)
    lt = _lighter(c, 8)
    iron = (52, 48, 44)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    # rough irregular stone — uneven mortar lines
    for gy in [7, 15, 23]:
        offset = 3 if (gy // 8) % 2 else 0
        pygame.draw.line(s, dk, (0, gy), (BS, gy+1), 1)
        for gx in range(offset, BS, 12):
            pygame.draw.line(s, dk, (gx, gy-7), (gx+1, gy), 1)
    # iron ring staple
    pygame.draw.arc(s, iron, (cx2-5, cy2-4, 10, 8), 0, math.pi, 2)
    pygame.draw.rect(s, iron, (cx2-5, cy2, 3, 4))
    pygame.draw.rect(s, iron, (cx2+2, cy2, 3, 4))
    pygame.draw.line(s, _lighter(iron, 20), (cx2-4, cy2-4), (cx2+4, cy2-4), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CASTLE_FIREPLACE
    # if bid == CASTLE_FIREPLACE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # stone surround
    pygame.draw.rect(s, c, (2, 2, BS-4, BS-2))
    # arch opening
    pygame.draw.rect(s, (15, 12, 10), (6, 12, BS-12, BS-13))
    pygame.draw.arc(s, c, (5, 7, BS-10, 12), 0, math.pi, 4)
    pygame.draw.arc(s, lt, (7, 8, BS-14, 10), 0.1, math.pi-0.1, 1)
    # mantel shelf
    pygame.draw.rect(s, _lighter(c, 8), (0, 10, BS, 3))
    pygame.draw.line(s, lt, (0, 10), (BS, 10), 1)
    # ember glow at base
    pygame.draw.rect(s, (110, 45, 10), (8, BS-6, BS-16, 4))
    pygame.draw.rect(s, (180, 90, 20), (10, BS-5, 6, 2))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = HERALDIC_PANEL
    # if bid == HERALDIC_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    lt = _lighter(c, 16)
    gold = (190, 152, 42)
    BS = BLOCK_SIZE
    cx2, cy2 = BS//2, BS//2
    # shield outline (heater shield shape)
    shield = [(6,4),(BS-7,4),(BS-5,cy2),(cx2,BS-4),(7,cy2)]
    pygame.draw.polygon(s, c, shield)
    pygame.draw.polygon(s, dk, shield, 2)
    # quarterly division lines
    pygame.draw.line(s, dk, (cx2, 4), (cx2, BS-4), 1)
    pygame.draw.line(s, dk, (6, cy2), (BS-7, cy2), 1)
    # gold chevron on lower half
    pts = [(7, cy2+4), (cx2, BS-8), (BS-8, cy2+4)]
    pygame.draw.polygon(s, gold, pts, 2)
    # central boss
    pygame.draw.circle(s, gold, (cx2, cy2), 4)
    pygame.draw.circle(s, lt, (cx2, cy2), 2)
    surfs[bid] = s

    bid = WALL_WALK_FLOOR
    # if bid == WALL_WALK_FLOOR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 25)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    # paving flags with slight drainage groove
    pygame.draw.line(s, dk, (0, BS//2), (BS, BS//2), 1)
    for gx in [BS//3, BS*2//3]:
        pygame.draw.line(s, dk, (gx, 0), (gx, BS//2), 1)
    for gx in [BS//4, BS*3//4]:
        pygame.draw.line(s, dk, (gx, BS//2), (gx, BS), 1)
    # worn highlights
    for qx, qy, qw, qh in [(1,1,10,1),(BS//3+1,1,8,1),(1,BS//2+1,6,1),(BS//2+1,BS//2+1,10,1)]:
        pygame.draw.line(s, lt, (qx, qy), (qx+qw, qy), 1)
    # drainage groove
    pygame.draw.line(s, _darken(c, 18), (0, BS-3), (BS, BS-3), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CASTLE_GATE_ARCH
    # if bid == CASTLE_GATE_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 18))
    lt = _lighter(c, 10)
    dk = _darken(c, 35)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # stone voussoirs around arch
    for i in range(7):
        a1 = math.pi * i / 6
        a2 = math.pi * (i + 1) / 6
        pts = [
            (cx2+int(14*math.cos(math.pi-a1)), 18+int(14*math.sin(math.pi-a1))),
            (cx2+int(14*math.cos(math.pi-a2)), 18+int(14*math.sin(math.pi-a2))),
            (cx2+int(7 *math.cos(math.pi-a2)), 18+int(7 *math.sin(math.pi-a2))),
            (cx2+int(7 *math.cos(math.pi-a1)), 18+int(7 *math.sin(math.pi-a1))),
        ]
        c2 = c if i % 2 == 0 else _darken(c, 12)
        pygame.draw.polygon(s, c2, pts)
        pygame.draw.polygon(s, dk, pts, 1)
    # door passage (dark)
    pygame.draw.rect(s, (12, 10, 8), (cx2-7, 18, 14, BS-19))
    # iron studs on door posts
    for by2 in [20, 26]:
        for bx2 in [cx2-6, cx2+5]:
            pygame.draw.circle(s, (52, 48, 44), (bx2, by2), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = DRAWBRIDGE_CHAIN
    # if bid == DRAWBRIDGE_CHAIN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((28, 26, 24))
    iron = (65, 60, 55)
    lt   = (90, 84, 78)
    BS = BLOCK_SIZE
    # alternating horizontal and vertical oval chain links
    for i in range(5):
        cy2 = i * 7 + 3
        if i % 2 == 0:
            # horizontal link
            pygame.draw.ellipse(s, iron, (BS//2-7, cy2, 14, 5))
            pygame.draw.ellipse(s, lt,   (BS//2-6, cy2+1, 12, 3), 1)
        else:
            # vertical link
            for lx in [BS//2-4, BS//2+1]:
                pygame.draw.ellipse(s, iron, (lx, cy2-1, 5, 7))
                pygame.draw.ellipse(s, lt,   (lx+1, cy2, 3, 5), 1)
    surfs[bid] = s

    bid = DUNGEON_GRATE
    # if bid == DUNGEON_GRATE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill((35, 32, 28))
    iron = (55, 50, 46)
    lt   = (78, 72, 66)
    BS = BLOCK_SIZE
    # stone border
    pygame.draw.rect(s, (88, 82, 72), (0, 0, BS, 4))
    pygame.draw.rect(s, (88, 82, 72), (0, BS-4, BS, 4))
    pygame.draw.rect(s, (88, 82, 72), (0, 0, 4, BS))
    pygame.draw.rect(s, (88, 82, 72), (BS-4, 0, 4, BS))
    # iron bars vertical
    for bx2 in [6, 12, 18, 24]:
        pygame.draw.rect(s, iron, (bx2, 4, 3, BS-8))
        pygame.draw.line(s, lt, (bx2, 4), (bx2, BS-5), 1)
    # iron bars horizontal
    for by2 in [10, 18]:
        pygame.draw.rect(s, iron, (4, by2, BS-8, 3))
    # rivet crosses
    for bx2 in [7, 13, 19, 25]:
        for by2 in [11, 19]:
            pygame.draw.circle(s, lt, (bx2, by2), 2)
    surfs[bid] = s

    bid = MOAT_STONE
    # if bid == MOAT_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    algae = (48, 88, 52)
    lt = _lighter(c, 8)
    BS = BLOCK_SIZE
    # stone courses with dampness
    mortar = _darken(c, 40)
    for row, off in [(0,0),(1,7),(2,0),(3,7)]:
        gy = row * 8 + 1
        for col in range(-1, 3):
            bx2 = col * 16 + off
            bw = min(bx2+14, BS) - max(bx2, 0)
            if bw > 0:
                pygame.draw.rect(s, c, (max(bx2, 0), gy, bw, 7))
                pygame.draw.line(s, mortar, (max(bx2,0), gy+7), (max(bx2,0)+bw, gy+7), 1)
    # algae/moss patches
    for ax, ay, aw, ah in [(2,18,8,4),(14,22,6,3),(22,12,5,5),(1,5,4,3)]:
        pygame.draw.rect(s, algae, (ax, ay, aw, ah))
    # water seepage stain streaks
    for sx in [6, 15, 24]:
        pygame.draw.line(s, _darken(c, 22), (sx, 0), (sx+1, BS), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CHAPEL_STONE
    # if bid == CHAPEL_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 28)
    lt = _lighter(c, 16)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # pointed arch niche
    pygame.draw.polygon(s, _darken(c, 12),
        [(cx2-8, BS-4), (cx2-8, 14), (cx2, 6), (cx2+8, 14), (cx2+8, BS-4)])
    # lancet arch outline
    pygame.draw.line(s, dk, (cx2-8, BS-4), (cx2-8, 14), 1)
    pygame.draw.line(s, dk, (cx2+8, BS-4), (cx2+8, 14), 1)
    pygame.draw.line(s, dk, (cx2-8, 14), (cx2, 6), 1)
    pygame.draw.line(s, dk, (cx2+8, 14), (cx2, 6), 1)
    # cross within niche
    pygame.draw.rect(s, lt, (cx2-1, 10, 3, 12))
    pygame.draw.rect(s, lt, (cx2-4, 16, 9, 3))
    # stone block surround
    pygame.draw.rect(s, dk, (0, 0, 5, BS))
    pygame.draw.rect(s, dk, (BS-5, 0, 5, BS))
    pygame.draw.line(s, lt, (1, 1), (4, 1), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MURDER_HOLE
    # if bid == MURDER_HOLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 40)
    lt = _lighter(c, 8)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # stone ceiling block
    pygame.draw.rect(s, _darken(c, 15), (0, 0, BS, 10))
    pygame.draw.line(s, lt, (0, 1), (BS, 1), 1)
    # rectangular drop hole (dark void)
    pygame.draw.rect(s, (10, 8, 6), (cx2-5, 4, 10, BS-5))
    # stone edges around hole
    pygame.draw.rect(s, dk, (cx2-5, 4, 10, BS-5), 1)
    # depth shadow
    pygame.draw.rect(s, _darken(c, 25), (cx2-4, 5, 8, 4))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = GARDEROBE_CHUTE
    # if bid == GARDEROBE_CHUTE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 28)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    # wall face
    for gy in range(8, BS, 8):
        pygame.draw.line(s, dk, (0, gy), (BS, gy), 1)
    # projecting chute box (corbelled out from wall)
    chute_x = cx2 - 6
    pygame.draw.rect(s, _darken(c, 10), (chute_x, 6, 12, BS-10))
    pygame.draw.rect(s, dk, (chute_x, 6, 12, BS-10), 1)
    pygame.draw.line(s, lt, (chute_x, 6), (chute_x+12, 6), 1)
    # corbel brackets supporting chute
    for side, sign in [(chute_x-3, 1), (chute_x+12, -1)]:
        pts = [(side, 6), (side+sign*3, 6), (side+sign*3, 12), (side, 14)]
        pygame.draw.polygon(s, c, pts)
        pygame.draw.polygon(s, dk, pts, 1)
    # open bottom (dark hole)
    pygame.draw.rect(s, (15, 12, 10), (chute_x+1, BS-10, 10, 8))
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = CRENELLATION
    # if bid == CRENELLATION
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = FAN_VAULT
    # if bid == FAN_VAULT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ACANTHUS_PANEL
    # if bid == ACANTHUS_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PEBBLE_DASH
    # if bid == PEBBLE_DASH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    for px2, py2, pr in [(3,3,2),(8,7,3),(13,2,2),(20,5,3),(26,3,2),(5,12,3),
                         (11,15,2),(18,12,3),(25,14,2),(2,20,2),(8,24,3),(15,21,2),
                         (22,22,3),(28,19,2),(4,28,3),(12,29,2),(20,27,3),(27,29,2)]:
        pygame.draw.ellipse(s, dk, (px2-pr, py2-pr, pr*2+1, pr*2))
        pygame.draw.ellipse(s, _lighter(c, 10), (px2-pr+1, py2-pr, pr, pr))
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = ENCAUSTIC_TILE
    # if bid == ENCAUSTIC_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CHEQUERBOARD_MARBLE
    # if bid == CHEQUERBOARD_MARBLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = WROUGHT_IRON_BALUSTRADE
    # if bid == WROUGHT_IRON_BALUSTRADE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = OPUS_INCERTUM
    # if bid == OPUS_INCERTUM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = GROTESQUE_FRIEZE
    # if bid == GROTESQUE_FRIEZE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BARREL_VAULT
    # if bid == BARREL_VAULT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = POINTED_ARCH
    # if bid == POINTED_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ENGLISH_BOND
    # if bid == ENGLISH_BOND
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = RELIEF_PANEL
    # if bid == RELIEF_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = DIAGONAL_TILE
    # if bid == DIAGONAL_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = JAPANESE_SHOJI
    # if bid == JAPANESE_SHOJI
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    wood = (120, 88, 48)
    s.fill(c)
    pygame.draw.rect(s, wood, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
    for x2 in [10, 21]:
        pygame.draw.line(s, wood, (x2, 2), (x2, BLOCK_SIZE-3), 1)
    for y2 in [10, 21]:
        pygame.draw.line(s, wood, (2, y2), (BLOCK_SIZE-3, y2), 1)
    surfs[bid] = s

    bid = OTTOMAN_TILE
    # if bid == OTTOMAN_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = LEADLIGHT_WINDOW
    # if bid == LEADLIGHT_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TUDOR_ROSE
    # if bid == TUDOR_ROSE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = GREEK_KEY
    # if bid == GREEK_KEY
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 35)
    meander = [(0,2),(6,2),(6,0),(12,0),(12,6),(2,6),(2,4),(10,4),(10,2),(8,2),(8,8),(0,8)]
    for rep_x, rep_y in [(1,1),(1,17),(17,1),(17,17)]:
        pts = [(x+rep_x, y+rep_y) for x, y in meander]
        pygame.draw.lines(s, dk, False, pts, 2)
    pygame.draw.rect(s, _darken(c, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = VENETIAN_PLASTER
    # if bid == VENETIAN_PLASTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 12)
    dk = _darken(c, 8)
    for i in range(0, BLOCK_SIZE*2, 6):
        shade = lt if (i // 6) % 2 == 0 else dk
        pygame.draw.line(s, shade, (i - BLOCK_SIZE, 0), (i, BLOCK_SIZE), 1)
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = SCOTTISH_RUBBLE
    # if bid == SCOTTISH_RUBBLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ART_NOUVEAU_PANEL
    # if bid == ART_NOUVEAU_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = DUTCH_GABLE
    # if bid == DUTCH_GABLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STRIPED_ARCH
    # if bid == STRIPED_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TIMBER_TRUSS
    # if bid == TIMBER_TRUSS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = HEARTH_STONE
    # if bid == HEARTH_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = LINEN_FOLD
    # if bid == LINEN_FOLD
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PARQUET_FLOOR
    # if bid == PARQUET_FLOOR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = COFFERED_CEILING
    # if bid == COFFERED_CEILING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = OPUS_SIGNINUM
    # if bid == OPUS_SIGNINUM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    for tx2, ty2, ts in [(3,4,2),(7,8,3),(12,3,2),(18,6,3),(24,2,2),(28,7,3),
                         (2,14,3),(8,18,2),(14,13,3),(20,16,2),(26,13,3),
                         (5,23,2),(10,27,3),(16,22,2),(22,25,3),(29,20,2),
                         (1,29,3),(13,30,2),(20,29,3),(28,28,2)]:
        pygame.draw.rect(s, (230, 225, 215), (tx2, ty2, ts, ts))
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = WHITEWASHED_WALL
    # if bid == WHITEWASHED_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 12)
    for hy in [7, 15, 23]:
        pygame.draw.line(s, dk, (1, hy), (BLOCK_SIZE - 2, hy), 1)
    pygame.draw.rect(s, (80, 18, 15), (0, 0, BLOCK_SIZE, 4))
    pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
    surfs[bid] = s

    bid = MONASTERY_ROOF
    # if bid == MONASTERY_ROOF
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MANI_STONE
    # if bid == MANI_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PRAYER_FLAG_BLOCK
    # if bid == PRAYER_FLAG_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.line(s, (80, 60, 40), (0, 8), (BLOCK_SIZE, 8), 1)
    for i, fc in enumerate([(60, 100, 175), (230, 225, 210), (180, 35, 30),
                            (45, 135, 60), (200, 175, 30)]):
        fx2 = i * 6 + 1
        pygame.draw.rect(s, fc, (fx2, 9, 5, 8))
        pygame.draw.rect(s, _darken(fc, 20), (fx2, 9, 5, 8), 1)
    surfs[bid] = s

    bid = GLAZED_ROOF_TILE
    # if bid == GLAZED_ROOF_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = LATTICE_SCREEN
    # if bid == LATTICE_SCREEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MOON_GATE
    # if bid == MOON_GATE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PAINTED_BEAM
    # if bid == PAINTED_BEAM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = DOUGONG
    # if bid == DOUGONG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CERAMIC_PLANTER
    # if bid == CERAMIC_PLANTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STONE_LANTERN
    # if bid == STONE_LANTERN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = LACQUER_PANEL
    # if bid == LACQUER_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PAPER_LANTERN
    # if bid == PAPER_LANTERN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = DRAGON_TILE
    # if bid == DRAGON_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = HAN_BRICK
    # if bid == HAN_BRICK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PAVILION_FLOOR
    # if bid == PAVILION_FLOOR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BAMBOO_SCREEN
    # if bid == BAMBOO_SCREEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CLOUD_MOTIF
    # if bid == CLOUD_MOTIF
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = COIN_TILE
    # if bid == COIN_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BLUE_WHITE_TILE
    # if bid == BLUE_WHITE_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = GARDEN_ROCK
    # if bid == GARDEN_ROCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STEPPED_WALL
    # if bid == STEPPED_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PAGODA_EAVE
    # if bid == PAGODA_EAVE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CINNABAR_WALL
    # if bid == CINNABAR_WALL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MUGHAL_ARCH
    # if bid == MUGHAL_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PIETRA_DURA
    # if bid == PIETRA_DURA
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = EGYPTIAN_FRIEZE
    # if bid == EGYPTIAN_FRIEZE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = SANDSTONE_COLUMN
    # if bid == SANDSTONE_COLUMN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = AZTEC_SUNSTONE
    # if bid == AZTEC_SUNSTONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MAYA_RELIEF
    # if bid == MAYA_RELIEF
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = VIKING_CARVING
    # if bid == VIKING_CARVING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = RUNE_STONE
    # if bid == RUNE_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PERSIAN_IWAN
    # if bid == PERSIAN_IWAN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = KILIM_TILE
    # if bid == KILIM_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = AFRICAN_MUD_BRICK
    # if bid == AFRICAN_MUD_BRICK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = KENTE_PANEL
    # if bid == KENTE_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = WAT_FINIAL
    # if bid == WAT_FINIAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = KHMER_STONE
    # if bid == KHMER_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = HANJI_SCREEN
    # if bid == HANJI_SCREEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = DANCHEONG
    # if bid == DANCHEONG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ART_DECO_PANEL
    # if bid == ART_DECO_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = OBSIDIAN_CUT
    # if bid == OBSIDIAN_CUT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = OTTOMAN_ARCH
    # if bid == OTTOMAN_ARCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = LOTUS_CAPITAL
    # if bid == LOTUS_CAPITAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = AZULEJO_TILE
    # if bid == AZULEJO_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MANUELINE_PANEL
    # if bid == MANUELINE_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TORII_PANEL
    # if bid == TORII_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = INCA_ASHLAR
    # if bid == INCA_ASHLAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = RUSSIAN_KOKOSHNIK
    # if bid == RUSSIAN_KOKOSHNIK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ONION_DOME_TILE
    # if bid == ONION_DOME_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = GEORGIAN_FANLIGHT
    # if bid == GEORGIAN_FANLIGHT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PALLADIAN_WINDOW
    # if bid == PALLADIAN_WINDOW
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = STAVE_PLANK
    # if bid == STAVE_PLANK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = IONIC_CAPITAL
    # if bid == IONIC_CAPITAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MOORISH_STAR_TILE
    # if bid == MOORISH_STAR_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = CRAFTSMAN_PANEL
    # if bid == CRAFTSMAN_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BRUTALIST_PANEL
    # if bid == BRUTALIST_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = METOPE
    # if bid == METOPE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ARMENIAN_KHACHKAR
    # if bid == ARMENIAN_KHACHKAR
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BENIN_RELIEF
    # if bid == BENIN_RELIEF
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MAORI_CARVING
    # if bid == MAORI_CARVING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MUGHAL_JALI
    # if bid == MUGHAL_JALI
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PERSIAN_TILE
    # if bid == PERSIAN_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = SWISS_CHALET
    # if bid == SWISS_CHALET
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ANDEAN_TEXTILE
    # if bid == ANDEAN_TEXTILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BAROQUE_ORNAMENT
    # if bid == BAROQUE_ORNAMENT
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = POLYNESIAN_CARVED
    # if bid == POLYNESIAN_CARVED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MOORISH_COLUMN
    # if bid == MOORISH_COLUMN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = PORTUGUESE_CORK
    # if bid == PORTUGUESE_CORK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = MCM_BREEZE_BLOCK
    # if bid == MCM_BREEZE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 28)
    void = (16, 14, 11)
    BS = BLOCK_SIZE
    cx2, cy2 = BS // 2, BS // 2
    pygame.draw.rect(s, void, (4, cy2 - 4, BS - 8, 8))
    pygame.draw.rect(s, void, (cx2 - 4, 4, 8, BS - 8))
    pygame.draw.rect(s, _darken(c, 8), (cx2 - 2, cy2 - 2, 4, 4))
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = MCM_BOARD_BATTEN
    # if bid == MCM_BOARD_BATTEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 25)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    for bx in (10, 21):
        pygame.draw.rect(s, dk, (bx, 0, 2, BS))
        pygame.draw.line(s, lt, (bx, 0), (bx, BS), 1)
    for gy in range(7, BS, 7):
        pygame.draw.line(s, _darken(c, 8), (0, gy), (BS, gy), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MCM_WALNUT_PANEL
    # if bid == MCM_WALNUT_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 14)
    BS = BLOCK_SIZE
    for pi in range(4):
        py = pi * (BS // 4)
        col = _darken(c, 8) if pi % 2 else c
        pygame.draw.rect(s, col, (0, py, BS, BS // 4 - 1))
        for gy in range(py + 2, py + BS // 4 - 2, 3):
            pygame.draw.line(s, _darken(col, 10), (1, gy), (BS - 1, gy), 1)
        pygame.draw.line(s, dk, (0, py), (BS, py), 1)
        pygame.draw.line(s, lt, (0, py + 1), (BS, py + 1), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MCM_TEAK_PANEL
    # if bid == MCM_TEAK_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 20)
    lt = _lighter(c, 10)
    BS = BLOCK_SIZE
    ph = BS // 5
    for pi in range(5):
        py = pi * ph
        col = _lighter(c, 6) if pi % 2 else c
        pygame.draw.rect(s, col, (0, py, BS, ph - 1))
        for gy in range(py + 2, py + ph - 1, 2):
            pygame.draw.line(s, _darken(col, 8), (1, gy), (BS - 1, gy), 1)
        pygame.draw.line(s, dk, (0, py + ph - 1), (BS, py + ph - 1), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MCM_ROMAN_BRICK
    # if bid == MCM_ROMAN_BRICK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    mortar_c = (200, 190, 175)
    s.fill(mortar_c)
    dk = _darken(c, 18)
    BS = BLOCK_SIZE
    rh = 6
    for row in range(BS // rh + 1):
        oy = row * rh
        ox = (row % 2) * 9
        for bx in range(-9, BS + 9, 18):
            pygame.draw.rect(s, c, (bx + ox, oy, 16, 4))
            pygame.draw.rect(s, dk, (bx + ox, oy, 16, 4), 1)
    pygame.draw.rect(s, _darken(mortar_c, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = TERRAZZO_FLOOR_MCM
    # if bid == TERRAZZO_FLOOR_MCM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    chips = [
        ((185, 68, 52), 4, 3, 2), ((65, 118, 165), 12, 8, 2), ((215, 172, 48), 22, 4, 1),
        ((72, 145, 82), 7, 16, 2), ((155, 55, 45), 18, 20, 2), ((62, 115, 160), 28, 12, 1),
        ((210, 168, 48), 5, 26, 1), ((72, 140, 80), 25, 27, 2), ((150, 52, 42), 14, 3, 1),
        ((65, 118, 162), 20, 18, 2), ((185, 68, 52), 27, 22, 1), ((70, 140, 78), 3, 22, 1),
        ((152, 50, 42), 16, 28, 2), ((210, 165, 45), 11, 25, 2), ((62, 112, 155), 24, 29, 1),
        ((215, 172, 50), 29, 5, 2), ((68, 135, 76), 8, 9, 1),
    ]
    for cc, cx3, cy3, sz in chips:
        pygame.draw.rect(s, cc, (cx3, cy3, sz, sz))
    pygame.draw.rect(s, _darken(c, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = TRAVERTINE_FLOOR_MCM
    # if bid == TRAVERTINE_FLOOR_MCM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 14)
    BS = BLOCK_SIZE
    for gy in range(4, BS, 5):
        pygame.draw.line(s, _darken(c, 6), (0, gy), (BS, gy), 1)
    for vx, vy in ((4, 4), (10, 12), (18, 7), (24, 18), (6, 22), (20, 26), (28, 10), (8, 28), (14, 2)):
        pygame.draw.rect(s, _darken(c, 28), (vx, vy, 2, 1))
    pygame.draw.line(s, dk, (BS // 2, 0), (BS // 2, BS), 1)
    pygame.draw.line(s, dk, (0, BS // 2), (BS, BS // 2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = FLAGSTONE_PATIO
    # if bid == FLAGSTONE_PATIO
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    mortar_c = _darken(c, 25)
    s.fill(mortar_c)
    lt = _lighter(c, 8)
    BS = BLOCK_SIZE
    stones = [
        [(1, 1), (14, 1), (15, 13), (1, 14)],
        [(17, 1), (BS - 1, 2), (BS - 1, 13), (16, 14)],
        [(1, 16), (13, 15), (12, BS - 1), (1, BS - 1)],
        [(15, 16), (BS - 1, 15), (BS - 1, BS - 1), (14, BS - 1)],
    ]
    for pts in stones:
        pygame.draw.polygon(s, c, pts)
        pygame.draw.polygon(s, lt, pts, 1)
    pygame.draw.rect(s, mortar_c, s.get_rect(), 1)
    surfs[bid] = s

    bid = MCM_PARQUET
    # if bid == MCM_PARQUET
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 25)
    lt = _lighter(c, 10)
    alt = _darken(c, 12)
    BS = BLOCK_SIZE
    for i in range(7):
        x1 = i * 5
        pygame.draw.line(s, dk, (x1, 0), (x1 + BS // 2, BS // 2), 3)
        pygame.draw.line(s, lt, (x1 + 1, 0), (x1 + BS // 2 + 1, BS // 2), 1)
    for i in range(7):
        x1 = i * 5
        pygame.draw.line(s, alt, (BS - x1, BS // 2), (BS - x1 - BS // 2, BS), 3)
        pygame.draw.line(s, dk, (BS - x1 - 1, BS // 2), (BS - x1 - BS // 2 - 1, BS), 1)
    pygame.draw.line(s, dk, (0, BS // 2), (BS, BS // 2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = PLATE_GLASS_PANEL
    # if bid == PLATE_GLASS_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 22)
    lt = _lighter(c, 35)
    BS = BLOCK_SIZE
    pygame.draw.polygon(s, lt, [(2, 2), (BS - 9, 2), (2, BS - 9)])
    pygame.draw.rect(s, dk, s.get_rect(), 3)
    pygame.draw.line(s, lt, (3, 3), (BS - 4, 3), 1)
    surfs[bid] = s

    bid = TINTED_GLASS_PANEL
    # if bid == TINTED_GLASS_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 28)
    dk = _darken(c, 15)
    BS = BLOCK_SIZE
    pygame.draw.polygon(s, _lighter(c, 16), [(2, 2), (BS // 3, 2), (2, BS // 3)])
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    pygame.draw.line(s, lt, (3, 3), (BS // 3, 3), 1)
    surfs[bid] = s

    bid = RIBBED_GLASS_MCM
    # if bid == RIBBED_GLASS_MCM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 18)
    lt = _lighter(c, 25)
    BS = BLOCK_SIZE
    for gx in range(0, BS, 4):
        pygame.draw.line(s, lt, (gx, 0), (gx, BS), 1)
        pygame.draw.line(s, dk, (gx + 2, 0), (gx + 2, BS), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = BRASS_TRIM_PANEL
    # if bid == BRASS_TRIM_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 28)
    lt = _lighter(c, 28)
    BS = BLOCK_SIZE
    for by in range(0, BS, 6):
        pygame.draw.line(s, lt, (0, by), (BS, by), 1)
        pygame.draw.line(s, dk, (0, by + 5), (BS, by + 5), 1)
    pygame.draw.line(s, dk, (BS // 2, 0), (BS // 2, BS), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = COPPER_SCREEN_MCM
    # if bid == COPPER_SCREEN_MCM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 28)
    hole = _darken(c, 45)
    BS = BLOCK_SIZE
    for gy in range(5, BS, 8):
        for gx in range(5, BS, 8):
            pygame.draw.rect(s, hole, (gx, gy, 3, 3))
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = ANODIZED_ALUMINUM
    # if bid == ANODIZED_ALUMINUM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 14)
    lt = _lighter(c, 18)
    BS = BLOCK_SIZE
    for gy in range(0, BS, 2):
        pygame.draw.line(s, lt if gy % 4 == 0 else dk, (0, gy), (BS, gy), 1)
    pygame.draw.rect(s, _darken(c, 30), s.get_rect(), 2)
    surfs[bid] = s

    bid = RATTAN_SCREEN_MCM
    # if bid == RATTAN_SCREEN_MCM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 10))
    dk = _darken(c, 32)
    lt = _lighter(c, 18)
    BS = BLOCK_SIZE
    for gx in range(0, BS, 5):
        pygame.draw.line(s, lt, (gx, 0), (gx, BS), 2)
    for gy in range(0, BS, 5):
        pygame.draw.line(s, dk, (0, gy), (BS, gy), 2)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = SPLIT_BAMBOO_PANEL
    # if bid == SPLIT_BAMBOO_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 28)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    for gx in range(0, BS, 6):
        col = _lighter(c, 8) if (gx // 6) % 2 else _darken(c, 5)
        pygame.draw.rect(s, col, (gx, 0, 5, BS))
        pygame.draw.line(s, dk, (gx, 0), (gx, BS), 1)
    for gy in (8, 20):
        pygame.draw.line(s, dk, (0, gy), (BS, gy), 2)
        pygame.draw.line(s, lt, (0, gy - 1), (BS, gy - 1), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = MCM_TONGUE_GROOVE
    # if bid == MCM_TONGUE_GROOVE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 20)
    lt = _lighter(c, 15)
    shad = _darken(c, 35)
    BS = BLOCK_SIZE
    bh = BS // 4
    for bi in range(4):
        by = bi * bh
        col = _darken(c, 6) if bi % 2 else c
        pygame.draw.rect(s, col, (0, by, BS, bh - 1))
        for gy in range(by + 3, by + bh - 2, 4):
            pygame.draw.line(s, _darken(col, 8), (1, gy), (BS - 1, gy), 1)
        pygame.draw.line(s, shad, (0, by + bh - 1), (BS, by + bh - 1), 1)
        pygame.draw.line(s, lt, (0, by), (BS, by), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = BUTTERFLY_BEAM
    # if bid == BUTTERFLY_BEAM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 8))
    dk = _darken(c, 30)
    lt = _lighter(c, 20)
    BS = BLOCK_SIZE
    cx2 = BS // 2
    pygame.draw.polygon(s, c, [(0, 0), (cx2, BS - 4), (cx2 + 4, BS - 4), (6, 0)])
    pygame.draw.polygon(s, dk, [(0, 0), (cx2, BS - 4), (cx2 + 4, BS - 4), (6, 0)], 1)
    pygame.draw.line(s, lt, (1, 1), (cx2 - 1, BS - 5), 1)
    pygame.draw.polygon(s, _darken(c, 10), [(cx2, BS - 4), (BS, 0), (BS - 6, 0), (cx2 + 4, BS - 4)])
    pygame.draw.polygon(s, dk, [(cx2, BS - 4), (BS, 0), (BS - 6, 0), (cx2 + 4, BS - 4)], 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = STARBURST_PANEL
    # if bid == STARBURST_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    gold = (195, 162, 72)
    BS = BLOCK_SIZE
    cx2, cy2 = BS // 2, BS // 2
    for i in range(12):
        a = math.pi * 2 * i / 12
        length = 13 if i % 3 == 0 else 10
        ex = cx2 + int(length * math.cos(a))
        ey = cy2 + int(length * math.sin(a))
        color = gold if i % 3 == 0 else dk
        width = 2 if i % 3 == 0 else 1
        pygame.draw.line(s, color, (cx2, cy2), (ex, ey), width)
    pygame.draw.circle(s, gold, (cx2, cy2), 3)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    bid = STONE_BRIDGE
    # if bid == STONE_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    dk = _darken(c, 25)
    lt = _lighter(c, 12)
    BS = BLOCK_SIZE
    s.fill(c)
    # stone slab courses — horizontal mortar lines across the bridge deck
    for gy in range(5, BS, 7):
        pygame.draw.line(s, dk, (0, gy), (BS, gy), 1)
    # irregular stone block joints — vertical lines staggered per row
    for row in range(BS // 7 + 1):
        gy = row * 7
        offset = (row % 2) * 5
        for gx in range(offset, BS, 9):
            pygame.draw.line(s, dk, (gx, gy), (gx, min(gy + 7, BS)), 1)
    # subtle highlight on each stone face
    for row in range(BS // 7 + 1):
        gy = row * 7 + 1
        for gx in range((row % 2) * 5, BS, 9):
            if gx + 1 < BS and gy + 1 < BS:
                pygame.draw.line(s, lt, (gx + 1, gy), (gx + 7, gy), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    # --- TIMBER BRIDGE: log-and-plank deck, warm brown, boreal/birch ---
    bid = TIMBER_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]          # (110, 75, 42)
    dk = _darken(c, 30)
    lt = _lighter(c, 18)
    grain = _darken(c, 15)
    BS = BLOCK_SIZE
    s.fill(c)
    # horizontal plank lines
    for gy in range(4, BS, 6):
        pygame.draw.line(s, dk, (0, gy), (BS, gy), 1)
    # vertical wood-grain streaks
    for gx in range(0, BS, 10):
        offset = (gx // 10) % 2
        pygame.draw.line(s, grain, (gx + offset, 0), (gx + offset, BS), 1)
    # small knot circles on alternating planks
    for row, kx in enumerate(range(3, BS - 3, 10)):
        ky = 2 + (row % 3) * 6 + 1
        if ky < BS - 2:
            pygame.draw.circle(s, dk, (kx + 2, ky), 2, 1)
    # bright top-edge highlight on each plank
    for gy in range(0, BS, 6):
        pygame.draw.line(s, lt, (1, gy), (BS - 1, gy), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    # --- MOSSY BRIDGE: cracked weathered stone with green moss, wetland/swamp ---
    bid = MOSSY_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]          # (78, 95, 72)
    dk = _darken(c, 28)
    lt = _lighter(c, 14)
    moss = (90, 118, 68)
    BS = BLOCK_SIZE
    s.fill(c)
    # irregular stone courses (shorter slabs than STONE_BRIDGE)
    for gy in range(5, BS, 6):
        pygame.draw.line(s, dk, (0, gy), (BS, gy), 1)
    # staggered vertical joints
    for row in range(BS // 6 + 1):
        gy = row * 6
        offset = (row % 2) * 4
        for gx in range(offset, BS, 8):
            pygame.draw.line(s, dk, (gx, gy), (gx, min(gy + 6, BS)), 1)
    # moss patches across upper half
    _rnd_m = _rnd.Random(0xB4057)
    for _ in range(8):
        mx = _rnd_m.randint(1, BS - 4)
        my = _rnd_m.randint(1, BS // 2)
        mw = _rnd_m.randint(2, 5)
        mh = _rnd_m.randint(1, 3)
        pygame.draw.rect(s, moss, (mx, my, mw, mh))
    # subtle stone-face highlight
    for row in range(BS // 6 + 1):
        gy = row * 6 + 1
        for gx in range((row % 2) * 4, BS, 8):
            if gx + 1 < BS and gy < BS:
                pygame.draw.line(s, lt, (gx + 1, gy), (gx + 6, gy), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    # --- SANDSTONE BRIDGE: warm banded sandstone, jungle/tropical ---
    bid = SANDSTONE_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]          # (192, 158, 100)
    dk = _darken(c, 28)
    lt = _lighter(c, 16)
    band_hi = _lighter(c, 8)
    band_lo = _darken(c, 12)
    BS = BLOCK_SIZE
    s.fill(c)
    # sedimentary banding — alternating slightly lighter/darker horizontal strata
    band_h = 4
    for row in range(BS // band_h + 1):
        gy = row * band_h
        col = band_hi if row % 2 == 0 else band_lo
        pygame.draw.line(s, col, (0, gy), (BS, gy), band_h - 1)
    # faint vertical block joints for carved-stone look
    for row in range(BS // band_h + 1):
        gy = row * band_h
        offset = (row % 3) * 4
        for gx in range(offset, BS, 11):
            pygame.draw.line(s, dk, (gx, gy), (gx, min(gy + band_h, BS)), 1)
    # warm highlight on top edge of each band
    for row in range(BS // band_h + 1):
        gy = row * band_h
        pygame.draw.line(s, lt, (1, gy), (BS - 1, gy), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    # --- BRICK BRIDGE: red-brick running bond with mortar, rolling-hills ---
    bid = BRICK_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]          # (168, 82, 52)
    mortar = _darken(c, 35)
    lt = _lighter(c, 18)
    face = _lighter(c, 6)
    BS = BLOCK_SIZE
    s.fill(mortar)
    brick_h = 5
    brick_w = 9
    for row in range(BS // brick_h + 1):
        gy = row * brick_h
        offset = (row % 2) * (brick_w // 2)
        for gx in range(-brick_w + offset, BS + brick_w, brick_w + 1):
            bx0 = gx + 1
            by0 = gy + 1
            bw  = brick_w - 1
            bh  = brick_h - 1
            if bx0 < BS and by0 < BS:
                pygame.draw.rect(s, face, (bx0, by0, min(bw, BS - bx0), min(bh, BS - by0)))
                # top highlight
                pygame.draw.line(s, lt, (bx0, by0), (min(bx0 + bw - 1, BS - 1), by0), 1)
    pygame.draw.rect(s, mortar, s.get_rect(), 1)
    surfs[bid] = s

    # --- COBBLE BRIDGE: tightly packed rounded cobblestones, steppe ---
    bid = COBBLE_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]          # (108, 98, 84)
    dk = _darken(c, 28)
    lt = _lighter(c, 16)
    gap = _darken(c, 40)
    BS = BLOCK_SIZE
    s.fill(gap)
    _rnd_c = _rnd.Random(0xC0BB1E)
    cobble_cx = [(x, y) for y in range(4, BS, 7) for x in range(3 + (y // 7 % 2) * 3, BS, 8)]
    shades = [_darken(c, v) for v in (0, 8, 16)] + [_lighter(c, v) for v in (6, 12)]
    for (cx2, cy2) in cobble_cx:
        rx = _rnd_c.randint(3, 4)
        ry = _rnd_c.randint(2, 3)
        shade = shades[_rnd_c.randint(0, len(shades) - 1)]
        pygame.draw.ellipse(s, shade, (cx2 - rx, cy2 - ry, rx * 2, ry * 2))
        pygame.draw.ellipse(s, lt, (cx2 - rx + 1, cy2 - ry, rx - 1, ry - 1))
        pygame.draw.ellipse(s, dk, (cx2 - rx, cy2 - ry, rx * 2, ry * 2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    # --- DRIFTWOOD BRIDGE: pale weathered sea-worn planks, coastal ---
    bid = DRIFTWOOD_BRIDGE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]          # (185, 172, 148)
    dk = _darken(c, 22)
    lt = _lighter(c, 14)
    bleach = _lighter(c, 24)
    BS = BLOCK_SIZE
    s.fill(c)
    # irregular plank seams — slightly uneven spacing for weathered look
    _rnd_d = _rnd.Random(0xD4175)
    seams = sorted([_rnd_d.randint(4, BS - 4) for _ in range(BS // 5)])
    for gy in seams:
        pygame.draw.line(s, dk, (0, gy), (BS, gy), 1)
    # bleached salt-streaks across planks
    for _ in range(6):
        sx = _rnd_d.randint(0, BS - 6)
        sy = _rnd_d.randint(1, BS - 2)
        pygame.draw.line(s, bleach, (sx, sy), (sx + _rnd_d.randint(4, 8), sy), 1)
    # vertical grain lines
    for gx in range(0, BS, 9):
        pygame.draw.line(s, dk, (gx, 0), (gx, BS), 1)
    # top-edge plank highlight
    prev = 0
    for gy in seams + [BS]:
        pygame.draw.line(s, lt, (1, prev), (BS - 1, prev), 1)
        prev = gy
    pygame.draw.rect(s, dk, s.get_rect(), 1)
    surfs[bid] = s

    return surfs
