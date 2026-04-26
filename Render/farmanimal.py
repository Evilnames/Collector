import pygame


def _tinted(base_color, shift):
    return tuple(max(0, min(255, int(base_color[i] + shift[i] * 255))) for i in range(3))


def draw_sheep(screen, sx, sy, sheep):
    W, H = sheep.W, sheep.H
    traits = getattr(sheep, 'traits', {})
    shift = traits.get("color_shift", (0, 0, 0))
    s = traits.get("size", 1.0)
    body_h = H - int(8 * s)
    leg_y = sy + body_h

    for lx_off in [2, 7, 14, 19]:
        pygame.draw.rect(screen, (80, 60, 40),
                         (sx + int(lx_off * s), leg_y, max(1, int(3 * s)), int(8 * s)))

    _WOOL_BASE = {"white": (220, 220, 220), "grey": (175, 175, 175),
                  "brown": (165, 115, 70),  "black": (50, 45, 42)}
    _WOOL_SHORN = {"white": (175, 140, 95), "grey": (145, 115, 80),
                   "brown": (130, 90, 55),  "black": (45, 38, 32)}
    wc = getattr(sheep, 'traits', {}).get("wool_color", "white")
    wool_base  = _WOOL_BASE.get(wc, _WOOL_BASE["white"])
    shorn_base = _WOOL_SHORN.get(wc, _WOOL_SHORN["white"])

    body_color = _tinted(wool_base if sheep.has_wool else shorn_base, shift)
    pygame.draw.rect(screen, body_color, (sx, sy, W, body_h))

    head_w, head_h = int(9 * s), int(9 * s)
    head_color = _tinted(
        tuple(max(0, c - 20) for c in wool_base) if sheep.has_wool
        else tuple(max(0, c - 20) for c in shorn_base), shift
    )
    hx = (sx + W - int(2 * s)) if sheep.facing == 1 else (sx - head_w + int(2 * s))
    hy = sy - max(1, int(1 * s))
    pygame.draw.rect(screen, head_color, (hx, hy, head_w, head_h))
    eye_x = (hx + head_w - int(3 * s)) if sheep.facing == 1 else (hx + max(1, int(1 * s)))
    pygame.draw.rect(screen, (30, 30, 30), (eye_x, hy + int(3 * s), 2, 2))

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
    traits = getattr(goat, 'traits', {})
    shift = traits.get("color_shift", (0, 0, 0))
    s = traits.get("size", 1.0)
    body_h = H - int(8 * s)
    leg_y = sy + body_h

    for lx_off in [2, 6, 13, 17]:
        pygame.draw.rect(screen, _tinted((90, 70, 50), shift),
                         (sx + int(lx_off * s), leg_y, max(1, int(3 * s)), int(8 * s)))

    _GOAT_BASE = {"tan": (195, 180, 155), "white": (235, 232, 225),
                  "brown": (130, 90, 55),  "black": (45, 40, 35)}
    gc = traits.get("coat_color", "tan")
    body_color = _tinted(_GOAT_BASE.get(gc, _GOAT_BASE["tan"]), shift)
    pygame.draw.rect(screen, body_color, (sx, sy, W, body_h))

    head_w, head_h = int(9 * s), int(9 * s)
    head_color = _tinted(tuple(max(0, c - 12) for c in _GOAT_BASE.get(gc, _GOAT_BASE["tan"])), shift)
    hx = (sx + W - int(2 * s)) if goat.facing == 1 else (sx - head_w + int(2 * s))
    hy = sy - int(2 * s)
    pygame.draw.rect(screen, head_color, (hx, hy, head_w, head_h))

    horn_color = _tinted((80, 65, 45), shift)
    if goat.facing == 1:
        pygame.draw.rect(screen, horn_color, (hx + int(1 * s), hy - int(4 * s), max(1, int(2 * s)), int(4 * s)))
        pygame.draw.rect(screen, horn_color, (hx + int(5 * s), hy - int(5 * s), max(1, int(2 * s)), int(5 * s)))
    else:
        pygame.draw.rect(screen, horn_color, (hx + head_w - int(3 * s), hy - int(4 * s), max(1, int(2 * s)), int(4 * s)))
        pygame.draw.rect(screen, horn_color, (hx + head_w - int(7 * s), hy - int(5 * s), max(1, int(2 * s)), int(5 * s)))

    beard_x = (hx + int(1 * s)) if goat.facing == 1 else (hx + head_w - int(3 * s))
    pygame.draw.rect(screen, _tinted((155, 140, 115), shift),
                     (beard_x, hy + head_h, max(1, int(2 * s)), max(1, int(4 * s))))

    eye_x = (hx + head_w - int(3 * s)) if goat.facing == 1 else (hx + max(1, int(1 * s)))
    pygame.draw.rect(screen, (20, 12, 5), (eye_x, hy + int(3 * s), 2, 2))

    if goat.has_milk:
        pygame.draw.rect(screen, (235, 225, 205),
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


def draw_cow(screen, sx, sy, cow):
    W, H = cow.W, cow.H
    traits = getattr(cow, 'traits', {})
    shift = traits.get("color_shift", (0, 0, 0))
    s = traits.get("size", 1.0)
    body_h = H - int(8 * s)
    leg_y = sy + body_h

    for lx_off in [2, 8, 18, 24]:
        pygame.draw.rect(screen, (60, 40, 30),
                         (sx + int(lx_off * s), leg_y, max(1, int(4 * s)), int(8 * s)))

    hide = traits.get("hide", "solid")
    body_color = _tinted((140, 85, 45), shift)
    pygame.draw.rect(screen, body_color, (sx, sy, W, body_h))
    if hide == "spotted":
        patch = _tinted((28, 18, 8), shift)
        pygame.draw.rect(screen, patch, (sx + int(8 * s), sy + int(2 * s), int(10 * s), int(5 * s)))
        pygame.draw.rect(screen, patch, (sx + int(20 * s), sy + int(5 * s), int(6 * s), int(4 * s)))
    elif hide == "belted":
        belt_x = sx + int(W * 0.3)
        belt_w = int(W * 0.38)
        pygame.draw.rect(screen, _tinted((240, 235, 225), shift), (belt_x, sy, belt_w, body_h))
    elif hide == "piebald":
        patch = _tinted((28, 18, 8), shift)
        pygame.draw.rect(screen, patch, (sx + int(4 * s), sy + int(1 * s), int(8 * s), int(7 * s)))
        pygame.draw.rect(screen, patch, (sx + int(16 * s), sy + int(3 * s), int(9 * s), int(8 * s)))
        pygame.draw.rect(screen, patch, (sx + int(2 * s), sy + int(9 * s), int(6 * s), int(3 * s)))

    head_w, head_h = int(11 * s), int(11 * s)
    hx = (sx + W - int(3 * s)) if cow.facing == 1 else (sx - head_w + int(3 * s))
    hy = sy - int(2 * s)
    head_color = _tinted((140, 85, 45), shift)
    pygame.draw.rect(screen, head_color, (hx, hy, head_w, head_h))
    snout_x = (hx + head_w - int(4 * s)) if cow.facing == 1 else hx
    pygame.draw.rect(screen, _tinted((190, 130, 100), shift),
                     (snout_x, hy + int(6 * s), int(4 * s), int(4 * s)))
    eye_x = (hx + head_w - int(4 * s)) if cow.facing == 1 else (hx + max(1, int(1 * s)))
    pygame.draw.rect(screen, (20, 10, 5), (eye_x, hy + int(2 * s), 2, 2))

    if cow.has_milk:
        udder_x = sx + W // 2 - int(4 * s)
        pygame.draw.rect(screen, (220, 180, 180),
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


def draw_chicken(screen, sx, sy, chicken):
    W, H = chicken.W, chicken.H
    traits = getattr(chicken, 'traits', {})
    shift = traits.get("color_shift", (0, 0, 0))
    s = traits.get("size", 1.0)

    for lx_off in [4, 11]:
        pygame.draw.rect(screen, (220, 160, 30),
                         (sx + int(lx_off * s), sy + H - int(6 * s), max(1, int(2 * s)), int(6 * s)))

    _PLUMAGE_BASE = {"white": (235, 235, 210), "yellow": (230, 210, 130),
                     "brown": (175, 130, 80),  "black": (38, 34, 30)}
    pc = traits.get("plumage", "white")
    body_color = _tinted(_PLUMAGE_BASE.get(pc, _PLUMAGE_BASE["white"]), shift)
    pygame.draw.ellipse(screen, body_color,
                        (sx + max(1, int(1 * s)), sy + int(2 * s), W - int(4 * s), H - int(8 * s)))

    head_w, head_h = int(8 * s), int(8 * s)
    hx = (sx + W - int(4 * s)) if chicken.facing == 1 else (sx - head_w + int(4 * s))
    hy = sy - int(2 * s)
    pygame.draw.ellipse(screen, body_color, (hx, hy, head_w, head_h))
    beak_x = (hx + head_w - max(1, int(1 * s))) if chicken.facing == 1 else (hx - int(3 * s))
    pygame.draw.rect(screen, (220, 160, 30),
                     (beak_x, hy + int(3 * s), int(3 * s), int(2 * s)))
    eye_x = (hx + head_w - int(3 * s)) if chicken.facing == 1 else (hx + max(1, int(1 * s)))
    pygame.draw.rect(screen, (20, 20, 20), (eye_x, hy + int(2 * s), 2, 2))
    pygame.draw.rect(screen, (220, 50, 50),
                     (hx + int(2 * s), hy - int(2 * s), int(4 * s), int(3 * s)))

    if chicken.has_egg:
        pygame.draw.ellipse(screen, (245, 235, 200),
                            (sx + W // 2 - int(3 * s), sy + H - int(10 * s), int(6 * s), int(5 * s)))

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
        pygame.draw.rect(screen, (220, 50, 50),
                         (sx, sy - 13, int(W * chicken.health / 3), 3))
