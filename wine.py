import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class Grape:
    uid: str
    origin_biome: str        # biodome where cluster was harvested ("blend" for blended)
    variety: str             # e.g. "cabernet_sauvignon", "chardonnay", "blend"
    state: str               # "raw" | "crushed" | "fermented" | "aged" | "blended"
    style: str               # "" | "red" | "white" | "rose" | "sparkling" | "dessert"
    sweetness: float
    acidity: float
    tannin: float
    body: float
    aromatics: float
    alcohol: float           # 0.0–1.0 (set by fermentation)
    complexity: float        # 0.0–1.0 (ferment + aging)
    press_quality: float     # 0.0–1.0 (crush mini-game)
    ferment_quality: float   # 0.0–1.0 (ferment mini-game)
    flavor_notes: list
    seed: int
    blend_components: list = field(default_factory=list)
    crush_style: str = ""    # "whole_cluster" | "destemmed" | "rose_bleed" | "skin_fermented"
    yeast: str = ""          # "wild" | "champagne" | "bordeaux" | "burgundy"
    vessel: str = ""         # "oak" | "steel" | "amphora"


# Base grape profiles per biome. Same biome keys as coffee.
BIOME_GRAPE_PROFILES = {
    "tropical":        {"sweetness": 0.80, "acidity": 0.80, "tannin": 0.20, "body": 0.40, "aromatics": 0.85, "variety": "sauvignon_blanc"},
    "jungle":          {"sweetness": 0.55, "acidity": 0.50, "tannin": 0.75, "body": 0.80, "aromatics": 0.60, "variety": "syrah"},
    "savanna":         {"sweetness": 0.45, "acidity": 0.55, "tannin": 0.65, "body": 0.75, "aromatics": 0.50, "variety": "tempranillo"},
    "wetland":         {"sweetness": 0.50, "acidity": 0.70, "tannin": 0.45, "body": 0.55, "aromatics": 0.80, "variety": "pinot_noir"},
    "arid_steppe":     {"sweetness": 0.60, "acidity": 0.55, "tannin": 0.70, "body": 0.70, "aromatics": 0.55, "variety": "grenache"},
    "canyon":          {"sweetness": 0.40, "acidity": 0.60, "tannin": 0.90, "body": 0.90, "aromatics": 0.45, "variety": "cabernet_sauvignon"},
    "beach":           {"sweetness": 0.85, "acidity": 0.85, "tannin": 0.15, "body": 0.35, "aromatics": 0.90, "variety": "riesling"},
    "tundra":          {"sweetness": 0.65, "acidity": 0.90, "tannin": 0.25, "body": 0.40, "aromatics": 0.75, "variety": "pinot_gris"},
    "swamp":           {"sweetness": 0.45, "acidity": 0.50, "tannin": 0.80, "body": 0.85, "aromatics": 0.55, "variety": "malbec"},
    "alpine_mountain": {"sweetness": 0.70, "acidity": 0.80, "tannin": 0.20, "body": 0.55, "aromatics": 0.80, "variety": "chardonnay"},
    "rocky_mountain":  {"sweetness": 0.45, "acidity": 0.75, "tannin": 0.85, "body": 0.85, "aromatics": 0.65, "variety": "nebbiolo"},
    "rolling_hills":   {"sweetness": 0.60, "acidity": 0.60, "tannin": 0.60, "body": 0.65, "aromatics": 0.65, "variety": "merlot"},
}

_FLAVOR_POOLS = {
    "sweetness":  ["ripe cherry", "honey", "fig", "candied plum", "vanilla", "brown sugar"],
    "acidity":    ["citrus zest", "green apple", "white peach", "lime pith", "cranberry", "verjuice"],
    "tannin":     ["leather", "graphite", "dark chocolate", "cedar shavings", "walnut skin", "dried tea"],
    "body":       ["blackberry jam", "cocoa", "espresso", "plum compote", "stewed fruit", "smoke"],
    "aromatics":  ["violet", "rose petal", "elderflower", "jasmine", "lavender", "orange blossom"],
}

_CRUSH_NOTES = {
    "whole_cluster":   ["stem spice", "herbal lift", "crushed leaf"],
    "destemmed":       ["clean fruit", "polished core"],
    "rose_bleed":      ["strawberry", "watermelon rind", "pink grapefruit"],
    "skin_fermented":  ["orange peel", "amber tea", "nutskin", "wax"],
}

_YEAST_NOTES = {
    "wild":       ["barnyard", "funk", "bruised apple", "wet stone"],
    "champagne":  ["brioche", "yeasty lees", "crisp finish"],
    "bordeaux":   ["cassis", "pencil shavings", "dark plum"],
    "burgundy":   ["forest floor", "dried violets", "dark cherry"],
}

_VESSEL_NOTES = {
    "oak":     ["toast", "coconut", "baking spice", "cedar"],
    "steel":   ["clean", "steely", "mineral"],
    "amphora": ["clay", "earth", "dried herb", "honey dust"],
}

WINE_STYLE_DESCS = {
    "red":       "Red Wine — tannic, full, dark fruit",
    "white":     "White Wine — crisp, bright, floral",
    "rose":      "Rosé — light, berry-forward, summer",
    "sparkling": "Sparkling — bubbles, bright, celebratory",
    "dessert":   "Dessert Wine — rich, sweet, concentrated",
}

WINE_STYLE_COLORS = {
    "red":       (120,  30,  40),
    "white":     (220, 210, 160),
    "rose":      (225, 145, 155),
    "sparkling": (240, 225, 180),
    "dessert":   (160,  95,  30),
}

CRUSH_STYLES = {
    "whole_cluster": {
        "label": "Whole Cluster",
        "desc":  "Stems in. Boosts tannin and earthy complexity.",
        "sweetness": -0.05, "acidity": +0.05, "tannin": +0.18, "body": +0.08, "aromatics": -0.05,
        "style_bias": "red",
    },
    "destemmed": {
        "label": "Destemmed",
        "desc":  "Classic. Balanced fruit, polished profile.",
        "sweetness": +0.00, "acidity": +0.00, "tannin": +0.05, "body": +0.03, "aromatics": +0.02,
        "style_bias": "red",
    },
    "rose_bleed": {
        "label": "Rosé Bleed",
        "desc":  "Brief skin contact. Light body, bright fruit.",
        "sweetness": +0.08, "acidity": +0.10, "tannin": -0.20, "body": -0.20, "aromatics": +0.12,
        "style_bias": "rose",
    },
    "skin_fermented": {
        "label": "Skin Fermented",
        "desc":  "Long skin contact on white grapes. Amber, textured.",
        "sweetness": -0.05, "acidity": -0.05, "tannin": +0.15, "body": +0.12, "aromatics": +0.05,
        "style_bias": "white",
    },
}

YEASTS = {
    "wild": {
        "label": "Wild",
        "desc":  "Native yeast. Unpredictable, extra complexity, lower alcohol.",
        "alcohol_delta": -0.08, "complexity_delta": +0.12, "body": +0.03,
    },
    "champagne": {
        "label": "Champagne",
        "desc":  "Bright, clean. High alcohol tolerance. Biased to sparkling.",
        "alcohol_delta": +0.08, "complexity_delta": +0.02, "acidity": +0.05, "style_bias": "sparkling",
    },
    "bordeaux": {
        "label": "Bordeaux",
        "desc":  "Structured. Builds body and tannin. Classic reds.",
        "alcohol_delta": +0.05, "complexity_delta": +0.05, "body": +0.06, "tannin": +0.04, "style_bias": "red",
    },
    "burgundy": {
        "label": "Burgundy",
        "desc":  "Elegant. Aromatic lift, moderate body.",
        "alcohol_delta": +0.02, "complexity_delta": +0.08, "aromatics": +0.08, "style_bias": "red",
    },
}

VESSELS = {
    "oak": {
        "label": "Oak Barrel",
        "desc":  "Adds body, spice, and complexity. Softens brightness.",
        "body": +0.12, "complexity_delta": +0.12, "aromatics": -0.05, "quality_mult": 1.08,
    },
    "steel": {
        "label": "Steel Tank",
        "desc":  "Preserves ferment profile. Keeps it bright.",
        "body": -0.05, "aromatics": +0.06, "complexity_delta": +0.02, "quality_mult": 1.00,
    },
    "amphora": {
        "label": "Clay Amphora",
        "desc":  "Earth and minerality. Gentle oxidation adds complexity.",
        "body": +0.05, "tannin": +0.04, "complexity_delta": +0.08, "quality_mult": 1.05,
    },
}

AGE_DURATIONS = {
    "short":  {"label": "Short (6mo)",   "quality_mult": 1.00, "complexity_delta": 0.05},
    "medium": {"label": "Medium (2yr)",  "quality_mult": 1.05, "complexity_delta": 0.10},
    "long":   {"label": "Long (5yr)",    "quality_mult": 1.10, "complexity_delta": 0.18},
}

SERVING_METHODS = {
    "goblet":     {"label": "Goblet",      "style": "red",       "buff": "warmth",        "glass_mult": 1.00},
    "white_flute":{"label": "White Glass", "style": "white",     "buff": "serenity",      "glass_mult": 1.00},
    "rose_glass": {"label": "Rosé Glass",  "style": "rose",      "buff": "charm",         "glass_mult": 1.00},
    "flute":      {"label": "Flute",       "style": "sparkling", "buff": "vivacity",      "glass_mult": 1.00},
    "cordial":    {"label": "Cordial",     "style": "dessert",   "buff": "contemplation", "glass_mult": 1.00},
}

SERVING_TEMPS = {
    "chilled": {"label": "Chilled",     "duration_mult": 1.15, "quality_bonus": 0.05},
    "cellar":  {"label": "Cellar Temp", "duration_mult": 1.00, "quality_bonus": 0.10},
    "room":    {"label": "Room Temp",   "duration_mult": 0.90, "quality_bonus": 0.02},
}

BUFF_DESCS = {
    "warmth":        "Cold damage -50%",
    "serenity":      "Hunger drain -60%",
    "charm":         "Collect radius +75%",
    "vivacity":      "Jump +1 / No fall damage",
    "contemplation": "Discovery XP +25%",
}

BIOME_DISPLAY_NAMES = {
    "tropical":        "Tropical",
    "jungle":          "Jungle",
    "savanna":         "Savanna",
    "wetland":         "Wetland",
    "arid_steppe":     "Arid Steppe",
    "canyon":          "Canyon",
    "beach":           "Beach",
    "tundra":          "Tundra",
    "swamp":           "Swamp",
    "alpine_mountain": "Alpine",
    "rocky_mountain":  "Rocky Mtn",
    "rolling_hills":   "Rolling Hills",
    "blend":           "Blend",
}

VARIETY_DISPLAY_NAMES = {
    "sauvignon_blanc":    "Sauvignon Blanc",
    "syrah":              "Syrah",
    "tempranillo":        "Tempranillo",
    "pinot_noir":         "Pinot Noir",
    "grenache":           "Grenache",
    "cabernet_sauvignon": "Cabernet",
    "riesling":           "Riesling",
    "pinot_gris":         "Pinot Gris",
    "malbec":             "Malbec",
    "chardonnay":         "Chardonnay",
    "nebbiolo":           "Nebbiolo",
    "merlot":             "Merlot",
    "blend":              "Blend",
}

_CODEX_BIOMES = list(BIOME_GRAPE_PROFILES.keys())
WINE_STYLE_ORDER = ["red", "white", "rose", "sparkling", "dessert"]
WINE_TYPE_ORDER = [f"{biome}_{style}" for biome in _CODEX_BIOMES for style in WINE_STYLE_ORDER]


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def apply_crush_style(grape: "Grape", style_key: str):
    mods = CRUSH_STYLES.get(style_key)
    if not mods:
        return
    grape.crush_style = style_key
    for attr in ("sweetness", "acidity", "tannin", "body", "aromatics"):
        setattr(grape, attr, _clamp(getattr(grape, attr) + mods.get(attr, 0.0)))


def apply_press_result(grape: "Grape", avg_pressure: float,
                       time_in_green: float, time_in_yellow: float,
                       total_time: float, over_press_penalty: int):
    if total_time <= 0:
        total_time = 0.1
    green_frac  = time_in_green / total_time
    yellow_frac = time_in_yellow / total_time
    quality = _clamp(green_frac * 0.8 + yellow_frac * 0.3 - over_press_penalty * 0.15)
    # Yellow band adds tannin but reduces softness
    grape.tannin = _clamp(grape.tannin + yellow_frac * 0.15)
    grape.body   = _clamp(grape.body   + yellow_frac * 0.08)
    grape.press_quality = quality
    grape.state = "crushed"


def apply_yeast(grape: "Grape", yeast_key: str):
    mods = YEASTS.get(yeast_key)
    if not mods:
        return
    grape.yeast = yeast_key
    for attr in ("sweetness", "acidity", "tannin", "body", "aromatics"):
        if attr in mods:
            setattr(grape, attr, _clamp(getattr(grape, attr) + mods[attr]))


def determine_style(grape: "Grape", stop_time: float, total_time: float) -> str:
    """Decide red/white/rose/sparkling/dessert from crush + yeast + stop timing."""
    crush_bias = CRUSH_STYLES.get(grape.crush_style, {}).get("style_bias", "red")
    yeast_bias = YEASTS.get(grape.yeast, {}).get("style_bias")
    frac = stop_time / max(0.1, total_time)
    if yeast_bias == "sparkling":
        return "sparkling"
    if frac < 0.25:
        return "dessert"
    if crush_bias == "rose":
        return "rose"
    if crush_bias == "white":
        return "white"
    # For white-biased grape varieties with destemmed crush, prefer white
    white_varieties = {"sauvignon_blanc", "riesling", "chardonnay", "pinot_gris"}
    if grape.variety in white_varieties and crush_bias == "red":
        return "white"
    return "red"


def apply_ferment_result(grape: "Grape",
                         temp_band_frac: float, nutrient_band_frac: float,
                         punchdown_hit_frac: float, stop_frac: float,
                         penalties: int,
                         stop_time: float, total_time: float):
    # Alcohol climbs with stop time; yeast delta shifts it.
    base_alcohol = _clamp(0.35 + stop_frac * 0.55)
    alcohol_delta = YEASTS.get(grape.yeast, {}).get("alcohol_delta", 0.0)
    grape.alcohol = _clamp(base_alcohol + alcohol_delta)
    # Dryness inverse of stop time: stop early = sweet retained, stop late = dry.
    grape.sweetness = _clamp(grape.sweetness * (1.15 - stop_frac * 0.8))
    # Complexity from yeast + quality.
    comp_delta = YEASTS.get(grape.yeast, {}).get("complexity_delta", 0.0)
    grape.complexity = _clamp(0.25 + comp_delta + punchdown_hit_frac * 0.20)
    # Composite ferment quality.
    quality = _clamp(
        temp_band_frac * 0.35
        + nutrient_band_frac * 0.25
        + punchdown_hit_frac * 0.25
        + min(1.0, stop_frac * 1.1) * 0.15
        - penalties * 0.10
    )
    grape.ferment_quality = quality
    grape.state = "fermented"
    grape.style = determine_style(grape, stop_time, total_time)
    grape.flavor_notes = generate_flavor_notes(grape)


def apply_aging(grape: "Grape", vessel_key: str, duration_key: str):
    vmods = VESSELS.get(vessel_key)
    dmods = AGE_DURATIONS.get(duration_key)
    if not vmods or not dmods:
        return
    grape.vessel = vessel_key
    scale = {"short": 0.5, "medium": 1.0, "long": 1.5}.get(duration_key, 1.0)
    for attr in ("sweetness", "acidity", "tannin", "body", "aromatics"):
        if attr in vmods:
            setattr(grape, attr, _clamp(getattr(grape, attr) + vmods[attr] * scale))
    grape.complexity = _clamp(grape.complexity
                              + vmods.get("complexity_delta", 0.0) * scale
                              + dmods.get("complexity_delta", 0.0))
    grape.ferment_quality = _clamp(grape.ferment_quality
                                   * vmods.get("quality_mult", 1.0)
                                   * dmods.get("quality_mult", 1.0))
    grape.state = "aged"
    grape.flavor_notes = generate_flavor_notes(grape)


def generate_flavor_notes(grape: "Grape") -> list:
    rng = random.Random(hash((grape.seed, "wine_flavor", grape.style, grape.vessel)))
    notes = []
    for attr, pool in _FLAVOR_POOLS.items():
        val = getattr(grape, attr, 0.0)
        if val > 0.6:
            notes.append(rng.choice(pool))
    if grape.crush_style in _CRUSH_NOTES:
        notes.append(rng.choice(_CRUSH_NOTES[grape.crush_style]))
    if grape.yeast in _YEAST_NOTES:
        notes.append(rng.choice(_YEAST_NOTES[grape.yeast]))
    if grape.vessel in _VESSEL_NOTES:
        notes.append(rng.choice(_VESSEL_NOTES[grape.vessel]))
    # Style-flavored tail notes
    if grape.style == "sparkling":
        notes.append("effervescent")
    elif grape.style == "dessert":
        notes.append("luscious")
    # Deduplicate and cap.
    seen = []
    for n in notes:
        if n not in seen:
            seen.append(n)
    return seen[:6] if seen else ["subtle"]


def make_blend(components: list) -> "Grape":
    n = len(components)
    seed = sum(g.seed for g in components) // n
    uid = hashlib.md5(f"wineblend_{'_'.join(g.uid for g in components)}".encode()).hexdigest()[:12]

    def avg(attr):
        return _clamp(sum(getattr(g, attr) for g in components) / n)

    style_counts = {}
    for g in components:
        style_counts[g.style] = style_counts.get(g.style, 0) + 1
    dominant_style = max(style_counts, key=style_counts.get) if style_counts else "red"

    all_notes = []
    for g in components:
        for note in g.flavor_notes:
            if note not in all_notes:
                all_notes.append(note)

    return Grape(
        uid=uid,
        origin_biome="blend",
        variety="blend",
        state="blended",
        style=dominant_style,
        sweetness=avg("sweetness"),
        acidity=avg("acidity"),
        tannin=avg("tannin"),
        body=avg("body"),
        aromatics=avg("aromatics"),
        alcohol=avg("alcohol"),
        complexity=avg("complexity"),
        press_quality=avg("press_quality"),
        ferment_quality=avg("ferment_quality"),
        flavor_notes=all_notes[:6],
        seed=seed,
        blend_components=[g.uid for g in components],
    )


def get_bottle_output_id(style: str, quality: float) -> str:
    base = {
        "red": "red_wine", "white": "white_wine", "rose": "rose_wine",
        "sparkling": "sparkling_wine", "dessert": "dessert_wine",
    }.get(style, "red_wine")
    if quality >= 0.7:
        return f"{base}_reserve"
    if quality >= 0.4:
        return f"{base}_fine"
    return base


def get_bottle_duration_multiplier(serving_temp: str) -> float:
    return SERVING_TEMPS.get(serving_temp, SERVING_TEMPS["cellar"])["duration_mult"]


def get_bottle_quality_bonus(serving_temp: str) -> float:
    return SERVING_TEMPS.get(serving_temp, SERVING_TEMPS["cellar"])["quality_bonus"]


class WineGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, biodome: str) -> "Grape":
        self._counter += 1
        seed = (self._world_seed * 37 + self._counter * 6151) & 0xFFFFFFFF
        uid = hashlib.md5(f"grape_{seed}_{self._counter}".encode()).hexdigest()[:12]

        profile = BIOME_GRAPE_PROFILES.get(biodome, BIOME_GRAPE_PROFILES["rolling_hills"])
        rng = random.Random(seed)

        def jitter(base):
            return _clamp(base + rng.gauss(0, 0.08))

        return Grape(
            uid=uid,
            origin_biome=biodome,
            variety=profile["variety"],
            state="raw",
            style="",
            sweetness=jitter(profile["sweetness"]),
            acidity=jitter(profile["acidity"]),
            tannin=jitter(profile["tannin"]),
            body=jitter(profile["body"]),
            aromatics=jitter(profile["aromatics"]),
            alcohol=0.0,
            complexity=0.0,
            press_quality=0.0,
            ferment_quality=0.0,
            flavor_notes=[],
            seed=seed,
        )
