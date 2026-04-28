"""Visual rain particle system.

Spawns diagonal raindrop streaks while world._rain_active is True.
Drop direction and lean follow world._wind_dir / _wind_strength.
"""
import pygame
from constants import SCREEN_W, SCREEN_H

_MAX_PARTICLES = 500
_SPAWN_RATE    = 90   # particles per second at base rain intensity


def spawn_rain_particles(particles, world, cam_x, cam_y, rng, dt):
    if not getattr(world, '_rain_active', False):
        return
    wind_str = getattr(world, '_wind_strength', 1.0) if getattr(world, '_wind_active', False) else 0.0
    wind_dir = getattr(world, '_wind_dir', 1)
    count = int(_SPAWN_RATE * dt * (1.0 + wind_str * 0.4))
    slots = _MAX_PARTICLES - len(particles)
    if slots <= 0:
        return
    for _ in range(min(count, slots)):
        wx = cam_x + rng.uniform(-30, SCREEN_W + 30)
        wy = cam_y + rng.uniform(-60, SCREEN_H * 0.25)
        vx = wind_dir * wind_str * rng.uniform(30, 80)
        vy = rng.uniform(300, 450)
        life = rng.uniform(0.35, 0.75)
        particles.append({"wx": wx, "wy": wy, "vx": vx, "vy": vy, "life": life, "max_life": life})


def tick_rain_particles(particles, cam_y, dt):
    i = 0
    while i < len(particles):
        p = particles[i]
        p["life"] -= dt
        if p["life"] <= 0 or p["wy"] > cam_y + SCREEN_H + 20:
            particles.pop(i)
            continue
        p["wx"] += p["vx"] * dt
        p["wy"] += p["vy"] * dt
        i += 1


def draw_rain_particles(screen, cam_x, cam_y, particles):
    if not particles:
        return
    surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for p in particles:
        sx = p["wx"] - cam_x
        sy = p["wy"] - cam_y
        if sx < -10 or sx > SCREEN_W + 10 or sy < -10 or sy > SCREEN_H + 10:
            continue
        fade = min(1.0, p["life"] / (p["max_life"] * 0.3))
        alpha = int(145 * fade)
        ex = sx + p["vx"] * 0.045
        ey = sy + p["vy"] * 0.045
        pygame.draw.line(surf, (180, 205, 235, alpha),
                         (int(sx), int(sy)), (int(ex), int(ey)), 1)
    screen.blit(surf, (0, 0))
