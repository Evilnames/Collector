import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class Cheese:
    uid:             str
    origin_biome:    str
    animal_type:     str    # "cow" | "goat" | "sheep"
    variety:         str    # biome signature variety
    state:           str    # "milk" | "curd" | "pressed" | "aged"
    richness:        float  # creaminess / fat content
    sharpness:       float  # intensity / bite
    nuttiness:       float  # earthy / toasted depth
    saltiness:       float  # brine character
    moisture:        float  # decreases with aging
    culture_quality: float  # score from Dairy Vat mini-game
    age_quality:     float  # score from Aging Cave
    flavor_notes:    list
    seed:            int
    blend_components: list = field(default_factory=list)
    cheese_type:      str   = ""   # set at press: fresh|soft_ripened|washed_rind|pressed|aged_hard|blue
    press_quality:    float = 0.0  # score from Cheese Press mini-game


# Base milk profiles per animal type (richness, sharpness, nuttiness, saltiness, moisture)
ANIMAL_MILK_PROFILES = {
    "cow":   {"richness": 0.65, "sharpness": 0.35, "nuttiness": 0.50, "saltiness": 0.45, "moisture": 0.80},
    "goat":  {"richness": 0.40, "sharpness": 0.70, "nuttiness": 0.30, "saltiness": 0.55, "moisture": 0.75},
    "sheep": {"richness": 0.80, "sharpness": 0.50, "nuttiness": 0.65, "saltiness": 0.50, "moisture": 0.70},
}

# Biome flavor offsets and signature variety (applied on top of animal base)
BIOME_CHEESE_PROFILES = {
    "tropical":        {"richness": +0.05, "sharpness": -0.10, "nuttiness": -0.05, "saltiness":  0.00, "variety": "queso_fresco"},
    "jungle":          {"richness": +0.10, "sharpness": -0.05, "nuttiness": +0.05, "saltiness": -0.05, "variety": "brie"},
    "savanna":         {"richness":  0.00, "sharpness": +0.05, "nuttiness": +0.10, "saltiness":  0.00, "variety": "gouda"},
    "wetland":         {"richness": -0.05, "sharpness": +0.15, "nuttiness": +0.05, "saltiness": +0.05, "variety": "gorgonzola"},
    "arid_steppe":     {"richness": +0.05, "sharpness": +0.10, "nuttiness": +0.15, "saltiness": +0.05, "variety": "manchego"},
    "canyon":          {"richness": -0.05, "sharpness": +0.20, "nuttiness": +0.10, "saltiness": +0.10, "variety": "aged_jack"},
    "beach":           {"richness": -0.10, "sharpness": +0.15, "nuttiness": -0.05, "saltiness": +0.20, "variety": "feta"},
    "tundra":          {"richness": +0.10, "sharpness": -0.05, "nuttiness": +0.05, "saltiness": -0.05, "variety": "havarti"},
    "swamp":           {"richness": +0.05, "sharpness": +0.10, "nuttiness":  0.00, "saltiness": +0.10, "variety": "taleggio"},
    "alpine_mountain": {"richness": +0.05, "sharpness": +0.10, "nuttiness": +0.20, "saltiness":  0.00, "variety": "gruyere"},
    "rocky_mountain":  {"richness": -0.05, "sharpness": +0.20, "nuttiness": +0.10, "saltiness": +0.05, "variety": "roquefort"},
    "rolling_hills":   {"richness": +0.05, "sharpness": +0.15, "nuttiness": +0.10, "saltiness": +0.05, "variety": "cheddar"},
    "boreal":          {"richness":  0.00, "sharpness": +0.05, "nuttiness": +0.15, "saltiness": +0.10, "variety": "smoked_edam"},
}

_FLAVOR_POOLS = {
    "richness":  ["cream", "butter", "whole milk", "triple cream", "lard"],
    "sharpness": ["sharp bite", "piquant", "tang", "aged vinegar", "barnyard"],
    "nuttiness": ["toasted hazelnut", "walnut", "browned butter", "roasted grain"],
    "saltiness": ["sea salt", "brine", "salted caramel", "mineral"],
    "moisture":  ["fresh curd", "milky", "whey", "young rind", "cave damp"],
}

CHEESE_TYPE_DESCS = {
    "fresh":        "Fresh — milky, high-moisture, mild",
    "soft_ripened": "Soft-Ripened — creamy, bloomy rind",
    "washed_rind":  "Washed-Rind — pungent, orange rind",
    "pressed":      "Pressed — firm, moderate flavour",
    "aged_hard":    "Aged Hard — sharp, crystalline",
    "blue":         "Blue-Veined — complex, bold",
    "smoked":       "Smoked — smoky, dense, warming",
    "stretched":    "Stretched — elastic, milky, fresh",
    "brined":       "Brined — salty, crumbly, tangy",
    "herb_crusted": "Herb-Crusted — aromatic, green rind",
    "double_cream": "Double Cream — ultra-rich, lush",
    "truffled":     "Truffled — earthy, rare, complex",
    "ash_coated":   "Ash-Coated — mineral, sharp, grey rind",
    "alpine":       "Alpine — nutty, firm, with holes",
    "clothbound":   "Clothbound — artisan wrapped, dense",
    "cream":        "Cream — spreadable, light, fresh",
    "monastery":    "Monastery — beer-washed, yeasty, amber",
    "cured":        "Cured — dried hard, peppery rind",
}

CHEESE_TYPE_COLORS = {
    "fresh":        (245, 242, 225),
    "soft_ripened": (240, 235, 200),
    "washed_rind":  (210, 150,  80),
    "pressed":      (220, 185, 100),
    "aged_hard":    (190, 155,  70),
    "blue":         (160, 155, 140),
    "smoked":       (130, 100,  65),
    "stretched":    (252, 248, 230),
    "brined":       (235, 225, 195),
    "herb_crusted": (175, 190, 135),
    "double_cream": (252, 246, 218),
    "truffled":     (145, 125, 105),
    "ash_coated":   (158, 152, 148),
    "alpine":       (225, 210, 155),
    "clothbound":   (175, 140,  80),
    "cream":        (255, 252, 242),
    "monastery":    (165, 120,  70),
    "cured":        (155, 118,  55),
}

# Aging cycles required per cheese type
CHEESE_TYPE_AGING = {
    "fresh":        0,
    "soft_ripened": 1,
    "washed_rind":  2,
    "pressed":      3,
    "aged_hard":    5,
    "blue":         4,
    "smoked":       3,
    "stretched":    1,
    "brined":       2,
    "herb_crusted": 2,
    "double_cream": 1,
    "truffled":     4,
    "ash_coated":   3,
    "alpine":       4,
    "clothbound":   5,
    "cream":        0,
    "monastery":    3,
    "cured":        4,
}

# Moisture drop applied at press stage
CHEESE_TYPE_MOISTURE_DROP = {
    "fresh":        0.00,
    "soft_ripened": 0.15,
    "washed_rind":  0.25,
    "pressed":      0.35,
    "aged_hard":    0.50,
    "blue":         0.30,
    "smoked":       0.30,
    "stretched":    0.10,
    "brined":       0.20,
    "herb_crusted": 0.20,
    "double_cream": 0.05,
    "truffled":     0.40,
    "ash_coated":   0.35,
    "alpine":       0.40,
    "clothbound":   0.45,
    "cream":        0.00,
    "monastery":    0.25,
    "cured":        0.50,
}

# Optional ingredients consumed at the Cheese Press for a quality bonus.
# Any item in the list qualifies; the first one found in inventory is used.
CHEESE_PRESS_INGREDIENTS = {
    "smoked":       {"items": ["coal"],                                                 "bonus": 0.12, "label": "Coal"},
    "herb_crusted": {"items": ["dried_chamomile", "dried_lavender", "dried_mint", "dried_rosemary",
                               "chamomile", "lavender", "mint", "rosemary"],            "bonus": 0.15, "label": "Herb"},
    "monastery":    {"items": ["red_wine", "white_wine", "rose_wine", "pear_wine",
                               "spirit_bourbon", "spirit_whisky", "spirit_gin"],        "bonus": 0.15, "label": "Wine/Spirit"},
    "truffled":     {"items": ["mushroom", "dried_mushroom"],                           "bonus": 0.15, "label": "Mushroom"},
    "ash_coated":   {"items": ["coal", "stone_chip"],                                   "bonus": 0.08, "label": "Ash/Stone"},
    "blue":         {"items": ["coal", "stone_chip"],                                   "bonus": 0.10, "label": "Cave Salt"},
}

BUFF_DESCS = {
    "satiation":  "Hunger drain -40%",
    "vitality":   "Health regen +1 HP/tick",
    "keenness":   "Mining speed +15%",
    "abundance":  "Harvest yield +20%",
    "nimbleness": "Move speed +20%",
    "resilience": "Instant +5 health on eat",
    "vigor":      "Pick power +1",
}

_CODEX_BIOMES = [
    "tropical", "jungle", "savanna", "wetland", "arid_steppe", "canyon", "beach",
    "tundra", "swamp", "alpine_mountain", "rocky_mountain", "rolling_hills", "boreal",
]

# Codex entries: biome × cheese_type (animal_type tracked but not as separate codex axis)
CHEESE_TYPE_ORDER = [
    f"{biome}_{ct}"
    for biome in _CODEX_BIOMES
    for ct in CHEESE_TYPE_DESCS
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


def generate_flavor_notes(cheese: "Cheese") -> list:
    rng = random.Random(hash((cheese.seed, "cheese_flavor")))
    notes = []
    for attr, pool in _FLAVOR_POOLS.items():
        val = getattr(cheese, attr)
        if val > 0.6:
            notes.append(rng.choice(pool))
    if cheese.cheese_type == "blue":
        notes.append(rng.choice(["blue mold", "cave mustiness", "earthy blue"]))
    elif cheese.cheese_type == "washed_rind":
        notes.append(rng.choice(["funky rind", "straw", "meaty"]))
    elif cheese.cheese_type in ("aged_hard", "pressed"):
        notes.append(rng.choice(["crystalline", "crumbly paste", "cave-aged"]))
    elif cheese.cheese_type == "smoked":
        notes.append(rng.choice(["woodsmoke", "char", "campfire", "hickory"]))
    elif cheese.cheese_type == "stretched":
        notes.append(rng.choice(["fresh milk", "elastic", "clean finish"]))
    elif cheese.cheese_type == "brined":
        notes.append(rng.choice(["sharp brine", "pickled", "sea salt crust"]))
    elif cheese.cheese_type == "herb_crusted":
        notes.append(rng.choice(["dried thyme", "rosemary crust", "lavender", "meadow herbs"]))
    elif cheese.cheese_type == "double_cream":
        notes.append(rng.choice(["clotted cream", "rich butter", "silky paste"]))
    elif cheese.cheese_type == "truffled":
        notes.append(rng.choice(["black truffle", "forest floor", "deep earth", "mushroom"]))
    elif cheese.cheese_type == "ash_coated":
        notes.append(rng.choice(["mineral ash", "clean slate", "grey dust", "vegetal char"]))
    elif cheese.cheese_type == "alpine":
        notes.append(rng.choice(["mountain hay", "sweet grass", "nutty paste", "mild sweetness"]))
    elif cheese.cheese_type == "clothbound":
        notes.append(rng.choice(["aged cloth", "dense core", "earthy paste", "cave cured"]))
    elif cheese.cheese_type == "cream":
        notes.append(rng.choice(["silky", "mild tang", "fresh dairy", "butter"]))
    elif cheese.cheese_type == "monastery":
        notes.append(rng.choice(["beer-washed", "yeasty crust", "amber rind", "malty"]))
    elif cheese.cheese_type == "cured":
        notes.append(rng.choice(["peppery rind", "dry paste", "aged salt", "crumbled"]))
    seen = []
    for n in notes:
        if n not in seen:
            seen.append(n)
    return seen[:5] if seen else ["mild"]


class CheeseGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter    = 0

    def generate(self, biodome: str, animal_type: str) -> "Cheese":
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid  = hashlib.md5(f"cheese_{seed}_{self._counter}".encode()).hexdigest()[:12]

        animal = ANIMAL_MILK_PROFILES.get(animal_type, ANIMAL_MILK_PROFILES["cow"])
        biome  = BIOME_CHEESE_PROFILES.get(biodome, BIOME_CHEESE_PROFILES["rolling_hills"])
        rng    = random.Random(seed)

        def jitter(base):
            return _clamp(base + rng.gauss(0, 0.06))

        return Cheese(
            uid             = uid,
            origin_biome    = biodome,
            animal_type     = animal_type,
            variety         = biome["variety"],
            state           = "milk",
            richness        = jitter(_clamp(animal["richness"]  + biome["richness"])),
            sharpness       = jitter(_clamp(animal["sharpness"] + biome["sharpness"])),
            nuttiness       = jitter(_clamp(animal["nuttiness"] + biome["nuttiness"])),
            saltiness       = jitter(_clamp(animal["saltiness"] + biome["saltiness"])),
            moisture        = jitter(animal["moisture"]),
            culture_quality = 0.0,
            age_quality     = 0.0,
            flavor_notes    = [],
            seed            = seed,
        )


def apply_curd_result(cheese: "Cheese", temp_score: float, culture_score: float, penalties: int):
    quality = _clamp(temp_score * 0.5 + culture_score * 0.5 - penalties * 0.12)
    cheese.culture_quality = quality
    cheese.state = "curd"


def apply_press_result(cheese: "Cheese", cheese_type: str, pressure_score: float):
    cheese.cheese_type  = cheese_type
    cheese.press_quality = _clamp(pressure_score)
    cheese.moisture = _clamp(cheese.moisture - CHEESE_TYPE_MOISTURE_DROP.get(cheese_type, 0.20))
    cheese.state = "pressed"


def apply_aging_result(cheese: "Cheese", duration_cycles: int, care_bonus: float):
    age_factor       = min(1.0, duration_cycles / 5.0)
    cheese.sharpness = _clamp(cheese.sharpness + age_factor * 0.20)
    cheese.nuttiness = _clamp(cheese.nuttiness + age_factor * 0.15)
    cheese.moisture  = _clamp(cheese.moisture  - age_factor * 0.10)
    cheese.age_quality = _clamp(age_factor * 0.6 + care_bonus * 0.4)
    cheese.state     = "aged"
    cheese.flavor_notes = generate_flavor_notes(cheese)


def get_cheese_output_id(cheese_type: str, culture_quality: float, press_quality: float, age_quality: float) -> str:
    total = (culture_quality + press_quality + age_quality) / 3.0
    if total >= 0.70:
        tier = "_superior"
    elif total >= 0.45:
        tier = "_fine"
    else:
        tier = ""
    if cheese_type == "fresh":
        return "cheese_fresh"
    return f"cheese_{cheese_type}{tier}"
