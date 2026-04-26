import pygame
import math
from dogs import DOG_EYE_COLORS

WHITE = (248, 248, 248)

# Surface buffer at scale 1.0 — sized for the largest silhouette below.
_BUF_X  = 10
_BUF_Y  = 12
_SURF_W = 60
_SURF_H = 33
_FEET_Y = 20  # foot baseline, in unscaled units below anchor

# ── Per-breed silhouette: (body_len, body_h, leg_len, head_w, head_h, snout_len)
# Tweak these to change a breed's read-at-a-glance proportions. All values are
# in unscaled pixel units; the renderer multiplies by the draw scale.
BREED_SILHOUETTES = {
    "Border Collie":        (22, 10, 6,  9,  9, 4),
    "Husky":                (24, 11, 7, 10, 10, 4),
    "Greyhound":            (26,  7, 9,  8,  9, 5),
    "Bloodhound":           (24, 11, 6, 11, 11, 6),
    "German Shepherd":      (24, 10, 7, 10, 10, 5),
    "Labrador":             (22, 11, 6, 10, 10, 4),
    "Dalmatian":            (23, 10, 7,  9,  9, 5),
    "Beagle":               (19,  9, 4,  9,  9, 4),
    "Poodle":               (21,  9, 7,  9,  9, 5),
    "Bulldog":              (18, 12, 4, 12, 10, 3),
    "Malamute":             (24, 12, 7, 11, 11, 4),
    "Vizsla":               (22,  9, 7,  9,  9, 5),
    "Australian Shepherd":  (21, 10, 6,  9,  9, 4),
    "Dachshund":            (30,  7, 3,  9,  9, 5),
    "Setter":               (24, 10, 7,  9,  9, 5),
    "Akita":                (22, 11, 6, 11, 11, 4),
    "Rottweiler":           (23, 12, 6, 12, 11, 4),
    "Samoyed":              (22, 12, 6, 10, 10, 4),
    "Shiba Inu":            (19,  9, 5,  9,  9, 4),
    "Great Pyrenees":       (26, 13, 7, 12, 12, 5),
    "Weimaraner":           (23,  9, 8,  9,  9, 5),
    "Doberman":             (23,  9, 8,  9, 10, 5),
    "Chow Chow":            (21, 11, 5, 11, 10, 3),
    "Jack Russell":         (18,  8, 4,  8,  8, 4),
    "Rhodesian Ridgeback":  (24, 10, 7, 10, 10, 5),
    "Cane Corso":           (24, 13, 7, 13, 12, 4),
    "Bernese Mountain Dog": (24, 12, 7, 11, 11, 4),
    "Whippet":              (24,  7, 9,  8,  9, 5),
    "Basenji":              (19,  9, 5,  9,  9, 4),
    "Saint Bernard":        (26, 13, 7, 13, 12, 4),
}

# Fallback silhouettes for mixed-breed dogs whose breed name isn't listed.
SIZE_CLASS_SILHOUETTES = {
    "small":  (19,  9, 5,  9,  9, 4),
    "medium": (22, 10, 6, 10,  9, 4),
    "large":  (23, 11, 7, 10, 10, 4),
    "giant":  (26, 13, 7, 12, 12, 4),
}


# ── Colour helpers ────────────────────────────────────────────────────────────

def _darker(c, amt=40):
    return tuple(max(0, v - amt) for v in c)

def _lighter(c, amt=35):
    return tuple(min(255, v + amt) for v in c)


# ── Silhouette lookup ─────────────────────────────────────────────────────────

def _silhouette_for(traits):
    breed = traits.get("breed", "")
    if breed in BREED_SILHOUETTES:
        return BREED_SILHOUETTES[breed]
    return SIZE_CLASS_SILHOUETTES.get(
        traits.get("size_class", "medium"),
        SIZE_CLASS_SILHOUETTES["medium"],
    )


# ── Sub-piece drawers ─────────────────────────────────────────────────────────

def _legs_xs(body_x, body_w, i):
    """Return (back_a, back_b, front_a, front_b) leg x positions."""
    return (
        body_x + i(2),
        body_x + i(6),
        body_x + body_w - i(8),
        body_x + body_w - i(4),
    )

def _draw_legs(surf, body_x, body_w, leg_top_y, leg_h, leg_w, dark, i):
    for lx in _legs_xs(body_x, body_w, i):
        pygame.draw.rect(surf, dark, (lx, leg_top_y, leg_w, leg_h))

def _draw_body(surf, body_x, body_top_y, body_w, body_h, coat, c_length, i, s):
    if c_length == "long" and s >= 0.8:
        pygame.draw.rect(surf, _lighter(coat, 20),
            (body_x - i(1), body_top_y - i(1), body_w + i(2), body_h + i(2)),
            border_radius=2)
    pygame.draw.rect(surf, coat,
        (body_x, body_top_y, body_w, body_h), border_radius=i(2))

def _draw_pattern(surf, body_x, body_top_y, body_w, body_h, pattern, dark, i):
    if pattern == "spotted":
        n = max(3, body_w // max(1, i(5)))
        for k in range(n):
            cx = body_x + int(body_w * (k + 0.5) / n)
            cy = body_top_y + i(2 + (k % 4))
            pygame.draw.circle(surf, dark, (cx, cy), max(1, i(2 + (k % 2))))
    elif pattern == "merle":
        n = max(2, body_w // max(1, i(7)))
        for k in range(n):
            cx = body_x + int(body_w * (k + 0.5) / n)
            cy = body_top_y + i(1 + (k % 4))
            pygame.draw.ellipse(surf, dark, (cx - i(3), cy, i(6), i(4)))
    elif pattern == "brindle":
        step = max(i(1) + 1, i(4))
        for lx in range(body_x + i(4), body_x + body_w - i(1), step):
            pygame.draw.line(surf, dark,
                (lx, body_top_y + i(1)),
                (lx, body_top_y + body_h - i(1)))
    elif pattern == "saddle":
        pygame.draw.rect(surf, dark,
            (body_x + i(4), body_top_y, body_w - i(8), body_h))
    elif pattern == "ticked":
        n = max(6, body_w // max(1, i(3)))
        ys = (1, 3, 5, 2, 6, 4)
        for k in range(n):
            cx = body_x + int(body_w * (k + 0.5) / n)
            cy = body_top_y + i(ys[k % 6])
            pygame.draw.rect(surf, dark, (cx, cy, max(1, i(1)), max(1, i(1))))

def _draw_white_spotting(surf, body_x, body_top_y, body_w, body_h,
                         head_x, head_top_y, head_w, head_h,
                         leg_top_y, leg_h, leg_w, w_spotting, i):
    if w_spotting == "irish":
        pygame.draw.rect(surf, WHITE,
            (body_x + body_w - i(6), body_top_y + i(2), i(6), body_h - i(2)))
        for lx in _legs_xs(body_x, body_w, i):
            pygame.draw.rect(surf, WHITE,
                (lx, leg_top_y + leg_h - i(3), leg_w, i(3)))
    elif w_spotting == "piebald":
        pygame.draw.rect(surf, WHITE,
            (body_x + body_w - i(8), body_top_y + i(1), i(8), body_h - i(1)))
        pygame.draw.ellipse(surf, WHITE,
            (body_x + i(3), body_top_y, i(7), i(7)))
        for lx in _legs_xs(body_x, body_w, i):
            pygame.draw.rect(surf, WHITE,
                (lx, leg_top_y - i(2), leg_w, leg_h + i(2)))
    elif w_spotting == "extreme_white":
        pygame.draw.rect(surf, WHITE,
            (body_x, body_top_y, body_w, body_h), border_radius=i(2))
        pygame.draw.rect(surf, WHITE,
            (head_x, head_top_y, head_w, head_h), border_radius=i(2))
        for lx in _legs_xs(body_x, body_w, i):
            pygame.draw.rect(surf, WHITE, (lx, leg_top_y, leg_w, leg_h))

def _draw_coat_texture(surf, body_x, body_top_y, body_w, body_h,
                       coat, dark, c_type, i, s):
    if c_type == "wavy" and s >= 1.0:
        light = _lighter(coat, 10)
        for r in range(0, body_h, max(1, i(3))):
            pygame.draw.line(surf, light,
                (body_x + i(1), body_top_y + r),
                (body_x + body_w - i(2), body_top_y + r + i(1)))
    elif c_type == "wire" and s >= 1.0:
        step = max(i(1) + 1, i(3))
        for x_off in range(i(2), body_w - i(2), step):
            pygame.draw.line(surf, dark,
                (body_x + x_off, body_top_y),
                (body_x + x_off, body_top_y + i(2)))

def _draw_tail(surf, body_x, body_top_y, tail_type, dark, i):
    tx = body_x - i(1)
    ty = body_top_y + i(1)
    if tail_type == "long":
        pygame.draw.line(surf, dark, (tx, ty), (tx - i(8), ty - i(5)),
                         max(1, i(2)))
    elif tail_type == "curled":
        for t in range(8):
            ang = math.pi * t / 8
            cx = tx - int(i(5) * math.cos(ang))
            cy = ty - int(i(5) * math.sin(ang))
            pygame.draw.circle(surf, dark, (cx, cy), max(1, i(2)))
    elif tail_type == "short":
        pygame.draw.rect(surf, dark, (tx - i(4), ty, i(5), i(3)))
    elif tail_type == "bob":
        pygame.draw.circle(surf, dark, (tx - i(2), ty + i(1)), max(1, i(3)))

def _draw_head(surf, head_x, head_top_y, head_w, head_h, coat, c_length, i, s):
    rect = pygame.Rect(head_x, head_top_y, head_w, head_h)
    pygame.draw.rect(surf, coat, rect, border_radius=i(2))
    if c_length == "long" and s >= 0.8:
        pygame.draw.rect(surf, _lighter(coat, 15), rect, 1, border_radius=i(2))

def _draw_muzzle(surf, head_x, head_top_y, head_w, head_h, snout_len,
                 coat, light, i):
    muzzle_w = i(snout_len)
    muzzle_h = i(3)
    muzzle_x = head_x + head_w - i(2)
    muzzle_y = head_top_y + head_h - i(4)
    pygame.draw.rect(surf, light, (muzzle_x, muzzle_y, muzzle_w, muzzle_h))
    pygame.draw.rect(surf, _darker(coat, 60),
        (muzzle_x + max(0, muzzle_w - i(2)), muzzle_y, i(2), i(2)))

def _draw_eye(surf, head_x, head_top_y, head_w, eye_col, i):
    eye_pos = (head_x + head_w - i(3), head_top_y + i(2))
    pygame.draw.circle(surf, eye_col, eye_pos, max(1, i(2)))
    pygame.draw.circle(surf, (20, 15, 10), eye_pos, max(1, i(1)))

def _draw_ear(surf, head_x, head_top_y, ear_type, dark, i):
    ear_x = head_x + i(1)
    if ear_type == "erect":
        pygame.draw.polygon(surf, dark, [
            (ear_x,        head_top_y),
            (ear_x + i(4), head_top_y - i(7)),
            (ear_x + i(6), head_top_y),
        ])
    elif ear_type == "semi-erect":
        pygame.draw.polygon(surf, dark, [
            (ear_x,        head_top_y),
            (ear_x + i(3), head_top_y - i(5)),
            (ear_x + i(6), head_top_y - i(2)),
        ])
    else:  # floppy
        pygame.draw.rect(surf, dark,
            (ear_x + i(2), head_top_y + i(1), i(5), i(4)),
            border_radius=i(1))

def _draw_overlays(surf, dog, body_top_y, head_x, head_top_y, head_w, traits, i):
    if getattr(dog, "stay_mode", False) and getattr(dog, "tamed", False):
        cx = head_x + head_w // 2
        pygame.draw.circle(surf, (220, 240, 200),
            (cx, head_top_y - i(5)), max(1, i(2)))
    if traits.get("collar_applied", False):
        pygame.draw.rect(surf, (200, 60, 40),
            (head_x - i(1), body_top_y, i(4), i(2)))


# ── Right-facing draw orchestrator ────────────────────────────────────────────

def _draw_dog_right(surf, ox, oy, dog, s):
    """Draw a right-facing dog onto surf, anchor at (ox, oy)."""
    traits = getattr(dog, "traits", {})
    body_len, body_h, leg_len, head_w, head_h, snout_len = _silhouette_for(traits)

    coat       = traits.get("coat_color", (160, 100, 50))
    dark       = _darker(coat, 40)
    light      = _lighter(coat, 35)
    pattern    = traits.get("coat_pattern", "solid")
    w_spot     = traits.get("white_spotting", "solid")
    c_length   = traits.get("coat_length", "short")
    c_type     = traits.get("coat_type", "smooth")
    ear_type   = traits.get("ear_type", "floppy")
    tail_type  = traits.get("tail_type", "long")
    eye_col    = DOG_EYE_COLORS.get(traits.get("eye_color", "brown"), (100, 60, 20))

    def i(v): return int(v * s)

    feet_y     = oy + i(_FEET_Y)
    leg_h_pix  = i(leg_len)
    leg_top_y  = feet_y - leg_h_pix
    body_h_pix = i(body_h)
    body_top_y = leg_top_y - body_h_pix
    body_x     = ox + i(2)
    body_w     = i(body_len)
    head_w_pix = i(head_w)
    head_h_pix = i(head_h)
    head_x     = body_x + body_w - i(2)
    head_top_y = body_top_y - i(3)
    leg_w      = max(1, i(4))

    _draw_body(surf, body_x, body_top_y, body_w, body_h_pix,
               coat, c_length, i, s)
    _draw_pattern(surf, body_x, body_top_y, body_w, body_h_pix,
                  pattern, dark, i)
    _draw_white_spotting(surf, body_x, body_top_y, body_w, body_h_pix,
        head_x, head_top_y, head_w_pix, head_h_pix,
        leg_top_y, leg_h_pix, leg_w, w_spot, i)
    _draw_legs(surf, body_x, body_w, leg_top_y, leg_h_pix, leg_w, dark, i)
    _draw_head(surf, head_x, head_top_y, head_w_pix, head_h_pix,
               coat, c_length, i, s)
    _draw_muzzle(surf, head_x, head_top_y, head_w_pix, head_h_pix, snout_len,
                 coat, light, i)
    _draw_eye(surf, head_x, head_top_y, head_w_pix, eye_col, i)
    _draw_ear(surf, head_x, head_top_y, ear_type, dark, i)
    _draw_tail(surf, body_x, body_top_y, tail_type, dark, i)
    _draw_coat_texture(surf, body_x, body_top_y, body_w, body_h_pix,
                       coat, dark, c_type, i, s)
    _draw_overlays(surf, dog, body_top_y, head_x, head_top_y,
                   head_w_pix, traits, i)


# ── Public entry points ───────────────────────────────────────────────────────

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
    sc = size / 36.0
    pygame.draw.rect(screen, (28, 20, 12), (dx, dy, size, size))
    pygame.draw.rect(screen, (60, 45, 25), (dx, dy, size, size), 1)
    ox = dx + int(size * 0.10)
    oy = dy + int(size * 0.40)
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
    heart_w = 10
    total_w = threshold * (heart_w + 2)
    start_x = sx - total_w // 2
    for i_h in range(threshold):
        hx     = start_x + i_h * (heart_w + 2)
        filled = i_h < progress
        col    = (220, 60, 80) if filled else (80, 40, 40)
        pts    = [(hx + 5, sy), (hx + 10, sy + 4), (hx + 5, sy + 8), (hx, sy + 4)]
        pygame.draw.polygon(screen, col, pts)
        if not filled:
            pygame.draw.polygon(screen, (120, 60, 70), pts, 1)
