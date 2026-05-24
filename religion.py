"""Religion — faiths, clergy, and the doctrinal layer over regions.

Each biome group seeds one primary faith; regions in the same group share that
primary faith but each gets its own bishop and per-region adherence. Faiths
have a doctrine (martial / ascetic / mercantile / naturalist / scholarly /
mystic) that drives drift, interactions with houses/guilds/orders, and player
actions.

This module is the skeleton: data classes, registries, worldgen seeding,
clergy generation, a daily drift tick, and save/load. Player actions,
schisms, heresy, and inquisitions are layered on in later passes — they
plug into the same registries.

Mirrors politics.py in structure. Pure data + tick logic. No pygame, no UI.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Doctrines — the spine of the system. Each entry drives drift, blessings,
# and which player actions are legal. New doctrines just need a row here.
# ---------------------------------------------------------------------------

FAITH_DOCTRINES = {
    "martial": {
        "piety_drift":      +0.10,
        "orthodoxy_drift":  +0.05,
        "zeal_drift":       +0.15,
        "treasury_mult":    1.00,
        "blesses_orders":   True,
        "hostile_to":       ("scandal", "heresy"),
        "tint":             (200, 100, 90),
        "epithet":          "the Iron Faith",
    },
    "ascetic": {
        "piety_drift":      +0.20,
        "orthodoxy_drift":  +0.10,
        "zeal_drift":       -0.05,
        "treasury_mult":    0.85,
        "blesses_orders":   False,
        "hostile_to":       ("wealth", "hedonism"),
        "tint":             (180, 190, 210),
        "epithet":          "the Hollow Path",
    },
    "mercantile": {
        "piety_drift":      0.0,
        "orthodoxy_drift":  -0.05,
        "zeal_drift":       -0.10,
        "treasury_mult":    1.15,
        "blesses_orders":   False,
        "hostile_to":       ("asceticism",),
        "tint":             (210, 175, 90),
        "epithet":          "the Covenant",
    },
    "naturalist": {
        "piety_drift":      +0.05,
        "orthodoxy_drift":  -0.10,
        "zeal_drift":       0.0,
        "treasury_mult":    0.95,
        "blesses_orders":   False,
        "hostile_to":       ("mining", "industry"),
        "tint":             (110, 170, 110),
        "epithet":          "the Greenpath",
    },
    "scholarly": {
        "piety_drift":      0.0,
        "orthodoxy_drift":  +0.15,
        "zeal_drift":       -0.10,
        "treasury_mult":    0.95,
        "blesses_orders":   False,
        "hostile_to":       ("heresy",),
        "tint":             (150, 175, 200),
        "epithet":          "the Lettered Way",
    },
    "mystic": {
        "piety_drift":      +0.05,
        "orthodoxy_drift":  -0.20,
        "zeal_drift":       +0.05,
        "treasury_mult":    0.95,
        "blesses_orders":   False,
        "hostile_to":       ("scholarship",),
        "tint":             (170, 120, 200),
        "epithet":          "the Veiled Faith",
    },
}
_DEFAULT_DOCTRINE = "ascetic"


def doctrine_profile(doctrine: str) -> dict:
    return FAITH_DOCTRINES.get(doctrine, FAITH_DOCTRINES[_DEFAULT_DOCTRINE])


# Biome-group → which doctrines are eligible as the *primary* faith. The first
# is the most likely; the rest are fallbacks if multiple faiths seed in one
# group. Minor faiths can pick from any doctrine.
PRIMARY_DOCTRINE_BY_GROUP = {
    "forest":         ["naturalist", "mystic"],
    "boreal":         ["ascetic", "martial"],
    "jungle":         ["mystic", "naturalist"],
    "tropical":       ["naturalist", "mercantile"],
    "mediterranean":  ["mercantile", "scholarly"],
    "coastal":        ["mercantile", "naturalist"],
    "desert":         ["ascetic", "mystic"],
    "steppe":         ["martial", "mystic"],
    "east_asian":     ["scholarly", "mystic"],
    "levant":         ["scholarly", "mercantile"],
    "wasteland":      ["ascetic", "martial"],
    "highlands":      ["martial", "ascetic"],
    "silk_road":      ["mercantile", "scholarly"],
    "arabia":         ["mystic", "scholarly"],
    "persia":         ["scholarly", "mystic"],
    "south_asian":    ["mystic", "ascetic"],
    "yunnan":         ["scholarly", "naturalist"],
}
_FALLBACK_PRIMARY = ["ascetic", "scholarly"]


# Faith name fragments by doctrine — combined procedurally so each world's
# faiths sound distinct without us listing every possible name.
_FAITH_NAME_FRAGMENTS = {
    "martial":     {"prefix": ["Order", "Crucible", "Forge", "Iron Faith", "Brotherhood"],
                    "of":     ["the Pyre", "the Anvil", "the Crimson Vow", "the Long March",
                               "the Watchful Flame", "the Last Stand"]},
    "ascetic":     {"prefix": ["Path", "Stillness", "Hollow Faith", "Vow", "Silent Way"],
                    "of":     ["the Empty Bowl", "Endless Dawn", "the Quiet Stone",
                               "the Bare Hand", "Patient Dust", "the Long Fast"]},
    "mercantile":  {"prefix": ["Covenant", "Concord", "Guild Faith", "Pact"],
                    "of":     ["the Open Hand", "Honest Coin", "the Sealed Ledger",
                               "the Twin Scales", "the Bright Mark", "the Counting House"]},
    "naturalist":  {"prefix": ["Greenpath", "Wildkeeping", "Root Faith", "Old Ways"],
                    "of":     ["the Long Root", "the Turning Year", "the Hidden Grove",
                               "the Antlered One", "Mother Soil", "the Quiet Wood"]},
    "scholarly":   {"prefix": ["Scriptorium", "Codex Faith", "Lettered Way", "Pale Library"],
                    "of":     ["the Inked Word", "the Open Folio", "the Glass Tower",
                               "the Index", "the Marginal Hand", "the Bound Page"]},
    "mystic":      {"prefix": ["Veil", "Mirror Faith", "Cult", "Inner Eye", "Threshold"],
                    "of":     ["the Pale Witness", "the Folded Sky", "the Sleeping King",
                               "the Whispering Stones", "the Mirror Twin", "Unseen Stars"]},
}


# ---------------------------------------------------------------------------
# Registries — module-level singletons. Same shape as politics.HOUSE_STATES.
# ---------------------------------------------------------------------------

FAITH_STATES:    dict[int, "FaithState"]   = {}      # faith_id -> state
FAITH_REGIONS:   dict[int, dict[int, int]] = {}      # faith_id -> {region_id: adherence_pct 0..100}
CLERGY:          dict[int, "RegionalClergy"] = {}    # region_id -> clergy slate
FAITH_RELATIONS: dict[tuple[int, int], int] = {}     # (lo, hi) -> -100..+100
FAITH_RELATION_REASONS: dict[tuple[int, int], list] = {}   # last-8 incident log
SCHISMS:         dict[int, "SchismState"] = {}       # faith_id -> active crisis
HERESY:          dict[int, dict[int, int]] = {}      # region_id -> {faith_id: heresy_pct}
PLAYER_STANDING: dict[int, "FaithStandingRecord"] = {}   # faith_id -> record

_NEXT_FAITH_ID = 1

# Per-region scandal last-seen, so the daily tick can react to *deltas* in
# House.scandal rather than the standing value. Filled lazily in tick.
_HOUSE_SCANDAL_SEEN: dict[int, int] = {}

# Highest newswire day we've already reacted to — prevents double-processing
# when the day-tick fires repeatedly during a single sim step.
_NEWSWIRE_LAST_DAY: int = -1


ORTHODOXY_SCHISM_THRESHOLD = 30
HERESY_SCHISM_THRESHOLD    = 40
CONCLAVE_INTERVAL_YEARS    = 7
SCHISM_RESOLVE_DAYS        = 60


# ---------------------------------------------------------------------------
# Cross-system reaction maps. Tweak these to change how faiths respond to
# the rest of the world — single source of truth, no logic scattered.
# ---------------------------------------------------------------------------

# House.agenda → per-doctrine reactions when the agenda matches.
# +piety / +scandal / +zeal / +orthodoxy are applied to faiths whose
# doctrine appears here when a backing house carries that agenda.
HOUSE_AGENDA_DOCTRINE_BONUS = {
    "pious":       {"ascetic":    {"piety": +1, "scandal": -1},
                    "scholarly":  {"orthodoxy": +1}},
    "martial":     {"martial":    {"zeal": +1}},
    "mercantile":  {"mercantile": {"treasury": +30},
                    "ascetic":    {"scandal": +1}},
    "builder":     {"naturalist": {"piety": -1}},
    "hedonist":    {"ascetic":    {"scandal": +2},
                    "mystic":     {"orthodoxy": -1}},
    "scholarly":   {"scholarly":  {"orthodoxy": +1, "piety": +1},
                    "mystic":     {"orthodoxy": -1}},
}

# industry_events.EVENT_REGISTRY key → per-doctrine reactions.
INDUSTRY_EVENT_DOCTRINE_REACTION = {
    "gold_rush":   {"naturalist": {"piety": -2, "scandal": +3},
                    "mercantile": {"piety": +2, "treasury": +50}},
    "plague":      {"ascetic":    {"piety": +3},
                    "scholarly":  {"orthodoxy": +2},
                    "mystic":     {"zeal": +2}},
    "bumper":      {"naturalist": {"piety": +2},
                    "mercantile": {"piety": +1}},
    "festival":    {"mercantile": {"piety": +2},
                    "ascetic":    {"scandal": +1}},
    "embargo":     {"mercantile": {"piety": -2, "treasury": -40}},
    "strike":      {"mercantile": {"piety": -2},
                    "ascetic":    {"piety": +1}},
    "fashion":     {"ascetic":    {"orthodoxy": -2, "scandal": +1},
                    "mercantile": {"treasury": +30}},
    "frost":       {"naturalist": {"piety": +1, "zeal": +1}},
    "drought":     {"naturalist": {"piety": +1, "zeal": +1}},
    "shoal":       {"naturalist": {"piety": +1},
                    "mercantile": {"piety": +1}},
    "sabotage":    {"ascetic":    {"piety": +1},
                    "mercantile": {"scandal": +1}},
}

# Knightly-order tradition → which doctrines bond ("+") vs clash ("-").
# Bonded orders feed faith zeal; clashing orders bleed faith prestige.
ORDER_TRADITION_DOCTRINE_AFFINITY = {
    "templar":     {"+": ("martial", "ascetic"),    "-": ("mercantile",)},
    "hospitaller": {"+": ("ascetic", "naturalist"), "-": ("martial",)},
    "cavalier":    {"+": ("martial", "mercantile"), "-": ("ascetic",)},
    "mercenary":   {"+": ("mercantile",),           "-": ("ascetic", "scholarly")},
    "marcher":     {"+": ("martial",),              "-": ()},
    "magisterial": {"+": ("scholarly",),            "-": ("mystic",)},
    "berserker":   {"+": ("martial", "mystic"),     "-": ("ascetic", "scholarly")},
    "errant":      {"+": (),                        "-": ()},
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class FaithState:
    faith_id:   int
    name:       str
    doctrine:   str
    biome_group: str             # group the faith was seeded from
    piety:      int = 50         # 0..100  — adherence weighted average
    orthodoxy:  int = 80         # 0..100  — drift below schism threshold splits
    zeal:       int = 20         # 0..100  — drives crusades / inquisitions
    treasury:   int = 0          # tithes + relics - upkeep
    scandal:    int = 0          # 0..100
    posture:    str = "stable"   # stable | rising | declining | crisis | schism
    head_id:    int = 0          # opaque slate id, see _head_slate
    head_name:  str = ""
    head_title: str = "Hierophant"
    last_event_day: int = -1
    # Historical backbone — populated at creation by _build_faith_history.
    founded_year:      int  = 0
    past_heads:        list = field(default_factory=list)   # [{year, title, name}]
    historical_events: list = field(default_factory=list)   # [{year, kind, text}]


@dataclass
class RegionalClergy:
    region_id:  int
    faith_id:   int                              # the dominant faith in this region
    bishop_name: str = ""
    bishop_title: str = "Bishop"
    posture:    str = "loyal"                    # loyal | reformist | heretical
    abbots:     list = field(default_factory=list)   # [{"name", "monastery_outpost_id"}]
    next_conclave_year: int = 0


@dataclass
class SchismState:
    faith_id:   int
    crisis_started_day: int
    breakaway_name:     str
    breakaway_doctrine: str
    support:    int = 30             # how strong the breakaway is, 0..100
    resolved:   bool = False
    outcome:    str = ""              # "reunited" | "split" | "purged"


@dataclass
class FaithStandingRecord:
    faith_id:   int
    standing:   int = 0              # -100..+100
    pilgrim_marks: int = 0           # cumulative pilgrimage credit
    relics_donated: int = 0
    log:        list = field(default_factory=list)   # [{"day","delta","source"}]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pair_key(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def get_faith(faith_id: int) -> Optional[FaithState]:
    return FAITH_STATES.get(faith_id)


def faiths_for_region(region_id: int) -> list[FaithState]:
    """All faiths with non-zero adherence in this region, sorted by share."""
    out = []
    for fid, regions in FAITH_REGIONS.items():
        share = regions.get(region_id, 0)
        if share > 0:
            f = FAITH_STATES.get(fid)
            if f:
                out.append((share, f))
    out.sort(key=lambda t: -t[0])
    return [f for _, f in out]


def primary_faith_of(region_id: int) -> Optional[FaithState]:
    faiths = faiths_for_region(region_id)
    return faiths[0] if faiths else None


def faith_for_region(region_id: int) -> Optional[FaithState]:
    """Guaranteed faith lookup: primary if present; if not, lazy-seed clergy
    + adherence from the world-spanning minor faith; if NOTHING is seeded
    yet (very early in worldgen), return any FaithState we can find."""
    f = primary_faith_of(region_id)
    if f is not None:
        return f
    # Try to lazy-bind the most adherent existing faith to this region.
    if FAITH_STATES:
        # Prefer a faith that already touches this region (any adherence)
        for fid, regions in FAITH_REGIONS.items():
            if regions.get(region_id, 0) > 0:
                return FAITH_STATES.get(fid)
        # Otherwise attach the first faith (often the world-spanning minor)
        fallback = next(iter(FAITH_STATES.values()))
        FAITH_REGIONS.setdefault(fallback.faith_id, {})[region_id] = 30
        return fallback
    return None


def faith_for_outpost(op) -> Optional[FaithState]:
    """Resolve an outpost's faith. Heretic hideouts route to a schismatic
    breakaway if one exists in the region (otherwise to any mystic/ascetic
    faith); other religious outposts use the regional primary."""
    try:
        from outposts import region_for_outpost
    except Exception:
        return None
    region = region_for_outpost(op)
    if region is None:
        # Outpost outside any region — pick any faith so the panel still works
        return next(iter(FAITH_STATES.values()), None)

    if getattr(op, "outpost_type", "") == "heretic_hideout":
        return _heretical_faith_for_region(region.region_id)
    return faith_for_region(region.region_id)


def _heretical_faith_for_region(region_id: int) -> Optional[FaithState]:
    """For heretic hideouts: prefer an active schism's breakaway (lives as
    its own FaithState after step 7 split), else the most off-orthodoxy
    faith touching the region, else any mystic/ascetic faith."""
    # 1. Look for a recently-spawned breakaway whose biome_group matches the
    #    region's biome_group — that's a real schism faith.
    try:
        from towns import REGIONS
        region = REGIONS.get(region_id)
        group  = getattr(region, "biome_group", "") if region else ""
    except Exception:
        group = ""
    breakaways = [f for f in FAITH_STATES.values()
                  if f.biome_group == group
                  and f.faith_id not in {fid for fid in FAITH_REGIONS
                                          if FAITH_REGIONS[fid].get(region_id, 0) >= 50}]
    if breakaways:
        # The newest faith (highest id) is the most likely breakaway
        breakaways.sort(key=lambda f: -f.faith_id)
        return breakaways[0]
    # 2. Any non-mainstream faith with low orthodoxy
    if FAITH_STATES:
        candidates = sorted(FAITH_STATES.values(),
                            key=lambda f: f.orthodoxy)
        for f in candidates:
            if f.doctrine in ("mystic", "ascetic"):
                return f
        return candidates[0]
    return None


def faith_for_position(world, bx: int) -> Optional[FaithState]:
    """Resolve a faith for any in-world position — used by NPCs at spawn."""
    try:
        from towns import region_for_bx
        region = region_for_bx(world, bx)
    except Exception:
        region = None
    if region is None:
        return next(iter(FAITH_STATES.values()), None)
    return faith_for_region(region.region_id)


def get_relation(a: int, b: int) -> int:
    return FAITH_RELATIONS.get(_pair_key(a, b), 0)


def adjust_faith_relation(a: int, b: int, delta: int) -> int:
    if a == b:
        return 0
    cur = get_relation(a, b)
    new = max(-100, min(100, cur + delta))
    FAITH_RELATIONS[_pair_key(a, b)] = new
    return new


def log_faith_relation(a: int, b: int, day: int, kind: str, note: str) -> None:
    key = _pair_key(a, b)
    bucket = FAITH_RELATION_REASONS.setdefault(key, [])
    bucket.insert(0, {"day": day, "kind": kind, "note": note})
    del bucket[8:]


def get_standing(faith_id: int) -> int:
    rec = PLAYER_STANDING.get(faith_id)
    return rec.standing if rec else 0


def add_standing(faith_id: int, delta: int, source: str, day: int) -> None:
    rec = PLAYER_STANDING.setdefault(faith_id, FaithStandingRecord(faith_id=faith_id))
    rec.standing = max(-100, min(100, rec.standing + delta))
    rec.log.insert(0, {"day": day, "delta": delta, "source": source})
    del rec.log[200:]


def standing_tier(score: int) -> tuple[str, tuple]:
    if score >= 80:  return ("Anointed",      (235, 215, 130))
    if score >= 40:  return ("Patron",        (220, 200, 70))
    if score >= 10:  return ("Faithful",      (160, 200, 130))
    if score >= -10: return ("Lay",           (140, 130, 100))
    if score >= -40: return ("Suspect",       (210, 140, 80))
    return ("Heretic", (210, 80, 70))


# ---------------------------------------------------------------------------
# Name generation
# ---------------------------------------------------------------------------

def _make_faith_name(doctrine: str, rng: random.Random) -> str:
    frags = _FAITH_NAME_FRAGMENTS.get(doctrine, _FAITH_NAME_FRAGMENTS["ascetic"])
    return f"{rng.choice(frags['prefix'])} of {rng.choice(frags['of'])}"


_HEAD_TITLE_BY_DOCTRINE = {
    "martial":     "Grandmaster Patriarch",
    "ascetic":     "Hierophant",
    "mercantile":  "High Steward",
    "naturalist":  "Archdruid",
    "scholarly":   "Lector Primarch",
    "mystic":      "Veilkeeper",
}

_BISHOP_TITLE_BY_DOCTRINE = {
    "martial":     "Templar Bishop",
    "ascetic":     "Anchorite",
    "mercantile":  "Provost",
    "naturalist":  "Greenwarden",
    "scholarly":   "Lector",
    "mystic":      "Veil-Bishop",
}


def _first_name_pool(biome_group: str) -> list[str]:
    """Reuse politics' name pools — keeps faith heads consistent with the
    cultural flavor of their home region."""
    try:
        import politics as pol
        return pol._FIRST_NAMES_BY_GROUP.get(biome_group, pol._DEFAULT_FIRST_NAMES)
    except Exception:
        return ["Aldric", "Maren", "Tirien", "Veska", "Oren", "Lyra"]


def _make_head_name(faith: FaithState, rng: random.Random) -> tuple[str, str]:
    pool = _first_name_pool(faith.biome_group)
    name = rng.choice(pool)
    title = _HEAD_TITLE_BY_DOCTRINE.get(faith.doctrine, "Hierophant")
    return (name, title)


# ---------------------------------------------------------------------------
# Faith + clergy seeding
# ---------------------------------------------------------------------------

def _create_faith(doctrine: str, biome_group: str, rng: random.Random) -> FaithState:
    global _NEXT_FAITH_ID
    fid = _NEXT_FAITH_ID
    _NEXT_FAITH_ID += 1
    faith = FaithState(
        faith_id    = fid,
        name        = _make_faith_name(doctrine, rng),
        doctrine    = doctrine,
        biome_group = biome_group,
    )
    head_name, head_title = _make_head_name(faith, rng)
    faith.head_name  = head_name
    faith.head_title = head_title
    faith.head_id    = rng.randint(1, 1_000_000)
    FAITH_STATES[fid] = faith
    FAITH_REGIONS[fid] = {}
    _build_faith_history(faith, rng)
    return faith


# ---------------------------------------------------------------------------
# Historical ledger generation — gives every faith a procedural backstory.
# Each event has (year, kind, text). Kinds are short tags used by UI for
# coloring. Text uses {head} / {faith} substitution.
# ---------------------------------------------------------------------------

# Doctrine → event pool. Each entry: (weight, kind, template). Weights make
# certain stories more common for certain doctrines.
_FAITH_EVENT_POOL = {
    "martial": [
        (4, "crusade",      "The {faith} marched on the heathen at {place}."),
        (3, "miracle",      "{head} survived an arrow at {place}; the troops called it divine."),
        (2, "schism",       "A breakaway brotherhood was put to the sword."),
        (2, "saint",        "Brother {place} of the lance was canonised."),
        (1, "persecution",  "The faithful were driven from {place} for a generation."),
    ],
    "ascetic": [
        (4, "founder_fast", "{head} kept the long fast at {place} for a year and a day."),
        (3, "hermitage",    "A new hermitage was founded in the cliffs of {place}."),
        (2, "miracle",      "{head} restored sight to a beggar at {place}."),
        (2, "vow",          "The Vow of {place} — adherents renounced metal for a decade."),
        (1, "plague",       "Plague struck; the faithful nursed strangers and were sainted."),
    ],
    "mercantile": [
        (4, "council",      "The Council of {place} set fair weights for every market."),
        (3, "golden_age",   "Tithes from the {place} trade quadrupled the treasury."),
        (2, "scandal",      "{head} was caught skimming the {place} tithe; replaced quietly."),
        (2, "trade_pact",   "A pact with the {place} guilds bound coin to scripture."),
        (1, "famine",       "Famine year — the faith opened its granaries and was praised."),
    ],
    "naturalist": [
        (4, "grove",        "The Old Grove at {place} was consecrated; no axe has touched it."),
        (3, "miracle",      "A spring opened at {head}'s feet in the dust of {place}."),
        (2, "schism",       "The leafkeepers split from the rootkeepers over the burning of {place}."),
        (2, "harvest",      "Seven good harvests followed {head}'s blessing of {place}."),
        (1, "axe_riot",     "Lumbermen burned the shrine at {place} and were cursed in turn."),
    ],
    "scholarly": [
        (4, "library",      "The {place} Library was founded; copies of every sacred text within."),
        (3, "translation",  "{head} completed the {place} translation in fifteen years."),
        (2, "debate",       "The Great Debate at {place} settled the question of the Three Names."),
        (2, "schism",       "A heretical commentary on the {place} verses split the order."),
        (1, "burning",      "A rival burned the {place} scriptorium; nothing survived but the index."),
    ],
    "mystic": [
        (4, "vision",       "{head} had the Vision of the {place} Star and wrote the silent book."),
        (3, "pilgrimage",   "A pilgrimage to the {place} Mirror began the great gathering."),
        (2, "schism",       "The Veil split — half the order followed the inner door."),
        (2, "miracle",      "The {place} stones spoke once, and only {head} heard."),
        (1, "persecution",  "The faithful were burned for whispering names in {place}."),
    ],
}

# Generic place-fragment pools by biome group for event flavor text.
_PLACE_FRAGMENTS = {
    "forest":         ["Greenmere", "Oakhollow", "Bracken Vale", "the Long Wood"],
    "boreal":         ["Frostgate", "Hoarvale", "the White Pass", "Wolfholt"],
    "jungle":         ["Vinemark", "the Emerald River", "Sun-Parrot Hill", "Canopy Hold"],
    "tropical":       ["Coralhaven", "the Reef Quay", "Palm Cay", "Saltwind"],
    "mediterranean":  ["Olivara", "the Silver Bay", "Cypress Hill", "the Argent Sun"],
    "coastal":        ["Anchor Bay", "Gullmark", "the Driftwood Quay"],
    "desert":         ["Dustfall", "the Dune Sea", "the Crescent Well"],
    "steppe":         ["the Long Grass", "Stallion Field", "Bronze Bow"],
    "east_asian":     ["the Cherry Pass", "Crane Hill", "the Lotus Lake"],
    "levant":         ["Cedar Hill", "Saffron Gate", "the Star of Dawn"],
    "wasteland":      ["the Ash Pits", "Rust Hollow", "the Cracked Bell"],
    "highlands":      ["Eagle Crag", "Thistle Glen", "Iron Tarn"],
    "silk_road":      ["the Caravan Pass", "Salt Comet Hill", "White Camel Wells"],
    "arabia":         ["the Crescent Quarter", "Saffron Bazaar", "Date Palm Hollow"],
    "persia":         ["the Sun-Disc Court", "Peacock Hall", "the Cedar Throne"],
    "south_asian":    ["Vermilion Sun", "the Sandalwood Vale", "Lotus Court"],
    "yunnan":         ["Jade Pass", "Mist Crane Hill", "the Bamboo River"],
}
_DEFAULT_PLACES = ["the Old Hall", "Foundstone", "the First Shrine", "the Long Road"]

# Founding year ranges by doctrine — gives older feel to ascetic/mystic, newer
# to mercantile.
_FOUNDING_AGE_RANGE = {
    "martial":     (200, 450),
    "ascetic":     (350, 600),
    "mercantile":  (120, 280),
    "naturalist":  (300, 550),
    "scholarly":   (220, 420),
    "mystic":      (400, 700),
}


def _build_faith_history(faith: FaithState, rng: random.Random) -> None:
    """Synthesize the faith's pre-game history. Deterministic given rng."""
    # Founding year (years before "present" — we use day 0 as present)
    age_min, age_max = _FOUNDING_AGE_RANGE.get(faith.doctrine, (250, 500))
    age = rng.randint(age_min, age_max)
    faith.founded_year = -age  # negative = years before day 0

    # Line of past heads — one every ~25 years up to today
    place_pool = _PLACE_FRAGMENTS.get(faith.biome_group, _DEFAULT_PLACES)
    name_pool  = _first_name_pool(faith.biome_group)
    heads: list = []
    yr = faith.founded_year
    while yr < 0:
        heads.append({
            "year":  yr,
            "title": faith.head_title,
            "name":  rng.choice(name_pool),
        })
        yr += rng.randint(18, 32)
    faith.past_heads = heads

    # Sprinkle 8–14 notable events between founding and present
    event_pool = _FAITH_EVENT_POOL.get(faith.doctrine,
                                        _FAITH_EVENT_POOL["ascetic"])
    weights = [w for w, _, _ in event_pool]
    n_events = rng.randint(8, 14)
    events: list = []

    # The first event is always the founding.
    founder = heads[0]["name"] if heads else faith.head_name
    events.append({
        "year": faith.founded_year,
        "kind": "founding",
        "text": (f"{founder} founded {faith.name} in the wake of strife at "
                 f"{rng.choice(place_pool)}."),
    })

    span = -faith.founded_year - 5  # leave ~5y gap before present
    for _ in range(n_events):
        spec = rng.choices(event_pool, weights=weights, k=1)[0]
        _, kind, tmpl = spec
        ev_year = faith.founded_year + rng.randint(5, max(6, span))
        head_at = _head_at_year(heads, ev_year, faith.head_name)
        place   = rng.choice(place_pool)
        text = tmpl.format(head=head_at, faith=faith.name, place=place)
        events.append({"year": ev_year, "kind": kind, "text": text})

    events.sort(key=lambda e: e["year"])
    faith.historical_events = events


def _head_at_year(heads: list, year: int, fallback: str) -> str:
    """Find which head was in office in the given year."""
    if not heads:
        return fallback
    current = heads[0]["name"]
    for h in heads:
        if h["year"] > year:
            break
        current = h["name"]
    return current


def _seed_clergy_for_region(region, faith: FaithState, rng: random.Random) -> RegionalClergy:
    pool = _first_name_pool(getattr(region, "biome_group", ""))
    bishop_name = rng.choice(pool)
    title = _BISHOP_TITLE_BY_DOCTRINE.get(faith.doctrine, "Bishop")
    clergy = RegionalClergy(
        region_id   = region.region_id,
        faith_id    = faith.faith_id,
        bishop_name = bishop_name,
        bishop_title = title,
        posture     = "loyal",
        next_conclave_year = CONCLAVE_INTERVAL_YEARS,
    )
    CLERGY[region.region_id] = clergy
    return clergy


def seed_faiths_for_world(world) -> None:
    """Idempotent. Walks REGIONS, groups them by biome_group, creates one
    primary faith per group + a single cross-cutting minor faith, and assigns
    bishops. Safe to call on every load."""
    try:
        from towns import REGIONS
    except Exception:
        return
    if not REGIONS:
        return

    seed = getattr(world, "seed", 0) or 0
    rng = random.Random((seed ^ 0xFA17_E1A1) & 0xFFFFFFFF)

    # Group regions by biome_group
    by_group: dict[str, list] = {}
    for region in REGIONS.values():
        by_group.setdefault(region.biome_group or "", []).append(region)

    # Track which (group, doctrine) we've created so re-seeding is a no-op.
    seeded_keys = {(f.biome_group, f.doctrine) for f in FAITH_STATES.values()}

    primary_faiths: dict[str, FaithState] = {}

    for group, regions in by_group.items():
        # Prefer first eligible doctrine for the group, deterministically chosen.
        candidates = PRIMARY_DOCTRINE_BY_GROUP.get(group, _FALLBACK_PRIMARY)
        group_rng = random.Random((seed ^ hash(group)) & 0xFFFFFFFF)
        doctrine = candidates[0]
        key = (group, doctrine)
        if key in seeded_keys:
            # Find the existing faith for this group/doctrine
            faith = next((f for f in FAITH_STATES.values()
                         if f.biome_group == group and f.doctrine == doctrine), None)
        else:
            faith = _create_faith(doctrine, group, group_rng)
            seeded_keys.add(key)
        primary_faiths[group] = faith

        # Assign each region to this faith with high adherence + seed a bishop
        adherence_rng = random.Random((seed ^ hash(group) ^ 0x9E37) & 0xFFFFFFFF)
        for region in regions:
            FAITH_REGIONS[faith.faith_id][region.region_id] = adherence_rng.randint(60, 85)
            if region.region_id not in CLERGY:
                _seed_clergy_for_region(region, faith, adherence_rng)

    # One world-spanning minor faith (mercantile by default — trade follows
    # trade routes across biomes). Lower adherence in every region.
    minor_key = ("__world__", "mercantile")
    if minor_key not in seeded_keys:
        minor_rng = random.Random((seed ^ 0xBEEF_CAFE) & 0xFFFFFFFF)
        minor = _create_faith("mercantile", "__world__", minor_rng)
        minor.name = _make_faith_name("mercantile", minor_rng)
        seeded_keys.add(minor_key)
        # Spread thinly across all regions
        for region in REGIONS.values():
            FAITH_REGIONS[minor.faith_id][region.region_id] = minor_rng.randint(5, 20)

    # Initial faith-faith relations — primaries are neutral to each other,
    # mildly hostile to their doctrine's hostile_to list. (Cheap heuristic.)
    faiths = list(FAITH_STATES.values())
    for i, fa in enumerate(faiths):
        for fb in faiths[i+1:]:
            key = _pair_key(fa.faith_id, fb.faith_id)
            if key in FAITH_RELATIONS:
                continue
            profile_a = doctrine_profile(fa.doctrine)
            profile_b = doctrine_profile(fb.doctrine)
            score = 0
            # Tag-based heuristic — symmetric.
            doctrine_b_tags = (fb.doctrine, _doctrine_tag(fb.doctrine))
            doctrine_a_tags = (fa.doctrine, _doctrine_tag(fa.doctrine))
            for tag in profile_a["hostile_to"]:
                if tag in doctrine_b_tags:
                    score -= 25
            for tag in profile_b["hostile_to"]:
                if tag in doctrine_a_tags:
                    score -= 25
            FAITH_RELATIONS[key] = score


def _doctrine_tag(doctrine: str) -> str:
    """Map a doctrine to its 'hostility tag' so relations seeding can match
    e.g. ascetic.hostile_to=('wealth',) against mercantile."""
    return {
        "mercantile": "wealth",
        "ascetic":    "asceticism",
        "scholarly":  "scholarship",
        "mystic":     "heresy",       # mystics drift into heresy easily
        "naturalist": "nature",
        "martial":    "war",
    }.get(doctrine, doctrine)


# ---------------------------------------------------------------------------
# Daily tick — drift + treasury + posture
# ---------------------------------------------------------------------------

def _compute_posture(faith: FaithState) -> str:
    if faith.faith_id in SCHISMS and not SCHISMS[faith.faith_id].resolved:
        return "schism"
    if faith.scandal >= 60 or faith.orthodoxy <= ORTHODOXY_SCHISM_THRESHOLD:
        return "crisis"
    if faith.zeal >= 70 and faith.piety >= 60:
        return "rising"
    if faith.piety <= 25:
        return "declining"
    return "stable"


def _tick_drift(faith: FaithState) -> None:
    """Apply doctrine-flavored drift. Slow — values move by fractions per day."""
    profile = doctrine_profile(faith.doctrine)
    faith.piety     = _clamp(faith.piety     + profile["piety_drift"])
    faith.orthodoxy = _clamp(faith.orthodoxy + profile["orthodoxy_drift"])
    faith.zeal      = _clamp(faith.zeal      + profile["zeal_drift"])
    # Natural piety decay if no recent events
    if faith.last_event_day >= 0:
        # nothing — _tithes / events nudge piety
        pass


def _tick_tithes(faith: FaithState) -> None:
    """Tithes scale with adherence × number of regions × doctrine multiplier.
    Treasury is capped to avoid runaway accumulation."""
    profile = doctrine_profile(faith.doctrine)
    regions = FAITH_REGIONS.get(faith.faith_id, {})
    if not regions:
        return
    avg_adherence = sum(regions.values()) // max(1, len(regions))
    daily = int(avg_adherence * len(regions) * 0.02 * profile["treasury_mult"])
    # Upkeep: bishops + monastery staff
    upkeep = 5 * len(regions)
    faith.treasury = max(0, faith.treasury + daily - upkeep)


def _clamp(v: float) -> int:
    return max(0, min(100, int(round(v))))


def _apply_reaction(faith: FaithState, delta: dict, day: int) -> None:
    """Apply a single reaction dict (e.g. {'piety': +2, 'scandal': -1}) to a
    faith, clamping fields and logging the day so we can show recency in UI."""
    for field_name, amount in delta.items():
        if field_name == "treasury":
            faith.treasury = max(0, faith.treasury + int(amount))
        elif hasattr(faith, field_name):
            cur = getattr(faith, field_name)
            setattr(faith, field_name, _clamp(cur + amount))
    faith.last_event_day = day


def _react_to_houses(day: int) -> None:
    """Pass 1: read HOUSE_STATES, react to scandal deltas and agenda matches.
    Pull-based — politics already ran today, so the house state is current."""
    try:
        from politics import HOUSE_STATES
        from towns import REGIONS
    except Exception:
        return
    for house in HOUSE_STATES.values():
        region = REGIONS.get(house.region_id)
        if region is None:
            continue
        faith = primary_faith_of(house.region_id)
        if faith is None:
            continue

        # ── Scandal delta — only react when it jumped today ──────────────
        prev = _HOUSE_SCANDAL_SEEN.get(house.region_id, house.scandal)
        delta = house.scandal - prev
        if delta >= 5:
            # A backing house just took a scandal hit — the local faith
            # is implicated by association. Piety bleeds, scandal rises.
            _apply_reaction(faith,
                            {"piety": -1, "scandal": +max(1, delta // 5)},
                            day)
        _HOUSE_SCANDAL_SEEN[house.region_id] = house.scandal

        # ── Agenda × doctrine alignment ──────────────────────────────────
        agenda_bonuses = HOUSE_AGENDA_DOCTRINE_BONUS.get(
            getattr(region, "agenda", ""), {})
        bonus = agenda_bonuses.get(faith.doctrine)
        if bonus:
            _apply_reaction(faith, bonus, day)

        # ── House in crisis → clergy posture shifts toward reformist ────
        if house.posture == "crisis":
            clergy = CLERGY.get(house.region_id)
            if clergy and clergy.posture == "loyal":
                clergy.posture = "reformist"
        elif house.posture in ("stable", "rising"):
            clergy = CLERGY.get(house.region_id)
            if clergy and clergy.posture == "reformist":
                clergy.posture = "loyal"


def _react_to_orders(day: int) -> None:
    """Pass 2: walk knightly orders, apply affinity bonuses/penalties to the
    faith of their home region. A templar order in a martial faith's region
    feeds zeal; a mercenary order in an ascetic region bleeds piety."""
    try:
        from knightly_orders import ORDERS
    except Exception:
        return
    for order in ORDERS.values():
        rid = getattr(order, "home_region", None)
        if rid is None:
            continue
        faith = primary_faith_of(rid)
        if faith is None:
            continue
        affinity = ORDER_TRADITION_DOCTRINE_AFFINITY.get(
            getattr(order, "tradition", "errant"), {"+": (), "-": ()})
        if faith.doctrine in affinity["+"]:
            _apply_reaction(faith, {"zeal": +1, "piety": +1}, day)
        elif faith.doctrine in affinity["-"]:
            _apply_reaction(faith,
                            {"orthodoxy": -1, "piety": -1, "scandal": +1},
                            day)


def _react_to_industry_events(day: int) -> None:
    """Pass 3: scan today's newswire for industry event keys; apply per-
    doctrine reactions to *all* faiths matching. Industry events are
    world-spanning so they hit every faith of the right doctrine."""
    global _NEWSWIRE_LAST_DAY
    try:
        import industry_events as ie
    except Exception:
        return
    if day <= _NEWSWIRE_LAST_DAY:
        return
    # Build a map of event keys → display names so we can match on either
    event_keys = {spec["name"]: spec["key"] for spec in ie.EVENT_REGISTRY}
    for entry in ie.NEWSWIRE:
        ev_day = entry.get("day", -1)
        if ev_day != day:
            continue
        kind = entry.get("kind", "")
        if kind != "event" and kind != "rivalry":
            continue
        headline = entry.get("headline", "")
        # Headlines are "<event_name>: ..." — pick the leading event_name.
        if kind == "rivalry":
            key = "sabotage"
        else:
            key = None
            for name, k in event_keys.items():
                if headline.startswith(name):
                    key = k
                    break
            if key is None:
                continue
        reactions = INDUSTRY_EVENT_DOCTRINE_REACTION.get(key, {})
        if not reactions:
            continue
        for faith in FAITH_STATES.values():
            delta = reactions.get(faith.doctrine)
            if delta:
                _apply_reaction(faith, delta, day)
    _NEWSWIRE_LAST_DAY = day


# ---------------------------------------------------------------------------
# Step 8: Heresy growth + auto-inquisitions
# ---------------------------------------------------------------------------

HERESY_GROWTH_ORTHODOXY_THRESHOLD = 50
HERESY_GROWTH_SCANDAL_THRESHOLD   = 20
INQUISITION_ZEAL_THRESHOLD        = 60
INQUISITION_INTERVAL_DAYS         = 21

# Tracks the last day each faith ran an auto-inquisition (per faith).
_LAST_INQUISITION_DAY: dict[int, int] = {}


def get_heresy(region_id: int, faith_id: int) -> int:
    return HERESY.get(region_id, {}).get(faith_id, 0)


def _adjust_heresy(region_id: int, faith_id: int, delta: int) -> int:
    row = HERESY.setdefault(region_id, {})
    cur = row.get(faith_id, 0)
    new = max(0, min(100, cur + delta))
    row[faith_id] = new
    return new


def _grow_heresy(day: int) -> None:
    """Heresy% climbs in regions where a faith is doctrinally fragile —
    low orthodoxy or high scandal. Bounded; decays on its own when the
    faith stabilizes."""
    for faith in FAITH_STATES.values():
        adh = FAITH_REGIONS.get(faith.faith_id, {})
        if not adh:
            continue
        growth = 0
        if faith.orthodoxy < HERESY_GROWTH_ORTHODOXY_THRESHOLD:
            growth += 1
        if faith.scandal > HERESY_GROWTH_SCANDAL_THRESHOLD:
            growth += 1
        if faith.orthodoxy < ORTHODOXY_SCHISM_THRESHOLD:
            growth += 1   # accelerated near the schism cliff
        if growth == 0:
            # Slow natural decay
            for rid in list(adh.keys()):
                if HERESY.get(rid, {}).get(faith.faith_id, 0) > 0:
                    _adjust_heresy(rid, faith.faith_id, -1)
            continue
        for rid in adh:
            _adjust_heresy(rid, faith.faith_id, growth)


def _maybe_run_inquisition(faith: FaithState, day: int) -> None:
    """Zealous faiths automatically purge heresy in their regions. Costs
    treasury, drives piety up, bumps scandal slightly (collateral)."""
    if faith.zeal < INQUISITION_ZEAL_THRESHOLD:
        return
    last = _LAST_INQUISITION_DAY.get(faith.faith_id, -999)
    if day - last < INQUISITION_INTERVAL_DAYS:
        return
    adh = FAITH_REGIONS.get(faith.faith_id, {})
    purged = 0
    for rid in adh:
        h = HERESY.get(rid, {}).get(faith.faith_id, 0)
        if h <= 0:
            continue
        _adjust_heresy(rid, faith.faith_id, -min(20, h))
        purged += 1
    if purged == 0:
        return
    _LAST_INQUISITION_DAY[faith.faith_id] = day
    _apply_reaction(faith,
                    {"piety": +2, "orthodoxy": +2,
                     "scandal": +1, "treasury": -120},
                    day)
    _push_religion_news(day,
                        f"{faith.name} launches an inquisition across {purged} "
                        f"region{'s' if purged != 1 else ''}.")


# ---------------------------------------------------------------------------
# Step 7: Schisms + conclaves
# ---------------------------------------------------------------------------

def _check_schisms(day: int) -> None:
    """Open a schism crisis when a faith's orthodoxy crashes or its heresy
    spreads past a tipping point. One active crisis per faith."""
    for faith in FAITH_STATES.values():
        if faith.faith_id in SCHISMS and not SCHISMS[faith.faith_id].resolved:
            continue
        too_unorthodox = faith.orthodoxy <= ORTHODOXY_SCHISM_THRESHOLD
        adh = FAITH_REGIONS.get(faith.faith_id, {})
        widespread_heresy = any(
            HERESY.get(rid, {}).get(faith.faith_id, 0) >= HERESY_SCHISM_THRESHOLD
            for rid in adh)
        if not (too_unorthodox or widespread_heresy):
            continue
        rng = random.Random((faith.faith_id * 7919) ^ (day * 0x4A1B) ^ 0xC0DE)
        # Breakaway doctrine drifts toward whatever's adjacent in flavor.
        breakaway = _alt_doctrine(faith.doctrine, rng)
        crisis = SchismState(
            faith_id           = faith.faith_id,
            crisis_started_day = day,
            breakaway_name     = _make_faith_name(breakaway, rng),
            breakaway_doctrine = breakaway,
            support            = rng.randint(25, 45),
        )
        SCHISMS[faith.faith_id] = crisis
        faith.posture = "schism"
        _push_religion_news(day,
                            f"Schism in {faith.name}: a breakaway calling "
                            f"itself {crisis.breakaway_name} gathers followers.")


def _alt_doctrine(doctrine: str, rng: random.Random) -> str:
    """Pick a plausible adjacent doctrine for a breakaway. Avoids returning
    the original."""
    alt_map = {
        "martial":     ["zealous", "ascetic", "mystic"],
        "ascetic":     ["mystic", "scholarly"],
        "mercantile":  ["scholarly", "naturalist"],
        "naturalist":  ["mystic", "ascetic"],
        "scholarly":   ["mystic", "ascetic"],
        "mystic":      ["ascetic", "naturalist"],
    }
    pool = [d for d in alt_map.get(doctrine, ["ascetic"])
            if d in FAITH_DOCTRINES and d != doctrine]
    if not pool:
        pool = [d for d in FAITH_DOCTRINES if d != doctrine]
    return rng.choice(pool)


def _resolve_schisms(day: int) -> None:
    """After SCHISM_RESOLVE_DAYS the crisis snaps. Outcomes:
       * support ≥ 60: split — breakaway becomes a real faith taking a
         slice of adherence; original loses prestige + piety.
       * support 30..60: reunited — orthodoxy restored, scandal added.
       * support < 30: purged — the breakaway is crushed; zeal spike."""
    for fid, crisis in list(SCHISMS.items()):
        if crisis.resolved:
            continue
        if day - crisis.crisis_started_day < SCHISM_RESOLVE_DAYS:
            continue
        faith = FAITH_STATES.get(fid)
        if faith is None:
            crisis.resolved = True
            continue
        rng = random.Random((fid * 4099) ^ day ^ 0xBABE)
        if crisis.support >= 60:
            crisis.outcome = "split"
            new_faith = _spawn_breakaway_faith(faith, crisis, rng)
            _apply_reaction(faith,
                            {"piety": -12, "orthodoxy": +5, "scandal": +8},
                            day)
            _push_religion_news(day,
                                f"{faith.name} splits — {new_faith.name} "
                                f"breaks away.")
        elif crisis.support >= 30:
            crisis.outcome = "reunited"
            _apply_reaction(faith,
                            {"orthodoxy": +15, "scandal": +5,
                             "piety": -3},
                            day)
            _push_religion_news(day,
                                f"{faith.name} reunites under "
                                f"{faith.head_title} {faith.head_name}.")
        else:
            crisis.outcome = "purged"
            _apply_reaction(faith,
                            {"zeal": +10, "scandal": +3, "piety": +2,
                             "orthodoxy": +8},
                            day)
            _push_religion_news(day,
                                f"{faith.name} crushes the {crisis.breakaway_name} "
                                f"breakaway.")
        crisis.resolved = True
        faith.posture = _compute_posture(faith)


def _spawn_breakaway_faith(parent: FaithState, crisis: "SchismState",
                            rng: random.Random) -> FaithState:
    """Materialize the breakaway as a new FaithState taking ~30% of the
    parent's adherence in each region."""
    new = _create_faith(crisis.breakaway_doctrine, parent.biome_group, rng)
    new.name = crisis.breakaway_name
    new.piety     = max(20, parent.piety - 10)
    new.orthodoxy = 70  # fresh start
    new.zeal      = max(30, parent.zeal + 10)
    # Slice adherence from parent regions
    parent_adh = FAITH_REGIONS.get(parent.faith_id, {})
    for rid, pct in list(parent_adh.items()):
        cut = max(5, pct // 3)
        parent_adh[rid] = max(0, pct - cut)
        FAITH_REGIONS[new.faith_id][rid] = cut
    return new


# ---------------------------------------------------------------------------
# News piggyback — religion entries land in the same Newswire UI as politics
# ---------------------------------------------------------------------------

def _push_religion_news(day: int, headline: str) -> None:
    try:
        import industry_events as ie
        ie._push_news(day, headline, "religion")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Daily tick
# ---------------------------------------------------------------------------

def tick_religion(world, player) -> None:
    """Daily religious tick. Idempotent within a day. Call after tick_politics
    so we can react to house scandals + guild events when those hooks land."""
    try:
        from towns import REGIONS
    except Exception:
        return
    if not REGIONS:
        return
    seed_faiths_for_world(world)
    day = getattr(world, "day_count", 0)

    # Cross-system reaction passes (depend on politics + guilds being ticked).
    _react_to_houses(day)
    _react_to_orders(day)
    _react_to_industry_events(day)

    # Heresy growth + auto-inquisitions for zealous faiths.
    _grow_heresy(day)
    for faith in list(FAITH_STATES.values()):
        _maybe_run_inquisition(faith, day)

    # Schism crises (open + resolve)
    _check_schisms(day)
    _resolve_schisms(day)

    # Per-faith drift / tithes / scandal decay / posture
    for faith in FAITH_STATES.values():
        _tick_drift(faith)
        _tick_tithes(faith)
        if faith.scandal > 0:
            faith.scandal = max(0, faith.scandal - 1)
        faith.posture = _compute_posture(faith)


# ---------------------------------------------------------------------------
# Persistence — pure serialization
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Player actions — return (ok, message, gold_cost). Caller deducts gold +
# logs results. Mirror politics.action_* shape so the UI dispatcher is
# consistent across both systems.
# ---------------------------------------------------------------------------

DONATE_RELIC_ITEMS    = ("votive_tablet", "philosophers_scroll", "olive_branch")
FUND_PILGRIMAGE_COST  = 250
ENDOW_CATHEDRAL_COST  = 1500
TITHE_BOYCOTT_PAYOUT  = 80


def _faith_at_outpost(op) -> "FaithState | None":
    try:
        from outposts import region_for_outpost
    except Exception:
        return None
    region = region_for_outpost(op)
    if region is None:
        return None
    return primary_faith_of(region.region_id)


def action_donate_relic(player, faith: FaithState, day: int) -> tuple[bool, str, int]:
    inv = getattr(player, "inventory", {})
    relic_key = next((k for k in DONATE_RELIC_ITEMS
                      if inv.get(k, 0) > 0), None)
    if relic_key is None:
        return (False, "Need a votive tablet, scroll, or olive branch.", 0)
    inv[relic_key] -= 1
    if inv[relic_key] <= 0:
        del inv[relic_key]
    _apply_reaction(faith, {"piety": +3, "treasury": +60}, day)
    add_standing(faith.faith_id, +12, "donated relic", day)
    rec = PLAYER_STANDING.get(faith.faith_id)
    if rec:
        rec.relics_donated += 1
    return (True, f"Donated a {relic_key.replace('_', ' ')}.", 0)


def action_fund_pilgrimage(player, faith: FaithState, day: int) -> tuple[bool, str, int]:
    money = getattr(player, "money", 0)
    if money < FUND_PILGRIMAGE_COST:
        return (False, f"Need {FUND_PILGRIMAGE_COST}g.", 0)
    _apply_reaction(faith, {"piety": +4, "zeal": +2}, day)
    add_standing(faith.faith_id, +8, "funded pilgrimage", day)
    rec = PLAYER_STANDING.get(faith.faith_id)
    if rec:
        rec.pilgrim_marks += 1
    return (True, "Pilgrimage funded — your name is sung at the shrine.",
            FUND_PILGRIMAGE_COST)


def action_confess(player, faith: FaithState, day: int) -> tuple[bool, str, int]:
    # Free; only effective if scandal > 0 OR player standing is negative.
    standing = get_standing(faith.faith_id)
    did_anything = False
    if faith.scandal > 0:
        _apply_reaction(faith, {"scandal": -1}, day)
        did_anything = True
    if standing < 0:
        add_standing(faith.faith_id, +3, "confession", day)
        did_anything = True
    if not did_anything:
        return (False, "Nothing weighs on the books — go in peace.", 0)
    return (True, "Confession accepted.", 0)


def action_endow_cathedral(player, faith: FaithState, day: int) -> tuple[bool, str, int]:
    money = getattr(player, "money", 0)
    if money < ENDOW_CATHEDRAL_COST:
        return (False, f"Need {ENDOW_CATHEDRAL_COST}g.", 0)
    _apply_reaction(faith,
                    {"piety": +5, "orthodoxy": +3, "treasury": +400},
                    day)
    add_standing(faith.faith_id, +25, "endowed cathedral", day)
    # Rival faiths take a scandal bump — hostile_to tag matches.
    profile = doctrine_profile(faith.doctrine)
    hostile_tags = set(profile.get("hostile_to", ()))
    for other in FAITH_STATES.values():
        if other.faith_id == faith.faith_id:
            continue
        other_doctrine_tags = (other.doctrine, _doctrine_tag(other.doctrine))
        if hostile_tags.intersection(other_doctrine_tags):
            _apply_reaction(other, {"scandal": +3}, day)
            log_faith_relation(faith.faith_id, other.faith_id, day,
                                "endowment",
                                f"Player endowed {faith.name} cathedral")
    return (True, f"{faith.name} cathedral endowed in your name.",
            ENDOW_CATHEDRAL_COST)


def action_accuse_heresy(player, faith: FaithState, day: int) -> tuple[bool, str, int]:
    """Target the nearest visited House to the faith — drops a scandal on
    it, lifts faith zeal. Risk: 25% chance the player gets implicated."""
    try:
        from politics import HOUSE_STATES, log_relation_reason
        from towns import REGIONS
    except Exception:
        return (False, "Politics not available.", 0)
    if get_standing(faith.faith_id) < 10:
        return (False, "You must be Faithful (+10) before accusing heresy.", 0)
    # Pick a region where this faith has adherence and a backing house.
    adh = FAITH_REGIONS.get(faith.faith_id, {})
    candidates = []
    for rid in adh:
        h = HOUSE_STATES.get(rid)
        if h is not None and rid in REGIONS:
            candidates.append((adh[rid], h, rid))
    if not candidates:
        return (False, "No House under this faith's reach to accuse.", 0)
    candidates.sort(key=lambda t: -t[0])
    _, target_house, target_rid = candidates[0]
    rng = random.Random((day << 4) ^ faith.faith_id ^ target_rid ^ 0xACE)
    if rng.random() < 0.25:
        # Backfires — player loses standing
        add_standing(faith.faith_id, -15, "accusation backfired", day)
        _apply_reaction(faith, {"scandal": +2}, day)
        return (True,
                f"The accusation was thrown back at you. Standing slipped.",
                0)
    target_house.scandal = min(100, target_house.scandal + 15)
    target_house.days_since_leak = 0
    _apply_reaction(faith, {"zeal": +3}, day)
    add_standing(faith.faith_id, +5, "accused heresy", day)
    try:
        log_relation_reason(target_rid, target_rid, day, "heresy_charge",
                            f"{faith.name} levied heresy charges")
    except Exception:
        pass
    return (True,
            f"Charges of heresy laid against {target_house.name}.", 0)


def action_tithe_boycott(player, faith: FaithState, day: int) -> tuple[bool, str, int]:
    """Refuse to tithe — pocket some gold, take a standing hit. Repeatable."""
    standing = get_standing(faith.faith_id)
    if standing <= -60:
        return (False, "You are already a Heretic in their eyes.", 0)
    add_standing(faith.faith_id, -12, "boycotted tithe", day)
    _apply_reaction(faith, {"treasury": -30, "piety": -1}, day)
    # Negative cost = payout to player
    return (True, f"You pocket {TITHE_BOYCOTT_PAYOUT}g but their gaze sours.",
            -TITHE_BOYCOTT_PAYOUT)


BACK_SCHISMATIC_COST    = 600
SPONSOR_INQUISITION_COST = 900


def action_back_schismatic(player, faith: FaithState, day: int) -> tuple[bool, str, int]:
    """Fund the breakaway during a schism crisis — boosts its support so
    the crisis is more likely to resolve as a split."""
    crisis = SCHISMS.get(faith.faith_id)
    if crisis is None or crisis.resolved:
        return (False, "No active schism in this faith.", 0)
    if getattr(player, "money", 0) < BACK_SCHISMATIC_COST:
        return (False, f"Need {BACK_SCHISMATIC_COST}g.", 0)
    crisis.support = min(100, crisis.support + 20)
    add_standing(faith.faith_id, -10, "backed schismatic", day)
    _push_religion_news(day,
                        f"Foreign gold props up the {crisis.breakaway_name} "
                        f"breakaway within {faith.name}.")
    return (True,
            f"{crisis.breakaway_name} support climbs (+20).",
            BACK_SCHISMATIC_COST)


def action_sponsor_inquisition(player, faith: FaithState, day: int) -> tuple[bool, str, int]:
    """Pay the faith to run an inquisition *now*, bypassing zeal/cooldown
    gates. Aggressive — bumps faith zeal and scandal."""
    if getattr(player, "money", 0) < SPONSOR_INQUISITION_COST:
        return (False, f"Need {SPONSOR_INQUISITION_COST}g.", 0)
    adh = FAITH_REGIONS.get(faith.faith_id, {})
    purged = 0
    for rid in adh:
        h = HERESY.get(rid, {}).get(faith.faith_id, 0)
        if h <= 0:
            continue
        _adjust_heresy(rid, faith.faith_id, -min(30, h))
        purged += 1
    if purged == 0:
        return (False,
                "No heresy to root out — your gold would be wasted.",
                0)
    _LAST_INQUISITION_DAY[faith.faith_id] = day
    _apply_reaction(faith,
                    {"piety": +3, "orthodoxy": +3,
                     "zeal": +5, "scandal": +3},
                    day)
    add_standing(faith.faith_id, +8, "sponsored inquisition", day)
    _push_religion_news(day,
                        f"At foreign urging, {faith.name} sweeps "
                        f"{purged} region{'s' if purged != 1 else ''} for heretics.")
    return (True,
            f"Inquisition runs across {purged} region"
            f"{'s' if purged != 1 else ''}.",
            SPONSOR_INQUISITION_COST)


# Action ID → (handler, label used in temple UI)
TEMPLE_ACTION_HANDLERS = {
    "Donate Relic":         action_donate_relic,
    "Fund Pilgrimage":      action_fund_pilgrimage,
    "Confess":              action_confess,
    "Endow Cathedral":      action_endow_cathedral,
    "Accuse Heresy":        action_accuse_heresy,
    "Tithe Boycott":        action_tithe_boycott,
    "Back Schismatic":      action_back_schismatic,
    "Sponsor Inquisition":  action_sponsor_inquisition,
}


def reset_registries() -> None:
    global _NEXT_FAITH_ID, _NEWSWIRE_LAST_DAY
    FAITH_STATES.clear()
    FAITH_REGIONS.clear()
    CLERGY.clear()
    FAITH_RELATIONS.clear()
    FAITH_RELATION_REASONS.clear()
    SCHISMS.clear()
    HERESY.clear()
    PLAYER_STANDING.clear()
    _HOUSE_SCANDAL_SEEN.clear()
    _LAST_INQUISITION_DAY.clear()
    _NEXT_FAITH_ID = 1
    _NEWSWIRE_LAST_DAY = -1


def serialize_faiths() -> list:
    out = []
    for f in FAITH_STATES.values():
        out.append({
            "faith_id":   f.faith_id, "name": f.name, "doctrine": f.doctrine,
            "biome_group": f.biome_group,
            "piety":      f.piety, "orthodoxy": f.orthodoxy, "zeal": f.zeal,
            "treasury":   f.treasury, "scandal": f.scandal, "posture": f.posture,
            "head_id":    f.head_id, "head_name": f.head_name, "head_title": f.head_title,
            "last_event_day": f.last_event_day,
            "founded_year":      f.founded_year,
            "past_heads":        list(f.past_heads),
            "historical_events": list(f.historical_events),
        })
    return out


def deserialize_faiths(rows: list) -> None:
    global _NEXT_FAITH_ID
    for r in rows:
        f = FaithState(
            faith_id    = r["faith_id"], name = r["name"], doctrine = r["doctrine"],
            biome_group = r.get("biome_group", ""),
            piety       = r.get("piety", 50), orthodoxy = r.get("orthodoxy", 80),
            zeal        = r.get("zeal", 20), treasury = r.get("treasury", 0),
            scandal     = r.get("scandal", 0), posture = r.get("posture", "stable"),
            head_id     = r.get("head_id", 0),
            head_name   = r.get("head_name", ""), head_title = r.get("head_title", "Hierophant"),
            last_event_day    = r.get("last_event_day", -1),
            founded_year      = r.get("founded_year", 0),
            past_heads        = list(r.get("past_heads", [])),
            historical_events = list(r.get("historical_events", [])),
        )
        FAITH_STATES[f.faith_id] = f
        FAITH_REGIONS.setdefault(f.faith_id, {})
        _NEXT_FAITH_ID = max(_NEXT_FAITH_ID, f.faith_id + 1)
        # Back-fill history for faiths loaded from saves that pre-date it.
        if not f.historical_events:
            rng = random.Random((f.faith_id * 991) ^ 0xF411)
            _build_faith_history(f, rng)


def serialize_faith_regions() -> list:
    out = []
    for fid, regions in FAITH_REGIONS.items():
        for rid, adh in regions.items():
            out.append({"faith_id": fid, "region_id": rid, "adherence": adh})
    return out


def deserialize_faith_regions(rows: list) -> None:
    for r in rows:
        FAITH_REGIONS.setdefault(r["faith_id"], {})[r["region_id"]] = int(r["adherence"])


def serialize_clergy() -> list:
    out = []
    for c in CLERGY.values():
        out.append({
            "region_id": c.region_id, "faith_id": c.faith_id,
            "bishop_name": c.bishop_name, "bishop_title": c.bishop_title,
            "posture": c.posture, "abbots": list(c.abbots),
            "next_conclave_year": c.next_conclave_year,
        })
    return out


def deserialize_clergy(rows: list) -> None:
    for r in rows:
        c = RegionalClergy(
            region_id   = r["region_id"], faith_id = r["faith_id"],
            bishop_name = r.get("bishop_name", ""), bishop_title = r.get("bishop_title", "Bishop"),
            posture     = r.get("posture", "loyal"),
            abbots      = list(r.get("abbots", [])),
            next_conclave_year = r.get("next_conclave_year", CONCLAVE_INTERVAL_YEARS),
        )
        CLERGY[c.region_id] = c


def serialize_faith_relations() -> list:
    return [{"a": a, "b": b, "score": s} for (a, b), s in FAITH_RELATIONS.items()]


def deserialize_faith_relations(rows: list) -> None:
    for r in rows:
        FAITH_RELATIONS[_pair_key(r["a"], r["b"])] = int(r["score"])


def serialize_standing() -> list:
    out = []
    for fid, rec in PLAYER_STANDING.items():
        out.append({
            "faith_id": fid, "standing": rec.standing,
            "pilgrim_marks": rec.pilgrim_marks,
            "relics_donated": rec.relics_donated,
            "log": rec.log[:200],
        })
    return out


def deserialize_standing(rows: list) -> None:
    for r in rows:
        PLAYER_STANDING[r["faith_id"]] = FaithStandingRecord(
            faith_id        = r["faith_id"],
            standing        = r.get("standing", 0),
            pilgrim_marks   = r.get("pilgrim_marks", 0),
            relics_donated  = r.get("relics_donated", 0),
            log             = list(r.get("log", [])),
        )


def serialize_schisms() -> list:
    out = []
    for s in SCHISMS.values():
        out.append({
            "faith_id": s.faith_id,
            "crisis_started_day": s.crisis_started_day,
            "breakaway_name": s.breakaway_name,
            "breakaway_doctrine": s.breakaway_doctrine,
            "support": s.support,
            "resolved": s.resolved,
            "outcome": s.outcome,
        })
    return out


def deserialize_schisms(rows: list) -> None:
    for r in rows:
        s = SchismState(
            faith_id           = r["faith_id"],
            crisis_started_day = r.get("crisis_started_day", 0),
            breakaway_name     = r.get("breakaway_name", ""),
            breakaway_doctrine = r.get("breakaway_doctrine", "ascetic"),
            support            = r.get("support", 30),
            resolved           = r.get("resolved", False),
            outcome            = r.get("outcome", ""),
        )
        SCHISMS[s.faith_id] = s


def serialize_heresy() -> list:
    out = []
    for rid, row in HERESY.items():
        for fid, pct in row.items():
            if pct > 0:
                out.append({"region_id": rid, "faith_id": fid, "pct": pct})
    return out


def deserialize_heresy(rows: list) -> None:
    for r in rows:
        HERESY.setdefault(r["region_id"], {})[r["faith_id"]] = int(r["pct"])
