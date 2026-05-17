import pygame


def _tinted(base_color, shift):
    return tuple(max(0, min(255, int(base_color[i] + shift[i] * 255))) for i in range(3))


def draw_sheep(screen, sx, sy, sheep):
    W, H = sheep.W, sheep.H
    traits     = getattr(sheep, 'traits', {})
    shift      = traits.get("color_shift", (0, 0, 0))
    s          = traits.get("size", 1.0)
    wc         = traits.get("wool_color", "white")
    pattern    = traits.get("wool_pattern", "solid")
    face_wool  = traits.get("face_wool", "open")
    dark_face  = traits.get("dark_face", False)
    horn_type  = traits.get("horn_type", "none")
    ear_type   = traits.get("ear_type", "upright")
    tail_type  = traits.get("tail_type", "normal")
    wool_length = traits.get("wool_length", 0.5)
    body_h     = H - int(8 * s)
    leg_y      = sy + body_h

    _WOOL_BASE  = {"white": (220, 220, 220), "grey": (175, 175, 175),
                   "brown": (165, 115, 70),  "black": (50, 45, 42)}
    _WOOL_SHORN = {"white": (175, 140, 95),  "grey": (145, 115, 80),
                   "brown": (130, 90, 55),   "black": (45, 38, 32)}
    wool_base  = _WOOL_BASE.get(wc, _WOOL_BASE["white"])
    shorn_base = _WOOL_SHORN.get(wc, _WOOL_SHORN["white"])
    active_base = wool_base if sheep.has_wool else shorn_base

    # Fat tail — drawn behind body at back end (opposite the head)
    if tail_type == "fat_tailed":
        tail_col = _tinted(tuple(max(0, c - 10) for c in active_base), shift)
        if sheep.facing == 1:   # head right, tail at left
            pygame.draw.rect(screen, tail_col, (sx - int(5*s), sy + int(3*s), int(6*s), body_h - int(3*s)))
        else:                   # head left, tail at right
            pygame.draw.rect(screen, tail_col, (sx + W - int(1*s), sy + int(3*s), int(6*s), body_h - int(3*s)))
    elif tail_type == "stub":
        tail_col = _tinted(active_base, shift)
        if sheep.facing == 1:
            pygame.draw.rect(screen, tail_col, (sx - int(3*s), sy + int(4*s), int(3*s), int(4*s)))
        else:
            pygame.draw.rect(screen, tail_col, (sx + W, sy + int(4*s), int(3*s), int(4*s)))

    # Legs
    leg_color = _tinted((80, 60, 40), shift)
    for lx_off in [2, 7, 14, 19]:
        pygame.draw.rect(screen, leg_color,
                         (sx + int(lx_off * s), leg_y, max(1, int(3 * s)), int(8 * s)))

    # Wool puff outline — long-wooled breeds look fluffier (drawn behind body)
    if sheep.has_wool and wool_length > 0.35:
        puff = max(1, int((wool_length - 0.35) * 4.5 * s))
        puff_col = _tinted(tuple(min(255, c + 10) for c in wool_base), shift)
        pygame.draw.rect(screen, puff_col, (sx - puff, sy - puff, W + puff * 2, body_h + puff))

    # Body
    body_color = _tinted(active_base, shift)
    pygame.draw.rect(screen, body_color, (sx, sy, W, body_h))

    # Wool patterns (only when unshorn)
    if sheep.has_wool:
        if pattern == "spotted":
            spot = _tinted(tuple(max(0, c - 75) for c in wool_base), shift)
            pygame.draw.rect(screen, spot, (sx + int(4*s), sy + int(2*s), int(6*s), int(4*s)))
            pygame.draw.rect(screen, spot, (sx + int(13*s), sy + int(4*s), int(5*s), int(4*s)))
        elif pattern == "badgerface":
            band = _tinted(tuple(max(0, c - 55) for c in wool_base), shift)
            pygame.draw.rect(screen, band, (sx, sy + body_h - int(4*s), W, int(4*s)))
        elif pattern == "piebald":
            if wool_base[0] > 140:
                patch = _tinted((45, 35, 28), shift)
            else:
                patch = _tinted((215, 210, 205), shift)
            pygame.draw.rect(screen, patch, (sx + int(3*s), sy + int(1*s), int(7*s), int(6*s)))
            pygame.draw.rect(screen, patch, (sx + int(14*s), sy + int(3*s), int(6*s), int(5*s)))

    # Head
    head_w, head_h = int(9 * s), int(9 * s)
    hx = (sx + W - int(2 * s)) if sheep.facing == 1 else (sx - head_w + int(2 * s))
    hy = sy - max(1, int(1 * s))

    if face_wool == "covered" and sheep.has_wool:
        face_color = _tinted(wool_base, shift)
    elif dark_face:
        face_color = _tinted((38, 28, 20), shift)
    else:
        face_color = _tinted(tuple(max(0, c - 35) for c in active_base), shift)

    pygame.draw.rect(screen, face_color, (hx, hy, head_w, head_h))

    # Ears
    ear_col = _tinted(tuple(max(0, c - 18) for c in face_color), shift)
    if ear_type == "upright":
        # Two small points at top of head
        pygame.draw.rect(screen, ear_col, (hx + int(1*s), hy - int(4*s), max(1, int(2*s)), int(4*s)))
        pygame.draw.rect(screen, ear_col, (hx + int(5*s), hy - int(3*s), max(1, int(2*s)), int(3*s)))
    else:  # drooping — pendulous ears hanging from sides of head
        pygame.draw.rect(screen, ear_col, (hx - int(2*s), hy + int(1*s), int(3*s), int(5*s)))
        pygame.draw.rect(screen, ear_col, (hx + head_w - int(1*s), hy + int(1*s), int(3*s), int(5*s)))

    # Eye — less visible on covered-face breeds
    eye_x = (hx + head_w - int(3 * s)) if sheep.facing == 1 else (hx + max(1, int(1 * s)))
    eye_color = (30, 30, 30) if face_wool != "covered" or not sheep.has_wool else (55, 48, 42)
    pygame.draw.rect(screen, eye_color, (eye_x, hy + int(3 * s), 2, 2))

    # Horns (drawn after head so they appear on top)
    if horn_type != "none":
        horn_color = _tinted((100, 82, 50), shift)
        # Horns sweep toward the back of the sheep
        if sheep.facing == 1:   # head right, back is left → horns sweep left
            hbase_x = hx + int(1*s)
            sweep   = -1
        else:                   # head left, back is right → horns sweep right
            hbase_x = hx + head_w - int(3*s)
            sweep   = 1

        if horn_type == "single_curved":
            pygame.draw.rect(screen, horn_color,
                             (hbase_x, hy - int(5*s), max(1, int(2*s)), int(5*s)))
            pygame.draw.rect(screen, horn_color,
                             (hbase_x + sweep * int(3*s), hy - int(5*s), int(3*s), max(1, int(2*s))))

        elif horn_type == "double_curved":
            for ox in [0, int(3*s)]:
                pygame.draw.rect(screen, horn_color,
                                 (hbase_x + ox, hy - int(5*s), max(1, int(2*s)), int(5*s)))
            pygame.draw.rect(screen, horn_color,
                             (hbase_x + sweep * int(3*s), hy - int(5*s), int(5*s), max(1, int(2*s))))

        elif horn_type == "spiral":
            sh = int(7*s)
            sw = int(4*s)
            # Shaft up
            pygame.draw.rect(screen, horn_color, (hbase_x, hy - sh, max(1, int(2*s)), sh))
            # Backward sweep at top
            pygame.draw.rect(screen, horn_color, (hbase_x + sweep * sw, hy - sh, sw, max(1, int(2*s))))
            # Curl down
            pygame.draw.rect(screen, horn_color,
                             (hbase_x + sweep * sw, hy - int(5*s), max(1, int(2*s)), int(3*s)))
            # Inward tip
            pygame.draw.rect(screen, horn_color,
                             (hbase_x + sweep * int(2*s), hy - int(3*s), int(3*s), max(1, int(2*s))))

    if getattr(sheep, 'tamed', False):
        pygame.draw.circle(screen, (255, 80, 120), (sx + W // 2, sy - 10), 4)

    if sheep.being_harvested:
        if sheep._kill_timer > 0:
            progress = sheep._kill_timer / 0.5
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (220, 60, 60), (sx, sy - 7, int(W * progress), 4))
        elif sheep._harvest_time > 0:
            progress = sheep._harvest_time / sheep.HARVEST_TIME
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (100, 220, 100), (sx, sy - 7, int(W * progress), 4))

    if sheep.health < 3:
        pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 13, W, 3))
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 13, int(W * sheep.health / 3), 3))


def draw_goat(screen, sx, sy, goat):
    W, H = goat.W, goat.H
    traits   = getattr(goat, 'traits', {})
    shift    = traits.get("color_shift", (0, 0, 0))
    s        = traits.get("size", 1.0)
    gc       = traits.get("coat_color", "tan")
    pattern  = traits.get("coat_pattern", "solid")
    horn_type = traits.get("horn_type", "curved")
    ear_type  = traits.get("ear_type", "upright")
    beard     = traits.get("beard", "small")
    fiber     = traits.get("fiber", 0.0)
    is_female = traits.get("sex", "female") == "female"
    body_h   = H - int(8 * s)
    leg_y    = sy + body_h

    _GOAT_BASE = {"tan": (195, 180, 155), "white": (235, 232, 225),
                  "brown": (130, 90, 55),  "black": (45, 40, 35)}
    base_rgb  = _GOAT_BASE.get(gc, _GOAT_BASE["tan"])
    body_color = _tinted(base_rgb, shift)
    leg_color  = _tinted(tuple(max(0, c - 25) for c in base_rgb), shift)
    horn_color = _tinted((80, 65, 45), shift)
    ear_color  = _tinted(tuple(max(0, c - 18) for c in base_rgb), shift)

    # Legs
    for lx_off in [2, 6, 13, 17]:
        pygame.draw.rect(screen, leg_color,
                         (sx + int(lx_off * s), leg_y, max(1, int(3 * s)), int(8 * s)))

    # Fiber coat puff (Angora / Cashmere) — drawn behind body
    if fiber > 0.3:
        puff = max(1, int((fiber - 0.3) * 4 * s))
        puff_col = _tinted(tuple(min(255, c + 14) for c in base_rgb), shift)
        pygame.draw.rect(screen, puff_col, (sx - puff, sy - puff, W + puff * 2, body_h + puff))

    # Body
    pygame.draw.rect(screen, body_color, (sx, sy, W, body_h))

    # Coat patterns
    if pattern == "chamoisee":
        stripe = _tinted(tuple(max(0, c - 50) for c in base_rgb), shift)
        pygame.draw.rect(screen, stripe, (sx, sy, W, max(1, int(2 * s))))
    elif pattern == "broken":
        patch = _tinted(tuple(max(0, c - 65) for c in base_rgb), shift)
        pygame.draw.rect(screen, patch, (sx + int(3*s), sy + int(2*s), int(9*s), int(5*s)))
    elif pattern == "sundgau":
        accent = _tinted(tuple(min(255, c + 80) for c in base_rgb), shift)
        pygame.draw.rect(screen, accent,
                         (sx + int(2*s), sy + body_h - int(3*s), W - int(4*s), int(3*s)))

    # Head
    head_w, head_h = int(9 * s), int(9 * s)
    head_color = _tinted(tuple(max(0, c - 12) for c in base_rgb), shift)
    hx = (sx + W - int(2 * s)) if goat.facing == 1 else (sx - head_w + int(2 * s))
    hy = sy - int(2 * s)
    pygame.draw.rect(screen, head_color, (hx, hy, head_w, head_h))

    # Ears
    if ear_type == "drooping":
        pygame.draw.rect(screen, ear_color, (hx - int(2*s), hy + int(1*s), int(3*s), int(8*s)))
        pygame.draw.rect(screen, ear_color, (hx + head_w - int(1*s), hy + int(1*s), int(3*s), int(7*s)))
    elif ear_type == "upright":
        pygame.draw.rect(screen, ear_color, (hx + int(1*s), hy - int(4*s), max(1, int(2*s)), int(4*s)))
        pygame.draw.rect(screen, ear_color, (hx + int(5*s), hy - int(3*s), max(1, int(2*s)), int(3*s)))
    else:  # gopher — tiny nubs
        pygame.draw.rect(screen, ear_color, (hx + int(1*s), hy, max(1, int(2*s)), max(1, int(2*s))))
        pygame.draw.rect(screen, ear_color, (hx + int(5*s), hy, max(1, int(2*s)), max(1, int(2*s))))

    # Horns
    if horn_type != "polled":
        if horn_type == "scurred":
            sh = int(2 * s)
        elif horn_type == "straight":
            sh = int(7 * s)
        else:  # curved
            sh = int(5 * s)

        if goat.facing == 1:
            pygame.draw.rect(screen, horn_color, (hx + int(1*s), hy - sh, max(1, int(2*s)), sh))
            pygame.draw.rect(screen, horn_color, (hx + int(5*s), hy - sh - int(1*s), max(1, int(2*s)), sh + int(1*s)))
            if horn_type == "curved":
                pygame.draw.rect(screen, horn_color, (hx - int(1*s), hy - sh, int(3*s), max(1, int(2*s))))
                pygame.draw.rect(screen, horn_color, (hx + int(3*s), hy - sh - int(1*s), int(3*s), max(1, int(2*s))))
        else:
            pygame.draw.rect(screen, horn_color, (hx + head_w - int(3*s), hy - sh, max(1, int(2*s)), sh))
            pygame.draw.rect(screen, horn_color, (hx + head_w - int(7*s), hy - sh - int(1*s), max(1, int(2*s)), sh + int(1*s)))
            if horn_type == "curved":
                pygame.draw.rect(screen, horn_color, (hx + head_w - int(2*s), hy - sh, int(3*s), max(1, int(2*s))))
                pygame.draw.rect(screen, horn_color, (hx + head_w - int(6*s), hy - sh - int(1*s), int(3*s), max(1, int(2*s))))

    # Beard
    if beard != "none":
        beard_len = int(7 * s) if beard == "full" else int(4 * s)
        beard_x   = (hx + int(1 * s)) if goat.facing == 1 else (hx + head_w - int(3 * s))
        pygame.draw.rect(screen, _tinted((155, 140, 115), shift),
                         (beard_x, hy + head_h, max(1, int(2 * s)), beard_len))

    # Eye
    eye_x = (hx + head_w - int(3 * s)) if goat.facing == 1 else (hx + max(1, int(1 * s)))
    pygame.draw.rect(screen, (20, 12, 5), (eye_x, hy + int(3 * s), 2, 2))

    # Udder (females only)
    if is_female:
        udder_col = (235, 225, 205) if goat.has_milk else (200, 190, 175)
        pygame.draw.rect(screen, udder_col,
                         (sx + W // 2 - int(3 * s), leg_y - int(3 * s), int(6 * s), int(3 * s)))

    if getattr(goat, 'tamed', False):
        pygame.draw.circle(screen, (255, 80, 120), (sx + W // 2, sy - 10), 4)

    if goat.being_harvested:
        if goat._kill_timer > 0:
            progress = goat._kill_timer / 0.5
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (220, 60, 60), (sx, sy - 7, int(W * progress), 4))
        elif goat._harvest_time > 0:
            progress = goat._harvest_time / goat.HARVEST_TIME
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (80, 160, 220), (sx, sy - 7, int(W * progress), 4))

    if goat.health < 3:
        pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 13, W, 3))
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 13, int(W * goat.health / 3), 3))


def _draw_milking_overlay(screen, sx, sy, cow_w, m):
    """Milking mini-game panel drawn above the cow in screen space."""
    PANEL_W, PANEL_H = 112, 68
    px = sx + cow_w // 2 - PANEL_W // 2
    py = sy - PANEL_H - 10

    # Background + border
    pygame.draw.rect(screen, (22, 17, 14), (px, py, PANEL_W, PANEL_H))
    pygame.draw.rect(screen, (75, 58, 44), (px, py, PANEL_W, PANEL_H), 2)

    # Progress bar (hits out of 4)
    bar_x, bar_y = px + 8, py + 8
    bar_w = PANEL_W - 16
    pygame.draw.rect(screen, (45, 36, 30), (bar_x, bar_y, bar_w, 7))
    filled = int(bar_w * m["hits"] / 4)
    if filled > 0:
        pygame.draw.rect(screen, (65, 195, 100), (bar_x, bar_y, filled, 7))
    pygame.draw.rect(screen, (80, 65, 50), (bar_x, bar_y, bar_w, 7), 1)

    # 4 teats — each is a lobe + hanging stem
    teat_xs = [px + 18, px + 40, px + 72, px + 94]
    lobe_y  = py + 28   # top of lobe
    lobe_w, lobe_h = 10, 8

    for i, tx in enumerate(teat_xs):
        is_active = (i == m["teat"])
        phase     = m["phase"] if is_active else "idle"

        if phase == "hit":
            lobe_col = (75, 210, 95)
            stem_col = (50, 160, 70)
            stem_h   = 18
        elif phase == "miss":
            lobe_col = (210, 65, 55)
            stem_col = (165, 50, 42)
            stem_h   = 10
        elif phase == "open":
            lobe_col = (240, 120, 150)
            stem_col = (195, 80, 108)
            stem_h   = 20
        else:
            lobe_col = (110, 72, 82)
            stem_col = (82, 52, 60)
            stem_h   = 9

        # Lobe (udder quarter)
        pygame.draw.rect(screen, lobe_col, (tx - lobe_w // 2, lobe_y, lobe_w, lobe_h))
        # Stem (the teat itself, hanging down)
        pygame.draw.rect(screen, stem_col, (tx - 3, lobe_y + lobe_h - 1, 6, stem_h))
        # Rounded tip
        pygame.draw.rect(screen, stem_col, (tx - 4, lobe_y + lobe_h + stem_h - 4, 8, 4))

    # SPACE prompt — pulses when a teat is open
    if m["phase"] == "open":
        prompt_col = (200, 175, 140)
    else:
        prompt_col = (85, 68, 55)
    # Draw a small square "key" icon for SPACE
    key_x, key_y = px + PANEL_W // 2 - 18, py + PANEL_H - 14
    pygame.draw.rect(screen, prompt_col, (key_x, key_y, 36, 9), 1)
    # Fill 3 small dashes inside to represent spacebar label
    for dx in [-8, 0, 8]:
        pygame.draw.rect(screen, prompt_col, (key_x + 18 + dx - 2, key_y + 3, 4, 3))


def draw_cow(screen, sx, sy, cow):
    W, H = cow.W, cow.H
    traits = getattr(cow, 'traits', {})
    shift       = traits.get("color_shift", (0, 0, 0))
    s           = traits.get("size", 1.0)
    base_coat   = traits.get("coat_color", (140, 85, 45))
    hide        = traits.get("hide", "solid")
    horn_length = traits.get("horn_length", 0.0)  # 0.0=polled, 1.0=max Longhorn
    hair_length = traits.get("hair_length", 0.0)  # 0.0=bare, 1.0=max shaggy
    is_male     = traits.get("sex", "female") == "male"
    body_h = H - int(8 * s)
    leg_y  = sy + body_h

    body_color   = _tinted(base_coat, shift)
    fringe_color = _tinted(tuple(max(0, c - 25) for c in base_coat), shift)
    horn_color   = _tinted((90, 75, 50), shift)
    leg_color    = _tinted(tuple(max(0, c - 55) for c in base_coat), shift)

    has_hair   = hair_length > 0.15
    fringe_len = max(1, int(hair_length * 6 * s))
    outline_px = max(1, int(hair_length * 3 * s))

    # Legs
    for lx_off in [2, 8, 18, 24]:
        pygame.draw.rect(screen, leg_color,
                         (sx + int(lx_off * s), leg_y, max(1, int(4 * s)), int(8 * s)))

    # Hair: shaggy puff outline behind body
    if has_hair:
        pygame.draw.rect(screen, fringe_color,
                         (sx - outline_px, sy - outline_px, W + outline_px * 2, body_h + outline_px))

    # Body
    pygame.draw.rect(screen, body_color, (sx, sy, W, body_h))

    # Hide patterns
    if hide == "spotted":
        patch = _tinted(tuple(max(0, c - 85) for c in base_coat), shift)
        pygame.draw.rect(screen, patch, (sx + int(8 * s), sy + int(2 * s), int(10 * s), int(5 * s)))
        pygame.draw.rect(screen, patch, (sx + int(20 * s), sy + int(5 * s), int(6 * s), int(4 * s)))
    elif hide == "belted":
        pygame.draw.rect(screen, _tinted((240, 235, 225), shift),
                         (sx + int(W * 0.3), sy, int(W * 0.38), body_h))
    elif hide == "piebald":
        patch = _tinted((28, 18, 8) if base_coat[0] > 140 else (230, 225, 220), shift)
        pygame.draw.rect(screen, patch, (sx + int(4 * s), sy + int(1 * s), int(8 * s), int(7 * s)))
        pygame.draw.rect(screen, patch, (sx + int(16 * s), sy + int(3 * s), int(9 * s), int(8 * s)))
        pygame.draw.rect(screen, patch, (sx + int(2 * s), sy + int(9 * s), int(6 * s), int(3 * s)))

    # Hair: fringe skirt hanging below body over leg tops
    if has_hair:
        for fx in range(sx + int(2*s), sx + W - int(2*s), max(1, int(4*s))):
            pygame.draw.rect(screen, fringe_color, (fx, leg_y, max(1, int(2*s)), fringe_len))

    # Head
    head_w, head_h = int(11 * s), int(11 * s)
    hx = (sx + W - int(3 * s)) if cow.facing == 1 else (sx - head_w + int(3 * s))
    hy = sy - int(2 * s)

    # Hair: puff outline behind head
    if has_hair:
        pygame.draw.rect(screen, fringe_color,
                         (hx - outline_px, hy - outline_px, head_w + outline_px * 2, head_h + outline_px))

    pygame.draw.rect(screen, body_color, (hx, hy, head_w, head_h))

    # Bull: raised poll crest at top of head
    if is_male:
        crest_color = _tinted(tuple(max(0, c - 15) for c in base_coat), shift)
        pygame.draw.rect(screen, crest_color,
                         (hx + int(3*s), hy - int(3*s), max(1, int(5*s)), int(3*s)))

    # Hair: forehead fringe hanging down over face
    if has_hair:
        for fx in range(hx + int(1*s), hx + head_w - int(1*s), max(1, int(3*s))):
            pygame.draw.rect(screen, fringe_color, (fx, hy, max(1, int(2*s)), fringe_len))

    # Snout and eye
    snout_x = (hx + head_w - int(4 * s)) if cow.facing == 1 else hx
    pygame.draw.rect(screen, _tinted((190, 130, 100), shift),
                     (snout_x, hy + int(6 * s), int(4 * s), int(4 * s)))
    eye_x = (hx + head_w - int(4 * s)) if cow.facing == 1 else (hx + max(1, int(1 * s)))
    pygame.draw.rect(screen, (20, 10, 5), (eye_x, hy + int(2 * s), 2, 2))

    # Horns — continuous scaling driven by horn_length (0.0=polled, 1.0=max Longhorn sweep).
    # shaft_h scales linearly; horizontal spread only opens past 0.25 and drives the tip height.
    if horn_length > 0.05:
        shaft_h = max(1, int(horn_length * 8 * s))
        spread  = int(max(0, (horn_length - 0.25) * 18 * s / 0.75))
        tip_h   = max(1, int(spread * 0.35)) if spread > 2 else 0
        base_y  = hy - shaft_h

        pygame.draw.rect(screen, horn_color, (hx + int(1*s), base_y, max(1, int(2*s)), shaft_h))
        if spread:
            pygame.draw.rect(screen, horn_color,
                             (hx + int(1*s) - spread, base_y, spread, max(1, int(2*s))))
            if tip_h:
                pygame.draw.rect(screen, horn_color,
                                 (hx + int(1*s) - spread, base_y - tip_h + int(2*s), max(1, int(2*s)), tip_h))

        pygame.draw.rect(screen, horn_color, (hx + int(7*s), base_y, max(1, int(2*s)), shaft_h))
        if spread:
            pygame.draw.rect(screen, horn_color,
                             (hx + int(7*s), base_y, spread + int(2*s), max(1, int(2*s))))
            if tip_h:
                pygame.draw.rect(screen, horn_color,
                                 (hx + int(7*s) + spread, base_y - tip_h + int(2*s), max(1, int(2*s)), tip_h))

    # Udder — females only
    if not is_male:
        udder_x = sx + W // 2 - int(4 * s)
        udder_color = (220, 180, 180) if cow.has_milk else (185, 150, 150)
        pygame.draw.rect(screen, udder_color,
                         (udder_x, leg_y - int(3 * s), int(8 * s), int(3 * s)))

    if getattr(cow, 'tamed', False):
        pygame.draw.circle(screen, (255, 80, 120), (sx + W // 2, sy - 10), 4)

    if cow.being_harvested:
        if cow._kill_timer > 0:
            progress = cow._kill_timer / 0.5
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (220, 60, 60), (sx, sy - 7, int(W * progress), 4))
        elif cow._harvest_time > 0:
            progress = cow._harvest_time / cow.HARVEST_TIME
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (80, 160, 220), (sx, sy - 7, int(W * progress), 4))

    if cow.health < 3:
        pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 13, W, 3))
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 13, int(W * cow.health / 3), 3))

    # Milking mini-game overlay
    m = getattr(cow, '_milking', None)
    if m is not None:
        _draw_milking_overlay(screen, sx, sy, W, m)


def draw_chicken(screen, sx, sy, chicken):
    W, H = chicken.W, chicken.H
    traits   = getattr(chicken, 'traits', {})
    shift    = traits.get("color_shift", (0, 0, 0))
    s        = traits.get("size", 1.0)
    pc       = traits.get("plumage", "white")
    pattern  = traits.get("pattern", "solid")
    comb_type = traits.get("comb_type", "single")
    leg_type  = traits.get("leg_type", "yellow")
    feath     = traits.get("feather_density", 0.0)
    is_hen    = traits.get("sex", "female") == "female"
    egg_tint  = traits.get("egg_tint", (245, 235, 200))

    _PLUMAGE_BASE = {"white": (235, 235, 210), "yellow": (230, 210, 130),
                     "brown": (175, 130, 80),  "black": (38, 34, 30)}
    _LEG_COLORS   = {"yellow": (220, 160, 30), "white": (215, 208, 188),
                     "dark":   (65, 50, 35),   "feathered": (220, 160, 30)}
    base_rgb   = _PLUMAGE_BASE.get(pc, _PLUMAGE_BASE["white"])
    body_color = _tinted(base_rgb, shift)
    leg_color  = _LEG_COLORS.get(leg_type, _LEG_COLORS["yellow"])

    # Legs (+ feathered leg fluff for Silkie/Brahma/Barbu)
    for lx_off in [4, 11]:
        lx = sx + int(lx_off * s)
        pygame.draw.rect(screen, leg_color, (lx, sy + H - int(6 * s), max(1, int(2 * s)), int(6 * s)))
        if leg_type == "feathered":
            fluff = _tinted(tuple(min(255, c + 28) for c in base_rgb), shift)
            pygame.draw.rect(screen, fluff, (lx - int(1*s), sy + H - int(6*s), int(4*s), int(3*s)))

    # Rooster tail feathers — long rects behind body
    if not is_hen:
        tail_col = _tinted(tuple(max(0, c - 22) for c in base_rgb), shift)
        if chicken.facing == 1:
            pygame.draw.rect(screen, tail_col, (sx - int(4*s), sy + int(1*s), int(4*s), int(7*s)))
        else:
            pygame.draw.rect(screen, tail_col, (sx + W, sy + int(1*s), int(4*s), int(7*s)))

    # Feather density puff (Orpington / Silkie / Brahma)
    body_rect = (sx + max(1, int(1*s)), sy + int(2*s), W - int(4*s), H - int(8*s))
    if feath > 0.3:
        puff = max(1, int((feath - 0.3) * 5 * s))
        puff_col = _tinted(tuple(min(255, c + 14) for c in base_rgb), shift)
        pygame.draw.ellipse(screen, puff_col,
                            (body_rect[0] - puff, body_rect[1] - puff,
                             body_rect[2] + puff * 2, body_rect[3] + puff * 2))

    # Body
    pygame.draw.ellipse(screen, body_color, body_rect)

    # Feather patterns
    if pattern == "barred":
        stripe = _tinted(tuple(max(0, c - 65) for c in base_rgb), shift)
        for by in range(body_rect[1] + int(2*s), body_rect[1] + body_rect[3], int(4*s)):
            pygame.draw.rect(screen, stripe, (body_rect[0] + 1, by, body_rect[2] - 2, max(1, int(2*s))))
    elif pattern == "laced":
        lace = _tinted(tuple(max(0, c - 50) for c in base_rgb), shift)
        pygame.draw.ellipse(screen, lace, body_rect, max(1, int(2*s)))
    elif pattern == "speckled":
        spot = _tinted(tuple(max(0, c - 70) for c in base_rgb), shift)
        for ox, oy in [(3, 3), (7, 5), (4, 8), (10, 3), (2, 6), (8, 8)]:
            pygame.draw.rect(screen, spot,
                             (sx + int(ox*s), sy + int(oy*s) + int(2*s), max(1, int(2*s)), max(1, int(2*s))))

    # Head
    head_w, head_h = int(8 * s), int(8 * s)
    hx = (sx + W - int(4 * s)) if chicken.facing == 1 else (sx - head_w + int(4 * s))
    hy = sy - int(2 * s)
    pygame.draw.ellipse(screen, body_color, (hx, hy, head_w, head_h))

    # Comb — larger on roosters
    comb_col = (220, 50, 50)
    comb_h   = int(3 * s) if is_hen else int(5 * s)
    if comb_type == "single":
        pygame.draw.rect(screen, comb_col, (hx + int(2*s), hy - comb_h, int(4*s), comb_h))
    elif comb_type == "rose":
        pygame.draw.rect(screen, comb_col, (hx + int(1*s), hy - max(1, int(2*s)), int(6*s), max(1, int(2*s))))
    elif comb_type == "pea":
        for cx in [int(1*s), int(3*s), int(5*s)]:
            pygame.draw.rect(screen, comb_col, (hx + cx, hy - comb_h + int(1*s), max(1, int(2*s)), comb_h - int(1*s)))
    else:  # walnut
        pygame.draw.rect(screen, comb_col, (hx + int(2*s), hy - max(1, int(2*s)), int(4*s), max(1, int(2*s))))

    # Wattle — larger and visible on roosters
    wattle_x = (hx + int(1*s)) if chicken.facing == 1 else (hx + head_w - int(3*s))
    wattle_h = int(2*s) if is_hen else int(4*s)
    pygame.draw.rect(screen, (200, 40, 40), (wattle_x, hy + head_h - int(1*s), int(2*s), wattle_h))

    # Beak and eye
    beak_x = (hx + head_w - max(1, int(1*s))) if chicken.facing == 1 else (hx - int(3*s))
    pygame.draw.rect(screen, leg_color, (beak_x, hy + int(3*s), int(3*s), int(2*s)))
    eye_x = (hx + head_w - int(3*s)) if chicken.facing == 1 else (hx + max(1, int(1*s)))
    pygame.draw.rect(screen, (20, 20, 20), (eye_x, hy + int(2*s), 2, 2))

    # Egg (hens only)
    if chicken.has_egg and is_hen:
        pygame.draw.ellipse(screen, egg_tint,
                            (sx + W // 2 - int(3*s), sy + H - int(10*s), int(6*s), int(5*s)))

    if getattr(chicken, 'tamed', False):
        pygame.draw.circle(screen, (255, 80, 120), (sx + W // 2, sy - 10), 4)

    if chicken.being_harvested:
        if chicken._kill_timer > 0:
            progress = chicken._kill_timer / 0.5
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (220, 60, 60), (sx, sy - 7, int(W * progress), 4))
        elif chicken._harvest_time > 0:
            progress = chicken._harvest_time / chicken.HARVEST_TIME
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (245, 220, 100), (sx, sy - 7, int(W * progress), 4))

    if chicken.health < 3:
        pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 13, W, 3))
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 13, int(W * chicken.health / 3), 3))


def draw_capybara(screen, sx, sy, cap):
    W, H = cap.W, cap.H
    shift = cap.traits.get("color_shift", (0, 0, 0))
    s     = cap.traits.get("size", 1.0)

    body_color = _tinted((118, 88, 55), shift)
    leg_color  = _tinted((90, 65, 38), shift)
    head_color = _tinted((105, 78, 48), shift)
    nose_color = _tinted((80, 55, 32), shift)
    ear_color  = _tinted((148, 108, 75), shift)

    body_h = H - int(5 * s)
    leg_h  = int(5 * s)
    leg_y  = sy + body_h

    # Legs — short stubby pairs
    for lx_off in [3, 9, 21, 27]:
        pygame.draw.rect(screen, leg_color,
                         (sx + int(lx_off * s), leg_y, max(1, int(3 * s)), leg_h))

    # Body — barrel-shaped, slightly rounded via two rects
    pygame.draw.rect(screen, body_color, (sx, sy, W, body_h))
    belly = _tinted((138, 105, 68), shift)
    pygame.draw.rect(screen, belly,
                     (sx + int(4 * s), sy + int(4 * s), W - int(8 * s), body_h - int(6 * s)))

    # Head — blunt rectangle (distinctive capybara feature)
    head_w = int(13 * s)
    head_h = int(11 * s)
    hx = (sx + W - int(3 * s)) if cap.facing == 1 else (sx - head_w + int(3 * s))
    hy = sy + int(1 * s)
    pygame.draw.rect(screen, head_color, (hx, hy, head_w, head_h))

    # Nose/muzzle — darker block at snout end
    if cap.facing == 1:
        pygame.draw.rect(screen, nose_color,
                         (hx + head_w - int(4 * s), hy + int(3 * s), int(4 * s), int(5 * s)))
    else:
        pygame.draw.rect(screen, nose_color,
                         (hx, hy + int(3 * s), int(4 * s), int(5 * s)))

    # Ears — small round nubs on top of head
    ear_r = max(1, int(2 * s))
    ear_y = hy - ear_r
    pygame.draw.circle(screen, ear_color, (hx + int(3 * s), ear_y), ear_r)
    pygame.draw.circle(screen, ear_color, (hx + int(8 * s), ear_y), ear_r)

    # Eye — tiny dark dot
    eye_color = (25, 18, 10)
    eye_x = (hx + int(7 * s)) if cap.facing == 1 else (hx + int(5 * s))
    pygame.draw.rect(screen, eye_color, (eye_x, hy + int(2 * s), max(1, int(2 * s)), max(1, int(2 * s))))


_LLAMA_COAT = {
    "white": (235, 230, 220),
    "fawn":  (200, 165, 115),
    "brown": (135,  90,  55),
    "black": ( 50,  45,  42),
    "grey":  (165, 155, 145),
}
_LLAMA_SHORN = {
    "white": (180, 165, 140),
    "fawn":  (155, 125,  85),
    "brown": (105,  70,  45),
    "black": ( 42,  38,  34),
    "grey":  (130, 122, 115),
}


def draw_llama(screen, sx, sy, llama):
    W, H = llama.W, llama.H
    traits      = getattr(llama, 'traits', {})
    shift       = traits.get("color_shift", (0, 0, 0))
    s           = traits.get("size", 1.0)
    coat_color  = traits.get("coat_color", "fawn")
    pattern     = traits.get("coat_pattern", "solid")
    ear_type    = traits.get("ear_type", "banana")
    fiber_len   = traits.get("fiber_length", 0.5)

    base   = _LLAMA_COAT.get(coat_color, _LLAMA_COAT["fawn"])
    shorn  = _LLAMA_SHORN.get(coat_color, _LLAMA_SHORN["fawn"])
    active = base if llama.has_wool else shorn

    # Llama body — taller, narrower than sheep. Body sits at upper 60% of H.
    body_h = int(H * 0.55)
    body_y = sy + int(H * 0.15)
    leg_top = body_y + body_h
    leg_h   = sy + H - leg_top

    # Fluff outline behind body when unshorn and long fibre
    if llama.has_wool and fiber_len > 0.4:
        puff = max(1, int((fiber_len - 0.35) * 5 * s))
        puff_col = _tinted(tuple(min(255, c + 12) for c in base), shift)
        pygame.draw.rect(screen, puff_col,
                         (sx - puff, body_y - puff, W + puff * 2, body_h + puff))

    # Legs — long, four of them
    leg_color = _tinted(tuple(max(0, c - 35) for c in active), shift)
    leg_w = max(2, int(3 * s))
    for lx_off in (int(2*s), int(8*s), W - int(8*s) - leg_w, W - int(2*s) - leg_w):
        pygame.draw.rect(screen, leg_color, (sx + lx_off, leg_top, leg_w, leg_h))

    # Body
    body_color = _tinted(active, shift)
    pygame.draw.rect(screen, body_color, (sx, body_y, W, body_h))

    # Pattern markings (only when unshorn)
    if llama.has_wool:
        if pattern == "tipped":
            tip = _tinted(tuple(max(0, c - 50) for c in base), shift)
            pygame.draw.rect(screen, tip, (sx, body_y, W, int(body_h * 0.3)))
        elif pattern == "spotted":
            spot = _tinted(tuple(max(0, c - 70) for c in base), shift)
            pygame.draw.rect(screen, spot, (sx + int(4*s),  body_y + int(2*s), int(5*s), int(4*s)))
            pygame.draw.rect(screen, spot, (sx + int(13*s), body_y + int(4*s), int(5*s), int(4*s)))
        elif pattern == "appaloosa":
            spot = _tinted(tuple(max(0, c - 70) for c in base), shift)
            for ox, oy in ((3, 2), (10, 5), (17, 3), (8, 10), (16, 9)):
                px = sx + int(ox * s)
                py = body_y + int(oy * s)
                pygame.draw.rect(screen, spot, (px, py, max(1, int(2*s)), max(1, int(2*s))))

    # Neck — long upright, sloping forward
    neck_w = int(5 * s)
    neck_h = int(H * 0.30)
    if llama.facing == 1:
        neck_x = sx + W - neck_w - int(1 * s)
    else:
        neck_x = sx + int(1 * s)
    neck_y = body_y - neck_h + int(2 * s)
    neck_color = _tinted(active, shift)
    pygame.draw.rect(screen, neck_color, (neck_x, neck_y, neck_w, neck_h))

    # Head — square muzzle perched atop the neck
    head_w = int(6 * s)
    head_h = int(6 * s)
    if llama.facing == 1:
        hx = neck_x + neck_w - int(1 * s)
    else:
        hx = neck_x - head_w + int(1 * s)
    hy = neck_y - head_h + int(1 * s)
    face_color = _tinted(tuple(max(0, c - 25) for c in active), shift)
    pygame.draw.rect(screen, face_color, (hx, hy, head_w, head_h))

    # Muzzle stub forward
    muzzle_w = int(3 * s)
    muzzle_h = int(3 * s)
    mx = (hx + head_w - int(1 * s)) if llama.facing == 1 else (hx - muzzle_w + int(1 * s))
    my = hy + int(head_h - muzzle_h - 1)
    pygame.draw.rect(screen, face_color, (mx, my, muzzle_w, muzzle_h))

    # Ears — banana ears are the llama signature
    ear_color = _tinted(tuple(max(0, c - 18) for c in face_color), shift)
    if ear_type == "banana":
        eh = int(5 * s)
        ew = max(1, int(2 * s))
        pygame.draw.rect(screen, ear_color, (hx + int(1*s), hy - eh, ew, eh))
        pygame.draw.rect(screen, ear_color, (hx + head_w - int(2*s), hy - eh, ew, eh))
        # Curved tip — small inward nub
        pygame.draw.rect(screen, ear_color, (hx + int(2*s), hy - eh, max(1, int(s)), max(1, int(s))))
        pygame.draw.rect(screen, ear_color, (hx + head_w - int(3*s), hy - eh, max(1, int(s)), max(1, int(s))))
    elif ear_type == "upright":
        pygame.draw.rect(screen, ear_color, (hx + int(1*s), hy - int(3*s), max(1, int(2*s)), int(3*s)))
        pygame.draw.rect(screen, ear_color, (hx + head_w - int(3*s), hy - int(3*s), max(1, int(2*s)), int(3*s)))
    else:  # short
        pygame.draw.rect(screen, ear_color, (hx + int(1*s), hy - int(2*s), max(1, int(2*s)), int(2*s)))
        pygame.draw.rect(screen, ear_color, (hx + head_w - int(3*s), hy - int(2*s), max(1, int(2*s)), int(2*s)))

    # Eye
    eye_x = (hx + head_w - int(2 * s)) if llama.facing == 1 else (hx + max(1, int(1 * s)))
    pygame.draw.rect(screen, (25, 22, 18), (eye_x, hy + int(2 * s), 2, 2))

    # Tail — short tuft pointing away from head
    tail_color = _tinted(active, shift)
    if llama.facing == 1:
        tx = sx - int(2 * s)
    else:
        tx = sx + W
    pygame.draw.rect(screen, tail_color, (tx, body_y + int(1 * s), int(3 * s), int(4 * s)))

    if getattr(llama, 'tamed', False):
        pygame.draw.circle(screen, (255, 80, 120), (sx + W // 2, sy - 12), 4)

    if llama.being_harvested:
        if llama._kill_timer > 0:
            progress = llama._kill_timer / 0.5
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (220, 60, 60), (sx, sy - 7, int(W * progress), 4))
        elif llama._harvest_time > 0:
            progress = llama._harvest_time / llama.HARVEST_TIME
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (100, 220, 100), (sx, sy - 7, int(W * progress), 4))

    if llama.health < 3:
        pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 13, W, 3))
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 13, int(W * llama.health / 3), 3))


_YAK_COAT = {
    "black":   ( 45,  40,  38),
    "brown":   (110,  75,  50),
    "white":   (225, 220, 210),
    "piebald": ( 60,  55,  50),   # base; piebald patches drawn on top
    "golden":  (200, 165,  85),
}
_YAK_SHORN = {
    "black":   ( 55,  50,  46),
    "brown":   ( 95,  68,  45),
    "white":   (180, 168, 150),
    "piebald": ( 70,  65,  60),
    "golden":  (165, 135,  70),
}
_YAK_SKIRT_HEIGHT = {"full": 0.65, "medium": 0.45, "short": 0.25}


def draw_yak(screen, sx, sy, yak):
    W, H = yak.W, yak.H
    traits     = getattr(yak, 'traits', {})
    shift      = traits.get("color_shift", (0, 0, 0))
    s          = traits.get("size", 1.0)
    coat_color = traits.get("coat_color", "black")
    horn_type  = traits.get("horn_type", "wide")
    skirt      = traits.get("skirt_length", "full")
    fiber_len  = traits.get("fiber_length", 0.6)

    base   = _YAK_COAT.get(coat_color, _YAK_COAT["black"])
    shorn  = _YAK_SHORN.get(coat_color, _YAK_SHORN["black"])
    active = base if yak.has_wool else shorn

    # Body — broad and low
    body_h = int(H * 0.55)
    body_y = sy + int(H * 0.18)
    leg_top = body_y + body_h
    leg_h   = sy + H - leg_top

    # Shaggy skirt — long body hair hanging over the legs (only when unshorn)
    if yak.has_wool:
        skirt_h = int(leg_h * _YAK_SKIRT_HEIGHT.get(skirt, 0.5))
        skirt_col = _tinted(tuple(max(0, c - 10) for c in base), shift)
        pygame.draw.rect(screen, skirt_col, (sx + int(1 * s), leg_top, W - int(2 * s), skirt_h))

    # Fluff outline behind body when long fibre
    if yak.has_wool and fiber_len > 0.4:
        puff = max(1, int((fiber_len - 0.35) * 5 * s))
        puff_col = _tinted(tuple(min(255, c + 10) for c in base), shift)
        pygame.draw.rect(screen, puff_col,
                         (sx - puff, body_y - puff, W + puff * 2, body_h + puff))

    # Legs — thick and stubby
    leg_color = _tinted(tuple(max(0, c - 30) for c in active), shift)
    leg_w = max(3, int(4 * s))
    for lx_off in (int(3*s), int(10*s), W - int(10*s) - leg_w, W - int(3*s) - leg_w):
        pygame.draw.rect(screen, leg_color, (sx + lx_off, leg_top, leg_w, leg_h))

    # Body
    body_color = _tinted(active, shift)
    pygame.draw.rect(screen, body_color, (sx, body_y, W, body_h))

    # Hump — characteristic yak shoulder hump, on the front-shoulder side
    hump_w = int(W * 0.35)
    hump_h = int(body_h * 0.45)
    if yak.facing == 1:
        hump_x = sx + W - hump_w - int(2 * s)
    else:
        hump_x = sx + int(2 * s)
    hump_y = body_y - hump_h + int(2 * s)
    hump_color = _tinted(tuple(max(0, c - 8) for c in base), shift) if yak.has_wool else body_color
    pygame.draw.rect(screen, hump_color, (hump_x, hump_y, hump_w, hump_h))

    # Piebald patches (only when unshorn)
    if yak.has_wool and coat_color == "piebald":
        patch = _tinted((220, 215, 205), shift)
        pygame.draw.rect(screen, patch, (sx + int(5*s),  body_y + int(2*s), int(8*s), int(5*s)))
        pygame.draw.rect(screen, patch, (sx + int(18*s), body_y + int(4*s), int(7*s), int(4*s)))

    # Head — broad, low-slung
    head_w = int(10 * s)
    head_h = int(9 * s)
    if yak.facing == 1:
        hx = sx + W - int(2 * s)
    else:
        hx = sx - head_w + int(2 * s)
    hy = body_y + int(body_h * 0.25)
    face_color = _tinted(tuple(max(0, c - 20) for c in active), shift)
    pygame.draw.rect(screen, face_color, (hx, hy, head_w, head_h))

    # Forehead tuft — shaggy fringe between horns
    if yak.has_wool:
        tuft_col = _tinted(tuple(max(0, c - 5) for c in base), shift)
        pygame.draw.rect(screen, tuft_col, (hx + int(2*s), hy - int(3*s), head_w - int(4*s), int(3*s)))

    # Horns — characteristic curved spread
    horn_color = _tinted((90, 78, 55), shift)
    if horn_type != "polled":
        if horn_type == "wide":
            # Long sweeping horns curving out and forward
            for side, sx_off in ((-1, int(1*s)), (1, head_w - int(2*s))):
                base_x = hx + sx_off
                pygame.draw.rect(screen, horn_color, (base_x, hy - int(2*s), max(1, int(2*s)), int(2*s)))
                pygame.draw.rect(screen, horn_color, (base_x + side * int(2*s), hy - int(4*s),
                                                       int(3*s), max(1, int(2*s))))
                pygame.draw.rect(screen, horn_color, (base_x + side * int(4*s), hy - int(6*s),
                                                       max(1, int(2*s)), int(3*s)))
        elif horn_type == "curved":
            for side, sx_off in ((-1, int(1*s)), (1, head_w - int(2*s))):
                base_x = hx + sx_off
                pygame.draw.rect(screen, horn_color, (base_x, hy - int(4*s), max(1, int(2*s)), int(4*s)))
                pygame.draw.rect(screen, horn_color, (base_x + side * int(2*s), hy - int(5*s),
                                                       int(2*s), max(1, int(2*s))))
        else:  # short
            for sx_off in (int(2*s), head_w - int(3*s)):
                pygame.draw.rect(screen, horn_color, (hx + sx_off, hy - int(2*s), max(1, int(2*s)), int(2*s)))

    # Eye
    eye_x = (hx + head_w - int(3 * s)) if yak.facing == 1 else (hx + max(1, int(1 * s)))
    pygame.draw.rect(screen, (20, 18, 14), (eye_x, hy + int(3 * s), 2, 2))

    # Tail tuft — opposite the head
    tail_color = _tinted(base if yak.has_wool else active, shift)
    if yak.facing == 1:
        tx = sx - int(3 * s)
    else:
        tx = sx + W
    pygame.draw.rect(screen, tail_color, (tx, body_y + int(2 * s), int(4 * s), int(7 * s)))

    if getattr(yak, 'tamed', False):
        pygame.draw.circle(screen, (255, 80, 120), (sx + W // 2, sy - 12), 4)

    if yak.being_harvested:
        if yak._kill_timer > 0:
            progress = yak._kill_timer / 0.5
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (220, 60, 60), (sx, sy - 7, int(W * progress), 4))
        elif yak._harvest_time > 0:
            progress = yak._harvest_time / yak.HARVEST_TIME
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (100, 220, 100), (sx, sy - 7, int(W * progress), 4))

    max_health = max(3, getattr(yak, 'health', 3))
    if yak.health < 4:
        pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 13, W, 3))
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 13, int(W * yak.health / max(4, max_health)), 3))


_PIG_BASE = {
    "pink":    (235, 175, 165),
    "black":   ( 45,  38,  35),
    "red":     (170,  90,  55),
    "white":   (235, 225, 215),
    "spotted": (220, 175, 160),
    "blonde":  (215, 190, 130),
}


def draw_pig(screen, sx, sy, pig):
    W, H = pig.W, pig.H
    traits  = getattr(pig, 'traits', {})
    shift   = traits.get("color_shift", (0, 0, 0))
    s       = traits.get("size", 1.0)
    color   = traits.get("coat_color", "pink")
    pattern = traits.get("coat_pattern", "solid")
    ear     = traits.get("ear_type", "upright")
    snout   = traits.get("snout_length", "medium")
    fat     = traits.get("fat", 1.0)

    base_rgb   = _PIG_BASE.get(color, _PIG_BASE["pink"])
    body_color = _tinted(base_rgb, shift)
    belly_col  = _tinted(tuple(min(255, c + 18) for c in base_rgb), shift)
    leg_color  = _tinted(tuple(max(0, c - 25) for c in base_rgb), shift)
    ear_color  = _tinted(tuple(max(0, c - 18) for c in base_rgb), shift)
    snout_color = _tinted(tuple(max(0, c - 8) for c in base_rgb), shift)

    body_h = H - int(6 * s)
    leg_y  = sy + body_h

    # Legs — short and stocky
    for lx_off in [2, 8, 16, 22]:
        pygame.draw.rect(screen, leg_color,
                         (sx + int(lx_off * s), leg_y, max(1, int(3 * s)), int(6 * s)))

    # Fat halo — extra girth for high-fat breeds (Mangalitsa)
    if fat > 1.2:
        bulge = max(1, int((fat - 1.2) * 5 * s))
        pygame.draw.rect(screen, body_color, (sx - bulge, sy + 1, W + bulge * 2, body_h))

    # Body — rounded rectangle look
    pygame.draw.rect(screen, body_color, (sx, sy, W, body_h))
    # Belly highlight
    pygame.draw.rect(screen, belly_col,
                     (sx + int(2 * s), sy + body_h - int(4 * s), W - int(4 * s), int(3 * s)))

    # Patterns
    if pattern == "belted":
        belt = _tinted((245, 240, 230), shift) if color != "white" else _tinted((40, 40, 40), shift)
        belt_w = int(W * 0.32)
        belt_x = sx + (W - belt_w) // 2
        pygame.draw.rect(screen, belt, (belt_x, sy, belt_w, body_h))
    elif pattern == "spotted":
        spot = _tinted(tuple(max(0, c - 55) for c in base_rgb), shift)
        pygame.draw.rect(screen, spot, (sx + int(4 * s), sy + int(2 * s), int(3 * s), int(3 * s)))
        pygame.draw.rect(screen, spot, (sx + int(11 * s), sy + int(4 * s), int(3 * s), int(3 * s)))
        pygame.draw.rect(screen, spot, (sx + int(17 * s), sy + int(2 * s), int(3 * s), int(3 * s)))
    elif pattern == "piebald":
        patch = _tinted((245, 235, 220), shift)
        pygame.draw.rect(screen, patch, (sx + int(3 * s), sy + int(1 * s), int(7 * s), int(5 * s)))
        pygame.draw.rect(screen, patch, (sx + int(14 * s), sy + int(3 * s), int(6 * s), int(4 * s)))

    # Curly Mangalitsa coat dots
    if color == "blonde" and pattern == "solid":
        curl = _tinted(tuple(min(255, c + 12) for c in base_rgb), shift)
        for dx_off in range(1, W - 1, max(2, int(3 * s))):
            pygame.draw.rect(screen, curl, (sx + dx_off, sy + 1, 1, 1))
            pygame.draw.rect(screen, curl, (sx + dx_off, sy + int(4 * s), 1, 1))

    # Head — at the front
    head_w = int(10 * s)
    head_h = int(9 * s)
    hx = (sx + W - int(2 * s)) if pig.facing == 1 else (sx - head_w + int(2 * s))
    hy = sy + int(1 * s)
    pygame.draw.rect(screen, _tinted(tuple(max(0, c - 10) for c in base_rgb), shift),
                     (hx, hy, head_w, head_h))

    # Snout — flat disk
    snout_w = {"short": int(3 * s), "medium": int(4 * s), "long": int(6 * s)}.get(snout, int(4 * s))
    snout_h = int(4 * s)
    sx_pos = (hx + head_w - 1) if pig.facing == 1 else (hx - snout_w + 1)
    pygame.draw.rect(screen, snout_color, (sx_pos, hy + int(3 * s), snout_w, snout_h))
    # Nostrils
    nx = sx_pos + (snout_w - 2 if pig.facing == 1 else 0)
    pygame.draw.rect(screen, (40, 25, 25), (nx, hy + int(4 * s), 1, 1))
    pygame.draw.rect(screen, (40, 25, 25), (nx, hy + int(5 * s), 1, 1))

    # Ears
    if ear == "upright":
        pygame.draw.rect(screen, ear_color, (hx + int(1 * s), hy - int(3 * s), max(1, int(2 * s)), int(3 * s)))
        pygame.draw.rect(screen, ear_color, (hx + int(6 * s), hy - int(3 * s), max(1, int(2 * s)), int(3 * s)))
    elif ear == "lop":
        pygame.draw.rect(screen, ear_color, (hx + int(1 * s), hy, max(1, int(2 * s)), int(5 * s)))
        pygame.draw.rect(screen, ear_color, (hx + int(6 * s), hy, max(1, int(2 * s)), int(5 * s)))
    else:  # semi_lop
        pygame.draw.rect(screen, ear_color, (hx + int(1 * s), hy - int(1 * s), max(1, int(2 * s)), int(4 * s)))
        pygame.draw.rect(screen, ear_color, (hx + int(6 * s), hy - int(1 * s), max(1, int(2 * s)), int(4 * s)))

    # Eye
    eye_x = (hx + head_w - int(3 * s)) if pig.facing == 1 else (hx + max(1, int(1 * s)))
    pygame.draw.rect(screen, (20, 12, 5), (eye_x, hy + int(3 * s), 2, 2))

    # Curly tail
    tail_x = (sx - int(2 * s)) if pig.facing == 1 else (sx + W)
    tail_col = _tinted(tuple(max(0, c - 18) for c in base_rgb), shift)
    pygame.draw.rect(screen, tail_col, (tail_x, sy + int(1 * s), max(1, int(2 * s)), max(1, int(2 * s))))
    pygame.draw.rect(screen, tail_col, (tail_x + (1 if pig.facing != 1 else -1), sy + int(3 * s), 1, 1))

    if getattr(pig, 'has_manure', False):
        pygame.draw.rect(screen, (85, 55, 30), (sx + W - int(3 * s), leg_y + int(1 * s), 2, 2))

    if getattr(pig, 'being_harvested', False):
        if getattr(pig, '_kill_timer', 0) > 0:
            progress = pig._kill_timer / 0.5
            pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 7, W, 4))
            pygame.draw.rect(screen, (220, 80, 80), (sx, sy - 7, int(W * progress), 4))

    max_health = max(3, getattr(pig, 'health', 3))
    if pig.health < 4:
        pygame.draw.rect(screen, (40, 40, 40), (sx, sy - 13, W, 3))
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 13, int(W * pig.health / max(4, max_health)), 3))
