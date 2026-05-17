"""Phase 1: build the biome strip.

Produces ``list[BiomeCell]`` with elevation backbone, coastal stretches,
streaky biome assignment via Markov transitions, and decoupled deep-biome
ore variation.
"""

import math
import random

from biomes import BIOMES, BIODOME_TYPES, BIODOME_TERRAIN_MODS
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
                 "mediterranean", "east_asian", "savanna", "steppe", "arid_steppe",
                 "red_rock"],
    "highland": ["boreal", "rolling_hills", "steep_hills", "rocky_mountain",
                 "tundra", "canyon", "wasteland", "red_rock"],
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
    "desert": "desert", "tundra": "tundra", "red_rock": "desert",
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


def _weathering(seed: int, i: int) -> float:
    """Slow regional noise in [0.35, 1.55]: <1 = young/jagged, >1 = old/eroded.

    Wavelength sits between drama and the elevation backbone, so contiguous
    20-50 cell stretches share a 'geologic age': fresh peaks vs worn-down
    ancient ranges. Feeds the erosion pass strength.
    """
    rng = random.Random((seed * 5471) ^ 0xE03B7)
    phases = [rng.uniform(0, math.tau) for _ in range(3)]
    freqs = [0.008, 0.022, 0.05]
    amps  = [0.50,  0.30, 0.20]
    s = 0.0
    for p, f, a in zip(phases, freqs, amps):
        s += a * (math.sin(i * f + p) * 0.5 + 0.5)
    raw = s / sum(amps)
    return 0.35 + raw * 1.20


# Per-cell anomaly catalog. Applied AFTER erosion so the feature survives the
# smoothing pass. offset = override of predicted_y_offset; erosion = override
# of the erosion factor (lower = sharper detail noise on top).
_ANOMALY_TYPES = {
    "mesa":     {"offset": -9.0, "erosion": 0.20, "weight": 3, "where": "land"},
    "plateau":  {"offset": -5.5, "erosion": 0.30, "weight": 4, "where": "land"},
    "spike":    {"offset": -16.0, "erosion": 1.10, "weight": 2, "where": "land"},
    "sinkhole": {"offset":  10.0, "erosion": 0.50, "weight": 2, "where": "land"},
    "trench":   {"offset":  12.0, "erosion": 0.20, "weight": 4, "where": "ocean"},
}
_LAND_ANOMALY_CHANCE = 0.045   # per non-coastal land cell
_OCEAN_ANOMALY_CHANCE = 0.10   # per interior ocean cell

# Per-biodome overrides — high-anomaly biomes get a much greater chance and
# can restrict the pool to a thematic subset.
_BIODOME_ANOMALY = {
    # Sedona / Arizona-style mesa country: most cells are flat-topped buttes
    # or terraced plateaus. Few non-mesa anomalies break it up.
    "red_rock": {"chance": 0.55, "pool": ["mesa", "plateau", "mesa", "spike"]},
}


def _pick_anomaly(rng: random.Random, where: str) -> str:
    pool = [(k, v["weight"]) for k, v in _ANOMALY_TYPES.items() if v["where"] == where]
    if not pool:
        return ""
    names, weights = zip(*pool)
    return rng.choices(names, weights=weights, k=1)[0]


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
    "standard":    {"weight": 4, "width_range": (15, 35), "island_chance": 0.18, "edge": "beach",
                    "depth_range": (16, 26)},
    "archipelago": {"weight": 2, "width_range": (22, 40), "island_chance": 0.50, "edge": "beach",
                    "depth_range": (10, 20)},
    "deep":        {"weight": 2, "width_range": (28, 48), "island_chance": 0.00, "edge": "beach",
                    "depth_range": (24, 36)},
    "inland_sea":  {"weight": 2, "width_range": ( 8, 14), "island_chance": 0.05, "edge": "coastal",
                    "depth_range": (10, 16)},
    "reef":        {"weight": 1, "width_range": (12, 22), "island_chance": 0.35, "edge": "beach",
                    "depth_range": (12, 20)},
}


def _ocean_depth_offset(idx: int, start: int, end: int, otype: str,
                        rng: random.Random) -> float:
    """Per-cell ocean basin depth — shallow at edges, deeper toward the middle.

    Picks a depth between the otype's (min, max) by smoothstepping the cell's
    distance from the stretch edge, then adds a small per-cell jitter.
    """
    spec = OCEAN_TYPES.get(otype, OCEAN_TYPES["standard"])
    d_min, d_max = spec["depth_range"]
    width = max(1, end - start)
    pos = idx - start
    edge_dist = min(pos, width - 1 - pos) / max(1.0, width / 2.0)
    edge_dist = max(0.0, min(1.0, edge_dist))
    smooth = edge_dist * edge_dist * (3 - 2 * edge_dist)
    depth = d_min + (d_max - d_min) * smooth
    return depth + rng.uniform(-1.5, 1.5)


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


def _predicted_offset(biodome: str, drama: float) -> float:
    """Mean surface offset from SURFACE_Y for a cell.

    Positive = below sea level (ocean basin); negative = above (mountains).
    Mirrors the formula the game uses for the un-noised baseline, including
    drama amplification of negative bias so dramatic regions tower higher.
    """
    bias, _scale = BIODOME_TERRAIN_MODS.get(biodome, (0.0, 1.0))
    if bias < 0:
        bias *= (0.5 + drama * 0.8)
    return float(bias)


def _erode(offsets: list, weathering: list, passes: int = 4) -> tuple:
    """Smooth per-cell baseline offsets toward neighbor averages.

    Each pass pulls every cell a little toward a weighted neighborhood mean.
    Cells whose original height diverges sharply from neighbors get tugged
    harder and accumulate a smaller erosion factor — the game uses that
    factor to dampen noise amplitude there, producing flatter slopes around
    sharp biome transitions.

    Per-cell weathering scales the pull strength: young/jagged regions (<1)
    keep their sharp profile, old/eroded regions (>1) get smoothed harder.
    """
    h = list(offsets)
    n = len(h)
    erosion = [1.0] * n
    if n == 0:
        return h, erosion
    for _ in range(passes):
        new_h = list(h)
        for i in range(n):
            l = h[i - 1] if i > 0 else h[i]
            r = h[i + 1] if i + 1 < n else h[i]
            avg = (l + h[i] * 2 + r) / 4.0
            diff = abs(h[i] - avg)
            t = min(0.65, diff * 0.05 * weathering[i])
            new_h[i] = h[i] * (1 - t) + avg * t
            erosion[i] *= (1.0 - t * 0.35)
        h = new_h
    return h, erosion


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
    raw_offsets = []
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
        weathering = _weathering(seed, i)

        # Ocean cells get a position-based depth profile instead of the flat
        # biodome bias, so a stretch reads as shelf → basin → shelf.
        if biodome == "ocean" and i in coast_map:
            s, e, otype = coast_map[i]
            base_off = _ocean_depth_offset(i, s, e, otype, rng)
        else:
            base_off = _predicted_offset(biodome, drama)

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
            weathering=weathering,
        ))
        raw_offsets.append(base_off)
        prev_biodome = biodome

    # Step 4 — erosion pass. Smooth the baseline offsets toward neighbor
    # means; weathering controls how hard each cell gets tugged.
    weather_list = [c.weathering for c in cells]
    eroded, erosion = _erode(raw_offsets, weather_list, passes=4)

    # Step 5 — anomaly overrides. Rare per-cell features (mesas, spikes,
    # sinkholes, trenches) that survive the erosion pass with their own
    # offset + erosion values. Coastal/beach cells stay untouched so shores
    # don't sprout cliffs mid-transition.
    for i, c in enumerate(cells):
        c.predicted_y_offset = eroded[i]
        c.erosion = erosion[i]

        if c.biodome in ("beach", "coastal", "pacific_island"):
            continue
        anom_rng = random.Random(c.seed ^ 0xA105E)
        if c.biodome == "ocean":
            if anom_rng.random() < _OCEAN_ANOMALY_CHANCE:
                # Skip trenches at the very edges of a stretch.
                cm = coast_map.get(i)
                if cm and 2 <= (i - cm[0]) < (cm[1] - cm[0]) - 2:
                    name = _pick_anomaly(anom_rng, "ocean")
                    spec = _ANOMALY_TYPES[name]
                    c.anomaly = name
                    c.predicted_y_offset = c.predicted_y_offset + spec["offset"] * 0.5
                    c.erosion = spec["erosion"]
        else:
            override = _BIODOME_ANOMALY.get(c.biodome)
            chance = override["chance"] if override else _LAND_ANOMALY_CHANCE
            if anom_rng.random() < chance:
                if override:
                    name = anom_rng.choice(override["pool"])
                else:
                    name = _pick_anomaly(anom_rng, "land")
                spec = _ANOMALY_TYPES[name]
                c.anomaly = name
                c.predicted_y_offset = spec["offset"]
                c.erosion = spec["erosion"]

    return cells
