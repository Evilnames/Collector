"""Phase 2: seed starting kingdoms at attractive sites.

Picks K capitals on attractive cells, clusters neighbors into territories,
generates kingdom identity (name, heraldry, leader, agenda, founding dynasty),
and lays out 1-5 settlement seeds per kingdom.
"""

import random
from dataclasses import asdict

import heraldry
import towns as _towns
from worldgen.config import WORLDGEN_CONFIG
from worldgen.geography import BIODOME_GROUP
from worldgen.plan import Kingdom, Settlement, Person, Dynasty


# ---------------------------------------------------------------------------
# Cell scoring
# ---------------------------------------------------------------------------

# Attractive surface biodomes get a base bonus.
_BIODOME_ATTRACTIVENESS = {
    "temperate": 1.0, "mediterranean": 1.0, "rolling_hills": 0.9,
    "savanna": 0.8, "wetland": 0.7, "south_asian": 0.9, "east_asian": 0.9,
    "boreal": 0.6, "birch_forest": 0.7, "redwood": 0.6, "jungle": 0.5,
    "tropical": 0.6, "steppe": 0.5, "arid_steppe": 0.4, "swamp": 0.3,
    "desert": 0.3, "tundra": 0.2, "wasteland": 0.1, "canyon": 0.2,
    "rocky_mountain": 0.2, "alpine_mountain": 0.1, "steep_hills": 0.5,
    "beach": 0.7, "coastal": 0.8, "ocean": 0.0, "pacific_island": 0.4,
}

# Ore-rich deep biomes give a small bonus (good for cities).
_BIOME_BONUS = {
    "ferrous": 0.2, "sedimentary": 0.15, "crystal": 0.1,
    "igneous": 0.05, "void": 0.0,
}


def _score_cell(cell, neighbors_coast: bool) -> float:
    base = _BIODOME_ATTRACTIVENESS.get(cell.biodome, 0.3)
    base += _BIOME_BONUS.get(cell.biome, 0.0)
    if neighbors_coast:
        base += 0.25
    # Penalize peaks and pure ocean.
    if cell.biodome in ("ocean", "alpine_mountain"):
        return 0.0
    return base


def _score_all(cells: list) -> list:
    """Return per-cell attractiveness including coast-adjacency bonus."""
    n = len(cells)
    coast_flag = [c.biodome in ("coastal", "beach") for c in cells]
    scores = []
    for i, c in enumerate(cells):
        near_coast = any(coast_flag[max(0, i - 2): min(n, i + 3)])
        scores.append(_score_cell(c, near_coast))
    return scores


# ---------------------------------------------------------------------------
# Capital selection
# ---------------------------------------------------------------------------

def _pick_capitals(cells: list, scores: list, k: int, seed: int,
                   min_separation: int = 36) -> list:
    """Greedy: pick top-scoring cells with minimum separation between them."""
    rng = random.Random(seed ^ 0xCAFE)
    candidates = sorted(range(len(cells)),
                        key=lambda i: (scores[i] + rng.random() * 0.05),
                        reverse=True)
    chosen = []
    for idx in candidates:
        if scores[idx] <= 0.1:
            continue
        if all(abs(idx - j) >= min_separation for j in chosen):
            chosen.append(idx)
            if len(chosen) >= k:
                break
    chosen.sort()
    return chosen


# ---------------------------------------------------------------------------
# Identity helpers (name, heraldry, dynasty)
# ---------------------------------------------------------------------------

def _kingdom_biome_group(cell) -> str:
    """Match towns.py grouping (different from BIODOME_GROUP in geography)."""
    return _towns._BIOME_GROUP.get(cell.biodome, _towns._DEFAULT_BIOME_GROUP)


def _gen_kingdom_name(group: str, used: set, rng: random.Random) -> str:
    pool = _towns._REGION_NAMES_BY_GROUP.get(group) or _towns._REGION_NAMES_BY_GROUP["highland"]
    options = [n for n in pool if n not in used]
    pool = options if options else pool
    return rng.choice(pool)


def _gen_settlement_name(rng: random.Random, used: set) -> str:
    for _ in range(20):
        name = rng.choice(_towns._PREFIXES) + rng.choice(_towns._SUFFIXES)
        if name not in used:
            return name
    return name


def _gen_heraldry(group: str, rng: random.Random):
    primary = rng.choice(heraldry._COLORS)
    charge_pool = _towns._CHARGES_BY_GROUP.get(group, heraldry._CHARGES)
    coa = heraldry.generate(rng, primary, charge_pool)
    return coa


def _gen_dynasty(seed: int, kingdom_id: int, founded_year: int,
                 next_person_id: list, next_dynasty_id: list) -> Dynasty:
    rng = random.Random(seed ^ (0xD1A5A * (kingdom_id + 1)))
    syll_a = ["Vor", "Kal", "Mar", "Drav", "Ash", "Bel", "Cor", "Tyr",
              "Sel", "Nov", "Ulm", "Ren", "Far", "Hesh", "Jor", "Kael",
              "Lan", "Mor", "Pyr", "Sar", "Tav", "Veld", "Win", "Yor"]
    syll_b = ["mont", "vain", "thys", "renn", "kar", "shar", "lin",
              "veil", "drak", "fall", "stride", "gren", "wyn", "thorn"]
    house = "House " + rng.choice(syll_a) + rng.choice(syll_b)
    dynasty_id = next_dynasty_id[0]; next_dynasty_id[0] += 1
    pid = next_person_id[0]; next_person_id[0] += 1
    founder = Person(
        person_id=pid,
        dynasty_id=dynasty_id,
        name=rng.choice(syll_a) + rng.choice(syll_b).rstrip("nrs"),
        born_year=founded_year - rng.randint(20, 45),
        role="founder",
        epithet=rng.choice(["the Bold", "the Wise", "the Founder", "the First",
                            "the Steel-Handed", "the Fair", "the Resolute",
                            "the Sea-Borne", "the Hill-Born", "the Wanderer"]),
    )
    return Dynasty(
        dynasty_id=dynasty_id,
        house_name=house,
        founder_id=founder.person_id,
        head_id=founder.person_id,
        members={founder.person_id: founder},
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def seed_kingdoms(cells: list, seed: int, founded_year: int = 0):
    """Build starting kingdoms + settlements + dynasties.

    Returns (kingdoms_dict, settlements_dict, dynasties_dict, next_ids_tuple).
    """
    cfg = WORLDGEN_CONFIG
    span = len(cells)
    k = max(2, round(span * cfg["starting_kingdoms_per_100_cells"] / 100))

    scores = _score_all(cells)
    capital_indices = _pick_capitals(cells, scores, k, seed)

    # Territory borders: midpoint between adjacent capitals (clipped to span ends).
    territories = []
    for i, cap_idx in enumerate(capital_indices):
        lo = (capital_indices[i - 1] + cap_idx) // 2 if i > 0 else 0
        hi = (cap_idx + capital_indices[i + 1]) // 2 if i + 1 < len(capital_indices) else span
        territories.append((lo, hi))

    rng = random.Random(seed ^ 0x1FAB)
    next_person_id = [0]
    next_dynasty_id = [0]
    next_settlement_id = [0]

    kingdoms = {}
    settlements = {}
    dynasties = {}
    used_kingdom_names = set()
    used_settlement_names = set()
    s_min, s_max = cfg["settlements_per_kingdom_range"]
    SETTLEMENT_MIN_SEP = cfg.get("settlement_min_separation_cells", 14)

    for kid, cap_idx in enumerate(capital_indices):
        cap_cell = cells[cap_idx]
        group = _kingdom_biome_group(cap_cell)
        kname = _gen_kingdom_name(group, used_kingdom_names, rng)
        used_kingdom_names.add(kname)
        coa = _gen_heraldry(group, rng)
        leader_title = _towns._LEADER_TITLES.get(group, ("Lord", "Lady"))
        agenda = rng.choice(list(_towns.LEADER_AGENDAS.keys()))
        dyn = _gen_dynasty(seed, kid, founded_year, next_person_id, next_dynasty_id)
        dynasties[dyn.dynasty_id] = dyn

        # Spread settlements across the kingdom's full territory (not packed
        # near the capital). Min-separation keeps lots of buildable land
        # between every pair so the player can lay claim in between.
        terr_lo, terr_hi = territories[kid]
        n_settlements = rng.randint(s_min, s_max)
        candidates = sorted(
            [j for j in range(terr_lo, terr_hi)
             if j != cap_idx and scores[j] > 0.25
             and not _cell_already_claimed(j, settlements, cells)],
            key=lambda j: -scores[j],
        )
        chosen_cells = [cap_idx]
        for j in candidates:
            if len(chosen_cells) >= n_settlements:
                break
            if all(abs(j - c) >= SETTLEMENT_MIN_SEP for c in chosen_cells):
                chosen_cells.append(j)

        member_ids = []
        capital_sid = None
        for slot, cidx in enumerate(chosen_cells):
            cell = cells[cidx]
            sid = next_settlement_id[0]; next_settlement_id[0] += 1
            sname = _gen_settlement_name(rng, used_settlement_names)
            used_settlement_names.add(sname)
            is_cap = (slot == 0)
            jitter = rng.randint(-cfg["cell_block_width"] // 4, cfg["cell_block_width"] // 4)
            tier = "village" if is_cap else "hamlet"
            settlements[sid] = Settlement(
                settlement_id=sid,
                kingdom_id=kid,
                original_kingdom_id=kid,
                name=sname,
                cell_index=cidx,
                world_x=cell.world_x + jitter,
                tier=tier,
                founded_year=founded_year,
                is_capital=is_cap,
                dynasty_id=dyn.dynasty_id,
                state="alive",
            )
            member_ids.append(sid)
            if is_cap:
                capital_sid = sid

        kingdoms[kid] = Kingdom(
            kingdom_id=kid,
            name=kname,
            biome_group=group,
            capital_settlement_id=capital_sid,
            member_settlement_ids=member_ids,
            dynasty_id=dyn.dynasty_id,
            leader_title=leader_title,
            agenda=agenda,
            heraldry=_coa_to_dict(coa),
            color=coa.primary,
            founded_year=founded_year,
            territory_lo=terr_lo,
            territory_hi=terr_hi,
        )

    # Initial neutral relations between all kingdom pairs.
    for kid in kingdoms:
        for other in kingdoms:
            if other == kid:
                continue
            kingdoms[kid].relations[other] = "neutral"

    next_ids = (next_person_id[0], next_dynasty_id[0], next_settlement_id[0])
    return kingdoms, settlements, dynasties, next_ids


def _cell_already_claimed(cell_idx: int, settlements: dict, cells: list) -> bool:
    return any(s.cell_index == cell_idx for s in settlements.values())


def _coa_to_dict(coa) -> dict:
    return {
        "primary":   list(coa.primary),
        "secondary": list(coa.secondary),
        "metal":     list(coa.metal),
        "division":  coa.division,
        "ordinary":  coa.ordinary,
        "charge":    coa.charge,
        "motto":     coa.motto,
    }


def coa_from_dict(d: dict):
    return heraldry.CoatOfArms(
        primary   = tuple(d["primary"]),
        secondary = tuple(d["secondary"]),
        metal     = tuple(d["metal"]),
        division  = d["division"],
        ordinary  = d["ordinary"],
        charge    = d["charge"],
        motto     = d["motto"],
    )
