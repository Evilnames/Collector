"""Numismatic collectible system.

CoinGenerator builds 100+ coin types from the world seed at init time (stable
per save). Individual Coin objects are generated when a COIN_CACHE_BLOCK is
mined, when a ruin chest is looted, or when purchased from a coin trader.
"""
import random
import hashlib
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Name / text pools
# ---------------------------------------------------------------------------

_CIV_PRE = [
    "Aur", "Val", "Mag", "Cor", "Sen", "Kel", "Mor", "Drac", "Ith", "Zar",
    "Ber", "Gal", "Mon", "Tor", "Sal", "Pyr", "Ven", "Cal", "Dar", "Eld",
    "Ost", "Kra", "Vyn", "Thal", "Myr", "Bel", "Str", "Cyr", "Omn", "Arx",
    "Hel", "Nor", "Sax", "Umb", "Rav", "Pel", "Qor", "Ixm", "Zan", "Fel",
]
_CIV_SUF = [
    "um", "ia", "or", "ania", "eum", "is", "ara", "idor", "eth", "oss",
    "ix", "ari", "un", "el", "on", "ax", "ath", "yn", "os", "ern",
    "ond", "ima", "ela", "ys", "an", "esh", "id", "ium", "ica", "ova",
    "rix", "ath", "orr", "ind", "ula", "ena", "ard", "oth", "esh", "inar",
]

_RULER_FIRST = [
    "Maximus", "Valeria", "Tiberius", "Draco", "Cassia", "Mordain", "Seraphel",
    "Korvin", "Ithel", "Zara", "Aldric", "Pyrona", "Celindra", "Gareth",
    "Vyndra", "Myrion", "Isolde", "Theron", "Braxis", "Calyx", "Osara",
    "Kravin", "Elda", "Beryn", "Stryx", "Cyren", "Omaria", "Arxia", "Vela",
    "Doriv", "Tahla", "Exon", "Unara", "Kelsa", "Serith", "Bavron", "Tolmir",
    "Ixara", "Zaneth", "Felion", "Norvik", "Saxen", "Umbra", "Ravon", "Pelios",
]

_RULER_TITLES = {
    "classical":  ["Imperator", "Rex", "Dominus", "Consul", "Princeps", "Augustus"],
    "medieval":   ["Rex", "Regina", "Dux", "Comes", "Princeps", "Khan", "Sultan", "Basileus"],
    "eastern":    ["Wang", "Tian", "Emir", "Shah", "Khagan", "Shogun", "Pharaoh"],
    "merchant":   ["Doge", "Capitano", "Provost", "Lord", "Mayor", "Baas", "Syndic"],
    "imperial":   ["Kaiser", "Koenig", "Furst", "Markgraf", "Herzog", "Graf"],
    "gallic":     ["Rix", "Vergo", "Touta", "Rex", "Tigernos", "Uergobretus"],
}

_MINT_MID = ["op", "ul", "ar", "en", "el", "or", "um", "is", "ix", "an", "on", "os", "ev", "al"]
_MINT_SUF = ["is", "um", "a", "on", "ia", "ax", "os", "ium", "ath", "ica", "ora", "ena"]

# ---------------------------------------------------------------------------
# Currency systems  (key, label_template using {s}=civ_short, relative value, rarity pool)
# ---------------------------------------------------------------------------

_CURRENCY_SYSTEMS = {
    "classical": [
        {"key": "as",         "label": "{s} As",        "value": 1,    "rp": ["common", "common", "common", "uncommon"]},
        {"key": "sestertius", "label": "{s} Sestertius", "value": 4,    "rp": ["common", "common", "uncommon"]},
        {"key": "denarius",   "label": "{s} Denarius",  "value": 16,   "rp": ["common", "uncommon", "rare"]},
        {"key": "aureus",     "label": "{s} Aureus",    "value": 400,  "rp": ["uncommon", "rare", "epic"]},
        {"key": "solidus",    "label": "{s} Solidus",   "value": 800,  "rp": ["rare", "epic", "legendary"]},
    ],
    "medieval": [
        {"key": "farthing",   "label": "{s} Farthing",  "value": 1,    "rp": ["common", "common", "common", "uncommon"]},
        {"key": "penny",      "label": "{s} Penny",     "value": 4,    "rp": ["common", "common", "uncommon"]},
        {"key": "groat",      "label": "{s} Groat",     "value": 16,   "rp": ["common", "uncommon", "rare"]},
        {"key": "shilling",   "label": "{s} Shilling",  "value": 60,   "rp": ["uncommon", "rare"]},
        {"key": "sovereign",  "label": "{s} Sovereign", "value": 240,  "rp": ["rare", "epic"]},
        {"key": "noble",      "label": "{s} Noble",     "value": 480,  "rp": ["epic", "legendary"]},
    ],
    "eastern": [
        {"key": "cash",       "label": "{s} Cash",      "value": 1,    "rp": ["common", "common", "common", "uncommon"]},
        {"key": "fen",        "label": "{s} Fen",       "value": 10,   "rp": ["common", "uncommon"]},
        {"key": "yuan",       "label": "{s} Yuan",      "value": 100,  "rp": ["uncommon", "rare"]},
        {"key": "tael",       "label": "{s} Tael",      "value": 500,  "rp": ["rare", "epic"]},
        {"key": "ingot",      "label": "{s} Ingot",     "value": 2000, "rp": ["epic", "legendary"]},
    ],
    "merchant": [
        {"key": "bit",        "label": "{s} Bit",       "value": 1,    "rp": ["common", "common", "uncommon"]},
        {"key": "piece",      "label": "{s} Piece",     "value": 8,    "rp": ["common", "uncommon", "rare"]},
        {"key": "mark",       "label": "{s} Mark",      "value": 32,   "rp": ["uncommon", "rare"]},
        {"key": "royal",      "label": "{s} Royal",     "value": 128,  "rp": ["rare", "epic", "legendary"]},
    ],
    "imperial": [
        {"key": "pfennig",    "label": "{s} Pfennig",   "value": 1,    "rp": ["common", "common", "common", "uncommon"]},
        {"key": "groschen",   "label": "{s} Groschen",  "value": 12,   "rp": ["common", "uncommon"]},
        {"key": "kreuzer",    "label": "{s} Kreuzer",   "value": 6,    "rp": ["common", "uncommon"]},
        {"key": "thaler",     "label": "{s} Thaler",    "value": 90,   "rp": ["uncommon", "rare"]},
        {"key": "ducat",      "label": "{s} Ducat",     "value": 360,  "rp": ["rare", "epic"]},
    ],
    "gallic": [
        {"key": "potin",      "label": "{s} Potin",     "value": 1,    "rp": ["common", "common", "uncommon"]},
        {"key": "quarter",    "label": "{s} Quarter",   "value": 5,    "rp": ["common", "uncommon", "rare"]},
        {"key": "stater",     "label": "{s} Stater",    "value": 20,   "rp": ["uncommon", "rare"]},
        {"key": "gold_stater","label": "{s} Gold Stater","value": 80,  "rp": ["rare", "epic", "legendary"]},
    ],
}

_ERAS = {
    "ancient":       {"label": "Ancient",      "year_range": (-900, -300), "currency": ["classical", "gallic"]},
    "classical":     {"label": "Classical",    "year_range": (-300,  400), "currency": ["classical", "eastern"]},
    "medieval":      {"label": "Medieval",     "year_range": ( 400, 1100), "currency": ["medieval", "eastern"]},
    "late_medieval": {"label": "Late Medieval","year_range": (1100, 1450), "currency": ["medieval", "imperial", "merchant"]},
    "renaissance":   {"label": "Renaissance",  "year_range": (1450, 1650), "currency": ["imperial", "merchant", "medieval"]},
}

# ---------------------------------------------------------------------------
# Motifs
# ---------------------------------------------------------------------------

_OBVERSE = [
    "Ruler portrait laureate", "Helmeted profile", "Veiled queen portrait",
    "Bearded king facing right", "Radiate crown profile", "Diademed bust",
    "Armoured general left", "Draped empress right", "Young prince bust",
    "Abstract sunburst face", "Stylised deity head", "Torc-wearing chieftain",
    "Facing Gorgon mask", "Winged victory bust", "Seated ruler enthroned",
    "Beardless youth with laurel", "Stern matriarch right-facing",
]

_REVERSE = [
    "Eagle with spread wings", "Lion passant", "Bull charging",
    "Serpent coiled round staff", "Galley under oars", "Chariot drawn by horses",
    "Temple of four columns", "Triumphal arch", "Mint monogram in wreath",
    "Wheat sheaf bound", "Palm tree with dates", "Laurel wreath encircling value",
    "Crescent and star", "Crossed swords", "Scales of justice",
    "Griffin rampant", "Dolphin leaping", "Owl on amphora",
    "Castle with three towers", "Ship's prow", "Cornucopia overflowing",
    "Thunderbolt of the gods", "Trident upright", "Double-headed axe",
    "Rose en soleil", "Fleur-de-lis", "Rampant horse",
    "Seated deity holding sceptre", "Standing warrior with spear",
    "Phoenix rising from flames", "Two fish counter-swimming",
    "Hammer and anvil", "Tower by the sea",
]

# ---------------------------------------------------------------------------
# Condition / rarity constants
# ---------------------------------------------------------------------------

CONDITIONS = ["poor", "fair", "good", "fine", "very_fine", "mint"]
CONDITION_LABELS = {
    "poor":      "Poor — heavily worn, details mostly lost",
    "fair":      "Fair — well worn, major features visible",
    "good":      "Good — moderate wear, design clear",
    "fine":      "Fine — light wear, high points smooth",
    "very_fine": "Very Fine — slight wear on high points only",
    "mint":      "Mint State — uncirculated, full lustre",
}
CONDITION_SHORT = {
    "poor": "P", "fair": "F", "good": "G",
    "fine": "VF", "very_fine": "EF", "mint": "MS",
}

RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary"]
RARITY_COLORS = {
    "common":    (180, 180, 180),
    "uncommon":  (100, 210,  90),
    "rare":      (100, 160, 255),
    "epic":      (190, 100, 240),
    "legendary": (255, 210,  50),
}
RARITY_BG = {
    "common":    (30, 30, 35),
    "uncommon":  (18, 38, 18),
    "rare":      (18, 28, 58),
    "epic":      (38, 18, 52),
    "legendary": (48, 38,  8),
}

# ---------------------------------------------------------------------------
# Visual metadata — metal types, portrait parameters
# ---------------------------------------------------------------------------

DENOMINATION_METALS = {
    "as":        "copper",   "farthing":   "copper",  "cash":       "copper",
    "pfennig":   "copper",   "potin":      "bronze",  "bit":        "bronze",
    "sestertius":"billon",   "penny":      "silver",  "fen":        "billon",
    "groschen":  "billon",   "kreuzer":    "billon",  "quarter":    "silver",
    "denarius":  "silver",   "groat":      "silver",  "shilling":   "silver",
    "yuan":      "silver",   "mark":       "silver",  "thaler":     "silver",
    "stater":    "silver",   "piece":      "silver",
    "aureus":    "gold",     "sovereign":  "gold",    "tael":       "gold",
    "royal":     "gold",     "ducat":      "gold",    "gold_stater":"gold",
    "solidus":   "electrum", "noble":      "gold",    "ingot":      "gold",
}

# (base_col, highlight_col, shadow_col, patina_col)
METAL_COLORS = {
    "copper":  ((172,  85, 45), (220, 130,  80), (110,  50, 25), ( 80, 140,  90)),
    "bronze":  ((150, 100, 50), (195, 145,  85), ( 95,  65, 30), ( 70, 120,  80)),
    "billon":  ((130, 120, 90), (170, 160, 125), ( 85,  80, 55), ( 90, 100,  80)),
    "silver":  ((185, 185,200), (230, 230, 240), (120, 120,135), ( 60,  60,  70)),
    "electrum":((200, 185, 90), (240, 230, 140), (135, 125, 55), (120, 115,  60)),
    "gold":    ((215, 175, 45), (255, 225, 110), (155, 120, 30), (160, 135,  40)),
}

_CROWN_TYPES = {
    "classical": ["laurel", "radiate", "diadem", "helmet"],
    "medieval":  ["crown",  "helmet",  "circlet", "coif"],
    "eastern":   ["mitra",  "helmet",  "crown",   "none"],
    "merchant":  ["cap",    "circlet", "none",    "hat"],
    "imperial":  ["crown",  "helmet",  "circlet", "laurel"],
    "gallic":    ["helmet", "torc",    "boar_crest", "laurel"],
}


def coin_metal(denomination_key: str) -> str:
    return DENOMINATION_METALS.get(denomination_key, "silver")


def coin_portrait_params(coin: "Coin") -> dict:
    """Deterministic portrait visual parameters derived from coin seed."""
    rng = random.Random(coin.seed ^ 0xFACEC01A)
    crown_pool = _CROWN_TYPES.get(coin.currency_system, _CROWN_TYPES["classical"])
    return {
        "facing_right": rng.random() < 0.55,
        "crown":        rng.choice(crown_pool),
        "beard":        rng.random() < 0.42,
        "age":          rng.choice(["young", "middle", "old"]),
        "bust":         rng.choice(["draped", "armoured", "laureate"]),
    }

_RARITY_CONDITION_WEIGHTS = {
    "common":    [50, 25, 13, 7, 4, 1],
    "uncommon":  [22, 25, 25, 18, 8, 2],
    "rare":      [6,  14, 24, 30, 20, 6],
    "epic":      [2,   6, 14, 26, 34, 18],
    "legendary": [0,   2,  6, 14, 36, 42],
}

# Spawn weight for each rarity tier when picking from a cache
_RARITY_SPAWN_WEIGHT = {
    "common": 8, "uncommon": 4, "rare": 2, "epic": 0.8, "legendary": 0.15,
}

# ---------------------------------------------------------------------------
# Error coins
# ---------------------------------------------------------------------------

ERROR_TYPES = {
    "double_strike":    {
        "label": "Double Strike",
        "desc":  "Die struck twice with slight offset — design appears doubled",
    },
    "off_center":       {
        "label": "Off-Center Strike",
        "desc":  "Die misaligned at striking — design shifted to one side",
    },
    "clipped_planchet": {
        "label": "Clipped Planchet",
        "desc":  "Blank was clipped before striking — irregular scalloped edge",
    },
    "die_crack":        {
        "label": "Die Crack",
        "desc":  "Crack in the die left a raised line across the face",
    },
    "wrong_metal":      {
        "label": "Wrong Metal",
        "desc":  "Struck on a blank of incorrect metal — a rare minter's error",
    },
    "brockage":         {
        "label": "Brockage",
        "desc":  "Incuse mirror-image impression — previous coin stuck in the die",
    },
}

_ERROR_KEYS   = list(ERROR_TYPES.keys())
_ERROR_CHANCE = {
    "common": 0.0, "uncommon": 0.02, "rare": 0.06, "epic": 0.14, "legendary": 0.28,
}

# ---------------------------------------------------------------------------
# Provenance lore
# ---------------------------------------------------------------------------

_PROVENANCE_TEMPLATES = [
    "Recovered from a sunken merchant vessel of the {era_label} era",
    "Unearthed beneath the ruins of {mint_city}",
    "Found in the sealed treasury of {ruler_name}",
    "Salvaged from a {civilization_name} battlefield cache",
    "Excavated from the estate of a {era_label} nobleman",
    "Pulled from a collapsed coin hoard near {mint_city}",
    "Discovered in the tomb of a {civilization_name} dignitary",
    "Acquired from a {era_label} antiquarian's estate sale",
    "Recovered during excavation of the {mint_city} forum",
    "Looted from a {civilization_name} temple strongroom",
    "Found sealed in a clay amphora buried in {mint_city}",
    "Inherited through a merchant family of {civilization_name}",
    "Surfaced at a {era_label} coin fair — provenance disputed",
    "Unearthed in a farmer's field outside {mint_city}",
    "Recovered from the wreck of a {civilization_name} war galley",
    "Struck under {ruler_name} — hoarded and never circulated",
]

_PROVENANCE_CHANCE = 0.12

# ---------------------------------------------------------------------------
# Coin dataclass
# ---------------------------------------------------------------------------

@dataclass
class Coin:
    uid:                str
    coin_type_id:       str
    civilization_name:  str
    civ_short:          str
    era_label:          str
    year:               int     # negative = BCE
    currency_system:    str
    denomination_key:   str
    denomination_label: str
    face_value:         int     # relative to smallest denom in that system
    obverse_motif:      str
    reverse_motif:      str
    ruler_name:         str
    mint_city:          str
    condition:          str
    rarity:             str
    seed:               int
    error_type:         str = ""   # key into ERROR_TYPES, empty = no error
    provenance:         str = ""   # lore string, empty = none

    @property
    def year_label(self) -> str:
        return f"{abs(self.year)} BCE" if self.year < 0 else f"{self.year} CE"

    @property
    def display_name(self) -> str:
        return f"{self.denomination_label} ({self.year_label})"

    @property
    def condition_short(self) -> str:
        return CONDITION_SHORT.get(self.condition, "?")

    @property
    def error_label(self) -> str:
        return ERROR_TYPES[self.error_type]["label"] if self.error_type else ""

    @property
    def is_error_coin(self) -> bool:
        return bool(self.error_type)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class CoinGenerator:
    """Generates the civilization registry and individual coins.

    Call _build_type_registry() once (done in __init__). The registry is
    deterministic for a given world_seed — the same 100+ coin types appear
    every run.
    """

    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter    = 0
        self.coin_types:    dict = {}   # type_id → type_def
        self.civilizations: list = []   # ordered list of civ_defs
        self._build_type_registry()

    # ── Registry construction ────────────────────────────────────────────

    def _make_civ_name(self, rng: random.Random) -> tuple:
        """Return (full_name, short_4)."""
        name  = rng.choice(_CIV_PRE) + rng.choice(_CIV_SUF)
        short = name[:4].upper()
        return name, short

    def _make_mint_city(self, rng: random.Random, civ_name: str) -> str:
        return civ_name[:3].capitalize() + rng.choice(_MINT_MID) + rng.choice(_MINT_SUF)

    def _build_type_registry(self):
        era_keys = list(_ERAS.keys())
        n_civs   = 22   # produces ~100 types across all denominations

        for i in range(n_civs):
            seed_i  = (self._world_seed ^ (i * 0x7B4A31) ^ 0x11C0223) & 0xFFFFFFFF
            rng     = random.Random(seed_i)

            civ_name, civ_short = self._make_civ_name(rng)
            # Avoid duplicate names (rare, but guard it)
            while any(c["name"] == civ_name for c in self.civilizations):
                civ_name = rng.choice(_CIV_PRE) + rng.choice(_CIV_SUF)
                civ_short = civ_name[:4].upper()

            era_key   = era_keys[i % len(era_keys)]
            era       = _ERAS[era_key]
            sys_key   = rng.choice(era["currency"])
            denoms    = _CURRENCY_SYSTEMS[sys_key]
            title_pool = _RULER_TITLES.get(sys_key, _RULER_TITLES["classical"])
            mint_city  = self._make_mint_city(rng, civ_name)

            civ_def = {
                "name": civ_name, "short": civ_short,
                "era_key": era_key, "era_label": era["label"],
                "year_range": era["year_range"],
                "currency_system": sys_key,
                "title_pool": title_pool,
                "mint_city": mint_city,
                "denom_keys": [d["key"] for d in denoms],
            }
            self.civilizations.append(civ_def)

            for denom in denoms:
                type_id = f"{civ_name.lower()}_{denom['key']}"
                self.coin_types[type_id] = {
                    "civilization_name": civ_name,
                    "civ_short":         civ_short,
                    "era_label":         era["label"],
                    "era_key":           era_key,
                    "year_range":        era["year_range"],
                    "currency_system":   sys_key,
                    "denomination_key":  denom["key"],
                    "denomination_label":denom["label"].format(s=civ_short),
                    "face_value":        denom["value"],
                    "rarity_pool":       denom["rp"],
                    "mint_city":         mint_city,
                    "title_pool":        title_pool,
                }

    # ── Individual coin generation ────────────────────────────────────────

    def _make_error_and_provenance(self, rng: random.Random, rarity: str,
                                      td: dict, ruler_name: str) -> tuple:
        """Return (error_type, provenance) strings for a coin."""
        error_type = ""
        if _ERROR_CHANCE.get(rarity, 0) > 0 and rng.random() < _ERROR_CHANCE[rarity]:
            error_type = rng.choice(_ERROR_KEYS)
        provenance = ""
        if rng.random() < _PROVENANCE_CHANCE:
            tmpl = rng.choice(_PROVENANCE_TEMPLATES)
            provenance = tmpl.format(
                era_label         = td["era_label"],
                mint_city         = td["mint_city"],
                ruler_name        = ruler_name,
                civilization_name = td["civilization_name"],
            )
        return error_type, provenance

    def _pick_type(self, rng: random.Random) -> str:
        """Weighted random type: common denoms appear far more than gold."""
        ids     = list(self.coin_types.keys())
        weights = []
        for tid in ids:
            pool = self.coin_types[tid]["rarity_pool"]
            w    = sum(_RARITY_SPAWN_WEIGHT.get(r, 1) for r in pool) / len(pool)
            weights.append(w)
        return rng.choices(ids, weights=weights, k=1)[0]

    def generate(self, source: str = "cache") -> "Coin":
        """Generate one Coin. source = 'cache' | 'ruin' | 'trader'."""
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid  = hashlib.md5(f"coin_{seed}_{self._counter}".encode()).hexdigest()[:12]
        rng  = random.Random(seed)

        # Trader and ruins bias toward rarer coins
        if source == "trader":
            rng2 = random.Random(seed ^ 0xABCDEF)
            # 30% chance to force a rarer pick by running the pick twice and taking higher rarity
            type_id  = self._pick_type(rng)
            td       = self.coin_types[type_id]
            rarity   = rng2.choice(td["rarity_pool"])
            if rng2.random() < 0.3:
                alt_id  = self._pick_type(rng2)
                alt_td  = self.coin_types[alt_id]
                alt_rar = rng2.choice(alt_td["rarity_pool"])
                if RARITY_ORDER.index(alt_rar) > RARITY_ORDER.index(rarity):
                    type_id, td, rarity = alt_id, alt_td, alt_rar
        else:
            type_id = self._pick_type(rng)
            td      = self.coin_types[type_id]
            rarity  = rng.choice(td["rarity_pool"])

        cond_weights = _RARITY_CONDITION_WEIGHTS.get(rarity, _RARITY_CONDITION_WEIGHTS["common"])
        condition    = rng.choices(CONDITIONS, weights=cond_weights, k=1)[0]

        year        = rng.randint(*td["year_range"])
        ruler_name  = f"{rng.choice(_RULER_FIRST)} {rng.choice(td['title_pool'])}"
        obverse     = rng.choice(_OBVERSE)
        reverse     = rng.choice(_REVERSE)
        error_type, provenance = self._make_error_and_provenance(rng, rarity, td, ruler_name)

        return Coin(
            uid               = uid,
            coin_type_id      = type_id,
            civilization_name = td["civilization_name"],
            civ_short         = td["civ_short"],
            era_label         = td["era_label"],
            year              = year,
            currency_system   = td["currency_system"],
            denomination_key  = td["denomination_key"],
            denomination_label= td["denomination_label"],
            face_value        = td["face_value"],
            obverse_motif     = obverse,
            reverse_motif     = reverse,
            ruler_name        = ruler_name,
            mint_city         = td["mint_city"],
            condition         = condition,
            rarity            = rarity,
            seed              = seed,
            error_type        = error_type,
            provenance        = provenance,
        )

    def generate_from_type(self, type_id: str) -> "Coin":
        """Generate a coin of a specific type (for trader stock)."""
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid  = hashlib.md5(f"coin_t_{seed}_{self._counter}".encode()).hexdigest()[:12]
        rng  = random.Random(seed)

        if type_id not in self.coin_types:
            return self.generate("trader")
        td      = self.coin_types[type_id]
        rarity  = rng.choice(td["rarity_pool"])
        cond_weights = _RARITY_CONDITION_WEIGHTS.get(rarity, _RARITY_CONDITION_WEIGHTS["common"])
        condition    = rng.choices(CONDITIONS, weights=cond_weights, k=1)[0]
        year        = rng.randint(*td["year_range"])
        ruler_name  = f"{rng.choice(_RULER_FIRST)} {rng.choice(td['title_pool'])}"
        obverse     = rng.choice(_OBVERSE)
        reverse     = rng.choice(_REVERSE)
        error_type, provenance = self._make_error_and_provenance(rng, rarity, td, ruler_name)

        return Coin(
            uid=uid, coin_type_id=type_id,
            civilization_name=td["civilization_name"], civ_short=td["civ_short"],
            era_label=td["era_label"], year=year,
            currency_system=td["currency_system"],
            denomination_key=td["denomination_key"],
            denomination_label=td["denomination_label"],
            face_value=td["face_value"],
            obverse_motif=obverse, reverse_motif=reverse,
            ruler_name=ruler_name, mint_city=td["mint_city"],
            condition=condition, rarity=rarity, seed=seed,
            error_type=error_type, provenance=provenance,
        )


# ---------------------------------------------------------------------------
# Trader shop — generates a rotating daily stock of coins for sale
# ---------------------------------------------------------------------------

# Price in gold coins based on rarity × condition multiplier
_BASE_PRICE = {"common": 8, "uncommon": 22, "rare": 65, "epic": 180, "legendary": 500}
_COND_MULT  = {"poor": 0.4, "fair": 0.6, "good": 0.9, "fine": 1.2, "very_fine": 1.7, "mint": 2.8}

def coin_price(coin: Coin) -> int:
    base = _BASE_PRICE.get(coin.rarity, 10)
    mult = _COND_MULT.get(coin.condition, 1.0)
    return max(1, int(base * mult))


def generate_trader_stock(gen: CoinGenerator, day: int, town_seed: int,
                          stock_size: int = 8) -> list:
    """Return a list of Coins available from a coin trader on a given day."""
    rng = random.Random(town_seed ^ (day * 0x3A7F1B) ^ 0xC01A25)
    coins = []
    for _ in range(stock_size):
        # Bias: 60% normal generate, 40% pick a specific type the trader specialises in
        if rng.random() < 0.4 and gen.coin_types:
            tid = rng.choice(list(gen.coin_types.keys()))
            coins.append(gen.generate_from_type(tid))
        else:
            coins.append(gen.generate("trader"))
    return coins
