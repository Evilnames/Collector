import pygame
import math
import random as _rnd
from blocks import BLOCKS
from blocks import *  # all block ID constants
from constants import BLOCK_SIZE
from Render.block_helpers import _darken, _lighter, _tinted, _MSTYLES, CAVE_MUSHROOMS, render_mushroom_preview


def build_crop_surfs():
    surfs = {}
    bid = STRAWBERRY_BUSH
    # if bid == STRAWBERRY_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (40, 140, 40),  (2, 12, 28, 18))
    pygame.draw.rect(s, (55, 165, 55),  (6, 5,  20, 20))
    for bx2, by2 in [(6, 8), (14, 14), (20, 9), (23, 16)]:
        pygame.draw.rect(s, (220, 40, 70), (bx2, by2, 4, 4))
    surfs[bid] = s

    bid = WHEAT_BUSH
    # if bid == WHEAT_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    stalk_col = (160, 140, 50)
    head_col  = (220, 200, 60)
    for stx, sth in [(4, 22), (9, 18), (14, 26), (19, 20), (24, 16)]:
        pygame.draw.rect(s, stalk_col, (stx, BLOCK_SIZE - sth, 2, sth))
        pygame.draw.rect(s, head_col,  (stx - 1, BLOCK_SIZE - sth - 5, 4, 6))
    surfs[bid] = s

    bid = STRAWBERRY_CROP_YOUNG
    # if bid == STRAWBERRY_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (50, 160, 50), (15, 20, 3, 12))
    pygame.draw.rect(s, (70, 190, 70), (9,  22, 8, 4))
    pygame.draw.rect(s, (70, 190, 70), (16, 19, 8, 4))
    surfs[bid] = s

    bid = STRAWBERRY_CROP_MATURE
    # if bid == STRAWBERRY_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (50, 150, 50), (14, 10, 4, 20))
    pygame.draw.rect(s, (70, 185, 70), (5,  14, 12, 5))
    pygame.draw.rect(s, (70, 185, 70), (16, 10, 12, 5))
    for bx2, by2 in [(6, 8), (18, 6), (10, 18), (22, 14)]:
        pygame.draw.rect(s, (220, 40, 70), (bx2, by2, 5, 5))
    surfs[bid] = s

    bid = WHEAT_CROP_YOUNG
    # if bid == WHEAT_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [10, 16, 22]:
        pygame.draw.rect(s, (130, 160, 60), (stx, 18, 2, 14))
    surfs[bid] = s

    bid = WHEAT_CROP_MATURE
    # if bid == WHEAT_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [5, 10, 15, 20, 25]:
        pygame.draw.rect(s, (190, 175, 55), (stx, 8, 3, 22))
        pygame.draw.rect(s, (230, 210, 55), (stx - 1, 3, 5, 7))
    surfs[bid] = s

    bid = CARROT_BUSH
    # if bid == CARROT_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (50, 150, 50), (4, 14, 24, 16))
    for bx2 in [6, 13, 20]:
        pygame.draw.rect(s, (255, 140, 0), (bx2, 18, 5, 9))
        pygame.draw.rect(s, (80, 200, 80), (bx2 + 1, 12, 3, 7))
    surfs[bid] = s

    bid = TOMATO_BUSH
    # if bid == TOMATO_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (40, 140, 40), (2, 10, 28, 20))
    for bx2, by2 in [(5, 10), (14, 7), (21, 12), (9, 18)]:
        pygame.draw.circle(s, (210, 50, 50), (bx2, by2), 4)
    surfs[bid] = s

    bid = CORN_BUSH
    # if bid == CORN_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 26), (14, 22), (22, 24)]:
        pygame.draw.rect(s, (100, 160, 50), (stx, BLOCK_SIZE - sth, 3, sth))
        pygame.draw.rect(s, (230, 210, 55), (stx - 1, BLOCK_SIZE - sth, 5, 10))
    surfs[bid] = s

    bid = PUMPKIN_BUSH
    # if bid == PUMPKIN_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (50, 150, 50), (4, 16, 24, 14))
    for bx2, by2 in [(5, 17), (13, 14), (21, 18)]:
        pygame.draw.ellipse(s, (200, 100, 30), (bx2, by2, 8, 7))
    surfs[bid] = s

    bid = APPLE_BUSH
    # if bid == APPLE_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (40, 140, 40), (2, 8, 28, 22))
    for bx2, by2 in [(6, 10), (16, 8), (22, 14), (10, 18)]:
        pygame.draw.circle(s, (180, 40, 40), (bx2, by2), 4)
        pygame.draw.rect(s, (80, 160, 50), (bx2, by2 - 6, 2, 4))
    surfs[bid] = s

    bid = CARROT_CROP_YOUNG
    # if bid == CARROT_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [10, 16, 22]:
        pygame.draw.rect(s, (80, 190, 80), (stx, 20, 2, 12))
    surfs[bid] = s

    bid = CARROT_CROP_MATURE
    # if bid == CARROT_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [7, 14, 21]:
        pygame.draw.rect(s, (80, 190, 80), (stx, 10, 3, 12))
        pygame.draw.rect(s, (255, 140, 0), (stx, 22, 4, 8))
    surfs[bid] = s

    bid = TOMATO_CROP_YOUNG
    # if bid == TOMATO_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [10, 16, 22]:
        pygame.draw.rect(s, (70, 180, 70), (stx, 18, 2, 14))
    surfs[bid] = s

    bid = TOMATO_CROP_MATURE
    # if bid == TOMATO_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 170, 60), (12, 8, 4, 18))
    for bx2, by2 in [(5, 12), (19, 10), (8, 20), (21, 18)]:
        pygame.draw.circle(s, (210, 50, 50), (bx2, by2), 4)
    surfs[bid] = s

    bid = CORN_CROP_YOUNG
    # if bid == CORN_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [10, 16, 22]:
        pygame.draw.rect(s, (120, 170, 55), (stx, 14, 3, 18))
    surfs[bid] = s

    bid = CORN_CROP_MATURE
    # if bid == CORN_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [6, 14, 22]:
        pygame.draw.rect(s, (130, 175, 55), (stx, 4, 4, 26))
        pygame.draw.rect(s, (230, 210, 55), (stx - 1, 8, 6, 12))
    surfs[bid] = s

    bid = PUMPKIN_CROP_YOUNG
    # if bid == PUMPKIN_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (70, 180, 70), (12, 16, 3, 16))
    pygame.draw.rect(s, (80, 190, 80), (5, 20, 22, 4))
    surfs[bid] = s

    bid = PUMPKIN_CROP_MATURE
    # if bid == PUMPKIN_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 170, 60), (14, 4, 3, 12))
    pygame.draw.ellipse(s, (200, 100, 30), (4, 14, 24, 16))
    pygame.draw.rect(s, (60, 120, 40), (13, 13, 5, 4))
    surfs[bid] = s

    bid = APPLE_CROP_YOUNG
    # if bid == APPLE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 170, 60), (14, 14, 3, 18))
    pygame.draw.rect(s, (70, 185, 70), (8, 16, 16, 5))
    surfs[bid] = s

    bid = APPLE_CROP_MATURE
    # if bid == APPLE_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (50, 160, 50), (14, 4, 4, 16))
    pygame.draw.rect(s, (60, 175, 60), (6, 10, 20, 6))
    for bx2, by2 in [(6, 14), (17, 12), (10, 20), (22, 18)]:
        pygame.draw.circle(s, (180, 40, 40), (bx2, by2), 4)
        pygame.draw.rect(s, (70, 160, 50), (bx2, by2 - 5, 2, 3))
    surfs[bid] = s

    bid = RICE_BUSH
    # if bid == RICE_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 20), (10, 16), (15, 22), (20, 18), (25, 14)]:
        pygame.draw.rect(s, (120, 160, 60), (stx, BLOCK_SIZE - sth, 2, sth))
        pygame.draw.rect(s, (210, 200, 130), (stx - 1, BLOCK_SIZE - sth - 4, 4, 5))
    surfs[bid] = s

    bid = GINGER_BUSH
    # if bid == GINGER_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (80, 150, 60), (4, 12, 24, 18))
    for bx2, by2 in [(6, 18), (14, 13), (22, 19)]:
        pygame.draw.ellipse(s, (200, 160, 60), (bx2, by2, 7, 5))
    surfs[bid] = s

    bid = BOK_CHOY_BUSH
    # if bid == BOK_CHOY_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth, sw in [(6, 20, 5), (13, 24, 6), (21, 18, 5)]:
        pygame.draw.rect(s, (50, 170, 80), (stx, BLOCK_SIZE - sth, sw, sth))
        pygame.draw.rect(s, (240, 240, 210), (stx + 1, BLOCK_SIZE - sth + 2, 2, sth - 4))
    surfs[bid] = s

    bid = GARLIC_BUSH
    # if bid == GARLIC_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 22), (14, 18), (21, 20)]:
        pygame.draw.rect(s, (140, 175, 90), (stx, BLOCK_SIZE - sth, 3, sth))
        pygame.draw.ellipse(s, (230, 225, 200), (stx - 2, BLOCK_SIZE - sth - 6, 7, 7))
    surfs[bid] = s

    bid = RICE_CROP_YOUNG
    # if bid == RICE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [9, 15, 21]:
        pygame.draw.rect(s, (130, 175, 65), (stx, 16, 2, 16))
    surfs[bid] = s

    bid = RICE_CROP_MATURE
    # if bid == RICE_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [6, 12, 18, 24]:
        pygame.draw.rect(s, (150, 170, 65), (stx, 6, 3, 20))
        pygame.draw.rect(s, (220, 205, 135), (stx - 1, 1, 5, 7))
    surfs[bid] = s

    bid = GINGER_CROP_YOUNG
    # if bid == GINGER_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (90, 160, 65), (12, 14, 3, 18))
    pygame.draw.rect(s, (100, 170, 70), (6, 20, 20, 4))
    surfs[bid] = s

    bid = GINGER_CROP_MATURE
    # if bid == GINGER_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (80, 150, 60), (13, 6, 4, 16))
    pygame.draw.rect(s, (90, 160, 65), (6, 14, 20, 5))
    for bx2, by2 in [(5, 20), (13, 22), (21, 19)]:
        pygame.draw.ellipse(s, (200, 160, 60), (bx2, by2, 8, 5))
    surfs[bid] = s

    bid = BOK_CHOY_CROP_YOUNG
    # if bid == BOK_CHOY_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(9, 16), (15, 20), (21, 14)]:
        pygame.draw.rect(s, (70, 185, 80), (stx, BLOCK_SIZE - sth, 4, sth))
    surfs[bid] = s

    bid = BOK_CHOY_CROP_MATURE
    # if bid == BOK_CHOY_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (11, 28), (18, 22), (24, 20)]:
        pygame.draw.rect(s, (50, 170, 80), (stx, BLOCK_SIZE - sth, 5, sth))
        pygame.draw.rect(s, (240, 240, 210), (stx + 1, BLOCK_SIZE - sth + 3, 2, sth - 6))
    surfs[bid] = s

    bid = GARLIC_CROP_YOUNG
    # if bid == GARLIC_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [10, 16, 22]:
        pygame.draw.rect(s, (155, 185, 100), (stx, 16, 3, 16))
    surfs[bid] = s

    bid = GARLIC_CROP_MATURE
    # if bid == GARLIC_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [8, 14, 20]:
        pygame.draw.rect(s, (140, 175, 90), (stx, 8, 3, 18))
        pygame.draw.ellipse(s, (230, 225, 200), (stx - 2, 2, 8, 8))
    surfs[bid] = s

    bid = SCALLION_BUSH
    # if bid == SCALLION_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 24), (12, 20), (18, 26), (24, 18)]:
        pygame.draw.rect(s, (50, 185, 70), (stx, BLOCK_SIZE - sth, 3, sth))
        pygame.draw.rect(s, (80, 210, 100), (stx - 1, BLOCK_SIZE - sth, 5, 6))
    surfs[bid] = s

    bid = CHILI_BUSH
    # if bid == CHILI_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (50, 145, 50), (3, 10, 26, 20))
    for bx2, by2 in [(5, 12), (13, 8), (21, 13), (9, 20), (18, 18)]:
        pygame.draw.rect(s, (210, 50, 35), (bx2, by2, 3, 7))
        pygame.draw.rect(s, (80, 160, 50), (bx2 + 1, by2 - 3, 2, 4))
    surfs[bid] = s

    bid = SCALLION_CROP_YOUNG
    # if bid == SCALLION_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [9, 15, 21]:
        pygame.draw.rect(s, (60, 195, 80), (stx, 14, 3, 18))
    surfs[bid] = s

    bid = SCALLION_CROP_MATURE
    # if bid == SCALLION_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [6, 12, 18, 24]:
        pygame.draw.rect(s, (50, 185, 70), (stx, 6, 3, 24))
        pygame.draw.rect(s, (240, 240, 200), (stx + 1, 8, 2, 12))
    surfs[bid] = s

    bid = CHILI_CROP_YOUNG
    # if bid == CHILI_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [9, 15, 21]:
        pygame.draw.rect(s, (80, 178, 70), (stx, 16, 2, 16))
    surfs[bid] = s

    bid = CHILI_CROP_MATURE
    # if bid == CHILI_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 165, 60), (13, 6, 4, 18))
    pygame.draw.rect(s, (70, 178, 65), (6, 14, 20, 4))
    for bx2, by2 in [(5, 18), (14, 16), (21, 20), (10, 24)]:
        pygame.draw.rect(s, (215, 50, 35), (bx2, by2, 3, 7))
    surfs[bid] = s

    bid = PEPPER_BUSH
    # if bid == PEPPER_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (50, 145, 50), (3, 12, 26, 18))
    for bx2, by2 in [(5, 10), (12, 7), (20, 11), (8, 18), (19, 19)]:
        pygame.draw.rect(s, (220, 70, 30), (bx2, by2, 4, 8))
        pygame.draw.rect(s, (70, 165, 55), (bx2 + 1, by2 - 3, 2, 4))
    surfs[bid] = s

    bid = ONION_BUSH
    # if bid == ONION_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 22), (13, 26), (20, 20)]:
        pygame.draw.rect(s, (130, 175, 90), (stx, BLOCK_SIZE - sth, 3, sth))
    for bx2, by2 in [(5, 14), (13, 10), (20, 15)]:
        pygame.draw.ellipse(s, (175, 148, 85), (bx2, by2, 8, 6))
    surfs[bid] = s

    bid = POTATO_BUSH
    # if bid == POTATO_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (95, 165, 75), (4, 10, 24, 18))
    for bx2, by2 in [(5, 22), (12, 24), (20, 21), (9, 27)]:
        pygame.draw.ellipse(s, (160, 128, 62), (bx2, by2, 7, 5))
    surfs[bid] = s

    bid = EGGPLANT_BUSH
    # if bid == EGGPLANT_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (55, 150, 60), (3, 10, 26, 16))
    for bx2, by2 in [(5, 9), (14, 6), (21, 10), (9, 18)]:
        pygame.draw.ellipse(s, (95, 45, 135), (bx2, by2, 6, 10))
        pygame.draw.rect(s, (70, 170, 65), (bx2 + 2, by2 - 3, 2, 4))
    surfs[bid] = s

    bid = CABBAGE_BUSH
    # if bid == CABBAGE_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for bx2, by2, bw2, bh2 in [(3, 16, 14, 14), (14, 14, 15, 16), (7, 8, 18, 12)]:
        pygame.draw.ellipse(s, (75, 155, 85), (bx2, by2, bw2, bh2))
    pygame.draw.ellipse(s, (95, 175, 100), (8, 10, 16, 12))
    surfs[bid] = s

    bid = WILDFLOWER_PATCH
    # if bid == WILDFLOWER_PATCH
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

    bid = WILDFLOWER_DISPLAY_BLOCK
    # if bid == WILDFLOWER_DISPLAY_BLOCK
    # Empty vase: glass cylinder on a wooden base
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    # Wooden base
    pygame.draw.rect(s, (120, 80, 40), (6, 26, 20, 6))
    # Glass vase body
    pygame.draw.rect(s, (180, 220, 210, 100), (9, 8, 14, 18))
    pygame.draw.rect(s, (140, 190, 185, 180), (9, 8, 14, 18), 1)
    # Vase rim
    pygame.draw.rect(s, (140, 190, 185, 200), (8, 7, 16, 3))
    surfs[bid] = s

    bid = GARDEN_BLOCK
    # if bid == GARDEN_BLOCK
    # Planter box: wooden rim + dark soil interior
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    wood   = (110, 72, 38)
    wood_l = (140, 95, 50)
    soil   = (62, 42, 28)
    soil_l = (78, 55, 36)
    # Soil fill
    pygame.draw.rect(s, soil,   (3, 10, 26, 18))
    # Soil texture dots
    for dx, dy in [(6, 14), (13, 19), (20, 13), (9, 22), (17, 24)]:
        pygame.draw.rect(s, soil_l, (dx, dy, 2, 2))
    # Wooden sides (left, right, bottom)
    pygame.draw.rect(s, wood,   (0, 8, 3, 22))   # left wall
    pygame.draw.rect(s, wood,   (29, 8, 3, 22))  # right wall
    pygame.draw.rect(s, wood,   (0, 28, 32, 4))  # bottom
    # Wooden rim across the top
    pygame.draw.rect(s, wood_l, (0, 6, 32, 4))
    surfs[bid] = s

    bid = PEPPER_CROP_YOUNG
    # if bid == PEPPER_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [9, 15, 21]:
        pygame.draw.rect(s, (75, 178, 65), (stx, 16, 3, 16))
    surfs[bid] = s

    bid = PEPPER_CROP_MATURE
    # if bid == PEPPER_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 165, 55), (14, 6, 4, 18))
    pygame.draw.rect(s, (70, 178, 65), (7, 14, 18, 4))
    for bx2, by2 in [(5, 18), (14, 15), (21, 19), (10, 23)]:
        pygame.draw.rect(s, (220, 70, 30), (bx2, by2, 4, 8))
    surfs[bid] = s

    bid = ONION_CROP_YOUNG
    # if bid == ONION_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 18), (14, 22), (20, 16)]:
        pygame.draw.rect(s, (120, 185, 90), (stx, BLOCK_SIZE - sth, 3, sth))
    surfs[bid] = s

    bid = ONION_CROP_MATURE
    # if bid == ONION_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 22), (13, 26), (20, 20)]:
        pygame.draw.rect(s, (110, 175, 80), (stx, BLOCK_SIZE - sth, 3, sth))
    for bx2 in [5, 12, 19]:
        pygame.draw.ellipse(s, (175, 148, 85), (bx2, BLOCK_SIZE - 10, 9, 8))
    surfs[bid] = s

    bid = POTATO_CROP_YOUNG
    # if bid == POTATO_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [8, 14, 20]:
        pygame.draw.rect(s, (100, 170, 75), (stx, 14, 4, 18))
    surfs[bid] = s

    bid = POTATO_CROP_MATURE
    # if bid == POTATO_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (90, 160, 70), (5, 6, 6, 20))
    pygame.draw.rect(s, (90, 160, 70), (14, 4, 6, 22))
    pygame.draw.rect(s, (90, 160, 70), (22, 8, 4, 16))
    for bx2, by2 in [(3, 22), (12, 24), (21, 20)]:
        pygame.draw.ellipse(s, (160, 128, 62), (bx2, by2, 8, 6))
    surfs[bid] = s

    bid = EGGPLANT_CROP_YOUNG
    # if bid == EGGPLANT_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [8, 14, 20]:
        pygame.draw.rect(s, (85, 168, 75), (stx, 16, 3, 16))
    surfs[bid] = s

    bid = EGGPLANT_CROP_MATURE
    # if bid == EGGPLANT_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (65, 158, 60), (14, 4, 4, 20))
    pygame.draw.rect(s, (75, 165, 70), (7, 12, 18, 4))
    for bx2, by2 in [(5, 14), (16, 12), (8, 22)]:
        pygame.draw.ellipse(s, (95, 45, 135), (bx2, by2, 7, 12))
        pygame.draw.rect(s, (70, 170, 60), (bx2 + 2, by2 - 4, 2, 5))
    surfs[bid] = s

    bid = CABBAGE_CROP_YOUNG
    # if bid == CABBAGE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for bx2, by2, bw2, bh2 in [(6, 18, 10, 10), (16, 16, 12, 12)]:
        pygame.draw.ellipse(s, (90, 175, 95), (bx2, by2, bw2, bh2))
    surfs[bid] = s

    bid = CABBAGE_CROP_MATURE
    # if bid == CABBAGE_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for bx2, by2, bw2, bh2 in [(2, 16, 14, 14), (15, 14, 14, 16), (7, 8, 18, 14)]:
        pygame.draw.ellipse(s, (75, 155, 85), (bx2, by2, bw2, bh2))
    pygame.draw.ellipse(s, (95, 175, 100), (8, 9, 16, 12))
    pygame.draw.ellipse(s, (115, 190, 115), (10, 11, 12, 8))
    surfs[bid] = s

    bid = BEET_BUSH
    # if bid == BEET_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 20), (13, 24), (21, 18)]:
        pygame.draw.rect(s, (80, 140, 60), (stx, BLOCK_SIZE - sth, 3, sth - 10))
    for bx2, by2 in [(4, 18), (12, 15), (20, 19)]:
        pygame.draw.ellipse(s, (130, 25, 55), (bx2, by2, 9, 8))
        pygame.draw.rect(s, (80, 140, 60), (bx2 + 3, by2 - 4, 2, 5))
    surfs[bid] = s

    bid = BEET_CROP_YOUNG
    # if bid == BEET_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (14, 18), (21, 12)]:
        pygame.draw.rect(s, (85, 155, 65), (stx, BLOCK_SIZE - sth, 3, sth))
    surfs[bid] = s

    bid = BEET_CROP_MATURE
    # if bid == BEET_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 20), (13, 24), (21, 18)]:
        pygame.draw.rect(s, (80, 140, 60), (stx, BLOCK_SIZE - sth, 3, sth - 8))
    for bx2 in [4, 12, 20]:
        pygame.draw.ellipse(s, (130, 25, 55), (bx2, BLOCK_SIZE - 10, 9, 8))
    surfs[bid] = s

    bid = TURNIP_BUSH
    # if bid == TURNIP_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 20), (14, 24), (21, 18)]:
        pygame.draw.rect(s, (90, 155, 70), (stx, BLOCK_SIZE - sth, 3, sth - 8))
    for bx2, by2 in [(4, 17), (12, 14), (20, 18)]:
        pygame.draw.ellipse(s, (210, 188, 212), (bx2, by2, 9, 9))
        pygame.draw.ellipse(s, (170, 60, 90), (bx2, by2 + 5, 9, 4))
        pygame.draw.rect(s, (90, 155, 70), (bx2 + 3, by2 - 4, 2, 5))
    surfs[bid] = s

    bid = TURNIP_CROP_YOUNG
    # if bid == TURNIP_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (14, 18), (21, 12)]:
        pygame.draw.rect(s, (90, 165, 75), (stx, BLOCK_SIZE - sth, 3, sth))
    surfs[bid] = s

    bid = TURNIP_CROP_MATURE
    # if bid == TURNIP_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 20), (13, 24), (21, 18)]:
        pygame.draw.rect(s, (90, 155, 70), (stx, BLOCK_SIZE - sth, 3, sth - 8))
    for bx2 in [4, 12, 20]:
        pygame.draw.ellipse(s, (210, 188, 212), (bx2, BLOCK_SIZE - 11, 9, 9))
        pygame.draw.ellipse(s, (170, 60, 90), (bx2, BLOCK_SIZE - 6, 9, 4))
    surfs[bid] = s

    bid = LEEK_BUSH
    # if bid == LEEK_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, scol in [(4, (55, 180, 75)), (10, (65, 195, 85)),
                       (17, (50, 170, 70)), (23, (60, 185, 80))]:
        pygame.draw.rect(s, scol, (stx, 2, 4, 22))
        pygame.draw.rect(s, (230, 240, 220), (stx, 22, 4, 8))
    surfs[bid] = s

    bid = LEEK_CROP_YOUNG
    # if bid == LEEK_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [8, 15, 22]:
        pygame.draw.rect(s, (60, 185, 80), (stx, 10, 3, 22))
    surfs[bid] = s

    bid = LEEK_CROP_MATURE
    # if bid == LEEK_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [6, 13, 20]:
        pygame.draw.rect(s, (60, 185, 75), (stx, 2, 4, 22))
        pygame.draw.rect(s, (220, 235, 215), (stx, 22, 4, 10))
    surfs[bid] = s

    bid = ZUCCHINI_BUSH
    # if bid == ZUCCHINI_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 140, 50), (3, 12, 26, 14))
    for zx, zy in [(4, 16), (14, 13), (20, 18)]:
        pygame.draw.rect(s, (55, 130, 45), (zx, zy, 12, 5))
        pygame.draw.ellipse(s, (80, 160, 65), (zx - 1, zy - 1, 14, 7))
        pygame.draw.rect(s, (100, 180, 80), (zx + 11, zy, 3, 4))
    surfs[bid] = s

    bid = ZUCCHINI_CROP_YOUNG
    # if bid == ZUCCHINI_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [7, 14, 21]:
        pygame.draw.rect(s, (80, 170, 65), (stx, 12, 4, 20))
        pygame.draw.ellipse(s, (100, 185, 80), (stx - 2, 9, 8, 6))
    surfs[bid] = s

    bid = ZUCCHINI_CROP_MATURE
    # if bid == ZUCCHINI_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 145, 50), (5, 10, 22, 10))
    for zx, zy in [(3, 18), (14, 15)]:
        pygame.draw.rect(s, (60, 138, 48), (zx, zy, 13, 5))
        pygame.draw.ellipse(s, (78, 158, 62), (zx - 1, zy - 1, 15, 7))
        pygame.draw.rect(s, (95, 175, 75), (zx + 12, zy, 3, 4))
    surfs[bid] = s

    bid = SWEET_POTATO_BUSH
    # if bid == SWEET_POTATO_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for vx, vy in [(3, 14), (10, 10), (20, 12)]:
        pygame.draw.rect(s, (80, 155, 65), (vx, vy, 10, 3))
        pygame.draw.ellipse(s, (75, 150, 62), (vx - 1, vy - 2, 12, 7))
    for bx2, by2 in [(5, 19), (15, 16), (21, 21)]:
        pygame.draw.ellipse(s, (190, 95, 45), (bx2, by2, 9, 6))
    surfs[bid] = s

    bid = SWEET_POTATO_CROP_YOUNG
    # if bid == SWEET_POTATO_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for vx, vy in [(5, 18), (13, 14), (21, 20)]:
        pygame.draw.rect(s, (95, 170, 75), (vx, vy, 8, 3))
        pygame.draw.ellipse(s, (110, 185, 85), (vx - 1, vy - 2, 10, 6))
    surfs[bid] = s

    bid = SWEET_POTATO_CROP_MATURE
    # if bid == SWEET_POTATO_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for vx, vy in [(3, 12), (12, 8), (20, 13)]:
        pygame.draw.rect(s, (80, 155, 65), (vx, vy, 10, 3))
        pygame.draw.ellipse(s, (75, 150, 62), (vx - 1, vy - 2, 12, 7))
    for bx2, by2 in [(4, 20), (14, 17), (20, 22)]:
        pygame.draw.ellipse(s, (190, 95, 45), (bx2, by2, 10, 7))
    surfs[bid] = s

    bid = WATERMELON_BUSH
    # if bid == WATERMELON_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (55, 135, 48), (3, 16, 26, 8))
    pygame.draw.ellipse(s, (50, 128, 42), (5, 8, 22, 18))
    for sx2 in [7, 12, 17, 22]:
        pygame.draw.line(s, (35, 100, 30), (sx2, 8), (sx2 - 1, 26), 1)
    pygame.draw.ellipse(s, (210, 55, 65), (9, 12, 14, 10))
    surfs[bid] = s

    bid = WATERMELON_CROP_YOUNG
    # if bid == WATERMELON_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [6, 14, 22]:
        pygame.draw.rect(s, (65, 158, 58), (stx, 14, 4, 18))
        pygame.draw.ellipse(s, (85, 175, 72), (stx - 2, 10, 8, 7))
    surfs[bid] = s

    bid = WATERMELON_CROP_MATURE
    # if bid == WATERMELON_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.ellipse(s, (50, 128, 42), (4, 6, 24, 20))
    for sx2 in [8, 13, 18, 23]:
        pygame.draw.line(s, (35, 100, 30), (sx2, 6), (sx2 - 1, 26), 1)
    pygame.draw.rect(s, (55, 135, 48), (2, 20, 28, 6))
    surfs[bid] = s

    bid = RADISH_BUSH
    # if bid == RADISH_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 18), (13, 22), (21, 16)]:
        pygame.draw.rect(s, (75, 145, 60), (stx, BLOCK_SIZE - sth, 3, sth - 8))
    for bx2, by2 in [(4, 18), (12, 15), (20, 19)]:
        pygame.draw.ellipse(s, (215, 55, 75), (bx2, by2, 8, 8))
        pygame.draw.ellipse(s, (240, 240, 240), (bx2 + 1, by2 + 5, 6, 4))
        pygame.draw.rect(s, (75, 145, 60), (bx2 + 3, by2 - 4, 2, 5))
    surfs[bid] = s

    bid = RADISH_CROP_YOUNG
    # if bid == RADISH_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (14, 18), (21, 12)]:
        pygame.draw.rect(s, (85, 165, 70), (stx, BLOCK_SIZE - sth, 3, sth))
    surfs[bid] = s

    bid = RADISH_CROP_MATURE
    # if bid == RADISH_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 18), (13, 22), (21, 16)]:
        pygame.draw.rect(s, (75, 145, 60), (stx, BLOCK_SIZE - sth, 3, sth - 7))
    for bx2 in [4, 12, 20]:
        pygame.draw.ellipse(s, (215, 55, 75), (bx2, BLOCK_SIZE - 10, 8, 8))
        pygame.draw.ellipse(s, (240, 240, 240), (bx2 + 1, BLOCK_SIZE - 5, 6, 4))
    surfs[bid] = s

    bid = PEA_BUSH
    # if bid == PEA_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for vx, vy in [(3, 8), (12, 5), (20, 9), (6, 18), (18, 16)]:
        pygame.draw.rect(s, (85, 175, 60), (vx, vy, 10, 3))
    for px2, py2 in [(4, 12), (13, 9), (20, 13), (7, 20), (19, 19)]:
        pygame.draw.rect(s, (95, 180, 65), (px2, py2, 10, 5))
        for dot in range(3):
            pygame.draw.circle(s, (120, 200, 80), (px2 + 2 + dot * 3, py2 + 2), 2)
    surfs[bid] = s

    bid = PEA_CROP_YOUNG
    # if bid == PEA_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for vx, vy in [(5, 16), (13, 12), (21, 18)]:
        pygame.draw.rect(s, (100, 185, 70), (vx, vy, 8, 3))
        pygame.draw.ellipse(s, (115, 195, 80), (vx - 1, vy - 2, 10, 6))
    surfs[bid] = s

    bid = PEA_CROP_MATURE
    # if bid == PEA_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for vx, vy in [(3, 8), (14, 5), (20, 10)]:
        pygame.draw.rect(s, (85, 175, 60), (vx, vy, 10, 3))
    for px2, py2 in [(3, 14), (13, 11), (19, 16)]:
        pygame.draw.rect(s, (100, 182, 62), (px2, py2, 11, 5))
        for dot in range(3):
            pygame.draw.circle(s, (130, 200, 80), (px2 + 2 + dot * 3, py2 + 2), 2)
    surfs[bid] = s

    bid = CELERY_BUSH
    # if bid == CELERY_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth, scol in [(4, 28, (90, 178, 98)), (9, 30, (80, 168, 88)),
                            (15, 26, (95, 182, 102)), (21, 28, (85, 175, 95)),
                            (26, 24, (90, 178, 98))]:
        pygame.draw.rect(s, scol, (stx, BLOCK_SIZE - sth, 4, sth))
        pygame.draw.line(s, _darken(scol, 20), (stx + 2, BLOCK_SIZE - sth + 2),
                         (stx + 2, BLOCK_SIZE - 2), 1)
    surfs[bid] = s

    bid = CELERY_CROP_YOUNG
    # if bid == CELERY_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [7, 14, 21]:
        pygame.draw.rect(s, (85, 172, 92), (stx, 14, 4, 18))
        pygame.draw.line(s, (65, 148, 72), (stx + 2, 16), (stx + 2, 30), 1)
    surfs[bid] = s

    bid = CELERY_CROP_MATURE
    # if bid == CELERY_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 26), (10, 28), (16, 24), (22, 26)]:
        pygame.draw.rect(s, (90, 178, 98), (stx, BLOCK_SIZE - sth, 4, sth))
        pygame.draw.line(s, (68, 152, 75), (stx + 2, BLOCK_SIZE - sth + 2),
                         (stx + 2, BLOCK_SIZE - 2), 1)
    surfs[bid] = s

    bid = BROCCOLI_BUSH
    # if bid == BROCCOLI_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 16), (14, 20), (22, 14)]:
        pygame.draw.rect(s, (50, 125, 55), (stx, BLOCK_SIZE - sth, 4, sth - 8))
    for bx2, by2 in [(4, 10), (13, 6), (21, 11)]:
        pygame.draw.ellipse(s, (42, 118, 50), (bx2, by2, 10, 8))
        pygame.draw.ellipse(s, (55, 135, 62), (bx2 + 1, by2, 4, 4))
        pygame.draw.ellipse(s, (55, 135, 62), (bx2 + 5, by2 + 1, 4, 4))
    surfs[bid] = s

    bid = BROCCOLI_CROP_YOUNG
    # if bid == BROCCOLI_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [8, 16]:
        pygame.draw.rect(s, (60, 148, 65), (stx, 16, 4, 16))
        pygame.draw.ellipse(s, (48, 130, 55), (stx - 1, 10, 8, 8))
    surfs[bid] = s

    bid = BROCCOLI_CROP_MATURE
    # if bid == BROCCOLI_CROP_MATURE
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

    bid = CHAMOMILE_BUSH
    # if bid == CHAMOMILE_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 18), (13, 22), (22, 16)]:
        pygame.draw.rect(s, (100, 165, 75), (stx, BLOCK_SIZE - sth, 2, sth - 8))
    for fx, fy in [(3, 8), (12, 5), (20, 9)]:
        for dx, dy in [(-4,0),(4,0),(0,-4),(0,4),(-3,-3),(3,-3),(-3,3),(3,3)]:
            pygame.draw.ellipse(s, (240, 240, 220), (fx + dx, fy + dy, 4, 3))
        pygame.draw.circle(s, (230, 210, 60), (fx, fy), 3)
    surfs[bid] = s

    bid = CHAMOMILE_CROP_YOUNG
    # if bid == CHAMOMILE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (23, 12)]:
        pygame.draw.rect(s, (110, 175, 85), (stx, BLOCK_SIZE - sth, 2, sth))
    surfs[bid] = s

    bid = CHAMOMILE_CROP_MATURE
    # if bid == CHAMOMILE_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 22), (13, 26), (22, 20)]:
        pygame.draw.rect(s, (100, 165, 75), (stx, BLOCK_SIZE - sth, 2, sth - 9))
    for fx, fy in [(2, 6), (12, 2), (20, 7)]:
        for dx, dy in [(-5,0),(5,0),(0,-5),(0,5),(-3,-3),(3,-3),(-3,3),(3,3)]:
            pygame.draw.ellipse(s, (245, 245, 230), (fx + dx, fy + dy, 5, 4))
        pygame.draw.circle(s, (235, 215, 55), (fx, fy), 4)
    surfs[bid] = s

    bid = LAVENDER_BUSH
    # if bid == LAVENDER_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, (115, 145, 100), (stx, BLOCK_SIZE - sth, 2, sth - 10))
        pygame.draw.rect(s, (175, 130, 215), (stx - 1, BLOCK_SIZE - sth - 2, 4, 10))
        for dy in range(1, 9, 2):
            pygame.draw.circle(s, (195, 150, 230), (stx + 1, BLOCK_SIZE - sth - 2 + dy), 2)
    surfs[bid] = s

    bid = LAVENDER_CROP_YOUNG
    # if bid == LAVENDER_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (23, 12)]:
        pygame.draw.rect(s, (120, 150, 105), (stx, BLOCK_SIZE - sth, 2, sth))
    surfs[bid] = s

    bid = LAVENDER_CROP_MATURE
    # if bid == LAVENDER_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 26), (13, 30), (21, 24)]:
        pygame.draw.rect(s, (115, 145, 100), (stx, BLOCK_SIZE - sth, 2, sth - 12))
        pygame.draw.rect(s, (185, 140, 220), (stx - 2, BLOCK_SIZE - sth - 2, 5, 12))
        for dy in range(1, 11, 2):
            pygame.draw.circle(s, (205, 160, 235), (stx + 1, BLOCK_SIZE - sth - 2 + dy), 2)
    surfs[bid] = s

    bid = MINT_BUSH
    # if bid == MINT_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 20), (13, 24), (21, 18)]:
        pygame.draw.rect(s, (55, 180, 110), (stx, BLOCK_SIZE - sth, 3, sth - 6))
    for lx, ly in [(3, 12), (11, 8), (19, 13), (7, 18), (16, 17)]:
        pygame.draw.ellipse(s, (60, 200, 140), (lx, ly, 9, 7))
        pygame.draw.line(s, (40, 160, 110), (lx + 4, ly + 1), (lx + 4, ly + 6), 1)
    surfs[bid] = s

    bid = MINT_CROP_YOUNG
    # if bid == MINT_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (23, 12)]:
        pygame.draw.rect(s, (60, 185, 115), (stx, BLOCK_SIZE - sth, 3, sth - 4))
        pygame.draw.ellipse(s, (70, 200, 130), (stx - 2, BLOCK_SIZE - sth - 4, 7, 6))
    surfs[bid] = s

    bid = MINT_CROP_MATURE
    # if bid == MINT_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, (55, 180, 110), (stx, BLOCK_SIZE - sth, 3, sth - 7))
    for lx, ly in [(2, 8), (11, 4), (19, 9), (6, 17), (15, 15)]:
        pygame.draw.ellipse(s, (65, 210, 150), (lx, ly, 11, 8))
        pygame.draw.line(s, (45, 165, 115), (lx + 5, ly + 1), (lx + 5, ly + 7), 1)
    surfs[bid] = s

    bid = ROSEMARY_BUSH
    # if bid == ROSEMARY_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (12, 26), (20, 20)]:
        pygame.draw.rect(s, (105, 140, 80), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (125, 155, 95), (stx - 3, ny, 4, 1))
            pygame.draw.rect(s, (125, 155, 95), (stx + 2, ny + 1, 4, 1))
    surfs[bid] = s

    bid = ROSEMARY_CROP_YOUNG
    # if bid == ROSEMARY_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (23, 12)]:
        pygame.draw.rect(s, (110, 148, 85), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
            pygame.draw.rect(s, (130, 162, 98), (stx - 2, ny, 3, 1))
    surfs[bid] = s

    bid = ROSEMARY_CROP_MATURE
    # if bid == ROSEMARY_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (20, 22)]:
        pygame.draw.rect(s, (105, 140, 80), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (130, 158, 98), (stx - 4, ny, 5, 1))
            pygame.draw.rect(s, (130, 158, 98), (stx + 2, ny + 1, 5, 1))
    surfs[bid] = s

    bid = THYME_BUSH
    # if bid == THYME_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 20), (13, 24), (21, 18)]:
        pygame.draw.rect(s, ( 90, 148,  68), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (120, 172,  90), (stx - 3, ny, 4, 1))
            pygame.draw.rect(s, (120, 172,  90), (stx + 2, ny + 1, 4, 1))
    surfs[bid] = s

    bid = THYME_CROP_YOUNG
    # if bid == THYME_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (23, 12)]:
        pygame.draw.rect(s, ( 95, 152,  72), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
            pygame.draw.rect(s, (118, 168,  88), (stx - 2, ny, 3, 1))
    surfs[bid] = s

    bid = THYME_CROP_MATURE
    # if bid == THYME_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (20, 22)]:
        pygame.draw.rect(s, ( 90, 148,  68), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (125, 178,  95), (stx - 4, ny, 5, 1))
            pygame.draw.rect(s, (125, 178,  95), (stx + 2, ny + 1, 5, 1))
    surfs[bid] = s

    bid = SAGE_BUSH
    # if bid == SAGE_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(3,16,10,5),(12,12,11,6),(20,18,9,5),(6,22,8,4)]:
        pygame.draw.ellipse(s, (138, 155, 125), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (158, 175, 142), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = SAGE_CROP_YOUNG
    # if bid == SAGE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(5,20,8,4),(14,17,9,5),(20,22,7,4)]:
        pygame.draw.ellipse(s, (118, 138, 108), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (138, 158, 128), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = SAGE_CROP_MATURE
    # if bid == SAGE_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(2,13,12,6),(11,10,12,7),(20,15,10,6),(5,20,9,5)]:
        pygame.draw.ellipse(s, (142, 158, 128), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (162, 178, 148), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = BASIL_BUSH
    # if bid == BASIL_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(2,14,12,8),(13,10,12,9),(19,17,10,7),(5,21,9,6)]:
        pygame.draw.ellipse(s, ( 42, 155,  58), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, ( 58, 178,  72), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = BASIL_CROP_YOUNG
    # if bid == BASIL_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(5,18,10,7),(14,15,10,8),(20,21,8,6)]:
        pygame.draw.ellipse(s, ( 36, 138,  50), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, ( 50, 158,  65), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = BASIL_CROP_MATURE
    # if bid == BASIL_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(1,11,13,9),(12,8,13,10),(20,14,11,8),(4,19,10,7)]:
        pygame.draw.ellipse(s, ( 45, 162,  60), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, ( 62, 185,  78), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = OREGANO_BUSH
    # if bid == OREGANO_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 18), (14, 22), (22, 16)]:
        pygame.draw.rect(s, ( 82, 138,  65), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
            pygame.draw.ellipse(s, (102, 158,  78), (stx - 3, ny, 5, 3))
            pygame.draw.ellipse(s, (102, 158,  78), (stx + 2, ny + 2, 5, 3))
    surfs[bid] = s

    bid = OREGANO_CROP_YOUNG
    # if bid == OREGANO_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 12), (16, 16), (23, 10)]:
        pygame.draw.rect(s, ( 82, 138,  65), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 5):
            pygame.draw.ellipse(s, (100, 155,  75), (stx - 2, ny, 4, 3))
    surfs[bid] = s

    bid = OREGANO_CROP_MATURE
    # if bid == OREGANO_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 22), (12, 26), (21, 20)]:
        pygame.draw.rect(s, ( 82, 138,  65), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.ellipse(s, (112, 168,  85), (stx - 4, ny, 6, 3))
            pygame.draw.ellipse(s, (112, 168,  85), (stx + 2, ny + 2, 6, 3))
    surfs[bid] = s

    bid = DILL_BUSH
    # if bid == DILL_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, (108, 168,  65), (stx, BLOCK_SIZE - sth, 1, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 4, 3):
            pygame.draw.rect(s, (128, 188,  75), (stx - 4, ny, 4, 1))
            pygame.draw.rect(s, (128, 188,  75), (stx + 1, ny + 1, 4, 1))
    surfs[bid] = s

    bid = DILL_CROP_YOUNG
    # if bid == DILL_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, (108, 168,  65), (stx, BLOCK_SIZE - sth, 1, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 4, 4):
            pygame.draw.rect(s, (125, 182,  70), (stx - 3, ny, 3, 1))
    surfs[bid] = s

    bid = DILL_CROP_MATURE
    # if bid == DILL_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 26), (12, 30), (21, 24)]:
        pygame.draw.rect(s, (108, 168,  65), (stx, BLOCK_SIZE - sth, 1, sth))
        for ny in range(BLOCK_SIZE - sth + 4, BLOCK_SIZE - 4, 3):
            pygame.draw.rect(s, (138, 195,  82), (stx - 5, ny, 5, 1))
            pygame.draw.rect(s, (138, 195,  82), (stx + 1, ny + 1, 5, 1))
        pygame.draw.circle(s, (215, 198,  55), (stx + 1, BLOCK_SIZE - sth + 2), 3)
    surfs[bid] = s

    bid = FENNEL_BUSH
    # if bid == FENNEL_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, (100, 160,  60), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 4, 4):
            pygame.draw.rect(s, (120, 180,  72), (stx - 4, ny, 4, 1))
            pygame.draw.rect(s, (120, 180,  72), (stx + 2, ny + 2, 4, 1))
    surfs[bid] = s

    bid = FENNEL_CROP_YOUNG
    # if bid == FENNEL_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, (100, 160,  60), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 4, 5):
            pygame.draw.rect(s, (115, 172,  68), (stx - 3, ny, 3, 1))
    surfs[bid] = s

    bid = FENNEL_CROP_MATURE
    # if bid == FENNEL_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 26), (12, 30), (20, 24)]:
        pygame.draw.rect(s, (100, 160,  60), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 4, BLOCK_SIZE - 4, 3):
            pygame.draw.rect(s, (130, 188,  78), (stx - 4, ny, 5, 1))
            pygame.draw.rect(s, (130, 188,  78), (stx + 2, ny + 2, 5, 1))
        pygame.draw.circle(s, (210, 190,  50), (stx + 1, BLOCK_SIZE - sth + 2), 3)
    surfs[bid] = s

    bid = TARRAGON_BUSH
    # if bid == TARRAGON_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 20), (13, 24), (21, 18)]:
        pygame.draw.rect(s, ( 75, 142,  72), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 4):
            pygame.draw.rect(s, ( 95, 162,  85), (stx - 3, ny, 3, 2))
            pygame.draw.rect(s, ( 95, 162,  85), (stx + 2, ny + 2, 3, 2))
    surfs[bid] = s

    bid = TARRAGON_CROP_YOUNG
    # if bid == TARRAGON_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 14), (16, 17), (23, 12)]:
        pygame.draw.rect(s, ( 75, 142,  72), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 5):
            pygame.draw.rect(s, ( 92, 158,  82), (stx - 2, ny, 3, 2))
    surfs[bid] = s

    bid = TARRAGON_CROP_MATURE
    # if bid == TARRAGON_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (21, 22)]:
        pygame.draw.rect(s, ( 75, 142,  72), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 3):
            pygame.draw.rect(s, (102, 172,  90), (stx - 4, ny, 4, 2))
            pygame.draw.rect(s, (102, 172,  90), (stx + 2, ny + 2, 4, 2))
    surfs[bid] = s

    bid = LEMON_BALM_BUSH
    # if bid == LEMON_BALM_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(2,15,11,7),(12,11,11,8),(20,17,9,6),(5,21,8,5)]:
        pygame.draw.ellipse(s, ( 82, 175,  75), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (100, 198,  90), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = LEMON_BALM_CROP_YOUNG
    # if bid == LEMON_BALM_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(5,19,9,6),(14,16,9,7),(20,22,8,5)]:
        pygame.draw.ellipse(s, ( 78, 162,  70), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, ( 95, 182,  85), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = LEMON_BALM_CROP_MATURE
    # if bid == LEMON_BALM_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(1,12,12,8),(12,9,12,9),(20,14,10,7),(4,19,9,6)]:
        pygame.draw.ellipse(s, ( 88, 182,  80), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (108, 205,  95), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = ECHINACEA_BUSH
    # if bid == ECHINACEA_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 22), (14, 26), (22, 20)]:
        pygame.draw.rect(s, ( 95, 138,  78), (stx, BLOCK_SIZE - sth, 2, sth))
    surfs[bid] = s

    bid = ECHINACEA_CROP_YOUNG
    # if bid == ECHINACEA_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 14), (16, 18), (23, 12)]:
        pygame.draw.rect(s, ( 95, 138,  78), (stx, BLOCK_SIZE - sth, 2, sth))
        pygame.draw.ellipse(s, (105, 148,  88), (stx - 2, BLOCK_SIZE - sth, 6, 4))
    surfs[bid] = s

    bid = ECHINACEA_CROP_MATURE
    # if bid == ECHINACEA_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (13, 28), (22, 22)]:
        pygame.draw.rect(s, ( 95, 138,  78), (stx, BLOCK_SIZE - sth, 2, sth))
        pygame.draw.circle(s, (165,  65, 155), (stx + 1, BLOCK_SIZE - sth + 1), 4)
        for ang in range(0, 360, 45):
            px3 = int((stx + 1) + 6 * math.cos(math.radians(ang)))
            py3 = int((BLOCK_SIZE - sth + 1) + 6 * math.sin(math.radians(ang)))
            pygame.draw.ellipse(s, (198, 100, 185), (px3 - 2, py3 - 1, 4, 2))
    surfs[bid] = s

    bid = VALERIAN_BUSH
    # if bid == VALERIAN_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, (115, 148,  92), (stx, BLOCK_SIZE - sth, 2, sth))
    surfs[bid] = s

    bid = VALERIAN_CROP_YOUNG
    # if bid == VALERIAN_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, (115, 148,  92), (stx, BLOCK_SIZE - sth, 2, sth))
        pygame.draw.ellipse(s, (125, 158, 102), (stx - 2, BLOCK_SIZE - sth, 6, 4))
    surfs[bid] = s

    bid = VALERIAN_CROP_MATURE
    # if bid == VALERIAN_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 25), (13, 29), (21, 22)]:
        pygame.draw.rect(s, (115, 148,  92), (stx, BLOCK_SIZE - sth, 2, sth))
        pygame.draw.circle(s, (230, 230, 225), (stx + 1, BLOCK_SIZE - sth + 1), 4)
        for px3, py3 in [(-3,-2),(3,-2),(0,-4),(-3,2),(3,2)]:
            pygame.draw.circle(s, (245, 245, 240), (stx + 1 + px3, BLOCK_SIZE - sth + 1 + py3), 2)
    surfs[bid] = s

    bid = ST_JOHNS_WORT_BUSH
    # if bid == ST_JOHNS_WORT_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 20), (13, 24), (21, 18)]:
        pygame.draw.rect(s, (115, 155,  78), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 4):
            pygame.draw.ellipse(s, (125, 165,  88), (stx - 3, ny, 5, 3))
    surfs[bid] = s

    bid = ST_JOHNS_WORT_CROP_YOUNG
    # if bid == ST_JOHNS_WORT_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, (115, 155,  78), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 5):
            pygame.draw.ellipse(s, (122, 162,  85), (stx - 2, ny, 4, 3))
    surfs[bid] = s

    bid = ST_JOHNS_WORT_CROP_MATURE
    # if bid == ST_JOHNS_WORT_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (21, 22)]:
        pygame.draw.rect(s, (115, 155,  78), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 6, BLOCK_SIZE - 3, 5):
            pygame.draw.ellipse(s, (128, 168,  88), (stx - 3, ny, 5, 3))
        pygame.draw.circle(s, (228, 210,  55), (stx + 1, BLOCK_SIZE - sth + 1), 4)
        for px3, py3 in [(-4,0),(4,0),(0,-4),(0,4)]:
            pygame.draw.rect(s, (238, 220,  65), (stx + 1 + px3 - 1, BLOCK_SIZE - sth + 1 + py3 - 1, 2, 2))
    surfs[bid] = s

    bid = YARROW_BUSH
    # if bid == YARROW_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 20), (13, 24), (21, 18)]:
        pygame.draw.rect(s, (115, 155,  85), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 4):
            pygame.draw.rect(s, (125, 165,  95), (stx - 3, ny, 5, 1))
    surfs[bid] = s

    bid = YARROW_CROP_YOUNG
    # if bid == YARROW_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, (115, 155,  85), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 5):
            pygame.draw.rect(s, (122, 162,  92), (stx - 2, ny, 4, 1))
    surfs[bid] = s

    bid = YARROW_CROP_MATURE
    # if bid == YARROW_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (21, 22)]:
        pygame.draw.rect(s, (115, 155,  85), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 6, BLOCK_SIZE - 3, 4):
            pygame.draw.rect(s, (128, 168,  95), (stx - 3, ny, 5, 1))
        pygame.draw.ellipse(s, (248, 248, 242), (stx - 3, BLOCK_SIZE - sth - 2, 8, 4))
    surfs[bid] = s

    bid = BERGAMOT_BUSH
    # if bid == BERGAMOT_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, ( 98, 148,  88), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 4):
            pygame.draw.ellipse(s, (108, 158,  98), (stx - 3, ny, 5, 3))
    surfs[bid] = s

    bid = BERGAMOT_CROP_YOUNG
    # if bid == BERGAMOT_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, ( 98, 148,  88), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 5):
            pygame.draw.ellipse(s, (105, 155,  95), (stx - 2, ny, 4, 3))
    surfs[bid] = s

    bid = BERGAMOT_CROP_MATURE
    # if bid == BERGAMOT_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (21, 22)]:
        pygame.draw.rect(s, ( 98, 148,  88), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 6, BLOCK_SIZE - 3, 5):
            pygame.draw.ellipse(s, (112, 162, 100), (stx - 3, ny, 5, 3))
        pygame.draw.circle(s, (198, 105, 185), (stx + 1, BLOCK_SIZE - sth + 2), 5)
        for px3, py3 in [(-5,-2),(5,-2),(-5,2),(5,2),(0,-5)]:
            pygame.draw.ellipse(s, (215, 118, 202), (stx + 1 + px3 - 2, BLOCK_SIZE - sth + 2 + py3 - 1, 4, 2))
    surfs[bid] = s

    bid = WORMWOOD_BUSH
    # if bid == WORMWOOD_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, (148, 158, 128), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (165, 175, 145), (stx - 4, ny, 5, 1))
            pygame.draw.rect(s, (165, 175, 145), (stx + 2, ny + 1, 5, 1))
    surfs[bid] = s

    bid = WORMWOOD_CROP_YOUNG
    # if bid == WORMWOOD_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, (148, 158, 128), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
            pygame.draw.rect(s, (160, 170, 140), (stx - 2, ny, 3, 1))
    surfs[bid] = s

    bid = WORMWOOD_CROP_MATURE
    # if bid == WORMWOOD_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (20, 22)]:
        pygame.draw.rect(s, (148, 158, 128), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (178, 188, 158), (stx - 4, ny, 5, 1))
            pygame.draw.rect(s, (178, 188, 158), (stx + 2, ny + 1, 5, 1))
    surfs[bid] = s

    bid = RUE_BUSH
    # if bid == RUE_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(3,16,9,6),(12,12,10,7),(20,17,8,5),(6,22,7,5)]:
        pygame.draw.ellipse(s, (118, 148, 155), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (135, 165, 172), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = RUE_CROP_YOUNG
    # if bid == RUE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(5,19,7,5),(14,17,8,6),(20,22,6,4)]:
        pygame.draw.ellipse(s, (105, 135, 142), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (122, 152, 158), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = RUE_CROP_MATURE
    # if bid == RUE_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(2,13,10,7),(11,10,11,8),(20,15,9,6),(5,21,8,5)]:
        pygame.draw.ellipse(s, (122, 152, 160), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (140, 168, 178), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = LEMON_VERBENA_BUSH
    # if bid == LEMON_VERBENA_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, (172, 195,  70), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 4):
            pygame.draw.rect(s, (192, 215,  82), (stx - 4, ny, 5, 2))
            pygame.draw.rect(s, (192, 215,  82), (stx + 2, ny + 2, 5, 2))
    surfs[bid] = s

    bid = LEMON_VERBENA_CROP_YOUNG
    # if bid == LEMON_VERBENA_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, (172, 195,  70), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 5):
            pygame.draw.rect(s, (182, 205,  78), (stx - 3, ny, 4, 2))
    surfs[bid] = s

    bid = LEMON_VERBENA_CROP_MATURE
    # if bid == LEMON_VERBENA_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (21, 22)]:
        pygame.draw.rect(s, (172, 195,  70), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 3):
            pygame.draw.rect(s, (200, 225,  88), (stx - 5, ny, 6, 2))
            pygame.draw.rect(s, (200, 225,  88), (stx + 2, ny + 2, 6, 2))
    surfs[bid] = s

    bid = HYSSOP_BUSH
    # if bid == HYSSOP_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, ( 92, 140,  88), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 4, 4):
            pygame.draw.circle(s, (118, 145, 205), (stx + 1, ny), 2)
    surfs[bid] = s

    bid = HYSSOP_CROP_YOUNG
    # if bid == HYSSOP_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, ( 92, 140,  88), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 4, 5):
            pygame.draw.circle(s, (105, 140,  95), (stx + 1, ny), 2)
    surfs[bid] = s

    bid = HYSSOP_CROP_MATURE
    # if bid == HYSSOP_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (21, 22)]:
        pygame.draw.rect(s, ( 92, 140,  88), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 4, 3):
            pygame.draw.circle(s, (130, 155, 222), (stx + 1, ny), 3)
    surfs[bid] = s

    bid = CATNIP_BUSH
    # if bid == CATNIP_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(3,16,9,6),(12,12,10,7),(20,17,8,5),(6,22,7,5)]:
        pygame.draw.ellipse(s, (148, 168, 138), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (165, 185, 155), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = CATNIP_CROP_YOUNG
    # if bid == CATNIP_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(5,19,8,5),(14,17,8,6),(20,22,6,4)]:
        pygame.draw.ellipse(s, (135, 155, 125), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (152, 172, 142), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = CATNIP_CROP_MATURE
    # if bid == CATNIP_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(2,12,11,7),(11,9,11,8),(20,14,9,6),(4,20,9,5)]:
        pygame.draw.ellipse(s, (152, 172, 142), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (170, 190, 158), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = WOOD_SORREL_BUSH
    # if bid == WOOD_SORREL_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for cx2, cy2 in [(8,20),(16,18),(12,25),(20,23),(6,26)]:
        pygame.draw.ellipse(s, ( 72, 168,  72), (cx2-3, cy2-2, 6, 4))
        pygame.draw.ellipse(s, ( 72, 168,  72), (cx2-1, cy2-4, 4, 6))
        pygame.draw.ellipse(s, ( 72, 168,  72), (cx2+1, cy2-2, 6, 4))
    surfs[bid] = s

    bid = WOOD_SORREL_CROP_YOUNG
    # if bid == WOOD_SORREL_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for cx2, cy2 in [(8,22),(16,20),(12,27)]:
        pygame.draw.ellipse(s, ( 62, 152,  62), (cx2-2, cy2-2, 5, 3))
        pygame.draw.ellipse(s, ( 62, 152,  62), (cx2-1, cy2-4, 3, 5))
        pygame.draw.ellipse(s, ( 62, 152,  62), (cx2+1, cy2-2, 5, 3))
    surfs[bid] = s

    bid = WOOD_SORREL_CROP_MATURE
    # if bid == WOOD_SORREL_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for cx2, cy2 in [(7,18),(15,16),(11,22),(20,20),(5,24),(18,26)]:
        pygame.draw.ellipse(s, ( 78, 178,  78), (cx2-3, cy2-2, 6, 4))
        pygame.draw.ellipse(s, ( 78, 178,  78), (cx2-1, cy2-4, 4, 6))
        pygame.draw.ellipse(s, ( 78, 178,  78), (cx2+1, cy2-2, 6, 4))
    surfs[bid] = s

    bid = MARJORAM_BUSH
    # if bid == MARJORAM_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 20), (14, 24), (22, 18)]:
        pygame.draw.rect(s, ( 88, 145,  70), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
            pygame.draw.ellipse(s, (105, 162,  82), (stx - 3, ny, 5, 3))
            pygame.draw.ellipse(s, (105, 162,  82), (stx + 2, ny + 2, 5, 3))
    surfs[bid] = s

    bid = MARJORAM_CROP_YOUNG
    # if bid == MARJORAM_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 13), (16, 16), (23, 11)]:
        pygame.draw.rect(s, ( 88, 145,  70), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 5):
            pygame.draw.ellipse(s, (100, 155,  78), (stx - 2, ny, 4, 3))
    surfs[bid] = s

    bid = MARJORAM_CROP_MATURE
    # if bid == MARJORAM_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 23), (12, 27), (21, 21)]:
        pygame.draw.rect(s, ( 88, 145,  70), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.ellipse(s, (115, 172,  88), (stx - 4, ny, 6, 3))
            pygame.draw.ellipse(s, (115, 172,  88), (stx + 2, ny + 2, 6, 3))
    surfs[bid] = s

    bid = SAVORY_BUSH
    # if bid == SAVORY_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 20), (14, 23), (22, 18)]:
        pygame.draw.rect(s, ( 98, 135,  75), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (115, 152,  88), (stx - 3, ny, 4, 1))
            pygame.draw.rect(s, (115, 152,  88), (stx + 2, ny + 1, 4, 1))
    surfs[bid] = s

    bid = SAVORY_CROP_YOUNG
    # if bid == SAVORY_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 12), (16, 16), (23, 11)]:
        pygame.draw.rect(s, ( 98, 135,  75), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
            pygame.draw.rect(s, (112, 148,  85), (stx - 2, ny, 3, 1))
    surfs[bid] = s

    bid = SAVORY_CROP_MATURE
    # if bid == SAVORY_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 23), (12, 27), (21, 21)]:
        pygame.draw.rect(s, ( 98, 135,  75), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.rect(s, (125, 162,  95), (stx - 4, ny, 5, 1))
            pygame.draw.rect(s, (125, 162,  95), (stx + 2, ny + 1, 5, 1))
    surfs[bid] = s

    bid = ANGELICA_BUSH
    # if bid == ANGELICA_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(6, 24), (14, 28), (22, 22)]:
        pygame.draw.rect(s, ( 75, 152,  95), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
            pygame.draw.ellipse(s, ( 88, 168, 108), (stx - 4, ny, 6, 4))
            pygame.draw.ellipse(s, ( 88, 168, 108), (stx + 2, ny + 2, 6, 4))
    surfs[bid] = s

    bid = ANGELICA_CROP_YOUNG
    # if bid == ANGELICA_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 14), (16, 18), (23, 12)]:
        pygame.draw.rect(s, ( 75, 152,  95), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 5):
            pygame.draw.ellipse(s, ( 82, 158, 102), (stx - 3, ny, 5, 3))
    surfs[bid] = s

    bid = ANGELICA_CROP_MATURE
    # if bid == ANGELICA_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 26), (12, 30), (21, 24)]:
        pygame.draw.rect(s, ( 75, 152,  95), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 4, BLOCK_SIZE - 2, 4):
            pygame.draw.ellipse(s, ( 95, 178, 118), (stx - 5, ny, 7, 4))
            pygame.draw.ellipse(s, ( 95, 178, 118), (stx + 2, ny + 2, 7, 4))
        pygame.draw.circle(s, (238, 238, 232), (stx + 1, BLOCK_SIZE - sth + 2), 4)
    surfs[bid] = s

    bid = BORAGE_BUSH
    # if bid == BORAGE_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, ( 92, 142,  88), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 4):
            pygame.draw.ellipse(s, (102, 152,  98), (stx - 3, ny, 5, 3))
    surfs[bid] = s

    bid = BORAGE_CROP_YOUNG
    # if bid == BORAGE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, ( 92, 142,  88), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 3, 5):
            pygame.draw.ellipse(s, (100, 148,  95), (stx - 2, ny, 4, 3))
    surfs[bid] = s

    bid = BORAGE_CROP_MATURE
    # if bid == BORAGE_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (21, 22)]:
        pygame.draw.rect(s, ( 92, 142,  88), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 6, BLOCK_SIZE - 3, 5):
            pygame.draw.ellipse(s, (105, 155,  98), (stx - 3, ny, 5, 3))
        pygame.draw.circle(s, (115, 155, 220), (stx + 1, BLOCK_SIZE - sth + 2), 4)
        for px3, py3 in [(-4,0),(4,0),(0,-4),(0,4),(-3,-3),(3,-3),(-3,3),(3,3)]:
            pygame.draw.rect(s, (128, 168, 235), (stx + 1 + px3 - 1, BLOCK_SIZE - sth + 2 + py3 - 1, 2, 2))
    surfs[bid] = s

    bid = COMFREY_BUSH
    # if bid == COMFREY_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(2,14,13,8),(13,10,12,9),(20,16,10,7),(4,21,10,6)]:
        pygame.draw.ellipse(s, ( 90, 148,  85), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (105, 165,  98), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = COMFREY_CROP_YOUNG
    # if bid == COMFREY_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(4,18,11,7),(13,15,10,8),(20,21,8,6)]:
        pygame.draw.ellipse(s, ( 82, 138,  78), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, ( 95, 155,  90), (lx2+1, ly2+1, lw-2, lh-2))
    surfs[bid] = s

    bid = COMFREY_CROP_MATURE
    # if bid == COMFREY_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for lx2, ly2, lw, lh in [(1,11,14,9),(12,8,13,10),(20,14,11,8),(4,19,10,7)]:
        pygame.draw.ellipse(s, ( 92, 152,  88), (lx2, ly2, lw, lh))
        pygame.draw.ellipse(s, (108, 168, 102), (lx2+1, ly2+1, lw-2, lh-2))
    for px3, py3 in [(8,6),(16,4),(22,8)]:
        pygame.draw.ellipse(s, (158, 128, 205), (px3, py3, 4, 6))
    surfs[bid] = s

    bid = MUGWORT_BUSH
    # if bid == MUGWORT_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, (132, 148, 112), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 4):
            pygame.draw.ellipse(s, (148, 165, 128), (stx - 4, ny, 6, 3))
            pygame.draw.ellipse(s, (185, 195, 165), (stx - 4, ny, 6, 2))
    surfs[bid] = s

    bid = MUGWORT_CROP_YOUNG
    # if bid == MUGWORT_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (22, 12)]:
        pygame.draw.rect(s, (132, 148, 112), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 5):
            pygame.draw.ellipse(s, (142, 158, 122), (stx - 3, ny, 5, 3))
    surfs[bid] = s

    bid = MUGWORT_CROP_MATURE
    # if bid == MUGWORT_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (12, 28), (21, 22)]:
        pygame.draw.rect(s, (132, 148, 112), (stx, BLOCK_SIZE - sth, 2, sth))
        for ny in range(BLOCK_SIZE - sth + 2, BLOCK_SIZE - 2, 3):
            pygame.draw.ellipse(s, (158, 175, 138), (stx - 5, ny, 7, 3))
            pygame.draw.ellipse(s, (195, 205, 175), (stx - 5, ny, 7, 2))
    surfs[bid] = s

    bid = CACTUS_YOUNG
    # if bid == CACTUS_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 148, 55), (12, 4, 8, 28))
    pygame.draw.rect(s, (80, 168, 72), (13, 4, 4, 28))
    for sy in range(6, 30, 5):
        pygame.draw.rect(s, (45, 125, 42), (11, sy, 10, 1))
    surfs[bid] = s

    bid = CACTUS_MATURE
    # if bid == CACTUS_MATURE
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

    bid = DATE_PALM_BUSH
    # if bid == DATE_PALM_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (158, 128, 68), (14, 18, 4, 14))
    for ang, ly in [(-0.8, 10), (-0.3, 5), (0.3, 5), (0.8, 10), (0.0, 3)]:
        ex = int(14 + 14 * math.sin(ang))
        ey = int(10 - 10 * math.cos(abs(ang)))
        pygame.draw.line(s, (48, 175, 78), (14, 12), (ex, ey + ly), 2)
        pygame.draw.ellipse(s, (55, 185, 82), (ex - 3, ey + ly - 2, 8, 4))
    surfs[bid] = s

    bid = DATE_PALM_CROP_YOUNG
    # if bid == DATE_PALM_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (158, 128, 68), (14, 22, 4, 10))
    for ang2 in [-0.6, 0.0, 0.6]:
        ex2 = int(14 + 10 * math.sin(ang2))
        ey2 = int(16 - 8 * math.cos(abs(ang2)))
        pygame.draw.line(s, (55, 182, 80), (14, 18), (ex2, ey2), 2)
        pygame.draw.ellipse(s, (65, 192, 88), (ex2 - 2, ey2 - 2, 6, 4))
    surfs[bid] = s

    bid = DATE_PALM_CROP_MATURE
    # if bid == DATE_PALM_CROP_MATURE
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

    bid = AGAVE_BUSH
    # if bid == AGAVE_BUSH
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

    bid = AGAVE_CROP_YOUNG
    # if bid == AGAVE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for ang5, dist5 in [(-0.5, 10), (0.0, 12), (0.5, 10)]:
        ex5 = int(16 + dist5 * math.sin(ang5))
        ey5 = int(24 - dist5 * math.cos(abs(ang5)))
        pygame.draw.line(s, (70, 162, 88), (16, 26), (ex5, ey5), 4)
        pygame.draw.polygon(s, (55, 145, 75),
                            [(ex5 - 2, ey5), (ex5 + 2, ey5), (ex5, ey5 - 3)])
    surfs[bid] = s

    bid = AGAVE_CROP_MATURE
    # if bid == AGAVE_CROP_MATURE
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

    bid = SAGUARO_YOUNG
    # if bid == SAGUARO_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (52, 142, 48), (13, 2, 6, 30))
    pygame.draw.rect(s, (72, 162, 65), (14, 2, 3, 30))
    for ry in range(4, 30, 4):
        pygame.draw.rect(s, (40, 115, 38), (12, ry, 8, 1))
    surfs[bid] = s

    bid = SAGUARO_MATURE
    # if bid == SAGUARO_MATURE
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

    bid = BARREL_CACTUS_YOUNG
    # if bid == BARREL_CACTUS_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.ellipse(s, (62, 148, 55), (6, 8, 20, 22))
    pygame.draw.ellipse(s, (78, 165, 68), (8, 10, 14, 16))
    for rx in range(9, 26, 3):
        pygame.draw.line(s, (48, 122, 42), (rx, 9), (rx, 29), 1)
    for sx_off in [-3, 0, 3]:
        pygame.draw.line(s, (210, 192, 128), (16 + sx_off, 8), (16 + sx_off, 4), 1)
    surfs[bid] = s

    bid = BARREL_CACTUS_MATURE
    # if bid == BARREL_CACTUS_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.ellipse(s, (58, 142, 52), (5, 6, 22, 24))
    pygame.draw.ellipse(s, (74, 158, 64), (7, 8, 16, 18))
    for rx in range(8, 27, 3):
        pygame.draw.line(s, (45, 118, 40), (rx, 8), (rx, 29), 1)
    pygame.draw.ellipse(s, (235, 175, 35), (10, 2, 12, 7))
    pygame.draw.ellipse(s, (255, 145, 15), (12, 3, 8, 5))
    surfs[bid] = s

    bid = OCOTILLO_YOUNG
    # if bid == OCOTILLO_YOUNG
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

    bid = OCOTILLO_MATURE
    # if bid == OCOTILLO_MATURE
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

    bid = PRICKLY_PEAR_YOUNG
    # if bid == PRICKLY_PEAR_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.ellipse(s, (68, 155, 62), (5, 14, 14, 18))
    pygame.draw.ellipse(s, (72, 162, 68), (10, 5, 13, 17))
    for px_s, py_s in [(10, 18), (16, 16), (13, 22), (14, 9), (18, 12)]:
        pygame.draw.circle(s, (205, 192, 135), (px_s, py_s), 1)
    surfs[bid] = s

    bid = PRICKLY_PEAR_MATURE
    # if bid == PRICKLY_PEAR_MATURE
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

    bid = CHOLLA_YOUNG
    # if bid == CHOLLA_YOUNG
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

    bid = CHOLLA_MATURE
    # if bid == CHOLLA_MATURE
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

    bid = PALO_VERDE_YOUNG
    # if bid == PALO_VERDE_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (95, 148, 72), (14, 14, 4, 18))
    for ang_pv, base_pv in [(-0.6, 14), (0.5, 14)]:
        ex_pv = int(16 + 10 * math.sin(ang_pv))
        ey_pv = int(14 - 8 * math.cos(abs(ang_pv)))
        pygame.draw.line(s, (95, 148, 72), (16, 14), (ex_pv, ey_pv), 2)
        pygame.draw.ellipse(s, (78, 168, 62), (ex_pv - 4, ey_pv - 3, 10, 6))
    surfs[bid] = s

    bid = PALO_VERDE_MATURE
    # if bid == PALO_VERDE_MATURE
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

    bid = COFFEE_BUSH
    # if bid == COFFEE_BUSH
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

    bid = COFFEE_CROP_YOUNG
    # if bid == COFFEE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (95, 65, 40), (15, 18, 2, 14))
    pygame.draw.ellipse(s, (55, 135, 60), (6, 16, 10, 5))
    pygame.draw.ellipse(s, (55, 135, 60), (16, 14, 10, 5))
    pygame.draw.ellipse(s, (80, 165, 80), (8, 17, 6, 2))
    pygame.draw.ellipse(s, (80, 165, 80), (18, 15, 6, 2))
    surfs[bid] = s

    bid = COFFEE_CROP_MATURE
    # if bid == COFFEE_CROP_MATURE
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

    bid = GRAPEVINE_BUSH
    # if bid == GRAPEVINE_BUSH
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

    bid = GRAPEVINE_CROP_YOUNG
    # if bid == GRAPEVINE_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (100, 68, 38), (15, 10, 2, 22))
    pygame.draw.ellipse(s, (55, 135, 55), (5, 16, 10, 6))
    pygame.draw.ellipse(s, (55, 135, 55), (17, 13, 10, 6))
    pygame.draw.ellipse(s, (85, 170, 80), (7, 17, 6, 2))
    pygame.draw.ellipse(s, (85, 170, 80), (19, 14, 6, 2))
    surfs[bid] = s

    bid = GRAPEVINE_CROP_MATURE
    # if bid == GRAPEVINE_CROP_MATURE
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

    bid = FLAX_BUSH
    # if bid == FLAX_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 16), (13, 20), (21, 14)]:
        pygame.draw.rect(s, (130, 165, 195), (stx, BLOCK_SIZE - sth, 2, sth - 6))
    for fx, fy in [(4, 10), (12, 6), (21, 11)]:
        pygame.draw.ellipse(s, (140, 175, 215), (fx-3, fy-2, 8, 5))
        pygame.draw.ellipse(s, (165, 195, 230), (fx-2, fy-1, 5, 3))
    surfs[bid] = s

    bid = FLAX_CROP_YOUNG
    # if bid == FLAX_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 14), (16, 18), (24, 12)]:
        pygame.draw.rect(s, (120, 180, 140), (stx, BLOCK_SIZE - sth, 2, sth))
    surfs[bid] = s

    bid = FLAX_CROP_MATURE
    # if bid == FLAX_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 24), (13, 28), (21, 22)]:
        pygame.draw.rect(s, (145, 175, 210), (stx, BLOCK_SIZE - sth, 2, sth - 8))
        pygame.draw.ellipse(s, (155, 185, 220), (stx-3, BLOCK_SIZE - sth - 2, 8, 5))
        pygame.draw.ellipse(s, (175, 200, 235), (stx-2, BLOCK_SIZE - sth - 1, 5, 3))
    surfs[bid] = s

    bid = COTTON_BUSH
    # if bid == COTTON_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 14), (13, 18), (21, 12)]:
        pygame.draw.rect(s, (120, 155, 100), (stx, BLOCK_SIZE - sth, 2, sth - 5))
    for bx, by in [(4, 9), (12, 5), (20, 10)]:
        pygame.draw.ellipse(s, (235, 238, 225), (bx-3, by-3, 9, 7))
        pygame.draw.ellipse(s, (248, 250, 242), (bx-2, by-2, 6, 4))
    surfs[bid] = s

    bid = COTTON_CROP_YOUNG
    # if bid == COTTON_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(8, 12), (16, 16), (24, 10)]:
        pygame.draw.rect(s, (110, 175, 115), (stx, BLOCK_SIZE - sth, 2, sth))
    surfs[bid] = s

    bid = COTTON_CROP_MATURE
    # if bid == COTTON_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 22), (13, 26), (21, 20)]:
        pygame.draw.rect(s, (130, 160, 110), (stx, BLOCK_SIZE - sth, 2, sth - 7))
        pygame.draw.ellipse(s, (238, 240, 232), (stx-4, BLOCK_SIZE - sth - 4, 10, 8))
        pygame.draw.ellipse(s, (250, 252, 246), (stx-3, BLOCK_SIZE - sth - 3, 7, 5))
    surfs[bid] = s

    bid = TEA_BUSH
    # if bid == TEA_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 20), (13, 24), (22, 18)]:
        pygame.draw.rect(s, (65, 100, 50), (stx, BLOCK_SIZE - sth, 2, sth - 8))
    for lx, ly in [(2, 12), (8, 7), (16, 10), (22, 14), (6, 17), (19, 18)]:
        pygame.draw.ellipse(s, (50, 115, 45), (lx, ly, 10, 7))
        pygame.draw.ellipse(s, (70, 140, 60), (lx + 1, ly + 1, 7, 4))
    for fx, fy in [(5, 8), (18, 10)]:
        pygame.draw.circle(s, (245, 240, 220), (fx, fy), 3)
        pygame.draw.circle(s, (230, 200, 80), (fx, fy), 1)
    surfs[bid] = s

    bid = TEA_CROP_YOUNG
    # if bid == TEA_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (23, 12)]:
        pygame.draw.rect(s, (65, 105, 50), (stx, BLOCK_SIZE - sth, 2, sth - 5))
        pygame.draw.ellipse(s, (75, 135, 60), (stx - 2, BLOCK_SIZE - sth - 4, 7, 5))
    surfs[bid] = s

    bid = TEA_CROP_MATURE
    # if bid == TEA_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 24), (13, 28), (22, 22)]:
        pygame.draw.rect(s, (60, 95, 45), (stx, BLOCK_SIZE - sth, 2, sth - 10))
    for lx, ly in [(1, 10), (7, 5), (15, 8), (21, 12), (5, 16), (18, 17), (10, 14)]:
        pygame.draw.ellipse(s, (45, 110, 40), (lx, ly, 11, 8))
        pygame.draw.ellipse(s, (65, 135, 55), (lx + 1, ly + 1, 8, 5))
    for fx, fy in [(4, 6), (14, 4), (22, 8)]:
        pygame.draw.circle(s, (245, 240, 222), (fx, fy), 3)
        pygame.draw.circle(s, (225, 195, 75), (fx, fy), 1)
    surfs[bid] = s

    bid = GRAIN_CROP_BUSH
    # if bid == GRAIN_CROP_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    stalk_col = (145, 125, 55)
    head_col  = (195, 168, 50)
    for stx, sth in [(3, 20), (9, 16), (15, 24), (20, 18), (25, 14)]:
        pygame.draw.rect(s, stalk_col, (stx, BLOCK_SIZE - sth, 2, sth))
        pygame.draw.rect(s, head_col,  (stx - 1, BLOCK_SIZE - sth - 6, 4, 7))
    surfs[bid] = s

    bid = GRAIN_CROP_YOUNG
    # if bid == GRAIN_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 14), (15, 18), (23, 12)]:
        pygame.draw.rect(s, (120, 155, 50), (stx, BLOCK_SIZE - sth, 2, sth))
        pygame.draw.rect(s, (140, 175, 60), (stx - 3, BLOCK_SIZE - sth - 2, 5, 2))
    surfs[bid] = s

    bid = GRAIN_CROP_MATURE
    # if bid == GRAIN_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(3, 22), (9, 18), (15, 26), (21, 20), (26, 16)]:
        pygame.draw.rect(s, (175, 150, 50), (stx, BLOCK_SIZE - sth, 2, sth - 8))
        for gy in range(BLOCK_SIZE - sth - 1, BLOCK_SIZE - sth + 6):
            pygame.draw.rect(s, (205, 180, 55), (stx - 2, gy, 2, 1))
            pygame.draw.rect(s, (205, 180, 55), (stx + 2, gy + 1, 2, 1))
    surfs[bid] = s

    bid = CHICKPEA_CROP_YOUNG
    # if bid == CHICKPEA_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(5, 18), (14, 22), (22, 16)]:
        pygame.draw.rect(s, (80, 160, 75), (stx, BLOCK_SIZE - sth, 2, sth - 6))
    for lx, ly in [(2, 12), (6, 8), (11, 6), (16, 8), (20, 11), (24, 14), (8, 16)]:
        pygame.draw.ellipse(s, (90, 170, 80), (lx, ly, 8, 5))
    surfs[bid] = s

    bid = CHICKPEA_CROP_MATURE
    # if bid == CHICKPEA_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(4, 20), (13, 24), (22, 18)]:
        pygame.draw.rect(s, (165, 145, 90), (stx, BLOCK_SIZE - sth, 2, sth - 6))
    for px, py in [(2, 10), (7, 6), (14, 8), (20, 10), (25, 14), (10, 16), (17, 17)]:
        pygame.draw.ellipse(s, (210, 188, 140), (px, py, 9, 5))
        pygame.draw.ellipse(s, (230, 210, 165), (px + 1, py + 1, 6, 3))
    surfs[bid] = s

    bid = LENTIL_CROP_YOUNG
    # if bid == LENTIL_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [4, 12, 20]:
        pygame.draw.line(s, (80, 150, 70), (stx, 28), (stx + 6, 10), 1)
        for t in [0.3, 0.6, 0.85]:
            lx2 = int(stx + 6 * t)
            ly2 = int(28 - 18 * t)
            pygame.draw.ellipse(s, (100, 165, 85), (lx2 - 3, ly2 - 2, 6, 4))
    surfs[bid] = s

    bid = LENTIL_CROP_MATURE
    # if bid == LENTIL_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [3, 11, 20]:
        pygame.draw.line(s, (160, 95, 60), (stx, 28), (stx + 5, 8), 1)
        for t in [0.25, 0.55, 0.8]:
            lx2 = int(stx + 5 * t)
            ly2 = int(28 - 20 * t)
            pygame.draw.ellipse(s, (182, 105, 65), (lx2 - 4, ly2 - 2, 8, 4))
            pygame.draw.ellipse(s, (200, 125, 80), (lx2 - 3, ly2 - 1, 5, 3))
    surfs[bid] = s

    bid = SESAME_CROP_YOUNG
    # if bid == SESAME_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sth in [(7, 18), (15, 22), (23, 16)]:
        pygame.draw.rect(s, (75, 155, 80), (stx, BLOCK_SIZE - sth, 2, sth))
        pygame.draw.ellipse(s, (90, 170, 90), (stx - 4, BLOCK_SIZE - sth + 2, 5, 3))
        pygame.draw.ellipse(s, (90, 170, 90), (stx + 3, BLOCK_SIZE - sth + 5, 5, 3))
    surfs[bid] = s

    bid = SESAME_CROP_MATURE
    # if bid == SESAME_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pod_col = (235, 220, 175)
    for stx, sth in [(5, 24), (14, 28), (22, 22)]:
        pygame.draw.rect(s, (180, 165, 100), (stx, BLOCK_SIZE - sth, 2, sth - 6))
        for py2 in range(BLOCK_SIZE - sth + 1, BLOCK_SIZE - 6, 5):
            pygame.draw.rect(s, pod_col, (stx - 3, py2, 3, 4))
            pygame.draw.rect(s, pod_col, (stx + 3, py2 + 2, 3, 4))
    surfs[bid] = s

    bid = SAFFRON_CROP_YOUNG
    # if bid == SAFFRON_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for bx2, sth in [(5, 20), (10, 24), (16, 18), (21, 22), (26, 16)]:
        pygame.draw.rect(s, (80, 155, 85), (bx2, BLOCK_SIZE - sth, 2, sth))
    surfs[bid] = s

    bid = SAFFRON_CROP_MATURE
    # if bid == SAFFRON_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    petal = (145, 80, 185)
    petal_lt = (175, 110, 210)
    stamen = (210, 120, 25)
    for cx2, cy2 in [(7, 14), (17, 10), (25, 16)]:
        for ang in range(0, 360, 60):
            rad = math.radians(ang)
            px2 = int(cx2 + 5 * math.cos(rad))
            py2 = int(cy2 + 5 * math.sin(rad))
            pygame.draw.ellipse(s, petal, (px2 - 2, py2 - 3, 5, 6))
        pygame.draw.circle(s, petal_lt, (cx2, cy2), 3)
        pygame.draw.line(s, stamen, (cx2, cy2), (cx2, cy2 - 5), 1)
        pygame.draw.circle(s, stamen, (cx2, cy2 - 5), 1)
    for bx2, sth in [(5, 18), (15, 22), (24, 16)]:
        pygame.draw.rect(s, (75, 145, 80), (bx2, BLOCK_SIZE - sth, 1, sth - 8))
    surfs[bid] = s

    bid = HOP_VINE_BUSH
    # if bid == HOP_VINE_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    vine_col = (85, 138, 52)
    cone_col = (145, 175, 60)
    pygame.draw.line(s, vine_col, (6, 30), (10, 10), 2)
    pygame.draw.line(s, vine_col, (14, 30), (20, 8), 2)
    pygame.draw.line(s, vine_col, (22, 30), (28, 14), 2)
    for cx2, cy2 in [(10, 10), (20, 8), (27, 14)]:
        pygame.draw.ellipse(s, cone_col, (cx2 - 3, cy2, 6, 10))
        pygame.draw.ellipse(s, (165, 195, 70), (cx2 - 2, cy2 + 1, 4, 7))
    surfs[bid] = s

    bid = HOP_VINE_YOUNG
    # if bid == HOP_VINE_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    vine_col = (95, 150, 58)
    pygame.draw.line(s, vine_col, (8, 30), (12, 10), 2)
    pygame.draw.line(s, vine_col, (16, 30), (22, 6), 2)
    pygame.draw.line(s, vine_col, (24, 30), (30, 14), 2)
    for lx2, ly2 in [(8, 14), (17, 9), (25, 16), (5, 22), (20, 20)]:
        pygame.draw.ellipse(s, (110, 168, 70), (lx2 - 3, ly2 - 2, 7, 5))
    surfs[bid] = s

    bid = HOP_VINE_MATURE
    # if bid == HOP_VINE_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    vine_col = (130, 165, 52)
    cone_col = (155, 190, 52)
    pygame.draw.line(s, vine_col, (5, 30), (9, 6), 2)
    pygame.draw.line(s, vine_col, (14, 30), (20, 4), 2)
    pygame.draw.line(s, vine_col, (23, 30), (29, 10), 2)
    for cx2, cy2 in [(9, 6), (20, 4), (28, 10), (6, 16), (21, 18)]:
        pygame.draw.ellipse(s, cone_col, (cx2 - 3, cy2, 6, 12))
        for gy2 in range(cy2 + 1, cy2 + 12, 3):
            pygame.draw.line(s, (175, 210, 68), (cx2 - 2, gy2), (cx2 + 2, gy2), 1)
    surfs[bid] = s

    bid = POMEGRANATE_TREE_YOUNG
    # if bid == POMEGRANATE_TREE_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (90, 60, 35), (13, 16, 5, 16))
    pygame.draw.circle(s, (50, 125, 50), (16, 12), 11)
    pygame.draw.circle(s, (65, 145, 60), (13, 10), 7)
    pygame.draw.circle(s, (45, 115, 45), (20, 11), 7)
    surfs[bid] = s

    bid = POMEGRANATE_TREE_MATURE
    # if bid == POMEGRANATE_TREE_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (85, 55, 30), (13, 16, 5, 16))
    pygame.draw.circle(s, (45, 118, 45), (16, 12), 12)
    for fx2, fy2 in [(8, 8), (18, 6), (24, 12), (10, 16)]:
        pygame.draw.circle(s, (175, 30, 50), (fx2, fy2), 4)
        pygame.draw.circle(s, (200, 55, 65), (fx2, fy2), 2)
    surfs[bid] = s

    bid = OLIVE_TREE_YOUNG
    # if bid == OLIVE_TREE_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (105, 85, 55), (13, 20, 4, 12))
    pygame.draw.line(s, (105, 85, 55), (9, 24), (13, 20), 2)
    for lx2, ly2 in [(5, 14), (10, 8), (16, 6), (22, 10), (25, 16), (8, 18), (20, 18)]:
        pygame.draw.ellipse(s, (88, 138, 68), (lx2 - 2, ly2 - 4, 5, 8))
        pygame.draw.ellipse(s, (110, 155, 85), (lx2 - 1, ly2 - 3, 3, 6))
    surfs[bid] = s

    bid = OLIVE_TREE_MATURE
    # if bid == OLIVE_TREE_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (95, 75, 45), (12, 18, 5, 14))
    pygame.draw.line(s, (95, 75, 45), (7, 22), (12, 18), 2)
    pygame.draw.line(s, (95, 75, 45), (18, 22), (17, 18), 2)
    for lx2, ly2 in [(4, 12), (9, 6), (16, 4), (22, 8), (26, 14), (7, 18), (21, 17)]:
        pygame.draw.ellipse(s, (85, 132, 65), (lx2 - 2, ly2 - 4, 5, 8))
    for ox2, oy2 in [(6, 10), (15, 7), (23, 12), (11, 16)]:
        pygame.draw.ellipse(s, (50, 75, 42), (ox2 - 2, oy2 - 3, 4, 6))
    surfs[bid] = s

    bid = TARO_BUSH
    # if bid == TARO_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sty, pts in [
        (8,  28, [(8, 28),(4, 14),(15, 5),(22, 14),(16, 28)]),
        (22, 28, [(22, 28),(19, 14),(28, 6),(32, 14),(26, 28)]),
    ]:
        pygame.draw.polygon(s, (115, 88, 138), pts)
        pygame.draw.polygon(s, (135, 105, 158), [(pts[0][0], pts[0][1]), (pts[2][0], pts[2][1]), (pts[4][0], pts[4][1])])
        pygame.draw.line(s, (155, 125, 175), pts[0], pts[2], 1)
    surfs[bid] = s

    bid = TARO_CROP_YOUNG
    # if bid == TARO_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.line(s, (90, 148, 112), (15, 30), (15, 12), 2)
    pygame.draw.polygon(s, (95, 145, 115), [(15, 12), (4, 5), (10, 18), (20, 18), (26, 5)])
    pygame.draw.line(s, (115, 168, 132), (15, 12), (15, 5), 1)
    surfs[bid] = s

    bid = TARO_CROP_MATURE
    # if bid == TARO_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx, sty, pts in [
        (10, 30, [(10, 30),(5, 14),(16, 4),(22, 14),(18, 30)]),
        (20, 30, [(20, 30),(16, 14),(26, 5),(32, 14),(28, 30)]),
        (4,  30, [(4,  30),(0,  16),(10, 8),(15, 16),(12, 30)]),
    ]:
        pygame.draw.polygon(s, (140, 112, 162), pts)
        pygame.draw.line(s, (165, 138, 185), pts[0], pts[2], 1)
    surfs[bid] = s

    bid = BREADFRUIT_BUSH
    # if bid == BREADFRUIT_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (88, 62, 32), (14, 22, 4, 10))
    pygame.draw.circle(s, (95, 145, 65), (16, 16), 11)
    for lx2, ly2 in [(6, 10), (14, 5), (22, 9), (26, 16), (8, 18)]:
        pygame.draw.line(s, (75, 120, 50), (lx2, ly2 + 5), (lx2 + 4, ly2), 1)
        pygame.draw.line(s, (75, 120, 50), (lx2, ly2 + 5), (lx2 - 4, ly2 + 3), 1)
    surfs[bid] = s

    bid = BREADFRUIT_CROP_YOUNG
    # if bid == BREADFRUIT_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (78, 55, 28), (14, 22, 3, 10))
    for lx2, ly2, lw2, lh2 in [(4, 14, 12, 7), (17, 10, 13, 8), (2, 20, 10, 6)]:
        pygame.draw.ellipse(s, (75, 138, 58), (lx2, ly2, lw2, lh2))
        pygame.draw.line(s, (55, 115, 40), (lx2 + lw2//2, ly2), (lx2 + lw2//2, ly2 + lh2), 1)
    surfs[bid] = s

    bid = BREADFRUIT_CROP_MATURE
    # if bid == BREADFRUIT_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (80, 58, 30), (14, 18, 4, 14))
    pygame.draw.circle(s, (128, 158, 80), (16, 14), 13)
    for lx2, ly2 in [(6, 8), (14, 3), (22, 7), (27, 14), (7, 18)]:
        pygame.draw.line(s, (95, 125, 55), (lx2, ly2 + 5), (lx2 + 5, ly2), 1)
    for fx2, fy2 in [(10, 12), (20, 10)]:
        pygame.draw.circle(s, (130, 158, 82), (fx2, fy2), 5)
        _rng_bf = _rnd.Random(fx2 * 31 + fy2)
        for _ in range(8):
            bx2 = fx2 + _rng_bf.randint(-4, 4)
            by2 = fy2 + _rng_bf.randint(-4, 4)
            pygame.draw.circle(s, (100, 130, 62), (bx2, by2), 1)
    surfs[bid] = s

    bid = COCONUT_BUSH
    # if bid == COCONUT_BUSH
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    frond_col = (88, 122, 60)
    for fx2, fy2, tx2, ty2 in [(16, 20, 4, 8), (16, 20, 28, 6), (16, 20, 10, 28), (16, 20, 22, 28)]:
        pygame.draw.line(s, frond_col, (fx2, fy2), (tx2, ty2), 2)
        mx2, my2 = (fx2 + tx2) // 2, (fy2 + ty2) // 2
        pygame.draw.ellipse(s, (105, 145, 72), (mx2 - 3, my2 - 2, 6, 3))
    surfs[bid] = s

    bid = COCONUT_CROP_YOUNG
    # if bid == COCONUT_CROP_YOUNG
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (148, 118, 62), (13, 14, 5, 18))
    for ry2 in range(16, 30, 4):
        pygame.draw.rect(s, (168, 138, 78), (13, ry2, 5, 2))
    frond_col = (72, 115, 50)
    for fx2, fy2, tx2, ty2 in [(16, 14, 2, 4), (16, 14, 30, 4), (16, 14, 6, 26), (16, 14, 26, 26), (16, 14, 16, 2)]:
        pygame.draw.line(s, frond_col, (fx2, fy2), (tx2, ty2), 2)
    surfs[bid] = s

    bid = COCONUT_CROP_MATURE
    # if bid == COCONUT_CROP_MATURE
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (115, 88, 52), (13, 10, 5, 22))
    for ry2 in range(12, 30, 4):
        pygame.draw.rect(s, (135, 105, 65), (13, ry2, 5, 2))
    frond_col = (65, 108, 45)
    for tx2, ty2 in [(0, 2), (32, 2), (4, 22), (28, 22), (16, 0)]:
        pygame.draw.line(s, frond_col, (16, 10), (tx2, ty2), 2)
        mx2, my2 = (16 + tx2) // 2, (10 + ty2) // 2
        pygame.draw.ellipse(s, (80, 128, 56), (mx2 - 4, my2 - 2, 8, 4))
    for cx2, cy2 in [(11, 8), (17, 6), (21, 9)]:
        pygame.draw.circle(s, (110, 82, 48), (cx2, cy2), 4)
        pygame.draw.circle(s, (85, 62, 35), (cx2, cy2), 2)
    surfs[bid] = s

    # Premium crops — same geometry as their regular counterparts, gold sparkle added
    bid = STRAWBERRY_CROP_YOUNG_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (60, 170, 60), (15, 20, 3, 12))
    pygame.draw.rect(s, (80, 200, 80), (9, 22, 8, 4))
    pygame.draw.rect(s, (80, 200, 80), (16, 19, 8, 4))
    for sx2, sy2 in [(5, 18), (24, 15), (12, 28)]:
        pygame.draw.circle(s, (240, 215, 55), (sx2, sy2), 2)
    surfs[bid] = s

    bid = STRAWBERRY_CROP_MATURE_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (55, 162, 55), (14, 10, 4, 20))
    pygame.draw.rect(s, (75, 195, 75), (5, 14, 12, 5))
    pygame.draw.rect(s, (75, 195, 75), (16, 10, 12, 5))
    for bx2, by2 in [(6, 8), (18, 6), (10, 18), (22, 14)]:
        pygame.draw.rect(s, (255, 60, 90), (bx2, by2, 5, 5))
    for sx2, sy2 in [(3, 5), (27, 8), (14, 26)]:
        pygame.draw.circle(s, (240, 215, 55), (sx2, sy2), 2)
    surfs[bid] = s

    bid = TOMATO_CROP_YOUNG_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [10, 16, 22]:
        pygame.draw.rect(s, (80, 190, 80), (stx, 18, 2, 14))
    for sx2, sy2 in [(5, 16), (26, 20), (14, 30)]:
        pygame.draw.circle(s, (240, 215, 55), (sx2, sy2), 2)
    surfs[bid] = s

    bid = TOMATO_CROP_MATURE_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.rect(s, (65, 178, 65), (12, 8, 4, 18))
    for bx2, by2 in [(5, 12), (19, 10), (8, 20), (21, 18)]:
        pygame.draw.circle(s, (235, 65, 65), (bx2, by2), 4)
    for sx2, sy2 in [(2, 8), (28, 14), (15, 28)]:
        pygame.draw.circle(s, (240, 215, 55), (sx2, sy2), 2)
    surfs[bid] = s

    bid = WATERMELON_CROP_YOUNG_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [6, 14, 22]:
        pygame.draw.rect(s, (75, 168, 68), (stx, 14, 4, 18))
        pygame.draw.ellipse(s, (95, 185, 82), (stx - 2, 10, 8, 7))
    for sx2, sy2 in [(2, 10), (28, 12), (14, 30)]:
        pygame.draw.circle(s, (240, 215, 55), (sx2, sy2), 2)
    surfs[bid] = s

    bid = WATERMELON_CROP_MATURE_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    pygame.draw.ellipse(s, (55, 138, 48), (4, 6, 24, 20))
    for sx2 in [8, 13, 18, 23]:
        pygame.draw.line(s, (38, 108, 34), (sx2, 6), (sx2 - 1, 26), 1)
    pygame.draw.rect(s, (60, 145, 52), (2, 20, 28, 6))
    for sx2, sy2 in [(2, 4), (28, 8), (15, 28)]:
        pygame.draw.circle(s, (240, 215, 55), (sx2, sy2), 2)
    surfs[bid] = s

    bid = CORN_CROP_YOUNG_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [10, 16, 22]:
        pygame.draw.rect(s, (130, 180, 60), (stx, 14, 3, 18))
    for sx2, sy2 in [(5, 12), (27, 16), (14, 30)]:
        pygame.draw.circle(s, (240, 215, 55), (sx2, sy2), 2)
    surfs[bid] = s

    bid = CORN_CROP_MATURE_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [6, 14, 22]:
        pygame.draw.rect(s, (138, 182, 58), (stx, 4, 4, 26))
        pygame.draw.rect(s, (240, 218, 62), (stx - 1, 8, 6, 12))
    for sx2, sy2 in [(2, 4), (28, 6), (16, 28)]:
        pygame.draw.circle(s, (255, 240, 80), (sx2, sy2), 2)
    surfs[bid] = s

    bid = RICE_CROP_YOUNG_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [9, 15, 21]:
        pygame.draw.rect(s, (140, 185, 72), (stx, 16, 2, 16))
    for sx2, sy2 in [(4, 14), (26, 18), (15, 30)]:
        pygame.draw.circle(s, (240, 215, 55), (sx2, sy2), 2)
    surfs[bid] = s

    bid = RICE_CROP_MATURE_P
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for stx in [6, 12, 18, 24]:
        pygame.draw.rect(s, (158, 178, 70), (stx, 6, 3, 20))
        pygame.draw.rect(s, (228, 212, 142), (stx - 1, 1, 5, 7))
    for sx2, sy2 in [(2, 4), (28, 2), (15, 28)]:
        pygame.draw.circle(s, (240, 215, 55), (sx2, sy2), 2)
    surfs[bid] = s

    return surfs
