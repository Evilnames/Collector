import math as _m
import pygame
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H


def _darken(color, amount=25):
    return tuple(max(0, c - amount) for c in color)


def get_town_flag_surf(cache, region_id, flag_col):
    if region_id not in cache:
        BS = BLOCK_SIZE
        s = pygame.Surface((BS, BS), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        pole = (120, 100, 70)
        pygame.draw.rect(s, pole, (BS // 2 - 2, 0, 3, BS))
        pts = [(BS // 2 + 1, 3), (BS - 4, 9), (BS // 2 + 1, 16)]
        pygame.draw.polygon(s, flag_col, pts)
        pygame.draw.polygon(s, _darken(flag_col), pts, 1)
        cache[region_id] = s
    return cache[region_id]


def get_outpost_flag_surf(cache, outpost_type, flag_col):
    if outpost_type not in cache:
        BS = BLOCK_SIZE
        s = pygame.Surface((BS, BS), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        pole = (120, 100, 70)
        pygame.draw.rect(s, pole, (BS // 2 - 2, 0, 3, BS))
        pts = [(BS // 2 + 1, 3), (BS - 4, 9), (BS // 2 + 1, 16)]
        pygame.draw.polygon(s, flag_col, pts)
        pygame.draw.polygon(s, _darken(flag_col), pts, 1)
        cache[outpost_type] = s
    return cache[outpost_type]


def build_sky_surf():
    sky_top    = (85,  145, 230)
    sky_bottom = (155, 210, 255)
    surf = pygame.Surface((SCREEN_W, SCREEN_H)).convert()
    for y in range(SCREEN_H):
        t = y / (SCREEN_H - 1)
        r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * t)
        g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * t)
        b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_W - 1, y))
    return surf


def build_night_sky_surf():
    sky_top    = (8,  12, 35)
    sky_bottom = (18, 25, 65)
    surf = pygame.Surface((SCREEN_W, SCREEN_H)).convert()
    for y in range(SCREEN_H):
        t = y / (SCREEN_H - 1)
        r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * t)
        g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * t)
        b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_W - 1, y))
    return surf


def build_dawn_sky_surf():
    """Warm amber-rose sky for the morning golden hour."""
    top    = (215, 105, 45)
    bottom = (255, 180, 95)
    surf = pygame.Surface((SCREEN_W, SCREEN_H)).convert()
    for y in range(SCREEN_H):
        t = y / (SCREEN_H - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_W - 1, y))
    return surf


def build_dusk_sky_surf():
    """Deep orange-red sky for the evening golden hour."""
    top    = (165, 60, 20)
    bottom = (245, 135, 55)
    surf = pygame.Surface((SCREEN_W, SCREEN_H)).convert()
    for y in range(SCREEN_H):
        t = y / (SCREEN_H - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_W - 1, y))
    return surf


def sky_night_alpha(time_of_day):
    from world import DAY_DURATION
    DAWN = 130.0
    DUSK = 130.0
    t = time_of_day
    if t < DAWN:
        # Smoothstep ease so darkness lingers, then fades gently into morning.
        p = 1.0 - t / DAWN
        s = p * p * (3 - 2 * p)
        return int(255 * s)
    elif t < DAY_DURATION - DUSK:
        return 0
    elif t < DAY_DURATION:
        p = (t - (DAY_DURATION - DUSK)) / DUSK
        s = p * p * (3 - 2 * p)
        return int(255 * s)
    else:
        return 255


def golden_hour_alphas(time_of_day):
    """Returns (dawn_alpha, dusk_alpha) each 0-255, peaking mid-transition.

    Uses a sin^1.5 envelope so the overlay holds near peak longer and tails off
    gently toward day, instead of the symmetric sin curve which falls just as
    fast as it rose and produces a perceived 'flash' to blue.
    """
    from world import MORNING_END, DUSK_START, DAY_DURATION
    t = time_of_day
    if t < MORNING_END:
        p = t / MORNING_END
        env = max(0.0, _m.sin(p * _m.pi)) ** 1.5
        return int(210 * env), 0
    if t >= DUSK_START:
        p = (t - DUSK_START) / (DAY_DURATION - DUSK_START)
        env = max(0.0, _m.sin(p * _m.pi)) ** 1.5
        return 0, int(230 * env)
    return 0, 0
