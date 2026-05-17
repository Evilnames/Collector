"""Falconry system.

Wild raptors (a subset of birds.py species) can be captured with a Falconer's
Gauntlet and trained at a Falconer's Perch. Tamed raptors hunt small game
on the player's command. This module holds:

  * RAPTOR_SPECIES  — the trainable bird roster + base stats
  * TRAINING_DRILLS — per-stat training mini-game definitions
  * QUARRY          — huntable quarry types with biome + drop tables
  * Raptor          — dataclass tracking a single tamed bird
  * helpers         — generation, training application, hunt resolution
"""

import random
import hashlib
from dataclasses import dataclass, field


# ── Roster ───────────────────────────────────────────────────────────────────
# Each entry: a stable string key (used in save files) -> display info, biome
# affinity, base 0..1 stats, and a "specialty" flag the UI uses for flavor.
RAPTOR_SPECIES = {
    "peregrine_falcon": {
        "name": "Peregrine Falcon", "tier": 3, "wing": "pointed",
        "biomes": ("alpine_mountain", "rolling_hills", "steep_hills", "beach"),
        "color": (90, 100, 130),
        "base": {"speed": 0.85, "strength": 0.45, "intelligence": 0.65,
                 "endurance": 0.55, "boldness": 0.70, "vision": 0.75},
        "specialty": "stoop",
    },
    "merlin": {
        "name": "Merlin", "tier": 2, "wing": "pointed",
        "biomes": ("boreal", "tundra", "rolling_hills", "birch_forest"),
        "color": (110, 90, 70),
        "base": {"speed": 0.70, "strength": 0.30, "intelligence": 0.55,
                 "endurance": 0.65, "boldness": 0.85, "vision": 0.60},
        "specialty": "pursuit",
    },
    "prairie_falcon": {
        "name": "Prairie Falcon", "tier": 2, "wing": "pointed",
        "biomes": ("steppe", "arid_steppe", "canyon", "wasteland"),
        "color": (160, 130, 80),
        "base": {"speed": 0.75, "strength": 0.50, "intelligence": 0.55,
                 "endurance": 0.70, "boldness": 0.60, "vision": 0.70},
        "specialty": "pursuit",
    },
    "lanner_falcon": {
        "name": "Lanner Falcon", "tier": 2, "wing": "pointed",
        "biomes": ("savanna", "desert", "mediterranean"),
        "color": (170, 110, 60),
        "base": {"speed": 0.72, "strength": 0.42, "intelligence": 0.60,
                 "endurance": 0.62, "boldness": 0.65, "vision": 0.68},
        "specialty": "pursuit",
    },
    "goshawk": {
        "name": "Goshawk", "tier": 3, "wing": "broad",
        "biomes": ("temperate", "birch_forest", "boreal", "redwood"),
        "color": (90, 95, 100),
        "base": {"speed": 0.65, "strength": 0.75, "intelligence": 0.60,
                 "endurance": 0.55, "boldness": 0.85, "vision": 0.65},
        "specialty": "ambush",
    },
    "kite": {
        "name": "Red Kite", "tier": 1, "wing": "broad",
        "biomes": ("temperate", "rolling_hills", "wetland"),
        "color": (165, 80, 50),
        "base": {"speed": 0.55, "strength": 0.40, "intelligence": 0.50,
                 "endurance": 0.80, "boldness": 0.45, "vision": 0.55},
        "specialty": "soaring",
    },
    "harrier": {
        "name": "Harrier", "tier": 1, "wing": "broad",
        "biomes": ("wetland", "swamp", "rolling_hills"),
        "color": (120, 130, 110),
        "base": {"speed": 0.50, "strength": 0.45, "intelligence": 0.55,
                 "endurance": 0.75, "boldness": 0.55, "vision": 0.65},
        "specialty": "low_quarter",
    },
    "golden_eagle": {
        "name": "Golden Eagle", "tier": 4, "wing": "broad",
        "biomes": ("alpine_mountain", "rocky_mountain", "canyon"),
        "color": (110, 80, 40),
        "base": {"speed": 0.60, "strength": 0.95, "intelligence": 0.60,
                 "endurance": 0.70, "boldness": 0.80, "vision": 0.80},
        "specialty": "large_quarry",
    },
    "osprey": {
        "name": "Osprey", "tier": 2, "wing": "broad",
        "biomes": ("beach", "wetland", "tropical"),
        "color": (180, 175, 165),
        "base": {"speed": 0.55, "strength": 0.60, "intelligence": 0.60,
                 "endurance": 0.70, "boldness": 0.60, "vision": 0.85},
        "specialty": "fish",
    },
    "eagle_owl": {
        "name": "Eagle Owl", "tier": 3, "wing": "broad",
        "biomes": ("boreal", "redwood", "tundra"),
        "color": (130, 100, 70),
        "base": {"speed": 0.50, "strength": 0.70, "intelligence": 0.75,
                 "endurance": 0.55, "boldness": 0.60, "vision": 0.95},
        "specialty": "night",
    },
    "kestrel": {
        "name": "African Kestrel", "tier": 1, "wing": "pointed",
        "biomes": ("savanna", "arid_steppe", "rolling_hills"),
        "color": (175, 130, 70),
        "base": {"speed": 0.65, "strength": 0.30, "intelligence": 0.55,
                 "endurance": 0.65, "boldness": 0.55, "vision": 0.70},
        "specialty": "hover",
    },
    "pygmy_falcon": {
        "name": "Pygmy Falcon", "tier": 1, "wing": "pointed",
        "biomes": ("savanna", "desert"),
        "color": (200, 195, 180),
        "base": {"speed": 0.62, "strength": 0.25, "intelligence": 0.50,
                 "endurance": 0.55, "boldness": 0.75, "vision": 0.60},
        "specialty": "pursuit",
    },
    "bateleur_eagle": {
        "name": "Bateleur Eagle", "tier": 3, "wing": "broad",
        "biomes": ("savanna",),
        "color": (165, 60, 40),
        "base": {"speed": 0.60, "strength": 0.80, "intelligence": 0.60,
                 "endurance": 0.85, "boldness": 0.70, "vision": 0.75},
        "specialty": "soaring",
    },
    "snowy_owl": {
        "name": "Snowy Owl", "tier": 3, "wing": "broad",
        "biomes": ("tundra",),
        "color": (240, 240, 235),
        "base": {"speed": 0.55, "strength": 0.70, "intelligence": 0.75,
                 "endurance": 0.60, "boldness": 0.55, "vision": 0.90},
        "specialty": "night",
    },
    "barn_owl": {
        "name": "Barn Owl", "tier": 2, "wing": "broad",
        "biomes": ("temperate", "rolling_hills", "wetland"),
        "color": (220, 195, 150),
        "base": {"speed": 0.50, "strength": 0.45, "intelligence": 0.70,
                 "endurance": 0.55, "boldness": 0.45, "vision": 0.90},
        "specialty": "night",
    },
}

# Stable codex order
SPECIES_ORDER = list(RAPTOR_SPECIES.keys())

# Maps the bird species name strings used by birds.py classes onto our keys.
# Used when the player attempts capture on a wild Bird.
BIRD_CLASS_TO_RAPTOR = {
    "PeregrineFalcon":  "peregrine_falcon",
    "Merlin":           "merlin",
    "PrairieFalcon":    "prairie_falcon",
    "LannerFalcon":     "lanner_falcon",
    "Goshawk":          "goshawk",
    "Kite":             "kite",
    "Harrier":          "harrier",
    "Eagle":            "golden_eagle",
    "VerreauxsEagle":   "golden_eagle",
    "Osprey":           "osprey",
    "Owl":              "eagle_owl",
    "SnowyOwl":         "snowy_owl",
    "BarnOwl":          "barn_owl",
    "AfricanKestrel":   "kestrel",
    "PygmyFalcon":      "pygmy_falcon",
    "BateleurEagle":    "bateleur_eagle",
    "RedNeckedFalcon":  "lanner_falcon",
    "MartialEagle":     "golden_eagle",
    "TawnyEagle":       "golden_eagle",
    "AfricanFishEagle": "osprey",
}


# ── Training drills ──────────────────────────────────────────────────────────
TRAINING_DRILLS = {
    "lure_recall":    {"label": "Lure Recall",     "stat": "intelligence",
                       "desc": "A swung lure teaches reliable return-to-glove.",
                       "food_cost": 2, "gain": 0.04},
    "block_perch":    {"label": "Block Perching",  "stat": "boldness",
                       "desc": "Standing on the outdoor block builds composure around people and noise.",
                       "food_cost": 1, "gain": 0.03},
    "stooping":       {"label": "Stoop Drill",     "stat": "speed",
                       "desc": "High-altitude dive practice on a swung pigeon-feather lure.",
                       "food_cost": 3, "gain": 0.05},
    "weight_carry":   {"label": "Carrying Drills", "stat": "strength",
                       "desc": "Heavier prey-dummies build wing strength.",
                       "food_cost": 3, "gain": 0.04},
    "long_flights":   {"label": "Long Flights",    "stat": "endurance",
                       "desc": "Extended cross-country flights to a distant lure.",
                       "food_cost": 2, "gain": 0.04},
    "manning":        {"label": "Manning",         "stat": "boldness",
                       "desc": "Long time on the gauntlet to bond the bird to its falconer.",
                       "food_cost": 1, "gain": 0.05},
}


# ── Quarry ───────────────────────────────────────────────────────────────────
# All drops reference items that already exist in items.py (raw_rabbit,
# raw_duck, raw_pheasant, raw_turkey, feather, rabbit_pelt).
QUARRY = {
    "rabbit":   {"label": "Rabbit",   "difficulty": 0.35, "strength_req": 0.30,
                 "biomes": ("temperate", "rolling_hills", "savanna", "steppe",
                            "arid_steppe", "desert", "canyon", "wasteland"),
                 "drops": [("raw_rabbit", 2), ("rabbit_pelt", 1)]},
    "hare":     {"label": "Hare",     "difficulty": 0.45, "strength_req": 0.35,
                 "biomes": ("rolling_hills", "temperate", "steep_hills", "alpine_mountain"),
                 "drops": [("raw_rabbit", 3), ("rabbit_pelt", 1)]},
    "pheasant": {"label": "Pheasant", "difficulty": 0.40, "strength_req": 0.30,
                 "biomes": ("temperate", "birch_forest", "rolling_hills"),
                 "drops": [("raw_pheasant", 2), ("feather", 4)]},
    "duck":     {"label": "Duck",     "difficulty": 0.50, "strength_req": 0.35,
                 "biomes": ("wetland", "swamp", "beach"),
                 "drops": [("raw_duck", 2), ("feather", 3)]},
    "quail":    {"label": "Quail",    "difficulty": 0.30, "strength_req": 0.25,
                 "biomes": ("steppe", "arid_steppe", "savanna", "desert"),
                 "drops": [("raw_pheasant", 1), ("feather", 2)]},
    "grouse":   {"label": "Grouse",   "difficulty": 0.42, "strength_req": 0.32,
                 "biomes": ("boreal", "tundra", "alpine_mountain"),
                 "drops": [("raw_pheasant", 2), ("feather", 3)]},
    "marmot":   {"label": "Marmot",   "difficulty": 0.55, "strength_req": 0.50,
                 "biomes": ("alpine_mountain", "rocky_mountain", "steep_hills"),
                 "drops": [("raw_rabbit", 3), ("rabbit_pelt", 1)]},
    "turkey":   {"label": "Wild Turkey", "difficulty": 0.55, "strength_req": 0.60,
                 "biomes": ("temperate", "birch_forest", "redwood"),
                 "drops": [("raw_turkey", 3), ("feather", 5)]},
}

QUARRY_ORDER = list(QUARRY.keys())


# ── Name pool ────────────────────────────────────────────────────────────────
NAME_POOL = [
    "Ascalon", "Bran", "Caelin", "Drysden", "Erol", "Fenrik", "Garreth",
    "Hawthorne", "Ivor", "Jorah", "Kael", "Lothar", "Marek", "Nyx", "Orin",
    "Percival", "Quill", "Rook", "Strix", "Talon", "Vespa", "Wynn", "Yara",
    "Zephyr", "Saker", "Hessa", "Mirage", "Storm", "Echo", "Vigil", "Stoop",
    "Ember", "Banner", "Ashling", "Vanguard", "Sable", "Argent", "Crest",
]


# ── Data class ───────────────────────────────────────────────────────────────
@dataclass
class Raptor:
    uid: str
    species: str
    name: str
    origin_biome: str
    speed: float
    strength: float
    intelligence: float
    endurance: float
    boldness: float
    vision: float
    bond: float = 0.5
    hunger: float = 0.5
    condition: float = 1.0
    hunts_completed: int = 0
    days_owned: int = 0
    seed: int = 0
    perch_pos: tuple = None     # (bx, by) or None when on the glove
    state: str = "perched"      # perched | hunting | training | resting
    cooldown: float = 0.0


# ── Generation / helpers ─────────────────────────────────────────────────────
def species_for_biome(biome: str) -> list:
    return [k for k, d in RAPTOR_SPECIES.items() if biome in d["biomes"]]


def make_raptor(species: str, biome: str, world_seed: int, counter: int) -> Raptor:
    sp = RAPTOR_SPECIES[species]
    seed = (world_seed * 41 + counter * 9337 + (hash(species) & 0xFFFF)) & 0xFFFFFFFF
    rng = random.Random(seed)

    def j(b):
        return max(0.05, min(0.99, b + rng.gauss(0, 0.06)))

    base = sp["base"]
    uid = hashlib.md5(f"raptor_{seed}_{counter}".encode()).hexdigest()[:12]
    name = rng.choice(NAME_POOL)
    return Raptor(
        uid=uid, species=species, name=name, origin_biome=biome or "",
        speed=j(base["speed"]),
        strength=j(base["strength"]),
        intelligence=j(base["intelligence"]),
        endurance=j(base["endurance"]),
        boldness=j(base["boldness"]),
        vision=j(base["vision"]),
        seed=seed,
    )


def species_rating(species: str) -> int:
    """Tier 1..4 used by codex display."""
    return RAPTOR_SPECIES.get(species, {}).get("tier", 1)


def quarry_for_biome(biome: str) -> list:
    return [k for k, d in QUARRY.items() if biome in d["biomes"]]


# ── Capture ──────────────────────────────────────────────────────────────────
def capture_success_chance(raptor_species: str, gauntlet_quality: float = 1.0) -> float:
    """Higher-tier birds are harder to take cleanly."""
    tier = species_rating(raptor_species)
    base = {1: 0.70, 2: 0.55, 3: 0.40, 4: 0.25}.get(tier, 0.50)
    return max(0.10, min(0.95, base * gauntlet_quality))


# ── Training application ─────────────────────────────────────────────────────
def apply_training(raptor: Raptor, drill_key: str, performance: float):
    """performance is 0..1 from the training mini-game."""
    d = TRAINING_DRILLS.get(drill_key)
    if not d:
        return
    stat = d["stat"]
    gain = d["gain"] * (0.4 + performance * 1.2)
    cur = getattr(raptor, stat)
    setattr(raptor, stat, max(0.0, min(0.99, cur + gain)))
    # Every drill nudges bond up; manning especially
    bond_bonus = 0.06 + performance * 0.04 if drill_key == "manning" else 0.01 + performance * 0.02
    raptor.bond = max(0.0, min(1.0, raptor.bond + bond_bonus))
    raptor.hunger = max(0.0, min(1.0, raptor.hunger + 0.10))
    raptor.cooldown = 6.0
    raptor.state = "resting"


# ── Hunt resolution ──────────────────────────────────────────────────────────
def hunt_outcome(raptor: Raptor, quarry_key: str, rng: random.Random = None) -> dict:
    """Return outcome dict with keys: success, drops, condition_loss, bond_gain, msg."""
    if rng is None:
        rng = random.Random()
    q = QUARRY.get(quarry_key)
    if not q:
        return {"success": False, "drops": [], "condition_loss": 0.0,
                "bond_gain": 0.0, "msg": "Unknown quarry."}

    if raptor.condition < 0.20:
        return {"success": False, "drops": [], "condition_loss": 0.0,
                "bond_gain": 0.0, "msg": f"{raptor.name} is in poor condition."}
    if raptor.hunger > 0.85:
        return {"success": False, "drops": [], "condition_loss": 0.0,
                "bond_gain": -0.02, "msg": f"{raptor.name} is too full to hunt."}
    if raptor.strength < q["strength_req"] * 0.6:
        return {"success": False, "drops": [], "condition_loss": 0.0,
                "bond_gain": -0.01,
                "msg": f"{raptor.name} refuses — quarry too large."}

    # Skill weighted by hunger drive and bond
    skill = (raptor.speed * 0.30 + raptor.vision * 0.25 +
             raptor.intelligence * 0.20 + raptor.boldness * 0.15 +
             raptor.endurance * 0.10) * raptor.condition
    drive = 1.0 + (0.20 if raptor.hunger > 0.5 else 0.0)
    p = 0.40 + skill * drive - q["difficulty"]
    if raptor.bond < 0.3:
        p -= 0.15
    p = max(0.05, min(0.95, p))

    if rng.random() < p:
        drops = list(q["drops"])
        # Strong birds bring back a heavier carcass
        if raptor.strength > q["strength_req"] + 0.25:
            drops.append(("raw_rabbit", 1) if "rabbit" in quarry_key or "hare" in quarry_key
                         else ("feather", 2))
        return {
            "success": True, "drops": drops,
            "condition_loss": rng.uniform(0.02, 0.07),
            "bond_gain": 0.04,
            "msg": f"{raptor.name} returns with the {q['label'].lower()}.",
        }
    return {
        "success": False, "drops": [],
        "condition_loss": rng.uniform(0.05, 0.15),
        "bond_gain": -0.02,
        "msg": f"{raptor.name} returns empty-taloned.",
    }


def apply_hunt(raptor: Raptor, outcome: dict):
    raptor.condition = max(0.0, min(1.0, raptor.condition - outcome.get("condition_loss", 0.0)))
    raptor.bond = max(0.0, min(1.0, raptor.bond + outcome.get("bond_gain", 0.0)))
    if outcome.get("success"):
        raptor.hunts_completed += 1
    raptor.hunger = max(0.0, min(1.0, raptor.hunger + 0.15))
    raptor.cooldown = 12.0
    raptor.state = "resting"


def feed_raptor(raptor: Raptor, portions: int = 1):
    """Each portion reduces hunger and slightly restores condition."""
    raptor.hunger = max(0.0, raptor.hunger - 0.25 * portions)
    raptor.condition = min(1.0, raptor.condition + 0.06 * portions)
    raptor.bond = min(1.0, raptor.bond + 0.01 * portions)


# ── Quality stars (for codex) ────────────────────────────────────────────────
def raptor_quality_stars(r: Raptor) -> int:
    """0..5 stars based on aggregate stat sum."""
    s = r.speed + r.strength + r.intelligence + r.endurance + r.boldness + r.vision
    if s >= 5.4: return 5
    if s >= 4.8: return 4
    if s >= 4.2: return 3
    if s >= 3.6: return 2
    if s >= 3.0: return 1
    return 0
