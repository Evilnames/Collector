import math
import pygame
from constants import BLOCK_SIZE

BS = BLOCK_SIZE
H  = BS // 2
Q  = BS // 4

# Per-tier colors: (dim, lit) — dim = idle, lit = has items in buffer
_TIER_COLORS = {
    1: ((120,  95,  75), (200, 150, 100)),   # wooden  — warm brown
    2: ((100, 120, 145), (150, 185, 220)),   # iron    — cool grey-blue
    3: (( 40, 150, 140), ( 80, 230, 210)),   # crystal — bright teal
}
_ITEM_DOT_COLOR = (255, 210, 90)   # moving item dot color


# ---------------------------------------------------------------------------
# Pipe tile (drawn in pipe mode overlay, not in the block surface cache)
# ---------------------------------------------------------------------------

def draw_pipe_tile(screen, bx, by, world, cam_x, cam_y):
    from blocks import PIPE_DEVICE_BLOCKS
    sx = bx * BS - cam_x
    sy = by * BS - cam_y

    tier = world.get_pipe(bx, by)
    dim, lit = _TIER_COLORS.get(tier, _TIER_COLORS[1])

    n = world.get_pipe(bx, by - 1) or (world.get_block(bx, by - 1) in PIPE_DEVICE_BLOCKS)
    s = world.get_pipe(bx, by + 1) or (world.get_block(bx, by + 1) in PIPE_DEVICE_BLOCKS)
    w = world.get_pipe(bx - 1, by) or (world.get_block(bx - 1, by) in PIPE_DEVICE_BLOCKS)
    e = world.get_pipe(bx + 1, by) or (world.get_block(bx + 1, by) in PIPE_DEVICE_BLOCKS)

    has_staged = bool(world.pipe_buffers.get((bx, by)))
    col = lit if has_staged else dim

    cx, cy = sx + H, sy + H
    pygame.draw.circle(screen, col, (cx, cy), 3)
    if n:
        pygame.draw.line(screen, col, (cx, cy), (cx, sy),      2)
    if s:
        pygame.draw.line(screen, col, (cx, cy), (cx, sy + BS), 2)
    if w:
        pygame.draw.line(screen, col, (cx, cy), (sx, cy),      2)
    if e:
        pygame.draw.line(screen, col, (cx, cy), (sx + BS, cy), 2)
    if not (n or s or w or e):
        pygame.draw.line(screen, col, (sx + Q, cy), (sx + BS - Q, cy), 2)
        pygame.draw.line(screen, col, (cx, sy + Q), (cx, sy + BS - Q), 2)


def draw_pipe_transit_dots(screen, world, cam_x, cam_y):
    """Draw animated dots for every item currently in transit through the pipe network."""
    for packet in world.pipe_in_transit:
        path     = packet["path"]
        progress = packet["progress"]
        path_len = len(path)
        if path_len < 1:
            continue

        idx  = min(int(progress), path_len - 1)
        frac = progress - int(progress)

        bx1, by1 = path[idx]
        if idx + 1 < path_len:
            bx2, by2 = path[idx + 1]
        else:
            bx2, by2 = bx1, by1

        px1 = bx1 * BS - cam_x + H
        py1 = by1 * BS - cam_y + H
        px2 = bx2 * BS - cam_x + H
        py2 = by2 * BS - cam_y + H

        dot_x = int(px1 + (px2 - px1) * frac)
        dot_y = int(py1 + (py2 - py1) * frac)

        pygame.draw.circle(screen, _ITEM_DOT_COLOR, (dot_x, dot_y), 4)
        pygame.draw.circle(screen, (255, 255, 200), (dot_x, dot_y), 2)


# ---------------------------------------------------------------------------
# Device surfaces (static, built once)
# ---------------------------------------------------------------------------

def build_hopper_surf():
    s = pygame.Surface((BS, BS), pygame.SRCALPHA)
    body   = (100, 80, 60)
    accent = (180, 130, 80)
    pygame.draw.rect(s, body, (Q, Q, H, H))
    pygame.draw.line(s, accent, (Q, Q), (H, H + Q // 2), 2)
    pygame.draw.line(s, accent, (Q + H, Q), (H, H + Q // 2), 2)
    pygame.draw.rect(s, accent, (2, 2, BS - 4, Q - 2), 2)
    pygame.draw.rect(s, (150, 120, 90), (0, 0, BS, BS), 1)
    return s


def build_pipe_output_surf():
    s = pygame.Surface((BS, BS), pygame.SRCALPHA)
    body  = (60, 90, 110)
    arrow = (120, 180, 220)
    pygame.draw.rect(s, body, (2, 2, BS - 4, BS - 4))
    mx = H
    pygame.draw.line(s, arrow, (mx, Q), (mx, BS - Q), 2)
    pygame.draw.line(s, arrow, (mx, BS - Q), (mx - Q // 2, H + Q // 2), 2)
    pygame.draw.line(s, arrow, (mx, BS - Q), (mx + Q // 2, H + Q // 2), 2)
    pygame.draw.rect(s, (80, 120, 150), (0, 0, BS, BS), 1)
    return s


def build_pipe_filter_surf():
    s    = pygame.Surface((BS, BS), pygame.SRCALPHA)
    body = (95, 75, 55)
    grid = (200, 160, 100)
    pygame.draw.rect(s, body, (2, 2, BS - 4, BS - 4))
    for i in range(1, 4):
        x = i * BS // 4
        pygame.draw.line(s, grid, (x, 2), (x, BS - 2), 1)
    for i in range(1, 4):
        y = i * BS // 4
        pygame.draw.line(s, grid, (2, y), (BS - 2, y), 1)
    pygame.draw.rect(s, (150, 120, 80), (0, 0, BS, BS), 1)
    return s


def build_pipe_sorter_surf():
    s     = pygame.Surface((BS, BS), pygame.SRCALPHA)
    body  = (65, 65, 95)
    arrow = (160, 140, 220)
    pygame.draw.rect(s, body, (2, 2, BS - 4, BS - 4))
    mx, my = H, H
    sz = Q // 2
    for ax, ay in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        ex, ey = mx + ax * sz * 2, my + ay * sz * 2
        pygame.draw.line(s, arrow, (mx, my), (ex, ey), 2)
        px = -ay * sz
        py =  ax * sz
        pygame.draw.line(s, arrow, (ex, ey), (ex + px, ey + py), 2)
        pygame.draw.line(s, arrow, (ex, ey), (ex - px, ey - py), 2)
    pygame.draw.rect(s, (100, 90, 150), (0, 0, BS, BS), 1)
    return s


def build_factory_surf():
    s    = pygame.Surface((BS, BS), pygame.SRCALPHA)
    body = (55, 80, 65)
    trim = (90, 160, 120)
    gear = (140, 210, 170)
    pygame.draw.rect(s, body, (2, 2, BS - 4, BS - 4))
    # Gear teeth (simplified: 8 small rects around a central circle)
    cx, cy, r = H, H, H - 6
    pygame.draw.circle(s, gear, (cx, cy), r - 2)
    pygame.draw.circle(s, body, (cx, cy), r - 6)
    for i in range(8):
        import math
        angle = math.pi * i / 4
        tx = int(cx + (r + 2) * math.cos(angle))
        ty = int(cy + (r + 2) * math.sin(angle))
        pygame.draw.circle(s, gear, (tx, ty), 3)
    # Center dot
    pygame.draw.circle(s, trim, (cx, cy), 3)
    pygame.draw.rect(s, trim, (0, 0, BS, BS), 1)
    return s


def draw_factory_overlays(screen, world, cam_x, cam_y):
    """
    Drawn every frame (not just pipe mode) over every visible FACTORY_BLOCK.
    - Active factory: spinning gear-dot ring + thin progress arc around block
    - Cap full: red corner pip
    - Completion flash: brief bright pulse
    """
    from blocks import FACTORY_BLOCK as _FB
    from factory import DEFAULT_INV_CAP

    for (bx, by), state in world.factory_data.items():
        if world.get_block(bx, by) != _FB:
            continue

        sx = bx * BS - cam_x
        sy = by * BS - cam_y
        cx = sx + H
        cy = sy + H

        recipe     = state.get("recipe", {})
        craft_time = max(0.5, recipe.get("craft_time", 5.0))
        progress   = state.get("progress", 0.0)
        inv        = state.get("inventory", {})
        inv_cap    = state.get("inv_cap", DEFAULT_INV_CAP)
        total_inv  = sum(inv.values())
        inputs     = [s for s in recipe.get("inputs", []) if s]
        outputs    = [s for s in recipe.get("outputs", []) if s]
        active     = (progress > 0 and inputs and outputs)
        at_cap     = (total_inv >= inv_cap)
        flash_t    = world.factory_flash.get((bx, by), 0.0)

        # ── Completion flash ─────────────────────────────────────────────────
        if flash_t > 0:
            from factory import FLASH_DURATION
            alpha = int(200 * (flash_t / FLASH_DURATION))
            flash_surf = pygame.Surface((BS, BS), pygame.SRCALPHA)
            flash_surf.fill((160, 255, 180, alpha))
            screen.blit(flash_surf, (sx, sy))

        # ── Progress arc (thin ring around block) ────────────────────────────
        if active:
            frac  = min(1.0, progress / craft_time)
            r_arc = H + 3
            # Background arc (full circle, dark)
            pygame.draw.circle(screen, (30, 60, 40), (cx, cy), r_arc, 1)
            # Filled arc approximated with short line segments
            if frac > 0:
                steps    = max(3, int(frac * 32))
                arc_col  = (80, 220, 120)
                start_a  = -math.pi / 2           # 12 o'clock
                end_a    = start_a + frac * math.pi * 2
                prev_x   = cx + int(r_arc * math.cos(start_a))
                prev_y   = cy + int(r_arc * math.sin(start_a))
                for step in range(1, steps + 1):
                    a     = start_a + (end_a - start_a) * step / steps
                    nx    = cx + int(r_arc * math.cos(a))
                    ny    = cy + int(r_arc * math.sin(a))
                    pygame.draw.line(screen, arc_col, (prev_x, prev_y), (nx, ny), 2)
                    prev_x, prev_y = nx, ny

        # ── Spinning gear-dot ring ────────────────────────────────────────────
        if active:
            angle_offset = (progress / craft_time) * math.pi * 2
            r_ring       = H - 5
            dot_r        = 2
            dot_col      = (100, 240, 150)
            for i in range(8):
                a  = angle_offset + i * (math.pi / 4)
                dx = int(cx + r_ring * math.cos(a))
                dy = int(cy + r_ring * math.sin(a))
                pygame.draw.circle(screen, dot_col, (dx, dy), dot_r)

        # ── Cap-full indicator (red corner pip) ──────────────────────────────
        if at_cap:
            pygame.draw.circle(screen, (220, 60, 60), (sx + BS - 4, sy + 4), 4)
            pygame.draw.circle(screen, (255, 120, 100), (sx + BS - 4, sy + 4), 2)


def build_pipe_surfs():
    from blocks import HOPPER_BLOCK, PIPE_OUTPUT_BLOCK, PIPE_FILTER_BLOCK, PIPE_SORTER_BLOCK, FACTORY_BLOCK
    return {
        HOPPER_BLOCK:      build_hopper_surf(),
        PIPE_OUTPUT_BLOCK: build_pipe_output_surf(),
        PIPE_FILTER_BLOCK: build_pipe_filter_surf(),
        PIPE_SORTER_BLOCK: build_pipe_sorter_surf(),
        FACTORY_BLOCK:     build_factory_surf(),
    }


# ---------------------------------------------------------------------------
# Pipe mode HUD badge
# ---------------------------------------------------------------------------

def _draw_pipe_mode_hud(screen):
    try:
        font = pygame.font.SysFont("monospace", 14, bold=True)
    except Exception:
        return
    text = "PIPE MODE   [P] exit"
    surf = font.render(text, True, (200, 160, 110))
    w, h = surf.get_size()
    pad  = 6
    badge = pygame.Surface((w + pad * 2, h + pad * 2), pygame.SRCALPHA)
    badge.fill((20, 15, 10, 180))
    badge.blit(surf, (pad, pad))
    screen.blit(badge, (screen.get_width() - badge.get_width() - 8, 8))
