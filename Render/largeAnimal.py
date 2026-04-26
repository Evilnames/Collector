import pygame


def _tinted(base_color, shift):
    return tuple(max(0, min(255, int(base_color[i] + shift[i] * 255))) for i in range(3))


_trade_warn_font = None


def _get_trade_warn_font():
    global _trade_warn_font
    if _trade_warn_font is None:
        _trade_warn_font = pygame.font.SysFont("consolas", 14, bold=True)
    return _trade_warn_font


def draw_horse(screen, sx, sy, horse):
    W, H = horse.W, horse.H
    traits    = getattr(horse, 'traits', {})
    s         = traits.get("size", 1.0)
    shift     = traits.get("color_shift", (0, 0, 0))
    coat      = traits.get("coat_color", (160, 115, 65))
    body_color = _tinted(coat, shift)
    dark_coat  = tuple(max(0, c - 40) for c in body_color)
    _MANE_COLORS = {
        "match":  tuple(max(0, c - 60) for c in body_color),
        "flaxen": _tinted((215, 185, 95), shift),
        "silver": _tinted((185, 185, 195), shift),
        "dark":   _tinted((28, 22, 18), shift),
    }
    mane_color = _MANE_COLORS.get(traits.get("mane_color", "match"), _MANE_COLORS["match"])

    body_h = int(H * 0.65)
    leg_h  = H - body_h
    leg_y  = sy + body_h

    leg_marking = traits.get("leg_marking", "none")
    leg_w = max(1, int(4 * s))
    sock_color = (240, 238, 230)
    for lx_off in [3, 9, 22, 28]:
        pygame.draw.rect(screen, dark_coat,
                         (sx + int(lx_off * s), leg_y, leg_w, leg_h))
        if leg_marking == "stockings":
            pygame.draw.rect(screen, sock_color,
                             (sx + int(lx_off * s), leg_y, leg_w, leg_h - 2))
        elif leg_marking == "socks":
            sock_h = max(2, leg_h // 2)
            pygame.draw.rect(screen, sock_color,
                             (sx + int(lx_off * s), leg_y + leg_h - sock_h, leg_w, sock_h - 2))
    hoof_c = (30, 25, 20)
    for lx_off in [3, 9, 22, 28]:
        pygame.draw.rect(screen, hoof_c,
                         (sx + int(lx_off * s), leg_y + leg_h - 2, leg_w, 2))

    pygame.draw.rect(screen, body_color, (sx, sy, W, body_h))
    pygame.draw.rect(screen, mane_color,
                     (sx + int(4 * s), sy, int((W - 8) * s), max(2, int(4 * s))))

    coat_pattern = traits.get("coat_pattern", "solid")
    if coat_pattern == "dappled":
        dapple_c = tuple(max(0, c - 30) for c in body_color)
        for ox, oy, ow, oh in [(6, 4, 6, 4), (16, 2, 5, 4), (10, 9, 5, 3),
                                (22, 7, 6, 3), (4, 11, 4, 3)]:
            px2 = sx + int(ox * s)
            py2 = sy + int(oy * s)
            pygame.draw.ellipse(screen, dapple_c,
                                (px2, py2, max(3, int(ow * s)), max(2, int(oh * s))))
    elif coat_pattern == "spotted":
        spot_c = tuple(min(255, c + 50) for c in body_color)
        for ox, oy, r in [(8, 5, 4), (20, 3, 3), (14, 10, 5), (26, 9, 3)]:
            pygame.draw.circle(screen, spot_c,
                               (sx + int(ox * s), sy + int(oy * s)), max(2, int(r * s)))
    elif coat_pattern == "blanket":
        blanket_c = tuple(min(255, c + 45) for c in body_color)
        blanket_x = sx + int(W * 0.55)
        blanket_w = W - int(W * 0.55)
        pygame.draw.rect(screen, blanket_c, (blanket_x, sy, blanket_w, body_h))

    tail_x = sx if horse.facing == 1 else sx + W - int(5 * s)
    pygame.draw.rect(screen, mane_color,
                     (tail_x, sy + int(4 * s), max(2, int(4 * s)), int(body_h * 0.6)))

    head_w = int(12 * s)
    head_h = int(12 * s)
    hx = (sx + W - int(2 * s)) if horse.facing == 1 else (sx - head_w + int(2 * s))
    hy = sy - int(4 * s)
    pygame.draw.rect(screen, body_color, (hx, hy, head_w, head_h))

    face_marking = traits.get("face_marking", "none")
    mark_c = (245, 242, 238)
    if face_marking == "star":
        mark_cx = hx + head_w // 2
        mark_cy = hy + int(3 * s)
        pygame.draw.circle(screen, mark_c, (mark_cx, mark_cy), max(2, int(2 * s)))
    elif face_marking == "blaze":
        blaze_w = max(3, int(4 * s))
        blaze_x = hx + head_w // 2 - blaze_w // 2
        pygame.draw.rect(screen, mark_c, (blaze_x, hy, blaze_w, head_h))
    elif face_marking == "stripe":
        stripe_w = max(1, int(2 * s))
        stripe_x = hx + head_w // 2 - stripe_w // 2
        pygame.draw.rect(screen, mark_c, (stripe_x, hy, stripe_w, head_h))

    muzzle_w = int(5 * s)
    muzzle_x = (hx + head_w - muzzle_w) if horse.facing == 1 else hx
    pygame.draw.rect(screen, _tinted((200, 175, 145), shift),
                     (muzzle_x, hy + int(6 * s), muzzle_w, int(5 * s)))

    eye_x = (hx + head_w - int(5 * s)) if horse.facing == 1 else (hx + max(1, int(2 * s)))
    pygame.draw.rect(screen, (15, 10, 5), (eye_x, hy + int(3 * s), 2, 2))

    ear_x = (hx + int(2 * s)) if horse.facing == 1 else (hx + head_w - int(4 * s))
    pygame.draw.rect(screen, dark_coat, (ear_x, hy - int(4 * s), max(2, int(3 * s)), int(4 * s)))

    if getattr(horse, 'tamed', False) and getattr(horse, '_broken', False):
        saddle_x = sx + int(W * 0.3)
        saddle_w = int(W * 0.4)
        pygame.draw.rect(screen, (110, 65, 25),
                         (saddle_x, sy, saddle_w, max(2, int(5 * s))))

    if getattr(horse, 'tamed', False) and not getattr(horse, '_broken', False):
        pygame.draw.circle(screen, (255, 80, 120), (sx + W // 2, sy - 10), 4)
    elif getattr(horse, 'tamed', False):
        pygame.draw.circle(screen, (80, 180, 255), (sx + W // 2, sy - 10), 4)

    if getattr(horse, '_on_trade_run', False) and getattr(horse, '_trade_stuck', False):
        font = _get_trade_warn_font()
        warn = font.render("!", True, (255, 160, 0))
        cx = sx + W // 2
        pygame.draw.circle(screen, (255, 160, 0), (cx, sy - 22), 7, 2)
        screen.blit(warn, (cx - warn.get_width() // 2, sy - 29))

    temp = traits.get("temperament", "spirited")
    temp_colors = {"calm": (80, 200, 80), "spirited": (220, 180, 40), "wild": (220, 60, 60)}
    pygame.draw.circle(screen, temp_colors.get(temp, (180, 180, 180)),
                       (sx + 4, sy - 6), 3)


def draw_dog(screen, sx, sy, dog, font):
    from Render.dogs import draw_dog as _draw_dog_base, draw_tame_hearts
    _draw_dog_base(screen, sx, sy, dog, scale=1.0, facing=getattr(dog, "facing", 1))
    if getattr(dog, "stay_mode", False) and getattr(dog, "tamed", False):
        lbl = font.render("SIT", True, (180, 240, 140))
        screen.blit(lbl, (sx + dog.W // 2 - lbl.get_width() // 2, sy - 14))
    if not dog.tamed and dog.tame_progress > 0:
        stubbornness = dog.traits.get("stubbornness", 0.5)
        threshold = max(1, int(5 + stubbornness * 7))
        draw_tame_hearts(screen, sx + dog.W // 2, sy - 14, dog.tame_progress, threshold)
    if getattr(dog, "_tracking_hint", False):
        pygame.draw.circle(screen, (240, 210, 80), (sx + dog.W + 4, sy + 4), 3)
        dog._tracking_hint = False


def draw_snow_leopard(screen, sx, sy, cat):
    W, H = cat.W, cat.H
    s = cat.traits.get("size", 1.0)
    shift = cat.traits.get("color_shift", (0, 0, 0))
    body_h = int(12 * s)
    leg_h = H - body_h
    leg_y = sy + body_h

    fur    = _tinted((215, 215, 222), shift)
    spot   = _tinted((68, 68, 82),    shift)
    leg_c  = _tinted((195, 195, 205), shift)
    eye_c  = (95, 165, 130)

    tail_seg1_len = int(11 * s)
    tail_seg2_len = int(7 * s)
    tail_w = max(2, int(3 * s))
    tail_y1 = sy + int(5 * s)
    tail_y2 = sy + int(2 * s)
    if cat.facing == 1:
        pygame.draw.rect(screen, fur, (sx - tail_seg1_len, tail_y1, tail_seg1_len, tail_w))
        pygame.draw.rect(screen, spot, (sx - int(4 * s), tail_y1, max(1, int(2 * s)), tail_w))
        pygame.draw.rect(screen, fur, (sx - tail_seg1_len - tail_seg2_len, tail_y2, tail_seg2_len, tail_w))
    else:
        tx = sx + W
        pygame.draw.rect(screen, fur, (tx, tail_y1, tail_seg1_len, tail_w))
        pygame.draw.rect(screen, spot, (tx + int(7 * s), tail_y1, max(1, int(2 * s)), tail_w))
        pygame.draw.rect(screen, fur, (tx + tail_seg1_len, tail_y2, tail_seg2_len, tail_w))

    for lx_off in [int(4 * s), int(10 * s), int(22 * s), int(28 * s)]:
        pygame.draw.rect(screen, leg_c, (sx + lx_off, leg_y, max(1, int(3 * s)), leg_h))

    pygame.draw.rect(screen, fur, (sx, sy, W, body_h))
    for bx_off, by_off in [(int(5 * s), int(2 * s)), (int(14 * s), int(6 * s)), (int(23 * s), int(2 * s))]:
        pygame.draw.rect(screen, spot, (sx + bx_off, sy + by_off, max(2, int(4 * s)), max(2, int(3 * s))))
        pygame.draw.rect(screen, spot, (sx + bx_off + max(1, int(2 * s)), sy + by_off - max(1, int(1 * s)), max(1, int(2 * s)), max(1, int(2 * s))))

    head_w, head_h = int(10 * s), int(12 * s)
    hx = (sx + W - max(1, int(2 * s))) if cat.facing == 1 else (sx - head_w + max(1, int(2 * s)))
    hy = sy - max(1, int(2 * s))
    pygame.draw.rect(screen, fur, (hx, hy, head_w, head_h))

    ear_w, ear_h = max(2, int(3 * s)), max(2, int(4 * s))
    pygame.draw.rect(screen, leg_c, (hx + max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))
    pygame.draw.rect(screen, leg_c, (hx + head_w - ear_w - max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))

    eye_x = (hx + head_w - max(2, int(4 * s))) if cat.facing == 1 else (hx + max(1, int(2 * s)))
    pygame.draw.rect(screen, eye_c, (eye_x, hy + max(2, int(4 * s)), 2, 2))


def draw_mountain_lion(screen, sx, sy, cat):
    W, H = cat.W, cat.H
    s = cat.traits.get("size", 1.0)
    shift = cat.traits.get("color_shift", (0, 0, 0))
    body_h = int(14 * s)
    leg_h = H - body_h
    leg_y = sy + body_h

    fur      = _tinted((188, 148, 78),  shift)
    belly    = _tinted((218, 192, 138), shift)
    tail_tip = _tinted((65,  50,  25),  shift)
    leg_c    = _tinted((170, 135, 70),  shift)
    eye_c    = (200, 155, 40)

    tail_seg1_len = int(12 * s)
    tail_seg2_len = int(7 * s)
    tail_w = max(2, int(3 * s))
    tail_y1 = sy + int(5 * s)
    tail_y2 = sy + int(3 * s)
    if cat.facing == 1:
        pygame.draw.rect(screen, fur, (sx - tail_seg1_len, tail_y1, tail_seg1_len, tail_w))
        pygame.draw.rect(screen, tail_tip, (sx - tail_seg1_len - tail_seg2_len, tail_y2, tail_seg2_len, tail_w))
    else:
        tx = sx + W
        pygame.draw.rect(screen, fur, (tx, tail_y1, tail_seg1_len, tail_w))
        pygame.draw.rect(screen, tail_tip, (tx + tail_seg1_len, tail_y2, tail_seg2_len, tail_w))

    for lx_off in [int(4 * s), int(11 * s), int(24 * s), int(31 * s)]:
        pygame.draw.rect(screen, leg_c, (sx + lx_off, leg_y, max(1, int(3 * s)), leg_h))

    pygame.draw.rect(screen, fur, (sx, sy, W, body_h))
    belly_w = int(18 * s)
    pygame.draw.rect(screen, belly,
                     (sx + (W - belly_w) // 2, sy + int(6 * s), belly_w, int(5 * s)))

    head_w, head_h = int(11 * s), int(13 * s)
    hx = (sx + W - max(1, int(3 * s))) if cat.facing == 1 else (sx - head_w + max(1, int(3 * s)))
    hy = sy - max(1, int(3 * s))
    pygame.draw.rect(screen, fur, (hx, hy, head_w, head_h))

    muzzle_w, muzzle_h = max(2, int(5 * s)), max(2, int(4 * s))
    muzzle_x = (hx + head_w - muzzle_w) if cat.facing == 1 else hx
    pygame.draw.rect(screen, belly, (muzzle_x, hy + int(7 * s), muzzle_w, muzzle_h))

    ear_w, ear_h = max(2, int(3 * s)), max(2, int(4 * s))
    pygame.draw.rect(screen, leg_c, (hx + max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))
    pygame.draw.rect(screen, leg_c, (hx + head_w - ear_w - max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))

    eye_x = (hx + head_w - max(2, int(4 * s))) if cat.facing == 1 else (hx + max(1, int(2 * s)))
    pygame.draw.rect(screen, eye_c, (eye_x, hy + max(2, int(4 * s)), 2, 2))


def draw_tiger(screen, sx, sy, cat):
    W, H = cat.W, cat.H
    s = cat.traits.get("size", 1.0)
    shift = cat.traits.get("color_shift", (0, 0, 0))
    body_h = int(15 * s)
    leg_h = H - body_h
    leg_y = sy + body_h

    fur      = _tinted((210, 120, 40),  shift)
    stripe   = _tinted((35,  25,  10),  shift)
    belly    = _tinted((230, 195, 155), shift)
    leg_c    = _tinted((190, 105, 35),  shift)
    eye_c    = (210, 175, 30)

    tail_len = int(14 * s)
    tail_tip_len = int(5 * s)
    tail_w = max(2, int(3 * s))
    tail_y = sy + int(5 * s)
    if cat.facing == 1:
        pygame.draw.rect(screen, fur,    (sx - tail_len, tail_y, tail_len, tail_w))
        pygame.draw.rect(screen, stripe, (sx - tail_tip_len, tail_y, tail_tip_len, tail_w))
    else:
        tx = sx + W
        pygame.draw.rect(screen, fur,    (tx, tail_y, tail_len, tail_w))
        pygame.draw.rect(screen, stripe, (tx + tail_len - tail_tip_len, tail_y, tail_tip_len, tail_w))

    for lx_off in [int(4 * s), int(12 * s), int(27 * s), int(35 * s)]:
        pygame.draw.rect(screen, leg_c, (sx + lx_off, leg_y, max(2, int(4 * s)), leg_h))

    pygame.draw.rect(screen, fur, (sx, sy, W, body_h))
    belly_w = int(20 * s)
    pygame.draw.rect(screen, belly, (sx + (W - belly_w) // 2, sy + int(7 * s), belly_w, int(5 * s)))
    for bx_off in [int(6 * s), int(14 * s), int(23 * s), int(31 * s)]:
        pygame.draw.rect(screen, stripe, (sx + bx_off, sy, max(2, int(3 * s)), body_h))

    head_w, head_h = int(13 * s), int(15 * s)
    hx = (sx + W - max(1, int(3 * s))) if cat.facing == 1 else (sx - head_w + max(1, int(3 * s)))
    hy = sy - max(1, int(3 * s))
    pygame.draw.rect(screen, fur, (hx, hy, head_w, head_h))
    pygame.draw.rect(screen, stripe, (hx + head_w // 2 - 1, hy, max(2, int(2 * s)), int(5 * s)))
    muzzle_w, muzzle_h = max(3, int(6 * s)), max(2, int(5 * s))
    muzzle_x = (hx + head_w - muzzle_w) if cat.facing == 1 else hx
    pygame.draw.rect(screen, belly, (muzzle_x, hy + int(8 * s), muzzle_w, muzzle_h))

    ear_w, ear_h = max(2, int(4 * s)), max(2, int(4 * s))
    pygame.draw.rect(screen, stripe, (hx + max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))
    pygame.draw.rect(screen, stripe, (hx + head_w - ear_w - max(0, int(1 * s)), hy - ear_h, ear_w, ear_h))

    eye_x = (hx + head_w - max(2, int(4 * s))) if cat.facing == 1 else (hx + max(1, int(2 * s)))
    pygame.draw.rect(screen, eye_c, (eye_x, hy + max(2, int(4 * s)), 2, 2))
