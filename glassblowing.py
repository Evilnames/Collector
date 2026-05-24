"""Glassblowing system.

Sand (block 153) harvested in different biomes carries variety. The chain is:

    Glass Kiln (524)  →  Blowing Bench (1732)  →  Annealing Oven (1733)

At each stage a small mini-game (chosen from the OPTION tables below) jitters
the piece's numeric attributes. The final piece becomes one of three shapes:
bottle (cross-system ingredient), vessel (decorative collectible), pane
(placeable window block 1735).
"""

import hashlib
import random
from dataclasses import dataclass, field


# ─── Data shape ─────────────────────────────────────────────────────────────

@dataclass
class GlassPiece:
    uid: str
    origin_biome: str          # "desert" | "beach" | "volcanic" | "saltflat"
    variety: str               # "soda_lime" | "sea_green" | "obsidian_black" | "crystal"
    state: str                 # "gather" | "melted" | "blown" | "annealed"
    shape: str                 # "" until blown, then "bottle" | "vessel" | "pane"
    clarity: float             # 0.0–1.0
    tint_strength: float       # 0.0–1.0
    symmetry: float            # 0.0–1.0 (set by blowing bench)
    bubble_count: int          # set at melt (lower = better)
    wall_thickness: float      # 0.0–1.0 (set by blowing bench)
    flavor_notes: list = field(default_factory=list)
    seed: int = 0


# ─── Biome profiles ─────────────────────────────────────────────────────────

SAND_BIOME_PROFILES = {
    "desert":   {"base_clarity": 0.75, "tint_strength": 0.10, "variety": "soda_lime",      "tint_rgb": (200, 220, 210)},
    "beach":    {"base_clarity": 0.55, "tint_strength": 0.55, "variety": "sea_green",      "tint_rgb": (130, 200, 175)},
    "volcanic": {"base_clarity": 0.40, "tint_strength": 0.85, "variety": "obsidian_black", "tint_rgb": ( 35,  30,  45)},
    "saltflat": {"base_clarity": 0.95, "tint_strength": 0.05, "variety": "crystal",        "tint_rgb": (235, 240, 250)},
}

VARIETY_DISPLAY = {
    "soda_lime":      "Soda-Lime",
    "sea_green":      "Sea-Green",
    "obsidian_black": "Obsidian Black",
    "crystal":        "Crystal",
}

BIOME_DISPLAY_NAMES = {
    "desert":   "Desert",
    "beach":    "Coastal",
    "volcanic": "Volcanic",
    "saltflat": "Salt Flat",
}

# Maps raw world biome / biodome strings → our four sand varieties.
SAND_BIOME_MAP = {
    "desert": "desert", "red_rock": "desert", "canyon": "desert",
    "beach": "beach", "coastal": "beach", "pacific_island": "beach", "ocean": "beach",
    "volcanic": "volcanic", "igneous": "volcanic",
    "salt_flat": "saltflat", "saltflat": "saltflat", "salt_lake": "saltflat",
}


def classify_sand_biome(biome_or_biodome: str) -> str:
    return SAND_BIOME_MAP.get(biome_or_biodome, "desert")


def sand_item_for_biome(sand_biome: str) -> str:
    return f"sand_{sand_biome}"


# ─── Mini-game option tables ────────────────────────────────────────────────

MELT_TEMPS = {
    "low":      {"label": "Low Heat",      "clarity": -0.10, "bubble_delta": +3, "desc": "Quick to melt, leaves bubbles."},
    "standard": {"label": "Standard Heat", "clarity": +0.05, "bubble_delta":  0, "desc": "Balanced clarity and bubble control."},
    "high":     {"label": "High Heat",     "clarity": +0.15, "bubble_delta": -2, "desc": "Clearest melt; risk of scorching tint."},
}

BLOW_SHAPES = {
    "bottle": {"label": "Bottle", "target_thickness": 0.45, "symmetry_bias": 0.10, "desc": "Crafting ingredient for fine wine, beer, spirits."},
    "vessel": {"label": "Vessel", "target_thickness": 0.55, "symmetry_bias": 0.00, "desc": "Decorative collectible graded by clarity & symmetry."},
    "pane":   {"label": "Pane",   "target_thickness": 0.30, "symmetry_bias": 0.20, "desc": "Placeable window block; lets light through."},
}

ANNEAL_RATES = {
    "quick":    {"label": "Quick Cool",    "clarity": -0.10, "break_chance": 0.20, "desc": "Fast — saves time, risks shattering."},
    "standard": {"label": "Standard Cool", "clarity":  0.00, "break_chance": 0.05, "desc": "Reliable cure."},
    "slow":     {"label": "Slow Anneal",   "clarity": +0.12, "break_chance": 0.00, "desc": "Slow — best clarity, no breakage."},
}


# ─── Output descriptions ────────────────────────────────────────────────────

OUTPUT_DESCS = {
    "bottle": "Glass Bottle — bottles fine wine, beer, and spirits",
    "vessel": "Glass Vessel — decorative; graded by clarity & symmetry",
    "pane":   "Glass Pane — placeable window block; passes light",
}

OUTPUT_COLORS = {
    "bottle": (170, 210, 200),
    "vessel": (200, 220, 230),
    "pane":   (210, 235, 240),
}

_FLAVOR_NOTE_POOLS = {
    "desert":   ["sun-clear body", "soda-lime finish", "warm amber glint", "smooth dune-cast surface"],
    "beach":    ["sea-green tint", "salt-fogged edge", "iron-touched body", "shoreline shimmer"],
    "volcanic": ["obsidian-dark body", "smoky inclusions", "ash-flecked surface", "molten-night sheen"],
    "saltflat": ["mirror-clear body", "crystalline ring", "ultra-pure body", "diamond-bright finish"],
}

_CODEX_BIOMES = list(SAND_BIOME_PROFILES.keys())
TYPE_ORDER    = [f"{biome}_{shape}" for biome in _CODEX_BIOMES for shape in OUTPUT_DESCS]


def discovered_key(piece: "GlassPiece") -> str:
    return f"{piece.origin_biome}_{piece.shape}"


# ─── Generator ──────────────────────────────────────────────────────────────

def _clamp(v: float) -> float:
    return max(0.0, min(1.0, v))


class GlassblowingGenerator:
    """Creates raw GlassPiece objects from sand harvest."""

    def __init__(self, world_seed: int):
        self._world_seed = world_seed & 0xFFFFFFFF
        self._counter    = 0

    def gather(self, sand_biome: str) -> "GlassPiece":
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid  = hashlib.md5(f"glass_{seed}_{self._counter}".encode()).hexdigest()[:12]
        rng  = random.Random(seed)

        profile = SAND_BIOME_PROFILES.get(sand_biome, SAND_BIOME_PROFILES["desert"])
        notes_pool = _FLAVOR_NOTE_POOLS.get(sand_biome, _FLAVOR_NOTE_POOLS["desert"])

        return GlassPiece(
            uid            = uid,
            origin_biome   = sand_biome,
            variety        = profile["variety"],
            state          = "gather",
            shape          = "",
            clarity        = _clamp(profile["base_clarity"] + rng.uniform(-0.05, 0.05)),
            tint_strength  = _clamp(profile["tint_strength"] + rng.uniform(-0.05, 0.05)),
            symmetry       = 0.0,
            bubble_count   = rng.randint(2, 6),
            wall_thickness = 0.0,
            flavor_notes   = rng.sample(notes_pool, k=min(2, len(notes_pool))),
            seed           = seed,
        )


# ─── Stage application ──────────────────────────────────────────────────────

def apply_melt(piece: "GlassPiece", temp_key: str) -> None:
    """Apply Glass Kiln results — adjusts clarity & bubble_count."""
    cfg = MELT_TEMPS.get(temp_key, MELT_TEMPS["standard"])
    piece.clarity      = _clamp(piece.clarity + cfg["clarity"])
    piece.bubble_count = max(0, piece.bubble_count + cfg["bubble_delta"])
    piece.state        = "melted"


def apply_blow(piece: "GlassPiece", shape_key: str, puff_count: int) -> None:
    """Apply Blowing Bench results.

    `puff_count` is the number of taps the player landed during the blowing
    mini-game. The target window per shape is roughly 4–8 taps:
        below window → thick wall (cracked vessel ok, pane fails)
        above window → thin wall (bursts; sets shape="" failure)
    """
    cfg = BLOW_SHAPES.get(shape_key, BLOW_SHAPES["vessel"])
    target_taps = 6  # ideal centre
    delta = puff_count - target_taps  # signed distance from ideal
    # Wall thickness inversely related to puff count (more puffs = thinner)
    piece.wall_thickness = _clamp(0.85 - puff_count * 0.10)
    # Symmetry penalty grows with distance from ideal taps
    piece.symmetry = _clamp(0.95 - abs(delta) * 0.12 + cfg["symmetry_bias"])
    # Burst on extreme overpuff
    if puff_count >= 11:
        piece.shape = ""    # burst — no shape set
        piece.state = "blown"
        return
    piece.shape = shape_key
    piece.state = "blown"


def apply_anneal(piece: "GlassPiece", rate_key: str, rng: random.Random | None = None) -> bool:
    """Apply Annealing Oven results. Returns True on success, False if it shattered."""
    rng = rng or random.Random(piece.seed ^ 0x5A5A5A)
    cfg = ANNEAL_RATES.get(rate_key, ANNEAL_RATES["standard"])
    piece.clarity = _clamp(piece.clarity + cfg["clarity"])
    piece.state   = "annealed"
    if rng.random() < cfg["break_chance"]:
        return False
    return True


# ─── Output mapping ─────────────────────────────────────────────────────────

def get_output_item(piece: "GlassPiece") -> str:
    """Map an annealed piece → the inventory item id to grant."""
    if piece.shape == "bottle":
        return "glass_bottle"
    if piece.shape == "pane":
        return "glass_pane_item"
    if piece.shape == "vessel":
        # Three tiers based on combined quality.
        q = (piece.clarity * 0.5 + piece.symmetry * 0.5) - (piece.bubble_count * 0.05)
        if q >= 0.78:
            return "glass_vessel_superior"
        if q >= 0.55:
            return "glass_vessel_fine"
        return "glass_vessel"
    return "glass_shards"  # burst / failed
