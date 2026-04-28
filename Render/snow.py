"""Snow particle system.

Spawns gently falling snowflakes in snow biomes at all times, with
additional horizontal blowing snow when wind is active.
"""
import math
import pygame
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H

_SNOW_BIOMES = frozenset({"tundra", "alpine_mountain"})

_MAX_PARTICLES = 350
_PASSIVE_RATE  = 30   # flakes per second during calm
_BLOWING_RATE  = 80   # extra flakes per second when wind is active


def _in_snow_biome(world, cam_x):
    bx = int(cam_x) // BLOCK_SIZE + SCREEN_W // (2 * BLOCK_SIZE)
    return world.get_biome(bx) in _SNOW_BIOMES


def spawn_snow_particles(particles, world, cam_x, cam_y, rng, dt):
    if not _in_snow_biome(world, cam_x):
        return
    wind_active = getattr(world, '_wind_active', False)
    wind_dir    = getattr(world, '_wind_dir', 1)
    wind_str    = getattr(world, '_wind_strength', 1.0) if wind_active else 0.0

    rate  = _PASSIVE_RATE + _BLOWING_RATE * wind_str * 0.5
    count = int(rate * dt)
    slots = _MAX_PARTICLES - len(particles)
    if slots <= 0:
        return
    for _ in range(min(count, slots)):
        # Spawn across and slightly above the top of screen
        wx = cam_x + rng.uniform(-20, SCREEN_W + 20)
        wy = cam_y + rng.uniform(-20, SCREEN_H * 0.1)
        size   = rng.choice([1, 1, 1, 2])
        wobble = rng.uniform(0.8, 2.2)
        phase  = rng.uniform(0, math.pi * 2)
        # Blowing adds horizontal velocity matching wind
        vx = wind_dir * wind_str * rng.uniform(20, 60) if wind_active else rng.uniform(-8, 8)
        vy = rng.uniform(28, 65)
        life = rng.uniform(3.5, 7.0)
        particles.append({
            "wx": wx, "wy": wy,
            "vx": vx, "vy": vy,
            "size": size, "wobble": wobble, "phase": phase,
            "life": life, "max_life": life,
        })


def tick_snow_particles(particles, cam_y, dt):
    i = 0
    while i < len(particles):
        p = particles[i]
        p["life"] -= dt
        if p["life"] <= 0 or p["wy"] > cam_y + SCREEN_H + 16:
            particles.pop(i)
            continue
        p["phase"] += p["wobble"] * dt
        p["vx"] *= (1 - 0.25 * dt)          # gentle horizontal drag
        flutter_vx = math.sin(p["phase"]) * 12
        p["wx"] += (p["vx"] + flutter_vx) * dt
        p["wy"] += p["vy"] * dt
        i += 1


def draw_snow_particles(screen, cam_x, cam_y, particles):
    if not particles:
        return
    surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for p in particles:
        sx = p["wx"] - cam_x
        sy = p["wy"] - cam_y
        if sx < -4 or sx > SCREEN_W + 4 or sy < -4 or sy > SCREEN_H + 4:
            continue
        fade = min(1.0, p["life"] / (p["max_life"] * 0.4))
        alpha = int(210 * fade)
        sz = p["size"]
        pygame.draw.rect(surf, (230, 240, 255, alpha), (int(sx), int(sy), sz, sz))
    screen.blit(surf, (0, 0))
