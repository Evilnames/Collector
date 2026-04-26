import math as _math
import pygame
from constants import BLOCK_SIZE


def _darken(color, amount=25):
    return tuple(max(0, c - amount) for c in color)


def draw_pottery_displays(screen, world, cam_xi, cam_yi):
    if not world.pottery_display_data:
        return
    clay_color = (185, 120, 80)
    dark_clay  = _darken(clay_color, 35)
    sw = screen.get_width()
    sh = screen.get_height()
    for (bx, by), piece in world.pottery_display_data.items():
        sx = bx * BLOCK_SIZE - cam_xi
        sy = by * BLOCK_SIZE - cam_yi
        if sx < -BLOCK_SIZE or sx > sw or sy < -BLOCK_SIZE or sy > sh:
            continue
        profile = piece.profile
        n = len(profile)
        if n == 0:
            continue
        row_h = max(1, 18 // n)
        top_y = sy + 7 - row_h * n // 2 + 1
        cx = sx + BLOCK_SIZE // 2
        scale = 12.0 / max(profile) if max(profile) > 0 else 1.0
        for row, rad in enumerate(profile):
            ry = top_y + row * row_h
            w = max(1, int(rad * scale))
            pygame.draw.rect(screen, clay_color, (cx - w, ry, w * 2, row_h))
            pygame.draw.rect(screen, dark_clay,  (cx - w, ry, w * 2, 1))


def draw_sculpture_at(screen, cam_x, cam_y, sc, root_bx, root_by):
    actual_cols    = len(sc.grid[0]) if sc.grid and sc.grid[0] else 8
    rows_per_block = len(sc.grid) // max(1, sc.height)
    CELL_W = BLOCK_SIZE // actual_cols
    CELL_H = BLOCK_SIZE // rows_per_block
    cam_xi = int(cam_x)
    cam_yi = int(cam_y)
    base_color = sc.color
    hi_color   = tuple(min(255, c + 25) for c in base_color)
    lo_color   = tuple(max(0,   c - 35) for c in base_color)
    rows_total = len(sc.grid)
    for row_idx in range(rows_total - 1, -1, -1):
        row = sc.grid[row_idx]
        rows_from_bottom = rows_total - 1 - row_idx
        block_offset     = rows_from_bottom // rows_per_block
        local_row        = rows_from_bottom % rows_per_block
        world_y  = root_by - block_offset
        screen_x = root_bx * BLOCK_SIZE - cam_xi
        screen_y = world_y  * BLOCK_SIZE - cam_yi + local_row * CELL_H
        for col_idx, filled in enumerate(row):
            if not filled:
                continue
            color = hi_color if col_idx % 2 == 0 else lo_color
            pygame.draw.rect(screen, color,
                             (screen_x + col_idx * CELL_W, screen_y, CELL_W, CELL_H))


def draw_all_sculptures(screen, cam_x, cam_y, world):
    for pos, data in world.sculpture_data.items():
        if isinstance(data, dict) and "root" in data:
            continue
        bx, by = pos
        draw_sculpture_at(screen, cam_x, cam_y, data, bx, by)


def draw_tapestry_at(screen, cam_x, cam_y, tp, root_bx, root_by):
    actual_cols    = len(tp.grid[0]) if tp.grid and tp.grid[0] else 16
    rows_per_block = len(tp.grid) // max(1, tp.height)
    tp_width       = getattr(tp, "width", 1)
    CELL_W = (BLOCK_SIZE * tp_width) // actual_cols
    CELL_H = BLOCK_SIZE // rows_per_block
    cam_xi = int(cam_x)
    cam_yi = int(cam_y)
    base_color = tp.color
    hi_color   = tuple(min(255, c + 30) for c in base_color)
    lo_color   = tuple(max(0,   c - 38) for c in base_color)
    rows_total = len(tp.grid)
    for row_idx in range(rows_total - 1, -1, -1):
        row = tp.grid[row_idx]
        rows_from_bottom = rows_total - 1 - row_idx
        block_offset     = rows_from_bottom // rows_per_block
        local_row        = rows_from_bottom % rows_per_block
        world_y  = root_by - block_offset
        screen_x = root_bx * BLOCK_SIZE - cam_xi
        screen_y = world_y  * BLOCK_SIZE - cam_yi + local_row * CELL_H
        for col_idx, filled in enumerate(row):
            if not filled:
                continue
            color = hi_color if row_idx % 2 == 0 else lo_color
            pygame.draw.rect(screen, color,
                             (screen_x + col_idx * CELL_W, screen_y, CELL_W, CELL_H))
            if CELL_H >= 3 and CELL_W >= 2:
                mid_x = screen_x + col_idx * CELL_W + CELL_W // 2
                shade = tuple(max(0, c - 25) for c in color)
                pygame.draw.line(screen, shade,
                                 (mid_x, screen_y), (mid_x, screen_y + CELL_H - 1))


def draw_all_tapestries(screen, cam_x, cam_y, world):
    for pos, data in world.tapestry_data.items():
        if isinstance(data, dict) and "root" in data:
            continue
        bx, by = pos
        draw_tapestry_at(screen, cam_x, cam_y, data, bx, by)


def draw_garden_blocks(screen, world, cam_xi, cam_yi):
    if not world.garden_data:
        return
    sw = screen.get_width()
    sh = screen.get_height()
    for (bx, by), flowers in world.garden_data.items():
        if not flowers:
            continue
        sx = bx * BLOCK_SIZE - cam_xi
        sy = by * BLOCK_SIZE - cam_yi
        if sx < -BLOCK_SIZE or sx > sw or sy < -BLOCK_SIZE or sy > sh:
            continue
        count = min(len(flowers), 5)
        for i, wf in enumerate(flowers[:count]):
            fx = 5 + int(i * 22 / max(count - 1, 1)) if count > 1 else 16
            fy = 13 + (i % 2) * 5
            stem_top = fy - 6
            pygame.draw.line(screen, (50, 130, 40), (sx + fx, sy + fy), (sx + fx, sy + stem_top), 1)
            pc = wf.primary_color
            sc = wf.secondary_color
            for j in range(5):
                ang = j * 2 * _math.pi / 5 - _math.pi / 2
                px2 = int(sx + fx + 3 * _math.cos(ang))
                py2 = int(sy + stem_top + 3 * _math.sin(ang))
                pygame.draw.circle(screen, pc if j % 2 == 0 else sc, (px2, py2), 2)
            pygame.draw.circle(screen, wf.center_color, (sx + fx, sy + stem_top), 1)


def draw_wildflower_displays(screen, world, cam_xi, cam_yi):
    if not world.wildflower_display_data:
        return
    sw = screen.get_width()
    sh = screen.get_height()
    for (bx, by), wf in world.wildflower_display_data.items():
        if wf is None:
            continue
        sx = bx * BLOCK_SIZE - cam_xi
        sy = by * BLOCK_SIZE - cam_yi
        if sx < -BLOCK_SIZE or sx > sw or sy < -BLOCK_SIZE or sy > sh:
            continue
        pygame.draw.line(screen, (50, 140, 40), (sx + 16, sy + 14), (sx + 16, sy + 25), 1)
        petal_c = wf.primary_color + (220,)
        sec_c   = wf.secondary_color + (180,)
        for i in range(5):
            ang = i * 2 * _math.pi / 5 - _math.pi / 2
            px = int(sx + 16 + 5 * _math.cos(ang))
            py = int(sy + 11 + 5 * _math.sin(ang))
            pygame.draw.circle(screen, petal_c if i % 2 == 0 else sec_c, (px, py), 3)
        pygame.draw.circle(screen, wf.center_color, (sx + 16, sy + 11), 2)
