"""Ruins — broken settlements left behind by the history sim.

A "ruin" is a small cluster of weathered walls (mossy brick / cobblestone /
cracked stone) with collapsed sections, scattered rubble, and one or more
chests holding era-appropriate loot pulled from the original kingdom's agenda.

Spawned lazily during chunk streaming via ``spawn_ruins_for_chunk`` (see
world.py / cities.py wiring). Idempotent — tracks already-built settlement
ids on the World instance.
"""

import random

from blocks import (
    AIR, GRASS, DIRT, STONE, COBBLESTONE, MOSSY_BRICK, CRACKED_STONE,
    MOSS_PATCH, SAND, CHEST_BLOCK, RUIN_MARKER_BLOCK,
)
from constants import SURFACE_Y


# ---------------------------------------------------------------------------
# Loot tables
# ---------------------------------------------------------------------------

# Items that can appear in any ruin chest (filler).
_LOOT_COMMON = [
    ("dirt_clump", 1, 4),
    ("stone_chip", 1, 3),
    ("cobblestone", 1, 3),
    ("crystal_shard", 1, 2),
    ("bone", 1, 2),
    ("clay", 1, 2),
    ("rock_dust", 1, 2),
]

# Items biased by the ruined kingdom's agenda — what its rulers hoarded.
_LOOT_BY_AGENDA = {
    "martial":    [("iron_chunk", 1, 4), ("bone_arrow", 1, 6),
                   ("stone_pickaxe", 1, 1)],
    "mercantile": [("gold_nugget", 1, 3), ("amethyst_gem", 1, 1),
                   ("citrine_gem", 1, 1), ("quartz_gem", 1, 2)],
    "scholarly":  [("philosophers_scroll", 1, 1), ("quartz_gem", 1, 2),
                   ("rare_mushroom", 1, 2)],
    "pious":      [("clay_oil_lamp", 1, 2), ("ruby_dust", 1, 1),
                   ("emerald_dust", 1, 1)],
    "builder":    [("cobblestone", 3, 8), ("rough_stone_wall", 1, 2),
                   ("iron_chunk", 1, 2)],
    "hedonist":   [("pottery_vase", 1, 1), ("ruby", 1, 1),
                   ("gold_nugget", 1, 2)],
}

# Higher-value relic tier — small chance, weighted up by ruin age.
_LOOT_RELICS = [
    ("diamond", 1, 1),
    ("ruby", 1, 1),
    ("philosophers_scroll", 1, 1),
    ("pottery_vase_fine", 1, 1),
]


def roll_chest_contents(rng: random.Random, agenda: str, age_years: int) -> dict:
    """Build a chest inventory dict {item_id: count} for one ruin chest."""
    contents = {}
    # 2-4 common drops
    for _ in range(rng.randint(2, 4)):
        item, lo, hi = rng.choice(_LOOT_COMMON)
        contents[item] = contents.get(item, 0) + rng.randint(lo, hi)
    # 1-2 agenda drops
    pool = _LOOT_BY_AGENDA.get(agenda, _LOOT_BY_AGENDA["builder"])
    for _ in range(rng.randint(1, 2)):
        item, lo, hi = rng.choice(pool)
        contents[item] = contents.get(item, 0) + rng.randint(lo, hi)
    # Relic chance: scales with how old the ruin is.
    relic_chance = min(0.6, 0.10 + age_years * 0.0010)
    if rng.random() < relic_chance:
        item, lo, hi = rng.choice(_LOOT_RELICS)
        contents[item] = contents.get(item, 0) + rng.randint(lo, hi)
    return contents


# ---------------------------------------------------------------------------
# Building shapes
# ---------------------------------------------------------------------------

# Each template is a list of "structures" placed relative to ruin center bx.
# A structure = (offset_x, width, wall_height) where the building was once a
# rectangle of that footprint; the ruin renderer randomly knocks out chunks
# of the wall to leave a broken silhouette.

_TEMPLATES = {
    "small":      [(-3, 7, 4)],
    "medium":     [(-7, 6, 5), (1, 6, 4)],
    "large":      [(-10, 6, 5), (-2, 7, 6), (6, 5, 4)],
    "metropolis": [(-14, 6, 5), (-6, 8, 7), (3, 7, 5), (11, 6, 4)],
}


def _template_for(tier: str) -> list:
    if tier in ("metropolis", "megalopolis"):
        return _TEMPLATES["metropolis"]
    if tier in ("city", "town"):
        return _TEMPLATES["large"]
    if tier == "village":
        return _TEMPLATES["medium"]
    return _TEMPLATES["small"]


# ---------------------------------------------------------------------------
# Block-placement helpers
# ---------------------------------------------------------------------------

def _safe_set(world, x: int, y: int, bid: int):
    """Set foreground block, but only into chunks that are loaded."""
    cx = x // 32  # CHUNK_W
    if cx not in world._chunks:
        return False
    if y < 0 or y >= world.height:
        return False
    chunk = world._chunks[cx]
    chunk[y][x % 32] = bid
    world._dirty_chunks.add(cx)
    return True


def _wall_block(rng: random.Random, biome: str) -> int:
    """Pick a weathered wall block, biased by biome (sandy ruins → cobblestone)."""
    if biome in ("desert", "wasteland", "canyon", "arid_steppe"):
        return rng.choice([COBBLESTONE, COBBLESTONE, CRACKED_STONE])
    return rng.choice([MOSSY_BRICK, MOSSY_BRICK, COBBLESTONE, CRACKED_STONE])


def _build_one_structure(world, rng, base_x: int, sy: int,
                         offset_x: int, width: int, wall_h: int,
                         biome: str, chest_pos_out: list):
    """Place one broken-rectangle structure. Records candidate chest positions."""
    x0 = base_x + offset_x
    x1 = x0 + width

    # Walls — left and right verticals, with random missing rows.
    for wall_x in (x0, x1 - 1):
        for dy in range(wall_h):
            # Higher rows more likely to be knocked out.
            knockout = rng.random() < 0.10 + dy * 0.18
            if knockout:
                continue
            _safe_set(world, wall_x, sy - 1 - dy, _wall_block(rng, biome))

    # Bottom row of front/back interior — partial floor
    for x in range(x0 + 1, x1 - 1):
        if rng.random() < 0.65:
            _safe_set(world, x, sy - 1, _wall_block(rng, biome))

    # Rubble piles at the base
    for x in range(x0 - 1, x1 + 1):
        if rng.random() < 0.30:
            _safe_set(world, x, sy, COBBLESTONE)
        elif rng.random() < 0.20:
            _safe_set(world, x, sy, MOSS_PATCH)

    # Chest candidate: midway, ground level.
    chest_pos_out.append((x0 + width // 2, sy - 1))


def spawn_ruin_for_settlement(world, settlement) -> bool:
    """Build one ruin's worth of geometry + chests at this settlement.

    Returns True if anything was placed (chunks must be loaded for the
    settlement's x range; otherwise returns False and we'll retry next stream).
    """
    plan = world.plan
    if settlement.state not in ("ruin", "abandoned"):
        return False

    # Idempotency: track per-World which settlement ids we've materialized.
    built = getattr(world, "_ruins_built", None)
    if built is None:
        built = set()
        world._ruins_built = built
    if settlement.settlement_id in built:
        return False

    base_x = settlement.world_x

    # Make sure all relevant chunks are loaded — the template can span ~30 blocks.
    span_lo = base_x - 16
    span_hi = base_x + 16
    chunk_lo = span_lo // 32
    chunk_hi = (span_hi - 1) // 32
    for cx in range(chunk_lo, chunk_hi + 1):
        if cx not in world._chunks:
            return False  # caller will retry once chunks finish streaming

    # Don't spawn ruins underwater.
    biome = world.biodome_at(base_x)
    if biome == "ocean":
        built.add(settlement.settlement_id)
        return False
    if world.surface_height(base_x) > SURFACE_Y:
        built.add(settlement.settlement_id)
        return False

    rng = random.Random((world.seed ^ (settlement.settlement_id * 0x517F)) & 0xFFFFFFFF)
    sy = world.surface_height(base_x)
    template = _template_for(settlement.tier)

    chest_candidates = []
    for offset_x, width, wall_h in template:
        _build_one_structure(world, rng, base_x, sy,
                             offset_x, width, wall_h, biome, chest_candidates)

    # Place 1-2 chests with era-appropriate loot.
    kingdom = plan.kingdoms.get(settlement.original_kingdom_id)
    agenda = kingdom.agenda if kingdom else "builder"
    age_years = max(0, plan.history_years - settlement.ruined_year) if settlement.ruined_year > 0 else 100
    n_chests = 1 if settlement.tier in ("hamlet", "village") else 2
    rng.shuffle(chest_candidates)
    for cx_pos, cy_pos in chest_candidates[:n_chests]:
        if _safe_set(world, cx_pos, cy_pos, CHEST_BLOCK):
            world.chest_data[(cx_pos, cy_pos)] = roll_chest_contents(rng, agenda, age_years)

    # Place a weathered marker stone just outside the ruin footprint with a
    # lore plaque the player can read (E key). Lookup is by world_x against
    # plan.settlements, so no separate persistence is needed.
    marker_x = base_x
    marker_y = sy - 1
    if _safe_set(world, marker_x, marker_y, RUIN_MARKER_BLOCK):
        if not hasattr(world, "ruin_markers") or world.ruin_markers is None:
            world.ruin_markers = {}
        world.ruin_markers[(marker_x, marker_y)] = build_marker_info(plan, settlement)

    built.add(settlement.settlement_id)
    return True


# ---------------------------------------------------------------------------
# Marker plaque lookup
# ---------------------------------------------------------------------------

_CAUSE_PHRASE = {
    "sacked":     "Sacked in war.",
    "plague":     "Lost to plague.",
    "earthquake": "Levelled by an earthquake.",
    "decline":    "Slowly abandoned as fortunes faded.",
    "":           "Lost to time.",
}


def build_marker_info(plan, settlement) -> dict:
    """Compose the lore plaque dict for a single ruined settlement."""
    orig_k = plan.kingdoms.get(settlement.original_kingdom_id)
    cur_k  = plan.kingdoms.get(settlement.kingdom_id) if settlement.kingdom_id != -1 else None

    # Pull the chronicle events tied to this settlement, oldest first.
    events = plan.chronicle_for_settlement(settlement.settlement_id)
    event_lines = [f"Yr {e.year} — {e.text}" for e in events][-6:]

    # Founder dynasty when the settlement was raised (if known).
    founder_dyn = None
    if orig_k is not None:
        d = plan.dynasties.get(orig_k.dynasty_id)
        if d is not None:
            founder_dyn = d.house_name

    return {
        "name":              settlement.name,
        "tier":              settlement.tier,
        "founded_year":      settlement.founded_year,
        "ruined_year":       settlement.ruined_year,
        "cause_of_ruin":     settlement.cause_of_ruin or "",
        "cause_phrase":      _CAUSE_PHRASE.get(settlement.cause_of_ruin or "", _CAUSE_PHRASE[""]),
        "original_kingdom":  orig_k.name if orig_k else "an unknown realm",
        "current_kingdom":   cur_k.name if cur_k else None,
        "founder_dynasty":   founder_dyn,
        "events":            event_lines,
        "history_years":     plan.history_years,
    }


def lookup_marker_info(world, bx: int, by: int) -> dict | None:
    """Return the plaque info for a ruin marker at (bx,by). Cache-or-derive.

    Falls back to scanning ``world.plan.settlements`` for the closest ruined
    settlement within 24 blocks of bx, so save/load doesn't need persistence.
    """
    cache = getattr(world, "ruin_markers", None)
    if cache is not None and (bx, by) in cache:
        return cache[(bx, by)]
    plan = getattr(world, "plan", None)
    if plan is None:
        return None
    best = None
    best_dist = 25  # max search radius
    for s in plan.settlements.values():
        if s.state not in ("ruin", "abandoned"):
            continue
        dist = abs(s.world_x - bx)
        if dist < best_dist:
            best = s
            best_dist = dist
    if best is None:
        return None
    info = build_marker_info(plan, best)
    if cache is None:
        world.ruin_markers = {}
    world.ruin_markers[(bx, by)] = info
    return info


def spawn_ruins_for_chunk(world, cx: int):
    """Build any plan ruins/abandoned settlements whose footprint enters chunk cx."""
    plan = getattr(world, "plan", None)
    if plan is None:
        return
    base_x = cx * 32
    end_x = base_x + 32
    for s in plan.settlements.values():
        if s.state not in ("ruin", "abandoned"):
            continue
        # Footprint extends ~16 blocks each side of world_x; check overlap.
        if s.world_x + 16 < base_x or s.world_x - 16 >= end_x:
            continue
        spawn_ruin_for_settlement(world, s)
