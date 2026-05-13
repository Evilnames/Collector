import math
import pygame

from constants import SCREEN_W, SCREEN_H


def draw_reptiles(screen, cam_x, cam_y, reptiles):
    for rep in reptiles:
        if rep.state == "hidden":
            continue
        sx = int(rep.x - cam_x)
        sy = int(rep.y - cam_y)
        if sx < -40 or sx > SCREEN_W + 40 or sy < -40 or sy > SCREEN_H + 40:
            continue
        _draw_reptile(screen, rep, sx, sy)


def _draw_reptile(screen, rep, sx, sy):
    bt = rep.BODY_TYPE
    phase = rep._anim_phase
    if bt == "snake":
        _draw_snake(screen, rep, sx, sy, phase)
    elif bt == "turtle":
        _draw_turtle(screen, rep, sx, sy, phase)
    elif bt == "frog":
        _draw_frog(screen, rep, sx, sy, phase)
    else:
        _draw_lizard(screen, rep, sx, sy, phase)


def _draw_snake(screen, rep, sx, sy, phase):
    W, H = rep.W, rep.H
    bc = rep.BODY_COLOR
    pc = rep.PATTERN_COLOR
    belly = rep.BELLY_COLOR
    moving = rep.state in ("moving", "fleeing")
    amp = int(abs(math.sin(phase)) * 3) if moving else 0

    # Draw body as three connected ellipses: tail, mid, head
    seg = W // 3
    # Tail
    pygame.draw.ellipse(screen, bc, (sx, sy - amp, seg + 2, H - 2))
    # Mid-body (slight wave)
    pygame.draw.ellipse(screen, bc, (sx + seg - 1, sy + amp, seg + 2, H))
    # Head (slightly larger, different shade)
    pygame.draw.ellipse(screen, bc, (sx + seg * 2 - 1, sy - amp, seg + 3, H))
    # Head highlight (darker)
    hx = sx + seg * 2 + 1 if rep.facing == 1 else sx + seg * 2 - 1
    pygame.draw.ellipse(screen, pc, (hx, sy - amp + 1, seg, H - 2))
    # Belly stripe
    pygame.draw.ellipse(screen, belly, (sx + 1, sy + H // 3, W - 4, H // 3))
    # Pattern bands
    for i in range(1, 3):
        bx = sx + (W * i) // 3 - 1
        by = sy + amp if i == 1 else sy - amp
        pygame.draw.rect(screen, pc, (bx, by, 2, H - 1))
    # Eye
    ex = sx + W - 5 if rep.facing == 1 else sx + 3
    pygame.draw.circle(screen, (20, 15, 10), (ex, sy - amp + H // 3), 1)


def _draw_lizard(screen, rep, sx, sy, phase):
    W, H = rep.W, rep.H
    bc = rep.BODY_COLOR
    pc = rep.PATTERN_COLOR
    belly = rep.BELLY_COLOR
    moving = rep.state in ("moving", "fleeing")
    leg_spread = int(abs(math.sin(phase)) * 2) if moving else 0

    # Body
    body_w = W - 6
    pygame.draw.ellipse(screen, bc, (sx + 3, sy, body_w, H - 2))
    # Belly
    pygame.draw.ellipse(screen, belly, (sx + 4, sy + 2, body_w - 4, H - 5))
    # Tail
    tail_len = W // 3 + 2
    tx = sx + W - 4 if rep.facing == -1 else sx - tail_len + 2
    pygame.draw.ellipse(screen, bc, (tx, sy + H // 3, tail_len, H // 3))
    # Head
    head_r = H // 2
    hx = sx + W - head_r - 2 if rep.facing == 1 else sx + head_r
    pygame.draw.circle(screen, bc, (hx, sy + head_r), head_r)
    # Eye
    ex = hx + head_r // 2 if rep.facing == 1 else hx - head_r // 2
    pygame.draw.circle(screen, (20, 15, 10), (ex, sy + head_r - 1), 1)
    # Legs (front and back pair)
    leg_y_top = sy + H - 2
    for lx_off in (W // 4, W * 3 // 4 - 2):
        lx = sx + lx_off
        pygame.draw.line(screen, pc, (lx, sy + H - 3), (lx - 3, leg_y_top + leg_spread), 1)
        pygame.draw.line(screen, pc, (lx, sy + H - 3), (lx + 3, leg_y_top + leg_spread), 1)
    # Pattern dots
    for i in range(1, 3):
        pygame.draw.circle(screen, pc, (sx + 4 + (body_w * i) // 3, sy + H // 2 - 1), 1)


def _draw_turtle(screen, rep, sx, sy, phase):
    W, H = rep.W, rep.H
    bc = rep.BODY_COLOR
    pc = rep.PATTERN_COLOR
    belly = rep.BELLY_COLOR
    moving = rep.state == "moving"
    head_bob = int(abs(math.sin(phase)) * 1) if moving else 0

    # Shell (dome polygon)
    shell_pts = [
        (sx + 2,     sy + H - 2),
        (sx,         sy + H // 2),
        (sx + W // 4, sy + 1),
        (sx + W * 3 // 4, sy + 1),
        (sx + W,     sy + H // 2),
        (sx + W - 2, sy + H - 2),
    ]
    pygame.draw.polygon(screen, bc, shell_pts)
    pygame.draw.polygon(screen, pc, shell_pts, 1)
    # Shell scute lines
    mid_x = sx + W // 2
    pygame.draw.line(screen, pc, (mid_x, sy + 2), (mid_x, sy + H - 2), 1)
    pygame.draw.line(screen, pc, (sx + 2, sy + H // 2), (sx + W - 2, sy + H // 2), 1)
    # Belly
    pygame.draw.ellipse(screen, belly, (sx + 3, sy + H - 4, W - 6, 3))
    # Head
    hx = sx + W if rep.facing == 1 else sx - 4
    pygame.draw.ellipse(screen, bc, (hx, sy + H // 2 - 2 - head_bob, 5, 4))
    # Eye
    ex = hx + 3 if rep.facing == 1 else hx + 1
    pygame.draw.circle(screen, (20, 15, 10), (ex, sy + H // 2 - 2 - head_bob), 1)
    # Legs (stubby)
    leg_col = bc
    for lx_off, ly_off in ((2, H - 3), (W - 4, H - 3)):
        pygame.draw.ellipse(screen, leg_col, (sx + lx_off - 1, sy + ly_off, 4, 2))


def _draw_frog(screen, rep, sx, sy, phase):
    W, H = rep.W, rep.H
    bc = rep.BODY_COLOR
    pc = rep.PATTERN_COLOR
    belly = rep.BELLY_COLOR
    jumping = rep.state in ("moving", "fleeing")
    # Crouch offset: body rises slightly when jumping
    bob = -int(abs(math.sin(phase * 1.5)) * 3) if jumping else 0

    cx = sx + W // 2
    cy = sy + H // 2 + bob

    # Back legs (wide, bent outward)
    back_leg_col = bc
    for side in (-1, 1):
        # Upper leg
        lx = cx + side * (W // 2 - 1)
        pygame.draw.line(screen, back_leg_col,
                         (cx + side * (W // 4), cy + H // 4),
                         (lx, cy + H // 2), 2)
        # Lower leg / foot
        foot_x = lx + side * 3
        pygame.draw.line(screen, back_leg_col,
                         (lx, cy + H // 2),
                         (foot_x, cy + H // 2 + 2), 2)

    # Body (wide, squat ellipse)
    body_rect = (sx + 1, sy + H // 4 + bob, W - 2, H * 3 // 4)
    pygame.draw.ellipse(screen, bc, body_rect)

    # Belly patch
    belly_rect = (sx + 3, sy + H // 2 + bob, W - 6, H // 3)
    pygame.draw.ellipse(screen, belly, belly_rect)

    # Front legs (small, tucked under chin)
    front_leg_col = bc
    for side in (-1, 1):
        flx = cx + side * (W // 3)
        pygame.draw.line(screen, front_leg_col,
                         (flx, sy + H // 2 + bob),
                         (flx + side * 2, sy + H // 2 + H // 4 + bob), 1)

    # Head (slightly wider than body top, blends in)
    head_r = W // 3
    pygame.draw.ellipse(screen, bc, (cx - head_r, sy + bob, head_r * 2, H // 2))

    # Eyes (prominent, on top of head)
    for side in (-1, 1):
        ex = cx + side * (head_r - 2)
        ey = sy + 1 + bob
        pygame.draw.circle(screen, (235, 185, 40), (ex, ey), 2)
        pygame.draw.circle(screen, (15, 12, 8), (ex, ey), 1)

    # Pattern spots on back
    for i, (ox, oy) in enumerate(((-W // 5, H // 3), (W // 5, H // 3), (0, H // 2))):
        pygame.draw.circle(screen, pc, (cx + ox, sy + oy + bob), 1)
