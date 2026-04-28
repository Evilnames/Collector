"""Wind leaf-particle system.

Spawns small leaf fragments from visible tree leaf blocks while wind is active.
Particles drift in the wind direction, flutter vertically, and fade out.
"""
import random
import math
import pygame
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H

# Random block positions to probe each frame looking for leaves to spawn from
_SPAWN_PROBES  = 30
# Max live particles on screen
_MAX_PARTICLES = 150
# Seconds a particle lives
_LIFE_MIN = 2.5
_LIFE_MAX = 6.0

# Per-leaf-block-ID color hint (R, G, B)
_LEAF_COLORS = {
    15:   (80,  130, 55),   # TREE_LEAVES
    52:   (60,  100, 60),   # PINE_LEAVES
    54:   (180, 210, 120),  # BIRCH_LEAVES
    56:   (40,  160, 60),   # JUNGLE_LEAVES
    58:   (90,  150, 70),   # WILLOW_LEAVES
    60:   (160, 60,  40),   # REDWOOD_LEAVES
    62:   (90,  160, 80),   # PALM_LEAVES
    64:   (130, 160, 55),   # ACACIA_LEAVES
    202:  (200, 90,  30),   # MAPLE_LEAVES (autumn orange)
    204:  (230, 160, 190),  # CHERRY_LEAVES (pink)
    206:  (60,  120, 70),   # CYPRESS_LEAVES
    208:  (110, 150, 50),   # BAOBAB_LEAVES
    1115: (50,  130, 90),   # MANGROVE_LEAVES
    1117: (70,  110, 70),   # SPRUCE_LEAVES
    1119: (200, 200, 80),   # GINKGO_LEAVES (yellow)
    1121: (60,  140, 70),   # BANYAN_LEAVES
    1123: (100, 160, 70),   # PEAR_LEAVES
    1125: (80,  150, 65),   # FIG_LEAVES
    1127: (90,  160, 60),   # CITRUS_LEAVES
    1129: (80,  140, 55),   # APPLE_LEAVES
    1131: (90,  130, 60),   # POMEGRANATE_LEAVES
}
_DEFAULT_LEAF_COLOR = (80, 130, 55)


def _leaf_color(block_id):
    return _LEAF_COLORS.get(block_id, _DEFAULT_LEAF_COLOR)


def spawn_wind_particles(particles, world, cam_x, cam_y, rng, wind_dir, wind_strength):
    """Probe random visible positions; emit a particle when a leaf block is found."""
    if len(particles) >= _MAX_PARTICLES:
        return

    blocks_x = SCREEN_W // BLOCK_SIZE + 2
    blocks_y = SCREEN_H // BLOCK_SIZE + 2
    # cam_x/cam_y are world-pixel coords of the screen's top-left corner
    cam_bx = int(cam_x) // BLOCK_SIZE
    cam_by = int(cam_y) // BLOCK_SIZE

    for _ in range(_SPAWN_PROBES):
        if len(particles) >= _MAX_PARTICLES:
            break
        bx = cam_bx + rng.randint(0, blocks_x)
        by = cam_by + rng.randint(0, blocks_y)
        bid = world.get_block(bx, by)
        if bid not in world._all_leaves_set:
            continue

        # World-space spawn anywhere inside that leaf block
        wx = bx * BLOCK_SIZE + rng.uniform(2, BLOCK_SIZE - 2)
        wy = by * BLOCK_SIZE + rng.uniform(2, BLOCK_SIZE - 2)

        speed = wind_strength * rng.uniform(35, 80)
        vx    = wind_dir * speed
        vy    = rng.uniform(-15, 10)
        life  = rng.uniform(_LIFE_MIN, _LIFE_MAX)
        size  = rng.randint(3, 5)
        color = _leaf_color(bid)
        wobble       = rng.uniform(3.0, 7.0)
        wobble_phase = rng.uniform(0, math.pi * 2)

        particles.append({
            "wx": wx, "wy": wy,
            "vx": vx, "vy": vy,
            "life": life, "max_life": life,
            "size": size, "color": color,
            "wobble": wobble, "phase": wobble_phase,
            "age": 0.0,
        })


def spawn_passive_leaves(particles, world, cam_x, cam_y, rng, dt):
    """A few leaves drifting down gently even without wind."""
    if len(particles) >= _MAX_PARTICLES or rng.random() > dt * 1.8:
        return
    blocks_x = SCREEN_W // BLOCK_SIZE + 2
    blocks_y = SCREEN_H // BLOCK_SIZE + 2
    cam_bx   = int(cam_x) // BLOCK_SIZE
    cam_by   = int(cam_y) // BLOCK_SIZE
    for _ in range(4):
        bx = cam_bx + rng.randint(0, blocks_x)
        by = cam_by + rng.randint(0, blocks_y)
        bid = world.get_block(bx, by)
        if bid not in world._all_leaves_set:
            continue
        wx = bx * BLOCK_SIZE + rng.uniform(4, BLOCK_SIZE - 4)
        wy = by * BLOCK_SIZE + rng.uniform(4, BLOCK_SIZE - 4)
        particles.append({
            "wx": wx, "wy": wy,
            "vx": rng.uniform(-10, 10), "vy": rng.uniform(-4, 4),
            "life": rng.uniform(2.5, 4.5), "max_life": 3.5,
            "size": rng.randint(2, 3), "color": _leaf_color(bid),
            "wobble": rng.uniform(1.5, 3.5),
            "phase": rng.uniform(0, math.pi * 2),
            "age": 0.0,
        })
        break


def tick_wind_particles(particles, dt):
    """Advance particle physics and expire dead ones in-place."""
    i = 0
    while i < len(particles):
        p = particles[i]
        p["age"]  += dt
        p["life"] -= dt
        if p["life"] <= 0:
            particles.pop(i)
            continue
        p["phase"] += p["wobble"] * dt
        p["vy"]    += 20 * dt           # gentle gravity
        p["vx"]    *= (1 - 0.6 * dt)   # horizontal drag
        flutter_vy  = math.sin(p["phase"]) * 28
        p["wx"] += p["vx"] * dt
        p["wy"] += (p["vy"] + flutter_vy) * dt
        i += 1


def draw_wind_particles(screen, cam_x, cam_y, particles):
    """Draw all live particles onto the screen."""
    if not particles:
        return
    surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for p in particles:
        sx = p["wx"] - cam_x
        sy = p["wy"] - cam_y
        if sx < -8 or sx > SCREEN_W + 8 or sy < -8 or sy > SCREEN_H + 8:
            continue
        fade_in  = min(1.0, p["age"] / 0.25)
        fade_out = min(1.0, p["life"] / 1.2)
        alpha    = int(240 * fade_in * fade_out)
        r, g, b  = p["color"]
        sz       = p["size"]
        pygame.draw.rect(surf, (r, g, b, alpha), (int(sx), int(sy), sz, sz))
    screen.blit(surf, (0, 0))
