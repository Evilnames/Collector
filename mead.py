"""Mead system — honey-wine batches, additives, fermentation, and bottling."""
import hashlib
import random
from dataclasses import dataclass, field


@dataclass
class MeadBatch:
    uid:             str
    origin_biome:    str
    honey_tier:      str    # "base" | "fine" | "artisan"
    additive:        str    # "none" | "pepper" | "saffron" | "red_wine" | "wheat_beer"
    yeast_type:      str    # "wild" | "wine" | "champagne" | "bread"
    state:           str    # "must" | "fermenting" | "bottled"
    sweetness:       float
    body:            float
    floral:          float
    complexity:      float
    carbonation:     float
    ferment_quality: float
    flavor_notes:    list
    seed:            int
    blend_components: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Biome profiles
# ---------------------------------------------------------------------------

BIOME_MEAD_PROFILES = {
    "temperate":       {"sweetness": 0.65, "body": 0.55, "floral": 0.70, "complexity": 0.45, "carbonation": 0.30},
    "alpine_mountain": {"sweetness": 0.50, "body": 0.65, "floral": 0.80, "complexity": 0.55, "carbonation": 0.25},
    "jungle":          {"sweetness": 0.55, "body": 0.60, "floral": 0.90, "complexity": 0.60, "carbonation": 0.30},
    "desert":          {"sweetness": 0.80, "body": 0.70, "floral": 0.45, "complexity": 0.50, "carbonation": 0.20},
    "rolling_hills":   {"sweetness": 0.70, "body": 0.50, "floral": 0.75, "complexity": 0.48, "carbonation": 0.35},
    "coastal":         {"sweetness": 0.60, "body": 0.55, "floral": 0.60, "complexity": 0.42, "carbonation": 0.40},
    "steppe":          {"sweetness": 0.60, "body": 0.65, "floral": 0.55, "complexity": 0.45, "carbonation": 0.25},
    "boreal":          {"sweetness": 0.45, "body": 0.60, "floral": 0.65, "complexity": 0.50, "carbonation": 0.30},
    "birch_forest":    {"sweetness": 0.60, "body": 0.55, "floral": 0.72, "complexity": 0.48, "carbonation": 0.32},
    "mediterranean":   {"sweetness": 0.65, "body": 0.60, "floral": 0.75, "complexity": 0.52, "carbonation": 0.30},
    "tropical":        {"sweetness": 0.72, "body": 0.58, "floral": 0.88, "complexity": 0.55, "carbonation": 0.35},
    "swamp":           {"sweetness": 0.40, "body": 0.62, "floral": 0.55, "complexity": 0.48, "carbonation": 0.28},
}
_DEFAULT_PROFILE = {"sweetness": 0.60, "body": 0.55, "floral": 0.65, "complexity": 0.45, "carbonation": 0.30}

BIOME_DISPLAY_NAMES = {
    "temperate":       "Temperate",
    "alpine_mountain": "Alpine",
    "jungle":          "Jungle",
    "desert":          "Desert",
    "rolling_hills":   "Rolling Hills",
    "coastal":         "Coastal",
    "steppe":          "Steppe",
    "boreal":          "Boreal",
    "birch_forest":    "Birch Forest",
    "mediterranean":   "Mediterranean",
    "tropical":        "Tropical",
    "swamp":           "Swamp",
}
_CODEX_BIOMES = list(BIOME_MEAD_PROFILES.keys())


# ---------------------------------------------------------------------------
# Additives — optional ingredient that shifts character and names the style
# ---------------------------------------------------------------------------

MEAD_ADDITIVES = {
    "none":       {"label": "None (Traditional)",   "item": None,         "sweetness": +0.00, "body": +0.00, "floral": +0.00, "complexity": +0.05, "carbonation": +0.00},
    "pepper":     {"label": "Pepper (Metheglin)",   "item": "pepper",     "sweetness": -0.05, "body": +0.10, "floral": +0.05, "complexity": +0.20, "carbonation": +0.05},
    "saffron":    {"label": "Saffron (Golden Mead)","item": "saffron",    "sweetness": +0.05, "body": +0.05, "floral": +0.12, "complexity": +0.22, "carbonation": +0.00},
    "red_wine":   {"label": "Red Wine (Pyment)",    "item": "red_wine",   "sweetness": +0.10, "body": +0.20, "floral": +0.15, "complexity": +0.28, "carbonation": +0.00},
    "wheat_beer": {"label": "Wheat Beer (Braggot)", "item": "wheat_beer", "sweetness": -0.05, "body": +0.18, "floral": -0.05, "complexity": +0.18, "carbonation": +0.15},
}

MEAD_STYLE_NAMES = {
    "none":       "Traditional Mead",
    "pepper":     "Metheglin",
    "saffron":    "Golden Mead",
    "red_wine":   "Pyment",
    "wheat_beer": "Braggot",
}


# ---------------------------------------------------------------------------
# Yeast types
# ---------------------------------------------------------------------------

YEAST_TYPES = {
    "wild":      {"label": "Wild Yeast",       "sweetness": +0.05, "body": +0.05, "complexity": +0.15, "carbonation": +0.10, "quality_variance": 0.25, "desc": "Unpredictable — high complexity, variable quality"},
    "wine":      {"label": "Wine Yeast",       "sweetness": -0.05, "body": +0.00, "complexity": +0.10, "carbonation": -0.05, "quality_variance": 0.10, "desc": "Clean — enhances floral notes, consistent"},
    "champagne": {"label": "Champagne Yeast",  "sweetness": -0.15, "body": -0.05, "complexity": +0.05, "carbonation": +0.25, "quality_variance": 0.08, "desc": "Dry and sparkling — crisp effervescent finish"},
    "bread":     {"label": "Bread Yeast",      "sweetness": +0.10, "body": +0.10, "complexity": +0.00, "carbonation": +0.05, "quality_variance": 0.15, "desc": "Rustic — adds warmth and body"},
}

_HONEY_TIER_BONUS = {"base": 0.0, "fine": 0.12, "artisan": 0.25}


# ---------------------------------------------------------------------------
# Flavor pools
# ---------------------------------------------------------------------------

_FLAVOR_POOLS = {
    "light":   ["delicate honey", "light floral", "fresh blossom", "gentle sweetness", "clean finish"],
    "floral":  ["wildflower bouquet", "lavender notes", "rose petal", "jasmine", "elderflower"],
    "rich":    ["golden honey", "beeswax warmth", "caramel undertone", "dried fruit", "amber sweetness"],
    "complex": ["layered depth", "herbal earthiness", "mineral finish", "fermented honey", "oak whisper"],
}
_ADDITIVE_NOTES = {
    "none":       [],
    "pepper":     ["warm pepper", "spice heat", "peppery finish"],
    "saffron":    ["exotic saffron", "golden warmth", "floral saffron"],
    "red_wine":   ["grape tannin", "vinous depth", "dark berry"],
    "wheat_beer": ["grainy sweetness", "wheat body", "bready malt"],
}
_YEAST_NOTES = {
    "wild":      ["wild ferment", "earthy funk", "rustic character"],
    "wine":      ["clean floral", "crisp acidity", "wine elegance"],
    "champagne": ["fine bubbles", "dry crispness", "effervescent"],
    "bread":     ["warm bread", "rustic yeast", "bready warmth"],
}


# ---------------------------------------------------------------------------
# Output descriptions and display colors
# ---------------------------------------------------------------------------

MEAD_TYPE_DESCS = {
    "none":       "Traditional Mead — pure honey and water, the ancient drink of celebration.",
    "pepper":     "Metheglin — spiced mead with bold warmth from freshly cracked pepper.",
    "saffron":    "Golden Mead — honey wine tinted with saffron's exotic floral character.",
    "red_wine":   "Pyment — a noble blend of honey must and red wine, rich and layered.",
    "wheat_beer": "Braggot — a hybrid of mead and beer, malty and effervescent.",
}
MEAD_TYPE_COLORS = {
    "none":       (225, 175,  60),
    "pepper":     (195, 130,  45),
    "saffron":    (235, 185,  35),
    "red_wine":   (160,  70,  55),
    "wheat_beer": (210, 175,  90),
}

BUFF_DESCS = {
    "vitality":    "Vitality (+15% max health)",
    "vigor":       "Vigor (+10% stamina regeneration)",
    "inspiration": "Inspiration (+12% crafting quality)",
}
MEAD_BUFFS = {
    "mead":         {"vitality":    {"duration":  90.0}},
    "mead_fine":    {"vitality":    {"duration": 110.0}, "vigor":       {"duration": 100.0}},
    "mead_reserve": {"vitality":    {"duration": 130.0}, "vigor":       {"duration": 120.0},
                     "inspiration": {"duration": 110.0}},
}


# ---------------------------------------------------------------------------
# Processing helpers
# ---------------------------------------------------------------------------

def apply_stir_result(batch: MeadBatch, stir_quality: float) -> None:
    batch.ferment_quality = max(0.0, min(1.0, stir_quality))
    batch.state = "fermenting"


def apply_condition_result(batch: MeadBatch, rack_bonus: float) -> None:
    batch.complexity    = min(1.0, batch.complexity + 0.05 + rack_bonus * 0.5)
    batch.ferment_quality = min(1.0, batch.ferment_quality + rack_bonus)
    batch.state         = "bottled"
    batch.flavor_notes  = _build_flavor_notes(batch)


def _build_flavor_notes(batch: MeadBatch) -> list:
    rng = random.Random(batch.seed)
    notes: list[str] = []
    q = batch.ferment_quality

    pool_keys = ["rich", "complex", "floral"] if q >= 0.75 else (["floral", "rich", "light"] if q >= 0.45 else ["light", "floral"])
    for pk in pool_keys:
        candidates = [n for n in _FLAVOR_POOLS[pk] if n not in notes]
        if candidates:
            notes.append(rng.choice(candidates))

    add_notes = _ADDITIVE_NOTES.get(batch.additive, [])
    if add_notes:
        notes.append(rng.choice(add_notes))

    yeast_notes = _YEAST_NOTES.get(batch.yeast_type, [])
    if yeast_notes and rng.random() < 0.6:
        notes.append(rng.choice(yeast_notes))

    return notes[:4]


def get_bottle_output_id(batch: MeadBatch) -> str:
    q = batch.ferment_quality
    if q >= 0.80:
        return "mead_reserve"
    elif q >= 0.55:
        return "mead_fine"
    return "mead"


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class MeadGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter    = 0

    def generate(self, biodome: str, honey_tier: str,
                 additive: str, yeast_type: str) -> MeadBatch:
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid  = hashlib.md5(f"mead_{seed}_{self._counter}".encode()).hexdigest()[:12]
        rng  = random.Random(seed)

        profile = BIOME_MEAD_PROFILES.get(biodome, _DEFAULT_PROFILE)
        add     = MEAD_ADDITIVES.get(additive, MEAD_ADDITIVES["none"])
        yeast   = YEAST_TYPES.get(yeast_type, YEAST_TYPES["wine"])
        tier_q  = _HONEY_TIER_BONUS.get(honey_tier, 0.0)

        def jitter(base: float) -> float:
            return max(0.0, min(1.0, base + rng.uniform(-0.10, 0.10)))

        sweetness   = jitter(profile["sweetness"]   + add["sweetness"]   + yeast["sweetness"])
        body        = jitter(profile["body"]         + add["body"]        + yeast["body"])
        floral      = jitter(profile["floral"]       + add["floral"])
        complexity  = jitter(profile["complexity"]   + add["complexity"]  + yeast["complexity"] + tier_q * 0.15)
        carbonation = jitter(profile["carbonation"]  + add["carbonation"] + yeast["carbonation"])

        return MeadBatch(
            uid=uid, origin_biome=biodome, honey_tier=honey_tier,
            additive=additive, yeast_type=yeast_type, state="must",
            sweetness=sweetness, body=body, floral=floral,
            complexity=complexity, carbonation=carbonation,
            ferment_quality=0.0, flavor_notes=[], seed=seed,
        )
