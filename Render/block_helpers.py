import pygame
import random as _rnd
from blocks import (BLOCKS, CAVE_MUSHROOMS,
    CAVE_MUSHROOM, EMBER_CAP, PALE_GHOST, GOLD_CHANTERELLE, COBALT_CAP,
    MOSSY_CAP, VIOLET_CROWN, BLOOD_CAP, SULFUR_DOME, IVORY_BELL, ASH_BELL,
    TEAL_BELL, RUST_SHELF, COPPER_SHELF, OBSIDIAN_SHELF, COAL_PUFF, STONE_PUFF,
    AMBER_PUFF, SULFUR_TUFT, HONEY_CLUSTER, CORAL_TUFT, BONE_STALK, MAGMA_CAP,
    DEEP_INK, BIOLUME)
from constants import BLOCK_SIZE

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
