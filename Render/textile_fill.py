"""Tiny weave-overlay helper shared by NPC renderers.

Mirrors the textile-codex `_draw_textured_region` from worldScene/scene.py
so any draw_npc_* function can fill a torso/hem/cuff rect with the same
patterns the player weaves on a loom.  Patterns are pixel-cheap and clamp
to short rects (sleeves, trim bands).
"""

import pygame


def draw_textured_rect(screen, x, y, w, h, base_col, texture):
    """Fill (x, y, w, h) with base_col, then overlay a weave pattern."""
    pygame.draw.rect(screen, base_col, (x, y, w, h))
    if not texture or texture == "plain" or w < 3 or h < 3:
        return

    lum = (base_col[0] + base_col[1] + base_col[2]) // 3
    if lum < 140:
        hi = tuple(min(255, c + 55) for c in base_col)
    else:
        hi = tuple(max(0, c - 45) for c in base_col)
    dk = tuple(max(0, c - 35) for c in base_col)
    r = pygame.draw.rect

    if texture == "twill":
        for offset in range(-(h - 1), w, 3):
            for row in range(h):
                col = offset + row
                if 0 <= col < w:
                    r(screen, hi, (x + col, y + row, 1, 1))

    elif texture == "tartan":
        for row in range(0, h, 3):
            r(screen, hi, (x, y + row, w, 1))
        for col in range(0, w, 3):
            r(screen, dk, (x + col, y, 1, h))

    elif texture == "herringbone":
        for row in range(h):
            d = 1 if (row // 2) % 2 == 0 else -1
            start = (row * d % 3 + 3) % 3
            col = start
            while 0 <= col < w:
                r(screen, hi, (x + col, y + row, 1, 1))
                col += 3

    elif texture == "damask":
        for row in range(0, h, 3):
            for col in range(0, w, 3):
                r(screen, hi, (x + col, y + row, 1, 1))

    elif texture == "diamond":
        for cy in range(0, h, 5):
            for cx in range(0, w, 5):
                mx, my = x + cx + 2, y + cy + 2
                for dx, dy in ((0, -2), (2, 0), (0, 2), (-2, 0)):
                    if x <= mx + dx < x + w and y <= my + dy < y + h:
                        r(screen, hi, (mx + dx, my + dy, 1, 1))

    elif texture == "brocade":
        for cy in range(2, h, 4):
            for cx in range(2, w, 4):
                mx, my = x + cx, y + cy
                if x <= mx < x + w and y <= my < y + h:
                    r(screen, hi, (mx, my, 1, 1))
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    if x <= mx + dx < x + w and y <= my + dy < y + h:
                        r(screen, hi, (mx + dx, my + dy, 1, 1))
                for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
                    if x <= mx + dx < x + w and y <= my + dy < y + h:
                        r(screen, dk, (mx + dx, my + dy, 1, 1))

    elif texture == "stripes":
        for row in range(0, h, 3):
            r(screen, hi, (x, y + row, w, 1))

    elif texture == "dots":
        for row in range(1, h, 4):
            for col in range(1, w, 4):
                r(screen, hi, (x + col, y + row, 1, 1))


def draw_trim_band(screen, x, y, w, h, base_col, texture):
    """Same as draw_textured_rect but uses the trim-friendly subset.

    Kept as a thin alias so call sites read clearly at the hem/cuff lines.
    """
    draw_textured_rect(screen, x, y, w, h, base_col, texture)
