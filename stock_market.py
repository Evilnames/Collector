"""Stock-market simulation for guilds.

Phase 1: daily revenue + share-price recompute + weekly dividend payout.
Bankruptcy / expansion / competition are deferred to later phases.

The daily tick is intentionally cheap — at most a handful of arithmetic ops per
chapter — so it's safe to call every in-game day from world.update_time.
"""

import random

import guilds
from guilds import GUILDS, CHAPTERS, SHARE_HOLDINGS, ShareHolding

# ---------------------------------------------------------------------------
# Tuning
# ---------------------------------------------------------------------------

UPKEEP_PER_OUTPOST   = 4     # gold/day overhead per outpost
REVENUE_PER_OUTPOST  = 18    # baseline gold/day per outpost before need-pressure
NEED_PENALTY_MULT    = 0.5   # how strongly unsatisfied needs throttle revenue

PROFIT_EMA_ALPHA     = 0.15
PRICE_LERP           = 0.25
PRICE_NOISE_FRAC     = 0.02
PRICE_FLOOR          = 0.10
PRICE_BASE_TARGET    = 10.0   # neutral target if a guild has no signals yet

DIVIDEND_PERIOD_DAYS = 7
WEEKLY_PERIOD_DAYS   = 7
BANKRUPTCY_DAYS      = 30
DISTRESSED_DAYS      = 14

EXPANSION_COST_PER_OUTPOST  = 220
EXPANSION_REVENUE_PER_GHOST = 12   # synthetic ghost outpost contribution before a real one spawns

SHUTTER_TREASURY_FLOOR = -120

NPC_TRADE_CHANCE       = 0.08    # per holder per day
NPC_TRADE_LOT_FRAC     = 0.10    # holder trades up to 10% of position per event
NPC_MOMENTUM_THRESHOLD = 0.02    # forecast must be >2% off price to trigger

# ---------------------------------------------------------------------------
# Daily tick
# ---------------------------------------------------------------------------

def tick_market(world, player=None) -> None:
    """Run a single daily market step.

    - Per chapter: compute revenue from owned outposts, deduct upkeep, roll up
      to the guild treasury.
    - Recompute each active guild's share price.
    - Track days_negative for bankruptcy.
    - Every DIVIDEND_PERIOD_DAYS, pay dividends to all shareholders (including
      the player if `player` is provided).
    """
    if not GUILDS:
        return
    from outposts import OUTPOSTS

    day = getattr(world, "day_count", 0)
    rng = random.Random((getattr(world, "seed", 0) ^ day) & 0xFFFFFFFF)

    daily_profit_by_guild = {gid: 0 for gid in GUILDS}

    from industry_events import effect_multiplier
    for ch in CHAPTERS.values():
        g = GUILDS.get(ch.guild_id)
        if g is None or g.state != "active":
            continue
        revenue = 0
        upkeep  = 0
        shuttered = set(ch.shuttered_outpost_ids)
        for op_id in ch.outpost_ids:
            if op_id in shuttered:
                continue
            op = OUTPOSTS.get(op_id)
            if op is None:
                continue
            # Outpost revenue is throttled by how well its needs are met.
            satisfaction = _need_satisfaction(op)
            revenue += int(REVENUE_PER_OUTPOST * (1.0 - NEED_PENALTY_MULT * (1.0 - satisfaction)))
            upkeep  += UPKEEP_PER_OUTPOST
        # Ghost expansions contribute synthetic revenue until the world spawns
        # the real outposts at their slot positions.
        revenue += ch.pending_expansions * EXPANSION_REVENUE_PER_GHOST
        # Industry events / sabotage stack on revenue (never on upkeep).
        revenue = int(revenue * effect_multiplier(g))
        profit = revenue - upkeep
        ch.local_treasury += profit
        daily_profit_by_guild[g.guild_id] += profit

    for gid, profit in daily_profit_by_guild.items():
        g = GUILDS[gid]
        if g.state != "active":
            continue
        g.treasury += profit
        g.profit_ema = (1.0 - PROFIT_EMA_ALPHA) * g.profit_ema + PROFIT_EMA_ALPHA * profit
        if g.treasury < 0:
            g.days_negative += 1
        else:
            g.days_negative = 0
        if g.days_negative >= BANKRUPTCY_DAYS:
            _go_bankrupt(g)
        elif g.days_negative >= DISTRESSED_DAYS:
            g.state = "distressed"
        _recompute_price(g, rng)

    _npc_trade_tick(rng)
    from industry_events import daily_decay
    daily_decay()
    # Phase 7 daily: short carry + loan interest + bond maturity
    _accrue_short_carry(player)
    _accrue_loan_interest(player)
    if player is not None:
        from bonds import daily_maturity_check, weekly_coupons
        daily_maturity_check(day, player)
        weekly_coupons(day, player)

    if day > 0 and day % DIVIDEND_PERIOD_DAYS == 0:
        _pay_dividends(player)
    if day > 0 and day % WEEKLY_PERIOD_DAYS == 0:
        _resolve_competition(rng)
        _expansion_tick(rng)
        _shutter_tick(rng)
        _resolve_mergers()
        from industry_events import roll_event, roll_rivalries, roll_tournament_day
        roll_event(rng, day)
        roll_rivalries(rng, day)
        roll_tournament_day(rng, day)
        from bonds import issue_periodic_bonds
        issue_periodic_bonds(day)
        _margin_call_check(player)


def _need_satisfaction(op) -> float:
    needs = getattr(op, "needs", None) or {}
    if not needs:
        return 1.0
    total = 0.0
    for entry in needs.values():
        req = entry.get("required", 0) if isinstance(entry, dict) else 0
        sup = entry.get("supplied", 0) if isinstance(entry, dict) else 0
        if req <= 0:
            continue
        total += min(1.0, sup / req)
    return total / max(1, len(needs))


def _recompute_price(g, rng) -> None:
    # Profit trend → unitless score roughly in [-1, +1]
    profit_trend = max(-1.0, min(1.0, g.profit_ema / max(20.0, REVENUE_PER_OUTPOST)))
    chapter_count = len(g.chapter_ids)
    outpost_count = sum(len(CHAPTERS[cid].outpost_ids) for cid in g.chapter_ids if cid in CHAPTERS)
    scale = max(1.0, outpost_count * 0.8 + chapter_count * 0.4)
    # Historical quality bias persists from worldgen — keeps centuries-old
    # blue-chips trading above flash-in-the-pan guilds with the same outpost
    # count. Range roughly ±0.3 → ±30% equilibrium price.
    quality_bias = float(g.charter.get("quality_bias", 0.0))
    target = PRICE_BASE_TARGET * scale * (1.0 + 0.4 * profit_trend + quality_bias)
    sentiment = 1.0 + rng.uniform(-0.03, 0.03)
    target *= sentiment

    new_price = g.share_price + (target - g.share_price) * PRICE_LERP
    new_price += rng.gauss(0.0, PRICE_NOISE_FRAC * max(g.share_price, 1.0))
    g.share_price = max(PRICE_FLOOR, new_price)
    g.price_history.append(round(g.share_price, 3))


# ---------------------------------------------------------------------------
# Weekly dividend
# ---------------------------------------------------------------------------

def _npc_trade_tick(rng) -> None:
    """Anonymous NPC traders nudge holdings each day based on simple momentum.

    Effect on the simulation:
      - NPCs buying drains shares from the public float (no real gold moves).
      - NPCs selling adds to the float; player can buy them up.
      - Each trade tilts share_price slightly toward the trade direction,
        modelling order-flow pressure on top of the existing price recompute.
    """
    if not SHARE_HOLDINGS:
        return
    # Snapshot — we mutate SHARE_HOLDINGS inside the loop.
    for h in list(SHARE_HOLDINGS):
        if h.owner_id == "player":
            continue
        if rng.random() > NPC_TRADE_CHANCE:
            continue
        g = GUILDS.get(h.guild_id)
        if g is None or g.state != "active":
            continue
        fc = forecast_target(g)
        edge = (fc - g.share_price) / max(g.share_price, 0.01)
        if abs(edge) < NPC_MOMENTUM_THRESHOLD:
            continue
        lot = max(1, int(h.shares * NPC_TRADE_LOT_FRAC))
        if edge > 0:
            # Bullish — accumulate from the float (if any unowned shares exist).
            total_held = sum(x.shares for x in SHARE_HOLDINGS if x.guild_id == g.guild_id)
            float_left = max(0, g.share_count - total_held)
            buy_qty = min(lot, float_left)
            if buy_qty > 0:
                h.shares += buy_qty
                g.share_price *= 1.0 + 0.005 * (buy_qty / max(1, g.share_count))
        else:
            # Bearish — sell back to the float.
            sell_qty = min(lot, h.shares)
            if sell_qty > 0:
                h.shares -= sell_qty
                g.share_price *= 1.0 - 0.005 * (sell_qty / max(1, g.share_count))
                if h.shares <= 0:
                    SHARE_HOLDINGS.remove(h)


def _resolve_mergers() -> None:
    """If a single holder owns >50% of two active guilds in the same industry,
    the smaller guild becomes a subsidiary of the larger one.

    Subsidiary effect: state becomes "subsidiary_of:<parent_id>", treasury
    rolls up to the parent, dividends pause, but outposts stay attached so
    the parent keeps benefiting from their revenue contribution.
    """
    # Build {owner_id: [(pct, guild_id)]} for guilds where owner has >50%
    dominant: dict = {}
    for h in SHARE_HOLDINGS:
        g = GUILDS.get(h.guild_id)
        if g is None or g.state != "active":
            continue
        pct = h.shares / max(1, g.share_count)
        if pct > 0.50:
            dominant.setdefault(h.owner_id, []).append((pct, g))

    for owner_id, controlled in dominant.items():
        if len(controlled) < 2:
            continue
        # Group by industry and pick the largest as the parent.
        by_industry: dict = {}
        for pct, g in controlled:
            by_industry.setdefault(g.industry, []).append(g)
        for industry, group in by_industry.items():
            if len(group) < 2:
                continue
            group.sort(key=lambda gg: -gg.market_cap())
            parent = group[0]
            for child in group[1:]:
                if child.state.startswith("subsidiary_of:"):
                    continue
                child.state = f"subsidiary_of:{parent.guild_id}"
                child.dividend_rate = 0.0
                parent.treasury += child.treasury
                child.treasury = 0


def _accrue_short_carry(player) -> None:
    if player is None:
        return
    from guilds import short_carry_cost
    for h in list(SHARE_HOLDINGS):
        if h.owner_id != "player_short" or h.shares <= 0:
            continue
        g = GUILDS.get(h.guild_id)
        if g is None:
            continue
        cost = short_carry_cost(g, h)
        if cost <= 0:
            continue
        player.money = max(0, getattr(player, "money", 0) - cost)


def _accrue_loan_interest(player) -> None:
    if player is None:
        return
    from guilds import LOAN_INTEREST_DAILY
    debt = getattr(player, "guild_debt", 0)
    if debt <= 0:
        return
    interest = int(round(debt * LOAN_INTEREST_DAILY))
    if interest <= 0:
        return
    player.guild_debt = debt + interest


def _margin_call_check(player) -> None:
    if player is None:
        return
    from guilds import portfolio_value, MARGIN_CALL_LTV, GUILDS as _G, SHARE_HOLDINGS as _H
    debt = getattr(player, "guild_debt", 0)
    if debt <= 0:
        return
    pv = portfolio_value()
    if pv == 0:
        # No collateral left — wipe debt against cash (force).
        cash = getattr(player, "money", 0)
        taken = min(debt, cash)
        player.money -= taken
        player.guild_debt = debt - taken
        return
    if debt / max(1, pv) <= MARGIN_CALL_LTV:
        return
    # Liquidate the most valuable holding to cover.
    holdings = [(h, _G.get(h.guild_id)) for h in _H if h.owner_id == "player"]
    holdings = [(h, g) for (h, g) in holdings if g is not None and g.state == "active"]
    holdings.sort(key=lambda hg: -(hg[1].share_price * hg[0].shares))
    for h, g in holdings:
        if player.guild_debt <= 0:
            return
        needed_gold = player.guild_debt
        sell_qty = min(h.shares, max(1, int(needed_gold // max(g.share_price, 0.01)) + 1))
        proceeds = int(round(g.share_price * sell_qty))
        h.shares -= sell_qty
        if h.shares <= 0:
            _H.remove(h)
        # Proceeds repay the loan directly (no cash hits player.money).
        player.guild_debt = max(0, player.guild_debt - proceeds)


def _go_bankrupt(g) -> None:
    """Escalate a distressed guild to bankrupt. Outposts go neutral."""
    from guild_worldgen import detach_outpost
    g.state = "bankrupt"
    g.dividend_rate = 0.0
    g.charter["price_mult"] = 1.0
    for cid in list(g.chapter_ids):
        ch = CHAPTERS.get(cid)
        if ch is None:
            continue
        # Release every outpost back to neutral (auction in a later phase).
        for op_id in list(ch.outpost_ids):
            detach_outpost(op_id)
        ch.shuttered_outpost_ids.clear()
        ch.pending_expansions = 0
        ch.local_price_mult = 1.0


def _resolve_competition(rng) -> None:
    """Reallocate weekly revenue between competing guilds in the same (industry, region).

    Single-chapter guilds are unaffected. When two or more chapters share a
    region+industry, treasury+outpost share determines who keeps how much of
    the week's accumulated profit_ema.
    """
    buckets: dict = {}
    for ch in CHAPTERS.values():
        g = GUILDS.get(ch.guild_id)
        if g is None or g.state != "active":
            continue
        buckets.setdefault((g.industry, ch.region_id), []).append((g, ch))
    for competitors in buckets.values():
        if len(competitors) < 2:
            continue
        weights = []
        for g, ch in competitors:
            w = max(0.1, g.treasury * 0.001 + ch.active_outpost_count())
            weights.append(w)
        total = sum(weights)
        # Pool the contested fraction of each guild's profit_ema and re-split it.
        share_pool = sum(g.profit_ema * 0.25 for g, _ in competitors)
        for (g, _), w in zip(competitors, weights):
            g.profit_ema = g.profit_ema * 0.75 + share_pool * (w / total)


def _expansion_tick(rng) -> None:
    """Treasury-rich guilds with appetite incubate a new ghost outpost."""
    for g in GUILDS.values():
        if g.state != "active":
            continue
        if g.treasury < EXPANSION_COST_PER_OUTPOST:
            continue
        appetite = float(g.charter.get("expansion_appetite", 0.5))
        if rng.random() > appetite:
            continue
        # Pick the chapter with the most existing outposts (likely strongest region).
        chapters = [CHAPTERS[cid] for cid in g.chapter_ids if cid in CHAPTERS]
        if not chapters:
            continue
        ch = max(chapters, key=lambda c: c.active_outpost_count())
        g.treasury -= EXPANSION_COST_PER_OUTPOST
        ch.pending_expansions += 1


def _shutter_tick(rng) -> None:
    """Distressed chapters mothball their worst outposts until the guild recovers."""
    from outposts import OUTPOSTS
    for g in GUILDS.values():
        if g.state == "active":
            # Reactivate shuttered outposts once the treasury recovers.
            if g.treasury > 0:
                for cid in g.chapter_ids:
                    ch = CHAPTERS.get(cid)
                    if ch and ch.shuttered_outpost_ids:
                        ch.shuttered_outpost_ids.clear()
            continue
        if g.state != "distressed":
            continue
        if g.treasury > SHUTTER_TREASURY_FLOOR:
            continue
        for cid in g.chapter_ids:
            ch = CHAPTERS.get(cid)
            if ch is None or len(ch.shuttered_outpost_ids) >= len(ch.outpost_ids):
                continue
            # Pick the outpost with the worst need satisfaction.
            live = [op_id for op_id in ch.outpost_ids if op_id not in ch.shuttered_outpost_ids]
            if not live:
                continue
            worst = min(live, key=lambda oid: _need_satisfaction(OUTPOSTS[oid])
                                              if oid in OUTPOSTS else 1.0)
            ch.shuttered_outpost_ids.append(worst)
            break  # one shutter per guild per week


# ---------------------------------------------------------------------------
# Insider forecast (research T4)
# ---------------------------------------------------------------------------

def forecast_target(g) -> float:
    """Best-effort next-day price target — used by the insider info UI."""
    chapter_count = len(g.chapter_ids)
    outpost_count = sum(
        max(0, len(CHAPTERS[cid].outpost_ids) - len(CHAPTERS[cid].shuttered_outpost_ids))
        + CHAPTERS[cid].pending_expansions
        for cid in g.chapter_ids if cid in CHAPTERS
    )
    scale = max(1.0, outpost_count * 0.8 + chapter_count * 0.4)
    profit_trend = max(-1.0, min(1.0, g.profit_ema / max(20.0, REVENUE_PER_OUTPOST)))
    target = PRICE_BASE_TARGET * scale * (1.0 + 0.4 * profit_trend)
    return g.share_price + (target - g.share_price) * PRICE_LERP


# ---------------------------------------------------------------------------
# Weekly dividend
# ---------------------------------------------------------------------------

def _pay_dividends(player) -> None:
    for g in GUILDS.values():
        if g.state != "active":
            continue
        period_profit = g.profit_ema * DIVIDEND_PERIOD_DAYS
        if period_profit <= 0:
            g.last_week_profit = 0
            continue
        payout_pool = int(period_profit * g.dividend_rate)
        if payout_pool <= 0 or g.share_count <= 0:
            g.last_week_profit = int(period_profit)
            continue
        per_share = payout_pool / g.share_count
        for h in SHARE_HOLDINGS:
            if h.guild_id != g.guild_id or h.shares <= 0:
                continue
            payout = int(round(per_share * h.shares))
            if payout <= 0:
                continue
            g.treasury = max(0, g.treasury - payout)
            if h.owner_id == "player" and player is not None:
                player.money = getattr(player, "money", 0) + payout
        g.last_week_profit = int(period_profit)
