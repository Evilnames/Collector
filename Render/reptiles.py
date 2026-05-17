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


def _shade(color, factor):
    return (
        max(0, min(255, int(color[0] * factor))),
        max(0, min(255, int(color[1] * factor))),
        max(0, min(255, int(color[2] * factor))),
    )


def _draw_snake(screen, rep, sx, sy, phase):
    W, H = rep.W, rep.H
    bc = rep.BODY_COLOR
    pc = rep.PATTERN_COLOR
    belly = rep.BELLY_COLOR
    shadow = _shade(bc, 0.55)
    highlight = _shade(bc, 1.25)
    moving = rep.state in ("moving", "fleeing")
    facing = rep.facing

    # Body thickness: rattlesnakes/pythons are chunkier, garter snakes slim.
    body_r = max(2, H // 2)
    head_r = body_r + 1

    # Sinuous S-curve traced left→right; flip mirror via facing for head placement.
    # Segments are dense small circles for smooth scale-like appearance.
    seg_count = max(14, W)
    cy = sy + H // 2
    wave_amp = (body_r + 1) if moving else max(1, body_r - 1)
    wave_freq = 2.0 * math.pi / max(8, W // 2)
    wave_speed = phase if moving else phase * 0.25

    # Precompute spine points and per-segment radius (taper toward tail).
    spine = []
    for i in range(seg_count + 1):
        t = i / seg_count  # 0 = tail, 1 = head
        x = sx + int(t * (W - 1))
        # Tail sways more than head; head is anchored for striking pose.
        sway_scale = (1.0 - t) * 0.7 + 0.3
        y = cy + int(math.sin(t * wave_freq * (W // 2) - wave_speed) * wave_amp * sway_scale)
        # Taper: thin tail, full mid, slightly bulged neck before head.
        if t < 0.15:
            r = max(1, int(body_r * (0.35 + t * 4.0)))
        elif t > 0.88:
            r = body_r  # neck holds full width into head
        else:
            r = body_r
        spine.append((x, y, r))

    # If facing left, mirror the spine across the bbox so the head ends up on the left.
    if facing == -1:
        x_min = sx
        x_max = sx + W - 1
        spine = [(x_min + (x_max - x), y, r) for (x, y, r) in spine]

    # Body: dark underbelly shadow first, then main color, then top highlight.
    for (x, y, r) in spine:
        pygame.draw.circle(screen, shadow, (x, y + 1), r)
    for (x, y, r) in spine:
        pygame.draw.circle(screen, bc, (x, y), r)
    # Dorsal highlight (top ridge — gives roundness)
    for (x, y, r) in spine:
        if r >= 2:
            pygame.draw.circle(screen, highlight, (x, y - r + 1), max(1, r - 1))

    # Belly: light pixels along underside, only where spine is.
    for (x, y, r) in spine[2:-2]:
        if r >= 2:
            pygame.draw.line(screen, belly, (x, y + r - 1), (x, y + r - 1))

    # Pattern bands / diamonds along the back, following the curve.
    # Spacing scales with body length so small snakes don't look noisy.
    band_spacing = max(3, seg_count // 8)
    for i in range(2, seg_count - 1, band_spacing):
        x, y, r = spine[i]
        if r >= 2:
            # Diamond shape on dorsal surface
            pygame.draw.line(screen, pc, (x - 1, y - r + 1), (x + 1, y - r + 1))
            pygame.draw.line(screen, pc, (x, y - r), (x, y - r + 2))

    # Head: oval oriented along facing direction. Use last spine point as anchor.
    hx, hy, _ = spine[-1]
    head_dx = facing
    # Head body
    head_rect = (hx - head_r + (head_dx * 1), hy - head_r + 1, head_r * 2, head_r * 2 - 1)
    pygame.draw.ellipse(screen, bc, head_rect)
    # Top of head highlight
    pygame.draw.ellipse(screen, highlight,
                        (head_rect[0] + 1, head_rect[1], head_rect[2] - 2, max(1, head_r - 1)))
    # Jaw line shadow
    pygame.draw.line(screen, shadow,
                     (head_rect[0] + 1, hy + head_r - 2),
                     (head_rect[0] + head_rect[2] - 2, hy + head_r - 2))

    # Eye: small bright dot with dark pupil, set forward on the head.
    eye_x = hx + head_dx * (head_r - 1)
    eye_y = hy - 1
    pygame.draw.circle(screen, (240, 220, 160), (eye_x, eye_y), 1)
    pygame.draw.circle(screen, (10, 8, 5), (eye_x + head_dx, eye_y), 1)

    # Forked tongue flick when alert/moving — flickers with phase.
    if moving and math.sin(phase * 3.0) > 0.4:
        tongue_col = (200, 40, 60)
        tip_x = hx + head_dx * (head_r + 2)
        mid_x = hx + head_dx * (head_r + 1)
        pygame.draw.line(screen, tongue_col, (mid_x, hy), (tip_x, hy - 1))
        pygame.draw.line(screen, tongue_col, (mid_x, hy), (tip_x, hy + 1))

    # Rattle tail for rattlesnakes (any species with "rattle" in name).
    species = getattr(rep, "SPECIES", "")
    if "rattle" in species or species == "sidewinder" or "diamondback" in species:
        tail_x, tail_y, _ = spine[0]
        rattle_col = _shade(belly, 0.85)
        rx = tail_x - head_dx * 2
        for k in range(3):
            pygame.draw.rect(screen, rattle_col, (rx - head_dx * k * 2, tail_y - 1, 2, 3), 0)
            pygame.draw.rect(screen, shadow, (rx - head_dx * k * 2, tail_y - 1, 2, 3), 1)


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
