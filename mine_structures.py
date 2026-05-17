"""Underground mine carving for the Miners' Guild.

When a Miners-industry outpost is built, `generate_mine` carves a branching
mineshaft beneath it: a vertical entry shaft (with a wellhead room at the
top), two to three horizontal galleries at different depths, side alcoves
off the galleries, and ore-rich chambers at the end of each gallery.

Per-outpost flavor lives in `OUTPOST_MINE_PROFILES`: coal pits seed coal-
heavy chambers, lapidary ateliers seed crystal/ruby, dwarven holds get
the grand pillared hall, gold-panning camps go shallow with sparse but
gold-rich pockets, etc.

All decorative fixtures (timber supports, rails, lanterns, entrance arch,
parked cart, scaffolding, debris, ore heaps, pillars) are placed as
background blocks so the player can walk freely through the tunnels.

Pure worldgen — call once per mining outpost at build time.
"""

import random

from blocks import (
    AIR, STONE, LADDER, WATER,
    COAL_ORE, IRON_ORE, GOLD_ORE, CRYSTAL_ORE, RUBY_ORE, OBSIDIAN,
    MINE_ENTRANCE_BLOCK, MINE_SUPPORT_BEAM, MINE_TIMBER_FRAME,
    MINE_RAIL, MINE_CART_DECOR, MINE_LANTERN_BLOCK,
    MINE_SCAFFOLD, MINE_DEBRIS, MINE_ORE_HEAP, MINE_PILLAR_BLOCK,
)

# ---------------------------------------------------------------------------
# Layout constants — defaults; profiles below can override per outpost type.
# ---------------------------------------------------------------------------

SHAFT_WIDTH        = 3       # entry shaft is 3 blocks wide
SHAFT_DEPTH_MIN    = 35
SHAFT_DEPTH_MAX    = 55
WELLHEAD_W         = 7       # width of the room around the shaft mouth
WELLHEAD_H         = 3       # height of the wellhead room
GALLERY_HEIGHT     = 3
GALLERY_LEN_MIN    = 14
GALLERY_LEN_MAX    = 26
CHAMBER_W          = 8
CHAMBER_H          = 4
SUPPORT_SPACING    = 5
LANTERN_SPACING    = 8
ORE_FILL_CHANCE    = 0.55    # default; profiles override
ALCOVE_CHANCE      = 0.45    # per-segment chance of a side alcove
ALCOVE_SPACING     = 7       # check for an alcove every N blocks of gallery
DEBRIS_CHANCE      = 0.15    # random rubble pile per gallery floor block

_BRANCH_DEPTHS         = (12, 24, 38)
_BRANCH_DEPTHS_SHALLOW = ( 6, 12, 18)   # for shallow placer-style profiles

# Sub-level shaft constants — used when a profile sets sub_levels > 0.
SUBSHAFT_DEPTH_MIN   = 20    # how far the sub-shaft descends below its parent
SUBSHAFT_DEPTH_MAX   = 35
SUBLEVEL_GALLERY_LEN = (16, 28)
JUNCTION_W           = 5     # width of the hub room where shaft meets a gallery
JUNCTION_H           = 4
SUMP_DEPTH           = 3     # water depth at the bottom of every shaft
SUMP_HALF_W          = 2     # widens shaft by this much each side at the sump
VEIN_CLUSTER_SIZE    = 5     # ore blocks per cluster (anchor + neighbors)
VEIN_CLUSTER_COUNT   = (3, 6)  # number of clusters seeded per chamber


# ---------------------------------------------------------------------------
# Per-outpost-type flavor profiles
# Each entry: ore_pool (list of (block_id, weight)), density, layout key,
#             optional shaft_depth tweak, lantern/heap counts.
# Outpost types not listed fall back to the "default" profile.
# ---------------------------------------------------------------------------

def _pool_balanced():
    return [(COAL_ORE, 35), (IRON_ORE, 45), (GOLD_ORE, 15), (CRYSTAL_ORE, 5)]

def _pool_coal_heavy():
    return [(COAL_ORE, 80), (IRON_ORE, 15), (GOLD_ORE, 5)]

def _pool_stone_quarry():
    return [(STONE, 60), (COAL_ORE, 25), (IRON_ORE, 15)]

def _pool_marble():
    return [(STONE, 70), (CRYSTAL_ORE, 20), (IRON_ORE, 10)]

def _pool_gem():
    return [(RUBY_ORE, 45), (CRYSTAL_ORE, 35), (GOLD_ORE, 15), (OBSIDIAN, 5)]

def _pool_prospector():
    return [(COAL_ORE, 25), (IRON_ORE, 30), (GOLD_ORE, 25),
            (CRYSTAL_ORE, 15), (RUBY_ORE, 5)]

def _pool_dwarven():
    return [(GOLD_ORE, 35), (RUBY_ORE, 25), (CRYSTAL_ORE, 20),
            (OBSIDIAN, 15), (IRON_ORE, 5)]

def _pool_sulfur():
    return [(OBSIDIAN, 35), (RUBY_ORE, 20), (COAL_ORE, 30), (IRON_ORE, 15)]

def _pool_panning():
    return [(GOLD_ORE, 70), (IRON_ORE, 25), (COAL_ORE, 5)]

OUTPOST_MINE_PROFILES = {
    "default": {
        "ore_pool":    _pool_balanced, "density": 0.55, "layout": "standard",
        "shaft_depth": (35, 55), "extra_heaps": 0, "sub_levels": 0,
    },
    "deep_mine_camp": {
        "ore_pool":    _pool_balanced, "density": 0.60, "layout": "standard",
        "shaft_depth": (40, 60), "extra_heaps": 1, "sub_levels": 1,
    },
    "coal_pit": {
        "ore_pool":    _pool_coal_heavy, "density": 0.70, "layout": "standard",
        "shaft_depth": (25, 40), "extra_heaps": 2, "sub_levels": 0,
    },
    "quarry_camp": {
        "ore_pool":    _pool_stone_quarry, "density": 0.45, "layout": "standard",
        "shaft_depth": (15, 30), "extra_heaps": 1, "sub_levels": 0,
    },
    "marble_quarry": {
        "ore_pool":    _pool_marble, "density": 0.50, "layout": "standard",
        "shaft_depth": (15, 30), "extra_heaps": 2, "sub_levels": 0,
    },
    "lapidary_atelier": {
        "ore_pool":    _pool_gem, "density": 0.40, "layout": "standard",
        "shaft_depth": (30, 50), "extra_heaps": 1, "sub_levels": 1,
    },
    "prospector_post": {
        "ore_pool":    _pool_prospector, "density": 0.50, "layout": "standard",
        "shaft_depth": (35, 55), "extra_heaps": 0, "sub_levels": 1,
    },
    "dwarven_hold": {
        "ore_pool":    _pool_dwarven, "density": 0.65, "layout": "dwarven_hall",
        "shaft_depth": (50, 70), "extra_heaps": 3, "sub_levels": 2,
    },
    "sulfur_pit": {
        "ore_pool":    _pool_sulfur, "density": 0.55, "layout": "standard",
        "shaft_depth": (25, 45), "extra_heaps": 1, "sub_levels": 0,
    },
    "gold_panning_camp": {
        "ore_pool":      _pool_panning, "density": 0.45, "layout": "standard",
        "shaft_depth":   (12, 22), "extra_heaps": 1, "sub_levels": 0,
        "branch_depths": _BRANCH_DEPTHS_SHALLOW,
    },
}


def profile_for(outpost_type: str) -> dict:
    return OUTPOST_MINE_PROFILES.get(outpost_type, OUTPOST_MINE_PROFILES["default"])


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------

def generate_mine(world, surface_bx: int, surface_sy: int,
                  rng: random.Random = None,
                  outpost_type: str = "default") -> None:
    """Carve a branching mineshaft below (surface_bx, surface_sy) tailored to
    the outpost type. Defaults to the balanced 'default' profile if the
    outpost type is unknown."""
    if rng is None:
        rng = random.Random((surface_bx * 7919) & 0xFFFFFFFF)

    profile = profile_for(outpost_type)
    depth_lo, depth_hi = profile["shaft_depth"]
    shaft_bottom = surface_sy + rng.randint(depth_lo, depth_hi)
    shaft_bottom = min(shaft_bottom, world.height - 6)

    _carve_entrance(world, surface_bx, surface_sy)
    _carve_wellhead_room(world, surface_bx, surface_sy)
    _carve_shaft(world, surface_bx, surface_sy, shaft_bottom)
    _carve_sump(world, surface_bx, shaft_bottom)

    n_branches = rng.randint(2, 3)
    sides = [-1, 1]
    rng.shuffle(sides)
    branch_depths = profile.get("branch_depths", _BRANCH_DEPTHS)
    deepest_chamber = None     # (chamber_center_bx, gallery_y, side)
    for i in range(n_branches):
        depth_off = branch_depths[i] if i < len(branch_depths) else branch_depths[-1] + i * 6
        gallery_y = surface_sy + depth_off
        if gallery_y + GALLERY_HEIGHT >= shaft_bottom - 2:
            continue
        side = sides[i % len(sides)]
        length = rng.randint(GALLERY_LEN_MIN, GALLERY_LEN_MAX)
        # Carve a junction hub where the shaft opens into this gallery.
        _carve_junction_hub(world, surface_bx, gallery_y)
        chamber_center = _carve_gallery(world, surface_bx, gallery_y, side,
                                        length, rng, profile)
        deepest_chamber = (chamber_center, gallery_y, side)

    # Multi-level: descend from the deepest chamber's floor into a sub-level.
    sub_levels = profile.get("sub_levels", 0)
    if sub_levels > 0 and deepest_chamber is not None:
        _carve_sub_level(world, deepest_chamber, sub_levels, profile, rng)


# ---------------------------------------------------------------------------
# Entrance + wellhead + shaft
# ---------------------------------------------------------------------------

def _carve_entrance(world, bx: int, sy: int) -> None:
    for dy in range(1, 4):
        for dx in (-1, 0, 1):
            _set_air(world, bx + dx, sy - dy)
    _set_bg(world, bx, sy - 1, MINE_ENTRANCE_BLOCK)
    _set_bg(world, bx - 1, sy - 1, MINE_SUPPORT_BEAM)
    _set_bg(world, bx + 1, sy - 1, MINE_SUPPORT_BEAM)
    _set_bg(world, bx, sy - 2, MINE_TIMBER_FRAME)
    # Two flanking ore heaps at the doorstep — visible signage that this is
    # a working mine, not an abandoned shaft.
    _set_bg(world, bx - 2, sy - 1, MINE_ORE_HEAP)
    _set_bg(world, bx + 2, sy - 1, MINE_ORE_HEAP)


def _carve_wellhead_room(world, bx: int, sy: int) -> None:
    """Carve a small chamber around the shaft mouth so the entrance has
    breathing room — scaffolding, lanterns, a foreman desk feel."""
    half = WELLHEAD_W // 2
    for dy in range(WELLHEAD_H):
        for dx in range(-half, half + 1):
            _set_air(world, bx + dx, sy + dy)
    # Ceiling beam across the whole room
    for dx in range(-half, half + 1):
        _set_bg(world, bx + dx, sy, MINE_TIMBER_FRAME)
    # Floor rails across the room
    for dx in range(-half, half + 1):
        _set_bg(world, bx + dx, sy + WELLHEAD_H - 1, MINE_RAIL)
    # Scaffolding at the corners
    _set_bg(world, bx - half, sy + 1, MINE_SCAFFOLD)
    _set_bg(world, bx + half, sy + 1, MINE_SCAFFOLD)
    # A wall lantern on each side
    _set_bg(world, bx - half + 1, sy + 1, MINE_LANTERN_BLOCK)
    _set_bg(world, bx + half - 1, sy + 1, MINE_LANTERN_BLOCK)
    # Solid foreground platforms flanking the shaft mouth so the player can
    # walk across the wellhead instead of immediately dropping in. The
    # ladder column (bx) is left open so the shaft is still enterable.
    _bridge_shaft_floor(world, bx, sy + WELLHEAD_H)


def _carve_shaft(world, bx: int, sy: int, bottom: int) -> None:
    half = SHAFT_WIDTH // 2
    for y in range(sy, bottom + 1):
        for dx in range(-half, half + 1):
            _set_air(world, bx + dx, y)
        _set_block(world, bx, y, LADDER)
        if (y - sy) % SUPPORT_SPACING == 0 and y > sy:
            _set_bg(world, bx - half - 1, y, MINE_SUPPORT_BEAM)
            _set_bg(world, bx + half + 1, y, MINE_SUPPORT_BEAM)
            _set_bg(world, bx, y, MINE_TIMBER_FRAME)
        if (y - sy) % LANTERN_SPACING == 4:
            _set_bg(world, bx - half, y, MINE_LANTERN_BLOCK)


def _carve_junction_hub(world, bx: int, gy: int) -> None:
    """Carve a small hub room where the vertical shaft meets a gallery —
    gives each level a readable landing instead of a flat T-intersection."""
    half_w = JUNCTION_W // 2
    for dx in range(-half_w, half_w + 1):
        for dy in range(JUNCTION_H):
            _set_air(world, bx + dx, gy + dy)
    floor_y = gy + JUNCTION_H - 1
    # Floor rails + ceiling beam across the hub
    for dx in range(-half_w, half_w + 1):
        _set_bg(world, bx + dx, gy, MINE_TIMBER_FRAME)
        _set_bg(world, bx + dx, floor_y, MINE_RAIL)
    # Corner supports
    _set_bg(world, bx - half_w, gy + 1, MINE_SUPPORT_BEAM)
    _set_bg(world, bx + half_w, gy + 1, MINE_SUPPORT_BEAM)
    # Hub lantern hanging from the ceiling
    _set_bg(world, bx, gy + 1, MINE_LANTERN_BLOCK)
    # The hub corners stand on uncarved stone, but the shaft column (bx ± 1)
    # is one continuous air drop — bridge it with foreground timber so each
    # gallery level is a real landing instead of a hole in the floor.
    _bridge_shaft_floor(world, bx, gy + JUNCTION_H)


def _carve_sump(world, bx: int, bottom: int) -> None:
    """Widen the shaft bottom and fill the lowest few rows with water —
    every mine ends in a flooded bedrock pool."""
    half = SHAFT_WIDTH // 2 + SUMP_HALF_W
    sump_top = bottom
    sump_bot = min(world.height - 2, bottom + SUMP_DEPTH)
    for y in range(sump_top, sump_bot + 1):
        for dx in range(-half, half + 1):
            _set_air(world, bx + dx, y)
    # Frame the sump with timber and add a single lantern above the water line
    _set_bg(world, bx - half, sump_top, MINE_SUPPORT_BEAM)
    _set_bg(world, bx + half, sump_top, MINE_SUPPORT_BEAM)
    _set_bg(world, bx, sump_top, MINE_TIMBER_FRAME)
    _set_bg(world, bx - half + 1, sump_top, MINE_LANTERN_BLOCK)
    # Fill the bottom three rows with water
    for y in range(sump_bot - SUMP_DEPTH + 1, sump_bot + 1):
        for dx in range(-half + 1, half):
            _set_block(world, bx + dx, y, WATER)
    # A debris pile and an ore heap on the dry rim of the sump
    _set_bg(world, bx + half - 1, sump_top, MINE_DEBRIS)
    _set_bg(world, bx - half + 1, sump_top, MINE_ORE_HEAP)


def _bridge_shaft_floor(world, shaft_bx: int, y: int) -> None:
    """Plant solid foreground timber on either side of the ladder column at
    row `y` so the shaft has a real, standable floor at this level. The
    ladder column (shaft_bx) is left untouched so vertical traversal still
    works. Used at the wellhead, every junction, and every chamber→sub-
    shaft transition — without this the entire shaft is one continuous air
    drop from the entrance to the sump."""
    _set_block(world, shaft_bx - 1, y, MINE_TIMBER_FRAME)
    _set_block(world, shaft_bx + 1, y, MINE_TIMBER_FRAME)


def _carve_sub_level(world, parent_chamber, levels_remaining: int,
                     profile: dict, rng: random.Random) -> None:
    """Drop a sub-shaft from the parent chamber's floor and carve a deeper
    gallery + chamber at the bottom. Recurses for additional levels."""
    if levels_remaining <= 0:
        return
    parent_bx, parent_gy, parent_side = parent_chamber
    parent_floor = parent_gy + CHAMBER_H - 1
    sub_depth = rng.randint(SUBSHAFT_DEPTH_MIN, SUBSHAFT_DEPTH_MAX)
    sub_bottom = min(parent_floor + sub_depth, world.height - 6)

    # Carve the sub-shaft (narrower — 1 block wide ladder column)
    for y in range(parent_floor, sub_bottom + 1):
        for dx in (-1, 0, 1):
            _set_air(world, parent_bx + dx, y)
        _set_block(world, parent_bx, y, LADDER)
        if (y - parent_floor) % SUPPORT_SPACING == 0 and y > parent_floor:
            _set_bg(world, parent_bx - 2, y, MINE_SUPPORT_BEAM)
            _set_bg(world, parent_bx + 2, y, MINE_SUPPORT_BEAM)
        if (y - parent_floor) % LANTERN_SPACING == 3:
            _set_bg(world, parent_bx - 1, y, MINE_LANTERN_BLOCK)
    # The sub-shaft just punched a hole through the chamber's supporting
    # stone — bridge it so the chamber floor stays standable on either
    # side of the new ladder column.
    _bridge_shaft_floor(world, parent_bx, parent_floor + 1)

    # Sub-level gallery (one direction, opposite side from parent for variety)
    sub_gy = sub_bottom - GALLERY_HEIGHT - 1
    sub_side = -parent_side
    sub_len = rng.randint(*SUBLEVEL_GALLERY_LEN)
    _carve_junction_hub(world, parent_bx, sub_gy)
    sub_chamber_center = _carve_gallery(world, parent_bx, sub_gy, sub_side,
                                        sub_len, rng, profile)

    if levels_remaining > 1:
        # Recurse: descend one more level from this deeper chamber.
        _carve_sub_level(world,
                         (sub_chamber_center, sub_gy, sub_side),
                         levels_remaining - 1, profile, rng)


def _seed_ore_clusters(world, lo_bx: int, hi_bx: int, cy_lo: int, cy_hi: int,
                       profile: dict, rng: random.Random,
                       extra_clusters: int = 0) -> None:
    """Place vein clusters in the walls around a chamber. Each cluster picks
    one ore type and seeds a 4–6 block patch — feels more geological than
    pure random scatter."""
    base_count_lo, base_count_hi = VEIN_CLUSTER_COUNT
    density = profile["density"]
    cluster_count = rng.randint(base_count_lo, base_count_hi) + extra_clusters
    # Add a density bonus: high-density chambers get extra clusters.
    cluster_count += int(density * 4)

    # Candidate anchor positions: any wall block one row outside the chamber.
    anchors = []
    for bx in range(lo_bx - 1, hi_bx + 2):
        anchors.append((bx, cy_lo - 1))
        anchors.append((bx, cy_hi + 1))
    for by in range(cy_lo, cy_hi + 1):
        anchors.append((lo_bx - 1, by))
        anchors.append((hi_bx + 1, by))
    rng.shuffle(anchors)

    for i in range(min(cluster_count, len(anchors))):
        ax, ay = anchors[i]
        ore = _pick_ore(ay, profile, rng)
        _set_block(world, ax, ay, ore)
        # Seed neighbours of the same ore type for the vein feel
        for _ in range(VEIN_CLUSTER_SIZE - 1):
            dx = rng.choice((-2, -1, -1, 0, 1, 1, 2))
            dy = rng.choice((-1, -1, 0, 0, 1, 1))
            nx, ny = ax + dx, ay + dy
            # Don't poke ore into the hollow chamber interior
            if lo_bx <= nx <= hi_bx and cy_lo <= ny <= cy_hi:
                continue
            _set_block(world, nx, ny, ore)


# ---------------------------------------------------------------------------
# Galleries, alcoves, chambers
# ---------------------------------------------------------------------------

def _carve_gallery(world, shaft_bx: int, gy: int, side: int, length: int,
                   rng: random.Random, profile: dict) -> int:
    """Carve gallery + chamber. Returns the chamber's center bx (used by the
    caller to anchor a sub-level descent from the deepest chamber)."""
    step = 1 if side > 0 else -1
    start = shaft_bx + (SHAFT_WIDTH // 2 + 1) * step
    end   = start + length * step

    floor_y = gy + GALLERY_HEIGHT - 1
    for i, bx in enumerate(range(start, end, step)):
        for dy in range(GALLERY_HEIGHT):
            _set_air(world, bx, gy + dy)
        _set_bg(world, bx, floor_y, MINE_RAIL)
        if i % 2 == 0:
            _set_bg(world, bx, gy, MINE_TIMBER_FRAME)
        if i % SUPPORT_SPACING == 0 and i > 0:
            _set_bg(world, bx, gy + 1, MINE_SUPPORT_BEAM)
        if i % LANTERN_SPACING == 5:
            _set_bg(world, bx, gy + 1, MINE_LANTERN_BLOCK)
        if i > 2 and i < length - 2 and rng.random() < DEBRIS_CHANCE:
            _set_bg(world, bx, floor_y, MINE_DEBRIS)
        if i > 0 and i % ALCOVE_SPACING == 0 and rng.random() < ALCOVE_CHANCE:
            _carve_alcove(world, bx, gy, rng.choice((-1, 1)), profile, rng)

    threshold = end
    _set_bg(world, threshold - step, gy, MINE_SCAFFOLD)
    _set_bg(world, threshold - step, gy + GALLERY_HEIGHT - 2, MINE_SCAFFOLD)

    if profile.get("layout") == "dwarven_hall":
        return _carve_dwarven_hall(world, end, gy, side, profile, rng)
    return _carve_chamber(world, end, gy, side, profile, rng)


def _carve_alcove(world, bx: int, gy: int, vertical: int,
                  profile: dict, rng: random.Random) -> None:
    """Small 3x3 niche above or below the gallery — debris, ore heap, or a
    bonus ore deposit. Vertical: -1 = above, +1 = below."""
    if vertical < 0:
        ay = gy - 3
        if ay < 1:
            return
    else:
        ay = gy + GALLERY_HEIGHT
        if ay + 3 >= 220:
            return
    for dx in (-1, 0, 1):
        for dy in range(3):
            _set_air(world, bx + dx, ay + dy)
    # Frame the alcove
    _set_bg(world, bx - 1, ay, MINE_TIMBER_FRAME)
    _set_bg(world, bx,     ay, MINE_TIMBER_FRAME)
    _set_bg(world, bx + 1, ay, MINE_TIMBER_FRAME)
    # Contents: choose by roll
    pick = rng.random()
    floor = ay + 2
    if pick < 0.40:
        _set_bg(world, bx, floor, MINE_ORE_HEAP)
    elif pick < 0.75:
        _set_bg(world, bx - 1, floor, MINE_DEBRIS)
        _set_bg(world, bx + 1, floor, MINE_DEBRIS)
    else:
        _set_bg(world, bx, ay + 1, MINE_LANTERN_BLOCK)
    # Seed a couple of bonus ore in the alcove walls
    for cbx in (bx - 2, bx + 2):
        for cby in (ay, ay + 1, ay + 2):
            if rng.random() < 0.55:
                _set_block(world, cbx, cby, _pick_ore(cby, profile, rng))


def _carve_chamber(world, near_bx: int, gy: int, side: int,
                   profile: dict, rng: random.Random) -> int:
    step = 1 if side > 0 else -1
    far  = near_bx + CHAMBER_W * step
    lo_bx, hi_bx = (near_bx, far) if step > 0 else (far, near_bx)
    cy_lo = gy - 1
    cy_hi = gy + CHAMBER_H
    floor_y = cy_hi - 1

    for bx in range(lo_bx, hi_bx + 1):
        for by in range(cy_lo, cy_hi + 1):
            _set_air(world, bx, by)

    for bx in range(lo_bx, hi_bx + 1):
        _set_bg(world, bx, floor_y, MINE_RAIL)
        _set_bg(world, bx, cy_lo, MINE_TIMBER_FRAME)
    _set_bg(world, lo_bx, cy_lo + 1, MINE_SUPPORT_BEAM)
    _set_bg(world, hi_bx, cy_lo + 1, MINE_SUPPORT_BEAM)
    mid = (lo_bx + hi_bx) // 2
    _set_bg(world, mid, cy_lo + 1, MINE_LANTERN_BLOCK)
    cart_bx = hi_bx - 1 if step > 0 else lo_bx + 1
    _set_bg(world, cart_bx, floor_y, MINE_CART_DECOR)
    heap_bx = lo_bx + 1 if step > 0 else hi_bx - 1
    _set_bg(world, heap_bx, floor_y, MINE_ORE_HEAP)
    for _ in range(profile.get("extra_heaps", 0)):
        hx = rng.randint(lo_bx + 1, hi_bx - 1)
        _set_bg(world, hx, floor_y, MINE_ORE_HEAP)

    _seed_ore_clusters(world, lo_bx, hi_bx, cy_lo, cy_hi, profile, rng)
    return mid


def _carve_dwarven_hall(world, near_bx: int, gy: int, side: int,
                        profile: dict, rng: random.Random) -> int:
    """Grand pillared hall — wider, taller, with two rows of carved pillars
    and dense rare-ore walls. Only used for dwarven_hold outposts."""
    step = 1 if side > 0 else -1
    hall_w = 14
    hall_h = 6
    far = near_bx + hall_w * step
    lo_bx, hi_bx = (near_bx, far) if step > 0 else (far, near_bx)
    cy_lo = gy - 2
    cy_hi = gy + hall_h
    floor_y = cy_hi - 1

    for bx in range(lo_bx, hi_bx + 1):
        for by in range(cy_lo, cy_hi + 1):
            _set_air(world, bx, by)

    # Stone-pillar-and-timber ceiling — alternating beam pattern
    for bx in range(lo_bx, hi_bx + 1):
        _set_bg(world, bx, cy_lo, MINE_TIMBER_FRAME)
        _set_bg(world, bx, floor_y, MINE_RAIL)

    # Two rows of pillars (4 pillars, framing a central aisle)
    pillar_xs = [lo_bx + 3, lo_bx + 7, hi_bx - 7, hi_bx - 3]
    for px in pillar_xs:
        for py in range(cy_lo + 1, floor_y):
            _set_bg(world, px, py, MINE_PILLAR_BLOCK)

    # Lanterns hung between each pair of pillars
    for px in pillar_xs:
        _set_bg(world, px, cy_lo + 1, MINE_LANTERN_BLOCK)

    # Corner scaffolding
    _set_bg(world, lo_bx,     cy_lo + 1, MINE_SCAFFOLD)
    _set_bg(world, lo_bx,     cy_lo + 3, MINE_SCAFFOLD)
    _set_bg(world, hi_bx,     cy_lo + 1, MINE_SCAFFOLD)
    _set_bg(world, hi_bx,     cy_lo + 3, MINE_SCAFFOLD)

    # Cart at the far end, foreman ore heaps in a row
    cart_bx = hi_bx - 2 if step > 0 else lo_bx + 2
    _set_bg(world, cart_bx, floor_y, MINE_CART_DECOR)
    for hx in (lo_bx + 1, lo_bx + 5, hi_bx - 5, hi_bx - 1):
        _set_bg(world, hx, floor_y, MINE_ORE_HEAP)

    # Dense rare-ore walls (more clusters for the grand hall)
    _seed_ore_clusters(world, lo_bx, hi_bx, cy_lo, cy_hi, profile, rng,
                       extra_clusters=4)
    return (lo_bx + hi_bx) // 2


# ---------------------------------------------------------------------------
# Ore selection — depth-aware mix of the profile's ore pool
# ---------------------------------------------------------------------------

def _pick_ore(depth: int, profile: dict, rng: random.Random) -> int:
    pool = profile["ore_pool"]()
    total = sum(w for _, w in pool)
    roll = rng.randint(1, total)
    acc = 0
    for bid, w in pool:
        acc += w
        if roll <= acc:
            return bid
    return pool[0][0]


# ---------------------------------------------------------------------------
# World-write helpers — out-of-bounds is silently ignored to keep worldgen
# robust against partial chunk loading at world edges.
# ---------------------------------------------------------------------------

def _set_block(world, bx: int, by: int, block_id: int) -> None:
    try:
        if 0 <= by < world.height:
            world.set_block(bx, by, block_id)
    except Exception:
        pass


def _set_air(world, bx: int, by: int) -> None:
    _set_block(world, bx, by, AIR)


def _set_bg(world, bx: int, by: int, block_id: int) -> None:
    try:
        if 0 <= by < world.height:
            world.set_bg_block(bx, by, block_id)
    except Exception:
        pass
