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


def _icon_potato(surf, color, s):
    cx, cy = s // 2, s // 2 + 2
    offsets = [0, 3, -2, 4, -3, 2, -2, 3, 0, -3, 2, -4]
    pts = []
    for i in range(12):
        a = math.tau * i / 12
        rr = s * 8 // 22 + offsets[i]
        pts.append((cx + int(rr * math.cos(a)), cy + int(rr * math.sin(a))))
    pygame.draw.polygon(surf, color, pts)
    eye = _darker(color, 40)
    for ex, ey in [(cx - 4, cy - 2), (cx + 5, cy + 3), (cx - 2, cy + 5)]:
        pygame.draw.circle(surf, eye, (ex, ey), 2)
    pygame.draw.polygon(surf, _darker(color, 50), pts, 1)


def _icon_onion(surf, color, s):
    cx, cy = s // 2, s // 2 + 2
    r = s * 8 // 22
    pygame.draw.circle(surf, color, (cx, cy), r)
    layer = _darker(color, 35)
    for lr in [r - 4, r - 8]:
        if lr > 2:
            pygame.draw.arc(surf, layer, (cx - lr, cy - lr, lr * 2, lr * 2), 0.3, math.pi - 0.3, 1)
    pygame.draw.line(surf, _darker(color, 40), (cx, cy + r - 1), (cx, cy + r + 4), 2)
    pygame.draw.line(surf, (90, 155, 60), (cx, cy - r), (cx, cy - r - 6), 2)
    pygame.draw.circle(surf, _darker(color, 30), (cx, cy), r, 1)


def _icon_pepper(surf, color, s):
    cx, cy = s // 2, s // 2 + 2
    r = s * 8 // 22
    for ox in [-r // 3, 0, r // 3]:
        pygame.draw.ellipse(surf, color, (cx + ox - r // 2 + 2, cy - r // 2, r - 2, r + 2))
    pygame.draw.rect(surf, _darker(color, 20), (cx - r // 2, cy - r // 2 - 3, r, 5))
    pygame.draw.line(surf, (70, 140, 40), (cx, cy - r // 2 - 2), (cx, cy - r // 2 - 9), 2)
    pygame.draw.ellipse(surf, _darker(color, 35), (cx - r * 4 // 5, cy - r // 2, r * 8 // 5, r + 2), 1)


def _icon_eggplant(surf, color, s):
    cx = s // 2
    pygame.draw.ellipse(surf, color, (cx - s // 6, s // 4, s // 3, s // 2))
    calyx = (50, 110, 50)
    pygame.draw.ellipse(surf, calyx, (cx - s // 6, s // 6, s // 3, s // 6))
    pygame.draw.line(surf, calyx, (cx, s // 5), (cx, s // 10), 2)
    pygame.draw.ellipse(surf, _darker(color, 35), (cx - s // 6, s // 4, s // 3, s // 2), 1)


def _icon_cabbage(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 9 // 25
    pygame.draw.circle(surf, color, (cx, cy), r)
    leaf = _darker(color, 20)
    for a in [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]:
        ex = cx + int((r - 4) * math.cos(a))
        ey = cy + int((r - 4) * math.sin(a))
        pygame.draw.line(surf, leaf, (cx, cy), (ex, ey), 1)
    pygame.draw.circle(surf, _lighter(color, 30), (cx, cy), r // 3)
    pygame.draw.circle(surf, _darker(color, 30), (cx, cy), r, 1)


def _icon_beet(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 8 // 22
    pygame.draw.circle(surf, color, (cx, cy), r)
    pygame.draw.circle(surf, _lighter(color, 40), (cx - r // 3, cy - r // 3), r // 4)
    pygame.draw.line(surf, _darker(color, 50), (cx, cy + r - 1), (cx + 2, cy + r + 7), 2)
    for lx, la in [(-4, -0.7), (0, -0.3), (4, 0.1)]:
        ex = cx + lx + int(10 * math.cos(la - math.pi / 2))
        ey = cy - r + int(10 * math.sin(la - math.pi / 2))
        pygame.draw.line(surf, (60, 140, 60), (cx + lx, cy - r + 2), (ex, ey), 2)
    pygame.draw.circle(surf, _darker(color, 40), (cx, cy), r, 1)


def _icon_turnip(surf, color, s):
    cx, cy = s // 2, s // 2 + 2
    r = s * 8 // 22
    pygame.draw.circle(surf, (235, 230, 220), (cx, cy), r)
    pygame.draw.ellipse(surf, color, (cx - r, cy - r, r * 2, r))
    pygame.draw.line(surf, _darker(color, 40), (cx, cy + r - 1), (cx, cy + r + 5), 2)
    pygame.draw.line(surf, (70, 150, 60), (cx - 4, cy - r), (cx - 7, cy - r - 7), 2)
    pygame.draw.line(surf, (70, 150, 60), (cx + 4, cy - r), (cx + 7, cy - r - 7), 2)
    pygame.draw.circle(surf, (180, 160, 155), (cx, cy), r, 1)


def _icon_leek(surf, color, s):
    cx = s // 2
    white = (235, 230, 215)
    pygame.draw.rect(surf, white, (cx - 5, s * 5 // 8, 10, s * 3 // 8 - 2))
    pygame.draw.ellipse(surf, white, (cx - 5, s * 5 // 8 - 4, 10, 8))
    for ox in [-4, 0, 4]:
        pygame.draw.line(surf, color, (cx + ox, s * 5 // 8),
                         (cx + ox + ox // 2, s // 8), 3)
    pygame.draw.rect(surf, _darker(white, 30), (cx - 5, s * 5 // 8, 10, s * 3 // 8 - 2), 1)


def _icon_zucchini(surf, color, s):
    cy = s // 2
    pygame.draw.ellipse(surf, color, (s // 8, cy - s // 7, s * 3 // 4, s * 2 // 7))
    stripe = _darker(color, 30)
    for dy in [-3, 0, 3]:
        pygame.draw.line(surf, stripe, (s // 8 + 4, cy + dy // 2), (s * 7 // 8 - 4, cy + dy // 2), 1)
    pygame.draw.line(surf, (70, 130, 50), (s * 7 // 8 - 3, cy), (s * 7 // 8 + 3, cy - 7), 2)
    pygame.draw.ellipse(surf, _darker(color, 35), (s // 8, cy - s // 7, s * 3 // 4, s * 2 // 7), 1)


def _icon_sweet_potato(surf, color, s):
    cx, cy = s // 2, s // 2 + 1
    pts = []
    for i in range(12):
        a = math.tau * i / 12
        base_r = s * 4 // 12 if i in [0, 1, 11, 6, 7, 5] else s * 3 // 12
        offsets = [0, 2, -3, 4, -2, 3, -4, 2, 0, -3, 3, -2]
        rr = base_r + offsets[i]
        pts.append((cx + int(rr * math.cos(a)), cy + int(rr * math.sin(a) * 0.65)))
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _lighter(color, 40), pts[0], pts[3], 1)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 1)


def _icon_watermelon(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 9 // 25
    pygame.draw.circle(surf, color, (cx, cy), r)
    stripe = _darker(color, 40)
    for a in [0.5, 1.1, 1.7, 2.3, 2.9, 3.5, 4.1, 4.7, 5.3, 5.9]:
        ex = cx + int(r * math.cos(a))
        ey = cy + int(r * math.sin(a))
        pygame.draw.line(surf, stripe, (cx, cy), (ex, ey), 1)
    pygame.draw.circle(surf, (210, 50, 60), (cx, cy), r // 3)
    pygame.draw.circle(surf, _darker(color, 30), (cx, cy), r, 1)


def _icon_radish(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 8 // 22
    pygame.draw.circle(surf, color, (cx, cy), r)
    pygame.draw.ellipse(surf, (240, 240, 235), (cx - r, cy, r * 2, r))
    pygame.draw.line(surf, _darker(color, 20), (cx, cy + r - 1), (cx, cy + r + 6), 2)
    for lx in [-5, 0, 5]:
        pygame.draw.line(surf, (60, 155, 60), (cx + lx, cy - r + 1), (cx + lx - 2, cy - r - 7), 2)
    pygame.draw.circle(surf, _darker(color, 40), (cx, cy), r, 1)


def _icon_pea(surf, color, s):
    cy = s // 2
    pts = [(s // 6, cy), (s // 4, cy - s // 6),
           (s * 3 // 4, cy - s // 6), (s * 5 // 6, cy),
           (s * 3 // 4, cy + s // 6), (s // 4, cy + s // 6)]
    pygame.draw.polygon(surf, _darker(color, 10), pts)
    for px in [s // 4 + 3, s // 3 + 2, s // 2, s * 2 // 3 - 2]:
        pygame.draw.circle(surf, color, (px, cy), s // 10)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 1)
    pygame.draw.line(surf, (60, 150, 50), (s * 5 // 6, cy), (s * 5 // 6 + 4, cy - 5), 1)


def _icon_celery(surf, color, s):
    cx = s // 2
    for ox in [-6, -2, 2, 6]:
        stalk_c = _lighter(color, 20) if ox % 4 == 0 else color
        pygame.draw.line(surf, stalk_c, (cx + ox, s * 9 // 10), (cx + ox + ox // 4, s // 8), 2)
    white = (235, 235, 215)
    pygame.draw.rect(surf, white, (cx - 9, s * 3 // 4, 18, 8))
    pygame.draw.rect(surf, _darker(white, 30), (cx - 9, s * 3 // 4, 18, 8), 1)


def _icon_broccoli(surf, color, s):
    cx = s // 2
    stem_c = _darker(color, 20)
    pygame.draw.rect(surf, stem_c, (cx - 3, s * 5 // 8, 6, s * 3 // 8 - 2))
    for bx, by, br in [(cx, s * 4 // 9, 7), (cx - 7, s // 2, 5), (cx + 7, s // 2, 5),
                       (cx - 4, s * 5 // 12, 5), (cx + 4, s * 5 // 12, 5)]:
        pygame.draw.circle(surf, color, (bx, by), br)
    pygame.draw.circle(surf, _darker(color, 35), (cx, s * 4 // 9), 7, 1)


def _icon_cactus_fruit(surf, color, s):
    cx, cy = s // 2, s // 2 + 1
    r = s * 8 // 22
    pygame.draw.ellipse(surf, color, (cx - r, cy - r * 6 // 5, r * 2, r * 12 // 5))
    spine_c = _lighter(color, 80)
    for sx, sy in [(cx - 4, cy - 5), (cx + 5, cy - 3), (cx - 3, cy + 4), (cx + 4, cy + 6), (cx, cy - 8)]:
        pygame.draw.circle(surf, spine_c, (sx, sy), 2)
    pygame.draw.ellipse(surf, _darker(color, 40), (cx - r, cy - r * 6 // 5, r * 2, r * 12 // 5), 1)


def _icon_date(surf, color, s):
    cx, cy = s // 2, s // 2
    pygame.draw.ellipse(surf, color, (cx - s // 7, cy - s // 4, s * 2 // 7, s // 2))
    pygame.draw.line(surf, _lighter(color, 50), (cx - 2, cy - s // 4 + 3), (cx - 2, cy + s // 4 - 4), 1)
    pygame.draw.line(surf, (70, 130, 50), (cx, cy - s // 4), (cx - 2, cy - s // 4 - 6), 1)
    pygame.draw.ellipse(surf, _darker(color, 40), (cx - s // 7, cy - s // 4, s * 2 // 7, s // 2), 1)


def _icon_agave(surf, color, s):
    cx, cy = s // 2, s // 2
    for a in range(6):
        angle = math.tau * a / 6
        ex = cx + int(s * 5 // 12 * math.cos(angle))
        ey = cy + int(s * 5 // 12 * math.sin(angle))
        pts = [
            (cx + int(4 * math.cos(angle + math.pi / 2)), cy + int(4 * math.sin(angle + math.pi / 2))),
            (ex, ey),
            (cx + int(4 * math.cos(angle - math.pi / 2)), cy + int(4 * math.sin(angle - math.pi / 2))),
        ]
        pygame.draw.polygon(surf, color, pts)
        pygame.draw.polygon(surf, _darker(color, 30), pts, 1)
    pygame.draw.circle(surf, _lighter(color, 20), (cx, cy), 5)


def _icon_raw_meat(surf, color, s):
    cx, cy = s // 2, s // 2
    offsets = [0, 5, 2, -3, 4, -5, 3, -4, 0, 4, -2, 5]
    pts = []
    for i in range(12):
        a = math.tau * i / 12
        rr = s * 8 // 22 + offsets[i]
        pts.append((cx + int(rr * math.cos(a)), cy + int(rr * math.sin(a) * 0.7)))
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _lighter(color, 60), (cx - 5, cy - 3), (cx + 6, cy - 1), 2)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 1)


def _icon_cooked_meat(surf, color, s):
    cx, cy = s // 2, s // 2
    offsets = [0, 4, 2, -3, 3, -4, 2, -3, 0, 3, -2, 4]
    pts = []
    for i in range(12):
        a = math.tau * i / 12
        rr = s * 8 // 22 + offsets[i]
        pts.append((cx + int(rr * math.cos(a)), cy + int(rr * math.sin(a) * 0.7)))
    pygame.draw.polygon(surf, color, pts)
    grill = _darker(color, 50)
    for dy in [-4, 0, 4]:
        pygame.draw.line(surf, grill, (cx - 7, cy + dy), (cx + 7, cy + dy + 1), 2)
    pygame.draw.polygon(surf, _darker(color, 50), pts, 1)


def _icon_knife(surf, color, s):
    handle = (100, 65, 30)
    pygame.draw.rect(surf, handle, (s // 2, s * 3 // 5, s // 4, s // 5))
    pygame.draw.rect(surf, _darker(handle, 30), (s // 2, s * 3 // 5, s // 4, s // 5), 1)
    pts = [(s // 6, s * 2 // 5), (s * 2 // 3, s * 3 // 5 - 1), (s // 6, s * 3 // 5 - 1)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, _lighter(color, 80), pts[0], (s * 5 // 12, s * 8 // 20), 1)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 1)


def _icon_bed(surf, color, s):
    pad = s // 8
    frame_c = (130, 85, 40)
    pygame.draw.rect(surf, frame_c, (pad, pad, s - pad * 2, s - pad * 2))
    mat = (235, 225, 215)
    pygame.draw.rect(surf, mat, (pad + 3, pad + 5, s - pad * 2 - 6, s - pad * 2 - 10))
    pillow = (255, 255, 250)
    pygame.draw.ellipse(surf, pillow, (pad + 4, pad + 6, s // 3, s // 4))
    pygame.draw.ellipse(surf, _darker(pillow, 20), (pad + 4, pad + 6, s // 3, s // 4), 1)
    pygame.draw.rect(surf, color, (pad + 3, s // 2, s - pad * 2 - 6, s - pad - s // 2 - 5))
    pygame.draw.rect(surf, _darker(frame_c, 30), (pad, pad, s - pad * 2, s - pad * 2), 2)


def _icon_chest(surf, color, s):
    pad = s // 8
    body = pygame.Rect(pad, pad + s // 6, s - pad * 2, s - pad * 2 - s // 6)
    pygame.draw.rect(surf, color, body)
    lid = pygame.Rect(pad, pad, s - pad * 2, s // 6 + 2)
    pygame.draw.rect(surf, _lighter(color, 20), lid)
    pygame.draw.line(surf, _darker(color, 40), (pad, pad + s // 6 + 1), (s - pad, pad + s // 6 + 1), 2)
    pygame.draw.rect(surf, (180, 150, 50), (s // 2 - 3, pad + s // 6 - 3, 6, 6))
    pygame.draw.rect(surf, _darker(color, 50), body, 2)
    pygame.draw.rect(surf, _darker(_lighter(color, 20), 50), lid, 1)


def _icon_barrel(surf, color, s):
    pad = s // 7
    pts = [(pad + 2, pad), (s - pad - 2, pad),
           (s - pad, s // 2), (s - pad - 2, s - pad),
           (pad + 2, s - pad), (pad, s // 2)]
    pygame.draw.polygon(surf, color, pts)
    band = _darker(color, 50)
    for by in [pad + s // 6, s // 2 - 1, s - pad - s // 6]:
        pygame.draw.line(surf, band, (pad, by), (s - pad, by), 2)
    pygame.draw.line(surf, _lighter(color, 40), (pad + 3, pad + 3), (pad + 3, s - pad - 3), 1)
    pygame.draw.polygon(surf, _darker(color, 50), pts, 1)


def _icon_fence(surf, color, s):
    pad = s // 7
    pygame.draw.rect(surf, color, (pad + 2, pad, 5, s - pad * 2))
    pygame.draw.rect(surf, color, (s - pad - 7, pad, 5, s - pad * 2))
    rail_c = _darker(color, 20)
    pygame.draw.rect(surf, rail_c, (pad, pad + s // 5, s - pad * 2, 4))
    pygame.draw.rect(surf, rail_c, (pad, s - pad - s // 5 - 4, s - pad * 2, 4))
    pygame.draw.line(surf, _lighter(color, 40), (pad + 3, pad + 2), (pad + 3, s - pad - 2), 1)
    pygame.draw.line(surf, _lighter(color, 40), (s - pad - 6, pad + 2), (s - pad - 6, s - pad - 2), 1)


def _icon_door(surf, color, s):
    pad = s // 8
    r = pygame.Rect(pad + 3, pad, s - pad * 2 - 6, s - pad - 2)
    pygame.draw.rect(surf, color, r)
    panel_c = _darker(color, 25)
    pw = (r.width - 6) // 2
    pygame.draw.rect(surf, panel_c, (r.x + 2, r.y + 3, pw, r.height // 2 - 4), 1)
    pygame.draw.rect(surf, panel_c, (r.x + pw + 4, r.y + 3, pw, r.height // 2 - 4), 1)
    pygame.draw.rect(surf, panel_c, (r.x + 2, r.y + r.height // 2 + 1, r.width - 4, r.height // 2 - 4), 1)
    pygame.draw.circle(surf, (180, 150, 50), (r.right - 5, r.centery), 3)
    pygame.draw.rect(surf, _darker(color, 50), r, 2)


def _icon_bird_feeder(surf, color, s):
    dark = _darker(color, 45)
    roof = _darker(color, 65)
    # Post
    pygame.draw.rect(surf, dark, (s // 2 - 2, s * 2 // 5, 4, s * 3 // 5 - s // 8))
    # Tray
    pygame.draw.rect(surf, color, (s // 8, s * 2 // 5 - 4, s * 6 // 8, 4))
    # Seeds
    for sx2 in [s // 4, s * 2 // 4, s * 3 // 4 - 3]:
        pygame.draw.rect(surf, (220, 190, 60), (sx2, s * 2 // 5 - 4, 2, 2))
    # Roof ridge
    pygame.draw.rect(surf, roof, (s // 10, s // 4, s * 8 // 10, s // 5))
    # Roof peak
    pygame.draw.polygon(surf, color, [(s // 2, s // 8), (s // 10, s // 4 + 1), (s * 9 // 10, s // 4 + 1)])
    pygame.draw.polygon(surf, dark, [(s // 2, s // 8), (s // 10, s // 4 + 1), (s * 9 // 10, s // 4 + 1)], 1)


def _icon_bird_bath(surf, color, s):
    dark = _darker(color, 40)
    water = (75, 148, 215)
    # Pedestal
    pygame.draw.rect(surf, dark, (s // 2 - 3, s * 2 // 5, 6, s * 3 // 5 - s // 8))
    pygame.draw.rect(surf, color, (s // 2 - 2, s * 2 // 5, 2, s * 3 // 5 - s // 8))
    # Basin
    pygame.draw.rect(surf, color, (s // 8, s // 4, s * 6 // 8, s // 5))
    pygame.draw.rect(surf, dark, (s // 8, s // 4, s * 6 // 8, s // 5), 1)
    # Water
    pygame.draw.rect(surf, water, (s // 8 + 2, s // 4 + 2, s * 6 // 8 - 4, s // 5 - 4))
    pygame.draw.rect(surf, _lighter(water, 50), (s // 4, s // 4 + 3, s // 6, 1))


def _icon_bbq_grill(surf, color, s):
    pad = s // 7
    leg_c = _darker(color, 30)
    pygame.draw.line(surf, leg_c, (pad + 4, s * 2 // 3), (pad, s - pad), 3)
    pygame.draw.line(surf, leg_c, (s - pad - 4, s * 2 // 3), (s - pad, s - pad), 3)
    pts = [(pad, s // 3), (s - pad, s // 3), (s - pad + 2, s * 2 // 3), (pad - 2, s * 2 // 3)]
    pygame.draw.polygon(surf, color, pts)
    grate = _lighter(color, 50)
    for gx in range(pad + 3, s - pad - 1, 5):
        pygame.draw.line(surf, grate, (gx, s // 3 + 2), (gx, s * 2 // 3 - 2), 1)
    pygame.draw.polygon(surf, _darker(color, 50), pts, 1)


def _icon_clay_pot(surf, color, s):
    cx = s // 2
    pad = s // 8
    rim_y = s // 4
    pts = [(pad + 2, rim_y)]
    for i in range(11):
        a = math.pi * i / 10
        w = s // 2 - pad
        h = s * 6 // 10
        pts.append((cx + int(w * math.cos(math.pi - a)), rim_y + int(h * math.sin(math.pi - a))))
    pts.append((s - pad - 2, rim_y))
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.rect(surf, _lighter(color, 20), (pad, rim_y - 4, s - pad * 2, 6))
    pygame.draw.line(surf, _darker(color, 40), (pad, rim_y), (s - pad, rim_y), 2)
    pygame.draw.line(surf, _lighter(color, 30), (cx - s // 4, rim_y + s // 5), (cx + s // 4, rim_y + s // 5), 1)


def _icon_cactus_fiber(surf, color, s):
    rng = random.Random(42)
    for _ in range(8):
        x1 = rng.randint(s // 6, s // 3)
        x2 = rng.randint(s * 2 // 3, s * 5 // 6)
        y1 = rng.randint(s // 4, s * 3 // 4)
        pygame.draw.line(surf, color, (x1, y1), (x2, y1 + rng.randint(-3, 3)), 1)
    for _ in range(4):
        x1 = rng.randint(s // 5, s * 2 // 5)
        x2 = rng.randint(s * 3 // 5, s * 4 // 5)
        y1 = rng.randint(s // 3, s * 2 // 3)
        pygame.draw.line(surf, _darker(color, 20), (x1, y1), (x2, y1 + rng.randint(-2, 2)), 2)


def _icon_agave_syrup(surf, color, s):
    cx = s // 2
    pad = s // 7
    pts = [(cx - s // 5, pad + s // 6), (cx + s // 5, pad + s // 6),
           (cx + s // 4, s - pad), (cx - s // 4, s - pad)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.rect(surf, _darker(color, 10), (cx - s // 8, pad, s // 4, s // 6 + 2))
    pygame.draw.rect(surf, (90, 70, 40), (cx - s // 7, pad - 3, s * 2 // 7, 5))
    pygame.draw.line(surf, _lighter(color, 60), (cx - s // 6, pad + s // 5), (cx - s // 6, s - pad - 4), 1)
    pygame.draw.polygon(surf, _darker(color, 40), pts, 1)


def _icon_desert_glass(surf, color, s):
    cx, cy = s // 2, s // 2
    r = s * 8 // 22
    pts = [(cx, s // 8), (cx + r, cy - 2), (cx + r - 4, cy + r),
           (cx, s * 7 // 8), (cx - r + 4, cy + r), (cx - r, cy - 2)]
    pygame.draw.polygon(surf, color, pts)
    bright = _lighter(color, 100)
    pygame.draw.line(surf, bright, pts[0], pts[1], 1)
    pygame.draw.line(surf, bright, pts[0], pts[5], 1)
    pygame.draw.polygon(surf, _darker(color, 30), pts, 1)
    pygame.draw.line(surf, (255, 255, 255), (cx - 3, cy - r // 2), (cx + 2, cy - r // 3), 1)


def _icon_sandstone(surf, color, s):
    _slab(surf, color, s)
    pad = s // 7
    line_c = _darker(color, 25)
    for dy in [s * 5 // 14, s * 7 // 14, s * 9 // 14]:
        pygame.draw.line(surf, line_c, (pad + 2, dy), (s - pad - 2, dy), 1)


def _icon_farm_bot(surf, color, s):
    pad = s // 7
    r = pygame.Rect(pad, pad, s - pad * 2, s - pad * 2)
    pygame.draw.rect(surf, color, r)
    visor = pygame.Rect(pad * 2, pad * 2, s - pad * 4, s // 5)
    pygame.draw.rect(surf, (20, 60, 20), visor)
    pygame.draw.rect(surf, (60, 160, 60), visor, 1)
    arm_c = _darker(color, 40)
    pygame.draw.line(surf, arm_c, (pad, s * 2 // 3), (pad - 4, s - pad), 3)
    pygame.draw.line(surf, arm_c, (s - pad, s * 2 // 3), (s - pad + 4, s - pad), 3)
    pygame.draw.line(surf, (60, 160, 50), (s // 3, s // 2), (s * 2 // 3, s // 2), 1)
    pygame.draw.line(surf, (60, 160, 50), (s // 2, s * 5 // 12), (s // 2, s * 7 // 12), 1)
    pygame.draw.rect(surf, _darker(color, 60), r, 2)


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
    "diamond":                _gem,
    "quartz_gem":             _gem,
    "amethyst_gem":           _gem,
    "citrine_gem":            _gem,
    "fused_ingot":            _ingot,
    "void_essence":           _icon_void,

    "coal_miner_item":    _icon_miner,
    "iron_miner_item":    _icon_miner,
    "crystal_miner_item": _icon_miner,

    # Vegetables
    "pepper":       _icon_pepper,
    "onion":        _icon_onion,
    "potato":       _icon_potato,
    "eggplant":     _icon_eggplant,
    "cabbage":      _icon_cabbage,
    "beet":         _icon_beet,
    "turnip":       _icon_turnip,
    "leek":         _icon_leek,
    "zucchini":     _icon_zucchini,
    "sweet_potato": _icon_sweet_potato,
    "watermelon":   _icon_watermelon,
    "radish":       _icon_radish,
    "pea":          _icon_pea,
    "celery":       _icon_celery,
    "broccoli":     _icon_broccoli,

    # Desert ingredients
    "cactus_fruit":    _icon_cactus_fruit,
    "date_palm_fruit": _icon_date,
    "agave":           _icon_agave,
    "cactus_spine":    _icon_seed,
    "date_palm_seed":  _icon_seed,
    "agave_seed":      _icon_seed,
    "sand_grain":      _icon_dirt,

    # Meats
    "raw_mutton":     _icon_raw_meat,
    "raw_beef":       _icon_raw_meat,
    "raw_chicken":    _icon_raw_meat,
    "cooked_mutton":  _icon_cooked_meat,
    "cooked_beef":    _icon_cooked_meat,
    "cooked_chicken": _icon_cooked_meat,

    # Tools
    "hunting_knife":   _icon_knife,
    "tempered_pickaxe": _icon_pickaxe,
    "tempered_axe":    _icon_axe,

    # Desert forge outputs
    "sandstone":    _icon_sandstone,
    "desert_glass": _icon_desert_glass,
    "tempered_iron": _ingot,
    "cactus_fiber": _icon_cactus_fiber,
    "agave_syrup":  _icon_agave_syrup,

    # Furniture & equipment
    "bed":              _icon_bed,
    "chest_item":       _icon_chest,
    "bird_feeder":      _icon_bird_feeder,
    "bird_bath":        _icon_bird_bath,
    "empty_barrel":     _icon_barrel,
    "oil_barrel":       _icon_barrel,
    "wood_fence":       _icon_fence,
    "iron_fence":       _icon_fence,
    "wood_door":        _icon_door,
    "iron_door":        _icon_door,
    "bbq_grill_item":   _icon_bbq_grill,
    "clay_pot_item":    _icon_clay_pot,
    "desert_forge_item": _machine,
    "backhoe_item":     _machine,

    # Farm bots
    "farm_bot_item":         _icon_farm_bot,
    "iron_farm_bot_item":    _icon_farm_bot,
    "crystal_farm_bot_item": _icon_farm_bot,

    # Jam / missing baked
    "strawberry_jam": _bowl,

    # BBQ grill dishes
    "grilled_corn":    _bowl,
    "potato_wedges":   _bowl,
    "bbq_eggplant":    _bowl,
    "grilled_mushroom": _bowl,
    "stuffed_pepper":  _bowl,
    "eggplant_skewer": _bowl,
    "corn_ribs":       _bowl,
    "bbq_tofu":        _bowl,
    "roast_onion":     _bowl,
    "grilled_cabbage": _bowl,

    # Clay pot dishes
    "potato_stew":          _bowl,
    "cabbage_soup":         _bowl,
    "braised_eggplant":     _bowl,
    "pepper_soup":          _bowl,
    "onion_broth":          _bowl,
    "potato_mushroom_stew": _bowl,
    "stuffed_cabbage":      _bowl,
    "braised_tofu":         _bowl,
    "pepper_pot":           _bowl,
    "harvest_stew":         _bowl,
    "beet_soup":            _bowl,
    "root_medley":          _bowl,
    "radish_kimchi":        _bowl,
    "pea_soup":             _bowl,
    "stuffed_zucchini":     _bowl,
    "garden_soup":          _bowl,
    "turnip_mash":          _bowl,
    "zucchini_stir_fry":    _bowl,
    "celery_stir_fry":      _bowl,
    "broccoli_stir_fry":    _bowl,
    "leek_potato_soup":     _bowl,
    "sweet_potato_pie":     _bowl,
    "sweet_potato_wedges":  _bowl,
    "grilled_leek":         _bowl,
    "watermelon_salad":     _bowl,

    # Desert food
    "grilled_cactus":  _bowl,
    "date_cake":       _bread,
    "cactus_candy":    _round_food,
    "desert_salad":    _bowl,
    "date_palm_broth": _bowl,
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
