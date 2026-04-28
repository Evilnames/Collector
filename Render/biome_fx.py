"""Biome-specific screen effects: color grading overlay and heat shimmer."""
import math
import pygame
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, SURFACE_Y

# ---------------------------------------------------------------------------
# Biome color grading
# (R, G, B, alpha) — alpha should stay in the 10–25 range to stay subtle
# ---------------------------------------------------------------------------
_BIOME_GRADE = {
    "desert":          (230, 185, 100, 22),
    "arid_steppe":     (215, 175, 110, 18),
    "canyon":          (200, 130,  80, 20),
    "savanna":         (200, 180, 110, 15),
    "tundra":          (155, 195, 235, 18),
    "alpine_mountain": (160, 200, 240, 15),
    "rocky_mountain":  (160, 165, 175, 12),
    "jungle":          ( 80, 155,  80, 14),
    "tropical":        ( 90, 160,  95, 16),
    "wetland":         (100, 140, 100, 14),
    "swamp":           (100, 130,  75, 20),
    "boreal":          (120, 155, 140, 12),
    "birch_forest":    (170, 195, 150, 10),
    "wasteland":       (130, 115, 140, 18),
    "beach":           (220, 210, 155, 14),
    "mediterranean":   (205, 175, 120, 14),
    "east_asian":      (140, 170, 155, 12),
    "south_asian":     (200, 160, 110, 16),
}

_LERP_SPEED = 0.8   # fraction per second to blend toward target color


def _screen_center_biome(world, cam_x):
    bx = int(cam_x) // BLOCK_SIZE + SCREEN_W // (2 * BLOCK_SIZE)
    return world.get_biome(bx)


def update_grade(renderer, world, dt):
    """Lerp renderer._grade_rgba toward the target biome color."""
    biome = _screen_center_biome(world, renderer.cam_x)
    tr, tg, tb, ta = _BIOME_GRADE.get(biome, (0, 0, 0, 0))
    cr, cg, cb, ca = renderer._grade_rgba
    k = min(1.0, _LERP_SPEED * dt)
    renderer._grade_rgba = (
        cr + (tr - cr) * k,
        cg + (tg - cg) * k,
        cb + (tb - cb) * k,
        ca + (ta - ca) * k,
    )


def draw_grade(renderer):
    """Draw the current lerped color grade over the whole screen."""
    r, g, b, a = renderer._grade_rgba
    ia = int(a)
    if ia <= 0:
        return
    surf = renderer._grade_surf
    surf.fill((int(r), int(g), int(b)))
    surf.set_alpha(ia)
    renderer.screen.blit(surf, (0, 0))


# ---------------------------------------------------------------------------
# Heat shimmer
# ---------------------------------------------------------------------------
_SHIMMER_BIOMES = frozenset({"desert", "arid_steppe", "canyon"})

# Vertical extent of the shimmer band around ground level (px)
_SHIMMER_ABOVE = 55
_SHIMMER_BELOW = 35
_SHIMMER_MAX_PX = 3   # maximum horizontal pixel shift per row


def draw_shimmer(renderer, world, dt):
    """Distort a horizontal strip near the ground surface in hot biomes."""
    biome = _screen_center_biome(world, renderer.cam_x)
    if biome not in _SHIMMER_BIOMES:
        return

    ground_sy = SURFACE_Y * BLOCK_SIZE - int(renderer.cam_y)
    strip_top = ground_sy - _SHIMMER_ABOVE
    strip_bot = ground_sy + _SHIMMER_BELOW
    # Nothing to do if the band is off-screen
    if strip_bot < 0 or strip_top > SCREEN_H:
        return

    visible_top = max(0, strip_top)
    visible_bot = min(SCREEN_H, strip_bot)
    visible_h   = visible_bot - visible_top
    if visible_h <= 0:
        return

    screen = renderer.screen
    rect   = pygame.Rect(0, visible_top, SCREEN_W, visible_h)
    strip  = screen.subsurface(rect).copy()

    t = pygame.time.get_ticks() / 1000.0
    for row in range(visible_h):
        world_y = visible_top + row
        # Shimmer weakens toward the edges of the band
        band_center = (strip_top + strip_bot) / 2
        edge_fade   = 1.0 - abs(world_y - band_center) / max(1, (_SHIMMER_ABOVE + _SHIMMER_BELOW) / 2)
        strength = _SHIMMER_MAX_PX * edge_fade
        offset = int(math.sin(t * 2.8 + world_y * 0.13) * strength)
        if offset == 0:
            continue
        src_x   = max(0, -offset)
        blit_x  = max(0, offset)
        blit_w  = SCREEN_W - abs(offset)
        if blit_w > 0:
            screen.blit(strip, (blit_x, world_y),
                        pygame.Rect(src_x, row, blit_w, 1))
