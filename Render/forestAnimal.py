import pygame


def draw_deer(screen, sx, sy, e):
    W, H = e.W, e.H  # 28×22
    s = e.traits.get("size", 1.0)
    body_col   = (175, 125, 72)
    leg_col    = (148, 103, 58)
    antler_col = (108,  72, 32)
    f = e.facing  # 1 = right

    # Slender body
    pygame.draw.ellipse(screen, body_col,
                        (sx + 2, sy + int(H * 0.32), W - 4, int(H * 0.52)))
    # White rump patch (back side, opposite to head)
    rump_x = sx if f == 1 else sx + W - int(5 * s)
    pygame.draw.ellipse(screen, (242, 228, 205),
                        (rump_x, sy + int(H * 0.38), int(5 * s), int(4 * s)))

    # Four thin legs, well spaced
    leg_w = max(2, int(2 * s))
    for lp in (0.12, 0.30, 0.58, 0.76):
        lx = sx + int(W * lp)
        pygame.draw.rect(screen, leg_col,
                         (lx, sy + int(H * 0.72), leg_w, int(H * 0.28)))

    # Neck
    nw = int(5 * s)
    nx = (sx + W - int(9 * s)) if f == 1 else (sx + int(4 * s))
    pygame.draw.rect(screen, body_col,
                     (nx, sy + int(H * 0.10), nw, int(H * 0.32)))

    # Head (elongated oval)
    hw, hh = int(8 * s), int(6 * s)
    hx = (sx + W - hw + 1) if f == 1 else (sx - 1)
    pygame.draw.ellipse(screen, body_col, (hx, sy + int(H * 0.05), hw, hh))

    # Nose
    nose_x = hx + (hw - 2 if f == 1 else 0)
    pygame.draw.rect(screen, (110, 72, 42), (nose_x, sy + int(H * 0.18), 2, 2))

    # Eye
    eye_x = hx + (int(hw * 0.60) if f == 1 else int(hw * 0.35))
    pygame.draw.rect(screen, (25, 18, 12), (eye_x, sy + int(H * 0.10), 1, 1))

    # Antlers: Y-fork with brow tine, from back of skull
    ax = hx + (int(hw * 0.30) if f == 1 else int(hw * 0.70))
    ay = sy + int(H * 0.05)
    mid_y = ay - int(5 * s)
    pygame.draw.line(screen, antler_col, (ax, ay), (ax, mid_y), 1)
    pygame.draw.line(screen, antler_col, (ax, mid_y),
                     (ax + (3 if f == 1 else -3), mid_y - int(3 * s)), 1)
    pygame.draw.line(screen, antler_col, (ax, mid_y),
                     (ax + (-2 if f == 1 else 2), mid_y - int(3 * s)), 1)
    pygame.draw.line(screen, antler_col, (ax, ay - int(2 * s)),
                     (ax + (4 if f == 1 else -4), ay - int(4 * s)), 1)

    if e.health < 3:
        pygame.draw.rect(screen, (220, 50, 50),
                         (sx, sy - 5, int(W * e.health / 3), 2))


def draw_boar(screen, sx, sy, e):
    W, H = e.W, e.H  # 26×18
    s = e.traits.get("size", 1.0)
    body_col  = (82,  62, 48)
    dark_col  = (58,  42, 32)
    snout_col = (105, 80, 60)
    f = e.facing

    # Low-slung body
    pygame.draw.ellipse(screen, body_col,
                        (sx + 1, sy + int(H * 0.28), W - 2, int(H * 0.58)))
    # Spine bristle ridge (dark strip along the back)
    pygame.draw.ellipse(screen, dark_col,
                        (sx + int(W * 0.15), sy + int(H * 0.20),
                         int(W * 0.70), int(H * 0.22)))

    # Short stocky legs
    leg_w = max(3, int(4 * s))
    for lp in (0.12, 0.30, 0.56, 0.74):
        lx = sx + int(W * lp)
        pygame.draw.rect(screen, dark_col,
                         (lx, sy + int(H * 0.75), leg_w, int(H * 0.25)))

    # Large low-set head
    hw, hh = int(9 * s), int(8 * s)
    hx = (sx + W - hw) if f == 1 else sx
    pygame.draw.rect(screen, body_col,
                     (hx, sy + int(H * 0.25), hw, hh))

    # Eye (toward front of head)
    eye_x = hx + (int(hw * 0.60) if f == 1 else int(hw * 0.35))
    pygame.draw.rect(screen, (20, 15, 10),
                     (eye_x, sy + int(H * 0.30), 2, 2))

    # Wide snout
    sw, sh = int(6 * s), int(4 * s)
    snx = hx + (hw - sw if f == 1 else 0)
    sny = sy + int(H * 0.38)
    pygame.draw.rect(screen, snout_col, (snx, sny, sw, sh))
    # Nostrils
    nox = snx + (int(sw * 0.25) if f == 1 else int(sw * 0.45))
    pygame.draw.rect(screen, dark_col, (nox, sny + 1, 1, 1))
    pygame.draw.rect(screen, dark_col, (nox + 2, sny + 1, 1, 1))

    # Two upward-curving tusks
    tx = snx + (sw - 1 if f == 1 else 1)
    t_base_y = sny + sh - 1
    pygame.draw.line(screen, (232, 215, 182),
                     (tx, t_base_y),
                     (tx + (3 if f == 1 else -3), t_base_y - int(4 * s)), 1)
    pygame.draw.line(screen, (215, 198, 165),
                     (tx + (-2 if f == 1 else 2), t_base_y),
                     (tx + (1 if f == 1 else -1), t_base_y - int(3 * s)), 1)

    if e.health < 3:
        pygame.draw.rect(screen, (220, 50, 50),
                         (sx, sy - 5, int(W * e.health / 3), 2))


def draw_rabbit(screen, sx, sy, e):
    W, H = e.W, e.H  # 14×12
    s = e.traits.get("size", 1.0)
    col       = (212, 198, 178)
    ear_inner = (195, 155, 148)
    f = e.facing

    # Body
    pygame.draw.ellipse(screen, col,
                        (sx + 1, sy + int(H * 0.42), W - 2, int(H * 0.58)))

    # Head (offset toward facing direction)
    hw, hh = int(7 * s), int(6 * s)
    hx = (sx + W - hw) if f == 1 else sx
    pygame.draw.ellipse(screen, col, (hx, sy + int(H * 0.20), hw, hh))

    # Two tall ears, clearly separated
    e1x = hx + (int(hw * 0.65) if f == 1 else int(hw * 0.20))
    e2x = hx + (int(hw * 0.25) if f == 1 else int(hw * 0.60))
    ear_h = int(5 * s)
    for ex_ in (e1x, e2x):
        pygame.draw.rect(screen, col, (ex_, sy, 2, ear_h))
    pygame.draw.rect(screen, ear_inner, (e1x, sy + 1, 1, ear_h - 2))

    # Fluffy white tail (back side)
    tail_x = sx if f == 1 else sx + W - 3
    pygame.draw.ellipse(screen, (245, 242, 238),
                        (tail_x, sy + int(H * 0.50), 3, 3))

    # Eye
    eye_x = hx + (int(hw * 0.65) if f == 1 else int(hw * 0.25))
    pygame.draw.rect(screen, (38, 22, 18), (eye_x, sy + int(H * 0.28), 1, 1))

    if e.health < 1:
        pass  # rabbit dies in 1 hit
    else:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, W, 2))


def draw_turkey(screen, sx, sy, e):
    W, H = e.W, e.H  # 20×18
    s = e.traits.get("size", 1.0)
    body_col = (95, 72, 48)
    dark_col = (68, 50, 33)
    plume1   = (158, 82, 25)
    plume2   = (108, 52, 18)
    leg_col  = (128, 98, 50)
    f = e.facing

    # Fan tail drawn first (behind body)
    tcx = (sx + int(W * 0.18)) if f == 1 else (sx + int(W * 0.82))
    tcy = sy + int(H * 0.45)
    fd = -1 if f == 1 else 1  # fan x-direction (away from head)
    fan_tips = [
        (fd * int(6 * s), -int(2 * s)),
        (fd * int(5 * s), -int(5 * s)),
        (fd * int(3 * s), -int(7 * s)),
        (fd * int(1 * s), -int(7 * s)),
        (0,               -int(6 * s)),
    ]
    for i, (dx, dy) in enumerate(fan_tips):
        pygame.draw.line(screen, plume1 if i % 2 == 0 else plume2,
                         (tcx, tcy), (tcx + dx, tcy + dy), 2)

    # Plump body
    pygame.draw.ellipse(screen, body_col,
                        (sx + 1, sy + int(H * 0.28), W - 2, int(H * 0.58)))
    # Wing feather texture (slightly darker ellipse)
    pygame.draw.ellipse(screen, dark_col,
                        (sx + int(W * 0.25), sy + int(H * 0.36),
                         int(W * 0.50), int(H * 0.34)))

    # Two legs
    for i in range(2):
        lx = sx + int(W * (0.35 + i * 0.22))
        pygame.draw.line(screen, leg_col,
                         (lx, sy + int(H * 0.78)), (lx + 1, sy + H), 2)

    # Neck
    nw = int(4 * s)
    nx = (sx + W - int(6 * s)) if f == 1 else (sx + int(2 * s))
    pygame.draw.rect(screen, body_col,
                     (nx, sy + int(H * 0.15), nw, int(H * 0.24)))

    # Head
    hw = int(5 * s)
    hx = (sx + W - hw) if f == 1 else sx
    pygame.draw.ellipse(screen, body_col,
                        (hx, sy + int(H * 0.04), hw, int(H * 0.26)))

    # Red wattle/snood
    snood_x = hx + (hw - 1 if f == 1 else 0)
    pygame.draw.line(screen, (195, 45, 35),
                     (snood_x, sy + int(H * 0.22)),
                     (snood_x, sy + int(H * 0.35)), 2)

    # Eye
    eye_x = hx + (int(hw * 0.35) if f == 1 else int(hw * 0.60))
    pygame.draw.rect(screen, (25, 18, 12),
                     (eye_x, sy + int(H * 0.10), 1, 1))

    if e.health < 2:
        pygame.draw.rect(screen, (220, 50, 50),
                         (sx, sy - 5, int(W * e.health / 2), 2))


def draw_wolf(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col     = (110, 100,  90)
    leg_col = ( 85,  75,  65)
    # Lean body
    pygame.draw.rect(screen, col, (sx, sy + int(H * 0.3), W, int(H * 0.55)))
    # Legs
    for i in range(4):
        lx = sx + int(W * (0.12 + i * 0.22))
        pygame.draw.rect(screen, leg_col, (lx, sy + int(H * 0.75), max(2, int(3*s)), int(H * 0.25)))
    # Bushy tail (opposite to facing)
    tail_x = (sx - int(4*s)) if e.facing == 1 else (sx + W)
    pygame.draw.ellipse(screen, col, (tail_x, sy + int(H * 0.2), int(6*s), int(5*s)))
    # Head + snout
    head_w = int(8 * s)
    hx = (sx + W - head_w) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (hx, sy + int(H * 0.15), head_w, int(H * 0.45)))
    # Ears
    ex = hx + (int(head_w * 0.6) if e.facing == 1 else int(head_w * 0.2))
    pygame.draw.polygon(screen, col, [(ex, sy + int(H*0.15)), (ex-2, sy - int(4*s)), (ex+2, sy - int(4*s))])
    if e.health < 2:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health / 2), 2))


def draw_bear(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col     = ( 80,  58,  40)
    snout_c = (110,  85,  60)
    # Massive body
    pygame.draw.ellipse(screen, col, (sx, sy + int(H * 0.2), W, int(H * 0.72)))
    # Short thick legs
    leg_w = max(3, int(5*s))
    for i in range(4):
        lx = sx + int(W * (0.1 + i * 0.25))
        pygame.draw.rect(screen, col, (lx, sy + int(H * 0.75), leg_w, int(H * 0.25)))
    # Round head
    head_r = int(8 * s)
    hx = (sx + W - head_r * 2 + 2) if e.facing == 1 else sx
    pygame.draw.ellipse(screen, col, (hx, sy, head_r * 2, int(head_r * 1.6)))
    # Snout
    snout_x = hx + (head_r * 2 - int(4*s) if e.facing == 1 else int(2*s))
    pygame.draw.ellipse(screen, snout_c, (snout_x - 1, sy + int(H * 0.18), int(6*s), int(4*s)))
    # Ears
    ex = hx + (int(head_r * 0.4) if e.facing == 1 else int(head_r * 1.2))
    pygame.draw.circle(screen, col, (ex, sy + 2), max(2, int(3*s)))
    if e.health < 4:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 6, int(W * e.health / 4), 3))
