import hashlib
from dataclasses import dataclass, field


@dataclass
class Sculpture:
    uid: str
    mineral: str          # item id of mineral used ("limestone_chip", etc.)
    height: int           # 1–4 blocks tall
    grid: list            # list[list[bool]] — height*4 rows × 8 cols; True = stone
    color: tuple          # base mineral RGB as (r,g,b)
    template: str         # "custom" or template name
    seed: int

    def to_dict(self):
        return {
            "uid": self.uid,
            "mineral": self.mineral,
            "height": self.height,
            "grid": self.grid,
            "color": list(self.color),
            "template": self.template,
            "seed": self.seed,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            uid=d["uid"],
            mineral=d["mineral"],
            height=d["height"],
            grid=d["grid"],
            color=tuple(d["color"]),
            template=d["template"],
            seed=d["seed"],
        )


MINERAL_COLORS = {
    # Common stones
    "limestone_chip":  (200, 195, 175),
    "granite_slab":    (150, 140, 135),
    "polished_marble": (230, 225, 220),
    "basalt_chunk":    (80,  80,  85),
    "magmatic_stone":  (110, 60,  50),
    # Rare underground stones
    "marble_chunk":    (235, 232, 222),
    "alabaster_chunk": (232, 218, 198),
    "verdite_slab":    (50,  115,  65),
    "onyx_slab":       (32,   26,  42),
}

# Minerals that can be used for sculpting (item_id -> display name)
SCULPTABLE_MINERALS = {
    # Common
    "limestone_chip":  "Limestone",
    "granite_slab":    "Granite",
    "polished_marble": "Marble (deco)",
    "basalt_chunk":    "Basalt",
    "magmatic_stone":  "Magmatic",
    # Rare underground finds
    "marble_chunk":    "Marble",
    "alabaster_chunk": "Alabaster",
    "verdite_slab":    "Verdite",
    "onyx_slab":       "Onyx",
}


# ── Template grid builders ────────────────────────────────────────────────────
# Each returns a list of (height*4) rows, each row a list of 8 bools.
# Row 0 = TOP of the sculpture.

def _full(h):
    return [[True] * 8 for _ in range(h * 4)]

def _empty(h):
    return [[False] * 8 for _ in range(h * 4)]

def _make_pillar_grid(height):
    rows = height * 4
    g = _empty(height)
    for r in range(rows):
        # Wide cap/base on first and last 2 rows, narrow shaft in between
        if r < 2 or r >= rows - 2:
            g[r] = [True, True, True, True, True, True, True, True]
        else:
            g[r] = [False, False, True, True, True, True, False, False]
    return g

def _make_arch_grid(height):
    rows = height * 4
    g = _full(height)
    # Hollow out the inside arch (top two-thirds, middle 4 cols)
    arch_start = 0
    arch_end   = max(1, rows - 2)
    for r in range(arch_start, arch_end):
        g[r][2] = False
        g[r][3] = False
        g[r][4] = False
        g[r][5] = False
    return g

def _make_pedestal_grid(height):
    rows = height * 4
    g = _empty(height)
    for r in range(rows):
        frac = r / max(1, rows - 1)   # 0.0 = top, 1.0 = bottom
        # Taper: bottom is wide (8), top is narrow (4)
        w = int(4 + 4 * frac)
        pad = (8 - w) // 2
        for c in range(pad, pad + w):
            g[r][c] = True
    return g

def _make_obelisk_grid(height):
    rows = height * 4
    g = _empty(height)
    for r in range(rows):
        frac = r / max(1, rows - 1)   # 0 = top (point), 1 = bottom (wide)
        w = max(2, int(2 + 5 * frac))
        w = min(w, 8)
        pad = (8 - w) // 2
        for c in range(pad, pad + w):
            g[r][c] = True
    return g

def _make_ruins_grid(height):
    import random
    rng = random.Random(42)
    rows = height * 4
    g = _full(height)
    # Randomly remove chunks from the top to simulate crumbling
    for r in range(rows):
        for c in range(8):
            depth_frac = r / max(1, rows - 1)   # 0 = top, 1 = bottom
            # Higher up = more likely to be missing
            if rng.random() > 0.3 + 0.6 * depth_frac:
                g[r][c] = False
    # Ensure base row is always solid
    g[-1] = [True] * 8
    return g

def _make_lattice_grid(height):
    rows = height * 4
    g = _empty(height)
    for r in range(rows):
        for c in range(8):
            # Checkerboard-ish lattice with 2-wide bars
            if (r // 2 + c // 2) % 2 == 0:
                g[r][c] = True
    # Solid border
    for c in range(8):
        g[0][c] = True
        g[-1][c] = True
    for r in range(rows):
        g[r][0] = True
        g[r][7] = True
    return g

def _make_monolith_grid(height):
    g = _empty(height)
    rows = height * 4
    # Solid rectangular block with slight taper at top
    for r in range(rows):
        if r < 2:
            g[r] = [False, True, True, True, True, True, True, False]
        else:
            g[r] = [True, True, True, True, True, True, True, True]
    return g

def _make_column_grid(height):
    rows = height * 4
    g = _empty(height)
    for r in range(rows):
        if r < 2 or r >= rows - 2:
            # Capital and base: full width
            g[r] = [True] * 8
        elif r == 2 or r == rows - 3:
            g[r] = [False, True, True, True, True, True, True, False]
        else:
            # Fluted shaft: 4-wide with notches
            for c in range(8):
                g[r][c] = c in (1, 2, 3, 4, 5, 6)
    return g

def _make_effigy_grid(height):
    rows = height * 4
    g = _empty(height)
    if rows < 8:
        return _make_monolith_grid(height)
    # Head (top 3 rows)
    for r in range(3):
        g[r] = [False, False, True, True, True, True, False, False]
    # Shoulders
    g[3] = [False, True, True, True, True, True, True, False]
    # Body
    for r in range(4, max(4, rows - 4)):
        g[r] = [False, True, True, True, True, True, True, False]
    # Legs / base
    for r in range(max(4, rows - 4), rows):
        if (r - (rows - 4)) < 2:
            g[r] = [True, False, True, True, True, True, False, True]
        else:
            g[r] = [True, False, True, True, True, True, False, True]
    return g


def _make_pyramid_grid(height):
    rows = height * 4
    g = _empty(height)
    for r in range(rows):
        frac = r / max(1, rows - 1)   # 0=top(point) 1=bottom(wide)
        w    = max(2, round(2 + 6 * frac))
        pad  = (8 - min(8, w)) // 2
        for c in range(pad, 8 - pad): g[r][c] = True
    return g

def _make_diamond_grid(height):
    rows = height * 4
    g    = _empty(height)
    half = (rows - 1) / 2
    for r in range(rows):
        dist = abs(r - half) / max(1, half)
        w    = max(2, round(8 - 6 * dist))
        pad  = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    return g

def _make_cross_grid(height):
    rows    = height * 4
    g       = _empty(height)
    h_top   = rows // 5
    h_bot   = h_top + max(2, rows // 4)
    for r in range(rows):
        g[r][3] = g[r][4] = True         # vertical bar
        if h_top <= r < h_bot:
            g[r] = [True] * 8            # horizontal bar
    return g

def _make_hourglass_grid(height):
    rows = height * 4
    g    = _empty(height)
    half = (rows - 1) / 2
    for r in range(rows):
        dist = abs(r - half) / max(1, half)
        w    = max(2, round(2 + 6 * dist))
        pad  = (8 - min(8, w)) // 2
        for c in range(pad, 8 - pad): g[r][c] = True
    return g

def _make_frame_grid(height):
    rows = height * 4
    g    = _empty(height)
    for r in range(rows):
        if r < 2 or r >= rows - 2:
            g[r] = [True] * 8
        else:
            g[r][0] = g[r][1] = g[r][6] = g[r][7] = True
    return g

def _make_bars_grid(height):
    rows = height * 4
    g    = [[c in (0, 1, 3, 4, 6, 7) for c in range(8)] for _ in range(rows)]
    g[0] = g[-1] = [True] * 8
    return g

def _make_candle_grid(height):
    rows      = height * 4
    g         = _empty(height)
    flame_end = max(2, rows // 4)
    for r in range(flame_end):
        frac = r / max(1, flame_end - 1)
        w    = max(2, round(4 - 2 * frac))
        pad  = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    for r in range(flame_end, rows):
        g[r][3] = g[r][4] = True
    # small wax drip streaks
    if flame_end < rows - 1: g[flame_end][2] = True
    if flame_end + 1 < rows: g[flame_end + 1][5] = True
    return g

def _make_tower_grid(height):
    rows = height * 4
    g    = _full(height)
    # Battlements: three notches in top 2 rows
    for nc in (1, 4, 7):
        g[0][nc] = False
        if rows > 1: g[1][nc] = False
    # Arrow slit in middle
    if rows >= 8:
        mid = rows // 2
        for dr in range(2):
            for dc in (3, 4):
                if mid + dr < rows: g[mid + dr][dc] = False
    return g

def _make_step_pyramid_grid(height):
    rows  = height * 4
    steps = min(4, max(2, rows // 3))
    g     = _empty(height)
    sh    = max(1, rows // steps)
    for s in range(steps):
        r0  = s * sh;  r1 = min(rows, r0 + sh)
        w   = max(2, 8 - s * 2)
        pad = (8 - w) // 2
        for r in range(r0, r1):
            for c in range(pad, pad + w): g[r][c] = True
    for r in range(steps * sh, rows):
        w = max(2, 8 - (steps - 1) * 2); pad = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    return g

def _make_gate_grid(height):
    rows = height * 4
    g    = _empty(height)
    for r in range(rows):
        g[r][0] = g[r][1] = g[r][6] = g[r][7] = True
    g[0] = [True] * 8
    if rows > 1: g[1] = [True] * 8
    arch_end = max(3, rows // 3)
    for r in range(2, arch_end):
        frac   = (r - 2) / max(1, arch_end - 2)
        cstart = 2 + round(frac * 2)
        cend   = 5 - round(frac * 2)
        for c in range(cstart, max(cstart + 1, cend + 1)):
            g[r][c] = True
    return g

def _make_tree_grid(height):
    rows       = height * 4
    g          = _empty(height)
    trunk_from = max(rows - 3, rows * 2 // 3)
    for r in range(trunk_from, rows):
        g[r][3] = g[r][4] = True
    for r in range(trunk_from):
        frac = r / max(1, trunk_from - 1)
        w    = 2 if r == 0 else max(2, round(2 + 5 * frac))
        pad  = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    return g

def _make_mushroom_grid(height):
    rows       = height * 4
    g          = _empty(height)
    stem_from  = max(2, rows * 2 // 3)
    for r in range(stem_from, rows):
        g[r][3] = g[r][4] = True
    for r in range(stem_from):
        frac = r / max(1, stem_from - 1)
        w    = max(4, round(7 - 3 * frac))
        pad  = (8 - min(8, w)) // 2
        for c in range(pad, 8 - pad): g[r][c] = True
    if stem_from > 0:
        g[stem_from - 1] = [False, False, True, True, True, True, False, False]
    return g

def _make_flame_grid(height):
    import random as _rnd
    rng  = _rnd.Random(999)
    rows = height * 4
    g    = _empty(height)
    for r in range(rows):
        frac   = r / max(1, rows - 1)
        w      = max(1, round(1 + 6 * frac))
        jitter = round((rng.random() - 0.5) * 2 * max(0, 1 - frac))
        pad    = max(0, min(7, (8 - w) // 2 + jitter))
        w      = min(8 - pad, w)
        for c in range(pad, pad + w): g[r][c] = True
    g[-1] = [True] * 8
    return g

def _make_wave_grid(height):
    import math
    rows = height * 4
    g    = _empty(height)
    hw   = max(1, rows * 0.22)
    for c in range(8):
        center = rows * 0.5 + rows * 0.28 * math.sin(c / 7 * math.pi * 2)
        for r in range(rows):
            if abs(r - center) <= hw: g[r][c] = True
    g[-1] = [True] * 8
    return g

def _make_shield_grid(height):
    rows = height * 4
    g    = _empty(height)
    for r in range(rows):
        frac = r / max(1, rows - 1)
        if frac <= 0.55:
            w = 8
        elif frac <= 0.70:
            w = max(4, round(8 - (frac - 0.55) / 0.15 * 4))
        else:
            w = max(1, round(4 * (1 - (frac - 0.70) / 0.30)))
        pad = (8 - max(1, min(8, w))) // 2
        for c in range(pad, 8 - pad): g[r][c] = True
    return g

def _make_vase_grid(height):
    rows = height * 4
    g    = _empty(height)
    for r in range(rows):
        frac = r / max(1, rows - 1)
        if   frac < 0.08: w = 4
        elif frac < 0.18: w = max(2, round(4 - (frac - 0.08) / 0.10 * 2))
        elif frac < 0.25: w = 2
        elif frac < 0.45: w = round(2 + (frac - 0.25) / 0.20 * 5)
        elif frac < 0.75: w = 7
        elif frac < 0.88: w = round(7 - (frac - 0.75) / 0.13 * 3)
        elif frac < 0.95: w = 4
        else:             w = 6
        w   = max(2, min(8, w))
        pad = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    return g


# ── Renaissance-inspired templates ───────────────────────────────────────────

def _make_corinthian_grid(height):
    """Classical column: wide ornate capital flaring from a narrow shaft and base."""
    rows    = height * 4
    g       = _empty(height)
    cap_end = max(3, rows // 3)
    # Capital: abacus (full) → bell narrows toward neck
    for r in range(cap_end):
        frac = r / max(1, cap_end - 1)
        w    = max(4, round(8 - 3 * frac))
        pad  = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    # Shaft: 4 wide
    for r in range(cap_end, rows - 2):
        for c in range(2, 6): g[r][c] = True
    # Base: wide collar + slab
    g[-2] = [False, True, True, True, True, True, True, False]
    g[-1]  = [True] * 8
    return g

def _make_triumphal_arch_grid(height):
    """Roman triumphal arch: solid attic inscription zone above a semicircular arch passage."""
    import math
    rows   = height * 4
    g      = _full(height)
    attic  = max(2, rows // 4)
    base   = min(2, rows // 4)
    arch_h = rows - attic - base
    if arch_h <= 0: return g
    for r in range(attic, rows - base):
        frac   = (r - attic) / max(1, arch_h - 1)
        if frac <= 0.5:
            open_w = max(0, round(2 + 2 * math.sin(frac * math.pi)))
        else:
            open_w = 4                     # straight-sided passage
        open_w = min(4, open_w)
        start  = (8 - open_w) // 2
        for c in range(start, start + open_w): g[r][c] = False
    return g

def _make_baluster_grid(height):
    """Renaissance railing post: cap, neck, swelling vase body, waist, base."""
    import math
    rows = height * 4
    g    = _empty(height)
    for r in range(rows):
        frac = r / max(1, rows - 1)
        if   frac < 0.05:               w = 8          # cap slab
        elif frac < 0.12:               w = 4          # neck below cap
        elif frac < 0.38:               # upper vase swell
            t = (frac - 0.12) / 0.26
            w = round(4 + 3 * math.sin(t * math.pi))
        elif frac < 0.48:               w = 4          # waist
        elif frac < 0.72:               # lower swell (smaller)
            t = (frac - 0.48) / 0.24
            w = round(4 + 2 * math.sin(t * math.pi))
        elif frac < 0.82:               w = 4          # lower neck
        elif frac < 0.93:               w = 6          # base collar
        else:                           w = 8          # base slab
        w   = max(2, min(8, w))
        pad = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    return g

def _make_bust_grid(height):
    """Portrait bust: oval head, narrow neck, chest broadening to truncated torso, plinth."""
    rows = height * 4
    g    = _empty(height)
    if rows < 6:
        for r in range(rows - 1):
            g[r] = [False, True, True, True, True, True, True, False]
        g[-1] = [True] * 8
        return g
    head_end  = max(3, rows // 3)
    neck_end  = head_end + max(1, rows // 8)
    chest_end = rows - 2
    # Head: oval
    for r in range(head_end):
        frac = r / max(1, head_end - 1)
        dist = abs(frac - 0.4) / 0.6
        w    = max(3, round(6 - 3 * dist * dist))
        pad  = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    # Neck
    for r in range(head_end, neck_end):
        g[r][3] = g[r][4] = True
    # Chest / toga broadening downward
    for r in range(neck_end, chest_end):
        frac = (r - neck_end) / max(1, chest_end - neck_end - 1)
        w    = min(8, round(3 + 5 * frac))
        pad  = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    # Plinth
    g[-2] = [False, True, True, True, True, True, True, False]
    g[-1]  = [True] * 8
    return g

def _make_putto_grid(height):
    """Cherub figure: round head, wide spread wings, small rounded body."""
    rows      = height * 4
    g         = _empty(height)
    head_end  = max(2, rows // 4)
    wing_end  = head_end + max(2, rows // 4)
    # Head
    for r in range(head_end):
        frac = r / max(1, head_end - 1)
        dist = abs(frac - 0.5) / 0.5
        w    = max(2, round(4 - 2 * dist))
        pad  = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    # Wings: full width
    for r in range(head_end, wing_end):
        g[r] = [True] * 8
    # Chubby body tapering below wings
    for r in range(wing_end, rows):
        frac = (r - wing_end) / max(1, rows - wing_end - 1)
        w    = max(2, round(4 - 2 * frac))
        pad  = (8 - w) // 2
        for c in range(pad, pad + w): g[r][c] = True
    return g

def _make_tondo_grid(height):
    """Circular relief medallion — solid disc, the positive form of a moon gate."""
    import math
    rows = height * 4
    g    = _empty(height)
    cx   = 3.5;  cy = (rows - 1) / 2
    rad  = min(rows * 0.48, 3.8)
    for r in range(rows):
        for c in range(8):
            if (c - cx) ** 2 + (r - cy) ** 2 <= rad * rad:
                g[r][c] = True
    return g

def _make_cartouche_grid(height):
    """Ornamental scroll tablet: narrow rolled ends, rectangular body, recessed inner panel."""
    rows = height * 4
    g    = _empty(height)
    for r in range(rows):
        if r == 0 or r == rows - 1:
            for c in range(2, 6): g[r][c] = True          # narrow scroll terminal
        else:
            g[r] = [True] * 8
    # Recessed inner panel on taller versions
    if rows >= 8:
        for r in range(2, rows - 2):
            g[r][2] = g[r][3] = g[r][4] = g[r][5] = False
    return g


# ── Chinese-style templates ───────────────────────────────────────────────────

def _make_pagoda_grid(height):
    """Multi-tiered tower; each tier has a wide overhanging eave, narrowing toward the top."""
    rows  = height * 4
    tiers = min(4, max(2, height + 1))
    g     = _empty(height)
    tier_h    = rows // tiers
    remainder = rows - tier_h * tiers
    r_cur = 0
    for t in range(tiers):
        th    = tier_h + (1 if t >= tiers - remainder else 0)
        r_end = r_cur + th
        body_w = max(2, min(8, 2 + t * 2))   # t=0 narrowest, grows downward
        eave_w = min(8, body_w + 2)
        for r in range(r_cur, r_end):
            if r == rows - 1:                             # solid base row
                g[r] = [True] * 8
            elif r == r_end - 1 and t < tiers - 1:        # eave row
                ep = (8 - eave_w) // 2
                for c in range(ep, ep + eave_w): g[r][c] = True
            else:                                          # body
                bp = (8 - body_w) // 2
                for c in range(bp, bp + body_w): g[r][c] = True
        r_cur = r_end
    # Spire at very top
    g[0] = [False, False, False, True, True, False, False, False]
    return g

def _make_temple_gate_grid(height):
    """Paifang memorial gate: two pillars, sweeping roof, crossbeam below."""
    rows = height * 4
    g    = _empty(height)
    for r in range(rows):
        g[r][0] = g[r][1] = g[r][6] = g[r][7] = True
    roof_h = max(3, rows // 3)
    # Ridge: solid top
    for r in range(min(2, roof_h)):
        g[r] = [True] * 8
    # Upswept eave wings
    if roof_h > 2: g[2] = [True, True, False, False, False, False, True, True]
    if roof_h > 3: g[3] = [True, False, False, False, False, False, False, True]
    # Lintel below roof
    lr = roof_h
    if lr < rows:     g[lr] = [True] * 8
    if lr + 1 < rows: g[lr + 1] = [True] * 8
    return g

def _make_lantern_grid(height):
    """Hanging lantern: oval body widest at centre, decorative tassel fringe below."""
    rows   = height * 4
    g      = _empty(height)
    fringe = max(2, rows // 5)
    body   = rows - fringe - 1
    # Hanging cord
    g[0][3] = g[0][4] = True
    # Oval body
    for r in range(1, body + 1):
        frac = (r - 1) / max(1, body - 1)
        dist = abs(frac - 0.5) / 0.5
        w    = max(2, round(3 + 4 * (1 - dist * 0.75)))
        pad  = (8 - min(8, w)) // 2
        for c in range(pad, 8 - pad): g[r][c] = True
    # Tassel fringe
    for r in range(body + 1, rows):
        pos = r - (body + 1)
        cols = (2, 4, 6) if pos < fringe - 1 else (2, 6)
        for c in cols: g[r][c] = True
    return g

def _make_moon_gate_grid(height):
    """Circular opening cut from a solid stone wall — traditional garden moon gate."""
    import math
    rows = height * 4
    g    = _full(height)
    cx   = 3.5
    cy   = (rows - 1) / 2
    rad  = min(rows * 0.44, 3.4)
    for r in range(rows):
        for c in range(8):
            if (c - cx) ** 2 + (r - cy) ** 2 <= rad * rad:
                g[r][c] = False
    return g

def _make_dragon_coil_grid(height):
    """Sinuous dragon: S-curving serpent body with a broad head at the top."""
    import math
    rows  = height * 4
    g     = _empty(height)
    freqs = max(1, height)
    for r in range(rows):
        cx = 3.5 + 2.6 * math.sin(r / max(1, rows - 1) * math.pi * 2 * freqs)
        for c in range(8):
            if abs(c - cx) < 1.9: g[r][c] = True
    # Head: broader jaw at top 2 rows
    g[0] = [False, False, True, True, True, True, False, False]
    if rows > 1: g[1] = [False, True, True, True, True, True, True, False]
    return g

def _make_foo_dog_grid(height):
    """Seated guardian lion: wide mane, raised front paws, solid haunches."""
    rows = height * 4
    g    = _empty(height)
    if rows < 8:
        for r in range(rows):
            frac = r / max(1, rows - 1)
            w    = 6 if frac < 0.3 else 8
            pad  = (8 - w) // 2
            for c in range(pad, pad + w): g[r][c] = True
        return g
    head_end  = max(3, rows // 4)
    chest_end = max(head_end + 2, rows * 3 // 4)
    # Head / mane
    for r in range(head_end):
        g[r] = [False, True, True, True, True, True, True, False] if r < 2 else [True] * 8
    # Body
    for r in range(head_end, chest_end):
        g[r] = [False, True, True, True, True, True, True, False]
    # Raised front paws
    if chest_end + 1 < rows:
        g[chest_end]     = [True, False, True, True, True, True, False, True]
        g[chest_end + 1] = [True, False, False, True, True, False, False, True]
    # Haunches / base
    for r in range(max(chest_end + 2, rows - 3), rows):
        g[r] = [True] * 8
    return g

def _make_stele_grid(height):
    """Upright memorial stone tablet: rounded top, thick borders, wide base."""
    rows = height * 4
    g    = _empty(height)
    g[0] = [False, True, True, True, True, True, True, False]   # rounded top
    for r in range(1, rows - 2):
        g[r][0] = g[r][1] = g[r][6] = g[r][7] = True
        if r % 3 == 1: g[r][2] = g[r][5] = True                # inscription grooves
    g[-2] = g[-1] = [True] * 8                                  # wide base
    return g


TEMPLATES = {
    # Original 9
    "Pillar":        _make_pillar_grid,
    "Arch":          _make_arch_grid,
    "Pedestal":      _make_pedestal_grid,
    "Obelisk":       _make_obelisk_grid,
    "Ruins":         _make_ruins_grid,
    "Lattice":       _make_lattice_grid,
    "Monolith":      _make_monolith_grid,
    "Column":        _make_column_grid,
    # 16 new ones
    "Pyramid":       _make_pyramid_grid,
    "Diamond":       _make_diamond_grid,
    "Cross":         _make_cross_grid,
    "Hourglass":     _make_hourglass_grid,
    "Frame":         _make_frame_grid,
    "Bars":          _make_bars_grid,
    "Candle":        _make_candle_grid,
    "Tower":         _make_tower_grid,
    "Step Pyramid":  _make_step_pyramid_grid,
    "Gate":          _make_gate_grid,
    "Tree":          _make_tree_grid,
    "Mushroom":      _make_mushroom_grid,
    "Flame":         _make_flame_grid,
    "Wave":          _make_wave_grid,
    "Shield":        _make_shield_grid,
    "Vase":          _make_vase_grid,
    # Renaissance
    "Corinthian":    _make_corinthian_grid,
    "Triumphal Arch": _make_triumphal_arch_grid,
    "Baluster":      _make_baluster_grid,
    "Bust":          _make_bust_grid,
    "Putto":         _make_putto_grid,
    "Tondo":         _make_tondo_grid,
    "Cartouche":     _make_cartouche_grid,
    # Chinese-style
    "Pagoda":        _make_pagoda_grid,
    "Temple Gate":   _make_temple_gate_grid,
    "Lantern":       _make_lantern_grid,
    "Moon Gate":     _make_moon_gate_grid,
    "Dragon Coil":   _make_dragon_coil_grid,
    "Foo Dog":       _make_foo_dog_grid,
    "Stele":         _make_stele_grid,
    # Research-locked
    "Effigy":        _make_effigy_grid,
}

# All available by default (no research required)
BASE_TEMPLATES = [
    "Pillar", "Arch", "Pedestal", "Obelisk", "Ruins", "Lattice", "Monolith", "Column",
    "Pyramid", "Diamond", "Cross", "Hourglass", "Frame", "Bars", "Candle",
    "Tower", "Step Pyramid", "Gate", "Tree", "Mushroom", "Flame", "Wave", "Shield", "Vase",
    "Effigy",
    # Renaissance
    "Corinthian", "Triumphal Arch", "Baluster", "Bust", "Putto", "Tondo", "Cartouche",
    # Chinese
    "Pagoda", "Temple Gate", "Lantern", "Moon Gate", "Dragon Coil", "Foo Dog", "Stele",
]


class SculptureGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter    = 0

    def generate(self, mineral: str, height: int, grid: list, template: str) -> Sculpture:
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid  = hashlib.md5(f"sculpture_{seed}_{self._counter}".encode()).hexdigest()[:12]
        base_color = MINERAL_COLORS.get(mineral, (180, 175, 165))
        # Slight per-sculpture color jitter
        import random
        rng = random.Random(seed)
        jitter = lambda c: max(0, min(255, c + rng.randint(-8, 8)))
        color = tuple(jitter(c) for c in base_color)
        return Sculpture(
            uid=uid,
            mineral=mineral,
            height=height,
            grid=grid,
            color=color,
            template=template,
            seed=seed,
        )
