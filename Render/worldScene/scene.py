import math
import pygame
import random as _rnd
from blocks import (AIR, WATER, FISHING_SPOT_BLOCK, TILLED_SOIL, GRASS, DIRT, SAND, SNOW,
                    ALL_LOGS, ALL_LEAVES, ALL_FRUIT_CLUSTERS, STONE,
                    ELEVATOR_CABLE_BLOCK, LADDER, ELEVATOR_STOP_BLOCK,
                    MINE_TRACK_BLOCK, MINE_TRACK_STOP_BLOCK,
                    WOOD_DOOR_OPEN, IRON_DOOR_OPEN,
                    COBALT_DOOR_OPEN, CRIMSON_CEDAR_DOOR_OPEN,
                    TEAL_DOOR_OPEN, SAFFRON_DOOR_OPEN,
                    STUDDED_OAK_DOOR_OPEN, VERMILION_DOOR_OPEN,
                    SHOJI_DOOR_OPEN, GILDED_DOOR_OPEN,
                    BRONZE_DOOR_OPEN, SWAHILI_DOOR_OPEN,
                    SANDALWOOD_DOOR_OPEN, STONE_SLAB_DOOR_OPEN,
                    TOWN_FLAG_BLOCK, OUTPOST_FLAG_BLOCK, BANNER_BLOCK,
                    WILDFLOWER_PATCH,
                    RESOURCE_BLOCKS,
                    LIMESTONE_STONE, GRANITE_STONE, BASALT_STONE, MAGMATIC_STONE,
                    CLOUD_CIRRUS, CLOUD_CUMULUS, CLOUD_STRATUS, CLOUD_STORM,
                    CORAL_FRAGMENT_BLOCK, CORAL_GROWING, CORAL_FULL,
                    KELP_BLOCK, SEASHELL_BLOCK, SEA_ANEMONE,
                    BIOLUME_DEEP_BLOCK, OCEAN_ROCK)

# Blocks that sit in place of WATER — need the water surface drawn first
_OCEAN_DECOR_BLOCKS = frozenset((
    CORAL_FRAGMENT_BLOCK, CORAL_GROWING, CORAL_FULL,
    KELP_BLOCK, SEASHELL_BLOCK, SEA_ANEMONE,
    BIOLUME_DEEP_BLOCK, OCEAN_ROCK,
))
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, PLAYER_W, PLAYER_H, ROCK_WARM_ZONE, SURFACE_Y
from world import get_ocean_depth_zone
from block_shapes import blit_shaped
from Render.worldScene.art import (draw_all_sculptures, draw_all_tapestries,
                                    draw_pottery_displays, draw_wildflower_displays,
                                    draw_garden_blocks)

_OPEN_DOORS = (WOOD_DOOR_OPEN, IRON_DOOR_OPEN,
               COBALT_DOOR_OPEN, CRIMSON_CEDAR_DOOR_OPEN,
               TEAL_DOOR_OPEN, SAFFRON_DOOR_OPEN,
               STUDDED_OAK_DOOR_OPEN, VERMILION_DOOR_OPEN,
               SHOJI_DOOR_OPEN, GILDED_DOOR_OPEN,
               BRONZE_DOOR_OPEN, SWAHILI_DOOR_OPEN,
               SANDALWOOD_DOOR_OPEN, STONE_SLAB_DOOR_OPEN)

_SHIMMER_BLOCKS = None

# --- Cloud drift rates (pixels per second per layer) ---
_CLOUD_DRIFT_RATES = {
    CLOUD_CIRRUS:  3.0,
    CLOUD_CUMULUS: 1.8,
    CLOUD_STRATUS: 0.9,
    CLOUD_STORM:   0.5,
}

# --- Procedural cloud surface builder (cached by (w, h, bid, variant)) ---
_cloud_surf_cache = {}

def _make_cloud_surf(w, h, bid, variant=0):
    key = (w, h, bid, variant)
    if key in _cloud_surf_cache:
        return _cloud_surf_cache[key]
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    v = variant % 8
    # Seeded RNG so each (w,h,bid,variant) combo is deterministic but varied
    rng = _rnd.Random((w * 31 + h * 97 + bid * 7 + v * 13) & 0x7FFFFFFF)

    if bid == CLOUD_CIRRUS:
        # Thin horizontal brushstrokes — fade at both ends, no central blob.
        # h is only 16-22px so shapes must stay very thin.
        alpha = 125 + v * 8
        cr, cg, cb = 218, 236, 255
        # One main sweep spanning most of the width, vertically centred
        pygame.draw.ellipse(s, (cr, cg, cb, alpha),
                            (w // 8, h // 4, w * 3 // 4, h // 2))
        # Trailing wisp off one end (direction varies by variant)
        if v < 4:
            pygame.draw.ellipse(s, (cr, cg, cb, alpha - 55),
                                (0, h // 2, w // 3, h // 3))
        else:
            pygame.draw.ellipse(s, (cr, cg, cb, alpha - 55),
                                (w * 2 // 3, h // 4, w // 3, h // 3))
        # A second faint streak slightly offset for depth
        sx = rng.randint(w // 6, w // 3)
        pygame.draw.ellipse(s, (cr, cg, cb, alpha - 70),
                            (sx, h // 3 + rng.randint(0, h // 5),
                             w - sx - rng.randint(0, w // 6), max(3, h // 4)))

    elif bid == CLOUD_CUMULUS:
        # Flat bottom, rounded puffy top — the classic cumulus silhouette.
        # Strategy: circles overlapping across the top half give the cauliflower
        # top; a filled body underneath gives the flat-bottomed mass.
        cr, cg, cb   = 244, 244, 250   # body
        sr, sg, sb   = 215, 215, 228   # shadow underside
        br, bg, bb   = 255, 255, 255   # sunlit top

        # Body: wide ellipse anchored at the bottom
        pygame.draw.ellipse(s, (cr, cg, cb, 200), (0, h // 2, w, h // 2))
        # Fill so the very bottom edge reads flat rather than curved
        pygame.draw.rect(s, (cr, cg, cb, 200), (w // 8, h * 3 // 5, w * 3 // 4, h // 3))

        # Puffy top: overlapping circles whose centres sit at mid-height
        bump_r = max(7, h * 2 // 5)
        bump_n = max(2, w // bump_r + (v % 3))
        for i in range(bump_n):
            cx = int(w * (2 * i + 1) / (2 * bump_n))
            cy = h // 2
            r_i = bump_r + rng.randint(-max(1, h // 12), max(1, h // 12))
            pygame.draw.circle(s, (cr, cg, cb, 205), (cx, cy), max(5, r_i))

        # Darker underside — drawn AFTER the body so it sits on the bottom
        pygame.draw.ellipse(s, (sr, sg, sb, 170),
                            (w // 10, h * 3 // 5, w * 4 // 5, h * 2 // 7))

        # Sunlit highlight on the topmost bubble, slightly off-centre
        hx = rng.randint(w // 4, w // 2)
        pygame.draw.ellipse(s, (br, bg, bb, 190),
                            (hx, max(0, h // 2 - bump_r + 2),
                             max(8, bump_r), max(5, bump_r // 2)))

    elif bid == CLOUD_STRATUS:
        # Featureless flat gray sheet — no interior detail, just edge-fade.
        # Heavier and darker for variants 4-7.
        dark = v // 4   # 0 = lighter, 1 = heavier overcast
        cr = 192 - dark * 28
        cg = 197 - dark * 24
        cb = 208 - dark * 20
        alpha = 155 + dark * 35

        # Single flat body ellipse
        pygame.draw.ellipse(s, (cr, cg, cb, alpha),
                            (0, h // 5, w, h * 3 // 5))
        # Rect fill so the centre reads as a flat band, not a lens shape
        pygame.draw.rect(s, (cr, cg, cb, alpha),
                         (w // 8, h // 3, w * 3 // 4, h // 3))
        # Barely perceptible lighter centre (thin part lets more light through)
        pygame.draw.ellipse(s, (min(255, cr + 12), min(255, cg + 10),
                                min(255, cb + 8), min(255, alpha + 10)),
                            (w // 3, h * 2 // 5, w // 3, h // 5))

    elif bid == CLOUD_STORM:
        # Heavy dark mass — uniformly dark, NO bright interior highlights.
        # Slightly lighter at the very top where the cloud is thinner;
        # darkest at the flat-ish bottom (the ominous underside).
        cr, cg, cb   = 85, 80, 102    # main body
        dr, dg, db   = 62, 58,  80    # dark underside
        tr, tg, tb   = 105, 100, 122  # faint top (only slightly lighter)

        # Main rounded mass
        pygame.draw.ellipse(s, (cr, cg, cb, 218), (0, h // 5, w, h * 4 // 5))
        pygame.draw.ellipse(s, (cr, cg, cb, 218), (w // 8, 0, w * 3 // 4, h * 3 // 4))

        # Dark underside — the threatening flat belly
        pygame.draw.ellipse(s, (dr, dg, db, 225),
                            (w // 8, h * 3 // 5, w * 3 // 4, h * 2 // 7))
        pygame.draw.rect(s, (dr, dg, db, 215),
                         (w // 5, h * 2 // 3, w * 3 // 5, h // 6))

        # Very subtle top brightening — ambient sky light on the crown
        pygame.draw.ellipse(s, (tr, tg, tb, 160),
                            (w // 4, 0, w // 2, h // 4))

    _cloud_surf_cache[key] = s
    return s

# --- Horizon parallax cloud helpers ---
def _ensure_horizon_clouds(renderer, world_seed):
    if getattr(renderer, '_h_cloud_seed', None) == world_seed:
        return
    renderer._h_cloud_seed = world_seed
    rng = _rnd.Random(world_seed ^ 0xB0BAFAD)
    shapes = []
    for _ in range(60):
        w = rng.randint(55, 260)
        h = rng.randint(12, 52)
        base = rng.choice([(210, 220, 235), (195, 205, 220),
                           (230, 230, 235), (180, 188, 200), (215, 215, 225)])
        alpha = rng.randint(50, 105)
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (*base, alpha), (0, 0, w, h))
        iw, ih = max(4, w - 18), max(2, h - 8)
        pygame.draw.ellipse(s, (*base, min(255, alpha + 28)),
                            ((w - iw) // 2, (h - ih) // 2, iw, ih))
        shapes.append(s)
    renderer._h_cloud_shapes = shapes


def _draw_horizon_clouds(screen, renderer, cam_xi, cam_yi, world_seed):
    _ensure_horizon_clouds(renderer, world_seed)
    shapes = renderer._h_cloud_shapes
    n = len(shapes)
    horizon_base_sy = SURFACE_Y * BLOCK_SIZE - cam_yi - 5
    _PARALLAX = 0.22
    _GRID = 130  # cloud columns every 130px in parallax space
    eff_x = int(cam_xi * _PARALLAX)
    col_start = eff_x // _GRID
    for col in range(col_start - 2, col_start + (SCREEN_W // _GRID) + 4):
        wx = col * _GRID
        key = (world_seed ^ wx ^ 0xC10AD) & 0xFFFF
        if key > 0x7FFF:
            shape_idx = key % n
            surf = shapes[shape_idx]
            dy = (key * 17 & 0xFF) % 70 - 20
            sx = wx - eff_x
            screen.blit(surf, (sx, horizon_base_sy + dy))


# -----------------------------------------------
_wire_hud_font = None
_wire_hud_surf = None
_wire_hint_surf = None


def _draw_wire_mode_hud(screen):
    global _wire_hud_font, _wire_hud_surf
    if _wire_hud_surf is None:
        _wire_hud_font = pygame.font.SysFont(None, 20)
        lbl = _wire_hud_font.render(" WIRE MODE  [\\] to exit ", True, (0, 220, 255))
        bg = pygame.Surface((lbl.get_width() + 6, lbl.get_height() + 4))
        bg.fill((8, 8, 24))
        pygame.draw.rect(bg, (0, 180, 210), bg.get_rect(), 1)
        bg.blit(lbl, (3, 2))
        _wire_hud_surf = bg
    screen.blit(_wire_hud_surf, (8, 8))


def _draw_wire_hint(screen):
    global _wire_hint_surf
    if _wire_hint_surf is None:
        font = pygame.font.SysFont(None, 20)
        lbl = font.render(" [\\] Wire Mode ", True, (160, 200, 220))
        bg = pygame.Surface((lbl.get_width() + 6, lbl.get_height() + 4))
        bg.fill((8, 8, 24))
        pygame.draw.rect(bg, (60, 100, 130), bg.get_rect(), 1)
        bg.blit(lbl, (3, 2))
        _wire_hint_surf = bg
    screen.blit(_wire_hint_surf, (8, 8))

def _get_shimmer_blocks():
    global _SHIMMER_BLOCKS
    if _SHIMMER_BLOCKS is None:
        from blocks import CRYSTAL_ORE, RUBY_ORE, GEM_DEPOSIT, CAVE_CRYSTAL
        _SHIMMER_BLOCKS = {
            CRYSTAL_ORE:  (200, 255, 255),
            RUBY_ORE:     (255, 190, 190),
            GEM_DEPOSIT:  (230, 200, 255),
            CAVE_CRYSTAL: (190, 250, 255),
        }
    return _SHIMMER_BLOCKS


def _los_clear(world, px, py, tx, ty):
    dx = tx - px
    dy = ty - py
    nx = abs(dx)
    ny = abs(dy)
    sign_x = 1 if dx > 0 else -1
    sign_y = 1 if dy > 0 else -1
    x, y = px, py
    ix = iy = 0
    while ix < nx or iy < ny:
        step_x = (0.5 + ix) / nx if nx else float('inf')
        step_y = (0.5 + iy) / ny if ny else float('inf')
        if step_x < step_y:
            x += sign_x
            ix += 1
        else:
            y += sign_y
            iy += 1
        if x == tx and y == ty:
            break
        if world.get_block(x, y) != AIR:
            return False
    return True


def draw_world(renderer, world, player=None):
    from Render.surface.flags import golden_hour_alphas
    screen = renderer.screen
    screen.blit(renderer._sky_surf, (0, 0))
    time_of_day = getattr(world, 'time_of_day', 0.0)
    night_alpha = renderer._sky_night_alpha(time_of_day)
    if night_alpha > 0:
        renderer._sky_night_surf.set_alpha(night_alpha)
        screen.blit(renderer._sky_night_surf, (0, 0))
    dawn_a, dusk_a = golden_hour_alphas(time_of_day)
    if dawn_a > 0:
        renderer._dawn_sky_surf.set_alpha(dawn_a)
        screen.blit(renderer._dawn_sky_surf, (0, 0))
    if dusk_a > 0:
        renderer._dusk_sky_surf.set_alpha(dusk_a)
        screen.blit(renderer._dusk_sky_surf, (0, 0))

    cam_xi = int(renderer.cam_x)
    cam_yi = int(renderer.cam_y)

    _draw_horizon_clouds(screen, renderer, cam_xi, cam_yi, world.seed)

    bx0 = cam_xi // BLOCK_SIZE
    bx1 = (cam_xi + SCREEN_W) // BLOCK_SIZE + 2
    by0 = max(0, cam_yi // BLOCK_SIZE)
    by1 = min(world.height, (cam_yi + SCREEN_H) // BLOCK_SIZE + 2)

    if player is not None:
        px_blk = player.x / BLOCK_SIZE
        py_blk = player.y / BLOCK_SIZE
        detect  = player.rock_detect_range
        warm    = detect + ROCK_WARM_ZONE
    else:
        px_blk = py_blk = detect = warm = None

    surface_ys = {bx: world.surface_height(bx) for bx in range(bx0, bx1)}
    biomes     = {bx: world.get_biome(bx) for bx in range(bx0, bx1)}

    SHIMMER = _get_shimmer_blocks()

    # Cloud entity pass — draw dynamic clouds with per-layer drift
    _drift_t = pygame.time.get_ticks() / 1000.0
    _wind_vis = getattr(world, '_wind_visual_strength', 0.0)
    for _cloud in getattr(world, '_clouds', ()):
        _cx, _cy, _cw, _ch, _cbid = _cloud[:5]
        _cvar = _cloud[5] if len(_cloud) > 5 else 0
        _rate = _CLOUD_DRIFT_RATES.get(_cbid, 1.0)
        _sx = _cx - cam_xi + int(_drift_t * _rate)
        if -_cw < _sx < SCREEN_W:
            _sy = _cy - cam_yi
            if -_ch < _sy < SCREEN_H:
                screen.blit(_make_cloud_surf(_cw, _ch, _cbid, _cvar), (_sx, _sy))

    for by in range(by0, by1):
        for bx in range(bx0, bx1):
            bid = world.get_block(bx, by)
            if bid == AIR:
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                bg_bid = world.get_bg_block(bx, by)
                if bg_bid != AIR:
                    bg_surf = None
                    if bg_bid == OUTPOST_FLAG_BLOCK:
                        try:
                            from outposts import OUTPOSTS, OUTPOST_FLAG_COLORS
                            best = min(OUTPOSTS.values(),
                                       key=lambda op: abs(op.center_bx - bx),
                                       default=None)
                            if best is not None:
                                col = OUTPOST_FLAG_COLORS.get(best.outpost_type)
                                if col:
                                    bg_surf = renderer._get_outpost_flag_surf(best.outpost_type, col)
                        except Exception:
                            pass
                    if bg_surf is None:
                        if bg_bid == WILDFLOWER_PATCH:
                            bg_surf = renderer._block_surfs.get(bg_bid)
                        else:
                            bg_surf = renderer._bg_block_surfs.get(bg_bid)
                    if bg_surf:
                        screen.blit(bg_surf, (sx, sy))
                elif by > surface_ys.get(bx, 100):
                    screen.blit(renderer._cave_wall_surf, (sx, sy))
                continue
            if bid == WATER:
                level = world._water_level.get((bx, by), 8)
                if biomes.get(bx) in ("ocean", "coastal"):
                    zone = get_ocean_depth_zone(by)
                    wsurf = renderer._ocean_water_surfs[zone][level - 1]
                else:
                    wsurf = renderer._water_surfs[level - 1]
                wh = wsurf.get_height()
                draw_x = bx * BLOCK_SIZE - cam_xi
                draw_y = by * BLOCK_SIZE - cam_yi + BLOCK_SIZE - wh
                screen.blit(wsurf, (draw_x, draw_y))
                # Animated shimmer: a translucent highlight line that drifts upward
                tick = pygame.time.get_ticks()
                shimmer_off = (tick // 90 + bx * 3 + by * 7) % max(wh, 1)
                shimmer_y = draw_y + shimmer_off
                if draw_y <= shimmer_y < draw_y + wh:
                    pygame.draw.line(screen, (180, 230, 255, 55),
                                     (draw_x, shimmer_y),
                                     (draw_x + BLOCK_SIZE - 1, shimmer_y))
                continue
            if bid == FISHING_SPOT_BLOCK:
                # Render as full-level water with animated shimmer sparkles
                wsurf = renderer._water_surfs[7]
                screen.blit(wsurf, (bx * BLOCK_SIZE - cam_xi, by * BLOCK_SIZE - cam_yi))
                tick = pygame.time.get_ticks()
                import random as _rnd
                spark_rng = _rnd.Random((bx * 7919 + by * 4481 + tick // 800) & 0x7FFFFFFF)
                sx2 = bx * BLOCK_SIZE - cam_xi
                sy2 = by * BLOCK_SIZE - cam_yi
                for _ in range(4):
                    spx = sx2 + spark_rng.randint(2, BLOCK_SIZE - 3)
                    spy = sy2 + spark_rng.randint(2, BLOCK_SIZE - 3)
                    alpha = spark_rng.randint(160, 255)
                    spark = pygame.Surface((4, 4), pygame.SRCALPHA)
                    spark.fill((200, 235, 255, alpha))
                    screen.blit(spark, (spx, spy))
                continue
            if bid == TILLED_SOIL:
                moisture = world._soil_moisture.get((bx, by), 0)
                tsurf = renderer._tilled_soil_surfs[1 if moisture >= 4 else 0]
                screen.blit(tsurf, (bx * BLOCK_SIZE - cam_xi, by * BLOCK_SIZE - cam_yi))
                continue
            if bid == ELEVATOR_CABLE_BLOCK:
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                bg_bid = world.get_bg_block(bx, by)
                if bg_bid != AIR:
                    bg_surf = renderer._bg_block_surfs.get(bg_bid)
                    if bg_surf:
                        screen.blit(bg_surf, (sx, sy))
                elif by > surface_ys.get(bx, 100):
                    screen.blit(renderer._cave_wall_surf, (sx, sy))
                pygame.draw.rect(screen, (55, 55, 65), (sx + 14, sy, 4, BLOCK_SIZE))
                continue
            if bid == LADDER:
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                bg_bid = world.get_bg_block(bx, by)
                if bg_bid != AIR:
                    bg_surf = renderer._bg_block_surfs.get(bg_bid)
                    if bg_surf:
                        screen.blit(bg_surf, (sx, sy))
                elif by > surface_ys.get(bx, 100):
                    screen.blit(renderer._cave_wall_surf, (sx, sy))
                lsurf = renderer._block_surfs.get(LADDER)
                if lsurf:
                    screen.blit(lsurf, (sx, sy))
                continue
            if bid == ELEVATOR_STOP_BLOCK:
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                BS = BLOCK_SIZE
                bg_bid = world.get_bg_block(bx, by)
                if bg_bid != AIR:
                    bg_surf = renderer._bg_block_surfs.get(bg_bid)
                    if bg_surf:
                        screen.blit(bg_surf, (sx, sy))
                elif by > surface_ys.get(bx, 100):
                    screen.blit(renderer._cave_wall_surf, (sx, sy))
                pygame.draw.rect(screen, (55, 55, 65), (sx + 14, sy, 4, BS))
                pygame.draw.rect(screen, (68, 72, 92), (sx + 3, sy + 6, BS - 6, BS - 12))
                pygame.draw.rect(screen, (110, 116, 145), (sx + 3, sy + 6, BS - 6, BS - 12), 1)
                btn_cx = sx + BS // 2
                btn_cy = sy + BS // 2 + 2
                pygame.draw.circle(screen, (160, 165, 200), (btn_cx, btn_cy), 5)
                pygame.draw.circle(screen, (200, 205, 240), (btn_cx, btn_cy), 5, 1)
                pygame.draw.rect(screen, (90, 95, 120), (sx + 10, sy + 8, BS - 20, 4))
                continue
            if bid == MINE_TRACK_BLOCK:
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                BS = BLOCK_SIZE
                bg_bid = world.get_bg_block(bx, by)
                if bg_bid != AIR:
                    bg_surf = renderer._bg_block_surfs.get(bg_bid)
                    if bg_surf:
                        screen.blit(bg_surf, (sx, sy))
                elif by > surface_ys.get(bx, 100):
                    screen.blit(renderer._cave_wall_surf, (sx, sy))
                pygame.draw.rect(screen, (140, 130, 115), (sx, sy + 10, BS, 3))
                pygame.draw.rect(screen, (140, 130, 115), (sx, sy + BS - 13, BS, 3))
                for tx in range(sx + 2, sx + BS, 7):
                    pygame.draw.rect(screen, (100, 75, 50), (tx, sy + 8, 3, BS - 16))
                continue
            if bid == MINE_TRACK_STOP_BLOCK:
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                BS = BLOCK_SIZE
                bg_bid = world.get_bg_block(bx, by)
                if bg_bid != AIR:
                    bg_surf = renderer._bg_block_surfs.get(bg_bid)
                    if bg_surf:
                        screen.blit(bg_surf, (sx, sy))
                elif by > surface_ys.get(bx, 100):
                    screen.blit(renderer._cave_wall_surf, (sx, sy))
                pygame.draw.rect(screen, (140, 130, 115), (sx, sy + 10, BS, 3))
                pygame.draw.rect(screen, (140, 130, 115), (sx, sy + BS - 13, BS, 3))
                for tx in range(sx + 2, sx + BS, 7):
                    pygame.draw.rect(screen, (100, 75, 50), (tx, sy + 8, 3, BS - 16))
                for i in range(4):
                    col = (210, 175, 25) if i % 2 == 0 else (35, 35, 35)
                    pygame.draw.rect(screen, col, (sx + BS - 6, sy + i * (BS // 4), 4, BS // 4))
                continue
            if bid in _OPEN_DOORS:
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                bg_bid = world.get_bg_block(bx, by)
                if bg_bid != AIR:
                    bg_surf = renderer._bg_block_surfs.get(bg_bid)
                    if bg_surf:
                        screen.blit(bg_surf, (sx, sy))
                elif by > surface_ys.get(bx, 100):
                    screen.blit(renderer._cave_wall_surf, (sx, sy))
                dsurf = renderer._block_surfs.get(bid)
                if dsurf:
                    screen.blit(dsurf, (sx, sy))
                continue
            # Ocean decor blocks sit where a WATER block was; draw water first
            # so their transparent backgrounds show the correct underwater colour.
            if bid in _OCEAN_DECOR_BLOCKS:
                zone  = get_ocean_depth_zone(by)
                wsurf = renderer._ocean_water_surfs[zone][7]  # full level
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                screen.blit(wsurf, (sx, sy))
                dsurf = renderer._block_surfs.get(bid)
                if dsurf:
                    screen.blit(dsurf, (sx, sy))
                continue

            surf = renderer._block_surfs.get(bid)
            if bid in ALL_LOGS:
                var = renderer._log_variants.get(bid)
                if var:
                    surf = var[(bx * 97 + world.seed) % len(var)]
            elif bid in ALL_LEAVES:
                var = renderer._leaf_variants.get(bid)
                if var:
                    surf = var[(bx * 97 + by * 31 + world.seed) % len(var)]
            elif bid in ALL_FRUIT_CLUSTERS:
                var = renderer._fruit_cluster_variants.get(bid)
                if var:
                    surf = var[(bx * 97 + by * 31 + world.seed) % len(var)]
            elif bid == GRASS:
                surf = renderer._grass_variants[(bx * 73 + by * 41 + world.seed) % len(renderer._grass_variants)]
            elif bid == DIRT:
                surf = renderer._dirt_variants[(bx * 59 + by * 83 + world.seed) % len(renderer._dirt_variants)]
            elif bid == SAND:
                surf = renderer._sand_variants[(bx * 67 + by * 53 + world.seed) % len(renderer._sand_variants)]
            elif bid == SNOW:
                surf = renderer._snow_variants[(bx * 43 + by * 79 + world.seed) % len(renderer._snow_variants)]
            biome = biomes[bx]
            biome_stone = renderer._biome_stone_surfs.get(biome)
            if bid == STONE and biome_stone:
                surf = biome_stone
            dist = 0.0
            ore_visible = True
            if bid in RESOURCE_BLOCKS and px_blk is not None and not renderer.show_all_resources:
                dist = ((bx - px_blk) ** 2 + (by - py_blk) ** 2) ** 0.5
                underground = by > surface_ys.get(bx, 100)
                ore_visible = (not underground) or (
                    dist <= warm and _los_clear(world, int(px_blk), int(py_blk), bx, by)
                )
                if not ore_visible or dist > warm:
                    depth = by - surface_ys.get(bx, 0)
                    strata_id = (LIMESTONE_STONE if depth < 60 else
                                 GRANITE_STONE   if depth < 120 else
                                 BASALT_STONE    if depth < 180 else
                                 MAGMATIC_STONE) if depth >= 15 else STONE
                    surf = biome_stone or renderer._block_surfs.get(strata_id, renderer._block_surfs.get(STONE))
                elif dist > detect:
                    biome_hints = renderer._biome_resource_hint_surfs.get(biome, renderer._resource_hint_surfs)
                    surf = biome_hints.get(bid, renderer._resource_hint_surfs[bid])
                elif bid in renderer._ore_richness_surfs:
                    richness = world._ore_richness.get((bx, by), 2)
                    surf = renderer._ore_richness_surfs[bid][richness]
            elif bid in renderer._ore_richness_surfs:
                richness = world._ore_richness.get((bx, by), 2)
                surf = renderer._ore_richness_surfs[bid][richness]
            if bid == TOWN_FLAG_BLOCK:
                try:
                    from towns import REGIONS, get_town_for_block
                    town = get_town_for_block(world, bx, by)
                    if town:
                        region = REGIONS.get(town.region_id)
                        if region:
                            surf = renderer._get_town_flag_surf(region.region_id, region.leader_color)
                except Exception:
                    pass
            if bid == OUTPOST_FLAG_BLOCK:
                try:
                    from outposts import OUTPOSTS, OUTPOST_FLAG_COLORS
                    best = min(OUTPOSTS.values(),
                               key=lambda op: abs(op.center_bx - bx),
                               default=None)
                    if best is not None:
                        col = OUTPOST_FLAG_COLORS.get(best.outpost_type)
                        if col:
                            surf = renderer._get_outpost_flag_surf(best.outpost_type, col)
                except Exception:
                    pass
            if bid == BANNER_BLOCK:
                try:
                    coa = world.banner_data.get((bx, by))
                    if coa:
                        surf = renderer._get_banner_surf(coa)
                except Exception:
                    pass
            if surf:
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                if bid in ALL_LEAVES and _wind_vis > 0.01:
                    _sway_phase = bx * 0.41 + getattr(world, 'seed', 0) * 0.0001
                    _sway_x = int(math.sin(_drift_t * 1.5 + _sway_phase) * _wind_vis * 2.5)
                    screen.blit(surf, (sx + _sway_x, sy))
                    fc_bid = world.get_bg_block(bx, by)
                    if fc_bid in ALL_FRUIT_CLUSTERS:
                        fc_var = renderer._fruit_cluster_variants.get(fc_bid)
                        if fc_var:
                            fc_surf = fc_var[(bx * 97 + by * 31 + world.seed) % len(fc_var)]
                            screen.blit(fc_surf, (sx + _sway_x, sy))
                else:
                    _shape, _rot = world.get_block_shape(bx, by)
                    blit_shaped(screen, surf, sx, sy, _shape, _rot)
                    if bid in SHIMMER and ore_visible and (px_blk is None or dist <= detect):
                        now = pygame.time.get_ticks()
                        sc = SHIMMER[bid]
                        h = bx * 1283 + by * 7919
                        for i in range(4):
                            phase = (h + i * 4999) % 65536
                            if ((now + phase) // 350) % 5 == 0:
                                spx = 1 + (h * (i + 3) * 43) % 28
                                spy = 1 + (h * (i + 3) * 97) % 28
                                pygame.draw.rect(screen, sc, (sx + spx, sy + spy, 2, 2))
                    if bid in ALL_LEAVES:
                        fc_bid = world.get_bg_block(bx, by)
                        if fc_bid in ALL_FRUIT_CLUSTERS:
                            var = renderer._fruit_cluster_variants.get(fc_bid)
                            if var:
                                fc_surf = var[(bx * 97 + by * 31 + world.seed) % len(var)]
                                screen.blit(fc_surf, (sx, sy))

    if getattr(world, "wire_mode", False):
        from Render.logic_blocks import draw_wire_tile
        for by in range(by0, by1):
            for bx in range(bx0, bx1):
                if world.get_wire(bx, by):
                    draw_wire_tile(screen, bx, by, world, cam_xi, cam_yi)
    elif player is not None and player.hotbar[player.selected_slot] == "wire":
        _draw_wire_hint(screen)

    if getattr(world, "pipe_mode", False):
        from Render.pipe_blocks import draw_pipe_tile, draw_pipe_transit_dots
        for by in range(by0, by1):
            for bx in range(bx0, bx1):
                if world.get_pipe(bx, by):
                    draw_pipe_tile(screen, bx, by, world, cam_xi, cam_yi)
        draw_pipe_transit_dots(screen, world, cam_xi, cam_yi)

    if getattr(world, "factory_data", None):
        from Render.pipe_blocks import draw_factory_overlays
        draw_factory_overlays(screen, world, cam_xi, cam_yi)

    draw_all_sculptures(screen, renderer.cam_x, renderer.cam_y, world)
    draw_all_tapestries(screen, renderer.cam_x, renderer.cam_y, world)
    draw_pottery_displays(screen, world, cam_xi, cam_yi)
    draw_wildflower_displays(screen, world, cam_xi, cam_yi)
    draw_garden_blocks(screen, world, cam_xi, cam_yi)

    # Underwater darkness overlay — deepens proportionally below tidal zone
    if player is not None:
        player_by = int(player.y / BLOCK_SIZE)
        player_biome = world.get_biome(int(player.x / BLOCK_SIZE))
        if player_biome in ("ocean", "coastal") and player_by > SURFACE_Y + 5:
            zone = get_ocean_depth_zone(player_by)
            if zone != "tidal":
                zone_start = {"reef": SURFACE_Y + 15, "twilight": SURFACE_Y + 50, "deep": SURFACE_Y + 110}
                zone_end   = {"reef": SURFACE_Y + 50, "twilight": SURFACE_Y + 110, "deep": SURFACE_Y + 180}
                z0 = zone_start[zone]
                z1 = zone_end[zone]
                t = max(0.0, min(1.0, (player_by - z0) / max(1, z1 - z0)))
                max_alpha = {"reef": 50, "twilight": 95, "deep": 140}[zone]
                alpha = int(t * max_alpha)
                if alpha > 0:
                    _uw_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
                    _uw_surf.fill((0, 0, 20, alpha))
                    screen.blit(_uw_surf, (0, 0))


def draw_wire_hud(screen, world):
    if getattr(world, "wire_mode", False):
        _draw_wire_mode_hud(screen)


def draw_pipe_hud(screen, world):
    if getattr(world, "pipe_mode", False):
        from Render.pipe_blocks import _draw_pipe_mode_hud
        _draw_pipe_mode_hud(screen)


def _draw_textured_region(screen, x, y, w, h, base_col, texture):
    """Fill a rect with base_col then overlay a pixel pattern matching texture."""
    pygame.draw.rect(screen, base_col, (x, y, w, h))
    if texture == "plain" or w < 4 or h < 3:
        return
    lum = (base_col[0] + base_col[1] + base_col[2]) // 3
    hi = tuple(min(255, c + 65) for c in base_col) if lum < 140 else tuple(max(0, c - 55) for c in base_col)
    dk = tuple(max(0, c - 40) for c in base_col)
    r = pygame.draw.rect  # shorthand

    if texture == "twill":
        # Diagonal lines top-left → bottom-right, spaced 4 px
        for offset in range(-(h - 1), w, 4):
            for row in range(h):
                col = offset + row
                if 0 <= col < w:
                    r(screen, hi, (x + col, y + row, 1, 1))

    elif texture == "tartan":
        # Crosshatch: horizontal stripe every 4 px, vertical every 4 px
        for row in range(0, h, 4):
            r(screen, hi, (x, y + row, w, 1))
        for col in range(0, w, 4):
            r(screen, hi, (x + col, y, 1, h))

    elif texture == "herringbone":
        # Diagonal alternates direction every 3 rows (/ then \)
        for row in range(h):
            d = 1 if (row // 3) % 2 == 0 else -1
            start = (row * d % 4 + 4) % 4
            col = start
            while 0 <= col < w:
                r(screen, hi, (x + col, y + row, 1, 1))
                col += 4

    elif texture == "damask":
        # 2×2 highlight squares at every 4×4 grid cell
        for row in range(0, h, 4):
            for col in range(0, w, 4):
                if y + row < y + h and x + col < x + w:
                    r(screen, hi, (x + col, y + row, min(2, w - col), min(2, h - row)))

    elif texture == "diamond":
        # Small diamond outlines tiled every 6×6
        for cy in range(0, h, 6):
            for cx in range(0, w, 6):
                mx, my = x + cx + 3, y + cy + 3
                for dx, dy in [(0, -3), (3, 0), (0, 3), (-3, 0)]:
                    if x <= mx + dx < x + w and y <= my + dy < y + h:
                        r(screen, hi, (mx + dx, my + dy, 1, 1))
                for dx, dy in [(-1, -2), (1, -2), (-2, -1), (2, -1),
                                (-2,  1), (2,  1), (-1,  2), (1,  2)]:
                    if x <= mx + dx < x + w and y <= my + dy < y + h:
                        r(screen, dk, (mx + dx, my + dy, 1, 1))

    elif texture == "brocade":
        # Cross motif + corner dots tiled every 5×5
        for cy in range(2, h + 2, 5):
            for cx in range(2, w + 2, 5):
                mx, my = x + cx, y + cy
                for dx in range(-2, 3):
                    if x <= mx + dx < x + w and y <= my < y + h:
                        r(screen, hi, (mx + dx, my, 1, 1))
                for dy in range(-2, 3):
                    if x <= mx < x + w and y <= my + dy < y + h:
                        r(screen, hi, (mx, my + dy, 1, 1))
                for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                    if x <= mx + dx < x + w and y <= my + dy < y + h:
                        r(screen, dk, (mx + dx, my + dy, 1, 1))


_ARMOR_BASE = {
    "leather":  ((110,  72,  42), (148,  98,  56)),
    "bone":     ((228, 215, 190), (248, 238, 220)),
    "iron":     ((140, 148, 158), (192, 200, 210)),
    "steel":    ((100, 110, 125), (155, 168, 185)),
    "gold":     ((195, 158,  38), (242, 208,  72)),
    "obsidian": (( 22,  10,  38), ( 52,  24,  88)),
    "crystal":  ((112, 188, 220), (188, 232, 248)),
    "void":     (( 14,   6,  26), ( 38,  16,  72)),
}
_ARMOR_DEFAULT_TRIM = {
    "leather":  (178, 132,  52),
    "bone":     (200, 168, 118),
    "iron":     (210, 218, 228),
    "steel":    (165, 182, 212),
    "gold":     (222, 188,  58),
    "obsidian": (105,  42, 188),
    "crystal":  (222, 248, 255),
    "void":     (118,  55, 205),
}

def _armor_tier(item_id):
    if not item_id:
        return None
    for t in ("leather", "bone", "iron", "steel", "gold", "obsidian", "crystal", "void"):
        if t in item_id:
            return t
    return None

def _ab(c, f):
    return tuple(int(x * f) for x in c)

def _draw_helmet(screen, x, y, w, h, tier, pc, hc, dye):
    pygame.draw.rect(screen, pc, (x, y, w, h))
    if tier == "leather":
        pygame.draw.rect(screen, _ab(pc, 0.72), (x, y, w, 2))           # brow band
        pygame.draw.rect(screen, dye, (x + 1, y + h - 1, w - 2, 1))    # chin strap
        for rx in (x + 3, x + w - 5):                                    # rivets
            pygame.draw.rect(screen, dye, (rx, y + 3, 2, 2))
        pygame.draw.rect(screen, hc, (x + 2, y + 1, w - 4, 1))          # brow highlight
    elif tier == "iron":
        pygame.draw.rect(screen, dye, (x, y + h - 2, w, 2))             # brim
        pygame.draw.rect(screen, _ab(pc, 0.72), (x + w//2 - 1, y + 3, 2, h - 3))  # nasal
        pygame.draw.rect(screen, hc, (x, y, w, 1))                      # top highlight
        pygame.draw.rect(screen, hc, (x, y + 1, 1, h - 2))             # left edge
        pygame.draw.rect(screen, hc, (x + w - 1, y + 1, 1, h - 2))     # right edge
    elif tier == "steel":
        pygame.draw.rect(screen, dye, (x - 1, y + h - 2, w + 2, 2))    # wide brim
        pygame.draw.rect(screen, (18, 18, 18), (x + 2, y + 4, w - 4, 2))   # visor slot H
        pygame.draw.rect(screen, (18, 18, 18), (x + w//2 - 1, y + 5, 2, h - 5))  # visor slot V
        pygame.draw.rect(screen, dye, (x, y + 2, 1, h - 2))            # left flange
        pygame.draw.rect(screen, dye, (x + w - 1, y + 2, 1, h - 2))   # right flange
        pygame.draw.rect(screen, hc, (x, y, w, 1))                      # top highlight
        pygame.draw.rect(screen, hc, (x + 1, y + 1, 1, 3))             # left corner glint
    elif tier == "bone":
        pygame.draw.rect(screen, _ab(pc, 0.82), (x, y, w, 2))           # forehead ridge
        pygame.draw.rect(screen, dye, (x + 1, y + h - 1, w - 2, 1))    # jaw line
        pygame.draw.rect(screen, (95, 78, 55), (x + 2, y + h - 3, 2, 2))  # left joint
        pygame.draw.rect(screen, (95, 78, 55), (x + w - 4, y + h - 3, 2, 2))  # right joint
        pygame.draw.rect(screen, hc, (x + w//2 - 1, y + 1, 2, h - 3))  # brow seam
        pygame.draw.rect(screen, hc, (x + 1, y, w - 2, 1))             # top highlight
    elif tier == "gold":
        pygame.draw.rect(screen, hc, (x, y, w, 2))                      # crown band
        pygame.draw.rect(screen, dye, (x + w//2 - 1, y + 2, 3, 2))     # center gem
        pygame.draw.rect(screen, dye, (x, y + h - 2, w, 2))            # ornate brim
        pygame.draw.rect(screen, _ab(pc, 0.78), (x + 2, y + 4, w - 4, 1))  # visor shadow
        pygame.draw.rect(screen, hc, (x, y + 1, 1, h - 3))             # left glint
        pygame.draw.rect(screen, hc, (x + w - 1, y + 1, 1, h - 3))    # right glint
    elif tier == "obsidian":
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top glow edge
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # left glow edge
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # right glow edge
        pygame.draw.rect(screen, dye, (x, y + h - 1, w, 1))            # bottom glow edge
        pygame.draw.rect(screen, hc, (x + w//2 - 1, y, 2, h))          # shard ridge
        pygame.draw.rect(screen, (12, 12, 12), (x + 2, y + 3, w - 4, 3))  # eye slit
    elif tier == "crystal":
        pygame.draw.rect(screen, hc, (x, y, w, 1))                      # top shine
        pygame.draw.rect(screen, hc, (x, y, 1, h))                      # left shine
        pygame.draw.rect(screen, hc, (x + w - 1, y, 1, h))             # right shine
        pygame.draw.rect(screen, hc, (x, y + h - 1, w, 1))             # bottom shine
        pygame.draw.rect(screen, (205, 242, 252), (x + 2, y + h//3, w - 4, 1))  # facet line
        pygame.draw.rect(screen, (242, 252, 255), (x + w//2 - 1, y + 1, 2, 2))  # apex gem
        pygame.draw.rect(screen, dye, (x + 1, y + 1, w - 2, 1))        # inner edge
    elif tier == "void":
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top void glow
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # left glow
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # right glow
        pygame.draw.rect(screen, (6, 6, 14), (x + 2, y + 3, w - 4, 4)) # void slit
        pygame.draw.rect(screen, _ab(dye, 0.55), (x + 2, y + 3, 1, 4)) # inner glow L
        pygame.draw.rect(screen, _ab(dye, 0.55), (x + w - 3, y + 3, 1, 4))  # inner glow R

def _draw_chestplate(screen, x, y, w, h, tier, pc, hc, dye):
    pygame.draw.rect(screen, pc, (x, y, w, h))
    if tier == "leather":
        pygame.draw.rect(screen, _ab(pc, 0.76), (x + w//2, y, 1, h))   # center seam
        pygame.draw.rect(screen, dye, (x + 2, y + h//2, w - 4, 1))     # belly strap
        pygame.draw.rect(screen, hc, (x, y, 4, 2))                      # left shoulder
        pygame.draw.rect(screen, hc, (x + w - 4, y, 4, 2))             # right shoulder
        for rv in (x + 3, x + w - 5):                                   # chest rivets
            pygame.draw.rect(screen, dye, (rv, y + 2, 2, 2))
    elif tier == "iron":
        pygame.draw.rect(screen, _ab(pc, 0.74), (x + w//2 - 1, y, 1, h))  # ridge
        pygame.draw.rect(screen, dye, (x, y + h//3, w, 1))             # plate line
        pygame.draw.rect(screen, hc, (x, y, 3, 4))                      # left pauldron
        pygame.draw.rect(screen, hc, (x + w - 3, y, 3, 4))             # right pauldron
        pygame.draw.rect(screen, hc, (x, y, w, 1))                      # top edge
    elif tier == "steel":
        pygame.draw.rect(screen, _ab(pc, 0.70), (x + w//2 - 1, y, 2, h))  # wider ridge
        pygame.draw.rect(screen, dye, (x, y + h//3, w, 1))             # upper plate line
        pygame.draw.rect(screen, dye, (x, y + 2*h//3, w, 1))           # lower plate line
        pygame.draw.rect(screen, hc, (x, y, 4, 5))                      # left pauldron
        pygame.draw.rect(screen, hc, (x + w - 4, y, 4, 5))             # right pauldron
        pygame.draw.rect(screen, hc, (x, y, w, 1))                      # top edge
        pygame.draw.rect(screen, hc, (x + 1, y + 1, 2, 2))             # left glint
    elif tier == "bone":
        pygame.draw.rect(screen, _ab(pc, 0.82), (x + w//2, y, 1, h))   # sternum line
        pygame.draw.rect(screen, dye, (x + 2, y + h//2, w - 4, 1))     # rib strap
        pygame.draw.rect(screen, (95, 78, 55), (x + 2, y + 2, 2, 2))   # left joint knob
        pygame.draw.rect(screen, (95, 78, 55), (x + w - 4, y + 2, 2, 2))  # right joint knob
        pygame.draw.rect(screen, hc, (x, y, 4, 2))                      # left shoulder
        pygame.draw.rect(screen, hc, (x + w - 4, y, 4, 2))             # right shoulder
        pygame.draw.rect(screen, hc, (x, y, w, 1))                      # top edge
    elif tier == "gold":
        pygame.draw.rect(screen, _ab(pc, 0.76), (x + w//2 - 1, y, 1, h))  # ridge
        pygame.draw.rect(screen, dye, (x, y + h//3, w, 1))             # upper filigree line
        pygame.draw.rect(screen, dye, (x, y + 2*h//3, w, 1))           # lower filigree line
        pygame.draw.rect(screen, hc, (x, y, 5, 5))                      # large left pauldron
        pygame.draw.rect(screen, hc, (x + w - 5, y, 5, 5))             # large right pauldron
        pygame.draw.rect(screen, dye, (x + w//2 - 1, y + 2, 3, 1))    # center emblem
        pygame.draw.rect(screen, hc, (x, y, w, 1))                      # top shine
        pygame.draw.rect(screen, hc, (x + 1, y + 1, 2, 2))             # left corner glint
        pygame.draw.rect(screen, hc, (x + w - 3, y + 1, 2, 2))         # right corner glint
    elif tier == "obsidian":
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # left glow edge
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # right glow edge
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top glow edge
        pygame.draw.rect(screen, hc, (x + w//2 - 1, y, 1, h))          # shard spine
        pygame.draw.rect(screen, dye, (x + 2, y + h//2, w - 4, 1))     # void crack
        pygame.draw.rect(screen, hc, (x, y, 4, 5))                      # left obsidian shard
        pygame.draw.rect(screen, hc, (x + w - 4, y, 4, 5))             # right obsidian shard
    elif tier == "crystal":
        pygame.draw.rect(screen, hc, (x, y, w, 1))                      # top shine
        pygame.draw.rect(screen, hc, (x, y, 1, h))                      # left shine
        pygame.draw.rect(screen, hc, (x + w - 1, y, 1, h))             # right shine
        pygame.draw.rect(screen, (205, 242, 252), (x, y + h//3, w, 1)) # upper facet
        pygame.draw.rect(screen, (205, 242, 252), (x, y + 2*h//3, w, 1))  # lower facet
        pygame.draw.rect(screen, hc, (x, y, 4, 5))                      # left crystal pauldron
        pygame.draw.rect(screen, hc, (x + w - 4, y, 4, 5))             # right crystal pauldron
        pygame.draw.rect(screen, (242, 252, 255), (x + w//2 - 1, y + 1, 2, 2))  # chest gem
        pygame.draw.rect(screen, dye, (x + 1, y + 1, w - 2, 1))        # inner glow edge
    elif tier == "void":
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # left glow
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # right glow
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top glow
        pygame.draw.rect(screen, hc, (x + w//2 - 1, y, 2, h))          # void spine
        pygame.draw.rect(screen, dye, (x + 2, y + h//3, w - 4, 1))     # upper void crack
        pygame.draw.rect(screen, dye, (x + 2, y + 2*h//3, w - 4, 1))  # lower void crack
        pygame.draw.rect(screen, hc, (x, y, 4, 6))                      # left void pauldron
        pygame.draw.rect(screen, hc, (x + w - 4, y, 4, 6))             # right void pauldron

def _draw_leggings(screen, x, y, w, h, tier, pc, hc, dye):
    pygame.draw.rect(screen, pc, (x, y, w, h))
    if tier == "leather":
        pygame.draw.rect(screen, dye, (x, y, 2, h))                     # left stripe
        pygame.draw.rect(screen, dye, (x + w - 2, y, 2, h))            # right stripe
        pygame.draw.rect(screen, hc, (x + 2, y, w - 4, 1))             # top highlight
    elif tier == "iron":
        pygame.draw.rect(screen, hc, (x + w//2 - 2, y + 1, 4, h - 2)) # knee guard
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top band
        pygame.draw.rect(screen, _ab(pc, 0.75), (x + w//2, y + 1, 1, h - 1))  # knee seam
    elif tier == "steel":
        pygame.draw.rect(screen, hc, (x + w//2 - 3, y, 5, h))         # knee guard wide
        pygame.draw.rect(screen, _ab(pc, 0.70), (x + w//2 - 1, y, 2, h))  # knee crease
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top band
        pygame.draw.rect(screen, dye, (x, y + h - 1, w, 1))            # bottom band
    elif tier == "bone":
        pygame.draw.rect(screen, hc, (x + w//2 - 2, y + 1, 5, h - 2)) # knee knob
        pygame.draw.rect(screen, (95, 78, 55), (x + w//2 - 1, y + 2, 3, 2))  # joint mark
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top band
        pygame.draw.rect(screen, hc, (x + 2, y, w - 4, 1))             # top highlight
    elif tier == "gold":
        pygame.draw.rect(screen, hc, (x + w//2 - 3, y, 5, h))          # knee crest
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top filigree band
        pygame.draw.rect(screen, dye, (x, y + h - 1, w, 1))            # bottom filigree band
        pygame.draw.rect(screen, dye, (x + w//2 - 1, y + h//2, 3, 1)) # center jewel
        pygame.draw.rect(screen, hc, (x + 1, y, w - 2, 1))             # top highlight
    elif tier == "obsidian":
        pygame.draw.rect(screen, hc, (x + w//2 - 2, y, 4, h))          # shard kneecap
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # left glow
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # right glow
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top glow
        pygame.draw.rect(screen, dye, (x, y + h - 1, w, 1))            # bottom glow
    elif tier == "crystal":
        pygame.draw.rect(screen, hc, (x + w//2 - 3, y, 6, h))          # crystal kneeguard
        pygame.draw.rect(screen, (205, 242, 252), (x, y + h//2, w, 1)) # prismatic band
        pygame.draw.rect(screen, hc, (x, y, w, 1))                      # top shine
        pygame.draw.rect(screen, hc, (x, y + h - 1, w, 1))             # bottom shine
        pygame.draw.rect(screen, dye, (x + 1, y, 1, h))                # inner glow L
        pygame.draw.rect(screen, dye, (x + w - 2, y, 1, h))            # inner glow R
    elif tier == "void":
        pygame.draw.rect(screen, hc, (x + w//2 - 2, y, 5, h))          # void kneeguard
        pygame.draw.rect(screen, _ab(pc, 0.60), (x + w//2 - 1, y, 2, h))  # crease
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # left void glow
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # right void glow
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top glow
        pygame.draw.rect(screen, dye, (x + 2, y + h//2, w - 4, 1))    # void tendril

def _draw_boots(screen, x, y, w, h, tier, pc, hc, dye):
    pygame.draw.rect(screen, pc, (x, y, w, h))
    if tier == "leather":
        pygame.draw.rect(screen, hc, (x, y, w, 2))                      # toe cap
        pygame.draw.rect(screen, dye, (x, y + h - 1, w, 1))            # ankle strap
    elif tier == "iron":
        pygame.draw.rect(screen, hc, (x, y, w, 2))                      # toe cap
        pygame.draw.rect(screen, (215, 222, 232), (x, y, w, 1))         # toe shine
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # outer ridge
    elif tier == "steel":
        pygame.draw.rect(screen, hc, (x, y, w, 3))                      # toe cap tall
        pygame.draw.rect(screen, (228, 236, 248), (x, y, w, 1))         # toe shine bright
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # outer ridge
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # inner ridge
    elif tier == "bone":
        pygame.draw.rect(screen, hc, (x, y, w, 2))                      # toe cap
        pygame.draw.rect(screen, (95, 78, 55), (x + 1, y + h - 2, 2, 2))  # ankle joint L
        pygame.draw.rect(screen, (95, 78, 55), (x + w - 3, y + h - 2, 2, 2))  # ankle joint R
        pygame.draw.rect(screen, dye, (x, y + h - 1, w, 1))            # ankle strap
    elif tier == "gold":
        pygame.draw.rect(screen, hc, (x, y, w, 3))                      # toe cap
        pygame.draw.rect(screen, (245, 215, 80), (x, y, w, 1))          # toe shine
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # outer ridge
        pygame.draw.rect(screen, dye, (x, y + h - 1, w, 1))            # ankle filigree
    elif tier == "obsidian":
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top glow
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # left glow
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # right glow
        pygame.draw.rect(screen, hc, (x + 1, y, w - 2, 2))             # shard toe cap
    elif tier == "crystal":
        pygame.draw.rect(screen, hc, (x, y, w, 2))                      # crystal toe
        pygame.draw.rect(screen, (242, 252, 255), (x, y, w, 1))         # toe sparkle
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # left glow
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # right glow
    elif tier == "void":
        pygame.draw.rect(screen, dye, (x, y, w, 1))                     # top void glow
        pygame.draw.rect(screen, dye, (x, y, 1, h))                     # left glow
        pygame.draw.rect(screen, dye, (x + w - 1, y, 1, h))            # right glow
        pygame.draw.rect(screen, hc, (x + 1, y, w - 2, 2))             # void toe cap


_CLOAK_WIDTHS = {
    "garment_cloak":          5,
    "garment_cloak_hooded":   6,
    "garment_cloak_royal":    9,
    "garment_cloak_tattered": 5,
    "garment_cloak_half":     5,
}

def _draw_cloak(screen, cloak_t, px, py, head_h, body_h, facing):
    """Draw the back-slot cloak, dispatching on output_type for distinct silhouettes."""
    c    = tuple(cloak_t.dye_color)
    hi   = tuple(min(255, x + 55) for x in c)
    dk   = tuple(max(0,   x - 45) for x in c)
    ts   = pygame.time.get_ticks() / 1000.0
    ot   = cloak_t.output_type
    w    = _CLOAK_WIDTHS.get(ot, 5)
    sign = 1 if facing == 1 else -1
    # Back side of the body (opposite the arm)
    bx   = (px + PLAYER_W) if facing == 1 else (px - w)
    by   = py + head_h - 1

    if ot == "garment_cloak":
        # Standard cape: gentle travelling wave, grows from shoulder to hem
        for row in range(body_h):
            env  = row / max(1, body_h - 1)
            wave = math.sin(row * 0.9 + ts * 3.5) * env
            sx   = bx + sign * int(round(2.0 * wave))
            pygame.draw.rect(screen, hi if wave > 0.3 else c, (sx, by + row, w, 1))

    elif ot == "garment_cloak_hooded":
        # Hood: semicircular hump behind the head, then narrower cape with slow wave
        hood_cx = bx + (w // 2)
        for row in range(8):
            hw  = max(1, int(3.5 * math.sin(row / 7.0 * math.pi)))
            rx  = hood_cx - hw
            pygame.draw.rect(screen, hi if row < 3 else c, (rx, py - 1 + row, hw * 2, 1))
        for row in range(body_h):
            env  = row / max(1, body_h - 1)
            wave = math.sin(row * 0.7 + ts * 2.5) * env
            sx   = bx + sign * int(round(1.5 * wave))
            pygame.draw.rect(screen, c, (sx, by + row, w, 1))

    elif ot == "garment_cloak_royal":
        # Royal mantle: wide, long, fast dramatic wave, bright inner border
        extra = 4
        for row in range(body_h + extra):
            env  = row / max(1, body_h + extra - 1)
            wave = math.sin(row * 1.0 + ts * 4.5) * env
            sx   = bx + sign * int(round(3.0 * wave))
            pygame.draw.rect(screen, hi if abs(wave) > 0.5 else c, (sx, by + row, w, 1))
            edge_x = sx + (1 if facing == 1 else w - 2)
            pygame.draw.rect(screen, hi, (edge_x, by + row, 1, 1))

    elif ot == "garment_cloak_tattered":
        # Tattered: consistent ragged hem via seed-seeded RNG, slower wave
        fringe = [body_h - _rnd.Random(cloak_t.seed + i).randint(0, 7) for i in range(w)]
        for row in range(body_h):
            env  = row / max(1, body_h - 1)
            wave = math.sin(row * 1.1 + ts * 2.0) * env
            sx   = bx + sign * int(round(2.0 * wave))
            for col_off in range(w):
                if row < fringe[col_off]:
                    shade = dk if row >= body_h - 6 else c
                    pygame.draw.rect(screen, shade, (sx + col_off, by + row, 1, 1))

    elif ot == "garment_cloak_half":
        # Half cape: covers shoulder to mid-torso only, decorative clasp, subtle wave
        half_h = 9
        pygame.draw.rect(screen, hi, (bx + 1, by, 3, 2))          # clasp
        pygame.draw.rect(screen, dk, (bx + 2, by, 1, 1))           # clasp gem
        for row in range(1, half_h):
            env  = row / max(1, half_h - 1)
            wave = math.sin(row * 0.8 + ts * 2.8) * env
            sx   = bx + sign * int(round(1.0 * wave))
            pygame.draw.rect(screen, c, (sx, by + row, w, 1))


def draw_player(screen, cam_x, cam_y, player):
    px = int(player.x - cam_x)
    py = int(player.y - cam_y)
    head_h = 10
    body_h = PLAYER_H - head_h  # 18

    def get_t(slot):
        return player.get_worn_textile(slot)

    def col(t, default):
        return tuple(t.dye_color) if t else default

    def tex(t):
        return t.texture if t else "plain"

    vest_t  = get_t("chest")
    glove_t = get_t("hands")
    hat_t   = get_t("head")
    leg_t   = get_t("legs")
    boot_t  = get_t("feet")
    cloak_t = get_t("back")

    # Determine leg / foot colors and textures
    if leg_t and boot_t:
        leg_col, leg_tex   = col(leg_t,  (55, 90, 150)), tex(leg_t)
        foot_col, foot_tex = col(boot_t, (50, 80, 140)), tex(boot_t)
    elif boot_t:
        leg_col = foot_col = col(boot_t, (50, 80, 140))
        leg_tex = foot_tex = tex(boot_t)
    elif leg_t:
        leg_col = foot_col = col(leg_t, (55, 90, 150))
        leg_tex = foot_tex = tex(leg_t)
    else:
        leg_col = foot_col = (50, 80, 140)
        leg_tex = foot_tex = "plain"

    # Cloak: dispatched to _draw_cloak for type-specific silhouette and animation
    if cloak_t:
        _draw_cloak(screen, cloak_t, px, py, head_h, body_h, player.facing)

    # Hat: patterned crown above the head
    if hat_t:
        _draw_textured_region(screen, px + 2, py - 5, PLAYER_W - 4, 5,
                              col(hat_t, (80, 80, 80)), tex(hat_t))

    # Head (skin — never patterned)
    pygame.draw.rect(screen, (255, 210, 160), (px + 2, py, PLAYER_W - 4, head_h))

    # Eye
    eye_x = (px + PLAYER_W - 6) if player.facing == 1 else (px + 2)
    pygame.draw.rect(screen, (30, 30, 30), (eye_x, py + 3, 3, 3))

    # Vest: patterned torso
    _draw_textured_region(screen, px, py + head_h, PLAYER_W, body_h,
                          col(vest_t, (70, 120, 190)), tex(vest_t))

    # Leggings strip: 4-px band drawn over the lower torso
    if leg_t:
        _draw_textured_region(screen, px, py + head_h + body_h - 10, PLAYER_W, 4,
                              leg_col, leg_tex)

    # Arm / gloves
    arm_x = (px + PLAYER_W) if player.facing == 1 else (px - 3)
    _draw_textured_region(screen, arm_x, py + head_h + 2, 3, 8,
                          col(glove_t, (255, 210, 160)), tex(glove_t))

    # Feet / boots
    _draw_textured_region(screen, px,                  py + head_h + body_h - 6, 8, 6, foot_col, foot_tex)
    _draw_textured_region(screen, px + PLAYER_W - 8,   py + head_h + body_h - 6, 8, 6, foot_col, foot_tex)

    # ── Armor overlays (drawn over textiles) ─────────────────────────────
    wa  = getattr(player, "worn_armor",     {})
    wad = getattr(player, "worn_armor_dye", {})

    def _dye_col(slot, tier):
        fam = wad.get(slot)
        if fam:
            from textiles import DYE_FAMILY_COLORS
            raw = DYE_FAMILY_COLORS.get(fam)
            if raw:
                return tuple(raw)
        return _ARMOR_DEFAULT_TRIM[tier]

    ht = _armor_tier(wa.get("helmet"))
    if ht:
        pc, hc = _ARMOR_BASE[ht]
        _draw_helmet(screen, px + 1, py, PLAYER_W - 2, head_h, ht, pc, hc, _dye_col("helmet", ht))
        pygame.draw.rect(screen, (30, 30, 30), (eye_x, py + 3, 3, 3))

    ct = _armor_tier(wa.get("chestplate"))
    if ct:
        pc, hc = _ARMOR_BASE[ct]
        _draw_chestplate(screen, px, py + head_h, PLAYER_W, body_h - 8, ct, pc, hc, _dye_col("chestplate", ct))

    lt = _armor_tier(wa.get("leggings"))
    if lt:
        pc, hc = _ARMOR_BASE[lt]
        _draw_leggings(screen, px, py + head_h + body_h - 10, PLAYER_W, 8, lt, pc, hc, _dye_col("leggings", lt))

    bt = _armor_tier(wa.get("boots"))
    if bt:
        pc, hc = _ARMOR_BASE[bt]
        _draw_boots(screen, px,                py + head_h + body_h - 6, 8, 6, bt, pc, hc, _dye_col("boots", bt))
        _draw_boots(screen, px + PLAYER_W - 8, py + head_h + body_h - 6, 8, 6, bt, pc, hc, _dye_col("boots", bt))


def draw_entities(renderer, entities):
    screen = renderer.screen
    cam_x  = renderer.cam_x
    cam_y  = renderer.cam_y
    for e in entities:
        if getattr(e, 'dead', False):
            continue
        sx = int(e.x - cam_x)
        sy = int(e.y - cam_y)
        if getattr(e, '_stunned_timer', 0) > 0:
            pygame.draw.circle(screen, (100, 200, 80), (sx + e.W // 2, sy - 6), 4)
        if getattr(e, '_barbed_timer', 0) > 0:
            pygame.draw.circle(screen, (210, 80, 60), (sx + e.W // 2 + 8, sy - 6), 3)
        aid = e.animal_id
        if aid == "sheep":            renderer._draw_sheep(sx, sy, e)
        elif aid == "cow":            renderer._draw_cow(sx, sy, e)
        elif aid == "chicken":        renderer._draw_chicken(sx, sy, e)
        elif aid == "goat":           renderer._draw_goat(sx, sy, e)
        elif aid == "snow_leopard":   renderer._draw_snow_leopard(sx, sy, e)
        elif aid == "mountain_lion":  renderer._draw_mountain_lion(sx, sy, e)
        elif aid == "tiger":          renderer._draw_tiger(sx, sy, e)
        elif aid == "horse":          renderer._draw_horse(sx, sy, e)
        elif aid == "dog":            renderer._draw_dog(sx, sy, e)
        elif aid == "npc_royal_curator":       renderer._draw_npc_royal_curator(sx, sy, e)
        elif aid == "npc_royal_florist":       renderer._draw_npc_royal_florist(sx, sy, e)
        elif aid == "npc_royal_jeweler":       renderer._draw_npc_royal_jeweler(sx, sy, e)
        elif aid == "npc_royal_paleontologist":renderer._draw_npc_royal_paleontologist(sx, sy, e)
        elif aid == "npc_royal_angler":        renderer._draw_npc_royal_angler(sx, sy, e)
        elif aid == "npc_quest":      renderer._draw_npc_quest(sx, sy, e)
        elif aid == "npc_trade":      renderer._draw_npc_trade(sx, sy, e)
        elif aid == "npc_herbalist":  renderer._draw_npc_herbalist(sx, sy, e)
        elif aid == "npc_jeweler":    renderer._draw_npc_jeweler(sx, sy, e)
        elif aid == "npc_merchant":   renderer._draw_npc_merchant(sx, sy, e)
        elif aid == "npc_chef":       renderer._draw_npc_chef(sx, sy, e)
        elif aid == "npc_monk":       renderer._draw_npc_monk(sx, sy, e)
        elif aid == "npc_leader":     renderer._draw_npc_leader(sx, sy, e)
        elif aid == "npc_farmer":     renderer._draw_npc_farmer(sx, sy, e)
        elif aid == "npc_villager":   renderer._draw_npc_villager(sx, sy, e)
        elif aid == "settler":        renderer._draw_npc_settler(sx, sy, e)
        elif aid == "npc_child":      renderer._draw_npc_child(sx, sy, e)
        elif aid == "npc_guard":      renderer._draw_npc_guard(sx, sy, e)
        elif aid == "npc_elder":      renderer._draw_npc_elder(sx, sy, e)
        elif aid == "npc_beggar":     renderer._draw_npc_beggar(sx, sy, e)
        elif aid == "npc_noble":      renderer._draw_npc_noble(sx, sy, e)
        elif aid == "npc_pilgrim":    renderer._draw_npc_pilgrim(sx, sy, e)
        elif aid == "npc_drunkard":   renderer._draw_npc_drunkard(sx, sy, e)
        elif aid == "npc_blacksmith": renderer._draw_npc_blacksmith(sx, sy, e)
        elif aid == "npc_innkeeper":  renderer._draw_npc_innkeeper(sx, sy, e)
        elif aid == "npc_scholar":    renderer._draw_npc_scholar(sx, sy, e)
        elif aid == "deer":           renderer._draw_deer(sx, sy, e)
        elif aid == "boar":           renderer._draw_boar(sx, sy, e)
        elif aid == "rabbit":         renderer._draw_rabbit(sx, sy, e)
        elif aid == "turkey":         renderer._draw_turkey(sx, sy, e)
        elif aid == "wolf":           renderer._draw_wolf(sx, sy, e)
        elif aid == "bear":           renderer._draw_bear(sx, sy, e)
        elif aid == "duck":           renderer._draw_duck(sx, sy, e)
        elif aid == "elk":            renderer._draw_elk(sx, sy, e)
        elif aid == "bison":          renderer._draw_bison(sx, sy, e)
        elif aid == "fox":            renderer._draw_fox(sx, sy, e)
        elif aid == "arctic_fox":     renderer._draw_arctic_fox(sx, sy, e)
        elif aid == "moose":          renderer._draw_moose(sx, sy, e)
        elif aid == "bighorn":        renderer._draw_bighorn(sx, sy, e)
        elif aid == "pheasant":       renderer._draw_pheasant_animal(sx, sy, e)
        elif aid == "warthog":        renderer._draw_warthog(sx, sy, e)
        elif aid == "musk_ox":        renderer._draw_musk_ox(sx, sy, e)
        elif aid == "crocodile":      renderer._draw_crocodile(sx, sy, e)
        elif aid == "goose":          renderer._draw_goose(sx, sy, e)
        elif aid == "hare":           renderer._draw_hare(sx, sy, e)
        elif aid == "capybara":       renderer._draw_capybara(sx, sy, e)
        elif aid == "npc_outpost_keeper": renderer._draw_npc_outpost_keeper(sx, sy, e)
        elif aid == "npc_soldier":    renderer._draw_npc_soldier(sx, sy, e)
