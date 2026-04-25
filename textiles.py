import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class Textile:
    uid: str
    fiber_type: str        # "wool" | "linen" | "cotton" | "blend"
    state: str             # "thread" | "dyed" | "woven"
    output_type: str       # "cloth" | "rug" | "tapestry" | "garment_hat" | "garment_vest" | "garment_boots"
    texture: str           # "plain" | "twill" | "herringbone" | "diamond"
    dye_family: str        # "natural" | "golden" | "crimson" | "rose" | "cobalt" | "violet" | "verdant" | "amber" | "ivory"
    dye_color: list        # [R, G, B] stored as list for JSON round-trip
    quality: float         # 0.0–1.0 (set by spinning mini-game)
    softness: float        # 0.0–1.0
    luster: float          # 0.0–1.0
    pattern_quality: float # 0.0–1.0 (set by loom mini-game)
    seed: int


# Base fiber attributes per fiber type
FIBER_PROFILES = {
    "wool":   {"softness": 0.85, "luster": 0.50, "quality_base": 0.55},
    "linen":  {"softness": 0.50, "luster": 0.72, "quality_base": 0.50},
    "cotton": {"softness": 0.78, "luster": 0.42, "quality_base": 0.58},
    "blend":  {"softness": 0.68, "luster": 0.61, "quality_base": 0.60},
}

# Pattern quality modifiers per texture
TEXTURE_PATTERNS = {
    "plain":       {"label": "Plain",       "pattern_mod": 0.00, "desc": "Simple, clean weave."},
    "twill":       {"label": "Twill",       "pattern_mod": 0.10, "desc": "Diagonal rib — durable and supple."},
    "herringbone": {"label": "Herringbone", "pattern_mod": 0.18, "desc": "V-shaped chevron pattern."},
    "diamond":     {"label": "Diamond",     "pattern_mod": 0.28, "desc": "Intricate floating diamond."},
}

# Canonical RGB for each dye family (for block colors and display swatches)
DYE_FAMILY_COLORS = {
    "natural": [230, 215, 185],
    "golden":  [215, 175,  40],
    "crimson": [185,  35,  45],
    "rose":    [220, 110, 155],
    "cobalt":  [ 55,  90, 185],
    "violet":  [130,  65, 195],
    "verdant": [ 60, 148,  75],
    "amber":   [200, 115,  35],
    "ivory":   [245, 240, 220],
}

DYE_FAMILY_DISPLAY = {
    "natural": "Natural",
    "golden":  "Golden",
    "crimson": "Crimson",
    "rose":    "Rose",
    "cobalt":  "Cobalt",
    "violet":  "Violet",
    "verdant": "Verdant",
    "amber":   "Amber",
    "ivory":   "Ivory",
}

# Passive bonus stat each garment output type provides
GARMENT_BUFFS = {
    "garment_hat":   "focus",       # +mining speed scaled by quality
    "garment_vest":  "resilience",  # damage reduction scaled by quality
    "garment_boots": "swiftness",   # +movement speed scaled by quality
}

GARMENT_BUFF_DESCS = {
    "focus":      "Mining speed +{:.0f}%",
    "resilience": "Damage taken -{:.0f}%",
    "swiftness":  "Move speed +{:.0f}%",
}

# Max bonus at quality 1.0
GARMENT_MAX_BONUS = {
    "focus":      0.25,
    "resilience": 0.20,
    "swiftness":  0.20,
}

OUTPUT_DISPLAY = {
    "cloth":        "Artisan Cloth",
    "rug":          "Rug",
    "tapestry":     "Tapestry",
    "garment_hat":  "Woven Hat",
    "garment_vest": "Woven Vest",
    "garment_boots":"Woven Boots",
}

_FIBER_DISPLAY = {"wool": "Wool", "linen": "Linen", "cotton": "Cotton", "blend": "Blend"}
_OUTPUT_TYPES  = ["cloth", "rug", "tapestry", "garment_hat", "garment_vest", "garment_boots"]
_FIBERS        = ["wool", "linen", "cotton", "blend"]
_DYE_FAMILIES  = list(DYE_FAMILY_COLORS.keys())

TYPE_ORDER = [
    f"{fiber}_{dye}_{output}"
    for fiber in _FIBERS
    for dye in _DYE_FAMILIES
    for output in _OUTPUT_TYPES
]

TOTAL_TEXTILE_TYPES = len(TYPE_ORDER)


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def dye_family_from_color(rgb):
    """Map an arbitrary RGB tuple to one of the 9 dye families by rough hue."""
    r, g, b = rgb
    mx = max(r, g, b)
    mn = min(r, g, b)
    chroma = mx - mn

    # Near-white / ivory
    if mx > 210 and chroma < 40:
        return "ivory"
    # Near-neutral / muted — call it natural
    if chroma < 35:
        return "natural"

    # Dominant channel heuristics
    if r >= g and r >= b:
        if g > b + 40:
            return "amber"   # red+green = orange/amber
        if g > 130 and b < 100:
            return "golden"  # warm yellow
        return "crimson"     # red dominant
    if b >= r and b >= g:
        if r > 120:
            return "violet"  # red+blue = violet/purple
        return "cobalt"      # blue dominant
    # Green dominant
    if g >= r and g >= b:
        if r > 150:
            return "rose"    # pinkish
        return "verdant"

    return "natural"


class TextileGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, fiber_type: str) -> "Textile":
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid = hashlib.md5(f"textile_{seed}_{self._counter}".encode()).hexdigest()[:12]
        rng = random.Random(seed)

        profile = FIBER_PROFILES.get(fiber_type, FIBER_PROFILES["wool"])

        def jitter(base, sigma=0.08):
            return _clamp(base + rng.gauss(0, sigma))

        return Textile(
            uid=uid,
            fiber_type=fiber_type,
            state="thread",
            output_type="cloth",
            texture="plain",
            dye_family="natural",
            dye_color=list(DYE_FAMILY_COLORS["natural"]),
            quality=jitter(profile["quality_base"]),
            softness=jitter(profile["softness"]),
            luster=jitter(profile["luster"]),
            pattern_quality=0.0,
            seed=seed,
        )


def apply_dye(textile: "Textile", dye_family: str):
    """Mutate thread to dyed state; updates dye_family, dye_color, luster."""
    textile.dye_family = dye_family
    textile.dye_color = list(DYE_FAMILY_COLORS.get(dye_family, DYE_FAMILY_COLORS["natural"]))
    textile.luster = _clamp(textile.luster + 0.12)
    textile.state = "dyed"


def apply_weave(textile: "Textile", output_type: str, texture: str, pattern_quality: float):
    """Mutate textile to woven state with chosen output type, texture, and loom quality."""
    textile.output_type = output_type
    textile.texture = texture
    texture_mod = TEXTURE_PATTERNS.get(texture, TEXTURE_PATTERNS["plain"])["pattern_mod"]
    textile.pattern_quality = _clamp(pattern_quality + texture_mod)
    textile.state = "woven"


def get_garment_bonus(textile: "Textile") -> float:
    """Return the passive stat bonus (0.0–max) for a woven garment."""
    if textile.output_type not in GARMENT_BUFFS:
        return 0.0
    stat = GARMENT_BUFFS[textile.output_type]
    max_b = GARMENT_MAX_BONUS[stat]
    return _clamp(textile.quality * max_b, 0.0, max_b)


def output_item_key(textile: "Textile") -> str:
    """Return the inventory item key to grant when a textile is woven."""
    ot = textile.output_type
    df = textile.dye_family
    if ot == "rug":
        return f"textile_rug_{df}"
    if ot == "tapestry":
        return f"textile_tapestry_{df}"
    if ot in ("garment_hat", "garment_vest", "garment_boots"):
        return ot
    return "textile_cloth"


def discovery_key(textile: "Textile") -> str:
    return f"{textile.fiber_type}_{textile.dye_family}_{textile.output_type}"
