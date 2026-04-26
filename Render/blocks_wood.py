import pygame
import math
import random as _rnd
from blocks import BLOCKS
from blocks import *  # all block ID constants
from constants import BLOCK_SIZE
from Render.block_helpers import _darken, _lighter, _tinted, _MSTYLES, CAVE_MUSHROOMS, render_mushroom_preview


def build_wood_surfs():
    surfs = {}
    bid = LADDER
    # if bid == LADDER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    rail = BLOCKS[bid]["color"]
    dark = _darken(rail)
    pygame.draw.rect(s, rail, (4,                  0, 4, BLOCK_SIZE))
    pygame.draw.rect(s, rail, (BLOCK_SIZE - 8,     0, 4, BLOCK_SIZE))
    for ry in [3, 11, 19, 27]:
        pygame.draw.rect(s, dark, (4, ry, BLOCK_SIZE - 8, 3))
    surfs[bid] = s

    bid = WOOD_FENCE
    # if bid == WOOD_FENCE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    brown = (139, 90, 43)
    dbrown = (100, 65, 30)
    pygame.draw.rect(s, brown,  (12, 0, 8, 32))
    pygame.draw.rect(s, dbrown, (11, 0, 10, 3))
    pygame.draw.rect(s, brown,  (0, 10, 32, 4))
    pygame.draw.rect(s, brown,  (0, 20, 32, 4))
    surfs[bid] = s

    bid = IRON_FENCE
    # if bid == IRON_FENCE
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

    bid = WOOD_FENCE_OPEN
    # if bid == WOOD_FENCE_OPEN
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

    bid = IRON_FENCE_OPEN
    # if bid == IRON_FENCE_OPEN
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

    bid = WOOD_DOOR_CLOSED
    # if bid == WOOD_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(s, (110, 70, 30),  (0,  0, 32, 32))
    pygame.draw.rect(s, (160, 105, 55), (3,  3, 26, 26))
    pygame.draw.rect(s, (145, 95,  45), (6,  8, 20, 16))
    pygame.draw.circle(s, (220, 180, 80), (22, 16), 2)
    surfs[bid] = s

    bid = WOOD_DOOR_OPEN
    # if bid == WOOD_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (160, 105, 55), (0, 0, 8, 32))
    pygame.draw.rect(s, (100,  65, 30), (7, 0, 1, 32))
    surfs[bid] = s

    bid = IRON_DOOR_CLOSED
    # if bid == IRON_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(s, (120, 120, 128), (0,  0, 32, 32))
    pygame.draw.rect(s, (175, 175, 182), (3,  3, 26, 26))
    pygame.draw.rect(s, (100, 100, 108), (3, 15, 26,  2))
    for rx, ry in ((5, 5), (27, 5), (5, 27), (27, 27)):
        pygame.draw.circle(s, (100, 100, 108), (rx, ry), 2)
    pygame.draw.rect(s, (200, 200, 90), (22, 13, 4, 6))
    surfs[bid] = s

    bid = IRON_DOOR_OPEN
    # if bid == IRON_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (175, 175, 182), (0, 0, 8, 32))
    pygame.draw.rect(s, (100, 100, 108), (7, 0, 1, 32))
    pygame.draw.circle(s, (100, 100, 108), (4, 16), 2)
    surfs[bid] = s

    bid = COBALT_DOOR_CLOSED
    # if bid == COBALT_DOOR_CLOSED
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

    bid = COBALT_DOOR_OPEN
    # if bid == COBALT_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (55, 95, 185), (0, 0, 8, 32))
    pygame.draw.rect(s, (28, 55, 140), (7, 0, 1, 32))
    surfs[bid] = s

    bid = CRIMSON_CEDAR_DOOR_CLOSED
    # if bid == CRIMSON_CEDAR_DOOR_CLOSED
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

    bid = CRIMSON_CEDAR_DOOR_OPEN
    # if bid == CRIMSON_CEDAR_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (155, 45, 48), (0, 0, 8, 32))
    pygame.draw.rect(s, (105, 25, 28), (7, 0, 1, 32))
    surfs[bid] = s

    bid = TEAL_DOOR_CLOSED
    # if bid == TEAL_DOOR_CLOSED
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

    bid = TEAL_DOOR_OPEN
    # if bid == TEAL_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 150, 145), (0, 0, 8, 32))
    pygame.draw.rect(s, (30, 105, 100), (7, 0, 1, 32))
    surfs[bid] = s

    bid = SAFFRON_DOOR_CLOSED
    # if bid == SAFFRON_DOOR_CLOSED
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

    bid = SAFFRON_DOOR_OPEN
    # if bid == SAFFRON_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (210, 165, 42), (0, 0, 8, 32))
    pygame.draw.rect(s, (160, 115, 18), (7, 0, 1, 32))
    surfs[bid] = s

    bid = STUDDED_OAK_DOOR_CLOSED
    # if bid == STUDDED_OAK_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (100, 65, 35)
    frame = (70, 45, 25)
    iron = (70, 75, 80)
    s.fill(frame)
    pygame.draw.rect(s, base, (3, 3, 26, 26))
    for bx in (8, 16, 24):
        pygame.draw.line(s, frame, (bx, 3), (bx, 29), 1)
    # iron straps
    pygame.draw.rect(s, iron, (3, 8, 26, 4))
    pygame.draw.rect(s, iron, (3, 20, 26, 4))
    # studs
    for bx in (8, 16, 24):
        pygame.draw.circle(s, (40, 40, 40), (bx, 10), 1)
        pygame.draw.circle(s, (40, 40, 40), (bx, 22), 1)
    surfs[bid] = s

    bid = STUDDED_OAK_DOOR_OPEN
    # if bid == STUDDED_OAK_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (100, 65, 35), (0, 0, 8, 32))
    pygame.draw.rect(s, (70, 45, 25), (7, 0, 1, 32))
    pygame.draw.rect(s, (70, 75, 80), (0, 8, 8, 4))
    pygame.draw.rect(s, (70, 75, 80), (0, 20, 8, 4))
    surfs[bid] = s

    bid = VERMILION_DOOR_CLOSED
    # if bid == VERMILION_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (180, 40, 30)
    frame = (120, 20, 15)
    brass = (220, 180, 50)
    s.fill(frame)
    pygame.draw.rect(s, base, (3, 3, 26, 26))
    for bx in (8, 16, 24):
        for by in (8, 16, 24):
            pygame.draw.circle(s, brass, (bx, by), 2)
    # handles
    pygame.draw.circle(s, brass, (20, 16), 3, 1)
    surfs[bid] = s

    bid = VERMILION_DOOR_OPEN
    # if bid == VERMILION_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (180, 40, 30), (0, 0, 8, 32))
    pygame.draw.rect(s, (120, 20, 15), (7, 0, 1, 32))
    surfs[bid] = s

    bid = SHOJI_DOOR_CLOSED
    # if bid == SHOJI_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    frame = (180, 140, 90)
    paper = (240, 230, 210)
    s.fill(frame)
    pygame.draw.rect(s, paper, (3, 3, 26, 26))
    for bx in (11, 20):
        pygame.draw.line(s, frame, (bx, 3), (bx, 29), 1)
    for by in (8, 16, 24):
        pygame.draw.line(s, frame, (3, by), (29, by), 1)
    surfs[bid] = s

    bid = SHOJI_DOOR_OPEN
    # if bid == SHOJI_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (240, 230, 210), (0, 0, 8, 32))
    pygame.draw.rect(s, (180, 140, 90), (7, 0, 1, 32))
    pygame.draw.line(s, (180, 140, 90), (4, 0), (4, 32), 1)
    surfs[bid] = s

    bid = GILDED_DOOR_CLOSED
    # if bid == GILDED_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (240, 240, 245)
    gold = (220, 180, 50)
    s.fill(base)
    pygame.draw.rect(s, gold, (4, 4, 24, 10), 1)
    pygame.draw.rect(s, gold, (4, 18, 24, 10), 1)
    # rosette
    pygame.draw.circle(s, gold, (16, 9), 3)
    pygame.draw.circle(s, gold, (16, 23), 3)
    # handle
    pygame.draw.circle(s, gold, (25, 16), 2)
    surfs[bid] = s

    bid = GILDED_DOOR_OPEN
    # if bid == GILDED_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (240, 240, 245), (0, 0, 8, 32))
    pygame.draw.rect(s, (220, 180, 50), (7, 0, 1, 32))
    surfs[bid] = s

    bid = BRONZE_DOOR_CLOSED
    # if bid == BRONZE_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (100, 80, 50)
    dark = (60, 45, 25)
    s.fill(base)
    pygame.draw.rect(s, dark, (2, 2, 28, 28), 2)
    pygame.draw.rect(s, dark, (6, 6, 20, 20), 1)
    # cross icon
    pygame.draw.line(s, dark, (16, 10), (16, 22), 2)
    pygame.draw.line(s, dark, (12, 14), (20, 14), 2)
    surfs[bid] = s

    bid = BRONZE_DOOR_OPEN
    # if bid == BRONZE_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (100, 80, 50), (0, 0, 8, 32))
    pygame.draw.rect(s, (60, 45, 25), (7, 0, 1, 32))
    surfs[bid] = s

    bid = SWAHILI_DOOR_CLOSED
    # if bid == SWAHILI_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (90, 60, 30)
    dark = (50, 30, 10)
    brass = (200, 160, 40)
    s.fill(dark)
    pygame.draw.rect(s, base, (4, 4, 24, 24))
    # carved frame
    pygame.draw.rect(s, dark, (6, 6, 20, 20), 1)
    # spikes/studs along the center vertical
    pygame.draw.line(s, dark, (16, 4), (16, 28), 2)
    for by in (8, 14, 20, 26):
        pygame.draw.circle(s, brass, (16, by), 1)
    surfs[bid] = s

    bid = SWAHILI_DOOR_OPEN
    # if bid == SWAHILI_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (90, 60, 30), (0, 0, 8, 32))
    pygame.draw.rect(s, (50, 30, 10), (7, 0, 1, 32))
    surfs[bid] = s

    bid = SANDALWOOD_DOOR_CLOSED
    # if bid == SANDALWOOD_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (140, 90, 50)
    dark = (90, 50, 20)
    s.fill(dark)
    pygame.draw.rect(s, base, (2, 2, 28, 28))
    # dense floral carved motifs
    for dx, dy in [(8, 8), (24, 8), (8, 24), (24, 24), (16, 16)]:
        pygame.draw.circle(s, dark, (dx, dy), 4, 1)
        pygame.draw.circle(s, dark, (dx, dy), 2)
    pygame.draw.rect(s, dark, (4, 4, 24, 24), 1)
    surfs[bid] = s

    bid = SANDALWOOD_DOOR_OPEN
    # if bid == SANDALWOOD_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (140, 90, 50), (0, 0, 8, 32))
    pygame.draw.rect(s, (90, 50, 20), (7, 0, 1, 32))
    surfs[bid] = s

    bid = STONE_SLAB_DOOR_CLOSED
    # if bid == STONE_SLAB_DOOR_CLOSED
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (120, 120, 120)
    dark = (80, 80, 80)
    s.fill(dark)
    # trapezoidal
    pygame.draw.polygon(s, base, [(6, 2), (26, 2), (30, 30), (2, 30)])
    # glyphs
    pygame.draw.rect(s, dark, (12, 6, 8, 6), 1)
    pygame.draw.line(s, dark, (14, 9), (18, 9), 1)
    pygame.draw.rect(s, dark, (12, 16, 8, 8), 1)
    pygame.draw.circle(s, dark, (16, 20), 2, 1)
    surfs[bid] = s

    bid = STONE_SLAB_DOOR_OPEN
    # if bid == STONE_SLAB_DOOR_OPEN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (120, 120, 120), (0, 0, 8, 32))
    pygame.draw.rect(s, (80, 80, 80), (7, 0, 1, 32))
    surfs[bid] = s

    bid = STAIRS_RIGHT
    # if bid in (STAIRS_RIGHT, STAIRS_LEFT)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    wood  = BLOCKS[bid]["color"]
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

    bid = STAIRS_LEFT
    # if bid in (STAIRS_RIGHT, STAIRS_LEFT)
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    wood  = BLOCKS[bid]["color"]
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

    bid = CHEST_BLOCK
    # if bid == CHEST_BLOCK
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

    bid = BIRD_FEEDER_BLOCK
    # if bid == BIRD_FEEDER_BLOCK
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

    bid = BIRD_BATH_BLOCK
    # if bid == BIRD_BATH_BLOCK
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

    bid = OAK_PANEL
    # if bid == OAK_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BAMBOO_PANEL
    # if bid == BAMBOO_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = OBSIDIAN_TILE
    # if bid == OBSIDIAN_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = COBBLESTONE
    # if bid == COBBLESTONE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = BASALT_COLUMN
    # if bid == BASALT_COLUMN
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = LIMESTONE_BLOCK
    # if bid == LIMESTONE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = COPPER_TILE
    # if bid == COPPER_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = DRIFTWOOD_PLANK
    # if bid == DRIFTWOOD_PLANK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = JADE_PANEL
    # if bid == JADE_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    vn = _darken(c, 35)
    lt = _lighter(c, 20)
    pygame.draw.line(s, vn, (3, 0), (20, 32), 1)
    pygame.draw.line(s, lt, (4, 0), (21, 32), 1)
    pygame.draw.line(s, vn, (22, 0), (32, 12), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = ROSE_QUARTZ_BLOCK
    # if bid == ROSE_QUARTZ_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = AMETHYST_BLOCK
    # if bid == AMETHYST_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 30)
    dk = _darken(c, 40)
    for cx2, cw2, ch2 in [(2,6,14),(9,5,20),(16,6,16),(22,5,12),(27,4,18)]:
        pygame.draw.polygon(s, dk, [(cx2, BLOCK_SIZE), (cx2+cw2, BLOCK_SIZE), (cx2+cw2//2, BLOCK_SIZE-ch2)])
        pygame.draw.line(s, lt, (cx2+cw2//2, BLOCK_SIZE-ch2), (cx2+cw2//2-1, BLOCK_SIZE-ch2//2), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = AMBER_TILE
    # if bid == AMBER_TILE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = ASH_PLANK
    # if bid == ASH_PLANK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = FROSTED_GLASS
    # if bid == FROSTED_GLASS
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = TERRACOTTA_SHINGLE
    # if bid == TERRACOTTA_SHINGLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = THATCH_ROOF
    # if bid == THATCH_ROOF
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    bid = VERDIGRIS_COPPER
    # if bid == VERDIGRIS_COPPER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    dk = _darken(c, 30)
    lt = _lighter(c, 22)
    for px2, py2, pw2, ph2 in [(3,2,8,6),(18,5,7,5),(6,16,9,7),(20,18,8,6),(2,26,6,4)]:
        pygame.draw.ellipse(s, lt, (px2, py2, pw2, ph2))
        pygame.draw.ellipse(s, dk, (px2+1, py2+1, max(2, pw2-2), max(2, ph2-2)), 1)
    pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
    surfs[bid] = s

    bid = SILVER_PANEL
    # if bid == SILVER_PANEL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(c)
    lt = _lighter(c, 25)
    dk = _darken(c, 20)
    for ly2 in range(1, BLOCK_SIZE-1, 3):
        col2 = lt if (ly2 // 3) % 2 == 0 else dk
        pygame.draw.line(s, col2, (1, ly2), (BLOCK_SIZE-2, ly2), 1)
    pygame.draw.line(s, dk, (BLOCK_SIZE//2, 0), (BLOCK_SIZE//2, BLOCK_SIZE), 1)
    pygame.draw.rect(s, _darken(c), s.get_rect(), 1)
    surfs[bid] = s

    bid = GOLD_LEAF_TRIM
    # if bid == GOLD_LEAF_TRIM
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
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

    return surfs
