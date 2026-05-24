import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class Textile:
    uid: str
    fiber_type: str        # "wool" | "linen" | "cotton" | "blend" | "silk" | "cashmere" | "jute" | (silk variants)
    state: str             # "thread" | "dyed" | "woven"
    output_type: str       # "cloth" | "rug" | "tapestry" | garment_* (see OUTPUT_DISPLAY)
    texture: str           # "plain" | "twill" | "herringbone" | "diamond" | "brocade" | "damask" | "tartan" | "yunjin" | "kesi" | "song_brocade"
    dye_family: str        # see DYE_FAMILY_COLORS
    dye_color: list        # [R, G, B] stored as list for JSON round-trip
    quality: float         # 0.0–1.0 (set by spinning mini-game)
    softness: float        # 0.0–1.0
    luster: float          # 0.0–1.0
    pattern_quality: float # 0.0–1.0 (set by loom mini-game)
    seed: int
    motif: str = "none"    # see MOTIFS — auto-applied on figured silk weaves


# Base fiber attributes per fiber type
FIBER_PROFILES = {
    "wool":     {"softness": 0.85, "luster": 0.50, "quality_base": 0.55},
    "linen":    {"softness": 0.50, "luster": 0.72, "quality_base": 0.50},
    "cotton":   {"softness": 0.78, "luster": 0.42, "quality_base": 0.58},
    "blend":    {"softness": 0.68, "luster": 0.61, "quality_base": 0.60},
    "silk":         {"softness": 0.95, "luster": 0.92, "quality_base": 0.52},
    "cashmere":     {"softness": 0.98, "luster": 0.78, "quality_base": 0.50},
    "jute":         {"softness": 0.22, "luster": 0.38, "quality_base": 0.72},
    # Wild oak-fed silk — coarser, naturally golden, more robust
    "tussah_silk":  {"softness": 0.70, "luster": 0.80, "quality_base": 0.68},
    # Double-cocoon silk — nubby, rustic, lower luster but high character
    "dupioni_silk": {"softness": 0.78, "luster": 0.70, "quality_base": 0.62},
    # Byssus from pen-shell mollusks — vanishingly rare, brilliant lustre
    "sea_silk":     {"softness": 0.88, "luster": 0.98, "quality_base": 0.55},
}

# Pattern quality modifiers per texture
TEXTURE_PATTERNS = {
    "plain":       {"label": "Plain",       "pattern_mod": 0.00, "desc": "Simple, clean weave."},
    "twill":       {"label": "Twill",       "pattern_mod": 0.10, "desc": "Diagonal rib — durable and supple."},
    "tartan":      {"label": "Tartan",      "pattern_mod": 0.15, "desc": "Crossed bands of woven color."},
    "herringbone": {"label": "Herringbone", "pattern_mod": 0.18, "desc": "V-shaped chevron pattern."},
    "damask":      {"label": "Damask",      "pattern_mod": 0.22, "desc": "Reversible figured silk weave."},
    "diamond":     {"label": "Diamond",     "pattern_mod": 0.28, "desc": "Intricate floating diamond."},
    "brocade":     {"label": "Brocade",     "pattern_mod": 0.35, "desc": "Richly raised ornamental weave."},
    "song_brocade":{"label": "Song Brocade","pattern_mod": 0.38, "desc": "Layered Song-court silk lattice."},
    "yunjin":      {"label": "Yunjin",      "pattern_mod": 0.42, "desc": "Cloud brocade with gold-wrapped weft."},
    "kesi":        {"label": "Kesi",        "pattern_mod": 0.45, "desc": "Cut-silk tapestry, painterly and slow."},
    "luo":         {"label": "Luo Gauze",   "pattern_mod": 0.20, "desc": "Open leno-weave silk gauze."},
    "sha":         {"label": "Sha Sheer",   "pattern_mod": 0.16, "desc": "Featherweight sheer silk."},
    "jin":         {"label": "Jin Brocade", "pattern_mod": 0.40, "desc": "Polychrome warp-faced silk brocade."},
}

# Textures that earn a woven motif when paired with silk fibers.
MOTIF_TEXTURES = {"brocade", "damask", "song_brocade", "yunjin", "kesi", "jin"}

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
    "teal":    [ 40, 160, 165],
    "indigo":  [ 60,  40, 150],
    "ochre":   [195, 155,  30],
    # Chinese-tradition dye families
    "imperial_yellow": [240, 200,  50],
    "cinnabar":        [220,  55,  45],
    "jade":            [110, 180, 140],
    "porcelain_blue":  [ 65, 110, 200],
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
    "teal":    "Teal",
    "indigo":  "Indigo",
    "ochre":   "Ochre",
    "imperial_yellow": "Imperial Yellow",
    "cinnabar":        "Cinnabar",
    "jade":            "Jade",
    "porcelain_blue":  "Porcelain Blue",
}

# Passive bonus stat each garment output type provides
GARMENT_BUFFS = {
    "garment_hat":      "focus",       # +mining speed scaled by quality
    "garment_vest":     "resilience",  # damage reduction scaled by quality
    "garment_boots":    "swiftness",   # +movement speed scaled by quality
    "garment_gloves":   "precision",   # +crafting quality scaled by quality
    "garment_leggings": "endurance",   # -hunger drain scaled by quality
    "garment_cloak":         "warmth",  # cold/night resistance scaled by quality
    "garment_cloak_hooded":  "warmth",
    "garment_cloak_royal":   "warmth",
    "garment_cloak_tattered":"warmth",
    "garment_cloak_half":    "warmth",
    # Chinese-inspired silk wardrobe
    "garment_hanfu":         "grace",      # bartering and reputation
    "garment_qipao":         "charisma",   # NPC affinity
    "garment_changshan":     "scholar",    # research speed
    "garment_magua":         "swiftness",  # mounted/movement
    "garment_douli":         "shelter",    # rain/sun resist
    "garment_silk_slippers": "lightstep",  # silent move, less fall damage
    "garment_ruqun":         "grace",      # skirt+top: bartering bonus
    "garment_beizi":         "scholar",    # long scholar's coat
    "garment_daopao":        "qi",         # Taoist robe: stamina regen
    "garment_mamian":        "swiftness",  # pleated riding skirt
    "garment_yunjian":       "ward",       # shoulder cape: elemental resist
    "garment_fengguan":      "majesty",    # phoenix crown: trade prestige
}

GARMENT_BUFF_DESCS = {
    "focus":      "Mining speed +{:.0f}%",
    "resilience": "Damage taken -{:.0f}%",
    "swiftness":  "Move speed +{:.0f}%",
    "precision":  "Craft quality +{:.0f}%",
    "endurance":  "Hunger drain -{:.0f}%",
    "warmth":     "Cold resist +{:.0f}%",
    "grace":      "Barter prices +{:.0f}%",
    "charisma":   "NPC favor gain +{:.0f}%",
    "scholar":    "Research speed +{:.0f}%",
    "shelter":    "Rain/sun resist +{:.0f}%",
    "lightstep":  "Fall damage -{:.0f}%",
    "qi":         "Stamina regen +{:.0f}%",
    "ward":       "Elemental resist +{:.0f}%",
    "majesty":    "Trade prestige +{:.0f}%",
}

# Max bonus at quality 1.0
GARMENT_MAX_BONUS = {
    "focus":      0.40,
    "resilience": 0.35,
    "swiftness":  0.30,
    "precision":  0.30,
    "endurance":  0.40,
    "warmth":     0.30,
    "grace":      0.25,
    "charisma":   0.30,
    "scholar":    0.30,
    "shelter":    0.45,
    "lightstep":  0.50,
    "qi":         0.35,
    "ward":       0.30,
    "majesty":    0.35,
}

# Passive intrinsic granted per worn piece of a given fiber type (stacks per piece)
FIBER_INTRINSICS = {
    "silk":         {"lucky_drop":  0.08},  # 8% chance per silk piece to double a block drop
    "cashmere":     {"hp_regen":    0.40},  # +0.4 HP/s per cashmere piece (when hunger > 30)
    "jute":         {"move_hunger": 0.08},  # 8% less hunger drain per jute piece while moving
    "wool":         {"warmth_flat": 0.06},  # +6% extra warmth bonus per wool piece
    "linen":        {"day_speed":   0.04},  # +4% daytime speed per linen piece
    "cotton":       {"jump":        0.05},  # +5% jump force per cotton piece
    "blend":        {},
    "tussah_silk":  {"lucky_drop":  0.05, "warmth_flat": 0.04},  # tougher, warmer wild silk
    "dupioni_silk": {"lucky_drop":  0.06, "jump":        0.03},  # springier slubby silk
    "sea_silk":     {"lucky_drop":  0.12},                       # 12% per piece — rarest fiber
}

OUTPUT_DISPLAY = {
    "cloth":            "Artisan Cloth",
    "rug":              "Rug",
    "tapestry":         "Tapestry",
    "garment_hat":      "Woven Hat",
    "garment_vest":     "Woven Vest",
    "garment_boots":    "Woven Boots",
    "garment_gloves":   "Woven Gloves",
    "garment_leggings": "Woven Leggings",
    "garment_cloak":          "Woven Cloak",
    "garment_cloak_hooded":   "Hooded Cloak",
    "garment_cloak_royal":    "Royal Mantle",
    "garment_cloak_tattered": "Tattered Cloak",
    "garment_cloak_half":     "Half Cape",
    "garment_hanfu":          "Hanfu Robe",
    "garment_qipao":          "Qipao",
    "garment_changshan":      "Changshan",
    "garment_magua":          "Magua Jacket",
    "garment_douli":          "Douli Hat",
    "garment_silk_slippers":  "Silk Slippers",
    "garment_ruqun":          "Ruqun Set",
    "garment_beizi":          "Beizi Coat",
    "garment_daopao":         "Daopao Robe",
    "garment_mamian":         "Mamian Skirt",
    "garment_yunjian":        "Yunjian Collar",
    "garment_fengguan":       "Fengguan Crown",
}

# Wardrobe slot each garment output type occupies.
GARMENT_SLOTS = {
    "garment_hat":      "head",
    "garment_vest":     "chest",
    "garment_boots":    "feet",
    "garment_gloves":   "hands",
    "garment_leggings": "legs",
    "garment_cloak":          "back",
    "garment_cloak_hooded":   "back",
    "garment_cloak_royal":    "back",
    "garment_cloak_tattered": "back",
    "garment_cloak_half":     "back",
    "garment_hanfu":          "chest",
    "garment_qipao":          "chest",
    "garment_changshan":      "chest",
    "garment_magua":          "back",
    "garment_douli":          "head",
    "garment_silk_slippers":  "feet",
    "garment_ruqun":          "chest",
    "garment_beizi":          "back",
    "garment_daopao":         "chest",
    "garment_mamian":         "legs",
    "garment_yunjian":        "chest",
    "garment_fengguan":       "head",
}

# Woven figure motifs — applied automatically when a silk-class fiber is woven
# on a figured/brocade-class texture.  Stored on the Textile for codex/display.
MOTIFS = {
    "none":    {"label": "Plain",          "luster_bonus": 0.00, "pattern_bonus": 0.00},
    "dragon":  {"label": "Dragon",         "luster_bonus": 0.08, "pattern_bonus": 0.06},
    "phoenix": {"label": "Phoenix",        "luster_bonus": 0.08, "pattern_bonus": 0.05},
    "crane":   {"label": "Crane",          "luster_bonus": 0.05, "pattern_bonus": 0.04},
    "plum":    {"label": "Plum Blossom",   "luster_bonus": 0.04, "pattern_bonus": 0.03},
    "lotus":   {"label": "Lotus",          "luster_bonus": 0.04, "pattern_bonus": 0.04},
    "cloud":   {"label": "Auspicious Cloud","luster_bonus": 0.05, "pattern_bonus": 0.05},
    "bat":     {"label": "Five Bats",      "luster_bonus": 0.04, "pattern_bonus": 0.04},
    "peony":   {"label": "Peony",          "luster_bonus": 0.06, "pattern_bonus": 0.05},
    "bamboo":  {"label": "Bamboo",         "luster_bonus": 0.03, "pattern_bonus": 0.04},
    "qilin":   {"label": "Qilin",          "luster_bonus": 0.09, "pattern_bonus": 0.07},
}

# Fibers that count as "silk-class" for restriction + motif rules.
SILK_FIBERS = {"silk", "tussah_silk", "dupioni_silk", "sea_silk"}

# Garments that may only be woven from silk-class fibers.
SILK_ONLY_OUTPUTS = {
    "garment_hanfu", "garment_qipao", "garment_changshan",
    "garment_magua", "garment_silk_slippers",
    "garment_ruqun", "garment_beizi", "garment_daopao",
    "garment_yunjian", "garment_fengguan",
    # mamian skirt allowed in any fiber — peasant + court variants both exist
}

_FIBER_DISPLAY = {
    "wool": "Wool", "linen": "Linen", "cotton": "Cotton", "blend": "Blend",
    "silk": "Silk", "cashmere": "Cashmere", "jute": "Jute",
    "tussah_silk": "Tussah Silk", "dupioni_silk": "Dupioni Silk", "sea_silk": "Sea Silk",
}
_OUTPUT_TYPES  = [
    "cloth", "rug", "tapestry",
    "garment_hat", "garment_vest", "garment_boots",
    "garment_gloves", "garment_leggings",
    "garment_cloak", "garment_cloak_hooded", "garment_cloak_royal",
    "garment_cloak_tattered", "garment_cloak_half",
    "garment_hanfu", "garment_qipao", "garment_changshan",
    "garment_magua", "garment_douli", "garment_silk_slippers",
    "garment_ruqun", "garment_beizi", "garment_daopao",
    "garment_mamian", "garment_yunjian", "garment_fengguan",
]
_FIBERS        = ["wool", "linen", "cotton", "blend", "silk", "cashmere", "jute",
                  "tussah_silk", "dupioni_silk", "sea_silk"]
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
    """Map an arbitrary RGB tuple to one of the dye families by rough hue."""
    r, g, b = rgb
    mx = max(r, g, b)
    mn = min(r, g, b)
    chroma = mx - mn

    # Chinese-tradition families: very saturated, recognizable signatures.
    # Tested before the generic heuristics so a pigment ground from cinnabar
    # ore (or a porcelain-blue mineral) routes to the right family.
    if chroma >= 60:
        if r > 215 and 180 < g < 225 and b < 90:
            return "imperial_yellow"
        if r > 200 and g < 90 and b < 80:
            return "cinnabar"
        if 90 < r < 140 and g > 160 and 120 < b < 170:
            return "jade"
        if r < 100 and 90 < g < 140 and b > 180:
            return "porcelain_blue"

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
        if g > 130:
            return "teal"    # high green+blue, low red
        if g < 70:
            return "indigo"  # deep blue, very low green
        return "cobalt"      # blue dominant
    # Green dominant
    if g >= r and g >= b:
        if r > 150:
            return "rose"    # pinkish
        return "verdant"
    # Ochre: warm yellow-brown (r dominant, moderate g, low b)
    if r >= g and r >= b and 100 <= g <= 165 and b < 60:
        return "ochre"

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


def apply_pigment_dye(textile: "Textile", pigment) -> None:
    """Dye thread using a ground/refined Pigment object.

    Uses the pigment's exact RGB rather than a generic family swatch, so
    the stored dye_color reflects the true hue.  Purity boosts luster;
    stability gives a small quality lift.
    """
    fam = dye_family_from_color(pigment.color_rgb)
    textile.dye_family = fam
    textile.dye_color  = list(pigment.color_rgb)
    textile.luster     = _clamp(textile.luster  + pigment.purity   * 0.15)
    textile.quality    = _clamp(textile.quality + pigment.stability * 0.05)
    textile.state      = "dyed"


def apply_weave(textile: "Textile", output_type: str, texture: str, pattern_quality: float):
    """Mutate textile to woven state with chosen output type, texture, and loom quality.

    If the fiber is silk-class and the texture is in MOTIF_TEXTURES, a figured
    motif is rolled in (dragon, phoenix, crane, etc.) and contributes small
    pattern_quality and luster bonuses.
    """
    textile.output_type = output_type
    textile.texture = texture
    texture_mod = TEXTURE_PATTERNS.get(texture, TEXTURE_PATTERNS["plain"])["pattern_mod"]
    if texture in MOTIF_TEXTURES and textile.fiber_type in SILK_FIBERS:
        motif_rng = random.Random(textile.seed ^ hash(texture))
        motif_key = motif_rng.choice([m for m in MOTIFS.keys() if m != "none"])
        textile.motif = motif_key
        m = MOTIFS[motif_key]
        textile.pattern_quality = _clamp(pattern_quality + texture_mod + m["pattern_bonus"])
        textile.luster = _clamp(textile.luster + m["luster_bonus"])
    else:
        textile.motif = "none"
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
    if ot in GARMENT_SLOTS:
        return ot
    return "textile_cloth"


def can_weave(fiber_type: str, output_type: str) -> bool:
    """Return False when an output is gated to silk-class fibers and the
    selected fiber is not silk-class."""
    if output_type in SILK_ONLY_OUTPUTS and fiber_type not in SILK_FIBERS:
        return False
    return True


def motif_label(textile: "Textile") -> str:
    """Display label for the textile's woven motif (empty for plain)."""
    if textile.motif and textile.motif != "none":
        return MOTIFS.get(textile.motif, {}).get("label", textile.motif.title())
    return ""


def discovery_key(textile: "Textile") -> str:
    return f"{textile.fiber_type}_{textile.dye_family}_{textile.output_type}"
