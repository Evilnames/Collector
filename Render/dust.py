"""Dust and sand particle system.

Spawns blowing sand/dust particles in arid biomes when wind is active.
Particles skim along close to ground level and gradually settle.

During stormy weather a full sandstorm fires: particle count jumps,
speed increases, particles fill the entire screen height, and
draw_sandstorm_overlay() paints a tan visibility haze.
"""
import math
import pygame
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, SURFACE_Y

_DUST_BIOMES = frozenset({"desert", "arid_steppe", "canyon"})

_MAX_PARTICLES       = 600
_SPAWN_RATE          = 70    # particles/s per unit wind strength (non-storm)
_STORM_RATE          = 220   # particles/s during sandstorm (flat, wind implied)
_SANDSTORM_MAX_ALPHA = 130   # tan overlay alpha (0-255)


def _in_dust_biome(world, cam_x):
    bx = int(cam_x) // BLOCK_SIZE + SCREEN_W // (2 * BLOCK_SIZE)
    return world.get_biome(bx) in _DUST_BIOMES


def _is_sandstorm(world):
    return (getattr(world, '_weather_state', '') == 'stormy'
            and getattr(world, '_wind_active', False))


# Sandy color palette — tan to rust
_DUST_COLORS = [
    (195, 170, 120),
    (210, 185, 135),
    (180, 155, 105),
    (220, 195, 145),
    (170, 140,  90),
]

# Slightly darker/redder palette for full sandstorm
_STORM_COLORS = [
    (200, 160,  90),
    (215, 170, 100),
    (185, 145,  80),
    (225, 180, 110),
    (175, 130,  70),
    (160, 115,  60),
]


def spawn_dust_particles(particles, world, cam_x, cam_y, rng, dt):
    if not _in_dust_biome(world, cam_x):
        return
    wind_active = getattr(world, '_wind_active', False)
    sandstorm   = _is_sandstorm(world)

    if not wind_active and not sandstorm:
        return

    wind_dir = getattr(world, '_wind_dir', 1)
    wind_str = getattr(world, '_wind_strength', 1.0)

    if sandstorm:
        count = int(_STORM_RATE * dt)
    else:
        count = int(_SPAWN_RATE * wind_str * dt)

    slots = _MAX_PARTICLES - len(particles)
    if slots <= 0:
        return

    ground_py = (SURFACE_Y * BLOCK_SIZE) - cam_y

    for _ in range(min(count, slots)):
        edge_x = cam_x + ((-wind_dir) * (SCREEN_W * 0.55))
        wx = edge_x + rng.uniform(-40, 40)

        if sandstorm:
            # Fill entire screen height, not just near ground
            height_off = rng.uniform(0, SCREEN_H * 0.95)
            speed  = wind_str * rng.uniform(120, 320)
            size   = rng.choice([1, 1, 2, 2, 3])
            wobble = rng.uniform(3.0, 7.0)
            life   = rng.uniform(0.8, 2.5)
            color  = rng.choice(_STORM_COLORS)
        else:
            height_off = rng.uniform(0, SCREEN_H * 0.35)
            speed  = wind_str * rng.uniform(50, 140)
            size   = rng.choice([1, 1, 2])
            wobble = rng.uniform(2.0, 5.0)
            life   = rng.uniform(1.5, 4.0)
            color  = rng.choice(_DUST_COLORS)

        wy  = cam_y + ground_py - height_off
        vx  = wind_dir * speed
        vy  = rng.uniform(-20, 15)
        phase = rng.uniform(0, math.pi * 2)

        particles.append({
            "wx": wx, "wy": wy,
            "vx": vx, "vy": vy,
            "size": size, "wobble": wobble, "phase": phase,
            "color": color,
            "life": life, "max_life": life,
        })


def tick_dust_particles(particles, dt):
    i = 0
    while i < len(particles):
        p = particles[i]
        p["life"] -= dt
        if p["life"] <= 0:
            particles.pop(i)
            continue
        p["phase"] += p["wobble"] * dt
        p["vx"] *= (1 - 0.3 * dt)
        p["vy"] += 18 * dt
        flutter_vy = math.sin(p["phase"]) * 15
        p["wx"] += p["vx"] * dt
        p["wy"] += (p["vy"] + flutter_vy) * dt
        i += 1


def draw_dust_particles(screen, cam_x, cam_y, particles):
    if not particles:
        return
    surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for p in particles:
        sx = p["wx"] - cam_x
        sy = p["wy"] - cam_y
        if sx < -4 or sx > SCREEN_W + 4 or sy < -4 or sy > SCREEN_H + 4:
            continue
        fade = min(1.0, p["life"] / (p["max_life"] * 0.5))
        alpha = int(180 * fade)
        r, g, b = p["color"]
        sz = p["size"]
        pygame.draw.rect(surf, (r, g, b, alpha), (int(sx), int(sy), sz, sz))
    screen.blit(surf, (0, 0))


def draw_sandstorm_overlay(screen, world, cam_x):
    """Tan haze overlay that reduces visibility during a sandstorm."""
    if not _in_dust_biome(world, cam_x):
        return
    if not _is_sandstorm(world):
        return
    wind_str = getattr(world, '_wind_strength', 1.0)
    alpha = int(_SANDSTORM_MAX_ALPHA * min(1.0, wind_str / 2.0))
    if alpha <= 0:
        return
    surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    surf.fill((200, 165, 90, alpha))
    screen.blit(surf, (0, 0))
