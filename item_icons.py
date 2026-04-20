"""Procedural pixel-art icons for inventory items."""
import math
import random
import pygame

_cache: dict = {}


def _lighter(c, amt=60):
    return (min(255, c[0] + amt), min(255, c[1] + amt), min(255, c[2] + amt))

def _darker(c, amt=50):
    return (max(0, c[0] - amt), max(0, c[1] - amt), max(0, c[2] - amt))


# ---------------------------------------------------------------------------
# Shape primitives
# ---------------------------------------------------------------------------

def _gem(surf, color, s):
    cx, cy = s // 2, s // 2
    hw = s * 8 // 22
    pts = [
        (cx,       cy - s * 18 // 40),
        (cx + hw,  cy - s * 4 // 40),
        (cx + s * 6 // 22, cy + s * 14 // 40),
        (cx,       cy + s * 18 // 40),
        (cx - s * 6 // 22, cy + s * 14 // 40),
        (cx - hw,  cy - s * 4 // 40),
    ]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _lighter(color, 100), pts[0], pts[1], 1)
    pygame.draw.line(surf, _lighter(color, 100), pts[0], pts[5], 1)
    pygame.draw.line(surf, _lighter(color, 60), (cx - 2, cy - s // 7), (cx + 3, cy - s // 6), 2)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 1)


def _chunk(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 9 // 25
    offsets = [-2, 4, -5, 3, -3, 5, -4, 2]
    pts = []
    for i in range(8):
        angle = math.tau * i / 8 - math.pi / 8
        rr = r + offsets[i]
        pts.append((cx + int(rr * math.cos(angle)), cy + int(rr * math.sin(angle))))
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _lighter(color, 80), pts[7], pts[0], 2)
    pygame.draw.line(surf, _lighter(color, 80), pts[0], pts[1], 2)
    pygame.draw.polygon(surf, _darker(color, 35), pts, 1)


def _slab(surf, color, s):
    pad = s // 7
    r = pygame.Rect(pad, pad * 2, s - pad * 2, s - pad * 3)
    pygame.draw.rect(surf, color, r)
    pygame.draw.line(surf, _lighter(color), r.topleft, r.topright, 2)
    pygame.draw.line(surf, _lighter(color), r.topleft, r.bottomleft, 1)
    pygame.draw.line(surf, _darker(color), r.bottomleft, r.bottomright, 2)
    pygame.draw.line(surf, _darker(color), r.topright, r.bottomright, 1)
    pygame.draw.rect(surf, (0, 0, 0), r, 1)


def _round_food(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 9 // 25
    pygame.draw.circle(surf, color, (cx, cy), r)
    pygame.draw.circle(surf, _lighter(color, 80), (cx - r // 3, cy - r // 3), r // 4)
    pygame.draw.circle(surf, _darker(color, 40), (cx, cy), r, 1)


def _bowl(surf, color, s):
    cx = s // 2
    pad = s // 6
    rim_y = s * 6 // 20
    depth = s * 8 // 20
    r = s // 2 - pad
    pts = [(cx - r, rim_y)]
    for i in range(11):
        a = math.pi * i / 10
        pts.append((cx + int(r * math.cos(math.pi - a)),
                    rim_y + int(depth * math.sin(math.pi - a))))
    pts.append((cx + r, rim_y))
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _darker(color, 40), (cx - r, rim_y), (cx + r, rim_y), 2)
    pygame.draw.line(surf, _lighter(color, 50),
                     (cx - r // 2, rim_y + depth // 2), (cx + r // 2, rim_y + depth // 2), 1)


def _bread(surf, color, s):
    cx = s // 2
    pad = s // 7
    r = s // 2 - pad
    base_y = s * 11 // 20
    pygame.draw.rect(surf, color, (pad, base_y, r * 2, s - base_y - pad))
    pygame.draw.ellipse(surf, color, (pad, base_y - r // 2, r * 2, r))
    score = _darker(color, 40)
    pygame.draw.line(surf, score, (cx, base_y - r // 2 + 3), (cx, s - pad - 2), 1)
    pygame.draw.ellipse(surf, _darker(color, 30), (pad, base_y - r // 2, r * 2, r), 1)


def _lumber(surf, color, s):
    pad = s // 6
    r = pygame.Rect(pad, pad, s - pad * 2, s - pad * 2)
    pygame.draw.rect(surf, color, r)
    grain = _darker(color, 30)
    for dy in range(pad + 5, s - pad, 7):
        pygame.draw.line(surf, grain, (pad + 2, dy), (s - pad - 2, dy), 1)
    pygame.draw.rect(surf, _darker(color, 60), r, 2)


def _ladder(surf, color, s):
    pad = s // 6
    pygame.draw.line(surf, color, (pad + 4, pad), (pad + 4, s - pad), 3)
    pygame.draw.line(surf, color, (s - pad - 4, pad), (s - pad - 4, s - pad), 3)
    for y in range(pad + 4, s - pad, 8):
        pygame.draw.line(surf, _lighter(color, 20), (pad + 4, y), (s - pad - 4, y), 2)


def _ingot(surf, color, s):
    pad = s // 6
    pts = [(pad + 4, s - pad), (s - pad - 4, s - pad),
           (s - pad, pad), (pad, pad)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _lighter(color, 90), pts[3], pts[2], 2)
    pygame.draw.line(surf, _lighter(color, 90), pts[3], pts[0], 1)
    pygame.draw.polygon(surf, _darker(color, 50), pts, 1)


def _machine(surf, color, s):
    pad = s // 8
    r = pygame.Rect(pad, pad, s - pad * 2, s - pad * 2)
    pygame.draw.rect(surf, color, r)
    inner = pygame.Rect(pad * 3, pad * 3, s // 3, s // 3)
    pygame.draw.rect(surf, _darker(color, 50), inner)
    pygame.draw.rect(surf, _lighter(color, 30), inner, 1)
    pygame.draw.circle(surf, _darker(color, 40), (s - pad * 3, s - pad * 3), 4)
    pygame.draw.rect(surf, _darker(color, 60), r, 2)


# ---------------------------------------------------------------------------
# Item-specific icons
# ---------------------------------------------------------------------------

def _icon_dirt(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 9 // 25
    offs = [0, 4, -2, 5, -3, 3, -4, 2, 0, -3, 2, -5]
    pts = []
    for i in range(12):
        a = math.tau * i / 12
        rr = r + offs[i]
        pts.append((cx + int(rr * math.cos(a)), cy + int(rr * math.sin(a))))
    pygame.draw.polygon(surf, color, pts)
    dark = _darker(color, 30)
    for dx, dy in [(-5, -3), (4, 2), (-2, 5), (5, -4)]:
        pygame.draw.circle(surf, dark, (cx + dx, cy + dy), 2)
    pygame.draw.polygon(surf, _darker(color, 50), pts, 1)


def _icon_coal(surf, color, s):
    _chunk(surf, color, s)
    cx, cy = s // 2, s // 2
    pygame.draw.ellipse(surf, (80, 80, 95), (cx - s // 6, cy - s // 5, s // 5, s // 8))


def _icon_crystal(surf, color, s):
    cx = s // 2
    pts = [(cx, s // 8), (cx + s // 5, s // 3), (cx + s // 6, s * 4 // 5),
           (cx, s * 7 // 8), (cx - s // 6, s * 4 // 5), (cx - s // 5, s // 3)]
    pygame.draw.polygon(surf, color, pts)
    bright = _lighter(color, 90)
    pygame.draw.line(surf, bright, (cx, s // 8 + 3), (cx + s // 8, s // 3), 1)
    pygame.draw.line(surf, bright, (cx, s // 8 + 3), (cx - s // 8, s // 3), 1)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 1)


def _icon_sapling(surf, color, s):
    cx = s // 2
    pygame.draw.rect(surf, (100, 65, 25), (cx - 2, s * 11 // 20, 4, s * 8 // 20))
    pygame.draw.circle(surf, color, (cx, s * 9 // 20), s * 4 // 20)
    pygame.draw.circle(surf, _lighter(color, 50), (cx - 3, s * 7 // 20), s // 10)
    pygame.draw.circle(surf, _darker(color, 30), (cx, s * 9 // 20), s * 4 // 20, 1)


def _icon_strawberry(surf, color, s):
    cx, cy = s // 2, s * 11 // 20
    r = s * 5 // 20
    pygame.draw.circle(surf, color, (cx - r // 2, cy - r // 3), r // 2 + 2)
    pygame.draw.circle(surf, color, (cx + r // 2, cy - r // 3), r // 2 + 2)
    pts = [(cx - r, cy - r // 4), (cx + r, cy - r // 4), (cx, cy + r + 2)]
    pygame.draw.polygon(surf, color, pts)
    seed_c = _lighter(color, 110)
    for sx, sy in [(cx - 3, cy - 1), (cx + 3, cy - 3), (cx, cy + 4), (cx - 5, cy + 3), (cx + 5, cy + 2)]:
        pygame.draw.circle(surf, seed_c, (sx, sy), 1)
    pygame.draw.line(surf, (50, 160, 50), (cx, cy - r // 2 - 2), (cx, cy - r // 2 - 8), 2)


def _icon_wheat(surf, color, s):
    cx = s // 2
    pygame.draw.line(surf, _darker(color, 20), (cx, s * 9 // 10), (cx, s // 5), 2)
    for ox, oy in [(-4, 0), (-4, -5), (-4, -10), (4, 0), (4, -5), (4, -10), (0, -15)]:
        pygame.draw.ellipse(surf, color, (cx + ox - 3, s // 5 + oy, 6, 4))
    pygame.draw.line(surf, _darker(color, 20), (cx, s * 4 // 10), (cx - 6, s // 3), 1)
    pygame.draw.line(surf, _darker(color, 20), (cx, s * 4 // 10), (cx + 6, s // 3), 1)


def _icon_carrot(surf, color, s):
    pts = [(s * 3 // 8, s // 5), (s * 5 // 8, s // 5), (s // 2, s * 9 // 10)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _lighter(color, 60), (s * 7 // 16, s // 4), (s * 7 // 16, s * 3 // 4), 1)
    for i in range(3):
        ox = (i - 1) * 5
        pygame.draw.line(surf, (40, 160, 40),
                         (s // 2 + ox, s // 5),
                         (s // 2 + ox + (i - 1) * 3, s // 5 - 7 - i), 2)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 1)


def _icon_tomato(surf, color, s):
    cx, cy = s // 2, s * 11 // 20
    r = s * 8 // 20
    pygame.draw.circle(surf, color, (cx, cy), r)
    pygame.draw.circle(surf, _lighter(color, 60), (cx - r // 3, cy - r // 3), r // 4)
    pygame.draw.line(surf, (60, 140, 40), (cx, cy - r), (cx, cy - r - 5), 2)
    for ang_deg in [0, 72, 144, 216, 288]:
        rad = math.radians(ang_deg)
        pygame.draw.line(surf, (60, 160, 40),
                         (cx, cy - r),
                         (cx + int(6 * math.cos(rad)), cy - r + int(6 * math.sin(rad))), 1)
    pygame.draw.circle(surf, _darker(color, 40), (cx, cy), r, 1)


def _icon_corn(surf, color, s):
    cx = s // 2
    pts = [(cx - s // 6, s // 4), (cx + s // 6, s // 4),
           (cx + s // 8, s * 3 // 5), (cx - s // 8, s * 3 // 5)]
    pygame.draw.polygon(surf, color, pts)
    dark = _darker(color, 40)
    for row in range(4):
        for col in range(2):
            pygame.draw.circle(surf, dark, (cx - 3 + col * 7, s // 4 + 4 + row * 6), 2)
    pygame.draw.line(surf, (60, 140, 40), (cx, s // 4), (cx - 8, s // 4 - 7), 3)
    pygame.draw.line(surf, (60, 140, 40), (cx, s // 4), (cx + 8, s // 4 - 5), 2)
    pygame.draw.polygon(surf, dark, pts, 1)


def _icon_pumpkin(surf, color, s):
    cx, cy = s // 2, s // 2 + 2
    r = s * 9 // 25
    for ox in [-r // 2, 0, r // 2]:
        pygame.draw.ellipse(surf, color, (cx + ox - r // 2, cy - r, r, r * 2))
    pygame.draw.ellipse(surf, _darker(color, 30), (cx - r * 7 // 8, cy - r, r * 7 // 4, r * 2), 1)
    pygame.draw.rect(surf, (80, 50, 20), (cx - 2, cy - r - 6, 4, 8))


def _icon_apple(surf, color, s):
    cx, cy = s // 2, s * 11 // 20
    r = s * 8 // 20
    pygame.draw.circle(surf, color, (cx, cy), r)
    pygame.draw.circle(surf, _lighter(color, 70), (cx - r // 3, cy - r // 3), r // 4)
    pygame.draw.line(surf, (80, 50, 20), (cx, cy - r), (cx + 2, cy - r - 5), 2)
    leaf = [(cx + 2, cy - r - 4), (cx + 9, cy - r - 8), (cx + 4, cy - r - 2)]
    pygame.draw.polygon(surf, (50, 160, 50), leaf)
    pygame.draw.circle(surf, _darker(color, 50), (cx, cy), r, 1)


def _icon_egg(surf, color, s):
    cx, cy = s // 2, s // 2 + 2
    pygame.draw.ellipse(surf, color, (cx - s * 6 // 20, cy - s * 8 // 20, s * 12 // 20, s * 16 // 20))
    pygame.draw.ellipse(surf, _lighter(color, 60),
                        (cx - s * 4 // 20, cy - s * 6 // 20, s * 4 // 20, s * 5 // 20))
    pygame.draw.ellipse(surf, _darker(color, 30),
                        (cx - s * 6 // 20, cy - s * 8 // 20, s * 12 // 20, s * 16 // 20), 1)


def _icon_mushroom(surf, color, s):
    cx = s // 2
    pygame.draw.rect(surf, (220, 205, 175), (cx - s // 10, s * 11 // 20, s // 5, s * 9 // 25))
    r = s * 9 // 25
    pygame.draw.ellipse(surf, color, (cx - r, s * 5 // 20, r * 2, r))
    for sx, sy in [(cx - 5, s * 6 // 20), (cx + 5, s * 7 // 20), (cx, s * 5 // 20 + 4)]:
        pygame.draw.circle(surf, _lighter(color, 110), (sx, sy), 3)
    pygame.draw.ellipse(surf, _darker(color, 40), (cx - r, s * 5 // 20, r * 2, r), 1)


def _icon_rice(surf, color, s):
    cx, cy = s // 2, s // 2
    for gx, gy, rot in [(cx - 6, cy - 4, 0.3), (cx + 5, cy - 6, -0.2), (cx, cy + 2, 0.1),
                         (cx - 7, cy + 5, 0.5), (cx + 6, cy + 4, -0.3), (cx - 1, cy - 9, 0.0)]:
        pts = [
            (gx + int(5 * math.cos(rot)),                gy + int(5 * math.sin(rot))),
            (gx + int(3 * math.cos(rot + math.pi / 2)),  gy + int(3 * math.sin(rot + math.pi / 2))),
            (gx + int(5 * math.cos(rot + math.pi)),      gy + int(5 * math.sin(rot + math.pi))),
            (gx + int(3 * math.cos(rot + 3 * math.pi / 2)), gy + int(3 * math.sin(rot + 3 * math.pi / 2))),
        ]
        pygame.draw.polygon(surf, color, pts)


def _icon_ginger(surf, color, s):
    cx, cy = s // 2, s // 2
    pygame.draw.ellipse(surf, color, (s // 6, cy - s // 6, s * 2 // 3, s // 3))
    pygame.draw.ellipse(surf, color, (s // 4, cy - s // 4, s // 4, s // 5))
    pygame.draw.ellipse(surf, color, (s // 2, cy + s // 10, s // 4, s // 5))
    pygame.draw.ellipse(surf, _darker(color, 30), (s // 6, cy - s // 6, s * 2 // 3, s // 3), 1)


def _icon_bok_choy(surf, color, s):
    cx = s // 2
    stem_c = (220, 230, 210)
    for ox in [-6, 0, 6]:
        pygame.draw.line(surf, stem_c, (cx + ox, s * 9 // 10), (cx + ox, s // 2), 3)
    for ox in [-7, 0, 7]:
        pts = [(cx + ox - 6, s // 2), (cx + ox + 6, s // 2),
               (cx + ox + 3, s // 5), (cx + ox - 3, s // 5)]
        pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _darker(color, 30), (cx, s // 2), (cx, s // 5), 1)


def _icon_garlic(surf, color, s):
    cx, cy = s // 2, s * 11 // 20
    r = s * 8 // 22
    pygame.draw.ellipse(surf, color, (cx - r, cy - r, r * 2, r * 2))
    clove = _darker(color, 30)
    pygame.draw.line(surf, clove, (cx, cy - r + 2), (cx, cy + r - 2), 1)
    pygame.draw.line(surf, clove, (cx - r // 2, cy - r // 3), (cx - r // 2, cy + r // 2), 1)
    pygame.draw.line(surf, clove, (cx + r // 2, cy - r // 3), (cx + r // 2, cy + r // 2), 1)
    pygame.draw.line(surf, (100, 130, 60), (cx - 2, cy - r), (cx, cy - r - 7), 2)
    pygame.draw.line(surf, (100, 130, 60), (cx + 2, cy - r), (cx, cy - r - 7), 2)
    pygame.draw.ellipse(surf, _darker(color, 40), (cx - r, cy - r, r * 2, r * 2), 1)


def _icon_scallion(surf, color, s):
    cx = s // 2
    for ox in [-5, 0, 5]:
        pygame.draw.line(surf, color, (cx + ox, s * 9 // 10), (cx + ox + ox // 2, s // 8), 2)
    pygame.draw.ellipse(surf, (240, 240, 230), (cx - 8, s * 3 // 4, 16, 10))
    pygame.draw.ellipse(surf, (180, 180, 170), (cx - 8, s * 3 // 4, 16, 10), 1)


def _icon_chili(surf, color, s):
    cx = s // 2
    pts = [(cx - 2, s // 5), (cx + 6, s // 4), (cx + 10, s // 2),
           (cx + 5, s * 3 // 4), (cx, s * 7 // 8),
           (cx - 5, s * 3 // 4), (cx - 8, s // 2), (cx - 4, s // 4)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _lighter(color, 60), (cx - 1, s // 4), (cx + 2, s * 3 // 5), 1)
    pygame.draw.line(surf, (60, 140, 40), (cx - 2, s // 5), (cx - 4, s // 10), 2)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 1)


def _icon_seed(surf, color, s):
    cx, cy = s // 2, s // 2
    pygame.draw.ellipse(surf, color, (cx - s // 5, cy - s // 6, s * 2 // 5, s // 3))
    pygame.draw.ellipse(surf, _lighter(color, 60),
                        (cx - s // 7, cy - s // 8, s // 7, s // 8))
    pygame.draw.ellipse(surf, _darker(color, 40), (cx - s // 5, cy - s // 6, s * 2 // 5, s // 3), 1)


def _icon_pickaxe(surf, color, s):
    wood = (139, 90, 43)
    pygame.draw.line(surf, wood, (s * 3 // 4 - 2, s * 3 // 4 - 2), (s // 4 + 2, s // 4 + 2), 4)
    hx, hy = s * 3 // 4 - 3, s // 4 + 3
    pygame.draw.line(surf, color, (hx, hy), (hx - s // 5, hy - s // 5), 6)
    pygame.draw.line(surf, color, (hx, hy), (hx + s // 6, hy + s // 6), 4)
    pygame.draw.line(surf, color, (hx - s // 8, hy + s // 8), (hx + s // 8, hy - s // 8), 5)
    pygame.draw.line(surf, _lighter(color, 70),
                     (hx - s // 5 + 2, hy - s // 5 + 2), (hx - 2, hy - 2), 1)


def _icon_axe(surf, color, s):
    wood = (139, 90, 43)
    pygame.draw.line(surf, wood, (s // 4 + 2, s * 3 // 4 - 2), (s * 3 // 4 - 2, s // 4 + 2), 4)
    hx, hy = s // 4 + 3, s * 3 // 4 - 3
    blade_pts = [
        (hx,          hy),
        (hx - s // 5, hy - s // 5),
        (hx - s // 5, hy - s // 3),
        (hx + s // 8, hy - s // 3),
        (hx + s // 8, hy - s // 6),
    ]
    pygame.draw.polygon(surf, color, blade_pts)
    pygame.draw.polygon(surf, _darker(color, 40), blade_pts, 1)
    pygame.draw.line(surf, _lighter(color, 70),
                     (hx - s // 5 + 2, hy - s // 5), (hx, hy - s // 4), 1)


def _icon_shears(surf, color, s):
    pygame.draw.line(surf, color, (s // 5, s // 4), (s * 4 // 5, s * 3 // 4), 4)
    pygame.draw.line(surf, color, (s * 4 // 5, s // 4), (s // 5, s * 3 // 4), 4)
    for bx, by in [(s // 5 - 1, s * 3 // 4 + 2), (s * 4 // 5 + 1, s * 3 // 4 + 2)]:
        pygame.draw.circle(surf, _darker(color, 30), (bx, by), 5)
        pygame.draw.circle(surf, (0, 0, 0), (bx, by), 5, 1)


def _icon_bucket(surf, color, s):
    pad = s // 5
    pts = [(pad + 3, pad + 2), (s - pad - 3, pad + 2),
           (s - pad + 2, s - pad), (pad - 2, s - pad)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 2)
    pygame.draw.arc(surf, _darker(color, 50),
                    (pad + 2, pad - 8, s - pad * 2 - 4, s // 3), 0, math.pi, 2)


def _icon_wool(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 9 // 25
    pygame.draw.circle(surf, color, (cx, cy), r)
    for i in range(8):
        a = math.tau * i / 8
        bx = cx + int((r - 3) * math.cos(a))
        by = cy + int((r - 3) * math.sin(a))
        pygame.draw.circle(surf, _lighter(color, 20), (bx, by), r // 4)
    pygame.draw.circle(surf, _darker(color, 25), (cx, cy), r, 1)


def _icon_milk(surf, color, s):
    cx = s // 2
    pts = [(cx - s // 4, s // 5), (cx + s // 4, s // 5),
           (cx + s // 4 + 2, s * 4 // 5), (cx - s // 4 - 2, s * 4 // 5)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.ellipse(surf, (255, 255, 255), (cx - s // 4, s // 5 - 3, s // 2, s // 6))
    pygame.draw.polygon(surf, _darker(color, 20), pts, 1)


def _icon_rock_dust(surf, color, s):
    rng = random.Random(hash(color))
    pad = s // 5
    for _ in range(30):
        x = rng.randint(pad, s - pad)
        y = rng.randint(pad, s - pad)
        pygame.draw.circle(surf, color, (x, y), rng.randint(1, 3))


def _icon_void(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 8 // 22
    pygame.draw.circle(surf, color, (cx, cy), r)
    for i in range(3):
        rr = r - 4 - i * 4
        if rr > 2:
            pygame.draw.circle(surf, _lighter(color, 40 + i * 20), (cx, cy), rr, 1)
    pygame.draw.line(surf, (180, 100, 255), (cx, cy - r // 2), (cx, cy + r // 2), 1)
    pygame.draw.line(surf, (180, 100, 255), (cx - r // 2, cy), (cx + r // 2, cy), 1)


def _icon_miner(surf, color, s):
    pad = s // 7
    r = pygame.Rect(pad, pad, s - pad * 2, s - pad * 2)
    pygame.draw.rect(surf, color, r)
    visor = pygame.Rect(pad * 2, pad * 2, s - pad * 4, s // 5)
    pygame.draw.rect(surf, (30, 30, 80), visor)
    pygame.draw.rect(surf, (80, 120, 200), visor, 1)
    tread = _darker(color, 40)
    pygame.draw.rect(surf, tread, (pad, s - pad * 3, s // 5, pad * 2))
    pygame.draw.rect(surf, tread, (s - pad - s // 5, s - pad * 3, s // 5, pad * 2))
    pygame.draw.line(surf, _lighter(color, 20), (s - pad, s // 2), (s - pad + 4, s * 3 // 4), 3)
    pygame.draw.rect(surf, _darker(color, 60), r, 2)


def _icon_support(surf, color, s):
    pad = s // 6
    pygame.draw.rect(surf, color, (pad, pad, s - pad * 2, s - pad * 2))
    dark = _darker(color, 40)
    pygame.draw.line(surf, dark, (pad, pad), (s - pad, s - pad), 2)
    pygame.draw.line(surf, dark, (s - pad, pad), (pad, s - pad), 2)
    pygame.draw.rect(surf, _darker(color, 60), (pad, pad, s - pad * 2, s - pad * 2), 2)


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

_ICONS = {
    "dirt_clump":    _icon_dirt,
    "stone_chip":    _slab,
    "coal":          _icon_coal,
    "iron_chunk":    _chunk,
    "gold_nugget":   _chunk,
    "crystal_shard": _icon_crystal,
    "ruby":          _gem,
    "obsidian_slab": _slab,
    "lumber":        _lumber,
    "sapling":       _icon_sapling,

    "strawberry":    _icon_strawberry,
    "wheat":         _icon_wheat,
    "carrot":        _icon_carrot,
    "tomato":        _icon_tomato,
    "corn":          _icon_corn,
    "pumpkin":       _icon_pumpkin,
    "apple":         _icon_apple,
    "egg":           _icon_egg,
    "mushroom":      _icon_mushroom,
    "rice":          _icon_rice,
    "ginger":        _icon_ginger,
    "bok_choy":      _icon_bok_choy,
    "garlic":        _icon_garlic,
    "scallion":      _icon_scallion,
    "chili":         _icon_chili,

    "strawberry_seed": _icon_seed,
    "wheat_seed":      _icon_seed,
    "carrot_seed":     _icon_seed,
    "tomato_seed":     _icon_seed,
    "corn_seed":       _icon_seed,
    "pumpkin_seed":    _icon_seed,
    "apple_seed":      _icon_seed,
    "rice_seed":       _icon_seed,
    "ginger_seed":     _icon_seed,
    "bok_choy_seed":   _icon_seed,
    "garlic_seed":     _icon_seed,
    "scallion_seed":   _icon_seed,
    "chili_seed":      _icon_seed,

    "stone_pickaxe": _icon_pickaxe,
    "iron_pickaxe":  _icon_pickaxe,
    "gold_pickaxe":  _icon_pickaxe,
    "stone_axe":     _icon_axe,
    "iron_axe":      _icon_axe,
    "gold_axe":      _icon_axe,
    "shears":        _icon_shears,
    "bucket":        _icon_bucket,

    "wool":          _icon_wool,
    "milk":          _icon_milk,

    "tumbler_item":    _machine,
    "crusher_item":    _machine,
    "gem_cutter_item": _machine,
    "kiln_item":       _machine,
    "resonance_item":  _machine,
    "bakery_item":     _machine,
    "wok_item":        _machine,
    "steamer_item":    _machine,
    "noodle_pot_item": _machine,

    "bread":             _bread,
    "cheese":            _round_food,
    "tomato_soup":       _bowl,
    "corn_bread":        _bread,
    "pumpkin_pie":       _bowl,
    "apple_pie":         _bowl,
    "carrot_cake":       _bread,
    "cooked_egg":        _icon_egg,
    "omelette":          _bowl,
    "cheese_bread":      _bread,
    "noodles":           _bowl,
    "noodle_soup":       _bowl,
    "sesame_noodles":    _bowl,
    "garlic_bok_choy":   _bowl,
    "scallion_pancake":  _bowl,
    "chili_oil_tofu":    _bowl,
    "stir_fried_rice":   _bowl,
    "spicy_corn":        _bowl,
    "chili_bok_choy":    _bowl,
    "scallion_eggs":     _bowl,
    "steamed_bun":       _bread,
    "lotus_rice":        _bowl,
    "crystal_rolls":     _bowl,
    "steamed_egg":       _bowl,
    "pumpkin_cake":      _bowl,
    "soy_sauce":         _bowl,
    "ramen":             _bowl,
    "chili_noodles":     _bowl,
    "hot_pot_broth":     _bowl,
    "scallion_soup":     _bowl,
    "tofu":              _slab,
    "steamed_rice":      _bowl,
    "egg_fried_rice":    _bowl,
    "congee":            _bowl,
    "mapo_tofu":         _bowl,
    "dumplings":         _bowl,
    "wonton_soup":       _bowl,
    "kung_pao":          _bowl,
    "moon_cake":         _round_food,
    "hot_sour_soup":     _bowl,
    "sweet_rice_ball":   _round_food,

    "rock_dust":              _icon_rock_dust,
    "polished_stone":         _slab,
    "ladder_item":            _ladder,
    "support_item":           _icon_support,
    "iron_support_item":      _icon_support,
    "diamond_support_item":   _icon_support,
    "diamond":                _gem,
    "quartz_gem":             _gem,
    "amethyst_gem":           _gem,
    "citrine_gem":            _gem,
    "fused_ingot":            _ingot,
    "void_essence":           _icon_void,

    "coal_miner_item":    _icon_miner,
    "iron_miner_item":    _icon_miner,
    "crystal_miner_item": _icon_miner,
}


def render_item_icon(item_id: str, color: tuple, size: int = 46) -> pygame.Surface:
    """Return a cached Surface with a procedural icon for the given item."""
    key = (item_id, color, size)
    cached = _cache.get(key)
    if cached is not None:
        return cached
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    fn = _ICONS.get(item_id, _chunk)
    fn(surf, color, size)
    _cache[key] = surf
    return surf
