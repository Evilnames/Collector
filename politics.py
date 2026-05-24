"""Politics & Dynasties — the connective tissue between regions, guilds,
knightly orders, and dynasty events.

Each towns.Region gets a HouseState capturing its ruling family's political
state (power, prestige, scandal, posture, treasury). A daily tick recomputes
power from backing guilds and orders, reads guild sabotage events to swing
inter-house relationships, and drives succession crises triggered by royal
deaths.

This module is intentionally thin: dynasty *names* and lineage trees still
come from npc_dynasty / world.plan; heraldry from heraldry.py; guild data
from guilds.py; order data from knightly_orders.py. We just track the live
political layer on top.

Pure data + tick logic. No pygame, no UI. Safe to import anywhere.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Registries — module-level singletons, mirror guilds.GUILDS / ORDERS pattern
# ---------------------------------------------------------------------------

HOUSE_STATES:     dict[int, "HouseState"]   = {}   # region_id -> state
RELATIONS_SCORE:  dict[tuple[int, int], int] = {}  # (min_rid, max_rid) -> -100..+100
RELATION_REASONS: dict[tuple[int, int], list] = {} # (min_rid, max_rid) -> [{"day","kind","note"}] last 8
PLAYER_INFLUENCE: dict[int, "InfluenceRecord"] = {}  # region_id -> record
SUCCESSION:       dict[int, "SuccessionState"] = {}  # region_id -> crisis
PLAYER_PLEDGES:   dict[int, int] = {}   # order_id -> region_id the player has pledged the order to
HOUSE_HEIRS:      dict[int, "HeirSlate"] = {}   # region_id -> current ruler + heir names (lazy, rotates yearly)
ENVOY_REPORTS:    dict[int, dict] = {}   # region_id -> {"day": d, "report": str}

# Recent guild sabotage log — drained by tick. Filled by industry_events hook.
_PENDING_SABOTAGE: list = []   # [{"day", "attacker_gid", "target_gid"}]

# Recent dynasty events log — drained by tick. Filled by dynasty_events hook.
_PENDING_DYNASTY: list = []    # [{"day", "kind", "region_id"}]

ALLIANCE_THRESHOLD = 30
RIVAL_THRESHOLD    = -30
POSTURE_DELTA      = 8     # +/- power-shift over the 7-day window to flip posture
CRISIS_RESOLVE_DAYS = 30
NEWSWIRE_LIMIT_PER_DAY = 2


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class HouseState:
    region_id: int
    name:      str = ""              # House surname pulled from dynasty data
    power:     int = 50              # 0..100 composite
    prestige:  int = 20              # 0..100
    treasury:  int = 0               # mirrors region wealth
    scandal:   int = 0               # 0..100
    posture:   str = "stable"        # stable | rising | declining | crisis
    power_history: list = field(default_factory=list)   # rolling [int] last 7
    days_since_leak: int = 999       # for scandal decay rate
    last_event_day:  int = -1


@dataclass
class InfluenceRecord:
    total: int = 0
    log:   list = field(default_factory=list)   # [{"day", "delta", "source"}]


@dataclass
class SuccessionState:
    region_id: int
    crisis_started_day: int
    contenders: list = field(default_factory=list)   # [{"name", "support", "player_backed", "trait"}]
    resolved: bool = False
    winner: str = ""


@dataclass
class HeirSlate:
    region_id: int
    rotation_year: int
    ruler_name: str = ""
    ruler_title: str = "Lord"
    heir_name:   str = ""
    heir_age:    int = 18


# Agenda → tick modifiers and color tint. Agendas come from towns.LEADER_AGENDAS.
AGENDA_PROFILES = {
    "martial":     {"power_drift": +0.4, "scandal_decay": 0,
                    "prestige_drift": 0, "treasury_mult": 1.00,
                    "tint": (200, 110, 90),  "epithet": "the Steel Hand"},
    "mercantile":  {"power_drift": 0,    "scandal_decay": 0,
                    "prestige_drift": -0.2, "treasury_mult": 1.05,
                    "tint": (210, 175, 90), "epithet": "the Coin Counter"},
    "pious":       {"power_drift": -0.1, "scandal_decay": 2,
                    "prestige_drift": +0.3, "treasury_mult": 0.98,
                    "tint": (180, 200, 220), "epithet": "the Devout"},
    "builder":     {"power_drift": +0.2, "scandal_decay": 0,
                    "prestige_drift": +0.1, "treasury_mult": 1.00,
                    "tint": (170, 160, 130), "epithet": "the Builder"},
    "scholarly":   {"power_drift": 0,    "scandal_decay": 1,
                    "prestige_drift": +0.4, "treasury_mult": 0.97,
                    "tint": (150, 175, 200), "epithet": "the Learned"},
    "hedonist":    {"power_drift": -0.2, "scandal_decay": -2,
                    "prestige_drift": +0.2, "treasury_mult": 1.02,
                    "tint": (220, 140, 175), "epithet": "the Reveler"},
}
_DEFAULT_AGENDA_PROFILE = {"power_drift": 0, "scandal_decay": 0,
                            "prestige_drift": 0, "treasury_mult": 1.0,
                            "tint": (150, 140, 120), "epithet": "the Cautious"}


def agenda_profile(agenda: str) -> dict:
    return AGENDA_PROFILES.get(agenda or "", _DEFAULT_AGENDA_PROFILE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pair_key(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def get_house(region_id: int) -> Optional[HouseState]:
    return HOUSE_STATES.get(region_id)


def get_relation_score(a: int, b: int) -> int:
    return RELATIONS_SCORE.get(_pair_key(a, b), 0)


def set_relation_score(a: int, b: int, score: int) -> None:
    if a == b:
        return
    RELATIONS_SCORE[_pair_key(a, b)] = max(-100, min(100, score))


def adjust_relation(a: int, b: int, delta: int) -> int:
    cur = get_relation_score(a, b)
    new = max(-100, min(100, cur + delta))
    set_relation_score(a, b, new)
    _sync_region_relations(a, b, new)
    return new


def _sync_region_relations(a: int, b: int, score: int) -> None:
    """Mirror our numeric score into the legacy Region.relations string fields
    so existing UI (rep screen list/map) keeps working without changes."""
    try:
        from towns import REGIONS
    except Exception:
        return
    ra = REGIONS.get(a)
    rb = REGIONS.get(b)
    if ra is None or rb is None:
        return
    if score >= ALLIANCE_THRESHOLD:
        ra.relations[b] = "allied";  rb.relations[a] = "allied"
    elif score <= RIVAL_THRESHOLD:
        ra.relations[b] = "rival";   rb.relations[a] = "rival"
    else:
        ra.relations.pop(b, None);   rb.relations.pop(a, None)


def log_relation_reason(a: int, b: int, day: int, kind: str, note: str) -> None:
    key = _pair_key(a, b)
    bucket = RELATION_REASONS.setdefault(key, [])
    bucket.insert(0, {"day": day, "kind": kind, "note": note})
    del bucket[8:]


def relation_reasons(a: int, b: int) -> list:
    return RELATION_REASONS.get(_pair_key(a, b), [])


# ---------------------------------------------------------------------------
# Heir / ruler name generation — deterministic, rotates yearly so dynasties
# feel like time is passing without polluting the save with NPC churn.
# ---------------------------------------------------------------------------

_FIRST_NAMES_BY_GROUP = {
    "forest":   ["Aldric","Bryn","Caelen","Eirin","Faelan","Gwen","Hadrian","Iona","Joren","Kerra","Lyra","Maren","Nyssa","Oren","Pyrrha","Roen","Selene","Talin","Una","Veyra"],
    "boreal":   ["Astrid","Bjorn","Eira","Halvar","Ingmar","Jora","Kjell","Liv","Magnus","Nils","Odd","Rune","Sigrid","Thora","Ulf","Vidar"],
    "jungle":   ["Akoya","Bemba","Calix","Dembe","Elima","Faraji","Gola","Itzal","Jelani","Kwame","Lela","Moyo","Nia","Obi","Pemba","Rasha","Sefu","Tafari","Ubiri","Wema"],
    "tropical": ["Akela","Coral","Drift","Eira","Halia","Iona","Kai","Lani","Maile","Noa","Oahe","Pali","Reki","Sora","Tane"],
    "mediterranean":["Adrastos","Calista","Demetra","Eudora","Fotis","Galen","Hera","Isio","Kalia","Lyander","Myron","Nikos","Orsa","Petros","Renata","Sappho","Theron","Vasiliki"],
    "coastal":  ["Alba","Brenn","Cael","Doria","Erran","Fenn","Gale","Helia","Iren","Jorel","Kestrel","Lyssa","Maris","Nyx","Orin","Pell","Rian","Sage"],
    "desert":   ["Adira","Bahir","Cymara","Daheb","Esha","Faruq","Ghadir","Hala","Ifrit","Jamil","Karima","Lubna","Malik","Nadira","Omar","Qabil","Rafa","Saba","Talib","Yasmin"],
    "steppe":   ["Altan","Bayar","Chuluun","Erdene","Ganbat","Khulan","Munkh","Naran","Oyun","Saran","Temujin","Ulzii","Yul","Bortei"],
    "east_asian":["Akiko","Botan","Daiki","Eiko","Hana","Isamu","Jun","Kenji","Lin","Mei","Nori","Ren","Sora","Tora","Umi","Yuki","Akane","Hiroto"],
    "levant":   ["Adin","Bashir","Dalia","Elam","Faisal","Hadar","Ilias","Jaffa","Karam","Layla","Maron","Naim","Petra","Rami","Suri","Tariq","Yara"],
    "wasteland":["Ash","Bone","Cinder","Dust","Ember","Grit","Hollow","Iron","Marrow","Nail","Quill","Rust","Slag","Tine","Vex"],
    "highlands":["Aren","Brock","Cair","Drust","Ewen","Faolan","Gareth","Heron","Idris","Jenna","Kerwin","Lachlan","Morag","Niall","Owain","Rowan","Shea","Tamhas"],
    "silk_road":["Anvar","Behram","Daler","Erkin","Farrukh","Gulnara","Hasan","Iskander","Jamshid","Khurshed","Maryam","Nuriya","Otabek","Parviz","Rustam","Sabira","Timur"],
    "arabia":   ["Adnan","Basma","Dunia","Faridah","Habib","Ishaq","Jamilah","Karim","Layan","Marwan","Nour","Rashid","Sahar","Talia","Yusuf","Zahra"],
    "persia":   ["Anahid","Bahram","Cyra","Darya","Esmir","Farzan","Goli","Hossein","Iraj","Jasmin","Kourosh","Leyla","Mahsa","Nima","Roya","Soraya","Tehran","Yasmin"],
    "south_asian":["Aarav","Bhavna","Chitra","Devak","Esha","Gauri","Harshal","Indira","Kavi","Lakshmi","Manas","Nisha","Pranay","Rohan","Shanti","Vikram"],
    "yunnan":   ["An","Bao","Chen","Daiyu","Feng","Hua","Jing","Lan","Mei","Niang","Ping","Qiu","Shun","Tao","Wei","Xia","Yan","Zhi"],
}
_DEFAULT_FIRST_NAMES = ["Aldric","Maren","Tirien","Veska","Oren","Lyra","Ezra","Brynn"]

_HEIR_TITLES = {
    "Lord":      "Heir-Apparent",
    "Lady":      "Heir-Apparent",
    "King":      "Crown Prince",
    "Queen":     "Crown Princess",
    "Khan":      "Tsedendash",
    "Shah":      "Shahzade",
    "Sultan":    "Sultan-Heir",
    "Maharaja":  "Yuvraj",
    "Doge":      "Dogaressa",
    "Emir":      "Emir-Designate",
}

_CONTENDER_TRAITS = [
    "the Bold", "the Cautious", "the Pious", "the Hungry",
    "the Quiet", "the Drunken", "the Iron-Willed", "the Foreign-Born",
    "the Scarred", "the Younger", "the Elder", "the Lame",
    "the Generous", "the Bastard", "the Lettered", "the Cruel",
]


def _first_name_pool(region) -> list:
    return _FIRST_NAMES_BY_GROUP.get(getattr(region, "biome_group", ""), _DEFAULT_FIRST_NAMES)


def get_heir_slate(region) -> "HeirSlate":
    """Return a stable ruler+heir for the current in-game year. Rotates each
    year so the dynasty visibly ages without us needing to persist anything."""
    rid = region.region_id
    # Year derived from world day_count is read by caller; we just need
    # something stable per call. We accept the *region* and look up the
    # current year via the HouseState's last_event_day // 365 (close enough).
    house = HOUSE_STATES.get(rid)
    year = (house.last_event_day // 365 if house and house.last_event_day >= 0 else 0)
    existing = HOUSE_HEIRS.get(rid)
    if existing is not None and existing.rotation_year == year:
        return existing
    rng = random.Random((rid * 9319) ^ (year * 0x12B9B0A1) ^ 0xACE1)
    pool = _first_name_pool(region)
    ruler = rng.choice(pool)
    heir  = rng.choice([n for n in pool if n != ruler] or pool)
    title = getattr(region, "leader_title", "Lord")
    slate = HeirSlate(
        region_id     = rid,
        rotation_year = year,
        ruler_name    = ruler,
        ruler_title   = title,
        heir_name     = heir,
        heir_age      = rng.randint(14, 32),
    )
    HOUSE_HEIRS[rid] = slate
    return slate


def get_influence(region_id: int) -> int:
    rec = PLAYER_INFLUENCE.get(region_id)
    return rec.total if rec else 0


def add_influence(region_id: int, delta: int, source: str, day: int) -> None:
    rec = PLAYER_INFLUENCE.setdefault(region_id, InfluenceRecord())
    rec.total = max(-200, min(200, rec.total + delta))
    rec.log.insert(0, {"day": day, "delta": delta, "source": source})
    del rec.log[200:]


def influence_tier(score: int) -> tuple[str, tuple]:
    if score >= 80:  return ("Power Behind the Throne", (220, 175, 40))
    if score >= 40:  return ("Court Favored",            (220, 200, 70))
    if score >= 10:  return ("Recognized",               (160, 200, 130))
    if score >= -10: return ("Unknown",                  (140, 130, 100))
    if score >= -40: return ("Frowned Upon",             (210, 140, 80))
    return ("Marked Enemy", (210, 80, 70))


# ---------------------------------------------------------------------------
# Derivations — runtime lookups, not stored
# ---------------------------------------------------------------------------

def backing_guilds(region_id: int) -> list:
    try:
        from guilds import GUILDS
    except Exception:
        return []
    return [g for g in GUILDS.values()
            if g.home_region_id == region_id and g.state == "active"]


def backing_orders(region_id: int) -> list:
    try:
        from knightly_orders import ORDERS
    except Exception:
        return []
    return [o for o in ORDERS.values() if o.home_region == region_id]


def region_of_guild(guild_id: str) -> Optional[int]:
    try:
        from guilds import GUILDS
    except Exception:
        return None
    g = GUILDS.get(guild_id)
    return g.home_region_id if g else None


# ---------------------------------------------------------------------------
# House seeding
# ---------------------------------------------------------------------------

def _house_name_for_region(region) -> str:
    """Try the worldgen plan first, then towns dynasty data, else fall back
    to '<RegionName> Dynasty'."""
    rid = region.region_id
    name = ""
    # 1. world.plan-backed dynasty (matches dynasty_events flow)
    try:
        import npc_dynasty as nd
        # generate_family_tree is deterministic; cached internally
        # signature: (region_id, world_seed) -> dict with 'house_name'
        for fn in ("get_house_name", "house_name_for", "generate_family_tree"):
            f = getattr(nd, fn, None)
            if f is None:
                continue
            try:
                result = f(rid, 0)
                if isinstance(result, str) and result:
                    name = result
                    break
                if isinstance(result, dict):
                    name = result.get("house_name", "") or result.get("name", "")
                    if name:
                        break
            except TypeError:
                pass
    except Exception:
        pass
    if not name:
        name = f"House of {region.name}"
    return name


def seed_house_for_region(region) -> HouseState:
    """Idempotent — returns existing if present."""
    existing = HOUSE_STATES.get(region.region_id)
    if existing is not None:
        return existing
    name = _house_name_for_region(region)
    # Seed power/prestige off region's wealth bucket so different regions
    # start visibly different.
    wealth = getattr(region, "wealth", "modest")
    base_power = {"poor": 35, "modest": 50, "rich": 65}.get(wealth, 50)
    base_treasury = {"poor": 800, "modest": 2500, "rich": 6000}.get(wealth, 2500)
    house = HouseState(
        region_id = region.region_id,
        name      = name,
        power     = base_power,
        prestige  = 20 + (10 if wealth == "rich" else 0),
        treasury  = base_treasury,
        scandal   = 0,
        posture   = "stable",
    )
    HOUSE_STATES[region.region_id] = house
    return house


def seed_all_houses() -> None:
    """Seed any region missing a house state. Safe to call on every load."""
    try:
        from towns import REGIONS
    except Exception:
        return
    for region in REGIONS.values():
        seed_house_for_region(region)


# ---------------------------------------------------------------------------
# Power score recompute
# ---------------------------------------------------------------------------

def _compute_power(house: HouseState) -> int:
    """0..100 composite. Treasury (40%) + backing guilds (30%) + orders (20%)
    + prestige (10%) - scandal."""
    rid = house.region_id
    # Treasury contribution — log-ish curve so wealth doesn't dominate
    t = house.treasury
    treasury_score = min(40, int((t ** 0.5) / 4))    # 1600g -> 10, 10000g -> 25, 40000g -> 50 capped
    # Guild backing
    guilds = backing_guilds(rid)
    guild_score = min(30, len(guilds) * 6 + sum(int(g.share_price) for g in guilds) // 50)
    # Order backing
    orders = backing_orders(rid)
    order_score = min(20, sum(o.prestige for o in orders) // 10)
    prestige_score = min(10, house.prestige // 10)
    raw = treasury_score + guild_score + order_score + prestige_score - house.scandal // 3
    return max(0, min(100, raw))


def _update_posture(house: HouseState) -> None:
    hist = house.power_history
    if len(hist) < 4:
        house.posture = "crisis" if house.scandal >= 60 else "stable"
        return
    delta = hist[-1] - hist[0]
    if house.scandal >= 60 or house.region_id in SUCCESSION and not SUCCESSION[house.region_id].resolved:
        house.posture = "crisis"
    elif delta >= POSTURE_DELTA:
        house.posture = "rising"
    elif delta <= -POSTURE_DELTA:
        house.posture = "declining"
    else:
        house.posture = "stable"


# ---------------------------------------------------------------------------
# Event hooks — called from industry_events / dynasty_events
# ---------------------------------------------------------------------------

def on_guild_sabotage(attacker_gid: str, target_gid: str, day: int) -> None:
    _PENDING_SABOTAGE.append({
        "day": day, "attacker_gid": attacker_gid, "target_gid": target_gid,
    })
    del _PENDING_SABOTAGE[200:]


def on_dynasty_event(kind: str, region_id: int, day: int) -> None:
    _PENDING_DYNASTY.append({"day": day, "kind": kind, "region_id": region_id})
    del _PENDING_DYNASTY[200:]


# ---------------------------------------------------------------------------
# Newswire — piggyback on industry_events.NEWSWIRE
# ---------------------------------------------------------------------------

def _push_news(day: int, headline: str, kind: str = "politics") -> None:
    try:
        import industry_events as ie
        ie._push_news(day, headline, kind)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Per-tick processing
# ---------------------------------------------------------------------------

def _process_sabotage(day: int, rng: random.Random) -> int:
    """Apply pending guild sabotage events to inter-house relations.
    Returns number of headlines emitted."""
    emitted = 0
    while _PENDING_SABOTAGE:
        ev = _PENDING_SABOTAGE.pop(0)
        a_rid = region_of_guild(ev["attacker_gid"])
        t_rid = region_of_guild(ev["target_gid"])
        if a_rid is None or t_rid is None or a_rid == t_rid:
            continue
        # Look up guild names so the reason log is readable.
        atk_name = tgt_name = ""
        try:
            from guilds import GUILDS as _G
            ga = _G.get(ev["attacker_gid"]); gt = _G.get(ev["target_gid"])
            atk_name = ga.name if ga else ev["attacker_gid"]
            tgt_name = gt.name if gt else ev["target_gid"]
        except Exception:
            atk_name = ev["attacker_gid"]; tgt_name = ev["target_gid"]
        new = adjust_relation(a_rid, t_rid, -5)
        log_relation_reason(a_rid, t_rid, day, "sabotage",
                            f"{atk_name} sabotaged {tgt_name}")
        # Flip into feud territory? Announce it with a quote-worthy headline.
        if new <= RIVAL_THRESHOLD and new > RIVAL_THRESHOLD - 5:
            a_house = HOUSE_STATES.get(a_rid)
            t_house = HOUSE_STATES.get(t_rid)
            if a_house and t_house and emitted < NEWSWIRE_LIMIT_PER_DAY:
                _push_news(day,
                           f"Feud declared: {a_house.name} vs {t_house.name} "
                           f"— {atk_name}'s hand traced in attacks on {tgt_name}.",
                           "politics")
                emitted += 1
    return emitted


def _process_dynasty(day: int, rng: random.Random) -> int:
    """Apply pending dynasty events to house state."""
    emitted = 0
    while _PENDING_DYNASTY:
        ev = _PENDING_DYNASTY.pop(0)
        rid = ev.get("region_id")
        kind = ev.get("kind", "")
        house = HOUSE_STATES.get(rid) if rid is not None else None
        if house is None:
            continue
        house.last_event_day = day
        if kind == "marriage" or kind == "royal_betrothal" or kind == "alliance_signed":
            # Try to pair with a random nearby house — if region has any visited
            # neighbor with relations score >= 0, marry them.
            try:
                from towns import REGIONS
            except Exception:
                REGIONS = {}
            candidates = [r for r in REGIONS.values()
                          if r.region_id != rid
                          and get_relation_score(rid, r.region_id) >= -10]
            if candidates:
                other = rng.choice(candidates)
                new = adjust_relation(rid, other.region_id, 25)
                other_house = HOUSE_STATES.get(other.region_id)
                # Name both spouses so headlines feel personal
                slate_a = get_heir_slate(REGIONS[rid]) if rid in REGIONS else None
                slate_b = get_heir_slate(other) if other else None
                groom = slate_a.heir_name if slate_a else "the heir"
                bride = slate_b.heir_name if slate_b else "their heir"
                log_relation_reason(rid, other.region_id, day, "marriage",
                                    f"{groom} of {house.name} weds {bride}")
                if other_house and emitted < NEWSWIRE_LIMIT_PER_DAY:
                    _push_news(day,
                               f"Wedding bells: {groom} of {house.name} weds "
                               f"{bride} of {other_house.name}.",
                               "politics")
                    emitted += 1
            house.prestige = min(100, house.prestige + 4)
        elif kind == "coronation" or kind == "succession":
            house.prestige = min(100, house.prestige + 6)
            house.scandal  = max(0, house.scandal - 5)
        elif kind == "royal_death" or kind == "assassination_attempt":
            _trigger_crisis_if_unstable(rid, day, rng)
        elif kind == "intrigue" or kind == "bastard_recognized":
            house.scandal = min(100, house.scandal + 10)
            house.days_since_leak = 0
        elif kind == "rebellion_quelled":
            house.power = min(100, house.power + 3)
            house.scandal = max(0, house.scandal - 8)
        elif kind == "tournament":
            house.prestige = min(100, house.prestige + 2)
        elif kind == "plague_at_court":
            house.power = max(0, house.power - 5)
            house.scandal = min(100, house.scandal + 5)
    return emitted


def _trigger_crisis_if_unstable(region_id: int, day: int, rng: random.Random) -> None:
    if region_id in SUCCESSION and not SUCCESSION[region_id].resolved:
        return
    house = HOUSE_STATES.get(region_id)
    if house is None:
        return
    # High scandal OR low power → contested succession
    contested = house.scandal >= 40 or house.power <= 35 or rng.random() < 0.30
    if not contested:
        return
    # Real names from the region's first-name pool, with epithet traits.
    try:
        from towns import REGIONS
        region = REGIONS.get(region_id)
    except Exception:
        region = None
    if region is None:
        return
    pool = _first_name_pool(region)
    n = rng.choice([2, 2, 3])
    used_names = set()
    used_traits = set()
    contenders = []
    for _ in range(n):
        first = rng.choice([p for p in pool if p not in used_names] or pool)
        used_names.add(first)
        trait = rng.choice([t for t in _CONTENDER_TRAITS if t not in used_traits]
                            or _CONTENDER_TRAITS)
        used_traits.add(trait)
        contenders.append({
            "name":          f"{first} {trait}",
            "support":       rng.randint(20, 60),
            "player_backed": False,
            "trait":         trait,
        })
    SUCCESSION[region_id] = SuccessionState(
        region_id = region_id,
        crisis_started_day = day,
        contenders = contenders,
    )
    house.posture = "crisis"
    names = ", ".join(c["name"] for c in contenders)
    _push_news(day,
               f"Succession crisis in {house.name}: {names} vie for the seat.",
               "politics")


def _resolve_crises(day: int, rng: random.Random) -> int:
    emitted = 0
    for rid, crisis in list(SUCCESSION.items()):
        if crisis.resolved:
            continue
        elapsed = day - crisis.crisis_started_day
        if elapsed < CRISIS_RESOLVE_DAYS:
            continue
        house = HOUSE_STATES.get(rid)
        if house is None:
            crisis.resolved = True
            continue
        # Weighted pick — support + player_backed bonus - scandal penalty
        weights = []
        for c in crisis.contenders:
            w = max(1, c["support"]) + (40 if c["player_backed"] else 0)
            weights.append(w)
        winner = rng.choices(crisis.contenders, weights=weights, k=1)[0]
        crisis.winner = winner["name"]
        crisis.resolved = True
        house.prestige = min(100, house.prestige + 8)
        house.scandal  = max(0, house.scandal - 15)
        house.posture  = "stable"
        if winner["player_backed"] and emitted < NEWSWIRE_LIMIT_PER_DAY:
            _push_news(day,
                       f"{house.name}: {winner['name']} ascends — backed by you.",
                       "scandal")
            emitted += 1
        elif emitted < NEWSWIRE_LIMIT_PER_DAY:
            _push_news(day,
                       f"{house.name}: {winner['name']} takes the seat.",
                       "politics")
            emitted += 1
    return emitted


def _decay_scandals(day: int) -> None:
    try:
        from towns import REGIONS as _R
    except Exception:
        _R = {}
    for house in HOUSE_STATES.values():
        house.days_since_leak += 1
        if house.scandal <= 0:
            continue
        agenda  = getattr(_R.get(house.region_id), "agenda", "") if _R else ""
        profile = agenda_profile(agenda)
        # Pious heal scandal faster; hedonist heals slower (negative bonus).
        decay = (1 if house.days_since_leak < 5 else 3) + profile["scandal_decay"]
        if decay < 0:
            decay = 0
        house.scandal = max(0, house.scandal - decay)


# ---------------------------------------------------------------------------
# Public daily tick
# ---------------------------------------------------------------------------

def tick_politics(world, player) -> None:
    """Daily political tick. Idempotent within a day; uses world.day_count as
    its drive. Safe to call after towns/guilds/orders have ticked."""
    try:
        from towns import REGIONS
    except Exception:
        return
    if not REGIONS:
        return
    seed_all_houses()
    day = getattr(world, "day_count", 0)
    rng = random.Random((getattr(world, "seed", 0) ^ (day * 0x12345)) & 0xFFFFFFFF)

    # 1. Recompute power scores + apply agenda drifts + bankruptcy check
    try:
        from towns import REGIONS as _R
    except Exception:
        _R = {}
    for house in HOUSE_STATES.values():
        region   = _R.get(house.region_id)
        agenda   = getattr(region, "agenda", "") if region else ""
        profile  = agenda_profile(agenda)
        # Treasury: tax + agenda multiplier - upkeep
        guilds = backing_guilds(house.region_id)
        tax = int(sum(g.treasury for g in guilds) * 0.005 * profile["treasury_mult"])
        house.treasury = max(0, house.treasury + tax - 50)
        # Bankruptcy: empty coffers force a decline
        if house.treasury <= 0:
            house.scandal = min(100, house.scandal + 1)
            house.posture = "declining"
            if day - house.last_event_day > 14:
                _push_news(day,
                           f"{house.name} cannot pay its courtiers — coffers run dry.",
                           "scandal")
                house.last_event_day = day
        # Weekly drift from agenda (apply 1/7 each tick so it accumulates)
        house.power    = max(0, min(100, house.power + profile["power_drift"] / 7))
        # Natural prestige drift: agenda-flavored, with a slow baseline decay
        # so old houses fade unless they keep doing things.
        drift = profile["prestige_drift"] / 7 - 0.05
        house.prestige = max(0, min(100, house.prestige + drift))
        new_power = _compute_power(house)
        house.power = new_power
        house.power_history.append(new_power)
        if len(house.power_history) > 7:
            house.power_history.pop(0)
        _update_posture(house)

    # 2. Process pending sabotage → relationship shifts
    emitted = _process_sabotage(day, rng)

    # 3. Process pending dynasty events
    emitted += _process_dynasty(day, rng)

    # 4. Resolve succession crises that have aged out
    _resolve_crises(day, rng)

    # 5. Decay scandals
    _decay_scandals(day)


# ---------------------------------------------------------------------------
# Player actions — return (ok, message, gold_cost). Caller deducts gold.
# ---------------------------------------------------------------------------

BRIBE_BASE_COST = 200
SPONSOR_HEIR_COST = 1000
BROKER_MARRIAGE_COST = 500
FUND_RIVALRY_COST = 800
LEAK_SCANDAL_BASE_COST = 0
SPREAD_RUMOR_COST = 100
ENDOW_MONASTERY_COST = 1500
ARRANGE_TOURNAMENT_COST = 800
SEND_ENVOY_COST = 200
DEMAND_HOSTAGE_COST = 0   # only requires Court Favored standing


# ---------------------------------------------------------------------------
# Power breakdown — for the deep panel. Decomposes the same formula as
# _compute_power so the UI can show "+18 guilds, +12 treasury, ...".
# ---------------------------------------------------------------------------

def power_breakdown(region_id: int) -> dict:
    house = HOUSE_STATES.get(region_id)
    if house is None:
        return {}
    rid = region_id
    t = house.treasury
    treasury_score = min(40, int((t ** 0.5) / 4))
    guilds = backing_guilds(rid)
    guild_score = min(30, len(guilds) * 6 + sum(int(g.share_price) for g in guilds) // 50)
    orders = backing_orders(rid)
    order_score = min(20, sum(o.prestige for o in orders) // 10)
    prestige_score = int(min(10, house.prestige // 10))
    scandal_pen = int(house.scandal // 3)
    total = int(treasury_score + guild_score + order_score + prestige_score - scandal_pen)
    return {
        "treasury":      int(treasury_score),
        "guilds":        int(guild_score),
        "orders":        int(order_score),
        "prestige":      prestige_score,
        "scandal_pen":   scandal_pen,
        "n_guilds":      len(guilds),
        "n_orders":      len(orders),
        "total":         max(0, total),
    }


def action_bribe_official(player, region_id: int, day: int) -> tuple[bool, str, int]:
    house = HOUSE_STATES.get(region_id)
    if house is None:
        return (False, "No ruling house here.", 0)
    cost = BRIBE_BASE_COST + house.power * 12
    money = getattr(player, "money", 0)
    if money < cost:
        return (False, f"Need {cost}g.", 0)
    delta = 8 + (5 if house.power < 50 else 0)
    add_influence(region_id, delta, "bribe", day)
    # Risk: 20% scandal +10 if caught — applied to house, not player.
    rng = random.Random((day << 8) ^ region_id ^ 0xB1)
    if rng.random() < 0.20:
        house.scandal = min(100, house.scandal + 10)
        house.days_since_leak = 0
        _push_news(day, f"{house.name}: bribery scandal whispered at court.", "scandal")
    return (True, f"Bribed {house.name} courtiers (+{delta} influence).", cost)


def action_sponsor_heir(player, region_id: int, day: int) -> tuple[bool, str, int]:
    crisis = SUCCESSION.get(region_id)
    if crisis is None or crisis.resolved:
        return (False, "No active succession crisis here.", 0)
    if getattr(player, "money", 0) < SPONSOR_HEIR_COST:
        return (False, f"Need {SPONSOR_HEIR_COST}g.", 0)
    # Require a dynasty heirloom in inventory (spent as the gift)
    inv = getattr(player, "inventory", {})
    heirloom_key = None
    for k in inv:
        if isinstance(k, str) and k.startswith("dynasty_heir"):
            heirloom_key = k
            break
    if heirloom_key is None:
        return (False, "Need a dynasty heir-token in your inventory.", 0)
    inv[heirloom_key] = max(0, inv[heirloom_key] - 1)
    if inv[heirloom_key] == 0:
        del inv[heirloom_key]
    # Back the strongest unbacked contender
    target = None
    for c in crisis.contenders:
        if not c["player_backed"]:
            target = c
            break
    if target is None:
        target = crisis.contenders[0]
    target["player_backed"] = True
    add_influence(region_id, 20, "sponsored heir", day)
    house = HOUSE_STATES.get(region_id)
    if house:
        _push_news(day,
                   f"Whispers in {house.name}: a foreign patron backs {target['name']}.",
                   "politics")
    return (True, f"Sponsored {target['name']}.", SPONSOR_HEIR_COST)


def action_broker_marriage(player, region_a: int, region_b: int, day: int) -> tuple[bool, str, int]:
    if region_a == region_b:
        return (False, "Can't marry a house to itself.", 0)
    ha = HOUSE_STATES.get(region_a); hb = HOUSE_STATES.get(region_b)
    if ha is None or hb is None:
        return (False, "Both houses must exist.", 0)
    if get_influence(region_a) < 20 or get_influence(region_b) < 20:
        return (False, "Need at least Recognized standing in both houses.", 0)
    if get_relation_score(region_a, region_b) < RIVAL_THRESHOLD:
        return (False, "Houses are in open feud — too poisoned to marry.", 0)
    if getattr(player, "money", 0) < BROKER_MARRIAGE_COST:
        return (False, f"Need {BROKER_MARRIAGE_COST}g.", 0)
    new = adjust_relation(region_a, region_b, 35)
    ha.prestige = min(100, ha.prestige + 4)
    hb.prestige = min(100, hb.prestige + 4)
    add_influence(region_a, 10, "brokered marriage", day)
    add_influence(region_b, 10, "brokered marriage", day)
    _push_news(day,
               f"Marriage brokered: {ha.name} and {hb.name} pledge their heirs.",
               "politics")
    return (True, f"Alliance: {ha.name} ↔ {hb.name} ({new:+d}).", BROKER_MARRIAGE_COST)


def action_fund_rivalry(player, attacker_region: int, target_region: int, day: int) -> tuple[bool, str, int]:
    if attacker_region == target_region:
        return (False, "Pick two different regions.", 0)
    ha = HOUSE_STATES.get(attacker_region); ht = HOUSE_STATES.get(target_region)
    if ha is None or ht is None:
        return (False, "Both houses must exist.", 0)
    if getattr(player, "money", 0) < FUND_RIVALRY_COST:
        return (False, f"Need {FUND_RIVALRY_COST}g.", 0)
    # Find a guild we can buff to do the sabotage
    atk_guilds = backing_guilds(attacker_region)
    if not atk_guilds:
        return (False, f"{ha.name} has no guild to weaponize.", 0)
    g = atk_guilds[0]
    # Boost: append a 7-day "war chest" effect that doubles their sabotage roll
    g.active_effects.append({
        "event_key": "war_chest",
        "mult":      1.10,
        "days_left": 7,
        "note":      "Player war chest",
        "source":    "player",
    })
    adjust_relation(attacker_region, target_region, -10)
    rng = random.Random((day << 4) ^ attacker_region ^ target_region ^ 0xC2)
    if rng.random() < 0.15:
        ha.scandal = min(100, ha.scandal + 15)
        ha.days_since_leak = 0
        _push_news(day, f"{ha.name}: foreign coin traced in sabotage funds.", "scandal")
    else:
        _push_news(day,
                   f"{ha.name}'s {g.name} flush with new coin; rivals nervous.",
                   "politics")
    return (True, f"Funded {g.name} for 7 days.", FUND_RIVALRY_COST)


def action_leak_scandal(player, region_id: int, day: int) -> tuple[bool, str, int]:
    house = HOUSE_STATES.get(region_id)
    if house is None:
        return (False, "No ruling house here.", 0)
    # Spend a heirloom belonging to this house's event pool as evidence
    inv = getattr(player, "inventory", {})
    evidence_key = None
    for k in inv:
        if isinstance(k, str) and k.startswith("dynasty_") and inv[k] > 0:
            evidence_key = k
            break
    if evidence_key is None:
        return (False, "Need a dynasty heirloom or letter as evidence.", 0)
    inv[evidence_key] -= 1
    if inv[evidence_key] <= 0:
        del inv[evidence_key]
    house.scandal = min(100, house.scandal + 30)
    house.days_since_leak = 0
    house.power = max(0, house.power - 10)
    add_influence(region_id, -15, "leaked scandal", day)
    _push_news(day,
               f"Scandal at {house.name}: damning evidence surfaces.",
               "scandal")
    return (True, f"{house.name} scandal +30, power -10.", 0)


def action_pledge_order(player, order_id: int, region_id: int, day: int) -> tuple[bool, str, int]:
    """Shift a knightly order's alignment toward a house. Locks player out of
    rival orders in this region (lightly enforced by the UI)."""
    try:
        from knightly_orders import ORDERS
    except Exception:
        return (False, "Orders unavailable.", 0)
    order = ORDERS.get(order_id)
    house = HOUSE_STATES.get(region_id)
    if order is None or house is None:
        return (False, "Invalid order or house.", 0)
    PLAYER_PLEDGES[order_id] = region_id
    # Mark sworn alignment in existing kingdom_alignment dict
    order.kingdom_alignment = order.kingdom_alignment or {}
    order.kingdom_alignment[region_id] = "sworn"
    house.prestige = min(100, house.prestige + 5)
    add_influence(region_id, 10, "pledged order", day)
    _push_news(day,
               f"{order.name} pledges its lances to {house.name}.",
               "politics")
    return (True, f"{order.name} now sworn to {house.name}.", 0)


def action_spread_rumor(player, region_id: int, day: int) -> tuple[bool, str, int]:
    """Cheap, low-risk leak — small scandal, no evidence needed."""
    house = HOUSE_STATES.get(region_id)
    if house is None:
        return (False, "No ruling house here.", 0)
    if getattr(player, "money", 0) < SPREAD_RUMOR_COST:
        return (False, f"Need {SPREAD_RUMOR_COST}g.", 0)
    house.scandal = min(100, house.scandal + 5)
    house.days_since_leak = 0
    rng = random.Random((day << 6) ^ region_id ^ 0xD0)
    # Higher risk than bribe, but cheap. 30% chance the rumor traces back.
    if rng.random() < 0.30:
        add_influence(region_id, -8, "rumor traced back", day)
        _push_news(day,
                   f"{house.name}: court traces a slanderous rumor to a foreign coin.",
                   "scandal")
    else:
        _push_news(day,
                   f"{house.name}: tongues wag over {house.name.split()[-1]}'s court.",
                   "scandal")
    return (True, f"Rumor planted (+5 scandal).", SPREAD_RUMOR_COST)


def action_endow_monastery(player, region_id: int, day: int) -> tuple[bool, str, int]:
    """Pay to fund a regional monastery — big prestige boost, scandal washing,
    and a moderate influence gain. The pious agenda gets a bonus."""
    house = HOUSE_STATES.get(region_id)
    if house is None:
        return (False, "No ruling house here.", 0)
    if getattr(player, "money", 0) < ENDOW_MONASTERY_COST:
        return (False, f"Need {ENDOW_MONASTERY_COST}g.", 0)
    try:
        from towns import REGIONS
        region = REGIONS.get(region_id)
    except Exception:
        region = None
    profile = agenda_profile(getattr(region, "agenda", "") if region else "")
    prestige_gain = 8 + (4 if profile["scandal_decay"] > 0 else 0)
    house.prestige = min(100, house.prestige + prestige_gain)
    house.scandal  = max(0, house.scandal - 6)
    add_influence(region_id, 12, "endowed monastery", day)
    _push_news(day,
               f"{house.name} consecrates a new monastery — patron praised at court.",
               "politics")
    return (True, f"Monastery endowed (+{prestige_gain} prestige, -6 scandal).",
            ENDOW_MONASTERY_COST)


def action_arrange_tournament(player, region_id: int, day: int) -> tuple[bool, str, int]:
    """Sponsor a regional tournament. All orders in the region gain prestige;
    the house gains prestige; player gains standing."""
    house = HOUSE_STATES.get(region_id)
    if house is None:
        return (False, "No ruling house here.", 0)
    orders = backing_orders(region_id)
    if not orders:
        return (False, "No knightly orders in this region to ride.", 0)
    if getattr(player, "money", 0) < ARRANGE_TOURNAMENT_COST:
        return (False, f"Need {ARRANGE_TOURNAMENT_COST}g.", 0)
    for o in orders:
        o.prestige = min(100, o.prestige + 5)
    house.prestige = min(100, house.prestige + 6)
    add_influence(region_id, 10, "arranged tournament", day)
    names = ", ".join(o.name.split()[-1] for o in orders[:3])
    _push_news(day,
               f"{house.name} stages a grand tournament; {names} ride at your name.",
               "tournament")
    return (True, f"Tournament held — {len(orders)} orders +5 prestige.",
            ARRANGE_TOURNAMENT_COST)


def action_send_envoy(player, region_id: int, day: int) -> tuple[bool, str, int]:
    """Diplomatic visit — reveals hidden details (contender support breakdown,
    scandal recency, agenda profile, treasury vs upkeep). Persists a short
    report in ENVOY_REPORTS for the UI."""
    house = HOUSE_STATES.get(region_id)
    if house is None:
        return (False, "No ruling house here.", 0)
    if getattr(player, "money", 0) < SEND_ENVOY_COST:
        return (False, f"Need {SEND_ENVOY_COST}g.", 0)
    try:
        from towns import REGIONS
        region = REGIONS.get(region_id)
    except Exception:
        region = None
    profile = agenda_profile(getattr(region, "agenda", "") if region else "")
    parts = []
    parts.append(f"Agenda: {getattr(region, 'agenda', 'unknown').title() or 'Unknown'}; "
                 f"flavor — {profile['epithet']}.")
    parts.append(f"Treasury {house.treasury}g; net drift "
                 f"{'+' if profile['power_drift'] > 0 else ''}{profile['power_drift']:.1f}/wk.")
    crisis = SUCCESSION.get(region_id)
    if crisis and not crisis.resolved:
        slots = " · ".join(f"{c['name']}: {c['support']}" for c in crisis.contenders)
        parts.append(f"Crisis support — {slots}.")
    else:
        parts.append("No active succession crisis.")
    if house.days_since_leak < 14:
        parts.append(f"Last scandal: {house.days_since_leak}d ago.")
    report = " ".join(parts)
    ENVOY_REPORTS[region_id] = {"day": day, "report": report}
    add_influence(region_id, 3, "envoy visit", day)
    return (True, "Envoy report filed (see deep panel).", SEND_ENVOY_COST)


def action_demand_hostage(player, region_id: int, day: int) -> tuple[bool, str, int]:
    """Force +30 influence in one stroke — requires Court Favored standing
    already. One-time per region (consumed); causes -20 prestige to the house
    and adds a permanent feud-flavored relation note."""
    house = HOUSE_STATES.get(region_id)
    if house is None:
        return (False, "No ruling house here.", 0)
    if get_influence(region_id) < 40:
        return (False, "Need Court Favored standing (+40) first.", 0)
    # Check cooldown — once per 90 days
    rec = PLAYER_INFLUENCE.get(region_id)
    if rec:
        for entry in rec.log[:20]:
            if entry.get("source") == "demanded hostage" and day - entry["day"] < 90:
                return (False, "Already demanded a hostage recently.", 0)
    add_influence(region_id, 30, "demanded hostage", day)
    house.prestige = max(0, house.prestige - 20)
    house.scandal  = min(100, house.scandal + 5)
    _push_news(day,
               f"{house.name} surrenders a noble hostage to a foreign court.",
               "politics")
    return (True, "Hostage secured (+30 influence, house humbled).", 0)


# ---------------------------------------------------------------------------
# Persistence helpers — pure serialization
# ---------------------------------------------------------------------------

def reset_registries() -> None:
    HOUSE_STATES.clear()
    RELATIONS_SCORE.clear()
    RELATION_REASONS.clear()
    PLAYER_INFLUENCE.clear()
    SUCCESSION.clear()
    PLAYER_PLEDGES.clear()
    HOUSE_HEIRS.clear()
    ENVOY_REPORTS.clear()
    _PENDING_SABOTAGE.clear()
    _PENDING_DYNASTY.clear()


def serialize_houses() -> list:
    out = []
    for h in HOUSE_STATES.values():
        out.append({
            "region_id": h.region_id, "name": h.name,
            "power": h.power, "prestige": h.prestige,
            "treasury": h.treasury, "scandal": h.scandal,
            "posture": h.posture,
            "power_history": list(h.power_history),
            "days_since_leak": h.days_since_leak,
            "last_event_day": h.last_event_day,
        })
    return out


def deserialize_houses(rows: list) -> None:
    for r in rows:
        h = HouseState(
            region_id      = r["region_id"], name = r.get("name", ""),
            power          = r.get("power", 50), prestige = r.get("prestige", 20),
            treasury       = r.get("treasury", 0), scandal = r.get("scandal", 0),
            posture        = r.get("posture", "stable"),
            power_history  = list(r.get("power_history", [])),
            days_since_leak = r.get("days_since_leak", 999),
            last_event_day  = r.get("last_event_day", -1),
        )
        HOUSE_STATES[h.region_id] = h


def serialize_relations() -> list:
    return [{"a": a, "b": b, "score": s} for (a, b), s in RELATIONS_SCORE.items()]


def deserialize_relations(rows: list) -> None:
    for r in rows:
        RELATIONS_SCORE[_pair_key(r["a"], r["b"])] = int(r["score"])


def serialize_succession() -> list:
    out = []
    for s in SUCCESSION.values():
        out.append({
            "region_id": s.region_id,
            "crisis_started_day": s.crisis_started_day,
            "contenders": s.contenders,
            "resolved": s.resolved,
            "winner": s.winner,
        })
    return out


def deserialize_succession(rows: list) -> None:
    for r in rows:
        s = SuccessionState(
            region_id          = r["region_id"],
            crisis_started_day = r.get("crisis_started_day", 0),
            contenders         = r.get("contenders", []),
            resolved           = r.get("resolved", False),
            winner             = r.get("winner", ""),
        )
        SUCCESSION[s.region_id] = s


def serialize_influence() -> list:
    out = []
    for rid, rec in PLAYER_INFLUENCE.items():
        out.append({"region_id": rid, "total": rec.total, "log": rec.log[:200]})
    return out


def deserialize_influence(rows: list) -> None:
    for r in rows:
        PLAYER_INFLUENCE[r["region_id"]] = InfluenceRecord(
            total = r.get("total", 0),
            log   = list(r.get("log", [])),
        )


def serialize_pledges() -> dict:
    return {str(k): v for k, v in PLAYER_PLEDGES.items()}


def deserialize_pledges(d: dict) -> None:
    for k, v in d.items():
        PLAYER_PLEDGES[int(k)] = int(v)
