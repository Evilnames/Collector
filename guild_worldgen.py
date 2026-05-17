"""Guild seeding.

Strategy: lazy attachment. As outposts are created (or loaded), each one is
routed to the chapter that owns its (region, industry). Missing chapters and
missing guilds are created on demand. `seed_guilds(world)` simply walks the
current outpost registry and runs the attachment for every entry — safe to
call repeatedly, idempotent.

This avoids needing a separate up-front biome-distribution pass: guilds
materialize wherever the world actually places matching outposts.
"""

from collections import deque

import guilds
from guilds import (
    Guild, GuildChapter, GUILDS, CHAPTERS, HistoricalYear,
    INDUSTRY_DISPLAY, PRICE_HISTORY_LEN, industry_for_outpost,
    seed_npc_holders,
)


# Module-level — set by ``seed_guilds`` so ``_find_or_create_guild`` can pull
# pre-baked history without changing its signature (called from many sites).
_PLAN_GUILD_HISTORIES: dict = {}


# (bx, by) → guild_id. Rebuilt every call to `place_guild_halls`, which is
# idempotent and re-runs on save load via `seed_guilds`.
GUILD_HALL_AT: dict = {}


def guild_at_hall(bx: int, by: int):
    return GUILD_HALL_AT.get((bx, by))


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------

def seed_guilds(world) -> None:
    """Charter regional guilds and attach every outpost to its chapter.

    Two passes:
      1. **Eager region seeding** — for every Region the world knows about,
         charter one guild per industry that fits the region's biome (using
         `BIOME_OUTPOST_TYPES` → industry mapping). Guarantees the Market tab
         has tickers even in a fresh game with no outposts loaded yet.
      2. **Outpost attachment** — bind every existing outpost to its
         matching chapter (creates the chapter if missing).

    Idempotent — `_find_or_create_guild` and `attach_outpost` both no-op when
    state already exists, so the day-rollover hook can call this every day.
    """
    global _PLAN_GUILD_HISTORIES
    plan = getattr(world, "plan", None)
    _PLAN_GUILD_HISTORIES = getattr(plan, "guild_histories", {}) or {}
    _eager_seed_from_regions()
    from outposts import OUTPOSTS
    for op in list(OUTPOSTS.values()):
        attach_outpost(op)
    # Backfill NPC traders for any guild that doesn't have them yet
    # (e.g. v6 saves chartered before the NPC ledger landed).
    for gid in list(GUILDS.keys()):
        seed_npc_holders(gid)
    # Physical world presence (Phase 8).
    place_guild_halls(world)
    place_guild_flags(world)


_BIOME_GROUP_TO_HALL = {
    "forest":         "GUILD_HALL_FOREST",
    "boreal":         "GUILD_HALL_FOREST",
    "jungle":         "GUILD_HALL_JUNGLE",
    "tropical":       "GUILD_HALL_JUNGLE",
    "mediterranean":  "GUILD_HALL_MEDITERRANEAN",
    "coastal":        "GUILD_HALL_MEDITERRANEAN",
    "levant":         "GUILD_HALL_MEDITERRANEAN",
    "east_asian":     "GUILD_HALL_EAST_ASIAN",
    "south_asian":    "GUILD_HALL_EAST_ASIAN",
    "desert":         "GUILD_HALL_DESERT",
    "steppe":         "GUILD_HALL_DESERT",
    "wasteland":      "GUILD_HALL_DESERT",
}

_INDUSTRY_TO_FLAG = {
    "wine":     "GUILD_FLAG_WINE",
    "coffee":   "GUILD_FLAG_COFFEE",
    "tea":      "GUILD_FLAG_TEA",
    "spirits":  "GUILD_FLAG_SPIRITS",
    "brew":     "GUILD_FLAG_SPIRITS",
    "forge":    "GUILD_FLAG_FORGE",
    "textile":  "GUILD_FLAG_TEXTILE",
    "mining":   "GUILD_FLAG_MINING",
}


def _hall_block_for(biome_group: str) -> int:
    import blocks as _blocks
    name = _BIOME_GROUP_TO_HALL.get(biome_group)
    if name is None:
        return _blocks.GUILD_HALL_BLOCK
    return getattr(_blocks, name, _blocks.GUILD_HALL_BLOCK)


def _flag_block_for(industry: str) -> int:
    import blocks as _blocks
    name = _INDUSTRY_TO_FLAG.get(industry)
    if name is None:
        return _blocks.GUILD_FLAG_BLOCK
    return getattr(_blocks, name, _blocks.GUILD_FLAG_BLOCK)


_HALL_SPACING = 3   # blocks between adjacent guild halls along the capital row


def place_guild_halls(world) -> None:
    """Plant one Hall per guild in each regional capital, biome-flavored.

    Halls are walked left-to-right starting at `center_bx + 4`, spaced
    `_HALL_SPACING` apart. Guilds are sorted by industry so the same guild
    always lands on the same slot (idempotent across save/load).
    """
    from blocks import GUILD_HALL_VARIANTS, AIR
    from towns import TOWNS, REGIONS
    GUILD_HALL_AT.clear()
    for region in REGIONS.values():
        capital = TOWNS.get(region.capital_town_id)
        if capital is None:
            continue
        region_guilds = sorted(
            (g for g in GUILDS.values()
             if g.home_region_id == region.region_id and g.state != "bankrupt"),
            key=lambda g: g.industry,
        )
        if not region_guilds:
            continue
        hall_block = _hall_block_for(getattr(region, "biome_group", ""))
        for slot, g in enumerate(region_guilds):
            bx = capital.center_bx + 4 + slot * _HALL_SPACING
            sy = _surface_y(world, bx)
            if sy is None:
                continue
            hall_y = sy - 1
            try:
                current = world.get_block(bx, hall_y)
                if current in GUILD_HALL_VARIANTS:
                    GUILD_HALL_AT[(bx, hall_y)] = g.guild_id
                    continue
                if current == AIR:
                    world.set_block(bx, hall_y, hall_block)
                    GUILD_HALL_AT[(bx, hall_y)] = g.guild_id
            except Exception:
                continue


def place_guild_flags(world) -> None:
    """Plant industry-tinted banners above each guild-owned outpost."""
    from blocks import GUILD_FLAG_VARIANTS, AIR
    from outposts import OUTPOSTS
    for op in OUTPOSTS.values():
        industry = industry_for_outpost(op)
        if industry is None:
            continue
        bx = op.center_bx + 2
        sy = _surface_y(world, bx)
        if sy is None:
            continue
        flag_y = sy - 2
        flag_block = _flag_block_for(industry)
        try:
            current = world.get_bg_block(bx, flag_y)
            if current in GUILD_FLAG_VARIANTS:
                continue
            if current == AIR:
                world.set_bg_block(bx, flag_y, flag_block)
        except Exception:
            continue


def _surface_y(world, bx: int):
    """Return the y of the topmost solid block at bx (one below the placement row)."""
    try:
        return world.surface_height(bx)
    except Exception:
        return None


def _eager_seed_from_regions() -> None:
    """Charter one guild per (region, industry) inferred from region biome."""
    from towns import TOWNS, REGIONS
    from outposts import BIOME_OUTPOST_TYPES
    from guilds import OUTPOST_TYPE_TO_INDUSTRY
    if not REGIONS or not TOWNS:
        return
    # Index towns by region so we can sample a representative biome per region.
    towns_by_region: dict = {}
    for t in TOWNS.values():
        towns_by_region.setdefault(t.region_id, []).append(t)
    for region in REGIONS.values():
        region_towns = towns_by_region.get(region.region_id, [])
        if not region_towns:
            continue
        biomes = {t.biome for t in region_towns if getattr(t, "biome", None)}
        industries = set()
        for biome in biomes:
            for outpost_type in BIOME_OUTPOST_TYPES.get(biome, ()):
                industry = OUTPOST_TYPE_TO_INDUSTRY.get(outpost_type)
                if industry is not None:
                    industries.add(industry)
        for industry in industries:
            _find_or_create_guild(region.region_id, industry)
            # _find_or_create_guild handles the Guild; the chapter is built
            # lazily here so the Board Room can show its (empty) outpost list.
            from guilds import chapter_for
            if chapter_for(region.region_id, industry) is None:
                _create_chapter(region.region_id, region.capital_town_id, industry)


def attach_outpost(op) -> None:
    """Route a single outpost to its chapter, creating guild + chapter if new."""
    industry = industry_for_outpost(op)
    if industry is None:
        return
    region_id, capital_town_id = _region_for_outpost(op)
    if region_id is None:
        return

    chapter = _find_chapter(region_id, industry)
    if chapter is None:
        chapter = _create_chapter(region_id, capital_town_id, industry)
    if op.outpost_id not in chapter.outpost_ids:
        chapter.outpost_ids.append(op.outpost_id)
        _bump_initial_price(GUILDS[chapter.guild_id])


def detach_outpost(op_id: int) -> None:
    """Remove an outpost id from whichever chapter currently holds it."""
    for ch in CHAPTERS.values():
        if op_id in ch.outpost_ids:
            ch.outpost_ids.remove(op_id)
            return


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _region_for_outpost(op) -> tuple:
    """Return (region_id, capital_town_id) for an outpost, or (None, None)."""
    from towns import TOWNS, REGIONS
    if not TOWNS:
        return (None, None)
    nearest = min(TOWNS.values(), key=lambda t: abs(t.center_bx - op.center_bx))
    region = REGIONS.get(nearest.region_id)
    if region is None:
        return (None, None)
    return (region.region_id, region.capital_town_id)


def _find_chapter(region_id: int, industry: str):
    for ch in CHAPTERS.values():
        if ch.region_id != region_id:
            continue
        g = GUILDS.get(ch.guild_id)
        if g is not None and g.industry == industry:
            return ch
    return None


def _create_chapter(region_id: int, capital_town_id: int, industry: str) -> GuildChapter:
    guild = _find_or_create_guild(region_id, industry)
    chapter_id = f"CH_{industry}_{region_id}"
    ch = GuildChapter(
        chapter_id      = chapter_id,
        guild_id        = guild.guild_id,
        region_id       = region_id,
        capital_town_id = capital_town_id,
    )
    CHAPTERS[chapter_id] = ch
    if chapter_id not in guild.chapter_ids:
        guild.chapter_ids.append(chapter_id)
    return ch


def _find_or_create_guild(region_id: int, industry: str) -> Guild:
    # In Phase 1, one guild per (industry, region). Cross-region rollups (a
    # single Vintners' Guild spanning several regions) are a Phase 3 concern.
    guild_id = f"G_{industry}_{region_id}"
    g = GUILDS.get(guild_id)
    if g is not None:
        return g
    history = _PLAN_GUILD_HISTORIES.get(f"{region_id}|{industry}")
    if history is not None:
        g = _guild_from_history(guild_id, region_id, industry, history)
    else:
        g = Guild(
            guild_id       = guild_id,
            name           = _make_guild_name(region_id, industry),
            industry       = industry,
            home_region_id = region_id,
            share_price    = 10.0,
            treasury       = 200,
            price_history  = deque([10.0] * PRICE_HISTORY_LEN, maxlen=PRICE_HISTORY_LEN),
        )
    GUILDS[guild_id] = g
    seed_npc_holders(guild_id)
    return g


def _guild_from_history(guild_id: str, region_id: int, industry: str,
                        history: dict) -> Guild:
    """Build a Guild whose starting state is seeded by centuries of worldgen
    history. Long-term ledger is preserved on the Guild for the History UI;
    the 30-day rolling ``price_history`` is initialized from the tail of the
    ledger so the Market tab sparkline looks alive on day one."""
    ledger_dicts = history.get("ledger", []) or []
    # Convert dict rows back into HistoricalYear records.
    ledger = []
    for row in ledger_dicts:
        try:
            ledger.append(HistoricalYear(**row))
        except TypeError:
            # Forward-compat: ignore extra/missing keys.
            ledger.append(HistoricalYear(
                year        = row.get("year", 0),
                treasury    = row.get("treasury", 0),
                share_price = row.get("share_price", 10.0),
                income      = row.get("income", 0),
                members     = row.get("members", 1),
                event       = row.get("event", ""),
            ))
    final_price    = float(history.get("final_share_price", 10.0))
    final_treasury = int(history.get("final_treasury", 200))
    final_members  = int(history.get("final_members", 1))
    quality        = float(history.get("quality", 1.0))
    recent_avg     = float(history.get("recent_avg_income", 0.0))
    ledger_len     = len(ledger)
    # Tail of the ledger seeds the 30-day rolling sparkline.
    tail_prices = [row.share_price for row in ledger[-PRICE_HISTORY_LEN:]] or [final_price]
    while len(tail_prices) < PRICE_HISTORY_LEN:
        tail_prices.insert(0, tail_prices[0])
    # Outstanding shares: bigger, older, better-run guilds floated more shares
    # over the centuries. 400 base + members + maturity.
    share_count = max(200, int(400 + final_members * 120 + min(ledger_len, 400) * 1.2))
    # Dividend rate: mature, profitable, high-quality guilds pay more. Volatile
    # young guilds reinvest. Range ~1%..6%.
    dividend_rate = max(0.005, min(0.06,
        0.015 + 0.025 * max(0.0, (quality - 0.9))
              + 0.010 * (min(ledger_len, 300) / 300.0)
              + 0.010 * (1.0 if final_treasury > 5000 else final_treasury / 5000.0)))
    # Profit EMA is per-day; recent_avg is per-year → /365.
    profit_ema = recent_avg / 365.0
    last_week_profit = int(round(recent_avg / 52.0))
    # Charter price_mult — slightly above/below 1 by quality so industry events
    # land on a non-flat base.
    price_mult = round(0.9 + 0.2 * max(0.0, min(1.0, (quality - 0.75) / 0.55)), 3)
    # Starting state: if the late ledger logged a crash event in the last ~30
    # years, the guild boots in "distressed" so players see the consequence on
    # day one. Defunct (kingdom collapsed) → bankrupt unless rescued.
    _crash_tags = {"sacked", "plague", "collapse", "earthquake",
                   "civil_war", "founder_extinct"}
    state = "active"
    days_negative = 0
    if int(history.get("defunct_year", -1)) != -1:
        state = "bankrupt"
    else:
        for row in ledger[-30:]:
            if row.event in _crash_tags:
                state = "distressed"
                days_negative = 5   # already partway to bankruptcy clock
                break
    return Guild(
        guild_id          = guild_id,
        name              = _make_guild_name(region_id, industry),
        industry          = industry,
        home_region_id    = region_id,
        share_count       = share_count,
        share_price       = final_price,
        treasury          = final_treasury,
        price_history     = deque(tail_prices, maxlen=PRICE_HISTORY_LEN),
        dividend_rate     = round(dividend_rate, 4),
        last_week_profit  = last_week_profit,
        profit_ema        = round(profit_ema, 2),
        charter           = {"price_mult": price_mult,
                             "expansion_appetite": 0.5,
                             "quality_bias": round(quality - 1.0, 3)},
        state             = state,
        days_negative     = days_negative,
        founded_year      = int(history.get("founded_year", 0)),
        founder_name      = history.get("founder_name", ""),
        founder_house     = history.get("founder_house", ""),
        historical_ledger = ledger,
        legendary_events  = list(history.get("legendary_events", [])),
    )


def _make_guild_name(region_id: int, industry: str) -> str:
    from towns import REGIONS
    region = REGIONS.get(region_id)
    region_name = region.name if region else f"Region {region_id}"
    return f"{region_name} {INDUSTRY_DISPLAY.get(industry, industry.title())}"


def _bump_initial_price(g: Guild) -> None:
    """Nudge starting share price up as more outposts come under the guild."""
    outpost_count = sum(len(CHAPTERS[cid].outpost_ids) for cid in g.chapter_ids if cid in CHAPTERS)
    target = 8.0 + outpost_count * 1.5
    # Only adjust until the simulation tick takes over (price history all-equal).
    if len(set(g.price_history)) <= 1:
        g.share_price = target
        g.price_history = deque([target] * PRICE_HISTORY_LEN, maxlen=PRICE_HISTORY_LEN)
