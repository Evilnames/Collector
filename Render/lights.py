import math as _m
import pygame

from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, PLAYER_W, PLAYER_H
from blocks import LIGHT_EMITTERS, WARM_EMITTERS
from Render.surface.flags import golden_hour_alphas


def build_block_gradient(pattern, radius, flicker_frame=0):
    r = radius
    if pattern == "flicker":
        r = radius + int(_m.sin(flicker_frame * 0.524) * 9)
        pattern = "circle"
    size = r * 2 + 1

    if pattern == "circle":
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 255))
        for ir in range(r, 0, -4):
            alpha = int(255 * (ir / r) ** 0.55)
            pygame.draw.circle(surf, (0, 0, 0, alpha), (r, r), ir)
        return surf

    if pattern == "soft":
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 255))
        for ir in range(r, 0, -4):
            alpha = int(255 * (ir / r) ** 0.28)
            pygame.draw.circle(surf, (0, 0, 0, alpha), (r, r), ir)
        return surf

    if pattern == "dim":
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 255))
        for ir in range(r, 0, -3):
            alpha = int(255 * (ir / r) ** 0.72)
            pygame.draw.circle(surf, (0, 0, 0, alpha), (r, r), ir)
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
        surf.fill((0, 0, 0, 255))
        cx = cy = r
        for arm in range(r, 0, -2):
            ratio = arm / r
            alpha = int(255 * ratio ** 0.45)
            bw = max(5, int(12 * (1 - ratio * 0.5)))
            pygame.draw.line(surf, (0, 0, 0, alpha), (cx - arm, cy), (cx + arm, cy), bw)
            pygame.draw.line(surf, (0, 0, 0, alpha), (cx, cy - arm), (cx, cy + arm), bw)
        base_r = r // 3
        for ir in range(base_r, 0, -2):
            alpha = int(255 * (ir / base_r) ** 0.6)
            pygame.draw.circle(surf, (0, 0, 0, alpha), (cx, cy), ir)
        return surf

    if pattern == "star":
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 255))
        cx = cy = r
        for ir in range(r, 0, -4):
            alpha = int(255 * (ir / r) ** 0.3)
            pygame.draw.circle(surf, (0, 0, 0, alpha), (cx, cy), ir)
        for angle_deg in range(0, 360, 45):
            angle = _m.radians(angle_deg)
            dx = _m.cos(angle); dy = _m.sin(angle)
            for arm in range(r, 0, -2):
                ratio = arm / r
                alpha = int(255 * ratio ** 0.4)
                width = max(2, int(5 * (1 - ratio * 0.7)))
                ex = int(cx + dx * arm); ey = int(cy + dy * arm)
                pygame.draw.line(surf, (0, 0, 0, alpha), (cx, cy), (ex, ey), width)
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


def draw_lighting(renderer, player, world, depth, time_of_day=0.0):
    night_alpha = renderer._sky_night_alpha(time_of_day)
    dawn_a, dusk_a = golden_hour_alphas(time_of_day)

    night_factor = 1.0 - (night_alpha / 255.0) * 0.45
    surface_ambient = int(230 * night_factor)

    if depth <= 0:
        if night_alpha <= 0 and dawn_a == 0 and dusk_a == 0:
            return
        darkness = int(night_alpha * 0.72)
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

    if depth > 0:
        ambient = max(10, surface_ambient - depth * 2)
        radius  = max(70, 220 - depth)
        if renderer._light_cache_key != (ambient, radius):
            renderer._light_cache_key = (ambient, radius)
            size = radius * 2 + 1
            grad = pygame.Surface((size, size), pygame.SRCALPHA)
            grad.fill((0, 0, 0, darkness))
            for r in range(radius, 0, -5):
                ratio = r / radius
                brightness = int(ambient + (255 - ambient) * (1 - ratio ** 0.6))
                alpha = 255 - min(255, brightness)
                pygame.draw.circle(grad, (0, 0, 0, alpha), (radius, radius), r)
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
