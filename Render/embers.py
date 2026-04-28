"""Ember spark particles rising from active fire/hearth blocks."""
import pygame
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H
from blocks import WARM_EMITTERS

_MAX_EMBERS = 80
_FLICKER_BIDS = None


def _flicker_bids():
    global _FLICKER_BIDS
    if _FLICKER_BIDS is None:
        _FLICKER_BIDS = frozenset(
            bid for bid, (_, pat) in WARM_EMITTERS.items() if pat == "flicker"
        )
    return _FLICKER_BIDS


def spawn_embers(particles, world, cam_x, cam_y, rng):
    if len(particles) >= _MAX_EMBERS:
        return
    flicker = _flicker_bids()
    cam_xi  = int(cam_x)
    cam_yi  = int(cam_y)
    bx0 = cam_xi // BLOCK_SIZE
    bx1 = (cam_xi + SCREEN_W) // BLOCK_SIZE + 1
    by0 = max(0, cam_yi // BLOCK_SIZE)
    by1 = min(world.height, (cam_yi + SCREEN_H) // BLOCK_SIZE + 1)
    for by in range(by0, by1):
        for bx in range(bx0, bx1):
            if world.get_block(bx, by) not in flicker:
                continue
            if rng.random() > 0.006:
                continue
            if len(particles) >= _MAX_EMBERS:
                return
            wx  = bx * BLOCK_SIZE + rng.uniform(6, BLOCK_SIZE - 6)
            wy  = by * BLOCK_SIZE + BLOCK_SIZE // 3
            col = rng.choice(((255, 220, 60), (255, 160, 30), (255, 200, 80)))
            particles.append({
                "wx": wx, "wy": wy,
                "vx": rng.uniform(-20, 20),
                "vy": rng.uniform(-60, -28),
                "life": rng.uniform(0.3, 0.7),
                "max_life": 0.55,
                "color": col,
            })


def tick_embers(particles, dt):
    i = 0
    while i < len(particles):
        p = particles[i]
        p["life"] -= dt
        if p["life"] <= 0:
            particles.pop(i)
            continue
        p["vy"] += 70 * dt
        p["vx"] *= max(0.0, 1 - 2.0 * dt)
        p["wx"] += p["vx"] * dt
        p["wy"] += p["vy"] * dt
        i += 1


def draw_embers(screen, cam_x, cam_y, particles):
    if not particles:
        return
    surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for p in particles:
        sx = p["wx"] - cam_x
        sy = p["wy"] - cam_y
        if sx < -4 or sx > SCREEN_W + 4 or sy < -4 or sy > SCREEN_H + 4:
            continue
        fade  = p["life"] / p["max_life"]
        alpha = min(230, int(230 * fade))
        r, g, b = p["color"]
        pygame.draw.rect(surf, (r, g, b, alpha), (int(sx), int(sy), 2, 2))
    screen.blit(surf, (0, 0))
