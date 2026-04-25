import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class SaltCrystal:
    uid: str
    origin_biome: str       # biodome where deposit was mined ("blend" for blended)
    variety: str            # "solar" | "brine" | "volcanic" | "blend"
    state: str              # "raw" | "dried" | "finished"
    purity: float           # 0.0–1.0  mineral clarity; drives quality gate for fleur de sel
    salinity: float         # 0.0–1.0  concentration of salt flavour
    mineral: float          # 0.0–1.0  trace mineral content (magnesium, calcium, etc.)
    moisture: float         # 0.0–1.0  residual water; high moisture blocks fleur de sel
    grain_size: float       # 0.0–1.0  0 = powdery fine, 1 = large coarse crystals
    flavor_notes: list
    seed: int
    blend_components: list = field(default_factory=list)
    evap_method: str = ""   # "solar" | "brine_pool" | "volcanic_vent"
    refine_grade: str = ""  # "coarse" | "fine" | "fleur_de_sel"


# ---------------------------------------------------------------------------
# Biome mineral profiles
# ---------------------------------------------------------------------------
BIOME_SALT_PROFILES = {
    "coastal":     {"purity": 0.70, "salinity": 0.80, "mineral": 0.35, "moisture": 0.45, "grain_size": 0.50, "variety": "solar"},
    "desert":      {"purity": 0.85, "salinity": 0.90, "mineral": 0.20, "moisture": 0.10, "grain_size": 0.75, "variety": "solar"},
    "arid_steppe": {"purity": 0.65, "salinity": 0.75, "mineral": 0.40, "moisture": 0.20, "grain_size": 0.70, "variety": "solar"},
    "wetland":     {"purity": 0.50, "salinity": 0.55, "mineral": 0.60, "moisture": 0.70, "grain_size": 0.30, "variety": "brine"},
    "volcanic":    {"purity": 0.80, "salinity": 0.85, "mineral": 0.75, "moisture": 0.15, "grain_size": 0.55, "variety": "volcanic"},
    "alpine":      {"purity": 0.90, "salinity": 0.70, "mineral": 0.25, "moisture": 0.20, "grain_size": 0.40, "variety": "brine"},
    "sedimentary": {"purity": 0.60, "salinity": 0.65, "mineral": 0.55, "moisture": 0.35, "grain_size": 0.65, "variety": "brine"},
    "temperate":   {"purity": 0.55, "salinity": 0.60, "mineral": 0.45, "moisture": 0.50, "grain_size": 0.45, "variety": "solar"},
    "tropical":    {"purity": 0.75, "salinity": 0.80, "mineral": 0.30, "moisture": 0.55, "grain_size": 0.35, "variety": "solar"},
    "boreal":      {"purity": 0.45, "salinity": 0.50, "mineral": 0.65, "moisture": 0.60, "grain_size": 0.50, "variety": "brine"},
}

_FLAVOR_POOLS = {
    "purity":    ["crystalline", "clean finish", "transparent", "pure mineral", "clear brine"],
    "salinity":  ["oceanic", "briny depth", "sea-washed", "tidal flat", "brine"],
    "mineral":   ["iron-rich", "sulphurous", "ancient seabed", "magnesium", "volcanic ash"],
    "moisture":  ["damp cavern", "spring water", "humid cave", "wet clay", "mist"],
    "grain_size": ["crunchy texture", "crystalline flake", "powdery", "coarse grit", "airy flake"],
}

_EVAP_METHOD_NOTES = {
    "solar":         ["sun-dried", "wind-kissed", "dry crust"],
    "brine_pool":    ["deep brine", "mineral pool", "subterranean", "ancient water"],
    "volcanic_vent": ["smoky minerality", "sulfuric edge", "volcanic heat", "lava-kissed"],
}

# ---------------------------------------------------------------------------
# Evaporation methods
# ---------------------------------------------------------------------------
EVAP_METHODS = {
    "solar": {
        "label": "Solar Evaporation",
        "desc":  "Natural sun and wind drying. Brightens purity, reduces moisture.",
        "purity": +0.12, "salinity": +0.05, "mineral": -0.08, "moisture": -0.20, "grain_size": +0.05,
    },
    "brine_pool": {
        "label": "Brine Pool Soak",
        "desc":  "Mineral-rich brine concentration. Boosts mineral and grain size.",
        "purity": -0.05, "salinity": +0.10, "mineral": +0.18, "moisture": +0.05, "grain_size": +0.12,
    },
    "volcanic_vent": {
        "label": "Volcanic Vent",
        "desc":  "Geothermal heat evaporation. High mineral, fast-drying, intense flavour.",
        "purity": +0.05, "salinity": +0.08, "mineral": +0.25, "moisture": -0.25, "grain_size": +0.08,
        "variance_mult": 1.8,
    },
}

# ---------------------------------------------------------------------------
# Refine grades
# ---------------------------------------------------------------------------
REFINE_GRADES = {
    "coarse": {
        "label": "Coarse Salt",
        "desc":  "Large crystals. Robust flavour, long shelf life.",
        "grain_size_bias": +0.20,
        "purity_penalty":  -0.05,
    },
    "fine": {
        "label": "Fine Salt",
        "desc":  "Medium-fine crystals. Balanced and versatile.",
        "grain_size_bias": -0.05,
        "purity_penalty":   0.00,
    },
    "fleur_de_sel": {
        "label": "Fleur de Sel",
        "desc":  "Delicate surface crystals. Requires purity ≥ 0.65 and moisture ≤ 0.35.",
        "grain_size_bias": -0.25,
        "purity_penalty":  +0.08,
        "purity_req":  0.65,
        "moisture_req": 0.35,
    },
}

GRADES = ["coarse", "fine", "fleur_de_sel"]

# ---------------------------------------------------------------------------
# Output items
# ---------------------------------------------------------------------------
OUTPUT_DESCS = {
    "coarse_salt":          "Coarse Salt — robust, crunchy mineral crystals",
    "coarse_salt_fine":     "Coarse Salt (Fine) — hand-sorted large crystals",
    "coarse_salt_reserve":  "Coarse Salt (Reserve) — pristine mineral crunch",
    "fine_salt":            "Fine Salt — balanced, all-purpose table salt",
    "fine_salt_fine":       "Fine Salt (Fine) — even grind, pure flavour",
    "fine_salt_reserve":    "Fine Salt (Reserve) — premium refined crystals",
    "fleur_de_sel":         "Fleur de Sel — delicate surface harvest, rare",
    "fleur_de_sel_fine":    "Fleur de Sel (Fine) — exceptional petal flakes",
    "fleur_de_sel_reserve": "Fleur de Sel (Reserve) — the rarest salt of all",
}

OUTPUT_COLORS = {
    "coarse_salt":          (235, 230, 220),
    "coarse_salt_fine":     (245, 240, 232),
    "coarse_salt_reserve":  (255, 252, 245),
    "fine_salt":            (248, 245, 238),
    "fine_salt_fine":       (252, 250, 244),
    "fine_salt_reserve":    (255, 253, 248),
    "fleur_de_sel":         (240, 238, 230),
    "fleur_de_sel_fine":    (248, 246, 238),
    "fleur_de_sel_reserve": (252, 252, 248),
}

BUFF_DESCS = {
    "vitality":    "Mining speed +15%",
    "preservation":"Hunger restore +25%",
    "refinement":  "Crafting quality +20%",
}

# ---------------------------------------------------------------------------
# Codex ordering
# ---------------------------------------------------------------------------
_CODEX_BIOMES = list(BIOME_SALT_PROFILES.keys())
SALT_TYPE_ORDER = [f"{biome}_{grade}" for biome in _CODEX_BIOMES for grade in GRADES]

BIOME_DISPLAY_NAMES = {
    "coastal":     "Coastal",
    "desert":      "Desert",
    "arid_steppe": "Arid Steppe",
    "wetland":     "Wetland",
    "volcanic":    "Volcanic",
    "alpine":      "Alpine",
    "sedimentary": "Sedimentary",
    "temperate":   "Temperate",
    "tropical":    "Tropical",
    "boreal":      "Boreal",
    "blend":       "Blend",
}

VARIETY_DISPLAY_NAMES = {
    "solar":    "Solar",
    "brine":    "Brine",
    "volcanic": "Volcanic",
    "blend":    "Blend",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def get_salt_output_id(grade: str, quality: float) -> str:
    base = {"coarse": "coarse_salt", "fine": "fine_salt",
            "fleur_de_sel": "fleur_de_sel"}.get(grade, "coarse_salt")
    if quality >= 0.70:
        return f"{base}_reserve"
    if quality >= 0.40:
        return f"{base}_fine"
    return base


def fleur_eligible(crystal: "SaltCrystal") -> bool:
    """Returns True if the crystal meets the purity/moisture requirements for fleur de sel."""
    req = REFINE_GRADES["fleur_de_sel"]
    return crystal.purity >= req["purity_req"] and crystal.moisture <= req["moisture_req"]


# ---------------------------------------------------------------------------
# Processing functions
# ---------------------------------------------------------------------------
def apply_evap_method(crystal: "SaltCrystal", method_key: str):
    mods = EVAP_METHODS.get(method_key)
    if not mods:
        return
    crystal.evap_method = method_key
    for attr in ("purity", "salinity", "mineral", "moisture", "grain_size"):
        setattr(crystal, attr, _clamp(getattr(crystal, attr) + mods.get(attr, 0.0)))
    if "variance_mult" in mods:
        rng = random.Random(crystal.seed ^ 0xB44F)
        sigma = 0.06 * mods["variance_mult"]
        for attr in ("purity", "salinity", "mineral", "moisture", "grain_size"):
            setattr(crystal, attr, _clamp(getattr(crystal, attr) + rng.gauss(0, sigma)))


def apply_evap_result(crystal: "SaltCrystal",
                      time_in_sweet: float, total_time: float,
                      overheat_penalties: int):
    if total_time <= 0:
        total_time = 0.1
    sweet_frac = time_in_sweet / total_time
    quality = _clamp(sweet_frac * 0.75 - overheat_penalties * 0.12)
    crystal.purity   = _clamp(crystal.purity   + sweet_frac * 0.10)
    crystal.moisture = _clamp(crystal.moisture  - sweet_frac * 0.18)
    crystal.salinity = _clamp(crystal.salinity  + sweet_frac * 0.08)
    crystal._evap_quality = quality
    crystal.state = "dried"


def apply_refine_grade(crystal: "SaltCrystal", grade_key: str) -> str:
    mods = REFINE_GRADES.get(grade_key, REFINE_GRADES["coarse"])
    # Fleur de sel demotion: check requirements before applying
    if grade_key == "fleur_de_sel" and not fleur_eligible(crystal):
        grade_key = "fine"
        mods = REFINE_GRADES["fine"]
    crystal.refine_grade = grade_key
    crystal.grain_size = _clamp(crystal.grain_size + mods["grain_size_bias"])
    crystal.purity     = _clamp(crystal.purity     + mods["purity_penalty"])
    crystal.state = "finished"
    crystal.flavor_notes = generate_flavor_notes(crystal)
    quality = getattr(crystal, "_evap_quality", 0.0)
    return get_salt_output_id(grade_key, quality)


def generate_flavor_notes(crystal: "SaltCrystal") -> list:
    rng = random.Random(hash((crystal.seed, "salt_flavor", crystal.evap_method, crystal.refine_grade)))
    notes = []
    for attr, pool in _FLAVOR_POOLS.items():
        if getattr(crystal, attr, 0.0) > 0.55:
            notes.append(rng.choice(pool))
    if crystal.evap_method in _EVAP_METHOD_NOTES:
        notes.append(rng.choice(_EVAP_METHOD_NOTES[crystal.evap_method]))
    seen = []
    for n in notes:
        if n not in seen:
            seen.append(n)
    return seen[:5] if seen else ["mineral"]


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------
class SaltGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, biodome: str) -> "SaltCrystal":
        self._counter += 1
        seed = (self._world_seed * 41 + self._counter * 7723) & 0xFFFFFFFF
        uid = hashlib.md5(f"salt_{seed}_{self._counter}".encode()).hexdigest()[:12]

        profile = BIOME_SALT_PROFILES.get(biodome, BIOME_SALT_PROFILES["coastal"])
        rng = random.Random(seed)

        def jitter(base):
            return _clamp(base + rng.gauss(0, 0.07))

        return SaltCrystal(
            uid=uid,
            origin_biome=biodome,
            variety=profile["variety"],
            state="raw",
            purity=jitter(profile["purity"]),
            salinity=jitter(profile["salinity"]),
            mineral=jitter(profile["mineral"]),
            moisture=jitter(profile["moisture"]),
            grain_size=jitter(profile["grain_size"]),
            flavor_notes=[],
            seed=seed,
        )
