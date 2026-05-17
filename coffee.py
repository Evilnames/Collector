import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class CoffeeBean:
    uid: str
    origin_biome: str        # biodome where cherry was harvested ("blend" for blended)
    variety: str             # "arabica" | "robusta" | "liberica" | "blend"
    state: str               # "raw" | "roasted" | "blended"
    roast_level: str         # "green" | "light" | "medium" | "dark" | "charred"
    roast_quality: float     # 0.0–1.0, set by mini-game performance
    acidity: float
    body: float
    sweetness: float
    earthiness: float
    brightness: float
    flavor_notes: list       # 2–5 flavor strings
    seed: int
    blend_components: list = field(default_factory=list)  # uids of source beans
    processing_method: str = ""  # "washed" | "natural" | "honey" | ""
    terroir_quality: float = 0.0  # 0.0 = wild/unknown; >0 = farmed with soil care


# Base flavor profiles per biodome
BIOME_FLAVOR_PROFILES = {
    # Original 7
    "tropical":        {"acidity": 0.75, "body": 0.55, "sweetness": 0.80, "earthiness": 0.25, "brightness": 0.85, "variety": "arabica"},
    "jungle":          {"acidity": 0.60, "body": 0.70, "sweetness": 0.65, "earthiness": 0.55, "brightness": 0.60, "variety": "arabica"},
    "savanna":         {"acidity": 0.40, "body": 0.85, "sweetness": 0.45, "earthiness": 0.80, "brightness": 0.30, "variety": "robusta"},
    "wetland":         {"acidity": 0.30, "body": 0.90, "sweetness": 0.35, "earthiness": 0.90, "brightness": 0.20, "variety": "robusta"},
    "arid_steppe":     {"acidity": 0.55, "body": 0.65, "sweetness": 0.50, "earthiness": 0.70, "brightness": 0.40, "variety": "liberica"},
    "canyon":          {"acidity": 0.50, "body": 0.75, "sweetness": 0.40, "earthiness": 0.85, "brightness": 0.35, "variety": "liberica"},
    "beach":           {"acidity": 0.85, "body": 0.40, "sweetness": 0.90, "earthiness": 0.10, "brightness": 0.95, "variety": "arabica"},
    # New 5
    "tundra":          {"acidity": 0.80, "body": 0.30, "sweetness": 0.60, "earthiness": 0.15, "brightness": 0.90, "variety": "arabica"},
    "swamp":           {"acidity": 0.20, "body": 0.95, "sweetness": 0.30, "earthiness": 0.95, "brightness": 0.15, "variety": "robusta"},
    "alpine_mountain": {"acidity": 0.90, "body": 0.45, "sweetness": 0.70, "earthiness": 0.20, "brightness": 0.85, "variety": "arabica"},
    "rocky_mountain":  {"acidity": 0.45, "body": 0.80, "sweetness": 0.35, "earthiness": 0.80, "brightness": 0.25, "variety": "liberica"},
    "rolling_hills":   {"acidity": 0.55, "body": 0.60, "sweetness": 0.65, "earthiness": 0.45, "brightness": 0.55, "variety": "arabica"},
    "boreal":          {"acidity": 0.35, "body": 0.80, "sweetness": 0.40, "earthiness": 0.85, "brightness": 0.25, "variety": "robusta"},
}

_FLAVOR_POOLS = {
    "acidity":    ["citrus", "lemon zest", "bright cherry", "green apple", "tamarind", "passion fruit"],
    "body":       ["dark chocolate", "molasses", "walnut", "heavy cream", "black tea", "toffee"],
    "sweetness":  ["caramel", "honey", "ripe berry", "brown sugar", "vanilla", "dried fig"],
    "earthiness": ["cedar", "tobacco", "forest floor", "dried herb", "mushroom", "dark soil"],
    "brightness": ["floral", "jasmine", "bergamot", "stone fruit", "rose hip", "elderflower"],
}

# Exclusive notes unlocked by processing method
_PROCESSING_NOTES = {
    "washed":    ["clean finish", "crisp acidity", "tea-like clarity"],
    "natural":   ["fermented", "peach", "wine", "blueberry", "tropical funk"],
    "honey":     ["honey", "apricot", "nectarine", "white grape"],
    "anaerobic": ["lactic funk", "tropical fruit", "wine-like", "effervescent", "wild yeast"],
}

ROAST_LEVEL_DESCS = {
    "green":   "Unroasted — grassy, raw",
    "light":   "Light Roast — bright, delicate, tea-like",
    "medium":  "Medium Roast — balanced, caramel, full flavour",
    "dark":    "Dark Roast — bold, smoky, low acidity",
    "charred": "Charred — burnt, bitter, ashy",
    "ruined":  "Ruined — fermentation gone wrong",
}

ROAST_COLORS = {
    "green":   ( 90, 140,  70),
    "light":   (185, 130,  60),
    "medium":  (130,  80,  35),
    "dark":    ( 60,  35,  15),
    "charred": ( 25,  15,   8),
    "ruined":  ( 80, 100,  40),
}

PROCESSING_METHODS = {
    "washed": {
        "label": "Washed",
        "desc":  "Pulped and dried on raised beds. Clean, bright, acidity-forward.",
        "acidity": +0.15, "body": -0.05, "sweetness": -0.08, "earthiness": -0.15, "brightness": +0.10,
    },
    "natural": {
        "label": "Natural",
        "desc":  "Dried whole on the cherry. Fruity, fermented, heavy sweetness.",
        "acidity": -0.10, "body": +0.10, "sweetness": +0.20, "earthiness": +0.08, "brightness": -0.05,
    },
    "honey": {
        "label": "Honey",
        "desc":  "Pulped but dried with mucilage intact. Sweet and complex.",
        "acidity": +0.05, "body": +0.05, "sweetness": +0.15, "earthiness": -0.05, "brightness": +0.05,
    },
    "anaerobic": {
        "label": "Anaerobic",
        "desc":  "Sealed oxygen-deprived fermentation. Intense, volatile. 20% failure chance.",
        "acidity": -0.05, "body": +0.15, "sweetness": +0.30, "earthiness": +0.05, "brightness": +0.05,
        "variance_mult": 2.5,   # re-jitters all attributes after base modifier
        "failure_chance": 0.20, # chance the batch is ruined → vinegar_brew item
    },
}

GRIND_SIZES = {
    "coarse": {"label": "Coarse",  "desc": "Longer extraction, softer flavour.",  "duration_mult": 1.25, "intensity_mult": 0.85},
    "medium": {"label": "Medium",  "desc": "Balanced extraction.",                "duration_mult": 1.00, "intensity_mult": 1.00},
    "fine":   {"label": "Fine",    "desc": "Fast, concentrated, bold hit.",       "duration_mult": 0.75, "intensity_mult": 1.30},
}

WATER_QUALITIES = {
    "soft":     {"label": "Soft",     "desc": "Low mineral. Highlights acidity and brightness.",  "duration_mult": 1.00, "quality_bonus": 0.05},
    "hard":     {"label": "Hard",     "desc": "High mineral. Boosts body, mutes brightness.",     "duration_mult": 1.15, "quality_bonus": -0.03},
    "filtered": {"label": "Filtered", "desc": "Neutral. Small quality improvement across the board.", "duration_mult": 1.05, "quality_bonus": 0.10},
}

# All discoverable codex entries: "biome_roastlevel"
_CODEX_BIOMES = ["tropical", "jungle", "savanna", "wetland", "arid_steppe", "canyon", "beach",
                 "tundra", "swamp", "alpine_mountain", "rocky_mountain", "rolling_hills", "boreal"]
COFFEE_TYPE_ORDER = [
    f"{biome}_{roast}"
    for biome in _CODEX_BIOMES
    for roast in ["light", "medium", "dark", "charred", "green"]
]


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def apply_processing(bean: "CoffeeBean", method: str) -> bool:
    """Mutates bean attributes based on processing method; called before roasting.
    Returns False if the batch was ruined (anaerobic failure); caller should handle."""
    mods = PROCESSING_METHODS.get(method)
    if not mods:
        return True
    bean.processing_method = method
    bean.acidity    = _clamp(bean.acidity    + mods["acidity"])
    bean.body       = _clamp(bean.body       + mods["body"])
    bean.sweetness  = _clamp(bean.sweetness  + mods["sweetness"])
    bean.earthiness = _clamp(bean.earthiness + mods["earthiness"])
    bean.brightness = _clamp(bean.brightness + mods["brightness"])

    # Anaerobic: secondary jitter pass and possible failure
    if method == "anaerobic":
        rng = random.Random(bean.seed ^ 0xA3B7)
        if rng.random() < mods["failure_chance"]:
            bean.roast_level = "ruined"
            bean.flavor_notes = ["acetic acid", "over-fermented"]
            return False  # ruined batch
        sigma = 0.08 * mods["variance_mult"]
        for attr in ("acidity", "body", "sweetness", "earthiness", "brightness"):
            setattr(bean, attr, _clamp(getattr(bean, attr) + rng.gauss(0, sigma)))

    return True


def generate_flavor_notes(bean: "CoffeeBean") -> list:
    rng = random.Random(hash((bean.seed, "flavor")))
    notes = []
    for attr, pool in _FLAVOR_POOLS.items():
        val = getattr(bean, attr)
        if val > 0.6:
            notes.append(rng.choice(pool))
    # Processing method exclusive notes
    if bean.processing_method in _PROCESSING_NOTES:
        proc_pool = _PROCESSING_NOTES[bean.processing_method]
        notes.append(rng.choice(proc_pool))
    # Roast modulation
    if bean.roast_level == "charred":
        return ["ash", "bitter carbon"]
    if bean.roast_level == "dark":
        for e in ["smoky", "roasted grain"]:
            if e not in notes:
                notes.append(e)
    elif bean.roast_level == "light":
        for e in ["grassy", "tea-like"]:
            if e not in notes:
                notes.append(e)
    # Deduplicate and cap at 5
    seen = []
    for n in notes:
        if n not in seen:
            seen.append(n)
    return seen[:5] if seen else ["mild"]


class CoffeeGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, biodome: str, terroir: float = 0.0) -> "CoffeeBean":
        """Generate a raw coffee bean. terroir=0 for wild harvest; 0–1 for farmed soil care."""
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid = hashlib.md5(f"coffee_{seed}_{self._counter}".encode()).hexdigest()[:12]

        profile = BIOME_FLAVOR_PROFILES.get(biodome, BIOME_FLAVOR_PROFILES["tropical"])
        rng = random.Random(seed)

        # Well-tended soil narrows jitter (more predictable); 0.08 → 0.03 at max terroir.
        jitter_sigma = 0.08 - terroir * 0.05

        def jitter(base):
            return _clamp(base + rng.gauss(0, jitter_sigma))

        bean = CoffeeBean(
            uid=uid,
            origin_biome=biodome,
            variety=profile["variety"],
            state="raw",
            roast_level="green",
            roast_quality=0.0,
            acidity=jitter(profile["acidity"]),
            body=jitter(profile["body"]),
            sweetness=jitter(profile["sweetness"]),
            earthiness=jitter(profile["earthiness"]),
            brightness=jitter(profile["brightness"]),
            flavor_notes=[],
            seed=seed,
            terroir_quality=terroir,
        )

        # Apply terroir bonuses: fertility → body+sweetness; moisture → acidity+brightness
        if terroir > 0.0:
            # Split terroir into fertility-half and moisture-half for distinct effects
            t = terroir
            bean.body       = _clamp(bean.body       + t * 0.12)
            bean.sweetness  = _clamp(bean.sweetness  + t * 0.10)
            bean.acidity    = _clamp(bean.acidity    + t * 0.08)
            bean.brightness = _clamp(bean.brightness + t * 0.08)
            bean.earthiness = _clamp(bean.earthiness - t * 0.06)  # well-tended = less earthy

        return bean


def apply_roast_result(bean: "CoffeeBean", temp_at_stop: float,
                       timing_score: float, temp_control_score: float,
                       penalties: int):
    if bean.roast_level == "ruined":
        return  # anaerobic failure — already finalized in apply_processing
    if temp_at_stop < 0.25:
        bean.roast_level = "green"
    elif temp_at_stop < 0.45:
        bean.roast_level = "light"
    elif temp_at_stop < 0.65:
        bean.roast_level = "medium"
    elif temp_at_stop < 0.80:
        bean.roast_level = "dark"
    else:
        bean.roast_level = "charred"

    quality = _clamp(timing_score * 0.6 + temp_control_score * 0.4 - penalties * 0.15)
    bean.roast_quality = quality
    bean.state = "roasted"
    bean.flavor_notes = generate_flavor_notes(bean)


def make_blend(components: list) -> "CoffeeBean":
    import hashlib as _hlib
    n = len(components)
    seed = sum(b.seed for b in components) // n
    uid = _hlib.md5(f"blend_{'_'.join(b.uid for b in components)}".encode()).hexdigest()[:12]

    def avg(attr):
        return _clamp(sum(getattr(b, attr) for b in components) / n)

    roast_counts = {}
    for b in components:
        roast_counts[b.roast_level] = roast_counts.get(b.roast_level, 0) + 1
    dominant_roast = max(roast_counts, key=roast_counts.get)

    all_notes = []
    for b in components:
        for note in b.flavor_notes:
            if note not in all_notes:
                all_notes.append(note)

    bean = CoffeeBean(
        uid=uid,
        origin_biome="blend",
        variety="blend",
        state="blended",
        roast_level=dominant_roast,
        roast_quality=avg("roast_quality"),
        acidity=avg("acidity"),
        body=avg("body"),
        sweetness=avg("sweetness"),
        earthiness=avg("earthiness"),
        brightness=avg("brightness"),
        flavor_notes=all_notes[:5],
        seed=seed,
        blend_components=[b.uid for b in components],
    )
    return bean


def get_brew_output_id(method: str, roast_quality: float, herb: str = "") -> str:
    if roast_quality >= 0.7:
        tier = "_superior"
    elif roast_quality >= 0.4:
        tier = "_fine"
    else:
        tier = ""
    if herb and herb in HERB_PAIRINGS:
        return f"{method}{tier}_{herb}"
    return f"{method}{tier}"


def get_brew_duration_multiplier(water_quality: str, grind_size: str) -> float:
    wq = WATER_QUALITIES.get(water_quality, WATER_QUALITIES["soft"])
    gs = GRIND_SIZES.get(grind_size, GRIND_SIZES["medium"])
    return wq["duration_mult"] * gs["duration_mult"]


def get_brew_quality_bonus(water_quality: str) -> float:
    wq = WATER_QUALITIES.get(water_quality, WATER_QUALITIES["soft"])
    return wq.get("quality_bonus", 0.0)


BREW_METHODS = {
    "drip_coffee":  {"label": "Drip",         "buff": "focus",     "amplifies": ("sweetness", "brightness"), "suppresses": ("earthiness",)},
    "espresso":     {"label": "Espresso",      "buff": "rush",      "amplifies": ("body", "acidity"),         "suppresses": ("brightness",)},
    "pour_over":    {"label": "Pour Over",     "buff": "clarity",   "amplifies": ("acidity", "brightness"),   "suppresses": ("body",)},
    "cold_brew":    {"label": "Cold Brew",     "buff": "endurance", "amplifies": ("sweetness", "body"),       "suppresses": ("brightness",)},
    "french_press": {"label": "French Press",  "buff": "strength",  "amplifies": ("body", "earthiness"),      "suppresses": ("acidity",)},
}

BUFF_DESCS = {
    "focus":     "Mining speed +20%",
    "rush":      "Move speed +25%",
    "clarity":   "Collect radius +50%",
    "endurance": "Hunger drain -40%",
    "strength":  "Pick power +1",
}

# Dried herbs that can be added to brews; each gives a secondary herb_buff
# at 40% of the standard potion duration.
HERB_PAIRINGS = {
    "dried_ginger":    {"name": "Ginger",    "herb_buff": "haste",      "herb_buff_duration": 24.0, "note": "warming spice"},
    "dried_mint":      {"name": "Mint",      "herb_buff": "keen_eye",   "herb_buff_duration": 36.0, "note": "cool clarity"},
    "dried_rosemary":  {"name": "Rosemary",  "herb_buff": "focus",      "herb_buff_duration": 36.0, "note": "woodsy lift"},
    "dried_lavender":  {"name": "Lavender",  "herb_buff": "soothing",   "herb_buff_duration": 36.0, "note": "floral calm"},
    "dried_chamomile": {"name": "Chamomile", "herb_buff": "resilience", "herb_buff_duration": 36.0, "note": "gentle body"},
    "dried_garlic":    {"name": "Garlic",    "herb_buff": "fortune",    "herb_buff_duration": 48.0, "note": "pungent earth"},
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
    "boreal":          "Boreal",
    "blend":           "Blend",
}
