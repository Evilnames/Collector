import math
import pygame

from constants import SCREEN_W, SCREEN_H


def draw_live_fish(screen, cam_x, cam_y, fish_list):
    for f in fish_list:
        if f.dead:
            continue
        sx = int(f.x - cam_x)
        sy = int(f.y - cam_y)
        if sx < -40 or sx > SCREEN_W + 40 or sy < -40 or sy > SCREEN_H + 40:
            continue
        _draw_fish(screen, f, sx, sy)


def _draw_fish(screen, f, sx, sy):
    W, H = f.W, f.H
    facing = f.facing
    # Tail wiggle phase from drift_phase.
    wiggle = int(math.sin(f._drift_phase * 2.2) * 2)

    body = f.primary_color
    accent = f.secondary_color

    body_rect = pygame.Rect(sx, sy, W, H)
    pygame.draw.ellipse(screen, body, body_rect)

    # Belly stripe
    pygame.draw.ellipse(screen, accent,
                        (sx + 2, sy + H // 2, W - 4, max(1, H // 2)))

    # Tail (triangle on the trailing side)
    if facing < 0:
        tail_pts = [
            (sx + W, sy + H // 2),
            (sx + W + 5, sy + wiggle),
            (sx + W + 5, sy + H + wiggle),
        ]
    else:
        tail_pts = [
            (sx, sy + H // 2),
            (sx - 5, sy + wiggle),
            (sx - 5, sy + H + wiggle),
        ]
    pygame.draw.polygon(screen, body, tail_pts)

    # Eye
    eye_x = sx + (2 if facing < 0 else W - 4)
    pygame.draw.circle(screen, (240, 240, 240), (eye_x, sy + 2), 1)


def draw_spears(screen, cam_x, cam_y, spears):
    for s in spears:
        if s.dead:
            continue
        sx = int(s.x - cam_x)
        sy = int(s.y - cam_y)
        if sx < -40 or sx > SCREEN_W + 40 or sy < -40 or sy > SCREEN_H + 40:
            continue
        # Shaft
        length = 14
        if s.vx >= 0:
            x0, x1 = sx, sx + length
        else:
            x0, x1 = sx + length, sx
        pygame.draw.line(screen, (220, 210, 180), (x0, sy + 1), (x1, sy + 1), 2)
        # Tip
        tip_x = x1
        tip_y = sy + 1
        if s.vx >= 0:
            pts = [(tip_x, tip_y), (tip_x - 4, tip_y - 2), (tip_x - 4, tip_y + 2)]
        else:
            pts = [(tip_x, tip_y), (tip_x + 4, tip_y - 2), (tip_x + 4, tip_y + 2)]
        pygame.draw.polygon(screen, (200, 200, 215), pts)
