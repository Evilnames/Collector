"""Guild pricing policies — light wrapper used by cities.py.

Kept separate from `guilds.py` so call sites in cities.py (and elsewhere) can
import only this lightweight module without dragging the whole guild data
model and risking circular imports.

Phase 2: chapter price multipliers + player ownership discount/bonus.
"""

from guilds import (
    INDUSTRY_WINE, INDUSTRY_COFFEE, INDUSTRY_HERB, INDUSTRY_TEA,
    INDUSTRY_SPIRITS, INDUSTRY_BREW, INDUSTRY_POTTERY, INDUSTRY_TEXTILE,
    INDUSTRY_CHEESE, INDUSTRY_FISHING, INDUSTRY_SALT, INDUSTRY_OLIVE,
    INDUSTRY_SPICE, INDUSTRY_FORGE, INDUSTRY_TIMBER, INDUSTRY_FUR,
    INDUSTRY_APIARY,
    chapter_for, GUILDS,
)

# ---------------------------------------------------------------------------
# Item → industry mapping (best-effort; items not listed bypass guild pricing)
# ---------------------------------------------------------------------------

ITEM_TO_INDUSTRY = {
    # Wine
    "red_wine":          INDUSTRY_WINE,
    "white_wine":        INDUSTRY_WINE,
    "red_wine_fine":     INDUSTRY_WINE,
    "white_wine_fine":   INDUSTRY_WINE,
    "red_wine_reserve":  INDUSTRY_WINE,
    "white_wine_reserve": INDUSTRY_WINE,
    # Coffee
    "drip_coffee":       INDUSTRY_COFFEE,
    "espresso":          INDUSTRY_COFFEE,
    "pour_over":         INDUSTRY_COFFEE,
    "drip_coffee_fine":  INDUSTRY_COFFEE,
    "espresso_fine":     INDUSTRY_COFFEE,
    "pour_over_fine":    INDUSTRY_COFFEE,
    # Spirits
    "whiskey":           INDUSTRY_SPIRITS,
    "whiskey_aged":      INDUSTRY_SPIRITS,
    "whiskey_reserve":   INDUSTRY_SPIRITS,
    "bourbon":           INDUSTRY_SPIRITS,
    "bourbon_aged":      INDUSTRY_SPIRITS,
    "bourbon_reserve":   INDUSTRY_SPIRITS,
    # Pottery
    "clay_cooking_pot":      INDUSTRY_POTTERY,
    "clay_cooking_pot_fine": INDUSTRY_POTTERY,
    "pottery_vase":          INDUSTRY_POTTERY,
    "pottery_vase_fine":     INDUSTRY_POTTERY,
    "wine_amphora":          INDUSTRY_POTTERY,
    "wine_amphora_fine":     INDUSTRY_POTTERY,
    # Apiary / mead
    "honey_jar":  INDUSTRY_APIARY,
    "beeswax":    INDUSTRY_APIARY,
    "mead":       INDUSTRY_APIARY,
    "mead_fine":  INDUSTRY_APIARY,
    # Cheese
    "milk": INDUSTRY_CHEESE,
    # Timber
    "lumber": INDUSTRY_TIMBER,
    # Textile
    "wool": INDUSTRY_TEXTILE,
}


def industry_for_item(item_id):
    return ITEM_TO_INDUSTRY.get(item_id)


# ---------------------------------------------------------------------------
# Pricing
# ---------------------------------------------------------------------------

# Player ownership discount caps at 25% — even a 100% subsidiary stake shouldn't
# turn NPC trades into free gold.
PLAYER_DISCOUNT_CAP    = 0.25
PLAYER_DISCOUNT_SLOPE  = 0.5
PLAYER_DISCOUNT_FLOOR  = 0.05  # ignored below 5% ownership


def _player_pct_adjustment(g, side: str) -> float:
    """Return a multiplier that biases price in the player's favor.

    `side`:
      - "sell" → player is selling to an NPC, so a *higher* multiplier helps
        the player (NPC pays more).
      - "buy"  → player is buying from an NPC, so a *lower* multiplier helps
        the player (item costs less).
    """
    pct = g.player_pct()
    if pct < PLAYER_DISCOUNT_FLOOR:
        return 1.0
    bonus = min(PLAYER_DISCOUNT_CAP, pct * PLAYER_DISCOUNT_SLOPE)
    return (1.0 + bonus) if side == "sell" else (1.0 - bonus)


def apply_chapter_pricing(item_id, base_price: int, region_id, side: str = "sell") -> int:
    """Return a guild-modified price for `item_id` traded in `region_id`.

    Falls back to `base_price` whenever no chapter covers the item or the
    guild isn't active. Result is clamped to >= 1.
    """
    if region_id is None or not base_price:
        return base_price
    industry = ITEM_TO_INDUSTRY.get(item_id)
    if industry is None:
        return base_price
    chapter = chapter_for(region_id, industry)
    if chapter is None:
        return base_price
    g = GUILDS.get(chapter.guild_id)
    if g is None or g.state != "active":
        return base_price
    charter_mult = float(g.charter.get("price_mult", 1.0))
    mult = chapter.local_price_mult * charter_mult * _player_pct_adjustment(g, side)
    return max(1, int(round(base_price * mult)))


# ---------------------------------------------------------------------------
# Ownership thresholds (used by UI gating in Board Room tab)
# ---------------------------------------------------------------------------

OWNERSHIP_FINANCIALS = 0.10
OWNERSHIP_BOARD_SEAT = 0.25
OWNERSHIP_MAJORITY   = 0.51
OWNERSHIP_SUBSIDIARY = 1.00


def player_tier(g) -> str:
    pct = g.player_pct()
    if pct >= OWNERSHIP_SUBSIDIARY:
        return "subsidiary"
    if pct >= OWNERSHIP_MAJORITY:
        return "majority"
    if pct >= OWNERSHIP_BOARD_SEAT:
        return "board"
    if pct >= OWNERSHIP_FINANCIALS:
        return "informed"
    return "minority"
