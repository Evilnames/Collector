import random
import hashlib
from dataclasses import dataclass, field


WHEEL_ROWS    = 12   # vertical profile segments (top → bottom)
WHEEL_MAX_RAD = 8    # maximum half-width per row
WHEEL_MIN_RAD = 1    # minimum half-width per row


@dataclass
class PotteryPiece:
    uid: str
    clay_biome: str       # "wetland"|"tropical"|"temperate"|"river"|"mediterranean"|"celadon"|"blue_white"|"jun"
    shape: str            # auto-detected: "pot" | "amphora" | "jar" | "jug" | "vase"
    state: str            # "formed" | "fired" | "glazed"
    firing_level: str     # "cracked" | "intact" | "fine" | "masterwork"
    firing_quality: float # 0.0–1.0
    thickness: float      # 0.0–1.0 (average wall presence)
    evenness: float       # 0.0–1.0 (1 = perfectly uniform)
    glaze_type: str       # "" | "ruby" | "emerald" | "sapphire" | "amethyst" | "topaz" | "pigment"
    texture_notes: list
    seed: int
    profile: list         # list of WHEEL_ROWS int half-widths (top → bottom)
    blend_components: list = field(default_factory=list)
    pigment_glaze_color: list = field(default_factory=list)  # [R,G,B] when glaze_type=="pigment"


# Base clay attributes per biome
CLAY_BIOME_PROFILES = {
    "wetland":   {"thickness": 0.80, "evenness": 0.55, "variety": "earthenware",  "glaze_affinity": 0.40},
    "tropical":  {"thickness": 0.50, "evenness": 0.85, "variety": "porcelain",    "glaze_affinity": 0.90},
    "temperate": {"thickness": 0.90, "evenness": 0.65, "variety": "stoneware",    "glaze_affinity": 0.55},
    "river":         {"thickness": 0.65, "evenness": 0.75, "variety": "slipware",     "glaze_affinity": 0.80},
    "mediterranean": {"thickness": 0.35, "evenness": 0.90, "variety": "terracotta",        "glaze_affinity": 0.75},
    "celadon":       {"thickness": 0.55, "evenness": 0.85, "variety": "celadon",            "glaze_affinity": 0.85},
    "blue_white":    {"thickness": 0.40, "evenness": 0.92, "variety": "blue-white porcelain","glaze_affinity": 0.95},
    "jun":           {"thickness": 0.75, "evenness": 0.60, "variety": "jun ware",            "glaze_affinity": 0.38},
}

_TEXTURE_NOTE_POOLS = {
    "wetland":   ["iron-rich veins", "red ochre swirls", "earthy pitting", "warm terracotta", "mineral deposits"],
    "tropical":  ["translucent walls", "smooth porcelain finish", "fine grain", "white clay body", "delicate rim"],
    "temperate": ["grey stoneware body", "dense walls", "frost inclusions", "matte surface", "salt deposits"],
    "river":         ["blue-grey slip", "smooth burnish", "watermark lines", "silty finish", "ripple texture"],
    "mediterranean": ["iron-rich red clay body", "black gloss slip", "burnished ochre surface", "charcoal figure bands", "kiln-fired terracotta"],
    "celadon":       ["jade-green crackle glaze", "translucent celadon body", "smooth grey stoneware", "fine ash glaze", "glassy celadon finish"],
    "blue_white":    ["cobalt blue brushwork", "pure white ground", "crisp blue linework", "translucent glaze layer", "vivid cobalt wash"],
    "jun":           ["opalescent blue glaze", "copper-red splashes", "glaze pooling at foot", "milky glaze haze", "kiln-transformed copper bloom"],
}

GLAZE_TYPES = {
    "ruby":     {"label": "Ruby Glaze",     "color": (200,  60,  60), "dust_item": "ruby_dust"},
    "emerald":  {"label": "Emerald Glaze",  "color": ( 60, 180,  90), "dust_item": "emerald_dust"},
    "sapphire": {"label": "Sapphire Glaze", "color": ( 60, 100, 200), "dust_item": "sapphire_dust"},
    "amethyst": {"label": "Amethyst Glaze", "color": (160,  80, 200), "dust_item": "amethyst_dust"},
    "topaz":    {"label": "Topaz Glaze",    "color": (200, 160,  40), "dust_item": "topaz_dust"},
}

FIRING_LEVELS = ["cracked", "intact", "fine", "masterwork"]

# Maps shape × firing_level → output item id
SHAPE_OUTPUTS = {
    "pot":     {"intact": "clay_cooking_pot",  "fine": "clay_cooking_pot_fine",  "masterwork": "clay_cooking_pot_masterwork"},
    "amphora": {"intact": "wine_amphora",       "fine": "wine_amphora_fine",       "masterwork": "wine_amphora_masterwork"},
    "jar":     {"intact": "herb_storage_jar",  "fine": "herb_storage_jar_fine",  "masterwork": "herb_storage_jar_masterwork"},
    "jug":     {"intact": "water_jug",         "fine": "water_jug_fine",         "masterwork": "water_jug_masterwork"},
    "vase":    {"intact": "pottery_vase",      "fine": "pottery_vase_fine",      "masterwork": "pottery_vase_masterwork"},
}

BUFF_DESCS = {
    "cook_yield":    "Food station yields +1 serving (120–240 s)",
    "wine_complex":  "Wine complexity +0.15 per bottle (120–240 s)",
    "herb_preserve": "Dried herb duration +50% (120–240 s)",
    "irrigate":      "Crops count as irrigated (300–600 s)",
}

_CODEX_BIOMES = list(CLAY_BIOME_PROFILES.keys())
TYPE_ORDER = [f"{b}_{lvl}" for b in _CODEX_BIOMES for lvl in FIRING_LEVELS[1:]]  # cracked not tracked

BIOME_DISPLAY_NAMES = {
    "wetland":   "Wetland",
    "tropical":  "Tropical",
    "temperate": "Temperate",
    "river":         "River",
    "mediterranean": "Mediterranean",
    "celadon":       "Celadon",
    "blue_white":    "Blue & White",
    "jun":           "Jun Ware",
}


def classify_shape(profile: list) -> str:
    """Detect pottery shape from a half-width profile (top → bottom)."""
    n = len(profile)
    top    = sum(profile[:n//4])     / (n // 4)
    mid    = sum(profile[n//4:3*n//4]) / (n // 2)
    bottom = sum(profile[3*n//4:])   / (n // 4)
    peak   = max(profile)
    peak_i = profile.index(peak)

    # Amphora: narrow top, wide middle, narrow base with neck
    if top < mid * 0.7 and bottom < mid * 0.75 and mid > 4:
        return "amphora"
    # Pot: wide middle, narrowed at top and bottom
    if top < mid * 0.85 and bottom < mid * 0.85 and mid > 3:
        return "pot"
    # Vase: flared top, pinched lower section
    if top > mid * 0.9 and peak_i < n // 3:
        return "vase"
    # Jug: tall, mostly uniform with slight taper
    if abs(top - bottom) < 1.5 and peak < top + 2:
        return "jug"
    # Jar: short, wide, flat profile
    return "jar"


def profile_evenness(profile: list) -> float:
    """1.0 = perfectly uniform; lower = more variance between rows."""
    if not profile:
        return 1.0
    avg = sum(profile) / len(profile)
    if avg == 0:
        return 1.0
    variance = sum((r - avg) ** 2 for r in profile) / len(profile)
    # normalise: max variance ≈ WHEEL_MAX_RAD² / 4
    norm = min(1.0, variance / (WHEEL_MAX_RAD ** 2 / 4))
    return round(1.0 - norm, 3)


def profile_thickness(profile: list) -> float:
    """Average wall presence relative to WHEEL_MAX_RAD."""
    if not profile:
        return 0.0
    return round(sum(profile) / (len(profile) * WHEEL_MAX_RAD), 3)


def _clamp(v: float) -> float:
    return max(0.0, min(1.0, v))


class PotteryGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, clay_biome: str, profile: list,
                 thickness: float, evenness: float) -> "PotteryPiece":
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid = hashlib.md5(f"pottery_{seed}_{self._counter}".encode()).hexdigest()[:12]
        rng = random.Random(seed)

        profile_copy = CLAY_BIOME_PROFILES.get(clay_biome, CLAY_BIOME_PROFILES["wetland"])

        # Build texture notes from quality attributes
        pool = _TEXTURE_NOTE_POOLS.get(clay_biome, _TEXTURE_NOTE_POOLS["wetland"])
        notes_count = 2 + (1 if evenness > 0.7 else 0) + (1 if thickness > 0.7 else 0)
        notes = rng.sample(pool, min(notes_count, len(pool)))

        return PotteryPiece(
            uid=uid,
            clay_biome=clay_biome,
            shape=classify_shape(profile),
            state="formed",
            firing_level="intact",
            firing_quality=0.0,
            thickness=thickness,
            evenness=evenness,
            glaze_type="",
            texture_notes=notes,
            seed=seed,
            profile=list(profile),
        )


def apply_firing_result(piece: "PotteryPiece", temp_at_stop: float,
                        timing_score: float, temp_control_score: float,
                        shock_penalties: int):
    """Set firing_level and firing_quality from mini-game results."""
    if shock_penalties >= 3:
        piece.firing_level = "cracked"
        piece.firing_quality = 0.0
    elif temp_at_stop < 0.30:
        piece.firing_level = "cracked"   # underfired
        piece.firing_quality = 0.1
    elif temp_at_stop < 0.55:
        piece.firing_level = "intact"
        piece.firing_quality = _clamp(timing_score * 0.5 + temp_control_score * 0.5 - shock_penalties * 0.1)
    elif temp_at_stop < 0.72:
        piece.firing_level = "fine"
        piece.firing_quality = _clamp(timing_score * 0.6 + temp_control_score * 0.4 - shock_penalties * 0.1)
    elif temp_at_stop <= 0.82:
        piece.firing_level = "masterwork"
        piece.firing_quality = _clamp(timing_score * 0.7 + temp_control_score * 0.3 - shock_penalties * 0.1)
    else:
        piece.firing_level = "cracked"   # overfired / melt
        piece.firing_quality = 0.0

    piece.state = "fired"
    piece.evenness = _clamp(piece.evenness + temp_control_score * 0.1)


def apply_pigment_glaze(piece: "PotteryPiece", pigment) -> None:
    """Apply a ground/refined Pigment as a coloured slip glaze.

    The pigment's stability determines how much the firing quality improves;
    purity raises the piece one firing tier (intact→fine, fine→masterwork).
    """
    tier_up = {"intact": "fine", "fine": "masterwork", "masterwork": "masterwork"}
    if pigment.purity >= 0.60:
        piece.firing_level = tier_up.get(piece.firing_level, piece.firing_level)
    piece.firing_quality   = _clamp(piece.firing_quality + pigment.stability * 0.12)
    piece.glaze_type        = "pigment"
    piece.pigment_glaze_color = list(pigment.color_rgb)
    piece.state             = "glazed"


def get_output_item(piece: "PotteryPiece") -> str:
    """Return the item id to grant after firing."""
    if piece.firing_level == "cracked":
        return "cracked_pottery"
    return SHAPE_OUTPUTS.get(piece.shape, SHAPE_OUTPUTS["jar"]).get(piece.firing_level, "cracked_pottery")
