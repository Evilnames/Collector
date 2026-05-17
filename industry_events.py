"""Industry events + cross-guild rivalries.

A weekly stock-market tick rolls one industry-wide event and (separately) a
rivalry sabotage chance between guilds that already compete in the same
region+industry. Both modify `Guild.active_effects` — a small ribbon of dict
entries that decay each daily tick.

Each effect is `{event_key, mult, days_left, note, source}` where:
  - `mult` multiplies the guild's daily revenue (1.0 = no-op).
  - `days_left` decrements each daily tick; 0 → removed.
  - `note` is human-readable for the newswire log.
  - `source` is `"event"` or the rivaling guild_id.
"""

from guilds import (
    INDUSTRY_WINE, INDUSTRY_COFFEE, INDUSTRY_HERB, INDUSTRY_TEA,
    INDUSTRY_SPIRITS, INDUSTRY_BREW, INDUSTRY_POTTERY, INDUSTRY_TEXTILE,
    INDUSTRY_CHEESE, INDUSTRY_FISHING, INDUSTRY_SALT, INDUSTRY_OLIVE,
    INDUSTRY_SPICE, INDUSTRY_FORGE, INDUSTRY_TIMBER, INDUSTRY_FUR,
    INDUSTRY_APIARY, GUILDS,
)

# Each event spec: industries it targets, name, multiplier, duration in days.
EVENT_REGISTRY = [
    {"key": "frost",         "industries": [INDUSTRY_WINE, INDUSTRY_COFFEE, INDUSTRY_TEA, INDUSTRY_OLIVE],
     "name": "Frost",         "mult": 0.65, "days": 14, "weight": 6,
     "note": "Hard frost ruins yields across {industry}."},
    {"key": "gold_rush",     "industries": [INDUSTRY_FORGE],
     "name": "Gold Rush",     "mult": 1.40, "days": 14, "weight": 4,
     "note": "Gold rush sends {industry} commissions soaring."},
    {"key": "plague",        "industries": [INDUSTRY_HERB, INDUSTRY_APIARY],
     "name": "Plague",        "mult": 0.50, "days": 21, "weight": 3,
     "note": "Plague disrupts {industry} operations."},
    {"key": "bumper",        "industries": [INDUSTRY_COFFEE, INDUSTRY_TEA, INDUSTRY_APIARY, INDUSTRY_OLIVE, INDUSTRY_WINE],
     "name": "Bumper Harvest", "mult": 1.25, "days": 7, "weight": 6,
     "note": "{industry} celebrate a bumper harvest."},
    {"key": "embargo",       "industries": [INDUSTRY_SPICE, INDUSTRY_TEXTILE, INDUSTRY_SALT],
     "name": "Trade Embargo", "mult": 0.55, "days": 14, "weight": 4,
     "note": "Trade embargo throttles {industry}."},
    {"key": "strike",        "industries": [INDUSTRY_FORGE, INDUSTRY_TIMBER, INDUSTRY_POTTERY],
     "name": "Workers' Strike", "mult": 0.20, "days": 7, "weight": 3,
     "note": "Workers' strike halts {industry} output."},
    {"key": "festival",      "industries": [INDUSTRY_BREW, INDUSTRY_WINE, INDUSTRY_SPIRITS, INDUSTRY_APIARY],
     "name": "Regional Festival", "mult": 1.30, "days": 7, "weight": 6,
     "note": "Regional festivals drive demand for {industry}."},
    {"key": "shoal",         "industries": [INDUSTRY_FISHING],
     "name": "Massive Shoal", "mult": 1.50, "days": 7, "weight": 4,
     "note": "Massive shoal lifts {industry} hauls."},
    {"key": "drought",       "industries": [INDUSTRY_WINE, INDUSTRY_TEA, INDUSTRY_COFFEE, INDUSTRY_TEXTILE],
     "name": "Drought",       "mult": 0.70, "days": 14, "weight": 4,
     "note": "Drought withers {industry} output."},
    {"key": "fashion",       "industries": [INDUSTRY_TEXTILE, INDUSTRY_FUR],
     "name": "Fashion Boom",  "mult": 1.35, "days": 14, "weight": 3,
     "note": "Fashion boom inflates {industry} prices."},
]

NEWSWIRE_MAX = 20
NEWSWIRE: list = []     # newest first; each entry {day, headline, kind}


def roll_event(rng, day: int) -> dict | None:
    """Pick one event and apply it to every active guild in matching industries."""
    if not GUILDS:
        return None
    weights = [e["weight"] for e in EVENT_REGISTRY]
    spec = rng.choices(EVENT_REGISTRY, weights=weights, k=1)[0]
    industry = rng.choice(spec["industries"])
    affected = [g for g in GUILDS.values()
                if g.state == "active" and g.industry == industry]
    if not affected:
        return None
    for g in affected:
        g.active_effects.append({
            "event_key": spec["key"],
            "mult":      spec["mult"],
            "days_left": spec["days"],
            "note":      spec["name"],
            "source":    "event",
        })
    headline = spec["note"].format(industry=_industry_label(industry))
    _push_news(day, f"{spec['name']}: {headline}", "event")
    return spec


def roll_rivalries(rng, day: int) -> None:
    """Competing guilds (same industry + region) attempt sabotage on a rival.

    Triggers a sabotage attempt whenever multiple active guilds share an
    (industry, region_id); per attempt has ~25% success, applying a temporary
    debuff and naming-and-shaming in the newswire.
    """
    from guilds import CHAPTERS
    pairs: dict = {}
    for ch in CHAPTERS.values():
        g = GUILDS.get(ch.guild_id)
        if g is None or g.state != "active":
            continue
        pairs.setdefault((g.industry, ch.region_id), []).append(g)
    for competitors in pairs.values():
        if len(competitors) < 2:
            continue
        # Each competitor rolls one sabotage attempt this week.
        for attacker in competitors:
            rivals = [g for g in competitors if g.guild_id != attacker.guild_id]
            if not rivals:
                continue
            if rng.random() > 0.25:
                continue
            target = rng.choice(rivals)
            target.active_effects.append({
                "event_key": "sabotage",
                "mult":      0.70,
                "days_left": 5,
                "note":      "Sabotage",
                "source":    attacker.guild_id,
            })
            attacker.rivalry_target = target.guild_id
            _push_news(day,
                       f"{attacker.name} accused of sabotaging {target.name}.",
                       "rivalry")


def roll_tournament_day(rng, day: int) -> None:
    """Occasionally a tournament_grounds outpost hosts a tourney day.

    Fires a Newswire entry naming the region so the player knows to travel
    there. Doesn't gate the joust itself — visiting the marshal is always
    available — this just adds flavor + a heads-up.
    """
    if rng.random() > 0.30:
        return
    try:
        from outposts import OUTPOSTS, region_for_outpost
    except Exception:
        return
    tourney_ops = [op for op in OUTPOSTS.values()
                   if op.outpost_type == "tournament_grounds"]
    if not tourney_ops:
        return
    op = rng.choice(tourney_ops)
    region = region_for_outpost(op)
    rname = region.name if region else "the borderlands"
    _push_news(day, f"Tournament day at {op.name} ({rname}). Lances ride!",
               "tournament")


def daily_decay() -> None:
    """Decrement `days_left` on every guild's active_effects and drop expired."""
    for g in GUILDS.values():
        if not g.active_effects:
            continue
        kept = []
        for eff in g.active_effects:
            eff["days_left"] -= 1
            if eff["days_left"] > 0:
                kept.append(eff)
        g.active_effects = kept


def effect_multiplier(g) -> float:
    """Combined revenue multiplier from every active effect on a guild."""
    m = 1.0
    for eff in g.active_effects:
        m *= float(eff.get("mult", 1.0))
    return m


# ---------------------------------------------------------------------------
# Newswire
# ---------------------------------------------------------------------------

def _push_news(day: int, headline: str, kind: str) -> None:
    NEWSWIRE.insert(0, {"day": day, "headline": headline, "kind": kind})
    del NEWSWIRE[NEWSWIRE_MAX:]


def newswire_snapshot(limit: int = 10) -> list:
    return list(NEWSWIRE[:limit])


def clear_newswire() -> None:
    NEWSWIRE.clear()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _industry_label(industry: str) -> str:
    from guilds import INDUSTRY_DISPLAY
    return INDUSTRY_DISPLAY.get(industry, industry).lower()
