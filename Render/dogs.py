import pygame
import math
from dogs import DOG_EYE_COLORS

WHITE = (248, 248, 248)

# Surface buffers at scale 1.0:
#   9px left/right   — tail extends left ~7px, extra for right when facing-left
#   6px top          — erect ears reach ~5px above sy
_BUF_X = 9
_BUF_Y = 6
_SURF_W = 52   # 9 + 34 (dog span) + 9
_SURF_H = 27   # 6 + 21 (body+legs height)

# ── Colour helpers ────────────────────────────────────────────────────────────

def _darker(c, amt=40):
    return tuple(max(0, v - amt) for v in c)

def _lighter(c, amt=35):
    return tuple(min(255, v + amt) for v in c)

# ── Internal right-facing draw ────────────────────────────────────────────────

def _draw_dog_right(surf, ox, oy, dog, s):
    """Draw a right-facing dog onto surf with anchor at (ox, oy)."""
    traits     = getattr(dog, "traits", {})
    coat       = traits.get("coat_color", (160, 100, 50))
    dark       = _darker(coat, 40)
    light      = _lighter(coat, 35)
    pattern    = traits.get("coat_pattern", "solid")
    w_spotting = traits.get("white_spotting", "solid")
    c_length   = traits.get("coat_length", "short")
    c_type     = traits.get("coat_type", "smooth")
    ear_type   = traits.get("ear_type", "floppy")
    tail_type  = traits.get("tail_type", "long")
    eye_col    = DOG_EYE_COLORS.get(traits.get("eye_color", "brown"), (100, 60, 20))

    def i(v): return int(v * s)
    def x(v): return ox + i(v)
    def y(v): return oy + i(v)

    body_y   = y(5)
    body_h   = i(10)
    head_y   = y(2)
    head_h   = i(9)
    muzzle_y = y(7)
    muzzle_h = i(3)

    # ── Coat length: fuzzy border ─────────────────────────────────────────
    if c_length == "long" and s >= 0.8:
        pygame.draw.rect(surf, _lighter(coat, 20),
            (x(1), body_y - i(1), i(24), body_h + i(2)), border_radius=2)

    # ── Body ─────────────────────────────────────────────────────────────
    body_rect = pygame.Rect(x(2), body_y, i(22), body_h)
    pygame.draw.rect(surf, coat, body_rect, border_radius=i(2))

    # ── Pattern overlays ─────────────────────────────────────────────────
    if pattern == "spotted":
        for dx, dy, r in [(5, 3, 3), (10, 5, 2), (15, 2, 3), (18, 6, 2)]:
            pygame.draw.circle(surf, dark, (x(2 + dx), body_y + i(dy)), i(r))
    elif pattern == "merle":
        for dx, dy, rw, rh in [(4, 2, 5, 3), (12, 4, 6, 4), (17, 1, 4, 3)]:
            pygame.draw.ellipse(surf, dark, (x(2 + dx), body_y + i(dy), i(rw), i(rh)))
    elif pattern == "brindle":
        for dx in range(4, 22, 4):
            lx = x(2 + dx)
            pygame.draw.line(surf, dark, (lx, body_y + i(1)), (lx, body_y + body_h - i(1)))
    elif pattern == "saddle":
        pygame.draw.rect(surf, dark, (x(6), body_y, i(12), body_h))
    elif pattern == "ticked":
        for dx, dy in [(3,2),(7,6),(12,3),(16,7),(19,1),(21,5)]:
            pygame.draw.rect(surf, dark, (x(2+dx), body_y+i(dy), i(1), i(1)))

    # ── White spotting overlays ───────────────────────────────────────────
    if w_spotting == "irish":
        pygame.draw.rect(surf, WHITE, (x(16), body_y + i(2), i(6), body_h - i(2)))
        for lx_w in [3, 7, 16, 20]:
            pygame.draw.rect(surf, WHITE, (x(lx_w), y(17), i(4), i(3)))
    elif w_spotting == "piebald":
        pygame.draw.rect(surf, WHITE, (x(14), body_y + i(1), i(10), body_h - i(1)))
        pygame.draw.ellipse(surf, WHITE, (x(5), body_y, i(7), i(7)))
        for lx_w in [3, 7, 16, 20]:
            pygame.draw.rect(surf, WHITE, (x(lx_w), y(13), i(4), i(7)))
    elif w_spotting == "extreme_white":
        pygame.draw.rect(surf, WHITE, body_rect, border_radius=i(2))
        pygame.draw.rect(surf, WHITE,
            pygame.Rect(x(22), head_y, i(10), head_h), border_radius=i(2))
        for lx_w in [3, 7, 16, 20]:
            pygame.draw.rect(surf, WHITE, (x(lx_w), y(10), i(4), i(10)))

    # ── Legs ─────────────────────────────────────────────────────────────
    leg_y = y(15)
    leg_h = i(5)
    leg_w = i(4)
    for lx in [3, 7, 16, 20]:
        pygame.draw.rect(surf, dark, (x(lx), leg_y, leg_w, leg_h))

    # ── Head ─────────────────────────────────────────────────────────────
    head_rect = pygame.Rect(x(22), head_y, i(10), head_h)
    pygame.draw.rect(surf, coat, head_rect, border_radius=i(2))
    if c_length == "long" and s >= 0.8:
        pygame.draw.rect(surf, _lighter(coat, 15), head_rect, 1, border_radius=i(2))

    # ── Muzzle ────────────────────────────────────────────────────────────
    pygame.draw.rect(surf, light, (x(30), muzzle_y, i(4), muzzle_h))
    pygame.draw.rect(surf, _darker(coat, 60), (x(32), muzzle_y, i(2), i(2)))

    # ── Eye ───────────────────────────────────────────────────────────────
    eye_pos = (x(29), y(4))
    pygame.draw.circle(surf, eye_col, eye_pos, max(1, i(2)))
    pygame.draw.circle(surf, (20, 15, 10), eye_pos, max(1, i(1)))

    # ── Ear ───────────────────────────────────────────────────────────────
    ear_x = x(23)
    if ear_type == "erect":
        pygame.draw.polygon(surf, dark, [
            (ear_x,        y(2)),
            (ear_x + i(4), y(-5)),
            (ear_x + i(6), y(2)),
        ])
    elif ear_type == "semi-erect":
        pygame.draw.polygon(surf, dark, [
            (ear_x,        y(2)),
            (ear_x + i(3), y(-3)),
            (ear_x + i(6), y(0)),
        ])
    else:  # floppy
        pygame.draw.rect(surf, dark, (ear_x + i(2), y(3), i(5), i(4)), border_radius=i(1))

    # ── Tail ──────────────────────────────────────────────────────────────
    tail_base = (x(1), y(6))
    if tail_type == "long":
        pygame.draw.line(surf, dark,
            tail_base, (x(1) - i(8), y(6) - i(5)), max(1, i(2)))
    elif tail_type == "curled":
        for t in range(8):
            ang = math.pi * t / 8
            tx = x(1) + int(i(5) * math.cos(ang) * -1)
            ty = y(6) - int(i(5) * math.sin(ang))
            pygame.draw.circle(surf, dark, (tx, ty), max(1, i(2)))
    elif tail_type == "short":
        pygame.draw.rect(surf, dark, (x(1) - i(4), y(6), i(5), i(3)))
    elif tail_type == "bob":
        pygame.draw.circle(surf, dark, (x(1) - i(2), y(7)), i(3))

    # ── Coat type texture ─────────────────────────────────────────────────
    if c_type == "wavy" and s >= 1.0:
        for i_row in range(0, body_h, max(1, i(3))):
            pygame.draw.line(surf, _lighter(coat, 10),
                (x(3), body_y + i_row), (x(20), body_y + i_row + i(1)))
    elif c_type == "wire" and s >= 1.0:
        for dx_w in range(2, 22, 3):
            pygame.draw.line(surf, dark, (x(2 + dx_w), body_y), (x(2 + dx_w), body_y + i(2)))

    # ── Stay indicator ────────────────────────────────────────────────────
    if getattr(dog, "stay_mode", False) and getattr(dog, "tamed", False):
        pygame.draw.circle(surf, (220, 240, 200), (x(26), y(-3)), max(1, i(2)))

    # ── Collar ────────────────────────────────────────────────────────────
    if traits.get("collar_applied", False):
        pygame.draw.rect(surf, (200, 60, 40), (x(21), y(5), i(4), i(2)))


# ── Main draw function ────────────────────────────────────────────────────────

def draw_dog(screen, sx, sy, dog, scale=1.0, facing=None):
    """Draw a side-view pixel-art dog at (sx, sy) with trait-driven appearance."""
    s        = max(0.5, scale)
    facing_d = (facing if facing is not None else getattr(dog, "facing", 1))

    bx = int(_BUF_X * s)
    by = int(_BUF_Y * s)
    sw = int(_SURF_W * s)
    sh = int(_SURF_H * s)

    surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
    _draw_dog_right(surf, bx, by, dog, s)

    if facing_d == -1:
        surf = pygame.transform.flip(surf, True, False)

    screen.blit(surf, (sx - bx, sy - by))


def draw_dog_portrait(screen, dx, dy, dog, size=120):
    """Render an enlarged dog portrait for the view panel."""
    sc = size / 28.0
    pygame.draw.rect(screen, (28, 20, 12), (dx, dy, size, size))
    pygame.draw.rect(screen, (60, 45, 25), (dx, dy, size, size), 1)
    ox = dx + int(size * 0.05)
    oy = dy + int(size * 0.25)
    draw_dog(screen, ox, oy, dog, scale=sc, facing=1)

    traits = getattr(dog, "traits", {})
    if traits.get("collar_applied", False):
        collar_rect = pygame.Rect(dx, dy + size - 8, size, 8)
        pygame.draw.rect(screen, (180, 55, 35), collar_rect)
    breed = traits.get("dog_name") or traits.get("breed", "")
    if breed:
        try:
            fnt = pygame.font.SysFont("Arial", max(8, int(size * 0.1)), bold=True)
            lbl = fnt.render(breed[:20], True, (240, 220, 180))
            screen.blit(lbl, (dx + 3, dy + 3))
        except Exception:
            pass


def draw_tame_hearts(screen, sx, sy, progress, threshold):
    """Draw taming progress as small hearts above the dog."""
    if threshold <= 0:
        return
    heart_w   = 10
    total_w   = threshold * (heart_w + 2)
    start_x   = sx - total_w // 2
    for i_h in range(threshold):
        hx     = start_x + i_h * (heart_w + 2)
        filled = i_h < progress
        col    = (220, 60, 80) if filled else (80, 40, 40)
        pts    = [(hx + 5, sy), (hx + 10, sy + 4), (hx + 5, sy + 8), (hx, sy + 4)]
        pygame.draw.polygon(screen, col, pts)
        if not filled:
            pygame.draw.polygon(screen, (120, 60, 70), pts, 1)
