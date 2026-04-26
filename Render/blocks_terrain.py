import pygame
import math
import random as _rnd
from blocks import BLOCKS
from blocks import *  # all block ID constants
from constants import BLOCK_SIZE
from Render.block_helpers import _darken, _lighter, _tinted, _MSTYLES, CAVE_MUSHROOMS, render_mushroom_preview


def build_terrain_surfs():
    surfs = {}
    bid = CAVE_MOSS
    # if bid == CAVE_MOSS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
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

    bid = CAVE_CRYSTAL
    # if bid == CAVE_CRYSTAL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    base = BLOCKS[bid]["color"]
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

    bid = GRAVEL
    # if bid == GRAVEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
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

    bid = CRACKED_STONE
    # if bid == CRACKED_STONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 40)
    s.fill(base)
    pygame.draw.line(s, dark, (4, 6),  (14, 22), 1)
    pygame.draw.line(s, dark, (18, 3), (26, 15), 1)
    pygame.draw.line(s, dark, (8, 20), (15, 28), 1)
    pygame.draw.rect(s, _darken(base), s.get_rect(), 1)
    surfs[bid] = s

    bid = STALACTITE
    # if bid == STALACTITE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    pts = [(8, 0), (24, 0), (16, BLOCK_SIZE - 2)]
    pygame.draw.polygon(s, base, pts)
    pygame.draw.polygon(s, dark, pts, 1)
    surfs[bid] = s

    bid = CAVE_MUSHROOM
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = EMBER_CAP
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = PALE_GHOST
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = GOLD_CHANTERELLE
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = COBALT_CAP
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = MOSSY_CAP
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = VIOLET_CROWN
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = BLOOD_CAP
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = SULFUR_DOME
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = IVORY_BELL
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = ASH_BELL
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = TEAL_BELL
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = RUST_SHELF
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = COPPER_SHELF
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = OBSIDIAN_SHELF
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = COAL_PUFF
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = STONE_PUFF
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = AMBER_PUFF
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = SULFUR_TUFT
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = HONEY_CLUSTER
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = CORAL_TUFT
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = BONE_STALK
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = MAGMA_CAP
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = DEEP_INK
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = BIOLUME
    # if bid in CAVE_MUSHROOMS
    surfs[bid] = render_mushroom_preview(bid, BLOCK_SIZE)

    bid = STALAGMITE
    # if bid == STALAGMITE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    pts = [(16, 2), (8, BLOCK_SIZE), (24, BLOCK_SIZE)]
    pygame.draw.polygon(s, base, pts)
    pygame.draw.polygon(s, dark, pts, 1)
    surfs[bid] = s

    # if bid == WATER — skipped (rendered elsewhere)

    bid = COAL_ORE
    # if bid == COAL_ORE
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

    bid = CLAY_DEPOSIT
    # if bid == CLAY_DEPOSIT
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

    bid = LIMESTONE_DEPOSIT
    # if bid == LIMESTONE_DEPOSIT
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

    bid = MARBLE_VEIN
    # if bid == MARBLE_VEIN
    c = (235, 232, 222)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); s.fill(c)
    vein = _darken(c, 35)
    lt   = _lighter(c, 12)
    # Irregular diagonal veins
    for pts in [[(0,4),(8,2),(16,6),(24,3),(32,5)],
                 [(0,14),(6,12),(14,16),(22,13),(32,17)],
                 [(0,24),(10,22),(18,26),(32,23)]]:
        pygame.draw.lines(s, vein, False, pts, 1)
        pygame.draw.lines(s, lt,   False, [(x, y+1) for x, y in pts], 1)
    pygame.draw.rect(s, _darken(c, 22), s.get_rect(), 1)
    surfs[bid] = s

    bid = ALABASTER_VEIN
    # if bid == ALABASTER_VEIN
    c = (232, 218, 198)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); s.fill(c)
    dk = _darken(c, 14); lt = _lighter(c, 16)
    # Subtle horizontal banding (sedimentary feel)
    for ly in [7, 15, 22]:
        pygame.draw.line(s, dk, (0, ly),   (BLOCK_SIZE, ly),   2)
        pygame.draw.line(s, lt, (0, ly-1), (BLOCK_SIZE, ly-1), 1)
    # Soft highlight in top-left
    pygame.draw.rect(s, lt, (2, 2, 14, 14))
    pygame.draw.rect(s, _darken(c, 18), s.get_rect(), 1)
    surfs[bid] = s

    bid = VERDITE_VEIN
    # if bid == VERDITE_VEIN
    c = (38, 105, 58)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); s.fill(c)
    dk = _darken(c, 30); lt = _lighter(c, 25)
    # Mottled crystalline texture
    for fx, fy, fw, fh in [(3,3,6,5),(14,2,5,6),(22,5,7,4),
                            (5,14,8,5),(18,12,6,7),(28,16,4,4),
                            (8,22,7,6),(20,24,6,5)]:
        pygame.draw.rect(s, dk, (fx, fy, fw, fh))
    for fx, fy in [(5,5),(16,4),(24,7),(7,16),(20,14),(10,24),(22,26)]:
        pygame.draw.rect(s, lt, (fx, fy, 2, 2))
    pygame.draw.rect(s, _darken(c, 28), s.get_rect(), 1)
    surfs[bid] = s

    bid = ONYX_VEIN
    # if bid == ONYX_VEIN
    c = (28, 22, 38)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); s.fill(c)
    band = _lighter(c, 20)
    lt   = _lighter(c, 38)
    # White/gray banding characteristic of onyx
    for ly, thick in [(5,2),(12,1),(18,2),(26,1)]:
        pygame.draw.line(s, band, (0, ly), (BLOCK_SIZE, ly), thick)
    # Faint sheen spots
    for fx, fy in [(4,8),(20,6),(12,19),(27,22),(8,27)]:
        pygame.draw.rect(s, lt, (fx, fy, 3, 1))
    pygame.draw.rect(s, _darken(c, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = ALABASTER_BLOCK
    # if bid == ALABASTER_BLOCK
    c = (235, 222, 204)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); s.fill(c)
    lt = _lighter(c, 20); dk = _darken(c, 18)
    pygame.draw.rect(s, lt, (2, 2, BLOCK_SIZE-4, BLOCK_SIZE//2-2))
    pygame.draw.line(s, dk, (0, BLOCK_SIZE//2), (BLOCK_SIZE, BLOCK_SIZE//2), 1)
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = VERDITE_BLOCK
    # if bid == VERDITE_BLOCK
    c = (42, 108, 62)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); s.fill(c)
    lt = _lighter(c, 22); dk = _darken(c, 28)
    for fx, fy in [(2,2),(18,2),(2,18),(18,18)]:
        pygame.draw.rect(s, lt, (fx, fy, 6, 6))
    pygame.draw.rect(s, dk, s.get_rect(), 2)
    surfs[bid] = s

    bid = ONYX_BLOCK
    # if bid == ONYX_BLOCK
    c = (30, 24, 40)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)); s.fill(c)
    lt = _lighter(c, 35)
    # Thin white banding + reflective highlight diagonal
    pygame.draw.line(s, lt, (0, 10), (BLOCK_SIZE, 10), 1)
    pygame.draw.line(s, lt, (0, 22), (BLOCK_SIZE, 22), 1)
    pygame.draw.line(s, _lighter(c, 50), (2, 2), (12, 2), 1)
    pygame.draw.rect(s, _lighter(c, 20), s.get_rect(), 2)
    surfs[bid] = s

    bid = SAPLING
    # if bid == SAPLING
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (101, 67, 33), (14, 20, 4, 12))
    pygame.draw.circle(s, (50, 170, 50), (16, 14), 7)
    pygame.draw.circle(s, (70, 190, 70), (13, 11), 4)
    pygame.draw.circle(s, (70, 190, 70), (20, 12), 4)
    surfs[bid] = s

    bid = MUSHROOM_STEM
    # if bid == MUSHROOM_STEM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (228, 218, 198)
    dark = _darken(base, 20)
    s.fill(base)
    pygame.draw.rect(s, dark, (0, 0, 4, 32))
    pygame.draw.rect(s, dark, (28, 0, 4, 32))
    pygame.draw.rect(s, tuple(min(255, c + 15) for c in base), (4, 0, 24, 32))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = MUSHROOM_CAP
    # if bid == MUSHROOM_CAP
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    base = (175, 38, 38)
    dark = _darken(base, 30)
    pygame.draw.ellipse(s, base, (0, 8, 32, 24))
    pygame.draw.ellipse(s, dark, (0, 8, 32, 24), 1)
    for sx, sy in [(7, 14), (16, 11), (23, 15)]:
        pygame.draw.circle(s, (240, 235, 220), (sx, sy), 3)
    surfs[bid] = s

    return surfs
