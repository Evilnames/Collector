"""
landmark_buildings.py — Grand building structures for capital landmarks.

Each landmark type gets a distinct architectural design, culturally adapted
to the region's biome_group. Buildings are 26–36 blocks wide and 8–12 blocks
tall, placed opposite the capital palace. All functions share the same
signature and return flag_x (the LandmarkNPC interaction x).
"""

from constants import CHUNK_W
from blocks import (
    AIR, STONE, BEDROCK,
    LIMESTONE_BLOCK, POLISHED_MARBLE, COBBLESTONE,
    SANDSTONE_BLOCK, SANDSTONE_ASHLAR, SANDSTONE_COLUMN,
    COMPASS_PAVING, TATAMI_PAVING, ZEN_GRAVEL, ROMAN_MOSAIC,
    ROMAN_ARCH_REN, ROMANESQUE_ARCH, MUGHAL_ARCH, PAGODA_EAVE, TORII_PANEL,
    MOON_GATE, TRELLIS_ARCH, POINTED_ARCH,
    GARDEN_COLUMN, DORIC_CAPITAL, LOTUS_CAPITAL,
    MARBLE_PLINTH, MARBLE_STATUE,
    HERALDIC_PANEL, HERMES_STELE, VOTIVE_TABLET, PHILOSOPHERS_SCROLL,
    LACQUER_PANEL, PINE_PLANK_WALL, ROUGH_STONE_WALL, NORDIC_PLANK,
    CARVED_BENCH, MUGHAL_JALI,
    BRAZIER, TORCH, TRIPOD_BRAZIER, STONE_LANTERN, PAPER_LANTERN,
    TALL_SUNDIAL, SHELL_FOUNTAIN, KOI_POOL, LOTUS_POND, LOTUS_BLOCK,
    OLIVE_BRANCH, LAVENDER_BED, ROSE_BED, BAMBOO_CLUMP,
    GRAPEVINE_CROP_MATURE, GLOW_VINE,
    TOPIARY_PEACOCK, TOPIARY_ARCH, TOPIARY_BEAR,
    WEAPON_RACK_BLOCK, TROPHY_PANEL_REN, FORGE_BLOCK, RAIN_BARREL,
    PRAYER_FLAG_BLOCK, LANDMARK_FLAG_BLOCK,
)


# ---------------------------------------------------------------------------
# Shared helpers (mirror palace helpers from cities.py)
# ---------------------------------------------------------------------------

def _lm_set(world, bx, by, bid):
    if 0 <= by < world.height:
        world.set_block(bx, by, bid)

def _lm_bg(world, bx, by, bid):
    if 0 <= by < world.height:
        world.set_bg_block(bx, by, bid)

def _lm_fill(world, x0, x1, y0, y1, bid):
    for bx in range(x0, x1 + 1):
        for by in range(y0, y1 + 1):
            if 0 <= by < world.height:
                world.set_block(bx, by, bid)

def _lm_fill_bg(world, x0, x1, y0, y1, bid):
    for bx in range(x0, x1 + 1):
        for by in range(y0, y1 + 1):
            if 0 <= by < world.height:
                world.set_bg_block(bx, by, bid)

def _lm_clear_terrain(world, left_bx, width, sy):
    """Level terrain in the landmark footprint (mirrors _palace_clear_terrain)."""
    for cx in range((left_bx - 2) // CHUNK_W, (left_bx + width + 4) // CHUNK_W + 1):
        world.load_chunk(cx)
    for bx in range(left_bx - 1, left_bx + width + 2):
        for by in range(sy - 14, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
    for bx in range(left_bx, left_bx + width + 1):
        col_sy = world.surface_y_at(bx)
        for by in range(col_sy, sy):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)

def _lm_flag(world, spec, flag_bx, sy):
    """Place the visible marker block and interaction flags at the focal point."""
    _lm_set(world, flag_bx, sy - 2, spec["marker_block"])
    _lm_bg(world, flag_bx, sy - 2, LANDMARK_FLAG_BLOCK)
    _lm_bg(world, flag_bx, sy - 3, LANDMARK_FLAG_BLOCK)

def _lm_cols(world, lx, rx, bot_y, col_h, col_block, cap_block, spacing=4):
    """Place columns with capitals at regular intervals between lx and rx."""
    x = lx + spacing
    while x < rx:
        for by in range(bot_y - col_h + 1, bot_y + 1):
            _lm_bg(world, x, by, col_block)
        _lm_bg(world, x, bot_y - col_h, cap_block)
        x += spacing


# ---------------------------------------------------------------------------
# Arena  (martial, base)  — tiered colosseum ring
# ---------------------------------------------------------------------------

def _place_arena(world, spec, biome, right_bx, sy, rng):
    """
    Tiered fighting arena. Gate towers flank three ascending seating tiers
    on each side. Biome sets material palette.
    """
    W = 32
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    if biome == "mediterranean":
        wall, floor, arch, light = POLISHED_MARBLE, COMPASS_PAVING, ROMAN_ARCH_REN, BRAZIER
        panel = HERALDIC_PANEL
    elif biome in ("east_asian", "jungle"):
        wall, floor, arch, light = PINE_PLANK_WALL, TATAMI_PAVING, PAGODA_EAVE, STONE_LANTERN
        panel = LACQUER_PANEL
    else:
        wall, floor, arch, light = LIMESTONE_BLOCK, COBBLESTONE, ROMANESQUE_ARCH, BRAZIER
        panel = HERALDIC_PANEL

    # Foundation
    _lm_fill(world, left, left + W - 1, sy, sy, wall)

    # Gate towers (3 wide, 11 tall) on each side
    for dx in range(3):
        _lm_fill(world, left + dx, left + dx, sy - 11, sy, wall)
        _lm_fill(world, left + W - 1 - dx, left + W - 1 - dx, sy - 11, sy, wall)
    _lm_fill_bg(world, left, left + 2, sy - 11, sy, wall)
    _lm_fill_bg(world, left + W - 3, left + W - 1, sy - 11, sy, wall)
    _lm_set(world, left + 1, sy - 12, light)
    _lm_set(world, left + W - 2, sy - 12, light)
    _lm_bg(world, left + 1, sy - 7, arch)
    _lm_bg(world, left + W - 2, sy - 7, arch)

    # Three seating tiers per side — step down from outer wall to pit
    for dx, h in [(3, 9), (5, 6), (7, 4)]:
        _lm_fill(world, left + dx, left + dx + 1, sy - h, sy, wall)
        _lm_fill(world, left + W - 2 - dx, left + W - 1 - dx, sy - h, sy, wall)

    # Pit floor (central fighting surface)
    _lm_fill(world, left + 9, left + W - 10, sy - 1, sy, floor)

    # BG interior walls
    _lm_fill_bg(world, left + 3, left + W - 4, sy - 9, sy, wall)

    # Trophies on back interior wall
    _lm_bg(world, flag_bx, sy - 4, TROPHY_PANEL_REN)
    _lm_bg(world, flag_bx - 1, sy - 5, panel)
    _lm_bg(world, flag_bx + 1, sy - 5, panel)

    # Vomitorium tunnels — clear the base of every seating tier so the player
    # can walk from the entrance gates all the way to the pit floor
    for bx in range(left + 3, left + 9):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)
    for bx in range(left + W - 9, left + W - 3):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# War Camp  (martial, steppe)  — palisade enclosure with longhouse barracks
# ---------------------------------------------------------------------------

def _place_war_camp(world, spec, biome, right_bx, sy, rng):
    W = 30
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    # Palisade outer wall — tall log posts at every even block
    for bx in range(left, left + W):
        is_post = ((bx - left) % 2 == 0)
        h = 7 if is_post else 5
        _lm_fill(world, bx, bx, sy - h, sy, PINE_PLANK_WALL)
    _lm_fill_bg(world, left, left + W - 1, sy - 7, sy, NORDIC_PLANK)

    # Longhouse barracks in the interior (open-frame structure)
    hall_l, hall_r = left + 4, left + W - 5
    _lm_fill(world, hall_l, hall_r, sy - 5, sy - 5, NORDIC_PLANK)        # roof ridge
    _lm_fill_bg(world, hall_l, hall_r, sy - 5, sy - 1, NORDIC_PLANK)

    # Roof slope — two rows overhanging
    _lm_fill(world, hall_l - 1, hall_r + 1, sy - 6, sy - 6, PINE_PLANK_WALL)
    _lm_fill(world, hall_l - 2, hall_r + 2, sy - 7, sy - 7, PINE_PLANK_WALL)

    # Clear interior so player can walk in
    for by in range(sy - 4, sy):
        for bx in range(hall_l + 1, hall_r):
            _lm_set(world, bx, by, AIR)

    # Weapon racks and fire on interior BG
    for bx in (hall_l + 2, hall_l + 4, hall_r - 4, hall_r - 2):
        _lm_bg(world, bx, sy - 2, WEAPON_RACK_BLOCK)
    _lm_bg(world, flag_bx, sy - 2, BRAZIER)
    _lm_bg(world, flag_bx - 1, sy - 2, CARVED_BENCH)
    _lm_bg(world, flag_bx + 1, sy - 2, CARVED_BENCH)

    # Entrance (clear the front palisade posts for a 4-block gate)
    for bx in range(left + W // 2 - 2, left + W // 2 + 2):
        for by in range(sy - 4, sy):
            _lm_set(world, bx, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Gladiator Pits  (martial, desert)  — sandstone arena with sunken pit
# ---------------------------------------------------------------------------

def _place_gladiator_pits(world, spec, biome, right_bx, sy, rng):
    W = 30
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    wall = SANDSTONE_ASHLAR

    # Outer walls (4 wide each side, 10 tall) with sandstone column pillasters
    for dx in range(4):
        _lm_fill(world, left + dx, left + dx, sy - 10, sy, wall)
        _lm_fill(world, left + W - 1 - dx, left + W - 1 - dx, sy - 10, sy, wall)
    _lm_fill_bg(world, left, left + 3, sy - 10, sy, wall)
    _lm_fill_bg(world, left + W - 4, left + W - 1, sy - 10, sy, wall)

    # Mughal archway on each outer wall
    _lm_bg(world, left + 1, sy - 6, MUGHAL_ARCH)
    _lm_bg(world, left + W - 2, sy - 6, MUGHAL_ARCH)
    _lm_set(world, left + 2, sy - 10, BRAZIER)
    _lm_set(world, left + W - 3, sy - 10, BRAZIER)

    # Two seating tiers per side
    for dx, h in [(4, 7), (6, 5)]:
        _lm_fill(world, left + dx, left + dx + 1, sy - h, sy, wall)
        _lm_fill(world, left + W - 2 - dx, left + W - 1 - dx, sy - h, sy, wall)

    # Pit floor — SANDSTONE_BLOCK (the fighting sand)
    _lm_fill(world, left + 8, left + W - 9, sy - 1, sy, SANDSTONE_BLOCK)

    # BG interior
    _lm_fill_bg(world, left + 4, left + W - 5, sy - 8, sy, wall)
    _lm_bg(world, flag_bx, sy - 4, TROPHY_PANEL_REN)
    _lm_bg(world, flag_bx - 1, sy - 5, MUGHAL_JALI)
    _lm_bg(world, flag_bx + 1, sy - 5, MUGHAL_JALI)

    # Entrance gate + underpass through both seating tiers
    for bx in range(left + 2, left + 8):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)
    for bx in range(left + W - 8, left + W - 2):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Grand Bazaar  (mercantile, base)  — colonnaded market hall
# ---------------------------------------------------------------------------

def _place_grand_bazaar(world, spec, biome, right_bx, sy, rng):
    W = 34
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    if biome == "mediterranean":
        wall, floor, arch = POLISHED_MARBLE, ROMAN_MOSAIC, ROMAN_ARCH_REN
        col, cap, light = GARDEN_COLUMN, DORIC_CAPITAL, BRAZIER
    elif biome == "east_asian":
        wall, floor, arch = PINE_PLANK_WALL, TATAMI_PAVING, PAGODA_EAVE
        col, cap, light = PINE_PLANK_WALL, PAGODA_EAVE, STONE_LANTERN
    else:
        wall, floor, arch = LIMESTONE_BLOCK, COMPASS_PAVING, ROMANESQUE_ARCH
        col, cap, light = GARDEN_COLUMN, DORIC_CAPITAL, BRAZIER

    # Foundation + floor
    _lm_fill(world, left, left + W - 1, sy, sy, wall)
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, floor)

    # Outer walls (2 wide) + corner towers
    for dx in (0, 1):
        _lm_fill(world, left + dx, left + dx, sy - 9, sy, wall)
        _lm_fill(world, left + W - 1 - dx, left + W - 1 - dx, sy - 9, sy, wall)
    _lm_fill(world, left, left + 1, sy - 9, sy - 9, wall)
    _lm_fill(world, left + W - 2, left + W - 1, sy - 9, sy - 9, wall)
    _lm_set(world, left + 1, sy - 10, light)
    _lm_set(world, left + W - 2, sy - 10, light)

    # Central roof span
    _lm_fill(world, left + 2, left + W - 3, sy - 8, sy - 8, wall)

    # BG fill throughout
    _lm_fill_bg(world, left, left + W - 1, sy - 9, sy - 1, wall)

    # Colonnade: 4 columns per side
    _lm_cols(world, left + 2, left + W // 2 - 1, sy - 2, 6, col, cap, spacing=4)
    _lm_cols(world, left + W // 2, left + W - 3, sy - 2, 6, col, cap, spacing=4)

    # Arched bays on outer wall (bg)
    for bx in range(left + 3, left + W - 3, 5):
        _lm_bg(world, bx, sy - 5, arch)

    # Central fountain feature (BG so it doesn't block walking)
    _lm_bg(world, flag_bx, sy - 2, SHELL_FOUNTAIN)
    _lm_bg(world, flag_bx - 1, sy - 2, MARBLE_PLINTH)
    _lm_bg(world, flag_bx + 1, sy - 2, MARBLE_PLINTH)

    # Clear entrance on both outer walls
    for bx in (left, left + 1, left + W - 2, left + W - 1):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Harbor Exchange  (mercantile, coastal)  — quay hall with warehouse wings
# ---------------------------------------------------------------------------

def _place_harbor_exchange(world, spec, biome, right_bx, sy, rng):
    W = 32
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    # Quay approach (left 5 blocks) — limestone paving, low bollards
    _lm_fill(world, left, left + 4, sy, sy, LIMESTONE_BLOCK)
    _lm_fill(world, left, left + 4, sy - 1, sy - 1, COMPASS_PAVING)
    _lm_set(world, left + 1, sy - 2, RAIN_BARREL)
    _lm_set(world, left + 3, sy - 2, RAIN_BARREL)

    # Main exchange hall (middle 22 blocks, 9 tall)
    hx = left + 5
    _lm_fill(world, hx, hx + 21, sy, sy, POLISHED_MARBLE)
    _lm_fill(world, hx, hx + 21, sy - 9, sy - 9, POLISHED_MARBLE)
    for bx in (hx, hx + 21):
        _lm_fill(world, bx, bx, sy - 9, sy, POLISHED_MARBLE)
    _lm_fill_bg(world, hx + 1, hx + 20, sy - 9, sy - 1, POLISHED_MARBLE)
    _lm_fill(world, hx + 1, hx + 20, sy - 1, sy - 1, COMPASS_PAVING)

    # Arched hall windows (bg)
    for bx in range(hx + 2, hx + 20, 5):
        _lm_bg(world, bx, sy - 6, ROMAN_ARCH_REN)

    # Hall columns
    _lm_cols(world, hx + 1, hx + 20, sy - 2, 6, GARDEN_COLUMN, DORIC_CAPITAL, spacing=5)

    # Warehouse wing (right 5 blocks)
    wx = left + W - 5
    _lm_fill(world, wx, wx + 4, sy, sy, LIMESTONE_BLOCK)
    _lm_fill_bg(world, wx, wx + 4, sy - 6, sy, LIMESTONE_BLOCK)
    for bx in range(wx, wx + 4, 2):
        _lm_bg(world, bx, sy - 2, RAIN_BARREL)

    # Entrance on both hall walls so player can walk straight through
    for by in range(sy - 3, sy):
        _lm_set(world, hx, by, AIR)
        _lm_set(world, hx + 21, by, AIR)

    # Quay bollards and fountain as BG (don't block approach)
    _lm_bg(world, left + 1, sy - 2, RAIN_BARREL)
    _lm_bg(world, left + 3, sy - 2, RAIN_BARREL)

    # Central fountain (BG)
    _lm_bg(world, flag_bx, sy - 2, SHELL_FOUNTAIN)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Caravanserai  (mercantile, silk_road)  — courtyard inn with arched arcade
# ---------------------------------------------------------------------------

def _place_caravanserai(world, spec, biome, right_bx, sy, rng):
    W = 32
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    wall = SANDSTONE_ASHLAR

    # Outer enclosure wall (full perimeter, 2 thick, 8 tall)
    _lm_fill(world, left, left + W - 1, sy, sy, wall)
    _lm_fill(world, left, left + W - 1, sy - 8, sy - 8, wall)
    for by in range(sy - 8, sy + 1):
        _lm_set(world, left, by, wall)
        _lm_set(world, left + W - 1, by, wall)
        _lm_set(world, left + 1, by, wall)
        _lm_set(world, left + W - 2, by, wall)
    _lm_fill_bg(world, left, left + W - 1, sy - 8, sy - 1, wall)

    # Grand Mughal archway gate on the right side wall (facing the town)
    for by in range(sy - 5, sy):
        _lm_set(world, left + W - 2, by, AIR)
        _lm_set(world, left + W - 1, by, AIR)
    _lm_bg(world, left + W - 2, sy - 5, MUGHAL_ARCH)
    _lm_bg(world, left + W - 1, sy - 5, MUGHAL_ARCH)

    # Secondary arch on the left wall
    for by in range(sy - 4, sy):
        _lm_set(world, left, by, AIR)
        _lm_set(world, left + 1, by, AIR)

    # Interior arcades (3 arches per side on inner wall face)
    for bx in range(left + 3, left + 12, 3):
        _lm_bg(world, bx, sy - 4, MUGHAL_ARCH)
    for bx in range(left + W - 4, left + W - 13, -3):
        _lm_bg(world, bx, sy - 4, MUGHAL_ARCH)

    # Courtyard floor
    _lm_fill(world, left + 2, left + W - 3, sy - 1, sy - 1, SANDSTONE_BLOCK)

    # Lantern posts and central brazier as BG
    for bx in (left + 3, left + W - 4):
        _lm_bg(world, bx, sy - 2, STONE_LANTERN)
    _lm_bg(world, flag_bx, sy - 2, TRIPOD_BRAZIER)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Archive  (scholarly, base)  — grand reading hall with flanking galleries
# ---------------------------------------------------------------------------

def _place_archive(world, spec, biome, right_bx, sy, rng):
    W = 34
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    if biome == "mediterranean":
        wall, floor, arch = POLISHED_MARBLE, ROMAN_MOSAIC, ROMAN_ARCH_REN
        col, cap, light = GARDEN_COLUMN, DORIC_CAPITAL, BRAZIER
    elif biome == "east_asian":
        wall, floor, arch = PINE_PLANK_WALL, TATAMI_PAVING, PAGODA_EAVE
        col, cap, light = PINE_PLANK_WALL, PAGODA_EAVE, STONE_LANTERN
    else:
        wall, floor, arch = LIMESTONE_BLOCK, COMPASS_PAVING, ROMANESQUE_ARCH
        col, cap, light = GARDEN_COLUMN, DORIC_CAPITAL, TORCH

    # Foundation
    _lm_fill(world, left, left + W - 1, sy, sy, wall)

    # Flanking gallery wings (6 wide, 7 tall each)
    for wing_x in (left, left + W - 7):
        _lm_fill(world, wing_x, wing_x + 6, sy - 7, sy - 7, wall)
        for bx in (wing_x, wing_x + 6):
            _lm_fill(world, bx, bx, sy - 7, sy, wall)
        _lm_fill_bg(world, wing_x + 1, wing_x + 5, sy - 7, sy - 1, wall)
        _lm_fill(world, wing_x + 1, wing_x + 5, sy - 1, sy - 1, floor)
        _lm_bg(world, wing_x + 3, sy - 4, arch)
        # Scroll shelves on back wall
        for bx in range(wing_x + 1, wing_x + 6, 2):
            _lm_bg(world, bx, sy - 3, PHILOSOPHERS_SCROLL)
            _lm_bg(world, bx, sy - 5, PHILOSOPHERS_SCROLL)

    # Central reading hall (22 wide, 10 tall)
    cx = left + 6
    _lm_fill(world, cx, cx + 21, sy - 10, sy - 10, wall)
    _lm_fill(world, cx, cx + 21, sy - 11, sy - 11, wall)
    for bx in (cx, cx + 21):
        _lm_fill(world, bx, bx, sy - 10, sy, wall)
    _lm_fill_bg(world, cx + 1, cx + 20, sy - 10, sy - 1, wall)
    _lm_fill(world, cx + 1, cx + 20, sy - 1, sy - 1, floor)
    _lm_set(world, cx, sy - 12, light)
    _lm_set(world, cx + 21, sy - 12, light)

    # Hall arches and columns
    for bx in range(cx + 3, cx + 19, 5):
        _lm_bg(world, bx, sy - 7, arch)
    _lm_cols(world, cx + 1, cx + 20, sy - 2, 7, col, cap, spacing=5)

    # Scroll panels on hall back wall
    for bx in range(cx + 2, cx + 20, 3):
        _lm_bg(world, bx, sy - 4, PHILOSOPHERS_SCROLL)

    # Central reading table + lectern (BG so aisles stay clear)
    _lm_bg(world, flag_bx, sy - 3, HERMES_STELE)
    _lm_bg(world, flag_bx - 2, sy - 2, CARVED_BENCH)
    _lm_bg(world, flag_bx + 2, sy - 2, CARVED_BENCH)

    # Entrance: clear outer wing walls and the wing/hall junction
    for bx in (left, left + W - 1, left + 6, left + W - 7):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Imperial Library  (scholarly, east_asian)  — two-storey pagoda library
# ---------------------------------------------------------------------------

def _place_imperial_library(world, spec, biome, right_bx, sy, rng):
    W = 34
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    # Lower hall (full width, 7 tall)
    _lm_fill(world, left, left + W - 1, sy, sy, PINE_PLANK_WALL)
    _lm_fill(world, left, left + W - 1, sy - 7, sy - 7, PINE_PLANK_WALL)
    for bx in (left, left + W - 1):
        _lm_fill(world, bx, bx, sy - 7, sy, PINE_PLANK_WALL)
    _lm_fill_bg(world, left + 1, left + W - 2, sy - 7, sy - 1, LACQUER_PANEL)
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, TATAMI_PAVING)

    # Lower hall columns and scroll shelves
    for bx in range(left + 4, left + W - 4, 4):
        _lm_bg(world, bx, sy - 2, GARDEN_COLUMN)
        _lm_bg(world, bx, sy - 3, GARDEN_COLUMN)
        _lm_bg(world, bx, sy - 4, LOTUS_CAPITAL)
        _lm_bg(world, bx + 1, sy - 5, PHILOSOPHERS_SCROLL)
        _lm_bg(world, bx - 1, sy - 5, PHILOSOPHERS_SCROLL)

    # Pagoda eave on lower roof
    _lm_fill(world, left - 1, left + W, sy - 8, sy - 8, PAGODA_EAVE)

    # Upper storey (narrower, 6 tall)
    up_l, up_r = left + 5, left + W - 6
    _lm_fill(world, up_l, up_r, sy - 13, sy - 13, PINE_PLANK_WALL)
    for bx in (up_l, up_r):
        _lm_fill(world, bx, bx, sy - 13, sy - 8, PINE_PLANK_WALL)
    _lm_fill_bg(world, up_l + 1, up_r - 1, sy - 13, sy - 9, LACQUER_PANEL)
    _lm_fill(world, up_l + 1, up_r - 1, sy - 9, sy - 9, TATAMI_PAVING)

    # Upper pagoda eave
    _lm_fill(world, up_l - 1, up_r + 1, sy - 14, sy - 14, PAGODA_EAVE)

    # Torii gate approach and stone lanterns — BG so entrance stays clear
    _lm_bg(world, left + 2, sy - 2, TORII_PANEL)
    _lm_bg(world, left + W - 3, sy - 2, TORII_PANEL)
    _lm_bg(world, left + 2, sy - 3, TORII_PANEL)
    _lm_bg(world, left + W - 3, sy - 3, TORII_PANEL)
    _lm_bg(world, left + 1, sy - 2, STONE_LANTERN)
    _lm_bg(world, left + W - 2, sy - 2, STONE_LANTERN)

    # Central scroll rack and reading area
    for bx in range(flag_bx - 3, flag_bx + 4, 2):
        _lm_bg(world, bx, sy - 5, PHILOSOPHERS_SCROLL)
    _lm_bg(world, flag_bx, sy - 2, CARVED_BENCH)

    # Entrance
    for by in range(sy - 3, sy):
        _lm_set(world, left, by, AIR)
        _lm_set(world, left + W - 1, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Observatory  (scholarly, mediterranean)  — domed tower with flanking wings
# ---------------------------------------------------------------------------

def _place_observatory(world, spec, biome, right_bx, sy, rng):
    W = 28
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    # Low flanking wings (6 wide, 6 tall each)
    for wx in (left, left + W - 6):
        _lm_fill(world, wx, wx + 5, sy, sy, POLISHED_MARBLE)
        _lm_fill(world, wx, wx + 5, sy - 6, sy - 6, POLISHED_MARBLE)
        for bx in (wx, wx + 5):
            _lm_fill(world, bx, bx, sy - 6, sy, POLISHED_MARBLE)
        _lm_fill_bg(world, wx + 1, wx + 4, sy - 6, sy - 1, POLISHED_MARBLE)
        _lm_fill(world, wx + 1, wx + 4, sy - 1, sy - 1, COMPASS_PAVING)
        _lm_bg(world, wx + 2, sy - 4, ROMAN_ARCH_REN)

    # Sundial & approach paving (left wing deco)
    _lm_set(world, left + 2, sy - 2, TALL_SUNDIAL)
    _lm_fill(world, left + 3, left + 4, sy - 1, sy - 1, COMPASS_PAVING)

    # Central domed observation tower (8 wide, 12 tall)
    tx = left + 10
    _lm_fill(world, tx, tx + 7, sy, sy, POLISHED_MARBLE)
    for bx in (tx, tx + 7):
        _lm_fill(world, bx, bx, sy - 12, sy, POLISHED_MARBLE)
    _lm_fill_bg(world, tx + 1, tx + 6, sy - 12, sy - 1, POLISHED_MARBLE)
    _lm_fill(world, tx + 1, tx + 6, sy - 1, sy - 1, ROMAN_MOSAIC)

    # Dome cap — narrows over 3 rows (each row insets by 1 from previous)
    for row in range(3):
        by = sy - 13 - row
        _lm_fill(world, tx + 1 + row, tx + 6 - row, by, by, POLISHED_MARBLE)

    # Observatory ring arches
    for bx in (tx + 1, tx + 3, tx + 5):
        _lm_bg(world, bx, sy - 9, ROMAN_ARCH_REN)

    # Columns inside tower
    _lm_cols(world, tx + 1, tx + 6, sy - 2, 8, GARDEN_COLUMN, DORIC_CAPITAL, spacing=3)

    # Open roof platform (clear top 2 rows of tower interior)
    for by in range(sy - 12, sy - 10):
        for bx in range(tx + 1, tx + 7):
            _lm_set(world, bx, by, AIR)

    # Entrance passages to tower
    for bx in (tx, tx + 7):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Great Shrine  (pious, base)  — grand temple with portico and inner sanctum
# ---------------------------------------------------------------------------

def _place_great_shrine(world, spec, biome, right_bx, sy, rng):
    W = 32
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    if biome == "mediterranean":
        wall, floor, arch = POLISHED_MARBLE, ROMAN_MOSAIC, ROMAN_ARCH_REN
        col, cap, light = GARDEN_COLUMN, DORIC_CAPITAL, BRAZIER
        panel = MARBLE_STATUE
    elif biome == "east_asian":
        wall, floor, arch = PINE_PLANK_WALL, TATAMI_PAVING, PAGODA_EAVE
        col, cap, light = PINE_PLANK_WALL, PAGODA_EAVE, STONE_LANTERN
        panel = VOTIVE_TABLET
    elif biome in ("desert", "silk_road"):
        wall, floor, arch = SANDSTONE_ASHLAR, SANDSTONE_BLOCK, MUGHAL_ARCH
        col, cap, light = SANDSTONE_COLUMN, MUGHAL_ARCH, TRIPOD_BRAZIER
        panel = VOTIVE_TABLET
    else:
        wall, floor, arch = LIMESTONE_BLOCK, COBBLESTONE, ROMANESQUE_ARCH
        col, cap, light = GARDEN_COLUMN, DORIC_CAPITAL, TORCH
        panel = VOTIVE_TABLET

    # Foundation
    _lm_fill(world, left, left + W - 1, sy, sy, wall)

    # Colonnaded outer portico (full width, 6 tall) — open front
    _lm_fill(world, left, left + W - 1, sy - 6, sy - 6, wall)
    for bx in (left, left + W - 1):
        _lm_fill(world, bx, bx, sy - 6, sy, wall)
    _lm_fill(world, left, left + W - 1, sy - 7, sy - 7, wall)  # pediment
    _lm_fill_bg(world, left + 1, left + W - 2, sy - 6, sy - 1, wall)

    # Columns across the portico front face
    for bx in range(left + 2, left + W - 2, 4):
        _lm_bg(world, bx, sy - 5, col)
        _lm_bg(world, bx, sy - 4, col)
        _lm_bg(world, bx, sy - 3, col)
        _lm_set(world, bx, sy - 6, cap)  # capital at roof

    # Portico floor
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, floor)

    # Inner sanctum (narrower, sits behind — 16 wide, 10 tall)
    sx = left + 8
    _lm_fill(world, sx, sx + 15, sy - 10, sy - 10, wall)
    _lm_fill(world, sx, sx + 15, sy - 11, sy - 11, wall)
    for bx in (sx, sx + 15):
        _lm_fill(world, bx, bx, sy - 11, sy, wall)
    _lm_fill_bg(world, sx + 1, sx + 14, sy - 10, sy - 1, wall)
    _lm_fill(world, sx + 1, sx + 14, sy - 1, sy - 1, floor)
    _lm_set(world, sx + 7, sy - 12, light)
    _lm_set(world, sx + 8, sy - 12, light)

    # Sanctum arches and altar panels
    _lm_bg(world, sx + 4, sy - 8, arch)
    _lm_bg(world, sx + 11, sy - 8, arch)
    _lm_bg(world, flag_bx, sy - 5, panel)
    _lm_bg(world, flag_bx - 1, sy - 6, panel)
    _lm_bg(world, flag_bx + 1, sy - 6, panel)

    # Prayer flag altar in sanctum — BG so player can reach the flag
    _lm_bg(world, flag_bx, sy - 3, PRAYER_FLAG_BLOCK)
    _lm_bg(world, flag_bx - 1, sy - 2, MARBLE_PLINTH)
    _lm_bg(world, flag_bx + 1, sy - 2, MARBLE_PLINTH)

    # Outer portico entrances (both sides)
    for by in range(sy - 4, sy):
        _lm_set(world, left, by, AIR)
        _lm_set(world, left + W - 1, by, AIR)

    # Inner sanctum entrances — clear both sanctum walls at ground level
    for by in range(sy - 3, sy):
        _lm_set(world, sx, by, AIR)
        _lm_set(world, sx + 15, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Sea Temple  (pious, coastal)  — open marine temple on limestone quay
# ---------------------------------------------------------------------------

def _place_sea_temple(world, spec, biome, right_bx, sy, rng):
    W = 30
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    # Sea-wall quay approach (left 5 blocks) — open forecourt, floor only
    _lm_fill(world, left, left + 4, sy, sy, LIMESTONE_BLOCK)
    _lm_fill(world, left, left + 4, sy - 1, sy - 1, COMPASS_PAVING)
    _lm_bg(world, left + 2, sy - 2, SHELL_FOUNTAIN)

    # Open colonnaded hall (20 wide, 9 tall) — open on the sea side (left)
    hx = left + 5
    _lm_fill(world, hx, hx + 19, sy, sy, LIMESTONE_BLOCK)
    _lm_fill(world, hx, hx + 19, sy - 9, sy - 9, LIMESTONE_BLOCK)
    # Back wall only (sealed)
    _lm_fill(world, hx + 19, hx + 19, sy - 9, sy, LIMESTONE_BLOCK)
    _lm_fill_bg(world, hx, hx + 18, sy - 9, sy - 1, LIMESTONE_BLOCK)
    _lm_fill(world, hx, hx + 18, sy - 1, sy - 1, COMPASS_PAVING)

    # Arched colonnade on the front (sea-facing) edge
    for bx in range(hx, hx + 19, 4):
        _lm_bg(world, bx, sy - 6, ROMAN_ARCH_REN)
        _lm_set(world, bx, sy - 9, BRAZIER)

    # Columns
    _lm_cols(world, hx, hx + 18, sy - 2, 7, GARDEN_COLUMN, DORIC_CAPITAL, spacing=4)

    # Inner altar — all BG so player can reach the flag
    _lm_bg(world, hx + 14, sy - 2, MARBLE_PLINTH)
    _lm_bg(world, hx + 14, sy - 3, PRAYER_FLAG_BLOCK)
    _lm_bg(world, hx + 16, sy - 5, MARBLE_STATUE)
    _lm_bg(world, hx + 18, sy - 4, VOTIVE_TABLET)

    # Right wing (5 wide, 6 tall — votive alcove, BG only)
    wx = left + W - 5
    _lm_fill(world, wx, wx + 4, sy, sy, LIMESTONE_BLOCK)
    _lm_fill_bg(world, wx, wx + 3, sy - 6, sy, LIMESTONE_BLOCK)
    _lm_bg(world, wx + 2, sy - 3, VOTIVE_TABLET)

    # Entrance on the right (town-facing) back wall
    for by in range(sy - 3, sy):
        _lm_set(world, hx + 19, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Canopy Sanctum  (pious, jungle)  — living-wall open jungle sanctuary
# ---------------------------------------------------------------------------

def _place_canopy_sanctum(world, spec, biome, right_bx, sy, rng):
    W = 28
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    # Stone base / platform
    _lm_fill(world, left, left + W - 1, sy, sy, LIMESTONE_BLOCK)

    # Living outer walls — GLOW_VINE draped over limestone pillars
    for bx in range(left, left + W, 3):
        _lm_fill(world, bx, bx, sy - 9, sy, LIMESTONE_BLOCK)
    for bx in range(left, left + W):
        for by in range(sy - 10, sy - 1):
            _lm_bg(world, bx, by, GLOW_VINE)

    # Stone arch canopy roof
    _lm_fill(world, left - 1, left + W, sy - 10, sy - 10, LIMESTONE_BLOCK)
    _lm_fill(world, left, left + W - 1, sy - 9, sy - 9, LIMESTONE_BLOCK)

    # Interior floor (natural mossy stone)
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, COBBLESTONE)

    # Bamboo clusters flanking entrance — BG so gaps between pillars stay open
    _lm_bg(world, left + 1, sy - 2, BAMBOO_CLUMP)
    _lm_bg(world, left + 2, sy - 2, BAMBOO_CLUMP)
    _lm_bg(world, left + W - 2, sy - 2, BAMBOO_CLUMP)
    _lm_bg(world, left + W - 3, sy - 2, BAMBOO_CLUMP)

    # Paper lanterns strung across ceiling
    for bx in range(left + 3, left + W - 3, 3):
        _lm_set(world, bx, sy - 7, PAPER_LANTERN)

    # Lotus pond at centre approach
    _lm_set(world, flag_bx - 2, sy - 2, LOTUS_POND)
    _lm_set(world, flag_bx + 2, sy - 2, LOTUS_POND)

    # Altar: prayer flag and lotus in BG, altar platform at floor level only
    _lm_fill(world, flag_bx - 1, flag_bx + 1, sy - 1, sy - 1, LIMESTONE_BLOCK)
    _lm_bg(world, flag_bx, sy - 2, PRAYER_FLAG_BLOCK)
    _lm_bg(world, flag_bx - 1, sy - 4, LOTUS_BLOCK)
    _lm_bg(world, flag_bx + 1, sy - 4, LOTUS_BLOCK)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Stoneworks  (builder, base)  — forge complex with workshop and kiln
# ---------------------------------------------------------------------------

def _place_stoneworks(world, spec, biome, right_bx, sy, rng):
    W = 32
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    if biome == "alpine":
        wall, floor = ROUGH_STONE_WALL, LIMESTONE_BLOCK
        arch, light = ROMANESQUE_ARCH, TRIPOD_BRAZIER
    else:
        wall, floor = COBBLESTONE, COBBLESTONE
        arch, light = POINTED_ARCH, TRIPOD_BRAZIER

    # Foundation
    _lm_fill(world, left, left + W - 1, sy, sy, wall)

    # Outer workshop shell (full width, 8 tall)
    _lm_fill(world, left, left + W - 1, sy - 8, sy - 8, wall)
    for bx in (left, left + W - 1):
        _lm_fill(world, bx, bx, sy - 8, sy, wall)
    _lm_fill_bg(world, left + 1, left + W - 2, sy - 8, sy - 1, wall)
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, floor)

    # Interior dividing wall creating two bays
    mid = left + W // 2
    _lm_fill(world, mid, mid, sy - 8, sy - 4, wall)
    for by in range(sy - 3, sy):
        _lm_set(world, mid, by, AIR)  # open passage through divider

    # Kiln and forge in the two bays — BG so walkways stay open
    _lm_bg(world, left + 5, sy - 2, FORGE_BLOCK)
    _lm_bg(world, left + W - 6, sy - 2, FORGE_BLOCK)
    _lm_bg(world, left + 4, sy - 2, light)
    _lm_bg(world, left + W - 5, sy - 2, light)
    _lm_bg(world, left + 7, sy - 2, WEAPON_RACK_BLOCK)
    _lm_bg(world, left + W - 8, sy - 2, WEAPON_RACK_BLOCK)

    # Arched bays on outer wall
    _lm_bg(world, left + 4, sy - 5, arch)
    _lm_bg(world, left + W - 5, sy - 5, arch)

    # Storage barrels
    for bx in (left + 9, left + 10, left + W - 10, left + W - 11):
        _lm_bg(world, bx, sy - 2, RAIN_BARREL)
        _lm_bg(world, bx, sy - 3, RAIN_BARREL)

    # Entrance (clear front wall base)
    for by in range(sy - 3, sy):
        _lm_set(world, left, by, AIR)
        _lm_set(world, left + W - 1, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Stonecutters Guild  (builder, alpine)  — alpine guild hall with quarry face
# ---------------------------------------------------------------------------

def _place_stonecutters_guild(world, spec, biome, right_bx, sy, rng):
    W = 28
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    # Quarry-face foundation: uneven rough stone base
    _lm_fill(world, left, left + W - 1, sy, sy, ROUGH_STONE_WALL)
    for bx in range(left, left + W, 3):
        _lm_set(world, bx, sy + 1, ROUGH_STONE_WALL)

    # Guild hall main structure (full width, 8 tall)
    _lm_fill(world, left, left + W - 1, sy - 8, sy - 8, LIMESTONE_BLOCK)
    _lm_fill(world, left, left + W - 1, sy - 9, sy - 9, LIMESTONE_BLOCK)
    for bx in (left, left + W - 1):
        _lm_fill(world, bx, bx, sy - 9, sy, LIMESTONE_BLOCK)
    _lm_fill_bg(world, left + 1, left + W - 2, sy - 9, sy - 1, ROUGH_STONE_WALL)
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, LIMESTONE_BLOCK)

    # Romanesque arched portal — central 3-wide, 5-tall
    for bx in range(flag_bx - 1, flag_bx + 2):
        for by in range(sy - 4, sy):
            _lm_set(world, bx, by, AIR)
    _lm_bg(world, flag_bx, sy - 5, ROMANESQUE_ARCH)

    # Arched windows flanking portal
    _lm_bg(world, flag_bx - 5, sy - 5, ROMANESQUE_ARCH)
    _lm_bg(world, flag_bx + 5, sy - 5, ROMANESQUE_ARCH)

    # Tripod braziers well inside — not at the entrance columns
    _lm_bg(world, left + 3, sy - 2, TRIPOD_BRAZIER)
    _lm_bg(world, left + W - 4, sy - 2, TRIPOD_BRAZIER)

    # Tool display and workbench — all BG
    _lm_bg(world, flag_bx - 3, sy - 2, WEAPON_RACK_BLOCK)
    _lm_bg(world, flag_bx + 3, sy - 2, WEAPON_RACK_BLOCK)
    _lm_bg(world, flag_bx - 2, sy - 2, RAIN_BARREL)
    _lm_bg(world, flag_bx + 2, sy - 2, RAIN_BARREL)

    # Clear outer walls for entry
    for bx in (left, left + 1, left + W - 2, left + W - 1):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Pleasure Garden  (hedonist, base)  — formal garden with pergola colonnade
# ---------------------------------------------------------------------------

def _place_pleasure_garden(world, spec, biome, right_bx, sy, rng):
    W = 36
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    if biome in ("mediterranean",):
        wall, floor = POLISHED_MARBLE, ROMAN_MOSAIC
        arch, light = TRELLIS_ARCH, BRAZIER
    elif biome in ("east_asian",):
        wall, floor = PINE_PLANK_WALL, ZEN_GRAVEL
        arch, light = MOON_GATE, STONE_LANTERN
    else:
        wall, floor = LIMESTONE_BLOCK, COMPASS_PAVING
        arch, light = TRELLIS_ARCH, TORCH

    # Ground-level garden floor (the whole plot is walkable open garden)
    _lm_fill(world, left, left + W - 1, sy, sy, wall)
    _lm_fill(world, left, left + W - 1, sy - 1, sy - 1, floor)

    # Pergola colonnade: columns in BG so the garden is fully walkable
    col_ys = list(range(left + 2, left + W - 2, 4))
    for bx in col_ys:
        for by in range(sy - 6, sy - 1):
            _lm_bg(world, bx, by, wall)
        _lm_bg(world, bx, sy - 7, light)
        _lm_bg(world, bx, sy - 6, arch if bx != col_ys[0] else wall)

    # Trellis / pergola rooftop beams between columns (BG)
    _lm_fill_bg(world, left + 2, left + W - 3, sy - 7, sy - 7, wall)

    # Flower beds and topiaries in the open bays between columns
    topiary_choices = [TOPIARY_PEACOCK, TOPIARY_BEAR, TOPIARY_ARCH, TOPIARY_PEACOCK]
    for i, bx in enumerate(col_ys[:-1]):
        mid_bx = bx + 2
        _lm_bg(world, mid_bx, sy - 2, LAVENDER_BED if i % 2 == 0 else ROSE_BED)
        _lm_set(world, mid_bx + 1, sy - 2, topiary_choices[i % len(topiary_choices)])

    # Central fountain as focal point (BG)
    _lm_bg(world, flag_bx, sy - 2, SHELL_FOUNTAIN)
    _lm_bg(world, flag_bx - 2, sy - 2, OLIVE_BRANCH)
    _lm_bg(world, flag_bx + 2, sy - 2, OLIVE_BRANCH)

    # East Asian variant gets koi pool instead of fountain
    if biome == "east_asian":
        _lm_bg(world, flag_bx, sy - 2, KOI_POOL)
        _lm_bg(world, flag_bx - 1, sy - 2, KOI_POOL)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Vineyard Hall  (hedonist, mediterranean)  — wine hall with grape arcade
# ---------------------------------------------------------------------------

def _place_vineyard_hall(world, spec, biome, right_bx, sy, rng):
    W = 32
    left = right_bx - W
    flag_bx = right_bx - W // 2
    _lm_clear_terrain(world, left, W, sy)

    # Grapevine approach arcade — 5 blocks each side, all BG to stay walkable
    for side_bx in (range(left, left + 5), range(left + W - 5, left + W)):
        for bx in side_bx:
            _lm_set(world, bx, sy, POLISHED_MARBLE)
            _lm_bg(world, bx, sy - 1, GRAPEVINE_CROP_MATURE)
            _lm_bg(world, bx, sy - 2, GRAPEVINE_CROP_MATURE)
            _lm_bg(world, bx, sy - 3, GRAPEVINE_CROP_MATURE)

    # Central wine hall (22 wide, 9 tall)
    hx = left + 5
    _lm_fill(world, hx, hx + 21, sy, sy, POLISHED_MARBLE)
    _lm_fill(world, hx, hx + 21, sy - 9, sy - 9, POLISHED_MARBLE)
    for bx in (hx, hx + 21):
        _lm_fill(world, bx, bx, sy - 9, sy, POLISHED_MARBLE)
    _lm_fill_bg(world, hx + 1, hx + 20, sy - 9, sy - 1, POLISHED_MARBLE)
    _lm_fill(world, hx + 1, hx + 20, sy - 1, sy - 1, ROMAN_MOSAIC)

    # Barrel cellar alcoves on back wall (bg)
    for bx in range(hx + 2, hx + 20, 3):
        _lm_bg(world, bx, sy - 2, RAIN_BARREL)
        _lm_bg(world, bx, sy - 3, RAIN_BARREL)

    # Arched bays in hall
    for bx in range(hx + 3, hx + 19, 5):
        _lm_bg(world, bx, sy - 6, ROMAN_ARCH_REN)

    # Columns
    _lm_cols(world, hx + 1, hx + 20, sy - 2, 7, GARDEN_COLUMN, DORIC_CAPITAL, spacing=5)

    # Central tasting table (BG so walkway stays clear)
    _lm_bg(world, flag_bx, sy - 2, SHELL_FOUNTAIN)
    _lm_bg(world, flag_bx - 2, sy - 2, CARVED_BENCH)
    _lm_bg(world, flag_bx + 2, sy - 2, CARVED_BENCH)
    _lm_bg(world, flag_bx, sy - 4, OLIVE_BRANCH)

    # Entrance
    for bx in (hx, hx + 21):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

_BUILDERS = {
    "arena":            _place_arena,
    "war_camp":         _place_war_camp,
    "gladiator":        _place_gladiator_pits,
    "bazaar":           _place_grand_bazaar,
    "harbor":           _place_harbor_exchange,
    "caravanserai":     _place_caravanserai,
    "archive":          _place_archive,
    "imperial_library": _place_imperial_library,
    "observatory":      _place_observatory,
    "shrine":           _place_great_shrine,
    "sea_temple":       _place_sea_temple,
    "canopy_sanctum":   _place_canopy_sanctum,
    "stoneworks":       _place_stoneworks,
    "stonecutters":     _place_stonecutters_guild,
    "garden":           _place_pleasure_garden,
    "vineyard":         _place_vineyard_hall,
}


def place_landmark_building(world, spec, biome_group, right_bx, sy, rng, region) -> int:
    """Build the grand landmark structure and return the flag_x interaction point."""
    fn = _BUILDERS.get(spec["effect"])
    if fn is None:
        return right_bx
    return fn(world, spec, biome_group or "", right_bx, sy, rng)
