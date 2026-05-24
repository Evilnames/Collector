"""Knightly Order <-> Guild patronage.

A knightly order in every region is sponsored by one of the regional guilds.
Tradition biases the match: Templars seek Forge/Masonry guilds, Cavaliers
court Vintners/Weavers, Hospitallers ally with Apothecaries/Tea, and so on.

What the link does at runtime:

  * Weekly patronage flow: a slice of the patron guild's treasury raises
    the order's prestige. A bankrupt or subsidiary patron lets prestige
    decay slowly until a new patron is found.
  * Industry-event echoes: when the patron has an active Phase-6 effect
    (frost, boom, plague, festival, fashion), the order feels it.
  * Rivalry propagation: a Phase-6 guild sabotage between two patrons
    makes their orders rivals (KnightlyOrder.rival_id).
  * Player perks: owning shares in an order's patron guild unlocks
    quartermaster discounts and a small prestige drip.

Pure logic, no pygame. Import-safe from stock_market.py and UI modules.
"""

import random
from typing import Optional

import guilds
import knightly_orders as ko


# ---------------------------------------------------------------------------
# Tradition -> industry affinity. First entries are stronger weights.
# Any guild in the region can still be picked as fallback; these just bias.
# ---------------------------------------------------------------------------

_TRADITION_INDUSTRY_AFFINITY: dict = {
    "errant":      ["timber", "fur", "apiary"],
    "templar":     ["forge", "masonry", "spice"],
    "hospitaller": ["herb", "tea", "apiary"],
    "cavalier":    ["wine", "textile", "olive"],
    "mercenary":   ["spirits", "mining", "brew"],
    "marcher":     ["timber", "fur", "carpentry"],
    "magisterial": ["pottery", "tea", "coffee"],
    "berserker":   ["brew", "fur", "mining"],
    "horde":       ["fur", "salt", "mining"],
    "cataphract":  ["forge", "masonry", "olive"],
    "bushi":       ["tea", "textile", "pottery"],
    "furusiyya":   ["spice", "textile", "wine"],
    "rajput":      ["spice", "textile", "forge"],
}

# Cap on weekly prestige gain from any single source.
_PATRONAGE_WEEKLY_CAP   = 4
# Treasury -> prestige conversion. 2000g treasury ~= +1 prestige/week.
_PATRONAGE_TREASURY_DIV = 2000
# Per-week decay if patron is bankrupt/subsidiary/missing.
_ORPHAN_DECAY           = 1
# Event-keyed prestige nudges. Mirrors industry_events.py keys.
_EVENT_PRESTIGE = {
    "bumper":    +1,
    "boom":      +1,
    "gold_rush": +2,
    "festival":  +1,
    "fashion":   +1,
    "frost":     -1,
    "plague":    -2,
    "drought":   -1,
    "embargo":   -1,
    "strike":    -1,
    "sabotage":  -1,
}

# Player share-stake discount tiers at the quartermaster.
_QM_DISCOUNT_TIERS = [
    (0.51, 0.25),   # >=51% -> 25% off
    (0.25, 0.15),   # >=25% -> 15% off
    (0.10, 0.10),   # >=10% -> 10% off
]


# ---------------------------------------------------------------------------
# Patron assignment
# ---------------------------------------------------------------------------

def _candidates_in_region(region_id: int) -> list:
    out = []
    for g in guilds.GUILDS.values():
        if g.home_region_id != region_id:
            continue
        if not g.state.startswith("active") and g.state != "active":
            continue
        out.append(g)
    return out


def _pick_patron(rng: random.Random, order, candidates: list):
    if not candidates:
        return None
    affinities = _TRADITION_INDUSTRY_AFFINITY.get(order.tradition, [])
    weighted = []
    for g in candidates:
        w = 1.0
        if g.industry in affinities:
            idx = affinities.index(g.industry)
            w += 4.0 - idx  # 4,3,2 ...
        weighted.append((w, g))
    total = sum(w for w, _ in weighted)
    r = rng.random() * total
    cum = 0.0
    for w, g in weighted:
        cum += w
        if r <= cum:
            return g
    return weighted[-1][1]


def assign_patrons(seed: int = 0) -> int:
    """Fill in `patron_guild_id` for every order that lacks one.

    Idempotent — safe to call every day. Returns the number of new
    assignments made.
    """
    assigned = 0
    for order in ko.ORDERS.values():
        current = getattr(order, "patron_guild_id", None)
        if current and current in guilds.GUILDS:
            g = guilds.GUILDS[current]
            if g.state == "active":
                continue
            order.patron_guild_id = None  # patron died; re-roll below
        cands = _candidates_in_region(order.home_region)
        if not cands:
            continue
        rng = random.Random((seed ^ order.order_id * 2654435761) & 0xFFFFFFFF)
        g = _pick_patron(rng, order, cands)
        if g is not None:
            order.patron_guild_id = g.guild_id
            assigned += 1
    return assigned


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------

def patron_guild_for(order_id: int):
    order = ko.ORDERS.get(order_id)
    if order is None:
        return None
    gid = getattr(order, "patron_guild_id", None)
    if not gid:
        return None
    return guilds.GUILDS.get(gid)


def order_patronized_by(guild_id: str):
    """Return the first order whose patron is `guild_id`, or None."""
    for o in ko.ORDERS.values():
        if getattr(o, "patron_guild_id", None) == guild_id:
            return o
    return None


def patron_display_name(order_id: int) -> str:
    g = patron_guild_for(order_id)
    if g is None:
        return "unsponsored"
    return g.name


# ---------------------------------------------------------------------------
# Weekly ticks (called from stock_market.tick_market)
# ---------------------------------------------------------------------------

def tick_patronage() -> None:
    """Patron treasury slowly props up its order's prestige."""
    for order in ko.ORDERS.values():
        g = patron_guild_for(order.order_id)
        if g is None or g.state != "active":
            # Orphans decay; floor at 0.
            order.prestige = max(0, order.prestige - _ORPHAN_DECAY)
            continue
        if g.treasury <= 0:
            continue
        bump = min(_PATRONAGE_WEEKLY_CAP, g.treasury // _PATRONAGE_TREASURY_DIV)
        if bump > 0:
            order.prestige = min(500, order.prestige + int(bump))


def industry_event_prestige() -> None:
    """Active industry events nudge patron orders up or down."""
    for order in ko.ORDERS.values():
        g = patron_guild_for(order.order_id)
        if g is None:
            continue
        for eff in getattr(g, "active_effects", []) or []:
            key = eff.get("event_key", "")
            delta = _EVENT_PRESTIGE.get(key, 0)
            if delta:
                order.prestige = max(0, min(500, order.prestige + delta))


def propagate_rivalries() -> None:
    """If two guilds with patron orders are rivals, make the orders rivals too."""
    for g in guilds.GUILDS.values():
        target_gid = getattr(g, "rivalry_target", None)
        if not target_gid:
            continue
        target_g = guilds.GUILDS.get(target_gid)
        if target_g is None:
            continue
        a = order_patronized_by(g.guild_id)
        b = order_patronized_by(target_g.guild_id)
        if a is None or b is None or a.order_id == b.order_id:
            continue
        a.rival_id = b.order_id
        b.rival_id = a.order_id


# ---------------------------------------------------------------------------
# Player perks
# ---------------------------------------------------------------------------

def player_patron_pct(order_id: int) -> float:
    g = patron_guild_for(order_id)
    if g is None:
        return 0.0
    return g.player_pct()


def quartermaster_discount(player) -> float:
    """Returns a 0.0-0.25 discount based on shares in the patron guild."""
    order_id = int(getattr(player, "order_id", 0) or 0)
    if order_id == 0:
        return 0.0
    pct = player_patron_pct(order_id)
    for floor, disc in _QM_DISCOUNT_TIERS:
        if pct >= floor:
            return disc
    return 0.0


def discounted_price(player, base_price: int) -> int:
    disc = quartermaster_discount(player)
    if disc <= 0.0:
        return base_price
    return max(1, int(round(base_price * (1.0 - disc))))


def patron_join_bonus(player) -> int:
    """Instant prestige bump applied when joining an order whose patron
    the player already owns shares in. Caller invokes once at petition."""
    order_id = int(getattr(player, "order_id", 0) or 0)
    if order_id == 0:
        return 0
    pct = player_patron_pct(order_id)
    if pct >= 0.51:
        return 12
    if pct >= 0.25:
        return 6
    if pct >= 0.10:
        return 3
    return 0
