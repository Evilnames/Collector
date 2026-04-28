"""Dust and sand particle system.

Spawns blowing sand/dust particles in arid biomes when wind is active.
Particles skim along close to ground level and gradually settle.
"""
import math
import pygame
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, SURFACE_Y

_DUST_BIOMES = frozenset({"desert", "arid_steppe", "canyon"})

_MAX_PARTICLES = 250
_SPAWN_RATE    = 70   # particles per second per unit of wind strength


def _in_dust_biome(world, cam_x):
    bx = int(cam_x) // BLOCK_SIZE + SCREEN_W // (2 * BLOCK_SIZE)
    return world.get_biome(bx) in _DUST_BIOMES


# Sandy color palette — tan to rust
_DUST_COLORS = [
    (195, 170, 120),
    (210, 185, 135),
    (180, 155, 105),
    (220, 195, 145),
    (170, 140,  90),
]


def spawn_dust_particles(particles, world, cam_x, cam_y, rng, dt):
    if not getattr(world, '_wind_active', False):
        return
    if not _in_dust_biome(world, cam_x):
        return
    wind_dir = getattr(world, '_wind_dir', 1)
    wind_str = getattr(world, '_wind_strength', 1.0)

    count = int(_SPAWN_RATE * wind_str * dt)
    slots = _MAX_PARTICLES - len(particles)
    if slots <= 0:
        return

    # Ground reference for this screen position
    ground_py = (SURFACE_Y * BLOCK_SIZE) - cam_y

    for _ in range(min(count, slots)):
        # Spawn near the ground, offset to the upwind edge of the screen
        edge_x = cam_x + ((-wind_dir) * (SCREEN_W * 0.55))
        wx = edge_x + rng.uniform(-40, 40)
        # Height: low to the ground with some variation
        height_off = rng.uniform(0, SCREEN_H * 0.35)
        wy = cam_y + ground_py - height_off

        speed  = wind_str * rng.uniform(50, 140)
        vx     = wind_dir * speed
        vy     = rng.uniform(-20, 15)      # slight vertical drift
        size   = rng.choice([1, 1, 2])
        wobble = rng.uniform(2.0, 5.0)
        phase  = rng.uniform(0, math.pi * 2)
        color  = rng.choice(_DUST_COLORS)
        life   = rng.uniform(1.5, 4.0)

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
        p["vx"] *= (1 - 0.3 * dt)           # horizontal drag
        p["vy"] += 18 * dt                   # gentle gravity settle
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
