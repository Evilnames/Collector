import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class Spirit:
    uid: str
    origin_biome: str        # biodome where grain was harvested ("blend" for blended)
    grain_type: str          # "grain" | "corn" | "sugarcane" | "botanical" | "pomace" | "blend"
    spirit_type: str         # "whiskey" | "bourbon" | "rum" | "gin" | "brandy" | "vodka"
    state: str               # "raw" | "distilled" | "aged" | "blended"
    cut_quality: float       # 0.0–1.0, set by distillation mini-game
    proof: float             # 0.0–1.0, alcohol content (hearts cut = highest)
    grain_character: float   # malt/grain intensity
    sweetness: float
    spice: float
    smokiness: float
    smoothness: float
    age_quality: float       # 0.0–1.0, set by barrel aging
    flavor_notes: list
    seed: int
    blend_components: list = field(default_factory=list)
    barrel_type: str = ""    # "new_oak" | "charred_oak" | "used_oak"
    age_duration: str = ""   # "short" | "medium" | "long"


# Base profiles per biome — determines spirit type and starting attributes
BIOME_SPIRIT_PROFILES = {
    "tropical":        {"grain_type": "sugarcane",  "spirit_type": "rum",     "grain_character": 0.30, "sweetness": 0.85, "spice": 0.45, "smokiness": 0.10, "smoothness": 0.65},
    "jungle":          {"grain_type": "corn",        "spirit_type": "bourbon", "grain_character": 0.75, "sweetness": 0.65, "spice": 0.55, "smokiness": 0.20, "smoothness": 0.45},
    "savanna":         {"grain_type": "corn",        "spirit_type": "bourbon", "grain_character": 0.80, "sweetness": 0.55, "spice": 0.70, "smokiness": 0.25, "smoothness": 0.40},
    "wetland":         {"grain_type": "botanical",   "spirit_type": "gin",     "grain_character": 0.25, "sweetness": 0.40, "spice": 0.75, "smokiness": 0.05, "smoothness": 0.70},
    "arid_steppe":     {"grain_type": "grain",       "spirit_type": "whiskey", "grain_character": 0.70, "sweetness": 0.40, "spice": 0.85, "smokiness": 0.45, "smoothness": 0.35},
    "canyon":          {"grain_type": "grain",       "spirit_type": "whiskey", "grain_character": 0.65, "sweetness": 0.30, "spice": 0.75, "smokiness": 0.80, "smoothness": 0.25},
    "beach":           {"grain_type": "sugarcane",   "spirit_type": "rum",     "grain_character": 0.25, "sweetness": 0.80, "spice": 0.35, "smokiness": 0.05, "smoothness": 0.75},
    "tundra":          {"grain_type": "grain",       "spirit_type": "vodka",   "grain_character": 0.40, "sweetness": 0.20, "spice": 0.30, "smokiness": 0.05, "smoothness": 0.90},
    "swamp":           {"grain_type": "botanical",   "spirit_type": "gin",     "grain_character": 0.20, "sweetness": 0.35, "spice": 0.80, "smokiness": 0.30, "smoothness": 0.45},
    "alpine_mountain": {"grain_type": "pomace",      "spirit_type": "brandy",  "grain_character": 0.35, "sweetness": 0.75, "spice": 0.40, "smokiness": 0.10, "smoothness": 0.70},
    "rocky_mountain":  {"grain_type": "pomace",      "spirit_type": "brandy",  "grain_character": 0.40, "sweetness": 0.60, "spice": 0.55, "smokiness": 0.25, "smoothness": 0.55},
    "rolling_hills":   {"grain_type": "grain",       "spirit_type": "whiskey", "grain_character": 0.85, "sweetness": 0.50, "spice": 0.60, "smokiness": 0.30, "smoothness": 0.50},
    "boreal":          {"grain_type": "grain",       "spirit_type": "vodka",   "grain_character": 0.50, "sweetness": 0.15, "spice": 0.20, "smokiness": 0.10, "smoothness": 0.85},
}

_FLAVOR_POOLS = {
    "grain_character": ["malt", "cereal", "bread crust", "biscuit", "dried grain", "toasted barley"],
    "sweetness":       ["vanilla", "caramel", "honey", "ripe banana", "brown sugar", "molasses"],
    "spice":           ["black pepper", "clove", "nutmeg", "cinnamon", "dried chili", "white pepper"],
    "smokiness":       ["peat", "campfire", "char", "ash", "smoked oak", "bonfire"],
    "smoothness":      ["cream", "silk", "gentle oak", "soft finish", "velvety", "rounded malt"],
}

_BARREL_NOTES = {
    "new_oak":    ["fresh oak", "tannin", "sawdust", "bold wood"],
    "charred_oak":["vanilla char", "toasted coconut", "caramel layer", "sweet smoke"],
    "used_oak":   ["gentle oak", "dried fruit", "polished wood", "soft tannin"],
}

_AGE_NOTES = {
    "short":  ["young spirit", "raw edge"],
    "medium": ["mellow grain", "aged wood"],
    "long":   ["old oak", "dried plum", "complexity"],
}

SPIRIT_TYPE_DESCS = {
    "whiskey": "Whiskey — grain-forward, spiced, oak-kissed",
    "bourbon": "Bourbon — corn-sweet, caramel, full-bodied",
    "rum":     "Rum — sugarcane-bright, tropical, smooth",
    "gin":     "Gin — botanical, juniper-led, crisp",
    "brandy":  "Brandy — fruit-distilled, elegant, warming",
    "vodka":   "Vodka — clean, neutral, silky smooth",
}

SPIRIT_TYPE_COLORS = {
    "whiskey": (180, 120,  40),
    "bourbon": (200, 100,  30),
    "rum":     (220, 160,  60),
    "gin":     (190, 225, 235),
    "brandy":  (185, 110,  50),
    "vodka":   (230, 235, 240),
}

BARREL_TYPES = {
    "new_oak": {
        "label": "New Oak",
        "desc":  "Aggressive tannin and fresh wood. Bold spice and high complexity.",
        "grain_character": +0.05, "spice": +0.18, "smokiness": +0.05, "smoothness": -0.12, "sweetness": +0.08,
        "complexity_delta": +0.15, "quality_mult": 1.05,
    },
    "charred_oak": {
        "label": "Charred Oak",
        "desc":  "Caramel and vanilla from deep char. Classic American style.",
        "grain_character": +0.00, "spice": +0.08, "smokiness": +0.12, "smoothness": +0.05, "sweetness": +0.18,
        "complexity_delta": +0.12, "quality_mult": 1.08,
    },
    "used_oak": {
        "label": "Used Oak",
        "desc":  "Previous cask character. Gentle aging with fruit and soft tannin.",
        "grain_character": -0.05, "spice": +0.05, "smokiness": -0.05, "smoothness": +0.18, "sweetness": +0.10,
        "complexity_delta": +0.10, "quality_mult": 1.10,
    },
}

AGE_DURATIONS = {
    "short":  {"label": "Short (1 day)",   "days": 1,  "quality_mult": 1.00, "complexity_delta": 0.04},
    "medium": {"label": "Medium (8 days)", "days": 8,  "quality_mult": 1.06, "complexity_delta": 0.10},
    "long":   {"label": "Long (16 days)",  "days": 16, "quality_mult": 1.12, "complexity_delta": 0.20},
}

BUFF_DESCS = {
    "grit":       "Pick power +1.5 / Mining speed +20%",
    "warmth":     "Cold damage -60% / Hunger drain -20%",
    "sea_legs":   "Move speed +20% / Jump height +1",
    "clarity":    "Collect radius +60% / Discovery XP +15%",
    "refinement": "Discovery XP +30% / Craft speed +20%",
    "endurance":  "Hunger drain -50% / Stamina +25%",
}

SPIRIT_BUFFS = {
    "whiskey": "grit",
    "bourbon": "warmth",
    "rum":     "sea_legs",
    "gin":     "clarity",
    "brandy":  "refinement",
    "vodka":   "endurance",
}

# Codex ordering — one entry per biome per quality tier
_CODEX_BIOMES = list(BIOME_SPIRIT_PROFILES.keys())
SPIRIT_TYPE_ORDER = [
    f"{biome}_{tier}"
    for biome in _CODEX_BIOMES
    for tier in ["young", "aged", "reserve"]
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
    "blend":           "Blend",
}


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def apply_distillation_result(spirit: "Spirit",
                               time_in_heads: float, time_in_hearts: float,
                               time_in_tails: float, total_time: float,
                               penalties: int):
    if total_time <= 0:
        total_time = 0.1
    hearts_frac = time_in_hearts / total_time
    heads_frac  = time_in_heads  / total_time
    tails_frac  = time_in_tails  / total_time

    # Proof peaks in the hearts cut
    spirit.proof = _clamp(0.35 + hearts_frac * 0.55)
    # Heads contamination = harsh; tails = extra flavor but rough
    spirit.smoothness = _clamp(spirit.smoothness - heads_frac * 0.30 - tails_frac * 0.15)
    spirit.spice      = _clamp(spirit.spice      + tails_frac  * 0.12)
    spirit.smokiness  = _clamp(spirit.smokiness  + heads_frac  * 0.08)

    # Quality weighted toward hearts fraction, penalized for bad cuts
    heads_timing_score = 1.0 - abs(heads_frac - 0.20) * 2.0  # ideal heads ~20%
    quality = _clamp(
        hearts_frac * 0.65
        + max(0.0, heads_timing_score) * 0.20
        + min(hearts_frac, 0.5) * 0.15
        - penalties * 0.12
    )
    spirit.cut_quality = quality
    spirit.state = "distilled"
    spirit.flavor_notes = generate_flavor_notes(spirit)


def apply_barrel_aging(spirit: "Spirit", barrel_key: str, duration_key: str):
    bmods = BARREL_TYPES.get(barrel_key)
    dmods = AGE_DURATIONS.get(duration_key)
    if not bmods or not dmods:
        return
    spirit.barrel_type  = barrel_key
    spirit.age_duration = duration_key
    scale = {"short": 0.5, "medium": 1.0, "long": 1.5}.get(duration_key, 1.0)
    for attr in ("grain_character", "sweetness", "spice", "smokiness", "smoothness"):
        setattr(spirit, attr, _clamp(getattr(spirit, attr) + bmods.get(attr, 0.0) * scale))
    raw_quality = (spirit.cut_quality
                   * bmods.get("quality_mult", 1.0)
                   * dmods.get("quality_mult", 1.0))
    spirit.age_quality = _clamp(raw_quality + dmods.get("complexity_delta", 0.0) * 0.25)
    spirit.state = "aged"
    spirit.flavor_notes = generate_flavor_notes(spirit)


def generate_flavor_notes(spirit: "Spirit") -> list:
    rng = random.Random(hash((spirit.seed, "spirit_flavor", spirit.spirit_type, spirit.barrel_type)))
    notes = []
    for attr, pool in _FLAVOR_POOLS.items():
        val = getattr(spirit, attr, 0.0)
        if val > 0.60:
            notes.append(rng.choice(pool))
    if spirit.barrel_type in _BARREL_NOTES:
        notes.append(rng.choice(_BARREL_NOTES[spirit.barrel_type]))
    if spirit.age_duration in _AGE_NOTES:
        notes.append(rng.choice(_AGE_NOTES[spirit.age_duration]))
    tail = {
        "whiskey": "long grain finish", "bourbon": "sweet corn fade",
        "rum":     "tropical warmth",   "gin":     "juniper lift",
        "brandy":  "dried fruit",       "vodka":   "clean fade",
    }.get(spirit.spirit_type)
    if tail:
        notes.append(tail)
    seen = []
    for n in notes:
        if n not in seen:
            seen.append(n)
    return seen[:6] if seen else ["subtle spirit"]


def make_blend(components: list) -> "Spirit":
    n = len(components)
    seed = sum(s.seed for s in components) // n
    uid = hashlib.md5(
        f"spiritblend_{'_'.join(s.uid for s in components)}".encode()
    ).hexdigest()[:12]

    def avg(attr):
        return _clamp(sum(getattr(s, attr) for s in components) / n)

    type_counts = {}
    for s in components:
        type_counts[s.spirit_type] = type_counts.get(s.spirit_type, 0) + 1
    dominant_type = max(type_counts, key=type_counts.get)

    all_notes = []
    for s in components:
        for note in s.flavor_notes:
            if note not in all_notes:
                all_notes.append(note)

    return Spirit(
        uid=uid,
        origin_biome="blend",
        grain_type="blend",
        spirit_type=dominant_type,
        state="blended",
        cut_quality=avg("cut_quality"),
        proof=avg("proof"),
        grain_character=avg("grain_character"),
        sweetness=avg("sweetness"),
        spice=avg("spice"),
        smokiness=avg("smokiness"),
        smoothness=avg("smoothness"),
        age_quality=avg("age_quality"),
        flavor_notes=all_notes[:6],
        seed=seed,
        blend_components=[s.uid for s in components],
    )


def get_bottle_output_id(spirit_type: str, quality: float) -> str:
    if quality >= 0.70:
        return f"{spirit_type}_reserve"
    if quality >= 0.40:
        return f"{spirit_type}_aged"
    return spirit_type


class SpiritGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, biodome: str) -> "Spirit":
        self._counter += 1
        seed = (self._world_seed * 41 + self._counter * 5237) & 0xFFFFFFFF
        uid = hashlib.md5(f"spirit_{seed}_{self._counter}".encode()).hexdigest()[:12]

        profile = BIOME_SPIRIT_PROFILES.get(biodome, BIOME_SPIRIT_PROFILES["rolling_hills"])
        rng = random.Random(seed)

        def jitter(base):
            return _clamp(base + rng.gauss(0, 0.07))

        return Spirit(
            uid=uid,
            origin_biome=biodome,
            grain_type=profile["grain_type"],
            spirit_type=profile["spirit_type"],
            state="raw",
            cut_quality=0.0,
            proof=0.0,
            grain_character=jitter(profile["grain_character"]),
            sweetness=jitter(profile["sweetness"]),
            spice=jitter(profile["spice"]),
            smokiness=jitter(profile["smokiness"]),
            smoothness=jitter(profile["smoothness"]),
            age_quality=0.0,
            flavor_notes=[],
            seed=seed,
        )
