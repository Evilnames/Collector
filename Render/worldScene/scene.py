import pygame
from blocks import (AIR, WATER, TILLED_SOIL, GRASS, DIRT, SAND, SNOW,
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
                    TOWN_FLAG_BLOCK, OUTPOST_FLAG_BLOCK,
                    RESOURCE_BLOCKS,
                    LIMESTONE_STONE, GRANITE_STONE, BASALT_STONE, MAGMATIC_STONE)
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, PLAYER_W, PLAYER_H, ROCK_WARM_ZONE
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

_wire_hud_font = None
_wire_hud_surf = None


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
    screen = renderer.screen
    screen.blit(renderer._sky_surf, (0, 0))
    night_alpha = renderer._sky_night_alpha(getattr(world, 'time_of_day', 0.0))
    if night_alpha > 0:
        renderer._sky_night_surf.set_alpha(night_alpha)
        screen.blit(renderer._sky_night_surf, (0, 0))

    cam_xi = int(renderer.cam_x)
    cam_yi = int(renderer.cam_y)

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
                        bg_surf = renderer._bg_block_surfs.get(bg_bid)
                    if bg_surf:
                        screen.blit(bg_surf, (sx, sy))
                elif by > surface_ys.get(bx, 100):
                    screen.blit(renderer._cave_wall_surf, (sx, sy))
                continue
            if bid == WATER:
                level = world._water_level.get((bx, by), 8)
                wsurf = renderer._water_surfs[level - 1]
                wh = wsurf.get_height()
                screen.blit(wsurf, (bx * BLOCK_SIZE - cam_xi,
                                    by * BLOCK_SIZE - cam_yi + BLOCK_SIZE - wh))
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
            if surf:
                sx = bx * BLOCK_SIZE - cam_xi
                sy = by * BLOCK_SIZE - cam_yi
                screen.blit(surf, (sx, sy))
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
        _draw_wire_mode_hud(screen)

    draw_all_sculptures(screen, renderer.cam_x, renderer.cam_y, world)
    draw_all_tapestries(screen, renderer.cam_x, renderer.cam_y, world)
    draw_pottery_displays(screen, world, cam_xi, cam_yi)
    draw_wildflower_displays(screen, world, cam_xi, cam_yi)
    draw_garden_blocks(screen, world, cam_xi, cam_yi)


def draw_player(screen, cam_x, cam_y, player):
    px = int(player.x - cam_x)
    py = int(player.y - cam_y)
    head_h = 10
    body_h = PLAYER_H - head_h
    pygame.draw.rect(screen, (255, 210, 160), (px + 2, py, PLAYER_W - 4, head_h))
    eye_x = (px + PLAYER_W - 6) if player.facing == 1 else (px + 2)
    pygame.draw.rect(screen, (30, 30, 30), (eye_x, py + 3, 3, 3))
    pygame.draw.rect(screen, (70, 120, 190), (px, py + head_h, PLAYER_W, body_h))
    arm_x = (px + PLAYER_W) if player.facing == 1 else (px - 3)
    pygame.draw.rect(screen, (255, 210, 160), (arm_x, py + head_h + 2, 3, 8))
    pygame.draw.rect(screen, (50, 80, 140), (px, py + head_h + body_h - 6, 8, 6))
    pygame.draw.rect(screen, (50, 80, 140), (px + PLAYER_W - 8, py + head_h + body_h - 6, 8, 6))


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
