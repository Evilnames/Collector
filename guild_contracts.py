"""Guild Contracts — procedural mission board hosted at each Guild Hall.

Layered on top of the existing stock-market sim ([[project-guilds]]). Each
active guild keeps a small roster of open contracts that the player can
accept and turn in for gold, per-guild reputation, and (rarely) a bonus
dividend payout.

Contract kinds:
  - "supply"  — bring N raw materials of the guild's industry to this hall.
                Completes at the originating Guild Hall.
  - "courier" — carry N finished goods to a DIFFERENT guild's hall (any
                guild outside the issuer's region). Completes at the
                target hall. Pays roughly double.

Persisted (save v10):
  - CONTRACTS registry → SQLite table `guild_contracts`.
  - player.guild_rep / player.active_contracts → columns on `player`.

Pure data + logic. Imports guilds + items but never pygame.
"""

import random
from dataclasses import dataclass, field
from typing import Optional

import guilds


# ---------------------------------------------------------------------------
# Industry → demand pools.
# Raw materials a guild plausibly wants supplied (kind="supply"), and
# finished goods that travel as couriered cargo (kind="courier").
# ---------------------------------------------------------------------------

INDUSTRY_SUPPLY_POOL: dict = {
    "wine":     ["grape_cluster", "grape_seed"],
    "coffee":   ["coffee_cherry", "coffee_seed"],
    "tea":      ["tea_leaf", "tea_seed"],
    "spirits":  ["wheat", "barley_seed", "rye_seed"],
    "brew":     ["hop_cluster", "wheat", "barley_seed"],
    "herb":     ["herb_root", "herb_leaf", "wild_garlic"],
    "pottery":  ["clay", "wood_ash", "lumber"],
    "textile":  ["wool", "flax_fiber", "cotton_fiber", "silk_thread"],
    "cheese":   ["milk", "salt", "wood_ash"],
    "fishing":  ["salt", "lumber", "flax_fiber"],
    "salt":     ["lumber", "clay"],
    "olive":    ["olive_oil", "salt"],
    "spice":    ["wild_garlic", "salt", "honey"],
    "forge":    ["iron_chunk", "coal", "lumber"],
    "timber":   ["lumber", "coal"],
    "fur":      ["leather", "salt", "lumber"],
    "apiary":   ["honey", "wax", "flax_fiber"],
    "mining":   ["lumber", "coal", "iron_chunk"],
    "masonry":  ["clay", "sandstone", "lumber"],
    "carpentry":["lumber", "iron_chunk"],
    "roofing":  ["clay", "lumber"],
}

INDUSTRY_COURIER_POOL: dict = {
    "wine":     ["wine_amphora", "wine_amphora_fine"],
    "coffee":   ["coffee_cherry"],
    "tea":      ["tea_leaf"],
    "spirits":  ["mead", "mead_fine"],
    "brew":     ["wheat_beer", "barleywine"],
    "herb":     ["herb_leaf", "herb_root"],
    "pottery":  ["clay_pot_item", "pottery_display"],
    "textile":  ["textile_rug_natural", "textile_rug_golden"],
    "cheese":   ["cheese"],
    "fishing":  ["raw_chicken"],
    "salt":     ["salt"],
    "olive":    ["olive_oil"],
    "spice":    ["honey"],
    "forge":    ["iron_pickaxe", "iron_axe"],
    "timber":   ["lumber"],
    "fur":      ["leather_dressing", "fur_trimmed_hood"],
    "apiary":   ["honey"],
    "mining":   ["coal", "iron_chunk", "gold_nugget"],
    "masonry":  ["sandstone_ashlar", "sandstone_column"],
    "carpentry":["lumber"],
    "roofing":  ["clay"],
}

# Tier table → (count_mult, gold_mult, rep_amount, ttl_days, kind_label).
# A roll picks one entry by weight.
TIERS = [
    ("standing",  3.0, 0.4, 6, 30, 1, "Standing Order"),
    ("normal",    1.0, 1.0, 1, 14, 6, "Open Contract"),
    ("urgent",    1.0, 1.6, 2,  4, 3, "Urgent"),
    ("bumper",    3.0, 2.2, 4,  6, 2, "Bumper Run"),
]
# index: (slug, count_mult, gold_mult, rep, ttl, weight, label)

CONTRACTS_PER_GUILD = 3
BASE_COUNT_PER_SUPPLY  = 8     # multiplied by tier count_mult
BASE_COUNT_PER_COURIER = 5
BASE_GOLD_PER_ITEM_SUPPLY  = 6
BASE_GOLD_PER_ITEM_COURIER = 14  # courier pays more per item


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

CONTRACTS: dict = {}    # contract_id -> Contract
_NEXT_CONTRACT_ID = 1


def reset_registries() -> None:
    global _NEXT_CONTRACT_ID
    CONTRACTS.clear()
    _NEXT_CONTRACT_ID = 1


@dataclass
class Contract:
    contract_id:     int
    guild_id:        str          # issuing guild
    kind:            str          # "supply" | "courier"
    tier:            str          # tier slug
    item_id:         str
    count:           int
    reward_gold:     int
    reward_rep:      int
    posted_day:      int
    expires_day:     int
    target_guild_id: Optional[str] = None   # courier destination
    target_label:    str = ""              # display name of destination
    state:           str = "open"           # open | accepted | completed | expired
    accepted_by:     str = ""               # "player" or ""

    @property
    def title(self) -> str:
        item_name = _item_name(self.item_id)
        if self.kind == "supply":
            return f"Supply {self.count}× {item_name}"
        return f"Courier {self.count}× {item_name} → {self.target_label}"

    @property
    def description(self) -> str:
        g = guilds.GUILDS.get(self.guild_id)
        gname = g.name if g else "the guild"
        if self.kind == "supply":
            return (f"{gname} needs {self.count} {_item_name(self.item_id)} "
                    f"delivered to this Hall.")
        return (f"{gname} is shipping {self.count} {_item_name(self.item_id)} "
                f"to {self.target_label}. Carry the cargo and turn it in "
                f"at the destination Hall.")


def _item_name(item_id: str) -> str:
    try:
        from items import ITEMS
        return ITEMS.get(item_id, {}).get("name", item_id)
    except Exception:
        return item_id


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def _new_id() -> int:
    global _NEXT_CONTRACT_ID
    cid = _NEXT_CONTRACT_ID
    _NEXT_CONTRACT_ID += 1
    return cid


def _pick_tier(rng: random.Random):
    weights = [t[5] for t in TIERS]
    return rng.choices(TIERS, weights=weights, k=1)[0]


def _gen_supply(g, rng: random.Random, day: int) -> Optional[Contract]:
    pool = INDUSTRY_SUPPLY_POOL.get(g.industry, [])
    if not pool:
        return None
    item_id = rng.choice(pool)
    tier = _pick_tier(rng)
    slug, cmult, gmult, rep, ttl = tier[0], tier[1], tier[2], tier[3], tier[4]
    count = max(1, int(BASE_COUNT_PER_SUPPLY * cmult))
    gold = int(count * BASE_GOLD_PER_ITEM_SUPPLY * gmult)
    return Contract(
        contract_id=_new_id(),
        guild_id=g.guild_id,
        kind="supply",
        tier=slug,
        item_id=item_id,
        count=count,
        reward_gold=gold,
        reward_rep=rep,
        posted_day=day,
        expires_day=day + ttl,
    )


def _pick_courier_target(g, rng: random.Random):
    candidates = [og for og in guilds.GUILDS.values()
                  if og.state == "active"
                  and og.guild_id != g.guild_id
                  and og.home_region_id != g.home_region_id]
    if not candidates:
        return None
    return rng.choice(candidates)


def _gen_courier(g, rng: random.Random, day: int) -> Optional[Contract]:
    pool = INDUSTRY_COURIER_POOL.get(g.industry, [])
    if not pool:
        return None
    target = _pick_courier_target(g, rng)
    if target is None:
        return None
    item_id = rng.choice(pool)
    tier = _pick_tier(rng)
    slug, cmult, gmult, rep, ttl = tier[0], tier[1], tier[2], tier[3], tier[4]
    count = max(1, int(BASE_COUNT_PER_COURIER * cmult))
    gold = int(count * BASE_GOLD_PER_ITEM_COURIER * gmult)
    return Contract(
        contract_id=_new_id(),
        guild_id=g.guild_id,
        kind="courier",
        tier=slug,
        item_id=item_id,
        count=count,
        reward_gold=gold,
        reward_rep=rep + 1,
        posted_day=day,
        expires_day=day + ttl,
        target_guild_id=target.guild_id,
        target_label=target.name,
    )


def _open_for_guild(gid: str) -> list:
    return [c for c in CONTRACTS.values()
            if c.guild_id == gid and c.state == "open"]


def refresh_contracts(world) -> int:
    """Drop expired, refill every active guild to CONTRACTS_PER_GUILD.

    Idempotent. Safe to call weekly from stock_market.tick_market. Returns
    count of newly-issued contracts.
    """
    day = getattr(world, "day_count", 0)
    seed = getattr(world, "seed", 0) or 0
    # 1) expire stale open contracts
    for c in list(CONTRACTS.values()):
        if c.state == "open" and day >= c.expires_day:
            c.state = "expired"
    issued = 0
    for g in list(guilds.GUILDS.values()):
        if g.state != "active":
            continue
        open_n = len(_open_for_guild(g.guild_id))
        if open_n >= CONTRACTS_PER_GUILD:
            continue
        rng = random.Random((seed ^ (hash(g.guild_id) & 0xFFFFFFFF) ^ day) & 0xFFFFFFFF)
        while open_n < CONTRACTS_PER_GUILD:
            kind_roll = rng.random()
            c = (_gen_courier(g, rng, day) if kind_roll < 0.35 else
                 _gen_supply(g, rng, day))
            if c is None:
                # fall back to the other kind if pool empty
                c = _gen_supply(g, rng, day) if kind_roll < 0.35 else _gen_courier(g, rng, day)
            if c is None:
                break
            CONTRACTS[c.contract_id] = c
            open_n += 1
            issued += 1
    return issued


# ---------------------------------------------------------------------------
# Player interactions
# ---------------------------------------------------------------------------

def open_contracts_at(guild_id: str) -> list:
    """Open contracts the player can pick up at this hall."""
    return [c for c in CONTRACTS.values()
            if c.guild_id == guild_id and c.state == "open"]


def accepted_by_player(player) -> list:
    ids = list(getattr(player, "active_contracts", []) or [])
    out = []
    for cid in ids:
        c = CONTRACTS.get(cid)
        if c is not None:
            out.append(c)
    return out


def turn_in_hall_for(c: Contract) -> str:
    """Which hall the player must visit to complete this contract."""
    if c.kind == "supply":
        return c.guild_id
    return c.target_guild_id or c.guild_id


def can_accept(player, c: Contract) -> bool:
    if c.state != "open":
        return False
    if c.contract_id in (getattr(player, "active_contracts", []) or []):
        return False
    return True


def accept(player, c: Contract) -> bool:
    if not can_accept(player, c):
        return False
    c.state = "accepted"
    c.accepted_by = "player"
    lst = getattr(player, "active_contracts", None)
    if lst is None:
        player.active_contracts = []
        lst = player.active_contracts
    lst.append(c.contract_id)
    return True


def _inventory_count(player, item_id: str) -> int:
    inv = getattr(player, "inventory", None) or {}
    return int(inv.get(item_id, 0))


def _consume(player, item_id: str, count: int) -> bool:
    inv = getattr(player, "inventory", None)
    if inv is None or inv.get(item_id, 0) < count:
        return False
    inv[item_id] -= count
    if inv[item_id] <= 0:
        inv.pop(item_id, None)
    return True


def can_turn_in_here(player, c: Contract, current_hall_gid: str) -> bool:
    if c.state != "accepted":
        return False
    if turn_in_hall_for(c) != current_hall_gid:
        return False
    return _inventory_count(player, c.item_id) >= c.count


def turn_in(player, c: Contract, current_hall_gid: str) -> bool:
    if not can_turn_in_here(player, c, current_hall_gid):
        return False
    if not _consume(player, c.item_id, c.count):
        return False
    player.money = int(getattr(player, "money", 0)) + c.reward_gold
    _add_rep(player, c.guild_id, c.reward_rep)
    if c.kind == "courier" and c.target_guild_id:
        _add_rep(player, c.target_guild_id, 1)
    c.state = "completed"
    lst = getattr(player, "active_contracts", None)
    if lst and c.contract_id in lst:
        lst.remove(c.contract_id)
    return True


def abandon(player, c: Contract) -> None:
    """Drop an accepted contract back to open. Small rep hit."""
    if c.state != "accepted":
        return
    c.state = "open"
    c.accepted_by = ""
    lst = getattr(player, "active_contracts", None) or []
    if c.contract_id in lst:
        lst.remove(c.contract_id)
    _add_rep(player, c.guild_id, -1)


def _add_rep(player, gid: str, delta: int) -> None:
    rep = getattr(player, "guild_rep", None)
    if rep is None:
        player.guild_rep = {}
        rep = player.guild_rep
    rep[gid] = int(rep.get(gid, 0)) + int(delta)


def player_rep(player, gid: str) -> int:
    rep = getattr(player, "guild_rep", None) or {}
    return int(rep.get(gid, 0))


# Reputation tiers (loose narrative labels; gameplay perks come later).
REP_TIERS = [
    (0,   "Outsider"),
    (5,   "Acquainted"),
    (15,  "Trusted"),
    (40,  "Friend"),
    (90,  "Patron"),
    (180, "Honored"),
]


def rep_label(rep: int) -> str:
    out = REP_TIERS[0][1]
    for floor, name in REP_TIERS:
        if rep >= floor:
            out = name
    return out
