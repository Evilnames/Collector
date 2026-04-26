"""
heraldry.py — Procedural coat of arms generator for regions.

Each region gets a deterministic CoatOfArms generated from its seed.
Call draw(surface, x, y, w, h, coa) to render the heater-shield emblem.
"""

import math
import random
from dataclasses import dataclass

import pygame

# ---------------------------------------------------------------------------
# Tinctures
# ---------------------------------------------------------------------------

_COLORS = [
    (175,  38,  38),  # gules    (red)
    ( 38,  78, 175),  # azure    (blue)
    ( 45, 130,  45),  # vert     (green)
    ( 55,  55,  55),  # sable    (black)
    (120,  45, 150),  # purpure  (purple)
    (170,  85,  25),  # tenne    (orange)
    ( 25, 120, 130),  # bleu-celeste
]
_METALS = [
    (205, 170,  45),  # or       (gold)
    (210, 210, 210),  # argent   (silver)
]

_DIVISIONS  = [
    "plain", "plain",
    "per_pale", "per_fess", "quarterly",
    "per_bend", "per_bend_sinister", "gyronny",
    "barry", "paly", "bendy", "checky", "lozengy",
]
_ORDINARIES = [
    "none", "none", "none",
    "fess", "pale", "chief", "chevron", "cross", "saltire", "bend",
    "bordure", "pile", "pall", "base",
]
_CHARGES = [
    "none", "none",
    "star", "moon", "sun", "tree", "tower",
    "sword", "fish", "eagle", "castle", "crown", "anchor", "fleur", "cross",
    "lion", "wolf", "horse", "bear",
    "axe", "hammer", "arrow", "spear",
    "rose", "key", "ship", "wheat", "bell",
    # animals
    "dragon", "griffin", "stag", "boar", "fox",
    "owl", "raven", "swan", "serpent", "bull",
    "dolphin", "bee",
    # objects / symbols
    "chalice", "torch", "lantern", "portcullis", "orb",
    "hourglass", "scales", "acorn", "oak_leaf", "thistle",
    "grapes", "eye", "gauntlet", "helmet", "buckler",
    "mill", "boot", "bridge", "candle",
    # weapons / tools
    "mace", "trident", "scythe", "crossbow", "dagger",
    "lance", "anvil", "plow", "quiver", "cannon",
    # nature
    "mountain", "waves", "lightning", "snowflake", "flame",
    "cloud", "comet",
    # architecture / misc
    "gate", "harp",
]
_MOTTOS = [
    "Truth and Valor",       "By Steel and Stone",    "Ever Watchful",
    "Roots Run Deep",        "For the Common Good",   "Unyielding",
    "Through Fire, Forward", "In Unity, Strength",    "Hold Fast",
    "Rise and Build",        "Honor Above All",       "Faith, Flame, Fortune",
    "Stand Firm",            "Endure and Conquer",    "Seek and Find",
    "The Strong Endure",     "Light Through Darkness","Forged, Not Born",
    "By the Land We Stand",  "Swift and Sure",        "Blood and Bark",
    "Tempered by Trial",     "We Do Not Kneel",       "From Dust, Gold",
    "Claim What is Ours",    "Ever Forward",          "Shore to Summit",
]

# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------

@dataclass
class CoatOfArms:
    primary:   tuple   # main field tincture
    secondary: tuple   # contrasting tincture
    metal:     tuple   # or / argent — used for the charge
    division:  str     # field division style
    ordinary:  str     # geometric band across the field
    charge:    str     # central symbol
    motto:     str


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate(rng: random.Random, primary_color: tuple,
             charge_pool: list = None) -> CoatOfArms:
    """Build a deterministic CoatOfArms from the given rng and primary field color."""
    all_tinctures = _COLORS + _METALS
    pool = [c for c in all_tinctures if c != primary_color]
    secondary = rng.choice(pool)
    metal = rng.choice(_METALS)
    return CoatOfArms(
        primary   = primary_color,
        secondary = secondary,
        metal     = metal,
        division  = rng.choice(_DIVISIONS),
        ordinary  = rng.choice(_ORDINARIES),
        charge    = rng.choice(charge_pool if charge_pool else _CHARGES),
        motto     = rng.choice(_MOTTOS),
    )


# ---------------------------------------------------------------------------
# Public draw entry point
# ---------------------------------------------------------------------------

def draw(surface: pygame.Surface, x: int, y: int, w: int, h: int,
         coa: CoatOfArms) -> None:
    """Render the coat of arms shield into rect (x, y, w, h) on `surface`."""
    shield = _make_shield(w, h, coa)
    surface.blit(shield, (x, y))


# ---------------------------------------------------------------------------
# Shield construction
# ---------------------------------------------------------------------------

def _shield_pts(w: int, h: int) -> list:
    """Classic heater / escutcheon polygon (local coordinates)."""
    mx = w // 2
    return [
        (0,   0),
        (w,   0),
        (w,   int(h * 0.62)),
        (mx,  h),
        (0,   int(h * 0.62)),
    ]


def _make_shield(w: int, h: int, coa: CoatOfArms) -> pygame.Surface:
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    pts = _shield_pts(w, h)

    # Field
    field = pygame.Surface((w, h), pygame.SRCALPHA)
    field.fill((0, 0, 0, 0))
    _draw_field(field, w, h, coa.primary, coa.secondary, coa.division)
    _clip_to_shield(field, pts)
    surf.blit(field, (0, 0))

    # Ordinary
    if coa.ordinary != "none":
        ord_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        ord_surf.fill((0, 0, 0, 0))
        _draw_ordinary(ord_surf, w, h, coa.secondary, coa.ordinary)
        _clip_to_shield(ord_surf, pts)
        surf.blit(ord_surf, (0, 0))

    # Charge
    if coa.charge != "none":
        chg_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        chg_surf.fill((0, 0, 0, 0))
        cx = w // 2
        cy = int(h * 0.40)
        sz = min(w, h) // 4
        _draw_charge(chg_surf, cx, cy, sz, coa.metal, coa.charge)
        _clip_to_shield(chg_surf, pts)
        surf.blit(chg_surf, (0, 0))

    # Outline
    pygame.draw.polygon(surf, (18, 15, 10), pts, 2)
    return surf


def _clip_to_shield(surf: pygame.Surface, pts: list) -> None:
    """Clip surf in-place to the shield polygon using alpha masking."""
    mask = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.polygon(mask, (255, 255, 255, 255), pts)
    surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


# ---------------------------------------------------------------------------
# Field divisions
# ---------------------------------------------------------------------------

def _draw_field(surf, w, h, c1, c2, division):
    if division == "per_pale":
        pygame.draw.rect(surf, c1, (0,      0, w // 2,      h))
        pygame.draw.rect(surf, c2, (w // 2, 0, w - w // 2, h))
    elif division == "per_fess":
        pygame.draw.rect(surf, c1, (0, 0,      w, h // 2))
        pygame.draw.rect(surf, c2, (0, h // 2, w, h - h // 2))
    elif division == "quarterly":
        pygame.draw.rect(surf, c1, (0,      0,      w // 2,      h // 2))
        pygame.draw.rect(surf, c2, (w // 2, 0,      w - w // 2,  h // 2))
        pygame.draw.rect(surf, c2, (0,      h // 2, w // 2,      h - h // 2))
        pygame.draw.rect(surf, c1, (w // 2, h // 2, w - w // 2,  h - h // 2))
    elif division == "per_bend":
        pygame.draw.rect(surf, c1, (0, 0, w, h))
        pygame.draw.polygon(surf, c2, [(w, 0), (w, h), (0, h)])
    elif division == "per_bend_sinister":
        pygame.draw.rect(surf, c1, (0, 0, w, h))
        pygame.draw.polygon(surf, c2, [(0, 0), (w, h), (0, h)])
    elif division == "gyronny":
        # 6 alternating wedges from upper center
        pygame.draw.rect(surf, c1, (0, 0, w, h))
        ox, oy = w // 2, h // 3
        r = max(w, h) * 2
        for i in range(3):
            a1 = i * math.tau / 3
            a2 = a1 + math.tau / 6
            pts = [
                (ox, oy),
                (ox + int(r * math.cos(a1)), oy + int(r * math.sin(a1))),
                (ox + int(r * math.cos(a2)), oy + int(r * math.sin(a2))),
            ]
            pygame.draw.polygon(surf, c2, pts)
    elif division == "barry":
        bars = 6
        bh = h // bars
        for i in range(bars):
            pygame.draw.rect(surf, c1 if i % 2 == 0 else c2, (0, i * bh, w, bh + 1))
    elif division == "paly":
        pales = 6
        pw = w // pales
        for i in range(pales):
            pygame.draw.rect(surf, c1 if i % 2 == 0 else c2, (i * pw, 0, pw + 1, h))
    elif division == "bendy":
        stripes = 6
        sw = (w + h) // stripes
        pygame.draw.rect(surf, c1, (0, 0, w, h))
        for i in range(-1, stripes + 1, 2):
            ox = i * sw
            pygame.draw.polygon(surf, c2, [
                (ox,      0),
                (ox + sw, 0),
                (ox + sw + h, h),
                (ox + h,  h),
            ])
    elif division == "checky":
        cells = 5
        cw = w // cells
        ch = h // cells
        for row in range(cells + 1):
            for col in range(cells + 1):
                col_c = c1 if (row + col) % 2 == 0 else c2
                pygame.draw.rect(surf, col_c, (col * cw, row * ch, cw + 1, ch + 1))
    elif division == "lozengy":
        lw, lh = w // 4, h // 5
        pygame.draw.rect(surf, c1, (0, 0, w, h))
        for row in range(-1, 7):
            for col in range(-1, 6):
                ox = col * lw + (lw // 2 if row % 2 else 0)
                oy = row * lh
                cx2 = ox + lw // 2
                cy2 = oy + lh // 2
                pygame.draw.polygon(surf, c2, [
                    (cx2,       oy),
                    (cx2 + lw // 2, cy2),
                    (cx2,       oy + lh),
                    (cx2 - lw // 2, cy2),
                ])
    else:  # plain
        pygame.draw.rect(surf, c1, (0, 0, w, h))


# ---------------------------------------------------------------------------
# Ordinaries
# ---------------------------------------------------------------------------

def _draw_ordinary(surf, w, h, col, ordinary):
    th = max(4, w // 5)
    if ordinary == "fess":
        pygame.draw.rect(surf, col, (0, h // 2 - th // 2, w, th))
    elif ordinary == "pale":
        pygame.draw.rect(surf, col, (w // 2 - th // 2, 0, th, h))
    elif ordinary == "chief":
        pygame.draw.rect(surf, col, (0, 0, w, h // 5))
    elif ordinary == "chevron":
        mid = w // 2
        top_y = int(h * 0.35)
        bot_y = int(h * 0.60)
        pygame.draw.polygon(surf, col, [
            (0,   bot_y + th // 2),
            (mid, top_y - th // 2),
            (w,   bot_y + th // 2),
            (w,   bot_y - th // 2),
            (mid, top_y + th // 2),
            (0,   bot_y - th // 2),
        ])
    elif ordinary == "cross":
        pygame.draw.rect(surf, col, (0,            h // 2 - th // 2, w,  th))
        pygame.draw.rect(surf, col, (w // 2 - th // 2, 0,            th, h))
    elif ordinary == "saltire":
        lw = max(3, th // 2)
        pygame.draw.line(surf, col, (0, 0),  (w, h), lw)
        pygame.draw.line(surf, col, (w, 0),  (0, h), lw)
    elif ordinary == "bend":
        lw = max(4, th)
        pygame.draw.line(surf, col, (0, 0), (w, h), lw * 2)
    elif ordinary == "bordure":
        bw = max(3, w // 8)
        pygame.draw.polygon(surf, col, _shield_pts(w, h), bw)
    elif ordinary == "pile":
        pygame.draw.polygon(surf, col, [(0, 0), (w, 0), (w // 2, int(h * 0.72))])
    elif ordinary == "pall":
        lw = max(3, th // 2)
        mid = w // 2
        fork_y = int(h * 0.55)
        pygame.draw.line(surf, col, (mid, 0),  (mid, fork_y), lw)
        pygame.draw.line(surf, col, (mid, fork_y), (0, h),  lw)
        pygame.draw.line(surf, col, (mid, fork_y), (w, h),  lw)
    elif ordinary == "base":
        pygame.draw.rect(surf, col, (0, int(h * 0.72), w, h))


# ---------------------------------------------------------------------------
# Charges
# ---------------------------------------------------------------------------

def _draw_charge(surf, cx, cy, sz, col, charge):
    _CHARGE_FNS = {
        "star":   _charge_star,
        "moon":   _charge_moon,
        "sun":    _charge_sun,
        "tree":   _charge_tree,
        "tower":  _charge_tower,
        "sword":  _charge_sword,
        "fish":   _charge_fish,
        "eagle":  _charge_eagle,
        "castle": _charge_castle,
        "crown":  _charge_crown,
        "anchor": _charge_anchor,
        "fleur":  _charge_fleur,
        "cross":  _charge_cross,
        "lion":       _charge_lion,
        "wolf":       _charge_wolf,
        "horse":      _charge_horse,
        "bear":       _charge_bear,
        "axe":        _charge_axe,
        "hammer":     _charge_hammer,
        "arrow":      _charge_arrow,
        "spear":      _charge_spear,
        "rose":       _charge_rose,
        "key":        _charge_key,
        "ship":       _charge_ship,
        "wheat":      _charge_wheat,
        "bell":       _charge_bell,
        # new animals
        "dragon":     _charge_dragon,
        "griffin":    _charge_griffin,
        "stag":       _charge_stag,
        "boar":       _charge_boar,
        "fox":        _charge_fox,
        "owl":        _charge_owl,
        "raven":      _charge_raven,
        "swan":       _charge_swan,
        "serpent":    _charge_serpent,
        "bull":       _charge_bull,
        "dolphin":    _charge_dolphin,
        "bee":        _charge_bee,
        # new objects / symbols
        "chalice":    _charge_chalice,
        "torch":      _charge_torch,
        "lantern":    _charge_lantern,
        "portcullis": _charge_portcullis,
        "orb":        _charge_orb,
        "hourglass":  _charge_hourglass,
        "scales":     _charge_scales,
        "acorn":      _charge_acorn,
        "oak_leaf":   _charge_oak_leaf,
        "thistle":    _charge_thistle,
        "grapes":     _charge_grapes,
        "eye":        _charge_eye,
        "gauntlet":   _charge_gauntlet,
        "helmet":     _charge_helmet,
        "buckler":    _charge_buckler,
        "mill":       _charge_mill,
        "boot":       _charge_boot,
        "bridge":     _charge_bridge,
        "candle":     _charge_candle,
        # new weapons / tools
        "mace":       _charge_mace,
        "trident":    _charge_trident,
        "scythe":     _charge_scythe,
        "crossbow":   _charge_crossbow,
        "dagger":     _charge_dagger,
        "lance":      _charge_lance,
        "anvil":      _charge_anvil,
        "plow":       _charge_plow,
        "quiver":     _charge_quiver,
        "cannon":     _charge_cannon,
        # new nature
        "mountain":   _charge_mountain,
        "waves":      _charge_waves,
        "lightning":  _charge_lightning,
        "snowflake":  _charge_snowflake,
        "flame":      _charge_flame,
        "cloud":      _charge_cloud,
        "comet":      _charge_comet,
        # new architecture / misc
        "gate":       _charge_gate,
        "harp":       _charge_harp,
    }
    fn = _CHARGE_FNS.get(charge)
    if fn:
        fn(surf, cx, cy, sz, col)


def _charge_star(surf, cx, cy, sz, col):
    pts = []
    for i in range(5):
        a  = -math.pi / 2 + i * math.tau / 5
        a2 = a + math.pi / 5
        pts.append((cx + int(sz * math.cos(a)),        cy + int(sz * math.sin(a))))
        pts.append((cx + int(sz * 0.4 * math.cos(a2)), cy + int(sz * 0.4 * math.sin(a2))))
    pygame.draw.polygon(surf, col, pts)


def _charge_moon(surf, cx, cy, sz, col):
    """Crescent moon via circle minus offset circle."""
    d = sz * 2 + 4
    tmp = pygame.Surface((d, d), pygame.SRCALPHA)
    tmp.fill((0, 0, 0, 0))
    lc = sz + 2
    pygame.draw.circle(tmp, col, (lc, lc), sz)
    # Carve inner circle shifted right to create left-facing crescent
    mask = pygame.Surface((d, d), pygame.SRCALPHA)
    mask.fill((255, 255, 255, 255))
    offset = max(1, sz // 3)
    pygame.draw.circle(mask, (0, 0, 0, 0), (lc + offset, lc), int(sz * 0.80))
    tmp.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surf.blit(tmp, (cx - lc, cy - lc))


def _charge_sun(surf, cx, cy, sz, col):
    pygame.draw.circle(surf, col, (cx, cy), sz // 2)
    for i in range(8):
        a  = i * math.tau / 8
        x1 = cx + int(sz * 0.58 * math.cos(a))
        y1 = cy + int(sz * 0.58 * math.sin(a))
        x2 = cx + int(sz * 0.92 * math.cos(a))
        y2 = cy + int(sz * 0.92 * math.sin(a))
        pygame.draw.line(surf, col, (x1, y1), (x2, y2), max(2, sz // 7))


def _charge_tree(surf, cx, cy, sz, col):
    tw = max(2, sz // 4)
    th = sz // 2
    pygame.draw.rect(surf, col, (cx - tw // 2, cy, tw, th))
    pygame.draw.circle(surf, col, (cx, cy - sz // 4), sz // 2)


def _charge_tower(surf, cx, cy, sz, col):
    tw = sz * 3 // 4
    th = sz
    tx = cx - tw // 2
    ty = cy - th // 2
    pygame.draw.rect(surf, col, (tx, ty + sz // 6, tw, th - sz // 6))
    mw = max(2, tw // 5)
    for i in range(3):
        mx = tx + i * (tw // 2 - mw // 2)
        pygame.draw.rect(surf, col, (mx, ty, mw, sz // 5))
    dw = max(2, tw // 4)
    dh = th // 3
    pygame.draw.rect(surf, (0, 0, 0, 0),
                     (cx - dw // 2, ty + th - sz // 6 - dh, dw, dh))


def _charge_sword(surf, cx, cy, sz, col):
    bw  = max(2, sz // 6)
    gw  = sz * 3 // 4
    gh  = max(3, sz // 8)
    # Blade
    pygame.draw.rect(surf, col, (cx - bw // 2, cy - sz // 2, bw, sz))
    # Tip
    pygame.draw.polygon(surf, col, [
        (cx - bw // 2, cy - sz // 2),
        (cx + bw // 2, cy - sz // 2),
        (cx,           cy - sz // 2 - sz // 5),
    ])
    # Crossguard
    pygame.draw.rect(surf, col, (cx - gw // 2, cy - sz // 10, gw, gh))
    # Pommel
    pygame.draw.circle(surf, col, (cx, cy + sz // 2), max(2, sz // 8))


def _charge_fish(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col,
                        (cx - sz // 2, cy - sz // 4, sz, sz // 2))
    pygame.draw.polygon(surf, col, [
        (cx + sz // 2 - sz // 8, cy - sz // 4),
        (cx + sz // 2 - sz // 8, cy + sz // 4),
        (cx + sz // 2 + sz // 4, cy),
    ])


def _charge_eagle(surf, cx, cy, sz, col):
    # Wings
    pygame.draw.polygon(surf, col,
                        [(cx, cy), (cx - sz, cy - sz // 3), (cx - sz // 2, cy + sz // 3)])
    pygame.draw.polygon(surf, col,
                        [(cx, cy), (cx + sz, cy - sz // 3), (cx + sz // 2, cy + sz // 3)])
    # Body + head
    pygame.draw.ellipse(surf, col, (cx - sz // 6, cy - sz // 3, sz // 3, sz * 2 // 3))
    pygame.draw.circle(surf, col, (cx, cy - sz // 3), sz // 6)


def _charge_castle(surf, cx, cy, sz, col):
    ww = sz
    wh = sz // 2
    wy = cy - sz // 4
    pygame.draw.rect(surf, col, (cx - ww // 2, wy, ww, wh))
    tw = sz // 4
    th = wh + sz // 6
    pygame.draw.rect(surf, col, (cx - ww // 2 - tw // 4,       wy - sz // 6, tw, th))
    pygame.draw.rect(surf, col, (cx + ww // 2 - tw * 3 // 4,   wy - sz // 6, tw, th))
    gw = max(2, sz // 5)
    gh = sz // 4
    pygame.draw.rect(surf, (0, 0, 0, 0),
                     (cx - gw // 2, wy + wh - gh, gw, gh))
    mw = max(2, sz // 8)
    for ox in [-ww // 2 - tw // 4, -ww // 2 - tw // 4 + mw * 2,
               ww // 2 - tw * 3 // 4, ww // 2 - tw * 3 // 4 + mw * 2]:
        pygame.draw.rect(surf, col, (cx + ox, wy - sz // 6 - sz // 8, mw, sz // 8))


def _charge_crown(surf, cx, cy, sz, col):
    bw  = sz
    bh  = sz // 5
    base_y = cy + sz // 3
    pts = [
        (cx - bw // 2,  base_y - bh),
        (cx - bw // 2,  base_y - sz // 2),
        (cx - bw // 4,  base_y - bh),
        (cx,            base_y - sz * 2 // 3),
        (cx + bw // 4,  base_y - bh),
        (cx + bw // 2,  base_y - sz // 2),
        (cx + bw // 2,  base_y - bh),
        (cx + bw // 2,  base_y),
        (cx - bw // 2,  base_y),
    ]
    pygame.draw.polygon(surf, col, pts)


def _charge_anchor(surf, cx, cy, sz, col):
    r   = sz // 4
    sh  = sz * 3 // 4
    lw  = max(2, sz // 10)
    top = cy - sh // 2
    # Ring at top
    pygame.draw.circle(surf, col, (cx, top), r, lw)
    # Shaft
    pygame.draw.rect(surf, col, (cx - lw // 2, top + r, lw, sh))
    # Stock (horizontal bar near top)
    pygame.draw.rect(surf, col, (cx - sz // 2, top + r // 2, sz, max(3, sz // 8)))
    # Flukes
    fluke_y = cy + sh // 2 - sz // 8
    pygame.draw.line(surf, col, (cx, fluke_y),
                     (cx - sz // 3, cy + sh // 2 - sz // 3), max(2, lw * 2))
    pygame.draw.line(surf, col, (cx, fluke_y),
                     (cx + sz // 3, cy + sh // 2 - sz // 3), max(2, lw * 2))


def _charge_fleur(surf, cx, cy, sz, col):
    # Central tall petal
    pygame.draw.ellipse(surf, col,
                        (cx - sz // 5, cy - sz // 2, sz * 2 // 5, sz * 2 // 3))
    # Side petals
    pygame.draw.polygon(surf, col, [
        (cx, cy),
        (cx - sz // 2, cy - sz // 4),
        (cx - sz // 3, cy + sz // 6),
    ])
    pygame.draw.polygon(surf, col, [
        (cx, cy),
        (cx + sz // 2, cy - sz // 4),
        (cx + sz // 3, cy + sz // 6),
    ])
    # Base bar
    pygame.draw.rect(surf, col, (cx - sz // 3, cy + sz // 5, sz * 2 // 3, sz // 6))


def _charge_cross(surf, cx, cy, sz, col):
    th = max(3, sz // 5)
    pygame.draw.rect(surf, col, (cx - th // 2, cy - sz // 2, th, sz))
    pygame.draw.rect(surf, col, (cx - sz // 2, cy - th // 2, sz, th))


def _charge_lion(surf, cx, cy, sz, col):
    # Body
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy - sz // 4, sz, sz // 2))
    # Head
    pygame.draw.circle(surf, col, (cx + sz // 2, cy - sz // 4), sz // 3)
    # Mane ring
    pygame.draw.circle(surf, col, (cx + sz // 2, cy - sz // 4), sz // 2, max(2, sz // 6))
    # Tail
    pygame.draw.line(surf, col, (cx - sz // 2, cy),
                     (cx - sz * 3 // 4, cy - sz // 3), max(3, sz // 5))
    pygame.draw.circle(surf, col, (cx - sz * 3 // 4, cy - sz // 3), sz // 7)
    # Legs
    for ox in (-sz // 4, sz // 4):
        pygame.draw.line(surf, col, (cx + ox, cy + sz // 4),
                         (cx + ox, cy + sz // 2), max(3, sz // 6))


def _charge_wolf(surf, cx, cy, sz, col):
    # Body
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy - sz // 5, sz, sz * 2 // 5))
    # Head — pointed snout
    pygame.draw.polygon(surf, col, [
        (cx + sz // 2, cy - sz // 4),
        (cx + sz * 3 // 4, cy - sz // 5),
        (cx + sz * 7 // 8, cy),
        (cx + sz // 2, cy + sz // 8),
    ])
    # Ear
    pygame.draw.polygon(surf, col, [
        (cx + sz // 2, cy - sz // 4),
        (cx + sz * 5 // 8, cy - sz // 2),
        (cx + sz * 3 // 4, cy - sz // 4),
    ])
    # Tail
    pygame.draw.line(surf, col, (cx - sz // 2, cy - sz // 5),
                     (cx - sz * 3 // 4, cy - sz // 2), max(3, sz // 6))
    # Legs
    for ox in (-sz // 4, sz // 8):
        pygame.draw.line(surf, col, (cx + ox, cy + sz // 5),
                         (cx + ox, cy + sz // 2), max(3, sz // 7))


def _charge_horse(surf, cx, cy, sz, col):
    # Body
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy - sz // 5, sz, sz * 2 // 5))
    # Neck
    pygame.draw.polygon(surf, col, [
        (cx + sz // 3, cy - sz // 5),
        (cx + sz // 2, cy - sz // 2),
        (cx + sz * 2 // 3, cy - sz // 5),
    ])
    # Head
    pygame.draw.ellipse(surf, col, (cx + sz // 3, cy - sz * 2 // 3, sz // 3, sz // 3))
    # Mane
    for i in range(3):
        pygame.draw.circle(surf, col,
                           (cx + sz // 2 - i * sz // 8, cy - sz // 2 + i * sz // 8),
                           max(2, sz // 8))
    # Legs
    for ox in (-sz // 3, -sz // 8, sz // 8, sz // 3):
        pygame.draw.line(surf, col, (cx + ox, cy + sz // 5),
                         (cx + ox, cy + sz // 2), max(3, sz // 7))


def _charge_bear(surf, cx, cy, sz, col):
    # Body
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy - sz // 4, sz, sz // 2))
    # Head
    pygame.draw.circle(surf, col, (cx + sz // 3, cy - sz // 3), sz // 3)
    # Snout
    pygame.draw.ellipse(surf, col, (cx + sz // 4, cy - sz // 4, sz // 4, sz // 6))
    # Ears
    pygame.draw.circle(surf, col, (cx + sz // 4, cy - sz // 2), max(2, sz // 8))
    pygame.draw.circle(surf, col, (cx + sz // 2, cy - sz // 2), max(2, sz // 8))
    # Legs
    for ox in (-sz // 3, 0, sz // 6):
        pygame.draw.line(surf, col, (cx + ox, cy + sz // 4),
                         (cx + ox, cy + sz // 2), max(4, sz // 5))


def _charge_axe(surf, cx, cy, sz, col):
    hw = max(2, sz // 8)
    # Haft
    pygame.draw.rect(surf, col, (cx - hw // 2, cy - sz // 2, hw, sz))
    # Blade
    pygame.draw.polygon(surf, col, [
        (cx - hw // 2, cy - sz // 2),
        (cx - sz // 2, cy - sz // 4),
        (cx - sz // 2, cy + sz // 8),
        (cx - hw // 2, cy + sz // 8),
    ])
    # Back spike
    pygame.draw.polygon(surf, col, [
        (cx + hw // 2, cy - sz // 2),
        (cx + sz // 4, cy - sz // 3),
        (cx + hw // 2, cy - sz // 8),
    ])


def _charge_hammer(surf, cx, cy, sz, col):
    hw = max(2, sz // 7)
    # Handle
    pygame.draw.rect(surf, col, (cx - hw // 2, cy - sz // 4, hw, sz * 3 // 4))
    # Head
    hh = sz // 3
    pygame.draw.rect(surf, col, (cx - sz // 2, cy - sz // 2, sz, hh))


def _charge_arrow(surf, cx, cy, sz, col):
    lw = max(2, sz // 7)
    # Shaft
    pygame.draw.line(surf, col, (cx, cy - sz // 2), (cx, cy + sz // 2), lw)
    # Head
    pygame.draw.polygon(surf, col, [
        (cx, cy - sz // 2 - sz // 5),
        (cx - sz // 5, cy - sz // 2),
        (cx + sz // 5, cy - sz // 2),
    ])
    # Fletching
    pygame.draw.polygon(surf, col, [
        (cx, cy + sz // 3),
        (cx - sz // 4, cy + sz // 2),
        (cx, cy + sz // 4),
    ])
    pygame.draw.polygon(surf, col, [
        (cx, cy + sz // 3),
        (cx + sz // 4, cy + sz // 2),
        (cx, cy + sz // 4),
    ])


def _charge_spear(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    # Shaft
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz // 2, lw, sz))
    # Head — elongated diamond
    pygame.draw.polygon(surf, col, [
        (cx, cy - sz // 2 - sz // 3),
        (cx - sz // 5, cy - sz // 2),
        (cx, cy - sz // 4),
        (cx + sz // 5, cy - sz // 2),
    ])


def _charge_rose(surf, cx, cy, sz, col):
    # Petals — 5 circles around center
    r = max(2, sz // 4)
    for i in range(5):
        a = -math.pi / 2 + i * math.tau / 5
        px = cx + int(sz * 0.4 * math.cos(a))
        py = cy + int(sz * 0.4 * math.sin(a))
        pygame.draw.circle(surf, col, (px, py), r)
    # Center
    pygame.draw.circle(surf, col, (cx, cy), max(2, sz // 5))
    # Sepal points between petals
    for i in range(5):
        a = -math.pi / 2 + (i + 0.5) * math.tau / 5
        px = cx + int(sz * 0.65 * math.cos(a))
        py = cy + int(sz * 0.65 * math.sin(a))
        pygame.draw.line(surf, col, (cx, cy), (px, py), max(2, sz // 8))


def _charge_key(surf, cx, cy, sz, col):
    lw = max(2, sz // 7)
    r  = sz // 3
    # Ring at top
    pygame.draw.circle(surf, col, (cx, cy - sz // 4), r, lw)
    # Shaft
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz // 4 + r, lw, sz // 2))
    # Teeth
    tooth_y = cy + sz // 4
    for ox, tw, th in [(-sz // 5, sz // 5, sz // 8), (-sz // 5, sz // 6, sz // 10)]:
        pygame.draw.rect(surf, col, (cx + ox, tooth_y, tw, th))
        tooth_y += sz // 7


def _charge_ship(surf, cx, cy, sz, col):
    # Hull
    pygame.draw.polygon(surf, col, [
        (cx - sz // 2, cy),
        (cx + sz // 2, cy),
        (cx + sz * 3 // 8, cy + sz // 3),
        (cx - sz * 3 // 8, cy + sz // 3),
    ])
    # Mast
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz // 2, lw, sz // 2))
    # Sail
    pygame.draw.polygon(surf, col, [
        (cx, cy - sz // 2),
        (cx + sz // 3, cy - sz // 4),
        (cx, cy - sz // 8),
    ])


def _charge_wheat(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    # Central stalk
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz // 2, lw, sz))
    # Grain heads alternating left/right
    for i, (ox, sign) in enumerate([(-sz // 4, -1), (sz // 4, 1),
                                     (-sz // 3, -1), (sz // 3, 1),
                                     (-sz // 5, -1), (sz // 5, 1)]):
        gy = cy - sz // 2 + i * sz // 7
        pygame.draw.ellipse(surf, col, (cx + ox - sz // 10, gy - sz // 12,
                                        sz // 5, sz // 6))
        pygame.draw.line(surf, col, (cx, gy), (cx + ox, gy), lw)


def _charge_bell(surf, cx, cy, sz, col):
    steps = 12
    top_y = cy - sz // 2
    pts = [(cx, top_y)]
    for i in range(steps + 1):
        a = math.pi + i * math.pi / steps
        px = cx + int(sz // 2 * math.cos(a))
        py = top_y + int(sz * 0.7 * (0.5 - 0.5 * math.cos(i * math.pi / steps)))
        pts.append((px, py))
    pts.append((cx, top_y))
    pygame.draw.polygon(surf, col, pts)
    pygame.draw.rect(surf, col, (cx - sz // 2, cy + sz // 6, sz, sz // 8))
    pygame.draw.line(surf, col, (cx, cy), (cx, cy + sz // 4), max(2, sz // 7))
    pygame.draw.circle(surf, col, (cx, cy + sz // 4), max(2, sz // 8))


# ---------------------------------------------------------------------------
# New animal charges
# ---------------------------------------------------------------------------

def _charge_dragon(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy - sz // 6, sz * 3 // 4, sz // 3))
    pygame.draw.circle(surf, col, (cx + sz // 3, cy - sz // 4), sz // 5)
    pygame.draw.polygon(surf, col, [
        (cx + sz // 3, cy - sz // 5),
        (cx + sz * 2 // 3, cy - sz // 6),
        (cx + sz // 2, cy),
    ])
    pygame.draw.polygon(surf, col, [
        (cx, cy - sz // 6),
        (cx - sz // 4, cy - sz * 2 // 3),
        (cx - sz * 2 // 3, cy - sz // 3),
        (cx - sz // 3, cy),
    ])
    pygame.draw.line(surf, col, (cx - sz // 2, cy),
                     (cx - sz * 3 // 4, cy + sz // 3), max(3, sz // 7))
    pygame.draw.polygon(surf, col, [
        (cx - sz * 3 // 4, cy + sz // 3),
        (cx - sz * 2 // 3, cy + sz // 2),
        (cx - sz // 2,     cy + sz // 3),
    ])


def _charge_griffin(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy - sz // 8, sz * 2 // 3, sz // 3))
    pygame.draw.ellipse(surf, col, (cx - sz // 6, cy - sz // 3, sz // 2, sz // 3))
    pygame.draw.circle(surf, col, (cx + sz // 3, cy - sz // 3), sz // 5)
    pygame.draw.polygon(surf, col, [
        (cx + sz // 3, cy - sz // 4),
        (cx + sz * 2 // 3, cy - sz // 3),
        (cx + sz // 3, cy - sz // 2),
    ])
    pygame.draw.polygon(surf, col, [
        (cx, cy - sz // 4),
        (cx - sz // 2, cy - sz * 2 // 3),
        (cx - sz // 4, cy),
    ])
    pygame.draw.polygon(surf, col, [
        (cx, cy - sz // 4),
        (cx + sz // 6, cy - sz * 2 // 3),
        (cx + sz // 3, cy - sz // 4),
    ])


def _charge_stag(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy - sz // 5, sz, sz * 2 // 5))
    pygame.draw.polygon(surf, col, [
        (cx + sz // 3, cy - sz // 5),
        (cx + sz // 2, cy - sz * 2 // 3),
        (cx + sz * 2 // 3, cy - sz // 5),
    ])
    pygame.draw.circle(surf, col, (cx + sz // 2, cy - sz * 2 // 3), sz // 6)
    lw = max(2, sz // 8)
    bx, by = cx + sz // 2, cy - sz * 5 // 6
    pygame.draw.line(surf, col, (bx, by), (bx - sz // 4, by - sz // 4), lw)
    pygame.draw.line(surf, col, (bx - sz // 8, by - sz // 8), (bx - sz // 3, by), lw)
    pygame.draw.line(surf, col, (bx - sz // 4, by - sz // 4), (bx - sz // 3, by - sz // 3), lw)
    pygame.draw.line(surf, col, (bx, by), (bx + sz // 4, by - sz // 4), lw)
    pygame.draw.line(surf, col, (bx + sz // 8, by - sz // 8), (bx + sz // 3, by), lw)
    pygame.draw.line(surf, col, (bx + sz // 4, by - sz // 4), (bx + sz // 3, by - sz // 3), lw)
    for ox in (-sz // 3, -sz // 8, sz // 8, sz // 3):
        pygame.draw.line(surf, col, (cx + ox, cy + sz // 5),
                         (cx + ox, cy + sz // 2), max(3, sz // 7))


def _charge_boar(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy - sz // 4, sz * 3 // 4, sz // 2))
    pygame.draw.ellipse(surf, col, (cx + sz // 4, cy - sz // 3, sz // 2, sz * 2 // 5))
    pygame.draw.ellipse(surf, col, (cx + sz // 2, cy - sz // 5, sz // 4, sz // 5))
    pygame.draw.polygon(surf, col, [
        (cx + sz // 2, cy),
        (cx + sz * 3 // 4, cy + sz // 8),
        (cx + sz * 5 // 8, cy + sz // 4),
    ])
    pygame.draw.arc(surf, col,
                    (cx - sz * 3 // 4, cy - sz // 4, sz // 3, sz // 3),
                    0, math.pi * 1.5, max(2, sz // 8))
    for ox in (-sz // 3, 0):
        pygame.draw.line(surf, col, (cx + ox, cy + sz // 4),
                         (cx + ox, cy + sz // 2), max(3, sz // 6))


def _charge_fox(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 3, cy - sz // 5, sz * 2 // 3, sz * 2 // 5))
    pygame.draw.circle(surf, col, (cx + sz // 3, cy - sz // 4), sz // 5)
    pygame.draw.polygon(surf, col, [
        (cx + sz // 3, cy - sz // 5),
        (cx + sz * 2 // 3, cy - sz // 6),
        (cx + sz // 2, cy + sz // 8),
    ])
    pygame.draw.polygon(surf, col, [
        (cx + sz // 5, cy - sz * 2 // 5),
        (cx + sz // 4, cy - sz * 2 // 3),
        (cx + sz * 2 // 5, cy - sz * 2 // 5),
    ])
    pygame.draw.ellipse(surf, col, (cx - sz * 3 // 4, cy - sz // 4, sz // 2, sz * 2 // 5))
    pygame.draw.line(surf, col, (cx - sz // 3, cy),
                     (cx - sz * 2 // 3, cy - sz // 8), max(3, sz // 6))
    for ox in (-sz // 4, sz // 8):
        pygame.draw.line(surf, col, (cx + ox, cy + sz // 5),
                         (cx + ox, cy + sz // 2), max(3, sz // 7))


def _charge_owl(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 3, cy - sz // 4, sz * 2 // 3, sz * 3 // 4))
    pygame.draw.circle(surf, col, (cx, cy - sz // 3), sz // 3)
    pygame.draw.circle(surf, col, (cx - sz // 7, cy - sz // 3), max(3, sz // 5))
    pygame.draw.circle(surf, col, (cx + sz // 7, cy - sz // 3), max(3, sz // 5))
    pygame.draw.polygon(surf, col, [
        (cx - sz // 4, cy - sz * 2 // 3),
        (cx - sz // 5, cy - sz // 2),
        (cx - sz // 8, cy - sz * 2 // 3),
    ])
    pygame.draw.polygon(surf, col, [
        (cx + sz // 4, cy - sz * 2 // 3),
        (cx + sz // 5, cy - sz // 2),
        (cx + sz // 8, cy - sz * 2 // 3),
    ])
    pygame.draw.polygon(surf, col, [
        (cx - sz // 10, cy - sz // 4),
        (cx + sz // 10, cy - sz // 4),
        (cx,            cy - sz // 8),
    ])


def _charge_raven(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 4, cy - sz // 4, sz // 2, sz // 2))
    pygame.draw.circle(surf, col, (cx + sz // 4, cy - sz // 3), sz // 5)
    pygame.draw.polygon(surf, col, [
        (cx + sz // 3, cy - sz // 3),
        (cx + sz * 2 // 3, cy - sz // 4),
        (cx + sz // 3, cy - sz // 5),
    ])
    pygame.draw.polygon(surf, col, [
        (cx - sz // 4, cy + sz // 4),
        (cx - sz * 2 // 3, cy + sz // 2),
        (cx - sz * 2 // 3, cy + sz // 4),
        (cx - sz // 4, cy),
    ])
    pygame.draw.line(surf, col, (cx, cy + sz // 4), (cx, cy + sz // 2), max(2, sz // 7))
    pygame.draw.line(surf, col, (cx, cy + sz // 2),
                     (cx - sz // 6, cy + sz * 2 // 3), max(2, sz // 7))
    pygame.draw.line(surf, col, (cx, cy + sz // 2),
                     (cx + sz // 6, cy + sz * 2 // 3), max(2, sz // 7))


def _charge_swan(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy, sz * 3 // 4, sz // 3))
    pygame.draw.polygon(surf, col, [
        (cx - sz // 4, cy),
        (cx - sz // 2, cy - sz // 3),
        (cx + sz // 4, cy - sz // 4),
        (cx + sz // 4, cy),
    ])
    for i in range(5):
        t = i / 4
        nx = cx + sz // 4 + int(t * sz // 4)
        ny = cy - int((1 - (2 * t - 1) ** 2) * sz // 2)
        pygame.draw.circle(surf, col, (nx, ny), max(3, sz // 8 - i * sz // 40))
    pygame.draw.circle(surf, col, (cx + sz // 2, cy - sz // 3), sz // 7)
    pygame.draw.polygon(surf, col, [
        (cx + sz // 2, cy - sz // 4),
        (cx + sz * 3 // 4, cy - sz // 4),
        (cx + sz // 2, cy - sz // 3),
    ])


def _charge_serpent(surf, cx, cy, sz, col):
    lw = max(3, sz // 5)
    pts = []
    for i in range(20):
        t = i / 19
        pts.append((
            cx + int(sz // 3 * math.sin(t * math.pi * 2)),
            cy - sz // 2 + int(sz * t),
        ))
    if len(pts) >= 2:
        pygame.draw.lines(surf, col, False, pts, lw)
    head = pts[0]
    pygame.draw.circle(surf, col, head, sz // 7)
    tongue_tip = (head[0], head[1] - sz // 5)
    pygame.draw.line(surf, col, head, tongue_tip, max(2, sz // 8))
    pygame.draw.line(surf, col, tongue_tip,
                     (tongue_tip[0] - sz // 8, tongue_tip[1] - sz // 8), max(2, sz // 9))
    pygame.draw.line(surf, col, tongue_tip,
                     (tongue_tip[0] + sz // 8, tongue_tip[1] - sz // 8), max(2, sz // 9))


def _charge_bull(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 2, cy - sz // 5, sz, sz * 2 // 5))
    pygame.draw.circle(surf, col, (cx + sz // 2, cy - sz // 4), sz // 4)
    lw = max(3, sz // 7)
    pygame.draw.line(surf, col, (cx + sz // 3, cy - sz // 3),
                     (cx + sz // 5, cy - sz * 2 // 3), lw)
    pygame.draw.line(surf, col, (cx + sz * 2 // 3, cy - sz // 3),
                     (cx + sz * 5 // 6, cy - sz * 2 // 3), lw)
    for ox in (-sz // 3, -sz // 8, sz // 8, sz // 3):
        pygame.draw.line(surf, col, (cx + ox, cy + sz // 5),
                         (cx + ox, cy + sz // 2), max(3, sz // 7))


def _charge_dolphin(surf, cx, cy, sz, col):
    lw = max(4, sz // 4)
    pts = []
    for i in range(16):
        t = i / 15
        pts.append((
            cx - sz // 2 + int(sz * t),
            cy + int(sz // 2 * math.sin(t * math.pi)),
        ))
    if len(pts) >= 2:
        pygame.draw.lines(surf, col, False, pts, lw)
    pygame.draw.polygon(surf, col, [
        (cx - sz // 2, cy),
        (cx - sz * 3 // 4, cy - sz // 8),
        (cx - sz * 3 // 4, cy + sz // 8),
    ])
    pygame.draw.polygon(surf, col, [
        (cx + sz // 2, cy),
        (cx + sz * 3 // 4, cy - sz // 3),
        (cx + sz * 2 // 3, cy - sz // 5),
        (cx + sz * 3 // 4, cy + sz // 4),
    ])
    dp = pts[7] if len(pts) > 7 else (cx, cy - sz // 4)
    pygame.draw.polygon(surf, col, [
        dp,
        (dp[0], dp[1] - sz // 3),
        (dp[0] + sz // 5, dp[1]),
    ])


def _charge_bee(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 4, cy - sz // 4, sz // 2, sz // 2))
    pygame.draw.ellipse(surf, col, (cx - sz * 2 // 3, cy - sz // 3, sz // 2, sz // 4))
    pygame.draw.ellipse(surf, col, (cx + sz // 6,     cy - sz // 3, sz // 2, sz // 4))
    pygame.draw.circle(surf, col, (cx, cy - sz // 4), sz // 8)
    pygame.draw.polygon(surf, col, [
        (cx - sz // 8, cy + sz // 4),
        (cx + sz // 8, cy + sz // 4),
        (cx, cy + sz * 3 // 8),
    ])
    lw = max(1, sz // 10)
    pygame.draw.line(surf, col, (cx - sz // 10, cy - sz // 4),
                     (cx - sz // 4, cy - sz * 2 // 3), lw)
    pygame.draw.line(surf, col, (cx + sz // 10, cy - sz // 4),
                     (cx + sz // 4, cy - sz * 2 // 3), lw)


# ---------------------------------------------------------------------------
# New object / symbol charges
# ---------------------------------------------------------------------------

def _charge_chalice(surf, cx, cy, sz, col):
    pygame.draw.rect(surf, col, (cx - sz // 3, cy + sz * 3 // 8, sz * 2 // 3, sz // 8))
    pygame.draw.rect(surf, col, (cx - sz // 8, cy, sz // 4, sz // 3))
    pygame.draw.circle(surf, col, (cx, cy + sz // 8), sz // 8)
    pygame.draw.polygon(surf, col, [
        (cx - sz // 4, cy),
        (cx - sz // 2, cy - sz // 2),
        (cx + sz // 2, cy - sz // 2),
        (cx + sz // 4, cy),
    ])


def _charge_torch(surf, cx, cy, sz, col):
    hw = max(2, sz // 7)
    pygame.draw.rect(surf, col, (cx - hw // 2, cy, hw, sz // 2))
    lw = max(1, sz // 12)
    for i in range(3):
        y = cy + sz // 6 + i * sz // 8
        pygame.draw.line(surf, col, (cx - hw, y), (cx + hw, y), lw)
    pygame.draw.polygon(surf, col, [
        (cx,            cy - sz // 2),
        (cx - sz // 4,  cy - sz // 8),
        (cx - sz // 6,  cy),
        (cx + sz // 6,  cy),
        (cx + sz // 4,  cy - sz // 8),
    ])
    pygame.draw.polygon(surf, col, [
        (cx,            cy - sz * 2 // 5),
        (cx - sz // 8,  cy - sz // 8),
        (cx + sz // 8,  cy - sz // 8),
    ])


def _charge_lantern(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.arc(surf, col,
                    (cx - sz // 6, cy - sz * 2 // 3, sz // 3, sz // 4),
                    0, math.pi, lw)
    bx, by = cx - sz // 4, cy - sz // 3
    bw, bh = sz // 2, sz * 2 // 3
    pygame.draw.rect(surf, col, (bx, by, bw, bh), lw)
    pygame.draw.line(surf, col, (bx, by + bh // 3),  (bx + bw, by + bh // 3), lw)
    pygame.draw.line(surf, col, (bx, by + bh * 2 // 3), (bx + bw, by + bh * 2 // 3), lw)
    pygame.draw.line(surf, col, (bx + bw // 2, by), (bx + bw // 2, by + bh), lw)
    pygame.draw.circle(surf, col, (cx, cy), max(3, sz // 6))
    pygame.draw.rect(surf, col, (cx - sz // 3, cy + sz // 3, sz * 2 // 3, sz // 10))


def _charge_portcullis(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    top, bot = cy - sz // 2, cy + sz // 3
    for x in (cx - sz // 3, cx - sz // 9, cx + sz // 9, cx + sz // 3):
        pygame.draw.line(surf, col, (x, top), (x, bot), lw)
        pygame.draw.polygon(surf, col, [
            (x - lw, bot), (x + lw, bot), (x, bot + sz // 8),
        ])
    for y in (top, top + sz // 4, top + sz // 2):
        pygame.draw.line(surf, col, (cx - sz // 3, y), (cx + sz // 3, y), lw)


def _charge_orb(surf, cx, cy, sz, col):
    r  = sz // 3
    lw = max(2, sz // 8)
    pygame.draw.circle(surf, col, (cx, cy + sz // 8), r, lw)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz // 2, lw, sz // 4))
    pygame.draw.rect(surf, col, (cx - sz // 5,  cy - sz * 2 // 5, sz * 2 // 5, lw))
    pygame.draw.line(surf, col, (cx - r, cy + sz // 8), (cx + r, cy + sz // 8), lw)


def _charge_hourglass(surf, cx, cy, sz, col):
    pygame.draw.polygon(surf, col, [
        (cx - sz // 2, cy - sz // 2),
        (cx + sz // 2, cy - sz // 2),
        (cx, cy),
    ])
    pygame.draw.polygon(surf, col, [
        (cx, cy),
        (cx - sz // 2, cy + sz // 2),
        (cx + sz // 2, cy + sz // 2),
    ])
    th = max(3, sz // 8)
    pygame.draw.rect(surf, col, (cx - sz // 2, cy - sz // 2 - th // 2, sz, th))
    pygame.draw.rect(surf, col, (cx - sz // 2, cy + sz // 2 - th // 2, sz, th))


def _charge_scales(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz // 2, lw, sz))
    pygame.draw.rect(surf, col, (cx - sz // 2, cy - sz // 3, sz, lw))
    pygame.draw.line(surf, col, (cx - sz // 2, cy - sz // 3), (cx - sz // 2, cy), lw)
    pygame.draw.line(surf, col, (cx + sz // 2, cy - sz // 3), (cx + sz // 2, cy), lw)
    pygame.draw.arc(surf, col,
                    (cx - sz * 3 // 4, cy - sz // 8, sz // 2, sz // 4),
                    math.pi, math.tau, lw)
    pygame.draw.arc(surf, col,
                    (cx + sz // 4,     cy - sz // 8, sz // 2, sz // 4),
                    math.pi, math.tau, lw)


def _charge_acorn(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 4, cy - sz // 8, sz // 2, sz // 2))
    pygame.draw.ellipse(surf, col, (cx - sz // 3, cy - sz // 4, sz * 2 // 3, sz // 3))
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz // 2, lw, sz // 4))


def _charge_oak_leaf(surf, cx, cy, sz, col):
    left = [(-0.0, -0.50), (-0.30, -0.40), (-0.50, -0.30), (-0.35, -0.20),
            (-0.50,  0.00), (-0.35,  0.10), (-0.45,  0.25), (-0.25,  0.30),
            (-0.10,  0.50)]
    right = [(0.0, -0.50), (0.30, -0.40), (0.50, -0.30), (0.35, -0.20),
             (0.50,  0.00), (0.35,  0.10), (0.45,  0.25), (0.25,  0.30),
             (0.10,  0.50)]
    pts = ([(cx + int(x * sz), cy + int(y * sz)) for x, y in left] +
           [(cx + int(x * sz), cy + int(y * sz)) for x, y in reversed(right)])
    pygame.draw.polygon(surf, col, pts)
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy + sz // 2, lw, sz // 5))


def _charge_thistle(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy, lw, sz // 2))
    pygame.draw.polygon(surf, col, [(cx, cy + sz // 8), (cx - sz // 3, cy + sz // 4), (cx, cy + sz // 3)])
    pygame.draw.polygon(surf, col, [(cx, cy + sz // 8), (cx + sz // 3, cy + sz // 4), (cx, cy + sz // 3)])
    r = sz // 4
    pygame.draw.circle(surf, col, (cx, cy - sz // 6), r)
    for i in range(10):
        a = i * math.tau / 10
        x1 = cx + int(r * math.cos(a))
        y1 = (cy - sz // 6) + int(r * math.sin(a))
        x2 = cx + int((r + sz // 6) * math.cos(a))
        y2 = (cy - sz // 6) + int((r + sz // 6) * math.sin(a))
        pygame.draw.line(surf, col, (x1, y1), (x2, y2), lw)


def _charge_grapes(surf, cx, cy, sz, col):
    r = max(3, sz // 7)
    sp = r * 2 + max(1, sz // 12)
    for gx, gy in [(0, -2), (-1, -1), (1, -1), (-2, 0), (0, 0), (2, 0),
                   (-3, 1), (-1, 1), (1, 1), (3, 1)]:
        pygame.draw.circle(surf, col, (cx + gx * sp // 2, cy + gy * sp // 2), r)
    lw = max(2, sz // 9)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz * 2 // 3, lw, sz // 4))
    pygame.draw.ellipse(surf, col, (cx - sz // 5, cy - sz * 2 // 3, sz * 2 // 5, sz // 5))


def _charge_eye(surf, cx, cy, sz, col):
    pygame.draw.polygon(surf, col, [
        (cx - sz // 2, cy),
        (cx - sz // 4, cy - sz // 4),
        (cx + sz // 4, cy - sz // 4),
        (cx + sz // 2, cy),
        (cx + sz // 4, cy + sz // 4),
        (cx - sz // 4, cy + sz // 4),
    ])
    pygame.draw.circle(surf, col, (cx, cy), sz // 4, max(2, sz // 8))
    pygame.draw.circle(surf, col, (cx, cy), sz // 8)


def _charge_gauntlet(surf, cx, cy, sz, col):
    pygame.draw.rect(surf, col, (cx - sz // 3, cy + sz // 4, sz * 2 // 3, sz // 4))
    pygame.draw.rect(surf, col, (cx - sz // 4, cy - sz // 4, sz // 2, sz // 2))
    fw = max(2, sz // 8)
    for i in range(4):
        fx = cx - sz // 4 + i * (sz // 4 - fw // 4)
        pygame.draw.rect(surf, col, (fx, cy - sz // 2, fw, sz // 4))
    pygame.draw.rect(surf, col, (cx + sz // 4, cy - sz // 6, sz // 6, sz // 5))


def _charge_helmet(surf, cx, cy, sz, col):
    pygame.draw.polygon(surf, col, [
        (cx - sz // 2, cy),
        (cx - sz // 2, cy - sz // 4),
        (cx - sz // 3, cy - sz // 2),
        (cx + sz // 3, cy - sz // 2),
        (cx + sz // 2, cy - sz // 4),
        (cx + sz // 2, cy),
    ])
    lw = max(2, sz // 8)
    for i in range(3):
        y = cy - sz // 8 + i * sz // 12
        pygame.draw.line(surf, col, (cx - sz // 3, y), (cx + sz // 3, y), lw)
    pygame.draw.rect(surf, col, (cx - sz // 2, cy, sz // 4, sz // 3))
    pygame.draw.rect(surf, col, (cx + sz // 4, cy, sz // 4, sz // 3))
    pygame.draw.polygon(surf, col, [
        (cx - sz // 8, cy - sz // 2),
        (cx,            cy - sz * 3 // 4),
        (cx + sz // 8, cy - sz // 2),
    ])


def _charge_buckler(surf, cx, cy, sz, col):
    r  = sz // 3
    lw = max(3, sz // 7)
    pygame.draw.circle(surf, col, (cx, cy), r, lw)
    pygame.draw.circle(surf, col, (cx, cy), r // 3)
    pygame.draw.circle(surf, col, (cx, cy), r + lw // 2, max(2, sz // 12))


def _charge_mill(surf, cx, cy, sz, col):
    pygame.draw.circle(surf, col, (cx, cy), max(4, sz // 8))
    for i in range(4):
        a = i * math.pi / 2 + math.pi / 8
        dx, dy = int(sz // 2 * math.cos(a)), int(sz // 2 * math.sin(a))
        pa = a + math.pi / 2
        w  = max(3, sz // 6)
        px, py = int(w * math.cos(pa)), int(w * math.sin(pa))
        pygame.draw.polygon(surf, col, [
            (cx + px,       cy + py),
            (cx + dx + px,  cy + dy + py),
            (cx + dx - px,  cy + dy - py),
            (cx - px,       cy - py),
        ])


def _charge_boot(surf, cx, cy, sz, col):
    pygame.draw.rect(surf, col, (cx - sz // 4, cy - sz // 2, sz // 2, sz * 2 // 3))
    pygame.draw.polygon(surf, col, [
        (cx - sz // 4, cy + sz // 6),
        (cx - sz // 4, cy + sz // 3),
        (cx + sz // 2, cy + sz // 3),
        (cx + sz // 2, cy + sz // 5),
        (cx + sz // 4, cy + sz // 6),
    ])
    pygame.draw.ellipse(surf, col, (cx + sz // 4, cy + sz // 5, sz // 4, sz // 5))
    pygame.draw.rect(surf, col, (cx - sz // 4, cy + sz // 3, sz * 3 // 4, sz // 10))


def _charge_bridge(surf, cx, cy, sz, col):
    lw = max(3, sz // 8)
    pygame.draw.rect(surf, col, (cx - sz // 2, cy - sz // 8, sz, lw))
    pygame.draw.arc(surf, col,
                    (cx - sz // 3, cy - sz // 3, sz * 2 // 3, sz // 2),
                    0, math.pi, lw * 2)
    pygame.draw.rect(surf, col, (cx - sz // 3, cy - sz // 8, sz // 8, sz // 3))
    pygame.draw.rect(surf, col, (cx + sz // 5, cy - sz // 8, sz // 8, sz // 3))
    bw = max(4, sz // 8)
    for ox in range(-sz // 2, sz // 2, bw * 2):
        pygame.draw.rect(surf, col, (cx + ox, cy - sz // 4, bw, sz // 8))


def _charge_candle(surf, cx, cy, sz, col):
    pygame.draw.ellipse(surf, col, (cx - sz // 5, cy + sz // 3, sz * 2 // 5, sz // 8))
    pygame.draw.rect(surf, col, (cx - sz // 6, cy - sz // 4, sz // 3, sz * 2 // 3))
    lw = max(2, sz // 9)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz // 3, lw, sz // 8))
    pygame.draw.polygon(surf, col, [
        (cx,            cy - sz * 2 // 3),
        (cx - sz // 6,  cy - sz // 3),
        (cx + sz // 6,  cy - sz // 3),
    ])
    pygame.draw.polygon(surf, col, [
        (cx,            cy - sz // 2),
        (cx - sz // 10, cy - sz // 3),
        (cx + sz // 10, cy - sz // 3),
    ])


# ---------------------------------------------------------------------------
# New weapon / tool charges
# ---------------------------------------------------------------------------

def _charge_mace(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy, lw, sz // 2))
    r = sz // 4
    pygame.draw.circle(surf, col, (cx, cy - r), r)
    for i in range(6):
        a = i * math.tau / 6
        x1 = cx + int(r * math.cos(a))
        y1 = (cy - r) + int(r * math.sin(a))
        x2 = cx + int((r + sz // 5) * math.cos(a))
        y2 = (cy - r) + int((r + sz // 5) * math.sin(a))
        pygame.draw.line(surf, col, (x1, y1), (x2, y2), max(3, sz // 6))


def _charge_trident(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - lw // 2, cy - sz // 3, lw, sz * 5 // 6))
    for ox in (-sz // 3, 0, sz // 3):
        pygame.draw.rect(surf, col, (cx + ox - lw // 2, cy - sz // 2, lw, sz // 4))
        pygame.draw.polygon(surf, col, [
            (cx + ox - lw, cy - sz // 2),
            (cx + ox + lw, cy - sz // 2),
            (cx + ox,      cy - sz * 2 // 3),
        ])
    pygame.draw.rect(surf, col, (cx - sz // 3, cy - sz // 3, sz * 2 // 3, lw))


def _charge_scythe(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.line(surf, col,
                     (cx - sz // 3, cy + sz // 2),
                     (cx + sz // 3, cy - sz // 2), lw)
    pygame.draw.arc(surf, col,
                    (cx - sz // 4, cy - sz * 2 // 3, sz * 2 // 3, sz // 2),
                    math.pi * 0.1, math.pi * 0.9, max(3, sz // 5))


def _charge_crossbow(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - sz // 2, cy - lw, sz, lw * 2))
    pygame.draw.rect(surf, col, (cx - lw // 2, cy, lw, sz // 3))
    pygame.draw.arc(surf, col,
                    (cx - sz // 2, cy - sz // 3, sz // 3, sz * 2 // 3),
                    math.pi * 0.5, math.pi * 1.5, lw * 2)
    pygame.draw.arc(surf, col,
                    (cx + sz // 6, cy - sz // 3, sz // 3, sz * 2 // 3),
                    -math.pi * 0.5, math.pi * 0.5, lw * 2)
    pygame.draw.line(surf, col, (cx - sz // 3, cy - sz // 3), (cx - sz // 3, cy + sz // 3), lw)
    pygame.draw.line(surf, col, (cx + sz // 3, cy - sz // 3), (cx + sz // 3, cy + sz // 3), lw)


def _charge_dagger(surf, cx, cy, sz, col):
    bw = max(3, sz // 5)
    pygame.draw.polygon(surf, col, [
        (cx - bw // 2, cy - sz // 8),
        (cx + bw // 2, cy - sz // 8),
        (cx + bw // 4, cy - sz // 2),
        (cx,           cy - sz * 2 // 3),
        (cx - bw // 4, cy - sz // 2),
    ])
    pygame.draw.rect(surf, col,
                     (cx - sz // 3, cy - sz // 8 - sz // 12, sz * 2 // 3, sz // 6))
    pygame.draw.rect(surf, col, (cx - sz // 10, cy - sz // 8, sz // 5, sz // 3))
    pygame.draw.circle(surf, col, (cx, cy + sz // 5), max(3, sz // 6))


def _charge_lance(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.line(surf, col,
                     (cx - sz // 2, cy + sz // 2),
                     (cx + sz // 3, cy - sz // 3), lw * 2)
    pygame.draw.polygon(surf, col, [
        (cx + sz // 3, cy - sz // 3),
        (cx + sz // 4, cy - sz // 2),
        (cx + sz // 2, cy - sz // 2),
    ])
    pygame.draw.polygon(surf, col, [
        (cx, cy),
        (cx + sz // 5, cy - sz // 4),
        (cx + sz // 3, cy - sz // 8),
    ])


def _charge_anvil(surf, cx, cy, sz, col):
    pygame.draw.polygon(surf, col, [
        (cx - sz // 2, cy - sz // 8),
        (cx - sz // 4, cy - sz // 3),
        (cx - sz // 4, cy - sz // 8),
    ])
    pygame.draw.rect(surf, col, (cx - sz // 3, cy - sz // 3, sz * 2 // 3, sz // 4))
    pygame.draw.rect(surf, col, (cx - sz // 5, cy - sz // 8, sz * 2 // 5, sz // 5))
    pygame.draw.rect(surf, col, (cx - sz // 2, cy + sz // 8, sz, sz // 4))


def _charge_plow(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - sz // 2, cy - sz // 8, sz * 3 // 4, lw * 2))
    pygame.draw.line(surf, col,
                     (cx + sz // 4, cy - sz // 8),
                     (cx + sz // 2, cy - sz // 2), lw * 2)
    pygame.draw.rect(surf, col, (cx - sz // 4, cy - sz // 8, lw * 2, sz // 4))
    pygame.draw.polygon(surf, col, [
        (cx - sz // 3, cy + sz // 8),
        (cx,           cy + sz // 3),
        (cx + sz // 6, cy + sz // 8),
    ])


def _charge_quiver(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.rect(surf, col, (cx - sz // 5, cy - sz // 4, sz * 2 // 5, sz * 3 // 4), lw)
    pygame.draw.rect(surf, col, (cx - sz // 5, cy + sz // 2, sz * 2 // 5, sz // 10))
    for ox in (-sz // 8, 0, sz // 8):
        pygame.draw.line(surf, col, (cx + ox, cy - sz // 4),
                         (cx + ox, cy - sz * 2 // 3), max(1, lw // 2))
        pygame.draw.polygon(surf, col, [
            (cx + ox,              cy - sz * 2 // 3),
            (cx + ox - sz // 12,   cy - sz // 2),
            (cx + ox + sz // 12,   cy - sz // 2),
        ])


def _charge_cannon(surf, cx, cy, sz, col):
    pygame.draw.rect(surf, col, (cx - sz // 2, cy - sz // 6, sz * 3 // 4, sz // 3))
    lw = max(2, sz // 8)
    for ox in (cx - sz // 2, cx - sz // 3, cx + sz // 8):
        pygame.draw.rect(surf, col, (ox, cy - sz // 5, sz // 10, sz * 2 // 5))
    pygame.draw.rect(surf, col, (cx + sz // 4, cy - sz // 5, sz // 5, sz * 2 // 5))
    r = sz // 5
    pygame.draw.circle(surf, col, (cx - sz // 4, cy + sz // 5), r, lw * 2)
    pygame.draw.circle(surf, col, (cx + sz // 8, cy + sz // 5), r, lw * 2)
    pygame.draw.rect(surf, col,
                     (cx - sz // 4 - r // 2, cy + sz // 5 - lw // 2, sz // 3 + r, lw))


# ---------------------------------------------------------------------------
# New nature charges
# ---------------------------------------------------------------------------

def _charge_mountain(surf, cx, cy, sz, col):
    pygame.draw.polygon(surf, col, [
        (cx - sz // 2, cy + sz // 3),
        (cx - sz // 8, cy - sz // 2),
        (cx + sz // 3, cy + sz // 3),
    ])
    pygame.draw.polygon(surf, col, [
        (cx - sz // 6, cy + sz // 3),
        (cx + sz // 4, cy - sz // 3),
        (cx + sz // 2, cy + sz // 3),
    ])


def _charge_waves(surf, cx, cy, sz, col):
    lw = max(3, sz // 6)
    for i in range(3):
        y = cy - sz // 4 + i * sz // 4
        pygame.draw.arc(surf, col,
                        (cx - sz // 2, y - sz // 8, sz // 2, sz // 4),
                        0, math.pi, lw)
        pygame.draw.arc(surf, col,
                        (cx,           y - sz // 8, sz // 2, sz // 4),
                        math.pi, math.tau, lw)


def _charge_lightning(surf, cx, cy, sz, col):
    pygame.draw.polygon(surf, col, [
        (cx + sz // 4,  cy - sz // 2),
        (cx,            cy - sz // 8),
        (cx + sz // 4,  cy - sz // 8),
        (cx - sz // 4,  cy + sz // 2),
        (cx,            cy + sz // 8),
        (cx - sz // 4,  cy + sz // 8),
    ])


def _charge_snowflake(surf, cx, cy, sz, col):
    lw = max(2, sz // 7)
    for i in range(6):
        a = i * math.pi / 3
        x1 = cx + int(sz // 2 * math.cos(a))
        y1 = cy + int(sz // 2 * math.sin(a))
        pygame.draw.line(surf, col, (cx, cy), (x1, y1), lw)
        for sign in (-1, 1):
            bx = cx + int(sz // 4 * math.cos(a))
            by = cy + int(sz // 4 * math.sin(a))
            ba = a + sign * math.pi / 3
            pygame.draw.line(surf, col, (bx, by),
                             (bx + int(sz // 5 * math.cos(ba)),
                              by + int(sz // 5 * math.sin(ba))), lw)
    pygame.draw.circle(surf, col, (cx, cy), max(3, sz // 8))


def _charge_flame(surf, cx, cy, sz, col):
    pygame.draw.polygon(surf, col, [
        (cx,            cy - sz * 2 // 3),
        (cx - sz // 4,  cy - sz // 4),
        (cx - sz // 3,  cy + sz // 3),
        (cx + sz // 3,  cy + sz // 3),
        (cx + sz // 4,  cy - sz // 4),
    ])
    pygame.draw.polygon(surf, col, [
        (cx - sz // 8, cy - sz // 3),
        (cx - sz // 4, cy),
        (cx - sz // 4, cy + sz // 3),
        (cx,           cy + sz // 3),
    ])
    pygame.draw.polygon(surf, col, [
        (cx + sz // 8, cy - sz // 3),
        (cx + sz // 4, cy),
        (cx + sz // 4, cy + sz // 3),
        (cx,           cy + sz // 3),
    ])
    pygame.draw.rect(surf, col, (cx - sz // 3, cy + sz // 3, sz * 2 // 3, sz // 8))


def _charge_cloud(surf, cx, cy, sz, col):
    pygame.draw.rect(surf, col, (cx - sz // 2, cy - sz // 8, sz, sz // 3))
    for ox, r in ((-sz // 3, sz // 5), (-sz // 8, sz // 3),
                  (sz // 8,  sz // 3), (sz // 3,  sz // 5)):
        pygame.draw.circle(surf, col, (cx + ox, cy - sz // 8), r)
    pygame.draw.circle(surf, col, (cx - sz // 2, cy + sz // 8), sz // 6)
    pygame.draw.circle(surf, col, (cx + sz // 2, cy + sz // 8), sz // 6)


def _charge_comet(surf, cx, cy, sz, col):
    pygame.draw.circle(surf, col, (cx + sz // 4, cy - sz // 4), sz // 5)
    pygame.draw.circle(surf, col, (cx + sz // 4, cy - sz // 4), sz // 3, max(1, sz // 12))
    tip = (cx + sz // 4, cy - sz // 4)
    for end, w in (((cx - sz // 2, cy + sz // 3), max(3, sz // 6)),
                   ((cx - sz // 3, cy + sz // 2), max(2, sz // 9)),
                   ((cx - sz // 2, cy + sz // 8), max(2, sz // 9))):
        pygame.draw.line(surf, col, tip, end, w)


# ---------------------------------------------------------------------------
# New architecture / misc charges
# ---------------------------------------------------------------------------

def _charge_gate(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    tw = sz // 5
    for bx in (cx - sz // 2, cx + sz // 2 - tw):
        pygame.draw.rect(surf, col, (bx, cy - sz // 3, tw, sz * 2 // 3))
        for i in range(3):
            pygame.draw.rect(surf, col,
                             (bx + i * tw // 2, cy - sz // 3 - sz // 8, tw // 3, sz // 8))
    ar = sz // 3
    pygame.draw.arc(surf, col,
                    (cx - ar, cy - ar, ar * 2, ar * 2),
                    0, math.pi, lw * 2)
    pygame.draw.rect(surf, col, (cx - ar, cy, lw * 2, sz // 3))
    pygame.draw.rect(surf, col, (cx + ar - lw * 2, cy, lw * 2, sz // 3))


def _charge_harp(surf, cx, cy, sz, col):
    lw = max(2, sz // 8)
    pygame.draw.arc(surf, col,
                    (cx - sz // 2, cy - sz // 2, sz * 3 // 4, sz),
                    math.pi * 0.2, math.pi * 0.9, lw * 2)
    pygame.draw.rect(surf, col, (cx - sz // 3, cy - sz // 4, lw * 2, sz * 3 // 4))
    pygame.draw.rect(surf, col,
                     (cx - sz // 3, cy + sz // 3, sz * 7 // 12, sz // 8))
    string_tops = [
        (cx - sz // 4, cy - sz // 4),
        (cx - sz // 8, cy - sz * 2 // 5),
        (cx,           cy - sz // 2),
        (cx + sz // 8, cy - sz * 2 // 5),
        (cx + sz // 4, cy - sz // 4),
    ]
    base_y = cy + sz // 3
    for sx, sy in string_tops:
        pygame.draw.line(surf, col, (sx, sy), (sx, base_y), max(1, lw // 2))
