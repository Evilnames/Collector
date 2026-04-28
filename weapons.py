import hashlib
from dataclasses import dataclass, field
from gemstones import GEM_TYPES


@dataclass
class Weapon:
    uid: str
    weapon_type: str      # "dagger" | "sword" | "spear" | "axe" | …
    material: str         # "iron" | "gold" | "steel"
    quality: float        # 0.0–1.0 — base quality from smithing
    parts_quality: list   # [float] one entry per smithed part
    custom_name: str      # "" = use auto name
    seed: int
    style: str = "classic"          # "classic" | "ornate" | "rugged"
    decorations: list = field(default_factory=list)  # [{"slot", "item_id", "name", "rarity"}]


# ── Weapon types ──────────────────────────────────────────────────────────────

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

# ── Smithing styles ───────────────────────────────────────────────────────────

WEAPON_STYLES = {
    "classic": {
        "name": "Classic", "desc": "Time-tested form, reliable and balanced.",
        "damage_mult": 1.0, "quality_mod": 0.0,
    },
    "ornate": {
        "name": "Ornate", "desc": "Finely wrought craftsmanship. Adds one extra gem socket.",
        "damage_mult": 0.95, "quality_mod": 0.04,
    },
    "rugged": {
        "name": "Rugged", "desc": "Heavy-duty battle construction. Hits harder, looks rougher.",
        "damage_mult": 1.12, "quality_mod": -0.04,
    },
}
WEAPON_STYLE_ORDER = ["classic", "ornate", "rugged"]

# ── Decoration slots ──────────────────────────────────────────────────────────
# type "gem" draws from player inventory; type "shell" draws from player.seashells

DECORATION_SLOTS = {
    "pommel": {"label": "Pommel",    "type": "gem",   "weapons": "all"},
    "grip":   {"label": "Grip Wrap", "type": "shell", "weapons": "all"},
    "guard":  {"label": "Guard",     "type": "gem",
               "weapons": ["sword", "dagger", "rapier", "glaive", "halberd", "scythe"]},
}

# Ornate style adds an extra blade gem slot
ORNATE_EXTRA_SLOT = {"label": "Blade", "type": "gem", "weapons": "all"}

# ── Rarity bonus tables ───────────────────────────────────────────────────────

GEM_RARITY_BONUS = {
    "common": 0.01, "uncommon": 0.02, "rare": 0.03, "epic": 0.05, "legendary": 0.07,
}

SHELL_RARITY_BONUS = {
    "common": 0.01, "uncommon": 0.02, "rare": 0.04, "legendary": 0.06,
}

# ── Gem inlay catalogue — generated from the full GEM_TYPES registry ──────────
# color = representative primary from color_pool[0][0]; bonus comes from gem rarity at inlay time.

GEM_INLAY_ITEMS = {
    gem_type: {
        "name":  gem_type.replace("_", " ").title(),
        "color": data["color_pool"][0][0],
    }
    for gem_type, data in GEM_TYPES.items()
}

# ── Material profiles ─────────────────────────────────────────────────────────

MATERIAL_PROFILES = {
    "iron":  {"name": "Iron",  "color": (160, 165, 175), "damage_mult": 1.0, "ingot_item": "iron_bar",   "glow": (255, 140,  40)},
    "gold":  {"name": "Gold",  "color": (220, 185,  50), "damage_mult": 1.2, "ingot_item": "gold_ingot", "glow": (255, 220,  60)},
    "steel": {"name": "Steel", "color": (110, 120, 135), "damage_mult": 1.4, "ingot_item": "steel_ingot","glow": (255, 160,  60)},
}

# handle/hilt items needed for final assembly at the Assembly Bench
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


# ── Helper functions ──────────────────────────────────────────────────────────

def quality_tier(q: float) -> str:
    for threshold, label in QUALITY_TIERS:
        if q >= threshold:
            return label
    return "Poor"


def decoration_quality_bonus(weapon: "Weapon") -> float:
    """Sum of all quality bonuses from gem and shell decorations."""
    bonus = 0.0
    for dec in weapon.decorations:
        rarity = dec.get("rarity", "common")
        if dec.get("type") == "gem":
            bonus += GEM_RARITY_BONUS.get(rarity, 0.01)
        else:
            bonus += SHELL_RARITY_BONUS.get(rarity, 0.01)
    return bonus


def effective_quality(weapon: "Weapon") -> float:
    style_mod = WEAPON_STYLES.get(weapon.style, WEAPON_STYLES["classic"])["quality_mod"]
    return min(1.0, weapon.quality + decoration_quality_bonus(weapon) + style_mod)


def weapon_damage(weapon: "Weapon") -> float:
    wt    = WEAPON_TYPES[weapon.weapon_type]
    mt    = MATERIAL_PROFILES[weapon.material]
    style = WEAPON_STYLES.get(weapon.style, WEAPON_STYLES["classic"])
    eq    = effective_quality(weapon)
    return wt["base_damage"] * mt["damage_mult"] * style["damage_mult"] * (0.7 + eq * 0.6)


def weapon_display_name(weapon: "Weapon") -> str:
    if weapon.custom_name:
        return weapon.custom_name
    mat   = MATERIAL_PROFILES[weapon.material]["name"]
    kind  = WEAPON_TYPES[weapon.weapon_type]["name"]
    tier  = quality_tier(effective_quality(weapon))
    style = WEAPON_STYLES.get(weapon.style, WEAPON_STYLES["classic"])
    if weapon.style != "classic":
        return f"{mat} {style['name']} {kind} ({tier})"
    return f"{mat} {kind} ({tier})"


def weapon_decoration_slots(weapon: "Weapon") -> list[str]:
    """Return ordered list of slot keys available for this weapon."""
    slots = []
    for key, data in DECORATION_SLOTS.items():
        eligible = data["weapons"]
        if eligible == "all" or weapon.weapon_type in eligible:
            slots.append(key)
    if weapon.style == "ornate":
        slots.append("blade_gem")   # bonus slot for ornate style
    return slots


# ── Part shape templates (16 cols × 10 rows) ─────────────────────────────────
# True = metal should be present; False = excess to hammer away

def _row(cols):
    lo, hi = cols
    return [lo <= c <= hi for c in range(16)]


def _row_multi(*ranges):
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
        _row((7, 8)),
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
        _row((7, 8)),
        _row((6, 9)),
        _row((5, 10)),
        _row((4, 11)),
        _row((5, 10)),
        _row((6, 9)),
        _row((6, 9)),   # socket
        _row((6, 9)),
        _row((7, 8)),
        _row((7, 8)),
    ],
    "axe_head": [
        _row((8, 11)),
        _row((5, 11)),
        _row((3, 11)),
        _row((3, 11)),
        _row((4, 11)),
        _row((6,  9)),  # eye
        _row((6,  9)),
        _row((6,  9)),
        _row((6,  9)),
        _row((6,  9)),
    ],
    "mace_head": [
        _row((4, 11)),
        _row((3, 12)),
        _row((3, 12)),
        _row((3, 12)),
        _row((4, 11)),
        _row((5, 10)),
        _row((6,  9)),
        _row((6,  9)),
        _row((6,  9)),  # socket
        _row((6,  9)),
    ],
    "halberd_head": [
        _row((7,  8)),
        _row((7,  8)),
        _row((6,  9)),
        _row((4,  9)),
        _row((2,  9)),
        _row((2,  9)),
        _row((4,  9)),
        _row((6,  9)),
        _row((7,  8)),  # socket
        _row((7,  8)),
    ],
    "glaive_blade": [
        _row((9, 12)),
        _row((7, 12)),
        _row((5, 11)),
        _row((4, 10)),
        _row((4,  9)),
        _row((5,  9)),
        _row((6,  8)),
        _row((6,  8)),  # tang
        _row((6,  8)),
        _row((6,  8)),
    ],
    "rapier_blade": [
        _row((7,  8)),
        _row((7,  8)),
        _row((7,  8)),
        _row((7,  8)),
        _row((7,  8)),
        _row((7,  8)),
        _row((7,  8)),
        _row((6,  9)),
        _row((6,  9)),  # tang
        _row((6,  9)),
    ],
    "trident_head": [
        _row_multi((3, 4), (7, 8), (11, 12)),
        _row_multi((3, 4), (7, 8), (11, 12)),
        _row_multi((3, 4), (7, 8), (11, 12)),
        _row((3, 12)),
        _row((4, 11)),
        _row((6,  9)),
        _row((6,  9)),
        _row((6,  9)),  # socket
        _row((6,  9)),
        _row((6,  9)),
    ],
    "scythe_blade": [
        _row((11, 13)),
        _row(( 8, 13)),
        _row(( 5, 12)),
        _row(( 3, 11)),
        _row(( 3,  9)),
        _row(( 4,  7)),
        _row(( 5,  7)),
        _row(( 5,  7)),  # tang
        _row(( 5,  7)),
        _row(( 5,  7)),
    ],
}


def make_billet(part_key: str) -> list[list[str]]:
    target = PART_TEMPLATES[part_key]
    return [
        ["target" if target[r][c] else "excess" for c in range(16)]
        for r in range(10)
    ]


def calculate_part_quality(grid: list, target: list, mistakes: int) -> float:
    total_excess = sum(1 for r in range(10) for c in range(16) if not target[r][c])
    correct      = sum(1 for r in range(10) for c in range(16)
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

    def new_weapon(self, weapon_type: str, material: str, style: str = "classic") -> "Weapon":
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
            style        = style,
            decorations  = [],
        )

    def finalise(self, weapon: "Weapon") -> None:
        if weapon.parts_quality:
            weapon.quality = sum(weapon.parts_quality) / len(weapon.parts_quality)
