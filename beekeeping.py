import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class HoneyJar:
    uid: str
    origin_biome: str       # biodome where hive was placed
    dominant_flower: str    # most-represented nearby flower type
    flower_diversity: int   # distinct flower types detected near hive (0–10+)
    quality: float          # 0.0–1.0, set by spin mini-game
    sweetness: float        # 0.0–1.0
    floral: float           # 0.0–1.0
    earthiness: float       # 0.0–1.0
    flavor_notes: list
    seed: int
    state: str = "liquid"   # "liquid" | "crystallized"


# Base honey profiles per biodome
BIOME_HONEY_PROFILES = {
    "tropical":        {"sweetness": 0.75, "floral": 0.85, "earthiness": 0.30, "dominant": "hibiscus"},
    "jungle":          {"sweetness": 0.55, "floral": 0.90, "earthiness": 0.45, "dominant": "orchid"},
    "savanna":         {"sweetness": 0.60, "floral": 0.45, "earthiness": 0.70, "dominant": "acacia"},
    "wetland":         {"sweetness": 0.45, "floral": 0.55, "earthiness": 0.80, "dominant": "lotus"},
    "arid_steppe":     {"sweetness": 0.70, "floral": 0.40, "earthiness": 0.65, "dominant": "sage"},
    "canyon":          {"sweetness": 0.65, "floral": 0.40, "earthiness": 0.75, "dominant": "desert_bloom"},
    "beach":           {"sweetness": 0.60, "floral": 0.60, "earthiness": 0.35, "dominant": "sea_lavender"},
    "tundra":          {"sweetness": 0.35, "floral": 0.55, "earthiness": 0.75, "dominant": "arctic_poppy"},
    "swamp":           {"sweetness": 0.40, "floral": 0.55, "earthiness": 0.85, "dominant": "bog_flower"},
    "alpine_mountain": {"sweetness": 0.50, "floral": 0.80, "earthiness": 0.60, "dominant": "heather"},
    "rocky_mountain":  {"sweetness": 0.45, "floral": 0.65, "earthiness": 0.70, "dominant": "wildflower"},
    "rolling_hills":   {"sweetness": 0.70, "floral": 0.75, "earthiness": 0.30, "dominant": "clover"},
    "boreal":          {"sweetness": 0.45, "floral": 0.65, "earthiness": 0.70, "dominant": "fireweed"},
}

_FLAVOR_POOLS = {
    "sweetness":  ["clover", "caramel", "ripe fruit", "maple", "brown sugar", "dried apricot"],
    "floral":     ["rose", "lavender", "elderflower", "jasmine", "orange blossom", "chamomile"],
    "earthiness": ["pine resin", "forest floor", "beeswax", "dried grass", "cedar", "mushroom"],
}

# Notes that unlock when flower_diversity is high (≥4)
_DIVERSITY_NOTES = ["wildflower bouquet", "mixed blossom", "meadow blend", "botanical complexity"]

BUFF_DESCS = {
    "foraging": "Foraging Luck (+12%)",
    "bloom":    "Flower Bloom Rate (+15%)",
}

_CODEX_BIOMES = [
    "tropical", "jungle", "savanna", "wetland", "arid_steppe", "canyon",
    "beach", "tundra", "swamp", "alpine_mountain", "rocky_mountain",
    "rolling_hills", "boreal",
]

HONEY_TYPE_ORDER = [
    f"{biome}_{tier}"
    for biome in _CODEX_BIOMES
    for tier in ["base", "fine", "artisan"]
]

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
    "boreal":          "Boreal",
}


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def generate_flavor_notes(jar: "HoneyJar") -> list:
    rng = random.Random(hash((jar.seed, "honey_flavor")))
    notes = []
    for attr, pool in _FLAVOR_POOLS.items():
        val = getattr(jar, attr)
        if val > 0.55:
            notes.append(rng.choice(pool))
    if jar.flower_diversity >= 4:
        notes.append(rng.choice(_DIVERSITY_NOTES))
    seen = []
    for n in notes:
        if n not in seen:
            seen.append(n)
    return seen[:5] if seen else ["mild sweetness"]


def get_honey_item_id(quality: float) -> str:
    if quality >= 0.80:
        return "honey_jar_artisan"
    if quality >= 0.55:
        return "honey_jar_fine"
    return "honey_jar"


def get_quality_tier(quality: float) -> str:
    if quality >= 0.80:
        return "artisan"
    if quality >= 0.55:
        return "fine"
    return "base"


class HoneyGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, biodome: str, flower_diversity: int = 0) -> "HoneyJar":
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid = hashlib.md5(f"honey_{seed}_{self._counter}".encode()).hexdigest()[:12]

        profile = BIOME_HONEY_PROFILES.get(biodome, BIOME_HONEY_PROFILES["rolling_hills"])
        rng = random.Random(seed)
        sigma = max(0.04, 0.09 - flower_diversity * 0.005)

        def jitter(base):
            return _clamp(base + rng.gauss(0, sigma))

        jar = HoneyJar(
            uid=uid,
            origin_biome=biodome,
            dominant_flower=profile["dominant"],
            flower_diversity=flower_diversity,
            quality=0.0,  # filled in by mini-game result
            sweetness=jitter(profile["sweetness"]),
            floral=jitter(profile["floral"]),
            earthiness=jitter(profile["earthiness"]),
            flavor_notes=[],
            seed=seed,
        )
        # Higher flower diversity boosts floral and softens earthiness
        if flower_diversity > 0:
            bonus = min(flower_diversity, 8) * 0.015
            jar.floral    = _clamp(jar.floral    + bonus)
            jar.sweetness = _clamp(jar.sweetness + bonus * 0.5)
            jar.earthiness = _clamp(jar.earthiness - bonus * 0.3)

        return jar
