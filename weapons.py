import hashlib
from dataclasses import dataclass, field


@dataclass
class Weapon:
    uid: str
    weapon_type: str      # "dagger" | "sword" | "spear" | "axe"
    material: str         # "iron" | "gold" | "steel"
    quality: float        # 0.0–1.0 average of parts_quality
    parts_quality: list   # [float] one entry per smithed part
    custom_name: str      # "" = use auto name
    seed: int


# weapon_type → combat stats + which parts require smithing
WEAPON_TYPES = {
    "dagger":  {"name": "Dagger",  "parts": ["dagger_blade"],  "base_damage": 2, "attack_range": 1, "cooldown": 0.40},
    "sword":   {"name": "Sword",   "parts": ["sword_blade"],   "base_damage": 3, "attack_range": 1, "cooldown": 0.60},
    "spear":   {"name": "Spear",   "parts": ["spear_head"],    "base_damage": 3, "attack_range": 2, "cooldown": 0.70},
    "axe":     {"name": "Axe",     "parts": ["axe_head"],      "base_damage": 4, "attack_range": 1, "cooldown": 0.90},
    "mace":    {"name": "Mace",    "parts": ["mace_head"],     "base_damage": 5, "attack_range": 1, "cooldown": 1.10},
    "halberd": {"name": "Halberd", "parts": ["halberd_head"],  "base_damage": 5, "attack_range": 2, "cooldown": 1.20},
    "glaive":  {"name": "Glaive",  "parts": ["glaive_blade"],  "base_damage": 4, "attack_range": 2, "cooldown": 0.85},
    "rapier":  {"name": "Rapier",  "parts": ["rapier_blade"],  "base_damage": 3, "attack_range": 1, "cooldown": 0.35},
    "trident": {"name": "Trident", "parts": ["trident_head"],  "base_damage": 4, "attack_range": 2, "cooldown": 0.80},
    "scythe":  {"name": "Scythe",  "parts": ["scythe_blade"],  "base_damage": 6, "attack_range": 2, "cooldown": 1.30},
}

# part_key → item_id produced after smithing (prefixed by material at runtime)
PART_ITEM_PREFIX = {
    "dagger_blade":  "dagger_blade",
    "sword_blade":   "sword_blade",
    "spear_head":    "spear_head",
    "axe_head":      "axe_head",
    "mace_head":     "mace_head",
    "halberd_head":  "halberd_head",
    "glaive_blade":  "glaive_blade",
    "rapier_blade":  "rapier_blade",
    "trident_head":  "trident_head",
    "scythe_blade":  "scythe_blade",
}

# material → display info + which existing item acts as input ingot
MATERIAL_PROFILES = {
    "iron":  {"name": "Iron",  "color": (160, 165, 175), "damage_mult": 1.0, "ingot_item": "iron_bar",   "glow": (255, 140,  40)},
    "gold":  {"name": "Gold",  "color": (220, 185,  50), "damage_mult": 1.2, "ingot_item": "gold_ingot", "glow": (255, 220,  60)},
    "steel": {"name": "Steel", "color": (110, 120, 135), "damage_mult": 1.4, "ingot_item": "steel_ingot","glow": (255, 160,  60)},
}

# handle/hilt items needed for final assembly at crafting bench
ASSEMBLY_HANDLES = {
    "dagger":  "dagger_handle",
    "sword":   "sword_hilt",
    "spear":   "spear_shaft",
    "axe":     "axe_haft",
    "mace":    "mace_haft",
    "halberd": "halberd_shaft",
    "glaive":  "glaive_pole",
    "rapier":  "rapier_grip",
    "trident": "trident_shaft",
    "scythe":  "scythe_snath",
}

WEAPON_TYPE_ORDER = ["dagger", "sword", "spear", "axe", "mace", "halberd", "glaive",
                     "rapier", "trident", "scythe"]
MATERIAL_ORDER    = ["iron", "gold", "steel"]

QUALITY_TIERS = [
    (0.85, "Masterwork"),
    (0.65, "Fine"),
    (0.40, "Standard"),
    (0.00, "Poor"),
]


def quality_tier(q: float) -> str:
    for threshold, label in QUALITY_TIERS:
        if q >= threshold:
            return label
    return "Poor"


def weapon_damage(weapon: "Weapon") -> float:
    wt = WEAPON_TYPES[weapon.weapon_type]
    mt = MATERIAL_PROFILES[weapon.material]
    return wt["base_damage"] * mt["damage_mult"] * (0.7 + weapon.quality * 0.6)


def weapon_display_name(weapon: "Weapon") -> str:
    if weapon.custom_name:
        return weapon.custom_name
    mat  = MATERIAL_PROFILES[weapon.material]["name"]
    kind = WEAPON_TYPES[weapon.weapon_type]["name"]
    tier = quality_tier(weapon.quality)
    return f"{mat} {kind} ({tier})"


# ── Part shape templates (16 cols × 10 rows) ─────────────────────────────────
# True = metal should be present in the finished part; False = excess to hammer away

def _row(cols):
    """Build a 16-element row with True in the given column range (inclusive)."""
    lo, hi = cols
    return [lo <= c <= hi for c in range(16)]


def _row_multi(*ranges):
    """Row with True across multiple inclusive column ranges (for non-contiguous shapes)."""
    return [any(lo <= c <= hi for lo, hi in ranges) for c in range(16)]


PART_TEMPLATES = {
    "sword_blade": [
        _row((7, 8)),   # tip
        _row((7, 8)),
        _row((6, 9)),
        _row((6, 9)),
        _row((5, 10)),
        _row((5, 10)),
        _row((5, 10)),
        _row((5, 10)),
        _row((6, 9)),   # tang
        _row((6, 9)),
    ],
    "dagger_blade": [
        _row((7, 8)),   # tip
        _row((7, 8)),
        _row((6, 9)),
        _row((6, 9)),
        _row((5, 10)),
        _row((5, 10)),
        _row((6, 9)),   # tang
        _row((6, 9)),
        _row((6, 9)),
        _row((6, 9)),
    ],
    "spear_head": [
        _row((7, 8)),   # tip
        _row((6, 9)),
        _row((5, 10)),
        _row((4, 11)),  # widest
        _row((5, 10)),
        _row((6, 9)),
        _row((6, 9)),   # socket
        _row((6, 9)),
        _row((7, 8)),
        _row((7, 8)),
    ],
    "axe_head": [
        _row((8, 11)),  # blade top
        _row((5, 11)),
        _row((3, 11)),  # max sweep
        _row((3, 11)),
        _row((4, 11)),
        _row((6,  9)),  # eye / socket
        _row((6,  9)),
        _row((6,  9)),
        _row((6,  9)),
        _row((6,  9)),
    ],
    "mace_head": [
        _row((4, 11)),  # heavy crown
        _row((3, 12)),
        _row((3, 12)),  # widest bludgeon
        _row((3, 12)),
        _row((4, 11)),
        _row((5, 10)),  # tapered neck
        _row((6,  9)),
        _row((6,  9)),
        _row((6,  9)),  # socket
        _row((6,  9)),
    ],
    "halberd_head": [
        _row((7,  8)),  # top spike
        _row((7,  8)),
        _row((6,  9)),
        _row((4,  9)),  # axe blade extends to one side
        _row((2,  9)),  # max sweep (asymmetric)
        _row((2,  9)),
        _row((4,  9)),
        _row((6,  9)),
        _row((7,  8)),  # socket
        _row((7,  8)),
    ],
    "glaive_blade": [
        _row((9, 12)),  # curved tip leans right
        _row((7, 12)),
        _row((5, 11)),  # belly of the cleaver
        _row((4, 10)),
        _row((4,  9)),
        _row((5,  9)),
        _row((6,  8)),
        _row((6,  8)),  # tang
        _row((6,  8)),
        _row((6,  8)),
    ],
    "rapier_blade": [
        _row((7,  8)),  # needle point
        _row((7,  8)),
        _row((7,  8)),
        _row((7,  8)),
        _row((7,  8)),  # long thin profile
        _row((7,  8)),
        _row((7,  8)),
        _row((6,  9)),
        _row((6,  9)),  # tang
        _row((6,  9)),
    ],
    "trident_head": [
        _row_multi((3, 4), (7, 8), (11, 12)),  # three prong tips
        _row_multi((3, 4), (7, 8), (11, 12)),
        _row_multi((3, 4), (7, 8), (11, 12)),
        _row((3, 12)),                          # crossbar joining prongs
        _row((4, 11)),
        _row((6,  9)),                          # neck
        _row((6,  9)),
        _row((6,  9)),                          # socket
        _row((6,  9)),
        _row((6,  9)),
    ],
    "scythe_blade": [
        _row((11, 13)),  # tip points up-right
        _row(( 8, 13)),
        _row(( 5, 12)),  # sweeping curve
        _row(( 3, 11)),  # max sweep
        _row(( 3,  9)),
        _row(( 4,  7)),
        _row(( 5,  7)),
        _row(( 5,  7)),  # tang
        _row(( 5,  7)),
        _row(( 5,  7)),
    ],
}


def make_billet(part_key: str) -> list[list[str]]:
    """Return a 16×10 grid with cells labelled 'target' or 'excess'."""
    target = PART_TEMPLATES[part_key]
    return [
        ["target" if target[r][c] else "excess" for c in range(16)]
        for r in range(10)
    ]


def calculate_part_quality(grid: list, target: list, mistakes: int) -> float:
    total_excess   = sum(1 for r in range(10) for c in range(16) if not target[r][c])
    correct        = sum(1 for r in range(10) for c in range(16)
                         if not target[r][c] and grid[r][c] == "removed")
    if total_excess == 0:
        base = 1.0
    else:
        base = correct / total_excess
    penalty = min(1.0, mistakes * 0.15)
    return max(0.0, base * (1.0 - penalty))


class WeaponGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter    = 0

    def new_weapon(self, weapon_type: str, material: str) -> "Weapon":
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFF_FFFF
        uid  = hashlib.md5(f"weapon_{seed}_{self._counter}".encode()).hexdigest()[:12]
        return Weapon(
            uid          = uid,
            weapon_type  = weapon_type,
            material     = material,
            quality      = 0.0,
            parts_quality= [],
            custom_name  = "",
            seed         = seed,
        )

    def finalise(self, weapon: "Weapon") -> None:
        """Average parts_quality into weapon.quality."""
        if weapon.parts_quality:
            weapon.quality = sum(weapon.parts_quality) / len(weapon.parts_quality)
