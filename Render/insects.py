import math
import pygame

from constants import SCREEN_W, SCREEN_H


# ------------------------------------------------------------------

def draw_insects(screen, cam_x, cam_y, insects, night_alpha=0, time_of_day=0.0):
    from world import DAY_DURATION
    _dawn = time_of_day < 60.0
    _dusk = DAY_DURATION - 60.0 <= time_of_day < DAY_DURATION
    for ins in insects:
        if ins.spooked or ins.hidden:
            continue
        if ins.NIGHT_ONLY and night_alpha < 30:
            continue
        if ins.DAWN_ONLY and not _dawn:
            continue
        if ins.DUSK_ONLY and not _dusk:
            continue
        sx = int(ins.x - cam_x)
        sy = int(ins.y - cam_y)
        if sx < -30 or sx > SCREEN_W + 30 or sy < -30 or sy > SCREEN_H + 30:
            continue
        _draw_insect(screen, ins, sx, sy)

def _draw_insect(screen, ins, sx, sy):
    wt = ins.WING_TYPE
    wf = abs(math.sin(ins._hover_phase)) * 3
    if wt == "butterfly":
        _draw_insect_butterfly(screen, ins, sx, sy, wf)
    elif wt == "moth":
        _draw_insect_moth(screen, ins, sx, sy, wf)
    elif wt == "dragonfly":
        _draw_insect_dragonfly(screen, ins, sx, sy, wf)
    elif wt == "firefly":
        _draw_insect_firefly(screen, ins, sx, sy)
    elif wt == "beetle":
        _draw_insect_beetle(screen, ins, sx, sy)
    else:
        _draw_insect_generic(screen, ins, sx, sy, wf)

def _draw_insect_butterfly(screen, ins, sx, sy, wf):
    W, H = ins.W, ins.H
    wo = int(wf)
    # Upper wings
    pygame.draw.ellipse(screen, ins.WING_COLOR,
                        (sx, sy - wo, W // 2, H))
    pygame.draw.ellipse(screen, ins.WING_COLOR,
                        (sx + W // 2, sy - wo, W // 2, H))
    # Accent spots
    pygame.draw.ellipse(screen, ins.ACCENT_COLOR,
                        (sx + 2, sy - wo + 2, W // 2 - 3, H // 2))
    pygame.draw.ellipse(screen, ins.ACCENT_COLOR,
                        (sx + W // 2 + 1, sy - wo + 2, W // 2 - 3, H // 2))
    # Body
    pygame.draw.ellipse(screen, ins.BODY_COLOR,
                        (sx + W // 2 - 1, sy, 3, H))

def _draw_insect_moth(screen, ins, sx, sy, wf):
    W, H = ins.W, ins.H
    wo = int(wf)
    # Broad flat wings
    pygame.draw.ellipse(screen, ins.WING_COLOR,
                        (sx, sy + 1 - wo, W, H - 2))
    pygame.draw.ellipse(screen, ins.ACCENT_COLOR,
                        (sx + 2, sy + 2 - wo, W - 4, H - 4))
    # Body
    pygame.draw.ellipse(screen, ins.BODY_COLOR,
                        (sx + W // 2 - 1, sy, 3, H))

def _draw_insect_dragonfly(screen, ins, sx, sy, wf):
    W, H = ins.W, ins.H
    wo = int(wf)
    cx = sx + W // 2
    # 4 narrow wings
    pygame.draw.ellipse(screen, ins.WING_COLOR,
                        (sx, sy - 1 - wo, W // 2, 3))
    pygame.draw.ellipse(screen, ins.WING_COLOR,
                        (cx, sy - 1 - wo, W // 2, 3))
    pygame.draw.ellipse(screen, ins.WING_COLOR,
                        (sx + 2, sy + 2 - wo, W // 2 - 2, 2))
    pygame.draw.ellipse(screen, ins.WING_COLOR,
                        (cx - 2, sy + 2 - wo, W // 2 - 2, 2))
    # Elongated segmented body
    pygame.draw.ellipse(screen, ins.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    pygame.draw.ellipse(screen, ins.ACCENT_COLOR,
                        (sx + 3, sy + 2, W - 6, H - 4))

def _draw_insect_firefly(screen, ins, sx, sy):
    W, H = ins.W, ins.H
    pulse = abs(math.sin(ins._hover_phase * 0.5))
    # Small oval body
    pygame.draw.ellipse(screen, ins.BODY_COLOR, (sx, sy + 1, W, H - 2))
    pygame.draw.ellipse(screen, ins.WING_COLOR, (sx + 1, sy + 2, W - 2, H - 4))
    # Glowing tail — pulsing radius and brightness
    r = 2 + int(pulse)
    brightness = int(pulse * 200 + 55)
    gc = tuple(min(255, int(c * brightness / 255)) for c in ins.ACCENT_COLOR)
    tail_x = sx + W - 3
    tail_y = sy + H // 2
    pygame.draw.circle(screen, gc, (tail_x, tail_y), r)

def _draw_insect_beetle(screen, ins, sx, sy):
    W, H = ins.W, ins.H
    # Elytra (wing covers)
    pygame.draw.ellipse(screen, ins.WING_COLOR, (sx, sy, W, H))
    pygame.draw.ellipse(screen, ins.BODY_COLOR, (sx + 1, sy + 1, W - 2, H - 2))
    # Central seam
    pygame.draw.line(screen, ins.WING_COLOR,
                     (sx + W // 2, sy + 1), (sx + W // 2, sy + H - 2))
    # Head
    pygame.draw.circle(screen, ins.ACCENT_COLOR,
                       (sx + W // 6, sy + H // 2), H // 3)

def _draw_insect_generic(screen, ins, sx, sy, wf):
    W, H = ins.W, ins.H
    wo = int(wf)
    pygame.draw.ellipse(screen, ins.WING_COLOR,
                        (sx, sy - wo, W, H + wo))
    pygame.draw.ellipse(screen, ins.BODY_COLOR,
                        (sx + W // 4, sy + 1, W // 2, H - 2))
    pygame.draw.circle(screen, ins.ACCENT_COLOR,
                       (sx + W // 2, sy), H // 3)
