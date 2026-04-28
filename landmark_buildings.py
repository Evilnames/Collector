"""
landmark_buildings.py — Grand building structures for capital landmarks.

Each landmark type gets a distinct architectural silhouette and interior.
Buildings are 28–42 blocks wide and 8–16 blocks tall, placed opposite the
capital palace. All functions share the same signature and return flag_x.
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
    STUDDED_OAK_DOOR_CLOSED, SHOJI_DOOR_CLOSED, BRONZE_DOOR_CLOSED,
    COBALT_DOOR_CLOSED, SANDALWOOD_DOOR_CLOSED, STONE_SLAB_DOOR_CLOSED,
)


# ---------------------------------------------------------------------------
# Shared helpers
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

def _lm_clear_terrain(world, left_bx, width, sy) -> int:
    """Level terrain in the landmark footprint. Returns the floor sy used."""
    from cities import _city_terrain_profile
    for cx in range((left_bx - 2) // CHUNK_W, (left_bx + width + 4) // CHUNK_W + 1):
        world.load_chunk(cx)
    profile = _city_terrain_profile(world, left_bx, left_bx + width)
    vals = sorted(profile.values())
    sy = vals[len(vals) // 2]
    # Clear from actual column surface (+ tree canopy buffer) down to floor
    for bx in range(left_bx - 1, left_bx + width + 2):
        col_sy = world.surface_y_at(bx)
        clear_from = max(0, min(col_sy, sy) - 30)
        for by in range(clear_from, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
    # Fill valleys up to floor level
    for bx in range(left_bx, left_bx + width + 1):
        col_sy = world.surface_y_at(bx)
        for by in range(sy, col_sy + 1):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)
        if 0 <= sy < world.height and world.get_block(bx, sy) != BEDROCK:
            world.set_block(bx, sy, STONE)
    return sy

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

def _lm_tower(world, bx, bot_y, height, wall, light=None, cap=None):
    """Build a solid foreground tower column and optional light on top."""
    _lm_fill(world, bx, bx + 1, bot_y - height, bot_y, wall)
    _lm_fill_bg(world, bx, bx + 1, bot_y - height, bot_y, wall)
    if light:
        _lm_set(world, bx,     bot_y - height - 1, light)
        _lm_set(world, bx + 1, bot_y - height - 1, light)
    if cap:
        _lm_fill(world, bx - 1, bx + 2, bot_y - height, bot_y - height, cap)

def _lm_door(world, bx, sy, door_block):
    """Place a closed 2-tall door at bx. Bottom at sy-1, top at sy-2."""
    _lm_set(world, bx, sy - 1, door_block)
    _lm_set(world, bx, sy - 2, door_block)

def _lm_entrance(world, bx, sy, door_block):
    """Cut a clear opening through whatever is at bx and place a door there.
    Use this at the outer left/right edges so the player can walk in from either side."""
    for by in range(sy - 4, sy):
        _lm_set(world, bx, by, AIR)
    _lm_door(world, bx, sy, door_block)


# ---------------------------------------------------------------------------
# Arena  (martial, base)  — tiered colosseum with gate towers and vomitoria
# ---------------------------------------------------------------------------

def _place_arena(world, spec, biome, right_bx, sy, rng):
    W = 36
    left  = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    if biome == "mediterranean":
        wall, floor, arch, light = POLISHED_MARBLE, COMPASS_PAVING, ROMAN_ARCH_REN, BRAZIER
        panel = HERALDIC_PANEL
        door = BRONZE_DOOR_CLOSED
    elif biome in ("east_asian", "jungle"):
        wall, floor, arch, light = PINE_PLANK_WALL, TATAMI_PAVING, PAGODA_EAVE, STONE_LANTERN
        panel = LACQUER_PANEL
        door = SHOJI_DOOR_CLOSED
    else:
        wall, floor, arch, light = LIMESTONE_BLOCK, COBBLESTONE, ROMANESQUE_ARCH, BRAZIER
        panel = HERALDIC_PANEL
        door = STUDDED_OAK_DOOR_CLOSED

    # Foundation
    _lm_fill(world, left, left + W - 1, sy, sy, wall)

    # Gate towers — 3 wide, 14 tall, flanking the entrance on each side
    for side in (left, left + W - 3):
        _lm_fill(world, side, side + 2, sy - 14, sy, wall)
        _lm_fill_bg(world, side, side + 2, sy - 14, sy, wall)
        # Arch bays in tower face
        _lm_bg(world, side + 1, sy - 8, arch)
        _lm_bg(world, side + 1, sy - 4, arch)
        # Brazier crown
        _lm_set(world, side + 1, sy - 15, light)

    # Four ascending seating tiers per side (outer → inner, stepping down)
    for dx, h in [(3, 11), (5, 8), (7, 5), (9, 3)]:
        _lm_fill(world, left + dx, left + dx + 1, sy - h, sy, wall)
        _lm_fill(world, left + W - 2 - dx, left + W - 1 - dx, sy - h, sy, wall)

    # Pit floor — the fighting surface
    _lm_fill(world, left + 11, left + W - 12, sy - 1, sy, floor)

    # Trophy panels and heraldry on the back interior wall
    _lm_fill_bg(world, left + 3, left + W - 4, sy - 11, sy, wall)
    _lm_bg(world, flag_bx,     sy - 5, TROPHY_PANEL_REN)
    _lm_bg(world, flag_bx - 1, sy - 6, panel)
    _lm_bg(world, flag_bx + 1, sy - 6, panel)
    _lm_bg(world, flag_bx - 3, sy - 4, panel)
    _lm_bg(world, flag_bx + 3, sy - 4, panel)

    # Additional trophy stands at each tier step
    for dx in (4, 8):
        _lm_bg(world, left + dx, sy - 3, TROPHY_PANEL_REN)
        _lm_bg(world, left + W - 1 - dx, sy - 3, TROPHY_PANEL_REN)

    # Vomitorium passages — clear rows at the base of the tiers (interior access)
    for bx in range(left + 3, left + 11):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)
    for bx in range(left + W - 11, left + W - 3):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)
    # Outer edge entrances — punch through gate tower walls so player can walk in
    _lm_entrance(world, left,         sy, door)
    _lm_entrance(world, left + W - 1, sy, door)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# War Camp  (martial, steppe)  — palisade with watchtower and longhouse
# ---------------------------------------------------------------------------

def _place_war_camp(world, spec, biome, right_bx, sy, rng):
    W = 34
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    # Palisade outer wall — alternating tall/short posts
    for bx in range(left, left + W):
        is_post = ((bx - left) % 2 == 0)
        h = 8 if is_post else 5
        _lm_fill(world, bx, bx, sy - h, sy, PINE_PLANK_WALL)
    _lm_fill_bg(world, left, left + W - 1, sy - 8, sy, NORDIC_PLANK)

    # Watchtower on the right side — 4 wide, 16 tall, rises well above palisade
    tx = left + W - 6
    _lm_fill(world, tx, tx + 3, sy - 16, sy, PINE_PLANK_WALL)
    _lm_fill_bg(world, tx, tx + 3, sy - 16, sy, NORDIC_PLANK)
    _lm_set(world, tx + 1, sy - 17, TORCH)
    _lm_set(world, tx + 2, sy - 17, TORCH)
    # Lookout platform overhangs by 1 on each side
    _lm_fill(world, tx - 1, tx + 4, sy - 14, sy - 14, PINE_PLANK_WALL)
    # Clear interior so the player can see inside
    for by in range(sy - 4, sy - 1):
        for bx in range(tx + 1, tx + 3):
            _lm_set(world, bx, by, AIR)
    _lm_bg(world, tx + 1, sy - 3, WEAPON_RACK_BLOCK)

    # Longhouse barracks in the interior
    hall_l, hall_r = left + 3, tx - 1
    _lm_fill(world, hall_l, hall_r, sy - 5, sy - 5, NORDIC_PLANK)
    _lm_fill_bg(world, hall_l, hall_r, sy - 5, sy - 1, NORDIC_PLANK)
    _lm_fill(world, hall_l - 1, hall_r + 1, sy - 6, sy - 6, PINE_PLANK_WALL)
    _lm_fill(world, hall_l - 2, hall_r + 2, sy - 7, sy - 7, PINE_PLANK_WALL)
    # Clear interior walkway
    for by in range(sy - 4, sy):
        for bx in range(hall_l + 1, hall_r):
            _lm_set(world, bx, by, AIR)

    # Central fire pit, weapon racks, benches
    _lm_bg(world, flag_bx, sy - 2, BRAZIER)
    for bx in (hall_l + 2, hall_l + 4, hall_r - 4, hall_r - 2):
        _lm_bg(world, bx, sy - 2, WEAPON_RACK_BLOCK)
    _lm_bg(world, flag_bx - 2, sy - 2, CARVED_BENCH)
    _lm_bg(world, flag_bx + 2, sy - 2, CARVED_BENCH)

    # Trophy poles flanking the palisade gate (foreground, tall)
    for pole_bx in (left + W // 2 - 4, left + W // 2 + 3):
        _lm_set(world, pole_bx, sy - 9, TROPHY_PANEL_REN)
        _lm_set(world, pole_bx, sy - 10, TROPHY_PANEL_REN)

    # Palisade gate — clear a 5-block opening in the front wall (interior feature)
    for bx in range(left + W // 2 - 2, left + W // 2 + 2):
        for by in range(sy - 5, sy):
            _lm_set(world, bx, by, AIR)
    # Outer edge entrances — punch through palisade at left/right so player can walk in
    _lm_entrance(world, left,         sy, STUDDED_OAK_DOOR_CLOSED)
    _lm_entrance(world, left + W - 1, sy, STUDDED_OAK_DOOR_CLOSED)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Gladiator Pits  (martial, desert)  — sunken sandstone arena with obelisk
# ---------------------------------------------------------------------------

def _place_gladiator_pits(world, spec, biome, right_bx, sy, rng):
    W = 32
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    wall = SANDSTONE_ASHLAR

    # Outer walls — 4 wide each side, 12 tall
    for dx in range(4):
        _lm_fill(world, left + dx, left + dx, sy - 12, sy, wall)
        _lm_fill(world, left + W - 1 - dx, left + W - 1 - dx, sy - 12, sy, wall)
    _lm_fill_bg(world, left, left + 3, sy - 12, sy, wall)
    _lm_fill_bg(world, left + W - 4, left + W - 1, sy - 12, sy, wall)

    # Sandstone column pilasters on the outer wall face
    for bx in (left + 1, left + W - 2):
        _lm_bg(world, bx, sy - 8, SANDSTONE_COLUMN)
        _lm_bg(world, bx, sy - 9, SANDSTONE_COLUMN)
        _lm_bg(world, bx, sy - 10, SANDSTONE_COLUMN)
    # Mughal archways
    _lm_bg(world, left + 1, sy - 7, MUGHAL_ARCH)
    _lm_bg(world, left + W - 2, sy - 7, MUGHAL_ARCH)
    _lm_bg(world, left + 1, sy - 3, MUGHAL_ARCH)
    _lm_bg(world, left + W - 2, sy - 3, MUGHAL_ARCH)
    # Braziers atop outer walls
    _lm_set(world, left + 2,     sy - 12, BRAZIER)
    _lm_set(world, left + W - 3, sy - 12, BRAZIER)

    # Three seating tiers per side
    for dx, h in [(4, 9), (6, 6), (8, 4)]:
        _lm_fill(world, left + dx, left + dx + 1, sy - h, sy, wall)
        _lm_fill(world, left + W - 2 - dx, left + W - 1 - dx, sy - h, sy, wall)

    # Pit floor — fighting sand
    _lm_fill(world, left + 10, left + W - 11, sy - 1, sy, SANDSTONE_BLOCK)

    # Interior BG walls
    _lm_fill_bg(world, left + 4, left + W - 5, sy - 9, sy, wall)
    _lm_bg(world, flag_bx - 1, sy - 5, MUGHAL_JALI)
    _lm_bg(world, flag_bx + 1, sy - 5, MUGHAL_JALI)

    # Victory obelisk — a tall single-block monument in the pit (BG)
    for by in range(sy - 7, sy - 1):
        _lm_bg(world, flag_bx, by, SANDSTONE_COLUMN)
    _lm_bg(world, flag_bx, sy - 8, TROPHY_PANEL_REN)

    # Entrance passages through seating tiers (interior access)
    for bx in range(left + 3, left + 10):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)
    for bx in range(left + W - 10, left + W - 3):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)
    # Outer edge entrances — punch through outer walls so player can walk in
    _lm_entrance(world, left,         sy, COBALT_DOOR_CLOSED)
    _lm_entrance(world, left + W - 1, sy, COBALT_DOOR_CLOSED)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Grand Bazaar  (mercantile, base)  — open market square with flanking arcades
# ---------------------------------------------------------------------------

def _place_grand_bazaar(world, spec, biome, right_bx, sy, rng):
    """
    Open-air market: two covered arcade wings flank a wide central courtyard.
    Tall gate towers with arched portals mark each entrance. The courtyard
    itself is fully open overhead — no roof — giving it an airy market feel.
    """
    W = 42
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    if biome == "mediterranean":
        wall, floor, arch = POLISHED_MARBLE, ROMAN_MOSAIC, ROMAN_ARCH_REN
        col, cap, light   = GARDEN_COLUMN, DORIC_CAPITAL, BRAZIER
        door = BRONZE_DOOR_CLOSED
    elif biome == "east_asian":
        wall, floor, arch = PINE_PLANK_WALL, TATAMI_PAVING, PAGODA_EAVE
        col, cap, light   = PINE_PLANK_WALL, PAGODA_EAVE, STONE_LANTERN
        door = SHOJI_DOOR_CLOSED
    else:
        wall, floor, arch = LIMESTONE_BLOCK, COMPASS_PAVING, ROMANESQUE_ARCH
        col, cap, light   = GARDEN_COLUMN, DORIC_CAPITAL, BRAZIER
        door = STUDDED_OAK_DOOR_CLOSED

    # Foundation — full width
    _lm_fill(world, left, left + W - 1, sy, sy, wall)

    # ── Gate towers ── 4 wide, 14 tall, one on each end
    for side in (left, left + W - 4):
        _lm_fill(world, side, side + 3, sy - 14, sy, wall)
        _lm_fill_bg(world, side, side + 3, sy - 14, sy, wall)
        _lm_bg(world, side + 1, sy - 9, arch)
        _lm_bg(world, side + 2, sy - 9, arch)
        _lm_bg(world, side + 1, sy - 4, arch)
        _lm_bg(world, side + 2, sy - 4, arch)
        _lm_set(world, side + 1, sy - 15, light)
        _lm_set(world, side + 2, sy - 15, light)
        # Gate passage — clear inner columns for interior headroom
        for by in range(sy - 4, sy):
            _lm_set(world, side + 1, by, AIR)
            _lm_set(world, side + 2, by, AIR)

    # ── Left arcade wing ── covered, 9 wide, 9 tall; acts as the merchant hall
    ax = left + 4
    aw = 9
    _lm_fill(world, ax, ax + aw - 1, sy - 9, sy - 9, wall)
    _lm_fill(world, ax + aw - 1, ax + aw - 1, sy - 9, sy, wall)  # back wall
    _lm_fill_bg(world, ax, ax + aw - 2, sy - 9, sy - 1, wall)
    _lm_fill(world, ax, ax + aw - 1, sy - 1, sy - 1, floor)
    # Merchant stall arches on the open face
    for bx in range(ax, ax + aw - 1, 3):
        _lm_bg(world, bx, sy - 6, arch)
    # Market goods displays (BG)
    for bx in range(ax + 1, ax + aw - 2, 2):
        _lm_bg(world, bx, sy - 2, MARBLE_PLINTH)
    _lm_set(world, ax + aw - 2, sy - 10, light)

    # ── Right arcade wing ── mirror of left
    bx_r = left + W - 4 - aw
    _lm_fill(world, bx_r, bx_r + aw - 1, sy - 9, sy - 9, wall)
    _lm_fill(world, bx_r, bx_r, sy - 9, sy, wall)  # back wall
    _lm_fill_bg(world, bx_r + 1, bx_r + aw - 1, sy - 9, sy - 1, wall)
    _lm_fill(world, bx_r, bx_r + aw - 1, sy - 1, sy - 1, floor)
    for bx in range(bx_r + 1, bx_r + aw, 3):
        _lm_bg(world, bx, sy - 6, arch)
    for bx in range(bx_r + 1, bx_r + aw - 1, 2):
        _lm_bg(world, bx, sy - 2, MARBLE_PLINTH)
    _lm_set(world, bx_r + 1, sy - 10, light)

    # ── Open central courtyard ── no roof, open sky, paved floor
    cx_l = ax + aw
    cx_r = bx_r - 1
    _lm_fill(world, cx_l, cx_r, sy - 1, sy - 1, floor)
    # Low perimeter parapet on the courtyard edge (2 tall so player can see in)
    for bx in (cx_l - 1, cx_r + 1):
        _lm_fill(world, bx, bx, sy - 5, sy, wall)
        _lm_fill_bg(world, bx, bx, sy - 5, sy, wall)
        _lm_bg(world, bx, sy - 6, arch)
    # Colonnade lining the courtyard (BG pillars every 3)
    for bx in range(cx_l, cx_r + 1, 3):
        _lm_bg(world, bx, sy - 2, col)
        _lm_bg(world, bx, sy - 3, col)
        _lm_bg(world, bx, sy - 4, cap)

    # Central market fountain / rostrum — the landmark focal point
    _lm_bg(world, flag_bx,     sy - 2, SHELL_FOUNTAIN)
    _lm_bg(world, flag_bx - 1, sy - 2, MARBLE_PLINTH)
    _lm_bg(world, flag_bx + 1, sy - 2, MARBLE_PLINTH)
    _lm_bg(world, flag_bx - 2, sy - 3, MARBLE_PLINTH)
    _lm_bg(world, flag_bx + 2, sy - 3, MARBLE_PLINTH)

    # Outer edge entrances — punch through gate tower outer faces
    _lm_entrance(world, left,         sy, door)
    _lm_entrance(world, left + W - 1, sy, door)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Harbor Exchange  (mercantile, coastal)  — quay hall with dock and warehouse
# ---------------------------------------------------------------------------

def _place_harbor_exchange(world, spec, biome, right_bx, sy, rng):
    W = 36
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    # Quay approach — 6 blocks of open dock paving with bollards and barrels
    _lm_fill(world, left, left + 5, sy, sy, LIMESTONE_BLOCK)
    _lm_fill(world, left, left + 5, sy - 1, sy - 1, COMPASS_PAVING)
    _lm_set(world, left + 1, sy - 2, RAIN_BARREL)
    _lm_set(world, left + 3, sy - 2, RAIN_BARREL)
    _lm_set(world, left + 5, sy - 2, RAIN_BARREL)
    # Ship mast / dock pole — tall single pole visible from afar
    for by in range(sy - 10, sy - 1):
        _lm_set(world, left + 2, by, LIMESTONE_BLOCK)
    _lm_set(world, left + 1, sy - 9, HERALDIC_PANEL)
    _lm_set(world, left + 3, sy - 9, HERALDIC_PANEL)

    # Main exchange hall — 24 wide, 10 tall, arched windows
    hx = left + 6
    _lm_fill(world, hx, hx + 23, sy, sy, POLISHED_MARBLE)
    _lm_fill(world, hx, hx + 23, sy - 10, sy - 10, POLISHED_MARBLE)
    for bx in (hx, hx + 23):
        _lm_fill(world, bx, bx, sy - 10, sy, POLISHED_MARBLE)
    _lm_fill_bg(world, hx + 1, hx + 22, sy - 10, sy - 1, POLISHED_MARBLE)
    _lm_fill(world, hx + 1, hx + 22, sy - 1, sy - 1, COMPASS_PAVING)
    # Arched hall windows
    for bx in range(hx + 3, hx + 22, 5):
        _lm_bg(world, bx, sy - 7, ROMAN_ARCH_REN)
        _lm_bg(world, bx, sy - 3, ROMAN_ARCH_REN)
    # Columns
    _lm_cols(world, hx + 1, hx + 22, sy - 2, 7, GARDEN_COLUMN, DORIC_CAPITAL, spacing=5)
    # Hall lights atop corner buttresses
    _lm_set(world, hx,      sy - 11, BRAZIER)
    _lm_set(world, hx + 23, sy - 11, BRAZIER)

    # Warehouse wing — 5 wide, shelves visible through open face
    wx = left + W - 5
    _lm_fill(world, wx, wx + 4, sy, sy, LIMESTONE_BLOCK)
    _lm_fill_bg(world, wx, wx + 4, sy - 8, sy, LIMESTONE_BLOCK)
    for by in (sy - 2, sy - 4, sy - 6):
        for bx in range(wx, wx + 4):
            _lm_bg(world, bx, by, RAIN_BARREL)

    # Outer edge entrance from left (quay side) and hall walls on each side
    _lm_entrance(world, left,     sy, STUDDED_OAK_DOOR_CLOSED)
    _lm_entrance(world, hx,       sy, STUDDED_OAK_DOOR_CLOSED)
    _lm_entrance(world, hx + 23,  sy, STUDDED_OAK_DOOR_CLOSED)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Caravanserai  (mercantile, silk_road)  — courtyard inn with well and arcades
# ---------------------------------------------------------------------------

def _place_caravanserai(world, spec, biome, right_bx, sy, rng):
    W = 36
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    wall = SANDSTONE_ASHLAR

    # Outer enclosure — 2-thick walls, 10 tall, castellated (alternating merlons)
    _lm_fill(world, left, left + W - 1, sy, sy, wall)
    for bx in range(left, left + W):
        _lm_fill(world, bx, bx, sy - 10, sy, wall)
        _lm_fill_bg(world, bx, bx, sy - 10, sy, wall)
    # Merlons on the parapet (every other block rises 2 more)
    for bx in range(left, left + W, 2):
        _lm_fill(world, bx, bx, sy - 12, sy - 11, wall)
    # But hollow out the interior — clear everything 2 blocks in from walls
    for by in range(sy - 9, sy):
        for bx in range(left + 2, left + W - 2):
            _lm_set(world, bx, by, AIR)
    # Keep the outer wall faces solid (re-establish them)
    for by in range(sy - 10, sy + 1):
        for bx in (left, left + 1, left + W - 2, left + W - 1):
            _lm_set(world, bx, by, wall)

    # Interior courtyard floor
    _lm_fill(world, left + 2, left + W - 3, sy - 1, sy - 1, SANDSTONE_BLOCK)

    # Grand Mughal gate — right side, facing town (clear + arch)
    for by in range(sy - 6, sy):
        for bx in (left + W - 2, left + W - 1):
            _lm_set(world, bx, by, AIR)
    _lm_bg(world, left + W - 2, sy - 7, MUGHAL_ARCH)
    _lm_bg(world, left + W - 1, sy - 7, MUGHAL_ARCH)
    _lm_door(world, left + W - 2, sy, COBALT_DOOR_CLOSED)
    _lm_door(world, left + W - 1, sy, COBALT_DOOR_CLOSED)

    # Secondary gate — left side
    for by in range(sy - 5, sy):
        for bx in (left, left + 1):
            _lm_set(world, bx, by, AIR)
    _lm_door(world, left,     sy, COBALT_DOOR_CLOSED)
    _lm_door(world, left + 1, sy, COBALT_DOOR_CLOSED)

    # Interior arcade — 3 arches per side along the inner wall (BG)
    for bx in range(left + 3, left + W // 2 - 1, 4):
        _lm_bg(world, bx, sy - 5, MUGHAL_ARCH)
    for bx in range(left + W // 2 + 1, left + W - 3, 4):
        _lm_bg(world, bx, sy - 5, MUGHAL_ARCH)

    # Central well — two columns and a barrel suggesting water
    _lm_bg(world, flag_bx - 1, sy - 2, SANDSTONE_COLUMN)
    _lm_bg(world, flag_bx + 1, sy - 2, SANDSTONE_COLUMN)
    _lm_bg(world, flag_bx,     sy - 3, RAIN_BARREL)
    # Lantern posts flanking the courtyard
    _lm_bg(world, left + 4,     sy - 2, STONE_LANTERN)
    _lm_bg(world, left + W - 5, sy - 2, STONE_LANTERN)
    # Camel-load items stored around the yard
    for bx in (left + 6, left + 8, left + W - 7, left + W - 9):
        _lm_bg(world, bx, sy - 2, RAIN_BARREL)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Archive  (scholarly, base)  — stepped reading hall with flanking galleries
# ---------------------------------------------------------------------------

def _place_archive(world, spec, biome, right_bx, sy, rng):
    W = 38
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    if biome == "mediterranean":
        wall, floor, arch = POLISHED_MARBLE, ROMAN_MOSAIC, ROMAN_ARCH_REN
        col, cap, light   = GARDEN_COLUMN, DORIC_CAPITAL, BRAZIER
        door = BRONZE_DOOR_CLOSED
    elif biome == "east_asian":
        wall, floor, arch = PINE_PLANK_WALL, TATAMI_PAVING, PAGODA_EAVE
        col, cap, light   = PINE_PLANK_WALL, PAGODA_EAVE, STONE_LANTERN
        door = SHOJI_DOOR_CLOSED
    else:
        wall, floor, arch = LIMESTONE_BLOCK, COMPASS_PAVING, ROMANESQUE_ARCH
        col, cap, light   = GARDEN_COLUMN, DORIC_CAPITAL, TORCH
        door = STUDDED_OAK_DOOR_CLOSED

    # Foundation
    _lm_fill(world, left, left + W - 1, sy, sy, wall)

    # Flanking gallery wings — 7 wide, 8 tall each
    for wing_x in (left, left + W - 7):
        _lm_fill(world, wing_x, wing_x + 6, sy - 8, sy - 8, wall)
        for bx in (wing_x, wing_x + 6):
            _lm_fill(world, bx, bx, sy - 8, sy, wall)
        _lm_fill_bg(world, wing_x + 1, wing_x + 5, sy - 8, sy - 1, wall)
        _lm_fill(world, wing_x + 1, wing_x + 5, sy - 1, sy - 1, floor)
        _lm_bg(world, wing_x + 3, sy - 5, arch)
        # Three rows of scroll shelves on the back wall
        for bx in range(wing_x + 1, wing_x + 6, 2):
            _lm_bg(world, bx, sy - 3, PHILOSOPHERS_SCROLL)
            _lm_bg(world, bx, sy - 5, PHILOSOPHERS_SCROLL)
            _lm_bg(world, bx, sy - 7, PHILOSOPHERS_SCROLL)
        _lm_set(world, wing_x + 3, sy - 9, light)

    # Central reading hall — 24 wide, 13 tall (tall enough to feel grand)
    cx = left + 7
    _lm_fill(world, cx, cx + 23, sy - 13, sy - 13, wall)
    _lm_fill(world, cx, cx + 23, sy - 14, sy - 14, wall)  # cornice
    for bx in (cx, cx + 23):
        _lm_fill(world, bx, bx, sy - 13, sy, wall)
    _lm_fill_bg(world, cx + 1, cx + 22, sy - 13, sy - 1, wall)
    _lm_fill(world, cx + 1, cx + 22, sy - 1, sy - 1, floor)
    _lm_set(world, cx,      sy - 15, light)
    _lm_set(world, cx + 23, sy - 15, light)

    # Hall arches at two heights
    for bx in range(cx + 3, cx + 21, 5):
        _lm_bg(world, bx, sy - 9,  arch)
        _lm_bg(world, bx, sy - 5,  arch)
    # Columns
    _lm_cols(world, cx + 1, cx + 22, sy - 2, 9, col, cap, spacing=5)

    # Three rows of scroll panels on hall back wall
    for bx in range(cx + 2, cx + 22, 3):
        _lm_bg(world, bx, sy - 3, PHILOSOPHERS_SCROLL)
        _lm_bg(world, bx, sy - 6, PHILOSOPHERS_SCROLL)
        _lm_bg(world, bx, sy - 9, PHILOSOPHERS_SCROLL)

    # Reading table / lectern (BG)
    _lm_bg(world, flag_bx, sy - 3, HERMES_STELE)
    for bx in (flag_bx - 3, flag_bx - 2, flag_bx + 2, flag_bx + 3):
        _lm_bg(world, bx, sy - 2, CARVED_BENCH)

    # Wing / hall entrance passages
    for bx in (left, left + W - 1, left + 7, left + W - 8):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)
        _lm_door(world, bx, sy, door)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Imperial Library  (scholarly, east_asian)  — two-storey pagoda library
# ---------------------------------------------------------------------------

def _place_imperial_library(world, spec, biome, right_bx, sy, rng):
    W = 36
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    # Lower hall (full width, 7 tall)
    _lm_fill(world, left, left + W - 1, sy, sy, PINE_PLANK_WALL)
    _lm_fill(world, left, left + W - 1, sy - 7, sy - 7, PINE_PLANK_WALL)
    for bx in (left, left + W - 1):
        _lm_fill(world, bx, bx, sy - 7, sy, PINE_PLANK_WALL)
    _lm_fill_bg(world, left + 1, left + W - 2, sy - 7, sy - 1, LACQUER_PANEL)
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, TATAMI_PAVING)

    # Lower hall columns, scroll shelves, and lanterns
    for bx in range(left + 4, left + W - 4, 4):
        _lm_bg(world, bx, sy - 2, GARDEN_COLUMN)
        _lm_bg(world, bx, sy - 3, GARDEN_COLUMN)
        _lm_bg(world, bx, sy - 4, LOTUS_CAPITAL)
        # Three rows of scrolls in bays between columns
        _lm_bg(world, bx + 1, sy - 3, PHILOSOPHERS_SCROLL)
        _lm_bg(world, bx + 1, sy - 5, PHILOSOPHERS_SCROLL)
        _lm_bg(world, bx - 1, sy - 3, PHILOSOPHERS_SCROLL)
        _lm_bg(world, bx - 1, sy - 5, PHILOSOPHERS_SCROLL)

    # Pagoda eave on lower roof, extending 1 each side
    _lm_fill(world, left - 1, left + W, sy - 8, sy - 8, PAGODA_EAVE)
    # Corner lanterns on lower eave
    _lm_set(world, left - 1, sy - 9, STONE_LANTERN)
    _lm_set(world, left + W, sy - 9, STONE_LANTERN)

    # Upper storey (narrower — 6 in from each side, 6 tall)
    up_l, up_r = left + 6, left + W - 7
    _lm_fill(world, up_l, up_r, sy - 13, sy - 13, PINE_PLANK_WALL)
    for bx in (up_l, up_r):
        _lm_fill(world, bx, bx, sy - 13, sy - 8, PINE_PLANK_WALL)
    _lm_fill_bg(world, up_l + 1, up_r - 1, sy - 13, sy - 9, LACQUER_PANEL)
    _lm_fill(world, up_l + 1, up_r - 1, sy - 9, sy - 9, TATAMI_PAVING)
    # Upper hall scrolls
    for bx in range(up_l + 2, up_r - 1, 3):
        _lm_bg(world, bx, sy - 11, PHILOSOPHERS_SCROLL)
    # Upper pagoda eave
    _lm_fill(world, up_l - 1, up_r + 1, sy - 14, sy - 14, PAGODA_EAVE)
    # Pinnacle lanterns
    _lm_set(world, up_l - 1, sy - 15, STONE_LANTERN)
    _lm_set(world, up_r + 1, sy - 15, STONE_LANTERN)

    # Torii gate approach — double torii flanking the entrance
    for bx in (left + 2, left + W - 3):
        _lm_bg(world, bx, sy - 2, TORII_PANEL)
        _lm_bg(world, bx, sy - 3, TORII_PANEL)
        _lm_bg(world, bx, sy - 4, TORII_PANEL)
    _lm_bg(world, left + 1, sy - 2, STONE_LANTERN)
    _lm_bg(world, left + W - 2, sy - 2, STONE_LANTERN)

    # Central reading area with bench and scroll rack
    for bx in range(flag_bx - 3, flag_bx + 4, 2):
        _lm_bg(world, bx, sy - 5, PHILOSOPHERS_SCROLL)
    _lm_bg(world, flag_bx, sy - 2, CARVED_BENCH)
    _lm_bg(world, flag_bx - 2, sy - 2, CARVED_BENCH)
    _lm_bg(world, flag_bx + 2, sy - 2, CARVED_BENCH)

    # Entrance
    for by in range(sy - 3, sy):
        _lm_set(world, left,      by, AIR)
        _lm_set(world, left + W - 1, by, AIR)
    _lm_door(world, left,         sy, SHOJI_DOOR_CLOSED)
    _lm_door(world, left + W - 1, sy, SHOJI_DOOR_CLOSED)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Observatory  (scholarly, mediterranean)  — domed tower with flanking wings
# ---------------------------------------------------------------------------

def _place_observatory(world, spec, biome, right_bx, sy, rng):
    W = 32
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    # Flanking wings — 7 wide, 7 tall each
    for wx in (left, left + W - 7):
        _lm_fill(world, wx, wx + 6, sy, sy, POLISHED_MARBLE)
        _lm_fill(world, wx, wx + 6, sy - 7, sy - 7, POLISHED_MARBLE)
        for bx in (wx, wx + 6):
            _lm_fill(world, bx, bx, sy - 7, sy, POLISHED_MARBLE)
        _lm_fill_bg(world, wx + 1, wx + 5, sy - 7, sy - 1, POLISHED_MARBLE)
        _lm_fill(world, wx + 1, wx + 5, sy - 1, sy - 1, COMPASS_PAVING)
        _lm_bg(world, wx + 3, sy - 4, ROMAN_ARCH_REN)
        # Wing contents — sundial and scroll in one, instrument in other
        _lm_set(world, wx + 2, sy - 2, TALL_SUNDIAL)
        _lm_bg(world, wx + 4, sy - 3, PHILOSOPHERS_SCROLL)
        _lm_bg(world, wx + 4, sy - 5, PHILOSOPHERS_SCROLL)
        _lm_set(world, wx + 3, sy - 8, BRAZIER)

    # Central domed tower — 10 wide, 14 tall
    tx = left + 11
    _lm_fill(world, tx, tx + 9, sy, sy, POLISHED_MARBLE)
    for bx in (tx, tx + 9):
        _lm_fill(world, bx, bx, sy - 14, sy, POLISHED_MARBLE)
    _lm_fill_bg(world, tx + 1, tx + 8, sy - 14, sy - 1, POLISHED_MARBLE)
    _lm_fill(world, tx + 1, tx + 8, sy - 1, sy - 1, ROMAN_MOSAIC)

    # Dome — 4 rows narrowing inward to a point
    for row in range(4):
        by = sy - 15 - row
        _lm_fill(world, tx + 1 + row, tx + 8 - row, by, by, POLISHED_MARBLE)
    # Pinnacle brazier at dome tip
    _lm_set(world, tx + 4, sy - 20, BRAZIER)
    _lm_set(world, tx + 5, sy - 20, BRAZIER)

    # Observation ring arches at two heights
    for bx in (tx + 2, tx + 4, tx + 6):
        _lm_bg(world, bx, sy - 10, ROMAN_ARCH_REN)
        _lm_bg(world, bx, sy - 5,  ROMAN_ARCH_REN)

    # Columns inside tower
    _lm_cols(world, tx + 1, tx + 8, sy - 2, 9, GARDEN_COLUMN, DORIC_CAPITAL, spacing=3)

    # Open roof platform — top 2 rows cleared for stargazing
    for by in range(sy - 14, sy - 12):
        for bx in range(tx + 1, tx + 9):
            _lm_set(world, bx, by, AIR)

    # Outer edge entrances through wing walls, then inner doors into the tower
    _lm_entrance(world, left,         sy, BRONZE_DOOR_CLOSED)
    _lm_entrance(world, left + W - 1, sy, BRONZE_DOOR_CLOSED)
    for bx in (tx, tx + 9):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)
        _lm_door(world, bx, sy, BRONZE_DOOR_CLOSED)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Great Shrine  (pious, base)  — grand temple with deep portico and sanctum
# ---------------------------------------------------------------------------

def _place_great_shrine(world, spec, biome, right_bx, sy, rng):
    W = 36
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    if biome == "mediterranean":
        wall, floor, arch = POLISHED_MARBLE, ROMAN_MOSAIC, ROMAN_ARCH_REN
        col, cap, light   = GARDEN_COLUMN, DORIC_CAPITAL, BRAZIER
        panel             = MARBLE_STATUE
        door = BRONZE_DOOR_CLOSED
    elif biome == "east_asian":
        wall, floor, arch = PINE_PLANK_WALL, TATAMI_PAVING, PAGODA_EAVE
        col, cap, light   = PINE_PLANK_WALL, PAGODA_EAVE, STONE_LANTERN
        panel             = VOTIVE_TABLET
        door = SHOJI_DOOR_CLOSED
    elif biome in ("desert", "silk_road"):
        wall, floor, arch = SANDSTONE_ASHLAR, SANDSTONE_BLOCK, MUGHAL_ARCH
        col, cap, light   = SANDSTONE_COLUMN, MUGHAL_ARCH, TRIPOD_BRAZIER
        panel             = VOTIVE_TABLET
        door = COBALT_DOOR_CLOSED
    else:
        wall, floor, arch = LIMESTONE_BLOCK, COBBLESTONE, ROMANESQUE_ARCH
        col, cap, light   = GARDEN_COLUMN, DORIC_CAPITAL, TORCH
        panel             = VOTIVE_TABLET
        door = STUDDED_OAK_DOOR_CLOSED

    # Foundation
    _lm_fill(world, left, left + W - 1, sy, sy, wall)

    # Outer portico — full width, 7 tall, open front colonnade
    _lm_fill(world, left, left + W - 1, sy - 7, sy - 7, wall)
    _lm_fill(world, left, left + W - 1, sy - 8, sy - 8, wall)  # pediment
    for bx in (left, left + W - 1):
        _lm_fill(world, bx, bx, sy - 8, sy, wall)
    _lm_fill_bg(world, left + 1, left + W - 2, sy - 7, sy - 1, wall)
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, floor)

    # Portico columns — across the full front face
    for bx in range(left + 2, left + W - 2, 4):
        _lm_bg(world, bx, sy - 6, col)
        _lm_bg(world, bx, sy - 5, col)
        _lm_bg(world, bx, sy - 4, col)
        _lm_bg(world, bx, sy - 3, col)
        _lm_set(world, bx, sy - 7, cap)

    # Votive tablets and statues on the portico BG wall
    for bx in range(left + 3, left + W - 3, 6):
        _lm_bg(world, bx, sy - 5, panel)

    # Inner sanctum — 18 wide, 12 tall, stepped up 1 from portico
    sx = left + 9
    _lm_fill(world, sx, sx + 17, sy - 12, sy - 12, wall)
    _lm_fill(world, sx, sx + 17, sy - 13, sy - 13, wall)
    _lm_fill(world, sx, sx + 17, sy - 14, sy - 14, wall)  # tall sanctum pediment
    for bx in (sx, sx + 17):
        _lm_fill(world, bx, bx, sy - 14, sy, wall)
    _lm_fill_bg(world, sx + 1, sx + 16, sy - 12, sy - 1, wall)
    _lm_fill(world, sx + 1, sx + 16, sy - 1, sy - 1, floor)
    _lm_set(world, sx + 8,  sy - 15, light)
    _lm_set(world, sx + 9,  sy - 15, light)

    # Sanctum arches at two heights and altar panels
    for bx in (sx + 4, sx + 13):
        _lm_bg(world, bx, sy - 9, arch)
        _lm_bg(world, bx, sy - 5, arch)
    # Altar panels rising up the back wall
    for by in range(sy - 4, sy - 10, -2):
        _lm_bg(world, flag_bx - 1, by, panel)
        _lm_bg(world, flag_bx + 1, by, panel)
    _lm_bg(world, flag_bx, sy - 5, panel)

    # Prayer flag altar (BG — player can reach the flag)
    _lm_bg(world, flag_bx, sy - 3, PRAYER_FLAG_BLOCK)
    _lm_bg(world, flag_bx - 2, sy - 2, MARBLE_PLINTH)
    _lm_bg(world, flag_bx + 2, sy - 2, MARBLE_PLINTH)
    _lm_set(world, sx + 2, sy - 2, light)
    _lm_set(world, sx + 15, sy - 2, light)

    # Entrances — outer portico both sides, inner sanctum both sides
    for by in range(sy - 5, sy):
        _lm_set(world, left, by, AIR)
        _lm_set(world, left + W - 1, by, AIR)
    _lm_door(world, left,         sy, door)
    _lm_door(world, left + W - 1, sy, door)
    for by in range(sy - 3, sy):
        _lm_set(world, sx, by, AIR)
        _lm_set(world, sx + 17, by, AIR)
    _lm_door(world, sx,      sy, door)
    _lm_door(world, sx + 17, sy, door)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Sea Temple  (pious, coastal)  — wave-facing open temple on raised quay
# ---------------------------------------------------------------------------

def _place_sea_temple(world, spec, biome, right_bx, sy, rng):
    W = 34
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    # Wave-prow forecourt — 7 blocks, open to the sea (left side)
    # Stepped down 1 block to suggest a waterfront platform
    _lm_fill(world, left, left + 6, sy, sy, LIMESTONE_BLOCK)
    _lm_fill(world, left, left + 6, sy + 1, sy + 1, LIMESTONE_BLOCK)  # raised border
    _lm_fill(world, left, left + 6, sy - 1, sy - 1, COMPASS_PAVING)
    # Sea-wall pillars
    for bx in (left, left + 3, left + 6):
        _lm_fill(world, bx, bx, sy - 4, sy, LIMESTONE_BLOCK)
    _lm_bg(world, left + 1, sy - 3, SHELL_FOUNTAIN)
    _lm_bg(world, left + 4, sy - 3, SHELL_FOUNTAIN)
    # Offering plinths
    _lm_set(world, left + 2, sy - 2, MARBLE_PLINTH)
    _lm_set(world, left + 5, sy - 2, MARBLE_PLINTH)

    # Open colonnaded temple hall — 20 wide, 11 tall, open sea face (left)
    hx = left + 7
    _lm_fill(world, hx, hx + 19, sy, sy, LIMESTONE_BLOCK)
    _lm_fill(world, hx, hx + 19, sy - 11, sy - 11, LIMESTONE_BLOCK)
    # Back wall only
    _lm_fill(world, hx + 19, hx + 19, sy - 11, sy, LIMESTONE_BLOCK)
    _lm_fill_bg(world, hx, hx + 18, sy - 11, sy - 1, LIMESTONE_BLOCK)
    _lm_fill(world, hx, hx + 18, sy - 1, sy - 1, COMPASS_PAVING)
    # Braziers atop hall roof
    _lm_set(world, hx,      sy - 12, BRAZIER)
    _lm_set(world, hx + 19, sy - 12, BRAZIER)

    # Colonnaded front (sea-facing): arches and columns
    for bx in range(hx, hx + 19, 4):
        _lm_bg(world, bx, sy - 7, ROMAN_ARCH_REN)
        _lm_bg(world, bx, sy - 3, ROMAN_ARCH_REN)
    _lm_cols(world, hx, hx + 18, sy - 2, 8, GARDEN_COLUMN, DORIC_CAPITAL, spacing=4)

    # Inner altar — stepped plinth, statue, prayer tablets
    _lm_fill(world, hx + 14, hx + 17, sy - 1, sy - 1, LIMESTONE_BLOCK)
    _lm_fill(world, hx + 15, hx + 16, sy - 2, sy - 2, LIMESTONE_BLOCK)  # second step
    _lm_bg(world, hx + 15, sy - 3, PRAYER_FLAG_BLOCK)
    _lm_bg(world, hx + 16, sy - 3, PRAYER_FLAG_BLOCK)
    _lm_bg(world, hx + 14, sy - 4, MARBLE_STATUE)
    _lm_bg(world, hx + 17, sy - 4, MARBLE_STATUE)
    for bx in (hx + 13, hx + 18):
        _lm_bg(world, bx, sy - 3, VOTIVE_TABLET)
        _lm_bg(world, bx, sy - 5, VOTIVE_TABLET)

    # Votive alcove wing (right side — 7 wide)
    wx = left + W - 7
    _lm_fill(world, wx, wx + 6, sy, sy, LIMESTONE_BLOCK)
    _lm_fill_bg(world, wx, wx + 5, sy - 7, sy, LIMESTONE_BLOCK)
    for bx in range(wx + 1, wx + 5, 2):
        _lm_bg(world, bx, sy - 2, VOTIVE_TABLET)
        _lm_bg(world, bx, sy - 4, VOTIVE_TABLET)

    # Left outer entrance punches through quay pillar; right inner door into hall
    _lm_entrance(world, left,     sy, STONE_SLAB_DOOR_CLOSED)
    _lm_entrance(world, hx + 19,  sy, STONE_SLAB_DOOR_CLOSED)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Canopy Sanctum  (pious, jungle)  — living-wall open jungle sanctuary
# ---------------------------------------------------------------------------

def _place_canopy_sanctum(world, spec, biome, right_bx, sy, rng):
    W = 32
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    # Stone base
    _lm_fill(world, left, left + W - 1, sy, sy, LIMESTONE_BLOCK)

    # Living outer walls — limestone pillars every 3 blocks with glow vine between
    for bx in range(left, left + W, 3):
        _lm_fill(world, bx, bx, sy - 11, sy, LIMESTONE_BLOCK)
    for bx in range(left, left + W):
        for by in range(sy - 12, sy - 1):
            _lm_bg(world, bx, by, GLOW_VINE)

    # Stone arch canopy roof — stepped up slightly in center for visual interest
    _lm_fill(world, left - 1, left + W, sy - 12, sy - 12, LIMESTONE_BLOCK)
    _lm_fill(world, left, left + W - 1, sy - 11, sy - 11, LIMESTONE_BLOCK)
    # Center of roof rises 2 more (ridge)
    mid = left + W // 2
    _lm_fill(world, mid - 3, mid + 3, sy - 13, sy - 13, LIMESTONE_BLOCK)
    _lm_fill(world, mid - 1, mid + 1, sy - 14, sy - 14, LIMESTONE_BLOCK)

    # Interior floor
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, COBBLESTONE)

    # Bamboo clusters flanking the entrance columns
    for bx in (left + 1, left + 2, left + W - 2, left + W - 3):
        _lm_bg(world, bx, sy - 2, BAMBOO_CLUMP)
        _lm_bg(world, bx, sy - 3, BAMBOO_CLUMP)

    # Paper lanterns strung at two heights
    for bx in range(left + 3, left + W - 3, 3):
        _lm_set(world, bx, sy - 8, PAPER_LANTERN)
        _lm_set(world, bx, sy - 5, PAPER_LANTERN)

    # Lotus pools flanking the altar approach
    _lm_set(world, flag_bx - 3, sy - 2, LOTUS_POND)
    _lm_set(world, flag_bx - 2, sy - 2, LOTUS_POND)
    _lm_set(world, flag_bx + 2, sy - 2, LOTUS_POND)
    _lm_set(world, flag_bx + 3, sy - 2, LOTUS_POND)

    # Raised altar platform and prayer flag
    _lm_fill(world, flag_bx - 1, flag_bx + 1, sy - 1, sy - 1, LIMESTONE_BLOCK)
    _lm_bg(world, flag_bx, sy - 2, PRAYER_FLAG_BLOCK)
    _lm_bg(world, flag_bx - 1, sy - 4, LOTUS_BLOCK)
    _lm_bg(world, flag_bx + 1, sy - 4, LOTUS_BLOCK)
    _lm_bg(world, flag_bx, sy - 6, LOTUS_BLOCK)

    # Left entrance punches through the edge pillar; right edge (col W-1) is already open
    _lm_entrance(world, left, sy, SANDALWOOD_DOOR_CLOSED)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Stoneworks  (builder, base)  — forge complex with chimneys and workshop yard
# ---------------------------------------------------------------------------

def _place_stoneworks(world, spec, biome, right_bx, sy, rng):
    W = 36
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    if biome == "alpine":
        wall, floor = ROUGH_STONE_WALL, LIMESTONE_BLOCK
        arch, light = ROMANESQUE_ARCH, TRIPOD_BRAZIER
    else:
        wall, floor = COBBLESTONE, COBBLESTONE
        arch, light = POINTED_ARCH, TRIPOD_BRAZIER

    # Foundation
    _lm_fill(world, left, left + W - 1, sy, sy, wall)

    # Main workshop shell — full width, 9 tall
    _lm_fill(world, left, left + W - 1, sy - 9, sy - 9, wall)
    for bx in (left, left + W - 1):
        _lm_fill(world, bx, bx, sy - 9, sy, wall)
    _lm_fill_bg(world, left + 1, left + W - 2, sy - 9, sy - 1, wall)
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, floor)

    # Two chimney stacks — 2 wide each, rising 7 blocks above the roof
    for cx in (left + 5, left + W - 7):
        _lm_fill(world, cx, cx + 1, sy - 16, sy - 9, wall)
        _lm_fill_bg(world, cx, cx + 1, sy - 16, sy - 9, wall)
        # Smoke-cap overhang (1 wider each side)
        _lm_fill(world, cx - 1, cx + 2, sy - 17, sy - 17, wall)
        # Active brazier at chimney top
        _lm_set(world, cx,     sy - 18, BRAZIER)
        _lm_set(world, cx + 1, sy - 18, BRAZIER)

    # Interior dividing wall — two forge bays
    mid = left + W // 2
    _lm_fill(world, mid, mid, sy - 9, sy - 4, wall)
    for by in range(sy - 3, sy):
        _lm_set(world, mid, by, AIR)

    # Left forge bay — forges, anvil/weapon rack, tripod brazier
    _lm_bg(world, left + 3,  sy - 2, FORGE_BLOCK)
    _lm_bg(world, left + 4,  sy - 2, FORGE_BLOCK)
    _lm_bg(world, left + 3,  sy - 3, light)
    _lm_bg(world, left + 8,  sy - 2, WEAPON_RACK_BLOCK)
    _lm_bg(world, left + 10, sy - 2, WEAPON_RACK_BLOCK)
    # Barrel storage
    for bx in (left + 12, left + 13):
        _lm_bg(world, bx, sy - 2, RAIN_BARREL)
        _lm_bg(world, bx, sy - 3, RAIN_BARREL)
    # Arched bay window
    _lm_bg(world, left + 6, sy - 6, arch)

    # Right forge bay — mirror
    _lm_bg(world, left + W - 4, sy - 2, FORGE_BLOCK)
    _lm_bg(world, left + W - 5, sy - 2, FORGE_BLOCK)
    _lm_bg(world, left + W - 4, sy - 3, light)
    _lm_bg(world, left + W - 9,  sy - 2, WEAPON_RACK_BLOCK)
    _lm_bg(world, left + W - 11, sy - 2, WEAPON_RACK_BLOCK)
    for bx in (left + W - 13, left + W - 14):
        _lm_bg(world, bx, sy - 2, RAIN_BARREL)
        _lm_bg(world, bx, sy - 3, RAIN_BARREL)
    _lm_bg(world, left + W - 7, sy - 6, arch)

    # Entrances both sides
    for by in range(sy - 3, sy):
        _lm_set(world, left, by, AIR)
        _lm_set(world, left + W - 1, by, AIR)
    _lm_door(world, left,         sy, STUDDED_OAK_DOOR_CLOSED)
    _lm_door(world, left + W - 1, sy, STUDDED_OAK_DOOR_CLOSED)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Stonecutters Guild  (builder, alpine)  — guild hall with quarry face tower
# ---------------------------------------------------------------------------

def _place_stonecutters_guild(world, spec, biome, right_bx, sy, rng):
    W = 32
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    # Quarry-face approach — uneven rough stone base, boulders in front
    _lm_fill(world, left, left + W - 1, sy, sy, ROUGH_STONE_WALL)
    for bx in range(left, left + W, 4):
        _lm_set(world, bx, sy + 1, ROUGH_STONE_WALL)
    # Scattered quarry stones in foreground approach
    for bx in (left + 2, left + W - 3):
        _lm_set(world, bx, sy - 1, ROUGH_STONE_WALL)

    # Guild hall main building — full width, 9 tall
    _lm_fill(world, left, left + W - 1, sy - 9, sy - 9, LIMESTONE_BLOCK)
    _lm_fill(world, left, left + W - 1, sy - 10, sy - 10, LIMESTONE_BLOCK)  # cornice
    for bx in (left, left + W - 1):
        _lm_fill(world, bx, bx, sy - 10, sy, LIMESTONE_BLOCK)
    _lm_fill_bg(world, left + 1, left + W - 2, sy - 10, sy - 1, ROUGH_STONE_WALL)
    _lm_fill(world, left + 1, left + W - 2, sy - 1, sy - 1, LIMESTONE_BLOCK)

    # Quarry crane tower — right side, 4 wide, 14 tall (rises above hall)
    qt = left + W - 6
    _lm_fill(world, qt, qt + 3, sy - 14, sy - 10, ROUGH_STONE_WALL)
    _lm_fill_bg(world, qt, qt + 3, sy - 14, sy - 10, ROUGH_STONE_WALL)
    _lm_fill(world, qt - 1, qt + 4, sy - 14, sy - 14, LIMESTONE_BLOCK)  # cap
    _lm_set(world, qt + 1, sy - 15, TRIPOD_BRAZIER)
    _lm_set(world, qt + 2, sy - 15, TRIPOD_BRAZIER)
    # Winch/rope suggestion — heraldic panel
    _lm_bg(world, qt + 1, sy - 12, HERALDIC_PANEL)
    _lm_bg(world, qt + 2, sy - 12, HERALDIC_PANEL)

    # Romanesque arched portal — central, 5-wide, 6-tall clear entrance with double door
    for bx in range(flag_bx - 2, flag_bx + 3):
        for by in range(sy - 5, sy):
            _lm_set(world, bx, by, AIR)
    _lm_bg(world, flag_bx, sy - 6, ROMANESQUE_ARCH)
    _lm_door(world, flag_bx - 1, sy, STUDDED_OAK_DOOR_CLOSED)
    _lm_door(world, flag_bx,     sy, STUDDED_OAK_DOOR_CLOSED)
    # Flanking arched windows
    _lm_bg(world, flag_bx - 6, sy - 6, ROMANESQUE_ARCH)
    _lm_bg(world, flag_bx + 6, sy - 6, ROMANESQUE_ARCH)

    # Interior — tripod braziers, tool displays (all BG)
    _lm_bg(world, left + 3,  sy - 2, TRIPOD_BRAZIER)
    _lm_bg(world, left + W - 4, sy - 2, TRIPOD_BRAZIER)
    _lm_bg(world, flag_bx - 4, sy - 2, WEAPON_RACK_BLOCK)
    _lm_bg(world, flag_bx + 4, sy - 2, WEAPON_RACK_BLOCK)
    _lm_bg(world, flag_bx - 3, sy - 2, RAIN_BARREL)
    _lm_bg(world, flag_bx + 3, sy - 2, RAIN_BARREL)
    # Stone slabs stacked against the back wall
    for bx in range(left + 2, left + W - 5, 3):
        _lm_bg(world, bx, sy - 4, ROUGH_STONE_WALL)

    # Outer edge entrances on both sides
    _lm_entrance(world, left,         sy, STUDDED_OAK_DOOR_CLOSED)
    _lm_entrance(world, left + W - 1, sy, STUDDED_OAK_DOOR_CLOSED)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Pleasure Garden  (hedonist, base)  — formal garden with gate and pergola
# ---------------------------------------------------------------------------

def _place_pleasure_garden(world, spec, biome, right_bx, sy, rng):
    W = 40
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    if biome == "mediterranean":
        wall, floor = POLISHED_MARBLE, ROMAN_MOSAIC
        arch, light = TRELLIS_ARCH, BRAZIER
        door = BRONZE_DOOR_CLOSED
    elif biome == "east_asian":
        wall, floor = PINE_PLANK_WALL, ZEN_GRAVEL
        arch, light = MOON_GATE, STONE_LANTERN
        door = SHOJI_DOOR_CLOSED
    else:
        wall, floor = LIMESTONE_BLOCK, COMPASS_PAVING
        arch, light = TRELLIS_ARCH, TORCH
        door = STUDDED_OAK_DOOR_CLOSED

    # Garden floor — the whole plot is walkable open garden
    _lm_fill(world, left, left + W - 1, sy, sy, wall)
    _lm_fill(world, left, left + W - 1, sy - 1, sy - 1, floor)

    # Garden gate wall — 3 tall, runs across the entrance with a central gate opening
    # Left gate pillar
    _lm_fill(world, left, left + 2, sy - 5, sy, wall)
    _lm_fill_bg(world, left, left + 2, sy - 5, sy, wall)
    _lm_set(world, left + 1, sy - 6, light)
    # Right gate pillar
    _lm_fill(world, left + W - 3, left + W - 1, sy - 5, sy, wall)
    _lm_fill_bg(world, left + W - 3, left + W - 1, sy - 5, sy, wall)
    _lm_set(world, left + W - 2, sy - 6, light)
    # Gate arch over the central opening
    _lm_bg(world, left + W // 2, sy - 4, arch)
    _lm_bg(world, left + W // 2 + 1, sy - 4, arch)
    # Clear the gate passage interior
    for bx in range(left + 3, left + W - 3):
        for by in range(sy - 3, sy):
            _lm_set(world, bx, by, AIR)
    # Outer edge entrances — punch through gate pillar walls so player can walk in
    _lm_entrance(world, left,         sy, door)
    _lm_entrance(world, left + W - 1, sy, door)

    # Low hedge walls along the garden edges (2 tall) — BG so garden is walkable
    for bx in range(left + 3, left + W - 3):
        _lm_bg(world, bx, sy - 4, OLIVE_BRANCH)
        if bx % 5 == 0:
            _lm_bg(world, bx, sy - 5, OLIVE_BRANCH)  # irregular topiary silhouette

    # Pergola colonnade — BG columns running the length of the garden
    col_xs = list(range(left + 4, left + W - 4, 4))
    for bx in col_xs:
        for by in range(sy - 8, sy - 1):
            _lm_bg(world, bx, by, wall)
        _lm_bg(world, bx, sy - 9, light)
        _lm_bg(world, bx, sy - 8, arch if bx != col_xs[0] else wall)

    # Pergola roof beams (BG)
    _lm_fill_bg(world, left + 4, left + W - 5, sy - 9, sy - 9, wall)

    # Flower beds, topiaries, and koi pool in bays between columns
    topiary_choices = [TOPIARY_PEACOCK, TOPIARY_ARCH, TOPIARY_BEAR, TOPIARY_PEACOCK]
    for i, bx in enumerate(col_xs[:-1]):
        mid_bx = bx + 2
        _lm_bg(world, mid_bx - 1, sy - 2, LAVENDER_BED if i % 2 == 0 else ROSE_BED)
        _lm_set(world, mid_bx,     sy - 2, topiary_choices[i % len(topiary_choices)])
        _lm_bg(world, mid_bx + 1, sy - 2, ROSE_BED if i % 2 == 0 else LAVENDER_BED)

    # Central fountain as focal point — with olive branches and plinths
    _lm_bg(world, flag_bx,     sy - 2, SHELL_FOUNTAIN)
    _lm_bg(world, flag_bx - 2, sy - 2, OLIVE_BRANCH)
    _lm_bg(world, flag_bx + 2, sy - 2, OLIVE_BRANCH)
    _lm_bg(world, flag_bx - 3, sy - 3, MARBLE_PLINTH)
    _lm_bg(world, flag_bx + 3, sy - 3, MARBLE_PLINTH)

    # East Asian variant gets koi pool
    if biome == "east_asian":
        _lm_bg(world, flag_bx,     sy - 2, KOI_POOL)
        _lm_bg(world, flag_bx - 1, sy - 2, KOI_POOL)

    _lm_flag(world, spec, flag_bx, sy)
    return flag_bx


# ---------------------------------------------------------------------------
# Vineyard Hall  (hedonist, mediterranean)  — wine hall with cellar and trellis
# ---------------------------------------------------------------------------

def _place_vineyard_hall(world, spec, biome, right_bx, sy, rng):
    W = 36
    left    = right_bx - W
    flag_bx = left + W // 2
    sy = _lm_clear_terrain(world, left, W, sy)

    # Grapevine trellis approach — 6 blocks each side, BG columns so the approach is walkable
    for side_bx in (range(left, left + 6), range(left + W - 6, left + W)):
        for bx in side_bx:
            _lm_set(world, bx, sy, POLISHED_MARBLE)
            # Trellis columns as BG only — visible but not blocking
            if (bx - left) % 3 == 0:
                _lm_fill_bg(world, bx, bx, sy - 6, sy - 1, GARDEN_COLUMN)
            # Grapevine drapes between columns (BG, multiple rows)
            for by in range(sy - 5, sy - 1):
                _lm_bg(world, bx, by, GRAPEVINE_CROP_MATURE)
        # Torch at trellis tops
        _lm_set(world, list(side_bx)[2], sy - 7, TORCH)

    # Central wine hall — 24 wide, 10 tall
    hx = left + 6
    _lm_fill(world, hx, hx + 23, sy, sy, POLISHED_MARBLE)
    _lm_fill(world, hx, hx + 23, sy - 10, sy - 10, POLISHED_MARBLE)
    _lm_fill(world, hx, hx + 23, sy - 11, sy - 11, POLISHED_MARBLE)  # cornice
    for bx in (hx, hx + 23):
        _lm_fill(world, bx, bx, sy - 11, sy, POLISHED_MARBLE)
    _lm_fill_bg(world, hx + 1, hx + 22, sy - 11, sy - 1, POLISHED_MARBLE)
    _lm_fill(world, hx + 1, hx + 22, sy - 1, sy - 1, ROMAN_MOSAIC)
    _lm_set(world, hx,      sy - 12, BRAZIER)
    _lm_set(world, hx + 23, sy - 12, BRAZIER)

    # Arched hall windows at two heights
    for bx in range(hx + 3, hx + 21, 5):
        _lm_bg(world, bx, sy - 7, ROMAN_ARCH_REN)
        _lm_bg(world, bx, sy - 3, ROMAN_ARCH_REN)

    # Barrel cellar — three rows of barrels on back wall (visible through arch bays)
    for bx in range(hx + 2, hx + 22, 2):
        _lm_bg(world, bx, sy - 2, RAIN_BARREL)
        _lm_bg(world, bx, sy - 3, RAIN_BARREL)
        if bx % 4 == 0:
            _lm_bg(world, bx, sy - 4, RAIN_BARREL)

    # Columns
    _lm_cols(world, hx + 1, hx + 22, sy - 2, 8, GARDEN_COLUMN, DORIC_CAPITAL, spacing=5)

    # Central tasting table — benches, wine display, olive branches (all BG)
    _lm_bg(world, flag_bx,     sy - 2, SHELL_FOUNTAIN)
    _lm_bg(world, flag_bx - 3, sy - 2, CARVED_BENCH)
    _lm_bg(world, flag_bx + 3, sy - 2, CARVED_BENCH)
    _lm_bg(world, flag_bx - 1, sy - 4, OLIVE_BRANCH)
    _lm_bg(world, flag_bx + 1, sy - 4, OLIVE_BRANCH)
    _lm_bg(world, flag_bx,     sy - 5, GRAPEVINE_CROP_MATURE)

    # Hall entrances — trellis approach is walkable, these are the actual hall doors
    _lm_entrance(world, hx,      sy, BRONZE_DOOR_CLOSED)
    _lm_entrance(world, hx + 23, sy, BRONZE_DOOR_CLOSED)

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
