import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class TeaLeaf:
    uid: str
    origin_biome: str       # biome harvested in ("blend" for blended)
    variety: str            # "assam"|"yunnan"|"darjeeling"|"ceylon"|"high_mountain"|"blend"
    state: str              # "raw"|"withered"|"oxidized"|"brewed"|"blended"
    tea_type: str           # ""|"green"|"oolong"|"black"|"puerh"
    oxidation: float        # 0.0–1.0, set by mini-game
    astringency: float
    floral: float
    vegetal: float
    earthiness: float
    sweetness: float
    steep_quality: float    # 0.0–1.0
    complexity: float       # 0.0–1.0, grows with aging
    flavor_notes: list
    seed: int
    blend_components: list = field(default_factory=list)
    wither_method: str = ""         # "sun"|"shade"|"indoor"
    herbal_additions: list = field(default_factory=list)  # item keys added at blend
    age_duration: str = ""          # ""|"short"|"medium"|"long"


# Base flavor profiles per biome — only biomes where tea grows
BIOME_TEA_PROFILES = {
    "tropical":        {"astringency": 0.85, "floral": 0.35, "vegetal": 0.30, "earthiness": 0.40, "sweetness": 0.60, "variety": "assam"},
    "jungle":          {"astringency": 0.65, "floral": 0.40, "vegetal": 0.45, "earthiness": 0.75, "sweetness": 0.45, "variety": "yunnan"},
    "alpine_mountain": {"astringency": 0.35, "floral": 0.90, "vegetal": 0.55, "earthiness": 0.20, "sweetness": 0.70, "variety": "darjeeling"},
    "rolling_hills":   {"astringency": 0.55, "floral": 0.55, "vegetal": 0.50, "earthiness": 0.50, "sweetness": 0.55, "variety": "ceylon"},
    "tundra":          {"astringency": 0.25, "floral": 0.80, "vegetal": 0.65, "earthiness": 0.15, "sweetness": 0.75, "variety": "high_mountain"},
}

_FLAVOR_POOLS = {
    "astringency": ["brisk", "tannic grip", "drying finish", "bold structure", "robust"],
    "floral":      ["jasmine", "rose", "orchid", "magnolia", "lilac", "osmanthus"],
    "vegetal":     ["fresh grass", "steamed spinach", "snap pea", "seaweed", "hay", "matcha"],
    "earthiness":  ["forest floor", "wet stone", "aged wood", "mushroom", "dark soil", "petrichor"],
    "sweetness":   ["honey", "peach", "lychee", "apricot", "caramel", "dried fruit"],
}

_WITHER_NOTES = {
    "sun":    ["sun-dried apricot", "raisined sweetness"],
    "shade":  ["cool meadow", "dew-fresh"],
    "indoor": ["toasty warmth", "dried hay"],
}

_HERBAL_NOTES = {
    "ginger":         ["spiced ginger", "warming heat"],
    "chamomile_item": ["chamomile", "soft floral"],
    "mint":           ["cool mint", "fresh herbal"],
}

WITHER_METHODS = {
    "sun": {
        "label": "Sun Withered",
        "desc":  "Spread under open sun. Boosts sweetness, reduces vegetal notes.",
        "astringency": +0.08, "floral": -0.05, "vegetal": -0.10, "earthiness": +0.00, "sweetness": +0.05,
    },
    "shade": {
        "label": "Shade Withered",
        "desc":  "Slow wither under cloth. Lifts floral character.",
        "astringency": -0.05, "floral": +0.10, "vegetal": +0.05, "earthiness": -0.03, "sweetness": +0.02,
    },
    "indoor": {
        "label": "Indoor Withered",
        "desc":  "Controlled environment. Reduces vegetal sharpness, builds complexity.",
        "astringency": -0.03, "floral": +0.02, "vegetal": -0.15, "earthiness": +0.05, "sweetness": +0.10,
        "complexity_bonus": 0.05,
    },
}

# Oxidation level → tea type thresholds
OXIDATION_ZONES = {
    "green":  (0.00, 0.20),
    "oolong": (0.20, 0.75),
    "black":  (0.75, 0.95),
    "puerh":  (0.95, 1.00),
}

TEA_TYPE_DESCS = {
    "green":  "Green Tea — fresh, vegetal, bright",
    "oolong": "Oolong — complex, floral, semi-oxidized",
    "black":  "Black Tea — bold, malty, brisk",
    "puerh":  "Pu-erh — earthy, aged, deep",
}

TEA_TYPE_COLORS = {
    "green":  ( 80, 160,  80),
    "oolong": (180, 140,  60),
    "black":  ( 60,  35,  15),
    "puerh":  ( 45,  30,  10),
}

BUFF_DESCS = {
    "tranquility": "Incoming damage -30%",
    "harmony":     "Farm yield +25%",
    "alertness":   "Discovery XP +30%",
    "longevity":   "Hunger drain -55%",
}

# Maps tea_type → buff granted when consumed
TEA_TYPE_BUFFS = {
    "green":  "tranquility",
    "oolong": "harmony",
    "black":  "alertness",
    "puerh":  "longevity",
}

HERBAL_ADDITIVES = {
    "ginger": {
        "label":            "Ginger",
        "floral":           +0.05,
        "earthiness":       +0.10,
        "sweetness":        +0.05,
        "complexity_bonus": 0.05,
    },
    "chamomile_item": {
        "label":            "Chamomile",
        "floral":           +0.20,
        "sweetness":        +0.10,
        "astringency":      -0.10,
        "complexity_bonus": 0.04,
    },
    "mint": {
        "label":            "Mint",
        "vegetal":          -0.10,
        "floral":           +0.05,
        "sweetness":        +0.08,
        "astringency":      -0.08,
        "complexity_bonus": 0.03,
    },
}

AGE_DURATIONS = {
    "short":  {"label": "Short (3mo)",  "quality_mult": 1.00, "complexity_delta": 0.06},
    "medium": {"label": "Medium (1yr)", "quality_mult": 1.06, "complexity_delta": 0.12},
    "long":   {"label": "Long (3yr)",   "quality_mult": 1.12, "complexity_delta": 0.20},
}

_CODEX_BIOMES = ["tropical", "jungle", "alpine_mountain", "rolling_hills", "tundra"]
TEA_TYPE_ORDER = [f"{b}_{t}" for b in _CODEX_BIOMES for t in ["green", "oolong", "black", "puerh"]]

BIOME_DISPLAY_NAMES = {
    "tropical":        "Tropical",
    "jungle":          "Jungle",
    "alpine_mountain": "Alpine",
    "rolling_hills":   "Rolling Hills",
    "tundra":          "Tundra",
    "blend":           "Blend",
}

VARIETY_DISPLAY_NAMES = {
    "assam":        "Assam",
    "yunnan":       "Yunnan",
    "darjeeling":   "Darjeeling",
    "ceylon":       "Ceylon",
    "high_mountain": "High Mountain",
    "blend":        "Blend",
}


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def tea_type_from_oxidation(level: float) -> str:
    for t_type, (lo, hi) in OXIDATION_ZONES.items():
        if lo <= level <= hi:
            return t_type
    return "black"


def apply_wither(leaf: "TeaLeaf", method: str):
    mods = WITHER_METHODS.get(method)
    if not mods:
        return
    leaf.wither_method = method
    for attr in ("astringency", "floral", "vegetal", "earthiness", "sweetness"):
        if attr in mods:
            setattr(leaf, attr, _clamp(getattr(leaf, attr) + mods[attr]))
    leaf.complexity = _clamp(leaf.complexity + mods.get("complexity_bonus", 0.0))
    leaf.state = "withered"


def apply_oxidation(leaf: "TeaLeaf", oxidation_level: float, quality: float):
    leaf.oxidation    = _clamp(oxidation_level)
    leaf.tea_type     = tea_type_from_oxidation(leaf.oxidation)
    leaf.steep_quality = _clamp(quality)
    # Oxidation modifies attributes
    ox = leaf.oxidation
    leaf.astringency = _clamp(leaf.astringency + ox * 0.15)
    leaf.floral      = _clamp(leaf.floral      - ox * 0.10)
    leaf.vegetal     = _clamp(leaf.vegetal     - ox * 0.20)
    leaf.earthiness  = _clamp(leaf.earthiness  + ox * 0.25)
    leaf.sweetness   = _clamp(leaf.sweetness   - ox * 0.05)
    leaf.state       = "oxidized"
    leaf.flavor_notes = generate_flavor_notes(leaf)


def apply_aging(leaf: "TeaLeaf", duration_key: str):
    dmods = AGE_DURATIONS.get(duration_key)
    if not dmods or leaf.tea_type != "puerh":
        return
    leaf.age_duration  = duration_key
    leaf.complexity    = _clamp(leaf.complexity + dmods["complexity_delta"])
    leaf.steep_quality = _clamp(leaf.steep_quality * dmods["quality_mult"])
    # Aging deepens earthiness, smooths astringency
    scale = {"short": 0.5, "medium": 1.0, "long": 1.5}.get(duration_key, 1.0)
    leaf.earthiness  = _clamp(leaf.earthiness  + 0.08 * scale)
    leaf.astringency = _clamp(leaf.astringency - 0.06 * scale)
    leaf.flavor_notes = generate_flavor_notes(leaf)


def apply_herbal_blend(leaf: "TeaLeaf", ingredient_keys: list):
    for key in ingredient_keys:
        mods = HERBAL_ADDITIVES.get(key)
        if not mods:
            continue
        if key not in leaf.herbal_additions:
            leaf.herbal_additions.append(key)
        for attr in ("astringency", "floral", "vegetal", "earthiness", "sweetness"):
            if attr in mods:
                setattr(leaf, attr, _clamp(getattr(leaf, attr) + mods[attr]))
        leaf.complexity = _clamp(leaf.complexity + mods.get("complexity_bonus", 0.0))
    leaf.flavor_notes = generate_flavor_notes(leaf)


def generate_flavor_notes(leaf: "TeaLeaf") -> list:
    rng = random.Random(hash((leaf.seed, "tea_flavor")))
    notes = []
    for attr, pool in _FLAVOR_POOLS.items():
        val = getattr(leaf, attr, 0.0)
        if val > 0.6:
            notes.append(rng.choice(pool))
    if leaf.wither_method in _WITHER_NOTES:
        notes.append(rng.choice(_WITHER_NOTES[leaf.wither_method]))
    for key in leaf.herbal_additions:
        if key in _HERBAL_NOTES:
            notes.append(rng.choice(_HERBAL_NOTES[key]))
    # Tea-type character notes
    if leaf.tea_type == "puerh":
        notes = [n for n in notes if n not in ("fresh grass", "snap pea")] + ["aged earth", "camphor"]
    elif leaf.tea_type == "green":
        notes = [n for n in notes if n not in ("brisk", "tannic grip")] + ["fresh finish"]
    seen = []
    for n in notes:
        if n not in seen:
            seen.append(n)
    return seen[:5] if seen else ["delicate"]


def get_brew_item_id(leaf: "TeaLeaf") -> str:
    base = f"{leaf.tea_type}_tea"
    if leaf.steep_quality >= 0.7 or (leaf.tea_type == "puerh" and leaf.age_duration in ("medium", "long")):
        return f"{base}_aged"
    elif leaf.steep_quality >= 0.4:
        return f"{base}_fine"
    return base


def make_blend(components: list) -> "TeaLeaf":
    n = len(components)
    seed = sum(c.seed for c in components) // n
    uid  = hashlib.md5(f"teablend_{'_'.join(c.uid for c in components)}".encode()).hexdigest()[:12]

    def avg(attr):
        return _clamp(sum(getattr(c, attr) for c in components) / n)

    type_counts = {}
    for c in components:
        type_counts[c.tea_type] = type_counts.get(c.tea_type, 0) + 1
    dominant_type = max(type_counts, key=type_counts.get) if type_counts else "green"

    all_notes = []
    for c in components:
        for note in c.flavor_notes:
            if note not in all_notes:
                all_notes.append(note)

    return TeaLeaf(
        uid=uid,
        origin_biome="blend",
        variety="blend",
        state="blended",
        tea_type=dominant_type,
        oxidation=avg("oxidation"),
        astringency=avg("astringency"),
        floral=avg("floral"),
        vegetal=avg("vegetal"),
        earthiness=avg("earthiness"),
        sweetness=avg("sweetness"),
        steep_quality=avg("steep_quality"),
        complexity=avg("complexity"),
        flavor_notes=all_notes[:5],
        seed=seed,
        blend_components=[c.uid for c in components],
    )


class TeaGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter    = 0

    def generate(self, biodome: str) -> "TeaLeaf":
        self._counter += 1
        seed = (self._world_seed * 41 + self._counter * 5381) & 0xFFFFFFFF
        uid  = hashlib.md5(f"tea_{seed}_{self._counter}".encode()).hexdigest()[:12]

        profile = BIOME_TEA_PROFILES.get(biodome, BIOME_TEA_PROFILES["rolling_hills"])
        rng = random.Random(seed)

        def jitter(base):
            return _clamp(base + rng.gauss(0, 0.08))

        return TeaLeaf(
            uid=uid,
            origin_biome=biodome,
            variety=profile["variety"],
            state="raw",
            tea_type="",
            oxidation=0.0,
            astringency=jitter(profile["astringency"]),
            floral=jitter(profile["floral"]),
            vegetal=jitter(profile["vegetal"]),
            earthiness=jitter(profile["earthiness"]),
            sweetness=jitter(profile["sweetness"]),
            steep_quality=0.0,
            complexity=0.0,
            flavor_notes=[],
            seed=seed,
        )
