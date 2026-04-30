import math as _m
import pygame

from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, PLAYER_W, PLAYER_H
from blocks import LIGHT_EMITTERS, WARM_EMITTERS, GLASS_BLOCKS, OPEN_DOORS, ALL_LEAVES, BUSH_BLOCKS, CROP_BLOCKS
from Render.surface.flags import golden_hour_alphas

# Must match the RGB used in _light_surf.fill() so BLEND_RGBA_MIN doesn't
# create a pure-black square patch around each light (only alpha should vary).
_DR, _DG, _DB = 5, 8, 20


def build_block_gradient(pattern, radius, flicker_frame=0):
    r = radius
    if pattern == "flicker":
        r = radius + int(_m.sin(flicker_frame * 0.524) * 9)
        pattern = "circle"
    size = r * 2 + 1

    if pattern == "circle":
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((_DR, _DG, _DB, 255))
        for ir in range(r, 0, -4):
            alpha = int(255 * (ir / r) ** 0.55)
            pygame.draw.circle(surf, (_DR, _DG, _DB, alpha), (r, r), ir)
        return surf

    if pattern == "soft":
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((_DR, _DG, _DB, 255))
        for ir in range(r, 0, -4):
            alpha = int(255 * (ir / r) ** 0.28)
            pygame.draw.circle(surf, (_DR, _DG, _DB, alpha), (r, r), ir)
        return surf

    if pattern == "dim":
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((_DR, _DG, _DB, 255))
        for ir in range(r, 0, -3):
            alpha = int(255 * (ir / r) ** 0.72)
            pygame.draw.circle(surf, (_DR, _DG, _DB, alpha), (r, r), ir)
        return surf

    if pattern == "wide_oval":
        base = build_block_gradient("circle", r)
        return pygame.transform.scale(base, (r * 4 + 1, r * 2 + 1))

    if pattern == "tall_oval":
        base = build_block_gradient("circle", r)
        return pygame.transform.scale(base, (r * 2 + 1, int(r * 3.2) + 1))

    if pattern == "wide_flat":
        base = build_block_gradient("circle", r)
        return pygame.transform.scale(base, (int(r * 5.0) + 1, int(r * 0.8) + 1))

    if pattern in ("cone_up", "cone_down"):
        surf = build_block_gradient("circle", r).copy()
        w, h = surf.get_size()
        cy = h // 2
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 0))
        if pattern == "cone_up":
            for y in range(cy, h):
                d = min(255, int(255 * ((y - cy) / max(1, r)) * 1.6))
                pygame.draw.line(mask, (0, 0, 0, d), (0, y), (w - 1, y))
        else:
            for y in range(0, cy):
                d = min(255, int(255 * ((cy - y) / max(1, r)) * 1.6))
                pygame.draw.line(mask, (0, 0, 0, d), (0, y), (w - 1, y))
        surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)
        return surf

    if pattern == "cross":
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((_DR, _DG, _DB, 255))
        cx = cy = r
        for arm in range(r, 0, -2):
            ratio = arm / r
            alpha = int(255 * ratio ** 0.45)
            bw = max(5, int(12 * (1 - ratio * 0.5)))
            pygame.draw.line(surf, (_DR, _DG, _DB, alpha), (cx - arm, cy), (cx + arm, cy), bw)
            pygame.draw.line(surf, (_DR, _DG, _DB, alpha), (cx, cy - arm), (cx, cy + arm), bw)
        base_r = r // 3
        for ir in range(base_r, 0, -2):
            alpha = int(255 * (ir / base_r) ** 0.6)
            pygame.draw.circle(surf, (_DR, _DG, _DB, alpha), (cx, cy), ir)
        return surf

    if pattern == "star":
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((_DR, _DG, _DB, 255))
        cx = cy = r
        for ir in range(r, 0, -4):
            alpha = int(255 * (ir / r) ** 0.3)
            pygame.draw.circle(surf, (_DR, _DG, _DB, alpha), (cx, cy), ir)
        for angle_deg in range(0, 360, 45):
            angle = _m.radians(angle_deg)
            dx = _m.cos(angle); dy = _m.sin(angle)
            for arm in range(r, 0, -2):
                ratio = arm / r
                alpha = int(255 * ratio ** 0.4)
                width = max(2, int(5 * (1 - ratio * 0.7)))
                ex = int(cx + dx * arm); ey = int(cy + dy * arm)
                pygame.draw.line(surf, (_DR, _DG, _DB, alpha), (cx, cy), (ex, ey), width)
        return surf

    return build_block_gradient("circle", r)


def build_warm_gradient(radius, pattern, flicker_frame=0):
    """Amber-tinted gradient for the warm light pass (normal-blend, not additive)."""
    r = radius + int(_m.sin(flicker_frame * 0.524) * 6) if pattern == "flicker" else radius
    size = r * 2 + 1
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    max_alpha = 45 if pattern == "flicker" else 30
    for ir in range(r, 0, -3):
        t = 1.0 - (ir / r) ** 0.55
        alpha = int(max_alpha * t)
        pygame.draw.circle(surf, (255, 155, 55, alpha), (r, r), ir)
    return surf


def _draw_indoor_and_glass_shafts(renderer, world, cam_x, cam_y, day_strength):
    """
    Surface-level pass:
      1. Darkens enclosed interior spaces that have no sky view.
      2. Cuts sunbeam shafts downward through glass ceiling tiles.
    day_strength: 0-255, 255 = full noon.
    """
    if day_strength < 5:
        return

    bs = BLOCK_SIZE
    cam_xi = int(cam_x)
    cam_yi = int(cam_y)
    SCAN_ABOVE = 25
    bx0 = cam_xi // bs - 1
    bx1 = (cam_xi + SCREEN_W) // bs + 2
    by0 = max(0, cam_yi // bs - SCAN_ABOVE)
    by1 = min(world.height, (cam_yi + SCREEN_H) // bs + 2)

    darkness_base = max(0, 255 - day_strength)
    INDOOR_ALPHA = min(255, darkness_base + int(day_strength * 0.78))
    LEAF_ALPHA   = min(255, darkness_base + int(day_strength * 0.28))  # subtle tree shade
    MAX_SHAFT = 20

    # Blocks that are fully permeable — never act as ceilings
    _SKY_PASS = GLASS_BLOCKS | OPEN_DOORS | BUSH_BLOCKS | CROP_BLOCKS
    # Leaves create a softer shadow, tracked separately
    _LEAF_CEIL = ALL_LEAVES

    shaft_origins = []  # (bx, glass_by) for skylight beams

    for bx in range(bx0, bx1):
        pending_glass = []
        sky_open = True
        leaf_shade = False  # ceiling was leaves, not solid

        for by in range(by0, by1):
            bid = world.get_block(bx, by)

            if sky_open:
                if bid in GLASS_BLOCKS:
                    pending_glass.append(by)
                elif bid in _LEAF_CEIL:
                    sky_open = False
                    leaf_shade = True
                    for g in pending_glass:
                        shaft_origins.append((bx, g))
                elif bid != 0 and bid not in _SKY_PASS:
                    sky_open = False
                    leaf_shade = False
                    for g in pending_glass:
                        shaft_origins.append((bx, g))
            else:
                sy = by * bs - cam_yi
                if sy + bs < 0 or sy > SCREEN_H:
                    continue
                sx = bx * bs - cam_xi
                alpha = LEAF_ALPHA if leaf_shade else INDOOR_ALPHA
                if bid == 0:
                    pygame.draw.rect(renderer._light_surf, (_DR, _DG, _DB, alpha),
                                     (sx, sy, bs, bs))
                elif bid in GLASS_BLOCKS:
                    glass_alpha = max(darkness_base, alpha // 3)
                    pygame.draw.rect(renderer._light_surf, (_DR, _DG, _DB, glass_alpha),
                                     (sx, sy, bs, bs))
                elif bid in _LEAF_CEIL:
                    # Another leaf layer — don't change shade type, keep going
                    pass

    # Cut sunbeam shafts downward from each skylight glass tile
    for bx, glass_by in shaft_origins:
        sx = bx * bs - cam_xi
        if sx + bs < 0 or sx > SCREEN_W:
            continue
        for depth in range(1, MAX_SHAFT + 1):
            by = glass_by + depth
            if by >= world.height:
                break
            bid = world.get_block(bx, by)
            if bid != 0 and bid not in GLASS_BLOCKS:
                break  # Solid block stops the shaft
            sy = by * bs - cam_yi
            if sy + bs < 0 or sy > SCREEN_H:
                continue
            ratio = 1.0 - (depth / MAX_SHAFT) ** 0.7
            # Shaft cuts indoor darkness; clamp so it never goes below outdoor level
            cut_alpha = max(darkness_base, int(INDOOR_ALPHA * (1.0 - ratio * 0.93)))
            pygame.draw.rect(renderer._light_surf, (_DR, _DG, _DB, cut_alpha),
                             (bx * bs - cam_xi, sy, bs, bs))


def draw_lighting(renderer, player, world, depth, time_of_day=0.0):
    night_alpha = renderer._sky_night_alpha(time_of_day)
    dawn_a, dusk_a = golden_hour_alphas(time_of_day)

    night_factor = 1.0 - (night_alpha / 255.0) * 0.45
    surface_ambient = int(230 * night_factor)

    if depth <= 0:
        darkness = int(night_alpha * 0.72)
        # At noon with no atmospheric effects, only indoor shadows matter
        if night_alpha <= 0 and dawn_a == 0 and dusk_a == 0:
            if world is not None:
                renderer._light_surf.fill((_DR, _DG, _DB, 0))
                _draw_indoor_and_glass_shafts(renderer, world,
                                              renderer.cam_x, renderer.cam_y, 255)
                renderer.screen.blit(renderer._light_surf, (0, 0))
            return
    else:
        ambient  = max(10, surface_ambient - depth * 2)
        darkness = 255 - ambient

    # Atmospheric world tint: warm additive wash during golden hour, before darkness
    golden_a = max(dawn_a, dusk_a)
    if golden_a > 0:
        tint_strength = int(golden_a * 8 // 230)
        if dusk_a > 0:
            tint_col = (80, 35, 0, tint_strength)
        else:
            tint_col = (70, 40, 5, tint_strength)
        renderer._atmos_surf.fill(tint_col)
        renderer.screen.blit(renderer._atmos_surf, (0, 0),
                             special_flags=pygame.BLEND_RGBA_ADD)

    # Cool moonlit darkness (blue-tinted, not pure black)
    renderer._light_surf.fill((5, 8, 20, darkness))

    # Indoor shadows + glass sunbeam shafts (surface only)
    if depth <= 0 and world is not None:
        _draw_indoor_and_glass_shafts(renderer, world,
                                      renderer.cam_x, renderer.cam_y,
                                      max(0, 255 - darkness))

    if depth > 0:
        ambient = max(10, surface_ambient - depth * 2)
        radius  = max(70, 220 - depth)
        if renderer._light_cache_key != (ambient, radius):
            renderer._light_cache_key = (ambient, radius)
            size = radius * 2 + 1
            grad = pygame.Surface((size, size), pygame.SRCALPHA)
            grad.fill((_DR, _DG, _DB, darkness))
            for r in range(radius, 0, -5):
                ratio = r / radius
                brightness = int(ambient + (255 - ambient) * (1 - ratio ** 0.6))
                alpha = 255 - min(255, brightness)
                pygame.draw.circle(grad, (_DR, _DG, _DB, alpha), (radius, radius), r)
            renderer._light_gradient = grad
        px = int(player.x - renderer.cam_x) + PLAYER_W // 2
        py = int(player.y - renderer.cam_y) + PLAYER_H // 2
        renderer._light_surf.blit(renderer._light_gradient, (px - radius, py - radius),
                                  special_flags=pygame.BLEND_RGBA_MIN)

    if world is not None:
        cam_xi = int(renderer.cam_x)
        cam_yi = int(renderer.cam_y)
        extra  = 200
        bx0 = (cam_xi - extra) // BLOCK_SIZE
        bx1 = (cam_xi + SCREEN_W + extra) // BLOCK_SIZE + 1
        by0 = max(0, (cam_yi - extra) // BLOCK_SIZE)
        by1 = min(world.height, (cam_yi + SCREEN_H + extra) // BLOCK_SIZE + 1)
        flicker_frame = (pygame.time.get_ticks() // 80) % 12

        for by in range(by0, by1):
            for bx in range(bx0, bx1):
                for bid in (world.get_block(bx, by), world.get_bg_block(bx, by)):
                    if bid not in LIGHT_EMITTERS:
                        continue
                    light_r, pattern = LIGHT_EMITTERS[bid]
                    ff = flicker_frame if pattern == "flicker" else 0
                    key = (light_r, pattern, ff)
                    if key not in renderer._light_grad_cache:
                        renderer._light_grad_cache[key] = build_block_gradient(pattern, light_r, ff)
                    grad = renderer._light_grad_cache[key]
                    gw, gh = grad.get_size()
                    sx = bx * BLOCK_SIZE + BLOCK_SIZE // 2 - cam_xi
                    sy = by * BLOCK_SIZE + BLOCK_SIZE // 2 - cam_yi
                    renderer._light_surf.blit(grad, (sx - gw // 2, sy - gh // 2),
                                              special_flags=pygame.BLEND_RGBA_MIN)

    # Warm amber pass — only meaningful when there is some darkness to contrast against
    if world is not None and darkness > 10:
        renderer._warm_surf.fill((0, 0, 0, 0))
        warm_drawn = False
        for by in range(by0, by1):
            for bx in range(bx0, bx1):
                for bid in (world.get_block(bx, by), world.get_bg_block(bx, by)):
                    if bid not in WARM_EMITTERS:
                        continue
                    warm_drawn = True
                    light_r, pattern = WARM_EMITTERS[bid]
                    ff = flicker_frame if pattern == "flicker" else 0
                    key = ("warm", light_r, pattern, ff)
                    if key not in renderer._light_grad_cache:
                        renderer._light_grad_cache[key] = build_warm_gradient(light_r, pattern, ff)
                    grad = renderer._light_grad_cache[key]
                    gw, gh = grad.get_size()
                    sx = bx * BLOCK_SIZE + BLOCK_SIZE // 2 - cam_xi
                    sy = by * BLOCK_SIZE + BLOCK_SIZE // 2 - cam_yi
                    renderer._warm_surf.blit(grad, (sx - gw // 2, sy - gh // 2),
                                             special_flags=pygame.BLEND_RGBA_MAX)
        # Glass relay: warm emitters adjacent to glass leak warm glow through it
        for by in range(by0, by1):
            for bx in range(bx0, bx1):
                for bid in (world.get_block(bx, by), world.get_bg_block(bx, by)):
                    if bid not in WARM_EMITTERS:
                        continue
                    warm_r = WARM_EMITTERS[bid][0]
                    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        nbid = world.get_block(bx + dx, by + dy)
                        if nbid not in GLASS_BLOCKS:
                            continue
                        warm_drawn = True
                        relay_r = max(20, warm_r // 2)
                        relay_key = ("glass_relay", relay_r)
                        if relay_key not in renderer._light_grad_cache:
                            renderer._light_grad_cache[relay_key] = build_warm_gradient(relay_r, "soft", 0)
                        grad = renderer._light_grad_cache[relay_key]
                        gw, gh = grad.get_size()
                        sx = (bx + dx) * BLOCK_SIZE + BLOCK_SIZE // 2 - cam_xi
                        sy = (by + dy) * BLOCK_SIZE + BLOCK_SIZE // 2 - cam_yi
                        renderer._warm_surf.blit(grad, (sx - gw // 2, sy - gh // 2),
                                                 special_flags=pygame.BLEND_RGBA_MAX)
        if warm_drawn:
            renderer.screen.blit(renderer._warm_surf, (0, 0))

    # Firefly glow — punch soft holes in the darkness overlay
    if night_alpha > 30 and world is not None and hasattr(world, 'insects'):
        for ins in world.insects:
            if ins.WING_TYPE != "firefly" or ins.spooked:
                continue
            sx = int(ins.x) - cam_xi
            sy = int(ins.y) - cam_yi
            if sx < -80 or sx > SCREEN_W + 80 or sy < -80 or sy > SCREEN_H + 80:
                continue
            pulse = abs(_m.sin(ins._hover_phase * 0.5))
            r = 10 + int(pulse * 12)
            key = ("ff", r)
            if key not in renderer._light_grad_cache:
                renderer._light_grad_cache[key] = build_block_gradient("soft", r)
            grad = renderer._light_grad_cache[key]
            gw, gh = grad.get_size()
            tail_sx = sx + ins.W - 3
            tail_sy = sy + ins.H // 2
            renderer._light_surf.blit(grad, (tail_sx - gw // 2, tail_sy - gh // 2),
                                      special_flags=pygame.BLEND_RGBA_MIN)

    renderer.screen.blit(renderer._light_surf, (0, 0))
