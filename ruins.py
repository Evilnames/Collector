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
    LIMESTONE_BLOCK, OPUS_INCERTUM,
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
                   ("citrine_gem", 1, 1), ("quartz_gem", 1, 2),
                   ("coin_pouch", 1, 3)],
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
    ("coin_pouch", 1, 2),
]

# Dynasty heirlooms found in ruined-kingdom palaces, mausoleums, and chapter
# vaults. Rolled with a separate chance from _LOOT_RELICS so a single ruin
# can yield both a relic and a dynastic artifact. Heavier on portraits +
# regalia + funerary items (the things left behind when a kingdom falls).
_LOOT_DYNASTY = [
    # Regalia (common in ruined palaces)
    ("dynasty_throne_fragment", 1, 1),
    ("dynasty_throne_cushion", 1, 1),
    ("dynasty_state_mantle", 1, 1),
    ("dynasty_lesser_crown", 1, 1),
    ("dynasty_consort_crown", 1, 1),
    ("dynasty_royal_scepter", 1, 1),
    ("dynasty_orb_state", 1, 1),
    # Funerary (most ruins ARE mausoleums of fallen lines)
    ("dynasty_urn_gold", 1, 1),
    ("dynasty_urn_ivory", 1, 1),
    ("dynasty_urn_lacquer", 1, 1),
    ("dynasty_urn_jade", 1, 1),
    ("dynasty_death_mask_silver", 1, 1),
    ("dynasty_death_mask_gold", 1, 1),
    ("dynasty_ash_reliquary", 1, 1),
    ("dynasty_bone_casket", 1, 1),
    ("dynasty_grave_goods_set", 1, 1),
    ("dynasty_catafalque_plaque", 1, 1),
    ("dynasty_tombstone_rubbing", 1, 1),
    # Portraits & busts left in throne halls
    ("dynasty_founder_portrait", 1, 1),
    ("dynasty_bust_marble", 1, 1),
    ("dynasty_bust_bronze", 1, 1),
    ("dynasty_family_tree", 1, 1),
    ("dynasty_posthumous_portrait", 1, 1),
    ("dynasty_locket_miniature", 1, 1),
    # Heirlooms & signets
    ("dynasty_signet_founder", 1, 1),
    ("dynasty_signet_heir", 1, 1),
    ("dynasty_dowager_ring", 1, 1),
    ("dynasty_house_seal_stamp", 1, 1),
    ("dynasty_wax_seal_matrix", 1, 1),
    ("dynasty_lock_of_hair", 1, 1),
    ("dynasty_blood_vial", 1, 1),
    ("dynasty_frayed_banner", 1, 1),
    # Books / lineage / decree
    ("dynasty_book_lineage", 1, 1),
    ("dynasty_book_annals", 1, 1),
    ("dynasty_book_succession", 1, 1),
    ("dynasty_book_will", 1, 1),
    ("dynasty_book_decrees", 1, 1),
    ("dynasty_book_heraldry", 1, 1),
    # Jewelry
    ("dynasty_mourning_ring", 1, 1),
    ("dynasty_jade_pin", 1, 1),
    ("dynasty_diadem", 1, 1),
    ("dynasty_pearl_choker", 1, 1),
    ("dynasty_emerald_brooch", 1, 1),
    # Ceremonial arms
    ("dynasty_hereditary_longsword", 1, 1),
    ("dynasty_investiture_dagger", 1, 1),
    ("dynasty_gilded_mace", 1, 1),
    ("dynasty_ancestor_warhammer", 1, 1),
    # Court & toy heirlooms
    ("dynasty_music_box", 1, 1),
    ("dynasty_chess_board", 1, 1),
    ("dynasty_court_lute", 1, 1),
    ("dynasty_toy_horse", 1, 1),
    ("dynasty_toy_soldier_set", 1, 1),
    # Prophecy & oracle
    ("dynasty_founder_prophecy", 1, 1),
    ("dynasty_oracle_bones", 1, 1),
    ("dynasty_doom_prophecy", 1, 1),
    # Correspondence
    ("dynasty_love_letters", 1, 1),
    ("dynasty_sealed_letter", 1, 1),
    ("dynasty_court_decree", 1, 1),
    # Bastard tokens
    ("dynasty_bastard_quarter", 1, 1),
    ("dynasty_disinheritance_seal", 1, 1),
]

# Tier-2 high-value dynastic finds. Rolled only in older / capital ruins.
_LOOT_DYNASTY_GREAT = [
    ("dynasty_founders_crown", 1, 1),
    ("dynasty_state_crown", 1, 1),
    ("dynasty_coronation_crown", 1, 1),
    ("dynasty_sun_scepter", 1, 1),
    ("dynasty_tug_scepter", 1, 1),
    ("dynasty_lotus_scepter", 1, 1),
    ("dynasty_cross_orb", 1, 1),
    ("dynasty_sun_orb", 1, 1),
    ("dynasty_lotus_orb", 1, 1),
    ("dynasty_bust_jade", 1, 1),
    ("dynasty_bust_ivory", 1, 1),
    ("dynasty_death_mask_jade", 1, 1),
    ("dynasty_urn_jade", 1, 1),
    ("dynasty_coronation_sword", 1, 1),
    ("dynasty_khan_bow_state", 1, 1),
    ("dynasty_shogun_tachi", 1, 1),
    ("dynasty_sultan_tulwar", 1, 1),
    ("dynasty_maharana_khanda", 1, 1),
    ("dynasty_shah_kontos", 1, 1),
    ("dynasty_pectoral_plate", 1, 1),
    ("dynasty_state_portrait", 1, 1),
    ("dynasty_coronation_portrait", 1, 1),
    ("dynasty_equestrian_portrait", 1, 1),
]

# Heritage artifact item ids — one placed when a matching lost artifact exists.
_HERITAGE_ITEM_IDS = {
    "artwork":    "lost_artwork",
    "codex":      "lost_codex",
    "relic":      "dynasty_relic",
    "instrument": "cultural_instrument",
    "fragment":   "sacred_fragment",
    "blueprint":  "architectural_plan",
    "idol":       "ancient_idol",
    "map":        "ancient_map",
    "vessel":     "antique_vessel",
}


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
    # Dynasty heirloom chance: ruined kingdoms leave behind regalia + funerary
    # gear. Scales steeply with age — a 600-year-old ruin is almost guaranteed.
    dynasty_chance = min(0.85, 0.20 + age_years * 0.0015)
    if rng.random() < dynasty_chance:
        item, lo, hi = rng.choice(_LOOT_DYNASTY)
        contents[item] = contents.get(item, 0) + rng.randint(lo, hi)
        # Older ruins occasionally roll a great-tier dynastic find on top.
        great_chance = max(0.0, (age_years - 200) * 0.00075)
        if rng.random() < min(0.55, great_chance):
            item, lo, hi = rng.choice(_LOOT_DYNASTY_GREAT)
            contents[item] = contents.get(item, 0) + rng.randint(lo, hi)
    return contents


def roll_coin_count(rng: random.Random, age_years: int) -> int:
    """How many coins to generate for this ruin chest (0-3). Older ruins → more coins."""
    base_chance = min(0.90, 0.35 + age_years * 0.0008)
    if rng.random() > base_chance:
        return 0
    # Older ruins tend to have more coins
    if age_years > 600:
        return rng.randint(1, 3)
    if age_years > 200:
        return rng.randint(1, 2)
    return 1


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


def _pick_heritage_artifact(rng, world, settlement, age_years: int):
    """Return a lost artifact dict for this ruin, or None.

    Chance scales with age. Artifacts already discovered or already placed
    in another chest are excluded.
    """
    heritage_chance = min(0.40, 0.06 + age_years * 0.0009)
    if rng.random() >= heritage_chance:
        return None
    plan = getattr(world, "plan", None)
    if plan is None or not plan.lost_artifacts:
        return None
    kingdom = plan.kingdoms.get(settlement.original_kingdom_id)
    if kingdom is None:
        return None
    already_placed = set(getattr(world, "ruin_artifact_chests", {}).values())
    already_found  = getattr(world, "discovered_artifacts", set())
    matching = [
        a for a in plan.lost_artifacts
        if a["origin_kingdom"] == kingdom.name
        and a["uid"] not in already_placed
        and a["uid"] not in already_found
    ]
    if not matching:
        # Fall back to any undiscovered, unplaced artifact.
        matching = [
            a for a in plan.lost_artifacts
            if a["uid"] not in already_placed
            and a["uid"] not in already_found
        ]
    return rng.choice(matching) if matching else None


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

    # Pick a heritage artifact for this ruin (at most one per ruin).
    heritage_artifact = _pick_heritage_artifact(rng, world, settlement, age_years)

    for i, (cx_pos, cy_pos) in enumerate(chest_candidates[:n_chests]):
        if _safe_set(world, cx_pos, cy_pos, CHEST_BLOCK):
            world.chest_data[(cx_pos, cy_pos)] = roll_chest_contents(rng, agenda, age_years)
            # Slip the heritage artifact into the first chest.
            if i == 0 and heritage_artifact is not None:
                item_id = _HERITAGE_ITEM_IDS[heritage_artifact["category"]]
                world.chest_data[(cx_pos, cy_pos)][item_id] = \
                    world.chest_data[(cx_pos, cy_pos)].get(item_id, 0) + 1
                if not hasattr(world, "ruin_artifact_chests"):
                    world.ruin_artifact_chests = {}
                world.ruin_artifact_chests[(cx_pos, cy_pos)] = heritage_artifact["uid"]

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


# ---------------------------------------------------------------------------
# Underground ruins — buried city layers beneath old alive settlements
# ---------------------------------------------------------------------------
# Like Rome built on top of ancient Rome: old cities accumulate a buried layer
# of weathered walls, floors, and rubble that the player discovers by mining
# down through the soil beneath a living city.

# Layout configs: span = half-width of the buried level in blocks
_UG_CONFIGS = {
    "small":  {"span": 14, "room_h": 4, "wall_spacing": 7},
    "medium": {"span": 24, "room_h": 5, "wall_spacing": 9},
    "large":  {"span": 40, "room_h": 6, "wall_spacing": 10},
}

# Relic-tier loot bumped up for underground finds (deeper = rarer)
_UG_LOOT_RELICS = [
    ("diamond", 1, 1),
    ("ruby", 1, 1),
    ("alexandrite", 1, 1),
    ("philosophers_scroll", 1, 2),
    ("pottery_vase_fine", 1, 1),
    ("amethyst_gem", 1, 2),
]


def _ug_wall_block(rng: random.Random, age_factor: float) -> int:
    """Wall material — older settlements use more degraded/archaic blocks."""
    if age_factor >= 0.75:
        return rng.choices(
            [OPUS_INCERTUM, COBBLESTONE, MOSSY_BRICK, CRACKED_STONE],
            weights=[4, 3, 2, 2],
        )[0]
    if age_factor >= 0.40:
        return rng.choices(
            [COBBLESTONE, MOSSY_BRICK, CRACKED_STONE],
            weights=[4, 3, 1],
        )[0]
    return rng.choice([COBBLESTONE, COBBLESTONE, MOSSY_BRICK])


def _build_underground_city(world, rng: random.Random, center_x: int,
                             floor_y: int, layout: str, age_factor: float,
                             chest_candidates: list):
    """Carve a flat buried-city layer and fill it with ruins geometry."""
    cfg = _UG_CONFIGS[layout]
    span      = cfg["span"]
    room_h    = cfg["room_h"]
    wall_spc  = cfg["wall_spacing"]

    x_lo   = center_x - span
    x_hi   = center_x + span
    ceil_y = floor_y - room_h   # solid ceiling row

    # Carve interior void
    for x in range(x_lo + 1, x_hi):
        for y in range(ceil_y + 1, floor_y):
            _safe_set(world, x, y, AIR)

    # Solid floor
    for x in range(x_lo, x_hi + 1):
        blk = LIMESTONE_BLOCK if rng.random() < 0.65 else COBBLESTONE
        _safe_set(world, x, floor_y, blk)

    # Ceiling row — partially intact
    for x in range(x_lo, x_hi + 1):
        if rng.random() < 0.10:
            pass  # natural stone pokes through (leave as-is)
        else:
            _safe_set(world, x, ceil_y, _ug_wall_block(rng, age_factor))

    # Solid end walls
    for y in range(ceil_y, floor_y + 1):
        _safe_set(world, x_lo, y, _ug_wall_block(rng, age_factor))
        _safe_set(world, x_hi, y, _ug_wall_block(rng, age_factor))

    # Internal wall remnants at regular intervals
    for x in range(x_lo + wall_spc, x_hi, wall_spc):
        if rng.random() < 0.45:
            # Partial wall — rises from floor, leaves headroom gap
            remnant_h = rng.randint(1, room_h - 1)
            for dy in range(remnant_h):
                _safe_set(world, x, floor_y - dy, _ug_wall_block(rng, age_factor))
        else:
            # Full-height column — requires mining to pass
            for y in range(ceil_y, floor_y + 1):
                if rng.random() < 0.80:   # occasional missing blocks = decay
                    _safe_set(world, x, y, _ug_wall_block(rng, age_factor))

    # Floor debris and rubble
    for x in range(x_lo + 1, x_hi):
        r = rng.random()
        if r < 0.08:
            _safe_set(world, x, floor_y, COBBLESTONE)
        elif r < 0.12:
            _safe_set(world, x, floor_y, CRACKED_STONE)

    # Chest candidates — one per rough third of the span
    step = max(6, span * 2 // 3)
    for cx_pos in range(x_lo + span // 3, x_hi, step):
        chest_candidates.append((cx_pos, floor_y - 1))


def _ug_chest_loot(rng: random.Random, agenda: str, age_years: int) -> dict:
    """Underground chest has the same base loot but a better relic chance."""
    contents = roll_chest_contents(rng, agenda, age_years)
    # Extra relic roll scaled by age
    bonus_chance = min(0.80, 0.20 + age_years * 0.0015)
    if rng.random() < bonus_chance:
        item, lo, hi = rng.choice(_UG_LOOT_RELICS)
        contents[item] = contents.get(item, 0) + rng.randint(lo, hi)
    return contents


def spawn_underground_ruins_for_settlement(world, settlement) -> bool:
    """Carve a buried city layer beneath an old alive settlement.

    Only fires for settlements old enough that a prior city layer could
    plausibly be buried beneath them (age_factor >= 0.20).  Returns True
    if geometry was placed.
    """
    plan = getattr(world, "plan", None)
    if plan is None:
        return False
    if settlement.state != "alive":
        return False

    # Idempotency
    built = getattr(world, "_ug_ruins_built", None)
    if built is None:
        built = set()
        world._ug_ruins_built = built
    if settlement.settlement_id in built:
        return False

    age_years  = plan.history_years - settlement.founded_year
    age_factor = age_years / max(1, plan.history_years)

    if age_factor < 0.20:
        built.add(settlement.settlement_id)
        return False

    base_x = settlement.world_x
    biome  = world.biodome_at(base_x)
    if biome == "ocean":
        built.add(settlement.settlement_id)
        return False

    # Pick layout by age
    if age_factor >= 0.70:
        layout = "large"
    elif age_factor >= 0.40:
        layout = "medium"
    else:
        layout = "small"

    span = _UG_CONFIGS[layout]["span"]

    # Ensure all required chunks are loaded
    chunk_lo = (base_x - span - 2) // 32
    chunk_hi = (base_x + span + 2) // 32
    for cx in range(chunk_lo, chunk_hi + 1):
        if cx not in world._chunks:
            return False   # will retry on next chunk stream

    rng      = random.Random((world.seed ^ (settlement.settlement_id * 0x9A3C71) ^ 0xF12E45) & 0xFFFFFFFF)
    sy       = world.surface_height(base_x)

    # Depth: older = deeper; keeps the ceiling at least 15 blocks underground
    depth    = int(22 + age_factor * 20)   # 22 – 42 blocks below surface
    floor_y  = sy + depth

    if floor_y + 2 >= world.height:
        built.add(settlement.settlement_id)
        return False

    chest_candidates: list = []
    _build_underground_city(world, rng, base_x, floor_y, layout, age_factor, chest_candidates)

    # Place chests with era-appropriate loot
    kingdom = plan.kingdoms.get(settlement.original_kingdom_id)
    agenda  = kingdom.agenda if kingdom else "builder"
    n_chests = {"small": 1, "medium": 2, "large": 3}[layout]
    rng.shuffle(chest_candidates)
    for cx_pos, cy_pos in chest_candidates[:n_chests]:
        if _safe_set(world, cx_pos, cy_pos, CHEST_BLOCK):
            world.chest_data[(cx_pos, cy_pos)] = _ug_chest_loot(rng, agenda, age_years)

    built.add(settlement.settlement_id)
    return True
