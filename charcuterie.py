"""Charcuterie system — salt-cured and aged meat collectibles."""
import hashlib
import random
import time
from dataclasses import dataclass, field


@dataclass
class CuredMeat:
    uid:              str
    meat_source:      str    # raw item key e.g. "raw_boar_meat"
    cure_type:        str    # "prosciutto" | "salami" | "jerky" | "lardo"
    state:            str    # "salted" | "aging" | "finished"
    salt_penetration: float  # 0.0–1.0  how deeply the cure worked in
    spice_intensity:  float  # 0.0–1.0  strength of spice/herb notes
    fat_content:      float  # 0.0–1.0  derived from meat source
    age_quality:      float  # 0.0–1.0  final quality computed at retrieval
    cure_method:      str    # "dry_salt" | "spice_rub" | "herb_cure" | "smoke"
    age_start_time:   float  # Unix timestamp; 0.0 while still salted
    age_total_days:   int    # real-days target (per CURE_TYPES)
    flavor_notes:     list
    seed:             int
    blend_components: list = field(default_factory=list)
    smoke_wood:       str = ""     # "apple" | "hickory" | "cherry" | "oak" (only when method=smoke)
    breed_bonus:      float = 0.0  # 0.0–0.3 quality bonus from prize pig breeding


# ---------------------------------------------------------------------------
# Meat source profiles — keyed by existing item key
# ---------------------------------------------------------------------------
MEAT_SOURCES = {
    "raw_boar_meat": {
        "display":        "Boar",
        "fat":            0.65,
        "protein":        0.60,
        "eligible_cures": ["prosciutto", "salami", "jerky", "lardo", "pancetta"],
    },
    "raw_pork": {
        "display":        "Pork",
        "fat":            0.45,
        "protein":        0.55,
        "eligible_cures": ["prosciutto", "salami", "jerky", "pancetta"],
    },
    "lard": {
        "display":        "Lard (Fatback)",
        "fat":            0.95,
        "protein":        0.05,
        "eligible_cures": ["lardo"],
    },
    "raw_beef": {
        "display":        "Beef",
        "fat":            0.25,
        "protein":        0.75,
        "eligible_cures": ["salami", "jerky"],
    },
    "raw_venison": {
        "display":        "Venison",
        "fat":            0.10,
        "protein":        0.80,
        "eligible_cures": ["jerky", "salami"],
    },
    "raw_bison_meat": {
        "display":        "Bison",
        "fat":            0.20,
        "protein":        0.78,
        "eligible_cures": ["jerky", "salami"],
    },
    "raw_mutton": {
        "display":        "Mutton",
        "fat":            0.45,
        "protein":        0.65,
        "eligible_cures": ["jerky", "salami"],
    },
    "raw_bear_meat": {
        "display":        "Bear",
        "fat":            0.30,
        "protein":        0.70,
        "eligible_cures": ["jerky"],
    },
}

MEAT_DISPLAY_NAMES = {k: v["display"] for k, v in MEAT_SOURCES.items()}


# ---------------------------------------------------------------------------
# Cure types
# ---------------------------------------------------------------------------
CURE_TYPES = {
    "prosciutto": {
        "label":          "Prosciutto",
        "desc":           "Dry-cured whole leg. Long aging, delicate fat-laced slices.",
        "salt_req":       0.50,
        "age_days":       16,
        "eligible_meats": {"raw_boar_meat"},
    },
    "salami":     {
        "label":          "Salami",
        "desc":           "Ground and spiced, fermented in the casing. Rich and bold.",
        "salt_req":       0.40,
        "age_days":       8,
        "eligible_meats": {"raw_boar_meat", "raw_beef", "raw_venison",
                           "raw_bison_meat", "raw_mutton"},
    },
    "jerky":      {
        "label":          "Jerky",
        "desc":           "Thin strips dried hard. Portable, intensely savoury.",
        "salt_req":       0.55,
        "age_days":       2,
        "eligible_meats": {"raw_boar_meat", "raw_beef", "raw_venison",
                           "raw_bison_meat", "raw_mutton", "raw_bear_meat"},
    },
    "lardo":      {
        "label":          "Lardo",
        "desc":           "Pure fatback cured with herbs and spice. Silky and aromatic.",
        "salt_req":       0.35,
        "age_days":       12,
        "eligible_meats": {"raw_boar_meat", "lard"},
    },
    "pancetta":   {
        "label":          "Pancetta",
        "desc":           "Cured pork belly, rolled and aged. Rich, buttery, peppery.",
        "salt_req":       0.45,
        "age_days":       10,
        "eligible_meats": {"raw_boar_meat", "raw_pork"},
    },
    "bacon":      {
        "label":          "Bacon",
        "desc":           "Smoke-cured pork belly. Fast cure, savoury and crisp.",
        "salt_req":       0.50,
        "age_days":       3,
        "eligible_meats": {"raw_pork", "raw_boar_meat"},
        "required_method": "smoke",  # smoke method is mandatory
    },
    "sausage":    {
        "label":          "Sausage",
        "desc":           "Ground meat packed in casings. Quick fermentation.",
        "salt_req":       0.35,
        "age_days":       5,
        "eligible_meats": {"raw_pork", "raw_boar_meat", "raw_beef",
                           "raw_venison", "raw_bison_meat"},
        "required_extra": "sausage_casing",  # one casing per sausage
    },
}

CURE_ORDER = ["prosciutto", "salami", "jerky", "lardo", "pancetta", "bacon", "sausage"]


# ---------------------------------------------------------------------------
# Cure methods — modify salt_penetration and spice_intensity
# ---------------------------------------------------------------------------
CURE_METHODS = {
    "dry_salt":  {
        "label":            "Dry Salt",
        "desc":             "Pure salt rub. Deepest penetration, clean flavour.",
        "salt_penetration": +0.18,
        "spice_intensity":  -0.05,
    },
    "spice_rub": {
        "label":            "Spice Rub",
        "desc":             "Salt with crushed spices. Bold spice intensity.",
        "salt_penetration": +0.05,
        "spice_intensity":  +0.22,
    },
    "herb_cure": {
        "label":            "Herb Cure",
        "desc":             "Salt blended with dried herbs. Balanced and fragrant.",
        "salt_penetration": +0.08,
        "spice_intensity":  +0.12,
    },
    "smoke":     {
        "label":            "Smoke",
        "desc":             "Salt and slow smoke. Penetrating and preserving.",
        "salt_penetration": +0.12,
        "spice_intensity":  +0.08,
    },
}

CURE_METHOD_ORDER = ["dry_salt", "spice_rub", "herb_cure", "smoke"]


# ---------------------------------------------------------------------------
# Smoking woods — only consulted when cure_method == "smoke"
# ---------------------------------------------------------------------------
SMOKE_WOODS = {
    "apple":   {
        "label":            "Applewood",
        "item":             "smoking_chips_apple",
        "desc":             "Mild, fruity, slightly sweet. Pairs beautifully with pork.",
        "salt_penetration": +0.02,
        "spice_intensity":  +0.04,
        "quality_bonus":    +0.04,
        "notes":            ["sweet applewood", "fruit smoke", "mellow sweetness"],
    },
    "hickory": {
        "label":            "Hickory",
        "item":             "smoking_chips_hickory",
        "desc":             "Strong, bold, classic bacon smoke.",
        "salt_penetration": +0.06,
        "spice_intensity":  +0.06,
        "quality_bonus":    +0.05,
        "notes":            ["bold hickory", "deep smoke", "savory char"],
    },
    "cherry":  {
        "label":            "Cherry",
        "item":             "smoking_chips_cherry",
        "desc":             "Subtle fruit-sweet smoke with a rosy hue on the meat.",
        "salt_penetration": +0.03,
        "spice_intensity":  +0.05,
        "quality_bonus":    +0.06,
        "notes":            ["cherry smoke", "rose-tinted bark", "stone-fruit warmth"],
    },
    "oak":     {
        "label":            "Oak",
        "item":             "smoking_chips_oak",
        "desc":             "Balanced, traditional, long-lasting smoke flavour.",
        "salt_penetration": +0.05,
        "spice_intensity":  +0.05,
        "quality_bonus":    +0.05,
        "notes":            ["oak smoke", "tannin warmth", "barrel-room depth"],
    },
}

SMOKE_WOOD_ORDER = ["apple", "hickory", "cherry", "oak"]


# ---------------------------------------------------------------------------
# Buffs
# ---------------------------------------------------------------------------
BUFF_DESCS = {
    "preservation": "Preservation — food freshness +20%",
    "sustenance":   "Sustenance — hunger restore +15%",
    "vitality":     "Vitality — movement speed +12% for 60 s",
    "fortitude":    "Fortitude — mining speed +18% for 60 s",
    "decadence":    "Decadence — XP gain +25% for 90 s",
    "hearty":       "Hearty — health regen +0.5/s for 60 s",
    "stamina":      "Stamina — sprint stamina drain −30% for 60 s",
}

CURE_TYPE_BUFFS = {
    "prosciutto": "preservation",
    "salami":     "sustenance",
    "jerky":      "vitality",
    "lardo":      "fortitude",
    "pancetta":   "decadence",
    "bacon":      "hearty",
    "sausage":    "stamina",
}


# ---------------------------------------------------------------------------
# Output items
# ---------------------------------------------------------------------------
OUTPUT_DESCS = {
    "prosciutto":           "Prosciutto — long-aged dry-cured leg, paper-thin slices",
    "prosciutto_fine":      "Prosciutto (Fine) — silky, translucent rose-coloured slices",
    "prosciutto_superior":  "Prosciutto (Superior) — melt-on-tongue artisan reserve",
    "salami":               "Salami — spiced ground meat, firm and tangy",
    "salami_fine":          "Salami (Fine) — full-flavoured with a clean finish",
    "salami_superior":      "Salami (Superior) — aged reserve, intense and complex",
    "jerky":                "Jerky — tough chewy strips, deeply savoury",
    "jerky_fine":           "Jerky (Fine) — tender spiced strips, smoky depth",
    "jerky_superior":       "Jerky (Superior) — prime cut, well-seasoned masterwork",
    "lardo":                "Lardo — silky herb-cured fatback, aromatic",
    "lardo_fine":           "Lardo (Fine) — fragrant cured fat with herbal notes",
    "lardo_superior":       "Lardo (Superior) — reserved fatback, floral and rich",
    "pancetta":             "Pancetta — rolled cured pork belly, peppery edge",
    "pancetta_fine":        "Pancetta (Fine) — buttery belly with spiced crust",
    "pancetta_superior":    "Pancetta (Superior) — silken artisan-rolled reserve",
    "bacon":                "Bacon — smoke-cured pork belly strips",
    "bacon_fine":           "Bacon (Fine) — applewood-rich, lacquered edges",
    "bacon_superior":       "Bacon (Superior) — perfectly streaked artisan reserve",
    "sausage":              "Sausage — fermented links, garlicky and savoury",
    "sausage_fine":         "Sausage (Fine) — well-spiced fermented links",
    "sausage_superior":     "Sausage (Superior) — heirloom-grind reserve links",
}

OUTPUT_COLORS = {
    "prosciutto":           (210, 120, 100),
    "prosciutto_fine":      (225, 135, 110),
    "prosciutto_superior":  (240, 150, 120),
    "salami":               (155,  60,  55),
    "salami_fine":          (170,  70,  60),
    "salami_superior":      (185,  80,  65),
    "jerky":                (140,  85,  45),
    "jerky_fine":           (155,  95,  50),
    "jerky_superior":       (170, 105,  55),
    "lardo":                (235, 220, 205),
    "lardo_fine":           (245, 232, 218),
    "lardo_superior":       (252, 242, 230),
    "pancetta":             (200, 110,  95),
    "pancetta_fine":        (215, 125, 105),
    "pancetta_superior":    (230, 140, 115),
    "bacon":                (180,  90,  60),
    "bacon_fine":           (195, 100,  70),
    "bacon_superior":       (215, 115,  80),
    "sausage":              (170,  85,  65),
    "sausage_fine":         (185,  95,  75),
    "sausage_superior":     (200, 110,  85),
}


# ---------------------------------------------------------------------------
# Flavor note pools
# ---------------------------------------------------------------------------
_FLAVOR_POOLS = {
    "fat":   ["buttery richness", "marbled fat", "silky mouthfeel", "fatty depth", "creamy finish"],
    "salt":  ["salt-forward", "briny edge", "mineral crust", "saline depth", "clean salt"],
    "spice": ["warming spice", "peppery heat", "aromatic crust", "herbaceous", "juniper note"],
    "age":   ["aged complexity", "concentrated flavour", "nutty depth", "umami richness", "crystalline"],
}
_CURE_METHOD_NOTES = {
    "dry_salt":  ["austere mineral", "clean cure", "salt crystal"],
    "spice_rub": ["spiced crust", "bold pepper", "fragrant coating"],
    "herb_cure": ["rosemary lift", "thyme-scented", "herbal freshness"],
    "smoke":     ["smoky depth", "wood smoke", "charred edge"],
}


# ---------------------------------------------------------------------------
# Codex layout
# ---------------------------------------------------------------------------
_CODEX_MEATS = list(MEAT_SOURCES.keys())
TYPE_ORDER = [
    f"{meat}_{cure}"
    for meat in _CODEX_MEATS
    for cure in CURE_ORDER
]

DISPLAY_NAMES = {**MEAT_DISPLAY_NAMES, **{k: v["label"] for k, v in CURE_TYPES.items()}}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def get_charcuterie_output_id(cure_type: str, quality: float) -> str:
    if quality >= 0.72:
        return f"{cure_type}_superior"
    if quality >= 0.45:
        return f"{cure_type}_fine"
    return cure_type


def age_progress(item: CuredMeat) -> float:
    """Returns 0.0–1.0+ progress. Uses real wall-clock time."""
    if item.state != "aging" or item.age_start_time <= 0.0 or item.age_total_days <= 0:
        return 0.0
    elapsed = time.time() - item.age_start_time
    return elapsed / (item.age_total_days * 86_400)


def compute_age_quality(item: CuredMeat) -> float:
    rng = random.Random(item.seed ^ 0xC4A3)
    base = item.salt_penetration * 0.50 + item.spice_intensity * 0.30
    wood_bonus = SMOKE_WOODS.get(item.smoke_wood, {}).get("quality_bonus", 0.0)
    jit  = rng.gauss(0, 0.06)
    return _clamp(base + wood_bonus + item.breed_bonus + jit)


def generate_flavor_notes(item: CuredMeat) -> list:
    rng = random.Random(hash((item.seed, "char_flavor", item.cure_method, item.cure_type)))
    notes = []
    if item.fat_content > 0.40:
        notes.append(rng.choice(_FLAVOR_POOLS["fat"]))
    if item.salt_penetration > 0.50:
        notes.append(rng.choice(_FLAVOR_POOLS["salt"]))
    if item.spice_intensity > 0.40:
        notes.append(rng.choice(_FLAVOR_POOLS["spice"]))
    if item.age_quality > 0.55:
        notes.append(rng.choice(_FLAVOR_POOLS["age"]))
    if item.cure_method in _CURE_METHOD_NOTES:
        notes.append(rng.choice(_CURE_METHOD_NOTES[item.cure_method]))
    if item.smoke_wood in SMOKE_WOODS:
        notes.append(rng.choice(SMOKE_WOODS[item.smoke_wood]["notes"]))
    seen: list[str] = []
    for n in notes:
        if n not in seen:
            seen.append(n)
    return seen[:4] if seen else ["salt-cured"]


# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------
def apply_cure_method(item: CuredMeat, method_key: str, smoke_wood: str = "") -> None:
    mods = CURE_METHODS.get(method_key)
    if not mods:
        return
    item.cure_method      = method_key
    item.salt_penetration = _clamp(item.salt_penetration + mods["salt_penetration"])
    item.spice_intensity  = _clamp(item.spice_intensity  + mods["spice_intensity"])
    if method_key == "smoke" and smoke_wood in SMOKE_WOODS:
        wm = SMOKE_WOODS[smoke_wood]
        item.smoke_wood       = smoke_wood
        item.salt_penetration = _clamp(item.salt_penetration + wm["salt_penetration"])
        item.spice_intensity  = _clamp(item.spice_intensity  + wm["spice_intensity"])


def start_aging(item: CuredMeat) -> None:
    item.state           = "aging"
    item.age_start_time  = time.time()
    item.age_total_days  = CURE_TYPES[item.cure_type]["age_days"]


def finish_aging(item: CuredMeat) -> str:
    """Compute final quality, set flavor notes, return output item id."""
    item.age_quality  = compute_age_quality(item)
    item.flavor_notes = generate_flavor_notes(item)
    item.state        = "finished"
    return get_charcuterie_output_id(item.cure_type, item.age_quality)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------
class CharcuterieGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter    = 0

    def generate(self, meat_source: str, cure_type: str, breed_quality: float = 0.0) -> CuredMeat:
        """breed_quality: 0.0–1.0 normalized score from butchered pig genetics.
        Pork/lard meats translate this into salt/fat boosts plus a final quality bonus."""
        self._counter += 1
        seed = (self._world_seed * 37 + self._counter * 6971) & 0xFFFFFFFF
        uid  = hashlib.md5(f"char_{seed}_{self._counter}".encode()).hexdigest()[:12]
        rng  = random.Random(seed)

        profile = MEAT_SOURCES.get(meat_source, MEAT_SOURCES["raw_boar_meat"])

        def jitter(base: float) -> float:
            return _clamp(base + rng.gauss(0, 0.08))

        bq        = _clamp(breed_quality)
        fat_boost = bq * 0.20 if meat_source in ("raw_pork", "lard") else 0.0
        salt_boost = bq * 0.10 if meat_source in ("raw_pork", "lard") else 0.0
        breed_bon = bq * 0.18 if meat_source in ("raw_pork", "lard") else 0.0

        return CuredMeat(
            uid              = uid,
            meat_source      = meat_source,
            cure_type        = cure_type,
            state            = "salted",
            salt_penetration = jitter(CURE_TYPES[cure_type]["salt_req"] + salt_boost),
            spice_intensity  = jitter(0.30),
            fat_content      = jitter(profile["fat"] + fat_boost),
            age_quality      = 0.0,
            cure_method      = "",
            age_start_time   = 0.0,
            age_total_days   = 0,
            flavor_notes     = [],
            seed             = seed,
            breed_bonus      = breed_bon,
        )
