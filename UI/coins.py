"""Coin collection codex -- CollectionsMixin extension."""
import math
import random
import pygame
from coins import (
    RARITY_COLORS, RARITY_BG, CONDITION_LABELS, CONDITION_SHORT, RARITY_ORDER,
    CONDITIONS, METAL_COLORS, coin_metal, coin_portrait_params, ERROR_TYPES,
)
from constants import SCREEN_W, SCREEN_H


_GOLD   = (218, 182,  55)
_SILVER = (195, 195, 210)
_TITLE  = (245, 230, 160)
_LABEL  = (200, 185, 130)
_DIM    = ( 90,  82,  58)
_CELL   = ( 32,  28,  18)
_BG     = ( 22,  18,  10)

# Rendered coin surface cache  key = (coin.uid, r, side)
_SURF_CACHE: dict = {}


# ---------------------------------------------------------------------------
# Low-level drawing helpers
# ---------------------------------------------------------------------------

def _blend(a: tuple, b: tuple, t: float) -> tuple:
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _draw_portrait(surf, cx, cy, r, params: dict, col: tuple, wear: float):
    """Stylised profile bust carved into the coin face."""
    if r < 7:
        return
    f = 1 if params["facing_right"] else -1
    s = r * 0.52
    dark = _blend(col, (0, 0, 0), 0.25)

    pts = [
        (cx + f*s*0.22, cy - s*0.88),   # forehead
        (cx + f*s*0.48, cy - s*0.55),   # brow ridge
        (cx + f*s*0.70, cy - s*0.12),   # nose tip
        (cx + f*s*0.60, cy + s*0.22),   # chin
        (cx + f*s*0.38, cy + s*0.58),   # neck
        (cx - f*s*0.22, cy + s*0.65),   # back shoulder
        (cx - f*s*0.52, cy - s*0.28),   # back of head
        (cx - f*s*0.28, cy - s*0.84),   # top-back
    ]
    pts_int = [(int(x), int(y)) for x, y in pts]
    pygame.draw.polygon(surf, dark, pts_int)

    # Beard
    if params.get("beard") and r >= 10:
        bx = int(cx + f * s * 0.45)
        by = int(cy + s * 0.36)
        bw = max(2, int(s * 0.28))
        bh = max(2, int(s * 0.22))
        pygame.draw.ellipse(surf, dark, (bx - bw // 2, by, bw, bh))

    _draw_crown(surf, cx, cy, r, s, f, params.get("crown", "none"), dark, wear)


def _draw_crown(surf, cx, cy, r, s, f, crown: str, col: tuple, wear: float):
    if r < 8 or crown == "none":
        return
    top_x = int(cx + f * s * 0.05)
    top_y = int(cy - s * 0.88)
    hi = _blend(col, (255, 255, 255), 0.32)

    if crown == "laurel":
        for i in (-1, 0, 1):
            lx = top_x + int(f * i * s * 0.15)
            ly = top_y - int(s * 0.10)
            ew = max(2, int(s * 0.13))
            eh = max(2, int(s * 0.17))
            pygame.draw.ellipse(surf, hi, (lx - ew // 2, ly - eh // 2, ew, eh))

    elif crown == "radiate":
        for i in range(-2, 3):
            angle = math.pi * 0.5 + i * 0.28
            ex = top_x + int(math.cos(angle) * s * 0.38)
            ey = top_y - int(abs(math.sin(angle)) * s * 0.30) - int(s * 0.08)
            pygame.draw.line(surf, hi, (top_x, top_y), (ex, ey), 1)

    elif crown in ("crown", "mitra"):
        cw = max(4, int(s * 0.40))
        ch = max(3, int(s * 0.20))
        pygame.draw.rect(surf, hi, (top_x - cw // 2, top_y - ch, cw, ch // 2))
        for i in range(3):
            px = top_x - cw // 2 + i * (cw // 2)
            pygame.draw.polygon(surf, hi, [
                (px, top_y - ch),
                (px + cw // 6, top_y - ch - int(s * 0.15)),
                (px + cw // 3, top_y - ch),
            ])

    elif crown in ("helmet", "coif", "boar_crest"):
        hw = max(4, int(s * 0.42))
        hh = max(3, int(s * 0.24))
        pygame.draw.arc(surf, hi,
                        (top_x - hw // 2, top_y - hh, hw, hh * 2),
                        0, math.pi, max(1, r // 8))

    elif crown == "diadem":
        dw = max(4, int(s * 0.36))
        pygame.draw.line(surf, hi,
                         (top_x - dw // 2, top_y), (top_x + dw // 2, top_y), 2)
        pygame.draw.circle(surf, hi, (top_x, top_y - max(1, int(s * 0.08))), max(1, r // 8))

    elif crown == "circlet":
        cw = max(4, int(s * 0.34))
        pygame.draw.line(surf, hi,
                         (top_x - cw // 2, top_y), (top_x + cw // 2, top_y), 2)

    elif crown == "torc":
        tr = max(2, int(s * 0.18))
        pygame.draw.circle(surf, hi, (top_x, top_y), tr, max(1, tr // 2))

    elif crown in ("cap", "hat"):
        hw = max(4, int(s * 0.38))
        hh = max(3, int(s * 0.20))
        pygame.draw.polygon(surf, hi, [
            (top_x - hw // 2, top_y),
            (top_x, top_y - hh),
            (top_x + hw // 2, top_y),
        ])


def _reverse_category(motif: str) -> str:
    m = motif.lower()
    if "eagle"      in m: return "eagle"
    if "lion"       in m: return "lion"
    if "bull"       in m: return "bull"
    if "horse"      in m: return "horse"
    if "dolphin"    in m or "fish"   in m: return "fish"
    if "griffin"    in m: return "griffin"
    if "phoenix"    in m or "flame"  in m: return "phoenix"
    if "serpent"    in m or "snake"  in m: return "serpent"
    if "owl"        in m: return "owl"
    if "temple"     in m or "column" in m: return "temple"
    if "tower"      in m or "castle" in m: return "castle"
    if "arch"       in m: return "arch"
    if "galley"     in m or "ship"   in m or "prow" in m: return "ship"
    if "chariot"    in m: return "chariot"
    if "wreath"     in m or "laurel" in m: return "wreath"
    if "wheat"      in m or "sheaf"  in m: return "wheat"
    if "palm"       in m: return "palm"
    if "crescent"   in m or "star"   in m: return "crescent"
    if "trident"    in m: return "trident"
    if "sword"      in m or "axe"    in m: return "weapon"
    if "scale"      in m: return "scales"
    if "thunder"    in m or "bolt"   in m: return "bolt"
    if "rose"       in m or "fleur"  in m: return "flower"
    if "cornucopia" in m: return "cornucopia"
    if "hammer"     in m or "anvil"  in m: return "hammer"
    return "generic"


def _draw_reverse_motif(surf, cx, cy, r, category: str, col: tuple, sh: tuple):
    """Draw a symbolic motif on the reverse face. col=main, sh=shadow."""
    if r < 7:
        return
    s  = r * 0.58
    hi = _blend(col, (255, 255, 255), 0.25)
    lw = max(1, r // 10)

    if category == "eagle":
        # Spread wings + head
        pygame.draw.line(surf, col, (int(cx - s), cy), (int(cx + s), cy), max(1, int(s * 0.15)))
        pygame.draw.circle(surf, col, (cx, int(cy - s * 0.15)), max(2, int(s * 0.22)))
        pygame.draw.arc(surf, col,
                        (int(cx - s * 0.9), int(cy - s * 0.4), int(s), int(s * 0.7)),
                        math.pi, math.pi * 1.5, lw)
        pygame.draw.arc(surf, col,
                        (int(cx), int(cy - s * 0.4), int(s * 0.9), int(s * 0.7)),
                        math.pi * 1.5, math.pi * 2, lw)

    elif category == "lion":
        body = [
            (int(cx + s*0.15), int(cy - s*0.55)),
            (int(cx + s*0.50), int(cy - s*0.30)),
            (int(cx + s*0.45), int(cy + s*0.25)),
            (int(cx - s*0.05), int(cy + s*0.60)),
            (int(cx - s*0.35), int(cy + s*0.35)),
            (int(cx - s*0.30), int(cy - s*0.25)),
        ]
        pygame.draw.polygon(surf, col, body)
        pygame.draw.circle(surf, col, (int(cx + s*0.22), int(cy - s*0.62)), max(2, int(s*0.30)))

    elif category == "bull":
        pygame.draw.ellipse(surf, col, (int(cx - s*0.6), int(cy - s*0.35), int(s*1.1), int(s*0.65)))
        pygame.draw.circle(surf, col, (int(cx + s*0.60), int(cy - s*0.18)), max(2, int(s*0.28)))
        pygame.draw.arc(surf, col,
                        (int(cx + s*0.28), int(cy - s*0.65), int(s*0.45), int(s*0.40)),
                        math.pi, 0, lw)

    elif category == "horse":
        pts = [
            (int(cx - s*0.15), int(cy + s*0.60)),
            (int(cx - s*0.30), int(cy)),
            (int(cx - s*0.10), int(cy - s*0.55)),
            (int(cx + s*0.25), int(cy - s*0.70)),
            (int(cx + s*0.40), int(cy - s*0.40)),
            (int(cx + s*0.20), int(cy + s*0.10)),
            (int(cx + s*0.30), int(cy + s*0.60)),
        ]
        pygame.draw.polygon(surf, col, pts)

    elif category == "fish":
        pygame.draw.ellipse(surf, col,
                            (int(cx - s*0.55), int(cy - s*0.25), int(s*0.90), int(s*0.50)))
        pygame.draw.polygon(surf, col, [
            (int(cx + s*0.35), cy),
            (int(cx + s*0.75), int(cy - s*0.30)),
            (int(cx + s*0.75), int(cy + s*0.30)),
        ])

    elif category == "griffin":
        pygame.draw.line(surf, col,
                         (int(cx - s*0.8), int(cy - s*0.1)),
                         (int(cx + s*0.8), int(cy - s*0.1)), max(1, int(s*0.12)))
        pygame.draw.circle(surf, col, (cx, int(cy - s*0.25)), max(2, int(s*0.25)))
        pygame.draw.ellipse(surf, col,
                            (int(cx - s*0.3), int(cy + s*0.1), int(s*0.6), int(s*0.5)))

    elif category == "phoenix":
        for i in range(-2, 3):
            fx = cx + int(i * s * 0.18)
            fy = int(cy + s * 0.55)
            pygame.draw.line(surf, col, (fx, fy),
                             (cx + int(i * s * 0.08), int(cy - s * 0.65)), max(1, r // 12))
        pygame.draw.circle(surf, hi, (cx, int(cy - s * 0.58)), max(2, int(s * 0.20)))

    elif category == "serpent":
        prev = None
        for i in range(12):
            t = i / 11.0
            x = int(cx - s * 0.7 + t * s * 1.4)
            y = int(cy + math.sin(t * math.pi * 2.5) * s * 0.32)
            if prev:
                pygame.draw.line(surf, col, prev, (x, y), lw)
            prev = (x, y)
        pygame.draw.circle(surf, col, (int(cx + s * 0.72), cy), max(2, int(s * 0.18)))

    elif category == "owl":
        pygame.draw.circle(surf, col, (cx, int(cy - s * 0.18)), max(3, int(s * 0.38)))
        pygame.draw.ellipse(surf, col,
                            (int(cx - s*0.25), int(cy + s*0.22), int(s*0.50), int(s*0.40)))
        if r >= 10:
            pygame.draw.circle(surf, hi, (int(cx - s*0.12), int(cy - s*0.22)), max(1, int(s*0.10)))
            pygame.draw.circle(surf, hi, (int(cx + s*0.12), int(cy - s*0.22)), max(1, int(s*0.10)))

    elif category == "temple":
        tw = int(s * 1.1)
        tx = cx - tw // 2
        ty = int(cy - s * 0.1)
        pygame.draw.polygon(surf, col, [(tx, ty), (cx, ty - int(s*0.42)), (tx + tw, ty)])
        pygame.draw.rect(surf, col, (tx, ty, tw, max(2, int(s * 0.12))))
        n_cols = max(3, min(5, r // 6))
        for i in range(n_cols):
            colx = tx + int(tw * (i + 0.5) / n_cols)
            pygame.draw.line(surf, col, (colx, ty), (colx, int(cy + s * 0.45)), lw)

    elif category == "castle":
        cw = int(s * 0.80)
        ch = int(s * 0.65)
        tx = cx - cw // 2
        ty = int(cy - ch * 0.35)
        pygame.draw.rect(surf, col, (tx, ty, cw, ch))
        n = max(3, cw // 5)
        mw = max(2, cw // n)
        for i in range(0, n, 2):
            pygame.draw.rect(surf, col, (tx + i * mw, ty - int(s * 0.18), mw, int(s * 0.18)))
        gw = max(4, cw // 3)
        pygame.draw.rect(surf, sh, (cx - gw // 2, int(cy + s * 0.10), gw, int(s * 0.28)))

    elif category == "arch":
        aw = int(s * 0.90)
        ah = int(s * 0.75)
        tx = cx - aw // 2
        ty = int(cy - ah * 0.30)
        pygame.draw.rect(surf, col, (tx, ty + ah // 2, max(3, aw // 5), ah // 2))
        pygame.draw.rect(surf, col, (tx + aw - max(3, aw // 5), ty + ah // 2, max(3, aw // 5), ah // 2))
        pygame.draw.arc(surf, col, (tx, ty, aw, ah), 0, math.pi, lw * 2)

    elif category == "ship":
        pygame.draw.ellipse(surf, col,
                            (int(cx - s*0.75), int(cy), int(s*1.5), int(s*0.40)))
        mast_top = int(cy - s * 0.65)
        pygame.draw.line(surf, col, (cx, mast_top), (cx, int(cy)), lw)
        pygame.draw.polygon(surf, col, [
            (cx, mast_top),
            (int(cx + s * 0.45), int(cy - s * 0.12)),
            (cx, int(cy - s * 0.12)),
        ])

    elif category == "chariot":
        wr = max(3, int(s * 0.30))
        wx = int(cx + s * 0.35)
        wy = int(cy + s * 0.28)
        pygame.draw.circle(surf, col, (wx, wy), wr, lw)
        pygame.draw.line(surf, col, (wx, wy), (int(cx - s * 0.65), wy), lw)
        pygame.draw.ellipse(surf, col,
                            (int(cx - s*0.80), int(cy - s*0.30), int(s*0.55), int(s*0.45)))
        pygame.draw.circle(surf, col, (int(cx - s*0.60), int(cy - s*0.50)), max(2, int(s*0.18)))

    elif category == "wreath":
        wr = max(3, int(s * 0.68))
        pygame.draw.circle(surf, col, (cx, cy), wr, lw)
        n_leaves = max(8, r * 2)
        for i in range(n_leaves):
            a = math.pi * 2 * i / n_leaves
            lx = cx + int(math.cos(a) * wr)
            ly = cy + int(math.sin(a) * wr)
            pygame.draw.circle(surf, col, (lx, ly), max(1, r // 10))

    elif category == "wheat":
        pygame.draw.line(surf, col, (cx, int(cy + s*0.65)), (cx, int(cy - s*0.65)), lw)
        n_grains = max(4, r // 4)
        for i in range(n_grains):
            gy = int(cy - s * 0.55 + i * s * 1.1 / max(1, n_grains - 1))
            for side in (-1, 1):
                gx = cx + side * max(2, int(s * 0.28))
                pygame.draw.ellipse(surf, col, (gx - 2, gy - 3, 4, 6))

    elif category == "palm":
        pygame.draw.line(surf, col, (cx, int(cy + s*0.65)), (cx, int(cy - s*0.20)), lw)
        for i in range(-2, 3):
            a = math.pi * 0.5 + i * 0.45
            fl = s * 0.55
            ex = cx + int(math.cos(a) * fl)
            ey = int(cy - s * 0.20) - int(abs(math.sin(a)) * fl)
            pygame.draw.line(surf, col, (cx, int(cy - s * 0.20)), (ex, ey), lw)

    elif category == "crescent":
        moon_r = max(3, int(s * 0.45))
        pygame.draw.circle(surf, col, (cx, cy), moon_r)
        pygame.draw.circle(surf, sh, (int(cx + s*0.28), int(cy - s*0.10)), max(2, int(s*0.35)))
        if r >= 10:
            pygame.draw.circle(surf, col, (int(cx + s*0.52), int(cy - s*0.52)),
                                max(1, int(s * 0.14)))

    elif category == "trident":
        pygame.draw.line(surf, col, (cx, int(cy - s*0.75)), (cx, int(cy + s*0.75)), lw)
        tip_y = int(cy - s * 0.75)
        ph = max(4, int(s * 0.30))
        for dx_f in (-0.28, 0.0, 0.28):
            px = cx + int(s * dx_f)
            pygame.draw.line(surf, col, (px, tip_y), (px, tip_y + ph), lw)

    elif category == "weapon":
        pygame.draw.line(surf, col,
                         (int(cx - s*0.55), int(cy - s*0.55)),
                         (int(cx + s*0.55), int(cy + s*0.55)), lw)
        pygame.draw.line(surf, col,
                         (int(cx + s*0.55), int(cy - s*0.55)),
                         (int(cx - s*0.55), int(cy + s*0.55)), lw)

    elif category == "scales":
        pygame.draw.line(surf, col, (cx, int(cy - s*0.55)), (cx, int(cy + s*0.55)), lw)
        arm_y = int(cy - s * 0.28)
        aw = int(s * 0.65)
        pygame.draw.line(surf, col, (cx - aw, arm_y), (cx + aw, arm_y), lw)
        for side in (-1, 1):
            px = cx + side * aw
            pygame.draw.arc(surf, col,
                            (px - int(s*0.28), arm_y, int(s*0.56), int(s*0.35)),
                            0, math.pi, lw)

    elif category == "bolt":
        pts = [
            (int(cx + s*0.15), int(cy - s*0.72)),
            (int(cx - s*0.12), int(cy - s*0.10)),
            (int(cx + s*0.22), int(cy - s*0.05)),
            (int(cx - s*0.15), int(cy + s*0.72)),
        ]
        for i in range(len(pts) - 1):
            pygame.draw.line(surf, col, pts[i], pts[i + 1], lw)

    elif category == "flower":
        for i in range(5):
            a = math.pi * 2 * i / 5 - math.pi / 2
            px = cx + int(math.cos(a) * s * 0.42)
            py = cy + int(math.sin(a) * s * 0.42)
            pygame.draw.circle(surf, col, (px, py), max(2, int(s * 0.25)))
        pygame.draw.circle(surf, hi, (cx, cy), max(2, int(s * 0.20)))

    elif category == "cornucopia":
        pts = [
            (int(cx - s*0.60), int(cy - s*0.20)),
            (int(cx - s*0.10), int(cy - s*0.55)),
            (int(cx + s*0.50), int(cy - s*0.45)),
            (int(cx + s*0.65), int(cy + s*0.05)),
            (int(cx + s*0.40), int(cy + s*0.30)),
            (int(cx - s*0.10), int(cy + s*0.30)),
        ]
        pygame.draw.polygon(surf, col, pts)
        for i in range(3):
            pygame.draw.circle(surf, hi,
                               (int(cx - s*0.55 + i * int(s*0.20)), int(cy - s*0.40)),
                               max(1, int(s * 0.10)))

    elif category == "hammer":
        pygame.draw.rect(surf, col, (int(cx - s*0.12), int(cy - s*0.75), int(s*0.24), int(s*0.65)))
        pygame.draw.rect(surf, col, (int(cx - s*0.35), int(cy - s*0.75), int(s*0.70), int(s*0.24)))
        pygame.draw.rect(surf, col, (int(cx - s*0.42), int(cy + s*0.10), int(s*0.84), int(s*0.24)))
        pygame.draw.rect(surf, col, (int(cx - s*0.28), int(cy + s*0.34), int(s*0.56), int(s*0.28)))

    else:  # generic / monogram
        pygame.draw.line(surf, col,
                         (int(cx - s*0.45), int(cy - s*0.45)),
                         (int(cx + s*0.45), int(cy + s*0.45)), lw)
        pygame.draw.line(surf, col,
                         (int(cx + s*0.45), int(cy - s*0.45)),
                         (int(cx - s*0.45), int(cy + s*0.45)), lw)
        pygame.draw.circle(surf, col, (cx, cy), max(2, int(s * 0.22)))


def _draw_rim(surf, cx, cy, r, style: str, col: tuple):
    if r < 6:
        return
    if style == "beaded":
        n  = max(8, r * 2)
        br = max(1, r // 10)
        for i in range(n):
            a  = math.pi * 2 * i / n
            bx = cx + int((r - br - 1) * math.cos(a))
            by = cy + int((r - br - 1) * math.sin(a))
            pygame.draw.circle(surf, col, (bx, by), br)
    elif style == "serrated":
        n = max(14, r * 3)
        for i in range(n):
            a  = math.pi * 2 * i / n
            x1 = cx + int((r - 2) * math.cos(a))
            y1 = cy + int((r - 2) * math.sin(a))
            x2 = cx + int(r * math.cos(a))
            y2 = cy + int(r * math.sin(a))
            pygame.draw.line(surf, col, (x1, y1), (x2, y2), 1)


# ---------------------------------------------------------------------------
# Coin surface renderers
# ---------------------------------------------------------------------------

def _render_coin(coin, r: int) -> pygame.Surface:
    """Render coin obverse (portrait face) as a cached Surface."""
    key = (coin.uid, r, "o")
    if key in _SURF_CACHE:
        return _SURF_CACHE[key]

    size = r * 2 + 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = r + 1

    metal             = coin_metal(coin.denomination_key)
    base, hi, sh, pat = METAL_COLORS.get(metal, METAL_COLORS["silver"])

    cond_idx = CONDITIONS.index(coin.condition)
    wear     = 1.0 - cond_idx / (len(CONDITIONS) - 1)   # 1=poor, 0=mint

    face = _blend(base, pat, wear * 0.45)
    pygame.draw.circle(surf, face, (cx, cy), r)

    if r >= 6 and wear < 0.75:
        hl = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(hl, (*hi, int(55 * (1.0 - wear))),
                           (cx - r // 5, cy - r // 5), int(r * 0.72))
        surf.blit(hl, (0, 0))

    params = coin_portrait_params(coin)
    _draw_portrait(surf, cx, cy, r, params, sh, wear)

    # Condition wear -- scratches across the field
    if wear > 0.30 and r >= 8:
        rng = random.Random(coin.seed ^ 0x5CA700CC)
        for _ in range(max(1, int(wear * 5))):
            a1 = rng.uniform(0, math.pi * 2)
            d1 = rng.uniform(0.1, 0.80) * (r - 2)
            a2 = a1 + rng.uniform(-0.7, 0.7)
            d2 = rng.uniform(0.1, 0.80) * (r - 2)
            x1 = cx + int(math.cos(a1) * d1)
            y1 = cy + int(math.sin(a1) * d1)
            x2 = cx + int(math.cos(a2) * d2)
            y2 = cy + int(math.sin(a2) * d2)
            pygame.draw.line(surf, _blend(sh, (0, 0, 0), 0.4), (x1, y1), (x2, y2), 1)

    # Error coin visual effects
    err = getattr(coin, "error_type", "")
    if err and r >= 8:
        _draw_error_effect(surf, cx, cy, r, err, coin, sh, base, wear)

    pygame.draw.circle(surf, sh, (cx, cy), max(2, r - 2), 1)

    rng2 = random.Random(coin.seed ^ 0xA1BC01BB)
    _draw_rim(surf, cx, cy, r, rng2.choice(["beaded", "plain", "plain", "serrated"]), sh)

    # Error coins get a distinctive red rim marker
    rim_col = RARITY_COLORS.get(coin.rarity, sh)
    if err:
        rim_col = (220, 80, 60)
    pygame.draw.circle(surf, rim_col, (cx, cy), r, 2)

    _SURF_CACHE[key] = surf
    return surf


def _draw_error_effect(surf, cx, cy, r, error_type: str, coin, sh, base, wear):
    """Overlay the error visual on the coin obverse surface."""
    if error_type == "double_strike":
        # Ghost portrait shifted slightly
        params = coin_portrait_params(coin)
        off = max(2, r // 6)
        ghost = _blend(sh, base, 0.55)
        _draw_portrait(surf, cx + off, cy + off, r, params, ghost, min(wear + 0.3, 1.0))

    elif error_type == "off_center":
        # Dark wedge covering one side
        wedge = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.polygon(wedge, (*sh, 160), [
            (cx + 1, cy + 1),
            (cx + r + 1, cy - r // 2 + 1),
            (cx + r + 1, cy + r + 1),
        ])
        surf.blit(wedge, (0, 0))

    elif error_type == "clipped_planchet":
        # Black bite taken out of the top-right edge
        clip_s = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        clip_r = max(r // 3, 4)
        pygame.draw.circle(clip_s, (0, 0, 0, 255),
                           (cx + r - clip_r // 2, cy - r + clip_r // 2), clip_r)
        surf.blit(clip_s, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    elif error_type == "die_crack":
        rng_e = random.Random(coin.seed ^ 0xD1ECCCC)
        # 1-2 jagged lines across the face
        for _ in range(rng_e.randint(1, 2)):
            a   = rng_e.uniform(0, math.pi)
            pts = []
            n   = max(4, r // 3)
            for i in range(n):
                t  = i / (n - 1)
                bx = int(cx + math.cos(a) * (t - 0.5) * r * 1.8)
                by = int(cy + math.sin(a) * (t - 0.5) * r * 1.8)
                bx += rng_e.randint(-max(1, r // 8), max(1, r // 8))
                by += rng_e.randint(-max(1, r // 8), max(1, r // 8))
                pts.append((bx, by))
            hi = _blend(sh, (255, 255, 255), 0.5)
            for i in range(len(pts) - 1):
                pygame.draw.line(surf, hi, pts[i], pts[i + 1], max(1, r // 12))

    elif error_type == "wrong_metal":
        # Splotchy patches of a contrasting metal color
        metals  = list(METAL_COLORS.keys())
        my_metal = coin_metal(coin.denomination_key)
        alts    = [m for m in metals if m != my_metal]
        alt_col = METAL_COLORS[random.Random(coin.seed).choice(alts)][0]
        rng_e   = random.Random(coin.seed ^ 0xBADC01AB)
        for _ in range(3):
            px = cx + rng_e.randint(-r // 2, r // 2)
            py = cy + rng_e.randint(-r // 2, r // 2)
            pr = max(2, rng_e.randint(r // 5, r // 3))
            spl = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(spl, (*alt_col, 140), (px, py), pr)
            surf.blit(spl, (0, 0))

    elif error_type == "brockage":
        # Mirror-image incuse impression of the portrait, darker
        params = coin_portrait_params(coin)
        params_mirror = dict(params)
        params_mirror["facing_right"] = not params["facing_right"]
        ghost = _blend(sh, (0, 0, 0), 0.5)
        ghost_s = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        _draw_portrait(ghost_s, cx, cy, r, params_mirror, ghost, 0.6)
        surf.blit(ghost_s, (0, 0))


def _render_coin_reverse(coin, r: int) -> pygame.Surface:
    """Render coin reverse (motif face) as a cached Surface."""
    key = (coin.uid, r, "r")
    if key in _SURF_CACHE:
        return _SURF_CACHE[key]

    size = r * 2 + 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = r + 1

    metal             = coin_metal(coin.denomination_key)
    base, hi, sh, pat = METAL_COLORS.get(metal, METAL_COLORS["silver"])

    cond_idx = CONDITIONS.index(coin.condition)
    wear     = 1.0 - cond_idx / (len(CONDITIONS) - 1)

    face = _blend(base, pat, wear * 0.45)
    pygame.draw.circle(surf, face, (cx, cy), r)

    if r >= 6 and wear < 0.75:
        hl = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(hl, (*hi, int(55 * (1.0 - wear))),
                           (cx + r // 5, cy - r // 5), int(r * 0.72))
        surf.blit(hl, (0, 0))

    cat = _reverse_category(coin.reverse_motif)
    _draw_reverse_motif(surf, cx, cy, r, cat, sh, base)

    if wear > 0.30 and r >= 8:
        rng = random.Random(coin.seed ^ 0x5CA7AA11)
        for _ in range(max(1, int(wear * 4))):
            a1 = rng.uniform(0, math.pi * 2)
            d1 = rng.uniform(0.1, 0.80) * (r - 2)
            a2 = a1 + rng.uniform(-0.6, 0.6)
            d2 = rng.uniform(0.1, 0.80) * (r - 2)
            x1 = cx + int(math.cos(a1) * d1)
            y1 = cy + int(math.sin(a1) * d1)
            x2 = cx + int(math.cos(a2) * d2)
            y2 = cy + int(math.sin(a2) * d2)
            pygame.draw.line(surf, _blend(sh, (0, 0, 0), 0.4), (x1, y1), (x2, y2), 1)

    pygame.draw.circle(surf, sh, (cx, cy), max(2, r - 2), 1)
    rng2 = random.Random(coin.seed ^ 0xA1BC01BB)
    _draw_rim(surf, cx, cy, r, rng2.choice(["beaded", "plain", "plain", "serrated"]), sh)
    pygame.draw.circle(surf, RARITY_COLORS.get(coin.rarity, sh), (cx, cy), r, 2)

    _SURF_CACHE[key] = surf
    return surf


def _draw_coin_icon(surf, cx, cy, r, coin_or_rarity):
    """Blit a coin icon. Pass a Coin object for full art, or a rarity str for fallback."""
    from coins import Coin as _Coin
    if isinstance(coin_or_rarity, _Coin):
        s = _render_coin(coin_or_rarity, r)
        surf.blit(s, (cx - r - 1, cy - r - 1))
    else:
        rarity = coin_or_rarity
        brd  = RARITY_COLORS.get(rarity, _DIM)
        fill = RARITY_BG.get(rarity, _CELL)
        col  = (min(255, fill[0] + 20), min(255, fill[1] + 20), min(255, fill[2] + 20))
        pygame.draw.circle(surf, col, (cx, cy), r)
        pygame.draw.circle(surf, brd, (cx, cy), r, 2)
        pygame.draw.circle(surf, brd, (cx, cy), max(1, r - 4), 1)


# ---------------------------------------------------------------------------
# CoinsMixin -- codex panels
# ---------------------------------------------------------------------------

class CoinsMixin:

    def _draw_coin_codex(self, player, gy0=58, gx_off=130):
        gen  = getattr(player, "_coin_gen", None)
        if gen is None:
            return
        disc      = getattr(player, "discovered_coin_types", set())
        coins     = getattr(player, "coins", [])
        completed = getattr(player, "completed_coin_sets", set())

        total = len(gen.coin_types)
        sub   = self.small.render(
            f"Discovered: {len(disc)} / {total}  |  "
            f"{len(coins)} coin{'s' if len(coins) != 1 else ''} in collection",
            True, _LABEL)
        self.screen.blit(sub, (gx_off + 8, gy0))

        gy0 += 22
        avail_w  = SCREEN_W - gx_off - 4
        panel_w  = min(480, avail_w - 220)
        civs     = gen.civilizations
        row_h, gap = 34, 3
        list_w   = panel_w
        visible_h = SCREEN_H - gy0 - 4

        if not hasattr(self, "_coin_codex_scroll"):
            self._coin_codex_scroll   = 0
            self._coin_codex_selected = None
            self._coin_civ_rects      = {}
            self._coin_denom_rects    = {}

        max_scroll = max(0, len(civs) * (row_h + gap) - visible_h)
        self._coin_codex_scroll = min(self._coin_codex_scroll, max_scroll)

        clip = pygame.Rect(gx_off, gy0, list_w, visible_h)
        self.screen.set_clip(clip)
        self._coin_civ_rects.clear()

        for ci, civ in enumerate(civs):
            ry = gy0 + ci * (row_h + gap) - self._coin_codex_scroll
            if ry + row_h <= gy0 or ry >= gy0 + visible_h:
                continue

            civ_type_ids = [t for t in gen.coin_types
                            if gen.coin_types[t]["civilization_name"] == civ["name"]]
            found_types  = [t for t in civ_type_ids if t in disc]
            progress     = len(found_types)
            total_denoms = len(civ_type_ids)

            is_sel     = (self._coin_codex_selected == civ["name"])
            is_complete = civ["name"] in completed
            bg     = (50, 45, 25) if is_sel else (_CELL if not is_complete else (40, 35, 12))
            brd    = _GOLD if (is_sel or is_complete) else (_LABEL if progress > 0 else _DIM)

            rrect = pygame.Rect(gx_off + 2, ry, list_w - 6, row_h)
            self._coin_civ_rects[civ["name"]] = rrect.clip(clip)
            pygame.draw.rect(self.screen, bg, rrect)
            pygame.draw.rect(self.screen, brd, rrect, 2)

            # Representative coin icon -- best specimen from collection, or rarity fallback
            best_civ = None
            if progress > 0:
                candidates = [c for c in coins if c.coin_type_id in found_types]
                if candidates:
                    best_civ = max(candidates,
                                   key=lambda c: RARITY_ORDER.index(c.rarity) * 10 +
                                   ["poor","fair","good","fine","very_fine","mint"].index(c.condition))
            _draw_coin_icon(self.screen, rrect.x + 14, rrect.y + row_h // 2, 10,
                            best_civ if best_civ else ("rare" if progress > 0 else "uncommon"))

            name_col = _GOLD if is_complete else (_TITLE if progress > 0 else _DIM)
            ns = self.small.render(civ["name"], True, name_col)
            self.screen.blit(ns, (rrect.x + 30, rrect.y + 4))
            if is_complete:
                star_s = self.small.render(" ★", True, _GOLD)
                self.screen.blit(star_s, (rrect.x + 30 + ns.get_width(), rrect.y + 4))
            es = self.small.render(civ["era_label"], True, _LABEL if progress > 0 else _DIM)
            self.screen.blit(es, (rrect.x + 30, rrect.y + 18))

            bar_x = rrect.x + list_w - 80
            bar_w, bar_h = 68, 6
            bar_y = rrect.y + row_h // 2 - 3
            pygame.draw.rect(self.screen, (40, 35, 20), (bar_x, bar_y, bar_w, bar_h))
            if progress > 0:
                fill_w = int(bar_w * progress / max(1, total_denoms))
                pygame.draw.rect(self.screen, _GOLD, (bar_x, bar_y, fill_w, bar_h))
            pygame.draw.rect(self.screen, _DIM, (bar_x, bar_y, bar_w, bar_h), 1)
            cnt_s = self.small.render(f"{progress}/{total_denoms}", True, _LABEL)
            self.screen.blit(cnt_s, (bar_x, bar_y + 9))

        self.screen.set_clip(None)

        # ── Right panel ───────────────────────────────────────────────────
        sel_name = self._coin_codex_selected
        if sel_name is None:
            hint = self.small.render("<- Select a civilization", True, _DIM)
            self.screen.blit(hint, (gx_off + list_w + 20,
                                    gy0 + visible_h // 2 - hint.get_height() // 2))
            return

        sel_civ = next((c for c in civs if c["name"] == sel_name), None)
        if sel_civ is None:
            return

        rx0 = gx_off + list_w + 14
        ry0 = gy0
        rw  = SCREEN_W - rx0 - 4

        # ── Civ header ────────────────────────────────────────────────────
        hdr = self.font.render(sel_name, True, _GOLD)
        self.screen.blit(hdr, (rx0, ry0))
        ery = ry0 + hdr.get_height() + 2
        era_s = self.small.render(
            f"{sel_civ['era_label']}  •  {sel_civ['currency_system'].title()} currency"
            f"  •  Mint: {sel_civ['mint_city']}",
            True, _LABEL)
        self.screen.blit(era_s, (rx0, ery))
        content_y = ery + era_s.get_height() + 6

        # ── Split right panel into denomination list | detail ─────────────
        DENOM_LIST_W = 210
        DETAIL_X     = rx0 + DENOM_LIST_W + 10
        DETAIL_W     = SCREEN_W - DETAIL_X - 6

        civ_type_ids = [t for t in gen.coin_types
                        if gen.coin_types[t]["civilization_name"] == sel_name]
        row_h_d, row_gap_d = 52, 4
        list_clip = pygame.Rect(rx0, content_y, DENOM_LIST_W, SCREEN_H - content_y - 4)
        self.screen.set_clip(list_clip)
        self._coin_denom_rects.clear()

        if not hasattr(self, "_coin_denom_scroll"):
            self._coin_denom_scroll = 0
        max_denom_scroll = max(0, len(civ_type_ids) * (row_h_d + row_gap_d) - list_clip.height)
        self._coin_denom_scroll = min(self._coin_denom_scroll, max_denom_scroll)

        for di, tid in enumerate(civ_type_ids):
            td    = gen.coin_types[tid]
            found = tid in disc
            best  = None
            n_owned = 0
            if found:
                candidates = [c for c in coins if c.coin_type_id == tid]
                n_owned = len(candidates)
                if candidates:
                    best = max(candidates,
                               key=lambda c: RARITY_ORDER.index(c.rarity) * 10 +
                               ["poor","fair","good","fine","very_fine","mint"].index(c.condition))

            dy = content_y + di * (row_h_d + row_gap_d) - self._coin_denom_scroll
            drect = pygame.Rect(rx0, dy, DENOM_LIST_W, row_h_d)
            self._coin_denom_rects[tid] = drect.clip(list_clip)

            is_sel_d = (getattr(self, "_coin_denom_selected", None) == tid)
            bg  = RARITY_BG.get(best.rarity, _CELL) if best else (22, 18, 10)
            if is_sel_d:
                bg = tuple(min(255, v + 28) for v in bg)
            brd = RARITY_COLORS.get(best.rarity, _DIM) if best else _DIM
            if is_sel_d:
                brd = _GOLD
            pygame.draw.rect(self.screen, bg, drect)
            pygame.draw.rect(self.screen, brd, drect, 2 if is_sel_d else 1)

            # Coin icon
            icon_cx = rx0 + 22
            icon_cy = dy + row_h_d // 2
            if found and best:
                icon_s = _render_coin(best, 16)
                self.screen.blit(icon_s, (icon_cx - 16, icon_cy - 16))
            else:
                _draw_coin_icon(self.screen, icon_cx, icon_cy, 14,
                                "uncommon" if found else "common")
                if not found:
                    q = self.font.render("?", True, _DIM)
                    self.screen.blit(q, (icon_cx - q.get_width() // 2,
                                        icon_cy - q.get_height() // 2))

            tx = rx0 + 46
            metal = td.get("metal", "silver")
            denom_name = td["denomination_key"].replace("_", " ").title()
            dn_col = brd if found else _DIM
            dn_s = self.small.render(denom_name, True, dn_col)
            self.screen.blit(dn_s, (tx, dy + 6))

            metal_col = {"copper": (195, 110, 60), "bronze": (175, 130, 70),
                         "billon": (160, 155, 120), "silver": (200, 200, 215),
                         "electrum": (215, 200, 110), "gold": (230, 195, 60)}.get(metal, _LABEL)
            met_s = self.small.render(metal.title(), True, metal_col)
            self.screen.blit(met_s, (tx, dy + 20))

            if found:
                cond_short = CONDITION_SHORT.get(best.condition, "?")
                info_s = self.small.render(
                    f"{best.rarity.title()}  {cond_short}  x{n_owned}", True, _LABEL)
                self.screen.blit(info_s, (tx, dy + 34))
                if getattr(best, "error_type", ""):
                    err_dot = self.small.render("ERR", True, (220, 80, 60))
                    self.screen.blit(err_dot, (rx0 + DENOM_LIST_W - err_dot.get_width() - 4,
                                               dy + 6))
            else:
                unk_s = self.small.render("Undiscovered", True, _DIM)
                self.screen.blit(unk_s, (tx, dy + 34))

        self.screen.set_clip(None)

        # ── Detail panel (right column) ───────────────────────────────────
        sel_tid = getattr(self, "_coin_denom_selected", None)

        if not sel_tid or sel_tid not in disc:
            if civ_type_ids:
                hint2 = self.small.render("<- Select a denomination", True, _DIM)
                self.screen.blit(hint2, (DETAIL_X,
                                         content_y + (SCREEN_H - content_y) // 2))
            return

        td = gen.coin_types.get(sel_tid)
        if not td:
            return
        candidates = [c for c in coins if c.coin_type_id == sel_tid]
        if not candidates:
            return

        best = max(candidates,
                   key=lambda c: RARITY_ORDER.index(c.rarity) * 10 +
                   ["poor","fair","good","fine","very_fine","mint"].index(c.condition))
        dp_col = RARITY_COLORS.get(best.rarity, _LABEL)
        dp_bg  = RARITY_BG.get(best.rarity, _CELL)

        # Background card
        dp_rect = pygame.Rect(DETAIL_X, content_y, DETAIL_W, SCREEN_H - content_y - 6)
        pygame.draw.rect(self.screen, dp_bg, dp_rect)
        pygame.draw.rect(self.screen, dp_col, dp_rect, 2)

        # Large coin renders
        obv_r = 44
        obv_s = _render_coin(best, obv_r)
        rev_s = _render_coin_reverse(best, obv_r)
        coin_y = content_y + obv_r + 12
        obv_x  = DETAIL_X + 14
        rev_x  = obv_x + obv_r * 2 + 12
        self.screen.blit(obv_s, (obv_x, coin_y - obv_r))
        self.screen.blit(rev_s, (rev_x, coin_y - obv_r))

        obv_lbl = self.small.render("Obverse", True, _DIM)
        rev_lbl = self.small.render("Reverse", True, _DIM)
        self.screen.blit(obv_lbl, (obv_x + obv_r - obv_lbl.get_width() // 2,
                                   coin_y + obv_r + 2))
        self.screen.blit(rev_lbl, (rev_x + obv_r - rev_lbl.get_width() // 2,
                                   coin_y + obv_r + 2))

        # Text info column (to the right of coins)
        ix  = rev_x + obv_r * 2 + 14
        iy  = content_y + 8
        i_w = DETAIL_X + DETAIL_W - ix - 8

        def dline(txt, col=_LABEL, bold=False):
            nonlocal iy
            fnt = self.font if bold else self.small
            s = fnt.render(txt, True, col)
            self.screen.blit(s, (ix, iy))
            iy += s.get_height() + 2

        def dgap(n=6):
            nonlocal iy
            iy += n

        dline(best.denomination_label, dp_col, bold=True)
        dgap(2)
        dline(f"Civilization: {best.civilization_name}", _TITLE)
        dline(f"Era:          {best.era_label}", _LABEL)
        dline(f"Ruler:        {best.ruler_name}", _LABEL)
        dline(f"Year:         {best.year_label}", _LABEL)
        dline(f"Mint City:    {best.mint_city}", _LABEL)
        dgap()
        dline(f"Metal:        {td.get('metal','?').title()}", _LABEL)
        dline(f"Currency:     {best.currency_system.title()}", _LABEL)
        dgap()
        rar_s  = self.small.render(best.rarity.title(), True, dp_col)
        cond_s = self.small.render(
            f"  •  {CONDITION_LABELS.get(best.condition, best.condition)}", True, _LABEL)
        self.screen.blit(rar_s,  (ix, iy))
        self.screen.blit(cond_s, (ix + rar_s.get_width(), iy))
        iy += 15

        n_owned = len(candidates)
        owned_s = self.small.render(f"Owned: {n_owned} coin{'s' if n_owned != 1 else ''}",
                                    True, _GOLD)
        self.screen.blit(owned_s, (ix, iy))
        iy += 15

        # Motifs section (below coins)
        motif_y = coin_y + obv_r + 18
        mx = DETAIL_X + 10

        def mline(label, val, col=_LABEL):
            lbl_s = self.small.render(label, True, _DIM)
            val_s = self.small.render(val, True, col)
            self.screen.blit(lbl_s, (mx, motif_y + _mline_offset[0]))
            self.screen.blit(val_s, (mx + lbl_s.get_width() + 4, motif_y + _mline_offset[0]))
            _mline_offset[0] += 16

        _mline_offset = [0]
        mline("Obverse:", best.obverse_motif)
        mline("Reverse:", best.reverse_motif)

        # Error coin badge
        if getattr(best, "error_type", ""):
            _mline_offset[0] += 4
            err_info = ERROR_TYPES.get(best.error_type, {})
            err_s = self.small.render(
                f"ERROR: {err_info.get('label', best.error_type)}", True, (220, 80, 60))
            self.screen.blit(err_s, (mx, motif_y + _mline_offset[0]))
            _mline_offset[0] += 14
            desc_s = self.small.render(err_info.get("desc", ""), True, (180, 130, 110))
            self.screen.blit(desc_s, (mx, motif_y + _mline_offset[0]))
            _mline_offset[0] += 16

        # Provenance lore
        if getattr(best, "provenance", ""):
            _mline_offset[0] += 4
            prov = best.provenance
            max_w = DETAIL_W - 20
            # word-wrap provenance across up to 3 lines
            words = prov.split()
            lines, cur = [], ""
            for w in words:
                test = (cur + " " + w).strip()
                if self.small.size(test)[0] <= max_w:
                    cur = test
                else:
                    if cur:
                        lines.append(cur)
                    cur = w
            if cur:
                lines.append(cur)
            for li, ln in enumerate(lines[:3]):
                col = (160, 175, 140)
                prefix = '"' if li == 0 else "  "
                suffix = '"' if li == len(lines) - 1 else ""
                ps = self.small.render(prefix + ln + suffix, True, col)
                self.screen.blit(ps, (mx, motif_y + _mline_offset[0]))
                _mline_offset[0] += 15

    # ── Click / scroll handling ───────────────────────────────────────────

    def handle_coin_codex_click(self, pos, player):
        if not hasattr(self, "_coin_civ_rects"):
            return False
        for civ_name, rect in self._coin_civ_rects.items():
            if rect.collidepoint(pos):
                if self._coin_codex_selected == civ_name:
                    self._coin_codex_selected = None
                else:
                    self._coin_codex_selected = civ_name
                    self._coin_denom_selected = None
                    self._coin_denom_scroll   = 0
                return True
        for tid, rect in self._coin_denom_rects.items():
            if rect.collidepoint(pos):
                disc = getattr(player, "discovered_coin_types", set())
                if tid in disc:
                    self._coin_denom_selected = tid
                return True
        return False

    def handle_coin_codex_scroll(self, dy):
        if not hasattr(self, "_coin_codex_scroll"):
            self._coin_codex_scroll = 0
        if not hasattr(self, "_coin_denom_scroll"):
            self._coin_denom_scroll = 0
        mx = pygame.mouse.get_pos()[0]
        # If mouse is over the civ list area, scroll civs; otherwise scroll denom list
        from constants import SCREEN_W as _SW
        SIDEBAR_W = 130
        avail_w   = _SW - SIDEBAR_W - 4
        panel_w   = min(480, avail_w - 220)
        civ_right = SIDEBAR_W + panel_w + 14
        if mx < civ_right:
            self._coin_codex_scroll = max(0, self._coin_codex_scroll - dy * 20)
        else:
            self._coin_denom_scroll = max(0, self._coin_denom_scroll - dy * 20)
