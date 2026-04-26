"""
towns.py — Town and Region state, day-tick growth, supply logic.
Mirrors cities.py (geometry) but holds persistent town *identity*.
"""

import json
import random
from dataclasses import dataclass, field
from typing import Optional

import heraldry
from town_needs import (
    TOWN_CATEGORIES, BASE_NEED_AMOUNT, GOLD_PER_UNIT,
    REP_PER_NEED_FILLED, ITEM_TO_CATEGORY,
    LUXURY_CATEGORIES, BASE_NEED_AMOUNT_LUXURY, REP_PER_LUXURY_FILLED,
    LUXURY_VARIANT_POOLS, PREFERRED_BONUS_MULT,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DAYS_PER_TIER   = 5      # full-need days needed to tier up
REGION_SIZE     = 3      # towns per region

TIER_NAMES = ["Hamlet", "Village", "Town", "City"]

# ---------------------------------------------------------------------------
# Name pools
# ---------------------------------------------------------------------------

_PREFIXES = [
    "Ash", "Birch", "Cedar", "Dark", "Elder", "Fern", "Glen", "Hawk",
    "Iron", "Jade", "Kale", "Larch", "Moss", "North", "Oak", "Pine",
    "Red", "Stone", "Thorn", "Vale", "Willow",
]
_SUFFIXES = [
    "brook", "bury", "cliff", "dale", "field", "ford", "gate",
    "haven", "hold", "hurst", "keep", "moor", "reach", "ridge",
    "shire", "stead", "ton", "vale", "wick",
]
_BIOME_GROUP: dict[str, str] = {
    "temperate": "forest",    "boreal": "forest",
    "birch_forest": "forest", "redwood": "forest",
    "jungle": "jungle",       "tropical": "jungle",
    "wetland": "wetland",     "swamp": "wetland",
    "desert": "desert",       "arid_steppe": "desert",  "savanna": "desert",
    "alpine_mountain": "alpine", "tundra": "alpine",    "rocky_mountain": "alpine",
    "steppe": "steppe",       "wasteland": "steppe",    "canyon": "steppe",
    "beach": "coastal",
    "mediterranean": "mediterranean",
    "east_asian":    "east_asian",
    "south_asian":   "south_asian",
}
_DEFAULT_BIOME_GROUP = "highland"

_REGION_NAMES_BY_GROUP: dict[str, list[str]] = {
    "forest":   ["Ashenveil","Greywood","Brackenmoor","Fernhollow","Birchmore",
                 "Oldwood","Oakmere","Yewdale","Timbervast","Elmhurst",
                 "Kestrelwood","Lochvale","Embervast"],
    "jungle":   ["Fernwood","Deepcanopy","Mossveil","Rootmere","Greenhollow",
                 "Tanglemark","Ivywood","Verdantshire","Deepgrove","Thornveil",
                 "Jademark","Duskhollow"],
    "wetland":  ["Mirewood","Reedholm","Bogmere","Marshgate","Foghollow",
                 "Fenwick","Mistmere","Watershire","Deepfen","Mudvast",
                 "Vantmoor","Halvenmere"],
    "desert":   ["Dunemark","Sandveil","Scorchfield","Emberreach","Ashrock",
                 "Goldsand","Ironstone","Copperveil","Drysward","Dustholm",
                 "Cinderfall","Umberveil"],
    "alpine":   ["Frostholm","Glaciergate","Snowpeak","Icevast","Coldspire",
                 "Stonecrown","Highwall","Wintermere","Icemark","Frostgate",
                 "Frostmere","Ironstead"],
    "steppe":   ["Dustmoor","Windreach","Flatstone","Plainsmere","Dryfield",
                 "Dustgate","Windholm","Greystone","Barrensward","Stonefield",
                 "Thornwall","Westbrook"],
    "coastal":  ["Saltmere","Tidehollow","Wavemark","Driftgate","Shellstone",
                 "Beachholm","Tidegate","Sandhollow","Coralveil","Foamreach",
                 "Northgate","Ardenvale"],
    "highland": ["Peakshire","Ridgemere","Hillmark","Craghollow","Moorgate",
                 "Stoneback","Highmere","Cliffdale","Ridgeholm","Brokenstone",
                 "Quarrymere","Ossenfield"],
    "mediterranean": ["Aurelia","Campania","Iberia","Baetica","Achaea","Attica",
                      "Laconia","Liguria","Etruria","Apulia","Dalmatia","Lusitania",
                      "Calabria","Bithynia","Hellas"],
    "east_asian":    ["Longshan","Jadewater","Dragoncoast","Moonshore","Bamboohill",
                      "Crimsonriver","Cloudhaven","Silkdale","Lotusmere","Ivorygate",
                      "Cedarholm","Inkwater","Cherryreach",
                      "Longmen","Qinglong","Fenghuang","Zijincheng","Baihe",
                      "Sakuraholm","Fujimere","Tsukireach","Kirihaven","Momijivale",
                      "Goldencourt","Dragontower","Jadepalace","Redgate","Craneshore"],
    "south_asian":   ["Devapura","Suryanagar","Nagarjuna","Chandramukhi","Krishnagar",
                      "Indravale","Gangashore","Vedaholm","Aryadale","Rajamere",
                      "Lotusfield","Saffrongate","Kalidevi"],
}

_TAGLINES_BY_GROUP: dict[str, list[str]] = {
    "forest":   ["Known for fine timber and expert woodcraft",
                 "Famed for hunting and forest remedies",
                 "Renowned for deep-wood mushrooms and quiet wisdom",
                 "Known for charcoal burning and ironwood tools"],
    "jungle":   ["Rich in rare herbs and exotic birds",
                 "Known for ancient pottery and river trade",
                 "Famed for deep-canopy silks and rare dyes",
                 "Renowned for jungle honey and vine bridges"],
    "wetland":  ["Known for peat and medicinal reeds",
                 "Famed for river fish and wicker craft",
                 "Renowned for fog-glass and salt extraction",
                 "Known for eel smoking and marsh iron"],
    "desert":   ["Known for spice trade and ancient sandstone ruins",
                 "Renowned for glasswork and long camel routes",
                 "Famed for precious gems and sun-dried goods",
                 "Known for date wine and nomadic law"],
    "alpine":   ["Known for stonecutting and high-altitude sheep",
                 "Famed for fine wool and harsh winters",
                 "Renowned for mountain herbs and glacier ice trade",
                 "Known for goat cheese and fortress masonry"],
    "steppe":   ["Known for horse trade and wind-dried meats",
                 "Famed for grassland grain and swift riders",
                 "Renowned for leather work and open-sky stargazing",
                 "Known for bone carving and dry-stone walls"],
    "coastal":  ["Known for salt trade and deep-sea fishing",
                 "Famed for shipbuilding and coastal amber",
                 "Renowned for pearl diving and coral crafts",
                 "Known for smoked fish and tidal herb gardens"],
    "highland": ["Known for quarried stone and highland beef",
                 "Famed for ridge-road trade and sturdy ironwork",
                 "Renowned for moorland wool and carved stone",
                 "Known for high pasture cheese and cloudberry mead"],
    "mediterranean": ["Known for olive oil, fine wine, and sun-baked marble",
                      "Famed for seafaring merchants and painted ceramics",
                      "Renowned for philosophers, poets, and open-air theatre",
                      "Known for terraced vineyards and ancient stone temples"],
    "east_asian":    ["Known for fine silk, painted lacquer, and river trade",
                      "Famed for tea ceremonies and precise brushwork",
                      "Renowned for porcelain craft and mountain monasteries",
                      "Known for cherry blossom festivals and iron casting"],
    "south_asian":   ["Known for spice roads, sacred rivers, and temple sculpture",
                      "Famed for fine cotton weaving and elaborate festivals",
                      "Renowned for elaborate stonework and aromatic cuisine",
                      "Known for monsoon rice paddies and gold craftsmanship"],
}

_CHARGES_BY_GROUP: dict[str, list[str]] = {
    "forest":   ["tree", "moon", "eagle", "wolf", "bear", "stag", "fox", "owl",
                 "raven", "arrow", "rose", "acorn", "oak_leaf", "none"],
    "jungle":   ["tree", "fleur", "eagle", "spear", "rose", "serpent",
                 "grapes", "thistle", "none"],
    "wetland":  ["anchor", "fish", "moon", "ship", "bell", "scales",
                 "swan", "frog", "none"],
    "desert":   ["sun", "sword", "star", "spear", "key", "eye",
                 "scorpion", "comet", "hourglass", "none"],
    "alpine":   ["crown", "tower", "cross", "castle", "hammer", "bear", "axe",
                 "snowflake", "mountain", "helmet", "anvil"],
    "steppe":   ["sword", "star", "eagle", "horse", "arrow", "axe",
                 "lance", "lightning", "bull", "none"],
    "coastal":  ["anchor", "fish", "cross", "castle", "ship", "key", "bell",
                 "dolphin", "waves", "trident", "cannon"],
    "highland": ["castle", "tower", "cross", "axe", "hammer", "lion", "wheat",
                 "portcullis", "gate", "buckler", "dagger", "boar", "none"],
    "mediterranean": ["sun", "olive", "ship", "amphora", "laurel", "eagle", "column",
                      "grapes", "fish", "trident", "key", "rose", "none"],
    "east_asian":    ["dragon", "crane", "lotus", "moon", "wave", "phoenix", "bamboo",
                      "mountain", "cloud", "star", "fish", "none"],
    "south_asian":   ["lotus", "sun", "elephant", "peacock", "tiger", "wheel",
                      "star", "flower", "serpent", "none"],
}

_LEADER_TITLES: dict[str, tuple[str, str]] = {
    # (masculine, feminine) — randomly assigned at display time
    "forest":   ("Lord",     "Lady"),
    "jungle":   ("Chieftain","Chieftain"),
    "wetland":  ("Elder",    "Elder"),
    "desert":   ("Sultan",   "Sultana"),
    "alpine":   ("Jarl",     "Jarl"),
    "steppe":   ("Khan",     "Khatun"),
    "coastal":  ("Admiral",  "Admiral"),
    "highland":      ("Thane",     "Thane"),
    "mediterranean": ("Consul",    "Consul"),
    "east_asian":    ("Daimyo",    "Lady"),
    "south_asian":   ("Raja",      "Rani"),
}

_TOWN_NAMES_BY_GROUP: dict[str, tuple[list[str], list[str]]] = {
    # (prefixes, suffixes)
    "forest":   (["Ash","Birch","Oak","Elm","Larch","Elder","Fern","Moss","Pine","Willow"],
                 ["brook","bury","dale","field","ford","haven","hurst","moor","stead","wick"]),
    "jungle":   (["Vine","Deep","Root","Green","Fern","Jade","Moss","Thorn","Wild","Bough"],
                 ["grove","hollow","mere","fall","den","reach","wood","canopy","shade","run"]),
    "wetland":  (["Reed","Fog","Mud","Marsh","Mist","Fen","Bog","Moss","Grey","Ash"],
                 ["fen","mere","marsh","hollow","mire","water","pool","haven","banks","drift"]),
    "desert":   (["Dust","Sand","Ember","Copper","Gold","Iron","Salt","Bone","Sun","Dry"],
                 ["rock","post","well","pass","ridge","shard","dune","hold","gate","crossing"]),
    "alpine":   (["Snow","Frost","Stone","Peak","Ice","Cold","High","Grey","Fell","Crag"],
                 ["hold","gate","wall","spire","pass","keep","ford","stead","cliff","crest"]),
    "steppe":   (["Wind","Dust","Dry","Flat","Grey","Bare","Far","Wide","Gale","Drift"],
                 ["ford","plain","field","crossing","reach","stand","drift","run","post","gap"]),
    "coastal":  (["Salt","Tide","Wave","Shell","Drift","Crest","Foam","Gull","Cove","Sand"],
                 ["port","bay","cove","haven","shore","cliff","water","gate","drift","bank"]),
    "highland":      (["Peak","Crag","Moor","Ridge","Fell","Stone","Dark","High","Bleak","Cairn"],
                      ["top","rise","dale","shire","fell","moor","crag","side","head","ford"]),
    "mediterranean": (["Val","Serra","Monte","Villa","Porto","Costa","Agri","Ponte","Bella","Alto"],
                      ["nova","alta","bella","doro","mira","faro","vento","sole","mare","petra"]),
    "east_asian":    (["Long","Jade","Dragon","Crane","Lotus","Bamboo","Golden","Moon","River","Cloud",
                       "Huang","Qing","Hong","Zi","Jin","Bai","Sakura","Fuji","Tsuki","Kiri","Haru"],
                      ["zhou","jing","shan","hai","ming","dao","feng","yuan","shima","hama",
                       "men","guan","hu","jo","machi","zaki","mura","bao","gang","pu"]),
    "south_asian":   (["Deva","Naga","Surya","Chandra","Indra","Ganga","Arya","Raja","Kali","Veda"],
                      ["pura","ghat","nagar","tala","vati","shri","pur","mala","abad","devi"]),
}

# Biome-specific need multipliers: (food, wood, stone, metal)
# Values > 1.0 mean higher demand; values < 1.0 mean lower demand
_NEED_WEIGHTS: dict[str, dict[str, float]] = {
    "forest":   {"food": 1.0, "wood": 0.6, "stone": 1.0, "metal": 1.2},
    "jungle":   {"food": 0.7, "wood": 0.7, "stone": 1.2, "metal": 1.0},
    "wetland":  {"food": 0.8, "wood": 1.0, "stone": 1.3, "metal": 1.0},
    "desert":   {"food": 1.5, "wood": 1.4, "stone": 0.7, "metal": 0.8},
    "alpine":   {"food": 1.2, "wood": 1.5, "stone": 0.7, "metal": 0.8},
    "steppe":   {"food": 0.9, "wood": 1.3, "stone": 1.1, "metal": 1.0},
    "coastal":  {"food": 0.8, "wood": 0.9, "stone": 1.2, "metal": 1.1},
    "highland":      {"food": 1.1, "wood": 1.1, "stone": 0.8, "metal": 0.9},
    "mediterranean": {"food": 0.9, "wood": 1.1, "stone": 0.7, "metal": 1.1},
    "east_asian":    {"food": 0.8, "wood": 0.9, "stone": 1.1, "metal": 1.2},
    "south_asian":   {"food": 0.7, "wood": 1.0, "stone": 0.8, "metal": 1.3},
}

# Luxury goods each biome group craves.
# Primary luxury is wanted by all tiers; secondary is unlocked at tier >= 1.
_LUXURY_SPECIALTY: dict[str, list[str]] = {
    "forest":   ["wine",    "herbs"],
    "jungle":   ["coffee",  "pottery"],
    "wetland":  ["tea",     "herbs"],
    "desert":   ["coffee",  "spirits"],
    "alpine":   ["spirits", "tea"],
    "steppe":   ["spirits", "herbs"],
    "coastal":  ["wine",    "tea"],
    "highland":      ["wine",    "pottery"],
    "mediterranean": ["wine",    "pottery"],
    "east_asian":    ["tea",     "pottery"],
    "south_asian":   ["tea",     "herbs"],
}

_LEADER_GREETINGS: dict[str, list[str]] = {
    "forest":   ["The woods have many paths. Few lead here.",
                 "This kingdom grew from the trees. We honour that still.",
                 "Speak plainly. The forest rewards those who do."],
    "jungle":   ["The canopy watches all who enter. State your purpose.",
                 "Few outsiders find their way this deep. You must have need.",
                 "The jungle gives and takes in equal measure. Remember that."],
    "wetland":  ["The marsh speaks to those who listen. What do you seek?",
                 "These fens have kept us hidden and kept us safe. Until now.",
                 "Outsiders rarely visit without a reason. What is yours?"],
    "desert":   ["The sands are unforgiving, stranger. Trade sustains us.",
                 "Water and shade are worth more here than gold. Almost.",
                 "You have crossed far to reach us. The desert respects that."],
    "alpine":   ["The mountain passes bring few visitors. State your purpose.",
                 "We do not waste words up here. The cold teaches that.",
                 "You've climbed high. The view is your reward. Now speak."],
    "steppe":   ["You've ridden far. The plains teach patience.",
                 "Out here, trust is earned slowly. Talk is cheap.",
                 "The wind carries voices for miles on the steppe. Be careful."],
    "coastal":  ["Ha! A landlubber. Welcome to our harbour.",
                 "Every ship brings news. What do yours carry?",
                 "The tides wait for no one. Neither do we."],
    "highland":      ["You've climbed high to reach us. What do you want?",
                      "The moors have few secrets from those who live on them.",
                      "Blunt talk, sharp steel — that's the highland way."],
    "mediterranean": ["The sun shines on traders and philosophers alike. Which are you?",
                      "This city has stood a thousand years. A few more questions won't hurt it.",
                      "We debate everything here. But trade? That we decide quickly."],
    "east_asian":    ["You arrive as the cherry blossoms fall. Auspicious, perhaps.",
                      "Patience and precision — we value both. Show us you have them.",
                      "The river carries many things downstream. What does it carry today?",
                      "The dragon sleeps in the mountain. Do not wake it without purpose.",
                      "The brush moves, the record stands. We are watching.",
                      "Honour flows downward from the throne. Remember that."],
    "south_asian":   ["The gods watch all who pass through these gates. State your purpose.",
                      "Every road leads here eventually. The spice route does not lie.",
                      "Honour the traditions of this place and you will be welcome."],
}

_HERALDIC_COLORS = [
    (180,  40,  40), (40,  80, 180), (50, 140,  50),
    (160, 140,  30), (130,  50, 160), (30, 130, 140),
    (180,  90,  30), (60,  60,  60),
]

_LEADER_FIRST = [
    "Aldric", "Beatrix", "Calder", "Dorith", "Elowen", "Fenn",
    "Garet", "Hilda", "Islin", "Jorin", "Kessa", "Lorn",
    "Maren", "Nils", "Orla", "Pell", "Quen", "Reva",
    "Savan", "Tova", "Ulrik", "Vanna", "Wren",
]
_LEADER_LAST = [
    "Ashveil", "Bram", "Coldwater", "Dusk", "Embershard",
    "Frost", "Gale", "Hollow", "Ironmoor", "Jarn",
    "Knell", "Loch", "Marsh", "Nettlefield", "Orn",
    "Pike", "Quill", "Reed", "Stonehaven", "Thorn",
]


def _make_town_name(rng: random.Random, biome_group: str = _DEFAULT_BIOME_GROUP) -> str:
    if biome_group in _TOWN_NAMES_BY_GROUP:
        prefixes, suffixes = _TOWN_NAMES_BY_GROUP[biome_group]
    else:
        prefixes, suffixes = _PREFIXES, _SUFFIXES
    return rng.choice(prefixes) + rng.choice(suffixes)


def _biome_group_for(biodome: str) -> str:
    return _BIOME_GROUP.get(biodome, _DEFAULT_BIOME_GROUP)


def _make_region_name(rng: random.Random, used: set,
                      biome_group: str = _DEFAULT_BIOME_GROUP) -> str:
    source = _REGION_NAMES_BY_GROUP.get(biome_group,
                                        _REGION_NAMES_BY_GROUP[_DEFAULT_BIOME_GROUP])
    pool = [n for n in source if n not in used]
    if not pool:
        pool = source
    return rng.choice(pool)


def _make_tagline(rng: random.Random, biome_group: str) -> str:
    pool = _TAGLINES_BY_GROUP.get(biome_group, _TAGLINES_BY_GROUP[_DEFAULT_BIOME_GROUP])
    return rng.choice(pool)


def _make_leader_name(rng: random.Random) -> str:
    return f"{rng.choice(_LEADER_FIRST)} {rng.choice(_LEADER_LAST)}"


def leader_title_for(biome_group: str, rng: random.Random) -> str:
    """Return a biome-appropriate title (masc/fem chosen from rng)."""
    masc, fem = _LEADER_TITLES.get(biome_group, ("Lord", "Lady"))
    return rng.choice([masc, fem])


def leader_greeting_for(biome_group: str) -> str:
    """Return a random greeting line for a leader in this biome group."""
    import random as _random
    pool = _LEADER_GREETINGS.get(biome_group, _LEADER_GREETINGS["highland"])
    return _random.choice(pool)

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Town:
    town_id:          int
    region_id:        int
    is_capital:       bool
    center_bx:        int
    half_w:           int
    biome:            str
    name:             str
    leader_name:      Optional[str]
    tier:             int
    reputation:       int
    needs:            dict   # {"food": {"required": 200, "supplied": 50}, ...}
    growth_progress:  float  # 0..1; resets on tier up
    grown_buildings:  list   # [(offset, variant, width, height), ...]
    founded_day:      int
    size:             str    # "small"/"medium"/"large"

    def tier_name(self) -> str:
        return TIER_NAMES[min(self.tier, len(TIER_NAMES) - 1)]

    def all_needs_met(self) -> bool:
        return all(
            nd["supplied"] >= nd["required"]
            for nd in self.needs.values()
        )


@dataclass
class Region:
    region_id:       int
    name:            str
    capital_town_id: int
    member_town_ids: list
    leader_color:    tuple
    coat_of_arms:    Optional[heraldry.CoatOfArms] = None
    biome_group:     str = _DEFAULT_BIOME_GROUP
    tagline:         str = ""
    leader_title:    str = "Lord"
    # reputation is computed on read: sum of member town reps


# ---------------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------------

TOWNS:   dict[int, Town]   = {}
REGIONS: dict[int, Region] = {}

# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------

def _scan_bg_for_flags(world) -> list:
    """Scan in-memory bg chunks for TOWN_FLAG_BLOCK; return sorted list of bx values."""
    from blocks import TOWN_FLAG_BLOCK as _TFB
    from constants import CHUNK_W as _CW
    bxs = []
    for cx, chunk in world._bg_chunks.items():
        for by in range(len(chunk)):
            for lx in range(len(chunk[by])):
                if chunk[by][lx] == _TFB:
                    bxs.append(cx * _CW + lx)
    return sorted(bxs)


def init_towns(world) -> None:
    """Populate TOWNS and REGIONS from world.town_centers (set by generate_cities)."""
    TOWNS.clear()
    REGIONS.clear()

    # Try to load persisted data first
    if hasattr(world, '_save_mgr') and world._save_mgr is not None:
        rows = _load_from_db(world._save_mgr)
        if rows is not None:
            _fill_missing_coat_of_arms(world.seed)
            _restore_world_city_metadata(world)
            _respawn_leader_npcs(world)
            return

    centers = world.town_centers
    if not centers:
        # Old save: bg chunks are already loaded by _load_from; scan them for flags.
        centers = _scan_bg_for_flags(world)
        if not centers:
            return

    rng = random.Random(world.seed + 99999)
    used_names: set[str] = set()
    used_regions: set[str] = set()

    from cities import CITY_CONFIGS, _city_slot_metadata, CITY_SPACING
    city_sizes = getattr(world, 'city_sizes', [])
    slot_xs    = getattr(world, 'city_slot_xs', [])

    for town_id, center_bx in enumerate(centers):
        # Resolve slot_x: use stored value, or approximate from center_bx
        if town_id < len(slot_xs):
            slot_x = slot_xs[town_id]
        else:
            half   = CITY_SPACING // 2
            slot_x = round((center_bx - half) / CITY_SPACING) * CITY_SPACING + half

        meta   = _city_slot_metadata(slot_x)
        biome  = world.biodome_at(center_bx)
        name   = _make_town_name(rng, _biome_group_for(biome))
        used_names.add(name)

        size   = city_sizes[town_id] if town_id < len(city_sizes) else "medium"
        half_w = CITY_CONFIGS[size]["half_w"]

        TOWNS[town_id] = Town(
            town_id       = town_id,
            region_id     = meta["region_id"],
            is_capital    = meta["is_capital"],
            center_bx     = center_bx,
            half_w        = half_w,
            biome         = biome,
            name          = name,
            leader_name   = None,
            tier          = _starting_tier(size, meta["is_capital"]),
            reputation    = 0,
            needs         = {},
            growth_progress = 0.0,
            grown_buildings = [],
            founded_day   = 0,
            size          = size,
        )
        _assign_initial_needs(TOWNS[town_id])

    # Build regions — one deterministic RNG per region keyed by region_id
    region_ids = set(t.region_id for t in TOWNS.values())
    for rid in sorted(region_ids):
        members  = [t for t in TOWNS.values() if t.region_id == rid]
        capitals = [t for t in members if t.is_capital]
        capital  = capitals[0] if capitals else members[0]

        bg     = _biome_group_for(world.biodome_at(capital.center_bx))

        rng_r   = random.Random(world.seed + rid * 31337 + 88888)
        rname   = _make_region_name(rng_r, used_regions, bg)
        used_regions.add(rname)
        lcolor  = rng_r.choice(_HERALDIC_COLORS)
        lname   = _make_leader_name(rng_r)
        tagline = _make_tagline(rng_r, bg)
        title   = leader_title_for(bg, rng_r)
        capital.leader_name = lname

        coa = heraldry.generate(random.Random(), lcolor,
                                charge_pool=_CHARGES_BY_GROUP.get(bg))

        REGIONS[rid] = Region(
            region_id       = rid,
            name            = rname,
            capital_town_id = capital.town_id,
            member_town_ids = [t.town_id for t in members],
            leader_color    = lcolor,
            coat_of_arms    = coa,
            biome_group     = bg,
            tagline         = tagline,
            leader_title    = title,
        )

    # Place castles + LeaderNPCs for each capital
    for town in TOWNS.values():
        if town.is_capital:
            _place_capital_structures(town, world)


def register_new_town(world, city_bx: int, city_size: str,
                      region_id: int = 0, is_capital: bool = False) -> None:
    """Register a dynamically-generated (chunk-streamed) city as a full Town."""
    from cities import CITY_CONFIGS
    town_id = max(TOWNS.keys()) + 1 if TOWNS else 0
    half_w  = CITY_CONFIGS[city_size]["half_w"]
    biome   = world.biodome_at(city_bx)
    rng     = random.Random(world.seed + city_bx * 7919)
    name    = _make_town_name(rng, _biome_group_for(biome))

    TOWNS[town_id] = Town(
        town_id         = town_id,
        region_id       = region_id,
        is_capital      = is_capital,
        center_bx       = city_bx,
        half_w          = half_w,
        biome           = biome,
        name            = name,
        leader_name     = None,
        tier            = _starting_tier(city_size, is_capital),
        reputation      = 0,
        needs           = {},
        growth_progress = 0.0,
        grown_buildings = [],
        founded_day     = 0,
        size            = city_size,
    )
    _assign_initial_needs(TOWNS[town_id])

    # Lazily create the Region if it doesn't exist yet
    if region_id not in REGIONS:
        bg      = _biome_group_for(world.biodome_at(city_bx))
        rng_r   = random.Random(world.seed + region_id * 31337 + 88888)
        used    = {r.name for r in REGIONS.values()}
        rname   = _make_region_name(rng_r, used, bg)
        lcolor  = rng_r.choice(_HERALDIC_COLORS)
        lname   = _make_leader_name(rng_r)
        tagline = _make_tagline(rng_r, bg)
        title   = leader_title_for(bg, rng_r)
        coa     = heraldry.generate(random.Random(), lcolor,
                                    charge_pool=_CHARGES_BY_GROUP.get(bg))
        REGIONS[region_id] = Region(
            region_id       = region_id,
            name            = rname,
            capital_town_id = town_id if is_capital else -1,
            member_town_ids = [],
            leader_color    = lcolor,
            coat_of_arms    = coa,
            biome_group     = bg,
            tagline         = tagline,
            leader_title    = title,
        )
        if is_capital:
            TOWNS[town_id].leader_name = lname
    else:
        if is_capital:
            # Claim the capital slot if no capital has arrived yet
            region = REGIONS[region_id]
            if region.capital_town_id == -1:
                rng_r = random.Random(world.seed + region_id * 31337 + 88888)
                _make_region_name(rng_r, set())   # advance rng past name
                rng_r.choice(_HERALDIC_COLORS)    # advance past color
                lname = _make_leader_name(rng_r)
                TOWNS[town_id].leader_name = lname
                region.capital_town_id = town_id
                # Update biome_group to the capital's biome — the region may have been
                # created by a non-capital city that arrived first with a different biome.
                region.biome_group = _biome_group_for(biome)

    REGIONS[region_id].member_town_ids.append(town_id)

    if is_capital:
        _place_capital_structures(TOWNS[town_id], world)


def _restore_world_city_metadata(world) -> None:
    """Populate world.town_centers/city_zones/etc. from loaded TOWNS after a DB load."""
    from cities import CITY_CONFIGS, CITY_SPACING
    half_spacing = CITY_SPACING // 2
    world.town_centers = []
    world.city_sizes   = []
    world.city_slot_xs = []
    world.city_zones   = []
    for town in sorted(TOWNS.values(), key=lambda t: t.town_id):
        bx     = town.center_bx
        size   = town.size
        half_w = CITY_CONFIGS.get(size, CITY_CONFIGS["medium"])["half_w"]
        slot_x = round((bx - half_spacing) / CITY_SPACING) * CITY_SPACING + half_spacing
        world.town_centers.append(bx)
        world.city_sizes.append(size)
        world.city_slot_xs.append(slot_x)
        world.city_zones.append((bx - half_w, bx + half_w))


def _palace_type_for(palace_left: int, world_seed: int) -> str:
    """Deterministic palace type for a capital at palace_left.  Same inputs → same type."""
    from cities import PALACE_TYPES
    return random.Random(palace_left ^ world_seed ^ 0xCAFEBABE).choice(PALACE_TYPES)


def _respawn_leader_npcs(world) -> None:
    """Re-create LeaderNPC entities for capital towns after loading from DB.
    Blocks are already in loaded chunks; only the entity needs to be spawned."""
    from cities import PALACE_NPC_OFFSET, LeaderNPC
    from constants import BLOCK_SIZE

    for town in TOWNS.values():
        if not town.is_capital:
            continue
        region = REGIONS.get(town.region_id)
        if region is None:
            continue
        palace_left = town.center_bx + town.half_w + 4
        sy = world.surface_y_at(palace_left)
        ptype = _palace_type_for(palace_left, world.seed)
        npc_offset = PALACE_NPC_OFFSET[ptype]
        npc_px = (palace_left + npc_offset) * BLOCK_SIZE
        npc_py = (sy - 3) * BLOCK_SIZE
        world.entities.append(
            LeaderNPC(npc_px, npc_py, world,
                      region_id   = region.region_id,
                      region_name = region.name,
                      leader_name = town.leader_name or "Leader",
                      leader_color= region.leader_color,
                      palace_type = ptype)
        )


def _place_capital_structures(town: Town, world) -> None:
    """Place a randomly-selected palace + LeaderNPC for a capital town."""
    from cities import (
        _place_castle, _populate_castle, _place_castle_garden,
        _place_mediterranean_palace,
        _place_east_asian_palace,
        _place_south_asian_palace,
        _place_italian_palazzo,
        _place_moorish_palace,
        _place_middle_eastern_palace,
        _place_norse_hall,
        _place_gothic_palace,
        _place_african_palace,
        _place_byzantine_palace,
        _place_tibetan_palace,
        _place_japanese_palace,
        _place_chinese_palace,
        PALACE_NPC_OFFSET,
        LeaderNPC,
    )
    from constants import BLOCK_SIZE

    region = REGIONS.get(town.region_id)
    palace_left = town.center_bx + town.half_w + 4
    sy = world.surface_y_at(palace_left)

    ptype = _palace_type_for(palace_left, world.seed)

    if ptype == "mediterranean":
        _place_mediterranean_palace(world, palace_left, sy)
    elif ptype == "east_asian":
        _place_east_asian_palace(world, palace_left, sy)
    elif ptype == "south_asian":
        _place_south_asian_palace(world, palace_left, sy)
    elif ptype == "italian":
        _place_italian_palazzo(world, palace_left, sy)
    elif ptype == "moorish":
        _place_moorish_palace(world, palace_left, sy)
    elif ptype == "middle_eastern":
        _place_middle_eastern_palace(world, palace_left, sy)
    elif ptype == "norse":
        _place_norse_hall(world, palace_left, sy)
    elif ptype == "gothic":
        _place_gothic_palace(world, palace_left, sy)
    elif ptype == "african":
        _place_african_palace(world, palace_left, sy)
    elif ptype == "byzantine":
        _place_byzantine_palace(world, palace_left, sy)
    elif ptype == "tibetan":
        _place_tibetan_palace(world, palace_left, sy)
    elif ptype == "japanese":
        _place_japanese_palace(world, palace_left, sy)
    elif ptype == "chinese":
        _place_chinese_palace(world, palace_left, sy)
    else:
        castle_w = _place_castle(world, palace_left, sy)
        castle_rng = random.Random(palace_left ^ (world.seed * 0x9E3779B9) ^ 0xBEEF1)
        _populate_castle(world, palace_left, sy, castle_rng)
        _place_castle_garden(world, palace_left + castle_w + 1, sy, castle_rng, town.biome)

    npc_offset = PALACE_NPC_OFFSET[ptype]

    if region is None:
        return
    npc_px = (palace_left + npc_offset) * BLOCK_SIZE
    npc_py = (sy - 3) * BLOCK_SIZE
    world.entities.append(
        LeaderNPC(npc_px, npc_py, world,
                  region_id   = region.region_id,
                  region_name = region.name,
                  leader_name = town.leader_name or "Leader",
                  leader_color= region.leader_color,
                  palace_type = ptype)
    )


def _coa_rng(world_seed: int, region_id: int, leader_color: tuple) -> random.Random:
    """Deterministic rng used only for back-filling missing COAs on old saves."""
    seed = (world_seed ^ (region_id * 0x9E3779B9) ^ hash(leader_color)) & 0x7FFFFFFF
    return random.Random(seed)


def _fill_missing_coat_of_arms(world_seed: int) -> None:
    """Regenerate coat_of_arms for any region that was loaded without one (old saves)."""
    for region in REGIONS.values():
        if region.coat_of_arms is None:
            region.coat_of_arms = heraldry.generate(
                _coa_rng(world_seed, region.region_id, region.leader_color),
                region.leader_color,
            )


def _starting_tier(size: str, is_capital: bool) -> int:
    base = {"small": 0, "medium": 1, "large": 2}.get(size, 0)
    return min(base + (1 if is_capital else 0), len(TIER_NAMES) - 1)


def _assign_initial_needs(town: Town) -> None:
    tier    = town.tier
    bg      = _biome_group_for(town.biome)
    weights = _NEED_WEIGHTS.get(bg, {})
    town.needs = {
        cat: {
            "required": max(1, round(BASE_NEED_AMOUNT[cat]
                                     * weights.get(cat, 1.0)
                                     * (tier + 1))),
            "supplied": 0,
        }
        for cat in TOWN_CATEGORIES
    }
    # Luxury specialty: primary always wanted; secondary unlocked at tier >= 1
    lux_rng  = random.Random(town.town_id * 1_234_567 + 42)
    luxuries = _LUXURY_SPECIALTY.get(bg, [])
    for i, lux in enumerate(luxuries):
        if i == 0 or tier >= 1 or town.is_capital:
            pool      = LUXURY_VARIANT_POOLS.get(lux, {})
            variants  = pool.get(bg) or pool.get("_default", [])
            preferred = lux_rng.choice(variants) if variants else None
            town.needs[lux] = {
                "required":  max(1, round(BASE_NEED_AMOUNT_LUXURY[lux] * (tier + 1))),
                "supplied":  0,
                "preferred": preferred,
            }

# ---------------------------------------------------------------------------
# Supply
# ---------------------------------------------------------------------------

def supply_need(town: Town, player, category: str, amount: int) -> tuple[int, int]:
    """
    Deliver `amount` units of `category` from player to town.
    Returns (gold_earned, rep_earned).
    """
    if category not in town.needs:
        return 0, 0
    nd = town.needs[category]
    space = max(0, nd["required"] - nd["supplied"])
    can_supply = min(amount, space, player.count_items_in_category(category))
    if can_supply <= 0:
        return 0, 0

    # Count preferred-type items available before removal for gold bonus
    preferred = nd.get("preferred")
    pref_count = 0
    if preferred:
        pref_count = min(can_supply, sum(
            cnt for iid, cnt in player.inventory.items()
            if iid == preferred or iid.startswith(preferred + "_")
        ))

    removed = player.remove_items_in_category(category, can_supply)
    nd["supplied"] += removed

    base_rate = GOLD_PER_UNIT[category]
    gold = (round(pref_count * base_rate * PREFERRED_BONUS_MULT)
            + (removed - pref_count) * base_rate)
    player.money += gold

    rep = 0
    if nd["supplied"] >= nd["required"]:
        rep = REP_PER_LUXURY_FILLED if category in LUXURY_CATEGORIES else REP_PER_NEED_FILLED
        town.reputation += rep

    return gold, rep

# ---------------------------------------------------------------------------
# Day tick
# ---------------------------------------------------------------------------

def advance_day(world) -> None:
    """Called once per in-game day. Updates growth progress and triggers tier-ups."""
    for town in TOWNS.values():
        if not town.needs:
            continue
        if town.all_needs_met():
            town.growth_progress += 1.0 / DAYS_PER_TIER
            if town.growth_progress >= 1.0:
                _tier_up(town, world)

    # Reset daily supply tracking (needs carry over; only supplied resets each tier-up)
    # Daily decay: partially supplied needs decay 10% of required each day they aren't met
    for town in TOWNS.values():
        for nd in town.needs.values():
            if nd["supplied"] < nd["required"]:
                decay = max(1, nd["required"] // 10)
                nd["supplied"] = max(0, nd["supplied"] - decay)


def _tier_up(town: Town, world) -> None:
    town.tier = min(town.tier + 1, 3)
    town.growth_progress = 0.0
    _assign_initial_needs(town)
    _grow_town_buildings(town, world)
    # Broadcast toast via world attribute (main.py reads it)
    if not hasattr(world, '_town_toasts'):
        world._town_toasts = []
    world._town_toasts.append(f"{town.name} grew to {town.tier_name()}!")

    # Re-evaluate capital for the region (it's locked at init, so just update leader)
    region = REGIONS.get(town.region_id)
    if region and town.is_capital:
        pass  # already capital

# ---------------------------------------------------------------------------
# Growth building placement
# ---------------------------------------------------------------------------

def _grow_town_buildings(town: Town, world) -> None:
    """Attempt to place the next growth slot building for the town."""
    from cities import CITY_CONFIGS, _place_house, _place_house_two_story, _place_tower, BUILDING_PALETTES
    import random as _r

    cfg = CITY_CONFIGS.get(town.size, CITY_CONFIGS["medium"])
    slots_key = f"growth_slots_tier{town.tier}"
    slots = cfg.get(slots_key, [])
    if not slots:
        return

    # Find the next unused slot
    used_offsets = {b[0] for b in town.grown_buildings}
    rng = _r.Random(world.seed + town.town_id * 31337 + town.tier * 997)

    from blocks import STONE as _STONE, AIR as _AIR
    # Growth buildings sit on the same floor as the city.
    city_sy = world.surface_y_at(town.center_bx)

    for offset, w_range, h_range, variants in slots:
        if offset in used_offsets:
            continue
        left_x = town.center_bx + offset
        sy     = city_sy
        width  = rng.randint(*w_range)
        height = rng.randint(*h_range)
        variant = rng.choice(variants)

        # Safety check — don't overwrite player-placed blocks
        if _slot_is_blocked(world, left_x, sy, width, height):
            continue

        # Flatten 3 blocks outside each outer wall so players approaching from
        # outside the city don't hit solid wall above the door opening.
        for ext_x in list(range(left_x - 3, left_x)) + list(range(left_x + width, left_x + width + 3)):
            if not (0 <= ext_x < world.width):
                continue
            if 0 <= sy < world.height:
                world.set_block(ext_x, sy, _STONE)
            for wy in range(sy - 6, sy):
                if 0 <= wy < world.height and world.get_block(ext_x, wy) != _AIR:
                    world.set_block(ext_x, wy, _AIR)

        wall_block, roof_block = rng.choice(BUILDING_PALETTES)
        if variant == "two_story":
            floor2_h = rng.randint(2, 3)
            _place_house_two_story(world, left_x, sy, width, height, floor2_h,
                                   wall_block, roof_block)
        elif variant == "tower":
            _place_tower(world, left_x, sy, width, height, wall_block, roof_block)
        else:
            _place_house(world, left_x, sy, width, height, wall_block, roof_block)

        town.grown_buildings.append((offset, variant, width, height))
        return  # one building per tier-up


def _slot_is_blocked(world, left_x: int, sy: int, width: int, height: int) -> bool:
    """Return True if the slot contains player-placed non-natural blocks."""
    from blocks import AIR, STONE, GRASS, DIRT, BEDROCK
    natural = {AIR, STONE, GRASS, DIRT, BEDROCK}
    for bx in range(left_x, left_x + width + 1):
        for by in range(sy - height - 1, sy):
            bid = world.get_block(bx, by)
            if bid not in natural:
                return True
    return False

# ---------------------------------------------------------------------------
# Lookup
# ---------------------------------------------------------------------------

def get_town_for_block(world, bx: int, by: int) -> Optional[Town]:
    """Return the Town whose footprint contains (bx, by), or None."""
    for town in TOWNS.values():
        if town.center_bx - town.half_w - 2 <= bx <= town.center_bx + town.half_w + 2:
            return town
    return None

# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def serialize_all() -> tuple[list[dict], list[dict]]:
    town_rows = []
    for t in TOWNS.values():
        town_rows.append({
            "town_id":         t.town_id,
            "region_id":       t.region_id,
            "is_capital":      int(t.is_capital),
            "center_bx":       t.center_bx,
            "half_w":          t.half_w,
            "biome":           t.biome,
            "name":            t.name,
            "leader_name":     t.leader_name or "",
            "tier":            t.tier,
            "reputation":      t.reputation,
            "growth_progress": t.growth_progress,
            "founded_day":     t.founded_day,
            "size":            t.size,
            "needs_json":      json.dumps(t.needs),
            "grown_buildings_json": json.dumps(t.grown_buildings),
        })
    region_rows = []
    for r in REGIONS.values():
        coa = r.coat_of_arms
        coa_json = json.dumps({
            "primary":   list(coa.primary),
            "secondary": list(coa.secondary),
            "metal":     list(coa.metal),
            "division":  coa.division,
            "ordinary":  coa.ordinary,
            "charge":    coa.charge,
            "motto":     coa.motto,
        }) if coa else "null"
        region_rows.append({
            "region_id":            r.region_id,
            "name":                 r.name,
            "capital_town_id":      r.capital_town_id,
            "member_town_ids_json": json.dumps(r.member_town_ids),
            "leader_color_json":    json.dumps(list(r.leader_color)),
            "coat_of_arms_json":    coa_json,
            "biome_group":          r.biome_group,
            "tagline":              r.tagline,
            "leader_title":         r.leader_title,
        })
    return town_rows, region_rows


def deserialize_all(town_rows: list[dict], region_rows: list[dict]) -> None:
    TOWNS.clear()
    REGIONS.clear()
    for row in town_rows:
        t = Town(
            town_id         = row["town_id"],
            region_id       = row["region_id"],
            is_capital      = bool(row["is_capital"]),
            center_bx       = row["center_bx"],
            half_w          = row["half_w"],
            biome           = row["biome"],
            name            = row["name"],
            leader_name     = row["leader_name"] or None,
            tier            = row["tier"],
            reputation      = row["reputation"],
            needs           = json.loads(row["needs_json"]),
            growth_progress = row["growth_progress"],
            grown_buildings = json.loads(row["grown_buildings_json"]),
            founded_day     = row["founded_day"],
            size            = row.get("size", "medium"),
        )
        TOWNS[t.town_id] = t
    for row in region_rows:
        lcolor = tuple(json.loads(row["leader_color_json"]))
        coa = None
        raw_coa = row.get("coat_of_arms_json")
        if raw_coa and raw_coa != "null":
            try:
                d = json.loads(raw_coa)
                coa = heraldry.CoatOfArms(
                    primary   = tuple(d["primary"]),
                    secondary = tuple(d["secondary"]),
                    metal     = tuple(d["metal"]),
                    division  = d["division"],
                    ordinary  = d["ordinary"],
                    charge    = d["charge"],
                    motto     = d["motto"],
                )
            except Exception:
                coa = None
        r = Region(
            region_id       = row["region_id"],
            name            = row["name"],
            capital_town_id = row["capital_town_id"],
            member_town_ids = json.loads(row["member_town_ids_json"]),
            leader_color    = lcolor,
            coat_of_arms    = coa,
            biome_group     = row.get("biome_group") or _DEFAULT_BIOME_GROUP,
            tagline         = row.get("tagline") or "",
            leader_title    = row.get("leader_title") or "Lord",
        )
        REGIONS[r.region_id] = r


def _load_from_db(save_mgr) -> Optional[bool]:
    """Try to load town/region data from DB. Returns True if data found, None if not."""
    try:
        import sqlite3
        with sqlite3.connect(save_mgr.db_path) as con:
            con.row_factory = sqlite3.Row
            towns_exist = con.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='towns'"
            ).fetchone()
            if not towns_exist:
                return None
            town_rows   = [dict(r) for r in con.execute("SELECT * FROM towns").fetchall()]
            region_rows = [dict(r) for r in con.execute("SELECT * FROM regions").fetchall()]
            if not town_rows:
                return None
            deserialize_all(town_rows, region_rows)
            return True
    except Exception:
        return None
