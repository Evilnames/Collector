"""Phase 1: build the biome strip.

Produces ``list[BiomeCell]`` with elevation backbone, coastal stretches,
streaky biome assignment via Markov transitions, and decoupled deep-biome
ore variation.
"""

import math
import random

from biomes import BIOMES, BIODOME_TYPES
from worldgen.plan import BiomeCell
from worldgen.config import WORLDGEN_CONFIG


# Elevation bands derived from quantized fBm value (0..1).
_ELEV_BANDS = [
    (0.18, "lowland"),
    (0.45, "hill"),
    (0.78, "highland"),
    (1.01, "peak"),
]

# Biodome candidate pools by elevation band. Pulls from BIODOME_TYPES.
_BAND_POOLS = {
    "lowland":  ["temperate", "wetland", "swamp", "savanna", "steppe", "arid_steppe",
                 "tropical", "jungle", "mediterranean", "south_asian", "east_asian",
                 "desert", "tundra"],
    "hill":     ["temperate", "boreal", "birch_forest", "redwood", "rolling_hills",
                 "mediterranean", "east_asian", "savanna", "steppe", "arid_steppe"],
    "highland": ["boreal", "rolling_hills", "steep_hills", "rocky_mountain",
                 "tundra", "canyon", "wasteland"],
    "peak":     ["alpine_mountain", "rocky_mountain", "tundra", "wasteland"],
}

# Biome-group key for each biodome — used by towns.py name/heraldry pools.
BIODOME_GROUP = {
    "temperate": "forest", "boreal": "forest", "birch_forest": "forest",
    "redwood": "forest", "jungle": "jungle", "tropical": "jungle",
    "wetland": "wetland", "swamp": "wetland",
    "savanna": "plains", "steppe": "plains", "arid_steppe": "plains",
    "wasteland": "wasteland",
    "alpine_mountain": "mountain", "rocky_mountain": "mountain",
    "rolling_hills": "hills", "steep_hills": "hills",
    "desert": "desert", "tundra": "tundra",
    "beach": "coast", "coastal": "coast", "ocean": "coast",
    "pacific_island": "coast", "canyon": "wasteland",
    "mediterranean": "mediterranean", "east_asian": "east_asian",
    "south_asian": "south_asian",
}


def _fbm(seed: int, i: int, octaves: int = 4) -> float:
    """Smooth 1D pseudo-noise in [0,1] for cell index i."""
    rng = random.Random((seed * 7919) ^ 0xA17F)
    phases = [rng.uniform(0, math.tau) for _ in range(octaves)]
    freqs = [0.012, 0.035, 0.09, 0.21]
    amps =  [0.50,  0.28,  0.15, 0.07]
    s = 0.0
    for p, f, a in zip(phases, freqs, amps):
        s += a * (math.sin(i * f + p) * 0.5 + 0.5)
    return max(0.0, min(1.0, s / sum(amps)))


def _terrain_drama(seed: int, i: int) -> float:
    """Slow per-region 'drama' noise in [0.3, 1.0]: low = flat plains, high = dramatic peaks.

    Operates on a much larger wavelength than the elevation backbone so that
    contiguous 30-60 cell stretches feel like one regional 'mood' (e.g. the
    great steppe vs the ridged highlands).
    """
    rng = random.Random((seed * 13103) ^ 0xD8AAA)
    phases = [rng.uniform(0, math.tau) for _ in range(3)]
    freqs = [0.006, 0.014, 0.030]
    amps  = [0.55,  0.30,  0.15]
    s = 0.0
    for p, f, a in zip(phases, freqs, amps):
        s += a * (math.sin(i * f + p) * 0.5 + 0.5)
    raw = s / sum(amps)
    # Push extremes so we get genuinely flat AND genuinely dramatic regions.
    raw = raw * raw if raw < 0.5 else 1.0 - (1.0 - raw) ** 2
    return 0.30 + raw * 0.70


def _band_for(elev: float) -> str:
    for thr, name in _ELEV_BANDS:
        if elev < thr:
            return name
    return "peak"


def _pick_streaky_biodome(prev: str, candidates: list, rng: random.Random) -> str:
    """Bias toward repeating prev or picking a same-group neighbor."""
    if prev in candidates and rng.random() < 0.55:
        return prev
    if prev is not None:
        prev_group = BIODOME_GROUP.get(prev)
        same_group = [c for c in candidates if BIODOME_GROUP.get(c) == prev_group]
        if same_group and rng.random() < 0.45:
            return rng.choice(same_group)
    return rng.choice(candidates)


# Ocean stretch flavors — each tweaks width, island density, and edge style.
# weight: relative pick chance; width_range: cells; island_chance: per inner cell;
# edge: "beach" (sand) or "coastal" (flat shore, no beach band).
OCEAN_TYPES = {
    "standard":    {"weight": 4, "width_range": (15, 35), "island_chance": 0.18, "edge": "beach"},
    "archipelago": {"weight": 2, "width_range": (22, 40), "island_chance": 0.50, "edge": "beach"},
    "deep":        {"weight": 2, "width_range": (28, 48), "island_chance": 0.00, "edge": "beach"},
    "inland_sea":  {"weight": 2, "width_range": ( 8, 14), "island_chance": 0.05, "edge": "coastal"},
    "reef":        {"weight": 1, "width_range": (12, 22), "island_chance": 0.35, "edge": "beach"},
}


def _pick_ocean_type(rng: random.Random) -> str:
    types, weights = zip(*[(k, v["weight"]) for k, v in OCEAN_TYPES.items()])
    return rng.choices(types, weights=weights, k=1)[0]


def _coast_stretches(seed: int, span: int, elevation: list) -> list:
    """Return list of (start, end, ocean_type) cell-index ranges that are oceanic."""
    rng = random.Random(seed ^ 0xC0A57)
    cfg = WORLDGEN_CONFIG
    n_default = cfg["ocean_count_default"]
    n_variance = cfg["ocean_count_variance"]
    n_stretches = n_default + rng.randint(0, max(0, n_variance))

    # Find candidate centers: low-elevation runs.
    low_cells = [i for i, e in enumerate(elevation) if e < 0.30]
    if not low_cells:
        low_cells = list(range(span))

    placed = []
    attempts = 0
    while len(placed) < n_stretches and attempts < 40:
        attempts += 1
        otype = _pick_ocean_type(rng)
        w_low, w_high = OCEAN_TYPES[otype]["width_range"]
        center = rng.choice(low_cells)
        width = rng.randint(w_low, w_high)
        start = max(0, center - width // 2)
        end = min(span, start + width)
        # avoid overlap with existing stretches
        if any(not (end + 8 < s or start - 8 > e) for s, e, _ in placed):
            continue
        placed.append((start, end, otype))
    placed.sort()
    return placed


def _biodome_for_ocean_cell(idx: int, start: int, end: int, otype: str, rng: random.Random) -> str:
    """Inside an ocean stretch: pick ocean / pacific_island / coastal / beach edges."""
    spec = OCEAN_TYPES.get(otype, OCEAN_TYPES["standard"])
    width = end - start
    pos = idx - start
    # Outer edge: beach band for most types, plain coastal for inland seas.
    if pos == 0 or pos == width - 1:
        return spec["edge"]
    # One cell of coastal transition before open water.
    if pos == 1 or pos == width - 2:
        return "coastal"
    # Islands per type density.
    if 2 < pos < width - 2 and rng.random() < spec["island_chance"]:
        return "pacific_island"
    return "ocean"


def _pick_deep_biome(surface: str, rng: random.Random) -> str:
    """Deep biome: 60% concordance with a sensible surface mapping, else random."""
    surface_to_biome = {
        "alpine_mountain": "igneous",
        "rocky_mountain": "igneous",
        "canyon": "sedimentary",
        "desert": "sedimentary",
        "wasteland": "void",
        "tundra": "ferrous",
        "redwood": "crystal",
        "boreal": "crystal",
    }
    pref = surface_to_biome.get(surface)
    if pref and rng.random() < 0.60:
        return pref
    return rng.choice(BIOMES)


def build_geography(seed: int, span: int) -> list:
    """Return list[BiomeCell] of length span."""
    cell_w = WORLDGEN_CONFIG["cell_block_width"]
    world_min_x = -(span * cell_w) // 2

    # Step 1 — elevation backbone.
    elevation = [_fbm(seed + 1, i) for i in range(span)]

    # Step 2 — coastal stretches override biodome for those cells.
    stretches = _coast_stretches(seed, span, elevation)
    coast_map = {}
    for s, e, otype in stretches:
        for i in range(s, e):
            coast_map[i] = (s, e, otype)

    # Step 3 — biodome assignment with streaking.
    cells = []
    prev_biodome = None
    for i in range(span):
        cell_seed = (seed * 1009 + i * 9176_531) & 0x7FFFFFFF
        rng = random.Random(cell_seed)
        elev = elevation[i]
        band = _band_for(elev)

        if i in coast_map:
            s, e, otype = coast_map[i]
            biodome = _biodome_for_ocean_cell(i, s, e, otype, rng)
            coastal = True
        else:
            pool = _BAND_POOLS[band]
            biodome = _pick_streaky_biodome(prev_biodome, pool, rng)
            coastal = False

        biome = _pick_deep_biome(biodome, rng)
        world_x = world_min_x + i * cell_w + cell_w // 2
        drama = _terrain_drama(seed, i)
        cells.append(BiomeCell(
            index=i,
            world_x=world_x,
            biome=biome,
            biodome=biodome,
            elevation_band=band,
            elevation=elev,
            coastal=coastal,
            seed=cell_seed,
            drama=drama,
        ))
        prev_biodome = biodome

    return cells
