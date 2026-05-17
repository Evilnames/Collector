"""Per-guild economic backstory built from the historical chronicle.

Runs after ``simulate_history``. For each kingdom that survives long enough,
charters one guild per viable industry, then replays the chronicle year-by-year
generating an annual ledger row (treasury, share price, headcount, notable
event). Wars, plagues, sackings, kingdom splits, dynasty extinctions all
register against the local guild — so by the time the player loads the world,
each guild has centuries of track record they can read in the Stock Exchange
History tab.

The output is stashed on ``WorldPlan.guild_histories`` keyed
``"{kingdom_id}|{industry}"``. Consumed by ``guild_worldgen.seed_guilds``.
"""

import random
from dataclasses import asdict

from guilds import HistoricalYear, INDUSTRY_DISPLAY, OUTPOST_TYPE_TO_INDUSTRY


def _kingdom_industries(kingdom, settlements: dict, cells: list) -> set:
    """Mirror ``guild_worldgen._eager_seed_from_regions``: walk the kingdom's
    settlements, look up each one's biodome via the cell, then derive eligible
    industries from BIOME_OUTPOST_TYPES → OUTPOST_TYPE_TO_INDUSTRY.

    Importing outposts.BIOME_OUTPOST_TYPES inline keeps the import order stable
    (outposts.py depends on blocks.py which has its own side effects)."""
    from outposts import BIOME_OUTPOST_TYPES
    industries: set = set()
    seen_biomes: set = set()
    for sid in kingdom.member_settlement_ids:
        s = settlements.get(sid)
        if s is None or s.state != "alive":
            continue
        if 0 <= s.cell_index < len(cells):
            biodome = cells[s.cell_index].biodome
            if biodome in seen_biomes:
                continue
            seen_biomes.add(biodome)
            for outpost_type in BIOME_OUTPOST_TYPES.get(biodome, ()):
                industry = OUTPOST_TYPE_TO_INDUSTRY.get(outpost_type)
                if industry is not None:
                    industries.add(industry)
    return industries


# Notable-event reactions: chronicle event_kind -> (treasury_pct, price_pct,
# tag, prose_template). prose_template is .format()ed with `house` and
# `industry_display` and is what shows up in the Legendary Events panel.
_KIND_REACTIONS = {
    "sack":              (-0.55, -0.40, "sacked",         "The {industry_display} hall was put to the torch when {settlement} fell."),
    "earthquake":        (-0.30, -0.20, "earthquake",     "An earthquake cracked the {industry_display} warehouses; the cellars never quite recovered."),
    "plague":            (-0.25, -0.18, "plague",         "Plague carried off the senior masters; the rolls thinned for a generation."),
    "famine":            (-0.18, -0.10, "famine",         "A famine year saw the {industry_display} buy grain at any price."),
    "annex":             (-0.10, -0.08, "annexed",        "Annexation left the {industry_declined} of {house} under foreign charter."),
    "kingdom_collapse":  (-0.65, -0.55, "collapse",       "The crown fell. {house}'s {industry_display} were left without a charter."),
    "extinction":        (-0.30, -0.22, "founder_extinct","{house} went extinct; their {industry_display} drifted leaderless for years."),
    "succession_crisis": (-0.12, -0.08, "succession",     "A contested succession in {house} froze every guild ledger that season."),
    "alliance_form":     (+0.10, +0.08, "alliance_open",  "An alliance opened new markets to the {industry_display}."),
    "alliance_break":    (-0.08, -0.06, "alliance_break", "An alliance broke; trade caravans were turned back at the border."),
    "kingdom_split":     (-0.15, -0.12, "schism",         "When the realm split, a cadet branch of the {industry_display} broke off to charter their own."),
    "grow_to_tier":      (+0.08, +0.06, "boom",           "{settlement} grew, and orders poured into the {industry_display}."),
    "found_settlement":  (+0.04, +0.03, "new_market",     "A new settlement opened a fresh market for the {industry_display}."),
    "kingdom_reborn":    (+0.20, +0.15, "renewal",        "{house} took up the crown — masters returned and the {industry_display} flourished again."),
    "assassination":     (-0.10, -0.07, "intrigue",       "A blood-hand at court — the {industry_display} held their tongues and their gold."),
    "civil_war":         (-0.20, -0.16, "civil_war",      "Civil war split the masters between two banners."),
    "marriage":          (+0.03, +0.02, "wedding",        "A dynastic wedding brought a feast contract worth a year's takings."),
}


# ---------------------------------------------------------------------------
# Per-guild state during the sim
# ---------------------------------------------------------------------------

class _GuildSim:
    def __init__(self, kingdom_id, industry, biome_group,
                 founded_year, founder_name, founder_house, dynasty_id, rng):
        self.kingdom_id     = kingdom_id
        self.industry       = industry
        self.biome_group    = biome_group
        self.founded_year   = founded_year
        self.founder_name   = founder_name
        self.founder_house  = founder_house
        self.dynasty_id     = dynasty_id
        # Initial economic state: small cooperative, tiny treasury.
        self.treasury       = rng.randint(40, 120)
        self.share_price    = rng.uniform(5.0, 9.0)
        self.members        = 1
        self.profit_ema     = 0.0
        self.ledger:           list = []
        self.legendary_events: list = []
        self.defunct_year   = -1
        # Per-industry latent quality: 0.7..1.3 — a deterministic "house edge"
        # the player can only infer from the long-term trend.
        self.quality        = rng.uniform(0.75, 1.30)
        # Volatility tilt — some guilds are stable, others swing.
        self.volatility     = rng.uniform(0.05, 0.18)

    def annual_drift(self, year, rng):
        """One year of organic income. No event reactions here — those overlay."""
        # Slow upward drift × quality, plus volatile shocks.
        base = (8 + 4 * self.members) * self.quality
        shock = rng.gauss(0.0, self.volatility)
        income = int(round(base * (1.0 + shock)))
        self.treasury += income
        # Share price tracks a smoothed treasury, scaled to ~10g initial.
        target = max(1.0, (self.treasury / 50.0) ** 0.55 * self.quality * 3.0)
        self.share_price = self.share_price * 0.85 + target * 0.15
        # Occasional headcount growth (chapter founding).
        if rng.random() < 0.012 + 0.008 * max(0.0, self.profit_ema / 200.0):
            self.members += 1
        self.profit_ema = 0.9 * self.profit_ema + 0.1 * income
        self._snapshot(year, "", income)

    def react(self, year, kind, payload, rng):
        """React to a chronicle event landing this year on our kingdom."""
        rxn = _KIND_REACTIONS.get(kind)
        if rxn is None:
            return
        t_pct, p_pct, tag, prose = rxn
        self.treasury    = max(0, int(self.treasury * (1.0 + t_pct)))
        self.share_price = max(0.5, self.share_price * (1.0 + p_pct))
        # Tag the *current* year's ledger row (last one we wrote).
        if self.ledger:
            self.ledger[-1].event = tag
        # Add a prose line — capped to keep memory bounded.
        if len(self.legendary_events) < 8:
            try:
                line = prose.format(
                    house=self.founder_house or "the house",
                    industry_display=INDUSTRY_DISPLAY.get(self.industry, self.industry),
                    industry_declined=INDUSTRY_DISPLAY.get(self.industry, self.industry),
                    settlement=payload.get("settlement_name", "the capital"),
                )
            except Exception:
                line = prose
            self.legendary_events.append(f"Year {year}: {line}")
        # Kingdom collapse / extinction makes the guild defunct unless rescued.
        if kind in ("kingdom_collapse", "extinction"):
            if self.defunct_year == -1 and rng.random() < 0.65:
                # 35% of guilds survive a collapse by re-chartering. We can't
                # reach into the kingdom sim here; just flag dormancy.
                self.defunct_year = year

    def _snapshot(self, year, event_tag, income):
        self.ledger.append(HistoricalYear(
            year        = year,
            treasury    = int(self.treasury),
            share_price = round(self.share_price, 2),
            income      = int(income),
            members     = self.members,
            event       = event_tag,
        ))

    def to_dict(self):
        # Late-history profit summary feeds the runtime Guild's profit_ema and
        # last_week_profit so the market shows divergent recent performance.
        recent = self.ledger[-30:] if len(self.ledger) >= 30 else self.ledger
        recent_incomes = [row.income for row in recent if row.income > 0 or recent]
        recent_avg = (sum(r.income for r in recent) / max(1, len(recent))) if recent else 0.0
        return {
            "kingdom_id":        self.kingdom_id,
            "industry":          self.industry,
            "founded_year":      self.founded_year,
            "founder_name":      self.founder_name,
            "founder_house":     self.founder_house,
            "final_treasury":    int(self.treasury),
            "final_share_price": round(self.share_price, 2),
            "final_members":     self.members,
            "ledger":            [asdict(row) for row in self.ledger],
            "legendary_events":  list(self.legendary_events),
            "defunct_year":      self.defunct_year,
            "quality":           round(self.quality, 3),
            "recent_avg_income": round(recent_avg, 1),
        }


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------

def simulate_economy(seed: int, kingdoms: dict, dynasties: dict,
                     settlements: dict, cells: list,
                     chronicle_events: list, years: int) -> dict:
    """Walk the chronicle in year order and produce per-guild histories.

    Returns ``{"{kingdom_id}|{industry}": history_dict}`` ready to drop on
    ``WorldPlan.guild_histories``.
    """
    rng = random.Random(seed ^ 0xECC0_FEED)

    # 1) Charter guilds for every (kingdom, industry) viable in the kingdom's
    # actual settlements (same derivation runtime uses, so keys line up).
    guilds_sim: dict = {}
    for k in kingdoms.values():
        industries = _kingdom_industries(k, settlements, cells)
        if not industries:
            continue
        dyn = dynasties.get(k.dynasty_id)
        founder_name, founder_house, dynasty_id = _founder_for(dyn, rng)
        for industry in industries:
            charter_year = max(1, k.founded_year + rng.randint(5, 40))
            if charter_year >= years:
                continue
            key = f"{k.kingdom_id}|{industry}"
            guilds_sim[key] = _GuildSim(
                kingdom_id   = k.kingdom_id,
                industry     = industry,
                biome_group  = k.biome_group,
                founded_year = charter_year,
                founder_name = founder_name,
                founder_house = founder_house,
                dynasty_id   = dynasty_id,
                rng          = rng,
            )

    # 2) Index chronicle by year for O(N) replay.
    by_year: dict = {}
    for e in chronicle_events:
        by_year.setdefault(e.year, []).append(e)

    # 3) Walk years. Each guild ticks drift, then receives event reactions.
    for year in range(1, years + 1):
        # Annual drift first (so reactions land on top of the new row).
        for g in guilds_sim.values():
            if g.defunct_year != -1 or year < g.founded_year:
                continue
            g.annual_drift(year, rng)
        # Event reactions.
        for ev in by_year.get(year, ()):
            _route_event(ev, guilds_sim, settlements, kingdoms, rng)

    return {k: g.to_dict() for k, g in guilds_sim.items()}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _founder_for(dynasty, rng) -> tuple:
    """Pick a (name, house, dynasty_id) for a guild founded under this dynasty.

    Uses the dynasty's founder if available, otherwise a generated commoner
    so guilds that outlive their patron dynasty still have a backstory.
    """
    if dynasty is not None and dynasty.members:
        # Pick the founder member if alive in the dynasty record.
        founder = dynasty.members.get(dynasty.founder_id)
        if founder is not None:
            return (founder.name, dynasty.house_name, dynasty.dynasty_id)
    syl_a = ["Ber", "Cas", "Dor", "Eth", "Fyl", "Gra", "Hal", "Ire", "Jas", "Kor"]
    syl_b = ["en", "ar", "or", "ick", "as", "in", "ad", "yn", "us", "iel"]
    name  = rng.choice(syl_a) + rng.choice(syl_b)
    surname = "Old " + rng.choice(["Ovens", "Looms", "Anvils", "Vats", "Nets", "Hoes"])
    return (name, surname, -1)


def _route_event(ev, guilds_sim, settlements, kingdoms, rng):
    """Dispatch one chronicle event to every guild it touches."""
    kind = ev.kind
    actors = ev.actors or {}
    affected_kingdoms = _kingdoms_touched(actors)
    # Settlement-anchored events: include the settlement name in payload.
    payload = {}
    sid = actors.get("settlement") or actors.get("big") or actors.get("small")
    if sid is not None and sid in settlements:
        payload["settlement_name"] = settlements[sid].name
    elif ev.location_cell != -1:
        payload["settlement_name"] = f"the marches"
    else:
        payload["settlement_name"] = "the capital"
    for kid in affected_kingdoms:
        # Touch every industry guild in the affected kingdom.
        for key, g in guilds_sim.items():
            if g.kingdom_id != kid:
                continue
            if g.defunct_year != -1:
                continue
            if ev.year < g.founded_year:
                continue
            g.react(ev.year, kind, payload, rng)


def _kingdoms_touched(actors: dict) -> list:
    """Return the kingdom_ids implicated in an event."""
    out = []
    for key in ("kingdom", "attacker", "defender", "victor", "loser",
                "a", "b", "old_kingdom", "new_kingdom", "parent", "breakaway"):
        v = actors.get(key)
        if isinstance(v, int) and v >= 0:
            out.append(v)
    return list(dict.fromkeys(out))   # dedupe, preserve order
