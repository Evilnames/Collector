import pygame


def draw_duck(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    body_col = ( 60,  80,  50)
    head_col = ( 40,  60,  40)
    bill_col = (230, 165,  50)
    # Round body
    pygame.draw.ellipse(screen, body_col, (sx, sy + int(H * 0.35), W, int(H * 0.65)))
    # Head
    head_r = int(5 * s)
    hx = (sx + W - head_r * 2 + 1) if e.facing == 1 else sx
    pygame.draw.ellipse(screen, head_col, (hx, sy, head_r * 2, head_r * 2))
    # Bill
    bx = hx + (head_r * 2 - 1 if e.facing == 1 else -int(4*s) + 1)
    pygame.draw.rect(screen, bill_col, (bx, sy + int(H * 0.25), int(4*s), int(2*s)))
    # Tail curl
    tail_x = sx if e.facing == 1 else sx + W - int(3*s)
    pygame.draw.ellipse(screen, (80, 100, 70), (tail_x, sy + int(H * 0.2), int(4*s), int(3*s)))


def draw_elk(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    body_col = (130, 90, 55)
    leg_col  = (105, 72, 42)
    mane_col = ( 85, 55, 30)
    # Body
    pygame.draw.rect(screen, body_col, (sx, sy + int(H * 0.28), W, int(H * 0.55)))
    # Neck mane
    neck_x = (sx + W - int(7*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, mane_col, (neck_x, sy + int(H * 0.08), int(6*s), int(H * 0.38)))
    # Legs (longer than deer)
    for i in range(4):
        lx = sx + int(W * (0.12 + i * 0.22))
        pygame.draw.rect(screen, leg_col, (lx, sy + int(H * 0.72), max(2, int(3*s)), int(H * 0.28)))
    # Head
    head_w = int(8 * s)
    hx = (sx + W - head_w + 1) if e.facing == 1 else sx
    pygame.draw.rect(screen, body_col, (hx, sy, head_w, int(H * 0.32)))
    # Large palmate antlers
    ax = hx + (head_w - 1 if e.facing == 1 else 0)
    for i in range(3):
        off = i * 2 * (1 if e.facing == 1 else -1)
        pygame.draw.line(screen, (110, 78, 38),
                         (ax, sy - 1),
                         (ax + off + (4 if e.facing == 1 else -4), sy - int(7 + i*2)), 1)
    if e.health < 3:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health / 3), 2))


def draw_bison(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col      = ( 65,  48,  32)
    hump_col = ( 55,  40,  26)
    # Massive body — low-slung
    pygame.draw.rect(screen, col, (sx, sy + int(H * 0.3), W, int(H * 0.6)))
    # Shoulder hump
    hump_x = (sx + W - int(14*s)) if e.facing == 1 else (sx + int(4*s))
    pygame.draw.ellipse(screen, hump_col, (hump_x, sy + int(H * 0.1), int(14*s), int(H * 0.35)))
    # Short legs
    leg_w = max(3, int(5*s))
    for i in range(4):
        lx = sx + int(W * (0.1 + i * 0.25))
        pygame.draw.rect(screen, (50, 36, 22), (lx, sy + int(H * 0.75), leg_w, int(H * 0.25)))
    # Large shaggy head
    head_w = int(10 * s)
    hx = (sx + W - head_w) if e.facing == 1 else sx
    pygame.draw.rect(screen, hump_col, (hx, sy + int(H * 0.08), head_w, int(H * 0.45)))
    # Horns
    horn_x = hx + (int(head_w * 0.3) if e.facing == 1 else int(head_w * 0.5))
    pygame.draw.line(screen, (40, 32, 22), (horn_x, sy + int(H*0.08)), (horn_x + (5 if e.facing == 1 else -5), sy - int(3*s)), 2)
    if e.health < 3:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 6, int(W * e.health / 3), 3))


def draw_fox(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col      = (210,  95,  35)
    belly    = (240, 215, 185)
    # Slender body
    pygame.draw.rect(screen, col, (sx, sy + int(H * 0.3), W, int(H * 0.52)))
    # White belly
    pygame.draw.rect(screen, belly, (sx + int(W*0.2), sy + int(H*0.38), int(W*0.6), int(H*0.35)))
    # Legs
    for i in range(4):
        lx = sx + int(W * (0.12 + i * 0.22))
        pygame.draw.rect(screen, (170, 75, 25), (lx, sy + int(H*0.72), max(2, int(2*s)), int(H*0.28)))
    # Bushy tail
    tail_x = (sx - int(5*s)) if e.facing == 1 else (sx + W)
    pygame.draw.ellipse(screen, col, (tail_x, sy + int(H*0.25), int(7*s), int(5*s)))
    pygame.draw.ellipse(screen, belly, (tail_x + int(2*s), sy + int(H*0.4), int(3*s), int(2*s)))
    # Head + pointed snout
    head_w = int(7 * s)
    hx = (sx + W - head_w + 1) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (hx, sy + int(H*0.1), head_w, int(H*0.35)))
    snout_x = hx + (head_w - 1 if e.facing == 1 else -int(3*s))
    pygame.draw.polygon(screen, col, [
        (snout_x, sy + int(H*0.22)),
        (snout_x + (int(3*s) if e.facing == 1 else -int(3*s)), sy + int(H*0.28)),
        (snout_x, sy + int(H*0.34)),
    ])
    # Ear
    ex = hx + (int(head_w*0.4) if e.facing == 1 else int(head_w*0.5))
    pygame.draw.polygon(screen, col, [(ex, sy + int(H*0.1)), (ex-2, sy - int(5*s)), (ex+2, sy - int(5*s))])


def draw_arctic_fox(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col   = (230, 235, 240)   # white-grey coat
    belly = (250, 252, 255)   # bright white belly
    # Slender body
    pygame.draw.rect(screen, col, (sx, sy + int(H * 0.3), W, int(H * 0.52)))
    # White belly
    pygame.draw.rect(screen, belly, (sx + int(W*0.2), sy + int(H*0.38), int(W*0.6), int(H*0.35)))
    # Legs
    for i in range(4):
        lx = sx + int(W * (0.12 + i * 0.22))
        pygame.draw.rect(screen, (190, 195, 200), (lx, sy + int(H*0.72), max(2, int(2*s)), int(H*0.28)))
    # Bushy tail
    tail_x = (sx - int(5*s)) if e.facing == 1 else (sx + W)
    pygame.draw.ellipse(screen, col, (tail_x, sy + int(H*0.25), int(7*s), int(5*s)))
    pygame.draw.ellipse(screen, belly, (tail_x + int(2*s), sy + int(H*0.4), int(3*s), int(2*s)))
    # Head + pointed snout
    head_w = int(7 * s)
    hx = (sx + W - head_w + 1) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (hx, sy + int(H*0.1), head_w, int(H*0.35)))
    snout_x = hx + (head_w - 1 if e.facing == 1 else -int(3*s))
    pygame.draw.polygon(screen, col, [
        (snout_x, sy + int(H*0.22)),
        (snout_x + (int(3*s) if e.facing == 1 else -int(3*s)), sy + int(H*0.28)),
        (snout_x, sy + int(H*0.34)),
    ])
    # Ear
    ex = hx + (int(head_w*0.4) if e.facing == 1 else int(head_w*0.5))
    pygame.draw.polygon(screen, col, [(ex, sy + int(H*0.1)), (ex-2, sy - int(5*s)), (ex+2, sy - int(5*s))])


def draw_moose(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col = (90, 65, 42)
    # Tall body, longer legs than elk
    pygame.draw.rect(screen, col, (sx, sy + int(H * 0.25), W, int(H * 0.52)))
    for i in range(4):
        lx = sx + int(W * (0.1 + i * 0.25))
        pygame.draw.rect(screen, (68, 48, 30), (lx, sy + int(H * 0.72), max(2, int(3*s)), int(H * 0.28)))
    # Distinctive bulbous nose / dewlap
    hx = (sx + W - int(9*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (hx, sy + int(H*0.05), int(9*s), int(H*0.32)))
    snout_x = hx + (int(9*s) - 2 if e.facing == 1 else -int(3*s))
    pygame.draw.ellipse(screen, (75, 52, 33), (snout_x, sy + int(H*0.18), int(5*s), int(5*s)))
    # Broad palmate antlers
    ax = hx + (int(9*s) - 2 if e.facing == 1 else 2)
    for i in range(4):
        ox = i * 2 * (1 if e.facing == 1 else -1)
        pygame.draw.line(screen, (100, 72, 38), (ax, sy), (ax + ox + (5 if e.facing == 1 else -5), sy - int(8 + i)), 1)
    if e.health < 4:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 6, int(W * e.health / 4), 3))


def draw_bighorn(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col = (185, 155, 110)
    # Stocky body
    pygame.draw.rect(screen, col, (sx, sy + int(H*0.28), W, int(H*0.55)))
    for i in range(4):
        lx = sx + int(W * (0.12 + i * 0.22))
        pygame.draw.rect(screen, (155, 128, 88), (lx, sy + int(H*0.75), max(2, int(3*s)), int(H*0.25)))
    # Head
    hx = (sx + W - int(7*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (hx, sy + int(H*0.1), int(7*s), int(H*0.38)))
    # Curled horns — two arcs
    hcx = hx + (int(7*s) - 2 if e.facing == 1 else 2)
    pygame.draw.arc(screen, (140, 108, 65),
                    (hcx - int(5*s), sy - int(3*s), int(8*s), int(8*s)),
                    0, 3.14, 2)
    if e.health < 2:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health / 2), 2))


def draw_pheasant_animal(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    # Colourful plumage
    body_col  = (190, 110, 40)
    chest_col = (210,  60, 30)
    tail_col  = (165, 130, 50)
    pygame.draw.ellipse(screen, body_col, (sx + 2, sy + int(H*0.3), W - 4, int(H*0.6)))
    # Iridescent chest
    pygame.draw.ellipse(screen, chest_col,
                        (sx + int(W*0.35 if e.facing == 1 else 0.15), sy + int(H*0.35),
                         int(W*0.35), int(H*0.4)))
    # Long tail
    tail_x = sx if e.facing == 1 else sx + W - int(6*s)
    for i in range(3):
        pygame.draw.line(screen, tail_col,
                         (tail_x + int(3*s), sy + int(H*0.5)),
                         (tail_x + int(3*s) + (i-1)*2*(-1 if e.facing == 1 else 1),
                          sy + int(H*0.1)), 1)
    # Head + red wattle
    hx = (sx + W - int(5*s)) if e.facing == 1 else sx
    pygame.draw.ellipse(screen, (80, 55, 30), (hx, sy + int(H*0.1), int(5*s), int(H*0.32)))
    pygame.draw.line(screen, (200, 40, 40),
                     (hx + (int(5*s)-1 if e.facing == 1 else 0), sy + int(H*0.25)),
                     (hx + (int(5*s)+1 if e.facing == 1 else -2), sy + int(H*0.38)), 2)


def draw_warthog(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col  = (105,  85,  65)
    # Low, wide body
    pygame.draw.rect(screen, col, (sx, sy + int(H*0.3), W, int(H*0.58)))
    for i in range(4):
        lx = sx + int(W * (0.1 + i * 0.24))
        pygame.draw.rect(screen, (82, 65, 48), (lx, sy + int(H*0.78), max(2, int(4*s)), int(H*0.22)))
    # Warty head
    hx = (sx + W - int(9*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, (118, 95, 72), (hx, sy + int(H*0.15), int(9*s), int(H*0.42)))
    # Tusks
    tusk_y = sy + int(H*0.45)
    tusk_x = hx + (int(9*s) if e.facing == 1 else -int(4*s))
    pygame.draw.line(screen, (235, 225, 195), (tusk_x, tusk_y), (tusk_x + (4 if e.facing == 1 else -4), tusk_y - 3), 2)
    pygame.draw.line(screen, (235, 225, 195), (tusk_x, tusk_y + 2), (tusk_x + (4 if e.facing == 1 else -4), tusk_y - 1), 1)
    # Mane ridge
    for i in range(3):
        mx = sx + int(W * (0.2 + i * 0.25))
        pygame.draw.line(screen, (80, 62, 45), (mx, sy + int(H*0.3)), (mx, sy + int(H*0.15)), 1)
    if e.health < 2:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health / 2), 2))


def draw_musk_ox(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col     = (50, 38, 28)
    skirt_c = (35, 26, 18)
    # Shaggy skirted body (long fur hangs low)
    pygame.draw.rect(screen, col, (sx, sy + int(H*0.2), W, int(H*0.55)))
    pygame.draw.rect(screen, skirt_c, (sx - 1, sy + int(H*0.55), W + 2, int(H*0.28)))
    # Thick legs barely visible under skirt
    for i in range(4):
        lx = sx + int(W * (0.12 + i * 0.23))
        pygame.draw.rect(screen, (40, 30, 20), (lx, sy + int(H*0.78), max(2, int(4*s)), int(H*0.22)))
    # Massive shaggy head
    hx = (sx + W - int(10*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, skirt_c, (hx, sy + int(H*0.05), int(10*s), int(H*0.42)))
    # Down-curved horns
    horn_base = hx + (int(10*s) - int(3*s) if e.facing == 1 else int(3*s))
    pygame.draw.arc(screen, (120, 100, 72),
                    (horn_base - int(4*s), sy - int(2*s), int(8*s), int(6*s)),
                    3.14, 2*3.14, 2)
    if e.health < 3:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 6, int(W * e.health / 3), 3))


def draw_crocodile(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col      = (60, 88, 52)
    belly_c  = (95, 118, 80)
    # Long flat body close to ground
    pygame.draw.rect(screen, col, (sx, sy + int(H*0.4), W, int(H*0.45)))
    # Belly stripe
    pygame.draw.rect(screen, belly_c, (sx + int(W*0.1), sy + int(H*0.52), int(W*0.8), int(H*0.2)))
    # Scute ridges
    for i in range(5):
        rx = sx + int(W * (0.1 + i * 0.18))
        pygame.draw.rect(screen, (45, 68, 38), (rx, sy + int(H*0.35), max(2, int(2*s)), int(H*0.12)))
    # Short legs
    for i in range(4):
        lx = sx + int(W * (0.12 + i * 0.22))
        pygame.draw.rect(screen, (50, 75, 44), (lx, sy + int(H*0.8), max(2, int(3*s)), int(H*0.2)))
    # Long flat snout
    hx = (sx + W - int(12*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (hx, sy + int(H*0.3), int(12*s), int(H*0.22)))
    # Teeth line
    pygame.draw.line(screen, (230, 225, 210),
                     (hx, sy + int(H*0.42)),
                     (hx + int(12*s), sy + int(H*0.42)), 1)
    if e.health < 3:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health / 3), 2))


def draw_goose(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col      = (185, 175, 160)
    neck_col = (210, 200, 185)
    bill_col = (200, 145, 50)
    # Plump body
    pygame.draw.ellipse(screen, col, (sx, sy + int(H*0.3), W, int(H*0.7)))
    # Long neck
    nx = (sx + W - int(5*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, neck_col, (nx, sy, int(4*s), int(H*0.45)))
    # Head
    hx = nx + (int(4*s) - int(5*s) + 1 if e.facing == 1 else -int(1*s))
    pygame.draw.ellipse(screen, (50, 50, 50), (hx, sy - int(2*s), int(6*s), int(5*s)))
    # Orange bill
    bx = hx + (int(6*s) - 1 if e.facing == 1 else -int(4*s))
    pygame.draw.rect(screen, bill_col, (bx, sy - int(1*s) + int(H*0.1), int(4*s), int(2*s)))


def draw_hare(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col = (175, 155, 115)
    # Leaner than rabbit, longer ears
    pygame.draw.ellipse(screen, col, (sx, sy + int(H*0.25), W, int(H*0.75)))
    hx = (sx + W - int(8*s) + 1) if e.facing == 1 else sx
    pygame.draw.ellipse(screen, col, (hx, sy, int(8*s), int(H*0.55)))
    # Long upright ears
    ex = hx + (int(8*s*0.55) if e.facing == 1 else int(8*s*0.25))
    pygame.draw.rect(screen, col, (ex - 1, sy - int(8*s), 2, int(8*s)))
    pygame.draw.rect(screen, col, (ex + 3, sy - int(7*s), 2, int(7*s)))
    # Black ear tips
    pygame.draw.rect(screen, (50, 40, 30), (ex - 1, sy - int(8*s), 2, 2))
    pygame.draw.rect(screen, (50, 40, 30), (ex + 3, sy - int(7*s), 2, 2))


def draw_caribou(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col = (155, 130, 95)
    pale = (210, 195, 165)
    pygame.draw.rect(screen, col, (sx, sy + int(H*0.28), W, int(H*0.5)))
    pygame.draw.rect(screen, pale, (sx, sy + int(H*0.55), W, int(H*0.12)))
    for i in range(4):
        lx = sx + int(W * (0.12 + i * 0.24))
        pygame.draw.rect(screen, (115, 95, 70), (lx, sy + int(H*0.75), max(2, int(3*s)), int(H*0.25)))
    hx = (sx + W - int(8*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (hx, sy + int(H*0.08), int(8*s), int(H*0.34)))
    pygame.draw.rect(screen, pale, (hx, sy + int(H*0.3), int(8*s), int(H*0.08)))
    ax = hx + (int(8*s) - 2 if e.facing == 1 else 2)
    for i in range(5):
        ox = (i - 2) * 2 * (1 if e.facing == 1 else -1)
        pygame.draw.line(screen, (210, 185, 145), (ax, sy + 2), (ax + ox, sy - int(7 + i)), 1)
    if e.health < 3:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health / 3), 2))


def draw_antelope(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col = (190, 150, 100)
    pale = (235, 215, 175)
    pygame.draw.ellipse(screen, col, (sx, sy + int(H*0.3), W, int(H*0.55)))
    pygame.draw.rect(screen, pale, (sx + int(W*0.1), sy + int(H*0.6), int(W*0.8), int(H*0.12)))
    for i in range(4):
        lx = sx + int(W * (0.14 + i * 0.22))
        pygame.draw.rect(screen, (75, 55, 35), (lx, sy + int(H*0.78), max(2, int(2*s)), int(H*0.22)))
    nx = (sx + W - int(4*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (nx, sy + int(H*0.18), int(4*s), int(H*0.2)))
    hx = nx + ((int(4*s)) if e.facing == 1 else -int(5*s))
    pygame.draw.rect(screen, col, (hx, sy + int(H*0.1), int(5*s), int(H*0.22)))
    horn_x = hx + (int(5*s) - 2 if e.facing == 1 else 1)
    pygame.draw.line(screen, (50, 40, 28), (horn_x, sy + int(H*0.1)), (horn_x + (2 if e.facing == 1 else -2), sy - int(6*s)), 2)
    pygame.draw.line(screen, (50, 40, 28), (horn_x - (1 if e.facing == 1 else -1), sy + int(H*0.1)), (horn_x + (1 if e.facing == 1 else -1), sy - int(5*s)), 2)
    if e.health < 2:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health / 2), 2))


def draw_ibex(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col = (130, 105, 75)
    dark = (90, 70, 50)
    pygame.draw.rect(screen, col, (sx, sy + int(H*0.3), W, int(H*0.52)))
    for i in range(4):
        lx = sx + int(W * (0.12 + i * 0.24))
        pygame.draw.rect(screen, dark, (lx, sy + int(H*0.78), max(2, int(3*s)), int(H*0.22)))
    hx = (sx + W - int(6*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (hx, sy + int(H*0.12), int(6*s), int(H*0.35)))
    # Beard tuft
    bx = hx + (1 if e.facing == 1 else int(6*s) - 2)
    pygame.draw.rect(screen, dark, (bx, sy + int(H*0.42), 2, int(4*s)))
    # Long curved horns sweeping back
    base_x = hx + (int(5*s) if e.facing == 1 else 1)
    for i in range(4):
        x0 = base_x + (i * (-1 if e.facing == 1 else 1))
        pygame.draw.line(screen, (95, 70, 40),
                         (x0, sy + int(H*0.1) + i),
                         (x0 + ((-2 - i) if e.facing == 1 else (2 + i)), sy - int(2 + i*2)),
                         2)
    if e.health < 2:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health / 2), 2))


def draw_lynx(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col = (200, 175, 130)
    spot = (135, 105, 70)
    pygame.draw.ellipse(screen, col, (sx, sy + int(H*0.35), W, int(H*0.55)))
    for i in range(5):
        rx = sx + int(W * (0.15 + i * 0.17))
        pygame.draw.rect(screen, spot, (rx, sy + int(H*0.45), 2, 2))
    for i in range(4):
        lx = sx + int(W * (0.14 + i * 0.22))
        pygame.draw.rect(screen, (155, 130, 95), (lx, sy + int(H*0.8), max(2, int(3*s)), int(H*0.2)))
    hx = (sx + W - int(6*s)) if e.facing == 1 else sx
    pygame.draw.ellipse(screen, col, (hx, sy + int(H*0.2), int(6*s), int(H*0.32)))
    # Tufted ears
    ex = hx + (int(6*s*0.2) if e.facing == 1 else int(6*s*0.6))
    pygame.draw.line(screen, (50, 40, 30), (ex, sy + int(H*0.2)), (ex - 1, sy + int(H*0.05)), 2)
    pygame.draw.line(screen, (50, 40, 30), (ex + int(3*s), sy + int(H*0.2)), (ex + int(3*s) + 1, sy + int(H*0.05)), 2)
    # Stub tail
    tx = sx if e.facing == 1 else sx + W - 3
    pygame.draw.rect(screen, col, (tx, sy + int(H*0.4), 3, int(H*0.12)))
    if e.health < 2:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health / 2), 2))


def draw_coyote(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col = (170, 145, 105)
    pale = (210, 190, 155)
    pygame.draw.ellipse(screen, col, (sx, sy + int(H*0.32), W, int(H*0.55)))
    pygame.draw.rect(screen, pale, (sx + int(W*0.15), sy + int(H*0.6), int(W*0.7), int(H*0.1)))
    for i in range(4):
        lx = sx + int(W * (0.13 + i * 0.23))
        pygame.draw.rect(screen, (120, 100, 70), (lx, sy + int(H*0.78), max(2, int(2*s)), int(H*0.22)))
    hx = (sx + W - int(7*s)) if e.facing == 1 else sx
    pygame.draw.rect(screen, col, (hx, sy + int(H*0.2), int(7*s), int(H*0.3)))
    # Pointed snout
    snout_x = hx + (int(7*s) if e.facing == 1 else -int(3*s))
    pygame.draw.rect(screen, col, (snout_x, sy + int(H*0.3), int(3*s), int(H*0.14)))
    # Ears
    ex = hx + (1 if e.facing == 1 else int(7*s) - 3)
    pygame.draw.line(screen, col, (ex, sy + int(H*0.22)), (ex + 1, sy + int(H*0.08)), 2)
    pygame.draw.line(screen, col, (ex + int(4*s), sy + int(H*0.22)), (ex + int(4*s) - 1, sy + int(H*0.08)), 2)
    # Bushy tail
    tx = sx if e.facing == 1 else sx + W - int(5*s)
    pygame.draw.ellipse(screen, col, (tx, sy + int(H*0.4), int(5*s), int(H*0.2)))
    if e.health < 1:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health), 2))


def draw_beaver(screen, sx, sy, e):
    W, H = e.W, e.H
    s = e.traits.get("size", 1.0)
    col = (105, 70, 45)
    dark = (75, 50, 32)
    pygame.draw.ellipse(screen, col, (sx, sy + int(H*0.35), W, int(H*0.6)))
    # Flat paddle tail
    tx = sx if e.facing == 1 else sx + W - int(6*s)
    pygame.draw.ellipse(screen, dark, (tx, sy + int(H*0.6), int(6*s), int(H*0.28)))
    # Stubby legs
    for i in range(4):
        lx = sx + int(W * (0.18 + i * 0.2))
        pygame.draw.rect(screen, dark, (lx, sy + int(H*0.85), max(2, int(2*s)), int(H*0.15)))
    hx = (sx + W - int(6*s)) if e.facing == 1 else sx
    pygame.draw.ellipse(screen, col, (hx, sy + int(H*0.25), int(6*s), int(H*0.42)))
    # Buck teeth
    tooth_x = hx + (int(6*s) - 2 if e.facing == 1 else 1)
    pygame.draw.rect(screen, (235, 215, 130), (tooth_x, sy + int(H*0.5), 2, int(3*s)))
    # Small round ear
    ex = hx + (int(6*s*0.3) if e.facing == 1 else int(6*s*0.55))
    pygame.draw.rect(screen, dark, (ex, sy + int(H*0.22), 2, 2))
    if e.health < 1:
        pygame.draw.rect(screen, (220, 50, 50), (sx, sy - 5, int(W * e.health), 2))
