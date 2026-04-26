import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class Beer:
    uid: str
    origin_biome: str       # biodome where hops were harvested ("blend" for blended)
    grain_type: str         # grain character of the biome
    beer_type: str          # "ale" | "lager" | "stout" | "ipa" | "wheat_beer" | "saison"
    state: str              # "raw" | "brewed" | "fermented" | "conditioned" | "blended"
    bitterness: float       # 0.0–1.0 (hop character)
    maltiness: float        # 0.0–1.0 (grain sweetness)
    clarity: float          # 0.0–1.0 (1 = crystal clear, 0 = very hazy)
    body: float             # 0.0–1.0 (light to full)
    carbonation: float      # 0.0–1.0
    aroma: float            # 0.0–1.0
    ferment_quality: float  # 0.0–1.0, set by fermentation mini-game
    condition_quality: float  # 0.0–1.0, set by taproom
    flavor_notes: list
    seed: int
    blend_components: list = field(default_factory=list)
    mash_type: str = ""       # "pale_malt" | "crystal_malt" | "roasted_malt" | "wheat_malt"
    hop_addition: str = ""    # "early" | "late" | "dry"
    yeast_type: str = ""      # "ale_yeast" | "lager_yeast" | "wild_yeast" | "wheat_yeast"
    vessel: str = ""          # "cask" | "bottle" | "keg"
    condition_duration: str = ""  # "quick" | "standard" | "extended"


# Base profiles per biome — determines beer type and starting attributes
BIOME_BEER_PROFILES = {
    "tropical":        {"grain_type": "adjunct",      "beer_type": "wheat_beer", "bitterness": 0.20, "maltiness": 0.45, "clarity": 0.40, "body": 0.35, "carbonation": 0.65, "aroma": 0.75},
    "jungle":          {"grain_type": "spiced_grain",  "beer_type": "saison",    "bitterness": 0.35, "maltiness": 0.50, "clarity": 0.50, "body": 0.55, "carbonation": 0.60, "aroma": 0.80},
    "savanna":         {"grain_type": "pale_malt",     "beer_type": "lager",     "bitterness": 0.25, "maltiness": 0.40, "clarity": 0.85, "body": 0.30, "carbonation": 0.70, "aroma": 0.35},
    "wetland":         {"grain_type": "dark_malt",     "beer_type": "stout",     "bitterness": 0.55, "maltiness": 0.75, "clarity": 0.20, "body": 0.80, "carbonation": 0.35, "aroma": 0.55},
    "arid_steppe":     {"grain_type": "pale_malt",     "beer_type": "lager",     "bitterness": 0.20, "maltiness": 0.35, "clarity": 0.90, "body": 0.25, "carbonation": 0.75, "aroma": 0.30},
    "canyon":          {"grain_type": "crystal_malt",  "beer_type": "ale",       "bitterness": 0.40, "maltiness": 0.65, "clarity": 0.60, "body": 0.60, "carbonation": 0.50, "aroma": 0.50},
    "beach":           {"grain_type": "wheat_malt",    "beer_type": "wheat_beer","bitterness": 0.15, "maltiness": 0.40, "clarity": 0.30, "body": 0.30, "carbonation": 0.70, "aroma": 0.65},
    "tundra":          {"grain_type": "roasted_malt",  "beer_type": "stout",     "bitterness": 0.60, "maltiness": 0.80, "clarity": 0.15, "body": 0.85, "carbonation": 0.30, "aroma": 0.50},
    "swamp":           {"grain_type": "wild_grain",    "beer_type": "saison",    "bitterness": 0.30, "maltiness": 0.45, "clarity": 0.40, "body": 0.50, "carbonation": 0.65, "aroma": 0.85},
    "alpine_mountain": {"grain_type": "pale_malt",     "beer_type": "lager",     "bitterness": 0.30, "maltiness": 0.45, "clarity": 0.80, "body": 0.35, "carbonation": 0.65, "aroma": 0.40},
    "rocky_mountain":  {"grain_type": "hop_heavy",     "beer_type": "ipa",       "bitterness": 0.85, "maltiness": 0.40, "clarity": 0.65, "body": 0.50, "carbonation": 0.55, "aroma": 0.80},
    "rolling_hills":   {"grain_type": "crystal_malt",  "beer_type": "ale",       "bitterness": 0.45, "maltiness": 0.70, "clarity": 0.65, "body": 0.65, "carbonation": 0.50, "aroma": 0.55},
    "boreal":          {"grain_type": "hop_heavy",     "beer_type": "ipa",       "bitterness": 0.80, "maltiness": 0.35, "clarity": 0.70, "body": 0.45, "carbonation": 0.60, "aroma": 0.75},
    # Extended biomes
    "temperate":       {"grain_type": "crystal_malt",  "beer_type": "amber_ale", "bitterness": 0.38, "maltiness": 0.62, "clarity": 0.68, "body": 0.52, "carbonation": 0.52, "aroma": 0.52},
    "birch_forest":    {"grain_type": "dark_malt",     "beer_type": "brown_ale", "bitterness": 0.28, "maltiness": 0.68, "clarity": 0.55, "body": 0.62, "carbonation": 0.42, "aroma": 0.48},
    "redwood":         {"grain_type": "roasted_malt",  "beer_type": "porter",    "bitterness": 0.48, "maltiness": 0.62, "clarity": 0.28, "body": 0.72, "carbonation": 0.38, "aroma": 0.58},
    "wasteland":       {"grain_type": "pale_malt",     "beer_type": "barleywine","bitterness": 0.62, "maltiness": 0.85, "clarity": 0.52, "body": 0.88, "carbonation": 0.28, "aroma": 0.58},
    "fungal":          {"grain_type": "wild_grain",    "beer_type": "sour",      "bitterness": 0.12, "maltiness": 0.30, "clarity": 0.28, "body": 0.38, "carbonation": 0.72, "aroma": 0.70},
    "steep_hills":     {"grain_type": "pale_malt",     "beer_type": "pilsner",   "bitterness": 0.32, "maltiness": 0.35, "clarity": 0.92, "body": 0.28, "carbonation": 0.82, "aroma": 0.38},
    "steppe":          {"grain_type": "pale_malt",     "beer_type": "pilsner",   "bitterness": 0.28, "maltiness": 0.32, "clarity": 0.90, "body": 0.25, "carbonation": 0.80, "aroma": 0.35},
    "desert":          {"grain_type": "crystal_malt",  "beer_type": "barleywine","bitterness": 0.58, "maltiness": 0.80, "clarity": 0.55, "body": 0.85, "carbonation": 0.25, "aroma": 0.55},
    "mediterranean":   {"grain_type": "crystal_malt",  "beer_type": "amber_ale", "bitterness": 0.32, "maltiness": 0.58, "clarity": 0.72, "body": 0.48, "carbonation": 0.58, "aroma": 0.62},
    "east_asian":      {"grain_type": "wheat_malt",    "beer_type": "pilsner",   "bitterness": 0.18, "maltiness": 0.28, "clarity": 0.95, "body": 0.20, "carbonation": 0.85, "aroma": 0.28},
    "south_asian":     {"grain_type": "spiced_grain",  "beer_type": "sour",      "bitterness": 0.18, "maltiness": 0.42, "clarity": 0.32, "body": 0.42, "carbonation": 0.68, "aroma": 0.75},
}

MASH_TYPES = {
    "pale_malt":    {"label": "Pale Malt",    "desc": "Clean and crisp. The classic base malt for most beer styles.", "maltiness": +0.15, "body": +0.05, "bitterness": +0.00, "clarity": +0.00, "aroma": +0.00, "carbonation": +0.00},
    "crystal_malt": {"label": "Crystal Malt", "desc": "Caramel sweetness and fuller body. Adds red-amber color.", "maltiness": +0.20, "body": +0.10, "bitterness": +0.00, "clarity": +0.00, "aroma": +0.10, "carbonation": +0.00},
    "roasted_malt": {"label": "Roasted Malt", "desc": "Coffee and chocolate notes. Darkens the beer significantly.", "maltiness": +0.10, "body": +0.20, "bitterness": +0.05, "clarity": -0.15, "aroma": +0.05, "carbonation": +0.00},
    "wheat_malt":   {"label": "Wheat Malt",   "desc": "Hazy, soft body with bready notes. Essential for wheat beers.", "maltiness": +0.05, "body": -0.05, "bitterness": +0.00, "clarity": -0.10, "aroma": +0.15, "carbonation": +0.05},
}

HOP_ADDITIONS = {
    "early": {"label": "Early Hops (60 min)", "desc": "Bitter hops added at the boil start. High bitterness, less aroma.",         "bitterness": +0.20, "aroma": -0.05},
    "late":  {"label": "Late Hops (10 min)",  "desc": "Aromatic hops added near the end of boil. Fragrant, lower bitterness.",     "bitterness": +0.08, "aroma": +0.20},
    "dry":   {"label": "Dry Hop",             "desc": "Hops added after fermentation. Maximum aroma, minimal bitterness boost.",   "bitterness": +0.02, "aroma": +0.30, "clarity": -0.05},
}

YEAST_TYPES = {
    "ale_yeast":   {"label": "Ale Yeast",   "desc": "Warm fermentation. Fruity esters and full-flavored result.",  "aroma": +0.10, "body": +0.05, "clarity": +0.00, "ferment_var": 0.05},
    "lager_yeast": {"label": "Lager Yeast", "desc": "Cold-fermenting. Clean, crisp, and very clear result.",       "aroma": +0.00, "body": +0.00, "clarity": +0.10, "ferment_var": 0.03},
    "wild_yeast":  {"label": "Wild Yeast",  "desc": "Unpredictable funk and complexity. High-variance quality.",   "aroma": +0.15, "body": +0.00, "clarity": -0.05, "ferment_var": 0.18},
    "wheat_yeast": {"label": "Wheat Yeast", "desc": "Banana and clove notes. Traditional for hefeweizens.",        "aroma": +0.15, "body": +0.05, "clarity": -0.10, "ferment_var": 0.06},
}

VESSEL_TYPES = {
    "cask":   {"label": "Cask",   "desc": "Traditional cask conditioning. Soft carbonation and smooth body.",    "body": +0.05, "carbonation": +0.00, "quality_mult": 1.05},
    "bottle": {"label": "Bottle", "desc": "Classic bottle conditioning. Consistent carbonation and clean finish.", "body": +0.00, "carbonation": +0.05, "quality_mult": 1.00},
    "keg":    {"label": "Keg",    "desc": "Forced carbonation. Reliable quality and sharp, lively bubbles.",     "body": +0.00, "carbonation": +0.10, "quality_mult": 1.02},
}

CONDITION_DURATIONS = {
    "quick":    {"label": "Quick (2 weeks)",    "quality_mult": 1.00, "complexity_delta": 0.03},
    "standard": {"label": "Standard (4 weeks)", "quality_mult": 1.05, "complexity_delta": 0.07},
    "extended": {"label": "Extended (8 weeks)", "quality_mult": 1.10, "complexity_delta": 0.14},
}

BEER_TYPE_DESCS = {
    "ale":        "Ale — balanced, biscuity, warm-fermented",
    "lager":      "Lager — crisp, clean, cold-conditioned",
    "stout":      "Stout — dark, roasty, full-bodied",
    "ipa":        "IPA — hop-forward, bitter, aromatic",
    "wheat_beer": "Wheat Beer — hazy, refreshing, soft",
    "saison":     "Saison — spiced, rustic, farmhouse",
    "porter":     "Porter — smooth, dark, chocolate and coffee notes",
    "amber_ale":  "Amber Ale — balanced, caramel-malty, sessionable",
    "pilsner":    "Pilsner — crisp, clean, brilliantly clear",
    "brown_ale":  "Brown Ale — nutty, mild, mellow finish",
    "sour":       "Sour — tart, wild-fermented, refreshingly acidic",
    "barleywine": "Barleywine — intense, warming, high-gravity",
}

BEER_TYPE_COLORS = {
    "ale":        (190, 120,  40),
    "lager":      (220, 190,  80),
    "stout":      ( 40,  25,  15),
    "ipa":        (210, 150,  40),
    "wheat_beer": (235, 220, 140),
    "saison":     (200, 170,  70),
    "porter":     ( 55,  35,  20),
    "amber_ale":  (200, 110,  38),
    "pilsner":    (240, 225, 115),
    "brown_ale":  (150,  90,  40),
    "sour":       (210, 230, 140),
    "barleywine": (165,  85,  25),
}

BUFF_DESCS = {
    "heartiness":  "Max HP +20% / Melee power +10%",
    "refreshment": "Hunger drain -50% / Sprint speed +10%",
    "fortitude":   "Cold resistance / Mining speed +20%",
    "keenness":    "Collect radius +60% / Discovery XP +20%",
    "swiftness":   "Move speed +15% / Jump height +1",
    "wanderlust":  "Fall damage -40% / Explore radius +25%",
    "resilience":  "Fall damage -50% / Toughness",
    "abundance":   "Food restore +20% / Harvest bonus",
    "precision":   "Mining power +15% / Tool efficiency",
    "steadiness":  "Hunger drain -35% / Steady footing",
    "immunity":    "Health regen +0.8/s / Poison resist",
    "endurance":   "Mining power +10% / Carry strength",
}

BEER_BUFFS = {
    "ale":        "heartiness",
    "lager":      "refreshment",
    "stout":      "fortitude",
    "ipa":        "keenness",
    "wheat_beer": "swiftness",
    "saison":     "wanderlust",
    "porter":     "resilience",
    "amber_ale":  "abundance",
    "pilsner":    "precision",
    "brown_ale":  "steadiness",
    "sour":       "immunity",
    "barleywine": "endurance",
}

_FLAVOR_POOLS = {
    "bitterness":  ["pine resin", "grapefruit pith", "cedar", "dried hops", "herbal bite", "resin"],
    "maltiness":   ["biscuit", "bread crust", "caramel", "toffee", "toasted grain", "dried malt"],
    "aroma":       ["citrus zest", "floral", "tropical fruit", "fresh hops", "stone fruit", "spice"],
    "body":        ["velvety", "full-bodied", "creamy", "silky", "warming", "rounded"],
    "carbonation": ["lively", "crisp bubble", "effervescent", "sprightly", "soft fizz"],
}

_HOP_NOTES = {
    "early": ["classic bitter", "clean hop"],
    "late":  ["floral lift", "citrus burst"],
    "dry":   ["dry hop aroma", "fresh pine", "tropical wave"],
}

_VESSEL_NOTES = {
    "cask":   ["cask-smooth", "real ale character"],
    "bottle": ["bottle-conditioned", "clean finish"],
    "keg":    ["keg-fresh", "sharp pour"],
}

_DURATION_NOTES = {
    "quick":    ["young hop", "fresh"],
    "standard": ["balanced conditioning"],
    "extended": ["well-conditioned", "mature depth"],
}

# Codex ordering — one entry per biome per quality tier
_CODEX_BIOMES = list(BIOME_BEER_PROFILES.keys())
BEER_TYPE_ORDER = [
    f"{biome}_{tier}"
    for biome in _CODEX_BIOMES
    for tier in ["standard", "fine", "reserve"]
]

BIOME_DISPLAY_NAMES = {
    "tropical":        "Tropical",
    "jungle":          "Jungle",
    "savanna":         "Savanna",
    "wetland":         "Wetland",
    "arid_steppe":     "Arid Steppe",
    "canyon":          "Canyon",
    "beach":           "Beach",
    "tundra":          "Tundra",
    "swamp":           "Swamp",
    "alpine_mountain": "Alpine",
    "rocky_mountain":  "Rocky Mtn",
    "rolling_hills":   "Rolling Hills",
    "boreal":          "Boreal",
    "temperate":       "Temperate",
    "birch_forest":    "Birch Forest",
    "redwood":         "Redwood",
    "wasteland":       "Wasteland",
    "fungal":          "Fungal",
    "steep_hills":     "Steep Hills",
    "steppe":          "Steppe",
    "desert":          "Desert",
    "mediterranean":   "Mediterranean",
    "east_asian":      "East Asian",
    "south_asian":     "South Asian",
    "blend":           "Blend",
}


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def apply_brew_result(beer: "Beer", mash_type: str, hop_addition: str, mash_quality: float, hop_quality: float):
    mods = MASH_TYPES.get(mash_type, {})
    for attr in ("bitterness", "maltiness", "clarity", "body", "aroma", "carbonation"):
        setattr(beer, attr, _clamp(getattr(beer, attr) + mods.get(attr, 0.0)))
    hmods = HOP_ADDITIONS.get(hop_addition, {})
    beer.bitterness  = _clamp(beer.bitterness  + hmods.get("bitterness", 0.0))
    beer.aroma       = _clamp(beer.aroma       + hmods.get("aroma", 0.0))
    if "clarity" in hmods:
        beer.clarity = _clamp(beer.clarity + hmods["clarity"])
    # Quality contribution from mini-game skill (mash_quality: 0-1, hop_quality: 0-1)
    beer.ferment_quality = _clamp(mash_quality * 0.4 + hop_quality * 0.6)
    beer.mash_type   = mash_type
    beer.hop_addition = hop_addition
    beer.state = "brewed"
    beer.flavor_notes = generate_flavor_notes(beer)


def apply_ferment_result(beer: "Beer", yeast_type: str, time_in_optimal: float, total_time: float, rack_bonus: float, penalties: int):
    ymods = YEAST_TYPES.get(yeast_type, {})
    beer.aroma   = _clamp(beer.aroma   + ymods.get("aroma", 0.0))
    beer.body    = _clamp(beer.body    + ymods.get("body", 0.0))
    beer.clarity = _clamp(beer.clarity + ymods.get("clarity", 0.0))
    opt_frac = (time_in_optimal / max(total_time, 0.1))
    var = ymods.get("ferment_var", 0.05)
    quality = _clamp(
        opt_frac * 0.60
        + rack_bonus * 0.25
        + beer.ferment_quality * 0.15
        - penalties * 0.10
        + random.gauss(0, var)
    )
    beer.ferment_quality = quality
    beer.yeast_type = yeast_type
    beer.state = "fermented"
    beer.flavor_notes = generate_flavor_notes(beer)


def apply_condition_result(beer: "Beer", vessel: str, duration: str, dry_hopped: bool, dry_hop_bonus: float):
    vmods = VESSEL_TYPES.get(vessel, {})
    dmods = CONDITION_DURATIONS.get(duration, {})
    beer.body        = _clamp(beer.body        + vmods.get("body", 0.0))
    beer.carbonation = _clamp(beer.carbonation + vmods.get("carbonation", 0.0))
    if dry_hopped:
        beer.aroma    = _clamp(beer.aroma    + 0.12 + dry_hop_bonus * 0.10)
        beer.clarity  = _clamp(beer.clarity  - 0.05)
    raw_quality = beer.ferment_quality * vmods.get("quality_mult", 1.0) * dmods.get("quality_mult", 1.0)
    beer.condition_quality = _clamp(raw_quality + dmods.get("complexity_delta", 0.0) * 0.5)
    beer.vessel = vessel
    beer.condition_duration = duration
    beer.state = "conditioned"
    beer.flavor_notes = generate_flavor_notes(beer)


def generate_flavor_notes(beer: "Beer") -> list:
    rng = random.Random(hash((beer.seed, "beer_flavor", beer.beer_type, beer.hop_addition, beer.vessel)))
    notes = []
    for attr, pool in _FLAVOR_POOLS.items():
        val = getattr(beer, attr, 0.0)
        if val > 0.58:
            notes.append(rng.choice(pool))
    if beer.hop_addition in _HOP_NOTES:
        notes.append(rng.choice(_HOP_NOTES[beer.hop_addition]))
    if beer.vessel in _VESSEL_NOTES:
        notes.append(rng.choice(_VESSEL_NOTES[beer.vessel]))
    if beer.condition_duration in _DURATION_NOTES:
        notes.append(rng.choice(_DURATION_NOTES[beer.condition_duration]))
    tail = {
        "ale":        "warm ale finish",
        "lager":      "crisp lager fade",
        "stout":      "dark roast linger",
        "ipa":        "resinous hop trail",
        "wheat_beer": "soft wheat close",
        "saison":     "rustic spice end",
        "porter":     "smooth porter finish",
        "amber_ale":  "amber malt close",
        "pilsner":    "crisp pilsner fade",
        "brown_ale":  "nutty brown linger",
        "sour":       "tart sour pucker",
        "barleywine": "warming barleywine glow",
    }.get(beer.beer_type)
    if tail:
        notes.append(tail)
    seen = []
    for n in notes:
        if n not in seen:
            seen.append(n)
    return seen[:6] if seen else ["clean brew"]


def make_beer_blend(components: list) -> "Beer":
    n = len(components)
    seed = sum(b.seed for b in components) // n
    uid = hashlib.md5(
        f"beerblend_{'_'.join(b.uid for b in components)}".encode()
    ).hexdigest()[:12]

    def avg(attr):
        return _clamp(sum(getattr(b, attr) for b in components) / n)

    type_counts = {}
    for b in components:
        type_counts[b.beer_type] = type_counts.get(b.beer_type, 0) + 1
    dominant_type = max(type_counts, key=type_counts.get)

    all_notes = []
    for b in components:
        for note in b.flavor_notes:
            if note not in all_notes:
                all_notes.append(note)

    return Beer(
        uid=uid,
        origin_biome="blend",
        grain_type="blend",
        beer_type=dominant_type,
        state="blended",
        bitterness=avg("bitterness"),
        maltiness=avg("maltiness"),
        clarity=avg("clarity"),
        body=avg("body"),
        carbonation=avg("carbonation"),
        aroma=avg("aroma"),
        ferment_quality=avg("ferment_quality"),
        condition_quality=avg("condition_quality"),
        flavor_notes=all_notes[:6],
        seed=seed,
        blend_components=[b.uid for b in components],
    )


def get_bottle_output_id(beer_type: str, quality: float) -> str:
    if quality >= 0.70:
        return f"{beer_type}_reserve"
    if quality >= 0.40:
        return f"{beer_type}_fine"
    return beer_type


class BeerGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, biodome: str) -> "Beer":
        self._counter += 1
        seed = (self._world_seed * 53 + self._counter * 6271) & 0xFFFFFFFF
        uid = hashlib.md5(f"beer_{seed}_{self._counter}".encode()).hexdigest()[:12]

        profile = BIOME_BEER_PROFILES.get(biodome, BIOME_BEER_PROFILES["rolling_hills"])
        rng = random.Random(seed)

        def jitter(base):
            return _clamp(base + rng.gauss(0, 0.06))

        return Beer(
            uid=uid,
            origin_biome=biodome,
            grain_type=profile["grain_type"],
            beer_type=profile["beer_type"],
            state="raw",
            bitterness=jitter(profile["bitterness"]),
            maltiness=jitter(profile["maltiness"]),
            clarity=jitter(profile["clarity"]),
            body=jitter(profile["body"]),
            carbonation=jitter(profile["carbonation"]),
            aroma=jitter(profile["aroma"]),
            ferment_quality=0.0,
            condition_quality=0.0,
            flavor_notes=[],
            seed=seed,
        )
