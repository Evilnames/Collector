import pygame
import math
import random as _rnd
from blocks import BLOCKS
from blocks import *  # all block ID constants
from constants import BLOCK_SIZE
from Render.block_helpers import _darken, _lighter, _tinted, _MSTYLES, CAVE_MUSHROOMS, render_mushroom_preview


def build_crafting_surfs():
    surfs = {}
    bid = BAKERY_BLOCK
    # if bid == BAKERY_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
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

    bid = WOK_BLOCK
    # if bid == WOK_BLOCK
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

    bid = STEAMER_BLOCK
    # if bid == STEAMER_BLOCK
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

    bid = NOODLE_POT_BLOCK
    # if bid == NOODLE_POT_BLOCK
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

    bid = BBQ_GRILL_BLOCK
    # if bid == BBQ_GRILL_BLOCK
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

    bid = CLAY_POT_BLOCK
    # if bid == CLAY_POT_BLOCK
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

    bid = TUMBLER_BLOCK
    # if bid == TUMBLER_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 35)
    s.fill(dark)
    # Drum barrel (horizontal cylinder viewed from front)
    pygame.draw.ellipse(s, base, (3, 7, 26, 18))
    pygame.draw.ellipse(s, _lighter(base, 20), (5, 9, 10, 10))
    # Porthole door
    pygame.draw.circle(s, dark, (16, 16), 6)
    pygame.draw.circle(s, (205, 180, 155), (16, 16), 4)
    # Tumbling rocks inside porthole
    pygame.draw.circle(s, (200, 80, 80), (14, 15), 2)
    pygame.draw.circle(s, (80, 130, 210), (18, 17), 2)
    pygame.draw.circle(s, (200, 185, 60), (16, 19), 1)
    # Stand legs
    pygame.draw.rect(s, dark, (6, 25, 4, 6))
    pygame.draw.rect(s, dark, (22, 25, 4, 6))
    pygame.draw.rect(s, _darken(base, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = CRUSHER_BLOCK
    # if bid == CRUSHER_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 25)
    s.fill(dark)
    # Hopper at top
    pygame.draw.polygon(s, base, [(9, 2), (23, 2), (19, 10), (13, 10)])
    # Upper roller
    pygame.draw.rect(s, bright, (4, 10, 24, 8))
    for gx in [8, 13, 18, 23]:
        pygame.draw.line(s, dark, (gx, 10), (gx, 18), 1)
    # Lower roller
    pygame.draw.rect(s, base, (4, 19, 24, 8))
    for gx in [8, 13, 18, 23]:
        pygame.draw.line(s, dark, (gx, 19), (gx, 27), 1)
    # Output slot
    pygame.draw.rect(s, (35, 28, 18), (10, 27, 12, 4))
    pygame.draw.rect(s, _darken(dark, 10), s.get_rect(), 1)
    surfs[bid] = s

    bid = GEM_CUTTER_BLOCK
    # if bid == GEM_CUTTER_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 35)
    s.fill((40, 35, 30))
    # Base table
    pygame.draw.rect(s, (80, 65, 50), (2, 22, 28, 8))
    # Grinding disc wheel
    pygame.draw.ellipse(s, dark, (3, 8, 18, 16))
    pygame.draw.ellipse(s, base, (4, 9, 16, 13))
    pygame.draw.circle(s, dark, (12, 15), 3)
    pygame.draw.line(s, (80, 65, 50), (12, 18), (12, 22), 2)
    # Gem sparkle on right
    pygame.draw.circle(s, (120, 240, 255), (24, 13), 4)
    for dx, dy in [(-4, -4), (4, -4), (0, -6), (0, 2), (-4, 2), (4, 2)]:
        pygame.draw.line(s, (200, 245, 255), (24 + dx, 13 + dy), (24, 13), 1)
    pygame.draw.rect(s, (30, 25, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = KILN_BLOCK
    # if bid == KILN_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 40)
    s.fill(dark)
    # Brick rows
    for row in range(4):
        off = 4 if row % 2 == 0 else 0
        for col in range(-1, 4):
            pygame.draw.rect(s, base, (off + col * 8, row * 8, 7, 7), 1)
    # Arched furnace mouth
    pygame.draw.rect(s, (20, 10, 5), (8, 15, 16, 13))
    pygame.draw.arc(s, (20, 10, 5), (8, 9, 16, 12), 0, math.pi, 3)
    # Alchemical glow (green)
    pygame.draw.circle(s, (80, 210, 70), (16, 22), 4)
    # Chimney with purple smoke
    pygame.draw.rect(s, dark, (20, 0, 6, 8))
    pygame.draw.rect(s, (130, 60, 220), (21, 2, 4, 3))
    pygame.draw.rect(s, _darken(base, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = RESONANCE_BLOCK
    # if bid == RESONANCE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 40)
    s.fill((20, 10, 40))
    # Radiating lines (vibration burst)
    for ang_deg in [200, 215, 230, 310, 325, 340]:
        rad = math.radians(ang_deg)
        ex = int(16 + 13 * math.cos(rad))
        ey = int(16 + 13 * math.sin(rad))
        pygame.draw.line(s, _lighter(base, 10), (16, 16), (ex, ey), 1)
    # Central crystal pillar
    pygame.draw.polygon(s, base, [(14, 2), (18, 2), (20, 28), (12, 28)])
    pygame.draw.polygon(s, _lighter(base, 50), [(15, 3), (17, 3), (16, 11)])
    # Crystal glow
    pygame.draw.circle(s, (150, 100, 255), (16, 15), 4)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = DESERT_FORGE_BLOCK
    # if bid == DESERT_FORGE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 35)
    s.fill(dark)
    # Anvil top (wide face)
    pygame.draw.rect(s, _lighter(base, 20), (3, 8, 26, 6))
    # Anvil body
    pygame.draw.rect(s, base, (6, 14, 20, 8))
    # Anvil horn (left)
    pygame.draw.polygon(s, base, [(6, 14), (6, 20), (0, 18)])
    # Hot coals beneath
    pygame.draw.rect(s, (60, 45, 30), (5, 22, 22, 8))
    pygame.draw.rect(s, (220, 80, 20), (7, 23, 5, 5))
    pygame.draw.rect(s, (255, 160, 30), (13, 24, 5, 3))
    pygame.draw.rect(s, (200, 60, 10), (19, 23, 5, 5))
    # Bellows (right side)
    pygame.draw.rect(s, (110, 80, 50), (27, 12, 5, 10))
    for by2 in [13, 16, 19]:
        pygame.draw.line(s, dark, (27, by2), (31, by2), 1)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = ROASTER_BLOCK
    # if bid == ROASTER_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 30)
    s.fill(dark)
    # Drum body (horizontal cylinder)
    pygame.draw.ellipse(s, base, (3, 9, 24, 14))
    pygame.draw.ellipse(s, bright, (5, 10, 7, 10))
    # Crank handle
    pygame.draw.line(s, (150, 120, 75), (27, 16), (31, 10), 2)
    pygame.draw.circle(s, (165, 135, 85), (31, 10), 2)
    # Output chute
    pygame.draw.polygon(s, _darken(base, 15), [(11, 23), (21, 23), (23, 30), (9, 30)])
    # Heat glow
    pygame.draw.rect(s, (200, 100, 20), (7, 28, 18, 3))
    # Steam wisps
    for wx in [10, 15, 20]:
        pygame.draw.rect(s, bright, (wx, 4, 2, 5))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = BLEND_STATION_BLOCK
    # if bid == BLEND_STATION_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    s.fill(dark)
    # Machine body
    pygame.draw.rect(s, base, (4, 10, 24, 18))
    # Mixing bowl (ellipse top opening)
    pygame.draw.ellipse(s, _lighter(base, 20), (6, 6, 20, 10))
    pygame.draw.ellipse(s, (40, 28, 15), (8, 7, 16, 7))
    # Paddle in bowl
    pygame.draw.line(s, (205, 185, 135), (16, 3), (16, 13), 2)
    pygame.draw.line(s, (205, 185, 135), (11, 10), (21, 10), 2)
    # Dispense nozzle at bottom
    pygame.draw.rect(s, dark, (13, 28, 6, 4))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = BREW_STATION_BLOCK
    # if bid == BREW_STATION_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    s.fill(dark)
    # Base platform
    pygame.draw.rect(s, base, (3, 24, 26, 6))
    # Carafe body
    pygame.draw.rect(s, (52, 42, 32), (9, 15, 14, 10))
    pygame.draw.rect(s, (80, 65, 50), (9, 15, 14, 10), 1)
    # Carafe handle nub
    pygame.draw.rect(s, (52, 42, 32), (22, 17, 4, 5))
    # Drip funnel
    pygame.draw.polygon(s, _lighter(base, 15), [(10, 4), (22, 4), (18, 14), (14, 14)])
    # Steam
    pygame.draw.rect(s, _lighter(base, 30), (12, 12, 2, 4))
    pygame.draw.rect(s, _lighter(base, 30), (17, 13, 2, 3))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = FOSSIL_TABLE_BLOCK
    # if bid == FOSSIL_TABLE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 20)
    s.fill(dark)
    # Table surface
    pygame.draw.rect(s, base, (2, 12, 28, 15))
    pygame.draw.rect(s, bright, (2, 12, 28, 3))
    # Table legs
    pygame.draw.rect(s, _darken(base, 15), (4, 27, 4, 5))
    pygame.draw.rect(s, _darken(base, 15), (24, 27, 4, 5))
    # Ammonite fossil (concentric partial circles)
    pygame.draw.circle(s, (185, 168, 135), (14, 20), 6, 1)
    pygame.draw.circle(s, (185, 168, 135), (14, 20), 4, 1)
    pygame.draw.circle(s, (185, 168, 135), (14, 20), 2, 1)
    # Chisel tool on right
    pygame.draw.line(s, (165, 155, 140), (22, 14), (27, 21), 2)
    pygame.draw.rect(s, (205, 195, 175), (21, 12, 4, 3))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = ARTISAN_BENCH_BLOCK
    # if bid == ARTISAN_BENCH_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 25)
    s.fill(dark)
    # Bench top
    pygame.draw.rect(s, base, (2, 10, 28, 8))
    pygame.draw.rect(s, bright, (2, 10, 28, 2))
    # Bench legs
    pygame.draw.rect(s, _darken(base, 15), (4, 18, 5, 13))
    pygame.draw.rect(s, _darken(base, 15), (23, 18, 5, 13))
    # Shelf between legs
    pygame.draw.rect(s, _darken(base, 20), (4, 24, 24, 3))
    # Vise jaw on left
    pygame.draw.rect(s, (82, 77, 72), (0, 11, 4, 6))
    pygame.draw.rect(s, (62, 57, 52), (0, 11, 4, 6), 1)
    # Mallet on bench top
    pygame.draw.rect(s, _lighter(base, 15), (18, 7, 10, 4))
    pygame.draw.rect(s, _darken(base, 10), (22, 4, 3, 8))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = GRAPE_PRESS_BLOCK
    # if bid == GRAPE_PRESS_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    s.fill(dark)
    # Vat body (bottom)
    pygame.draw.rect(s, base, (4, 18, 24, 12))
    # Barrel hoops
    for hy in [20, 24, 28]:
        pygame.draw.line(s, dark, (4, hy), (28, hy), 1)
    # Screw press center bar
    pygame.draw.rect(s, (82, 67, 55), (14, 4, 4, 16))
    for ty in range(5, 20, 3):
        pygame.draw.line(s, _lighter(base, 20), (14, ty), (17, ty + 2), 1)
    # Press T-bar handle
    pygame.draw.rect(s, (105, 82, 68), (7, 4, 18, 3))
    # Press plate over vat
    pygame.draw.rect(s, (105, 82, 68), (6, 17, 20, 3))
    # Grape juice drip
    pygame.draw.rect(s, (120, 30, 80), (16, 30, 2, 2))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = FERMENTATION_BLOCK
    # if bid == FERMENTATION_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    s.fill(dark)
    # Tank body
    pygame.draw.rect(s, base, (5, 10, 22, 18))
    pygame.draw.ellipse(s, base, (5, 6, 22, 8))
    pygame.draw.ellipse(s, base, (5, 20, 22, 8))
    # Barrel hoop lines
    pygame.draw.ellipse(s, dark, (5, 6, 22, 8), 1)
    for hy in [13, 17, 21]:
        pygame.draw.line(s, dark, (5, hy), (27, hy), 1)
    pygame.draw.ellipse(s, dark, (5, 20, 22, 8), 1)
    # Airlock tube on top
    pygame.draw.rect(s, (82, 105, 125), (14, 2, 4, 6))
    pygame.draw.ellipse(s, (125, 165, 205), (13, 0, 6, 5))
    # Bubbles in airlock
    pygame.draw.circle(s, (205, 225, 255), (15, 2), 1)
    pygame.draw.circle(s, (205, 225, 255), (18, 3), 1)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = WINE_CELLAR_BLOCK
    # if bid == WINE_CELLAR_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 25)
    s.fill(dark)
    # Wine rack frame
    pygame.draw.rect(s, base, (2, 2, 28, 28), 2)
    # Horizontal dividers (3 tiers)
    for ry2 in [10, 18]:
        pygame.draw.line(s, base, (2, ry2), (30, ry2), 2)
    # Vertical divider
    pygame.draw.line(s, base, (16, 2), (16, 28), 2)
    # Bottle ends in each cell (circle = bottle end)
    for cx2, cy2 in [(8, 5), (22, 5), (8, 13), (22, 13), (8, 22), (22, 22)]:
        pygame.draw.circle(s, (82, 52, 67), (cx2, cy2), 4)
        pygame.draw.circle(s, bright, (cx2, cy2), 2)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = STILL_BLOCK
    # if bid == STILL_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 35)
    bright = _lighter(base, 30)
    s.fill((40, 30, 20))
    # Pot belly
    pygame.draw.ellipse(s, base, (3, 10, 16, 18))
    pygame.draw.ellipse(s, bright, (4, 11, 6, 8))
    # Swan neck / lyne arm
    pygame.draw.arc(s, base, (12, 4, 12, 12), math.pi * 0.5, math.pi * 1.5, 3)
    pygame.draw.line(s, base, (18, 10), (28, 15), 3)
    # Coiled worm condenser (right side)
    for cy2 in [13, 17, 21]:
        pygame.draw.arc(s, base, (22, cy2, 9, 5), 0, math.pi, 2)
    # Drip collection cup
    pygame.draw.rect(s, (52, 42, 32), (24, 26, 7, 5))
    pygame.draw.rect(s, (30, 22, 14), s.get_rect(), 1)
    surfs[bid] = s

    bid = BARREL_ROOM_BLOCK
    # if bid == BARREL_ROOM_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 20)
    s.fill(dark)
    # Left barrel
    pygame.draw.ellipse(s, base, (2, 6, 14, 22))
    pygame.draw.ellipse(s, bright, (3, 7, 6, 6))
    for hy in [9, 16, 22]:
        pygame.draw.arc(s, dark, (2, hy, 14, 4), 0, math.pi, 2)
    # Right barrel
    pygame.draw.ellipse(s, base, (16, 6, 14, 22))
    pygame.draw.ellipse(s, bright, (17, 7, 6, 6))
    for hy in [9, 16, 22]:
        pygame.draw.arc(s, dark, (16, hy, 14, 4), 0, math.pi, 2)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = BOTTLING_BLOCK
    # if bid == BOTTLING_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 20)
    s.fill(dark)
    # Platform
    pygame.draw.rect(s, base, (2, 14, 28, 5))
    # Three bottles
    for bx2 in [5, 13, 21]:
        pygame.draw.rect(s, (62, 92, 82), (bx2, 16, 6, 12))
        pygame.draw.rect(s, (62, 92, 82), (bx2 + 2, 11, 2, 5))
        pygame.draw.line(s, (100, 142, 132), (bx2 + 1, 17), (bx2 + 1, 27), 1)
    # Filling spout above platform
    pygame.draw.rect(s, (82, 72, 62), (12, 8, 8, 6))
    pygame.draw.rect(s, (62, 52, 47), (15, 6, 2, 8))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = COMPOST_BIN_BLOCK
    # if bid == COMPOST_BIN_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    s.fill(dark)
    # Slatted wooden box
    pygame.draw.rect(s, base, (3, 6, 26, 24))
    for sy in [10, 14, 18, 22]:
        pygame.draw.line(s, dark, (3, sy), (29, sy), 1)
    # Corner posts
    pygame.draw.rect(s, _darken(base, 15), (3, 6, 3, 24))
    pygame.draw.rect(s, _darken(base, 15), (26, 6, 3, 24))
    # Organic matter on top (green bits)
    for gx2, gy2 in [(7, 4), (12, 3), (17, 5), (22, 4)]:
        pygame.draw.circle(s, (70, 130, 50), (gx2, gy2), 2)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = STABLE_BLOCK
    # if bid == STABLE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    s.fill(dark)
    # Barn wall
    pygame.draw.rect(s, base, (2, 8, 28, 22))
    # Roof triangle
    pygame.draw.polygon(s, _darken(base, 20), [(0, 8), (16, 0), (32, 8)])
    # Door frame
    pygame.draw.rect(s, dark, (10, 16, 12, 14))
    # Door panels
    pygame.draw.rect(s, _darken(base, 10), (11, 17, 5, 13))
    pygame.draw.rect(s, _darken(base, 10), (17, 17, 4, 13))
    # Horseshoe on door
    pygame.draw.arc(s, (92, 82, 72), (12, 20, 8, 6), 0, math.pi, 2)
    pygame.draw.line(s, (92, 82, 72), (12, 23), (12, 26), 2)
    pygame.draw.line(s, (92, 82, 72), (20, 23), (20, 26), 2)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = CHICKEN_COOP_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    s.fill(dark)
    # Small barn walls
    pygame.draw.rect(s, base, (2, 10, 28, 20))
    # Roof triangle
    pygame.draw.polygon(s, _darken(base, 15), [(0, 10), (16, 2), (32, 10)])
    # Roof ridge stripe
    pygame.draw.line(s, _darken(base, 25), (4, 8), (28, 8), 1)
    # Nesting box opening (dark arch)
    pygame.draw.rect(s, dark, (8, 18, 7, 12))
    pygame.draw.ellipse(s, dark, (8, 15, 7, 6))
    # Second nesting box
    pygame.draw.rect(s, dark, (17, 18, 7, 12))
    pygame.draw.ellipse(s, dark, (17, 15, 7, 6))
    # Egg hint (small oval) in left box
    pygame.draw.ellipse(s, (245, 235, 195), (10, 22, 4, 5))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = HORSE_TROUGH_BLOCK
    # if bid == HORSE_TROUGH_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    wood = (112, 82, 47)
    s.fill(dark)
    # Trough wooden body
    pygame.draw.rect(s, wood, (2, 10, 28, 18))
    # Water inside
    pygame.draw.rect(s, base, (4, 12, 24, 12))
    pygame.draw.rect(s, _lighter(base, 20), (4, 12, 24, 3))
    # Wood slat lines
    for wx2 in [8, 15, 22]:
        pygame.draw.line(s, _darken(wood, 20), (wx2, 10), (wx2, 28), 1)
    # Support legs
    pygame.draw.rect(s, wood, (3, 28, 4, 4))
    pygame.draw.rect(s, wood, (25, 28, 4, 4))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = SALT_LICK_BLOCK
    # if bid == SALT_LICK_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (230, 220, 200)
    dark = _darken(base, 25)
    s.fill(dark)
    # Stone/log base
    pygame.draw.rect(s, (100,  75,  55), (4, 22, 24, 8))
    # Salt block (textured chunk)
    pygame.draw.rect(s, base, (8, 10, 16, 14))
    pygame.draw.rect(s, _lighter(base, 18), (8, 10, 16, 3))
    # Crystal facets — small triangular highlights
    for fx, fy in ((10, 14), (14, 17), (18, 13), (20, 19)):
        pygame.draw.polygon(s, _lighter(base, 30),
                            [(fx, fy), (fx + 3, fy + 2), (fx, fy + 3)])
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = FEED_TROUGH_BLOCK
    # if bid == FEED_TROUGH_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    wood = _darken(base, 20)
    hay  = (210, 180,  90)
    hay_dark = (175, 140,  60)
    s.fill(dark)
    # Trough wooden body
    pygame.draw.rect(s, wood, (2, 12, 28, 16))
    pygame.draw.rect(s, base, (4, 14, 24, 12))
    # Hay/feed inside — stipple
    for hx, hy in ((6, 16), (10, 15), (14, 17), (18, 15), (22, 16), (26, 17),
                    (8, 19), (16, 20), (24, 19), (12, 22), (20, 22)):
        pygame.draw.rect(s, hay, (hx, hy, 2, 2))
        pygame.draw.line(s, hay_dark, (hx, hy + 2), (hx + 1, hy + 3), 1)
    # Wood slat lines
    for wx2 in [9, 16, 23]:
        pygame.draw.line(s, _darken(wood, 30), (wx2, 12), (wx2, 28), 1)
    # Support legs
    pygame.draw.rect(s, wood, (3, 28, 4, 4))
    pygame.draw.rect(s, wood, (25, 28, 4, 4))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = WITHERING_RACK_BLOCK
    # if bid == WITHERING_RACK_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    leaf = (132, 157, 77)
    s.fill(dark)
    # Frame side posts
    pygame.draw.rect(s, base, (2, 2, 3, 28))
    pygame.draw.rect(s, base, (27, 2, 3, 28))
    # Three rack tiers with leaves
    for ry2 in [8, 16, 24]:
        pygame.draw.rect(s, _darken(base, 15), (2, ry2, 28, 2))
        for lx in [5, 10, 16, 21]:
            pygame.draw.ellipse(s, leaf, (lx, ry2 - 4, 5, 4))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = OXIDATION_STATION_BLOCK
    # if bid == OXIDATION_STATION_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    leaf = (117, 87, 47)
    s.fill(dark)
    # Table surface
    pygame.draw.rect(s, base, (2, 12, 28, 8))
    pygame.draw.rect(s, _lighter(base, 15), (2, 12, 28, 2))
    # Table legs
    pygame.draw.rect(s, _darken(base, 15), (4, 20, 4, 10))
    pygame.draw.rect(s, _darken(base, 15), (24, 20, 4, 10))
    # Tea leaves spread on table
    for lx2, ly2 in [(5, 14), (9, 16), (14, 14), (18, 16), (23, 14), (12, 17)]:
        pygame.draw.ellipse(s, leaf, (lx2, ly2, 5, 3))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = TEA_CELLAR_BLOCK
    # if bid == TEA_CELLAR_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 20)
    shelf_col = _lighter(base, 32)
    s.fill(dark)
    # Shelf unit frame
    pygame.draw.rect(s, shelf_col, (2, 2, 28, 28), 2)
    # Two shelves
    for sy2 in [12, 20]:
        pygame.draw.line(s, shelf_col, (2, sy2), (30, sy2), 2)
    # Tea canisters (3 per row, 2 rows)
    for sy2 in [5, 14]:
        for cx2 in [6, 14, 22]:
            pygame.draw.rect(s, _lighter(base, 26), (cx2 - 2, sy2, 5, 6))
            pygame.draw.line(s, _lighter(base, 42), (cx2, sy2), (cx2, sy2 + 2), 1)
    # Bottom dark storage area
    pygame.draw.rect(s, _darken(base, 10), (3, 21, 26, 8))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = DRYING_RACK_BLOCK
    # if bid == DRYING_RACK_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    s.fill(dark)
    # Top crossbar
    pygame.draw.rect(s, base, (2, 6, 28, 3))
    # Support legs
    pygame.draw.rect(s, base, (4, 6, 3, 24))
    pygame.draw.rect(s, base, (25, 6, 3, 24))
    # Hanging herb bundles
    for hx in [8, 14, 20, 26]:
        pygame.draw.line(s, (82, 102, 62), (hx, 9), (hx, 22), 1)
        # Leaves on each side of stem
        for hl in [12, 16, 20]:
            pygame.draw.line(s, (92, 122, 67), (hx, hl), (hx - 3, hl - 2), 1)
            pygame.draw.line(s, (92, 122, 67), (hx, hl), (hx + 3, hl - 2), 1)
        # Bundle tie
        pygame.draw.rect(s, (132, 112, 62), (hx - 2, 21, 5, 2))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = MORTAR_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 35)
    s.fill(dark)
    # Bowl rim (wide ellipse, bottom half of block)
    pygame.draw.ellipse(s, base, (3, 16, 26, 13))
    # Bowl interior (darker hollow)
    pygame.draw.ellipse(s, _darken(base, 50), (6, 18, 20, 9))
    # Pestle shaft
    pygame.draw.rect(s, base, (13, 3, 5, 16))
    # Pestle rounded cap
    pygame.draw.circle(s, _lighter(base, 20), (15, 4), 4)
    # Herb specks inside bowl
    pygame.draw.circle(s, (80, 130, 70), (10, 21), 2)
    pygame.draw.circle(s, (90, 145, 65), (16, 23), 1)
    pygame.draw.circle(s, (75, 125, 65), (20, 20), 2)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = BAIT_STATION_BLOCK
    # if bid == BAIT_STATION_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 20)
    s.fill(dark)
    # Tackle box body
    pygame.draw.rect(s, base, (3, 8, 26, 20))
    # Lid (lighter top half)
    pygame.draw.rect(s, bright, (3, 8, 26, 6))
    # Compartment lines
    for lx2 in [10, 17, 24]:
        pygame.draw.line(s, dark, (lx2, 14), (lx2, 28), 1)
    # Fishing hook (J shape)
    pygame.draw.arc(s, (182, 162, 102), (6, 17, 6, 7), math.pi, math.pi * 2, 2)
    pygame.draw.line(s, (182, 162, 102), (12, 21), (12, 16), 2)
    # Bobber (red/white float)
    pygame.draw.circle(s, (222, 62, 42), (22, 22), 3)
    pygame.draw.circle(s, (242, 242, 242), (22, 20), 2)
    # Latch
    pygame.draw.rect(s, (82, 72, 62), (14, 12, 4, 3))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = EVAPORATION_PAN_BLOCK
    # if bid == EVAPORATION_PAN_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 40)
    s.fill((162, 152, 132))
    # Wide shallow pan
    pygame.draw.rect(s, base, (2, 16, 28, 12))
    pygame.draw.ellipse(s, base, (2, 11, 28, 10))
    pygame.draw.ellipse(s, _darken(base, 20), (2, 11, 28, 10), 1)
    # Salt crystal formations inside pan
    for sx2, sy2 in [(6, 19), (11, 21), (17, 18), (22, 20), (14, 23)]:
        pygame.draw.polygon(s, (255, 255, 252), [(sx2, sy2), (sx2 + 2, sy2 - 3), (sx2 + 4, sy2)])
    # Water surface reflection
    pygame.draw.ellipse(s, _lighter(base, 10), (6, 12, 10, 4))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = SALT_GRINDER_BLOCK
    # if bid == SALT_GRINDER_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 35)
    s.fill(dark)
    # Grinder body (cylinder)
    pygame.draw.rect(s, base, (9, 8, 14, 18))
    pygame.draw.ellipse(s, _lighter(base, 15), (9, 5, 14, 8))
    pygame.draw.ellipse(s, _darken(base, 20), (9, 22, 14, 8))
    # Crank handle
    pygame.draw.rect(s, (152, 142, 132), (23, 8, 5, 3))
    pygame.draw.circle(s, (142, 132, 122), (27, 9), 2)
    # Salt granules at bottom
    for sx2, sy2 in [(11, 30), (14, 29), (17, 30), (20, 29)]:
        pygame.draw.circle(s, (242, 240, 234), (sx2, sy2), 1)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = DAIRY_VAT_BLOCK
    # if bid == DAIRY_VAT_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 40)
    s.fill((52, 42, 32))
    # Vat body
    pygame.draw.rect(s, base, (4, 12, 24, 16))
    pygame.draw.ellipse(s, base, (4, 8, 24, 10))
    pygame.draw.ellipse(s, _lighter(base, 15), (4, 8, 24, 10))
    # Milk surface (lighter top ellipse)
    pygame.draw.ellipse(s, (237, 234, 222), (5, 9, 22, 7))
    # Side handles
    pygame.draw.rect(s, dark, (1, 14, 4, 5))
    pygame.draw.rect(s, dark, (27, 14, 4, 5))
    # Stirring paddle
    pygame.draw.rect(s, (132, 107, 72), (15, 3, 2, 14))
    pygame.draw.rect(s, (132, 107, 72), (11, 14, 10, 3))
    # Legs
    pygame.draw.rect(s, (82, 67, 52), (5, 28, 4, 4))
    pygame.draw.rect(s, (82, 67, 52), (23, 28, 4, 4))
    pygame.draw.rect(s, (32, 24, 16), s.get_rect(), 1)
    surfs[bid] = s

    bid = CHEESE_PRESS_BLOCK
    # if bid == CHEESE_PRESS_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    s.fill(dark)
    # Press frame uprights
    pygame.draw.rect(s, base, (3, 4, 4, 24))
    pygame.draw.rect(s, base, (25, 4, 4, 24))
    # Crossbar top
    pygame.draw.rect(s, base, (3, 4, 26, 4))
    # Screw center bar
    pygame.draw.rect(s, _darken(base, 15), (14, 4, 4, 18))
    for ty in range(5, 21, 3):
        pygame.draw.line(s, _lighter(base, 20), (14, ty), (18, ty + 2), 1)
    # Cheese wheel under press
    pygame.draw.ellipse(s, (222, 197, 122), (6, 22, 20, 8))
    pygame.draw.ellipse(s, (202, 177, 102), (6, 22, 20, 8), 1)
    # Press plate
    pygame.draw.rect(s, (102, 82, 62), (5, 19, 22, 4))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = AGING_CAVE_BLOCK
    # if bid == AGING_CAVE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    interior = (57, 50, 42)
    s.fill(dark)
    # Cave interior
    pygame.draw.rect(s, interior, (4, 10, 24, 20))
    pygame.draw.ellipse(s, interior, (4, 4, 24, 14))
    # Stone arch surround
    pygame.draw.arc(s, base, (2, 2, 28, 16), 0, math.pi, 4)
    pygame.draw.rect(s, base, (2, 10, 4, 20))
    pygame.draw.rect(s, base, (26, 10, 4, 20))
    # Cheese wheels inside cave
    pygame.draw.ellipse(s, (212, 187, 112), (6, 16, 9, 6))
    pygame.draw.ellipse(s, (222, 197, 122), (17, 19, 9, 6))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = FLETCHING_TABLE_BLOCK
    # if bid == FLETCHING_TABLE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 20)
    s.fill(dark)
    # Table surface
    pygame.draw.rect(s, base, (2, 12, 28, 7))
    pygame.draw.rect(s, bright, (2, 12, 28, 2))
    # Table legs
    pygame.draw.rect(s, _darken(base, 15), (4, 19, 4, 12))
    pygame.draw.rect(s, _darken(base, 15), (24, 19, 4, 12))
    # Arrow 1 on table
    pygame.draw.line(s, (162, 132, 82), (4, 14), (22, 14), 2)
    pygame.draw.polygon(s, (172, 142, 92), [(22, 11), (27, 14), (22, 17)])
    pygame.draw.rect(s, (102, 142, 82), (3, 13, 4, 3))
    # Arrow 2 slightly below
    pygame.draw.line(s, (162, 132, 82), (4, 17), (21, 17), 1)
    pygame.draw.polygon(s, (172, 142, 92), [(21, 15), (26, 17), (21, 19)])
    pygame.draw.rect(s, (102, 142, 82), (3, 16, 3, 2))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = ANAEROBIC_TANK_BLOCK
    # if bid == ANAEROBIC_TANK_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 25)
    s.fill(dark)
    # Tank cylinder body
    pygame.draw.rect(s, base, (7, 8, 18, 18))
    pygame.draw.ellipse(s, bright, (7, 5, 18, 8))
    pygame.draw.ellipse(s, _darken(base, 20), (7, 22, 18, 8))
    # Sealed top cap
    pygame.draw.ellipse(s, bright, (7, 5, 18, 8), 2)
    # Pressure gauge
    pygame.draw.circle(s, (182, 177, 162), (16, 17), 5)
    pygame.draw.circle(s, (202, 197, 182), (16, 17), 3)
    pygame.draw.line(s, (82, 72, 62), (16, 17), (18, 14), 1)
    # Valve at top
    pygame.draw.rect(s, (82, 72, 62), (14, 2, 4, 5))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = JEWELRY_WORKBENCH_BLOCK
    # if bid == JEWELRY_WORKBENCH_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 35)
    bright = _lighter(base, 30)
    s.fill((32, 26, 20))
    # Bench surface
    pygame.draw.rect(s, base, (2, 14, 28, 7))
    pygame.draw.rect(s, bright, (2, 14, 28, 2))
    # Bench legs
    pygame.draw.rect(s, dark, (3, 21, 5, 10))
    pygame.draw.rect(s, dark, (24, 21, 5, 10))
    # Jeweler's mat
    pygame.draw.rect(s, (52, 42, 32), (7, 12, 14, 4))
    # Gem sparkle
    pygame.draw.polygon(s, (82, 202, 255), [(14, 8), (17, 12), (14, 14), (11, 12)])
    for dx2, dy2 in [(-4, -3), (4, -3), (0, -5)]:
        pygame.draw.line(s, (182, 232, 255), (14 + dx2, 11 + dy2), (14, 11), 1)
    # Loupe tool
    pygame.draw.circle(s, (102, 92, 82), (24, 11), 3, 1)
    pygame.draw.line(s, (102, 92, 82), (22, 13), (20, 16), 2)
    pygame.draw.rect(s, (22, 17, 12), s.get_rect(), 1)
    surfs[bid] = s

    bid = SCULPTORS_BENCH
    # if bid == SCULPTORS_BENCH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = BLOCKS[bid]["color"]
    dark = _darken(base, 30)
    bright = _lighter(base, 20)
    s.fill(dark)
    # Bench top
    pygame.draw.rect(s, base, (2, 12, 28, 7))
    pygame.draw.rect(s, bright, (2, 12, 28, 2))
    # Bench legs
    pygame.draw.rect(s, _darken(base, 15), (4, 19, 5, 12))
    pygame.draw.rect(s, _darken(base, 15), (23, 19, 5, 12))
    # Stone block being carved
    pygame.draw.rect(s, (147, 142, 132), (7, 6, 18, 8))
    pygame.draw.rect(s, (122, 117, 107), (7, 6, 18, 8), 1)
    # Chisel marks
    for mk in [(9, 8), (13, 9), (18, 8), (22, 10)]:
        pygame.draw.line(s, (102, 97, 87), mk, (mk[0] + 2, mk[1] + 3), 1)
    # Chisel tool
    pygame.draw.line(s, (152, 142, 127), (24, 5), (28, 12), 2)
    pygame.draw.rect(s, (112, 92, 62), (22, 4, 3, 3))
    # Stone dust chips
    for ch in [(9, 14), (14, 15), (20, 14)]:
        pygame.draw.circle(s, (182, 177, 167), ch, 1)
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    bid = GLASS_KILN_BLOCK
    # if bid == GLASS_KILN_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    brick = (160, 80, 50)
    dark  = (80, 40, 25)
    s.fill(brick)
    for row in range(4):
        offset_x = 4 if row % 2 == 0 else 0
        for col in range(-1, 4):
            pygame.draw.rect(s, dark, (offset_x + col * 8, row * 8, 7, 7), 1)
    # arched furnace mouth
    mouth_rect = pygame.Rect(7, 14, 18, 14)
    pygame.draw.rect(s, (30, 20, 15), mouth_rect)
    pygame.draw.arc(s, (30, 20, 15), (7, 8, 18, 14), 0, math.pi, 3)
    # orange glow inside arch
    pygame.draw.circle(s, (240, 130, 40), (16, 20), 4)
    # chimney
    pygame.draw.rect(s, dark, (20, 0, 6, 8))
    pygame.draw.rect(s, (240, 130, 40), (21, 2, 4, 3))
    pygame.draw.rect(s, _darken(brick, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = POTTERY_WHEEL_BLOCK
    # if bid == POTTERY_WHEEL_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    base = (130, 95, 65)
    dark = _darken(base, 35)
    s.fill(base)
    # wooden base frame
    pygame.draw.rect(s, dark, (4, 20, 24, 10))
    # wheel disc (top view oval)
    pygame.draw.ellipse(s, (165, 120, 80), (6, 6, 20, 14))
    pygame.draw.ellipse(s, dark, (6, 6, 20, 14), 2)
    # centre hub
    pygame.draw.circle(s, (100, 70, 45), (16, 13), 3)
    # spoke lines
    pygame.draw.line(s, (100, 70, 45), (16, 13), (8,  7), 1)
    pygame.draw.line(s, (100, 70, 45), (16, 13), (24, 7), 1)
    pygame.draw.line(s, (100, 70, 45), (16, 13), (16, 6), 1)
    pygame.draw.rect(s, _darken(base, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = POTTERY_KILN_BLOCK
    # if bid == POTTERY_KILN_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    brick = (80, 60, 50)
    dark  = (45, 30, 20)
    s.fill(brick)
    # brick row lines
    for row in range(4):
        off = 4 if row % 2 == 0 else 0
        for col in range(-1, 4):
            pygame.draw.rect(s, dark, (off + col * 8, row * 8, 7, 7), 1)
    # arched mouth opening
    mouth = pygame.Rect(8, 15, 16, 13)
    pygame.draw.rect(s, (20, 12, 8), mouth)
    pygame.draw.arc(s, (20, 12, 8), (8, 9, 16, 12), 0, math.pi, 3)
    # orange glow inside
    pygame.draw.circle(s, (230, 110, 30), (16, 21), 3)
    # small chimney
    pygame.draw.rect(s, dark, (21, 1, 5, 7))
    pygame.draw.rect(s, (200, 100, 30), (22, 2, 3, 3))
    pygame.draw.rect(s, _darken(brick, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = POTTERY_DISPLAY_BLOCK
    # if bid == POTTERY_DISPLAY_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    stone  = (160, 140, 110)
    dark   = _darken(stone, 30)
    shadow = _darken(stone, 50)
    s.fill((0, 0, 0))           # transparent background (shows as black — actual bg from world)
    s.fill(stone)
    # base slab (bottom third)
    pygame.draw.rect(s, dark,   (2, 22, 28, 8))
    pygame.draw.rect(s, shadow, (2, 22, 28, 2))
    # two column pillars
    pygame.draw.rect(s, stone,  (4,  8, 6, 15))
    pygame.draw.rect(s, stone,  (22, 8, 6, 15))
    pygame.draw.rect(s, shadow, (4,  8, 1, 15))
    pygame.draw.rect(s, shadow, (22, 8, 1, 15))
    # top plate (lintel)
    pygame.draw.rect(s, dark,   (2,  6, 28, 4))
    pygame.draw.rect(s, _darken(stone, 15), s.get_rect(), 1)
    surfs[bid] = s

    bid = GARDEN_WORKSHOP_BLOCK
    # if bid == GARDEN_WORKSHOP_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    c = BLOCKS[bid]["color"]
    s.fill(_darken(c, 15))
    wood = (139, 90, 43)
    pygame.draw.rect(s, wood, (1, 4, BLOCK_SIZE-2, BLOCK_SIZE//2-4))
    pygame.draw.line(s, _darken(wood, 20), (1, 4), (BLOCK_SIZE-2, 4), 1)
    pygame.draw.rect(s, c, (0, BLOCK_SIZE//2, BLOCK_SIZE, BLOCK_SIZE//2))
    for cx2 in [6, 12, 20, 26]:
        pygame.draw.line(s, _darken(wood, 25), (cx2, 8), (cx2+2, 14), 1)
    pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
    surfs[bid] = s

    bid = SPINNING_WHEEL_BLOCK
    # if bid == SPINNING_WHEEL_BLOCK
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

    bid = DYE_VAT_BLOCK
    # if bid == DYE_VAT_BLOCK
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

    bid = LOOM_BLOCK
    # if bid == LOOM_BLOCK
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

    bid = GAMBLING_TABLE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    felt = (20, 80, 40)
    felt_light = (28, 100, 52)
    s.fill(felt)
    # Inner felt surface
    pygame.draw.rect(s, felt_light, (3, 6, BLOCK_SIZE - 6, BLOCK_SIZE - 10))
    # White border
    pygame.draw.rect(s, (255, 255, 255), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
    # Two small dice
    die_size = 9
    for dx, dy in [(5, 10), (18, 10)]:
        pygame.draw.rect(s, (235, 235, 235), (dx, dy, die_size, die_size), border_radius=2)
        pygame.draw.rect(s, (50, 50, 50), (dx, dy, die_size, die_size), 1, border_radius=2)
        # Single pip each
        pygame.draw.circle(s, (30, 30, 30), (dx + die_size // 2, dy + die_size // 2), 1)
    surfs[bid] = s

    # Racing Rail — wooden post with horizontal fence slat
    bid = RACING_RAIL
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((42, 32, 18))
    post_col = (110, 80, 45)
    slat_col = (130, 95, 55)
    pygame.draw.rect(s, post_col, (BLOCK_SIZE // 2 - 2, 0, 5, BLOCK_SIZE))  # vertical post
    pygame.draw.rect(s, slat_col, (2, BLOCK_SIZE // 2 - 2, BLOCK_SIZE - 4, 5))  # horizontal slat
    pygame.draw.rect(s, _darken(post_col, 20), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
    surfs[bid] = s

    # Bet Counter — wooden counter with a small ledger on top
    bid = BET_COUNTER
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    wood = (90, 60, 30)
    top  = (115, 80, 42)
    s.fill(wood)
    pygame.draw.rect(s, top, (1, 1, BLOCK_SIZE - 2, BLOCK_SIZE // 2))   # counter top
    # Ledger book
    pygame.draw.rect(s, (230, 220, 190), (6, 4, 12, 9), border_radius=1)
    pygame.draw.line(s, (100, 90, 70), (12, 4), (12, 13), 1)             # page spine
    # Ink lines
    for ly in [6, 8, 10]:
        pygame.draw.line(s, (80, 70, 60), (7, ly), (11, ly), 1)
        pygame.draw.line(s, (80, 70, 60), (13, ly), (17, ly), 1)
    pygame.draw.rect(s, _darken(wood, 25), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
    surfs[bid] = s

    # Starting Gate — two white posts with a red crossbar
    bid = STARTING_GATE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((42, 32, 18))
    gate_col = (210, 205, 190)
    bar_col  = (200, 55, 45)
    pygame.draw.rect(s, gate_col, (2, 0, 4, BLOCK_SIZE))           # left post
    pygame.draw.rect(s, gate_col, (BLOCK_SIZE - 6, 0, 4, BLOCK_SIZE))  # right post
    pygame.draw.rect(s, bar_col, (2, BLOCK_SIZE // 2 - 2, BLOCK_SIZE - 4, 5))  # crossbar
    pygame.draw.rect(s, _darken(gate_col, 20), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
    surfs[bid] = s

    # Winners Post — golden post with a small flag on top
    bid = WINNERS_POST
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((42, 32, 18))
    post_gold = (185, 150, 40)
    flag_col  = (220, 60, 40)
    pygame.draw.rect(s, post_gold, (BLOCK_SIZE // 2 - 2, 4, 5, BLOCK_SIZE - 4))  # post
    # Flag triangle
    pygame.draw.polygon(s, flag_col, [
        (BLOCK_SIZE // 2 + 3, 4),
        (BLOCK_SIZE // 2 + 3, 14),
        (BLOCK_SIZE // 2 + 12, 9),
    ])
    pygame.draw.rect(s, _darken(post_gold, 20), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
    surfs[bid] = s

    # Tea House — warm wooden serving counter with a paper lantern
    bid = TEA_HOUSE_BLOCK
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    wood     = BLOCKS[bid]["color"]       # (122, 92, 58) warm brown
    dark     = _darken(wood, 30)
    countertop = _darken(wood, 45)
    plank    = _darken(wood, 15)
    lantern_amber = (232, 185, 75)
    lantern_glow  = (255, 225, 120)
    s.fill(dark)
    # Counter body
    pygame.draw.rect(s, wood, (2, 14, 28, 16))
    # Plank lines on counter face
    for fy in [18, 22, 26]:
        pygame.draw.line(s, plank, (2, fy), (30, fy), 1)
    # Countertop edge
    pygame.draw.rect(s, countertop, (1, 12, 30, 3))
    # Thin cord from ceiling to lantern
    pygame.draw.line(s, _darken(wood, 20), (7, 1), (7, 8), 1)
    # Paper lantern body (small oval)
    pygame.draw.ellipse(s, lantern_amber, (3, 8, 9, 7))
    pygame.draw.ellipse(s, lantern_glow,  (5, 9, 5, 5))
    # Lantern cap/base lines
    pygame.draw.line(s, _darken(lantern_amber, 20), (3, 9), (12, 9), 1)
    pygame.draw.line(s, _darken(lantern_amber, 20), (3, 14), (12, 14), 1)
    # Counter legs
    pygame.draw.rect(s, _darken(wood, 20), (3, 30, 3, 2))
    pygame.draw.rect(s, _darken(wood, 20), (26, 30, 3, 2))
    pygame.draw.rect(s, dark, s.get_rect(), 1)
    surfs[bid] = s

    return surfs
