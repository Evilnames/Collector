"""Guild data model.

Pure data — no pygame, no world references at import time. Outposts and towns
are linked by id; lookups happen against the runtime registries in outposts.py
and towns.py.

A Guild covers (industry, home_region). It owns one or more GuildChapter
records, one per region the guild operates in. Each chapter owns the outposts
of the matching industry within that region.

Phase 1 surface: data classes, the registry, the industry mapping, and a few
small helpers used by stock_market / guild_worldgen / UI.
"""

from collections import deque
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Industry tags
# ---------------------------------------------------------------------------

INDUSTRY_WINE     = "wine"
INDUSTRY_COFFEE   = "coffee"
INDUSTRY_HERB     = "herb"
INDUSTRY_TEA      = "tea"
INDUSTRY_SPIRITS  = "spirits"
INDUSTRY_BREW     = "brew"
INDUSTRY_POTTERY  = "pottery"
INDUSTRY_TEXTILE  = "textile"
INDUSTRY_CHEESE   = "cheese"
INDUSTRY_FISHING  = "fishing"
INDUSTRY_SALT     = "salt"
INDUSTRY_OLIVE    = "olive"
INDUSTRY_SPICE    = "spice"
INDUSTRY_FORGE    = "forge"
INDUSTRY_TIMBER   = "timber"
INDUSTRY_FUR      = "fur"
INDUSTRY_APIARY   = "apiary"
INDUSTRY_MINING   = "mining"

INDUSTRY_DISPLAY = {
    INDUSTRY_WINE:    "Vintners",
    INDUSTRY_COFFEE:  "Coffee Houses",
    INDUSTRY_HERB:    "Apothecaries",
    INDUSTRY_TEA:     "Tea Masters",
    INDUSTRY_SPIRITS: "Distillers",
    INDUSTRY_BREW:    "Brewers",
    INDUSTRY_POTTERY: "Potters",
    INDUSTRY_TEXTILE: "Weavers",
    INDUSTRY_CHEESE:  "Cheesemakers",
    INDUSTRY_FISHING: "Fishmongers",
    INDUSTRY_SALT:    "Salters",
    INDUSTRY_OLIVE:   "Olive Press Guild",
    INDUSTRY_SPICE:   "Spice Merchants",
    INDUSTRY_FORGE:   "Forge Guild",
    INDUSTRY_TIMBER:  "Timberwrights",
    INDUSTRY_FUR:     "Furriers",
    INDUSTRY_APIARY:  "Beekeepers",
    INDUSTRY_MINING:  "Miners",
}

# Map outpost_type → industry. Military / nomadic outposts are omitted.
OUTPOST_TYPE_TO_INDUSTRY = {
    "wine_estate":           INDUSTRY_WINE,
    "hillside_vineyard":     INDUSTRY_WINE,
    "coffee_plantation":     INDUSTRY_COFFEE,
    "herb_monastery":        INDUSTRY_HERB,
    "jungle_herbalist":      INDUSTRY_HERB,
    "bog_apothecary":        INDUSTRY_HERB,
    "swamp_alchemist":       INDUSTRY_HERB,
    "alpine_monastery":      INDUSTRY_HERB,
    "fungal_grove":          INDUSTRY_HERB,
    "tea_house":             INDUSTRY_TEA,
    "boreal_distillery":     INDUSTRY_SPIRITS,
    "spirit_distillery":     INDUSTRY_SPIRITS,
    "craft_brewery":         INDUSTRY_BREW,
    "hill_taproom":          INDUSTRY_BREW,
    "pottery_workshop":      INDUSTRY_POTTERY,
    "textile_guild":         INDUSTRY_TEXTILE,
    "silk_pavilion":         INDUSTRY_TEXTILE,
    "reed_weaver":           INDUSTRY_TEXTILE,
    "cheese_cave":           INDUSTRY_CHEESE,
    "fishing_outpost":       INDUSTRY_FISHING,
    "pearl_diving_camp":     INDUSTRY_FISHING,
    "canoe_trading_post":    INDUSTRY_FISHING,
    "salt_works":            INDUSTRY_SALT,
    "coastal_saltworks":     INDUSTRY_SALT,
    "olive_press":           INDUSTRY_OLIVE,
    "spice_market":          INDUSTRY_SPICE,
    "incense_lodge":         INDUSTRY_SPICE,
    "canyon_forge":          INDUSTRY_FORGE,
    "desert_glassworks":     INDUSTRY_FORGE,
    "sculpture_atelier":     INDUSTRY_FORGE,
    "timber_camp":           INDUSTRY_TIMBER,
    "trapper_post":          INDUSTRY_FUR,
    "apiary":                INDUSTRY_APIARY,
    "deep_mine_camp":        INDUSTRY_MINING,
    "quarry_camp":           INDUSTRY_MINING,
    "prospector_post":       INDUSTRY_MINING,
    "lapidary_atelier":      INDUSTRY_MINING,
    "coal_pit":              INDUSTRY_MINING,
    "marble_quarry":         INDUSTRY_MINING,
    "dwarven_hold":          INDUSTRY_MINING,
    "sulfur_pit":            INDUSTRY_MINING,
    "gold_panning_camp":     INDUSTRY_MINING,
}


def industry_for_outpost(op) -> Optional[str]:
    return OUTPOST_TYPE_TO_INDUSTRY.get(getattr(op, "outpost_type", None))


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

PRICE_HISTORY_LEN = 30


@dataclass
class HistoricalYear:
    """One year of a guild's pre-game history. Compact enough to hold ~500
    rows per guild without bloat. ``event`` is a short tag for notable shifts
    ("plague", "war_loss", "monopoly", "founder_died", "boom", "schism")
    and renders as a tooltip on the long-term sparkline."""
    year:        int
    treasury:    int
    share_price: float
    income:      int   = 0
    members:     int   = 1     # chapters/outposts under the guild
    event:       str   = ""


@dataclass
class GuildChapter:
    chapter_id:           str
    guild_id:             str
    region_id:            int
    capital_town_id:      int
    outpost_ids:          list  = field(default_factory=list)
    shuttered_outpost_ids: list = field(default_factory=list)
    pending_expansions:   int   = 0
    local_treasury:       int   = 0
    local_price_mult:     float = 1.0

    def active_outpost_count(self) -> int:
        return len(self.outpost_ids) - len(self.shuttered_outpost_ids) + self.pending_expansions


@dataclass
class Guild:
    guild_id:       str
    name:           str
    industry:       str
    home_region_id: int
    treasury:       int            = 0
    share_count:    int            = 1000
    share_price:    float          = 10.0
    price_history:  deque          = field(default_factory=lambda: deque(maxlen=PRICE_HISTORY_LEN))
    dividend_rate:  float          = 0.02     # fraction of profit paid out per week
    last_week_profit: int          = 0
    profit_ema:     float          = 0.0      # exponential moving average of daily profit
    reputation:     dict           = field(default_factory=dict)   # town_id → int
    charter:        dict           = field(default_factory=lambda: {
        "price_mult":          1.0,
        "expansion_appetite":  0.5,
        "quality_bias":        0.0,
    })
    chapter_ids:    list           = field(default_factory=list)
    state:          str            = "active"   # active | distressed | bankrupt | subsidiary_of:<id>
    days_negative:  int            = 0
    active_effects: list           = field(default_factory=list)   # [{event_key, mult, days_left, note, source}]
    rivalry_target: Optional[str]  = None        # gid currently targeted for sabotage
    # Worldgen historical backstory: populated by worldgen.history.economy during
    # world creation and shown in the Stock Exchange History tab so the player can
    # judge centuries of track record before buying shares. Empty for player-founded
    # guilds and for guilds in worlds saved before the feature shipped.
    founded_year:       int        = 0
    founder_name:       str        = ""
    founder_house:      str        = ""        # dynasty house, e.g. "House Voss"
    historical_ledger:  list       = field(default_factory=list)   # list[HistoricalYear]
    legendary_events:   list       = field(default_factory=list)   # list[str]

    def player_shares(self) -> int:
        return sum(h.shares for h in SHARE_HOLDINGS
                   if h.owner_id == "player" and h.guild_id == self.guild_id)

    def player_pct(self) -> float:
        if self.share_count <= 0:
            return 0.0
        return self.player_shares() / self.share_count

    def market_cap(self) -> int:
        return int(self.share_price * self.share_count)


@dataclass
class ShareHolding:
    owner_id:      str       # "player" or NPC id string
    guild_id:      str
    shares:        int
    avg_buy_price: float


# ---------------------------------------------------------------------------
# Registries (populated by guild_worldgen.seed_guilds and the save loader)
# ---------------------------------------------------------------------------

GUILDS:          dict[str, Guild]        = {}
CHAPTERS:        dict[str, GuildChapter] = {}
SHARE_HOLDINGS:  list                    = []   # list[ShareHolding]


def reset_registries() -> None:
    GUILDS.clear()
    CHAPTERS.clear()
    SHARE_HOLDINGS.clear()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def chapter_for_outpost(op_id: int) -> Optional[GuildChapter]:
    """Return the chapter that owns this outpost, or None if unaffiliated."""
    for ch in CHAPTERS.values():
        if op_id in ch.outpost_ids:
            return ch
    return None


def guild_for_outpost(op_id: int) -> Optional[Guild]:
    ch = chapter_for_outpost(op_id)
    if ch is None:
        return None
    return GUILDS.get(ch.guild_id)


def chapter_for(region_id: int, industry: str) -> Optional[GuildChapter]:
    """Return the chapter operating `industry` in `region_id`, or None."""
    for ch in CHAPTERS.values():
        if ch.region_id != region_id:
            continue
        g = GUILDS.get(ch.guild_id)
        if g is not None and g.industry == industry:
            return ch
    return None


def guild_by_id(guild_id: str) -> Optional[Guild]:
    return GUILDS.get(guild_id)


def active_guilds() -> list:
    return [g for g in GUILDS.values() if g.state == "active"]


def player_holding(guild_id: str) -> Optional[ShareHolding]:
    for h in SHARE_HOLDINGS:
        if h.owner_id == "player" and h.guild_id == guild_id:
            return h
    return None


def holdings_for(guild_id: str) -> list:
    return [h for h in SHARE_HOLDINGS if h.guild_id == guild_id]


def npc_holdings_for(guild_id: str) -> list:
    return [h for h in SHARE_HOLDINGS
            if h.guild_id == guild_id and h.owner_id != "player"]


def seed_npc_holders(guild_id: str, rng=None) -> None:
    """Distribute the unowned public float across 3–5 anonymous NPC traders.

    Idempotent: if NPC holders already exist for this guild, returns without
    re-seeding. Player-held shares are preserved.
    """
    import random as _random
    g = GUILDS.get(guild_id)
    if g is None:
        return
    existing_npc = npc_holdings_for(guild_id)
    if existing_npc:
        return
    held_by_player = g.player_shares()
    public_shares = g.share_count - held_by_player
    if public_shares <= 0:
        return
    if rng is None:
        rng = _random.Random(hash((guild_id, "npc-seed")) & 0xFFFFFFFF)
    n_traders = rng.randint(3, 5)
    # Random partition of public_shares across n_traders.
    weights = [rng.random() + 0.1 for _ in range(n_traders)]
    total_w = sum(weights)
    allocated = 0
    for i in range(n_traders):
        if i == n_traders - 1:
            shares = public_shares - allocated
        else:
            shares = max(1, int(public_shares * weights[i] / total_w))
            shares = min(shares, public_shares - allocated - (n_traders - i - 1))
        allocated += shares
        if shares <= 0:
            continue
        trader_id = f"npc_{guild_id}_{i}"
        SHARE_HOLDINGS.append(ShareHolding(
            owner_id=trader_id, guild_id=guild_id,
            shares=shares, avg_buy_price=g.share_price))


def buy_shares(guild_id: str, shares: int, gold: int) -> tuple[bool, int, str]:
    """Player buys `shares` of `guild_id`.

    Returns (success, gold_spent, message). Caller is responsible for deducting
    the gold from the player on success.
    """
    g = GUILDS.get(guild_id)
    if g is None or g.state != "active":
        return False, 0, "Guild not available."
    if shares <= 0:
        return False, 0, "Invalid share count."
    cost = int(round(g.share_price * shares))
    if cost > gold:
        return False, 0, "Not enough gold."
    # Cap at outstanding shares not already held by the player.
    held_by_player = g.player_shares()
    if held_by_player + shares > g.share_count:
        shares = g.share_count - held_by_player
        if shares <= 0:
            return False, 0, "All shares already owned."
        cost = int(round(g.share_price * shares))
    h = player_holding(guild_id)
    if h is None:
        SHARE_HOLDINGS.append(ShareHolding(
            owner_id="player", guild_id=guild_id,
            shares=shares, avg_buy_price=g.share_price))
    else:
        total_cost = h.avg_buy_price * h.shares + g.share_price * shares
        h.shares += shares
        h.avg_buy_price = total_cost / h.shares
    g.treasury += cost
    return True, cost, f"Bought {shares} share(s) at {g.share_price:.2f}g."


FOUNDING_FEE          = 500     # gold cost to charter a player guild
FOUNDING_FEE_PER_SHARE = 0.05    # additional fee scales with share count


def found_player_guild(name: str, industry: str, region_id: int,
                       capital_town_id: int, share_count: int,
                       ipo_price: float, public_float_pct: float,
                       player_gold: int) -> tuple:
    """Charter a brand-new player-founded guild and run its IPO.

    Returns (success, message, cost, guild_id). Caller deducts `cost` from
    player.money on success.
    """
    if share_count < 100 or share_count > 10000:
        return (False, "Share count must be between 100 and 10000.", 0, None)
    if ipo_price < 1.0:
        return (False, "IPO price must be at least 1g.", 0, None)
    public_float_pct = max(0.0, min(1.0, public_float_pct))

    fee = int(FOUNDING_FEE + share_count * FOUNDING_FEE_PER_SHARE)
    if player_gold < fee:
        return (False, f"Founding fee is {fee}g.", 0, None)

    # Build unique guild id even when a region+industry guild already exists.
    base_id = f"G_{industry}_{region_id}"
    guild_id = base_id
    suffix = 2
    while guild_id in GUILDS:
        guild_id = f"{base_id}_F{suffix}"
        suffix += 1

    from collections import deque
    public_shares = int(round(share_count * public_float_pct))
    player_shares = share_count - public_shares
    g = Guild(
        guild_id        = guild_id,
        name            = name.strip() or f"Player {industry.title()} Co.",
        industry        = industry,
        home_region_id  = region_id,
        share_count     = share_count,
        share_price     = ipo_price,
        price_history   = deque([ipo_price] * PRICE_HISTORY_LEN, maxlen=PRICE_HISTORY_LEN),
        treasury        = int(round(ipo_price * public_shares)),
    )
    GUILDS[guild_id] = g

    chapter_id = f"CH_{industry}_{region_id}_F{suffix}"
    ch = GuildChapter(
        chapter_id      = chapter_id,
        guild_id        = guild_id,
        region_id       = region_id,
        capital_town_id = capital_town_id,
    )
    CHAPTERS[chapter_id] = ch
    g.chapter_ids.append(chapter_id)

    if player_shares > 0:
        SHARE_HOLDINGS.append(ShareHolding(
            owner_id="player", guild_id=guild_id,
            shares=player_shares, avg_buy_price=ipo_price))
    seed_npc_holders(guild_id)
    return (True, f"Chartered {g.name}: you hold {player_shares} shares.",
            fee, guild_id)


def buyback_shares(guild_id: str, shares: int) -> tuple[bool, int, str]:
    """Guild treasury repurchases `shares` from the public float.

    Reduces `share_count`, which mechanically lifts the player's ownership %
    and the share price. Requires majority ownership (caller verifies).
    """
    g = GUILDS.get(guild_id)
    if g is None:
        return False, 0, "Guild not found."
    cost = int(round(g.share_price * shares))
    if cost > g.treasury:
        return False, 0, f"Treasury holds only {g.treasury}g."
    held = g.player_shares()
    public_outstanding = g.share_count - held
    if shares > public_outstanding:
        return False, 0, "Not enough public float to buy back."
    g.treasury -= cost
    g.share_count -= shares
    g.share_price = g.share_price * (1.0 + shares / max(1, g.share_count))
    return True, cost, f"Bought back {shares} share(s); price rose to {g.share_price:.2f}g."


def issue_shares(guild_id: str, shares: int) -> tuple[bool, int, str]:
    """Dilute existing shareholders by issuing new shares at the current price.

    Adds proceeds to guild treasury. Player's percentage drops; price softens
    slightly to reflect dilution.
    """
    g = GUILDS.get(guild_id)
    if g is None:
        return False, 0, "Guild not found."
    if shares <= 0:
        return False, 0, "Invalid share count."
    proceeds = int(round(g.share_price * shares))
    g.share_count += shares
    g.treasury    += proceeds
    g.share_price  = g.share_price * (1.0 - 0.5 * shares / max(1, g.share_count))
    return True, proceeds, f"Issued {shares} new share(s); treasury +{proceeds}g."


SHORT_MARGIN_FRAC      = 0.5     # collateral required = position × current price × this
SHORT_CARRY_RATE_DAILY = 0.001    # 0.1% of position value charged daily


def player_short(guild_id: str) -> Optional[ShareHolding]:
    for h in SHARE_HOLDINGS:
        if h.owner_id == "player_short" and h.guild_id == guild_id:
            return h
    return None


def open_short(guild_id: str, shares: int, gold: int) -> tuple[bool, int, str]:
    """Open or add to a short position. Requires collateral (margin)."""
    g = GUILDS.get(guild_id)
    if g is None or g.state != "active":
        return False, 0, "Guild not available for shorts."
    if shares <= 0:
        return False, 0, "Invalid share count."
    margin = int(round(g.share_price * shares * SHORT_MARGIN_FRAC))
    if margin > gold:
        return False, 0, f"Need {margin}g margin."
    existing = player_short(guild_id)
    if existing is None:
        SHARE_HOLDINGS.append(ShareHolding(
            owner_id="player_short", guild_id=guild_id,
            shares=shares, avg_buy_price=g.share_price))
    else:
        avg_cost = existing.avg_buy_price * existing.shares + g.share_price * shares
        existing.shares += shares
        existing.avg_buy_price = avg_cost / existing.shares
    return True, margin, f"Shorted {shares} share(s) at {g.share_price:.2f}g (margin {margin}g)."


def close_short(guild_id: str, shares: int = 0) -> tuple[bool, int, str]:
    """Close some/all of a short position. Returns net gold delta (+ release margin)."""
    g = GUILDS.get(guild_id)
    if g is None:
        return False, 0, "Guild not found."
    h = player_short(guild_id)
    if h is None:
        return False, 0, "No short position to close."
    if shares <= 0 or shares > h.shares:
        shares = h.shares
    pnl    = int(round((h.avg_buy_price - g.share_price) * shares))
    margin = int(round(h.avg_buy_price * shares * SHORT_MARGIN_FRAC))
    h.shares -= shares
    if h.shares <= 0:
        SHARE_HOLDINGS.remove(h)
    return True, margin + pnl, f"Closed {shares} short(s); P/L {pnl:+}g (margin {margin}g released)."


def short_carry_cost(g: "Guild", h: "ShareHolding") -> int:
    return int(round(g.share_price * h.shares * SHORT_CARRY_RATE_DAILY))


# ---------------------------------------------------------------------------
# Loans / margin
# ---------------------------------------------------------------------------

LOAN_INTEREST_DAILY = 0.0005       # 0.05%/day ≈ 1.5%/month
LOAN_LTV_CAP        = 0.30          # max debt = 30% of portfolio market value
MARGIN_CALL_LTV     = 0.50          # if debt > 50% of portfolio → force liquidate


def portfolio_value(only_active: bool = True) -> int:
    total = 0
    for h in SHARE_HOLDINGS:
        if h.owner_id != "player":
            continue
        g = GUILDS.get(h.guild_id)
        if g is None or (only_active and g.state != "active"):
            continue
        total += int(round(g.share_price * h.shares))
    return total


def borrow(player, amount: int) -> tuple[bool, int, str]:
    if amount <= 0:
        return False, 0, "Invalid amount."
    new_debt = getattr(player, "guild_debt", 0) + amount
    if new_debt > int(portfolio_value() * LOAN_LTV_CAP):
        return False, 0, "Borrow exceeds 30% loan-to-value cap."
    player.guild_debt = new_debt
    player.money = getattr(player, "money", 0) + amount
    return True, amount, f"Borrowed {amount}g (total debt {new_debt}g)."


def repay(player, amount: int) -> tuple[bool, int, str]:
    debt = getattr(player, "guild_debt", 0)
    if debt <= 0:
        return False, 0, "No outstanding debt."
    amount = min(amount, debt, getattr(player, "money", 0))
    if amount <= 0:
        return False, 0, "No funds to repay."
    player.guild_debt = debt - amount
    player.money     -= amount
    return True, amount, f"Repaid {amount}g (remaining debt {player.guild_debt}g)."


def sell_shares(guild_id: str, shares: int) -> tuple[bool, int, str]:
    """Player sells `shares`. Returns (success, gold_gained, message)."""
    g = GUILDS.get(guild_id)
    if g is None:
        return False, 0, "Guild not available."
    h = player_holding(guild_id)
    if h is None or h.shares <= 0:
        return False, 0, "No shares held."
    if shares <= 0:
        return False, 0, "Invalid share count."
    shares = min(shares, h.shares)
    proceeds = int(round(g.share_price * shares))
    h.shares -= shares
    if h.shares <= 0:
        SHARE_HOLDINGS.remove(h)
    # Treasury pays out share proceeds; clamp at 0 to keep the model simple.
    g.treasury = max(0, g.treasury - proceeds)
    return True, proceeds, f"Sold {shares} share(s) at {g.share_price:.2f}g."
